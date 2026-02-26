# Blender 5.0+ 兼容性指南

本文档记录 MBM_workflow 插件在 Blender 5.0+ 中的兼容性修复和注意事项。

## 概述

从 Blender 4.x 升级到 5.0+ 后，插件需要适配以下变化：

1. **翻译系统 API 变更** - `bpy.app.translations.register()` 参数要求
2. **UI 类命名规范** - Panel 和 UIList 类必须遵循特定命名格式

## 修复历史

### 2025-02-27: 翻译系统和 UI 类命名修复

**提交**: `df419e45`

**问题**:
- 翻译注册失败：`bpy.app.translations.register() argument 2 must be dict, not str`
- Panel 类缺少 `_PT_` 标识符警告
- UIList 类缺少 `_UL_` 标识符警告

**修复内容**:

#### 1. 翻译注册系统 (`i18n/__init__.py`)

实现 `load_translations_dict()` 函数从 .po 文件加载翻译字典：

```python
def load_translations_dict():
    """从 .po 文件加载翻译字典"""
    translations = {}
    locales_path = get_locales_path()

    for locale_name in os.listdir(locales_path):
        po_path = os.path.join(locales_path, locale_name, 'LC_MESSAGES', 'mbm_workflow.po')
        if os.path.exists(po_path):
            locale_translations = _parse_po_file(po_path)
            translations[locale_name] = locale_translations

    return translations

def register_translations():
    translations_dict = load_translations_dict()
    if translations_dict:
        bpy.app.translations.register(TRANSLATION_DOMAIN, translations_dict)
```

**关键变化**:
- 使用 `_parse_po_file()` 解析 .po 文件生成翻译字典
- 不再直接传递文件路径给 `register()`

#### 2. UI 类命名规范

所有 Panel 和 UIList 类已重命名以符合 Blender 5.0+ 规范：

| 旧类名 | 新类名 | 类型 |
|--------|--------|------|
| `MainPanel` | `MBM_PT_main_panel` | Panel |
| `BlockPanel` | `MBM_PT_block_panel` | Panel |
| `ImportPanel` | `MBM_PT_import_panel` | Panel |
| `ExportPanel` | `MBM_PT_export_panel` | Panel |
| `CreateLevel` | `MBM_PT_create_level` | Panel |
| `EditPanel` | `MBM_PT_edit_panel` | Panel |
| `MoreLevelSettings` | `MBM_PT_more_level_settings` | Panel |
| `Ability` | `MBM_PT_ability` | Panel |
| `GameRules` | `MBM_PT_game_rules` | Panel |
| `ResourcepacksPanel` | `MBM_PT_resourcepacks` | Panel |
| `ModPanel` | `MBM_PT_mod` | Panel |
| `ResourcepackList` | `MBM_UL_resourcepack_list` | UIList |
| `ColorToBlockList` | `MBM_UL_color_to_block_list` | UIList |
| `ModList` | `MBM_UL_mod_list` | UIList |
| `SwitchBlockList` | `MBM_UL_switch_block_list` | UIList |

**注意**: 所有 `template_list()` 调用中的类名字符串也已更新。

## 类命名规范

Blender 5.0+ 要求所有 UI 类遵循以下命名格式：

| 类类型 | 命令后缀 | 示例 |
|--------|----------|------|
| Panel | `_PT_*` | `MBM_PT_main_panel` |
| UIList | `_UL_*` | `MBM_UL_mod_list` |
| Operator | `_OT_*` | `MBM_OT_import_schem` |
| Menu | `_MT_*` | `MBM_MT_main_menu` |
| PropertyGroup | `_PG_*` | `MBM_PG_settings` |

**格式**: `{PLUGIN_ID}_{TYPE}_{NAME}`

其中：
- `PLUGIN_ID`: 插件标识符（本插件为 `MBM`）
- `TYPE`: 类类型缩写（PT/UL/OT/MT/PG）
- `NAME`: 类的描述性名称（使用下划线分隔）

## 翻译系统 API 变化

### Blender 4.x 及更早版本

```python
# 直接传递目录路径
bpy.app.translations.register("domain_name", "/path/to/locales")
```

### Blender 5.0+

```python
# 必须传递翻译字典
translations = {
    'zh_CN': {
        ('context', 'message'): '翻译',
        # ... 更多条目
    },
    'en_US': {
        ('context', 'message'): 'Translation',
    }
}
bpy.app.translations.register("domain_name", translations)
```

## 验证方法

### 1. 检查控制台输出

正常启动时应该看到：
```
[MBM_workflow] 加载翻译文件: .../en_US/LC_MESSAGES/mbm_workflow.po (168 条)
[MBM_workflow] 加载翻译文件: .../zh_CN/LC_MESSAGES/mbm_workflow.po (167 条)
[MBM_workflow] 翻译系统已注册: ['en_US', 'zh_CN']
```

**不应该看到**:
- `翻译注册失败: bpy.app.translations.register() argument 2 must be dict`
- `Warning: Class 'XXX' does not follow naming conventions`

### 2. 检查 UI 面板

所有面板应该正常显示，没有布局错乱或缺失。

## 相关文档

- [国际化系统实现总结](i18n-implementation.md)
- [UI 面板参考手册](ui-reference.md)
- [Blender API 文档: bpy.app.translations](https://docs.blender.org/api/current/bpy.app.translations.html)

## 参考资料

- Blender 5.0 Release Notes: https://www.blender.org/download/releases/5-0/
- Python API Migration Guide: https://wiki.blender.org/wiki/Reference/Release_Notes/5.0/Python_API
