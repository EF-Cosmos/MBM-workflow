"""
统一的依赖管理和安全导入模块 (Blender 5.0+)

提供安全导入接口和依赖检查功能，确保插件在依赖缺失时优雅降级而非崩溃。
"""
import sys

# ============================================================================
# Portalocker Monkey Patch - 绕过 pywin32 依赖
# ============================================================================
# Portalocker 3.2.0 的 MsvcrtLocker 在初始化时会创建 Win32Locker 实例，
# 而 Win32Locker 需要 pywin32。由于我们的使用场景不需要共享锁，
# 可以用虚拟的 Win32Locker 替代。

def _patch_portalocker():
    """
    修补 portalocker，移除对 pywin32 的依赖

    MsvcrtLocker 对独占锁使用 msvcrt.locking()，不需要 Win32 API。
    只有共享锁才需要 Win32Locker，而 Minecraft schem 导入/导出
    通常不需要共享锁。
    """
    try:
        import portalocker.portalocker as pl_module
    except ImportError:
        # portalocker 不可用，无需 patch
        return

    class _DummyWin32Locker:
        """虚拟 Win32Locker，避免 pywin32 依赖"""
        def lock(self, *args, **kwargs):
            # 共享锁请求时静默失败，回退到无锁行为
            pass

        def unlock(self, *args, **kwargs):
            pass

    def _patched_msvcrt_init(self):
        """
        MsvcrtLocker 的修补初始化方法

        不创建真正的 Win32Locker 实例，避免 pywin32 导入。
        """
        import msvcrt

        # 用虚拟对象替代 Win32Locker
        self._win32_locker = _DummyWin32Locker()

        # 设置 msvcrt 锁定常量（来自原始代码）
        attrs = ['LK_LOCK', 'LK_RLCK', 'LK_NBLCK', 'LK_UNLCK', 'LK_NBRLCK']
        defaults = [0, 1, 2, 3, 2]
        for attr, default_val in zip(attrs, defaults):
            if not hasattr(msvcrt, attr):
                setattr(msvcrt, attr, default_val)

    # 应用 patch
    pl_module.MsvcrtLocker.__init__ = _patched_msvcrt_init

# 在模块导入时立即执行 patch
_patch_portalocker()
# ============================================================================

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
        """
        def draw(self, context):
            layout = self.layout
            for line in message.split('\n'):
                layout.label(text=line)

        # 动态修改 Operator 的属性以显示不同的消息
        # 注意：这在多线程或频繁调用时可能不安全，但用于模态弹窗通常可以接受
        BAIGAVE_OT_DependencyError.bl_label = title
        BAIGAVE_OT_DependencyError.message = message
        BAIGAVE_OT_DependencyError.draw_func = draw
        
        # 强制更新类注册以应用新标签（可选，但通常 invoke 会处理）
        try:
            bpy.utils.unregister_class(BAIGAVE_OT_DependencyError)
            bpy.utils.register_class(BAIGAVE_OT_DependencyError)
        except:
            pass
            
        try:
            bpy.ops.wm.dependency_error('INVOKE_DEFAULT')
        except Exception as e:
            print(f"[{title}] {message}")
            print(f"Popup error: {e}")


class BAIGAVE_OT_DependencyError(bpy.types.Operator):
    bl_idname = "wm.dependency_error"
    bl_label = "Dependency Error"
    bl_description = "Show dependency error"
    bl_options = {'REGISTER', 'INTERNAL'}
    
    message = "Error"
    draw_func = None

    def execute(self, context):
        return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

    def draw(self, context):
        if hasattr(self, 'draw_func') and self.draw_func:
            self.draw_func(self, context)
        elif hasattr(self.__class__, 'draw_func') and self.__class__.draw_func:
            self.__class__.draw_func(self, context)
        else:
            layout = self.layout
            layout.label(text=self.message)

def register():
    try:
        bpy.utils.register_class(BAIGAVE_OT_DependencyError)
    except ValueError:
        pass

def unregister():
    try:
        bpy.utils.unregister_class(BAIGAVE_OT_DependencyError)
    except:
        pass


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
