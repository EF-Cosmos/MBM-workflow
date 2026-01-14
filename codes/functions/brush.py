import bpy
import bmesh
from bpy.props import EnumProperty
from mathutils.kdtree import KDTree
import bpy_extras.view3d_utils as view3d_utils

class BAIGAVE_OT_BlockBrush(bpy.types.Operator):
    bl_idname = "baigave.block_brush"
    bl_label = "方块笔刷"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.kd_tree = None
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
            self.kd_tree = None 
            self.target_obj = None
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            obj = context.active_object
            if not obj or obj.type != 'MESH' or 'blockid' not in obj.data.attributes:
                self.report({'WARNING'}, "请选择一个带有 blockid 属性的对象")
                return {'CANCELLED'}
            
            self.target_obj = obj
            self.report({'INFO'}, "构建索引中...")
            
            mesh = obj.data
            size = len(mesh.vertices)
            self.kd_tree = KDTree(size)
            for i, v in enumerate(mesh.vertices):
                self.kd_tree.insert(v.co, i)
            self.kd_tree.balance()
            
            self.report({'INFO'}, "方块笔刷已就绪 (左键: 绘制, Shift+左键: 吸管, 右键: 退出)")
            
            context.window.cursor_modal_set('PAINT_BRUSH')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found")
            return {'CANCELLED'}

    def brush_action(self, context, event):
        scene = context.scene
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y
        
        depsgraph = context.evaluated_depsgraph_get()
        
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        
        result, location, normal, index, obj, matrix = scene.ray_cast(depsgraph, origin, direction)
        
        if result and obj == self.target_obj:
            matrix_inv = obj.matrix_world.inverted()
            local_hit = matrix_inv @ location
            local_normal = matrix_inv.to_3x3() @ normal
            local_normal.normalize()
            
            center_guess = local_hit - local_normal * 0.5
            
            co, index, dist = self.kd_tree.find(center_guess)
            
            if dist < 0.8: 
                is_sample = event.shift
                
                if is_sample:
                    val = self.target_obj.data.attributes['blockid'].data[index].value
                    self.report({'INFO'}, f"吸取 ID: {val}")
                    try:
                        context.scene.my_properties.brush_block_enum = str(val)
                    except:
                        pass
                else:
                    try:
                        target_id = int(context.scene.my_properties.brush_block_enum)
                        self.target_obj.data.attributes['blockid'].data[index].value = target_id
                        self.target_obj.data.update()
                    except ValueError:
                        self.report({'WARNING'}, "无效的目标方块 ID")


def register():
    bpy.utils.register_class(BAIGAVE_OT_BlockBrush)


def unregister():
    bpy.utils.unregister_class(BAIGAVE_OT_BlockBrush)
