"""
统一的依赖管理和安全导入模块 (Blender 5.0+)

提供安全导入接口和依赖检查功能，确保插件在依赖缺失时优雅降级而非崩溃。
"""
import sys
import bpy


class DependencyManager:
    """
    依赖管理器，提供安全导入接口

    负责检查插件所需依赖是否可用，并提供友好的错误提示。
    """

    # 核心依赖列表
    REQUIRED_DEPS = {
        'amulet': 'Minecraft 世界解析',
        'amulet_nbt': 'NBT 数据格式',
    }

    # 可选依赖
    OPTIONAL_DEPS = {
        'numpy': '数组计算优化',
    }

    @classmethod
    def check_dependencies(cls):
        """
        检查所有必需依赖是否可用

        Returns:
            list: 缺失的依赖列表，格式为 [(name, description), ...]
        """
        missing = []
        for name, desc in cls.REQUIRED_DEPS.items():
            if not cls._is_available(name):
                missing.append((name, desc))
        return missing

    @classmethod
    def check_optional_dependencies(cls):
        """
        检查可选依赖是否可用

        Returns:
            list: 缺失的可选依赖列表
        """
        missing = []
        for name, desc in cls.OPTIONAL_DEPS.items():
            if not cls._is_available(name):
                missing.append((name, desc))
        return missing

    @classmethod
    def _is_available(cls, module_name):
        """
        检查模块是否可导入

        Args:
            module_name: 模块名称

        Returns:
            bool: 是否可用
        """
        try:
            __import__(module_name)
            return True
        except ImportError:
            return False

    @classmethod
    def safe_import(cls, module_name, fallback=None):
        """
        安全导入，失败时返回 fallback 或 None

        Args:
            module_name: 要导入的模块名称
            fallback: 导入失败时的返回值

        Returns:
            模块对象或 fallback
        """
        try:
            return __import__(module_name)
        except ImportError:
            if fallback is not None:
                return fallback
            return None

    @classmethod
    def show_dependency_error(cls, missing):
        """
        显示友好的依赖缺失错误

        Args:
            missing: 缺失的依赖列表，格式为 [(name, description), ...]
        """
        msg = "缺少以下必需依赖：\n\n"
        for name, desc in missing:
            msg += f"  • {name} - {desc}\n"
        msg += "\n请通过 Blender 扩展偏好设置重新安装插件"
        cls._show_popup("依赖缺失", msg, 'ERROR')

    @classmethod
    def show_optional_warning(cls, missing):
        """
        显示可选依赖缺失警告

        Args:
            missing: 缺失的可选依赖列表
        """
        if not missing:
            return
        msg = "以下可选依赖不可用（部分功能可能受限）：\n\n"
        for name, desc in missing:
            msg += f"  • {name} - {desc}\n"
        cls._show_popup("可选依赖缺失", msg, 'WARNING')

    @classmethod
    def _show_popup(cls, title, message, icon='INFO'):
        """
        显示 Blender 弹窗

        Args:
            title: 弹窗标题
            message: 弹窗消息
            icon: 图标类型
        """
        def draw(self, context):
            layout = self.layout
            for line in message.split('\n'):
                layout.label(text=line)

        bpy.types.Operator.cls = type(
            'DependencyError',
            (bpy.types.Operator,),
            {
                'bl_idname': 'wm.dependency_error',
                'bl_label': title,
                'bl_description': message,
                'bl_options': {'REGISTER'},
                'execute': lambda self, context: {'CANCELLED'},
                'invoke': lambda self, context, event: context.window_manager.invoke_popup(self),
                'draw': draw
            }
        )
        try:
            bpy.ops.wm.dependency_error()
        except Exception:
            # 如果弹窗失败，在控制台输出
            print(f"[{title}] {message}")


# 提供全局导入接口
# 所有模块应该从这里导入依赖，而不是直接 import
amulet = DependencyManager.safe_import('amulet')
amulet_nbt = DependencyManager.safe_import('amulet_nbt')
numpy = DependencyManager.safe_import('numpy', fallback=None)


def require_amulet():
    """
    装饰器：确保函数在使用前检查 amulet 依赖

    Usage:
        @require_amulet()
        def my_function():
            # 使用 amulet
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if amulet is None:
                print("警告：amulet 依赖不可用，无法执行该操作")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
