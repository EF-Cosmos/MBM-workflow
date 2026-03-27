import bpy
import os

from ..i18n.translations import operator_label as _t

# ──────────────────────────────────────────────
# 预览缓存（模块级单例）
# ──────────────────────────────────────────────

_pcoll = None  # bpy.utils.previews.ImagePreviewCollection
_block_preview_map = {}  # {str(enum_id): icon_id}

MAX_RECENT = 20
MAX_FAVORITES = 50


def _get_block_texture_path(block_obj):
    """从方块对象的材质中提取 '默认图片' 节点的纹理文件路径。"""
    if not block_obj or block_obj.type != "MESH":
        return None
    mesh = block_obj.data
    if not mesh.materials:
        return None
    mat = mesh.materials[0]
    if not mat or not mat.use_nodes:
        return None
    tree = mat.node_tree
    if not tree:
        return None
    for node in tree.nodes:
        if node.name == "默认图片":
            if node.image and node.image.filepath_raw:
                raw = bpy.path.abspath(node.image.filepath_raw)
                if os.path.isfile(raw):
                    return raw
    return None


def _ensure_previews_loaded(context):
    """懒加载所有方块的纹理预览图标。仅在首次调用时执行。"""
    global _pcoll, _block_preview_map

    if _pcoll is not None:
        return

    _pcoll = bpy.utils.previews.new()
    collection = bpy.data.collections.get("Blocks")
    if not collection:
        return

    for obj in collection.objects:
        if "#" not in obj.name:
            continue
        enum_id = obj.name.split("#", 1)[0]

        texture_path = _get_block_texture_path(obj)
        if texture_path:
            try:
                _pcoll.load(enum_id, texture_path, "IMAGE")
                _block_preview_map[enum_id] = _pcoll[enum_id].icon_id
            except Exception:
                pass


def get_preview_icon_id(enum_id):
    """返回指定方块 ID 的图标 ID，无图标则返回 0。"""
    return _block_preview_map.get(enum_id, 0)


def clear_previews():
    """注销时清理预览缓存，释放 GPU 内存。"""
    global _pcoll, _block_preview_map
    if _pcoll:
        bpy.utils.previews.remove(_pcoll)
        _pcoll = None
        _block_preview_map = {}


# ──────────────────────────────────────────────
# 收藏夹和最近使用管理
# ──────────────────────────────────────────────

def _add_to_recent(block_id):
    """将方块添加到最近使用列表头部。"""
    my_props = bpy.context.scene.my_properties
    current = my_props.palette_recent_blocks
    items = current.split("|") if current else []
    if block_id in items:
        items.remove(block_id)
    items.insert(0, block_id)
    items = items[:MAX_RECENT]
    my_props.palette_recent_blocks = "|".join(items)


def _toggle_favorite(block_id):
    """切换方块的收藏状态。"""
    my_props = bpy.context.scene.my_properties
    current = my_props.palette_favorites
    items = current.split("|") if current else []
    if block_id in items:
        items.remove(block_id)
    else:
        items.insert(0, block_id)
        items = items[:MAX_FAVORITES]
    my_props.palette_favorites = "|".join(items)


def _is_favorited(block_id):
    """查询方块是否已收藏。"""
    my_props = bpy.context.scene.my_properties
    current = my_props.palette_favorites
    return block_id in (current.split("|") if current else [])


# ──────────────────────────────────────────────
# 操作符
# ──────────────────────────────────────────────

class MBM_OT_PaletteSelectBlock(bpy.types.Operator):
    bl_idname = "mbm.palette_select_block"
    bl_label = _t("选择方块")
    bl_options = {"INTERNAL"}

    block_id: bpy.props.StringProperty(options={"HIDDEN"})

    def execute(self, context):
        my_props = context.scene.my_properties
        try:
            my_props.brush_block_enum = self.block_id
        except (TypeError, ValueError):
            self.report({"WARNING"}, f"无效的方块 ID: {self.block_id}")
            return {"CANCELLED"}

        _add_to_recent(self.block_id)

        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()

        return {"FINISHED"}


class MBM_OT_PaletteToggleFavorite(bpy.types.Operator):
    bl_idname = "mbm.palette_toggle_favorite"
    bl_label = _t("切换收藏")
    bl_options = {"INTERNAL"}

    block_id: bpy.props.StringProperty(options={"HIDDEN"})

    def execute(self, context):
        _toggle_favorite(self.block_id)

        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()

        return {"FINISHED"}


# ──────────────────────────────────────────────
# 注册
# ──────────────────────────────────────────────

classes = [
    MBM_OT_PaletteSelectBlock,
    MBM_OT_PaletteToggleFavorite,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    clear_previews()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
