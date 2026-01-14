---
name: blender5_addons
description: Blender 5.0 Python API and add-on development. Use for creating Blender plugins, scripting operators, building UI panels, and extending Blender functionality with Python.
---

# Blender5_Addons Skill

Blender 5.0 python api and add-on development. use for creating blender plugins, scripting operators, building ui panels, and extending blender functionality with python., generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with blender5_addons
- Asking about blender5_addons features or APIs
- Implementing blender5_addons solutions
- Debugging blender5_addons code
- Learning blender5_addons best practices

## Quick Reference

### Common Patterns

**Pattern 1:** You can access Blender’s data with the Python API in the same way as the animation system or user interface; this implies that any setting that can be changed via a button can also be changed with Python. Accessing data from the currently loaded blend-file is done with the module bpy.data. It gives access to library data, for example:

```
bpy.data
```

**Pattern 2:** Simple example:

```
obj = bpy.context.object
obj.location[2] = 0.0
obj.keyframe_insert(data_path="location", frame=10.0, index=2)
obj.location[2] = 1.0
obj.keyframe_insert(data_path="location", frame=20.0, index=2)
```

**Pattern 3:** For example:

```
import bpy
class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Tool Name"

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}

bpy.utils.register_class(SimpleOperator)
```

**Pattern 4:** Class mix-in example:

```
import bpy
class BaseOperator:
    def execute(self, context):
        print("Hello World BaseClass")
        return {'FINISHED'}

class SimpleOperator(bpy.types.Operator, BaseOperator):
    bl_idname = "object.simple_operator"
    bl_label = "Tool Name"

bpy.utils.register_class(SimpleOperator)
```

**Pattern 5:** Note In case you are using complex/multi-inheritance, super() may not work (as the Blender-defined parent may not be the first type in the MRO). It is best then to first explicitly invoke the Blender-defined parent class constructor, before any other. For example: import bpy class FancyRaytracer(AwesomeRaytracer, bpy.types.RenderEngine): def __init__(self, *args, **kwargs): bpy.types.RenderEngine.__init__(self, *args, **kwargs) AwesomeRaytracer.__init__(self, *args, **kwargs) self.my_var = 42 ...

```
super()
```

**Pattern 6:** For example:

```
# Add a new property to an existing type.
bpy.types.Object.my_float: bpy.props.FloatProperty()
# Remove it.
del bpy.types.Object.my_float
```

**Pattern 7:** To avoid expensive recalculations every time a property is modified, Blender defers the evaluation until the results are needed. However, while the script runs you may want to access the updated values. In this case you need to call bpy.types.ViewLayer.update after modifying values, for example:

```
bpy.types.ViewLayer.update
```

**Pattern 8:** Formatted string of file extensions supported by the file handler, each extension should start with a “.” and be separated by “;”. For Example: ".blend;.ble"

```
".blend;.ble"
```

### Example Code Patterns

**Example 1** (yaml):
```yaml
>>> bpy.ops.action.clean(threshold=0.001)
RuntimeError: Operator bpy.ops.action.clean.poll() failed, context is incorrect
```

**Example 2** (yaml):
```yaml
>>> bpy.ops.gpencil.draw()
RuntimeError: Operator bpy.ops.gpencil.draw.poll() Failed to find Grease Pencil data to draw into
```

**Example 3** (python):
```python
from threading import Timer

def my_timer():
      t = Timer(0.1, my_timer)
      t.setDaemon(True)
      t.start()
      print("Running...")

my_timer()
```

**Example 4** (markdown):
```markdown
bpy.data.meshes.new(name=meshid)

# Normally some code, function calls, etc.
bpy.data.meshes[meshid]
```

**Example 5** (markdown):
```markdown
obj.name = objname

# Normally some code, function calls, etc.
obj = bpy.data.meshes[objname]
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **animation.md** - Animation documentation
- **data_access.md** - Data Access documentation
- **getting_started.md** - Getting Started documentation
- **operators.md** - Operators documentation
- **other.md** - Other documentation
- **rendering.md** - Rendering documentation
- **types.md** - Types documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
