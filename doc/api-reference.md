# API 参考手册 (API Reference)

本文档列出了 MBM-workflow 插件的核心 Python API，供开发者进行扩展或脚本编写使用。

## 1. 核心模块: `schem`
位于 `codes/schem.py`。处理核心的点云生成逻辑。

### `schem(filepath, origin, separate_by_blockid, separate_by_chunk)`
主导入函数。
- **参数**:
  - `filepath` (str): `.schem` 或 `.litematic` 文件绝对路径。
  - `origin` (tuple): `(x, y, z)` 导入位置（Blender 坐标）。
  - `separate_by_blockid` (bool): 是否按方块 ID 拆分对象。
  - `separate_by_chunk` (bool): 是否按区块拆分。
- **返回**: 生成的 Blender 对象列表。

---

## 2. 核心模块: `register`
位于 `codes/register.py`。负责方块注册系统。

### `register_blocks(ids)`
将 Minecraft 方块 ID 注册到 Blender 系统中。
- **参数**:
  - `ids` (list): 方块状态字符串列表 (e.g., `["minecraft:stone", "minecraft:oak_log[axis=x]"]`)。
- **作用**: 
  1. 解析 blockstate JSON。
  2. 创建对应的 3D 模型。
  3. 更新全局 `id_map` 字典。

---

## 3. 核心模块: `exportfile`
位于 `codes/exportfile.py`。

### `export_schem(objects, filepath)`
导出函数。
- **参数**:
  - `objects` (list): 要导出的 Blender 对象列表。
  - `filepath` (str): 目标 `.schem` 路径。
- **要求**: 对象必须包含有效的 `blockid` 顶点属性。

---

## 4. 功能模块: `mesh_to_mc`
位于 `codes/functions/mesh_to_mc.py`。

### `set_modifier_socket_value(modifier, socket_identifier, fallback_name, value, is_input=True)`
**[关键]** 兼容 Blender 5.0+ 的几何节点属性设置函数。
- **参数**:
  - `modifier`: 几何节点修改器实例。
  - `socket_identifier` (str): Socket 的内部 ID。
  - `fallback_name` (str): Socket 显示名称（用于回退查找）。
  - `value`: 要设置的值（Float, Vector, etc.）。
  - `is_input` (bool): `True` 设置输入，`False` 设置输出名称。

---

## 5. 工具模块: `block`
位于 `codes/block.py`。

### `block(...)`
创建一个单独的方块网格。
- **参数**:
  - `textures` (dict): 纹理路径字典。
  - `elements` (list): 模型元素定义（来自 JSON）。
  - `position` (tuple): 放置位置。
  - `rot` (tuple): 旋转角度。

---

## 6. 属性访问

### 获取版本配置
```python
from codes.property import get_mc_version
platform, version = get_mc_version(bpy.context)
# 返回: ("java", (1, 20, 1))
```

### 访问方块 ID 映射
```python
import bpy
text_data = bpy.data.texts.get("Blocks.py")
id_map = eval(text_data.as_string())
# 返回: {'minecraft:stone': 1, ...}
```
