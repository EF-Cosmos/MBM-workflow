"""翻译辅助函数"""
import bpy
from bpy.app.translations import pgettext_iface

def iface_(msgctxt, message):
    """带上下文的界面翻译

    使用 Blender 的翻译 API 查找翻译。
    如果翻译不存在，返回原始消息。
    """
    if msgctxt:
        # 使用元组格式 (context, message) 查找翻译
        return bpy.app.translations.pgettext_iface((msgctxt, message))
    return pgettext_iface(message)

def panel_label(message):
    """翻译面板标签"""
    return iface_("Panel", message)

def operator_label(message):
    """翻译操作符标签"""
    return iface_("Operator", message)

def property_name(message):
    """翻译属性名称"""
    return iface_("Property", message)

def enum_item(identifier, name, description=""):
    """翻译枚举项"""
    context = "Enum|" + str(identifier)
    return (
        identifier,
        iface_(context, name),
        iface_(context, description)
    )

def ui_list_label(message):
    """翻译 UIList 标签"""
    return iface_("UIList", message)
