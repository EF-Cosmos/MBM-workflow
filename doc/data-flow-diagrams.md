# MBM-workflow 插件数据转化图

本文档详细描述 MBM-workflow (BaiGave's Tool) 插件中各种数据转化的流程。

## 目录

1. [方块注册流程](#1-方块注册流程)
2. [导入流程](#2-导入流程)
3. [导出流程](#3-导出流程)
4. [坐标系统转换](#4-坐标系统转换)
5. [材质系统流程](#5-材质系统流程)
6. [数据结构关系](#6-数据结构关系)

---

## 1. 方块注册流程

方块注册是将 Minecraft 的方块状态转换为 Blender 中可渲染的 3D 模型的核心流程。

```mermaid
flowchart TD
    subgraph Input["输入数据"]
        A["blockstates.json<br/>Minecraft 资源文件"]
        B["models/*.json<br/>方块模型定义"]
        C["textures/*.png<br/>纹理图片"]
    end

    subgraph Parse["解析阶段"]
        D["get_file_path()<br/>文件路径解析"]
        E["get_model()<br/>方块状态解析"]
        F["get_all_data()<br/>模型数据提取"]
    end

    subgraph Cache["缓存层"]
        G["cached_models<br/>模型数据缓存"]
        H["cached_parents<br/>父方块缓存"]
    end

    subgraph Create["创建阶段"]
        I["block()<br/>方块对象创建"]
        J["extract_vertices_from_elements()<br/>顶点提取"]
        K["bmesh 操作<br/>网格构建"]
    end

    subgraph Material["材质处理"]
        L["get_or_create_material()<br/>材质获取/创建"]
        M["create_node_material()<br/>着色器节点"]
    end

    subgraph Output["输出结果"]
        N["Blocks 集合<br/>所有方块模型"]
        O["id_map 字典<br/>方块ID映射"]
        P["Blocks.py 文本数据<br/>持久化存储"]
    end

    A --> D
    B --> D
    C --> D
    D --> E

    E -->|缓存命中| G
    E -->|缓存未命中| F
    F --> G
    F --> H

    G --> I
    H --> I

    I --> J
    J --> K
    K --> L
    L --> M

    I --> N
    N --> O
    O --> P

    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#e1f5fe
    style N fill:#c8e6c9
    style O fill:#c8e6c9
    style P fill:#c8e6c9
```

### 关键函数说明

| 函数 | 文件位置 | 作用 |
|------|----------|------|
| `register_blocks()` | `codes/register.py:20-81` | 注册方块到 Blocks 集合 |
| `block()` | `codes/block.py:76-238` | 创建单个方块对象 |
| `get_model()` | `codes/blockstates.py:199-306` | 解析方块状态和模型 |
| `get_all_data()` | `codes/functions/get_data.py:47-85` | 提取模型数据 |

### 数据结构

**id_map 格式**:
```python
{
    "minecraft:stone": 0,
    "minecraft:grass_block[snowy=true]": 1,
    "minecraft:oak_log[axis=x]": 2,
    ...
}
```

---

## 2. 导入流程

导入流程将 Minecraft 世界文件转换为 Blender 中的点云预览。

```mermaid
flowchart TD
    subgraph Input["输入文件"]
        A1[".schem 文件"]
        A2[".nbt 文件"]
        A3["世界存档"]
    end

    subgraph Amulet["Amulet 解析"]
        B["amulet.load_level()<br/>加载世界数据"]
        C["level.get_block()<br/>获取方块数据"]
        D["level.bounds()<br/>获取边界范围"]
    end

    subgraph Process["数据处理"]
        E["遍历坐标范围<br/>for x,y,z in range()"]
        F["方块字符串提取<br/>remove_brackets()"]
        G["排除过滤<br/>检查 exclude 列表"]
    end

    subgraph PointCloud["点云创建"]
        H["创建网格对象<br/>bpy.data.meshes.new()"]
        I["添加顶点属性<br/>blockid, waterlogged, biome"]
        J["坐标转换<br/>MC → Blender"]
    end

    subgraph Register["方块注册"]
        K["register_blocks()<br/>注册遇到的方块"]
        L["获取 id_map 映射"]
    end

    subgraph Attribute["属性设置"]
        M["设置 blockid 属性<br/>id_map[id_string]"]
        N["设置 waterlogged 属性"]
        O["设置 biome 颜色"]
    end

    subgraph GN["几何节点"]
        P["添加 NODES 修改器"]
        Q["导入 Schem 节点组"]
        R["设置集合信息"]
    end

    subgraph Output["最终结果"]
        S["点云网格对象<br/>带几何节点修改器"]
        T["实时预览<br/>实例化方块"]
    end

    A1 --> B
    A2 --> B
    A3 --> B

    B --> C
    B --> D
    D --> E
    C --> E

    E --> F
    F --> G
    G --> H

    H --> I
    I --> J
    J --> K

    K --> L
    L --> M
    M --> N
    N --> O

    H --> P
    P --> Q
    Q --> R

    R --> S
    S --> T

    style A1 fill:#e1f5fe
    style A2 fill:#e1f5fe
    style A3 fill:#e1f5fe
    style S fill:#c8e6c9
    style T fill:#c8e6c9
```

### 核心函数

| 函数 | 文件位置 | 作用 |
|------|----------|------|
| `schem()` | `codes/schem.py:29-136` | 创建点云并应用几何节点 |
| `schem_chunk()` | `codes/schem.py:139-172` | 分区块处理（多进程） |
| `schem_liquid()` | `codes/schem.py:176-447` | 流体方块处理 |

### 顶点属性结构

```
每个顶点包含三个属性：
┌─────────────────────────────────────┐
│  顶点 (x, y, z)                      │
├─────────────────────────────────────┤
│  blockid: INT      (方块数字ID)      │
│  waterlogged: INT  (含水状态 0/1)   │
│  biome: FLOAT_COLOR (群系颜色 RGBA) │
└─────────────────────────────────────┘
```

---

## 3. 导出流程

导出流程将 Blender 场景转换回 Minecraft 格式。

```mermaid
flowchart TD
    subgraph Input["输入"]
        A["Blender 选中对象<br/>selected_objects"]
    end

    subgraph Check["类型检查"]
        B{对象类型?}
        C{有修改器?}
        D["MESH 类型"]
        E["有 '模型转换' 修改器"]
        F["无修改器"]
    end

    subgraph Eval["评估"]
        G["depsgraph.evaluated_depsgraph_get()<br/>获取评估依赖图"]
        H["obj.evaluated_get()<br/>获取评估对象"]
    end

    subgraph Extract["数据提取"]
        I["遍历顶点"]
        J["获取世界坐标<br/>obj.matrix_world @ vertex.co"]
        K["读取 blockid 属性"]
        L["构建 vertex_dict<br/>{coord: blockid}"]
    end

    subgraph Lookup["ID 反向查询"]
        M["读取 Blocks.py 文本"]
        N["解析 id_map 字典"]
        O["blockid → 方块名称"]
    end

    subgraph NBT["NBT 构建"]
        P["创建 TAG_Compound"]
        Q["构建 Palette<br/>方块调色板"]
        R["构建 BlockData<br/>方块数组"]
        S["计算边界尺寸"]
    end

    subgraph Output["输出文件"]
        T[".schem 文件"]
        U["世界存档写入"]
    end

    A --> B
    B -->|是| C
    B -->|否| END1["跳过"]

    C -->|有| E
    C -->|无| F

    E --> G
    G --> H
    F --> I

    H --> I
    I --> J
    J --> K
    K --> L

    L --> M
    M --> N
    N --> O

    O --> P
    P --> Q
    Q --> R
    R --> S

    P --> T
    P --> U

    style A fill:#e1f5fe
    style T fill:#c8e6c9
    style U fill:#c8e6c9
```

### 核心函数

| 函数 | 文件位置 | 作用 |
|------|----------|------|
| `ExportSchem.execute()` | `codes/exportfile.py:43-116` | 导出为 .schem 文件 |
| `ExportToSave.execute()` | `codes/exportfile.py:262-361` | 导出到世界存档 |
| `export_schem()` | `codes/exportfile.py:118-177` | NBT 数据构建 |

### NBT 结构

```
schem 文件结构:
┌─────────────────────────────────────────┐
│  TAG_Compound (根)                       │
├─────────────────────────────────────────┤
│  DataVersion: TAG_Int(3465)             │
│  Version: TAG_Int(2)                    │
│  Metadata: TAG_Compound                 │
│  Palette: TAG_Compound                  │
│    ├─ minecraft:air: TAG_Int(0)         │
│    ├─ minecraft:stone: TAG_Int(1)       │
│    └─ ...                               │
│  PaletteMax: TAG_Int                    │
│  Width: TAG_Short                       │
│  Height: TAG_Short                      │
│  Length: TAG_Short                      │
│  BlockData: TAG_ByteArray               │
│  Offset: TAG_IntArray                   │
└─────────────────────────────────────────┘
```

---

## 4. 坐标系统转换

Minecraft 和 Blender 使用不同的坐标系统，需要进行转换。

```mermaid
graph LR
    subgraph MC["Minecraft 坐标系统"]
        MC["X: 东西<br/>Y: 高度<br/>Z: 南北"]
    end

    subgraph Conversion["转换规则"]
        RULE1["x → x (保持不变)"]
        RULE2["y → z (高度变成Z轴)"]
        RULE3["z → -y (反向+交换)"]
    end

    subgraph Blender["Blender 坐标系统"]
        BC["X: 东西<br/>Y: 南北<br/>Z: 高度"]
    end

    MC -->|"x,y,z"| Conversion
    Conversion -->|"x,-z,y"| Blender

    MC2["MC(1, 64, 1)<br/>地面位置"] --> CONV["转换"]
    CONV --> BL["Blender(1, -1, 64)<br/>对应位置"]

    style MC fill:#8d6e63
    style Blender fill:#42a5f5
```

### 转换公式

```python
# Minecraft → Blender
blender_x = mc_x
blender_y = -mc_z
blender_z = mc_y

# Blender → Minecraft
mc_x = blender_x
mc_y = blender_z
mc_z = -blender_y
```

### 实际代码位置

| 位置 | 代码 | 说明 |
|------|------|------|
| `codes/schem.py:86` | `(x-min_x, -(z-min_z), y-min_y)` | 导入时坐标转换 |
| `codes/exportfile.py:355` | `level.set_version_block(x, z, -y, ...)` | 导出时坐标转换 |

---

## 5. 材质系统流程

材质系统将 Minecraft 纹理转换为 Blender 着色器材质。

```mermaid
flowchart TD
    subgraph Input["纹理输入"]
        A["PNG 纹理文件<br/>assets/minecraft/textures/"]
        B["法线贴图<br/>*_n.png"]
        C["动画元数据<br/>*.png.mcmeta"]
    end

    subgraph Find["纹理查找"]
        D["get_file_path()<br/>遍历模组/资源包"]
        F["缓存纹理路径"]
    end

    subgraph Shader["着色器选择"]
        G{类型判断}
        H1["PBR着色器<br/>有法线/高光贴图"]
        H2["重叠面着色器<br/>双层纹理"]
        H3["树叶/草着色器<br/>+灰度图"]
        H6["动态材质<br/>+mcmeta动画"]
        H7["自发光着色器<br/>+e贴图"]
        H5["标准着色器<br/>基础纹理"]
    end

    subgraph Create["材质创建"]
        I["从 Material.blend<br/>复制着色器模板"]
        J["创建材质节点"]
        K["设置纹理图片"]
    end

    subgraph Attribute["材质属性"]
        L["基础颜色纹理"]
        M["法线/高光/发光贴图"]
        N["透明度"]
        O["金属度/粗糙度"]
        Q["动画帧率/插值"]
    end

    subgraph Output["输出"]
        P["bpy.data.materials<br/>材质库"]
    end

    A --> D
    B --> D
    C --> D

    D --> F
    F --> G

    G -->|有法线/高光| H1
    G -->|双层| H2
    G -->|树叶| H3
    G -->|有动画| H6
    G -->|有发光| H7
    G -->|其他| H5

    H1 --> I
    H2 --> I
    H3 --> I
    H6 --> I
    H7 --> I
    H5 --> I

    I --> J
    J --> K

    K --> L
    K --> M
    K --> N
    K --> O
    K --> Q

    J --> P

    style A fill:#e1f5fe
    style P fill:#c8e6c9
```

### 着色器类型

| 着色器 | 条件 | 节点来源 |
|--------|------|----------|
| PBR着色器 | 存在 `*_n.png` 或 `*_s.png` | `Material.blend` |
| 重叠面着色器 | 双层纹理 | `Material.blend` |
| 树叶/草着色器 | `block_type.Type1` | `Material.blend` |
| 动态材质 | 存在 `.mcmeta` | `Material.blend` |
| 自发光着色器 | 存在 `*_e.png` | `Material.blend` |
| 标准着色器 | 默认 | `Material.blend` |

### 核心函数

| 函数 | 文件位置 | 作用 |
|------|----------|------|
| `create_node_material()` | `codes/model.py:9-279` | 创建材质和着色器 |
| `get_or_create_material()` | `codes/model.py` | 获取或创建材质 |

---

## 6. 数据结构关系

展示插件中核心数据结构之间的关系。

```mermaid
graph TB
    subgraph Blender["Blender 数据"]
        A["bpy.data.collections<br/>集合系统"]
        B["bpy.data.objects<br/>对象列表"]
        C["bpy.data.meshes<br/>网格数据"]
        D["bpy.data.materials<br/>材质库"]
        E["bpy.data.texts<br/>文本数据"]
        F["bpy.data.node_groups<br/>节点组"]
    end

    subgraph Custom["自定义数据"]
        G["Blocks 集合<br/>隐藏集合"]
        H["点云对象<br/>带属性的网格"]
        I["方块模型<br/>3D 对象"]
        J["Blocks.py<br/>id_map 存储"]
        K["几何节点<br/>实例化逻辑"]
    end

    subgraph External["外部资源"]
        L["GeometryNodes.blend<br/>节点组资源"]
        M["Material.blend<br/>着色器库"]
        N["Minecraft 资源<br/>纹理/模型"]
    end

    subgraph Cache["缓存数据"]
        O["cached_models<br/>模型缓存"]
        P["cached_parents<br/>父方块缓存"]
        Q["schemcache/<br/>文件缓存"]
    end

    A --> G
    B --> H
    B --> I
    C --> H
    C --> I
    D --> I
    E --> J
    F --> K

    L --> K
    M --> D
    N --> I

    O --> N
    P --> N
    Q --> H

    style G fill:#ffecb3
    style H fill:#b3e5fc
    style I fill:#c8e6c9
    style J fill:#f8bbd0
    style K fill:#d1c4e9
```

### 核心数据结构

**Blocks 集合**:
```
Blocks/
├── 0#minecraft:air
├── 1#minecraft:stone
├── 2#minecraft:grass_block[snowy=true]
└── ...
```

**点云对象属性**:
```
点云网格:
- vertices: [(x1,y1,z1), (x2,y2,z2), ...]
- blockid: [0, 1, 2, ...]
- waterlogged: [0, 1, 0, ...]
- biome: [(r,g,b,a), ...]
- modifier: Geometry Nodes "Schem"
```

---

## 附录

### 关键文件索引

| 文件 | 核心功能 |
|------|----------|
| `codes/register.py` | 方块注册系统 |
| `codes/schem.py` | 导入和点云创建 |
| `codes/exportfile.py` | 导出功能 |
| `codes/blockstates.py` | 方块状态解析 |
| `codes/block.py` | 方块对象创建 |
| `codes/model.py` | 材质系统 |
| `codes/functions/get_data.py` | 数据获取 |
| `codes/functions/surface_optimization.py` | 面优化算法 |
| `codes/functions/sway_animation.py` | 植物摇摆动画 |

### 外部依赖

| 文件 | 用途 |
|------|------|
| `codes/blend_files/GeometryNodes.blend` | Schem 节点组 |
| `codes/blend_files/Material.blend` | 材质着色器库 |
| `site-packages.zip` | Python 依赖 (amulet, amulet_nbt) |

### 版本兼容性

- **Blender**: 5.0+
- **Python**: 3.x
- **Minecraft**: Java Edition 1.20.4
- **Amulet**: 最新稳定版
