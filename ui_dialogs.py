import bpy

from .codes.block_map_store import load_block_map

class SchemImportPanel(bpy.types.Operator):
    bl_idname = "mbm.schem_import_panel"
    bl_label = "导入Schem文件二级界面"

    def execute(self, context):
        
        return {'FINISHED'}

    def invoke(self, context, event):
        # 弹出界面
        return context.window_manager.invoke_popup(self)
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row(align=True)    
        row.label(text="导入.schem选项界面",icon="EVENT_S")
        if context.scene.separate_vertices_by_chunk ==False:
            row = layout.row()    
            row.prop(scene, "separate_vertices_by_blockid",text="是否按照方块状态分离？")
        if context.scene.separate_vertices_by_blockid ==False:
            row = layout.row()    
            row.prop(scene, "separate_vertices_by_chunk",text="是否按照区块分离？")
        row = layout.row()
        row.operator("mbm.import_schem", text="导入.schem文件")

class ColorToBlockPanel(bpy.types.Operator):
    bl_idname = "mbm.color_to_block_panel"
    bl_label = "颜色方块对照表制作界面"

    def execute(self, context):
        
        return {'FINISHED'}

    def invoke(self, context, event):
        # 弹出界面
        return context.window_manager.invoke_props_dialog(self,width=450)
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        my_properties = scene.my_properties 
        
        
        row = layout.row()
        
        row.label(text="生成方块颜色对照表：")
        row.emboss="NONE_OR_STATUS"
        row.operator("mbm.open_color_dict",text="加载已有对照表")
        row = layout.row()
        row.operator("mbm.clear_color_dict",text="清除当前对照表")
        row = layout.row()
        row.template_list("ColorToBlockList", "", my_properties, "color_to_block_list", my_properties, "color_to_block_list_index")
        col = row.column()
        col.operator("mbm.add_color_to_block_operator",text="", icon='ADD')
        col.operator("mbm.delete_color_to_block_operator",text="", icon='REMOVE')
        row = layout.row()
        if my_properties.color_file_path=="":
            row.operator("mbm.make_color_dict", text="新建")
        else:
            row.operator("mbm.edit_color_dict", text="编辑")
        row = layout.row()


class SwitchBlocks(bpy.types.Operator):
    bl_idname = "mbm.switch_blocks_panel"
    bl_label = "替换方块界面"

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene
        my_properties = scene.my_properties
        # 假设你已经选择了包含几何节点组的对象
        obj = bpy.context.active_object
        if obj is None:
            self.report({'WARNING'}, "物体未选中")
            return {'CANCELLED'}
        # 获取几何节点树
        geometry_nodes = obj.modifiers.get("模型转换")
        if geometry_nodes is None:
            self.report({'WARNING'}, "仅有 '模型转换' 几何节点激活时可行")
            return {'CANCELLED'}
        node_group = geometry_nodes.node_group
        for node in node_group.nodes:
            if node.name == 'SwitchBlock':
                switch=node
                switch.inputs[0].default_value = False
        # 打印选中的物体
        selected_objects = bpy.context.selected_objects
        # 尝试从 .blend 文件中获取文本数据
        text_data = bpy.data.texts.get("Blocks.py")
        if not text_data:  # 如果文本数据不存在，则创建一个新的文本数据对象
            return {'CANCELLED'}
        
        # 读取字典 id_map
        block_id_name_map = load_block_map(text_data)

        # 使用集合来存储不重复的 blockid
        unique_blockids = set()

        for obj in selected_objects:
            if obj.type == 'MESH':
                # 检查是否存在名为“模型转换”的修改器
                has_modifier = False
                for modifier in obj.modifiers:
                    if modifier.name == '模型转换':
                        has_modifier = True
                        break
                    

                if has_modifier:
                    depsgraph = bpy.context.evaluated_depsgraph_get()
                    obj_evaluated = bpy.context.active_object.evaluated_get(depsgraph)

                    # 检查 'blockid' 属性是否存在并且不为空
                    if 'blockid' in obj_evaluated.data.attributes and obj_evaluated.data.attributes['blockid'].data:
                        # 获取 'blockid' 属性列表
                        blockid_attr = obj_evaluated.data.attributes['blockid'].data

                        # 将不重复的 blockid 存入集合
                        for item in blockid_attr:
                            try:
                                blockid = item.value  # 获取blockid属性值
                            except:
                                blockid = 0
                            if blockid != 0:
                                unique_blockids.add(blockid)

                    continue
                elif not has_modifier:
                    mesh = obj.data

                    # 将不重复的 blockid 存入集合
                    for vertex in mesh.vertices:
                        try:
                            blockid = obj.data.attributes['blockid'].data[vertex.index].value
                        except:
                            blockid = 0
                        if blockid != 0:
                            unique_blockids.add(blockid)

        my_properties.switch_block_list.clear()
        for blockid in unique_blockids:
            item = my_properties.switch_block_list.add()
            item.id = blockid
            item.target_id = blockid
            item.target_block_enum = str(blockid)

            # 根据 blockid 找到对应的名称
            block_name = None
            for name, id in block_id_name_map.items():
                if id == blockid:
                    block_name = name
                    break
            
            if block_name is not None:
                item.name = block_name
            else:
                item.name = "Unknown"
        switch.inputs[0].default_value = True
        # 弹出界面
        return context.window_manager.invoke_props_dialog(self, width=450)
    def draw(self,context):
        layout = self.layout
        scene = context.scene
        my_properties = scene.my_properties 
        
        
        row = layout.row()
        
        row.label(text="方块切换界面：")
        row.emboss="NONE_OR_STATUS"
        row.operator("mbm.open_color_dict",text="刷新")
        row = layout.row()
        row.template_list("SwitchBlockList", "", my_properties, "switch_block_list", my_properties, "switch_block_list_index")
        row = layout.row()
        #row.operator("mbm.make_color_dict", text="准备（第一次需要按一下）")
        #row = layout.row()
