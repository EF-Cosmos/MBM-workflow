# UV 纹理导出 Schem 功能

本功能允许用户将带有 UV 纹理�?Blender 网格对象，通过纹理颜色采样匹配 Minecraft 方块，导出为 `.schem` 文件�?

## 功能概述

```
┌─────────────────�?
�? Blender 网格   �?
�? (�?UV 纹理)   �?
└────────┬────────�?
         �?
         �?
┌─────────────────�?
�? UV 坐标采样    �?
�? 纹理颜色       �?
└────────┬────────�?
         �?
         �?(可�?
┌─────────────────�?
�? AO 顶点色叠�? �?
�? 调整明暗       �?
└────────┬────────�?
         �?
         �?
┌─────────────────�?
�? 颜色匹配方块   �?
�? (欧几里得距离) �?
└────────┬────────�?
         �?
         �?
┌─────────────────�?
�? 导出 .schem    �?
└─────────────────�?
```

## 使用要求

### 1. 网格要求
- 物体必须�?**MESH** 类型
- 必须�?**UV 贴图**（至少一�?UV 层）

### 2. 材质要求
- 材质必须使用 **节点** 模式（Use Nodes = True�?
- 需要有 **图像纹理节点**（Image Texture�?
- 图像纹理需连接�?Principled BSDF �?Base Color 输入

示例材质节点设置�?
```
[Image Texture] ──�?[Principled BSDF] ──�?[Material Output]
    (你的纹理)         Base Color
```

## 操作步骤

### 步骤 1：准备模�?

1. 确保模型有正确的 UV 展开
2. 为模型分配带有图像纹理的材质
3. 调整模型的缩放（1 �?Blender 单位 = 1 �?Minecraft 方块�?

### 步骤 2：生�?AO 顶点色（可选）

如果希望导出的结构有明暗变化效果，可以使�?Blender 内置�?Dirty Vertex Colors 功能�?

1. 选择物体
2. 进入 **顶点绘制模式** (Vertex Paint)
3. 菜单�?*Paint �?Dirty Vertex Colors**
4. 调整参数后确�?
5. 将生成的颜色属性命名为 `ao`

### 步骤 3：导�?Schem

1. 选择要导出的物体
2. 点击 **"UV 纹理导出 Schem"**
3. 在弹出对话框中设置参数：
   - **体素缩放**: 每个方块对应�?Blender 单位大小（默�?1.0�?
   - **使用 AO 纹理**: 是否应用 AO 顶点�?
   - **AO 强度**: AO 对最终颜色的影响程度 (0-1)

4. 点击确认，文件将保存�?`schem/` 文件�?

## 参数说明

### UVToSchem 操作�?

| 参数 | 类型 | 默认�?| 说明 |
|------|------|--------|------|
| `voxel_scale` | Float | 1.0 | 体素缩放比例。值越小，导出的结构越�?|
| `use_ao` | Bool | False | 是否使用 AO 顶点色来调整颜色明暗 |
| `ao_strength` | Float | 0.5 | AO 的影响强度�?=无影响，1=完全影响 |

## 颜色匹配算法

使用 **欧几里得距离** �?RGB 颜色空间中查找最接近的方块：

```python
distance = sqrt((r1-r2)² + (g1-g2)² + (b1-b2)²)
```

当启�?AO 时，会先将采样颜色与 AO 值相乘：

```python
adjusted_color = (r * ao, g * ao, b * ao)
```

## 方块颜色字典

颜色匹配使用 `colors/` 文件夹下�?Python 文件，默认为 `minecraft.py`�?

可以通过场景属�?`color_list` 选择不同的颜色对照表�?

字典格式�?
```python
cube_dict = {
    'minecraft:stone': (0.49, 0.49, 0.49, 1.0),        # RGBA
    'minecraft:oak_planks': (0.62, 0.51, 0.32, 1.0),
    # ...
}
```

## 输出文件

- **位置**: `MBM_workflow/schem/` 文件�?
- **命名**: `{物体名}_uv.schem`
- **格式**: WorldEdit Schematic v2

## 示例用例

### 用例 1：简单颜色导�?
将一个带有彩色纹理的立方体导出为 Minecraft 结构�?

1. 创建立方体，展开 UV
2. 分配带有彩色纹理的材�?
3. 点击 "UV 纹理导出 Schem"
4. 保持默认设置，确�?

### 用例 2：带 AO 的建筑导�?
将一个建筑模型导出，保留阴影细节�?

1. 准备建筑模型和纹�?
2. 进入顶点绘制模式，使�?Paint �?Dirty Vertex Colors 生成 AO
3. 将颜色属性命名为 `ao`
4. 点击 "UV 纹理导出 Schem"
5. 勾�?"使用 AO 纹理"，设置强度为 0.7
6. 确认导出

### 用例 3：大比例场景导出
将一个大型场景缩小后导出�?

1. 准备场景模型（假�?10m = 1 方块�?
2. 点击 "UV 纹理导出 Schem"
3. 设置 "体素缩放" �?10.0
4. 确认导出

## 故障排除

### 问题：提�?物体没有 UV 贴图"
**解决方案**: 进入编辑模式，选择所有面，按 `U` 展开 UV

### 问题：提�?未找到材质纹�?
**解决方案**: 
1. 确保物体有材�?
2. 在着色器编辑器中添加 Image Texture 节点
3. 将纹理连接到 Principled BSDF �?Base Color

### 问题：导出的颜色不准�?
**解决方案**:
1. 检查纹理是否正确加�?
2. 检�?UV 是否正确展开
3. 尝试使用不同的颜色对照表

### 问题：导出的结构太大/太小
**解决方案**: 调整 "体素缩放" 参数

## API 参�?

### 函数

```python
sample_texture_at_uv(image, uv)
```
从纹理图像中�?UV 坐标采样颜色�?

**参数**:
- `image`: Blender 图像对象
- `uv`: UV 坐标元组 (u, v)

**返回**: RGBA 颜色元组

---

```python
find_closest_block(color, block_color_dict, ao_value=1.0)
```
根据颜色找到最接近�?Minecraft 方块�?

**参数**:
- `color`: RGBA 颜色元组
- `block_color_dict`: 方块颜色字典
- `ao_value`: AO �?(0-1)

**返回**: 方块名称字符�?

---

```python
get_material_image(obj)
```
从物体材质中获取 Base Color 纹理图像�?

**参数**:
- `obj`: Blender 物体

**返回**: Blender 图像对象�?None

---

```python
load_block_color_dict()
```
加载方块颜色字典�?

**返回**: 方块颜色字典 `{block_name: (r, g, b, a)}`

## 相关文件

- [codes/functions/mesh_to_mc.py](../codes/functions/mesh_to_mc.py) - 核心实现
- [colors/minecraft.py](../colors/minecraft.py) - 方块颜色字典
- [ui.py](../ui.py) - UI 面板定义
