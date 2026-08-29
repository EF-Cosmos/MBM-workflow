import bpy
import os
import time
import re
import subprocess

import numpy as np

from .block import block
from .functions.get_data import get_all_data
from .classification_files.block_type import exclude
from .schem import (schem_chunk, schem_liquid, schem, remove_brackets, collect_blocks,
                    separate_vertices_by_blockid, separate_vertices_by_chunk,
                    litematic_to_mesh, merge_chunks, SCHEMCACHE_DIR, VAR_CACHE_PATH)
from .functions.mesh_to_mc import create_mesh_from_dictionary,create_or_clear_collection
from .pointcloud import ensure_geometry_nodes_group, attach_schem_modifier, build_point_cloud_mesh
from .register import register_blocks
from .block_map_store import load_block_map, save_block_map
from . import dependency_manager
import json

# 使用依赖管理器导入
amulet = dependency_manager.amulet
amulet_nbt = dependency_manager.amulet_nbt


def write_var_cache(schempath, chunks, name, x_list, processnum):
    """多进程共享数据写入 var.json（替代不安全的 pickle）"""
    os.makedirs(SCHEMCACHE_DIR, exist_ok=True)
    data = {
        "schempath": schempath,
        "chunks": chunks,
        "name": name,
        "x_list": x_list,
        "processnum": processnum,
    }
    with open(VAR_CACHE_PATH, 'w') as f:
        json.dump(data, f)


def link_colormap_to_materials():
    """把所有材质中名为"色图"的 TEX_IMAGE 节点指向 colormap 图像。

    保留原有的全量扫描语义（旧材质也会被重新指向本次导入的 colormap）。
    """
    for material in bpy.data.materials:
        try:
            for node in material.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.name == '色图':
                    node.image = bpy.data.images.get("colormap")
        except Exception as e:
            print("材质出错了:", e)


def _decode_litematica_bit_array(bit_array):
    """numpy 批量解开 LitematicaBitArray 的紧凑位存储（等价于逐项 __getitem__）。

    条目 i 占据第 [i*nbits, (i+1)*nbits) 位，至多跨两个 64 位字；
    畸形数据的越界条目按 0（空气）处理，与原逐格 except 分支一致。
    """
    size = bit_array.size
    nbits = bit_array.nbits  # 类注解写作 nbit，实际属性名是 nbits
    words = np.array(bit_array.array, dtype=np.uint64)
    n_words = len(words)
    offs = np.arange(size, dtype=np.uint64) * np.uint64(nbits)
    w_idx = offs >> np.uint64(6)
    b_off = offs & np.uint64(63)
    if n_words:
        safe_idx = np.minimum(w_idx, np.uint64(n_words - 1))
    else:
        safe_idx = np.zeros(size, dtype=np.uint64)
    vals = words[safe_idx] >> b_off
    # 跨字的条目：高位部分来自下一个字（b_off==0 时移位量按 0 处理避免越界移位）
    spill = (b_off + np.uint64(nbits)) > np.uint64(64)
    if spill.any() and n_words:
        next_idx = np.minimum(w_idx + np.uint64(1), np.uint64(n_words - 1))
        shift = np.where(b_off == 0, np.uint64(0), np.uint64(64) - b_off)
        vals = np.where(spill, vals | (words[next_idx] << shift), vals)
    return (vals & np.uint64((1 << nbits) - 1)).astype(np.uint32)


