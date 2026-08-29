# 依赖升级计划（仅现成 wheel，不自编译）

## 升级清单（7 个文件，URL 已全部核实存在）

| 包 | 现版本 | 升级到 | wheel 形态 | 价值 |
|---|---|---|---|---|
| amulet-nbt | 2.1.5 | 2.1.8 | cp311 win ✓ | 补丁修复，同 API |
| amulet-leveldb | 1.0.2 | 1.0.7 | cp311 win ✓ | 补丁修复 |
| amulet-core | 1.9.33 | 1.9.44 | 纯 Python | 补丁修复（2026-08-10） |
| amulet-rocksdb | （新增） | 1.0.5 | cp311 win ✓ | core 1.9.44 的新依赖 |
| pymctranslate | 1.2.39 | 1.2.47 | 纯 Python | **新 MC 版本方块翻译数据** |
| pillow | 12.1.0 | 12.3.0 | cp311 win ✓ | 例行更新 |
| pywin32 | 311 | 312 | cp311 win ✓ | 例行更新 |

## 步骤

1. curl 下载 7 个新 wheel 到 `wheels/`，删除对应 6 个旧 wheel（11 → 12 个文件）
2. 同步更新 `blender_manifest.toml` 的 wheels 列表（7 处条目）
3. 冒烟验证：优先用本地 Python 3.11（`py -3.11`，若无则检查其它安装）pip --target 安装到临时目录，验证 `import amulet / amulet_nbt / TranslationManager 加载` 正常；确认 amulet-core 1.9.44 对 rocksdb 的导入方式
4. 不提交 git（除非你要求）

## 不动的部分（及理由）

- **lz4 4.4.5 / nbtlib 2.0.4**：已是最新
- **litemapy 0.9.0b0**：0.11.0b0 跨两个 beta 有 API 变更风险，且现版本工作正常，不冒进
- **platformdirs 4.5.1 / portalocker 3.2.0**：大版本跳跃（4.x）无用户价值，且偏离 amulet-core 声明约束已属现状
- **amulet 自编译 cp313**：按你的指示不做