"""MBM_workflow 国际化模块"""
import bpy
import os

TRANSLATION_DOMAIN = "mbm_workflow"

def get_locales_path():
    """获取翻译文件路径"""
    addon_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(addon_dir, "i18n", "locales")

def register_translations():
    """注册翻译系统"""
    try:
        locales_path = get_locales_path()
        if os.path.exists(locales_path):
            bpy.app.translations.register(TRANSLATION_DOMAIN, locales_path)
            print(f"[MBM_workflow] 翻译系统已注册: {locales_path}")
        else:
            print(f"[MBM_workflow] 翻译目录不存在: {locales_path}")
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