class ImportBlock(bpy.types.Operator):
    """导入方块"""
    bl_label = "导入方块"
    bl_idname = 'mbm.import_block'

    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.json文件
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}) # type: ignore

    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    def execute(self, context):
        id_list = []
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            # 使用 for 循环逐级向上查找，直到找到名为 'blockstates' 的目录
            dir_name = os.path.dirname(self.filepath)
            while os.path.basename(dir_name) != 'blockstates':
                dir_name = os.path.dirname(dir_name)
            # 获取 'blockstates' 目录的上一级目录名作为命名空间
            namespace = os.path.basename(os.path.dirname(dir_name)) + ":"
            # 读取JSON文件
            with open(self.filepath, 'r') as file:
                data = json.load(file)
            
            # 提取所需内容
            variants = data.get("variants", {})
            # 提取所需内容
            multipart = data.get("multipart", [])
            
            if variants != {}:
                for key, value in variants.items():
                    if key !="":
                        id_list.append(namespace+os.path.basename(self.filepath).replace(".json","") + "[" + key + "]")
                    else:
                        id_list.append(namespace+os.path.basename(self.filepath).replace(".json",""))
            if multipart !=[]:
                # 获取所有when可能的属性
                all_when_keys = set()
                for entry in multipart:
                    when_data = entry.get("when", {})
                    all_when_keys.update(when_data.keys())

                # 遍历multipart数组
                for i, entry in enumerate(multipart):
                    when_data = entry.get("when", {})

                    # 补充默认为False的属性
                    for key in all_when_keys:
                        if key not in when_data:
                            when_data[key] = "false"

                    # 将when数据按字母顺序排序
                    sorted_when_data = dict(sorted(when_data.items()))

                    # 生成[]内的字符串
                    when_string = ','.join([f'{key}={value}' for key, value in sorted_when_data.items()])

                    # 构建文件名
                    filename = os.path.basename(self.filepath).replace(".json","") + "[" + when_string + "]"

                    # 添加到结果列表
                    id_list.append(namespace+filename)
        register_blocks(id_list)


            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ImportNBT(bpy.types.Operator):
    bl_idname = "mbm.import_nbt"
    bl_label = "导入.nbt文件"
    
    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.nbt文件
    filter_glob: bpy.props.StringProperty(default="*.nbt", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    # 定义操作的执行函数
    def execute(self, context):
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            # 获取文件路径
            filepath = self.filepath
            filename = os.path.basename(filepath)
            data = amulet_nbt.load(filepath)
            
            blocks =data["blocks"]
            entities = data["entities"]
            if "palette" in data:
                palette = data["palette"]
            elif "palettes" in data:
                palette = data["palettes"][0]
            

            size = data["size"]
            d = {}  

            for block in blocks:
                pos_tags = block['pos']  
                pos = tuple(tag.value for tag in pos_tags)  
                state = block['state'].value 
                block_name = palette[state]['Name'].value if 'Name' in palette[state] else palette[state]['nbt']['name'].value
                if 'Properties' in palette[state]:
                    block_state = palette[state]['Properties'].value
                    block_state = ','.join([f'{k}={v}' for k, v in block_state.items()])
                elif 'nbt' in palette[state] and 'name' in palette[state]['nbt']:
                    block_state = palette[state]['nbt']['name'].value
                    block_state = ','.join([f'{k}={v}' for k, v in block_state.items()])
                else:
                    block_state = None
                if block_name !="minecraft:air":
                    if block_state is not None:
                        d[(pos[0],pos[2],pos[1])] = str(block_name)+"["+block_state+"]"
                    else:
                        d[(pos[0],pos[2],pos[1])] = block_name

            #普通方法，有面剔除，速度较慢。
            # start_time = time.time()
            # nbt(d,filename)
            # end_time = time.time()
            #print("代码块执行时间：", end_time - start_time, "秒")

            #py+几何节点做法，无面剔除，但速度快。
            create_mesh_from_dictionary(d,filename.replace(".nbt",""))
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# 定义一个导入.schem文件的操作类
class ImportSchem(bpy.types.Operator):
    bl_idname = "mbm.import_schem"
    bl_label = "导入.schem文件"
    
    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.schem文件
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore

    # 定义操作的执行函数
    def execute(self, context):
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            name=os.path.basename(self.filepath)
            folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+ "/schemcache"
            if os.path.exists(folder_path):
                file_names = os.listdir(folder_path)
                for file_name in file_names:
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)
            level = amulet.load_level(self.filepath)
            chunks = [list(point) for point in level.bounds("main").bounds]

            wm = context.window_manager
            wm.progress_begin(0, 100)
            try:
                # 判断方块数量，超过阈值自动启用多进程
                total_blocks = ((chunks[1][0] - chunks[0][0]) *
                                (chunks[1][1] - chunks[0][1]) *
                                (chunks[1][2] - chunks[0][2]))
                prefs = context.preferences.addons.get('MBM_Workflow')
                if prefs and total_blocks >= prefs.preferences.sna_minsize:
                    level.close()
                    print(f"[MBM] 方块数 {total_blocks} >= 阈值 {prefs.preferences.sna_minsize}，自动启用多进程")
                    bpy.ops.mbm.multiprocess_pool(filepath=self.filepath)
                    continue

                # 使用公共 API 加载 NBT 数据
                with open(self.filepath, "rb") as f:
                    nbt_data = amulet_nbt.load(f)

                size = {
                    "x":int(nbt_data["Width"]),
                    "y":int(nbt_data["Height"]),
                    "z":int(nbt_data["Length"])
                }

                # 设置图片的大小和颜色
                image_width = int(size["z"])
                image_height = int(size["x"])
                default_color = (0.47, 0.75, 0.35, 1.0)  # RGBA颜色，对应#79c05a

                # 创建一个新的图片
                image = bpy.data.images.new("colormap", width=image_width, height=image_height)
                image.use_fake_user = True

                # 使用 foreach_set 设置默认颜色（替代非线程安全的像素线程操作）
                pixel_count = image_width * image_height * 4
                pixels = [c for _ in range(image_width * image_height) for c in default_color]
                image.pixels.foreach_set(pixels)
                start_time = time.time()

                wm.progress_update(10)
                obj=schem(level,chunks,False,name)
                wm.progress_update(60)
                if context.scene.separate_vertices_by_blockid ==True:
                    separate_vertices_by_blockid(obj)
                elif context.scene.separate_vertices_by_chunk ==True:
                    separate_vertices_by_chunk(obj)
                wm.progress_update(70)
                schem_liquid(level,chunks)
                wm.progress_update(95)
            finally:
                wm.progress_end()

            end_time = time.time()
            execution_time = end_time - start_time

            print("程序运行时间为：", execution_time, "秒")
            link_colormap_to_materials()



        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ReloadBlocks(bpy.types.Operator):
    """重载失效或空的方块缓存，使插件重新尝试读取模型"""
    bl_idname = "mbm.reload_blocks"
    bl_label = "重载失效方块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text_data = bpy.data.texts.get("Blocks.py")
        if not text_data:
            self.report({'WARNING'}, "未找到 Blocks.py 数据")
            return {'FINISHED'}

        try:
            id_map = load_block_map(text_data)
        except Exception as e:
            self.report({'ERROR'}, f"无法解析方块数据: {e}")
            return {'CANCELLED'}

        collection = bpy.data.collections.get("Blocks")
        if not collection:
            self.report({'WARNING'}, "未找到 Blocks 集合")
            return {'FINISHED'}

        to_remove = []
        # 不需要重载的方块列表（确实是空的或特殊的）
        skip_list = ["minecraft:air", "minecraft:barrier", "minecraft:structure_void", "minecraft:light"]

        for id_str, index in id_map.items():
            if id_str in skip_list:
                continue
            
            # 对象命名格式: "index#id"
            # 查找以 "index#" 开头的对象
            target_obj = None
            prefix = f"{index}#"
            
            found = False
            for obj in collection.objects:
                if obj.name.startswith(prefix):
                    target_obj = obj
                    found = True
                    break
            
            is_broken = False
            if not found:
                # 记录在案但对象丢失 -> 需要重置
                is_broken = True
            elif target_obj and hasattr(target_obj.data, 'vertices') and len(target_obj.data.vertices) == 0:
                # 有对象但没有顶点数据 -> 可能是之前导入失败生成的空对象
                is_broken = True
                bpy.data.objects.remove(target_obj, do_unlink=True)
            
            if is_broken:
                to_remove.append(id_str)

        # 更新 id_map
        if to_remove:
            for id_str in to_remove:
                if id_str in id_map:
                    del id_map[id_str]
            
            # 写回 Blocks.py
            save_block_map(text_data, id_map, sort_by_value=True)
            
            context.view_layer.update()
            self.report({'INFO'}, f"已清理 {len(to_remove)} 个失效方块记录。下次导入时将重新加载。")
        else:
            self.report({'INFO'}, "未发现需要重载的失效方块。")

        return {'FINISHED'}


