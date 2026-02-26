# MBM_workflow 国际化（i18n）系统实现总结

## 概述

已成功为 MBM_workflow 插件实现了完整的国际化系统，支持中文（zh_CN）和英文（en_US）两种语言。

## 实现的文件

### 新建文件

```
i18n/
├── __init__.py                 # 翻译模块初始化
├── translations.py             # 翻译辅助函数
├── compile_translations.py     # 翻译文件编译脚本
└── locales/
    ├── zh_CN/LC_MESSAGES/
    │   ├── mbm_workflow.po     # 中文翻译源文件
    │   └── mbm_workflow.mo     # 中文翻译编译文件
    └── en_US/LC_MESSAGES/
        ├── mbm_workflow.po     # 英文翻译源文件
        └── mbm_workflow.mo     # 英文翻译编译文件
```

### 修改的文件

1. **load_modules.py** - 集成翻译系统到模块加载流程
2. **ui_panels.py** - 11 个面板类使用翻译函数
3. **ui_lists.py** - UIList 类使用翻译函数
4. **ui_dialogs.py** - 对话框类使用翻译函数
5. **codes/property.py** - 100+ 属性定义使用翻译函数
6. **.gitignore** - 忽略编译后的 .mo 文件

## 翻译辅助函数

### i18n/translations.py

```python
from bpy.app.translations import pgettext_iface as _
from ..i18n.translations import panel_label, operator_label, property_name, enum_item

# 翻译面板标签
bl_label = panel_label("方块")

# 翻译操作符标签
bl_label = operator_label("导入Schem文件二级界面")

# 翻译属性名称
name=property_name("难度")

# 翻译枚举项
items=[
    enum_item("0", "和平", "和平模式"),
    enum_item("1", "简单", "简单模式"),
]
```

## 如何添加新翻译

### 1. 在源代码中使用翻译函数

```python
# 使用 property_name() 翻译属性名称
bpy.types.Scene.new_property = bpy.props.StringProperty(
    name=property_name("新属性"),
    description=property_name("这是新属性的描述")
)

# 使用 panel_label() 翻译面板
class NewPanel(bpy.types.Panel):
    bl_label = panel_label("新面板")

# 使用 operator_label() 翻译操作符
class NewOperator(bpy.types.Operator):
    bl_label = operator_label("新操作")
```

### 2. 添加翻译条目

在 `i18n/locales/zh_CN/LC_MESSAGES/mbm_workflow.po` 中添加：

```po
msgctxt "Property"
msgid "新属性"
msgstr "新属性"

msgctxt "Property"
msgid "这是新属性的描述"
msgstr "这是新属性的描述"
```

在 `i18n/locales/en_US/LC_MESSAGES/mbm_workflow.po` 中添加：

```po
msgctxt "Property"
msgid "新属性"
msgstr "New Property"

msgctxt "Property"
msgid "这是新属性的描述"
msgstr "This is a new property description"
```

### 3. 重新编译翻译文件

```bash
python i18n/compile_translations.py
```

## 测试步骤

### 1. 在 Blender 中重新加载插件

```python
# 在 Blender 控制台中执行
import MBM_workflow
import importlib
importlib.reload(MBM_workflow)

# 或者通过菜单：编辑 → 偏好设置 → 插件 → MBM_workflow → 取消勾选 → 勾选
```

### 2. 检查控制台输出

应该看到以下消息（没有 `_UL_` 和 `_PT_` 警告）：
```
[MBM_workflow] 翻译系统已注册: E:\...\MBM_workflow\i18n\locales
```

### 3. 切换语言测试

**启动 Blender 指定语言：**

```bash
# 中文界面
blender --language zh_CN

# 英文界面
blender --language en_US
```

**在 Blender 中更改语言：**
1. 编辑 → 偏好设置 → 界面 → 翻译
2. 选择语言
3. 保存设置并重启 Blender

## 翻译上下文（msgctxt）

系统使用上下文来区分同名但含义不同的字符串：

| 上下文 | 用途 | 示例 |
|--------|------|------|
| `Panel` | 面板标签 | `panel_label("方块")` |
| `Operator` | 操作符标签 | `operator_label("导入")` |
| `Property` | 属性名称 | `property_name("难度")` |
| `Enum|identifier` | 枚举项 | `enum_item("0", "和平", "和平模式")` |
| `UIList` | UI列表标签 | `ui_list_label("自动")` |

## 注意事项

1. **翻译时机**：翻译必须在类定义时进行（在 `bl_label`、`name` 等属性赋值时），而不是在 `draw()` 方法中。这是性能考虑。

2. **回退机制**：如果某个字符串的翻译不存在，系统会自动回退到原始字符串。

3. **.mo 文件**：编译后的 .mo 文件可以提高加载速度，但 Blender 5.0+ 也可以直接使用 .po 文件。

4. **模块加载顺序**：i18n 模块必须在 UI 模块之前注册翻译系统，在模块列表中最后注册。

## 故障排除

### 翻译没有生效

1. 确认 .mo 文件已生成：
   ```bash
   ls i18n/locales/*/LC_MESSAGES/*.mo
   ```

2. 检查 Blender 控制台是否有错误消息

3. 确认插件已正确重新加载

### 重新编译翻译文件

```bash
# Windows
python i18n\compile_translations.py

# Linux/Mac
python i18n/compile_translations.py
```

## 添加新语言

1. 创建新的语言目录：
   ```
   i18n/locales/ja_JP/LC_MESSAGES/
   ```

2. 复制并翻译 .po 文件：
   ```bash
   cp i18n/locales/zh_CN/LC_MESSAGES/mbm_workflow.po \
      i18n/locales/ja_JP/LC_MESSAGES/mbm_workflow.po
   ```

3. 编辑新的 .po 文件，修改 `Language` 字段并翻译所有 `msgstr` 条目

4. 编译翻译文件：
   ```bash
   python i18n/compile_translations.py
   ```

5. 使用 `blender --language ja_JP` 启动 Blender

## 参考文档

- Blender 翻译系统 API: https://docs.blender.org/api/current/bpy.app.translations.html
- gettext 文档: https://www.gnu.org/software/gettext/manual/
