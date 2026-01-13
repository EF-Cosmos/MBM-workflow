# 依赖更新指南

本文档说明如何更新 MBM-workflow 插件的 Python 依赖包。

---

## 什么是 Wheel 文件

**.whl** (Wheel) 是 Python 的标准分发格式，本质是一个 ZIP 压缩包，包含：
- 编译好的 Python 代码
- 包元数据（版本、依赖等）
- 可选的二进制扩展模块

### Wheel 文件命名规则

```
{distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
```

| 部分 | 示例 | 说明 |
|------|------|------|
| distribution | `amulet_core` | 包名（下划线替代连字符） |
| version | `1.9.33` | 版本号 |
| python tag | `py3` / `cp311` | Python 版本兼容性 |
| abi tag | `none` / `cp311` | ABI 二进制接口兼容性 |
| platform tag | `any` / `win_amd64` | 平台兼容性 |

### 常见标签含义

| 标签 | 含义 |
|------|------|
| `py3` | 兼容 Python 3.x（纯 Python） |
| `cp311` | CPython 3.11 特定 |
| `none` | 无 ABI 限制（纯 Python） |
| `any` | 跨平台 |
| `win_amd64` | Windows 64 位 |
| `linux_x86_64` | Linux 64 位 |
| `macosx_10_9_x86_64` | macOS x86_64 |

---

## 当前依赖列表

### 跨平台通用包

| 包名 | 当前版本 | 最新版本 | 文件名 |
|------|----------|----------|--------|
| amulet-core | 1.9.33 | - | `amulet_core-*.whl` |
| PyMCTranslate | 1.2.39 | - | `pymctranslate-*.whl` |
| portalocker | 3.2.0 | - | `portalocker-*.whl` |
| platformdirs | 4.5.1 | - | `platformdirs-*.whl` |

### 平台特定包（C 扩展）

| 包名 | 平台 | 文件名 | 原因 |
|------|------|--------|------|
| pywin32 | Windows | `pywin32-*-win_amd64.whl` | Windows API 绑定 |
| amulet-leveldb | Windows | `amulet_leveldb-*-win_amd64.whl` | Cython wrapper |
| lz4 | 跨平台 | `lz4-*-cp311-win_amd64.whl` | C 绑定 |
| amulet-nbt | 跨平台 | `amulet_nbt-*-win_amd64.whl` | Cython 编写 |
| pillow | 跨平台 | `pillow-*-win_amd64.whl` | 图像处理 C 库 |
| mutf8 | ~~已移除~~ | - | 无 cp311 版本，使用纯 Python 回退 |

---

## 更新方法

### 方法 1：使用 pip download（推荐）

适用于**跨平台通用包**（`py3-none-any.whl`）：

```bash
# 创建临时目录
mkdir -p /tmp/wheels_new

# 下载最新版本（不检查依赖）
pip download --only-binary=:all: --no-deps --dest /tmp/wheels_new \
    "amulet-core==1.9.33" \
    "PyMCTranslate==1.2.39" \
    portalocker \
    platformdirs

# 复制到项目目录
cp /tmp/wheels_new/*.whl /path/to/MBM-worflow/wheels/

# 删除旧版本
rm /path/to/MBM-worflow/wheels/amulet_core-1.9.25-*.whl
rm /path/to/MBM-worflow/wheels/PyMCTranslate-1.2.27-*.whl
# ... 其他旧版本
```

### 方法 2：从 PyPI 手动下载

适用于**平台特定包**或**有特殊依赖的包**：