# 导入.litematic文件的操作类
class ImportLitematic(bpy.types.Operator):
    bl_idname = "mbm.import_litematic"
    bl_label = "导入.litematic文件"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.litematic", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore


    def _safe_load_nbt(self, context):
        """Safe wrapper to define Region.from_nbt before litemapy loads"""
         # Monkey-patch litemapy's Region.from_nbt to handle list index out of range errors
        try:
             # We need to import litemapy here (it's already loaded via dependency_manager but we need the module object)
            from . import dependency_manager
            import math
            litemapy_mod = dependency_manager.litemapy

            
            # The error 'list index out of range' in Region.from_nbt usually happens at:
            # region.__blocks[x][y][z] = bit_array[ind]
            # or
            # del region.__palette[0]
            
            # Let's verify if we can access schem.py's Region class
            if hasattr(litemapy_mod.schematic, 'Region'):
                RegionClass = litemapy_mod.schematic.Region
                
                # Check if we already patched it
                if getattr(RegionClass, '_is_patched_safe', False):
                    return

                original_from_nbt = RegionClass.from_nbt

                @staticmethod
                def safe_from_nbt(nbt):
                    try:
                        return original_from_nbt(nbt)
                    except IndexError as e:
                        # If list index out of range happens, try to inspect why or return a dummy region
                        # But returning dummy region might break Schematic.from_nbt structure.
                        # Instead, we want to fix the data if possible.
                        # Since we can't easily fix the NBT data on the fly without parsing logic...
                        
                        # Let's try a robust implementation of reading the region
                        # This requires re-implementing part of Region.from_nbt
                        
                        print(f"Litematic Fix: Detected malformed region data ({e}). Attempting to recover...")
                        
                        # Re-impl minimal parts
                        pos = nbt["Position"]
                        x, y, z = int(pos["x"]), int(pos["y"]), int(pos["z"])
                        size = nbt["Size"]
                        w, h, l = int(size["x"]), int(size["y"]), int(size["z"])
                        
                        region = RegionClass(x, y, z, w, h, l)
                        
                        # Populate palette safely
                        # Access private member if needed, or use public methods if available?
                        # Region attributes are __palette (private).
                        # We need to use name mangling: _Region__palette
                        
                        palette_list = getattr(region, "_Region__palette")
                        if len(palette_list) > 0 and palette_list[0].id == "minecraft:air":
                             del palette_list[0]
                        
                        from . import dependency_manager
                        BlockState = dependency_manager.litemapy.minecraft.BlockState
                        
                        for block_nbt in nbt["BlockStatePalette"]:
                             try:
                                block = BlockState.from_nbt(block_nbt)
                                palette_list.append(block)
                             except Exception as block_err:
                                print(f"Skipping bad block in palette: {block_err}")
                                # Add AIR to keep index alignment if possible, or just skip
                                palette_list.append(BlockState("minecraft:air"))

                        # Skip entities for now to minimize errors
                        
                        # Process blocks
                        blocks = nbt["BlockStates"]
                        nbits = max(math.ceil(math.log(len(palette_list), 2)), 2)
                        
                        LitematicaBitArray = dependency_manager.litemapy.storage.LitematicaBitArray
                        bit_array = LitematicaBitArray.from_nbt_long_array(blocks, abs(w*h*l), nbits)
                        
                        block_grid = getattr(region, "_Region__blocks")

                        # Safe assignment
                        palette_len = len(palette_list)

                        width_abs, height_abs, length_abs = abs(w), abs(h), abs(l)

                        # numpy 批量解码替代逐格 try/except 循环：
                        # ind = (y * W * L) + z * W + x，即按 (y, z, x) 行序铺开
                        decoded = _decode_litematica_bit_array(bit_array)
                        total_blocks = abs(w * h * l)
                        if len(decoded) < total_blocks:
                            decoded = np.concatenate([
                                decoded,
                                np.zeros(total_blocks - len(decoded), dtype=np.uint32)])
                        decoded = decoded[:total_blocks]
                        decoded[decoded >= palette_len] = 0  # 越界索引按空气处理
                        block_grid[:, :, :] = decoded.reshape(
                            height_abs, length_abs, width_abs).transpose(2, 0, 1)

                        return region

                RegionClass.from_nbt = safe_from_nbt
                setattr(RegionClass, '_is_patched_safe', True)
                print("Litemapy patched for safe loading.")
                
        except Exception as e:
            print(f"Failed to patch litemapy: {e}")

    def execute(self, context):
        from . import dependency_manager
        import math
        
        # Apply patch before loading
        self._safe_load_nbt(context)

        litemapy = dependency_manager.litemapy


        if litemapy is None:
            self.report({'ERROR'}, "litemapy 库未安装")
            return {'CANCELLED'}

        for f in self.files:
            self.filepath = str(os.path.dirname(self.filepath)) + "\\" + str(f.name)
            base_filename = os.path.basename(self.filepath).replace(".litematic", "")

            try:
                schem = litemapy.Schematic.load(self.filepath)
            except Exception as e:
                self.report({'ERROR'}, f"无法加载文件: {str(e)}")
                return {'CANCELLED'}

            if not schem.regions:
                self.report({'WARNING'}, "文件不包含任何区域")
                return {'CANCELLED'}

            region_count = len(schem.regions)

            wm = context.window_manager
            wm.progress_begin(0, region_count)
            try:
                for region_index, (region_name, region) in enumerate(schem.regions.items()):
                    wm.progress_update(region_index)
                    self._load_single_region(context, region, region_name, base_filename,
                                             region_count == 1)
            finally:
                wm.progress_end()

            print(f"成功导入 {region_count} 个区域")

        return {'FINISHED'}

    def _load_single_region(self, context, region, region_name, base_filename, single_region):
        # 尝试修复 invalid index issues (导致 list index out of range)
        try:
            # 访问私有属性 (name mangling: Region -> _Region)
            blocks = getattr(region, "_Region__blocks", None)
            palette = getattr(region, "_Region__palette", None)

            if blocks is not None and palette is not None:
                import numpy as np
                p_len = len(palette)
                if p_len > 0 and isinstance(blocks, np.ndarray):
                     # 检查是否有超出调色板范围的索引
                     # 注意: numpy.any() 可能会比较慢，但比起崩溃要好
                     if np.any(blocks >= p_len):
                         print(f"[Import Fix] 在区域 '{region_name}' 中发现无效的方块索引。正在修正...")
                         # 将无效索引重置为 0 (通常是 minecraft:air)
                         blocks[blocks >= p_len] = 0
        except Exception as e:
            print(f"[Import Fix] 尝试修复区域数据时出错: {e}")

        # 处理单个区域数据
        block_dict, bounds = self._process_single_region(region, region_name)

        if not block_dict:
            print(f"区域 '{region_name}' 不包含任何方块，跳过")
            return

        # 生成对象名称：单区域使用原文件名，多区域添加区域后缀
        if single_region:
            obj_filename = base_filename
        else:
            obj_filename = f"{base_filename}_{region_name}"

        # 创建网格对象
        obj = litematic_to_mesh(block_dict, bounds, obj_filename)

        # 应用可选的顶点分离
        if context.scene.separate_vertices_by_blockid:
            separate_vertices_by_blockid(obj)
        elif context.scene.separate_vertices_by_chunk:
            separate_vertices_by_chunk(obj)

    def _process_single_region(self, region, region_name):
        """处理单个区域，返回方块字典和边界"""
        from .classification_files.block_type import exclude

        # 优先 numpy 批量路径：直接读 Region 内部的调色板索引数组
        blocks = getattr(region, "_Region__blocks", None)
        if isinstance(blocks, np.ndarray):
            return self._process_region_numpy(region, blocks, exclude)

        # 回退：逐格访问（原实现）
        block_dict = {}
        format_cache = {}  # 相同 BlockState 内容只格式化一次
        min_x = min_y = min_z = None
        max_x = max_y = max_z = None

        for x, y, z in region.block_positions():
            block = region[x, y, z]

            if block.id == "minecraft:air":
                continue

            props = getattr(block, 'properties', None) or {}
            cache_key = (block.id, tuple(props.items()))
            block_str = format_cache.get(cache_key)
            if block_str is None:
                block_str = self._format_block_state(block)
                format_cache[cache_key] = block_str

            base_block = block_str.split('[', 1)[0]

            if base_block in exclude:
                continue

            # 使用区域相对坐标，同时单趟维护边界
            block_dict[(x, y, z)] = block_str
            if min_x is None:
                min_x = max_x = x
                min_y = max_y = y
                min_z = max_z = z
            else:
                if x < min_x: min_x = x
                elif x > max_x: max_x = x
                if y < min_y: min_y = y
                elif y > max_y: max_y = y
                if z < min_z: min_z = z
                elif z > max_z: max_z = z

        # 计算边界
        if min_x is None:
            min_coords = (0, 0, 0)
            max_coords = (0, 0, 0)
        else:
            min_coords = (min_x, min_y, min_z)
            max_coords = (max_x, max_y, max_z)

        return block_dict, (min_coords, max_coords)

    def _process_region_numpy(self, region, blocks, exclude):
        """numpy 批量读取 Region：调色板只格式化一次，argwhere 一次取出全部保留格。

        与逐格路径等价：region.palette 触发 _optimize_palette 后与 __getitem__
        读到的同一份内部数据一致；负尺寸区域的存储坐标按
        __region_coordinates_to_store_coordinates 的互逆映射翻转回区域坐标。
        """
        W, H, L = blocks.shape
        palette = region.palette
        n = len(palette)
        fmt = [None] * n
        keep = np.zeros(n, dtype=bool)
        for p, block in enumerate(palette):
            if block.id == "minecraft:air":
                continue
            block_str = self._format_block_state(block)
            if block_str.split('[', 1)[0] in exclude:
                continue
            fmt[p] = block_str
            keep[p] = True

        mask = keep[blocks]
        rel = np.argwhere(mask)  # (N, 3) 存储坐标 (x, y, z)
        vals = blocks[mask]
        # 存储坐标 → 区域坐标：负尺寸区域做平移（region = store + dim + 1），
        # 与 __region_coordinates_to_store_coordinates（store = region - dim - 1）互逆
        if region.width < 0:
            rel[:, 0] += region.width + 1
        if region.height < 0:
            rel[:, 1] += region.height + 1
        if region.length < 0:
            rel[:, 2] += region.length + 1

        block_dict = {}
        for x, y, z, p in zip(rel[:, 0].tolist(), rel[:, 1].tolist(),
                              rel[:, 2].tolist(), vals.tolist()):
            block_dict[(x, y, z)] = fmt[p]

        if block_dict:
            min_coords = (int(rel[:, 0].min()), int(rel[:, 1].min()), int(rel[:, 2].min()))
            max_coords = (int(rel[:, 0].max()), int(rel[:, 1].max()), int(rel[:, 2].max()))
        else:
            min_coords = max_coords = (0, 0, 0)
        return block_dict, (min_coords, max_coords)

    def _format_block_state(self, block):
        """格式化方块状态字符串"""
        block_str = block.id
        props = getattr(block, 'properties', None)
        if props:
            props = ','.join(f"{k}={v}" for k, v in props.items())
            block_str = f"{block.id}[{props}]"
        return block_str

    def _remove_brackets(self, input_string):
        """移除方括号内容获取基础方块名"""
        return input_string.split('[', 1)[0]

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#多进程结束后导入模型
class MultiprocessImport(bpy.types.Operator):
    bl_idname = "mbm.multiprocess_import"
    bl_label = "导入.schem文件"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        with open(VAR_CACHE_PATH, 'r') as f:
            data = json.load(f)
        chunks = data["chunks"]
        name = data["name"]
        processnum = data["processnum"]

        # 合并所有区块数据
        merge_chunks(processnum, name)

        # 使用合并后的数据创建最终网格
        # cached=True 分支只读 pickle，不再需要重新加载 schem 文件
        schem(None, chunks, True, name)

        link_colormap_to_materials()

        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#每个进程分别处理一个区块
