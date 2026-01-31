# 故障排除指南 (Troubleshooting Guide)

本文档旨在帮助用户和开发者解决在使用 MBM-workflow 插件时遇到的常见问题。

## 目录

1. [安装与依赖问题](#1-安装与依赖问题)
2. [版本兼容性问题](#2-版本兼容性问题)
3. [导入/导出问题](#3-导入导出问题)
4. [几何节点与显示问题](#4-几何节点与显示问题)
5. [性能问题](#5-性能问题)

---

## 1. 安装与依赖问题

### 错误：`ModuleNotFoundError: No module named 'amulet'`
**现象**：启用插件或运行脚本时报错，提示找不到 amulet 或其他库。

**原因**：
- Blender 5.0+ 尚未下载完依赖包。
- `blender_manifest.toml` 配置有误。
- 网络连接导致 pip 下载失败。

**解决方案**：
1. **等待自动安装**：首次启用插件时，Blender 会在后台下载依赖。请留意 Blender 底部状态栏的进度。
2. **检查控制台**：打开 `Window > Toggle System Console` 查看 pip 安装日志。
3. **手动安装**：如果自动安装失败，请参考 `doc/dependency-update-guide.md` 手动下载 wheels 到 `wheels/` 目录。
4. **重启 Blender**：依赖安装完成后，必须重启 Blender 才能生效。

### 错误：`ImportError: pywintypes is required for Win32Locker`
**现象**：控制台报错，提示需要 pywin32。

**原因**：`portalocker` 库在 Windows 上默认依赖 pywin32，但在某些精简环境下可能缺失。

**解决方案**：
- 插件已内置 Monkey Patch (在 `codes/dependency_manager.py` 中) 绕过此问题。
- 确保插件版本是最新的。
- 如果你是开发者，请**不要**删除 `dependency_manager.py` 中的 `_patch_portalocker()` 函数调用。

---

## 2. 版本兼容性问题

### 警告：`Java 1.21.x 可能不支持`
**现象**：在控制台看到关于版本的警告信息。

**原因**：PyMCTranslate 库的更新速度可能滞后于 Minecraft 最新快照版本。当前 PyMCTranslate 1.2.39 最高支持 Java 1.21.9。

**解决方案**：
- 在插件面板 `Mod 设置` 中，尝试选择较低的稳定版本（如 1.20.4 或 1.21.1）进行转换，通常方块 ID 变化不大，可以兼容。
- 等待插件更新 PyMCTranslate 依赖。

### 错误：`KeyError: 'minecraft:xxx'`
**现象**：导入时某些方块变为粉黑格（缺失材质）或报错。

**原因**：
- 该方块在当前选择的 Minecraft 版本中不存在。
- 资源包中缺失该方块的模型或纹理。

**解决方案**：
- 确认 `Mod 设置` 中的版本与地图版本一致。
- 确保已正确加载所需的资源包（Resource Packs）。
- 使用 `重载失效方块` 按钮尝试重新读取。

---

## 3. 导入/导出问题

### 导入 .litematic 失败
**现象**：点击导入按钮无反应，或提示依赖缺失。

**原因**：`litemapy` 库未正确加载。

**解决方案**：
- 检查 `wheels/` 目录下是否有 `litemapy-*.whl`。
- 确认 Blender 控制台无导入错误。

### 导出时方块错位或朝向错误
**原因**：Minecraft 和 Blender 的坐标系差异导致（Y/Z 轴翻转）。

**解决方案**：
- 插件会自动处理坐标转换 `(x, z, -y)`。请确保**不要**手动旋转导入的对象后再导出，除非你明确知道自己在做什么。
- 如果必须旋转，请在导出前应用旋转 (`Ctrl+A > Rotation`)。

---

## 4. 几何节点与显示问题

### 错误：几何节点修改器无法通过脚本修改
**现象**：开发者在脚本中尝试修改 Socket 值时报错 `KeyError`。

**原因**：Blender 5.0 改变了修改器属性的访问方式。

**解决方案**：
使用插件提供的辅助函数 `set_modifier_socket_value`：
```python
from codes.functions.mesh_to_mc import set_modifier_socket_value
set_modifier_socket_value(modifier, 'Input_Name', 'Fallback', value)
```

### 材质显示为紫色（丢失）
**原因**：Blender 无法找到纹理路径。

**解决方案**：
- 检查 `Mod 设置` 面板中的资源包路径是否正确。
- 点击 `Mod 设置` -> `刷新` 按钮，重新解压和索引资源文件。
- 确保 `temp/` 目录有写入权限。

---

## 5. 性能问题

### 导入大型 Schem 文件时 Blender 卡死
**原因**：Python 单线程处理大量方块数据导致 UI 阻塞。

**解决方案**：
- 插件会自动对超过 1,000,000 方块的文件启用多进程处理。
- 确保 CPU 核心未被其他繁重任务占用。
- 在导入面板勾选 `按区块分离`，减少单个对象的顶点数量。

### 视口操作卡顿
**原因**：几何节点实例数量过多。

**解决方案**：
1. 导入后点击 `优化与动画` -> `执行优化`。
2. 使用 `合并重叠面` 功能减少不可见的面。
3. 在几何节点修改器中，暂时降低视口显示密度（如果节点组支持）。
