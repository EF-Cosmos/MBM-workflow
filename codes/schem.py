import bpy
import math
import bmesh
from .model import create_mesh,add_mesh_to_collection,get_or_create_material,set_uv
import re
from . import dependency_manager
from .classification_files.block_type import liquid,exclude
import numpy as np
import os
from .register import create_or_clear_collection,register_blocks,registered_blocks
from .pointcloud import (BIOME_COLOR, ensure_geometry_nodes_group,
                         attach_schem_modifier, build_point_cloud_mesh)
import pickle
import json

# 缓存路径常量（基于插件包自身位置定位，兼容 legacy addons/ 与 5.x extensions 安装方式）
_ADDON_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMCACHE_DIR = os.environ.get("MBM_SCHEMCACHE_DIR") or os.path.join(_ADDON_ROOT, "schemcache")
VAR_CACHE_PATH = os.path.join(SCHEMCACHE_DIR, "var.json")

# 使用依赖管理器导入
amulet = dependency_manager.amulet
litemapy = dependency_manager.litemapy


def get_mc_version_config():
    """
    获取当前配置的 Minecraft 版本
    返回: (platform, version_tuple)
    """
    try:
        scene = bpy.context.scene
        platform = scene.mc_platform
        version_tuple = (
            scene.mc_version_major,
            scene.mc_version_minor,
            scene.mc_version_patch
        )
        return platform, version_tuple
    except Exception:
        # 默认版本
        return "java", (1, 21, 9)


#用于删除[]的部分
def remove_brackets(input_string):
    start = input_string.find('[')
    if start == -1:
        return input_string
    end = input_string.find(']', start)
    return input_string[:start] if end == -1 else input_string[:start] + input_string[end + 1:]


_MISSING = object()


def _selection_for_chunks(chunks):
    """把 [(min), (max)] 坐标范围转成 amulet SelectionBox（max 闭区间 → 半开区间）"""
    from amulet.api.selection import SelectionBox
    min_coords, max_coords = chunks[0], chunks[1]
    return SelectionBox(
        (min_coords[0], min_coords[1], min_coords[2]),
        (max_coords[0] + 1, max_coords[1] + 1, max_coords[2] + 1),
    )


def _collect_blocks_fast(level, dimension, min_coords, max_coords, platform, version):
    """chunk 级 numpy 批量读取，返回 (顶点数组, id字符串列表, waterlogged数组)。

    每个 chunk 只翻译一次调色板，再用布尔查找表 + argwhere 批量提取，
    彻底绕开逐格 get_block 的 Python 调用开销。
    amulet API 不符时抛异常，由调用方回退逐格路径。
    """
    translate = _make_translator(level, platform, version)
    verts_parts = []
    ids_parts = []
    wl_parts = []
    for chunk, slices, box in level.get_chunk_slice_box(
            dimension, _selection_for_chunks((min_coords, max_coords))):
        arr = np.asarray(chunk.blocks[slices])
        palette_blocks = chunk.block_palette.blocks
        n = len(palette_blocks)
        id_lut = np.empty(n, dtype=object)
        keep_lut = np.zeros(n, dtype=bool)
        wl_lut = np.zeros(n, dtype=np.int32)
        for p, block in enumerate(palette_blocks):
            id_str, base_name = translate(block)
            if id_str is not None and base_name not in exclude:
                id_lut[p] = id_str
                keep_lut[p] = True
                wl_lut[p] = 1 if block.extra_blocks else 0
        mask = keep_lut[arr]
        if not mask.any():
            continue
        rel = np.argwhere(mask)
        world = rel + np.array((box.min_x, box.min_y, box.min_z))
        verts_parts.append(np.stack([
            world[:, 0] - min_coords[0],
            -(world[:, 2] - min_coords[2]),
            world[:, 1] - min_coords[1],
        ], axis=1).astype(np.int64))
        picked = arr[mask]
        ids_parts.append(id_lut[picked])
        wl_parts.append(wl_lut[picked])
    if not verts_parts:
        return np.zeros((0, 3), dtype=np.int64), [], np.zeros(0, dtype=np.int32)
    return (np.concatenate(verts_parts),
            list(np.concatenate(ids_parts)),
            np.concatenate(wl_parts))


