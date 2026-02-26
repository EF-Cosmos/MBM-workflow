"""翻译辅助函数"""
import bpy

# 翻译域常量
TRANSLATION_DOMAIN = "mbm_workflow"

def iface_(msgctxt, message):
    """带上下文的界面翻译

    使用 Blender 的翻译 API 查找翻译。
    如果翻译不存在，返回原始消息。
    """
    if msgctxt:
        # 构造上下文键：context|message
        key = f"{msgctxt}|{message}"
        # 从 Blender 的翻译字典中查找
        trans_dict = bpy.app.translations.translations.get(TRANSLATION_DOMAIN, {})
        # 查找当前语言的翻译
        for lang_dict in trans_dict.values():
            if key in lang_dict:
                return lang_dict[key]
        # 使用 Blender 的内置翻译机制
        translated = bpy.app.translations.pgettext_iface(key)
        # 如果翻译后仍然是 key 格式，说明没有找到翻译，返回原始消息
        if translated == key:
            return message
        return translated
    return bpy.app.translations.pgettext_iface(message)

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
