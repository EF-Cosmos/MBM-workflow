"""翻译辅助函数"""
import bpy

def _get_translation(msgctxt, message):
    """内部翻译查找函数"""
    if msgctxt:
        # Blender 使用 context|message 格式查找翻译
        key = f"{msgctxt}|{message}"
        translated = bpy.app.translations.pgettext_iface(key)
        # 如果翻译后仍然是 key，说明没有找到翻译
        if "|" in translated and translated.startswith(msgctxt):
            return message
        return translated
    return bpy.app.translations.pgettext_iface(message)

def panel_label(message):
    """翻译面板标签 - 直接调用 Blender 翻译"""
    return _get_translation("Panel", message)

def operator_label(message):
    """翻译操作符标签 - 直接调用 Blender 翻译"""
    return _get_translation("Operator", message)

def property_name(message):
    """翻译属性名称 - 直接调用 Blender 翻译"""
    return _get_translation("Property", message)

def enum_item(identifier, name, description=""):
    """翻译枚举项"""
    context = "Enum|" + str(identifier)
    return (
        identifier,
        _get_translation(context, name),
        _get_translation(context, description)
    )

def ui_list_label(message):
    """翻译 UIList 标签 - 直接调用 Blender 翻译"""
    return _get_translation("UIList", message)