class MultiprocessSchem(bpy.types.Operator):
    bl_idname = "mbm.import_schem_mp"
    bl_label = "多进程区块处理"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    chunk_index: bpy.props.IntProperty(default=0) # type: ignore

    def execute(self, context):
        with open(VAR_CACHE_PATH, 'r') as f:
            data = json.load(f)
        level = amulet.load_level(self.filepath)
        schem_chunk(level, data["chunks"], data["x_list"],
                    chunk_index=self.chunk_index, filename=data["name"])
        return {'FINISHED'}


class ImportSchemLiquid(bpy.types.Operator):
    bl_idname = "mbm.import_schem_liquid"
    bl_label = "多进程流体处理"

    def execute(self, context):
        with open(VAR_CACHE_PATH, 'r') as f:
            data = json.load(f)
        level = amulet.load_level(data["schempath"])
        schem_liquid(level, data["chunks"])
        ModelCachePath = os.path.join(SCHEMCACHE_DIR, "liquid.blend")
        bpy.ops.wm.save_as_mainfile(filepath=ModelCachePath)
        return {'FINISHED'}


class MultiprocessPool(bpy.types.Operator):
    """多进程导入 .schem 文件（自动分块并行处理）"""
    bl_idname = "mbm.multiprocess_pool"
    bl_label = "多进程导入.schem文件"
    bl_options = {"REGISTER"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        prefs = context.preferences.addons['MBM_Workflow'].preferences
        processnum = prefs.sna_processnumber
        minsize = prefs.sna_minsize

        # 1. 加载 schem 文件
        level = amulet.load_level(self.filepath)
        bounds = level.bounds()
        chunks = [list(bounds.min), list(bounds.max)]
        total_blocks = ((chunks[1][0] - chunks[0][0]) *
                        (chunks[1][1] - chunks[0][1]) *
                        (chunks[1][2] - chunks[0][2]))

        # 2. 不满足多进程阈值时回退到单进程
        if total_blocks < minsize:
            print(f"[MBM] 方块数 {total_blocks} < 阈值 {minsize}，使用单进程导入")
            level.close()
            bpy.ops.mbm.import_schem(filepath=self.filepath)
            return {'FINISHED'}

        # 3. 计算 x_list 分割（沿 X 轴均分）
        x_range = chunks[1][0] - chunks[0][0]
        chunk_size = max(1, x_range // processnum)
        x_list = []
        for i in range(processnum):
            start = chunks[0][0] + i * chunk_size
            end = chunks[0][0] + (i + 1) * chunk_size if i < processnum - 1 else chunks[1][0] + 1
            x_list.append([start, end])

        # 4. 写 var.json
        name = os.path.splitext(os.path.basename(self.filepath))[0]
        level.close()
        write_var_cache(self.filepath, chunks, name, x_list, processnum)

        # 5. 启动子进程
        mp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "multiprocess")
        processes = []

        # 子进程通过环境变量接收 schemcache 绝对路径（不依赖 script_path_user()/addons/）
        child_env = {**os.environ, "MBM_VAR_CACHE_PATH": VAR_CACHE_PATH, "MBM_SCHEMCACHE_DIR": SCHEMCACHE_DIR}
        for i in range(processnum):
            p = subprocess.Popen(
                [bpy.app.binary_path, "--background", "--python",
                 os.path.join(mp_dir, "schem_mp.py")],
                env={**child_env, "MBM_CHUNK_INDEX": str(i)}
            )
            processes.append(p)

        # 启动液体处理子进程
        p_liquid = subprocess.Popen(
            [bpy.app.binary_path, "--background", "--python",
             os.path.join(mp_dir, "schem_liquid_mp.py")],
            env=child_env
        )
        processes.append(p_liquid)

        print(f"[MBM] 已启动 {len(processes)} 个子进程处理 {name}")
        self._processes = processes
        self._name = name
        self._context = context

        # 6. 使用 timer 轮询等待子进程完成（不阻塞 UI）
        bpy.app.timers.register(self._wait_for_processes, first_interval=2.0)
        return {'RUNNING_MODAL'}

    def _wait_for_processes(self):
        """轮询子进程完成状态"""
        all_done = all(p.poll() is not None for p in self._processes)
        if not all_done:
            return 2.0  # 2秒后再次检查

        # 所有子进程完成，执行合并导入
        try:
            with open(VAR_CACHE_PATH, 'r') as f:
                data = json.load(f)
            processnum = data["processnum"]

            # 检查子进程是否都成功
            for i, p in enumerate(self._processes):
                if p.returncode != 0:
                    print(f"[MBM] 子进程 {i} 异常退出，返回码: {p.returncode}")

            merge_chunks(processnum, self._name)
            level = amulet.load_level(data["schempath"])
            schem(level, data["chunks"], True, self._name)

            # 液体合并
            liquid_path = os.path.join(SCHEMCACHE_DIR, "liquid.blend")
            if os.path.exists(liquid_path):
                bpy.ops.wm.append(
                    filepath=liquid_path,
                    directory=os.path.dirname(liquid_path)
                )

            print(f"[MBM] 多进程导入完成: {self._name}")
        except Exception as e:
            print(f"[MBM] 多进程合并出错: {e}")
        return None  # 停止计时器

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class Importjson(bpy.types.Operator):
    """导入选定的json文件"""
    bl_idname = "mbm.import_json"
    bl_label = "导入json文件"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore

    def execute(self, context):
        # 检查文件路径是否有效
        if os.path.isfile(self.filepath) and self.filepath.endswith(".json"):
            # 获取文件名
            filename = os.path.basename(self.filepath)
            textures, elements,parent = get_all_data(os.path.dirname(self.filepath)+"\\", filename)
            position = [0, 0, 0]
            has_air = [True, True, True, True, True, True]
            block(textures, elements, position,[0,0,0], filename, has_air)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "请选择有效的.json文件")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # 打开文件选择对话框
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SNA_AddonPreferences_F35F8(bpy.types.AddonPreferences):
    bl_idname = 'MBM_Workflow'
    sna_processnumber: bpy.props.IntProperty(name='ProcessNumber', description='最大进程数，同时处理这么多个区块', default=6, subtype='NONE', min=1, max=64) # type: ignore
    sna_minsize: bpy.props.IntProperty(name='MinSize', description='超过这个数就会启用多进程分区块导入', default=1000000, subtype='NONE', min=1000, max=99999999) # type: ignore

    def draw(self, context):
        layout = self.layout


