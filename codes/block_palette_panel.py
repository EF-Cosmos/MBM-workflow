import bpy

from ..i18n.translations import panel_label
from .block_palette import (
    _ensure_previews_loaded,
    get_preview_icon_id,
)
from .property import get_block_items

ITEMS_PER_PAGE = 40
COLUMNS = 8


def _get_filtered_block_items(context):
    """根据搜索条件返回过滤后的方块列表。"""
    my_props = context.scene.my_properties
    block_items = get_block_items(None, context)

    search = my_props.palette_search.lower()
    if search:
        block_items = [
            item for item in block_items
            if search in item[1].lower() or search in item[0]
        ]
    return block_items


class MBM_PT_block_palette(bpy.types.Panel):
    bl_label = panel_label("方块调色板")
    bl_idname = "MBM_PT_block_palette"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_edit_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        my_props = context.scene.my_properties

        # 检查是否已导入方块
        if not bpy.data.collections.get("Blocks"):
            layout.label(text="尚未导入方块", icon="ERROR")
            layout.operator("mbm.import_block", text="导入方块", icon="IMPORT")
            return

        # 确保预览已加载
        _ensure_previews_loaded(context)
        
        # ── 获取过滤后的方块列表 ──
        block_items = _get_filtered_block_items(context)
        current_enum = my_props.brush_block_enum

        # ── 顶部：显示当前选中的方块名称 ──
        selected_name = "未选择"
        for item in block_items:
            if item[0] == current_enum:
                selected_name = item[1]
                break
        
        box = layout.box()
        box.label(text=f"当前选择: {selected_name}", icon='RESTRICT_SELECT_OFF')

        # ── 搜索框 ──
        row = layout.row()
        row.prop(my_props, "palette_search", text="", icon="VIEWZOOM")

        # ── 分页 ──
        total = len(block_items)
        page = my_props.palette_page
        max_page = max(0, (total - 1) // ITEMS_PER_PAGE) if total > 0 else 0

        if page > max_page:
            page = max_page

        start = page * ITEMS_PER_PAGE
        end = min(start + ITEMS_PER_PAGE, total)
        page_items = block_items[start:end]

        # ── 分页导航 ──
        row = layout.row(align=True)
        row.label(text=f"{start + 1}-{end} / {total}")
        sub1 = row.row(align=True)
        sub1.enabled = page > 0
        sub1.operator("mbm.palette_page_prev", text="", icon="TRIA_LEFT")
        sub2 = row.row(align=True)
        sub2.enabled = page < max_page
        sub2.operator("mbm.palette_page_next", text="", icon="TRIA_RIGHT")

        # ── 纯图标方块网格 ──
        col = layout.column(align=True)
        for i in range(0, len(page_items), COLUMNS):
            row = col.row(align=True)
            for j in range(COLUMNS):
                if i + j < len(page_items):
                    enum_id, name, desc = page_items[i + j]
                    icon_id = get_preview_icon_id(enum_id)
                    is_active = (enum_id == current_enum)

                    if icon_id:
                        props = row.operator(
                            "mbm.palette_select_block",
                            text="",
                            depress=is_active,
                            icon_value=icon_id,
                        )
                    else:
                        props = row.operator(
                            "mbm.palette_select_block",
                            text="",
                            depress=is_active,
                            icon="BLANK1",
                        )
                    props.block_id = enum_id
                else:
                    # 填充空白部分以保持对齐和宽度一致
                    row.label(text="", icon="BLANK1")

class MBM_OT_PalettePagePrev(bpy.types.Operator):
    bl_idname = "mbm.palette_page_prev"
    bl_label = ""
    bl_options = {"INTERNAL"}

    def execute(self, context):
        my_props = context.scene.my_properties
        total = len(_get_filtered_block_items(context))
        max_page = max(0, (total - 1) // ITEMS_PER_PAGE) if total > 0 else 0
        current = min(my_props.palette_page, max_page)
        my_props.palette_page = max(0, current - 1)
        return {"FINISHED"}


class MBM_OT_PalettePageNext(bpy.types.Operator):
    bl_idname = "mbm.palette_page_next"
    bl_label = ""
    bl_options = {"INTERNAL"}

    def execute(self, context):
        my_props = context.scene.my_properties
        total = len(_get_filtered_block_items(context))
        max_page = max(0, (total - 1) // ITEMS_PER_PAGE) if total > 0 else 0
        my_props.palette_page = min(my_props.palette_page + 1, max_page)
        return {"FINISHED"}


classes = [
    MBM_PT_block_palette,
    MBM_OT_PalettePagePrev,
    MBM_OT_PalettePageNext,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
