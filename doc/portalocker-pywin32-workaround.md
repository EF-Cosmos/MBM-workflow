# Portalocker pywin32 依赖绕过方案

本文档记录了 portalocker 3.2.0 在 Windows 上对 pywin32 的依赖问题及其解决方案。

---

## 问题描述

### 错误信息

```
ImportError: pywintypes is required for Win32Locker but not found. Please install pywin32.
```

### 根本原因

Portalocker 3.2.0 的 `MsvcrtLocker` 类在初始化时会创建 `Win32Locker` 实例：

```python
# portalocker/portalocker.py:186-197
class MsvcrtLocker(BaseLocker):
    _win32_locker: Win32Locker

    def __init__(self) -> None:
        self._win32_locker = Win32Locker()  # <- 这里触发 pywin32 导入
```

即使只想使用 `msvcrt.locking()` 进行独占锁，也会因为初始化 `Win32Locker` 而失败。

### 为什么存在这个依赖

Portalocker 在 Windows 上支持两种锁定方法：

1. **Win32 API** (`LockFileEx/UnlockFileEx`) - 需要 `pywin32`
   - 支持独占锁和共享锁
   - 更完整的实现

2. **msvcrt.locking()** - Windows CRT 内置
   - 仅支持独占锁
   - 无需额外依赖

`MsvcrtLocker` 使用 `msvcrt.locking()` 处理独占锁，但仍然需要 `Win32Locker` 来处理共享锁场景。

---

## 解决方案：Monkey Patch

### 为什么选择 Monkey Patch

| 方案 | 优点 | 缺点 |
|------|------|------|
| 添加 pywin32 wheel | 最直接 | 增加 ~1.2MB 依赖大小 |
| **Monkey Patch** | 零额外依赖，代码修改小 | 需要在导入前执行 |
| 替换为 filelock | 纯 Python | 需要验证兼容性 |

对于 MBM-workflow 的使用场景（schem 文件导入/导出），只需要独占锁，共享锁功能不是必需的。因此使用 Monkey Patch 方案是最优选择。

---

## 实施细节

### 修改文件

`codes/dependency_manager.py`

### 修改位置

在文件顶部，`import sys` 之后，`import bpy` 之前添加以下代码：

```python
# ============================================================================
# Portalocker Monkey Patch - 绕过 pywin32 依赖
# ============================================================================

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
```

---

## 工作原理

### 原始流程

```
MsvcrtLocker.__init__()
    └── Win32Locker.__init__()
            └── import pywintypes  <- 失败！
```

### Patch 后流程

```
MsvcrtLocker.__init__() [patched]
    ├── _DummyWin32Locker()  <- 虚拟对象，无需 pywin32
    └── msvcrt 常量设置
```

---

## 功能影响

| 功能 | 影响 | 说明 |
|------|------|------|
| 独占锁 (LOCK_EX) | ✅ 正常工作 | 使用 `msvcrt.locking()` |
| 共享锁 (LOCK_SH) | ⚠️ 降级为无锁 | 虚拟 Win32Locker 的 lock() 为空操作 |
| 非阻塞锁 | ✅ 正常工作 | 独占锁支持非阻塞模式 |

对于 MBM-workflow 的 schem 文件操作，通常只使用独占锁，因此这个影响可以接受。

---

## 验证

在 Blender 中测试以下操作：

1. 重载插件
2. 导入一个 .schem 文件
3. 检查控制台不再有 pywin32 错误

```python
# Blender Python 控制台测试代码
import portalocker.portalocker as pl
locker = pl.MsvcrtLocker()
print(f'Win32Locker type: {type(locker._win32_locker).__name__}')
# 输出: Win32Locker type: _DummyWin32Locker
```

---

## 相关问题

### Q: 为什么不直接添加 pywin32？

A: pywin32 包大小约 1.2MB，包含大量 Windows API 绑定，而 portalocker 只使用了其中一小部分。对于单功能插件来说，这个依赖负担过重。

### Q: 共享锁降级会有问题吗？

A: schem 文件的导入/导出通常是单线程操作，不需要共享锁。如果将来需要并发读取，可以考虑添加 pywin32 或使用其他锁定机制。

### Q: 未来 portalocker 更新会受影响吗？

A: Monkey Patch 依赖 portalocker 的内部实现。如果 portalocker 重大重构（如 `MsvcrtLocker` 类名或结构变化），需要相应调整 patch 代码。

---

## 参考资料

- Portalocker 源码: https://github.com/dannyzb/portalocker
- Blender 5.0+ 依赖管理: `doc/dependency-update-guide.md`
- 项目依赖配置: `blender_manifest.toml`
