"""点云网格装配的公共实现。

schem / litematic / nbt / world 各导入路径共用同一套模式：
无面点云 + 顶点属性(blockid/waterlogged/biome) + 几何节点实例化修改器。
批量数据写入统一走 foreach_set，避免逐顶点 Python 循环。
"""
import os
import re

import bpy
import numpy as np

BIOME_COLOR = (0.149, 0.660, 0.10, 0.00)


def ensure_geometry_nodes_group(collection_name="Blocks"):
    """确保实例化用的几何节点组就绪，返回可直接赋给修改器的节点组。

    首次导入时从 GeometryNodes.blend 追加 "Schem" 模板并复制为 collection_name；
    已存在时直接复用，避免同会话多次导入时重复追加和 "Blocks.001" 命名泄漏。
    """
    group = bpy.data.node_groups.get(collection_name)
    if group is None:
        if "Schem" not in bpy.data.node_groups:
            file_path = bpy.context.scene.geometrynodes_blend_path
            inner_path = 'NodeTree'
            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, "Schem"),
                directory=os.path.join(file_path, inner_path),
                filename="Schem",
            )
        group = bpy.data.node_groups["Schem"].copy()
        group.name = collection_name
    return group


def attach_schem_modifier(obj, collection_name="Blocks"):
    """为点云对象附加几何节点实例化修改器，集合信息节点指向指定集合。"""
    collection = bpy.data.collections.get(collection_name)
    group = ensure_geometry_nodes_group(collection_name)
    if not any(m.type == 'NODES' for m in obj.modifiers):
        obj.modifiers.new(name="Schem", type="NODES")
    nodes_modifier = obj.modifiers[0]
    nodes_modifier.node_group = group
    group.nodes["集合信息"].inputs[0].default_value = collection
    nodes_modifier.show_viewport = True
    return nodes_modifier


def build_point_cloud_mesh(filename, vertices, ids, id_map, waterlogged=None,
                           with_waterlogged=True):
    """创建点云对象并批量写入顶点与属性。

    vertices: [(x, y, z), ...]
    ids:       与顶点一一对应的方块字符串（未 re.escape）
    id_map:    register_blocks 返回的映射，键为 re.escape 后的字符串
    waterlogged: 与顶点一一对应的水属性值；None 时全部按 0 处理
    with_waterlogged: 是否创建 waterlogged 属性（world/nbt 路径原本没有该属性）

    返回创建的对象。
    """
    mesh = bpy.data.meshes.new(name=filename)
    mesh.attributes.new(name='blockid', type="INT", domain="POINT")
    if with_waterlogged:
        mesh.attributes.new(name='waterlogged', type="INT", domain="POINT")
    mesh.attributes.new(name='biome', type="FLOAT_COLOR", domain="POINT")
    obj = bpy.data.objects.new(filename, mesh)
    bpy.context.scene.collection.objects.link(obj)

    count = len(vertices)
    if count:
        # id_map 的键是 re.escape 后的字符串；先按唯一字符串建映射，
        # 避免 re.escape 在逐顶点循环里重复执行
        escaped = {s: id_map[re.escape(s)] for s in set(ids)}

        mesh.vertices.add(count)
        mesh.vertices.foreach_set(
            "co", np.asarray(vertices, dtype=np.float32).reshape(-1))
        mesh.attributes['blockid'].data.foreach_set(
            "value", np.fromiter((escaped[s] for s in ids),
                                 dtype=np.int32, count=count))
        if with_waterlogged:
            mesh.attributes['waterlogged'].data.foreach_set(
                "value", np.asarray(waterlogged if waterlogged is not None
                                    else [0] * count, dtype=np.int32))
        biome = np.empty(count * 4, dtype=np.float32)
        biome[0::4], biome[1::4], biome[2::4], biome[3::4] = BIOME_COLOR
        mesh.attributes['biome'].data.foreach_set("color", biome)
    mesh.update()
    return obj