1. 访问 [PyPI.org](https://pypi.org)
2. 搜索包名（如 `amulet-core`）
3. 点击 "Download files" 标签
4. 下载对应的 `.whl` 文件

| 包名 | PyPI 链接 |
|------|-----------|
| amulet-core | https://pypi.org/project/amulet-core/#files |
| PyMCTranslate | https://pypi.org/project/PyMCTranslate/#files |
| amulet-nbt | https://pypi.org/project/amulet-nbt/#files |

### 方法 3：使用 requirements.txt 批量下载

```bash
# 创建 requirements.txt
cat > requirements.txt << EOF
amulet-core==1.9.33
PyMCTranslate==1.2.39
portalocker>=3.0
platformdirs>=4.0
EOF

# 下载到 wheels 目录
pip download --only-binary=:all: --no-deps -r requirements.txt -d wheels/
```

---

## 更新 blender_manifest.toml

下载完成后，必须同步更新 `blender_manifest.toml`：

```toml
wheels = [
   # 核心 - 跨平台
   "./wheels/amulet_core-1.9.33-py3-none-any.whl",
   "./wheels/pymctranslate-1.2.39-py3-none-any.whl",

   # 工具库 - 跨平台
   "./wheels/portalocker-3.2.0-py3-none-any.whl",
   "./wheels/platformdirs-4.5.1-py3-none-any.whl",

   # Windows 特定依赖 (C扩展/平台相关)
   "./wheels/pywin32-311-cp311-cp311-win_amd64.whl",
   "./wheels/amulet_leveldb-1.0.2-cp311-cp311-win_amd64.whl",
   "./wheels/lz4-4.4.5-cp311-cp311-win_amd64.whl",
   "./wheels/amulet_nbt-2.1.5-cp311-cp311-win_amd64.whl",
   "./wheels/pillow-12.1.0-cp311-cp311-win_amd64.whl",
]
```

---

## 重要注意事项

### 1. Python 版本兼容性

Blender 5.0+ 使用 **Python 3.11**，下载 wheels 时需注意：

| Python 标签 | 含义 |
|-------------|------|
| `cp311` | CPython 3.11 专用（推荐） |
| `py3` | Python 3.x 通用（跨版本兼容） |
| `cp310` | CPython 3.10（可能不兼容） |

### 2. 平台特定依赖

**Windows 特定包必须在 Windows 环境下下载**，因为包含编译的二进制文件。

如果需要在 Linux/macOS 上准备 Windows 依赖：

```bash
# 使用 --platform 参数（Python 3.10+）
pip download --only-binary=:all: --platform win_amd64 \
    --python-version 3.11 --implementation cp --abi cp311 \
    --no-deps -d wheels/ amulet-nbt
```

### 3. 依赖冲突处理

某些包有特定的依赖要求（如 `numpy~=1.17`），使用 `--no-deps` 跳过：

```bash
# 不检查依赖，仅下载 wheel 本身
pip download --no-deps --only-binary=:all: -d wheels/ amulet-core
```

Blender 自带的 numpy 会满足运行时需求。

### 4. 验证完整性

下载后验证文件完整性：

```bash
# 查看文件信息
pip show /path/to/wheel_file.whl

# 或使用 unzip 查看
unzip -l /path/to/wheel_file.whl
```

---

## 测试更新

更新依赖后，需进行以下测试：

### 1. 重新安装插件

```
1. 在 Blender 中：Edit → Preferences → Extensions
2. 卸载旧版本
3. 安装新版本（Blender 会自动安装新的 wheels）
4. 重启 Blender
```

### 2. 功能测试

- [ ] 导入 .schem 文件
- [ ] 导出 .schem 文件
- [ ] 导入 Minecraft 存档
- [ ] 导出到存档
- [ ] 方块注册功能

### 3. 错误日志检查

```
Window → Toggle System Console
# 查找 ImportError 或其他异常
```

---

## 版本锁定建议

对于发布版本，建议在 `requirements.txt` 中锁定具体版本：

```txt
# 锁定版本（生产环境）
amulet-core==1.9.33
PyMCTranslate==1.2.39

# 允许小版本更新（开发环境）
portalocker>=3.0,<4.0
platformdirs>=4.0,<5.0
```

---

## 常见问题

### Q: 为什么有些包下载失败？

A: 可能原因：
- 包名拼写错误（注意 `PyMCTranslate` 的大小写和连字符）
- 平台不匹配（如 Linux 环境下载 Windows 特定包）
- PyPI 上没有该版本的 wheel

### Q: 如何获取最新版本号？

A: 使用 pip 命令查询：

```bash
pip index versions amulet-core
pip index versions PyMCTranslate
```

### Q: mutf8 包在哪里下载？

A: `mutf8` 1.0.6 最高只支持 Python 3.9（cp39），**没有 cp311 版本**。由于它有纯 Python 回退，已从 wheels 列表中移除，pip 会自动安装纯 Python 版本。

### Q: 为什么有些包没有跨平台版本？

A: 包含 C 扩展的包（如 amulet-nbt、lz4、pillow）需要为每个平台单独编译。这些包**无法**提供 `py3-none-any` 版本，因为包含编译的二进制代码。

---

## 更新记录

| 日期 | 更新内容 |
|------|----------|
| 2026-01-14 | **完整更新**：所有依赖更新到最新版本 |
| 2026-01-14 | amulet-nbt: 2.1.3 → **2.1.5** |
| 2026-01-14 | pillow: 10.4.0 → **12.1.0** |
| 2026-01-14 | lz4: 4.3.3 → **4.4.5** |
| 2026-01-14 | pywin32: 306 → **311** |
| 2026-01-14 | mutf8: **已移除**（无 cp311 版本） |
| 2026-01-14 | amulet-core: 1.9.25 → **1.9.33** |
| 2026-01-14 | PyMCTranslate: 1.2.27 → **1.2.39** |
| 2026-01-14 | portalocker: 2.10.1 → **3.2.0** |
| 2026-01-14 | platformdirs: 4.2.2 → **4.5.1** |