def collect_blocks(level, dimension, min_coords, max_coords, platform, version):
    """读取选区方块，优先 chunk 级批量路径，失败时回退逐格路径。"""
    try:
        return _collect_blocks_fast(level, dimension, min_coords, max_coords,
                                    platform, version)
    except Exception as e:
        print(f"[MBM] chunk 级批量读取不可用，回退逐格路径: {e}")
    # 逐格回退路径
    translate = _make_translator(level, platform, version)
    vertices = []
    ids = []
    waterlogged = []
    for x in range(min_coords[0], max_coords[0] + 1):
        for y in range(min_coords[1], max_coords[1] + 1):
            for z in range(min_coords[2], max_coords[2] + 1):
                try:
                    block = level.get_block(x, y, z, dimension)
                except Exception:
                    continue
                if isinstance(block, amulet.api.block.Block):
                    id_str, base_name = translate(block)
                    if id_str is not None and base_name not in exclude:
                        vertices.append((x - min_coords[0], -(z - min_coords[2]), y - min_coords[1]))
                        ids.append(id_str)
                        waterlogged.append(1 if block.extra_blocks else 0)
    return vertices, ids, waterlogged


def _make_translator(level, platform, version):
    """构建带缓存的通用方块 -> 版本化字符串翻译器。

    schematic 百万格中唯一方块种类通常只有几十种，按 str(block) 缓存后
    from_universal 的调用次数从"每格一次"降为"每个唯一方块一次"。
    翻译失败缓存为 (None, None)，与逐格 try/except 跳过的原行为一致。
    返回 translate(block) -> (完整字符串, 去括号基础名)。
    """
    version_block = level.translation_manager.get_version(platform, version).block
    cache = {}

    def translate(block):
        key = str(block)
        result = cache.get(key, _MISSING)
        if result is _MISSING:
            try:
                id_str = str(version_block.from_universal(block)[0]).replace('"', '')
                result = (id_str, remove_brackets(id_str))
            except Exception:
                result = (None, None)
            cache[key] = result
        return result

    return translate


def schem(level, chunks, cached, filename="schem", position=(0, 0, 0)):
    # 获取配置的版本
    platform, version = get_mc_version_config()

    # 获取最小和最大坐标
    min_coords = chunks[0]
    max_coords = chunks[1]

    # 创建一个新的集合
    collection_name="Blocks"
    create_or_clear_collection(collection_name)
    collection =bpy.data.collections.get(collection_name)
    #导入几何节点
    ensure_geometry_nodes_group(collection_name)

    if not cached:
        # chunk 级批量读取（翻译器内部也带缓存），失败自动回退逐格路径
        vertices, ids, waterlogged = collect_blocks(
            level, "main", min_coords, max_coords, platform, version)
        id_map=register_blocks(list(set(ids)))
    else:
        IDCachePath = os.path.join(SCHEMCACHE_DIR, "id_map.pkl")
        with open(IDCachePath, 'rb') as f:
            vertices,ids,id_map = pickle.load(f)
        id_map=register_blocks(id_map)

    # 创建点云对象并批量写入顶点与属性（foreach_set 替代逐顶点循环）
    obj = build_point_cloud_mesh(filename, vertices, ids, id_map, waterlogged)
    attach_schem_modifier(obj, collection_name)
    return obj
    

def schem_chunk(level, chunks, x_list, chunk_index=0, filename="schem", position=(0, 0, 0)):
    # 获取配置的版本
    platform, version = get_mc_version_config()

    # 获取最小和最大坐标
    min_coords = chunks[0]
    max_coords = chunks[1]

    # 创建顶点和顶点索引
    vertices = []
    ids = []  # 存储顶点id
    # 翻译器内部带缓存：唯一方块只翻译一次（get_version_block 逐格翻译开销大）
    translate = _make_translator(level, platform, version)

    # 遍历指定区块的 X 范围
    x_range = x_list[chunk_index]
    for x in range(x_range[0], x_range[1]):
        for y in range(min_coords[1], max_coords[1] + 1):
            for z in range(min_coords[2], max_coords[2] + 1):
                try:
                    # 获取坐标处的方块
                    block = level.get_block(x, y, z, "main")
                except Exception as e:
                    print(f"[MBM] 区块处理出错 ({x},{y},{z}): {e}")
                    continue
                if isinstance(block, amulet.api.block.Block):
                    id_str, base_name = translate(block)
                    if id_str is not None and base_name not in exclude:
                        vertices.append((x-min_coords[0],-(z-min_coords[2]),y-min_coords[1]))
                        # 将字符串id转换为相应的数字id
                        ids.append(id_str)

    id_map=register_blocks(list(set(ids)))

    IDCachePath = os.path.join(SCHEMCACHE_DIR, f"chunk{chunk_index}.pkl")
    with open(IDCachePath, 'wb') as f:
        pickle.dump((vertices,ids,id_map), f)


