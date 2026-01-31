# 方块笔刷功能修复文档

## 概述

方块笔刷 (Block Brush) 是一个在 3D 视图中直接绘制方块的交互式工具。它允许用户在导入的点云对象上修改方块的 blockid 属性，几何节点会自动更新显示对应的方块模型�?

**文件位置**: `codes/functions/brush.py`

---

## 功能说明

### 使用场景

方块笔刷**仅在几何节点修改器未应用�?*有效。它直接操作点云数据（顶点的 blockid 属性），几何节点会实时响应这些变化�?

### 操作方式

| 按键 | 功能 |
|------|------|
| 左键 | 将选中的方块类型绘制到点击位置 |
| Shift + 左键 | 吸取点击位置的方�?ID |
| 右键 / ESC | 退出笔刷模�?|

### 前置条件

1. 选择一个带�?`blockid` 属性的点云对象
2. `blockid` 属性的�?(domain) 必须�?`POINT`
3. 属性数据不能为�?
4. 几何节点修改器必�?*未应�?*（可以存在，但不能应用）

---

## 修复历史

### 问题 1: TypeError - `__init__` 参数不匹�?

**错误信息**:
```
TypeError: MBM_OT_BlockBrush.__init__() takes 1 positional argument but 2 were given
```

**原因**: Blender 5.0+ �?`bpy.types.Operator` 基类在初始化时传递了额外参数，但子类只定义了 `__init__(self)`�?

**修复** (line 12):
```python
# 修复�?
def __init__(self):
    self.kd_tree = None
    self.target_obj = None

# 修复�?
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.kd_tree = None
    self.target_obj = None
```

---

### 问题 2: IndexError - 属性数据访问越�?

**错误信息**:
```
IndexError: bpy_prop_collection[index]: index 988 out of range, size 0
```

**根本原因**:

1. **属性数据未检�?*: 原代码只检查属性是否存在，未检查属性数据是否为�?
2. **ray_cast 索引不匹�?*:
   - `scene.ray_cast(depsgraph, ...)` �?evaluated 对象上执�?
   - 返回�?`index` 是实例化网格的索引，而非原始点云的索�?
   - KDTree 基于原始点云构建，两者索引不匹配

**数据流示�?*:
```
┌─────────────────�?    ┌──────────────────�?    ┌─────────────────�?
�? 原始点云对象    �?──�?�? 几何节点修改�?  �?──�?�? 实例化网�?     �?
�? (obj.data)     �?    �? (未应用状�?     �?    �? (evaluated)    �?
├─────────────────�?    ├──────────────────�?    ├─────────────────�?
�?�?vertices[]    �?    �? 读取 blockid     �?    �?�?vertices[]    �?
�?�?blockid.data  �?    �? 实例化方块模�?  �?    �?�?blockid.data  �?
└─────────────────�?    └──────────────────�?    └─────────────────�?
        �?                                               �?
        �?                                               �?
   KDTree 基于此构�?                         ray_cast 返回此索�?
   (正确的顶点索�?                              (错误的索�?)
```

---

## 修复详情

### 修复 1: 增强 invoke 方法检�?(line 35-60)

添加了完整的属性验证：

```python
# 1. 基础类型检�?
if not obj or obj.type != 'MESH':
    return {'CANCELLED'}

# 2. 属性存在性检�?
if 'blockid' not in obj.data.attributes:
    return {'CANCELLED'}

# 3. 属性域检�?
blockid_attr = obj.data.attributes['blockid']
if blockid_attr.domain != 'POINT':
    return {'CANCELLED'}

# 4. 属性数据非空检查（关键！）
if not blockid_attr.data or len(blockid_attr.data) == 0:
    self.report({'WARNING'}, "blockid 属性数据为空，可能已应用几何节点修改器")
    return {'CANCELLED'}
```

### 修复 2: 修正 brush_action 方法 (line 81-122)

**核心改动**: 使用原始对象进行 ray_cast，而非 evaluated 对象�?

```python
# 修复�?
depsgraph = context.evaluated_depsgraph_get()
result, location, normal, index, obj, matrix = scene.ray_cast(depsgraph, origin, direction)
# index �?evaluated 对象的索�?�?错误�?

# 修复�?
result, location, normal, index = self.target_obj.ray_cast(origin, direction, distance=1.70141e+38)
# index 是原始对象的索引 �?正确�?
```

**添加边界检�?*:
```python
blockid_data = self.target_obj.data.attributes['blockid'].data

if kd_index < len(blockid_data):
    blockid_data[kd_index].value = target_id
else:
    self.report({'WARNING'}, f"索引 {kd_index} 超出范围")
```

**正确的数据更新通知**:
```python
# 修复�?
self.target_obj.data.update()

# 修复�?
self.target_obj.data.update_tag()  # 触发几何节点重新计算
```

---

## 技术要�?

### 几何节点与点云的交互

1. **点云创建** (`codes/schem.py:126-130`):
   ```python
   mesh.from_pydata(vertices, [], [])  # 只有顶点，无�?�?
   mesh.attributes.new(name='blockid', type="INT", domain="POINT")
   ```

2. **几何节点读取**:
   - Schem 节点组读取每个顶点的 `blockid` 属�?
   - 根据 ID �?"Blocks" 集合实例化对应方�?

3. **实时更新机制**:
   - 修改 `blockid` 属性后调用 `update_tag()`
   - 几何节点自动检测到属性变�?
   - 重新执行实例化，显示新的方块

### ray_cast 的两种模�?

| 模式 | 方法 | 返回索引 | 适用场景 |
|------|------|----------|----------|
| 场景�?| `scene.ray_cast(depsgraph, ...)` | evaluated 对象索引 | 应用了修改器的网�?|
| 对象�?| `obj.ray_cast(origin, direction)` | 原始对象索引 | 未应用修改器的点�?|

---

## 验证步骤

1. 打开 Blender，加载插�?
2. 导入 `.schem` 文件（创建带几何节点修改器的点云对象�?
3. **确保几何节点修改器未应用**
4. 选择点云对象，点�?启动方块笔刷"
5. 测试以下操作�?
   - [ ] 左键点击方块（应更新显示�?
   - [ ] Shift+左键吸取方块 ID（应显示 ID 提示�?
   - [ ] 右键退出笔�?

---

## 常见问题

### Q: 为什么笔刷不能在应用了几何节点修改器的对象上使用�?

**A**: 应用修改器后，原始点云数据被转换为实际的网格几何体，`blockid` 属性数据不再存在或无法访问。笔刷需要直接操作点云属性才能工作�?

### Q: 笔刷修改后方块没有立即更新？

**A**: 确保�?
1. 几何节点修改器处于启用状态（眼睛图标�?
2. 对象�?`blockid` 属性域�?`POINT`
3. 使用�?`update_tag()` 而非 `update()`

### Q: 出现"索引超出范围"错误�?

**A**: 检查：
1. 对象是否应用了几何节点修改器
2. `blockid` 属性数据是否为空（�?Blender 属性面板中查看对象属�?�?属性）
3. KDTree 是否基于正确的顶点数据构�?

---

## 相关文件

- `codes/functions/brush.py` - 方块笔刷主逻辑
- `codes/schem.py` - 点云创建和属性设�?
- `codes/functions/paint.py` - 使用 `foreach_get/set` 的参考实�?
- `codes/exportfile.py:85` - 属性检查参考实�?

---

## 修复日期

2025-01-15
