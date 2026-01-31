import bpy
import numpy as np
import os
import time
from mathutils import Vector
from mathutils.kdtree import KDTree

class MBM_OT_PaintBlock(bpy.types.Operator):
    bl_idname = "mbm.paint_block"
    bl_label = "应用顶点色到方块"
    bl_description = "根据顶点颜色，自动匹配颜色字典中最接近的方块"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        start_time = time.time()
        obj = context.active_object
        mesh = obj.data
        scene = context.scene
        
        if 'blockid' not in mesh.attributes:
            self.report({'ERROR'}, "对象缺少 'blockid' 属性，请确保这是有效的 Schem 对象")
            return {'CANCELLED'}
        
        if not mesh.color_attributes:
            self.report({'ERROR'}, "未找到顶点颜色层。请先在定点绘制模式下绘制颜色。")
            return {'CANCELLED'}
            
        color_attr = mesh.color_attributes.active
        
        if color_attr.domain != 'POINT':
            self.report({'WARNING'}, f"当前颜色属性域为 {color_attr.domain}，建议使用 POINT (顶点) 域以获得最佳效果")
            
        color_file_path = scene.my_properties.color_file_path
        if not color_file_path:
             path = scene.colors_dir
             selected = scene.color_list
             if selected:
                 color_file_path = os.path.join(path, selected)
        
        if not color_file_path or not os.path.exists(color_file_path):
            self.report({'ERROR'}, "未选择有效的颜色字典")
            return {'CANCELLED'}

        color_dict_vars = {}
        try:
            with open(color_file_path, 'r', encoding='utf-8') as f:
                exec(f.read(), {}, color_dict_vars)
        except Exception as e:
            self.report({'ERROR'}, f"读取颜色字典失败: {e}")
            return {'CANCELLED'}
            
        target_colors = {} 
        
        dicts_to_check = [
            "cube_dict", 
            "slab_dict", 
            "slab_top_dict"
        ]
        
        for d_name in dicts_to_check:
            if d_name in color_dict_vars:
                for name, color in color_dict_vars[d_name].items():
                    rgb = tuple(color[:3])
                    if rgb not in target_colors:
                        target_colors[rgb] = name

        if not target_colors:
            self.report({'ERROR'}, "颜色字典为空或无效")
            return {'CANCELLED'}

        # KDTree algorithm is necessary here to perform efficient nearest-neighbor search 
        # in 3D RGB space for potentially hundreds of thousands of vertices.
        kd = KDTree(len(target_colors))
        color_list = list(target_colors.keys()) 
        for i, color in enumerate(color_list):
            kd.insert(Vector(color), i)
        kd.balance()

        text_data = bpy.data.texts.get("Blocks.py")
        if not text_data:
            self.report({'ERROR'}, "未找到 Blocks.py 映射表，请确保插件已正确初始化")
            return {'CANCELLED'}
        
        try:
            name_to_id_map = eval(text_data.as_string()) 
        except:
             self.report({'ERROR'}, "Blocks.py 格式错误")
             return {'CANCELLED'}

        cached_ids = []
        for rgb in color_list:
            name = target_colors[rgb]
            if name in name_to_id_map:
                cached_ids.append(name_to_id_map[name])
            else:
                cached_ids.append(0) 

        n_points = len(mesh.vertices)
        
        colors = np.zeros(n_points * 4, dtype=np.float32)
        try:
            color_attr.data.foreach_get("color", colors)
        except:
            self.report({'ERROR'}, "读取颜色数据失败，请确保颜色属性域正确")
            return {'CANCELLED'}
            
        colors = colors.reshape(n_points, 4)
        
        blockid_attr = mesh.attributes['blockid']
        blockid_values = np.zeros(n_points, dtype=np.int32)
        blockid_attr.data.foreach_get("value", blockid_values)
        
        change_count = 0
        for i in range(n_points):
            c = colors[i]
            target_vector = Vector((c[0], c[1], c[2]))
            
            _, index, _ = kd.find(target_vector)
            
            new_id = cached_ids[index]
            
            if new_id != 0 and blockid_values[i] != new_id:
                blockid_values[i] = new_id
                change_count += 1
                
        blockid_attr.data.foreach_set("value", blockid_values)
        
        mesh.update()
        obj.data.update() 
        
        duration = time.time() - start_time
        self.report({'INFO'}, f"应用完成: 更新了 {change_count} 个方块 (耗时 {duration:.2f}s)")
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MBM_OT_PaintBlock)

def unregister():
    bpy.utils.unregister_class(MBM_OT_PaintBlock)
