import bpy

# 翻译支持
from bpy.app.translations import pgettext_iface as _
from .i18n.translations import ui_list_label

# -----------------------------------------------------------------------------
# UIList
# -----------------------------------------------------------------------------

class MBM_UL_resourcepack_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name)

# 定义 UIList 类 ColorToBlockList
class MBM_UL_color_to_block_list(bpy.types.UIList):
    def draw_item(self, _context, layout, _data, item, icon, _active_data, _active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            my_properties = bpy.context.scene.my_properties
            row = layout.row()
            split = row.split(factor=0.65)
             # 字符串映射字典（使用翻译）
            type_mapping = {
                -1: ui_list_label("自动"),
                0: ui_list_label("方块"),
                1: ui_list_label("台阶"),
                2: ui_list_label("楼梯"),
            }
            type_string = type_mapping.get(item.type, "Undefined")
            split.row().prop(item, "name", text="", emboss=False)
            if my_properties.color_file_path!="":
                split.row().prop(item, "color", text="")
            if my_properties.color_file_path=="":
                split.row().prop(item, "type", text="", emboss=False)
            split.row().label(text=type_string)
# 定义 UIList 类 ModList
class MBM_UL_mod_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # 显示模组名称、图标和描述
            row = layout.row(align=True)
            row.label(text=item.name)
            row.label(text=item.description)

# 定义 UIList 类 SwitchBlockList
class MBM_UL_switch_block_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # 显示模组名称、图标和描述
            split = layout.split()
            row = split.row()
            row.label(text=str(item.id)+"#"+item.name)
            row = layout.row(align=True)
            #row.label(text=item.name)
            split = row.split(factor=0.65)
            split.row().prop(item, "target_block_enum", text="")
