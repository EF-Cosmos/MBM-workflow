# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Blender 5.0+ 插件（MBM Workflow），在 Blender 内导入、编辑、导出 Minecraft 地图数据。核心思路：导入带 `blockid`/`biome`/`waterlogged` 顶点属性的点云，通过几何节点实例化方块模型，支持非破坏性编辑。

## 常用命令

```bash
# Blender 控制台重载插件
import importlib; import MBM_workflow.load_modules as m; importlib.reload(m); m.register()

# 查看方块映射
id_map = eval(bpy.data.texts.get("Blocks.py").as_string())

# 导入/测试
bpy.ops.mbm.import_schem(filepath='/path/to/file.schem')
bpy.ops.mbm.import_litematic(filepath='/path/to/file.litematic')
python test_version_support.py  # 在 Blender 脚本编辑器中运行
```

调试输出：窗口 → 切换系统控制台查看 `print()`。

## 核心架构

### 模块加载

```
__init__.py → load_modules.py → dependency_manager → i18n → [功能模块] → ui
```

- `load_modules.py` 维护有序 `module_list`，每个模块通过 `importlib.reload()` 加载（开发热更新）
- `register()` 顺序：先检查依赖 → 再逐模块注册；`unregister()` 逆序
- 每个子模块遵循相同模式：`classes` 列表 + `register()`/`unregister()`

### 依赖管理

两层机制：
- **构建时**：`blender_manifest.toml` 声明 `wheels/` 下的 11 个 .whl 文件，Blender 5.0+ 自动安装
- **运行时**：`codes/dependency_manager.py` 提供 `safe_import()` 返回 None 降级，monkey-patch portalocker 绕过 pywin32 依赖

```python
from .codes.dependency_manager import amulet, amulet_nbt, litemapy
if amulet is None:
    return {'CANCELLED'}
```

### 方块注册管线

```
导入文件 → 收集 blockstate 字符串 → register_blocks(ids)
  → blockstates.py: 解析 blockstate JSON → get_all_data() 递归解析模型继承
  → block.py: block() 创建网格对象
  → model.py: create_node_material() 选择着色器
  → register.py: 更新 Blocks 集合 + Blocks.py 文本数据中的 id_map
```

- `id_map`: `{blockstate_string: int}` 存储在 Blender 文本数据 `Blocks.py` 中
- `cached_models` / `cached_parents`（`blockstates.py`）缓存解析结果避免重复 I/O
- `block_map_store.py` 提供 `load_block_map()` / `save_block_map()` 读写 id_map

### 着色器选择（`model.py` → `create_node_material()`）

按方块类型自动选择：默认 → 透明（缺失纹理）→ PBR（检测 `_n.png`/`_s.png`）→ 发光（`_e.png`）→ 植被+colormap（Type1）→ colormap-only（Type2）→ 动画植被（Type3 + .mcmeta）。分类定义在 `codes/classification_files/shader_type.py`。

### 几何节点系统

节点组在外部 `.blend` 文件中定义（不在代码中创建）：
- `codes/blend_files/GeometryNodes.blend` — "Schem" 节点组：根据顶点 `blockid` 从 `Blocks` 集合实例化方块
- `codes/blend_files/BlockBlender++.blend` — "ObjToBlocks"、"模型转换" 节点组：网格转方块
- `codes/blend_files/Material.blend` — 所有着色器节点组

```python
# 访问几何节点属性
from codes.functions.mesh_to_mc import set_modifier_socket_value
set_modifier_socket_value(modifier, 'Input_58', 'UV', value, is_input=True)
```

### 坐标系统

MC `(x, y, z)` → Blender `(x, -z, y)`。Y（高度）映射到 Z 轴。

### 国际化系统（`i18n/`）

- `i18n/__init__.py`: 解析 `.po` 文件注册到 `bpy.app.translations`
- `i18n/translations.py`: 包装函数用于代码中引用翻译：

```python
from i18n.translations import panel_label, operator_label, property_name, enum_item
# 内部查找上下文: Panel|msg, Operator|msg, Property|msg, Enum|id|name
```

- 翻译文件：`i18n/locales/{zh_CN,en_US}/LC_MESSAGES/mbm_workflow.po`
- 修改 `.po` 后需运行 `i18n/compile_translations.py` 编译为 `.mo`

### 配置持久化（`config.py`）

`config.py` 存储运行时配置（mod_list、version、save 等）。`codes/functions/search_file.py` 中的目录扫描操作符通过正则直接重写该文件来更新配置值。这不优雅但有效——修改时需注意保持格式。

### 多进程导入

导入 `.schem` 时方块数超过 `sna_minsize`（默认 1M）自动启用：

1. `MultiprocessPool` 沿 X 轴均分 N 个区块，写入 `schemcache/var.json`（JSON 格式）
2. `subprocess.Popen` 启动 N 个 Blender 后台实例（`--background --python`）
3. 各子进程通过 `MBM_CHUNK_INDEX` 环境变量获取区块编号
4. 流体由独立子进程处理，结果保存为 `schemcache/liquid.blend`
5. 主进程通过 `bpy.app.timers.register()` 轮询（返回 `float` = 下次间隔，`None` = 停止）
6. 全部完成后 `merge_chunks()` 合并，`schem(cached=True)` 加载

**配置**（`AddonPreferences`）：`sna_processnumber`（进程数，默认 6）、`sna_minsize`（阈值）