def merge_chunks(chunk_count, filename="schem"):
    """读取所有 chunk*.pkl，合并顶点和 id_map，写入 id_map.pkl 供 schem() 的 cached 分支读取"""
    all_vertices = []
    all_ids = []
    merged_id_map = {}

    for i in range(chunk_count):
        chunk_path = os.path.join(SCHEMCACHE_DIR, f"chunk{i}.pkl")
        with open(chunk_path, 'rb') as f:
            vertices, ids, chunk_id_map = pickle.load(f)
        all_vertices.extend(vertices)
        all_ids.extend(ids)
        merged_id_map.update(chunk_id_map)

    # 写入合并后的 id_map.pkl
    id_map_path = os.path.join(SCHEMCACHE_DIR, "id_map.pkl")
    with open(id_map_path, 'wb') as f:
        pickle.dump((all_vertices, all_ids, merged_id_map), f)


def _collect_liquid_fast(level, min_coord, max_coord, platform, version):
    """chunk 级批量读取流体信息。返回 (流体格字典, is_liquid_at(x,y,z) 回调)。

    用稠密布尔数组表达"该格是否流体"，越界/缺失 chunk 一律按非流体处理，
    与逐格路径 get_block 失败时视为暴露的原语义一致。
    """
    translate = _make_translator(level, platform, version)
    shape = (max_coord[0] - min_coord[0] + 1,
             max_coord[1] - min_coord[1] + 1,
             max_coord[2] - min_coord[2] + 1)
    is_liquid = np.zeros(shape, dtype=bool)
    id_str_of = np.empty(shape, dtype=object)
    for chunk, slices, box in level.get_chunk_slice_box(
            "main", _selection_for_chunks((min_coord, max_coord))):
        arr = np.asarray(chunk.blocks[slices])
        palette_blocks = chunk.block_palette.blocks
        n = len(palette_blocks)
        liquid_lut = np.zeros(n, dtype=bool)
        str_lut = np.empty(n, dtype=object)
        for p, block in enumerate(palette_blocks):
            # 含附加方块（如含水）时与原实现一致：取第一个附加方块判定流体
            src = block.extra_blocks[0] if block.extra_blocks else block
            id_str, base_name = translate(src)
            if id_str is not None and base_name in liquid:
                liquid_lut[p] = True
                str_lut[p] = id_str
        liq = liquid_lut[arr]
        if not liq.any():
            continue
        world = np.argwhere(liq) + np.array((box.min_x, box.min_y, box.min_z))
        li = world[:, 0] - min_coord[0]
        lj = world[:, 1] - min_coord[1]
        lk = world[:, 2] - min_coord[2]
        is_liquid[li, lj, lk] = True
        id_str_of[li, lj, lk] = str_lut[arr[liq]]

    liquid_cells = {}
    for i, j, k in np.argwhere(is_liquid):
        liquid_cells[(int(i) + min_coord[0], int(j) + min_coord[1],
                      int(k) + min_coord[2])] = id_str_of[i, j, k]

    def is_liquid_at(x, y, z):
        i, j, k = x - min_coord[0], y - min_coord[1], z - min_coord[2]
        if 0 <= i < shape[0] and 0 <= j < shape[1] and 0 <= k < shape[2]:
            return bool(is_liquid[i, j, k])
        return False

    return liquid_cells, is_liquid_at


def _collect_liquid_cells(level, min_coord, max_coord, platform, version):
    """逐格读取流体信息（批量路径失败时的回退），返回值结构与 _collect_liquid_fast 相同。"""
    translate = _make_translator(level, platform, version)
    base_name_at = {}
    liquid_cells = {}
    for x in range(min_coord[0], max_coord[0] + 1):
        for y in range(min_coord[1], max_coord[1] + 1):
            for z in range(min_coord[2], max_coord[2] + 1):
                try:
                    block = level.get_block(x, y, z, "main")
                except Exception:
                    continue
                if not isinstance(block, amulet.api.block.Block):
                    continue
                # 含附加方块（如含水）时与原实现一致：取第一个附加方块判定流体
                src = block.extra_blocks[0] if block.extra_blocks else block
                id_str, base_name = translate(src)
                if id_str is None:
                    continue
                base_name_at[(x, y, z)] = base_name
                if base_name in liquid:
                    liquid_cells[(x, y, z)] = id_str

    def is_liquid_at(x, y, z):
        return base_name_at.get((x, y, z)) in liquid

    return liquid_cells, is_liquid_at