class SNA_OT_My_Generic_Operator_A38B8(bpy.types.Operator):
    bl_idname = "sna.my_generic_operator_a38b8"
    bl_label = "刷新"
    bl_description = "自动设置以下参数"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        cpu_half = max(1, int(os.cpu_count() / 2))
        prefs = bpy.context.preferences.addons['MBM_Workflow'].preferences
        prefs.sna_processnumber = cpu_half
        prefs.sna_minsize = 1000000
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


    
# class SelectArea(bpy.types.Operator):
#     """选择区域（性能有问题）"""
#     bl_label = "选择区域"
#     bl_idname = 'mbm.select'
    
#     def execute(self, context):
#         # 获取当前场景的名称
#         current_scene = bpy.context.scene.name
#         # 如果场景名称不为"地图"，则返回
#         if current_scene != "地图":
#             button_callback(self, context,"地图仍未创建！")
#             return {'CANCELLED'}
#         # 检查当前场景是否已经有名为"Map"的集合
#         existing_collections = bpy.data.collections.values()
#         for coll in existing_collections:
#             if coll.name == "Map":
#                 button_callback(self, context,"已经存在选择框！(如果你删除了一些东西请连同集合一起删除）")
#                 return {'CANCELLED'}
#         # 获取当前文件的路径
#         current_path = os.path.dirname(os.path.abspath(__file__))
#         # 拼接路径和文件名
#         filepath = os.path.join(current_path, "blend_files","Map.blend")
#         # 从文件中加载名为"Map"的集合
#         with bpy.data.libraries.load(filepath) as (data_from, data_to):
#             data_to.collections = ["Map"]
#         # 将集合链接到当前场景
#         for coll in data_to.collections:
#             if coll is not None:
#                 bpy.context.scene.collection.children.link(coll)
#         return {'FINISHED'}

