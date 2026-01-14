# 水处理机制探索报告

通过对插件代码的深入分析，该插件对“水”（及流体）的处理采用了**双重机制**，兼顾了视觉效果与性能优化。

## 1. 核心机制：双重处理

插件根据方块类型将水分为两种情况处理：

### A. 独立流体网格 (Liquid Volumes)
对于纯水的方块（如海洋、河流），插件使用 `codes/schem.py` 中的 `schem_liquid` 函数生成**真实网格 (Real Mesh)**。
- **面剔除 (Face Culling)**：插件会检测相邻方块。只有当水与空气或其他非流体方块相邻时，才会生成在该方向上的网格面，这极大地减少了多边形数量。
- **水位高度映射**：根据 Minecraft 中水的 `level` 属性（0-15），插件会自动调整网格顶点的高度（`z_offset`），从而还原水的流动坡度。
- **UV 映射**：自动为生成的流体面创建 UV 坐标，支持水的贴图和动画。

### B. 含水状态属性 (Waterlogged State)
对于非流体但可以“含水”的方块（如楼梯、栅栏、半砖），插件在 `schem` 函数中处理：
- **顶点属性**：在点云（Geometry Nodes）中为每个顶点添加一个名为 `waterlogged` 的整数属性。
- **逻辑判定**：如果 Minecraft 原型数据中包含 `extra_blocks`（通常代表含水），该属性设为 `1`，否则为 `0`。
- **几何节点交互**：几何节点（`Schem` 节点组）可以使用此属性来决定是否在方块内渲染水面。

## 2. 性能与并行化
- **分类排除**：在 `codes/classification_files/block_type.py` 中，`minecraft:water` 被列入 `exclude` 列表。这意味着它不会作为普通方块通过实例采样生成，而是由专门的流体逻辑处理。
- **多进程支持**：插件在 `multiprocess/schem_liquid_mp.py` 中实现了流体处理的并行化，能够快速处理超大规模地图的水面生成。

## 3. 分类定义
在 `codes/classification_files/block_type.py` 中定义了哪些方块被视为流体：
```python
liquid = ["minecraft:water", "minecraft:lava"]
exclude = ["minecraft:water", "minecraft:lava", "minecraft:air"]
```

## 4. 总结
该插件对水的处理非常专业：
1. **真实水体**：生成带水位高度的独立网格，适合渲染海洋和瀑布。
2. **含水方块**：通过顶点属性传递状态，由几何节点灵活处理，保证了建筑细节的还原。
3. **性能优化**：通过面剔除和多进程确保了导入效率。
