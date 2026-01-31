import bpy
import os


def set_modifier_socket_value(modifier, socket_identifier, fallback_name, value, is_input=True):
    """
    为几何节点修饰符的 socket 设置值，兼容 Blender 5.0+

    Args:
        modifier: 几何节点修饰符
        socket_identifier: socket 的标识符
        fallback_name: 回退匹配时的 socket 名称关键词
        value: 要设置的值
        is_input: True 表示输入 socket，False 表示输出 socket
    """
    try:
        modifier[socket_identifier] = value
    except (KeyError, TypeError):
        if not modifier.node_group:
            return
        sockets = modifier.node_group.inputs if is_input else modifier.node_group.outputs
        for socket in sockets:
            if socket.identifier == socket_identifier or fallback_name.lower() in socket.name.lower():
                socket.default_value = value
                break


class MapOptimize(bpy.types.Operator):
    """优化面"""
    bl_idname = "mbm.map_optimize"
    bl_label = "优化面"

    def execute(self, context):
        scene = context.scene
        is_weld = scene.is_weld
        objs = context.selected_objects
        nodetree_target = "UV"

        for obj in objs:
            obj.select_set(True)
            context.view_layer.objects.active = obj

            # 移除所有修改器
            for md in obj.modifiers:
                obj.modifiers.remove(md)

            bpy.ops.object.transform_apply(rotation=True)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')

            # 合并重叠的顶点
            if is_weld:
                bpy.ops.mesh.remove_doubles(threshold=0.001)

            # 精简面
            bpy.ops.mesh.dissolve_limited(
                angle_limit=0.0872665, use_dissolve_boundaries=False, delimit={'MATERIAL'}
            )

            bpy.ops.object.mode_set(mode='OBJECT')

            # 添加几何节点修改器
            bpy.ops.object.modifier_add(type='NODES')
            mg = obj.modifiers[0]
            obj.modifiers.active = mg

            # 导入几何节点（如果不存在）
            if nodetree_target not in bpy.data.node_groups:
                file_path = bpy.context.scene.geometrynodes_blend_path
                inner_path = 'NodeTree'
                object_name = 'UV'
                bpy.ops.wm.append(
                    filepath=os.path.join(file_path, inner_path, object_name),
                    directory=os.path.join(file_path, inner_path),
                    filename=object_name
                )

            mg.node_group = bpy.data.node_groups[nodetree_target]

            # 设置输出属性名称 (Blender 5.0+ 兼容)
            set_modifier_socket_value(
                mg, 'Output_2_attribute_name', 'attribute',
                obj.data.uv_layers.active.name, is_input=False
            )

            bpy.ops.object.modifier_apply(modifier=mg.name)

            # 转换属性格式以兼容 Blender 5.0+
            atts = obj.data.attributes
            attr_count = len(atts)
            i = 0

            while i < attr_count:
                attr = atts[i]
                if attr.data_type == "FLOAT_VECTOR" and attr.domain == "CORNER":
                    atts.active_index = i
                    bpy.ops.geometry.attribute_convert(
                        mode='GENERIC', domain='CORNER', data_type="FLOAT2"
                    )
                    attr_count -= 1
                    continue
                if attr.data_type == "FLOAT_COLOR" and attr.domain == "CORNER":
                    atts.active_index = i
                    bpy.ops.geometry.attribute_convert(
                        mode='GENERIC', domain='CORNER', data_type="BYTE_COLOR"
                    )
                    attr_count -= 1
                    continue
                i += 1

            obj.select_set(False)
        return {'FINISHED'}
    

classes=[MapOptimize]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        