#流体
def schem_liquid(level, chunks, filename="liquid", position=(0, 0, 0)):
    # 获取配置的版本
    platform, version = get_mc_version_config()

    vertices = []
    faces = []
    direction = []
    texture_list = []
    uv_list = []
    uv_rotation_list = []
    vertices_dict = {}

    water_levels = {
        "minecraft:water[level=0]": 16,
        "minecraft:water[level=1]": 14,
        "minecraft:water[level=2]": 12,
        "minecraft:water[level=3]": 10,
        "minecraft:water[level=4]": 8,
        "minecraft:water[level=5]": 6,
        "minecraft:water[level=6]": 4,
        "minecraft:water[level=7]": 2,
        #流下的水,该级别等于它上方不会流下的水的级别加上8。
        "minecraft:water[level=8]": 16,
        "minecraft:water[level=9]": 16,
        "minecraft:water[level=10]": 16,
        "minecraft:water[level=11]": 16,
        "minecraft:water[level=12]": 16,
        "minecraft:water[level=13]": 16,
        "minecraft:water[level=14]": 16,
        "minecraft:water[level=15]": 16,
    }
    # 定义一个元组，存储六个方向的偏移量，按照 上下北南东西 的顺序排序
    offsets = ((0, 0, -1),  # 东
                (0, 0, 1),  # 西
                (-1, 0, 0),  # 北
                (1, 0, 0),  # 南
                (0, -1, 0),  # 下
                (0, 1, 0))  # 上
    min_coord = chunks[0]  # 最小坐标
    max_coord = chunks[1]  # 最大坐标

    # 第一遍：收集流体格与邻居判定回调（优先 chunk 级批量路径，失败回退逐格）
    try:
        liquid_cells, is_liquid_at = _collect_liquid_fast(level, min_coord, max_coord, platform, version)
    except Exception as e:
        print(f"[MBM] 流体批量读取不可用，回退逐格路径: {e}")
        liquid_cells, is_liquid_at = _collect_liquid_cells(level, min_coord, max_coord, platform, version)

    # 第二遍：仅遍历流体格，邻居查询走回调（批量路径为稠密数组命中，回退路径为字典命中）
    for (x, y, z), id in liquid_cells.items():
        # 判断是否有空气方块（越界/缺失/非流体邻居视为暴露）
        has_air = [not is_liquid_at(x + offset[0], y + offset[1], z + offset[2])
                   for offset in offsets]

        # 将 has_air 中的值按照 东西北南上下 的顺序排列
        has_air = [has_air[2], has_air[3], has_air[0], has_air[1], has_air[5], has_air[4]]
        key=[x-min_coord[0],z-min_coord[2],y-min_coord[1]]
        # 计算哪些面需要生成
        faces_to_generate = [i for i, has_air_face in enumerate(has_air) if has_air_face]

        if faces_to_generate:
            water_level = water_levels.get(id, 0)
            z_offset = water_level / 16 
            key = (key[0], -key[1]-1, key[2])
            for face_index in faces_to_generate:
                if face_index == 5:
                    coords = np.array([
                        (key[0], key[1], key[2]), #0
                        (key[0]+1, key[1], key[2]), #1
                        (key[0]+1, key[1]+1, key[2]), #2
                        (key[0], key[1]+1, key[2]) #3
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('down')
                elif face_index == 0:
                    coords = np.array([
                        (key[0], key[1]+1, key[2]), #3
                        (key[0], key[1]+1, key[2]+z_offset),#7
                        (key[0], key[1], key[2]+z_offset), #4
                        (key[0], key[1], key[2]) #0
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('east') #x-
                elif face_index == 3:
                    coords = np.array([
                        (key[0], key[1], key[2]), #0
                        (key[0], key[1], key[2]+z_offset), #4
                        (key[0]+1, key[1], key[2]+z_offset), #5
                        (key[0]+1, key[1], key[2]) #1
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('north')
                elif face_index == 1:
                    coords = np.array([
                        (key[0]+1, key[1], key[2]), #1
                        (key[0]+1, key[1], key[2]+z_offset), #5
                        (key[0]+1, key[1]+1, key[2]+z_offset), #6
                        (key[0]+1, key[1]+1, key[2]) #2
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('west')
                elif face_index == 2:
                    coords = np.array([
                        (key[0]+1, key[1]+1, key[2]), #2
                        (key[0], key[1]+1, key[2]), #3
                        (key[0], key[1]+1, key[2]+z_offset),#7
                        (key[0]+1, key[1]+1, key[2]+z_offset)#5
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('south')
                elif face_index == 4:
                    coords = np.array([
                        (key[0]+1, key[1]+1, key[2]+z_offset),#6
                        (key[0]+1, key[1], key[2]+z_offset), #5
                        (key[0], key[1], key[2]+z_offset), #4
                        (key[0], key[1]+1, key[2]+z_offset)#7
                    ])
                    for coord in coords:
                        coord = tuple(coord)
                        if coord not in vertices_dict:
                            vertices_dict[coord] = len(vertices_dict)
                            vertices.append(coord)
                    faces.append([
                        vertices_dict[tuple(coords[0])],
                        vertices_dict[tuple(coords[1])],
                        vertices_dict[tuple(coords[2])],
                        vertices_dict[tuple(coords[3])]
                    ])
                    direction.append('up')

    collection = bpy.context.collection
    mesh_name = filename
    mesh = create_mesh(mesh_name)
    obj = add_mesh_to_collection(collection, mesh)
    obj.location = position

    bm = bmesh.new()
    for v in vertices:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    uv_layer = bm.loops.layers.uv.new()  # Add UV layer

    for face_index, f in enumerate(faces):
        verts_list=[]
        for i in f:
            vert =bm.verts[i]
            if vert not in verts_list:
                verts_list.append(vert)
        existing_face = bm.faces.get(verts_list)
        if existing_face is not None:
            face = existing_face
        elif len(verts_list)>2:
            face = bm.faces.new(verts_list)
        else:
            continue

        first_uv = None

        for loop in face.loops:
            vertex = loop.vert
            uv = (vertex.co.y, vertex.co.z) if direction[face_index] in ['west', 'east'] \
                else (vertex.co.x, vertex.co.z) if direction[face_index] in ['north', 'south'] \
                else (vertex.co.x, vertex.co.y)
            
            # 计算第一个顶点的 UV 坐标并记录
            if first_uv is None:
                first_uv = uv
            
            # 计算相对于第一个顶点的 UV 坐标偏移
            relative_uv = (uv[0] - first_uv[0], uv[1] - first_uv[1])
            
            loop[uv_layer].uv = relative_uv



    bm.faces.ensure_lookup_table()

    bm.to_mesh(mesh)
    bm.free()

def _read_point_cloud_arrays(obj):
    """批量读出点云的本地坐标、世界坐标整数键与顶点属性（foreach_get）。"""
    mesh = obj.data
    count = len(mesh.vertices)
    local = np.empty(count * 3, dtype=np.float64)
    mesh.vertices.foreach_get("co", local)
    local = local.reshape(-1, 3)

    world = local
    mw = np.array(obj.matrix_world)
    if not np.allclose(mw, np.eye(4)):
        hom = np.concatenate([local, np.ones((count, 1))], axis=1)
        world = (hom @ mw.T)[:, :3]

    blockids = np.zeros(count, dtype=np.int32)
    waterlogged = np.zeros(count, dtype=np.int32)
    biome = np.full(count * 4, 0.0, dtype=np.float32)
    biome[0::4], biome[1::4], biome[2::4], biome[3::4] = BIOME_COLOR
    blockid_attr = mesh.attributes.get('blockid')
    waterlogged_attr = mesh.attributes.get('waterlogged')
    biome_attr = mesh.attributes.get('biome')
    if blockid_attr is not None:
        blockid_attr.data.foreach_get("value", blockids)
    if waterlogged_attr is not None:
        waterlogged_attr.data.foreach_get("value", waterlogged)
    if biome_attr is not None:
        biome_attr.data.foreach_get("color", biome)
    return local, world, blockids, waterlogged, biome


def _write_separated_mesh(obj, name, local, selection, blockids, waterlogged, biome):
    """按选中的顶点索引子集创建拆分对象（复制修改器、按原始本地坐标重建）。"""
    new_mesh = bpy.data.meshes.new(name=f"{name}_Mesh")
    new_obj = bpy.data.objects.new(name=f"{name}_Object", object_data=new_mesh)
    bpy.context.collection.objects.link(new_obj)

    # 复制修改器
    for modifier in obj.modifiers:
        new_modifier = new_obj.modifiers.new(modifier.name, modifier.type)
        if modifier.type == 'NODES':
            new_modifier.node_group = modifier.node_group

    n = len(selection)
    new_mesh.vertices.add(n)
    new_mesh.vertices.foreach_set(
        "co", local[selection].astype(np.float32).reshape(-1))

    blockid_attr = new_mesh.attributes.new(name='blockid', type="INT", domain="POINT")
    waterlogged_attr = new_mesh.attributes.new(name='waterlogged', type="INT", domain="POINT")
    biome_attr = new_mesh.attributes.new(name='biome', type="FLOAT_COLOR", domain="POINT")
    blockid_attr.data.foreach_set("value", blockids[selection])
    waterlogged_attr.data.foreach_set("value", waterlogged[selection])
    biome_attr.data.foreach_set("color", biome.reshape(-1, 4)[selection].reshape(-1))
    new_mesh.update()

    # 将新物体移动到原始物体的位置
    new_obj.matrix_world = obj.matrix_world


def separate_vertices_by_blockid(obj):
    local, world, blockids, waterlogged, biome = _read_point_cloud_arrays(obj)

    # 按 blockid 分组顶点索引；相同整数坐标的顶点只保留第一个（与原实现一致）
    keys = world.astype(np.int64)
    vertex_dict = {}
    seen = set()
    for idx in range(len(keys)):
        coord = (keys[idx, 0], keys[idx, 1], keys[idx, 2])
        if coord in seen:
            continue
        seen.add(coord)
        vertex_dict.setdefault(int(blockids[idx]), []).append(idx)

    for blockid, selection in vertex_dict.items():
        _write_separated_mesh(obj, f"BlockID_{blockid}", local,
                              np.asarray(selection, dtype=np.int64), blockids, waterlogged, biome)
    # 删除原始对象
    bpy.data.objects.remove(obj, do_unlink=True)

def separate_vertices_by_chunk(obj, chunk_size=16):
    local, world, blockids, waterlogged, biome = _read_point_cloud_arrays(obj)

    # 计算顶点所在 chunk 的坐标，同时沿着正 y 轴平移 1 个单位
    chunk_keys = np.stack([
        np.floor(world[:, 0] / chunk_size) * chunk_size,
        np.floor((world[:, 1] - 1) / chunk_size) * chunk_size,
        np.floor(world[:, 2] / chunk_size) * chunk_size,
    ], axis=1).astype(np.int64)

    vertex_dict = {}
    for idx, key in enumerate(chunk_keys):
        vertex_dict.setdefault((key[0], key[1], key[2]), []).append(idx)

    for coord, selection in vertex_dict.items():
        _write_separated_mesh(obj, f"Chunk_{coord}", local,
                              np.asarray(selection, dtype=np.int64), blockids, waterlogged, biome)

    # 删除原始对象
    bpy.data.objects.remove(obj, do_unlink=True)


def litematic_to_mesh(block_dict, bounds, filename="litematic"):
    """将 litematic 数据转换为点云网格"""
    from .classification_files.block_type import exclude

    min_coords, max_coords = bounds

    # 创建 Blocks 集合并确保几何节点组就绪
    collection_name = "Blocks"
    create_or_clear_collection(collection_name)
    collection = bpy.data.collections.get(collection_name)
    ensure_geometry_nodes_group(collection_name)

    # 构建顶点和 ID 列表
    vertices = []
    ids = []
    waterlogged = []

    for (x, y, z), block_str in block_dict.items():
        # 坐标转换：MC (x, y, z) → Blender (x, -z, y)
        vertices.append((x - min_coords[0], -(z - min_coords[2]), y - min_coords[1]))
        ids.append(block_str)
        waterlogged.append(0)

    # 注册方块
    id_map = register_blocks(list(set(ids)))

    # 创建点云对象并批量写入顶点与属性（foreach_set 替代逐顶点循环）
    obj = build_point_cloud_mesh(filename, vertices, ids, id_map, waterlogged)
    attach_schem_modifier(obj, collection_name)

    return obj
