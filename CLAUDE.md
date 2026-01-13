# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Blender 插件（BaiGave's Tool / MBM-workflow），用于在 Blender 内直接导入、编辑和导出 Minecraft 地图数据。与 Mineways 或 jmc2obj 等工具不同，该插件导入的是带有 blockid 和 biome 属性的点云数据，通过几何节点实例化方块模型，支持非破坏性编辑。

## 核心架构

### 模块加载系统
- `__init__.py`: 插件入口，定义 `bl_info` 元数据
- `load_modules.py`: 管理所有模块的动态加载和重载，使用 `importlib.reload()` 支持开发时热更新
- `install.py`: 首次安装时解压 `site-packages.zip` 依赖并重启 Blender

### 核心功能模块
- `codes/property.py`: 定义所有 Blender 场景属性，包括路径配置、方块切换列表、游戏规则等
- `codes/register.py`: 方块注册系统，将 Minecraft 方块状态映射到 Blender 对象 ID
- `codes/importfile.py`: 导入 .schem、.nbt 文件和世界存档
- `codes/exportfile.py`: 导出为 .schem 文件或直接写入存档
- `codes/schem.py`: 处理 schem 数据结构，创建点云网格和几何节点
- `codes/blockstates.py`: 解析 Minecraft blockstate JSON 文件，缓存方块模型数据
- `codes/functions/mesh_to_mc.py`: 将普通网格体转换为 Minecraft 方块，包含面优化算法

### 几何节点系统
插件依赖外部 `.blend` 文件中的几何节点组（位于 `codes/blend_files/GeometryNodes.blend`）：
- **Schem 节点组**: 将点云实例化为方块模型
- **ObjToBlocks 节点组**: 普通网格转方块预览
- **模型转换节点组**: 完整的网格到方块转换，支持楼梯、台阶等特殊方块

## 常用命令

### 开发调试
```bash
# 在 Blender 控制台中重载插件
import importlib
import MBM_worflow.load_modules as load_modules
importlib.reload(load_modules)
load_modules.register()

# 查看当前注册的方块映射
import bpy
id_map = eval(bpy.data.texts.get("Blocks.py").as_string())
```

### 测试导入
```python
# 导入 .schem 文件（在 Blender 中）
bpy.ops.baigave.import_schem(filepath='/path/to/file.schem')

# 应用修改器并合并重叠面（优化面数）
bpy.ops.object.modifier_apply(modifier="Schem")
bpy.ops.baigave.merge_overlapping_faces()
```

## 重要数据流

### 方块注册流程
1. `register_blocks(ids)` 在 `codes/register.py` 中被调用
2. 创建/更新 `Blocks` 集合，包含所有方块状态的模型对象
3. 在 Blender 文本数据中维护 `id_map` 字典（方块状态字符串 → 数字 ID）
4. 缓存在 `cached_models` 中避免重复解析 blockstate JSON

### 几何节点工作流
1. 导入时创建只包含顶点的网格，每个顶点有 `blockid`、`biome`、`waterlogged` 属性
2. 应用几何节点修改器，引用 `Blocks` 集合
3. 节点根据顶点的 `blockid` 属性实例化对应方块
4. 应用修改器后可使用"合并重叠面"优化面数

### 坐标系统
- Minecraft 坐标 (x, y, z) 转换为 Blender (x, -z, y)
- Y 轴在 MC 中是高度，在 Blender 中映射到 Z 轴

## 文件结构

```
MBM-worflow/
├── __init__.py              # 插件入口
├── load_modules.py          # 模块加载器
├── config.py                # 默认配置
├── install.py               # 安装脚本
├── codes/
│   ├── property.py          # 属性定义
│   ├── register.py          # 方块注册
│   ├── importfile.py        # 导入功能
│   ├── exportfile.py        # 导出功能
│   ├── schem.py             # Schem 处理
│   ├── blockstates.py       # Blockstate 解析
│   ├── block.py             # 方块对象创建
│   ├── model.py             # 网格模型生成
│   ├── ui.py                # 用户界面
│   ├── functions/           # 工具函数
│   │   ├── mesh_to_mc.py    # 网格转方块
│   │   ├── get_data.py      # 数据获取
│   │   └── ...
│   ├── classification_files/ # 方块分类
│   │   ├── block_type.py    # 方块类型定义
│   │   └── shader_type.py   # 着色器类型
│   └── blend_files/         # 外部 blend 资源
├── colors/                  # 颜色映射文件
└── multiprocess/            # 多进程支持（已注释）
```

## 依赖项

- `amulet`: Minecraft 世界格式解析
- `amulet_nbt`: NBT 数据格式
- `bmesh`: Blender 网格操作
- `numpy`: 数组计算

这些依赖打包在 `site-packages.zip` 中，由 `install.py` 解压到 Blender 的 site-packages 目录。

## Blender 版本支持

- **当前支持**: Blender 5.0+
- **Blender 5.0 API 变化**:
  - 几何节点修改器属性访问 `modifier['Input_XX']` 语法已被废弃，需要使用 try-except 并通过节点组访问作为回退方案
  - `attribute_convert` 的 `UV_MAP` 模式已移除，必须使用 `GENERIC` 模式

**兼容性代码示例**:
```python
# 修饰符属性访问（Blender 5.0+）
try:
    modifier['Input_58'] = value
except (KeyError, TypeError):
    if modifier.node_group:
        for socket in modifier.node_group.inputs:
            if socket.identifier == 'Input_58':
                socket.default_value = value
                break
```

## 注意事项

1. **坐标转换**: 始终注意 MC 和 Blender 的坐标轴差异
2. **方块 ID 映射**: 修改方块后需同步更新 `Blocks.py` 文本数据
3. **几何节点路径**: `geometrynodes_blend_path` 属性指向包含节点组的 .blend 文件
4. **缓存清理**: 更新模组/资源包后需删除 `schemcache/` 缓存
5. **不可逆操作**: 应用几何节点修改器后无法恢复到点云编辑状态

## 开发提示

- 添加新方块类型时需更新 `codes/classification_files/block_type.py`
- 修改 UI 需编辑 `codes/ui.py`
- 几何节点修改需编辑外部 `blend_files/GeometryNodes.blend`
- 使用 `bpy.app.timers.register()` 处理耗时操作的完成回调
- **修改几何节点属性时**：始终使用 try-except 模式处理属性访问，参考 `mesh_to_mc.py` 和 `surface_optimization.py` 中的实现
- **版本检查**：不再需要支持 Blender 4.x，所有新代码应直接使用 Blender 5.0+ API