### 方块笔刷（`codes/functions/brush.py`）

使用哈希字典 O(1) 查找（非 KDTree）：

```python
# invoke: 构建索引（coord → 索引列表，math.floor 向下取整）
self.vertex_map = {}
for i, v in enumerate(mesh.vertices):
    coord = (math.floor(v.co.x), math.floor(v.co.y), math.floor(v.co.z))
    self.vertex_map.setdefault(coord, []).append(i)
# brush_action: 射线命中后精确匹配（返回索引列表）
vertex_indices = self.vertex_map.get((math.floor(hit.x), math.floor(hit.y), math.floor(hit.z)), [])
```

### 方块调色板（`codes/block_palette.py` + `block_palette_panel.py`）

- `block_palette.py`: 纹理预览缓存（`bpy.utils.previews`）、收藏/最近使用管理、选择/收藏操作符
- `block_palette_panel.py`: 分页网格面板，搜索过滤，标签页切换（全部/收藏/最近）
- 纹理从方块材质的 "默认图片" 节点提取
- 收藏/最近使用列表存储在 `property.py` 的 StringProperty 中（`|` 分隔）

## 版本转换

```
特定版本 → Universal Format → 目标版本
(1.12)       (中间层)         (1.21)
```

```python
# 获取版本配置
from codes.property import get_mc_version
platform, version_tuple = get_mc_version(context)  # ("java", (1, 21, 9))

# 获取转换器
converter = level.translation_manager.get_version(platform, version)
```

支持范围（PyMCTranslate 1.2.39）：Java 1.12~1.21.9，Bedrock 1.10~1.20.x

## 重要约束

1. **线程安全**：不要在子线程调用 Blender API，使用 `subprocess` 或 `bpy.app.timers`
2. **不可逆操作**：应用几何节点修改器后无法恢复到点云编辑状态
3. **私有 API**：使用 `amulet_nbt.load()` 而非 `amulet_nbt._load_nbt`
4. **Blender 版本**：仅支持 Blender 5.0+，新代码直接使用 5.0+ API
5. **模块级变量**：`importlib.reload()` 会重置模块级变量为默认值——不要在模块级变量中缓存需要跨 reload 持久的状态
6. **缓存清理**：更新模组/资源包后需删除 `schemcache/`
7. **几何节点路径**：`geometrynodes_blend_path` 场景属性指向包含节点组的 `.blend` 文件

## UI 修改

- 面板定义：`ui_panels.py`
- 弹窗对话框：`ui_dialogs.py`
- UIList 类：`ui_lists.py`
- 类聚合注册：`ui.py`
- 新方块类型需更新 `codes/classification_files/block_type.py` 中的 `exclude` 列表

## 相关文档

- `doc/data-flow-diagrams.md` — 数据流程图
- `doc/dependency-update-guide.md` — 依赖更新指南
- `doc/portalocker-pywin32-workaround.md` — Portalocker pywin32 绕过方案

## 项目结构

```
MBM_workflow/
├── __init__.py                    # 插件入口，bl_info
├── load_modules.py                # 模块加载编排，依赖检查
├── config.py                      # 运行时配置持久化
├── blender_manifest.toml          # Blender 5.0+ 插件清单
├── wheels/                        # Python 依赖包
├── ui.py / ui_panels.py / ui_dialogs.py / ui_lists.py  # UI 层
├── i18n/                          # 国际化（zh_CN, en_US）
├── codes/
│   ├── dependency_manager.py      # 安全导入 + portalocker patch
│   ├── property.py                # 场景属性（版本、路径、游戏规则、调色板状态）
│   ├── register.py                # 方块注册 → Blocks 集合 + id_map
│   ├── blockstates.py             # blockstate JSON 解析 + 模型缓存
│   ├── block.py                   # 方块网格对象创建
│   ├── model.py                   # 材质系统（着色器选择、网格构建）
│   ├── block_map_store.py         # Blocks.py 文本数据读写
│   ├── block_palette.py           # 方块调色板（预览缓存、收藏、最近）
│   ├── block_palette_panel.py     # 调色板面板 UI
│   ├── schem.py                   # schem/litematic 处理，merge_chunks
│   ├── importfile.py              # 导入操作符 + MultiprocessPool
│   ├── exportfile.py              # 导出操作符
│   ├── create_world.py            # 存档创建
│   ├── functions/
│   │   ├── mesh_to_mc.py          # 网格转方块（ObjToBlocks, BlockBlender）
│   │   ├── brush.py               # 方块笔刷（哈希字典 O(1) 查找）
│   │   ├── paint.py               # 顶点色到方块 ID
│   │   ├── surface_optimization.py # 面优化
│   │   ├── sway_animation.py      # 植物摇摆动画
│   │   ├── get_data.py            # 模型/纹理文件路径解析
│   │   └── search_file.py         # 目录扫描 + config.py 同步
│   ├── classification_files/
│   │   ├── block_type.py          # exclude/liquid 列表
│   │   └── shader_type.py         # 着色器分类（Type1/2/3）
│   └── blend_files/               # 外部 .blend（几何节点、材质）
├── multiprocess/                  # 多进程子进程脚本
├── mutf8/                         # Modified UTF-8 实现（amulet fallback）
├── colors/                        # 颜色对照表
└── doc/                           # 文档
```
