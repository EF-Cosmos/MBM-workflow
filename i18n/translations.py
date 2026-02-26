"""翻译辅助函数"""
import bpy
from bpy.app.translations import pgettext_iface as _

def iface_(msgctxt, message):
    """带上下文的界面翻译"""
    if msgctxt:
        return bpy.app.translations.pgettext_iface(msgctxt + "|" + message)
    return _(message)

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
    return (
        identifier,
        iface_("Enum|" + str(identifier), name),
        iface_("Enum|" + str(identifier), description)
    )

def ui_list_label(message):
    """翻译 UIList 标签"""
    return iface_("UIList", message)
