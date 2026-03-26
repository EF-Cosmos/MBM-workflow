# MBM Workflow / MBM-workflow

一个用于在 Blender 内直接导入、编辑与导出 Minecraft 地图数据的插件。与传统 OBJ 流程不同，本插件以带 `blockid` 等属性的点云为核心，通过几何节点实例化方块，实现可持续编辑的工作流。

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://github.com/EF-Cosmos/MBM-workflow/blob/main/LICENSE)
[![Blender](https://img.shields.io/badge/Blender-5.0+-orange.svg)](https://www.blender.org/download/)

## 当前功能（与代码对齐）

| 功能类别 | 当前实现 |
|---|---|
| 地图导入 | 支持 `.schem`、`.litematic`、`.nbt`、世界区域导入 |
| 导入选项 | 按方块状态分离、按区块分离、重载失效方块 |
| 地图编辑 | 方块笔刷（绘制/吸管/半径）、批量替换方块、颜色字典映射 |
| 点云处理 | `Merge + Regularize Point Cloud`（多对象合并并规整到整数网格） |
| 网格转方块 | `ObjToBlocks` + `BlockBlender`，支持楼梯/台阶等类型映射 |
| 优化与动画 | 执行优化、合并重叠面、植物摇摆动画 |
| 地图导出 | 导出 `.schem`、直接写入选中存档 |
| 存档创建 | 在 Blender 内创建 `level.dat`，支持游戏规则与玩家能力设置 |
| 版本转换 | 基于 PyMCTranslate 的跨版本方块转换（可配置平台与版本号） |

## UI 入口

Blender `3D View` -> `侧边栏 (N)` -> `MBM_workflow`。

主要面板：
- 方块
- 导入
- 导出
- 创建存档（含更多设置、游戏规则、玩家能力）
- 编辑
- Mod 设置（含资源包）

## 地图导入

### 支持格式

| 格式 | 说明 | 依赖 |
|---|---|---|
| `.schem` | WorldEdit / Sponge Schematic | amulet-core + amulet-nbt |
| `.litematic` | Litematica 格式，多区域可分别导入为对象 | litemapy |
| `.nbt` | 原版结构文件 | amulet-nbt |
| 世界存档目录 | 通过坐标范围导入世界中的方块 | amulet-core |

### 导入行为与选项

- 坐标转换：Minecraft `(x, y, z)` -> Blender `(x, -z, y)`。
- 可选分离：
  - 按方块状态分离（便于分类处理）
  - 按区块分离（便于大场景管理）
- `重载失效方块`：清理无效 `Blocks.py` 记录并触发后续重新加载。
- `.litematic` 导入按钮在缺少 `litemapy` 时会自动置灰。

## 编辑与转换

### 方块编辑

- 方块笔刷：
  - 左键绘制
  - `Shift + 左键` 吸管
  - 半径可调（`brush_radius`）
- 替换方块：在“替换方块”面板中批量设置目标 ID。
- 颜色到方块：通过颜色字典与 KDTree 最近邻匹配，将顶点色映射为方块 ID。

### 点云合并规整

- `Merge + Regularize Point Cloud`：
  - 合并多个含 `blockid` 的点云对象
  - 世界坐标规整到整数网格
  - 保留 `blockid` / `waterlogged` / `biome` 属性

### 网格转方块

推荐流程：
1. `生成点云 (ObjToBlocks)`
2. `转换网格体 (BlockBlender)`
3. `应用顶点色到方块`（可选）

该流程包含对楼梯、台阶等特殊方块形态的映射。

## 优化与动画

- `执行优化 (mbm.map_optimize)`：支持合并重叠顶点、面精简、属性转换。
- `合并重叠面`：删除重合面以减少不可见几何。
- `植物摇摆`：为选中对象添加位移动画驱动。

## 地图导出

- `导出结构`：将选中对象导出为 `.schem`。
- `计算结构大小`：计算当前导出尺寸与位置信息。
- `导出结构到存档`：按当前版本设置将方块直接写入选中的世界存档。

导出依赖对象上的 `blockid` 属性与 `Blocks.py` 映射数据。

## 创建存档

`创建存档` 面板可直接生成世界存档（`level.dat`），支持：
- 基础项：存档名、出生点、难度、模式、种子、时间等
- 更多设置：命令限制、随机刻速度、雪层高度等
- 游戏规则：多项布尔规则开关
- 玩家能力：速度、生命、护甲、攻击等属性

## Minecraft 版本配置与转换

插件通过场景属性配置版本：

```python
mc_platform       # "java" | "bedrock"
mc_version_major  # 1
mc_version_minor  # 21
mc_version_patch  # 9
```

转换链路：`源版本 -> Universal Format -> 目标版本`。

基于当前依赖（PyMCTranslate 1.2.39）的常用范围：
- Java Edition: 1.12 ~ 1.21.9
- Bedrock Edition: 1.10 ~ 1.20.x

## 安装与依赖

### 系统要求

- Blender 5.0+
- Python 3.11（Blender 5.0 内置）

### 安装

1. 下载 Release 压缩包
2. Blender -> 编辑 -> 偏好设置 -> 插件/扩展 -> 安装
3. 选择插件包并启用

### 依赖（由 `blender_manifest.toml` 管理）

| 包名 | 版本 |
|---|---|
| amulet-core | 1.9.33 |
| PyMCTranslate | 1.2.39 |
| portalocker | 3.2.0 |
| platformdirs | 4.5.1 |
| litemapy | 0.9.0b0 |
| nbtlib | 2.0.4 |
| pywin32 (Windows) | 311 |
| amulet-leveldb (Windows) | 1.0.2 |
| lz4 (Windows wheel) | 4.4.5 |
| amulet-nbt (Windows wheel) | 2.1.5 |
| pillow (Windows wheel) | 12.1.0 |

说明：
- 插件通过 `codes/dependency_manager.py` 进行安全导入与缺失依赖提示。
- `litemapy` 缺失时，`.litematic` 功能会自动降级（按钮置灰）。

## 项目结构

```text
MBM_workflow/
├── __init__.py
├── load_modules.py
├── blender_manifest.toml
├── ui.py / ui_panels.py / ui_dialogs.py
├── codes/
│   ├── dependency_manager.py
│   ├── property.py
│   ├── importfile.py
│   ├── exportfile.py
│   ├── create_world.py
│   ├── schem.py
│   ├── register.py
│   └── functions/
│       ├── brush.py
│       ├── mesh_to_mc.py
│       ├── paint.py
│       ├── surface_optimization.py
│       └── sway_animation.py
├── wheels/
└── doc/
```

## 已知限制

- 应用几何节点修改器后，点云编辑流程不可逆。
- 超大地图处理耗时较高，多进程流程目前仍属实验性模块。
- 依赖外部节点资源（如 `codes/blend_files/GeometryNodes.blend`）。

## 相关文档

- `CLAUDE.md`：项目开发说明
- `doc/ui-reference.md`：UI 面板手册
- `doc/troubleshooting.md`：故障排除
- `doc/data-flow-diagrams.md`：数据流说明
- `doc/dependency-update-guide.md`：依赖更新指南

## 贡献者

| 角色 | 贡献者 |
|---|---|
| 主要开发 | EF_Cosmos (GitHub) |
| 几何节点 | 火锅料理、抛瓦尔第、暗影苦力怕、Piggestpig、荒芜新谷 |
| 着色器 | WangXinRui |
| 多进程支持 | Piggestpig / 冬猫夏羊工作室 |
| 翻译 | marshmallowlands |

## 许可证

本项目采用 [AGPL-3.0](https://github.com/EF-Cosmos/MBM-workflow/blob/main/LICENSE) 许可证。

## 联系与支持

- QQ 群：878232347（Bug 反馈与交流）
- Bilibili：[白给的个人空间](https://space.bilibili.com/3461563635731405)
- GitHub Issues：[报告问题](https://github.com/EF-Cosmos/MBM-workflow/issues)
