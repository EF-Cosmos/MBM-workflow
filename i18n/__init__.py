"""MBM_workflow 国际化模块"""
import bpy
import os
import re

TRANSLATION_DOMAIN = "mbm_workflow"

def get_locales_path():
    """获取翻译文件路径"""
    addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(addon_dir, "i18n", "locales")

def _parse_po_file(po_path):
    """解析 .po 文件，返回翻译字典"""
    translations = {}
    current_msgctxt = None
    current_msgid = None
    current_msgstr = None

    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # 解析 msgctxt
            if line.startswith('msgctxt '):
                match = re.match(r'msgctxt\s+"(.+)"', line)
                if match:
                    current_msgctxt = match.group(1)
                else:
                    current_msgctxt = ''

            # 解析 msgid
            elif line.startswith('msgid '):
                match = re.match(r'msgid\s+"(.*)"', line)
                if match:
                    current_msgid = match.group(1)
                else:
                    current_msgid = ''

            # 解析 msgstr
            elif line.startswith('msgstr '):
                match = re.match(r'msgstr\s+"(.*)"', line)
                if match:
                    current_msgstr = match.group(1)
                else:
                    current_msgstr = ''

            # 处理多行字符串
            elif line.startswith('"') and current_msgid is not None:
                match = re.match(r'"(.*)"', line)
                if match:
                    if current_msgstr is not None:
                        current_msgstr += match.group(1)

            # 当遇到空行时，保存当前翻译条目
            elif not line and current_msgid and current_msgstr:
                # 跳过元数据条目（msgid 为空）
                if current_msgid:
                    # Blender 翻译字典格式: (context, message) -> translation
                    key = (current_msgctxt or '', current_msgid)
                    translations[key] = current_msgstr
                current_msgctxt = None
                current_msgid = None
                current_msgstr = None

    return translations

def load_translations_dict():
    """从 .po 文件加载翻译字典"""
    translations = {}
    locales_path = get_locales_path()

    if not os.path.exists(locales_path):
        print(f"[MBM_workflow] 翻译目录不存在: {locales_path}")
        return translations

    for locale_name in os.listdir(locales_path):
        locale_dir = os.path.join(locales_path, locale_name)
        if not os.path.isdir(locale_dir):
            continue

        po_path = os.path.join(locale_dir, 'LC_MESSAGES', 'mbm_workflow.po')
        if os.path.exists(po_path):
            try:
                locale_translations = _parse_po_file(po_path)
                if locale_translations:
                    translations[locale_name] = locale_translations
                    print(f"[MBM_workflow] 加载翻译文件: {po_path} ({len(locale_translations)} 条)")
            except Exception as e:
                print(f"[MBM_workflow] 加载翻译文件失败 {po_path}: {e}")

    return translations

def register_translations():
    """注册翻译系统"""
    try:
        translations_dict = load_translations_dict()
        if translations_dict:
            bpy.app.translations.register(TRANSLATION_DOMAIN, translations_dict)
            print(f"[MBM_workflow] 翻译系统已注册: {list(translations_dict.keys())}")
        else:
            print("[MBM_workflow] 无翻译数据可注册")
    except Exception as e:
        print(f"[MBM_workflow] 翻译注册失败: {e}")

def unregister_translations():
    """注销翻译系统"""
    try:
        bpy.app.translations.unregister(TRANSLATION_DOMAIN)
        print("[MBM_workflow] 翻译系统已注销")
    except Exception as e:
        print(f"[MBM_workflow] 翻译注销失败: {e}")

def register():
    """模块注册入口"""
    register_translations()

def unregister():
    """模块注销入口"""
    unregister_translations()
