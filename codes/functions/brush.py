import bpy
import bmesh
from bpy.props import EnumProperty
import bpy_extras.view3d_utils as view3d_utils

class BAIGAVE_OT_BlockBrush(bpy.types.Operator):
    bl_idname = "baigave.block_brush"
    bl_label = "方块笔刷"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vertex_map = {}
        self.target_obj = None

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.brush_action(context, event)
            return {'RUNNING_MODAL'}
            
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.window.cursor_modal_restore()
            self.vertex_map = {}
            self.target_obj = None
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            obj = context.active_object
            if not obj or obj.type != 'MESH':
                self.report({'WARNING'}, "请选择一个网格对象")
                return {'CANCELLED'}

            # 检查 blockid 属性是否存在
            if 'blockid' not in obj.data.attributes:
                self.report({'WARNING'}, "对象没有 blockid 属性")
                return {'CANCELLED'}

            blockid_attr = obj.data.attributes['blockid']
            if blockid_attr.domain != 'POINT':
                self.report({'WARNING'}, "blockid 属性必须是 POINT 域")
                return {'CANCELLED'}

            # 检查属性数据是否为空
            if not blockid_attr.data or len(blockid_attr.data) == 0:
                self.report({'WARNING'}, "blockid 属性数据为空，可能已应用几何节点修改器")
                return {'CANCELLED'}

            # 检查几何节点修改器状态
            has_nodes_modifier = any(mod.type == 'NODES' for mod in obj.modifiers)
            if has_nodes_modifier:
                self.report({'INFO'}, "检测到几何节点修改器，修改点云会自动更新显示")
            
            self.target_obj = obj
            self.report({'INFO'}, "构建索引中...")
            
            mesh = obj.data
            self.vertex_map = {}
            for i, v in enumerate(mesh.vertices):
                coord = (int(v.co.x), int(v.co.y), int(v.co.z))
                self.vertex_map[coord] = i
            
            self.report({'INFO'}, "方块笔刷已就绪 (左键: 绘制, Shift+左键: 吸管, 右键: 退出)")
            
            context.window.cursor_modal_set('PAINT_BRUSH')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found")
            return {'CANCELLED'}

    def brush_action(self, context, event):
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y

        # 获取世界空间的射线
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

        # 使用 scene.ray_cast 检测 evaluated 对象（实例化后的网格）
        depsgraph = context.evaluated_depsgraph_get()
        result, location, normal, index, obj, matrix = context.scene.ray_cast(
            depsgraph, origin, direction
        )

        if result and obj == self.target_obj:
            # 将击中位置转换到对象局部空间
            matrix_inv = self.target_obj.matrix_world.inverted()
            local_location = matrix_inv @ location

            # Debug: 输出射线击中的原始坐标
            print(f"[DEBUG] 射线击中 - 世界坐标: {location}, 局部坐标: {local_location}")

            # 计算方块坐标（向下取整）
            block_coord = (
                int(local_location.x),
                int(local_location.y),
                int(local_location.z)
            )

            # 从哈希字典查找顶点索引
            vertex_index = self.vertex_map.get(block_coord)

            print(f"[DEBUG] 方块坐标: {block_coord}, 顶点索引: {vertex_index}")

            if vertex_index is not None:
                is_sample = event.shift
                blockid_data = self.target_obj.data.attributes['blockid'].data

                if is_sample:
                    # 添加边界检查
                    if vertex_index < len(blockid_data):
                        val = blockid_data[vertex_index].value
                        self.report({'INFO'}, f"吸取 ID: {val}")
                        try:
                            context.scene.my_properties.brush_block_enum = str(val)
                        except:
                            pass
                    else:
                        self.report({'WARNING'}, f"索引 {vertex_index} 超出范围")
                else:
                    try:
                        target_id = int(context.scene.my_properties.brush_block_enum)
                        # 添加边界检查
                        if vertex_index < len(blockid_data):
                            blockid_data[vertex_index].value = target_id
                            self.target_obj.data.update_tag()  # 标记数据更新，触发几何节点重新计算
                        else:
                            self.report({'WARNING'}, f"索引 {vertex_index} 超出范围")
                    except ValueError:
                        self.report({'WARNING'}, "无效的目标方块 ID")


def register():
    bpy.utils.register_class(BAIGAVE_OT_BlockBrush)


def unregister():
    bpy.utils.unregister_class(BAIGAVE_OT_BlockBrush)