class ImportWorld(bpy.types.Operator):
    """导入世界(性能有问题)"""
    bl_label = "导入世界"
    bl_idname = 'mbm.import_world'

    current_chunk_index = 0  # 当前处理的区块索引

    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore


    def execute(self, context):
        # 获取配置的版本
        platform = context.scene.mc_platform
        version = (
            context.scene.mc_version_major,
            context.scene.mc_version_minor,
            context.scene.mc_version_patch
        )

        filename = "world"
        level = amulet.load_level(self.filepath)
        min_coords=context.scene.min_coordinates
        max_coords=context.scene.max_coordinates
        # 创建一个新的集合
        collection_name="Blocks"
        create_or_clear_collection(collection_name)
        collection =bpy.data.collections.get(collection_name)
        #导入几何节点
        ensure_geometry_nodes_group(collection_name)
        wm = context.window_manager
        wm.progress_begin(0, 100)
        try:
            wm.progress_update(10)
            # chunk 级批量读取（翻译器内部带缓存），失败自动回退逐格路径
            vertices, ids, _waterlogged = collect_blocks(
                level, "minecraft:overworld", min_coords, max_coords, platform, version)
            wm.progress_update(80)
        finally:
            wm.progress_end()

        id_map=register_blocks(list(set(ids)))
        # 创建点云对象并批量写入顶点与属性（原路径无 waterlogged 属性）
        obj = build_point_cloud_mesh(filename, vertices, ids, id_map, with_waterlogged=False)
        attach_schem_modifier(obj, collection_name)
        level.close()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes=[ImportBlock,ImportSchem,ImportLitematic,MultiprocessSchem,Importjson,ImportWorld,#SelectArea,
         ImportNBT,SNA_AddonPreferences_F35F8,SNA_OT_My_Generic_Operator_A38B8,ImportSchemLiquid,MultiprocessImport,
         MultiprocessPool,ReloadBlocks]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    
