# Blender5_Addons - Operators

**Pages:** 80

---

## Operators (bpy.ops)¶

**URL:** https://docs.blender.org/api/current/bpy.ops.html

**Contents:**
- Operators (bpy.ops)¶
- Calling Operators¶
  - Keywords and Positional Arguments¶
- Overriding Context¶
- Execution Context¶

Provides Python access to calling operators, this includes operators written in C++, Python or macros.

Only keyword arguments can be used to pass operator properties.

Operators don’t have return values as you might expect, instead they return a set() which is made up of: {'RUNNING_MODAL', 'CANCELLED', 'FINISHED', 'PASS_THROUGH'}. Common return values are {'FINISHED'} and {'CANCELLED'}, the latter meaning that the operator execution was aborted without making any changes or saving an undo history entry.

If operator was cancelled but there wasn’t any reports from it with {'ERROR'} type, it will just return {'CANCELLED'} without raising any exceptions. However, if there are error reports, a RuntimeError will be raised after the operator finishes execution, including all error report messages, regardless of the return status (even if it was {'FINISHED'}).

Calling an operator in the wrong context will raise a RuntimeError, there is a poll() method to avoid this problem.

Note that the operator ID (bl_idname) in this example is mesh.subdivide, bpy.ops is just the access path for Python.

For calling operators keywords are used for operator properties and positional arguments are used to define how the operator is called.

There are 2 optional positional arguments (documented in detail below).

execution_context - str (enum).

Each of these arguments is optional, but must be given in the order above.

It is possible to override context members that the operator sees, so that they act on specified rather than the selected or active data, or to execute an operator in the different part of the user interface.

The context overrides are passed in as keyword arguments, with keywords matching the context member names in bpy.context. For example to override bpy.context.active_object, you would pass active_object=object to bpy.types.Context.temp_override.

You will nearly always want to use a copy of the actual current context as basis (otherwise, you’ll have to find and gather all needed data yourself).

Context members are names which Blender uses for data access, overrides do not extend to overriding methods or any Python specific functionality.

When calling an operator you may want to pass the execution context.

This determines the context that is given for the operator to run in, and whether invoke() is called or only execute().

EXEC_DEFAULT is used by default, running only the execute() method, but you may want the operator to take user interaction with INVOKE_DEFAULT which will also call invoke() if existing.

The execution context is one of:

INVOKE_REGION_CHANNELS

INVOKE_REGION_PREVIEW

It is also possible to run an operator in a particular part of the user interface. For this we need to pass the window, area and sometimes a region.

**Examples:**

Example 1 (unknown):
```unknown
bpy.ops.test.operator(execution_context, undo)
```

Example 2 (python):
```python
import bpy

# Calling an operator.
bpy.ops.mesh.subdivide(number_cuts=3, smoothness=0.5)


# Check poll() to avoid exception.
if bpy.ops.object.mode_set.poll():
    bpy.ops.object.mode_set(mode='EDIT')
```

Example 3 (swift):
```swift
# Remove all objects in scene rather than the selected ones.
import bpy
from bpy import context
context_override = context.copy()
context_override["selected_objects"] = list(context.scene.objects)
with context.temp_override(**context_override):
    bpy.ops.object.delete()
```

Example 4 (markdown):
```markdown
# Collection add popup.
import bpy
bpy.ops.object.collection_instance_add('INVOKE_DEFAULT')
```

---

## Property Definitions (bpy.props)¶

**URL:** https://docs.blender.org/api/current/bpy.props.html

**Contents:**
- Property Definitions (bpy.props)¶
- Assigning to Existing Classes¶
- Operator Example¶
- PropertyGroup Example¶
- Collection Example¶
- Update Example¶
- Getter/Setter Example¶

This module defines properties to extend Blender’s internal data. The result of these functions is used to assign properties to classes registered with Blender and can’t be used directly.

All parameters to these functions must be passed as keywords.

Custom properties can be added to any subclass of an ID, Bone and PoseBone.

These properties can be animated, accessed by the user interface and Python like Blender’s existing properties.

Access to these properties might happen in threaded context, on a per-data-block level. This has to be carefully considered when using accessors or update callbacks.

Typically, these callbacks should not affect any other data that the one owned by their data-block. When accessing external non-Blender data, thread safety mechanisms should be considered.

A common use of custom properties is for Python based Operator classes. Test this code by running it in the text editor, or by clicking the button in the 3D View-port’s Tools panel. The latter will show the properties in the Redo panel and allow you to change them.

PropertyGroups can be used for collecting custom settings into one value to avoid many individual settings mixed in together.

Custom properties can be added to any subclass of an ID, Bone and PoseBone.

It can be useful to perform an action when a property is changed and can be used to update other properties or synchronize with external data.

All properties define update functions except for CollectionProperty.

Remember that these callbacks may be executed in threaded context.

If the property belongs to an Operator, the update callback’s first parameter will be an OperatorProperties instance, rather than an instance of the operator itself. This means you can’t access other internal functions of the operator, only its other properties.

Accessor functions can be used for boolean, int, float, string and enum properties.

If get or set callbacks are defined, the property will not be stored in the ID properties automatically. Instead, the get and set functions will be called when the property is respectively read or written from the API, and are responsible to handle the data storage.

It is illegal to define a set callback without a matching get one.

When a get callback is defined but no set one, the property is read-only.

get_transform and set_transform can be used when the returned value needs to be modified, but the default internal storage is still used. They can only transform the value before it is set or returned, but do not control how/where that data is stored.

It is possible to define both get/set and get_transform/set_transform callbacks for a same property. In practice however, this should rarely be needed, as most ‘transform’ operation can also happen within a get/set callback.

Remember that these callbacks may be executed in threaded context.

Take care when accessing other properties in these callbacks, as it can easily trigger complex issues, such as infinite loops (if e.g. two properties try to also set the other property’s value in their own set callback), or unexpected side effects due to changes in data, caused e.g. by an update callback.

Returns a new boolean property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype Number Items.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], bool]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, bool], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, bool, bool], bool]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, bool, bool, bool], bool]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new vector boolean property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

default (Sequence[bool]) – sequence of booleans the length of size.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype Number Array Items.

size (int | Sequence[int]) – Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], Sequence[bool]]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, tuple[bool, …]], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, Sequence[bool], bool], Sequence[bool]]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, Sequence[bool], Sequence[bool], bool], Sequence[bool]]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new collection property definition.

type (type[bpy.types.PropertyGroup]) – A subclass of a property group.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Collection Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

Returns a new enumerator property definition.

items (Iterable[tuple[str, str, str] | tuple[str, str, str, int] | tuple[str, str, str, int, int] | None] | Callable[[bpy.types.bpy_struct, bpy.types.Context | None], Iterable[tuple[str, str, str] | tuple[str, str, str, int] | tuple[str, str, str, int, int] | None]]) – sequence of enum items formatted: [(identifier, name, description, icon, number), ...]. The first three elements of the tuples are mandatory. identifier: The identifier is used for Python access. An empty identifier means that the item is a separator name: Name for the interface. description: Used for documentation and tooltips. icon: An icon string identifier or integer icon value (e.g. returned by bpy.types.UILayout.icon) number: Unique value used as the identifier for this item (stored in file data). Use when the identifier may need to change. If the ENUM_FLAG option is used, the values are bit-masks and should be powers of two. When an item only contains 4 items they define (identifier, name, description, number). Separators may be added using either None (nameless separator), or a regular item tuple with an empty identifier string, in which case the name, if non-empty, will be displayed in the UI above the separator line. For dynamic values a callback can be passed which returns a list in the same format as the static list. This function must take 2 arguments (self, context), context may be None. Warning There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.

sequence of enum items formatted: [(identifier, name, description, icon, number), ...].

The first three elements of the tuples are mandatory.

The identifier is used for Python access. An empty identifier means that the item is a separator

Name for the interface.

Used for documentation and tooltips.

An icon string identifier or integer icon value (e.g. returned by bpy.types.UILayout.icon)

Unique value used as the identifier for this item (stored in file data). Use when the identifier may need to change. If the ENUM_FLAG option is used, the values are bit-masks and should be powers of two.

When an item only contains 4 items they define (identifier, name, description, number).

Separators may be added using either None (nameless separator), or a regular item tuple with an empty identifier string, in which case the name, if non-empty, will be displayed in the UI above the separator line. For dynamic values a callback can be passed which returns a list in the same format as the static list. This function must take 2 arguments (self, context), context may be None.

There is a known bug with using a callback, Python must keep a reference to the strings returned by the callback or Blender will misbehave or even crash.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

default (str | int | set[str]) – The default value for this enum, a string from the identifiers used in items, or integer matching an item number. If the ENUM_FLAG option is used this must be a set of such string identifiers instead. WARNING: Strings cannot be specified for dynamic enums (i.e. if a callback function is given as items parameter).

options (set[str]) – Enumerator in Property Flag Enum Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], int]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, int], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, int, bool], int]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, int, int, bool], int]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new float (single precision) property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

min (float) – Hard minimum, trying to assign a value below will silently assign this minimum instead.

max (float) – Hard maximum, trying to assign a value above will silently assign this maximum instead.

soft_min (float) – Soft minimum (>= min), user won’t be able to drag the widget below this value in the UI.

soft_max (float) – Soft maximum (<= max), user won’t be able to drag the widget above this value in the UI.

step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).

precision (int) – Maximum number of decimal digits to display, in [0, 6]. Fraction is automatically hidden for exact integer values of fields with unit ‘NONE’ or ‘TIME’ (frame count) and step divisible by 100.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype Number Items.

unit (str) – Enumerator in Property Unit Items.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], float]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, float], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, float, bool], float]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, float, float, bool], float]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new vector float property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

default (Sequence[float]) – Sequence of floats the length of size.

min (float) – Hard minimum, trying to assign a value below will silently assign this minimum instead.

max (float) – Hard maximum, trying to assign a value above will silently assign this maximum instead.

soft_min (float) – Soft minimum (>= min), user won’t be able to drag the widget below this value in the UI.

soft_max (float) – Soft maximum (<= max), user won’t be able to drag the widget above this value in the UI.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).

precision (int) – Maximum number of decimal digits to display, in [0, 6]. Fraction is automatically hidden for exact integer values of fields with unit ‘NONE’ or ‘TIME’ (frame count) and step divisible by 100.

subtype (str) – Enumerator in Property Subtype Number Array Items.

unit (str) – Enumerator in Property Unit Items.

size (int | Sequence[int]) – Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], Sequence[float]]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, tuple[float, …]], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, Sequence[float], bool], Sequence[float]]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, Sequence[float], Sequence[float], bool], Sequence[float]]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new int property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

min (int) – Hard minimum, trying to assign a value below will silently assign this minimum instead.

max (int) – Hard maximum, trying to assign a value above will silently assign this maximum instead.

soft_min (int) – Soft minimum (>= min), user won’t be able to drag the widget below this value in the UI.

soft_max (int) – Soft maximum (<= max), user won’t be able to drag the widget above this value in the UI.

step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 1 (WARNING: unused currently!).

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype Number Items.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], int]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, int], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, int, bool], int]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, int, int, bool], int]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new vector int property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

default (Sequence[int]) – sequence of ints the length of size.

min (int) – Hard minimum, trying to assign a value below will silently assign this minimum instead.

max (int) – Hard maximum, trying to assign a value above will silently assign this maximum instead.

soft_min (int) – Soft minimum (>= min), user won’t be able to drag the widget below this value in the UI.

soft_max (int) – Soft maximum (<= max), user won’t be able to drag the widget above this value in the UI.

step (int) – Step of increment/decrement in UI, in [1, 100], defaults to 1 (WARNING: unused currently!).

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype Number Array Items.

size (int | Sequence[int]) – Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], Sequence[int]]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, tuple[int, …]], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, Sequence[int], bool], Sequence[int]]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, Sequence[int], Sequence[int], bool], Sequence[int]]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Returns a new pointer property definition.

type (type[bpy.types.PropertyGroup | bpy.types.ID]) – A subclass of a property group or ID types.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

poll (Callable[[bpy.types.bpy_struct, bpy.types.ID], bool]) – Function that determines whether an item is valid for this property. The function must take 2 values (self, object) and return a boolean. Note The return value will be checked only when assigning an item from the UI, but it is still possible to assign an “invalid” item to the property directly.

Function that determines whether an item is valid for this property. The function must take 2 values (self, object) and return a boolean.

The return value will be checked only when assigning an item from the UI, but it is still possible to assign an “invalid” item to the property directly.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

Pointer properties do not support storing references to embedded IDs (e.g. bpy.types.Scene.collection, bpy.types.Material.node_tree). These should exclusively be referenced and accessed through their owner ID (e.g. the scene or material).

Removes a dynamically defined property.

cls (type) – The class containing the property (must be a positional argument).

attr (str) – Property name (must be passed as a keyword).

Typically this function doesn’t need to be accessed directly. Instead use del cls.attr

Returns a new string property definition.

name (str) – Name used in the user interface.

description (str) – Text used for the tooltip and api documentation.

translation_context (str) – Text used as context to disambiguate translations.

default (str) – initializer string.

maxlen (int) – maximum length of the string.

options (set[str]) – Enumerator in Property Flag Items.

override (set[str]) – Enumerator in Property Override Flag Items.

tags (set[str]) – Enumerator of tags that are defined by parent class.

subtype (str) – Enumerator in Property Subtype String Items.

update (Callable[[bpy.types.bpy_struct, bpy.types.Context], None]) – Function to be called when this value is modified, This function must take 2 values (self, context) and return None. Warning there are no safety checks to avoid infinite recursion.

get (Callable[[bpy.types.bpy_struct], str]) – Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property. Note Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

Function to be called when this value is ‘read’, and the default, system-defined storage is not used for this property. This function must take 1 value (self) and return the value of the property.

Defining this callback without a matching set one will make the property read-only (even if READ_ONLY option is not set).

set (Callable[[bpy.types.bpy_struct, str], None]) – Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None. Note Defining this callback without a matching get one is invalid.

Function to be called when this value is ‘written’, and the default, system-defined storage is not used for this property. This function must take 2 values (self, value) and return None.

Defining this callback without a matching get one is invalid.

get_transform (Callable[[bpy.types.bpy_struct, str, bool], str]) – Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘read’, if some additional processing must be performed on the stored value. This function must take three arguments (self, the stored value, and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits of the property (min/max, length…) are respected. Otherwise a ValueError exception is raised.

set_transform (Callable[[bpy.types.bpy_struct, str, str, bool], str]) – Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property. Note The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

Function to be called when this value is ‘written’, if some additional processing must be performed on the given value before storing it. This function must take four arguments (self, the given value to store, the currently stored value (‘raw’ value, without any get_transform applied to it), and a boolean indicating if the property is currently set), and return the final, transformed value of the property.

The callback is responsible to ensure that value limits (min/max, length…) are respected. Otherwise a ValueError exception is raised.

search (Callable[[bpy.types.bpy_struct, bpy.types.Context, str], Iterable[str | tuple[str, str]]]) – Function to be called to show candidates for this string (shown in the UI). This function must take 3 values (self, context, edit_text) and return a sequence, iterator or generator where each item must be: A single string (representing a candidate to display). A tuple-pair of strings, where the first is a candidate and the second is additional information about the candidate.

Function to be called to show candidates for this string (shown in the UI). This function must take 3 values (self, context, edit_text) and return a sequence, iterator or generator where each item must be:

A single string (representing a candidate to display).

A tuple-pair of strings, where the first is a candidate and the second is additional information about the candidate.

search_options (set[str]) – Set of strings in: ’SORT’ sorts the resulting items. ’SUGGESTION’ lets the user enter values not found in search candidates. WARNING disabling this flag causes the search callback to run on redraw, so only disable this flag if it’s not likely to cause performance issues.

’SORT’ sorts the resulting items.

’SUGGESTION’ lets the user enter values not found in search candidates. WARNING disabling this flag causes the search callback to run on redraw, so only disable this flag if it’s not likely to cause performance issues.

**Examples:**

Example 1 (markdown):
```markdown
import bpy

# Assign a custom property to an existing type.
bpy.types.Material.custom_float = bpy.props.FloatProperty(name="Test Property")

# Test the property is there.
bpy.data.materials[0].custom_float = 5.0
```

Example 2 (swift):
```swift
import bpy


class OBJECT_OT_property_example(bpy.types.Operator):
    bl_idname = "object.property_example"
    bl_label = "Property Example"
    bl_options = {'REGISTER', 'UNDO'}

    my_float: bpy.props.FloatProperty(name="Some Floating Point")
    my_bool: bpy.props.BoolProperty(name="Toggle Option")
    my_string: bpy.props.StringProperty(name="String Value")

    def execute(self, context):
        self.report(
            {'INFO'}, "F: {:.2f}  B: {!s}  S: {!r}".format(
                self.my_float, self.my_bool, self.my_string,
            )
        )
        print('My float:', self.my_float)
        print('My bool:', self.my_bool)
        print('My string:', self.my_string)
        return {'FINISHED'}


class OBJECT_PT_property_example(bpy.types.Panel):
    bl_idname = "object_PT_property_example"
    bl_label = "Property Example"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        # You can set the property values that should be used when the user
        # presses the button in the UI.
        props = self.layout.operator('object.property_example')
        props.my_bool = True
        props.my_string = "Shouldn't that be 47?"

        # You can set properties dynamically:
        if context.object:
            props.my_float = context.object.location.x
        else:
            props.my_float = 327


bpy.utils.register_class(OBJECT_OT_property_example)
bpy.utils.register_class(OBJECT_PT_property_example)

# Demo call. Be sure to also test in the 3D Viewport.
bpy.ops.object.property_example(
    my_float=47,
    my_bool=True,
    my_string="Shouldn't that be 327?",
)
```

Example 3 (php):
```php
import bpy


class MaterialSettings(bpy.types.PropertyGroup):
    my_int: bpy.props.IntProperty()
    my_float: bpy.props.FloatProperty()
    my_string: bpy.props.StringProperty()


bpy.utils.register_class(MaterialSettings)

bpy.types.Material.my_settings = bpy.props.PointerProperty(type=MaterialSettings)

# Test the new settings work.
material = bpy.data.materials[0]

material.my_settings.my_int = 5
material.my_settings.my_float = 3.0
material.my_settings.my_string = "Foo"
```

Example 4 (python):
```python
import bpy


# Assign a collection.
class SceneSettingItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Test Property", default="Unknown")
    value: bpy.props.IntProperty(name="Test Property", default=22)


bpy.utils.register_class(SceneSettingItem)

bpy.types.Scene.my_settings = bpy.props.CollectionProperty(type=SceneSettingItem)

# Assume an armature object selected.
print("Adding 2 values!")

my_item = bpy.context.scene.my_settings.add()
my_item.name = "Spam"
my_item.value = 1000

my_item = bpy.context.scene.my_settings.add()
my_item.name = "Eggs"
my_item.value = 30

for my_item in bpy.context.scene.my_settings:
    print(my_item.name, my_item.value)
```

---

## Using Operators¶

**URL:** https://docs.blender.org/api/current/info_gotchas_operators.html

**Contents:**
- Using Operators¶
- Why does an operator’s poll fail?¶
- The operator still doesn’t work!¶

Blender’s operators are tools for users to access, that can be accessed with Python too which is very useful. Still operators have limitations that can make them cumbersome to script.

Can’t pass data such as objects, meshes or materials to operate on (operators use the context instead).

The return value from calling an operator is the success (if it finished or was canceled), in some cases it would be more logical from an API perspective to return the result of the operation.

Operators’ poll function can fail where an API function would raise an exception giving details on exactly why.

When calling an operator it gives an error like this:

Which raises the question as to what the correct context might be?

Typically operators check for the active area type, a selection or active object they can operate on, but some operators are more strict when they run. In most cases you can figure out what context an operator needs by examining how it’s used in Blender and thinking about what it does.

If you’re still stuck, unfortunately, the only way to eventually know what is causing the error is to read the source code for the poll function and see what it is checking. For Python operators it’s not so hard to find the source since it’s included with Blender and the source file and line is included in the operator reference docs. Downloading and searching the C code isn’t so simple, especially if you’re not familiar with the C language but by searching the operator name or description you should be able to find the poll function with no knowledge of C.

Blender does have the functionality for poll functions to describe why they fail, but it’s currently not used much, if you’re interested to help improve the API feel free to add calls to bpy.types.Operator.poll_message_set (CTX_wm_operator_poll_msg_set in C) where it’s not obvious why poll fails, e.g:

In some cases using bpy.types.Context.temp_override to enable temporary logging or using the context category when logging can help.

Certain operators in Blender are only intended for use in a specific context, some operators for example are only called from the properties editor where they check the current material, modifier or constraint.

Examples of this are:

bpy.ops.texture.slot_move

bpy.ops.constraint.limitdistance_reset

bpy.ops.object.modifier_copy

bpy.ops.buttons.file_browse

Another possibility is that you are the first person to attempt to use this operator in a script and some modifications need to be made to the operator to run in a different context. If the operator should logically be able to run but fails when accessed from a script it should be reported to the bug tracker.

**Examples:**

Example 1 (yaml):
```yaml
>>> bpy.ops.action.clean(threshold=0.001)
RuntimeError: Operator bpy.ops.action.clean.poll() failed, context is incorrect
```

Example 2 (yaml):
```yaml
>>> bpy.ops.gpencil.draw()
RuntimeError: Operator bpy.ops.gpencil.draw.poll() Failed to find Grease Pencil data to draw into
```

---

## Anim Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.anim.html

**Contents:**
- Anim Operators¶

Interactively change the current frame number

frame (float in [-1.04857e+06, 1.04857e+06], (optional)) – Frame

snap (boolean, (optional)) – Snap

seq_solo_preview (boolean, (optional)) – Strip Preview

Select all keyframes of channel under mouse

extend (boolean, (optional)) – Extend, Extend selection

Reset viewable area to show the channel under the cursor

include_handles (boolean, (optional)) – Include Handles, Include handles of keyframes when calculating extents

use_preview_range (boolean, (optional)) – Use Preview Range, Ignore frames outside of the preview range

Create keyframes following the current shape of F-Curves of selected channels

range (int array of 2 items in [-inf, inf], (optional)) – Frame Range, The range in which to create new keys

step (float in [0.01, inf], (optional)) – Frame Step, At which interval to add keys

remove_outside_range (boolean, (optional)) – Remove Outside Range, Removes keys outside the given range, leaving only the newly baked

interpolation_type (enum in ['BEZIER', 'LIN', 'CONST'], (optional)) – Interpolation Type, Choose the interpolation type with which new keys will be added BEZIER Bézier – New keys will be Bézier. LIN Linear – New keys will be linear. CONST Constant – New keys will be constant.

Interpolation Type, Choose the interpolation type with which new keys will be added

BEZIER Bézier – New keys will be Bézier.

LIN Linear – New keys will be linear.

CONST Constant – New keys will be constant.

bake_modifiers (boolean, (optional)) – Bake Modifiers, Bake Modifiers into keyframes and delete them after

Delete all empty animation data containers from visible data-blocks

Handle mouse clicks over animation channels

extend (boolean, (optional)) – Extend Select

extend_range (boolean, (optional)) – Extend Range, Selection of active channel to clicked channel

children_only (boolean, (optional)) – Select Children Only

Collapse (close) all selected expandable animation channels

all (boolean, (optional)) – All, Collapse all channels (not just selected ones)

Delete all selected animation channels

Toggle editability of selected channels

mode (enum in ['TOGGLE', 'DISABLE', 'ENABLE', 'INVERT'], (optional)) – Mode

type (enum in ['PROTECT', 'MUTE'], (optional)) – Type

Expand (open) all selected expandable animation channels

all (boolean, (optional)) – All, Expand all channels (not just selected ones)

Clear ‘disabled’ tag from all F-Curves to get broken F-Curves working again

Add selected F-Curves to a new group

name (string, (optional, never None)) – Name, Name of newly created group

Rearrange selected animation channels

direction (enum in ['TOP', 'UP', 'DOWN', 'BOTTOM'], (optional)) – Direction

Rename animation channel under mouse

Toggle selection of all animation channels

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all animation channels within the specified region

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

deselect (boolean, (optional)) – Deselect, Deselect rather than select items

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

Start entering text which filters the set of channels shown to only include those with matching names

Disable specified setting on all selected animation channels

mode (enum in ['TOGGLE', 'DISABLE', 'ENABLE', 'INVERT'], (optional)) – Mode

type (enum in ['PROTECT', 'MUTE'], (optional)) – Type

Enable specified setting on all selected animation channels

mode (enum in ['TOGGLE', 'DISABLE', 'ENABLE', 'INVERT'], (optional)) – Mode

type (enum in ['PROTECT', 'MUTE'], (optional)) – Type

Toggle specified setting on all selected animation channels

mode (enum in ['TOGGLE', 'DISABLE', 'ENABLE', 'INVERT'], (optional)) – Mode

type (enum in ['PROTECT', 'MUTE'], (optional)) – Type

Remove selected F-Curves from their current groups

Reset viewable area to show the selected channels

include_handles (boolean, (optional)) – Include Handles, Include handles of keyframes when calculating extents

use_preview_range (boolean, (optional)) – Use Preview Range, Ignore frames outside of the preview range

Mark actions with no F-Curves for deletion after save and reload of file preserving “action libraries”

only_unused (boolean, (optional)) – Only Unused, Only unused (Fake User only) actions get considered

startup/bl_operators/anim.py:365

Convert a legacy Action to a layered Action on the active object

Copy the driver for the highlighted button

Add driver for the property under the cursor

Edit the drivers for the connected property represented by the highlighted button

Remove the driver(s) for the connected property(s) represented by the highlighted button

all (boolean, (optional)) – All, Delete drivers for all elements of the array

Set the current frame as the preview or scene end frame

Clear all keyframes on the currently active property

all (boolean, (optional)) – All, Clear keyframes from all elements of the array

Remove all keyframe animation for selected objects

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Remove all keyframe animation for selected strips

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Delete keyframes on the current frame for all properties in the specified Keying Set

type (enum in ['DEFAULT'], (optional)) – Keying Set, The Keying Set to use

Delete current keyframe of current UI-active property

all (boolean, (optional)) – All, Delete keyframes from all elements of the array

Alternate access to ‘Delete Keyframe’ for keymaps to use

type (string, (optional, never None)) – Keying Set, The Keying Set to use

Remove keyframes on current frame for selected objects and bones

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Remove keyframes on current frame for selected strips

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Insert keyframes on the current frame using either the active keying set, or the user preferences if no keying set is active

type (enum in ['DEFAULT'], (optional)) – Keying Set, The Keying Set to use

Insert a keyframe for current UI-active property

all (boolean, (optional)) – All, Insert a keyframe for all element of the array

Alternate access to ‘Insert Keyframe’ for keymaps to use

type (string, (optional, never None)) – Keying Set, The Keying Set to use

Insert Keyframes for specified Keying Set, with menu of available Keying Sets if undefined

type (enum in ['DEFAULT'], (optional)) – Keying Set, The Keying Set to use

always_prompt (boolean, (optional)) – Always Show Menu

Set a new active keying set

type (enum in ['DEFAULT'], (optional)) – Keying Set, The Keying Set to use

Add a new (empty) keying set to the active Scene

Export Keying Set to a Python script

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_text (boolean, (optional)) – Filter text

filter_python (boolean, (optional)) – Filter Python

startup/bl_operators/anim.py:46

Add empty path to active keying set

Remove active Path from active keying set

Remove the active keying set

Add current UI-active property to current keying set

all (boolean, (optional)) – All, Add all elements of the array to a Keying Set

Remove current UI-active property from current keying set

Merge the animation of the selected objects into the action of the active object. Actions are not deleted by this, but might end up with zero users

Paste the driver in the internal clipboard to the highlighted button

Interactively define frame range used for playback

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Reset the horizontal view to the current scene frame range, taking the preview range into account if it is active

Move all slots of the action on the active object into newly created, separate actions. All users of those slots will be reassigned to the new actions. The current action won’t be deleted but will be empty and might end up having zero users

Move the selected slots into a newly created action

Create a new action slot for this data-block, to hold its animation

startup/bl_operators/anim.py:722

Un-assign the action slot from this constraint

startup/bl_operators/anim.py:780

Un-assign the action slot, effectively making this data-block non-animated

startup/bl_operators/anim.py:759

Un-assign the action slot from this NLA strip, effectively making it non-animated

startup/bl_operators/anim.py:780

Set the current frame as the preview or scene start frame

Update f-curves/drivers affecting Transform constraints (use it with files from 2.70 and earlier)

use_convert_to_radians (boolean, (optional)) – Convert to Radians, Convert f-curves/drivers affecting rotations to radians.Warning: Use this only once

startup/bl_operators/anim.py:400

Moves any F-Curves for the hide property of selected armatures into the action of the object. This will only operate on the first layer and strip of the action

startup/bl_operators/anim.py:843

Frame the property under the cursor in the Graph Editor

all (boolean, (optional)) – Show All, Frame the whole array property instead of only the index under the cursor

isolate (boolean, (optional)) – Isolate, Hides all F-Curves other than the ones being framed

---

## Action Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.action.html

**Contents:**
- Action Operators¶

Add keyframes on every frame between the selected keyframes

Simplify F-Curves by removing closely spaced keyframes

threshold (float in [0, inf], (optional)) – Threshold

channels (boolean, (optional)) – Channels

Select keyframes by clicking on them

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend Select, Toggle keyframe selection instead of leaving newly selected keyframes only

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

column (boolean, (optional)) – Column Select, Select all keyframes that occur on the same frame as the one under the mouse

channel (boolean, (optional)) – Only Channel, Select all the keyframes in the channel under the mouse

Copy selected keyframes to the internal clipboard

Remove all selected keyframes

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Make a copy of all selected keyframes

Make a copy of all selected keyframes and move them

ACTION_OT_duplicate (ACTION_OT_duplicate, (optional)) – Duplicate Keyframes, Make a copy of all selected keyframes

TRANSFORM_OT_transform (TRANSFORM_OT_transform, (optional)) – Transform, Transform selected items by mode type

Set easing type for the F-Curve segments starting from the selected keyframes

type (enum in Beztriple Interpolation Easing Items, (optional)) – Type

Set extrapolation mode for selected F-Curves

type (enum in ['CONSTANT', 'LINEAR', 'MAKE_CYCLIC', 'CLEAR_CYCLIC'], (optional)) – Type CONSTANT Constant Extrapolation – Values on endpoint keyframes are held. LINEAR Linear Extrapolation – Straight-line slope of end segments are extended past the endpoint keyframes. MAKE_CYCLIC Make Cyclic (F-Modifier) – Add Cycles F-Modifier if one does not exist already. CLEAR_CYCLIC Clear Cyclic (F-Modifier) – Remove Cycles F-Modifier if not needed anymore.

CONSTANT Constant Extrapolation – Values on endpoint keyframes are held.

LINEAR Linear Extrapolation – Straight-line slope of end segments are extended past the endpoint keyframes.

MAKE_CYCLIC Make Cyclic (F-Modifier) – Add Cycles F-Modifier if one does not exist already.

CLEAR_CYCLIC Clear Cyclic (F-Modifier) – Remove Cycles F-Modifier if not needed anymore.

Set the current frame to the average frame value of selected keyframes

Set type of handle for selected keyframes

type (enum in Keyframe Handle Type Items, (optional)) – Type

Set interpolation mode for the F-Curve segments starting from the selected keyframes

type (enum in Beztriple Interpolation Mode Items, (optional)) – Type

Insert keyframes for the specified channels

type (enum in ['ALL', 'SEL', 'GROUP'], (optional)) – Type

Set type of keyframe for the selected keyframes

type (enum in Beztriple Keyframe Type Items, (optional)) – Type

Move selected scene markers to the active Action as local ‘pose’ markers

Flip selected keyframes over the selected mirror line

type (enum in ['CFRA', 'XAXIS', 'MARKER'], (optional)) – Type CFRA By Times Over Current Frame – Flip times of selected keyframes using the current frame as the mirror line. XAXIS By Values Over Zero Value – Flip values of selected keyframes (i.e. negative values become positive, and vice versa). MARKER By Times Over First Selected Marker – Flip times of selected keyframes using the first selected marker as the reference point.

CFRA By Times Over Current Frame – Flip times of selected keyframes using the current frame as the mirror line.

XAXIS By Values Over Zero Value – Flip values of selected keyframes (i.e. negative values become positive, and vice versa).

MARKER By Times Over First Selected Marker – Flip times of selected keyframes using the first selected marker as the reference point.

Paste keyframes from the internal clipboard for the selected channels, starting on the current frame

offset (enum in Keyframe Paste Offset Items, (optional)) – Offset, Paste time offset of keys

merge (enum in Keyframe Paste Merge Items, (optional)) – Type, Method of merging pasted keys and existing

flipped (boolean, (optional)) – Flipped, Paste keyframes from mirrored bones if they exist

Set Preview Range based on extents of selected Keyframes

Push action down on to the NLA stack as a new strip

Toggle selection of all keyframes

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all keyframes within the specified region

axis_range (boolean, (optional)) – Axis Range

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

tweak (boolean, (optional)) – Tweak, Operator has been activated using a click-drag event

Select keyframe points using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select all keyframes on the specified frame(s)

mode (enum in ['KEYS', 'CFRA', 'MARKERS_COLUMN', 'MARKERS_BETWEEN'], (optional)) – Mode

Select keyframe points using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select keyframes to the left or the right of the current frame

mode (enum in ['CHECK', 'LEFT', 'RIGHT'], (optional)) – Mode

extend (boolean, (optional)) – Extend Select

Deselect keyframes on ends of selection islands

Select keyframes occurring in the same F-Curves as selected ones

Select keyframes beside already selected ones

Snap selected keyframes to the times specified

type (enum in ['CFRA', 'NEAREST_FRAME', 'NEAREST_SECOND', 'NEAREST_MARKER'], (optional)) – Type CFRA Selection to Current Frame – Snap selected keyframes to the current frame. NEAREST_FRAME Selection to Nearest Frame – Snap selected keyframes to the nearest (whole) frame (use to fix accidental subframe offsets). NEAREST_SECOND Selection to Nearest Second – Snap selected keyframes to the nearest second. NEAREST_MARKER Selection to Nearest Marker – Snap selected keyframes to the nearest marker.

CFRA Selection to Current Frame – Snap selected keyframes to the current frame.

NEAREST_FRAME Selection to Nearest Frame – Snap selected keyframes to the nearest (whole) frame (use to fix accidental subframe offsets).

NEAREST_SECOND Selection to Nearest Second – Snap selected keyframes to the nearest second.

NEAREST_MARKER Selection to Nearest Marker – Snap selected keyframes to the nearest marker.

Store this action in the NLA stack as a non-contributing strip for later use

create_new (boolean, (optional)) – Create New Action, Create a new action once the existing one has been safely stored

Store this action in the NLA stack as a non-contributing strip for later use, and create a new action

Unlink this action from the active action slot (and/or exit Tweak Mode)

force_delete (boolean, (optional)) – Force Delete, Clear Fake User and remove copy stashed in this data-block’s NLA stack

Reset viewable area to show full keyframe range

Move the view to the current frame

Reset viewable area to show selected keyframes range

---

## Armature Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.armature.html

**Contents:**
- Armature Operators¶

Align selected bones to the active bone (or to their parent)

Assign all selected bones to a collection, or unassign them, depending on whether the active bone is already assigned or not

collection_index (int in [-1, inf], (optional)) – Collection Index, Index of the collection to assign selected bones to. When the operator should create a new bone collection, use new_collection_name to define the collection name, and set this parameter to the parent index of the new bone collection

new_collection_name (string, (optional, never None)) – Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and assign the selected bones to it. To assign to an existing collection, do not include this parameter and use collection_index

Automatically renames the selected bones according to which side of the target axis they fall on

type (enum in ['XAXIS', 'YAXIS', 'ZAXIS'], (optional)) – Axis, Axis to tag names with XAXIS X-Axis – Left/Right. YAXIS Y-Axis – Front/Back. ZAXIS Z-Axis – Top/Bottom.

Axis, Axis to tag names with

XAXIS X-Axis – Left/Right.

YAXIS Y-Axis – Front/Back.

ZAXIS Z-Axis – Top/Bottom.

Add a new bone located at the 3D cursor

name (string, (optional, never None)) – Name, Name of the newly created bone

Automatically fix alignment of select bones’ axes

type (enum in ['POS_X', 'POS_Z', 'GLOBAL_POS_X', 'GLOBAL_POS_Y', 'GLOBAL_POS_Z', 'NEG_X', 'NEG_Z', 'GLOBAL_NEG_X', 'GLOBAL_NEG_Y', 'GLOBAL_NEG_Z', 'ACTIVE', 'VIEW', 'CURSOR'], (optional)) – Type

axis_flip (boolean, (optional)) – Flip Axis, Negate the alignment axis

axis_only (boolean, (optional)) – Shortest Rotation, Ignore the axis direction, use the shortest rotation to align

Create a new bone going from the last selected joint to the mouse position

Add a new bone collection

Add selected bones to the chosen bone collection

name (string, (optional, never None)) – Bone Collection, Name of the bone collection to assign this bone to; empty to assign to the active bone collection

Create a new bone collection and assign all selected bones

name (string, (optional, never None)) – Bone Collection, Name of the bone collection to create

Deselect bones of active Bone Collection

Change position of active Bone Collection in list of Bone collections

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active Bone Collection towards

Remove the active bone collection

Remove all bone collections that have neither bones nor children. This is done recursively, so bone collections that only have unused children are also removed

startup/bl_operators/anim.py:617

Select bones in active Bone Collection

Show all bone collections

startup/bl_operators/anim.py:572

Remove selected bones from the active bone collection

name (string, (optional, never None)) – Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection

Unassign the named bone from this bone collection

name (string, (optional, never None)) – Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection

bone_name (string, (optional, never None)) – Bone Name, Name of the bone to unassign from the collection; empty to use the active bone

Clear the ‘solo’ setting on all bone collections

startup/bl_operators/anim.py:595

Copy the bone color of the active bone to all selected bones

bone_type (enum in ['EDIT', 'POSE'], (optional)) – Type EDIT Bone – Copy Bone colors from the active bone to all selected bones. POSE Pose Bone – Copy Pose Bone colors from the active pose bone to all selected pose bones.

EDIT Bone – Copy Bone colors from the active bone to all selected bones.

POSE Pose Bone – Copy Pose Bone colors from the active pose bone to all selected pose bones.

startup/bl_operators/anim.py:491

Remove selected bones from the armature

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Dissolve selected bones from the armature

Make copies of the selected bones within the same armature

do_flip_names (boolean, (optional)) – Flip Names, Try to flip names of the bones, if possible, instead of adding a number extension

Make copies of the selected bones within the same armature and move them

ARMATURE_OT_duplicate (ARMATURE_OT_duplicate, (optional)) – Duplicate Selected Bone(s), Make copies of the selected bones within the same armature

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Create new bones from the selected joints

forked (boolean, (optional)) – Forked

Create new bones from the selected joints and move them

ARMATURE_OT_extrude (ARMATURE_OT_extrude, (optional)) – Extrude, Create new bones from the selected joints

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Create new bones from the selected joints and move them

ARMATURE_OT_extrude (ARMATURE_OT_extrude, (optional)) – Extrude, Create new bones from the selected joints

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Add bone between selected joint(s) and/or 3D cursor

Flips (and corrects) the axis suffixes of the names of selected bones

do_strip_numbers (boolean, (optional)) – Strip Numbers, Try to remove right-most dot-number from flipped names.Warning: May result in incoherent naming in some cases

Tag selected bones to not be visible in Edit Mode

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Move bones to a collection

collection_index (int in [-1, inf], (optional)) – Collection Index, Index of the collection to move selected bones to. When the operator should create a new bone collection, do not include this parameter and pass new_collection_name

new_collection_name (string, (optional, never None)) – Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and move the selected bones to it. To move to an existing collection, do not include this parameter and use collection_index

Remove the parent-child relationship between selected bones and their parents

type (enum in ['CLEAR', 'DISCONNECT'], (optional)) – Clear Type, What way to clear parenting

Set the active bone as the parent of the selected bones

type (enum in ['CONNECTED', 'OFFSET'], (optional)) – Parent Type, Type of parenting

Reveal all bones hidden in Edit Mode

select (boolean, (optional)) – Select

Clear roll for selected bones

roll (float in [-6.28319, 6.28319], (optional)) – Roll

Toggle selection status of all bones

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select immediate parent/children of selected bones

direction (enum in ['PARENT', 'CHILD'], (optional)) – Direction

extend (boolean, (optional)) – Extend, Extend the selection

Deselect those bones at the boundary of each selection region

Select all bones linked by parent/child connections to the current selection

all_forks (boolean, (optional)) – All Forks, Follow forks in the parents chain

(De)select bones linked by parent/child connections under the mouse cursor

deselect (boolean, (optional)) – Deselect

all_forks (boolean, (optional)) – All Forks, Follow forks in the parents chain

Mirror the bone selection

only_active (boolean, (optional)) – Active Only, Only operate on the active bone

extend (boolean, (optional)) – Extend, Extend the selection

Select those bones connected to the initial selection

Select similar bones by property types

type (enum in ['CHILDREN', 'CHILDREN_IMMEDIATE', 'SIBLINGS', 'LENGTH', 'DIRECTION', 'PREFIX', 'SUFFIX', 'BONE_COLLECTION', 'COLOR', 'SHAPE'], (optional)) – Type

threshold (float in [0, 1], (optional)) – Threshold

Isolate selected bones into a separate armature

Select shortest path between two bones

Split off selected bones from connected unselected bones

Break selected bones into chains of smaller bones

number_cuts (int in [1, 1000], (optional)) – Number of Cuts

Change the direction that a chain of bones points in (head and tail swap)

Enforce symmetry, make copies of the selection or use existing

direction (enum in ['NEGATIVE_X', 'POSITIVE_X'], (optional)) – Direction, Which sides to copy from and to (when both are selected)

copy_bone_colors (boolean, (optional)) – Bone Colors, Copy colors to existing bones

---

## Boid Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.boid.html

**Contents:**
- Boid Operators¶

Add a boid rule to the current boid state

type (enum in Boidrule Type Items, (optional)) – Type

Delete current boid rule

Move boid rule down in the list

Move boid rule up in the list

Add a boid state to the particle system

Delete current boid state

Move boid state down in the list

Move boid state up in the list

---

## Asset Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.asset.html

**Contents:**
- Asset Operators¶

Set this pose Action as active Action on the active Object

addons_core/pose_library/operators.py:103

Copy the current .blend file into an Asset Library. Only works on standalone .blend files (i.e. when no other files are referenced)

asset_library_reference (enum in [], (optional)) – asset_library_reference

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Remove an asset catalog from the asset library (contained assets will not be affected and show up as unassigned)

catalog_id (string, (optional, never None)) – Catalog ID, ID of the catalog to delete

Create a new catalog to put assets in

parent_path (string, (optional, never None)) – Parent Path, Optional path defining the location to put the new catalog under

Redo the last undone edit to the asset catalogs

Undo the last edit to the asset catalogs

Store the current state of the asset catalogs in the undo buffer

Make any edits to any catalogs permanent by writing the current set up to the asset library

Delete all asset metadata and turn the selected asset data-blocks back into normal data-blocks

set_fake_user (boolean, (optional)) – Set Fake User, Ensure the data-block is saved, even when it is no longer marked as asset

Delete all asset metadata and turn the asset data-block back into a normal data-block

set_fake_user (boolean, (optional)) – Set Fake User, Ensure the data-block is saved, even when it is no longer marked as asset

Reread assets and asset catalogs from the asset library on disk

Enable easier reuse of selected data-blocks through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

Enable easier reuse of a data-block through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

Open the blend file that contains the active asset

startup/bl_operators/assets.py:103

Capture a screenshot to use as a preview for the selected asset

p1 (int array of 2 items in [0, inf], (optional)) – Point 1, First point of the screenshot in screenspace

p2 (int array of 2 items in [0, inf], (optional)) – Point 2, Second point of the screenshot in screenspace

force_square (boolean, (optional)) – Force Square, If enabled, the screenshot will have the same height as width

Add a new keyword tag to the active asset

startup/bl_operators/assets.py:42

Remove an existing keyword tag from the active asset

startup/bl_operators/assets.py:65

---

## Brush Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.brush.html

**Contents:**
- Brush Operators¶

Activate a brush asset as current sculpt and paint tool

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

use_toggle (boolean, (optional)) – Toggle, Switch between the current and assigned brushes on consecutive uses.

Delete the active brush asset

Edit asset information like the catalog, preview image, tags, or author

catalog_path (string, (optional, never None)) – Catalog, The asset’s catalog path

author (string, (optional, never None)) – Author

description (string, (optional, never None)) – Description

Choose a preview image for the brush

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Revert the active brush settings to the default values from the asset library

Update the active brush asset in the asset library with current settings

Save a copy of the active brush asset into the default asset library, and make it the active brush

name (string, (optional, never None)) – Name, Name for the new brush asset

asset_library_reference (enum in [], (optional)) – Library, Asset library used to store the new brush

catalog_path (string, (optional, never None)) – Catalog, Catalog to use for the new asset

Change brush size by a scalar

scalar (float in [0, 2], (optional)) – Scalar, Factor to scale brush size by

Control the stencil brush

mode (enum in ['TRANSLATION', 'SCALE', 'ROTATION'], (optional)) – Tool

texmode (enum in ['PRIMARY', 'SECONDARY'], (optional)) – Tool

When using an image texture, adjust the stencil size to fit the image aspect ratio

use_repeat (boolean, (optional)) – Use Repeat, Use repeat mapping values

use_scale (boolean, (optional)) – Use Scale, Use texture scale values

mask (boolean, (optional)) – Modify Mask Stencil, Modify either the primary or mask stencil

Reset the stencil transformation to the default

mask (boolean, (optional)) – Modify Mask Stencil, Modify either the primary or mask stencil

---

## Cachefile Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.cachefile.html

**Contents:**
- Cachefile Operators¶

Add an override layer to the archive

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Move layer in the list, layers further down the list will overwrite data from the layers higher up

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active vertex group towards

Remove an override layer from the archive

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Update objects paths list with new data from the archive

---

## Camera Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.camera.html

**Contents:**
- Camera Operators¶

Add or remove a Camera Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

use_focal_length (boolean, (optional)) – Include Focal Length, Include focal length into the preset

startup/bl_operators/presets.py:119

Add or remove a Safe Areas Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

---

## Clip Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.clip.html

**Contents:**
- Clip Operators¶

Place new marker at specified location

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of marker on frame

Place new marker at the desired (clicked) position

Add new marker and move it on movie

CLIP_OT_add_marker (CLIP_OT_add_marker, (optional)) – Add Marker, Place new marker at specified location

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Add new marker and slide it with mouse until mouse button release

CLIP_OT_add_marker (CLIP_OT_add_marker, (optional)) – Add Marker, Place new marker at specified location

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Apply scale on solution itself to make distance between selected tracks equals to desired

distance (float in [-inf, inf], (optional)) – Distance, Distance between selected tracks

Average selected tracks into active

keep_original (boolean, (optional)) – Keep Original, Keep original tracks

Create vertex cloud using coordinates of reconstructed tracks

startup/bl_operators/clip.py:292

Add or remove a Tracking Camera Intrinsics Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

use_focal_length (boolean, (optional)) – Include Focal Length, Include focal length into the preset

startup/bl_operators/presets.py:119

Interactively change the current frame number

frame (int in [-1048574, 1048574], (optional)) – Frame

Clean tracks with high error values or few frames

frames (int in [0, inf], (optional)) – Tracked Frames, Affect tracks which are tracked less than the specified number of frames

error (float in [0, inf], (optional)) – Reprojection Error, Affect tracks which have a larger reprojection error

action (enum in ['SELECT', 'DELETE_TRACK', 'DELETE_SEGMENTS'], (optional)) – Action, Cleanup action to execute SELECT Select – Select unclean tracks. DELETE_TRACK Delete Track – Delete unclean tracks. DELETE_SEGMENTS Delete Segments – Delete unclean segments of tracks.

Action, Cleanup action to execute

SELECT Select – Select unclean tracks.

DELETE_TRACK Delete Track – Delete unclean tracks.

DELETE_SEGMENTS Delete Segments – Delete unclean segments of tracks.

Clear all calculated data

Clear tracks after/before current position or clear the whole track

action (enum in ['UPTO', 'REMAINED', 'ALL'], (optional)) – Action, Clear action to execute UPTO Clear Up To – Clear path up to current frame. REMAINED Clear Remained – Clear path at remaining frames (after current). ALL Clear All – Clear the whole path.

Action, Clear action to execute

UPTO Clear Up To – Clear path up to current frame.

REMAINED Clear Remained – Clear path at remaining frames (after current).

ALL Clear All – Clear the whole path.

clear_active (boolean, (optional)) – Clear Active, Clear active track only instead of all selected tracks

Create F-Curves for object which will copy object’s movement caused by this constraint

startup/bl_operators/clip.py:530

Copy the selected tracks to the internal clipboard

Create new plane track out of selected point tracks

Set 2D cursor location

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in normalized clip coordinates

Delete marker for current frame from selected tracks

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Delete movie clip proxy files from the hard drive

startup/bl_operators/clip.py:359

Delete selected tracks

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Automatically detect features and place markers to track

placement (enum in ['FRAME', 'INSIDE_GPENCIL', 'OUTSIDE_GPENCIL'], (optional)) – Placement, Placement for detected features FRAME Whole Frame – Place markers across the whole frame. INSIDE_GPENCIL Inside Annotated Area – Place markers only inside areas outlined with the Annotation tool. OUTSIDE_GPENCIL Outside Annotated Area – Place markers only outside areas outlined with the Annotation tool.

Placement, Placement for detected features

FRAME Whole Frame – Place markers across the whole frame.

INSIDE_GPENCIL Inside Annotated Area – Place markers only inside areas outlined with the Annotation tool.

OUTSIDE_GPENCIL Outside Annotated Area – Place markers only outside areas outlined with the Annotation tool.

margin (int in [0, inf], (optional)) – Margin, Only features further than margin pixels from the image edges are considered

threshold (float in [0.0001, inf], (optional)) – Threshold, Threshold level to consider feature good enough for tracking

min_distance (int in [0, inf], (optional)) – Distance, Minimal distance accepted between two features

Disable/enable selected markers

action (enum in ['DISABLE', 'ENABLE', 'TOGGLE'], (optional)) – Action, Disable action to execute DISABLE Disable – Disable selected markers. ENABLE Enable – Enable selected markers. TOGGLE Toggle – Toggle disabled flag for selected markers.

Action, Disable action to execute

DISABLE Disable – Disable selected markers.

ENABLE Enable – Enable selected markers.

TOGGLE Toggle – Toggle disabled flag for selected markers.

Select movie tracking channel

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location to select channel

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

Reset viewable area to show full keyframe range

Filter tracks which has weirdly looking spikes in motion curves

track_threshold (float in [-inf, inf], (optional)) – Track Threshold, Filter Threshold to select problematic tracks

startup/bl_operators/clip.py:206

Jump to special frame

position (enum in ['PATHSTART', 'PATHEND', 'FAILEDPREV', 'FAILNEXT'], (optional)) – Position, Position to jump to PATHSTART Path Start – Jump to start of current path. PATHEND Path End – Jump to end of current path. FAILEDPREV Previous Failed – Jump to previous failed frame. FAILNEXT Next Failed – Jump to next failed frame.

Position, Position to jump to

PATHSTART Path Start – Jump to start of current path.

PATHEND Path End – Jump to end of current path.

FAILEDPREV Previous Failed – Jump to previous failed frame.

FAILNEXT Next Failed – Jump to next failed frame.

Scroll view so current frame would be centered

Delete track corresponding to the selected curve

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Disable/enable selected markers

action (enum in ['DISABLE', 'ENABLE', 'TOGGLE'], (optional)) – Action, Disable action to execute DISABLE Disable – Disable selected markers. ENABLE Enable – Enable selected markers. TOGGLE Toggle – Toggle disabled flag for selected markers.

Action, Disable action to execute

DISABLE Disable – Disable selected markers.

ENABLE Enable – Enable selected markers.

TOGGLE Toggle – Toggle disabled flag for selected markers.

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location to select nearest entity

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

Change selection of all markers of active track

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select curve points using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

deselect (boolean, (optional)) – Deselect, Deselect rather than select items

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

View all curves in editor

unselected (boolean, (optional)) – Unselected, Hide unselected tracks

Clear hide selected tracks

Delete a keyframe from selected tracks at current frame

Insert a keyframe to selected tracks at current frame

Toggle Lock Selection option of the current clip editor

Lock/unlock selected tracks

action (enum in ['LOCK', 'UNLOCK', 'TOGGLE'], (optional)) – Action, Lock action to execute LOCK Lock – Lock selected tracks. UNLOCK Unlock – Unlock selected tracks. TOGGLE Toggle – Toggle locked flag for selected tracks.

Action, Lock action to execute

LOCK Lock – Lock selected tracks.

UNLOCK Unlock – Unlock selected tracks.

TOGGLE Toggle – Toggle locked flag for selected tracks.

Set the clip interaction mode

mode (enum in Clip Editor Mode Items, (optional)) – Mode

Create new image from the content of the plane marker

Load a sequence of frames or a movie file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

Paste tracks from the internal clipboard

Prefetch frames from disk for faster playback/tracking

Rebuild all selected proxies and timecode indices in the background

Refine selected markers positions by running the tracker from track’s reference to current frame

backwards (boolean, (optional)) – Backwards, Do backwards tracking

Select tracking markers

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Change selection of all tracking markers

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select markers using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select markers using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select all tracks from specified group

group (enum in ['KEYFRAMED', 'ESTIMATED', 'TRACKED', 'LOCKED', 'DISABLED', 'COLOR', 'FAILED'], (optional)) – Action, Clear action to execute KEYFRAMED Keyframed Tracks – Select all keyframed tracks. ESTIMATED Estimated Tracks – Select all estimated tracks. TRACKED Tracked Tracks – Select all tracked tracks. LOCKED Locked Tracks – Select all locked tracks. DISABLED Disabled Tracks – Select all disabled tracks. COLOR Tracks with Same Color – Select all tracks with same color as active track. FAILED Failed Tracks – Select all tracks which failed to be reconstructed.

Action, Clear action to execute

KEYFRAMED Keyframed Tracks – Select all keyframed tracks.

ESTIMATED Estimated Tracks – Select all estimated tracks.

TRACKED Tracked Tracks – Select all tracked tracks.

LOCKED Locked Tracks – Select all locked tracks.

DISABLED Disabled Tracks – Select all disabled tracks.

COLOR Tracks with Same Color – Select all tracks with same color as active track.

FAILED Failed Tracks – Select all tracks which failed to be reconstructed.

Select markers using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Undocumented, consider contributing.

startup/bl_operators/clip.py:221

Set the direction of a scene axis by rotating the camera (or its parent if present). This assumes that the selected track lies on a real axis connecting it to the origin

axis (enum in ['X', 'Y'], (optional)) – Axis, Axis to use to align bundle along X X – Align bundle align X axis. Y Y – Align bundle align Y axis.

Axis, Axis to use to align bundle along

X X – Align bundle align X axis.

Y Y – Align bundle align Y axis.

Set active marker as origin by moving camera (or its parent if present) in 3D space

use_median (boolean, (optional)) – Use Median, Set origin to median point of selected bundles

Set plane based on 3 selected bundles by moving camera (or its parent if present) in 3D space

plane (enum in ['FLOOR', 'WALL'], (optional)) – Plane, Plane to be used for orientation FLOOR Floor – Set floor plane. WALL Wall – Set wall plane.

Plane, Plane to be used for orientation

FLOOR Floor – Set floor plane.

WALL Wall – Set wall plane.

Set scale of scene by scaling camera (or its parent if present)

distance (float in [-inf, inf], (optional)) – Distance, Distance between selected tracks

Set scene’s start and end frame to match clip’s start frame and length

Set object solution scale using distance between two selected tracks

distance (float in [-inf, inf], (optional)) – Distance, Distance between selected tracks

Set keyframe used by solver

keyframe (enum in ['KEYFRAME_A', 'KEYFRAME_B'], (optional)) – Keyframe, Keyframe to set

Set current movie clip as a camera background in 3D Viewport (works only when a 3D Viewport is visible)

startup/bl_operators/clip.py:420

Prepare scene for compositing 3D objects into this footage

startup/bl_operators/clip.py:936

offset (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Offset, Offset in floating-point units, 1.0 is the width and height of the image

Slide plane marker areas

Solve camera motion from tracks

Add selected tracks to 2D translation stabilization

Remove selected track from translation stabilization

Add selected tracks to 2D rotation stabilization

Remove selected track from rotation stabilization

Select tracks which are used for rotation stabilization

Select tracks which are used for translation stabilization

Add or remove a Clip Track Color Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Copy color to all selected tracks

Track selected markers

backwards (boolean, (optional)) – Backwards, Do backwards tracking

sequence (boolean, (optional)) – Track Sequence, Track marker during image sequence rather than single image

Copy tracking settings from active track to default settings

startup/bl_operators/clip.py:965

Copy tracking settings from active track to selected tracks

startup/bl_operators/clip.py:1014

Create an Empty object which will be copying movement of active track

startup/bl_operators/clip.py:268

Add new object for tracking

Remove object for tracking

Add or remove a motion tracking settings preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Update current image used by plane marker from the content of the plane marker

View whole image with markers

fit_view (boolean, (optional)) – Fit View, Fit frame to the viewport

Center the view so that the cursor is in the middle of the view

Use a 3D mouse device to pan/zoom the view

offset (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Offset, Offset in floating-point units, 1.0 is the width and height of the image

View all selected elements

factor (float in [-inf, inf], (optional)) – Factor, Zoom factor, values higher than 1.0 zoom in, lower values zoom out

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in screen coordinates

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in normalized (0.0 to 1.0) coordinates

Set the zoom ratio (based on clip size)

ratio (float in [-inf, inf], (optional)) – Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out

---

## Buttons Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.buttons.html

**Contents:**
- Buttons Operators¶

Clear the search filter

Display properties editor context_menu

Open a directory browser, hold Shift to open the file, Alt to browse containing directory

directory (string, (optional, never None)) – Directory, Directory of the file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Open a file browser, hold Shift to open the file, Alt to browse containing directory

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

filter_glob (string, (optional, never None)) – Glob Filter, Custom filter

Start entering filter text

Keep the current data-block displayed

---

## Cloth Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.cloth.html

**Contents:**
- Cloth Operators¶

Add or remove a Cloth Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

---

## Console Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.console.html

**Contents:**
- Console Operators¶

Evaluate the namespace up until the cursor and give a list of options or complete the name if there is only one

startup/bl_operators/console.py:61

Print a message when the terminal initializes

startup/bl_operators/console.py:104

scrollback (boolean, (optional)) – Scrollback, Clear the scrollback history

history (boolean, (optional)) – History, Clear the command history

Clear the line and store in history

Copy selected text to clipboard

delete (boolean, (optional)) – Delete Selection, Whether to delete the selection after copying

Copy the console contents for use in a script

startup/bl_operators/console.py:82

Delete text by cursor position

type (enum in ['NEXT_CHARACTER', 'PREVIOUS_CHARACTER', 'NEXT_WORD', 'PREVIOUS_WORD'], (optional)) – Type, Which part of the text to delete

Execute the current console line as a Python expression

interactive (boolean, (optional)) – interactive

startup/bl_operators/console.py:38

Append history at cursor position

text (string, (optional, never None)) – Text, Text to insert at the cursor position

current_character (int in [0, inf], (optional)) – Cursor, The index of the cursor

remove_duplicates (boolean, (optional)) – Remove Duplicates, Remove duplicate items in the history

Cycle through history

reverse (boolean, (optional)) – Reverse, Reverse cycle history

Add 4 spaces at line beginning

Indent selected text or autocomplete

Insert text at cursor position

text (string, (optional, never None)) – Text, Text to insert at the cursor position

Set the current language for this console

language (string, (optional, never None)) – Language

startup/bl_operators/console.py:136

type (enum in ['LINE_BEGIN', 'LINE_END', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD'], (optional)) – Type, Where to move cursor to

select (boolean, (optional)) – Select, Whether to select while moving

Paste text from clipboard

selection (boolean, (optional)) – Selection, Paste text selected elsewhere rather than copied (X11/Wayland only)

Append scrollback text by type

text (string, (optional, never None)) – Text, Text to insert at the cursor position

type (enum in ['OUTPUT', 'INPUT', 'INFO', 'ERROR'], (optional)) – Type, Console output type

Set the console selection

Select word at cursor position

Delete 4 spaces from line beginning

---

## Collection Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.collection.html

**Contents:**
- Collection Operators¶

Create an object collection from selected objects

name (string, (optional, never None)) – Name, Name of the new collection

Invoke all configured exporters on this collection

Add exporter to the exporter list

name (string, (optional, never None)) – Name, FileHandler idname

Invoke the export operation

index (int in [0, inf], (optional)) – Index, Exporter index

Move exporter up or down in the exporter list

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active exporter

Remove exporter from the exporter list

index (int in [0, inf], (optional)) – Index, Exporter index

Add selected objects to one of the collections the active-object is part of. Optionally add to “All Collections” to ensure selected objects are included in the same collections as the active object

collection (enum in [], (optional)) – Collection, The collection to add other selected objects to

Remove selected objects from a collection

collection (enum in [], (optional)) – Collection, The collection to remove this object from

Remove the object from an object collection that contains the active object

collection (enum in [], (optional)) – Collection, The collection to remove other selected objects from

Remove selected objects from all collections

---

## Constraint Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.constraint.html

**Contents:**
- Constraint Operators¶

Add a target to the constraint

startup/bl_operators/constraint.py:26

Apply constraint and remove from the stack

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

report (boolean, (optional)) – Report, Create a notification after the operation

Clear inverse correction for Child Of constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Set inverse correction for Child Of constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Duplicate constraint at the same position in the stack

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

report (boolean, (optional)) – Report, Create a notification after the operation

Copy constraint to other selected objects/bones

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Remove constraint from constraint stack

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

report (boolean, (optional)) – Report, Create a notification after the operation

Set the influence of this constraint to zero while trying to maintain the object’s transformation. Other active constraints can still influence the final transformation

startup/bl_operators/constraint.py:86

Add default animation for path used by constraint if it isn’t animated already

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

frame_start (int in [-1048574, 1048574], (optional)) – Start Frame, First frame of path animation

length (int in [0, 1048574], (optional)) – Length, Number of frames that path animation should take

Reset limiting distance for Limit Distance Constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Move constraint down in constraint stack

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Change the constraint’s position in the list so it evaluates after the set number of others

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

index (int in [0, inf], (optional)) – Index, The index to move the constraint to

Move constraint up in constraint stack

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Normalize weights of all target bones

startup/bl_operators/constraint.py:61

Clear inverse correction for Object Solver constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Set inverse correction for Object Solver constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

Remove the target from the constraint

index (int in [-inf, inf], (optional)) – index

startup/bl_operators/constraint.py:44

Reset original length of bone for Stretch To Constraint

constraint (string, (optional, never None)) – Constraint, Name of the constraint to edit

owner (enum in ['OBJECT', 'BONE'], (optional)) – Owner, The owner of this constraint OBJECT Object – Edit a constraint on the active object. BONE Bone – Edit a constraint on the active bone.

Owner, The owner of this constraint

OBJECT Object – Edit a constraint on the active object.

BONE Bone – Edit a constraint on the active bone.

---

## Curve Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.curve.html

**Contents:**
- Curve Operators¶

Make active spline closed/opened loop

direction (enum in ['CYCLIC_U', 'CYCLIC_V'], (optional)) – Direction, Direction to make surface cyclic in

(De)select first of visible part of each NURBS

(De)select last of visible part of each NURBS

Simplify selected curves

ratio (float in [0, 1], (optional)) – Ratio

Delete selected control points or segments

type (enum in ['VERT', 'SEGMENT'], (optional)) – Type, Which elements to delete

Delete selected control points, correcting surrounding handles

Draw a freehand spline

error_threshold (float in [0, 10], (optional)) – Error, Error distance threshold (in object units)

fit_method (enum in Curve Fit Method Items, (optional)) – Fit Method

corner_angle (float in [0, 3.14159], (optional)) – Corner Angle

use_cyclic (boolean, (optional)) – Cyclic

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

wait_for_input (boolean, (optional)) – Wait for Input

Duplicate selected control points

Duplicate curve and move

CURVE_OT_duplicate (CURVE_OT_duplicate, (optional)) – Duplicate Curve, Duplicate selected control points

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude selected control point(s)

mode (enum in Transform Mode Type Items, (optional)) – Mode

Extrude curve and move result

CURVE_OT_extrude (CURVE_OT_extrude, (optional)) – Extrude, Extrude selected control point(s)

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Set type of handles for selected control points

type (enum in ['AUTOMATIC', 'VECTOR', 'ALIGNED', 'FREE_ALIGN', 'TOGGLE_FREE_ALIGN'], (optional)) – Type, Spline type

Hide (un)selected control points

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Join two curves by their selected ends

Match texture space to object’s bounding box

Recalculate the direction of selected handles

calc_length (boolean, (optional)) – Length, Recalculate handle length

Construct and edit splines

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

extrude_point (boolean, (optional)) – Extrude Point, Add a point connected to the last selected point

extrude_handle (enum in ['AUTO', 'VECTOR'], (optional)) – Extrude Handle Type, Type of the extruded handle

delete_point (boolean, (optional)) – Delete Point, Delete an existing point

insert_point (boolean, (optional)) – Insert Point, Insert Point into a curve segment

move_segment (boolean, (optional)) – Move Segment, Delete an existing point

select_point (boolean, (optional)) – Select Point, Select a point or its handles

move_point (boolean, (optional)) – Move Point, Move a point or its handles

close_spline (boolean, (optional)) – Close Spline, Make a spline cyclic by clicking endpoints

close_spline_method (enum in ['OFF', 'ON_PRESS', 'ON_CLICK'], (optional)) – Close Spline Method, The condition for close spline to activate OFF None. ON_PRESS On Press – Move handles after closing the spline. ON_CLICK On Click – Spline closes on release if not dragged.

Close Spline Method, The condition for close spline to activate

ON_PRESS On Press – Move handles after closing the spline.

ON_CLICK On Click – Spline closes on release if not dragged.

toggle_vector (boolean, (optional)) – Toggle Vector, Toggle between Vector and Auto handles

cycle_handle_type (boolean, (optional)) – Cycle Handle Type, Cycle between all four handle types

Construct a Bézier Circle

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Bézier Curve

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs Circle

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs Curve

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Set per-point radius which is used for bevel tapering

radius (float in [0, inf], (optional)) – Radius

Reveal hidden control points

select (boolean, (optional)) – Select

(De)select all control points

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Deselect control points at the boundary of each selection region

Select all control points linked to the current selection

Select all control points linked to already selected ones

deselect (boolean, (optional)) – Deselect, Deselect linked control points rather than selecting them

Select control points at the boundary of each selection region

Select control points following already selected ones along the curves

Deselect every Nth point starting from the active one

skip (int in [1, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Select control points preceding already selected ones along the curves

Randomly select some control points

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select a row of control points including active one. Successive use on the same point switches between U/V directions

Select similar curve points by property type

type (enum in ['TYPE', 'RADIUS', 'WEIGHT', 'DIRECTION'], (optional)) – Type

compare (enum in ['EQUAL', 'GREATER', 'LESS'], (optional)) – Compare

threshold (float in [0, inf], (optional)) – Threshold

Separate selected points from connected unselected points into a new object

Set shading to smooth

Select shortest path between two selections

Flatten angles of selected points

Interpolate radii of selected points

Interpolate tilt of selected points

Interpolate weight of selected points

Extrude selected boundary row around pivot point and current view axis

center (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center, Center in global view space

axis (mathutils.Vector of 3 items in [-1, 1], (optional)) – Axis, Axis in global view space

Set type of active spline

type (enum in ['POLY', 'BEZIER', 'NURBS'], (optional)) – Type, Spline type

use_handles (boolean, (optional)) – Handles, Use handles when converting Bézier curves into polygons

Set softbody goal weight for selected points

weight (float in [0, 1], (optional)) – Weight

Split off selected points from connected unselected points

Subdivide selected segments

number_cuts (int in [1, 1000], (optional)) – Number of Cuts

Switch direction of selected splines

Clear the tilt of selected control points

Add a new control point (linked to only selected end-curve one, if any)

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location to add new vertex at

---

## Cycles Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.cycles.html

**Contents:**
- Cycles Operators¶

Denoise rendered animation sequence using current scene and view layer settings. Requires denoising data passes and output to OpenEXR multilayer files

input_filepath (string, (optional, never None)) – Input Filepath, File path for image to denoise. If not specified, uses the render file path and frame range from the scene

output_filepath (string, (optional, never None)) – Output Filepath, If not specified, renders will be denoised in-place

addons_core/cycles/operators.py:49

Combine OpenEXR multi-layer images rendered with different sample ranges into one image with reduced noise

input_filepath1 (string, (optional, never None)) – Input Filepath, File path for image to merge

input_filepath2 (string, (optional, never None)) – Input Filepath, File path for image to merge

output_filepath (string, (optional, never None)) – Output Filepath, File path for merged image

addons_core/cycles/operators.py:137

Enable nodes on a light

addons_core/cycles/operators.py:23

---

## Curves Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.curves.html

**Contents:**
- Curves Operators¶

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Set values of the active attribute for selected elements

value_float (float in [-inf, inf], (optional)) – Value

value_float_vector_2d (float array of 2 items in [-inf, inf], (optional)) – Value

value_float_vector_3d (float array of 3 items in [-inf, inf], (optional)) – Value

value_int (int in [-inf, inf], (optional)) – Value

value_int_vector_2d (int array of 2 items in [-inf, inf], (optional)) – Value

value_color (float array of 4 items in [-inf, inf], (optional)) – Value

value_bool (boolean, (optional)) – Value

Add a new curves object based on the current state of the particle system

Add a new or update an existing hair particle system on the surface object

Set type of selected curves

type (enum in Curves Type Items, (optional)) – Type, Curve type

use_handles (boolean, (optional)) – Handles, Take handle information into account in the conversion

Make active curve closed/opened loop

Remove selected control points or curves

Draw a freehand curve

error_threshold (float in [0, 10], (optional)) – Error, Error distance threshold (in object units)

fit_method (enum in Curve Fit Method Items, (optional)) – Fit Method

corner_angle (float in [0, 3.14159], (optional)) – Corner Angle

use_cyclic (boolean, (optional)) – Cyclic

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

wait_for_input (boolean, (optional)) – Wait for Input

is_curve_2d (boolean, (optional)) – Curve 2D

bezier_as_nurbs (boolean, (optional)) – As NURBS

Copy selected points or curves

Make copies of selected elements and move them

CURVES_OT_duplicate (CURVES_OT_duplicate, (optional)) – Duplicate, Copy selected points or curves

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude selected control point(s)

Extrude curve and move result

CURVES_OT_extrude (CURVES_OT_extrude, (optional)) – Extrude, Extrude selected control point(s)

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Set the handle type for bezier curves

type (enum in ['AUTO', 'VECTOR', 'ALIGN', 'FREE_ALIGN', 'TOGGLE_FREE_ALIGN'], (optional)) – Type AUTO Auto – The location is automatically calculated to be smooth. VECTOR Vector – The location is calculated to point to the next/previous control point. ALIGN Align – The location is constrained to point in the opposite direction as the other handle. FREE_ALIGN Free – The handle can be moved anywhere, and does not influence the point’s other handle. TOGGLE_FREE_ALIGN Toggle Free/Align – Replace Free handles with Align, and all Align with Free handles.

AUTO Auto – The location is automatically calculated to be smooth.

VECTOR Vector – The location is calculated to point to the next/previous control point.

ALIGN Align – The location is constrained to point in the opposite direction as the other handle.

FREE_ALIGN Free – The handle can be moved anywhere, and does not influence the point’s other handle.

TOGGLE_FREE_ALIGN Toggle Free/Align – Replace Free handles with Align, and all Align with Free handles.

Construct and edit Bézier curves

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

extrude_point (boolean, (optional)) – Extrude Point, Add a point connected to the last selected point

extrude_handle (enum in ['AUTO', 'VECTOR'], (optional)) – Extrude Handle Type, Type of the extruded handle

delete_point (boolean, (optional)) – Delete Point, Delete an existing point

insert_point (boolean, (optional)) – Insert Point, Insert Point into a curve segment

move_segment (boolean, (optional)) – Move Segment, Delete an existing point

select_point (boolean, (optional)) – Select Point, Select a point or its handles

move_point (boolean, (optional)) – Move Point, Move a point or its handles

cycle_handle_type (boolean, (optional)) – Cycle Handle Type, Cycle between all four handle types

size (float in [0, inf], (optional)) – Size, Diameter of new points

Enter/Exit sculpt mode for curves

(De)select all control points

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select end points of curves

amount_start (int in [0, inf], (optional)) – Amount Front, Number of points to select from the front

amount_end (int in [0, inf], (optional)) – Amount Back, Number of points to select from the back

Shrink the selection by one point

Select all points in curves with any point selection

Select all points in the curve under the cursor

deselect (boolean, (optional)) – Deselect, Deselect linked control points rather than selecting them

Grow the selection by one point

Randomizes existing selection or create new random selection

seed (int in [-inf, inf], (optional)) – Seed, Source of randomness

probability (float in [0, 1], (optional)) – Probability, Chance of every point or curve being included in the selection

Separate selected geometry into a new object

Change the mode used for selection masking in curves sculpt mode

domain (enum in Attribute Curves Domain Items, (optional)) – Domain

Move curves so that the first point is exactly on the surface mesh

attach_mode (enum in ['NEAREST', 'DEFORM'], (optional)) – Attach Mode, How to find the point on the surface to attach to NEAREST Nearest – Find the closest point on the surface for the root point of every curve and move the root there. DEFORM Deform – Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.

Attach Mode, How to find the point on the surface to attach to

NEAREST Nearest – Find the closest point on the surface for the root point of every curve and move the root there.

DEFORM Deform – Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.

Split selected points

Subdivide selected curve segments

number_cuts (int in [1, 1000], (optional)) – Number of Cuts

Use the active object as surface for selected curves objects and set it as the parent

Reverse the direction of the selected curves

Clear the tilt of selected control points

---

## Dpaint Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.dpaint.html

**Contents:**
- Dpaint Operators¶

Bake dynamic paint image sequence surface

Add or remove Dynamic Paint output data layer

output (enum in ['A', 'B'], (optional)) – Output Toggle

Add a new Dynamic Paint surface slot

Remove the selected surface slot

Toggle whether given type is active or not

type (enum in Prop Dynamicpaint Type Items, (optional)) – Type

---

## Ed Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.ed.html

**Contents:**
- Ed Operators¶

Flush edit data from active editing modes

Save this data-block even if it has no users

Create an automatic preview for the selected data-block

Create a preview for this asset by rendering the active object

Choose an image to help identify the data-block visually

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Set if this library override data-block can be edited

Remove the preview of this data-block

Remove a usage of a data-block, clearing the assignment

Redo specific action in history

item (int in [0, inf], (optional)) – Item

Add an undo state (internal use only)

message (string, (optional, never None)) – Undo Message

Undo and redo previous action

---

## Export Anim Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.export_anim.html

**Contents:**
- Export Anim Operators¶

Save a BVH motion capture file from an armature

filepath (string, (optional, never None)) – File Path, Filepath used for exporting the file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_glob (string, (optional, never None)) – filter_glob

global_scale (float in [0.0001, 1e+06], (optional)) – Scale, Scale the BVH by this value

frame_start (int in [-inf, inf], (optional)) – Start Frame, Starting frame to export

frame_end (int in [-inf, inf], (optional)) – End Frame, End frame to export

rotate_mode (enum in ['NATIVE', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'], (optional)) – Rotation, Rotation conversion NATIVE Euler (Native) – Use the rotation order defined in the BVH file. XYZ Euler (XYZ) – Convert rotations to euler XYZ. XZY Euler (XZY) – Convert rotations to euler XZY. YXZ Euler (YXZ) – Convert rotations to euler YXZ. YZX Euler (YZX) – Convert rotations to euler YZX. ZXY Euler (ZXY) – Convert rotations to euler ZXY. ZYX Euler (ZYX) – Convert rotations to euler ZYX.

Rotation, Rotation conversion

NATIVE Euler (Native) – Use the rotation order defined in the BVH file.

XYZ Euler (XYZ) – Convert rotations to euler XYZ.

XZY Euler (XZY) – Convert rotations to euler XZY.

YXZ Euler (YXZ) – Convert rotations to euler YXZ.

YZX Euler (YZX) – Convert rotations to euler YZX.

ZXY Euler (ZXY) – Convert rotations to euler ZXY.

ZYX Euler (ZYX) – Convert rotations to euler ZYX.

root_transform_only (boolean, (optional)) – Root Translation Only, Only write out translation channels for the root bone

addons_core/io_anim_bvh/__init__.py:281

---

## Export Scene Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.export_scene.html

**Contents:**
- Export Scene Operators¶

filepath (string, (optional, never None)) – File Path, Filepath used for exporting the file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_glob (string, (optional, never None)) – filter_glob

use_selection (boolean, (optional)) – Selected Objects, Export selected and visible objects only

use_visible (boolean, (optional)) – Visible Objects, Export visible objects only

use_active_collection (boolean, (optional)) – Active Collection, Export only objects from the active collection (and its children)

collection (string, (optional, never None)) – Source Collection, Export only objects from this collection (and its children)

global_scale (float in [0.001, 1000], (optional)) – Scale, Scale all data (Some importers do not support scaled armatures!)

apply_unit_scale (boolean, (optional)) – Apply Unit, Take into account current Blender units settings (if unset, raw Blender Units values are used as-is)

apply_scale_options (enum in ['FBX_SCALE_NONE', 'FBX_SCALE_UNITS', 'FBX_SCALE_CUSTOM', 'FBX_SCALE_ALL'], (optional)) – Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way) FBX_SCALE_NONE All Local – Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0. FBX_SCALE_UNITS FBX Units Scale – Apply custom scaling to each object transformation, and units scaling to FBX scale. FBX_SCALE_CUSTOM FBX Custom Scale – Apply custom scaling to FBX scale, and units scaling to each object transformation. FBX_SCALE_ALL FBX All – Apply custom scaling and units scaling to FBX scale.

Apply Scalings, How to apply custom and units scalings in generated FBX file (Blender uses FBX scale to detect units on import, but many other applications do not handle the same way)

FBX_SCALE_NONE All Local – Apply custom scaling and units scaling to each object transformation, FBX scale remains at 1.0.

FBX_SCALE_UNITS FBX Units Scale – Apply custom scaling to each object transformation, and units scaling to FBX scale.

FBX_SCALE_CUSTOM FBX Custom Scale – Apply custom scaling to FBX scale, and units scaling to each object transformation.

FBX_SCALE_ALL FBX All – Apply custom scaling and units scaling to FBX scale.

use_space_transform (boolean, (optional)) – Use Space Transform, Apply global space transform to the object rotations. When disabled only the axis space is written to the file and all object transforms are left as-is

bake_space_transform (boolean, (optional)) – Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)

object_types (enum set in {'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'MESH', 'OTHER'}, (optional)) – Object Types, Which kind of object to export EMPTY Empty. CAMERA Camera. LIGHT Lamp. ARMATURE Armature – WARNING: not supported in dupli/group instances. MESH Mesh. OTHER Other – Other geometry types, like curve, metaball, etc. (converted to meshes).

Object Types, Which kind of object to export

ARMATURE Armature – WARNING: not supported in dupli/group instances.

OTHER Other – Other geometry types, like curve, metaball, etc. (converted to meshes).

use_mesh_modifiers (boolean, (optional)) – Apply Modifiers, Apply modifiers to mesh objects (except Armature ones) - WARNING: prevents exporting shape keys

use_mesh_modifiers_render (boolean, (optional)) – Use Modifiers Render Setting, Use render settings when applying modifiers to mesh objects (DISABLED in Blender 2.8)

mesh_smooth_type (enum in ['OFF', 'FACE', 'EDGE', 'SMOOTH_GROUP'], (optional)) – Smoothing, Export smoothing information (prefer ‘Normals Only’ option if your target importer understands custom normals) OFF Normals Only – Export only normals instead of writing edge or face smoothing data. FACE Face – Write face smoothing. EDGE Edge – Write edge smoothing. SMOOTH_GROUP Smoothing Groups – Write face smoothing groups.

Smoothing, Export smoothing information (prefer ‘Normals Only’ option if your target importer understands custom normals)

OFF Normals Only – Export only normals instead of writing edge or face smoothing data.

FACE Face – Write face smoothing.

EDGE Edge – Write edge smoothing.

SMOOTH_GROUP Smoothing Groups – Write face smoothing groups.

colors_type (enum in ['NONE', 'SRGB', 'LINEAR'], (optional)) – Vertex Colors, Export vertex color attributes NONE None – Do not export color attributes. SRGB sRGB – Export colors in sRGB color space. LINEAR Linear – Export colors in linear color space.

Vertex Colors, Export vertex color attributes

NONE None – Do not export color attributes.

SRGB sRGB – Export colors in sRGB color space.

LINEAR Linear – Export colors in linear color space.

prioritize_active_color (boolean, (optional)) – Prioritize Active Color, Make sure active color will be exported first. Could be important since some other software can discard other color attributes besides the first one

use_subsurf (boolean, (optional)) – Export Subdivision Surface, Export the last Catmull-Rom subdivision modifier as FBX subdivision (does not apply the modifier even if ‘Apply Modifiers’ is enabled)

use_mesh_edges (boolean, (optional)) – Loose Edges, Export loose edges (as two-vertices polygons)

use_tspace (boolean, (optional)) – Tangent Space, Add binormal and tangent vectors, together with normal they form the tangent space (will only work correctly with tris/quads only meshes!)

use_triangles (boolean, (optional)) – Triangulate Faces, Convert all faces to triangles

use_custom_props (boolean, (optional)) – Custom Properties, Export custom properties

add_leaf_bones (boolean, (optional)) – Add Leaf Bones, Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)

primary_bone_axis (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Primary Bone Axis

secondary_bone_axis (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Secondary Bone Axis

use_armature_deform_only (boolean, (optional)) – Only Deform Bones, Only write deforming bones (and non-deforming ones when they have deforming children)

armature_nodetype (enum in ['NULL', 'ROOT', 'LIMBNODE'], (optional)) – Armature FBXNode Type, FBX type of node (object) used to represent Blender’s armatures (use the Null type unless you experience issues with the other app, as other choices may not import back perfectly into Blender…) NULL Null – ‘Null’ FBX node, similar to Blender’s Empty (default). ROOT Root – ‘Root’ FBX node, supposed to be the root of chains of bones…. LIMBNODE LimbNode – ‘LimbNode’ FBX node, a regular joint between two bones….

Armature FBXNode Type, FBX type of node (object) used to represent Blender’s armatures (use the Null type unless you experience issues with the other app, as other choices may not import back perfectly into Blender…)

NULL Null – ‘Null’ FBX node, similar to Blender’s Empty (default).

ROOT Root – ‘Root’ FBX node, supposed to be the root of chains of bones….

LIMBNODE LimbNode – ‘LimbNode’ FBX node, a regular joint between two bones….

bake_anim (boolean, (optional)) – Baked Animation, Export baked keyframe animation

bake_anim_use_all_bones (boolean, (optional)) – Key All Bones, Force exporting at least one key of animation for all bones (needed with some target applications, like UE4)

bake_anim_use_nla_strips (boolean, (optional)) – NLA Strips, Export each non-muted NLA strip as a separated FBX’s AnimStack, if any, instead of global scene animation

bake_anim_use_all_actions (boolean, (optional)) – All Actions, Export each action as a separated FBX’s AnimStack, instead of global scene animation (note that animated objects will get all actions compatible with them, others will get no animation at all)

bake_anim_force_startend_keying (boolean, (optional)) – Force Start/End Keying, Always add a keyframe at start and end of actions for animated channels

bake_anim_step (float in [0.01, 100], (optional)) – Sampling Rate, How often to evaluate animated values (in frames)

bake_anim_simplify_factor (float in [0, 100], (optional)) – Simplify, How much to simplify baked values (0.0 to disable, the higher the more simplified)

path_mode (enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'MATCH', 'STRIP', 'COPY'], (optional)) – Path Mode, Method used to reference paths AUTO Auto – Use relative paths with subdirectories only. ABSOLUTE Absolute – Always write absolute paths. RELATIVE Relative – Write relative paths where possible. MATCH Match – Match absolute/relative setting with input path. STRIP Strip – Filename only. COPY Copy – Copy the file to the destination path (or subdirectory).

Path Mode, Method used to reference paths

AUTO Auto – Use relative paths with subdirectories only.

ABSOLUTE Absolute – Always write absolute paths.

RELATIVE Relative – Write relative paths where possible.

MATCH Match – Match absolute/relative setting with input path.

STRIP Strip – Filename only.

COPY Copy – Copy the file to the destination path (or subdirectory).

embed_textures (boolean, (optional)) – Embed Textures, Embed textures in FBX binary file (only for “Copy” path mode!)

batch_mode (enum in ['OFF', 'SCENE', 'COLLECTION', 'SCENE_COLLECTION', 'ACTIVE_SCENE_COLLECTION'], (optional)) – Batch Mode OFF Off – Active scene to file. SCENE Scene – Each scene as a file. COLLECTION Collection – Each collection (data-block ones) as a file, does not include content of children collections. SCENE_COLLECTION Scene Collections – Each collection (including master, non-data-block ones) of each scene as a file, including content from children collections. ACTIVE_SCENE_COLLECTION Active Scene Collections – Each collection (including master, non-data-block one) of the active scene as a file, including content from children collections.

OFF Off – Active scene to file.

SCENE Scene – Each scene as a file.

COLLECTION Collection – Each collection (data-block ones) as a file, does not include content of children collections.

SCENE_COLLECTION Scene Collections – Each collection (including master, non-data-block ones) of each scene as a file, including content from children collections.

ACTIVE_SCENE_COLLECTION Active Scene Collections – Each collection (including master, non-data-block one) of the active scene as a file, including content from children collections.

use_batch_own_dir (boolean, (optional)) – Batch Own Dir, Create a dir for each exported file

use_metadata (boolean, (optional)) – Use Metadata

axis_forward (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Forward

axis_up (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Up

addons_core/io_scene_fbx/__init__.py:598

Export scene as glTF 2.0 file

filepath (string, (optional, never None)) – File Path, Filepath used for exporting the file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

export_import_convert_lighting_mode (enum in ['SPEC', 'COMPAT', 'RAW'], (optional)) – Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights SPEC Standard – Physically-based glTF lighting units (cd, lx, nt). COMPAT Unitless – Non-physical, unitless lighting. Useful when exposure controls are not available. RAW Raw (Deprecated) – Blender lighting strengths with no conversion.

Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights

SPEC Standard – Physically-based glTF lighting units (cd, lx, nt).

COMPAT Unitless – Non-physical, unitless lighting. Useful when exposure controls are not available.

RAW Raw (Deprecated) – Blender lighting strengths with no conversion.

gltf_export_id (string, (optional, never None)) – Identifier, Identifier of caller (in case of add-on calling this exporter). Can be useful in case of Extension added by other add-ons

export_use_gltfpack (boolean, (optional)) – Use Gltfpack, Use gltfpack to simplify the mesh and/or compress its textures

export_gltfpack_tc (boolean, (optional)) – KTX2 Compression, Convert all textures to KTX2 with BasisU supercompression

export_gltfpack_tq (int in [1, 10], (optional)) – Texture Encoding Quality, Texture encoding quality

export_gltfpack_si (float in [0, 1], (optional)) – Mesh Simplification Ratio, Simplify meshes targeting triangle count ratio

export_gltfpack_sa (boolean, (optional)) – Aggressive Mesh Simplification, Aggressively simplify to the target ratio disregarding quality

export_gltfpack_slb (boolean, (optional)) – Lock Mesh Border Vertices, Lock border vertices during simplification to avoid gaps on connected meshes

export_gltfpack_vp (int in [1, 16], (optional)) – Position Quantization, Use N-bit quantization for positions

export_gltfpack_vt (int in [1, 16], (optional)) – Texture Coordinate Quantization, Use N-bit quantization for texture coordinates

export_gltfpack_vn (int in [1, 16], (optional)) – Normal/Tangent Quantization, Use N-bit quantization for normals and tangents

export_gltfpack_vc (int in [1, 16], (optional)) – Vertex Color Quantization, Use N-bit quantization for colors

export_gltfpack_vpi (enum in ['Integer', 'Normalized', 'Floating-point'], (optional)) – Vertex Position Attributes, Type to use for vertex position attributes Integer Integer – Use integer attributes for positions. Normalized Normalized – Use normalized attributes for positions. Floating-point Floating-point – Use floating-point attributes for positions.

Vertex Position Attributes, Type to use for vertex position attributes

Integer Integer – Use integer attributes for positions.

Normalized Normalized – Use normalized attributes for positions.

Floating-point Floating-point – Use floating-point attributes for positions.

export_gltfpack_noq (boolean, (optional)) – Disable Quantization, Disable quantization; produces much larger glTF files with no extensions

export_gltfpack_kn (boolean, (optional)) – Keep Named Nodes, Restrict some optimization to keep named nodes and meshes attached to named nodes so that named nodes can be transformed externally

export_format (enum in [], (optional)) – Format, Output format. Binary is most efficient, but JSON may be easier to edit later

ui_tab (enum in ['GENERAL', 'MESHES', 'OBJECTS', 'ANIMATION'], (optional)) – ui_tab, Export setting categories GENERAL General – General settings. MESHES Meshes – Mesh settings. OBJECTS Objects – Object settings. ANIMATION Animation – Animation settings.

ui_tab, Export setting categories

GENERAL General – General settings.

MESHES Meshes – Mesh settings.

OBJECTS Objects – Object settings.

ANIMATION Animation – Animation settings.

export_copyright (string, (optional, never None)) – Copyright, Legal rights and conditions for the model

export_image_format (enum in ['AUTO', 'JPEG', 'WEBP', 'NONE'], (optional)) – Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size. Alternatively they can be omitted if they are not needed AUTO Automatic – Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. For other formats, use PNG. JPEG JPEG Format (.jpg) – Save images as JPEGs. (Images that need alpha are saved as PNGs though.) Be aware of a possible loss in quality. WEBP WebP Format – Save images as WebPs as main image (no fallback). NONE None – Don’t export images.

Images, Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web applications due to the smaller file size. Alternatively they can be omitted if they are not needed

AUTO Automatic – Save PNGs as PNGs, JPEGs as JPEGs, WebPs as WebPs. For other formats, use PNG.

JPEG JPEG Format (.jpg) – Save images as JPEGs. (Images that need alpha are saved as PNGs though.) Be aware of a possible loss in quality.

WEBP WebP Format – Save images as WebPs as main image (no fallback).

NONE None – Don’t export images.

export_image_add_webp (boolean, (optional)) – Create WebP, Creates WebP textures for every texture. For already WebP textures, nothing happens

export_image_webp_fallback (boolean, (optional)) – WebP Fallback, For all WebP textures, create a PNG fallback texture

export_texture_dir (string, (optional, never None)) – Textures, Folder to place texture files in. Relative to the .gltf file

export_jpeg_quality (int in [0, 100], (optional)) – JPEG Quality, Quality of JPEG export

export_image_quality (int in [0, 100], (optional)) – Image Quality, Quality of image export

export_keep_originals (boolean, (optional)) – Keep Original, Keep original textures files if possible. WARNING: if you use more than one texture, where pbr standard requires only one, only one texture will be used. This can lead to unexpected results

export_texcoords (boolean, (optional)) – UVs, Export UVs (texture coordinates) with meshes

export_normals (boolean, (optional)) – Normals, Export vertex normals with meshes

export_gn_mesh (boolean, (optional)) – Geometry Nodes Instances (Experimental), Export Geometry nodes instance meshes

export_draco_mesh_compression_enable (boolean, (optional)) – Draco Mesh Compression, Compress mesh using Draco

export_draco_mesh_compression_level (int in [0, 10], (optional)) – Compression Level, Compression level (0 = most speed, 6 = most compression, higher values currently not supported)

export_draco_position_quantization (int in [0, 30], (optional)) – Position Quantization Bits, Quantization bits for position values (0 = no quantization)

export_draco_normal_quantization (int in [0, 30], (optional)) – Normal Quantization Bits, Quantization bits for normal values (0 = no quantization)

export_draco_texcoord_quantization (int in [0, 30], (optional)) – Texcoord Quantization Bits, Quantization bits for texture coordinate values (0 = no quantization)

export_draco_color_quantization (int in [0, 30], (optional)) – Color Quantization Bits, Quantization bits for color values (0 = no quantization)

export_draco_generic_quantization (int in [0, 30], (optional)) – Generic Quantization Bits, Quantization bits for generic values like weights or joints (0 = no quantization)

export_tangents (boolean, (optional)) – Tangents, Export vertex tangents with meshes

export_materials (enum in ['EXPORT', 'PLACEHOLDER', 'VIEWPORT', 'NONE'], (optional)) – Materials, Export materials EXPORT Export – Export all materials used by included objects. PLACEHOLDER Placeholder – Do not export materials, but write multiple primitive groups per mesh, keeping material slot information. VIEWPORT Viewport – Export minimal materials as defined in Viewport display properties. NONE No export – Do not export materials, and combine mesh primitive groups, losing material slot information.

Materials, Export materials

EXPORT Export – Export all materials used by included objects.

PLACEHOLDER Placeholder – Do not export materials, but write multiple primitive groups per mesh, keeping material slot information.

VIEWPORT Viewport – Export minimal materials as defined in Viewport display properties.

NONE No export – Do not export materials, and combine mesh primitive groups, losing material slot information.

export_unused_images (boolean, (optional)) – Unused Images, Export images not assigned to any material

export_unused_textures (boolean, (optional)) – Prepare Unused Textures, Export image texture nodes not assigned to any material. This feature is not standard and needs an external extension to be included in the glTF file

export_vertex_color (enum in ['MATERIAL', 'ACTIVE', 'NAME', 'NONE'], (optional)) – Use Vertex Color, How to export vertex color MATERIAL Material – Export vertex color when used by material. ACTIVE Active – Export active vertex color. NAME Name – Export vertex color with this name. NONE None – Do not export vertex color.

Use Vertex Color, How to export vertex color

MATERIAL Material – Export vertex color when used by material.

ACTIVE Active – Export active vertex color.

NAME Name – Export vertex color with this name.

NONE None – Do not export vertex color.

export_vertex_color_name (string, (optional, never None)) – Vertex Color Name, Name of vertex color to export

export_all_vertex_colors (boolean, (optional)) – Export All Vertex Colors, Export all vertex colors, even if not used by any material. If no Vertex Color is used in the mesh materials, a fake COLOR_0 will be created, in order to keep material unchanged

export_active_vertex_color_when_no_material (boolean, (optional)) – Export Active Vertex Color When No Material, When there is no material on object, export active vertex color

export_attributes (boolean, (optional)) – Attributes, Export Attributes (when starting with underscore)

use_mesh_edges (boolean, (optional)) – Loose Edges, Export loose edges as lines, using the material from the first material slot

use_mesh_vertices (boolean, (optional)) – Loose Points, Export loose points as glTF points, using the material from the first material slot

export_cameras (boolean, (optional)) – Cameras, Export cameras

use_selection (boolean, (optional)) – Selected Objects, Export selected objects only

use_visible (boolean, (optional)) – Visible Objects, Export visible objects only

use_renderable (boolean, (optional)) – Renderable Objects, Export renderable objects only

use_active_collection_with_nested (boolean, (optional)) – Include Nested Collections, Include active collection and nested collections

use_active_collection (boolean, (optional)) – Active Collection, Export objects in the active collection only

use_active_scene (boolean, (optional)) – Active Scene, Export active scene only

collection (string, (optional, never None)) – Source Collection, Export only objects from this collection (and its children)

at_collection_center (boolean, (optional)) – Export at Collection Center, Export at Collection center of mass of root objects of the collection

export_extras (boolean, (optional)) – Custom Properties, Export custom properties as glTF extras

export_yup (boolean, (optional)) – +Y Up, Export using glTF convention, +Y up

export_apply (boolean, (optional)) – Apply Modifiers, Apply modifiers (excluding Armatures) to mesh objects -WARNING: prevents exporting shape keys

export_shared_accessors (boolean, (optional)) – Shared Accessors, Export Primitives using shared accessors for attributes

export_animations (boolean, (optional)) – Animations, Exports active actions and NLA tracks as glTF animations

export_frame_range (boolean, (optional)) – Limit to Playback Range, Clips animations to selected playback range

export_frame_step (int in [1, 120], (optional)) – Sampling Rate, How often to evaluate animated values (in frames)

export_force_sampling (boolean, (optional)) – Always Sample Animations, Apply sampling to all animations

export_sampling_interpolation_fallback (enum in ['LINEAR', 'STEP'], (optional)) – Sampling Interpolation Fallback, Interpolation fallback for sampled animations, when the property is not keyed LINEAR Linear – Linear interpolation between keyframes. STEP Step – No interpolation between keyframes.

Sampling Interpolation Fallback, Interpolation fallback for sampled animations, when the property is not keyed

LINEAR Linear – Linear interpolation between keyframes.

STEP Step – No interpolation between keyframes.

export_pointer_animation (boolean, (optional)) – Export Animation Pointer (Experimental), Export material, Light & Camera animation as Animation Pointer. Available only for baked animation mode ‘NLA Tracks’ and ‘Scene’

export_animation_mode (enum in ['ACTIONS', 'ACTIVE_ACTIONS', 'BROADCAST', 'NLA_TRACKS', 'SCENE'], (optional)) – Animation Mode, Export Animation mode ACTIONS Actions – Export actions (actives and on NLA tracks) as separate animations. ACTIVE_ACTIONS Active actions merged – All the currently assigned actions become one glTF animation. BROADCAST Broadcast actions – Broadcast all compatible actions to all objects. Animated objects will get all actions compatible with them, others will get no animation at all. NLA_TRACKS NLA Tracks – Export individual NLA Tracks as separate animation. SCENE Scene – Export baked scene as a single animation.

Animation Mode, Export Animation mode

ACTIONS Actions – Export actions (actives and on NLA tracks) as separate animations.

ACTIVE_ACTIONS Active actions merged – All the currently assigned actions become one glTF animation.

BROADCAST Broadcast actions – Broadcast all compatible actions to all objects. Animated objects will get all actions compatible with them, others will get no animation at all.

NLA_TRACKS NLA Tracks – Export individual NLA Tracks as separate animation.

SCENE Scene – Export baked scene as a single animation.

export_nla_strips_merged_animation_name (string, (optional, never None)) – Merged Animation Name, Name of single glTF animation to be exported

export_def_bones (boolean, (optional)) – Export Deformation Bones Only, Export Deformation bones only

export_hierarchy_flatten_bones (boolean, (optional)) – Flatten Bone Hierarchy, Flatten Bone Hierarchy. Useful in case of non decomposable transformation matrix

export_hierarchy_flatten_objs (boolean, (optional)) – Flatten Object Hierarchy, Flatten Object Hierarchy. Useful in case of non decomposable transformation matrix

export_armature_object_remove (boolean, (optional)) – Remove Armature Object, Remove Armature object if possible. If Armature has multiple root bones, object will not be removed

export_leaf_bone (boolean, (optional)) – Add Leaf Bones, Append a final bone to the end of each chain to specify last bone length (use this when you intend to edit the armature from exported data)

export_optimize_animation_size (boolean, (optional)) – Optimize Animation Size, Reduce exported file size by removing duplicate keyframes

export_optimize_animation_keep_anim_armature (boolean, (optional)) – Force Keeping Channels for Bones, If all keyframes are identical in a rig, force keeping the minimal animation. When off, all possible channels for the bones will be exported, even if empty (minimal animation, 2 keyframes)

export_optimize_animation_keep_anim_object (boolean, (optional)) – Force Keeping Channel for Objects, If all keyframes are identical for object transformations, force keeping the minimal animation

export_optimize_disable_viewport (boolean, (optional)) – Disable Viewport for Other Objects, When exporting animations, disable viewport for other objects, for performance

export_negative_frame (enum in ['SLIDE', 'CROP'], (optional)) – Negative Frames, Negative Frames are slid or cropped SLIDE Slide – Slide animation to start at frame 0. CROP Crop – Keep only frames above frame 0.

Negative Frames, Negative Frames are slid or cropped

SLIDE Slide – Slide animation to start at frame 0.

CROP Crop – Keep only frames above frame 0.

export_anim_slide_to_zero (boolean, (optional)) – Set All glTF Animation Starting at 0, Set all glTF animation starting at 0.0s. Can be useful for looping animations

export_bake_animation (boolean, (optional)) – Bake All Objects Animations, Force exporting animation on every object. Can be useful when using constraints or driver. Also useful when exporting only selection

export_merge_animation (enum in ['NLA_TRACK', 'ACTION', 'NONE'], (optional)) – Merge Animation, Merge Animations NLA_TRACK NLA Track Names – Merge by NLA Track Names. ACTION Actions – Merge by Actions. NONE No Merge – Do Not Merge Animations.

Merge Animation, Merge Animations

NLA_TRACK NLA Track Names – Merge by NLA Track Names.

ACTION Actions – Merge by Actions.

NONE No Merge – Do Not Merge Animations.

export_anim_single_armature (boolean, (optional)) – Export all Armature Actions, Export all actions, bound to a single armature. WARNING: Option does not support exports including multiple armatures

export_reset_pose_bones (boolean, (optional)) – Reset Pose Bones Between Actions, Reset pose bones between each action exported. This is needed when some bones are not keyed on some animations

export_current_frame (boolean, (optional)) – Use Current Frame as Object Rest Transformations, Export the scene in the current animation frame. When off, frame 0 is used as rest transformations for objects

export_rest_position_armature (boolean, (optional)) – Use Rest Position Armature, Export armatures using rest position as joints’ rest pose. When off, current frame pose is used as rest pose

export_anim_scene_split_object (boolean, (optional)) – Split Animation by Object, Export Scene as seen in Viewport, But split animation by Object

export_skins (boolean, (optional)) – Skinning, Export skinning (armature) data

export_influence_nb (int in [1, inf], (optional)) – Bone Influences, Choose how many Bone influences to export

export_all_influences (boolean, (optional)) – Include All Bone Influences, Allow export of all joint vertex influences. Models may appear incorrectly in many viewers

export_morph (boolean, (optional)) – Shape Keys, Export shape keys (morph targets)

export_morph_normal (boolean, (optional)) – Shape Key Normals, Export vertex normals with shape keys (morph targets)

export_morph_tangent (boolean, (optional)) – Shape Key Tangents, Export vertex tangents with shape keys (morph targets)

export_morph_animation (boolean, (optional)) – Shape Key Animations, Export shape keys animations (morph targets)

export_morph_reset_sk_data (boolean, (optional)) – Reset Shape Keys Between Actions, Reset shape keys between each action exported. This is needed when some SK channels are not keyed on some animations

export_lights (boolean, (optional)) – Punctual Lights, Export directional, point, and spot lights. Uses “KHR_lights_punctual” glTF extension

export_try_sparse_sk (boolean, (optional)) – Use Sparse Accessor if Better, Try using Sparse Accessor if it saves space

export_try_omit_sparse_sk (boolean, (optional)) – Omitting Sparse Accessor if Data is Empty, Omitting Sparse Accessor if data is empty

export_gpu_instances (boolean, (optional)) – GPU Instances, Export using EXT_mesh_gpu_instancing. Limited to children of a given Empty. Multiple materials might be omitted

export_action_filter (boolean, (optional)) – Filter Actions, Filter Actions to be exported

export_convert_animation_pointer (boolean, (optional)) – Convert TRS/Weights to Animation Pointer, Export TRS and weights as Animation Pointer. Using KHR_animation_pointer extension

export_nla_strips (boolean, (optional)) – Group by NLA Track, When on, multiple actions become part of the same glTF animation if they’re pushed onto NLA tracks with the same name. When off, all the currently assigned actions become one glTF animation

export_original_specular (boolean, (optional)) – Export Original PBR Specular, Export original glTF PBR Specular, instead of Blender Principled Shader Specular

will_save_settings (boolean, (optional)) – Remember Export Settings, Store glTF export settings in the Blender project

export_hierarchy_full_collections (boolean, (optional)) – Full Collection Hierarchy, Export full hierarchy, including intermediate collections

export_extra_animations (boolean, (optional)) – Prepare Extra Animations, Export additional animations.This feature is not standard and needs an external extension to be included in the glTF file

export_loglevel (int in [-inf, inf], (optional)) – Log Level, Log Level

filter_glob (string, (optional, never None)) – filter_glob

addons_core/io_scene_gltf2/__init__.py:1084

---

## Extensions Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.extensions.html

**Contents:**
- Extensions Operators¶

Turn off this extension

addons_core/bl_pkg/bl_extension_ops.py:3588

Download and install the extension

repo_directory (string, (optional, never None)) – Repo Directory

repo_index (int in [-inf, inf], (optional)) – Repo Index

pkg_id (string, (optional, never None)) – Package ID

enable_on_install (boolean, (optional)) – Enable on Install, Enable after installing

url (string, (optional, never None)) – URL

do_legacy_replace (boolean, (optional)) – Do Legacy Replace

addons_core/bl_pkg/bl_extension_ops.py:1500

Install extensions from files into a locally managed repository

filter_glob (string, (optional, never None)) – filter_glob

directory (string, (optional, never None)) – Directory

files (bpy_prop_collection of OperatorFileListElement, (optional)) – files

filepath (string, (optional, never None)) – filepath

repo (enum in [], (optional)) – User Repository, The user repository to install extensions into

enable_on_install (boolean, (optional)) – Enable on Install, Enable after installing

target (enum in [], (optional)) – Legacy Target Path, Path to install legacy add-on packages to

overwrite (boolean, (optional)) – Legacy Overwrite, Remove existing add-ons with the same ID

url (string, (optional, never None)) – URL

addons_core/bl_pkg/bl_extension_ops.py:1500

Undocumented, consider contributing.

enable_on_install (boolean, (optional)) – Enable on Install, Enable after installing

addons_core/bl_pkg/bl_extension_ops.py:1500

Undocumented, consider contributing.

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3675

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:3722

Undocumented, consider contributing.

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3661

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:3686

Zeroes package versions, useful for development - to test upgrading

addons_core/bl_pkg/bl_extension_ops.py:3779

Undocumented, consider contributing.

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3748

Undocumented, consider contributing.

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3734

Undocumented, consider contributing.

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3762

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3616

pkg_id (string, (optional, never None)) – Package ID

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:3601

Disable and uninstall the extension

repo_directory (string, (optional, never None)) – Repo Directory

repo_index (int in [-inf, inf], (optional)) – Repo Index

pkg_id (string, (optional, never None)) – Package ID

addons_core/bl_pkg/bl_extension_ops.py:1500

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:1500

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:3579

Upgrade all the extensions to their latest version for all the remote repositories

use_active_only (boolean, (optional)) – Active Only, Only sync the active repository

addons_core/bl_pkg/bl_extension_ops.py:1500

Undocumented, consider contributing.

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:1830

Lock repositories - to test locking

addons_core/bl_pkg/bl_extension_ops.py:3848

Scan extension & legacy add-ons for changes to modules & meta-data (similar to restarting). Any issues are reported as warnings

use_active_only (boolean, (optional)) – Active Only, Only refresh the active repository

addons_core/bl_pkg/bl_extension_ops.py:1743

Undocumented, consider contributing.

repo_directory (string, (optional, never None)) – Repo Directory

repo_index (int in [-inf, inf], (optional)) – Repo Index

addons_core/bl_pkg/bl_extension_ops.py:1500

Refresh the list of extensions for all the remote repositories

use_active_only (boolean, (optional)) – Active Only, Only sync the active repository

addons_core/bl_pkg/bl_extension_ops.py:1500

Remove the repository file-system lock

addons_core/bl_pkg/bl_extension_ops.py:1917

Unlock repositories - to test unlocking

addons_core/bl_pkg/bl_extension_ops.py:3874

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:3647

Undocumented, consider contributing.

addons_core/bl_pkg/bl_extension_ops.py:3636

Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

addons_core/bl_pkg/bl_extension_ops.py:3999

Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

addons_core/bl_pkg/bl_extension_ops.py:4013

Open extensions preferences

addons_core/bl_pkg/bl_extension_ops.py:3939

Show system preferences “Network” panel to allow online access

addons_core/bl_pkg/bl_extension_ops.py:3979

Set the value of all tags

value (boolean, (optional)) – Value, Enable or disable all tags

data_path (string, (optional, never None)) – Data Path

addons_core/bl_pkg/bl_extension_ops.py:3908

---

## File Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.file.html

**Contents:**
- File Operators¶

Automatically pack all external files into the .blend file

Add a bookmark for the selected/active directory

Delete all invalid bookmarks

Delete selected bookmark

index (int in [-1, 20000], (optional)) – Index

Move the active bookmark up/down in the list

direction (enum in ['TOP', 'UP', 'DOWN', 'BOTTOM'], (optional)) – Direction, Direction to move the active bookmark towards TOP Top – Top of the list. UP Up. DOWN Down. BOTTOM Bottom – Bottom of the list.

Direction, Direction to move the active bookmark towards

TOP Top – Top of the list.

BOTTOM Bottom – Bottom of the list.

Cancel file operation

Move selected files to the trash or recycle bin

Create a new directory

directory (string, (optional, never None)) – Directory, Name of new directory

open (boolean, (optional)) – Open, Open new directory

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Start editing directory field

Execute selected file

Perform external operation on a file or folder

operation (enum in ['OPEN', 'FOLDER_OPEN', 'EDIT', 'NEW', 'FIND', 'SHOW', 'PLAY', 'BROWSE', 'PREVIEW', 'PRINT', 'INSTALL', 'RUNAS', 'PROPERTIES', 'FOLDER_FIND', 'CMD'], (optional)) – Operation, Operation to perform on the selected file or path OPEN Open – Open the file. FOLDER_OPEN Open Folder – Open the folder. EDIT Edit – Edit the file. NEW New – Create a new file of this type. FIND Find File – Search for files of this type. SHOW Show – Show this file. PLAY Play – Play this file. BROWSE Browse – Browse this file. PREVIEW Preview – Preview this file. PRINT Print – Print this file. INSTALL Install – Install this file. RUNAS Run As User – Run as specific user. PROPERTIES Properties – Show OS Properties for this item. FOLDER_FIND Find in Folder – Search for items in this folder. CMD Command Prompt Here – Open a command prompt here.

Operation, Operation to perform on the selected file or path

OPEN Open – Open the file.

FOLDER_OPEN Open Folder – Open the folder.

EDIT Edit – Edit the file.

NEW New – Create a new file of this type.

FIND Find File – Search for files of this type.

SHOW Show – Show this file.

PLAY Play – Play this file.

BROWSE Browse – Browse this file.

PREVIEW Preview – Preview this file.

PRINT Print – Print this file.

INSTALL Install – Install this file.

RUNAS Run As User – Run as specific user.

PROPERTIES Properties – Show OS Properties for this item.

FOLDER_FIND Find in Folder – Search for items in this folder.

CMD Command Prompt Here – Open a command prompt here.

Increment number in filename

increment (int in [-100, 100], (optional)) – Increment

Undocumented, consider contributing.

Try to find missing external files

find_all (boolean, (optional)) – Find All, Find all files in the search path (not just missing)

directory (string, (optional, never None)) – Directory, Directory of the file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Toggle hide hidden dot files

Highlight selected file(s)

Make all paths to external files absolute

Make all paths to external files relative to current .blend

Perform the current execute action for the file under the cursor (e.g. open the file)

Pack all used external files into this .blend

Store all data-blocks linked from other .blend files in the current .blend file. Library references are preserved so the linked data-blocks can be unpacked again

Move to parent directory

Move to previous folder

Refresh the file list

Rename file or file directory

Report all missing external files

Handle mouse clicks to select and activate items

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

fill (boolean, (optional)) – Fill, Select everything beginning with the last selection

open (boolean, (optional)) – Open, Open a directory when selecting it

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

only_activate_if_selected (boolean, (optional)) – Only Activate if Selected, Do not change selection if the item under the cursor is already selected, only activate it

pass_through (boolean, (optional)) – Pass Through, Even on successful execution, pass the event on so other operators can execute on it as well

Select or deselect all files

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select a bookmarked directory

dir (string, (optional, never None)) – Directory

Activate/select the file(s) contained in the border

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select/Deselect files by walking through them

direction (enum in ['UP', 'DOWN', 'LEFT', 'RIGHT'], (optional)) – Walk Direction, Select/Deselect element in this direction

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

fill (boolean, (optional)) – Fill, Select everything beginning with the last selection

Smooth scroll to make editable file visible

Change sorting to use column under cursor

Start entering filter text

Unpack all files packed into this .blend to external ones

method (enum in ['USE_LOCAL', 'WRITE_LOCAL', 'USE_ORIGINAL', 'WRITE_ORIGINAL', 'KEEP', 'REMOVE'], (optional)) – Method, How to unpack

Unpack this file to an external file

method (enum in ['USE_LOCAL', 'WRITE_LOCAL', 'USE_ORIGINAL', 'WRITE_ORIGINAL'], (optional)) – Method, How to unpack

id_name (string, (optional, never None)) – ID Name, Name of ID block to unpack

id_type (int in [0, inf], (optional)) – ID Type, Identifier type of ID block

Restore all packed linked data-blocks to their original locations

Scroll the selected files into view

---

## Fluid Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.fluid.html

**Contents:**
- Fluid Operators¶

Bake Entire Fluid Simulation

Free Entire Fluid Simulation

Add or remove a Fluid Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

---

## Font Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.font.html

**Contents:**
- Font Operators¶

case (enum in ['LOWER', 'UPPER'], (optional)) – Case, Lower or upper case

Change font character code

delta (int in [-255, 255], (optional)) – Delta, Number to increase or decrease character code with

delta (float in [-inf, inf], (optional)) – Delta, Amount to decrease or increase character spacing with

Delete text by cursor position

type (enum in ['NEXT_CHARACTER', 'PREVIOUS_CHARACTER', 'NEXT_WORD', 'PREVIOUS_WORD', 'SELECTION', 'NEXT_OR_SELECTION', 'PREVIOUS_OR_SELECTION'], (optional)) – Type, Which part of the text to delete

Insert line break at cursor position

Move cursor to position type

type (enum in ['LINE_BEGIN', 'LINE_END', 'TEXT_BEGIN', 'TEXT_END', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD', 'PREVIOUS_LINE', 'NEXT_LINE', 'PREVIOUS_PAGE', 'NEXT_PAGE'], (optional)) – Type, Where to move cursor to

Move the cursor while selecting

type (enum in ['LINE_BEGIN', 'LINE_END', 'TEXT_BEGIN', 'TEXT_END', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD', 'PREVIOUS_LINE', 'NEXT_LINE', 'PREVIOUS_PAGE', 'NEXT_PAGE'], (optional)) – Type, Where to move cursor to, to make a selection

Load a new font from a file

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Select word under cursor

style (enum in ['BOLD', 'ITALIC', 'UNDERLINE', 'SMALL_CAPS'], (optional)) – Style, Style to set selection to

clear (boolean, (optional)) – Clear, Clear style rather than setting it

style (enum in ['BOLD', 'ITALIC', 'UNDERLINE', 'SMALL_CAPS'], (optional)) – Style, Style to set selection to

Copy selected text to clipboard

Cut selected text to clipboard

Insert text at cursor position

text (string, (optional, never None)) – Text, Text to insert at the cursor position

accent (boolean, (optional)) – Accent Mode, Next typed character will strike through previous, for special character input

Insert Unicode Character

Paste text from clipboard

selection (boolean, (optional)) – Selection, Paste text selected elsewhere rather than copied (X11/Wayland only)

Paste contents from file

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

index (int in [0, inf], (optional)) – Index, The current text box

Unlink active font data-block

---

## Geometry Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.geometry.html

**Contents:**
- Geometry Operators¶

Add attribute to geometry

name (string, (optional, never None)) – Name, Name of new attribute

domain (enum in Attribute Domain Items, (optional)) – Domain, Type of element that attribute is stored on

data_type (enum in Attribute Type Items, (optional)) – Data Type, Type of data stored in attribute

Change how the attribute is stored

mode (enum in ['GENERIC', 'VERTEX_GROUP'], (optional)) – Mode

domain (enum in Attribute Domain Items, (optional)) – Domain, Which geometry element to move the attribute to

data_type (enum in Attribute Type Items, (optional)) – Data Type

Remove attribute from geometry

Add color attribute to geometry

name (string, (optional, never None)) – Name, Name of new color attribute

domain (enum in Color Attribute Domain Items, (optional)) – Domain, Type of element that attribute is stored on

data_type (enum in Color Attribute Type Items, (optional)) – Data Type, Type of data stored in attribute

color (float array of 4 items in [0, inf], (optional)) – Color, Default fill color

Change how the color attribute is stored

domain (enum in Color Attribute Domain Items, (optional)) – Domain, Type of element that attribute is stored on

data_type (enum in Color Attribute Type Items, (optional)) – Data Type, Type of data stored in attribute

Duplicate color attribute

Remove color attribute from geometry

Set default color attribute used for rendering

name (string, (optional, never None)) – Name, Name of color attribute

Execute a node group on geometry

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

mouse_position (int array of 2 items in [-inf, inf], (optional)) – Mouse Position, Mouse coordinates in region space

region_size (int array of 2 items in [0, inf], (optional)) – Region Size

cursor_position (float array of 3 items in [-inf, inf], (optional)) – 3D Cursor Position

cursor_rotation (float array of 4 items in [-inf, inf], (optional)) – 3D Cursor Rotation

viewport_projection_matrix (float array of 16 items in [-inf, inf], (optional)) – Viewport Projection Transform

viewport_view_matrix (float array of 16 items in [-inf, inf], (optional)) – Viewport View Transform

viewport_is_perspective (boolean, (optional)) – Viewport Is Perspective

Toggle geometry randomization for debugging purposes

value (boolean, (optional)) – Value, Randomize the order of geometry elements (e.g. vertices or edges) after some operations where there are no guarantees about the order. This avoids accidentally depending on something that may change in the future

---

## Gizmogroup Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.gizmogroup.html

**Contents:**
- Gizmogroup Operators¶

Select the currently highlighted gizmo

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

Tweak the active gizmo

---

## Gpencil Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.gpencil.html

**Contents:**
- Gpencil Operators¶

Make annotations on the active data

mode (enum in ['DRAW', 'DRAW_STRAIGHT', 'DRAW_POLY', 'ERASER'], (optional)) – Mode, Way to interpret mouse movements DRAW Draw Freehand – Draw freehand stroke(s). DRAW_STRAIGHT Draw Straight Lines – Draw straight line segment(s). DRAW_POLY Draw Poly Line – Click to place endpoints of straight line segments (connected). ERASER Eraser – Erase Annotation strokes.

Mode, Way to interpret mouse movements

DRAW Draw Freehand – Draw freehand stroke(s).

DRAW_STRAIGHT Draw Straight Lines – Draw straight line segment(s).

DRAW_POLY Draw Poly Line – Click to place endpoints of straight line segments (connected).

ERASER Eraser – Erase Annotation strokes.

arrowstyle_start (enum in ['NONE', 'ARROW', 'ARROW_OPEN', 'ARROW_OPEN_INVERTED', 'DIAMOND'], (optional)) – Start Arrow Style, Stroke start style NONE None – Don’t use any arrow/style in corner. ARROW Arrow – Use closed arrow style. ARROW_OPEN Open Arrow – Use open arrow style. ARROW_OPEN_INVERTED Segment – Use perpendicular segment style. DIAMOND Square – Use square style.

Start Arrow Style, Stroke start style

NONE None – Don’t use any arrow/style in corner.

ARROW Arrow – Use closed arrow style.

ARROW_OPEN Open Arrow – Use open arrow style.

ARROW_OPEN_INVERTED Segment – Use perpendicular segment style.

DIAMOND Square – Use square style.

arrowstyle_end (enum in ['NONE', 'ARROW', 'ARROW_OPEN', 'ARROW_OPEN_INVERTED', 'DIAMOND'], (optional)) – End Arrow Style, Stroke end style NONE None – Don’t use any arrow/style in corner. ARROW Arrow – Use closed arrow style. ARROW_OPEN Open Arrow – Use open arrow style. ARROW_OPEN_INVERTED Segment – Use perpendicular segment style. DIAMOND Square – Use square style.

End Arrow Style, Stroke end style

NONE None – Don’t use any arrow/style in corner.

ARROW Arrow – Use closed arrow style.

ARROW_OPEN Open Arrow – Use open arrow style.

ARROW_OPEN_INVERTED Segment – Use perpendicular segment style.

DIAMOND Square – Use square style.

use_stabilizer (boolean, (optional)) – Stabilize Stroke, Helper to draw smooth and clean lines. Press Shift for an invert effect (even if this option is not active)

stabilizer_factor (float in [0, 1], (optional)) – Stabilizer Stroke Factor, Higher values gives a smoother stroke

stabilizer_radius (int in [0, 200], (optional)) – Stabilizer Stroke Radius, Minimum distance from last point before stroke continues

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

wait_for_input (boolean, (optional)) – Wait for Input, Wait for first click instead of painting immediately

Delete the active frame for the active Annotation Layer

Add new Annotation data-block

Unlink active Annotation data-block

Add new Annotation layer or note for the active data-block

Move the active Annotation layer up/down in the list

type (enum in ['UP', 'DOWN'], (optional)) – Type

Remove active Annotation layer

---

## Graph Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.graph.html

**Contents:**
- Graph Operators¶

Add keyframes on every frame between the selected keyframes

Shift selected keys to the value of the neighboring keys as a block

factor (float in [-inf, inf], (optional)) – Offset Factor, Control which key to offset towards and how far

Blend selected keys to their default value from their current position

factor (float in [-inf, inf], (optional)) – Factor, How much to blend to the default value

Blends keyframes from current state to an ease-in or ease-out curve

factor (float in [-inf, inf], (optional)) – Blend, Favor either original data or ease curve

Blend selected keyframes to their left or right neighbor

factor (float in [-inf, inf], (optional)) – Blend, The blend factor with 0 being the current frame

Move selected keyframes to an inbetween position relative to adjacent keys

factor (float in [-inf, inf], (optional)) – Factor, Favor either the left or the right key

Smooth an F-Curve while maintaining the general shape of the curve

cutoff_frequency (float in [0, inf], (optional)) – Frequency Cutoff (Hz), Lower values give a smoother curve

filter_order (int in [1, 32], (optional)) – Filter Order, Higher values produce a harder frequency cutoff

samples_per_frame (int in [1, 64], (optional)) – Samples per Frame, How many samples to calculate per frame, helps with subframe data

blend (float in [0, inf], (optional)) – Blend, How much to blend to the smoothed curve

blend_in_out (int in [0, inf], (optional)) – Blend In/Out, Linearly blend the smooth data to the border frames of the selection

Simplify F-Curves by removing closely spaced keyframes

threshold (float in [0, inf], (optional)) – Threshold

channels (boolean, (optional)) – Channels

Insert new keyframe at the cursor position for the active F-Curve

frame (float in [-inf, inf], (optional)) – Frame Number, Frame to insert keyframe on

value (float in [-inf, inf], (optional)) – Value, Value for keyframe on

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

Select keyframes by clicking on them

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend Select, Toggle keyframe selection instead of leaving newly selected keyframes only

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

column (boolean, (optional)) – Column Select, Select all keyframes that occur on the same frame as the one under the mouse

curves (boolean, (optional)) – Only Curves, Select all the keyframes in the curve

Copy selected keyframes to the internal clipboard

Interactively set the current frame and value cursor

frame (float in [-1.04857e+06, 1.04857e+06], (optional)) – Frame

value (float in [-inf, inf], (optional)) – Value

Decimate F-Curves by removing keyframes that influence the curve shape the least

mode (enum in ['RATIO', 'ERROR'], (optional)) – Mode, Which mode to use for decimation RATIO Ratio – Use a percentage to specify how many keyframes you want to remove. ERROR Error Margin – Use an error margin to specify how much the curve is allowed to deviate from the original path.

Mode, Which mode to use for decimation

RATIO Ratio – Use a percentage to specify how many keyframes you want to remove.

ERROR Error Margin – Use an error margin to specify how much the curve is allowed to deviate from the original path.

factor (float in [0, 1], (optional)) – Factor, The ratio of keyframes to remove

remove_error_margin (float in [0, inf], (optional)) – Max Error Margin, How much the new decimated curve is allowed to deviate from the original

Remove all selected keyframes

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Delete all visible drivers considered invalid

Copy the driver variables of the active driver

Add copied driver variables to the active driver

replace (boolean, (optional)) – Replace Existing, Replace existing driver variables, instead of just appending to the end of the existing list

Make a copy of all selected keyframes

mode (enum in Transform Mode Type Items, (optional)) – Mode

Make a copy of all selected keyframes and move them

GRAPH_OT_duplicate (GRAPH_OT_duplicate, (optional)) – Duplicate Keyframes, Make a copy of all selected keyframes

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Align keyframes on a ease-in or ease-out curve

factor (float in [-inf, inf], (optional)) – Curve Bend, Defines if the keys should be aligned on an ease-in or ease-out curve

sharpness (float in [0.001, inf], (optional)) – Sharpness, Higher values make the change more abrupt

Set easing type for the F-Curve segments starting from the selected keyframes

type (enum in Beztriple Interpolation Easing Items, (optional)) – Type

Ensure selected keyframes’ handles have equal length, optionally making them horizontal. Automatic, Automatic Clamped, or Vector handle types will be converted to Aligned

side (enum in ['LEFT', 'RIGHT', 'BOTH'], (optional)) – Side, Side of the keyframes’ Bézier handles to affect LEFT Left – Equalize selected keyframes’ left handles. RIGHT Right – Equalize selected keyframes’ right handles. BOTH Both – Equalize both of a keyframe’s handles.

Side, Side of the keyframes’ Bézier handles to affect

LEFT Left – Equalize selected keyframes’ left handles.

RIGHT Right – Equalize selected keyframes’ right handles.

BOTH Both – Equalize both of a keyframe’s handles.

handle_length (float in [0.1, inf], (optional)) – Handle Length, Length to make selected keyframes’ Bézier handles

flatten (boolean, (optional)) – Flatten, Make the values of the selected keyframes’ handles the same as their respective keyframes

Fix large jumps and flips in the selected Euler Rotation F-Curves arising from rotation values being clipped when baking physics

Set extrapolation mode for selected F-Curves

type (enum in ['CONSTANT', 'LINEAR', 'MAKE_CYCLIC', 'CLEAR_CYCLIC'], (optional)) – Type CONSTANT Constant Extrapolation – Values on endpoint keyframes are held. LINEAR Linear Extrapolation – Straight-line slope of end segments are extended past the endpoint keyframes. MAKE_CYCLIC Make Cyclic (F-Modifier) – Add Cycles F-Modifier if one does not exist already. CLEAR_CYCLIC Clear Cyclic (F-Modifier) – Remove Cycles F-Modifier if not needed anymore.

CONSTANT Constant Extrapolation – Values on endpoint keyframes are held.

LINEAR Linear Extrapolation – Straight-line slope of end segments are extended past the endpoint keyframes.

MAKE_CYCLIC Make Cyclic (F-Modifier) – Add Cycles F-Modifier if one does not exist already.

CLEAR_CYCLIC Clear Cyclic (F-Modifier) – Remove Cycles F-Modifier if not needed anymore.

Add F-Modifier to the active/selected F-Curves

type (enum in Fmodifier Type Items, (optional)) – Type

only_active (boolean, (optional)) – Only Active, Only add F-Modifier to active F-Curve

Copy the F-Modifier(s) of the active F-Curve

Add copied F-Modifiers to the selected F-Curves

only_active (boolean, (optional)) – Only Active, Only paste F-Modifiers on active F-Curve

replace (boolean, (optional)) – Replace Existing, Replace existing F-Modifiers, instead of just appending to the end of the existing list

Place the cursor on the midpoint of selected keyframes

Smooth the curve using a Gaussian filter

factor (float in [0, inf], (optional)) – Factor, How much to blend to the default value

sigma (float in [0.001, inf], (optional)) – Sigma, The shape of the gaussian distribution, lower values make it sharper

filter_width (int in [1, 64], (optional)) – Filter Width, How far to each side the operator will average the key values

Clear F-Curve snapshots (Ghosts) for active Graph Editor

Create snapshot (Ghosts) of selected F-Curves as background aid for active Graph Editor

Set type of handle for selected keyframes

type (enum in Keyframe Handle Type Items, (optional)) – Type

Hide selected curves from Graph Editor view

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected curves

Set interpolation mode for the F-Curve segments starting from the selected keyframes

type (enum in Beztriple Interpolation Mode Items, (optional)) – Type

Insert keyframes for the specified channels

type (enum in ['ALL', 'SEL', 'ACTIVE', 'CURSOR_ACTIVE', 'CURSOR_SEL'], (optional)) – Type ALL All Channels – Insert a keyframe on all visible and editable F-Curves using each curve’s current value. SEL Only Selected Channels – Insert a keyframe on selected F-Curves using each curve’s current value. ACTIVE Only Active F-Curve – Insert a keyframe on the active F-Curve using the curve’s current value. CURSOR_ACTIVE Active Channels at Cursor – Insert a keyframe for the active F-Curve at the cursor point. CURSOR_SEL Selected Channels at Cursor – Insert a keyframe for selected F-Curves at the cursor point.

ALL All Channels – Insert a keyframe on all visible and editable F-Curves using each curve’s current value.

SEL Only Selected Channels – Insert a keyframe on selected F-Curves using each curve’s current value.

ACTIVE Only Active F-Curve – Insert a keyframe on the active F-Curve using the curve’s current value.

CURSOR_ACTIVE Active Channels at Cursor – Insert a keyframe for the active F-Curve at the cursor point.

CURSOR_SEL Selected Channels at Cursor – Insert a keyframe for selected F-Curves at the cursor point.

Jump to previous/next keyframe

next (boolean, (optional)) – Next Keyframe

Convert selected channels to an uneditable set of samples to save storage space

Blend selected keys to the slope of neighboring ones

factor (float in [-inf, inf], (optional)) – Factor, Defines which keys to use as slope and how much to blend towards them

Flip selected keyframes over the selected mirror line

type (enum in ['CFRA', 'VALUE', 'YAXIS', 'XAXIS', 'MARKER'], (optional)) – Type CFRA By Times Over Current Frame – Flip times of selected keyframes using the current frame as the mirror line. VALUE By Values Over Cursor Value – Flip values of selected keyframes using the cursor value (Y/Horizontal component) as the mirror line. YAXIS By Times Over Zero Time – Flip times of selected keyframes, effectively reversing the order they appear in. XAXIS By Values Over Zero Value – Flip values of selected keyframes (i.e. negative values become positive, and vice versa). MARKER By Times Over First Selected Marker – Flip times of selected keyframes using the first selected marker as the reference point.

CFRA By Times Over Current Frame – Flip times of selected keyframes using the current frame as the mirror line.

VALUE By Values Over Cursor Value – Flip values of selected keyframes using the cursor value (Y/Horizontal component) as the mirror line.

YAXIS By Times Over Zero Time – Flip times of selected keyframes, effectively reversing the order they appear in.

XAXIS By Values Over Zero Value – Flip values of selected keyframes (i.e. negative values become positive, and vice versa).

MARKER By Times Over First Selected Marker – Flip times of selected keyframes using the first selected marker as the reference point.

Paste keyframes from the internal clipboard for the selected channels, starting on the current frame

offset (enum in Keyframe Paste Offset Items, (optional)) – Frame Offset, Paste time offset of keys

value_offset (enum in Keyframe Paste Offset Value Items, (optional)) – Value Offset, Paste keys with a value offset

merge (enum in Keyframe Paste Merge Items, (optional)) – Type, Method of merging pasted keys and existing

flipped (boolean, (optional)) – Flipped, Paste keyframes from mirrored bones if they exist

Set Preview Range based on range of selected keyframes

Exaggerate or minimize the value of the selected keys

factor (float in [-inf, inf], (optional)) – Factor, Control how far to push or pull the keys

Make previously hidden curves visible again in Graph Editor view

select (boolean, (optional)) – Select

Convert selected channels from samples to keyframes

Scale selected key values by their combined average

factor (float in [-inf, inf], (optional)) – Scale Factor, The scale factor applied to the curve segments

Increase or decrease the value of selected keys in relationship to the neighboring one

factor (float in [-inf, inf], (optional)) – Factor, The factor to scale keys with

anchor (enum in ['LEFT', 'RIGHT'], (optional)) – Reference Key, Which end of the segment to use as a reference to scale from

Toggle selection of all keyframes

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all keyframes within the specified region

axis_range (boolean, (optional)) – Axis Range

include_handles (boolean, (optional)) – Include Handles, Are handles tested individually against the selection criteria, independently from their keys. When unchecked, handles are (de)selected in unison with their keys

tweak (boolean, (optional)) – Tweak, Operator has been activated using a click-drag event

use_curve_selection (boolean, (optional)) – Select Curves, Allow selecting all the keyframes of a curve by selecting the calculated F-curve

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select keyframe points using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

include_handles (boolean, (optional)) – Include Handles, Are handles tested individually against the selection criteria, independently from their keys. When unchecked, handles are (de)selected in unison with their keys

use_curve_selection (boolean, (optional)) – Select Curves, Allow selecting all the keyframes of a curve by selecting the curve itself

Select all keyframes on the specified frame(s)

mode (enum in ['KEYS', 'CFRA', 'MARKERS_COLUMN', 'MARKERS_BETWEEN'], (optional)) – Mode

For selected keyframes, select/deselect any combination of the key itself and its handles

left_handle_action (enum in ['SELECT', 'DESELECT', 'KEEP'], (optional)) – Left Handle, Effect on the left handle SELECT Select. DESELECT Deselect. KEEP Keep – Leave as is.

Left Handle, Effect on the left handle

KEEP Keep – Leave as is.

right_handle_action (enum in ['SELECT', 'DESELECT', 'KEEP'], (optional)) – Right Handle, Effect on the right handle SELECT Select. DESELECT Deselect. KEEP Keep – Leave as is.

Right Handle, Effect on the right handle

KEEP Keep – Leave as is.

key_action (enum in ['SELECT', 'DESELECT', 'KEEP'], (optional)) – Key, Effect on the key itself SELECT Select. DESELECT Deselect. KEEP Keep – Leave as is.

Key, Effect on the key itself

KEEP Keep – Leave as is.

Select keyframe points using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

include_handles (boolean, (optional)) – Include Handles, Are handles tested individually against the selection criteria, independently from their keys. When unchecked, handles are (de)selected in unison with their keys

use_curve_selection (boolean, (optional)) – Select Curves, Allow selecting all the keyframes of a curve by selecting the curve itself

Select keyframes to the left or the right of the current frame

mode (enum in ['CHECK', 'LEFT', 'RIGHT'], (optional)) – Mode

extend (boolean, (optional)) – Extend Select

Deselect keyframes on ends of selection islands

Select keyframes occurring in the same F-Curves as selected ones

Select keyframes beside already selected ones

Affect the value of the keys linearly, keeping the same relationship between them using either the left or the right key as reference

factor (float in [-inf, inf], (optional)) – Shear Factor, The amount of shear to apply

direction (enum in ['FROM_LEFT', 'FROM_RIGHT'], (optional)) – Direction, Which end of the segment to use as a reference to shear from FROM_LEFT From Left – Shear the keys using the left key as reference. FROM_RIGHT From Right – Shear the keys using the right key as reference.

Direction, Which end of the segment to use as a reference to shear from

FROM_LEFT From Left – Shear the keys using the left key as reference.

FROM_RIGHT From Right – Shear the keys using the right key as reference.

Apply weighted moving means to make selected F-Curves less bumpy

Snap selected keyframes to the chosen times/values

type (enum in ['CFRA', 'VALUE', 'NEAREST_FRAME', 'NEAREST_SECOND', 'NEAREST_MARKER', 'HORIZONTAL'], (optional)) – Type CFRA Selection to Current Frame – Snap selected keyframes to the current frame. VALUE Selection to Cursor Value – Set values of selected keyframes to the cursor value (Y/Horizontal component). NEAREST_FRAME Selection to Nearest Frame – Snap selected keyframes to the nearest (whole) frame (use to fix accidental subframe offsets). NEAREST_SECOND Selection to Nearest Second – Snap selected keyframes to the nearest second. NEAREST_MARKER Selection to Nearest Marker – Snap selected keyframes to the nearest marker. HORIZONTAL Flatten Handles – Flatten handles for a smoother transition.

CFRA Selection to Current Frame – Snap selected keyframes to the current frame.

VALUE Selection to Cursor Value – Set values of selected keyframes to the cursor value (Y/Horizontal component).

NEAREST_FRAME Selection to Nearest Frame – Snap selected keyframes to the nearest (whole) frame (use to fix accidental subframe offsets).

NEAREST_SECOND Selection to Nearest Second – Snap selected keyframes to the nearest second.

NEAREST_MARKER Selection to Nearest Marker – Snap selected keyframes to the nearest marker.

HORIZONTAL Flatten Handles – Flatten handles for a smoother transition.

Place the cursor value on the average value of selected keyframes

Bakes a sound wave to samples on selected channels

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

low (float in [0, 100000], (optional)) – Lowest Frequency, Cutoff frequency of a high-pass filter that is applied to the audio data

high (float in [0, 100000], (optional)) – Highest Frequency, Cutoff frequency of a low-pass filter that is applied to the audio data

attack (float in [0, 2], (optional)) – Attack Time, Value for the envelope calculation that tells how fast the envelope can rise (the lower the value the steeper it can rise)

release (float in [0, 5], (optional)) – Release Time, Value for the envelope calculation that tells how fast the envelope can fall (the lower the value the steeper it can fall)

threshold (float in [0, 1], (optional)) – Threshold, Minimum amplitude value needed to influence the envelope

use_accumulate (boolean, (optional)) – Accumulate, Only the positive differences of the envelope amplitudes are summarized to produce the output

use_additive (boolean, (optional)) – Additive, The amplitudes of the envelope are summarized (or, when Accumulate is enabled, both positive and negative differences are accumulated)

use_square (boolean, (optional)) – Square, The output is a square curve (negative values always result in -1, and positive ones in 1)

sthreshold (float in [0, 1], (optional)) – Square Threshold, Square only: all values with an absolute amplitude lower than that result in 0

Shifts the value of selected keys in time

frame_offset (float in [-inf, inf], (optional)) – Frame Offset, How far in frames to offset the animation

Reset viewable area to show full keyframe range

include_handles (boolean, (optional)) – Include Handles, Include handles of keyframes when calculating extents

Move the view to the current frame

Reset viewable area to show selected keyframe range

include_handles (boolean, (optional)) – Include Handles, Include handles of keyframes when calculating extents

---

## Grease Pencil Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.grease_pencil.html

**Contents:**
- Grease Pencil Operators¶

Delete the active Grease Pencil frame(s)

all (boolean, (optional)) – Delete all, Delete active keyframes of all layers

Bake Grease Pencil object transform to Grease Pencil keyframes

frame_start (int in [1, 100000], (optional)) – Start Frame, The start frame

frame_end (int in [1, 100000], (optional)) – End Frame, The end frame of animation

step (int in [1, 100], (optional)) – Step, Step between generated frames

only_selected (boolean, (optional)) – Only Selected Keyframes, Convert only selected keyframes

frame_target (int in [1, 100000], (optional)) – Target Frame, Destination frame

project_type (enum in ['KEEP', 'FRONT', 'SIDE', 'TOP', 'VIEW', 'CURSOR'], (optional)) – Projection Type KEEP No Reproject. FRONT Front – Reproject the strokes using the X-Z plane. SIDE Side – Reproject the strokes using the Y-Z plane. TOP Top – Reproject the strokes using the X-Y plane. VIEW View – Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using ‘Cursor’ Stroke Placement. CURSOR Cursor – Reproject the strokes using the orientation of 3D cursor.

FRONT Front – Reproject the strokes using the X-Z plane.

SIDE Side – Reproject the strokes using the Y-Z plane.

TOP Top – Reproject the strokes using the X-Y plane.

VIEW View – Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using ‘Cursor’ Stroke Placement.

CURSOR Cursor – Reproject the strokes using the orientation of 3D cursor.

Draw a new stroke in the active Grease Pencil object

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Change curve caps mode (rounded or flat)

type (enum in ['ROUND', 'FLAT', 'START', 'END'], (optional)) – Type ROUND Rounded – Set as default rounded. FLAT Flat. START Toggle Start. END Toggle End.

ROUND Rounded – Set as default rounded.

limit (int in [1, inf], (optional)) – Limit, Number of points to consider stroke as loose

Convert type of selected curves

type (enum in Curves Type Items, (optional)) – Type

threshold (float in [0, 100], (optional)) – Threshold, The distance that the resulting points are allowed to be within

Copy the selected Grease Pencil points or strokes to the internal clipboard

Close or open the selected stroke adding a segment from last to first point

type (enum in ['CLOSE', 'OPEN', 'TOGGLE'], (optional)) – Type

subdivide_cyclic_segment (boolean, (optional)) – Match Point Density, Add point in the new segment to keep the same density

Delete selected strokes or points

Remove breakdown frames generated by interpolating between two Grease Pencil frames

Delete Grease Pencil Frame(s)

type (enum in ['ACTIVE_FRAME', 'ALL_FRAMES'], (optional)) – Type, Method used for deleting Grease Pencil frames ACTIVE_FRAME Active Frame – Deletes current frame in the active layer. ALL_FRAMES All Active Frames – Delete active frames for all layers.

Type, Method used for deleting Grease Pencil frames

ACTIVE_FRAME Active Frame – Deletes current frame in the active layer.

ALL_FRAMES All Active Frames – Delete active frames for all layers.

Delete selected points without splitting strokes

type (enum in ['POINTS', 'BETWEEN', 'UNSELECT'], (optional)) – Type, Method used for dissolving stroke points POINTS Dissolve – Dissolve selected points. BETWEEN Dissolve Between – Dissolve points between selected points. UNSELECT Dissolve Unselect – Dissolve all unselected points.

Type, Method used for dissolving stroke points

POINTS Dissolve – Dissolve selected points.

BETWEEN Dissolve Between – Dissolve points between selected points.

UNSELECT Dissolve Unselect – Dissolve all unselected points.

Duplicate the selected points

Make copies of the selected Grease Pencil strokes and move them

GREASE_PENCIL_OT_duplicate (GREASE_PENCIL_OT_duplicate, (optional)) – Duplicate, Duplicate the selected points

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Erase points in the box region

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Erase points in the lasso region

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

Extrude the selected points

Extrude selected points and move them

GREASE_PENCIL_OT_extrude (GREASE_PENCIL_OT_extrude, (optional)) – Extrude Stroke Points, Extrude the selected points

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Fill with color the shape formed by strokes

invert (boolean, (optional)) – Invert, Find boundary of unfilled instead of filled regions

precision (boolean, (optional)) – Precision, Use precision movement for extension lines

Remove any keyframe that is a duplicate of the previous one

selected (boolean, (optional)) – Selected, Only delete selected keyframes

Make a copy of the active Grease Pencil frame(s)

all (boolean, (optional)) – Duplicate all, Duplicate active keyframes of all layer

Insert a blank frame on the current scene frame

all_layers (boolean, (optional)) – All Layers, Insert a blank frame in all editable layers

duration (int in [0, 1048574], (optional)) – Duration

Interpolate Grease Pencil strokes between frames

shift (float in [-1, 1], (optional)) – Shift, Bias factor for which frame has more influence on the interpolated strokes

layers (enum in ['ACTIVE', 'ALL'], (optional)) – Layer, Layers included in the interpolation

exclude_breakdowns (boolean, (optional)) – Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes

use_selection (boolean, (optional)) – Use Selection, Use only selected strokes for interpolating

flip (enum in ['NONE', 'FLIP', 'AUTO'], (optional)) – Flip Mode, Invert destination stroke to match start and end with source stroke

smooth_steps (int in [1, 3], (optional)) – Iterations, Number of times to smooth newly created strokes

smooth_factor (float in [0, 2], (optional)) – Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise

Generate ‘in-betweens’ to smoothly interpolate between Grease Pencil frames

step (int in [1, 1048574], (optional)) – Step, Number of frames between generated interpolated frames

layers (enum in ['ACTIVE', 'ALL'], (optional)) – Layer, Layers included in the interpolation

exclude_breakdowns (boolean, (optional)) – Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes

use_selection (boolean, (optional)) – Use Selection, Use only selected strokes for interpolating

flip (enum in ['NONE', 'FLIP', 'AUTO'], (optional)) – Flip Mode, Invert destination stroke to match start and end with source stroke

smooth_steps (int in [1, 3], (optional)) – Iterations, Number of times to smooth newly created strokes

smooth_factor (float in [0, 2], (optional)) – Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise

type (enum in ['LINEAR', 'CUSTOM', 'SINE', 'QUAD', 'CUBIC', 'QUART', 'QUINT', 'EXPO', 'CIRC', 'BACK', 'BOUNCE', 'ELASTIC'], (optional)) – Type, Interpolation method to use the next time ‘Interpolate Sequence’ is run LINEAR Linear – Straight-line interpolation between A and B (i.e. no ease in/out). CUSTOM Custom – Custom interpolation defined using a curve map. SINE Sinusoidal – Sinusoidal easing (weakest, almost linear but with a slight curvature). QUAD Quadratic – Quadratic easing. CUBIC Cubic – Cubic easing. QUART Quartic – Quartic easing. QUINT Quintic – Quintic easing. EXPO Exponential – Exponential easing (dramatic). CIRC Circular – Circular easing (strongest and most dynamic). BACK Back – Cubic easing with overshoot and settle. BOUNCE Bounce – Exponentially decaying parabolic bounce, like when objects collide. ELASTIC Elastic – Exponentially decaying sine wave, like an elastic band.

Type, Interpolation method to use the next time ‘Interpolate Sequence’ is run

LINEAR Linear – Straight-line interpolation between A and B (i.e. no ease in/out).

CUSTOM Custom – Custom interpolation defined using a curve map.

SINE Sinusoidal – Sinusoidal easing (weakest, almost linear but with a slight curvature).

QUAD Quadratic – Quadratic easing.

CUBIC Cubic – Cubic easing.

QUART Quartic – Quartic easing.

QUINT Quintic – Quintic easing.

EXPO Exponential – Exponential easing (dramatic).

CIRC Circular – Circular easing (strongest and most dynamic).

BACK Back – Cubic easing with overshoot and settle.

BOUNCE Bounce – Exponentially decaying parabolic bounce, like when objects collide.

ELASTIC Elastic – Exponentially decaying sine wave, like an elastic band.

easing (enum in Beztriple Interpolation Easing Items, (optional)) – Easing, Which ends of the segment between the preceding and following Grease Pencil frames easing interpolation is applied to

back (float in [0, inf], (optional)) – Back, Amount of overshoot for ‘back’ easing

amplitude (float in [0, inf], (optional)) – Amplitude, Amount to boost elastic bounces for ‘elastic’ easing

period (float in [-inf, inf], (optional)) – Period, Time between bounces for elastic easing

New stroke from selected points/strokes

type (enum in ['JOINSTROKES', 'SPLITCOPY', 'SPLIT'], (optional)) – Type, Defines how the operator will behave on the selection in the active layer JOINSTROKES Join Strokes – Join the selected strokes into one stroke. SPLITCOPY Split and Copy – Copy the selected points to a new stroke. SPLIT Split – Split the selected point to a new stroke.

Type, Defines how the operator will behave on the selection in the active layer

JOINSTROKES Join Strokes – Join the selected strokes into one stroke.

SPLITCOPY Split and Copy – Copy the selected points to a new stroke.

SPLIT Split – Split the selected point to a new stroke.

Set the active Grease Pencil layer

layer (int in [0, inf], (optional)) – Grease Pencil Layer

Add a new Grease Pencil layer in the active object

new_layer_name (string, (optional, never None)) – Name, Name of the new layer

Make a copy of the active Grease Pencil layer

empty_keyframes (boolean, (optional)) – Empty Keyframes, Add Empty Keyframes

Make a copy of the active Grease Pencil layer to selected object

only_active (boolean, (optional)) – Only Active, Copy only active Layer, uncheck to append all layers

mode (enum in ['ALL', 'ACTIVE'], (optional)) – Mode

Add a new Grease Pencil layer group in the active object

new_layer_group_name (string, (optional, never None)) – Name, Name of the new layer group

Change layer group icon

color_tag (enum in ['NONE', 'COLOR1', 'COLOR2', 'COLOR3', 'COLOR4', 'COLOR5', 'COLOR6', 'COLOR7', 'COLOR8'], (optional)) – Color Tag

Remove Grease Pencil layer group in the active object

keep_children (boolean, (optional)) – Keep children nodes, Keep the children nodes of the group and only delete the group itself

Hide selected/unselected Grease Pencil layers

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected layers

Make only active layer visible/editable

affect_visibility (boolean, (optional)) – Affect Visibility, Also affect the visibility

Lock all Grease Pencil layers to prevent them from being accidentally modified

lock (boolean, (optional)) – Lock Value, Lock/Unlock all layers

Add new layer as masking

name (string, (optional, never None)) – Layer, Name of the layer

Reorder the active Grease Pencil mask layer up/down in the list

direction (enum in ['UP', 'DOWN'], (optional)) – Direction

Combine layers based on the mode into one layer

mode (enum in ['ACTIVE', 'GROUP', 'ALL'], (optional)) – Mode ACTIVE Active – Combine the active layer with the layer just below (if it exists). GROUP Group – Combine layers in the active group into a single layer. ALL All – Combine all layers into a single layer.

ACTIVE Active – Combine the active layer with the layer just below (if it exists).

GROUP Group – Combine layers in the active group into a single layer.

ALL All – Combine all layers into a single layer.

Move the active Grease Pencil layer or Group

direction (enum in ['UP', 'DOWN'], (optional)) – Direction

Remove the active Grease Pencil layer

Show all Grease Pencil layers

Append Materials of the active Grease Pencil to other object

only_active (boolean, (optional)) – Only Active, Append only active material, uncheck to append all materials

Hide active/inactive Grease Pencil material(s)

invert (boolean, (optional)) – Invert, Hide inactive materials instead of the active one

Toggle whether the active material is the only one that is editable and/or visible

affect_visibility (boolean, (optional)) – Affect Visibility, In addition to toggling the editability, also affect the visibility

Lock all Grease Pencil materials to prevent them from being accidentally modified

Lock any material not used in any selected stroke

Lock and hide any material not used

Unhide all hidden Grease Pencil materials

Select/Deselect all Grease Pencil strokes using current material

deselect (boolean, (optional)) – Deselect, Unselect strokes

Unlock all Grease Pencil materials so that they can be edited

Move selected strokes to another layer

target_layer_name (string, (optional, never None)) – Name, Target Grease Pencil Layer

add_new_layer (boolean, (optional)) – New Layer, Move selection to a new layer

Convert selected strokes to perimeter

type (enum in ['VIEW', 'FRONT', 'SIDE', 'TOP', 'CURSOR', 'CAMERA'], (optional)) – Projection Mode

radius (float in [0, 10], (optional)) – Radius

offset_factor (float in [-1, 1], (optional)) – Offset Factor

corner_subdivisions (int in [0, 10], (optional)) – Corner Subdivisions

Enter/Exit paint mode for Grease Pencil strokes

back (boolean, (optional)) – Return to Previous Mode, Return to previous mode

Paste Grease Pencil points or strokes from the internal clipboard to the active layer

type (enum in ['ACTIVE', 'LAYER'], (optional)) – Type

paste_back (boolean, (optional)) – Paste on Back, Add pasted strokes behind all strokes

keep_world_transform (boolean, (optional)) – Keep World Transform, Keep the world transform of strokes from the clipboard unchanged

Construct and edit splines

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

extrude_point (boolean, (optional)) – Extrude Point, Add a point connected to the last selected point

extrude_handle (enum in ['AUTO', 'VECTOR'], (optional)) – Extrude Handle Type, Type of the extruded handle

delete_point (boolean, (optional)) – Delete Point, Delete an existing point

insert_point (boolean, (optional)) – Insert Point, Insert Point into a curve segment

move_segment (boolean, (optional)) – Move Segment, Delete an existing point

select_point (boolean, (optional)) – Select Point, Select a point or its handles

move_point (boolean, (optional)) – Move Point, Move a point or its handles

cycle_handle_type (boolean, (optional)) – Cycle Handle Type, Cycle between all four handle types

size (float in [0, inf], (optional)) – Size, Diameter of new points

Create predefined Grease Pencil stroke arcs

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Create predefined Grease Pencil stroke boxes

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Create predefined Grease Pencil stroke circles

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Create predefined Grease Pencil stroke curve shapes

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Create predefined Grease Pencil stroke lines

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Create predefined Grease Pencil stroke polylines

subdivision (int in [0, inf], (optional)) – Subdivisions, Number of subdivisions per segment

type (enum in ['BOX', 'LINE', 'POLYLINE', 'CIRCLE', 'ARC', 'CURVE'], (optional)) – Type, Type of shape

Mask active layer with layer above or below

mode (enum in ['ABOVE', 'BELOW'], (optional)) – Mode, Which relative layer (above or below) to use as a mask

startup/bl_operators/grease_pencil.py:39

Remove all the strokes that were created from the fill tool as guides

mode (enum in ['ACTIVE_FRAME', 'ALL_FRAMES'], (optional)) – Mode

Change the display order of the selected strokes

direction (enum in ['TOP', 'UP', 'DOWN', 'BOTTOM'], (optional)) – Direction

Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

type (enum in ['FRONT', 'SIDE', 'TOP', 'VIEW', 'SURFACE', 'CURSOR'], (optional)) – Projection Type FRONT Front – Reproject the strokes using the X-Z plane. SIDE Side – Reproject the strokes using the Y-Z plane. TOP Top – Reproject the strokes using the X-Y plane. VIEW View – Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using ‘Cursor’ Stroke Placement. SURFACE Surface – Reproject the strokes on to the scene geometry, as if drawn using ‘Surface’ placement. CURSOR Cursor – Reproject the strokes using the orientation of 3D cursor.

FRONT Front – Reproject the strokes using the X-Z plane.

SIDE Side – Reproject the strokes using the Y-Z plane.

TOP Top – Reproject the strokes using the X-Y plane.

VIEW View – Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using ‘Cursor’ Stroke Placement.

SURFACE Surface – Reproject the strokes on to the scene geometry, as if drawn using ‘Surface’ placement.

CURSOR Cursor – Reproject the strokes using the orientation of 3D cursor.

keep_original (boolean, (optional)) – Keep Original, Keep original strokes and create a copy before reprojecting

offset (float in [0, 10], (optional)) – Surface Offset

Reset UV transformation to default values

Sculpt strokes in the active Grease Pencil object

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Enter/Exit sculpt mode for Grease Pencil strokes

back (boolean, (optional)) – Return to Previous Mode, Return to previous mode

(De)select all visible strokes

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select alternated points in strokes with already selected points

deselect_ends (boolean, (optional)) – Deselect Ends, (De)select the first and last point of each stroke

Select end points of strokes

amount_start (int in [0, inf], (optional)) – Amount Start, Number of points to select from the start

amount_end (int in [0, inf], (optional)) – Amount End, Number of points to select from the end

Shrink the selection by one point

Select all points in curves with any point selection

Grow the selection by one point

Selects random points from the current strokes selection

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select all strokes with similar characteristics

mode (enum in ['LAYER', 'MATERIAL', 'VERTEX_COLOR', 'RADIUS', 'OPACITY'], (optional)) – Mode

threshold (float in [0, inf], (optional)) – Threshold

Separate the selected geometry into a new Grease Pencil object

mode (enum in ['SELECTED', 'MATERIAL', 'LAYER'], (optional)) – Mode SELECTED Selection – Separate selected geometry. MATERIAL By Material – Separate by material. LAYER By Layer – Separate by layer.

SELECTED Selection – Separate selected geometry.

MATERIAL By Material – Separate by material.

LAYER By Layer – Separate by layer.

Set the selected stroke material as the active material

Set the corner type of the selected points

corner_type (enum in ['ROUND', 'FLAT', 'SHARP'], (optional)) – Corner Type

miter_angle (float in [0, 3.14159], (optional)) – Miter Cut Angle, All corners sharper than the Miter angle will be cut flat

Set resolution of selected curves

resolution (int in [0, 10000], (optional)) – Resolution, The resolution to use for each curve segment

Set type of selected curves

type (enum in Curves Type Items, (optional)) – Type, Curve type

use_handles (boolean, (optional)) – Handles, Take handle information into account in the conversion

Set the handle type for Bézier curves

type (enum in ['AUTO', 'VECTOR', 'ALIGN', 'FREE_ALIGN', 'TOGGLE_FREE_ALIGN'], (optional)) – Type AUTO Auto – The location is automatically calculated to be smooth. VECTOR Vector – The location is calculated to point to the next/previous control point. ALIGN Align – The location is constrained to point in the opposite direction as the other handle. FREE_ALIGN Free – The handle can be moved anywhere, and does not influence the point’s other handle. TOGGLE_FREE_ALIGN Toggle Free/Align – Replace Free handles with Align, and all Align with Free handles.

AUTO Auto – The location is automatically calculated to be smooth.

VECTOR Vector – The location is calculated to point to the next/previous control point.

ALIGN Align – The location is constrained to point in the opposite direction as the other handle.

FREE_ALIGN Free – The handle can be moved anywhere, and does not influence the point’s other handle.

TOGGLE_FREE_ALIGN Toggle Free/Align – Replace Free handles with Align, and all Align with Free handles.

slot (enum in ['DEFAULT'], (optional)) – Material Slot

Change the selection mode for Grease Pencil strokes

mode (enum in Grease Pencil Selectmode Items, (optional)) – Mode

Select which point is the beginning of the curve

Set all stroke points to same opacity

opacity_stroke (float in [0, 1], (optional)) – Stroke Opacity

opacity_fill (float in [0, 1], (optional)) – Fill Opacity

Set all stroke points to same thickness

thickness (float in [0, 1000], (optional)) – Thickness, Thickness

Snap cursor to center of selected points

Snap selected points/strokes to the cursor

use_offset (boolean, (optional)) – With Offset, Offset the entire stroke instead of selected points only

Snap selected points to the nearest grid points

Assign the active material slot to the selected strokes

material (string, (optional, never None)) – Material, Name of the material

Merge points by distance

threshold (float in [0, 100], (optional)) – Threshold

use_unselected (boolean, (optional)) – Unselected, Use whole stroke, not only selected points

Reset vertex color for all or selected strokes

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

Simplify selected strokes

factor (float in [0, 100], (optional)) – Factor

length (float in [0.01, 100], (optional)) – Length

distance (float in [0, 100], (optional)) – Distance

steps (int in [0, 50], (optional)) – Steps

mode (enum in ['FIXED', 'ADAPTIVE', 'SAMPLE', 'MERGE'], (optional)) – Mode, Method used for simplifying stroke points FIXED Fixed – Delete alternating vertices in the stroke, except extremes. ADAPTIVE Adaptive – Use a Ramer-Douglas-Peucker algorithm to simplify the stroke preserving main shape. SAMPLE Sample – Re-sample the stroke with segments of the specified length. MERGE Merge – Simplify the stroke by merging vertices closer than a given distance.

Mode, Method used for simplifying stroke points

FIXED Fixed – Delete alternating vertices in the stroke, except extremes.

ADAPTIVE Adaptive – Use a Ramer-Douglas-Peucker algorithm to simplify the stroke preserving main shape.

SAMPLE Sample – Re-sample the stroke with segments of the specified length.

MERGE Merge – Simplify the stroke by merging vertices closer than a given distance.

Smooth selected strokes

iterations (int in [1, 100], (optional)) – Iterations

factor (float in [0, 1], (optional)) – Factor

smooth_ends (boolean, (optional)) – Smooth Endpoints

keep_shape (boolean, (optional)) – Keep Shape

smooth_position (boolean, (optional)) – Position

smooth_radius (boolean, (optional)) – Radius

smooth_opacity (boolean, (optional)) – Opacity

Split selected points to a new stroke

Subdivide between continuous selected points of the stroke adding a point half way between them

number_cuts (int in [1, 32], (optional)) – Number of Cuts

only_selected (boolean, (optional)) – Selected Points, Smooth only selected points in the stroke

Subdivide strokes and smooth them

GREASE_PENCIL_OT_stroke_subdivide (GREASE_PENCIL_OT_stroke_subdivide, (optional)) – Subdivide Stroke, Subdivide between continuous selected points of the stroke adding a point half way between them

GREASE_PENCIL_OT_stroke_smooth (GREASE_PENCIL_OT_stroke_smooth, (optional)) – Smooth Stroke, Smooth selected strokes

Change direction of the points of the selected strokes

Delete stroke points in between intersecting strokes

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

Draw a line to set the fill material gradient for the selected strokes

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

Extract Grease Pencil strokes from image

target (enum in ['NEW', 'SELECTED'], (optional)) – Target Object, Target Grease Pencil

radius (float in [0.001, 1], (optional)) – Radius

threshold (float in [0, 1], (optional)) – Color Threshold, Determine the lightness threshold above which strokes are generated

turnpolicy (enum in ['FOREGROUND', 'BACKGROUND', 'LEFT', 'RIGHT', 'MINORITY', 'MAJORITY', 'RANDOM'], (optional)) – Turn Policy, Determines how to resolve ambiguities during decomposition of bitmaps into paths FOREGROUND Foreground – Prefers to connect foreground components. BACKGROUND Background – Prefers to connect background components. LEFT Left – Always take a left turn. RIGHT Right – Always take a right turn. MINORITY Minority – Prefers to connect the color that occurs least frequently in the local neighborhood of the current position. MAJORITY Majority – Prefers to connect the color that occurs most frequently in the local neighborhood of the current position. RANDOM Random – Choose pseudo-randomly.

Turn Policy, Determines how to resolve ambiguities during decomposition of bitmaps into paths

FOREGROUND Foreground – Prefers to connect foreground components.

BACKGROUND Background – Prefers to connect background components.

LEFT Left – Always take a left turn.

RIGHT Right – Always take a right turn.

MINORITY Minority – Prefers to connect the color that occurs least frequently in the local neighborhood of the current position.

MAJORITY Majority – Prefers to connect the color that occurs most frequently in the local neighborhood of the current position.

RANDOM Random – Choose pseudo-randomly.

mode (enum in ['SINGLE', 'SEQUENCE'], (optional)) – Mode, Determines if trace simple image or full sequence SINGLE Single – Trace the current frame of the image. SEQUENCE Sequence – Trace full sequence.

Mode, Determines if trace simple image or full sequence

SINGLE Single – Trace the current frame of the image.

SEQUENCE Sequence – Trace full sequence.

use_current_frame (boolean, (optional)) – Start At Current Frame, Trace Image starting in current image frame

frame_number (int in [0, 9999], (optional)) – Trace Frame, Used to trace only one frame of the image sequence, set to zero to trace all

Draw on vertex colors in the active Grease Pencil object

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Adjust vertex color brightness/contrast

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

brightness (float in [-1, 1], (optional)) – Brightness

contrast (float in [-1, 1], (optional)) – Contrast

Adjust vertex color HSV values

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

h (float in [0, 1], (optional)) – Hue

s (float in [0, 2], (optional)) – Saturation

v (float in [0, 2], (optional)) – Value

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

Adjust levels of vertex colors

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

offset (float in [-1, 1], (optional)) – Offset, Value to add to colors

gain (float in [0, inf], (optional)) – Gain, Value to multiply colors by

Set active color to all selected vertex

mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Mode

factor (float in [0, 1], (optional)) – Factor, Mix Factor

Normalize weights of the active vertex group

Normalize the weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

lock_active (boolean, (optional)) – Lock Active, Keep the values of the active group while normalizing others

Smooth the weights of the active vertex group

factor (float in [0, 1], (optional)) – Factor

repeat (int in [1, 10000], (optional)) – Iterations

Enter/Exit vertex paint mode for Grease Pencil strokes

back (boolean, (optional)) – Return to Previous Mode, Return to previous mode

Draw weight on stroke points in the active Grease Pencil object

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Invert the weight of active vertex group

Set the weight of the Draw tool to the weight of the vertex under the mouse cursor

Toggle Add/Subtract for the weight paint draw tool

Enter/Exit weight paint mode for Grease Pencil strokes

back (boolean, (optional)) – Return to Previous Mode, Return to previous mode

---

## Image Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.image.html

**Contents:**
- Image Operators¶

Add a new render slot

Interactively change the current frame number

frame (int in [-1048574, 1048574], (optional)) – Frame

Clear the boundaries of the render region and disable render region

Clear the currently selected render slot

Copy the image to the clipboard

Paste new image from the clipboard

Convert selected reference images to textured mesh plane

interpolation (enum in ['Linear', 'Closest', 'Cubic', 'Smart'], (optional)) – Interpolation, Texture interpolation Linear Linear – Linear interpolation. Closest Closest – No interpolation (sample closest texel). Cubic Cubic – Cubic interpolation. Smart Smart – Bicubic when magnifying, else bilinear (OSL only).

Interpolation, Texture interpolation

Linear Linear – Linear interpolation.

Closest Closest – No interpolation (sample closest texel).

Cubic Cubic – Cubic interpolation.

Smart Smart – Bicubic when magnifying, else bilinear (OSL only).

extension (enum in ['CLIP', 'EXTEND', 'REPEAT'], (optional)) – Extension, How the image is extrapolated past its original bounds CLIP Clip – Clip to image size and set exterior pixels as transparent. EXTEND Extend – Extend by repeating edge pixels of the image. REPEAT Repeat – Cause the image to repeat horizontally and vertically.

Extension, How the image is extrapolated past its original bounds

CLIP Clip – Clip to image size and set exterior pixels as transparent.

EXTEND Extend – Extend by repeating edge pixels of the image.

REPEAT Repeat – Cause the image to repeat horizontally and vertically.

use_auto_refresh (boolean, (optional)) – Auto Refresh, Always refresh image on frame changes

relative (boolean, (optional)) – Relative Paths, Use relative file paths

shader (enum in ['PRINCIPLED', 'SHADELESS', 'EMISSION'], (optional)) – Shader, Node shader to use PRINCIPLED Principled – Principled shader. SHADELESS Shadeless – Only visible to camera and reflections. EMISSION Emission – Emission shader.

Shader, Node shader to use

PRINCIPLED Principled – Principled shader.

SHADELESS Shadeless – Only visible to camera and reflections.

EMISSION Emission – Emission shader.

emit_strength (float in [0, inf], (optional)) – Emission Strength, Strength of emission

use_transparency (boolean, (optional)) – Use Alpha, Use alpha channel for transparency

render_method (enum in ['DITHERED', 'BLENDED'], (optional)) – Render Method DITHERED Dithered – Allows for grayscale hashed transparency, and compatible with render passes and ray-tracing. Also known as deferred rendering.. BLENDED Blended – Allows for colored transparency, but incompatible with render passes and ray-tracing. Also known as forward rendering..

DITHERED Dithered – Allows for grayscale hashed transparency, and compatible with render passes and ray-tracing. Also known as deferred rendering..

BLENDED Blended – Allows for colored transparency, but incompatible with render passes and ray-tracing. Also known as forward rendering..

use_backface_culling (boolean, (optional)) – Backface Culling, Use backface culling to hide the back side of faces

show_transparent_back (boolean, (optional)) – Show Backface, Render multiple transparent layers (may introduce transparency sorting problems)

overwrite_material (boolean, (optional)) – Overwrite Material, Overwrite existing material with the same name

name_from (enum in ['OBJECT', 'IMAGE'], (optional)) – Name After, Name for new mesh object and material OBJECT Source Object – Name after object source with a suffix. IMAGE Source Image – Name from loaded image.

Name After, Name for new mesh object and material

OBJECT Source Object – Name after object source with a suffix.

IMAGE Source Image – Name from loaded image.

delete_ref (boolean, (optional)) – Delete Reference Object, Delete empty image object once mesh plane is created

startup/bl_operators/image_as_planes.py:1131

Set black point or white point for curves

point (enum in ['BLACK_POINT', 'WHITE_POINT'], (optional)) – Point, Set black point or white point for curves

size (int in [1, 128], (optional)) – Sample Size

Cycle through all non-void render slots

reverse (boolean, (optional)) – Cycle in Reverse

Edit image in an external application

filepath (string, (optional, never None)) – filepath

startup/bl_operators/image.py:54

Open an image file browser, hold Shift to open the file, Alt to browse containing directory

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_flip_x (boolean, (optional)) – Horizontal, Flip the image horizontally

use_flip_y (boolean, (optional)) – Vertical, Flip the image vertically

Create mesh plane(s) from image files with the appropriate aspect ratio

interpolation (enum in ['Linear', 'Closest', 'Cubic', 'Smart'], (optional)) – Interpolation, Texture interpolation Linear Linear – Linear interpolation. Closest Closest – No interpolation (sample closest texel). Cubic Cubic – Cubic interpolation. Smart Smart – Bicubic when magnifying, else bilinear (OSL only).

Interpolation, Texture interpolation

Linear Linear – Linear interpolation.

Closest Closest – No interpolation (sample closest texel).

Cubic Cubic – Cubic interpolation.

Smart Smart – Bicubic when magnifying, else bilinear (OSL only).

extension (enum in ['CLIP', 'EXTEND', 'REPEAT'], (optional)) – Extension, How the image is extrapolated past its original bounds CLIP Clip – Clip to image size and set exterior pixels as transparent. EXTEND Extend – Extend by repeating edge pixels of the image. REPEAT Repeat – Cause the image to repeat horizontally and vertically.

Extension, How the image is extrapolated past its original bounds

CLIP Clip – Clip to image size and set exterior pixels as transparent.

EXTEND Extend – Extend by repeating edge pixels of the image.

REPEAT Repeat – Cause the image to repeat horizontally and vertically.

use_auto_refresh (boolean, (optional)) – Auto Refresh, Always refresh image on frame changes

relative (boolean, (optional)) – Relative Paths, Use relative file paths

shader (enum in ['PRINCIPLED', 'SHADELESS', 'EMISSION'], (optional)) – Shader, Node shader to use PRINCIPLED Principled – Principled shader. SHADELESS Shadeless – Only visible to camera and reflections. EMISSION Emission – Emission shader.

Shader, Node shader to use

PRINCIPLED Principled – Principled shader.

SHADELESS Shadeless – Only visible to camera and reflections.

EMISSION Emission – Emission shader.

emit_strength (float in [0, inf], (optional)) – Emission Strength, Strength of emission

use_transparency (boolean, (optional)) – Use Alpha, Use alpha channel for transparency

render_method (enum in ['DITHERED', 'BLENDED'], (optional)) – Render Method DITHERED Dithered – Allows for grayscale hashed transparency, and compatible with render passes and ray-tracing. Also known as deferred rendering.. BLENDED Blended – Allows for colored transparency, but incompatible with render passes and ray-tracing. Also known as forward rendering..

DITHERED Dithered – Allows for grayscale hashed transparency, and compatible with render passes and ray-tracing. Also known as deferred rendering..

BLENDED Blended – Allows for colored transparency, but incompatible with render passes and ray-tracing. Also known as forward rendering..

use_backface_culling (boolean, (optional)) – Backface Culling, Use backface culling to hide the back side of faces

show_transparent_back (boolean, (optional)) – Show Backface, Render multiple transparent layers (may introduce transparency sorting problems)

overwrite_material (boolean, (optional)) – Overwrite Material, Overwrite existing material with the same name

filepath (string, (optional, never None)) – File Path, Filepath used for importing the file

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation

files (bpy_prop_collection of OperatorFileListElement, (optional)) – files

directory (string, (optional, never None)) – directory

filter_image (boolean, (optional)) – filter_image

filter_movie (boolean, (optional)) – filter_movie

filter_folder (boolean, (optional)) – filter_folder

force_reload (boolean, (optional)) – Force Reload, Force reload the image if it is already opened elsewhere in Blender

image_sequence (boolean, (optional)) – Detect Image Sequences, Import sequentially numbered images as an animated image sequence instead of separate planes

offset (boolean, (optional)) – Offset Planes, Offset planes from each other. If disabled, multiple planes will be created at the same location

offset_axis (enum in ['+X', '+Y', '+Z', '-X', '-Y', '-Z'], (optional)) – Offset Direction, How planes are oriented relative to each others’ local axis +X +X – Side by Side to the Left. +Y +Y – Side by Side, Downward. +Z +Z – Stacked Above. -X -X – Side by Side to the Right. -Y -Y – Side by Side, Upward. -Z -Z – Stacked Below.

Offset Direction, How planes are oriented relative to each others’ local axis

+X +X – Side by Side to the Left.

+Y +Y – Side by Side, Downward.

+Z +Z – Stacked Above.

-X -X – Side by Side to the Right.

-Y -Y – Side by Side, Upward.

-Z -Z – Stacked Below.

offset_amount (float in [-inf, inf], (optional)) – Offset Distance, Set distance between each plane

align_axis (enum in ['+X', '+Y', '+Z', '-X', '-Y', '-Z', 'CAM', 'CAM_AX'], (optional)) – Align, How to align the planes +X +X – Facing positive X. +Y +Y – Facing positive Y. +Z +Z – Facing positive Z. -X -X – Facing negative X. -Y -Y – Facing negative Y. -Z -Z – Facing negative Z. CAM Face Camera – Facing camera. CAM_AX Camera’s Main Axis – Facing the camera’s dominant axis.

Align, How to align the planes

+X +X – Facing positive X.

+Y +Y – Facing positive Y.

+Z +Z – Facing positive Z.

-X -X – Facing negative X.

-Y -Y – Facing negative Y.

-Z -Z – Facing negative Z.

CAM Face Camera – Facing camera.

CAM_AX Camera’s Main Axis – Facing the camera’s dominant axis.

prev_align_axis (enum in ['+X', '+Y', '+Z', '-X', '-Y', '-Z', 'CAM', 'CAM_AX', 'NONE'], (optional)) – prev_align_axis +X +X – Facing positive X. +Y +Y – Facing positive Y. +Z +Z – Facing positive Z. -X -X – Facing negative X. -Y -Y – Facing negative Y. -Z -Z – Facing negative Z. CAM Face Camera – Facing camera. CAM_AX Camera’s Main Axis – Facing the camera’s dominant axis. NONE Undocumented.

+X +X – Facing positive X.

+Y +Y – Facing positive Y.

+Z +Z – Facing positive Z.

-X -X – Facing negative X.

-Y -Y – Facing negative Y.

-Z -Z – Facing negative Z.

CAM Face Camera – Facing camera.

CAM_AX Camera’s Main Axis – Facing the camera’s dominant axis.

align_track (boolean, (optional)) – Track Camera, Add a constraint to make the planes track the camera

size_mode (enum in ['ABSOLUTE', 'CAMERA', 'DPI', 'DPBU'], (optional)) – Size Mode, Method for computing the plane size ABSOLUTE Absolute – Use absolute size. CAMERA Scale to Camera Frame – Scale to fit or fill the camera frame. DPI Pixels per Inch – Scale based on pixels per inch. DPBU Pixels per Blender Unit – Scale based on pixels per Blender Unit.

Size Mode, Method for computing the plane size

ABSOLUTE Absolute – Use absolute size.

CAMERA Scale to Camera Frame – Scale to fit or fill the camera frame.

DPI Pixels per Inch – Scale based on pixels per inch.

DPBU Pixels per Blender Unit – Scale based on pixels per Blender Unit.

fill_mode (enum in ['FILL', 'FIT'], (optional)) – Scale, Method to scale the plane with the camera frame FILL Fill – Fill camera frame, spilling outside the frame. FIT Fit – Fit entire image within the camera frame.

Scale, Method to scale the plane with the camera frame

FILL Fill – Fill camera frame, spilling outside the frame.

FIT Fit – Fit entire image within the camera frame.

height (float in [0.001, inf], (optional)) – Height, Height of the created plane

factor (float in [1, inf], (optional)) – Definition, Number of pixels per inch or Blender Unit

startup/bl_operators/image_as_planes.py:855

Invert image’s channels

invert_r (boolean, (optional)) – Red, Invert red channel

invert_g (boolean, (optional)) – Green, Invert green channel

invert_b (boolean, (optional)) – Blue, Invert blue channel

invert_a (boolean, (optional)) – Alpha, Invert alpha channel

Set image’s user’s length to the one of this video

name (string, (optional, never None)) – Name, Image data-block name

width (int in [1, inf], (optional)) – Width, Image width

height (int in [1, inf], (optional)) – Height, Image height

color (float array of 4 items in [0, inf], (optional)) – Color, Default fill color

alpha (boolean, (optional)) – Alpha, Create an image with an alpha channel

generated_type (enum in Image Generated Type Items, (optional)) – Generated Type, Fill the image with a grid for UV map testing

float (boolean, (optional)) – 32-bit Float, Create image with 32-bit floating-point bit depth

use_stereo_3d (boolean, (optional)) – Stereo 3D, Create an image with left and right views

tiled (boolean, (optional)) – Tiled, Create a tiled image

allow_path_tokens (boolean, (optional)) – Allow the path to contain substitution tokens

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_sequence_detection (boolean, (optional)) – Detect Sequences, Automatically detect animated sequences in selected images (based on file names)

use_udim_detecting (boolean, (optional)) – Detect UDIMs, Detect selected UDIM files and load all matching tiles

Undocumented, consider contributing.

directory (string, (optional, never None)) – directory

files (bpy_prop_collection of OperatorFileListElement, (optional)) – files

relative_path (boolean, (optional)) – Use relative path

use_sequence_detection (boolean, (optional)) – Use sequence detection

use_udim_detection (boolean, (optional)) – Use UDIM detection

startup/bl_operators/image.py:238

Pack an image as embedded data into the .blend file

Project edited image back onto the object

startup/bl_operators/image.py:192

Edit a snapshot of the 3D Viewport in an external image editor

startup/bl_operators/image.py:122

Read all the current scene’s view layers from cache, as needed

Reload current image from disk

Remove the current render slot

Set the boundaries of the render region and enable render region

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Replace current image by another one from disk

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

size (int array of 2 items in [1, inf], (optional)) – Size

all_udims (boolean, (optional)) – All UDIM Tiles, Scale all the image’s UDIM tiles

degrees (enum in ['90', '180', '270'], (optional)) – Degrees, Amount of rotation in degrees (90, 180, 270) 90 90 Degrees – Rotate 90 degrees clockwise. 180 180 Degrees – Rotate 180 degrees clockwise. 270 270 Degrees – Rotate 270 degrees clockwise.

Degrees, Amount of rotation in degrees (90, 180, 270)

90 90 Degrees – Rotate 90 degrees clockwise.

180 180 Degrees – Rotate 180 degrees clockwise.

270 270 Degrees – Rotate 270 degrees clockwise.

Use mouse to sample a color in current image

size (int in [1, 128], (optional)) – Sample Size

Sample a line and show it in Scope panels

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

Save the image with current name and settings

Save all modified images

Save the image with another name and/or settings

save_as_render (boolean, (optional)) – Save As Render, Save image with render color management.For display image formats like PNG, apply view and display transform.For intermediate image formats like OpenEXR, use the default render output color space

copy (boolean, (optional)) – Copy, Create a new image file without modifying the current image in Blender

allow_path_tokens (boolean, (optional)) – Allow the path to contain substitution tokens

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Save a sequence of images

Adds a tile to the image

number (int in [1001, 2000], (optional)) – Number, UDIM number of the tile

count (int in [1, inf], (optional)) – Count, How many tiles to add

label (string, (optional, never None)) – Label, Optional tile label

fill (boolean, (optional)) – Fill, Fill new tile with a generated image

color (float array of 4 items in [0, inf], (optional)) – Color, Default fill color

generated_type (enum in Image Generated Type Items, (optional)) – Generated Type, Fill the image with a grid for UV map testing

width (int in [1, inf], (optional)) – Width, Image width

height (int in [1, inf], (optional)) – Height, Image height

float (boolean, (optional)) – 32-bit Float, Create image with 32-bit floating-point bit depth

alpha (boolean, (optional)) – Alpha, Create an image with an alpha channel

Fill the current tile with a generated image

color (float array of 4 items in [0, inf], (optional)) – Color, Default fill color

generated_type (enum in Image Generated Type Items, (optional)) – Generated Type, Fill the image with a grid for UV map testing

width (int in [1, inf], (optional)) – Width, Image width

height (int in [1, inf], (optional)) – Height, Image height

float (boolean, (optional)) – 32-bit Float, Create image with 32-bit floating-point bit depth

alpha (boolean, (optional)) – Alpha, Create an image with an alpha channel

Removes a tile from the image

Save an image packed in the .blend file to disk

method (enum in Unpack Method Items, (optional)) – Method, How to unpack

id (string, (optional, never None)) – Image Name, Image data-block name to unpack

View the entire image

fit_view (boolean, (optional)) – Fit View, Fit frame to the viewport

Center the view so that the cursor is in the middle of the view

Set 2D Cursor To Center View location

fit_view (boolean, (optional)) – Fit View, Fit frame to the viewport

Use a 3D mouse device to pan/zoom the view

offset (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Offset, Offset in floating-point units, 1.0 is the width and height of the image

View all selected UVs

Zoom in/out the image

factor (float in [-inf, inf], (optional)) – Factor, Zoom factor, values higher than 1.0 zoom in, lower values zoom out

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Zoom in the view to the nearest item contained in the border

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

zoom_out (boolean, (optional)) – Zoom Out

Zoom in the image (centered around 2D cursor)

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in screen coordinates

Zoom out the image (centered around 2D cursor)

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in screen coordinates

Set zoom ratio of the view

ratio (float in [-inf, inf], (optional)) – Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out

---

## Import Anim Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.import_anim.html

**Contents:**
- Import Anim Operators¶

Load a BVH motion capture file

filepath (string, (optional, never None)) – File Path, Filepath used for importing the file

filter_glob (string, (optional, never None)) – filter_glob

target (enum in ['ARMATURE', 'OBJECT'], (optional)) – Target, Import target type

global_scale (float in [0.0001, 1e+06], (optional)) – Scale, Scale the BVH by this value

frame_start (int in [-inf, inf], (optional)) – Start Frame, Starting frame for the animation

use_fps_scale (boolean, (optional)) – Scale FPS, Scale the framerate from the BVH to the current scenes, otherwise each BVH frame maps directly to a Blender frame

update_scene_fps (boolean, (optional)) – Update Scene FPS, Set the scene framerate to that of the BVH file (note that this nullifies the ‘Scale FPS’ option, as the scale will be 1:1)

update_scene_duration (boolean, (optional)) – Update Scene Duration, Extend the scene’s duration to the BVH duration (never shortens the scene)

use_cyclic (boolean, (optional)) – Loop, Loop the animation playback

rotate_mode (enum in ['QUATERNION', 'NATIVE', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'], (optional)) – Rotation, Rotation conversion QUATERNION Quaternion – Convert rotations to quaternions. NATIVE Euler (Native) – Use the rotation order defined in the BVH file. XYZ Euler (XYZ) – Convert rotations to euler XYZ. XZY Euler (XZY) – Convert rotations to euler XZY. YXZ Euler (YXZ) – Convert rotations to euler YXZ. YZX Euler (YZX) – Convert rotations to euler YZX. ZXY Euler (ZXY) – Convert rotations to euler ZXY. ZYX Euler (ZYX) – Convert rotations to euler ZYX.

Rotation, Rotation conversion

QUATERNION Quaternion – Convert rotations to quaternions.

NATIVE Euler (Native) – Use the rotation order defined in the BVH file.

XYZ Euler (XYZ) – Convert rotations to euler XYZ.

XZY Euler (XZY) – Convert rotations to euler XZY.

YXZ Euler (YXZ) – Convert rotations to euler YXZ.

YZX Euler (YZX) – Convert rotations to euler YZX.

ZXY Euler (ZXY) – Convert rotations to euler ZXY.

ZYX Euler (ZYX) – Convert rotations to euler ZYX.

axis_forward (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Forward

axis_up (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Up

addons_core/io_anim_bvh/__init__.py:118

---

## Import Scene Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.import_scene.html

**Contents:**
- Import Scene Operators¶

filepath (string, (optional, never None)) – File Path, Filepath used for importing the file

directory (string, (optional, never None)) – directory

filter_glob (string, (optional, never None)) – filter_glob

files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path

ui_tab (enum in ['MAIN', 'ARMATURE'], (optional)) – ui_tab, Import options categories MAIN Main – Main basic settings. ARMATURE Armatures – Armature-related settings.

ui_tab, Import options categories

MAIN Main – Main basic settings.

ARMATURE Armatures – Armature-related settings.

use_manual_orientation (boolean, (optional)) – Manual Orientation, Specify orientation and scale, instead of using embedded data in FBX file

global_scale (float in [0.001, 1000], (optional)) – Scale

bake_space_transform (boolean, (optional)) – Apply Transform, Bake space transform into object data, avoids getting unwanted rotations to objects when target space is not aligned with Blender’s space (WARNING! experimental option, use at own risk, known to be broken with armatures/animations)

use_custom_normals (boolean, (optional)) – Custom Normals, Import custom normals, if available (otherwise Blender will recompute them)

colors_type (enum in ['NONE', 'SRGB', 'LINEAR'], (optional)) – Vertex Colors, Import vertex color attributes NONE None – Do not import color attributes. SRGB sRGB – Expect file colors in sRGB color space. LINEAR Linear – Expect file colors in linear color space.

Vertex Colors, Import vertex color attributes

NONE None – Do not import color attributes.

SRGB sRGB – Expect file colors in sRGB color space.

LINEAR Linear – Expect file colors in linear color space.

use_image_search (boolean, (optional)) – Image Search, Search subdirs for any associated images (WARNING: may be slow)

use_alpha_decals (boolean, (optional)) – Alpha Decals, Treat materials with alpha as decals (no shadow casting)

decal_offset (float in [0, 1], (optional)) – Decal Offset, Displace geometry of alpha meshes

use_anim (boolean, (optional)) – Import Animation, Import FBX animation

anim_offset (float in [-inf, inf], (optional)) – Animation Offset, Offset to apply to animation during import, in frames

use_subsurf (boolean, (optional)) – Subdivision Data, Import FBX subdivision information as subdivision surface modifiers

use_custom_props (boolean, (optional)) – Custom Properties, Import user properties as custom properties

use_custom_props_enum_as_string (boolean, (optional)) – Import Enums As Strings, Store enumeration values as strings

ignore_leaf_bones (boolean, (optional)) – Ignore Leaf Bones, Ignore the last bone at the end of each chain (used to mark the length of the previous bone)

force_connect_children (boolean, (optional)) – Force Connect Children, Force connection of children bones to their parent, even if their computed head/tail positions do not match (can be useful with pure-joints-type armatures)

automatic_bone_orientation (boolean, (optional)) – Automatic Bone Orientation, Try to align the major bone axis with the bone children

primary_bone_axis (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Primary Bone Axis

secondary_bone_axis (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Secondary Bone Axis

use_prepost_rot (boolean, (optional)) – Use Pre/Post Rotation, Use pre/post rotation from FBX transform (you may have to disable that in some cases)

mtl_name_collision_mode (enum in ['MAKE_UNIQUE', 'REFERENCE_EXISTING'], (optional)) – Material Name Collision, Behavior when the name of an imported material conflicts with an existing material MAKE_UNIQUE Make Unique – Import each FBX material as a unique Blender material. REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

Material Name Collision, Behavior when the name of an imported material conflicts with an existing material

MAKE_UNIQUE Make Unique – Import each FBX material as a unique Blender material.

REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

axis_forward (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Forward

axis_up (enum in ['X', 'Y', 'Z', '-X', '-Y', '-Z'], (optional)) – Up

addons_core/io_scene_fbx/__init__.py:222

filepath (string, (optional, never None)) – File Path, Filepath used for importing the file

export_import_convert_lighting_mode (enum in ['SPEC', 'COMPAT', 'RAW'], (optional)) – Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights SPEC Standard – Physically-based glTF lighting units (cd, lx, nt). COMPAT Unitless – Non-physical, unitless lighting. Useful when exposure controls are not available. RAW Raw (Deprecated) – Blender lighting strengths with no conversion.

Lighting Mode, Optional backwards compatibility for non-standard render engines. Applies to lights

SPEC Standard – Physically-based glTF lighting units (cd, lx, nt).

COMPAT Unitless – Non-physical, unitless lighting. Useful when exposure controls are not available.

RAW Raw (Deprecated) – Blender lighting strengths with no conversion.

filter_glob (string, (optional, never None)) – filter_glob

directory (string, (optional, never None)) – directory

files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path

loglevel (int in [-inf, inf], (optional)) – Log Level, Log Level

import_pack_images (boolean, (optional)) – Pack Images, Pack all images into .blend file

merge_vertices (boolean, (optional)) – Merge Vertices, The glTF format requires discontinuous normals, UVs, and other vertex attributes to be stored as separate vertices, as required for rendering on typical graphics hardware. This option attempts to combine co-located vertices where possible. Currently cannot combine verts with different normals

import_shading (enum in ['NORMALS', 'FLAT', 'SMOOTH'], (optional)) – Shading, How normals are computed during import

bone_heuristic (enum in ['BLENDER', 'TEMPERANCE', 'FORTUNE'], (optional)) – Bone Dir, Heuristic for placing bones. Tries to make bones pretty BLENDER Blender (best for import/export round trip) – Good for re-importing glTFs exported from Blender, and re-exporting glTFs to glTFs after Blender editing. Bone tips are placed on their local +Y axis (in glTF space). TEMPERANCE Temperance (average) – Decent all-around strategy. A bone with one child has its tip placed on the local axis closest to its child. FORTUNE Fortune (may look better, less accurate) – Might look better than Temperance, but also might have errors. A bone with one child has its tip placed at its child’s root. Non-uniform scalings may get messed up though, so beware.

Bone Dir, Heuristic for placing bones. Tries to make bones pretty

BLENDER Blender (best for import/export round trip) – Good for re-importing glTFs exported from Blender, and re-exporting glTFs to glTFs after Blender editing. Bone tips are placed on their local +Y axis (in glTF space).

TEMPERANCE Temperance (average) – Decent all-around strategy. A bone with one child has its tip placed on the local axis closest to its child.

FORTUNE Fortune (may look better, less accurate) – Might look better than Temperance, but also might have errors. A bone with one child has its tip placed at its child’s root. Non-uniform scalings may get messed up though, so beware.

disable_bone_shape (boolean, (optional)) – Disable Bone Shape, Do not create bone shapes

bone_shape_scale_factor (float in [-inf, inf], (optional)) – Bone Shape Scale, Scale factor for bone shapes

guess_original_bind_pose (boolean, (optional)) – Guess Original Bind Pose, Try to guess the original bind pose for skinned meshes from the inverse bind matrices. When off, use default/rest pose as bind pose

import_webp_texture (boolean, (optional)) – Import WebP Textures, If a texture exists in WebP format, loads the WebP texture instead of the fallback PNG/JPEG one

import_unused_materials (boolean, (optional)) – Import Unused Materials & Images, Import materials & Images not assigned to any mesh

import_select_created_objects (boolean, (optional)) – Select Imported Objects, Select created objects at the end of the import

import_scene_extras (boolean, (optional)) – Import Scene Extras, Import scene extras as custom properties. Existing custom properties will be overwritten

import_scene_as_collection (boolean, (optional)) – Import Scene as Collection, Import the scene as a collection

import_merge_material_slots (boolean, (optional)) – Merge Material Slot when possible, Merge material slots when possible

addons_core/io_scene_gltf2/__init__.py:2012

---

## Import Curve Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.import_curve.html

**Contents:**
- Import Curve Operators¶

filepath (string, (optional, never None)) – File Path, Filepath used for importing the file

filter_glob (string, (optional, never None)) – filter_glob

directory (string, (optional, never None)) – directory

files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path

addons_core/io_curve_svg/__init__.py:61

---

## Info Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.info.html

**Contents:**
- Info Operators¶

Copy selected reports to clipboard

Delete selected reports

Replay selected reports

Update the display of reports in Blender UI (internal use)

Change selection of all visible reports

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select reports by index

report_index (int in [0, inf], (optional)) – Report, Index of the report

extend (boolean, (optional)) – Extend, Extend report selection

---

## Lattice Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.lattice.html

**Contents:**
- Lattice Operators¶

Mirror all control points without inverting the lattice deform

axis (enum in ['U', 'V', 'W'], (optional)) – Flip Axis, Coordinates along this axis get flipped

Set UVW control points a uniform distance apart

Change selection of all UVW control points

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Deselect vertices at the boundary of each selection region

Select mirrored lattice points

axis (enum set in Axis Flag Xyz Items, (optional)) – Axis

extend (boolean, (optional)) – Extend, Extend the selection

Select vertex directly linked to already selected ones

Randomly select UVW control points

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select vertices without a group

extend (boolean, (optional)) – Extend, Extend the selection

---

## Marker Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.marker.html

**Contents:**
- Marker Operators¶

Add a new time marker

Bind the selected camera to a marker on the current frame

Delete selected time marker(s)

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Duplicate selected time marker(s)

frames (int in [-inf, inf], (optional)) – Frames

Copy selected markers to another scene

scene (enum in [], (optional)) – Scene

Move selected time marker(s)

frames (int in [-inf, inf], (optional)) – Frames

tweak (boolean, (optional)) – Tweak, Operator has been activated using a click-drag event

Rename first selected time marker

name (string, (optional, never None)) – Name, New name for marker

Select time marker(s)

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend, Extend the selection

camera (boolean, (optional)) – Camera, Select the camera

Change selection of all time markers

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all time markers using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

tweak (boolean, (optional)) – Tweak, Operator has been activated using a click-drag event

Select markers on and left/right of the current frame

mode (enum in ['LEFT', 'RIGHT'], (optional)) – Mode

extend (boolean, (optional)) – Extend Select

---

## Mask Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.mask.html

**Contents:**
- Mask Operators¶

Add vertex to feather

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of vertex in normalized space

Add new vertex to feather and slide it

MASK_OT_add_feather_vertex (MASK_OT_add_feather_vertex, (optional)) – Add Feather Vertex, Add vertex to feather

MASK_OT_slide_point (MASK_OT_slide_point, (optional)) – Slide Point, Slide control points

Add vertex to active spline

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of vertex in normalized space

Add new vertex and slide it

MASK_OT_add_vertex (MASK_OT_add_vertex, (optional)) – Add Vertex, Add vertex to active spline

MASK_OT_slide_point (MASK_OT_slide_point, (optional)) – Slide Point, Slide control points

Copy the selected splines to the internal clipboard

Toggle cyclic for selected splines

Delete selected control points or splines

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Duplicate selected control points and segments between them

Duplicate mask and move

MASK_OT_duplicate (MASK_OT_duplicate, (optional)) – Duplicate Mask, Duplicate selected control points and segments between them

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Reset the feather weight to zero

Set type of handles for selected control points

type (enum in ['AUTO', 'VECTOR', 'ALIGNED', 'ALIGNED_DOUBLESIDE', 'FREE'], (optional)) – Type, Spline type

Reveal temporarily hidden mask layers

select (boolean, (optional)) – Select

Temporarily hide mask layers

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected layers

Move the active layer up/down in the list

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active layer

Add new mask layer for masking

name (string, (optional, never None)) – Name, Name of new mask layer

name (string, (optional, never None)) – Name, Name of new mask

Recalculate the direction of selected handles

Clear the mask’s parenting

Set the mask’s parenting

Paste splines from the internal clipboard

Add new circle-shaped spline

size (float in [-inf, inf], (optional)) – Size, Size of new circle

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of new circle

Add new square-shaped spline

size (float in [-inf, inf], (optional)) – Size, Size of new circle

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of new circle

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Location of vertex in normalized space

Change selection of all curve points

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select curve points using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select curve points using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select curve points using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Deselect spline points at the boundary of each selection region

Select all curve points linked to already selected ones

(De)select all points linked to the curve under the mouse cursor

deselect (boolean, (optional)) – Deselect

Select more spline points connected to initial selection

Remove mask shape keyframe for active mask layer at the current frame

Reset feather weights on all selected points animation values

Insert mask shape keyframe for active mask layer at the current frame

Recalculate animation data on selected points for frames selected in the dopesheet

location (boolean, (optional)) – Location

feather (boolean, (optional)) – Feather

slide_feather (boolean, (optional)) – Slide Feather, First try to slide feather instead of vertex

is_new_point (boolean, (optional)) – Slide New Point, Newly created vertex is being slid

Slide a point on the spline to define its curvature

Switch direction of selected splines

---

## Mball Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.mball.html

**Contents:**
- Mball Operators¶

Delete selected metaball element(s)

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Duplicate selected metaball element(s)

Make copies of the selected metaball elements and move them

MBALL_OT_duplicate_metaelems (MBALL_OT_duplicate_metaelems, (optional)) – Duplicate Metaball Elements, Duplicate selected metaball element(s)

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Hide (un)selected metaball element(s)

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Reveal all hidden metaball elements

select (boolean, (optional)) – Select

Change selection of all metaball elements

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Randomly select metaball elements

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select similar metaballs by property types

type (enum in ['TYPE', 'RADIUS', 'STIFFNESS', 'ROTATION'], (optional)) – Type

threshold (float in [0, inf], (optional)) – Threshold

---

## Material Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.material.html

**Contents:**
- Material Operators¶

Copy the material settings and nodes

Paste the material settings and nodes

---

## Mesh Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.mesh.html

**Contents:**
- Mesh Operators¶

Set values of the active attribute for selected elements

value_float (float in [-inf, inf], (optional)) – Value

value_float_vector_2d (float array of 2 items in [-inf, inf], (optional)) – Value

value_float_vector_3d (float array of 3 items in [-inf, inf], (optional)) – Value

value_int (int in [-inf, inf], (optional)) – Value

value_int_vector_2d (int array of 2 items in [-inf, inf], (optional)) – Value

value_color (float array of 4 items in [-inf, inf], (optional)) – Value

value_bool (boolean, (optional)) – Value

Average custom normals of selected vertices

average_type (enum in ['CUSTOM_NORMAL', 'FACE_AREA', 'CORNER_ANGLE'], (optional)) – Type, Averaging method CUSTOM_NORMAL Custom Normal – Take average of vertex normals. FACE_AREA Face Area – Set all vertex normals by face area. CORNER_ANGLE Corner Angle – Set all vertex normals by corner angle.

Type, Averaging method

CUSTOM_NORMAL Custom Normal – Take average of vertex normals.

FACE_AREA Face Area – Set all vertex normals by face area.

CORNER_ANGLE Corner Angle – Set all vertex normals by corner angle.

weight (int in [1, 100], (optional)) – Weight, Weight applied per face

threshold (float in [0, 10], (optional)) – Threshold, Threshold value for different weights to be considered equal

Rearrange some faces to try to get less degenerated geometry

angle_limit (float in [0, 3.14159], (optional)) – Max Angle, Angle limit

Cut into selected items at an angle to create bevel or chamfer

offset_type (enum in ['OFFSET', 'WIDTH', 'DEPTH', 'PERCENT', 'ABSOLUTE'], (optional)) – Width Type, The method for determining the size of the bevel OFFSET Offset – Amount is offset of new edges from original. WIDTH Width – Amount is width of new face. DEPTH Depth – Amount is perpendicular distance from original edge to bevel face. PERCENT Percent – Amount is percent of adjacent edge length. ABSOLUTE Absolute – Amount is absolute distance along adjacent edge.

Width Type, The method for determining the size of the bevel

OFFSET Offset – Amount is offset of new edges from original.

WIDTH Width – Amount is width of new face.

DEPTH Depth – Amount is perpendicular distance from original edge to bevel face.

PERCENT Percent – Amount is percent of adjacent edge length.

ABSOLUTE Absolute – Amount is absolute distance along adjacent edge.

offset (float in [0, 1e+06], (optional)) – Width, Bevel amount

profile_type (enum in ['SUPERELLIPSE', 'CUSTOM'], (optional)) – Profile Type, The type of shape used to rebuild a beveled section SUPERELLIPSE Superellipse – The profile can be a concave or convex curve. CUSTOM Custom – The profile can be any arbitrary path between its endpoints.

Profile Type, The type of shape used to rebuild a beveled section

SUPERELLIPSE Superellipse – The profile can be a concave or convex curve.

CUSTOM Custom – The profile can be any arbitrary path between its endpoints.

offset_pct (float in [0, 100], (optional)) – Width Percent, Bevel amount for percentage method

segments (int in [1, 1000], (optional)) – Segments, Segments for curved edge

profile (float in [0, 1], (optional)) – Profile, Controls profile shape (0.5 = round)

affect (enum in ['VERTICES', 'EDGES'], (optional)) – Affect, Affect edges or vertices VERTICES Vertices – Affect only vertices. EDGES Edges – Affect only edges.

Affect, Affect edges or vertices

VERTICES Vertices – Affect only vertices.

EDGES Edges – Affect only edges.

clamp_overlap (boolean, (optional)) – Clamp Overlap, Do not allow beveled edges/vertices to overlap each other

loop_slide (boolean, (optional)) – Loop Slide, Prefer sliding along edges to even widths

mark_seam (boolean, (optional)) – Mark Seams, Preserve seams along beveled edges

mark_sharp (boolean, (optional)) – Mark Sharp, Preserve sharp edges along beveled edges

material (int in [-1, inf], (optional)) – Material Index, Material for bevel faces (-1 means use adjacent faces)

harden_normals (boolean, (optional)) – Harden Normals, Match normals of new faces to adjacent faces

face_strength_mode (enum in ['NONE', 'NEW', 'AFFECTED', 'ALL'], (optional)) – Face Strength Mode, Whether to set face strength, and which faces to set face strength on NONE None – Do not set face strength. NEW New – Set face strength on new faces only. AFFECTED Affected – Set face strength on new and modified faces only. ALL All – Set face strength on all faces.

Face Strength Mode, Whether to set face strength, and which faces to set face strength on

NONE None – Do not set face strength.

NEW New – Set face strength on new faces only.

AFFECTED Affected – Set face strength on new and modified faces only.

ALL All – Set face strength on all faces.

miter_outer (enum in ['SHARP', 'PATCH', 'ARC'], (optional)) – Outer Miter, Pattern to use for outside of miters SHARP Sharp – Outside of miter is sharp. PATCH Patch – Outside of miter is squared-off patch. ARC Arc – Outside of miter is arc.

Outer Miter, Pattern to use for outside of miters

SHARP Sharp – Outside of miter is sharp.

PATCH Patch – Outside of miter is squared-off patch.

ARC Arc – Outside of miter is arc.

miter_inner (enum in ['SHARP', 'ARC'], (optional)) – Inner Miter, Pattern to use for inside of miters SHARP Sharp – Inside of miter is sharp. ARC Arc – Inside of miter is arc.

Inner Miter, Pattern to use for inside of miters

SHARP Sharp – Inside of miter is sharp.

ARC Arc – Inside of miter is arc.

spread (float in [0, 1e+06], (optional)) – Spread, Amount to spread arcs for arc inner miters

vmesh_method (enum in ['ADJ', 'CUTOFF'], (optional)) – Vertex Mesh Method, The method to use to create meshes at intersections ADJ Grid Fill – Default patterned fill. CUTOFF Cutoff – A cutoff at each profile’s end before the intersection.

Vertex Mesh Method, The method to use to create meshes at intersections

ADJ Grid Fill – Default patterned fill.

CUTOFF Cutoff – A cutoff at each profile’s end before the intersection.

release_confirm (boolean, (optional)) – Confirm on Release

Cut geometry along a plane (click-drag to define plane)

plane_co (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Plane Point, A point on the plane

plane_no (mathutils.Vector of 3 items in [-1, 1], (optional)) – Plane Normal, The direction the plane points

use_fill (boolean, (optional)) – Fill, Fill in the cut

clear_inner (boolean, (optional)) – Clear Inner, Remove geometry behind the plane

clear_outer (boolean, (optional)) – Clear Outer, Remove geometry in front of the plane

threshold (float in [0, 10], (optional)) – Axis Threshold, Preserves the existing geometry along the cut plane

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

Blend in shape from a shape key

shape (enum in [], (optional)) – Shape, Shape key to use for blending

blend (float in [-1000, 1000], (optional)) – Blend, Blending factor

add (boolean, (optional)) – Add, Add rather than blend between shapes

Create a bridge of faces between two or more selected edge loops

type (enum in ['SINGLE', 'CLOSED', 'PAIRS'], (optional)) – Connect Loops, Method of bridging multiple loops

use_merge (boolean, (optional)) – Merge, Merge rather than creating faces

merge_factor (float in [0, 1], (optional)) – Merge Factor

twist_offset (int in [-1000, 1000], (optional)) – Twist, Twist offset for closed loops

number_cuts (int in [0, 1000], (optional)) – Number of Cuts

interpolation (enum in ['LINEAR', 'PATH', 'SURFACE'], (optional)) – Interpolation, Interpolation method

smoothness (float in [0, 1000], (optional)) – Smoothness, Smoothness factor

profile_shape_factor (float in [-1000, 1000], (optional)) – Profile Factor, How much intermediary new edges are shrunk/expanded

profile_shape (enum in Proportional Falloff Curve Only Items, (optional)) – Profile Shape, Shape of the profile

Flip direction of face corner color attribute inside faces

Rotate face corner color attribute inside faces

use_ccw (boolean, (optional)) – Counter Clockwise

Enclose selected vertices in a convex polyhedron

delete_unused (boolean, (optional)) – Delete Unused, Delete selected elements that are not used by the hull

use_existing_faces (boolean, (optional)) – Use Existing Faces, Skip hull triangles that are covered by a pre-existing face

make_holes (boolean, (optional)) – Make Holes, Delete selected faces that are used by the hull

join_triangles (boolean, (optional)) – Join Triangles, Merge adjacent triangles into quads

face_threshold (float in [0, 3.14159], (optional)) – Max Face Angle, Face angle limit

shape_threshold (float in [0, 3.14159], (optional)) – Max Shape Angle, Shape angle limit

topology_influence (float in [0, 2], (optional)) – Topology Influence, How much to prioritize regular grids of quads as well as quads that touch existing quads

uvs (boolean, (optional)) – Compare UVs

vcols (boolean, (optional)) – Compare Color Attributes

seam (boolean, (optional)) – Compare Seam

sharp (boolean, (optional)) – Compare Sharp

materials (boolean, (optional)) – Compare Materials

deselect_joined (boolean, (optional)) – Deselect Joined, Only select remaining triangles that were not merged

Add a custom normals layer, if none exists yet

Remove the custom normals layer, if it exists

Clear vertex sculpt masking data from the mesh

Add a vertex skin layer

Clear vertex skin layer

Simplify geometry by collapsing edges

ratio (float in [0, 1], (optional)) – Ratio

use_vertex_group (boolean, (optional)) – Vertex Group, Use active vertex group as an influence

vertex_group_factor (float in [0, 1000], (optional)) – Weight, Vertex group strength

invert_vertex_group (boolean, (optional)) – Invert, Invert vertex group influence

use_symmetry (boolean, (optional)) – Symmetry, Maintain symmetry on an axis

symmetry_axis (enum in Axis Xyz Items, (optional)) – Axis, Axis of symmetry

Delete selected vertices, edges or faces

type (enum in ['VERT', 'EDGE', 'FACE', 'EDGE_FACE', 'ONLY_FACE'], (optional)) – Type, Method used for deleting mesh data

Delete an edge loop by merging the faces on each side

use_face_split (boolean, (optional)) – Face Split, Split off face corners to maintain surrounding geometry

Delete loose vertices, edges or faces

use_verts (boolean, (optional)) – Vertices, Remove loose vertices

use_edges (boolean, (optional)) – Edges, Remove loose edges

use_faces (boolean, (optional)) – Faces, Remove loose faces

Dissolve zero area faces and zero length edges

threshold (float in [1e-06, 50], (optional)) – Merge Distance, Maximum distance between elements to merge

Dissolve edges, merging faces

use_verts (boolean, (optional)) – Dissolve Vertices, Dissolve remaining vertices which connect to only two edges

angle_threshold (float in [0, 3.14159], (optional)) – Angle Threshold, Remaining vertices which separate edge pairs are preserved if their edge angle exceeds this threshold.

use_face_split (boolean, (optional)) – Face Split, Split off face corners to maintain surrounding geometry

use_verts (boolean, (optional)) – Dissolve Vertices, Dissolve remaining vertices which connect to only two edges

Dissolve selected edges and vertices, limited by the angle of surrounding geometry

angle_limit (float in [0, 3.14159], (optional)) – Max Angle, Angle limit

use_dissolve_boundaries (boolean, (optional)) – All Boundaries, Dissolve all vertices in between face boundaries

delimit (enum set in Mesh Delimit Mode Items, (optional)) – Delimit, Delimit dissolve operation

Dissolve geometry based on the selection mode

use_verts (boolean, (optional)) – Dissolve Vertices, Dissolve remaining vertices which connect to only two edges

angle_threshold (float in [0, 3.14159], (optional)) – Angle Threshold, Remaining vertices which separate edge pairs are preserved if their edge angle exceeds this threshold.

use_face_split (boolean, (optional)) – Face Split, Split off face corners to maintain surrounding geometry

use_boundary_tear (boolean, (optional)) – Tear Boundary, Split off face corners instead of merging faces

Dissolve vertices, merge edges and faces

use_face_split (boolean, (optional)) – Face Split, Split off face corners to maintain surrounding geometry

use_boundary_tear (boolean, (optional)) – Tear Boundary, Split off face corners instead of merging faces

Duplicate and extrude selected vertices, edges or faces towards the mouse cursor

rotate_source (boolean, (optional)) – Rotate Source, Rotate initial selection giving better shape

Duplicate selected vertices, edges or faces

mode (int in [0, inf], (optional)) – Mode

Duplicate mesh and move

MESH_OT_duplicate (MESH_OT_duplicate, (optional)) – Duplicate, Duplicate selected vertices, edges or faces

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Collapse isolated edge and face regions, merging data such as UVs and color attributes. This can collapse edge-rings as well as regions of connected faces into vertices

Add an edge or face to selected

Rotate selected edge or adjoining faces

use_ccw (boolean, (optional)) – Counter Clockwise

Split selected edges so that each neighbor face gets its own copy

type (enum in ['EDGE', 'VERT'], (optional)) – Type, Method to use for splitting EDGE Faces by Edges – Split faces along selected edges. VERT Faces & Edges by Vertices – Split faces and edges connected to selected vertices.

Type, Method to use for splitting

EDGE Faces by Edges – Split faces along selected edges.

VERT Faces & Edges by Vertices – Split faces and edges connected to selected vertices.

extend (boolean, (optional)) – Extend, Extend the selection

deselect (boolean, (optional)) – Deselect, Remove from the selection

toggle (boolean, (optional)) – Toggle Select, Toggle the selection

ring (boolean, (optional)) – Select Ring, Select ring

Select all sharp enough edges

sharpness (float in [0.000174533, 3.14159], (optional)) – Sharpness

use_normal_flip (boolean, (optional)) – Flip Normals

use_dissolve_ortho_edges (boolean, (optional)) – Dissolve Orthogonal Edges

mirror (boolean, (optional)) – Mirror Editing

Extrude region together along the average normal

MESH_OT_extrude_context (MESH_OT_extrude_context, (optional)) – Extrude Context, Extrude selection

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude individual edges only

use_normal_flip (boolean, (optional)) – Flip Normals

mirror (boolean, (optional)) – Mirror Editing

Extrude edges and move result

MESH_OT_extrude_edges_indiv (MESH_OT_extrude_edges_indiv, (optional)) – Extrude Only Edges, Extrude individual edges only

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude individual faces only

mirror (boolean, (optional)) – Mirror Editing

Extrude each individual face separately along local normals

MESH_OT_extrude_faces_indiv (MESH_OT_extrude_faces_indiv, (optional)) – Extrude Individual Faces, Extrude individual faces only

TRANSFORM_OT_shrink_fatten (TRANSFORM_OT_shrink_fatten, (optional)) – Shrink/Fatten, Shrink/fatten selected vertices along normals

Extrude, dissolves edges whose faces form a flat surface and intersect new edges

MESH_OT_extrude_region (MESH_OT_extrude_region, (optional)) – Extrude Region, Extrude region of faces

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude region of faces

use_normal_flip (boolean, (optional)) – Flip Normals

use_dissolve_ortho_edges (boolean, (optional)) – Dissolve Orthogonal Edges

mirror (boolean, (optional)) – Mirror Editing

Extrude region and move result

MESH_OT_extrude_region (MESH_OT_extrude_region, (optional)) – Extrude Region, Extrude region of faces

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude region together along local normals

MESH_OT_extrude_region (MESH_OT_extrude_region, (optional)) – Extrude Region, Extrude region of faces

TRANSFORM_OT_shrink_fatten (TRANSFORM_OT_shrink_fatten, (optional)) – Shrink/Fatten, Shrink/fatten selected vertices along normals

Extrude selected vertices, edges or faces repeatedly

steps (int in [0, 1000000], (optional)) – Steps

offset (mathutils.Vector of 3 items in [-100000, 100000], (optional)) – Offset, Offset vector

scale_offset (float in [0, inf], (optional)) – Scale Offset

Extrude vertices and move result

MESH_OT_extrude_verts_indiv (MESH_OT_extrude_verts_indiv, (optional)) – Extrude Only Vertices, Extrude individual vertices only

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude individual vertices only

mirror (boolean, (optional)) – Mirror Editing

Flatten selected faces

factor (float in [-10, 10], (optional)) – Factor

repeat (int in [1, 10000], (optional)) – Iterations

Weld loose edges into faces (splitting them into new faces)

Select linked faces by angle

sharpness (float in [0.000174533, 3.14159], (optional)) – Sharpness

Display faces smooth (using vertex normals)

Fill a selected edge loop with faces

use_beauty (boolean, (optional)) – Beauty, Use best triangulation division

Fill grid from two loops

span (int in [1, 1000], (optional)) – Span, Number of grid columns

offset (int in [-1000, 1000], (optional)) – Offset, Vertex that is the corner of the grid

use_interp_simple (boolean, (optional)) – Simple Blending, Use simple interpolation of grid vertices

Fill in holes (boundary edge loops)

sides (int in [0, 1000], (optional)) – Sides, Number of sides in hole required to fill (zero fills all holes)

Flip the direction of selected faces’ normals (and of their vertices)

only_clnors (boolean, (optional)) – Custom Normals Only, Only flip the custom loop normals of the selected elements

Flips the tessellation of selected quads

Hide (un)selected vertices, edges or faces

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Inset new faces into selected faces

use_boundary (boolean, (optional)) – Boundary, Inset face boundaries

use_even_offset (boolean, (optional)) – Offset Even, Scale the offset to give more even thickness

use_relative_offset (boolean, (optional)) – Offset Relative, Scale the offset by surrounding geometry

use_edge_rail (boolean, (optional)) – Edge Rail, Inset the region along existing edges

thickness (float in [0, inf], (optional)) – Thickness

depth (float in [-inf, inf], (optional)) – Depth

use_outset (boolean, (optional)) – Outset, Outset rather than inset

use_select_inset (boolean, (optional)) – Select Outer, Select the new inset faces

use_individual (boolean, (optional)) – Individual, Individual face inset

use_interpolate (boolean, (optional)) – Interpolate, Blend face data across the inset

release_confirm (boolean, (optional)) – Confirm on Release

Cut an intersection into faces

mode (enum in ['SELECT', 'SELECT_UNSELECT'], (optional)) – Source SELECT Self Intersect – Self intersect selected faces. SELECT_UNSELECT Selected/Unselected – Intersect selected with unselected faces.

SELECT Self Intersect – Self intersect selected faces.

SELECT_UNSELECT Selected/Unselected – Intersect selected with unselected faces.

separate_mode (enum in ['ALL', 'CUT', 'NONE'], (optional)) – Separate Mode ALL All – Separate all geometry from intersections. CUT Cut – Cut into geometry keeping each side separate (Selected/Unselected only). NONE Merge – Merge all geometry from the intersection.

ALL All – Separate all geometry from intersections.

CUT Cut – Cut into geometry keeping each side separate (Selected/Unselected only).

NONE Merge – Merge all geometry from the intersection.

threshold (float in [0, 0.01], (optional)) – Merge Threshold

solver (enum in ['FLOAT', 'EXACT'], (optional)) – Solver, Which Intersect solver to use FLOAT Float – Simple solver with good performance, without support for overlapping geometry. EXACT Exact – Slower solver with the best results for coplanar faces.

Solver, Which Intersect solver to use

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

EXACT Exact – Slower solver with the best results for coplanar faces.

Cut solid geometry from selected to unselected

operation (enum in ['INTERSECT', 'UNION', 'DIFFERENCE'], (optional)) – Boolean Operation, Which boolean operation to apply

use_swap (boolean, (optional)) – Swap, Use with difference intersection to swap which side is kept

use_self (boolean, (optional)) – Self Intersection, Do self-union or self-intersection

threshold (float in [0, 0.01], (optional)) – Merge Threshold

solver (enum in ['FLOAT', 'EXACT'], (optional)) – Solver, Which Boolean solver to use FLOAT Float – Faster solver, some limitations. EXACT Exact – Exact solver, slower, handles more cases.

Solver, Which Boolean solver to use

FLOAT Float – Faster solver, some limitations.

EXACT Exact – Exact solver, slower, handles more cases.

Use other objects outlines and boundaries to project knife cuts

cut_through (boolean, (optional)) – Cut Through, Cut through all faces, not just visible ones

use_occlude_geometry (boolean, (optional)) – Occlude Geometry, Only cut the front most geometry

only_selected (boolean, (optional)) – Only Selected, Only cut selected geometry

xray (boolean, (optional)) – X-Ray, Show cuts hidden by geometry

visible_measurements (enum in ['NONE', 'BOTH', 'DISTANCE', 'ANGLE'], (optional)) – Measurements, Visible distance and angle measurements NONE None – Show no measurements. BOTH Both – Show both distances and angles. DISTANCE Distance – Show just distance measurements. ANGLE Angle – Show just angle measurements.

Measurements, Visible distance and angle measurements

NONE None – Show no measurements.

BOTH Both – Show both distances and angles.

DISTANCE Distance – Show just distance measurements.

ANGLE Angle – Show just angle measurements.

angle_snapping (enum in ['NONE', 'SCREEN', 'RELATIVE'], (optional)) – Angle Snapping, Angle snapping mode NONE None – No angle snapping. SCREEN Screen – Screen space angle snapping. RELATIVE Relative – Angle snapping relative to the previous cut edge.

Angle Snapping, Angle snapping mode

NONE None – No angle snapping.

SCREEN Screen – Screen space angle snapping.

RELATIVE Relative – Angle snapping relative to the previous cut edge.

angle_snapping_increment (float in [0, 3.14159], (optional)) – Angle Snap Increment, The angle snap increment used when in constrained angle mode

wait_for_input (boolean, (optional)) – Wait for Input

Select a loop of connected edges by connection type

ring (boolean, (optional)) – Ring

Select a loop of connected edges

extend (boolean, (optional)) – Extend Select, Extend the selection

deselect (boolean, (optional)) – Deselect, Remove from the selection

toggle (boolean, (optional)) – Toggle Select, Toggle the selection

ring (boolean, (optional)) – Select Ring, Select ring

Select region of faces inside of a selected loop of edges

select_bigger (boolean, (optional)) – Select Bigger, Select bigger regions instead of smaller ones

Add a new loop between existing loops

number_cuts (int in [1, 1000000], (optional)) – Number of Cuts

smoothness (float in [-1000, 1000], (optional)) – Smoothness, Smoothness factor

falloff (enum in Proportional Falloff Curve Only Items, (optional)) – Falloff, Falloff type of the feather

object_index (int in [-1, inf], (optional)) – Object Index

edge_index (int in [-1, inf], (optional)) – Edge Index

Cut mesh loop and slide it

MESH_OT_loopcut (MESH_OT_loopcut, (optional)) – Loop Cut, Add a new loop between existing loops

TRANSFORM_OT_edge_slide (TRANSFORM_OT_edge_slide, (optional)) – Edge Slide, Slide an edge loop along a mesh

(Un)mark selected edges as Freestyle feature edges

clear (boolean, (optional)) – Clear

(Un)mark selected faces for exclusion from Freestyle feature edge detection

clear (boolean, (optional)) – Clear

(Un)mark selected edges as a seam

clear (boolean, (optional)) – Clear

(Un)mark selected edges as sharp

clear (boolean, (optional)) – Clear

use_verts (boolean, (optional)) – Vertices, Consider vertices instead of edges to select which edges to (un)tag as sharp

Merge selected vertices

type (enum in ['CENTER', 'CURSOR', 'COLLAPSE', 'FIRST', 'LAST'], (optional)) – Type, Merge method to use

uvs (boolean, (optional)) – UVs, Move UVs according to merge

Merge custom normals of selected vertices

Set/Get strength of face (used in Weighted Normal modifier)

set (boolean, (optional)) – Set Value, Set value of faces

face_strength (enum in ['WEAK', 'MEDIUM', 'STRONG'], (optional)) – Face Strength, Strength to use for assigning or selecting face influence for weighted normal modifier

Make face and vertex normals point either outside or inside the mesh

inside (boolean, (optional)) – Inside

Custom normals tools using Normal Vector of UI

mode (enum in ['COPY', 'PASTE', 'ADD', 'MULTIPLY', 'RESET'], (optional)) – Mode, Mode of tools taking input from interface COPY Copy Normal – Copy normal to the internal clipboard. PASTE Paste Normal – Paste normal from the internal clipboard. ADD Add Normal – Add normal vector with selection. MULTIPLY Multiply Normal – Multiply normal vector with selection. RESET Reset Normal – Reset the internal clipboard and/or normal of selected element.

Mode, Mode of tools taking input from interface

COPY Copy Normal – Copy normal to the internal clipboard.

PASTE Paste Normal – Paste normal from the internal clipboard.

ADD Add Normal – Add normal vector with selection.

MULTIPLY Multiply Normal – Multiply normal vector with selection.

RESET Reset Normal – Reset the internal clipboard and/or normal of selected element.

absolute (boolean, (optional)) – Absolute Coordinates, Copy Absolute coordinates of Normal vector

Create offset edge loop from the current selection

use_cap_endpoint (boolean, (optional)) – Cap Endpoint, Extend loop around end-points

Offset edge loop slide

MESH_OT_offset_edge_loops (MESH_OT_offset_edge_loops, (optional)) – Offset Edge Loop, Create offset edge loop from the current selection

TRANSFORM_OT_edge_slide (TRANSFORM_OT_edge_slide, (optional)) – Edge Slide, Slide an edge loop along a mesh

Point selected custom normals to specified Target

mode (enum in ['COORDINATES', 'MOUSE'], (optional)) – Mode, How to define coordinates to point custom normals to COORDINATES Coordinates – Use static coordinates (defined by various means). MOUSE Mouse – Follow mouse cursor.

Mode, How to define coordinates to point custom normals to

COORDINATES Coordinates – Use static coordinates (defined by various means).

MOUSE Mouse – Follow mouse cursor.

invert (boolean, (optional)) – Invert, Invert affected normals

align (boolean, (optional)) – Align, Make all affected normals parallel

target_location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Target, Target location to which normals will point

spherize (boolean, (optional)) – Spherize, Interpolate between original and new normals

spherize_strength (float in [0, 1], (optional)) – Spherize Strength, Ratio of spherized normal to original normal

Split a face into a fan

offset (float in [-1000, 1000], (optional)) – Poke Offset, Poke Offset

use_relative_offset (boolean, (optional)) – Offset Relative, Scale the offset by surrounding geometry

center_mode (enum in ['MEDIAN_WEIGHTED', 'MEDIAN', 'BOUNDS'], (optional)) – Poke Center, Poke face center calculation MEDIAN_WEIGHTED Weighted Median – Weighted median face center. MEDIAN Median – Median face center. BOUNDS Bounds – Face bounds center.

Poke Center, Poke face center calculation

MEDIAN_WEIGHTED Weighted Median – Weighted median face center.

MEDIAN Median – Median face center.

BOUNDS Bounds – Face bounds center.

Undocumented, consider contributing.

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Undocumented, consider contributing.

Undocumented, consider contributing.

MESH_OT_polybuild_transform_at_cursor (MESH_OT_polybuild_transform_at_cursor, (optional)) – Poly Build Transform at Cursor

MESH_OT_extrude_edges_indiv (MESH_OT_extrude_edges_indiv, (optional)) – Extrude Only Edges, Extrude individual edges only

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Undocumented, consider contributing.

create_quads (boolean, (optional)) – Create Quads, Automatically split edges in triangles to maintain quad topology

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Undocumented, consider contributing.

MESH_OT_polybuild_face_at_cursor (MESH_OT_polybuild_face_at_cursor, (optional)) – Poly Build Face at Cursor

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Undocumented, consider contributing.

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Undocumented, consider contributing.

MESH_OT_polybuild_split_at_cursor (MESH_OT_polybuild_split_at_cursor, (optional)) – Poly Build Split at Cursor

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Undocumented, consider contributing.

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Undocumented, consider contributing.

MESH_OT_polybuild_transform_at_cursor (MESH_OT_polybuild_transform_at_cursor, (optional)) – Poly Build Transform at Cursor

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Construct a circle mesh

vertices (int in [3, 10000000], (optional)) – Vertices

radius (float in [0, inf], (optional)) – Radius

fill_type (enum in ['NOTHING', 'NGON', 'TRIFAN'], (optional)) – Fill Type NOTHING Nothing – Don’t fill at all. NGON N-Gon – Use n-gons. TRIFAN Triangle Fan – Use triangle fans.

NOTHING Nothing – Don’t fill at all.

NGON N-Gon – Use n-gons.

TRIFAN Triangle Fan – Use triangle fans.

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a conic mesh

vertices (int in [3, 10000000], (optional)) – Vertices

radius1 (float in [0, inf], (optional)) – Radius 1

radius2 (float in [0, inf], (optional)) – Radius 2

depth (float in [0, inf], (optional)) – Depth

end_fill_type (enum in ['NOTHING', 'NGON', 'TRIFAN'], (optional)) – Base Fill Type NOTHING Nothing – Don’t fill at all. NGON N-Gon – Use n-gons. TRIFAN Triangle Fan – Use triangle fans.

NOTHING Nothing – Don’t fill at all.

NGON N-Gon – Use n-gons.

TRIFAN Triangle Fan – Use triangle fans.

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a cube mesh that consists of six square faces

size (float in [0, inf], (optional)) – Size

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a cube mesh

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – Matrix

Construct a cylinder mesh

vertices (int in [3, 10000000], (optional)) – Vertices

radius (float in [0, inf], (optional)) – Radius

depth (float in [0, inf], (optional)) – Depth

end_fill_type (enum in ['NOTHING', 'NGON', 'TRIFAN'], (optional)) – Cap Fill Type NOTHING Nothing – Don’t fill at all. NGON N-Gon – Use n-gons. TRIFAN Triangle Fan – Use triangle fans.

NOTHING Nothing – Don’t fill at all.

NGON N-Gon – Use n-gons.

TRIFAN Triangle Fan – Use triangle fans.

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a subdivided plane mesh

x_subdivisions (int in [1, 10000000], (optional)) – X Subdivisions

y_subdivisions (int in [1, 10000000], (optional)) – Y Subdivisions

size (float in [0, inf], (optional)) – Size

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a spherical mesh that consists of equally sized triangles

subdivisions (int in [1, 10], (optional)) – Subdivisions

radius (float in [0, inf], (optional)) – Radius

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Suzanne mesh

size (float in [0, inf], (optional)) – Size

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a filled planar mesh with 4 vertices

size (float in [0, inf], (optional)) – Size

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a torus mesh

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation

major_segments (int in [3, 256], (optional)) – Major Segments, Number of segments for the main ring of the torus

minor_segments (int in [3, 256], (optional)) – Minor Segments, Number of segments for the minor ring of the torus

mode (enum in ['MAJOR_MINOR', 'EXT_INT'], (optional)) – Dimensions Mode MAJOR_MINOR Major/Minor – Use the major/minor radii for torus dimensions. EXT_INT Exterior/Interior – Use the exterior/interior radii for torus dimensions.

MAJOR_MINOR Major/Minor – Use the major/minor radii for torus dimensions.

EXT_INT Exterior/Interior – Use the exterior/interior radii for torus dimensions.

major_radius (float in [0, 10000], (optional)) – Major Radius, Radius from the origin to the center of the cross sections

minor_radius (float in [0, 10000], (optional)) – Minor Radius, Radius of the torus’ cross section

abso_major_rad (float in [0, 10000], (optional)) – Exterior Radius, Total Exterior Radius of the torus

abso_minor_rad (float in [0, 10000], (optional)) – Interior Radius, Total Interior Radius of the torus

generate_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

startup/bl_operators/add_mesh_torus.py:222

Construct a spherical mesh with quad faces, except for triangle faces at the top and bottom

segments (int in [3, 100000], (optional)) – Segments

ring_count (int in [3, 100000], (optional)) – Rings

radius (float in [0, inf], (optional)) – Radius

calc_uvs (boolean, (optional)) – Generate UVs, Generate a default UV map

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Triangulate selected faces

quad_method (enum in Modifier Triangulate Quad Method Items, (optional)) – Quad Method, Method for splitting the quads into triangles

ngon_method (enum in Modifier Triangulate Ngon Method Items, (optional)) – N-gon Method, Method for splitting the n-gons into triangles

Select boundary edges around the selected faces

Merge vertices based on their proximity

threshold (float in [1e-06, 50], (optional)) – Merge Distance, Maximum distance between elements to merge

use_centroid (boolean, (optional)) – Centroid Merge, Move vertices to the centroid of the duplicate cluster, otherwise the vertex closest to the centroid is used.

use_unselected (boolean, (optional)) – Unselected, Merge selected to other unselected vertices

use_sharp_edge_from_normals (boolean, (optional)) – Sharp Edges, Calculate sharp edges using custom normal data (when available)

Reorder mesh faces and vertices based on their spatial position for better BVH building and sculpting performance.

Reveal all hidden vertices, edges and faces

select (boolean, (optional)) – Select

Disconnect vertex or edges from connected geometry

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

use_fill (boolean, (optional)) – Fill, Fill the ripped region

Extend vertices along the edge closest to the cursor

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Extend vertices and move the result

MESH_OT_rip_edge (MESH_OT_rip_edge, (optional)) – Extend Vertices, Extend vertices along the edge closest to the cursor

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Rip polygons and move the result

MESH_OT_rip (MESH_OT_rip, (optional)) – Rip, Disconnect vertex or edges from connected geometry

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Extrude selected vertices in screw-shaped rotation around the cursor in indicated viewport

steps (int in [1, 100000], (optional)) – Steps, Steps

turns (int in [1, 100000], (optional)) – Turns, Turns

center (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center, Center in global view space

axis (mathutils.Vector of 3 items in [-1, 1], (optional)) – Axis, Axis in global view space

(De)select all vertices, edges or faces

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all data in the mesh on a single axis

orientation (enum in Transform Orientation Items, (optional)) – Axis Mode, Axis orientation

sign (enum in ['POS', 'NEG', 'ALIGN'], (optional)) – Axis Sign, Side to select

axis (enum in Axis Xyz Items, (optional)) – Axis, Select the axis to compare each vertex on

threshold (float in [1e-06, 50], (optional)) – Threshold

Select elements based on the active boolean attribute

Select vertices at poles by the number of connected edges. In edge and face mode the geometry connected to the vertices is selected

pole_count (int in [0, inf], (optional)) – Pole Count

type (enum in ['LESS', 'EQUAL', 'GREATER', 'NOTEQUAL'], (optional)) – Type, Type of comparison to make

extend (boolean, (optional)) – Extend, Extend the selection

exclude_nonmanifold (boolean, (optional)) – Exclude Non Manifold, Exclude non-manifold poles

Select vertices or faces by the number of face sides

number (int in [3, inf], (optional)) – Number of Vertices

type (enum in ['LESS', 'EQUAL', 'GREATER', 'NOTEQUAL'], (optional)) – Type, Type of comparison to make

extend (boolean, (optional)) – Extend, Extend the selection

Select faces where all edges have more than 2 face users

Deselect vertices, edges or faces at the boundary of each selection region

use_face_step (boolean, (optional)) – Face Step, Connected faces (instead of edges)

Select all vertices connected to the current selection

delimit (enum set in Mesh Delimit Mode Items, (optional)) – Delimit, Delimit selected region

(De)select all vertices linked to the edge under the mouse cursor

deselect (boolean, (optional)) – Deselect

delimit (enum set in Mesh Delimit Mode Items, (optional)) – Delimit, Delimit selected region

Select loose geometry based on the selection mode

extend (boolean, (optional)) – Extend, Extend the selection

Select mesh items at mirrored locations

axis (enum set in Axis Flag Xyz Items, (optional)) – Axis

extend (boolean, (optional)) – Extend, Extend the existing selection

Change selection mode

use_extend (boolean, (optional)) – Extend

use_expand (boolean, (optional)) – Expand

type (enum in Mesh Select Mode Items, (optional)) – Type

action (enum in ['DISABLE', 'ENABLE', 'TOGGLE'], (optional)) – Action, Selection action to execute DISABLE Disable – Disable selected markers. ENABLE Enable – Enable selected markers. TOGGLE Toggle – Toggle disabled flag for selected markers.

Action, Selection action to execute

DISABLE Disable – Disable selected markers.

ENABLE Enable – Enable selected markers.

TOGGLE Toggle – Toggle disabled flag for selected markers.

Select more vertices, edges or faces connected to initial selection

use_face_step (boolean, (optional)) – Face Step, Connected faces (instead of edges)

Select the next element (using selection order)

startup/bl_operators/mesh.py:18

Select all non-manifold vertices or edges

extend (boolean, (optional)) – Extend, Extend the selection

use_wire (boolean, (optional)) – Wire, Wire edges

use_boundary (boolean, (optional)) – Boundaries, Boundary edges

use_multi_face (boolean, (optional)) – Multiple Faces, Edges shared by more than two faces

use_non_contiguous (boolean, (optional)) – Non Contiguous, Edges between faces pointing in alternate directions

use_verts (boolean, (optional)) – Vertices, Vertices connecting multiple face regions

Deselect every Nth element starting from the active vertex, edge or face

skip (int in [1, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Select the previous element (using selection order)

startup/bl_operators/mesh.py:43

Randomly select vertices

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select similar vertices, edges or faces by property types

type (enum in ['VERT_NORMAL', 'VERT_FACES', 'VERT_GROUPS', 'VERT_EDGES', 'VERT_CREASE', 'EDGE_LENGTH', 'EDGE_DIR', 'EDGE_FACES', 'EDGE_FACE_ANGLE', 'EDGE_CREASE', 'EDGE_BEVEL', 'EDGE_SEAM', 'EDGE_SHARP', 'EDGE_FREESTYLE', 'FACE_MATERIAL', 'FACE_AREA', 'FACE_SIDES', 'FACE_PERIMETER', 'FACE_NORMAL', 'FACE_COPLANAR', 'FACE_SMOOTH', 'FACE_FREESTYLE'], (optional)) – Type

compare (enum in ['EQUAL', 'GREATER', 'LESS'], (optional)) – Compare

threshold (float in [0, 100000], (optional)) – Threshold

Select similar face regions to the current selection

Select vertices without a group

extend (boolean, (optional)) – Extend, Extend the selection

Separate selected geometry into a new mesh

type (enum in ['SELECTED', 'MATERIAL', 'LOOSE'], (optional)) – Type

Set the custom normals from the selected faces ones

keep_sharp (boolean, (optional)) – Keep Sharp Edges, Do not set sharp edges to face

Set edge sharpness based on the angle between neighboring faces

angle (float in [0.000174533, 3.14159], (optional)) – Angle

extend (boolean, (optional)) – Extend, Add new sharp edges without clearing existing sharp edges

Apply selected vertex locations to all other shape keys

Select shortest path between two selections

edge_mode (enum in ['SELECT', 'SEAM', 'SHARP', 'CREASE', 'BEVEL', 'FREESTYLE'], (optional)) – Edge Tag, The edge flag to tag when selecting the shortest path

use_face_step (boolean, (optional)) – Face Stepping, Traverse connected faces (includes diagonals and edge-rings)

use_topology_distance (boolean, (optional)) – Topology Distance, Find the minimum number of steps, ignoring spatial distance

use_fill (boolean, (optional)) – Fill Region, Select all paths between the source/destination elements

skip (int in [0, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Selected shortest path between two vertices/edges/faces

edge_mode (enum in ['SELECT', 'SEAM', 'SHARP', 'CREASE', 'BEVEL', 'FREESTYLE'], (optional)) – Edge Tag, The edge flag to tag when selecting the shortest path

use_face_step (boolean, (optional)) – Face Stepping, Traverse connected faces (includes diagonals and edge-rings)

use_topology_distance (boolean, (optional)) – Topology Distance, Find the minimum number of steps, ignoring spatial distance

use_fill (boolean, (optional)) – Fill Region, Select all paths between the source/destination elements

skip (int in [0, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Smooth custom normals based on adjacent vertex normals

factor (float in [0, 1], (optional)) – Factor, Specifies weight of smooth vs original normal

Create a solid skin by extruding, compensating for sharp angles

thickness (float in [-10000, 10000], (optional)) – Thickness

The order of selected vertices/edges/faces is modified, based on a given method

type (enum in ['VIEW_ZAXIS', 'VIEW_XAXIS', 'CURSOR_DISTANCE', 'MATERIAL', 'SELECTED', 'RANDOMIZE', 'REVERSE'], (optional)) – Type, Type of reordering operation to apply VIEW_ZAXIS View Z Axis – Sort selected elements from farthest to nearest one in current view. VIEW_XAXIS View X Axis – Sort selected elements from left to right one in current view. CURSOR_DISTANCE Cursor Distance – Sort selected elements from nearest to farthest from 3D cursor. MATERIAL Material – Sort selected faces from smallest to greatest material index. SELECTED Selected – Move all selected elements in first places, preserving their relative order. Warning: This will affect unselected elements’ indices as well. RANDOMIZE Randomize – Randomize order of selected elements. REVERSE Reverse – Reverse current order of selected elements.

Type, Type of reordering operation to apply

VIEW_ZAXIS View Z Axis – Sort selected elements from farthest to nearest one in current view.

VIEW_XAXIS View X Axis – Sort selected elements from left to right one in current view.

CURSOR_DISTANCE Cursor Distance – Sort selected elements from nearest to farthest from 3D cursor.

MATERIAL Material – Sort selected faces from smallest to greatest material index.

SELECTED Selected – Move all selected elements in first places, preserving their relative order. Warning: This will affect unselected elements’ indices as well.

RANDOMIZE Randomize – Randomize order of selected elements.

REVERSE Reverse – Reverse current order of selected elements.

elements (enum set in {'VERT', 'EDGE', 'FACE'}, (optional)) – Elements, Which elements to affect (vertices, edges and/or faces)

reverse (boolean, (optional)) – Reverse, Reverse the sorting effect

seed (int in [0, inf], (optional)) – Seed, Seed for random-based operations

Extrude selected vertices in a circle around the cursor in indicated viewport

steps (int in [0, 1000000], (optional)) – Steps, Steps

dupli (boolean, (optional)) – Use Duplicates

angle (float in [-inf, inf], (optional)) – Angle, Rotation for each step

use_auto_merge (boolean, (optional)) – Auto Merge, Merge first/last when the angle is a full revolution

use_normal_flip (boolean, (optional)) – Flip Normals

center (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center, Center in global view space

axis (mathutils.Vector of 3 items in [-1, 1], (optional)) – Axis, Axis in global view space

Split off selected geometry from connected unselected geometry

Split custom normals of selected vertices

Subdivide selected edges

number_cuts (int in [1, 100], (optional)) – Number of Cuts

smoothness (float in [0, 1000], (optional)) – Smoothness, Smoothness factor

ngon (boolean, (optional)) – Create N-Gons, When disabled, newly created faces are limited to 3 and 4 sided faces

quadcorner (enum in ['INNERVERT', 'PATH', 'STRAIGHT_CUT', 'FAN'], (optional)) – Quad Corner Type, How to subdivide quad corners (anything other than Straight Cut will prevent n-gons)

fractal (float in [0, 1e+06], (optional)) – Fractal, Fractal randomness factor

fractal_along_normal (float in [0, 1], (optional)) – Along Normal, Apply fractal displacement along normal only

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

Subdivide perpendicular edges to the selected edge-ring

number_cuts (int in [0, 1000], (optional)) – Number of Cuts

interpolation (enum in ['LINEAR', 'PATH', 'SURFACE'], (optional)) – Interpolation, Interpolation method

smoothness (float in [0, 1000], (optional)) – Smoothness, Smoothness factor

profile_shape_factor (float in [-1000, 1000], (optional)) – Profile Factor, How much intermediary new edges are shrunk/expanded

profile_shape (enum in Proportional Falloff Curve Only Items, (optional)) – Profile Shape, Shape of the profile

Enforce symmetry (both form and topological) across an axis

direction (enum in Symmetrize Direction Items, (optional)) – Direction, Which sides to copy from and to

threshold (float in [0, 10], (optional)) – Threshold, Limit for snap middle vertices to the axis center

Snap vertex pairs to their mirrored locations

direction (enum in Symmetrize Direction Items, (optional)) – Direction, Which sides to copy from and to

threshold (float in [0, 10], (optional)) – Threshold, Distance within which matching vertices are searched

factor (float in [0, 1], (optional)) – Factor, Mix factor of the locations of the vertices

use_center (boolean, (optional)) – Center, Snap middle vertices to the axis center

Merge triangles into four sided polygons where possible

face_threshold (float in [0, 3.14159], (optional)) – Max Face Angle, Face angle limit

shape_threshold (float in [0, 3.14159], (optional)) – Max Shape Angle, Shape angle limit

topology_influence (float in [0, 2], (optional)) – Topology Influence, How much to prioritize regular grids of quads as well as quads that touch existing quads

uvs (boolean, (optional)) – Compare UVs

vcols (boolean, (optional)) – Compare Color Attributes

seam (boolean, (optional)) – Compare Seam

sharp (boolean, (optional)) – Compare Sharp

materials (boolean, (optional)) – Compare Materials

deselect_joined (boolean, (optional)) – Deselect Joined, Only select remaining triangles that were not merged

Un-subdivide selected edges and faces

iterations (int in [1, 1000], (optional)) – Iterations, Number of times to un-subdivide

Flip direction of UV coordinates inside faces

Rotate UV coordinates inside faces

use_ccw (boolean, (optional)) – Counter Clockwise

Connect selected vertices of faces, splitting the face

Make all faces convex

Split non-planar faces that exceed the angle threshold

angle_limit (float in [0, 3.14159], (optional)) – Max Angle, Angle limit

Connect vertices by their selection order, creating edges, splitting faces

Flatten angles of selected vertices

factor (float in [-10, 10], (optional)) – Smoothing, Smoothing factor

repeat (int in [1, 1000], (optional)) – Repeat, Number of times to smooth the mesh

xaxis (boolean, (optional)) – X-Axis, Smooth along the X axis

yaxis (boolean, (optional)) – Y-Axis, Smooth along the Y axis

zaxis (boolean, (optional)) – Z-Axis, Smooth along the Z axis

wait_for_input (boolean, (optional)) – Wait for Input

Laplacian smooth of selected vertices

repeat (int in [1, 1000], (optional)) – Number of iterations to smooth the mesh

lambda_factor (float in [1e-07, 1000], (optional)) – Lambda factor

lambda_border (float in [1e-07, 1000], (optional)) – Lambda factor in border

use_x (boolean, (optional)) – Smooth X Axis, Smooth object along X axis

use_y (boolean, (optional)) – Smooth Y Axis, Smooth object along Y axis

use_z (boolean, (optional)) – Smooth Z Axis, Smooth object along Z axis

preserve_volume (boolean, (optional)) – Preserve Volume, Apply volume preservation after smooth

Create a solid wireframe from faces

use_boundary (boolean, (optional)) – Boundary, Inset face boundaries

use_even_offset (boolean, (optional)) – Offset Even, Scale the offset to give more even thickness

use_relative_offset (boolean, (optional)) – Offset Relative, Scale the offset by surrounding geometry

use_replace (boolean, (optional)) – Replace, Remove original faces

thickness (float in [0, 10000], (optional)) – Thickness

offset (float in [0, 10000], (optional)) – Offset

use_crease (boolean, (optional)) – Crease, Crease hub edges for an improved subdivision surface

crease_weight (float in [0, 1000], (optional)) – Crease Weight

---

## Nla Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.nla.html

**Contents:**
- Nla Operators¶

Push action down onto the top of the NLA stack as a new strip

track_index (int in [-1, inf], (optional)) – Track Index, Index of NLA action track to perform pushdown operation on

Synchronize the length of the referenced Action with the length used in the strip

active (boolean, (optional)) – Active Strip Only, Only sync the active length for the active strip

Unlink this action from the active action slot (and/or exit Tweak Mode)

force_delete (boolean, (optional)) – Force Delete, Clear Fake User and remove copy stashed in this data-block’s NLA stack

Add an Action-Clip strip (i.e. an NLA Strip referencing an Action) to the active track

action (enum in [], (optional)) – Action

Apply scaling of selected strips to their referenced Actions

Bake all selected objects location/scale/rotation animation to an action

frame_start (int in [0, 300000], (optional)) – Start Frame, Start frame for baking

frame_end (int in [1, 300000], (optional)) – End Frame, End frame for baking

step (int in [1, 120], (optional)) – Frame Step, Number of frames to skip forward while baking each frame

only_selected (boolean, (optional)) – Only Selected Bones, Only key selected bones (Pose baking only)

visual_keying (boolean, (optional)) – Visual Keying, Keyframe from the final transformations (with constraints applied)

clear_constraints (boolean, (optional)) – Clear Constraints, Remove all constraints from keyed object/bones. To get a correct bake with this setting Visual Keying should be enabled

clear_parents (boolean, (optional)) – Clear Parents, Bake animation onto the object then clear parents (objects only)

use_current_action (boolean, (optional)) – Overwrite Current Action, Bake animation into current action, instead of creating a new one (useful for baking only part of bones in an armature)

clean_curves (boolean, (optional)) – Clean Curves, After baking curves, remove redundant keys

bake_types (enum set in {'POSE', 'OBJECT'}, (optional)) – Bake Data, Which data’s transformations to bake POSE Pose – Bake bones transformations. OBJECT Object – Bake object transformations.

Bake Data, Which data’s transformations to bake

POSE Pose – Bake bones transformations.

OBJECT Object – Bake object transformations.

channel_types (enum set in {'LOCATION', 'ROTATION', 'SCALE', 'BBONE', 'PROPS'}, (optional)) – Channels, Which channels to bake LOCATION Location – Bake location channels. ROTATION Rotation – Bake rotation channels. SCALE Scale – Bake scale channels. BBONE B-Bone – Bake B-Bone channels. PROPS Custom Properties – Bake custom properties.

Channels, Which channels to bake

LOCATION Location – Bake location channels.

ROTATION Rotation – Bake rotation channels.

SCALE Scale – Bake scale channels.

BBONE B-Bone – Bake B-Bone channels.

PROPS Custom Properties – Bake custom properties.

startup/bl_operators/anim.py:274

Handle clicks to select NLA tracks

extend (boolean, (optional)) – Extend Select

Reset scaling of selected strips

Handle clicks to select NLA Strips

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend Select

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

Delete selected strips

Duplicate selected NLA-Strips, adding the new strips to new track(s)

linked (boolean, (optional)) – Linked, When duplicating strips, assign new copies of the actions they use

Duplicate Linked selected NLA-Strips, adding the new strips to new track(s)

NLA_OT_duplicate (NLA_OT_duplicate, (optional)) – Duplicate Strips, Duplicate selected NLA-Strips, adding the new strips to new track(s)

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Duplicate selected NLA-Strips, adding the new strips to new track(s)

NLA_OT_duplicate (NLA_OT_duplicate, (optional)) – Duplicate Strips, Duplicate selected NLA-Strips, adding the new strips to new track(s)

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Add F-Modifier to the active/selected NLA-Strips

type (enum in Fmodifier Type Items, (optional)) – Type

only_active (boolean, (optional)) – Only Active, Only add a F-Modifier of the specified type to the active strip

Copy the F-Modifier(s) of the active NLA-Strip

Add copied F-Modifiers to the selected NLA-Strips

only_active (boolean, (optional)) – Only Active, Only paste F-Modifiers on active strip

replace (boolean, (optional)) – Replace Existing, Replace existing F-Modifiers, instead of just appending to the end of the existing list

Make linked action local to each strip

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Add new meta-strips incorporating the selected strips

Separate out the strips held by the selected meta-strips

Move selected strips down a track if there’s room

Move selected strips up a track if there’s room

Mute or un-mute selected strips

Set Preview Range based on extends of selected strips

Select or deselect all NLA-Strips

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Use box selection to grab NLA-Strips

axis_range (boolean, (optional)) – Axis Range

tweak (boolean, (optional)) – Tweak, Operator has been activated using a click-drag event

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select strips to the left or the right of the current frame

mode (enum in ['CHECK', 'LEFT', 'RIGHT'], (optional)) – Mode

extend (boolean, (optional)) – Extend Select

Make selected objects appear in NLA Editor by adding Animation Data

Move start of strips to specified time

type (enum in ['CFRA', 'NEAREST_FRAME', 'NEAREST_SECOND', 'NEAREST_MARKER'], (optional)) – Type

Add a strip for controlling when speaker plays its sound clip

Split selected strips at their midpoints

Swap order of selected strips within tracks

Add NLA-Tracks above/after the selected tracks

above_selected (boolean, (optional)) – Above Selected, Add a new NLA Track above every existing selected one

Delete selected NLA-Tracks and the strips they contain

Add a transition strip between two adjacent selected strips

Enter tweaking mode for the action referenced by the active strip to edit its keyframes

isolate_action (boolean, (optional)) – Isolate Action, Enable ‘solo’ on the NLA Track containing the active strip, to edit it without seeing the effects of the NLA stack

use_upper_stack_evaluation (boolean, (optional)) – Evaluate Upper Stack, In tweak mode, display the effects of the tracks above the tweak strip

Exit tweaking mode for the action referenced by the active strip

isolate_action (boolean, (optional)) – Isolate Action, Disable ‘solo’ on any of the NLA Tracks after exiting tweak mode to get things back to normal

Reset viewable area to show full strips range

Move the view to the current frame

Reset viewable area to show selected strips range

---

## Outliner Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.outliner.html

**Contents:**
- Outliner Operators¶

Change the active action used

action (enum in [], (optional)) – Action

Undocumented, consider contributing.

type (enum in ['CLEAR_ANIMDATA', 'SET_ACT', 'CLEAR_ACT', 'REFRESH_DRIVERS', 'CLEAR_DRIVERS'], (optional)) – Animation Operation CLEAR_ANIMDATA Clear Animation Data – Remove this animation data container. SET_ACT Set Action. CLEAR_ACT Unlink Action. REFRESH_DRIVERS Refresh Drivers. CLEAR_DRIVERS Clear Drivers.

CLEAR_ANIMDATA Clear Animation Data – Remove this animation data container.

CLEAR_ACT Unlink Action.

REFRESH_DRIVERS Refresh Drivers.

CLEAR_DRIVERS Clear Drivers.

Clear the search filter

Set a color tag for the selected collections

color (enum in Collection Color Items, (optional)) – Color Tag

Disable viewport display in the view layers

Do not render this collection

Drag to move to collection in Outliner

Recursively duplicate the collection, all its children, objects and object data

Recursively duplicate the collection, all its children and objects, with linked object data

Enable viewport display in the view layers

Render the collection

Include collection in the active view layer

Exclude collection from the active view layer

Hide the collection in this view layer

Hide all the objects and collections inside the collection

Delete selected collection hierarchies

Clear masking of collection in the active view layer

Mask collection in the active view layer

Clear collection contributing only indirectly in the view layer

Set collection to only contribute indirectly (through shadows and reflections) in the view layer

Instance selected collections to active scene

Hide all but this collection and its parents

extend (boolean, (optional)) – Extend, Extend current visible collections

Link selected collections to active scene

Add a new collection inside selected collection

nested (boolean, (optional)) – Nested, Add as child of selected collection

Deselect objects in collection

Select objects in collection

Show the collection in this view layer

Show all the objects and collections inside the collection

Undocumented, consider contributing.

type (enum in ['ENABLE', 'DISABLE', 'DELETE'], (optional)) – Constraint Operation

Undocumented, consider contributing.

type (enum in ['DEFAULT'], (optional)) – Data Operation

Copy or reorder modifiers, constraints, and effects

Delete selected objects and collections

hierarchy (boolean, (optional)) – Hierarchy, Delete child objects and collections

Add drivers to selected items

Delete drivers assigned to selected items

Expand/Collapse all items

Hide selected objects and collections

Update the item highlight based on the current mouse position

Copy the selected data-blocks to the internal clipboard

Delete the ID under cursor

Replace the active linked ID (and its dependencies if any) by another one, from the same or a different library

General data-block management operations

type (enum in ['UNLINK', 'LOCAL', 'SINGLE', 'DELETE', 'REMAP', 'COPY', 'PASTE', 'ADD_FAKE', 'CLEAR_FAKE', 'RENAME', 'SELECT_LINKED'], (optional)) – ID Data Operation UNLINK Unlink. LOCAL Make Local. SINGLE Make Single User. DELETE Delete. REMAP Remap Users – Make all users of selected data-blocks to use instead current (clicked) one. COPY Copy. PASTE Paste. ADD_FAKE Add Fake User – Ensure data-block gets saved even if it isn’t in use (e.g. for motion and material libraries). CLEAR_FAKE Clear Fake User. RENAME Rename. SELECT_LINKED Select Linked.

SINGLE Make Single User.

REMAP Remap Users – Make all users of selected data-blocks to use instead current (clicked) one.

ADD_FAKE Add Fake User – Ensure data-block gets saved even if it isn’t in use (e.g. for motion and material libraries).

CLEAR_FAKE Clear Fake User.

SELECT_LINKED Select Linked.

Paste data-blocks from the internal clipboard

Undocumented, consider contributing.

id_type (enum in Id Type Items, (optional)) – ID Type

old_id (enum in [], (optional)) – Old ID, Old ID to replace

new_id (enum in [], (optional)) – New ID, New ID to remap all selected IDs’ users to

Handle mouse clicks to select and activate items

extend (boolean, (optional)) – Extend, Extend selection for activation

extend_range (boolean, (optional)) – Extend Range, Select a range from active element

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

recurse (boolean, (optional)) – Recurse, Select objects recursively from active element

Drag and drop element to another place

Toggle whether item under cursor is enabled or closed

all (boolean, (optional)) – All, Close or open all items

Rename the active element

use_active (boolean, (optional)) – Use Active, Rename the active item, rather than the one the mouse is over

Add selected items (blue-gray rows) to active Keying Set

Remove selected items (blue-gray rows) from active Keying Set

Undocumented, consider contributing.

type (enum in ['DELETE', 'RELOCATE', 'RELOAD'], (optional)) – Library Operation DELETE Delete – Delete this library and all its items. RELOCATE Relocate – Select a new path for this library, and reload all its data. RELOAD Reload – Reload all data from this library.

DELETE Delete – Delete this library and all its items.

RELOCATE Relocate – Select a new path for this library, and reload all its data.

RELOAD Reload – Reload all data from this library.

Relocate the library under cursor

Create, reset or clear library override hierarchies

type (enum in ['OVERRIDE_LIBRARY_CREATE_HIERARCHY', 'OVERRIDE_LIBRARY_RESET', 'OVERRIDE_LIBRARY_CLEAR_SINGLE'], (optional)) – Library Override Operation OVERRIDE_LIBRARY_CREATE_HIERARCHY Make – Create a local override of the selected linked data-blocks, and their hierarchy of dependencies. OVERRIDE_LIBRARY_RESET Reset – Reset the selected local overrides to their linked references values. OVERRIDE_LIBRARY_CLEAR_SINGLE Clear – Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable.

Library Override Operation

OVERRIDE_LIBRARY_CREATE_HIERARCHY Make – Create a local override of the selected linked data-blocks, and their hierarchy of dependencies.

OVERRIDE_LIBRARY_RESET Reset – Reset the selected local overrides to their linked references values.

OVERRIDE_LIBRARY_CLEAR_SINGLE Clear – Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable.

selection_set (enum in ['SELECTED', 'CONTENT', 'SELECTED_AND_CONTENT'], (optional)) – Selection Set, Over which part of the tree items to apply the operation SELECTED Selected – Apply the operation over selected data-blocks only. CONTENT Content – Apply the operation over content of the selected items only (the data-blocks in their sub-tree). SELECTED_AND_CONTENT Selected & Content – Apply the operation over selected data-blocks and all their dependencies.

Selection Set, Over which part of the tree items to apply the operation

SELECTED Selected – Apply the operation over selected data-blocks only.

CONTENT Content – Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

SELECTED_AND_CONTENT Selected & Content – Apply the operation over selected data-blocks and all their dependencies.

Advanced operations over library override to help fix broken hierarchies

type (enum in ['OVERRIDE_LIBRARY_RESYNC_HIERARCHY', 'OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE', 'OVERRIDE_LIBRARY_DELETE_HIERARCHY'], (optional)) – Library Override Troubleshoot Operation OVERRIDE_LIBRARY_RESYNC_HIERARCHY Resync – Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies. OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE Resync Enforce – Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies, enforcing these hierarchies to match the linked data (i.e. ignoring existing overrides on data-blocks pointer properties). OVERRIDE_LIBRARY_DELETE_HIERARCHY Delete – Delete the selected local overrides (including their hierarchies of override dependencies) and relink their usages to the linked data-blocks.

Library Override Troubleshoot Operation

OVERRIDE_LIBRARY_RESYNC_HIERARCHY Resync – Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies.

OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE Resync Enforce – Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies, enforcing these hierarchies to match the linked data (i.e. ignoring existing overrides on data-blocks pointer properties).

OVERRIDE_LIBRARY_DELETE_HIERARCHY Delete – Delete the selected local overrides (including their hierarchies of override dependencies) and relink their usages to the linked data-blocks.

selection_set (enum in ['SELECTED', 'CONTENT', 'SELECTED_AND_CONTENT'], (optional)) – Selection Set, Over which part of the tree items to apply the operation SELECTED Selected – Apply the operation over selected data-blocks only. CONTENT Content – Apply the operation over content of the selected items only (the data-blocks in their sub-tree). SELECTED_AND_CONTENT Selected & Content – Apply the operation over selected data-blocks and all their dependencies.

Selection Set, Over which part of the tree items to apply the operation

SELECTED Selected – Apply the operation over selected data-blocks only.

CONTENT Content – Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

SELECTED_AND_CONTENT Selected & Content – Apply the operation over selected data-blocks and all their dependencies.

Drag material to object in Outliner

Undocumented, consider contributing.

type (enum in ['APPLY', 'DELETE', 'TOGVIS', 'TOGREN'], (optional)) – Modifier Operation

Undocumented, consider contributing.

type (enum in ['SELECT', 'DESELECT', 'SELECT_HIERARCHY', 'REMAP', 'RENAME'], (optional)) – Object Operation SELECT Select. DESELECT Deselect. SELECT_HIERARCHY Select Hierarchy. REMAP Remap Users – Make all users of selected data-blocks to use instead a new chosen one. RENAME Rename.

SELECT_HIERARCHY Select Hierarchy.

REMAP Remap Users – Make all users of selected data-blocks to use instead a new chosen one.

Context menu for item operations

Open a window to manage unused data

Clear all orphaned data-blocks without any users from the file

do_local_ids (boolean, (optional)) – Local Data-blocks, Include unused local data-blocks into deletion

do_linked_ids (boolean, (optional)) – Linked Data-blocks, Include unused linked data-blocks into deletion

do_recursive (boolean, (optional)) – Recursive Delete, Recursively check for indirectly unused data-blocks, ensuring that no orphaned data-blocks remain after execution

Drag to clear parent in Outliner

Drag to parent in Outliner

Drag object to scene in Outliner

Context menu for scene operations

type (enum in ['DELETE'], (optional)) – Scene Operation

Scroll page up or down

up (boolean, (optional)) – Up, Scroll up one page

Toggle the Outliner selection of items

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Use box selection to select tree elements

tweak (boolean, (optional)) – Tweak, Tweak gesture from empty space for box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Use walk navigation to select tree elements

direction (enum in ['UP', 'DOWN', 'LEFT', 'RIGHT'], (optional)) – Walk Direction, Select/Deselect element in this direction

extend (boolean, (optional)) – Extend, Extend selection on walk

toggle_all (boolean, (optional)) – Toggle All, Toggle open/close hierarchy

Open up the tree and adjust the view so that the active object is shown centered

Open all object entries and close all others

Expand/collapse all entries by one level

open (boolean, (optional)) – Open, Expand all entries one level deep

Start entering filter text

Unhide all objects and collections

---

## Node Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.node.html

**Contents:**
- Node Operators¶

Activate selected viewer node in compositor and geometry nodes

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

startup/bl_operators/node.py:633

Add a collection info node to the current node editor

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add a color node to the current node editor

color (float array of 4 items in [0, inf], (optional)) – Color, Source color

gamma (boolean, (optional)) – Gamma Corrected, The source color is gamma corrected

has_alpha (boolean, (optional)) – Has Alpha, The source color contains an Alpha component

Add a group node with an empty group

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

startup/bl_operators/node.py:534

Add a For Each Geometry Element zone that allows executing nodes e.g. for each vertex separately

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

startup/bl_operators/node.py:633

Add an existing node group to the current node editor

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

show_datablock_in_node (boolean, (optional)) – Show the data-block selector in the node

Add a node group asset to the active node tree

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

Add a Group Input node with selected sockets to the current node editor

socket_identifier (string, (optional, never None)) – Socket Identifier, Socket to include in the added group input/output node

panel_identifier (int in [-inf, inf], (optional)) – Panel Identifier, Panel from which to add sockets to the added group input/output node

Add a image/movie file as node to the current node editor

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add an import node to the node tree

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

Add a mask node to the current node editor

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add a material node to the current node editor

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add a node to the active tree

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

type (string, (optional, never None)) – Node Type, Node type

visible_output (string, (optional, never None)) – Output Name, If provided, all outputs that are named differently will be hidden

startup/bl_operators/node.py:419

Add an object info node to the current node editor

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add a repeat zone that allows executing nodes a dynamic number of times

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

startup/bl_operators/node.py:633

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

cursor (int in [0, inf], (optional)) – Cursor

Add simulation zone input and output nodes to the active tree

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

startup/bl_operators/node.py:633

Undocumented, consider contributing.

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

use_transform (boolean, (optional)) – Use Transform, Start transform operator after inserting the node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

input_node_type (string, (optional, never None)) – Input Node, Specifies the input node used by the created zone

output_node_type (string, (optional, never None)) – Output Node, Specifies the output node used by the created zone

add_default_geometry_link (boolean, (optional)) – Add Geometry Link, When enabled, create a link between geometry sockets in this zone

startup/bl_operators/node.py:633

Attach active node to a frame

Fit the background image to the view

Use mouse to sample background image

Zoom in/out the background image

factor (float in [0, 10], (optional)) – Factor

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Clear the boundaries for viewer operations

Copy the selected nodes to the internal clipboard

Paste nodes from the internal clipboard to the active node tree

offset (float array of 2 items in [-inf, inf], (optional)) – Location, The 2D view location for the center of the new nodes, or unchanged if not set

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Toggle collapsed nodes and hide unused sockets

startup/bl_operators/node.py:856

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Connect active node to the active output node of the node tree

run_in_geometry_nodes (boolean, (optional)) – Run in Geometry Nodes Editor

startup/bl_operators/connect_to_output.py:251

Add a new input layer to a Cryptomatte node

Remove layer from a Cryptomatte node

Deactivate selected viewer node in geometry nodes

Set the width based on the parent group node in the current context

Remove selected nodes

Remove nodes and reconnect nodes as if deletion was muted

Detach selected nodes from parents

Detach nodes, move and attach to frame

NODE_OT_detach (NODE_OT_detach, (optional)) – Detach Nodes, Detach selected nodes from parents

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

NODE_OT_attach (NODE_OT_attach, (optional)) – Attach Nodes, Attach active node to a frame

Duplicate selected nodes

keep_inputs (boolean, (optional)) – Keep Inputs, Keep the input links to duplicated nodes

linked (boolean, (optional)) – Linked, Duplicate node but not node trees, linking to the original data

Duplicate the currently assigned compositing node group.

Duplicate selected nodes and move them

NODE_OT_duplicate (NODE_OT_duplicate, (optional)) – Duplicate Nodes, Duplicate selected nodes

NODE_OT_translate_attach (NODE_OT_translate_attach, (optional)) – Move and Attach, Move nodes and attach to frame

Duplicate selected nodes keeping input links and move them

NODE_OT_duplicate (NODE_OT_duplicate, (optional)) – Duplicate Nodes, Duplicate selected nodes

NODE_OT_translate_attach (NODE_OT_translate_attach, (optional)) – Move and Attach, Move nodes and attach to frame

Duplicate selected nodes, but not their node trees, and move them

NODE_OT_duplicate (NODE_OT_duplicate, (optional)) – Duplicate Nodes, Duplicate selected nodes

NODE_OT_translate_attach (NODE_OT_translate_attach, (optional)) – Move and Attach, Move nodes and attach to frame

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Search for a node by name and focus and select it

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Add a node to the active tree for glTF export

addons_core/io_scene_gltf2/blender/com/gltf2_blender_ui.py:34

exit (boolean, (optional)) – Exit

Enter or exit node group based on cursor location

Insert selected nodes into a node group

Make group from selected nodes

Separate selected nodes from the node group

type (enum in ['COPY', 'MOVE'], (optional)) – Type COPY Copy – Copy to parent node tree, keep group intact. MOVE Move – Move to parent node tree, remove from group.

COPY Copy – Copy to parent node tree, keep group intact.

MOVE Move – Move to parent node tree, remove from group.

Ungroup selected nodes

Toggle unused node socket display

Toggle collapsing of selected nodes

Add an item to the index switch

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Remove an item from the index switch

index (int in [0, inf], (optional)) – Index, Index to remove

Automatically offset nodes on insertion

Add a copy of the active item to the interface

startup/bl_operators/node.py:1042

Make the active boolean socket a toggle for its parent panel

startup/bl_operators/node.py:1118

Add a new item to the interface

item_type (enum in ['INPUT', 'OUTPUT', 'PANEL'], (optional)) – Item Type, Type of the item to create

startup/bl_operators/node.py:948

Add a checkbox to the currently selected panel

startup/bl_operators/node.py:1013

Remove active item from the interface

startup/bl_operators/node.py:1061

Make the panel toggle a stand-alone socket

startup/bl_operators/node.py:1166

Attach selected nodes to a new common frame

Create a new frame node around the selected nodes and name it immediately

NODE_OT_join (NODE_OT_join, (optional)) – Join Nodes in Frame, Attach selected nodes to a new common frame

WM_OT_call_panel (WM_OT_call_panel, (optional)) – Call Panel, Open a predefined panel

Merge selected group input nodes into one if possible

Use the mouse to create a link between two nodes

detach (boolean, (optional)) – Detach, Detach and redirect existing links

drag_start (float array of 2 items in [-6, 6], (optional)) – Drag Start, The position of the mouse cursor at the start of the operation

inside_padding (float in [0, 100], (optional)) – Inside Padding, Inside distance in UI units from the edge of the region within which to start panning

outside_padding (float in [0, 100], (optional)) – Outside Padding, Outside distance in UI units from the edge of the region at which to stop panning

speed_ramp (float in [0, 100], (optional)) – Speed Ramp, Width of the zone in UI units where speed increases with distance from the edge

max_speed (float in [0, 10000], (optional)) – Max Speed, Maximum speed in UI units per second

delay (float in [0, 10], (optional)) – Delay, Delay in seconds before maximum speed is reached

zoom_influence (float in [0, 1], (optional)) – Zoom Influence, Influence of the zoom factor on scroll speed

Make a link between selected output and input sockets

replace (boolean, (optional)) – Replace, Replace socket connections with the new links

Use the mouse to cut (remove) some links

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

cursor (int in [0, inf], (optional)) – Cursor

Remove all links to selected nodes, and try to connect neighbor nodes together

Use the mouse to mute links

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

cursor (int in [0, inf], (optional)) – Cursor

Move a node to detach links

NODE_OT_links_detach (NODE_OT_links_detach, (optional)) – Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Move a node to detach links

NODE_OT_links_detach (NODE_OT_links_detach, (optional)) – Detach Links, Remove all links to selected nodes, and try to connect neighbor nodes together

NODE_OT_translate_attach (NODE_OT_translate_attach, (optional)) – Move and Attach, Move nodes and attach to frame

Toggle muting of selected nodes

Create a new compositing node group and initialize it with default nodes

name (string, (optional, never None)) – Name

Create a new compositor node group for sequencer

name (string, (optional, never None)) – Name

Create a new geometry node group and assign it to the active modifier

startup/bl_operators/geometry_nodes.py:340

Create a new geometry node group for a tool

startup/bl_operators/geometry_nodes.py:361

Create a new modifier with a new geometry node group

startup/bl_operators/geometry_nodes.py:317

Create a new node tree

type (enum in [], (optional)) – Tree Type

name (string, (optional, never None)) – Name

Add or remove a Node Color Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Copy color to all selected nodes

Toggle option buttons display for selected nodes

Attach selected nodes

Toggle preview display for selected nodes

Read all render layers of all used scenes

Render current scene, when input node’s layer has been changed

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Select the node under the cursor

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

socket_select (boolean, (optional)) – Socket Select

clear_viewer (boolean, (optional)) – Clear Viewer, Deactivate geometry nodes viewer when clicking in empty space

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Use box selection to select nodes

tweak (boolean, (optional)) – Tweak, Only activate when mouse is not over a node (useful for tweak gesture)

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Use circle selection to select nodes

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select nodes with similar properties

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

type (enum in ['TYPE', 'COLOR', 'PREFIX', 'SUFFIX'], (optional)) – Type

Select nodes using lasso selection

tweak (boolean, (optional)) – Tweak, Only activate when mouse is not over a node (useful for tweak gesture)

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select node and link it to a viewer node

NODE_OT_select (NODE_OT_select, (optional)) – Select, Select the node under the cursor

NODE_OT_link_viewer (NODE_OT_link_viewer, (optional)) – Link to Viewer Node, Link to viewer node

Select nodes linked from the selected ones

Select nodes linked to the selected ones

Activate and view same node type, step by step

prev (boolean, (optional)) – Previous

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Update shader script node with new sockets and options from the script

Add item below active item

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Move direction

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

node_identifier (int in [0, inf], (optional)) – Node Identifier, Optional identifier of the node to operate on

Update sockets to match what is actually used

node_name (string, (optional, never None)) – Node Name

Replace active node with an empty group

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

startup/bl_operators/node.py:570

Swap selected nodes with the specified node group asset

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

Replace the selected nodes with the specified type

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

type (string, (optional, never None)) – Node Type, Node type

visible_output (string, (optional, never None)) – Output Name, If provided, all outputs that are named differently will be hidden

startup/bl_operators/node.py:464

Undocumented, consider contributing.

settings (bpy_prop_collection of NodeSetting, (optional)) – Settings, Settings to be applied on the newly created node

offset (float array of 2 items in [-inf, inf], (optional)) – Offset, Offset of nodes from the cursor when added

input_node_type (string, (optional, never None)) – Input Node, Specifies the input node used by the created zone

output_node_type (string, (optional, never None)) – Output Node, Specifies the output node used by the created zone

add_default_geometry_link (boolean, (optional)) – Add Geometry Link, When enabled, create a link between geometry sockets in this zone

startup/bl_operators/node.py:720

Create a new inlined shader node tree as is consumed by renderers

Toggle selected viewer node in compositor and geometry nodes

Move nodes and attach to frame

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

NODE_OT_attach (NODE_OT_attach, (optional)) – Attach Nodes, Attach active node to a frame

Move nodes and attach to frame

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

NODE_OT_attach (NODE_OT_attach, (optional)) – Attach Nodes, Attach active node to a frame

Go to parent node tree

parent_tree_index (int in [-inf, inf], (optional)) – Parent Index, Parent index in context path

startup/bl_operators/node.py:892

Resize view so you can see all nodes

Resize view so you can see selected nodes

Set the boundaries for viewer operations

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Toggle a specific viewer node using 1,2,..,9 keys

viewer_index (int in [-inf, inf], (optional)) – Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc..

startup/bl_operators/node.py:1280

Create a viewer shortcut for the selected node by pressing ctrl+1,2,..9

viewer_index (int in [-inf, inf], (optional)) – Viewer Index, Index corresponding to the shortcut, e.g. number key 1 corresponds to index 1 etc..

startup/bl_operators/node.py:1220

---

## Object Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.object.html

**Contents:**
- Object Operators¶

Add an object to the scene

radius (float in [0, inf], (optional)) – Radius

type (enum in Object Type Items, (optional)) – Type

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Undocumented, consider contributing.

startup/bl_ui/properties_data_modifier.py:303

linked (boolean, (optional)) – Linked, Duplicate object but not object data, linking to the original data

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – Matrix

drop_x (int in [-inf, inf], (optional)) – Drop X, X-coordinate (screen space) to place the new object under

drop_y (int in [-inf, inf], (optional)) – Drop Y, Y-coordinate (screen space) to place the new object under

bb_quality (boolean, (optional)) – High Quality, Enables high quality but slow calculation of the bounding box for perfect results on complex shape meshes with rotation/scale

align_mode (enum in ['OPT_1', 'OPT_2', 'OPT_3'], (optional)) – Align Mode, Side of object to use for alignment

relative_to (enum in ['OPT_1', 'OPT_2', 'OPT_3', 'OPT_4'], (optional)) – Relative To, Reference location to align to OPT_1 Scene Origin – Use the scene origin as the position for the selected objects to align to. OPT_2 3D Cursor – Use the 3D cursor as the position for the selected objects to align to. OPT_3 Selection – Use the selected objects as the position for the selected objects to align to. OPT_4 Active – Use the active object as the position for the selected objects to align to.

Relative To, Reference location to align to

OPT_1 Scene Origin – Use the scene origin as the position for the selected objects to align to.

OPT_2 3D Cursor – Use the 3D cursor as the position for the selected objects to align to.

OPT_3 Selection – Use the selected objects as the position for the selected objects to align to.

OPT_4 Active – Use the active object as the position for the selected objects to align to.

align_axis (enum set in {'X', 'Y', 'Z'}, (optional)) – Align, Align to axis

startup/bl_operators/object_align.py:386

Convert object animation for normal transforms to delta transforms

startup/bl_operators/object.py:822

Add an armature object to the scene

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Assign the current values of custom properties as their defaults, for use as part of the rest pose state in NLA track mixing

process_data (boolean, (optional)) – Process data properties

process_bones (boolean, (optional)) – Process bone properties

startup/bl_operators/object.py:979

Bake image textures of selected objects

type (enum in Bake Pass Type Items, (optional)) – Type, Type of pass to bake, some of them may not be supported by the current render engine

pass_filter (enum set in Bake Pass Filter Type Items, (optional)) – Pass Filter, Filter to combined, diffuse, glossy, transmission and subsurface passes

filepath (string, (optional, never None)) – File Path, Image filepath to use when saving externally

width (int in [1, inf], (optional)) – Width, Horizontal dimension of the baking map (external only)

height (int in [1, inf], (optional)) – Height, Vertical dimension of the baking map (external only)

margin (int in [0, inf], (optional)) – Margin, Extends the baked result as a post process filter

margin_type (enum in Bake Margin Type Items, (optional)) – Margin Type, Which algorithm to use to generate the margin

use_selected_to_active (boolean, (optional)) – Selected to Active, Bake shading on the surface of selected objects to the active object

max_ray_distance (float in [0, inf], (optional)) – Max Ray Distance, The maximum ray distance for matching points between the active and selected objects. If zero, there is no limit

cage_extrusion (float in [0, inf], (optional)) – Cage Extrusion, Inflate the active object by the specified distance for baking. This helps matching to points nearer to the outside of the selected object meshes

cage_object (string, (optional, never None)) – Cage Object, Object to use as cage, instead of calculating the cage from the active object with cage extrusion

normal_space (enum in Normal Space Items, (optional)) – Normal Space, Choose normal space for baking

normal_r (enum in Normal Swizzle Items, (optional)) – R, Axis to bake in red channel

normal_g (enum in Normal Swizzle Items, (optional)) – G, Axis to bake in green channel

normal_b (enum in Normal Swizzle Items, (optional)) – B, Axis to bake in blue channel

target (enum in Bake Target Items, (optional)) – Target, Where to output the baked map

save_mode (enum in Bake Save Mode Items, (optional)) – Save Mode, Where to save baked image textures

use_clear (boolean, (optional)) – Clear, Clear images before baking (only for internal saving)

use_cage (boolean, (optional)) – Cage, Cast rays to active object from a cage

use_split_materials (boolean, (optional)) – Split Materials, Split baked maps per material, using material name in output file (external only)

use_automatic_name (boolean, (optional)) – Automatic Name, Automatically name the output file with the pass type

uv_layer (string, (optional, never None)) – UV Layer, UV layer to override active

Bake image textures of selected objects

Add a camera object to the scene

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Update custom camera with new parameters from the shader

Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable

Add an object to a new collection

Add the dragged collection to the scene

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

use_instance (boolean, (optional)) – Instance, Add the dropped collection as collection instance

drop_x (int in [-inf, inf], (optional)) – Drop X, X-coordinate (screen space) to place the new object under

drop_y (int in [-inf, inf], (optional)) – Drop Y, Y-coordinate (screen space) to place the new object under

collection (enum in [], (optional)) – Collection

Add a collection instance

name (string, (optional, never None)) – Name, Collection name to add

collection (enum in [], (optional)) – Collection

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

drop_x (int in [-inf, inf], (optional)) – Drop X, X-coordinate (screen space) to place the new object under

drop_y (int in [-inf, inf], (optional)) – Drop Y, Y-coordinate (screen space) to place the new object under

Add an object to an existing collection

collection (enum in [], (optional)) – Collection

Select all objects in collection

Remove the active object from this collection

Unlink the collection from all objects

Add a constraint to the active object

type (enum in [], (optional)) – Type

Add a constraint to the active object, with target (where applicable) set to the selected objects/bones

type (enum in [], (optional)) – Type

Clear all constraints from the selected objects

Copy constraints to other selected objects

Convert selected objects to another type

target (enum in ['CURVE', 'MESH', 'POINTCLOUD', 'CURVES', 'GREASEPENCIL'], (optional)) – Target, Type of object to convert to CURVE Curve – Curve from Mesh or Text objects. MESH Mesh – Mesh from Curve, Surface, Metaball, Text, or Point Cloud objects. POINTCLOUD Point Cloud – Point Cloud from Mesh objects. CURVES Curves – Curves from evaluated curve data. GREASEPENCIL Grease Pencil – Grease Pencil from Curve or Mesh objects.

Target, Type of object to convert to

CURVE Curve – Curve from Mesh or Text objects.

MESH Mesh – Mesh from Curve, Surface, Metaball, Text, or Point Cloud objects.

POINTCLOUD Point Cloud – Point Cloud from Mesh objects.

CURVES Curves – Curves from evaluated curve data.

GREASEPENCIL Grease Pencil – Grease Pencil from Curve or Mesh objects.

keep_original (boolean, (optional)) – Keep Original, Keep original objects instead of replacing them

merge_customdata (boolean, (optional)) – Merge UVs, Merge UV coordinates that share a vertex to account for imprecision in some modifiers

thickness (int in [1, 100], (optional)) – Thickness

faces (boolean, (optional)) – Export Faces, Export faces as filled strokes

offset (float in [0, inf], (optional)) – Stroke Offset, Offset strokes from fill

Copies the matrix of the currently active object or pose bone to the clipboard. Uses world-space matrices

startup/bl_operators/copy_global_transform.py:150

Copies the matrix of the currently active object or pose bone to the clipboard. Uses matrices relative to a specific object or the active scene camera

startup/bl_operators/copy_global_transform.py:180

Bind base pose in Corrective Smooth modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Add an empty curve object to the scene with the selected mesh as surface

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add a curves object with random curves to the scene

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add an object data instance

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

type (enum in Id Type Items, (optional)) – Type

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

drop_x (int in [-inf, inf], (optional)) – Drop X, X-coordinate (screen space) to place the new object under

drop_y (int in [-inf, inf], (optional)) – Drop Y, Y-coordinate (screen space) to place the new object under

Transfer data layer(s) (weights, edge sharp, etc.) from active to selected meshes

use_reverse_transfer (boolean, (optional)) – Reverse Transfer, Transfer from selected objects to active one

use_freeze (boolean, (optional)) – Freeze Operator, Prevent changes to settings to re-run the operator, handy to change several things at once with heavy geometry

data_type (enum in ['VGROUP_WEIGHTS', 'BEVEL_WEIGHT_VERT', 'COLOR_VERTEX', 'SHARP_EDGE', 'SEAM', 'CREASE', 'BEVEL_WEIGHT_EDGE', 'FREESTYLE_EDGE', 'CUSTOM_NORMAL', 'COLOR_CORNER', 'UV', 'SMOOTH', 'FREESTYLE_FACE'], (optional)) – Data Type, Which data to transfer VGROUP_WEIGHTS Vertex Group(s) – Transfer active or all vertex groups. BEVEL_WEIGHT_VERT Bevel Weight – Transfer bevel weights. COLOR_VERTEX Colors – Color Attributes. SHARP_EDGE Sharp – Transfer sharp mark. SEAM UV Seam – Transfer UV seam mark. CREASE Subdivision Crease – Transfer crease values. BEVEL_WEIGHT_EDGE Bevel Weight – Transfer bevel weights. FREESTYLE_EDGE Freestyle Mark – Transfer Freestyle edge mark. CUSTOM_NORMAL Custom Normals – Transfer custom normals. COLOR_CORNER Colors – Color Attributes. UV UVs – Transfer UV layers. SMOOTH Smooth – Transfer flat/smooth mark. FREESTYLE_FACE Freestyle Mark – Transfer Freestyle face mark.

Data Type, Which data to transfer

VGROUP_WEIGHTS Vertex Group(s) – Transfer active or all vertex groups.

BEVEL_WEIGHT_VERT Bevel Weight – Transfer bevel weights.

COLOR_VERTEX Colors – Color Attributes.

SHARP_EDGE Sharp – Transfer sharp mark.

SEAM UV Seam – Transfer UV seam mark.

CREASE Subdivision Crease – Transfer crease values.

BEVEL_WEIGHT_EDGE Bevel Weight – Transfer bevel weights.

FREESTYLE_EDGE Freestyle Mark – Transfer Freestyle edge mark.

CUSTOM_NORMAL Custom Normals – Transfer custom normals.

COLOR_CORNER Colors – Color Attributes.

UV UVs – Transfer UV layers.

SMOOTH Smooth – Transfer flat/smooth mark.

FREESTYLE_FACE Freestyle Mark – Transfer Freestyle face mark.

use_create (boolean, (optional)) – Create Data, Add data layers on destination meshes if needed

vert_mapping (enum in Dt Method Vertex Items, (optional)) – Vertex Mapping, Method used to map source vertices to destination ones

edge_mapping (enum in Dt Method Edge Items, (optional)) – Edge Mapping, Method used to map source edges to destination ones

loop_mapping (enum in Dt Method Loop Items, (optional)) – Face Corner Mapping, Method used to map source faces’ corners to destination ones

poly_mapping (enum in Dt Method Poly Items, (optional)) – Face Mapping, Method used to map source faces to destination ones

use_auto_transform (boolean, (optional)) – Auto Transform, Automatically compute transformation to get the best possible match between source and destination meshes.Warning: Results will never be as good as manual matching of objects

use_object_transform (boolean, (optional)) – Object Transform, Evaluate source and destination meshes in global space

use_max_distance (boolean, (optional)) – Only Neighbor Geometry, Source elements must be closer than given distance from destination one

max_distance (float in [0, inf], (optional)) – Max Distance, Maximum allowed distance between source and destination element, for non-topology mappings

ray_radius (float in [0, inf], (optional)) – Ray Radius, ‘Width’ of rays (especially useful when raycasting against vertices or edges)

islands_precision (float in [0, 10], (optional)) – Islands Precision, Factor controlling precision of islands handling (the higher, the better the results)

layers_select_src (enum in Dt Layers Select Src Items, (optional)) – Source Layers Selection, Which layers to transfer, in case of multi-layers types

layers_select_dst (enum in Dt Layers Select Dst Items, (optional)) – Destination Layers Matching, How to match source and destination layers

mix_mode (enum in Dt Mix Mode Items, (optional)) – Mix Mode, How to affect destination elements with source values

mix_factor (float in [0, 1], (optional)) – Mix Factor, Factor to use when applying data to destination (exact behavior depends on mix mode)

Transfer layout of data layer(s) from active to selected meshes

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

data_type (enum in ['VGROUP_WEIGHTS', 'BEVEL_WEIGHT_VERT', 'COLOR_VERTEX', 'SHARP_EDGE', 'SEAM', 'CREASE', 'BEVEL_WEIGHT_EDGE', 'FREESTYLE_EDGE', 'CUSTOM_NORMAL', 'COLOR_CORNER', 'UV', 'SMOOTH', 'FREESTYLE_FACE'], (optional)) – Data Type, Which data to transfer VGROUP_WEIGHTS Vertex Group(s) – Transfer active or all vertex groups. BEVEL_WEIGHT_VERT Bevel Weight – Transfer bevel weights. COLOR_VERTEX Colors – Color Attributes. SHARP_EDGE Sharp – Transfer sharp mark. SEAM UV Seam – Transfer UV seam mark. CREASE Subdivision Crease – Transfer crease values. BEVEL_WEIGHT_EDGE Bevel Weight – Transfer bevel weights. FREESTYLE_EDGE Freestyle Mark – Transfer Freestyle edge mark. CUSTOM_NORMAL Custom Normals – Transfer custom normals. COLOR_CORNER Colors – Color Attributes. UV UVs – Transfer UV layers. SMOOTH Smooth – Transfer flat/smooth mark. FREESTYLE_FACE Freestyle Mark – Transfer Freestyle face mark.

Data Type, Which data to transfer

VGROUP_WEIGHTS Vertex Group(s) – Transfer active or all vertex groups.

BEVEL_WEIGHT_VERT Bevel Weight – Transfer bevel weights.

COLOR_VERTEX Colors – Color Attributes.

SHARP_EDGE Sharp – Transfer sharp mark.

SEAM UV Seam – Transfer UV seam mark.

CREASE Subdivision Crease – Transfer crease values.

BEVEL_WEIGHT_EDGE Bevel Weight – Transfer bevel weights.

FREESTYLE_EDGE Freestyle Mark – Transfer Freestyle edge mark.

CUSTOM_NORMAL Custom Normals – Transfer custom normals.

COLOR_CORNER Colors – Color Attributes.

UV UVs – Transfer UV layers.

SMOOTH Smooth – Transfer flat/smooth mark.

FREESTYLE_FACE Freestyle Mark – Transfer Freestyle face mark.

use_delete (boolean, (optional)) – Exact Match, Also delete some data layers from destination if necessary, so that it matches exactly source

layers_select_src (enum in Dt Layers Select Src Items, (optional)) – Source Layers Selection, Which layers to transfer, in case of multi-layers types

layers_select_dst (enum in Dt Layers Select Dst Items, (optional)) – Destination Layers Matching, How to match source and destination layers

Delete selected objects

use_global (boolean, (optional)) – Delete Globally, Remove object from all scenes

confirm (boolean, (optional)) – Confirm, Prompt for confirmation

Delete all keys that were generated by the ‘Fix to Scene Camera’ operator

startup/bl_operators/copy_global_transform.py:639

Undocumented, consider contributing.

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the geometry node group being dropped

show_datablock_in_modifier (boolean, (optional)) – Show the data-block selector in the modifier

Undocumented, consider contributing.

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Duplicate selected objects

linked (boolean, (optional)) – Linked, Duplicate object but not object data, linking to the original data

mode (enum in Transform Mode Type Items, (optional)) – Mode

Duplicate the selected objects and move them

OBJECT_OT_duplicate (OBJECT_OT_duplicate, (optional)) – Duplicate Objects, Duplicate selected objects

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Duplicate the selected objects, but not their object data, and move them

OBJECT_OT_duplicate (OBJECT_OT_duplicate, (optional)) – Duplicate Objects, Duplicate selected objects

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Make instanced objects attached to this object real

use_base_parent (boolean, (optional)) – Parent, Parent newly created objects to the original instancer

use_hierarchy (boolean, (optional)) – Keep Hierarchy, Maintain parent child relationships

Toggle object’s edit mode

Add an empty object with a physics effector to the scene

type (enum in ['FORCE', 'WIND', 'VORTEX', 'MAGNET', 'HARMONIC', 'CHARGE', 'LENNARDJ', 'TEXTURE', 'GUIDE', 'BOID', 'TURBULENCE', 'DRAG', 'FLUID'], (optional)) – Type

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add an empty object to the scene

type (enum in Object Empty Drawtype Items, (optional)) – Type

radius (float in [0, inf], (optional)) – Radius

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add an empty image type to scene with data

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

background (boolean, (optional)) – Put in Background, Make the image render behind all objects

Refresh data in the Explode modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Generate new keys to fix the selected object/bone to the camera on unkeyed frames

use_location (boolean, (optional)) – Location, Create Location keys when fixing to the scene camera

use_rotation (boolean, (optional)) – Rotation, Create Rotation keys when fixing to the scene camera

use_scale (boolean, (optional)) – Scale, Create Scale keys when fixing to the scene camera

startup/bl_operators/copy_global_transform.py:639

Toggle object’s force field

Delete baked data of a single bake node or simulation

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

modifier_name (string, (optional, never None)) – Modifier Name, Name of the modifier that contains the node

bake_id (int in [0, inf], (optional)) – Bake ID, Nested node id of the node

Pack baked data from disk into the .blend file

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

modifier_name (string, (optional, never None)) – Modifier Name, Name of the modifier that contains the node

bake_id (int in [0, inf], (optional)) – Bake ID, Nested node id of the node

Bake a single bake node or simulation

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

modifier_name (string, (optional, never None)) – Modifier Name, Name of the modifier that contains the node

bake_id (int in [0, inf], (optional)) – Bake ID, Nested node id of the node

Unpack baked data from the .blend file to disk

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

modifier_name (string, (optional, never None)) – Modifier Name, Name of the modifier that contains the node

bake_id (int in [0, inf], (optional)) – Bake ID, Nested node id of the node

method (enum in ['USE_LOCAL', 'WRITE_LOCAL', 'USE_ORIGINAL', 'WRITE_ORIGINAL'], (optional)) – Method, How to unpack

Duplicate the active geometry node group and assign it to the active modifier

Switch between an attribute and a single value to define the data for every element

input_name (string, (optional, never None)) – Input Name

modifier_name (string, (optional, never None)) – Modifier Name

Move inputs and outputs from in the modifier to a new node group

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

startup/bl_operators/geometry_nodes.py:280

Add a Grease Pencil object to the scene

type (enum in Object Gpencil Type Items, (optional)) – Type

use_in_front (boolean, (optional)) – Show In Front, Show Line Art Grease Pencil in front of everything

stroke_depth_offset (float in [0, inf], (optional)) – Stroke Offset, Stroke offset for the Line Art modifier

use_lights (boolean, (optional)) – Use Lights, Use lights for this Grease Pencil object

stroke_depth_order (enum in ['2D', '3D'], (optional)) – Stroke Depth Order, Defines how the strokes are ordered in 3D space (for objects not displayed ‘In Front’) 2D 2D Layers – Display strokes using Grease Pencil layers to define order. 3D 3D Location – Display strokes using real 3D position in 3D space.

Stroke Depth Order, Defines how the strokes are ordered in 3D space (for objects not displayed ‘In Front’)

2D 2D Layers – Display strokes using Grease Pencil layers to define order.

3D 3D Location – Display strokes using real 3D position in 3D space.

radius (float in [0, inf], (optional)) – Radius

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add a segment to the dash modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Move the active dash segment up or down

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

type (enum in ['UP', 'DOWN'], (optional)) – Type

Remove the active segment from the dash modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

index (int in [0, inf], (optional)) – Index, Index of the segment to remove

Add a segment to the time modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Move the active time segment up or down

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

type (enum in ['UP', 'DOWN'], (optional)) – Type

Remove the active segment from the time modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

index (int in [0, inf], (optional)) – Index, Index of the segment to remove

Show only objects in collection (Shift to extend)

collection_index (int in [-1, inf], (optional)) – Collection Index, Index of the collection to change visibility

toggle (boolean, (optional)) – Toggle, Toggle visibility

extend (boolean, (optional)) – Extend, Extend visibility

Reveal all render objects by setting the hide render flag

startup/bl_operators/object.py:729

Reveal temporarily hidden objects

select (boolean, (optional)) – Select, Select revealed objects

Temporarily hide objects from the viewport

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected objects

Hook selected vertices to a newly created object

Hook selected vertices to the first selected object

use_bone (boolean, (optional)) – Active Bone, Assign the hook to the hook object’s active bone

Assign the selected vertices to a hook

modifier (enum in [], (optional)) – Modifier, Modifier number to assign to

Set hook center to cursor position

modifier (enum in [], (optional)) – Modifier, Modifier number to assign to

Remove a hook from the active object

modifier (enum in [], (optional)) – Modifier, Modifier number to remove

Recalculate and clear offset transformation

modifier (enum in [], (optional)) – Modifier, Modifier number to assign to

Select affected vertices on mesh

modifier (enum in [], (optional)) – Modifier, Modifier number to remove

Set offset used for collection instances based on cursor position

startup/bl_operators/object.py:914

Set offset used for collection instances based on the active object position

startup/bl_operators/object.py:946

Set cursor position to the offset used for collection instances

startup/bl_operators/object.py:929

Hide unselected render objects of same type as active by setting the hide render flag

startup/bl_operators/object.py:709

Join selected objects into active object

Add the vertex positions of selected objects as shape keys or update existing shape keys with matching names

use_mirror (boolean, (optional)) – Mirror, Mirror the new shape key values

Transfer UV Maps from active to selected objects (needs matching geometry)

startup/bl_operators/object.py:610

Bind mesh to system in laplacian deform modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Add a lattice and use it to deform selected objects

fit_to_selected (boolean, (optional)) – Fit to Selected, Resize lattice to fit selected deformable objects

radius (float in [0, inf], (optional)) – Radius

margin (float in [0, inf], (optional)) – Margin, Add margin to lattice dimensions

add_modifiers (boolean, (optional)) – Add Modifiers, Automatically add lattice modifiers to selected objects

resolution_u (int in [1, 64], (optional)) – Resolution U, Lattice resolution in U direction

resolution_v (int in [1, 64], (optional)) – V, Lattice resolution in V direction

resolution_w (int in [1, 64], (optional)) – W, Lattice resolution in W direction

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Add a light object to the scene

type (enum in Light Type Items, (optional)) – Type

radius (float in [0, inf], (optional)) – Radius

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Create new light linking collection used by the active emitter

Light link selected blockers to the active emitter object

link_state (enum in ['INCLUDE', 'EXCLUDE'], (optional)) – Link State, State of the shadow linking INCLUDE Include – Include selected blockers to cast shadows from the active emitter. EXCLUDE Exclude – Exclude selected blockers from casting shadows from the active emitter.

Link State, State of the shadow linking

INCLUDE Include – Include selected blockers to cast shadows from the active emitter.

EXCLUDE Exclude – Exclude selected blockers from casting shadows from the active emitter.

Select all objects which block light from this emitter

Create new light linking collection used by the active emitter

Light link selected receivers to the active emitter object

link_state (enum in ['INCLUDE', 'EXCLUDE'], (optional)) – Link State, State of the light linking INCLUDE Include – Include selected receivers to receive light from the active emitter. EXCLUDE Exclude – Exclude selected receivers from receiving light from the active emitter.

Link State, State of the light linking

INCLUDE Include – Include selected receivers to receive light from the active emitter.

EXCLUDE Exclude – Exclude selected receivers from receiving light from the active emitter.

Select all objects which receive light from this emitter

Remove this object or collection from the light linking collection

Add a light probe object

type (enum in ['SPHERE', 'PLANE', 'VOLUME'], (optional)) – Type SPHERE Sphere – Light probe that captures precise lighting from all directions at a single point in space. PLANE Plane – Light probe that captures incoming light from a single direction on a plane. VOLUME Volume – Light probe that captures low frequency lighting inside a volume.

SPHERE Sphere – Light probe that captures precise lighting from all directions at a single point in space.

PLANE Plane – Light probe that captures incoming light from a single direction on a plane.

VOLUME Volume – Light probe that captures low frequency lighting inside a volume.

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Bake irradiance volume light cache

subset (enum in ['ALL', 'SELECTED', 'ACTIVE'], (optional)) – Subset, Subset of probes to update ALL All Volumes – Bake all light probe volumes. SELECTED Selected Only – Only bake selected light probe volumes. ACTIVE Active Only – Only bake the active light probe volume.

Subset, Subset of probes to update

ALL All Volumes – Bake all light probe volumes.

SELECTED Selected Only – Only bake selected light probe volumes.

ACTIVE Active Only – Only bake the active light probe volume.

Delete cached indirect lighting

subset (enum in ['ALL', 'SELECTED', 'ACTIVE'], (optional)) – Subset, Subset of probes to update ALL All Light Probes – Delete all light probes’ baked lighting data. SELECTED Selected Only – Only delete selected light probes’ baked lighting data. ACTIVE Active Only – Only delete the active light probe’s baked lighting data.

Subset, Subset of probes to update

ALL All Light Probes – Delete all light probes’ baked lighting data.

SELECTED Selected Only – Only delete selected light probes’ baked lighting data.

ACTIVE Active Only – Only delete the active light probe’s baked lighting data.

Bake Line Art for current Grease Pencil object

bake_all (boolean, (optional)) – Bake All, Bake all Line Art modifiers

Clear all strokes in current Grease Pencil object

clear_all (boolean, (optional)) – Clear All, Clear all Line Art modifier bakes

Link objects to a collection

collection_uid (int in [-1, inf], (optional)) – Collection UID, Session UID of the collection to link to

is_new (boolean, (optional)) – New, Link objects to a new collection

new_collection_name (string, (optional, never None)) – Name, Name of the newly added collection

Clear the object’s location

clear_delta (boolean, (optional)) – Clear Delta, Clear delta location in addition to clearing the normal location transform

Convert objects into instanced faces

startup/bl_operators/object.py:692

Transfer data from active object to selected objects

type (enum in ['OBDATA', 'MATERIAL', 'ANIMATION', 'GROUPS', 'DUPLICOLLECTION', 'FONTS', 'MODIFIERS', 'EFFECTS'], (optional)) – Type OBDATA Link Object Data – Replace assigned Object Data. MATERIAL Link Materials – Replace assigned Materials. ANIMATION Link Animation Data – Replace assigned Animation Data. GROUPS Link Collections – Replace assigned Collections. DUPLICOLLECTION Link Instance Collection – Replace assigned Collection Instance. FONTS Link Fonts to Text – Replace Text object Fonts. MODIFIERS Copy Modifiers – Replace Modifiers. EFFECTS Copy Grease Pencil Effects – Replace Grease Pencil Effects.

OBDATA Link Object Data – Replace assigned Object Data.

MATERIAL Link Materials – Replace assigned Materials.

ANIMATION Link Animation Data – Replace assigned Animation Data.

GROUPS Link Collections – Replace assigned Collections.

DUPLICOLLECTION Link Instance Collection – Replace assigned Collection Instance.

FONTS Link Fonts to Text – Replace Text object Fonts.

MODIFIERS Copy Modifiers – Replace Modifiers.

EFFECTS Copy Grease Pencil Effects – Replace Grease Pencil Effects.

Link selection to another scene

scene (enum in [], (optional)) – Scene

Make library linked data-blocks local to this file

type (enum in ['SELECT_OBJECT', 'SELECT_OBDATA', 'SELECT_OBDATA_MATERIAL', 'ALL'], (optional)) – Type

Create a local override of the selected linked objects, and their hierarchy of dependencies

collection (int in [-inf, inf], (optional)) – Override Collection, Session UID of the directly linked collection containing the selected object, to make an override from

Make linked data local to each object

type (enum in ['SELECTED_OBJECTS', 'ALL'], (optional)) – Type

object (boolean, (optional)) – Object, Make single user objects

obdata (boolean, (optional)) – Object Data, Make single user object data

material (boolean, (optional)) – Materials, Make materials local to each data-block

animation (boolean, (optional)) – Object Animation, Make object animation data local to each object

obdata_animation (boolean, (optional)) – Object Data Animation, Make object data (mesh, curve etc.) animation data local to each object

Add a new material slot

Assign active material slot to selection

Copy material to selected objects

Deselect by active material slot

Move the active material up/down in the list

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active material towards

Remove the selected material slot

Remove unused material slots

Select by active material slot

Bind mesh to cage in mesh deform modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Add an metaball object to the scene

type (enum in Metaelem Type Items, (optional)) – Primitive

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Sets the object interaction mode

mode (enum in Object Mode Items, (optional)) – Mode

toggle (boolean, (optional)) – Toggle

Sets the object interaction mode

mode (enum in Object Mode Items, (optional)) – Mode

toggle (boolean, (optional)) – Toggle

mesh_select_mode (enum set in Mesh Select Mode Items, (optional)) – Mesh Mode

Add a procedural operation/effect to the active object

type (enum in Object Modifier Type Items, (optional)) – Type

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Add a procedural operation/effect to the active object

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Apply modifier and remove from the stack

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

report (boolean, (optional)) – Report, Create a notification after the operation

merge_customdata (boolean, (optional)) – Merge UVs, For mesh objects, merge UV coordinates that share a vertex to account for imprecision in some modifiers

single_user (boolean, (optional)) – Make Data Single User, Make the object’s data single user if needed

all_keyframes (boolean, (optional)) – Apply to all keyframes, For Grease Pencil objects, apply the modifier to all the keyframes

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Apply modifier as a new shape key and remove from the stack

keep_modifier (boolean, (optional)) – Keep Modifier, Do not remove the modifier from stack

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

report (boolean, (optional)) – Report, Create a notification after the operation

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Convert particles to a mesh object

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Duplicate modifier at the same position in the stack

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Copy the modifier from the active object to all selected objects

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Move modifier down in the stack

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Change the modifier’s index in the stack so it evaluates after the set number of others

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

index (int in [0, inf], (optional)) – Index, The index to move the modifier to

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Move modifier up in the stack

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Remove a modifier from the active object

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

report (boolean, (optional)) – Report, Create a notification after the operation

use_selected_objects (boolean, (optional)) – Selected Objects, Affect all selected objects instead of just the active object

Activate the modifier to use as the context

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Clear all modifiers from the selected objects

Copy modifiers to other selected objects

Move objects to a collection

collection_uid (int in [-1, inf], (optional)) – Collection UID, Session UID of the collection to move to

is_new (boolean, (optional)) – New, Move objects to a new collection

new_collection_name (string, (optional, never None)) – Name, Name of the newly added collection

Modify the base mesh to conform to the displaced mesh

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

apply_heuristic (boolean, (optional)) – Apply Subdivision Heuristic, Whether or not the final base mesh positions will be slightly altered to account for a new subdivision modifier being added

Pack displacements from an external file

Save displacements to an external file

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Deletes the higher resolution mesh, potential loss of detail

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Rebuilds all possible subdivisions levels to generate a lower resolution base mesh

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Copy vertex coordinates from other object

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Add a new level of subdivision

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

mode (enum in ['CATMULL_CLARK', 'SIMPLE', 'LINEAR'], (optional)) – Subdivision Mode, How the mesh is going to be subdivided to create a new level CATMULL_CLARK Catmull-Clark – Create a new level using Catmull-Clark subdivisions. SIMPLE Simple – Create a new level using simple subdivisions. LINEAR Linear – Create a new level using linear interpolation of the sculpted displacement.

Subdivision Mode, How the mesh is going to be subdivided to create a new level

CATMULL_CLARK Catmull-Clark – Create a new level using Catmull-Clark subdivisions.

SIMPLE Simple – Create a new level using simple subdivisions.

LINEAR Linear – Create a new level using linear interpolation of the sculpted displacement.

Rebuild a lower subdivision level of the current base mesh

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Bake an image sequence of ocean data

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

free (boolean, (optional)) – Free, Free the bake, rather than generating it

Clear the object’s origin

Set the object’s origin, by either moving the data, or set to center of data, or use 3D cursor

type (enum in ['GEOMETRY_ORIGIN', 'ORIGIN_GEOMETRY', 'ORIGIN_CURSOR', 'ORIGIN_CENTER_OF_MASS', 'ORIGIN_CENTER_OF_VOLUME'], (optional)) – Type GEOMETRY_ORIGIN Geometry to Origin – Move object geometry to object origin. ORIGIN_GEOMETRY Origin to Geometry – Calculate the center of geometry based on the current pivot point (median, otherwise bounding box). ORIGIN_CURSOR Origin to 3D Cursor – Move object origin to position of the 3D cursor. ORIGIN_CENTER_OF_MASS Origin to Center of Mass (Surface) – Calculate the center of mass from the surface area. ORIGIN_CENTER_OF_VOLUME Origin to Center of Mass (Volume) – Calculate the center of mass from the volume (must be manifold geometry with consistent normals).

GEOMETRY_ORIGIN Geometry to Origin – Move object geometry to object origin.

ORIGIN_GEOMETRY Origin to Geometry – Calculate the center of geometry based on the current pivot point (median, otherwise bounding box).

ORIGIN_CURSOR Origin to 3D Cursor – Move object origin to position of the 3D cursor.

ORIGIN_CENTER_OF_MASS Origin to Center of Mass (Surface) – Calculate the center of mass from the surface area.

ORIGIN_CENTER_OF_VOLUME Origin to Center of Mass (Volume) – Calculate the center of mass from the volume (must be manifold geometry with consistent normals).

center (enum in ['MEDIAN', 'BOUNDS'], (optional)) – Center

Clear the object’s parenting

type (enum in ['CLEAR', 'CLEAR_KEEP_TRANSFORM', 'CLEAR_INVERSE'], (optional)) – Type CLEAR Clear Parent – Completely clear the parenting relationship, including involved modifiers if any. CLEAR_KEEP_TRANSFORM Clear and Keep Transformation – As ‘Clear Parent’, but keep the current visual transformations of the object. CLEAR_INVERSE Clear Parent Inverse – Reset the transform corrections applied to the parenting relationship, does not remove parenting itself.

CLEAR Clear Parent – Completely clear the parenting relationship, including involved modifiers if any.

CLEAR_KEEP_TRANSFORM Clear and Keep Transformation – As ‘Clear Parent’, but keep the current visual transformations of the object.

CLEAR_INVERSE Clear Parent Inverse – Reset the transform corrections applied to the parenting relationship, does not remove parenting itself.

Apply the object’s parent inverse to its data

Set the object’s parenting without setting the inverse parent correction

keep_transform (boolean, (optional)) – Keep Transform, Preserve the world transform throughout parenting

Set the object’s parenting

type (enum in ['OBJECT', 'ARMATURE', 'ARMATURE_NAME', 'ARMATURE_AUTO', 'ARMATURE_ENVELOPE', 'BONE', 'BONE_RELATIVE', 'CURVE', 'FOLLOW', 'PATH_CONST', 'LATTICE', 'VERTEX', 'VERTEX_TRI'], (optional)) – Type

xmirror (boolean, (optional)) – X Mirror, Apply weights symmetrically along X axis, for Envelope/Automatic vertex groups creation

keep_transform (boolean, (optional)) – Keep Transform, Apply transformation before parenting

Add a particle system

Remove the selected particle system

Pastes the matrix from the clipboard to the currently active pose bone or object. Uses world-space matrices

method (enum in ['CURRENT', 'EXISTING_KEYS', 'BAKE'], (optional)) – Paste Method, Update the current transform, selected keyframes, or even create new keys CURRENT Current Transform – Paste onto the current values only, only manipulating the animation data if auto-keying is enabled. EXISTING_KEYS Selected Keys – Paste onto frames that have a selected key, potentially creating new keys on those frames. BAKE Bake on Key Range – Paste onto all frames between the first and last selected key, creating new keyframes if necessary.

Paste Method, Update the current transform, selected keyframes, or even create new keys

CURRENT Current Transform – Paste onto the current values only, only manipulating the animation data if auto-keying is enabled.

EXISTING_KEYS Selected Keys – Paste onto frames that have a selected key, potentially creating new keys on those frames.

BAKE Bake on Key Range – Paste onto all frames between the first and last selected key, creating new keyframes if necessary.

bake_step (int in [1, inf], (optional)) – Frame Step, Only used for baking. Step=1 creates a key on every frame, step=2 bakes on 2s, etc

use_mirror (boolean, (optional)) – Mirror Transform, When pasting, mirror the transform relative to a specific object or bone

mirror_axis_loc (enum in ['x', 'y', 'z'], (optional)) – Location Axis, Coordinate axis used to mirror the location part of the transform

mirror_axis_rot (enum in ['x', 'y', 'z'], (optional)) – Rotation Axis, Coordinate axis used to mirror the rotation part of the transform

use_relative (boolean, (optional)) – Use Relative Paste, When pasting, assume the pasted matrix is relative to another object (set in the user interface)

startup/bl_operators/copy_global_transform.py:325

Generate motion paths for the selected objects

display_type (enum in Motionpath Display Type Items, (optional)) – Display Type

range (enum in Motionpath Range Items, (optional)) – Computation Range

Undocumented, consider contributing.

only_selected (boolean, (optional)) – Only Selected, Only clear motion paths of selected objects

Recalculate motion paths for selected objects

Recalculate all visible motion paths for objects and poses

Add a point cloud object to the scene

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Enable or disable posing/selecting bones

Create a new quad based mesh using the surface data of the current mesh. All data layers will be lost

use_mesh_symmetry (boolean, (optional)) – Use Mesh Symmetry, Generates a symmetrical mesh using the mesh symmetry configuration

use_preserve_sharp (boolean, (optional)) – Preserve Sharp, Try to preserve sharp features on the mesh

use_preserve_boundary (boolean, (optional)) – Preserve Mesh Boundary, Try to preserve mesh boundary on the mesh

preserve_attributes (boolean, (optional)) – Preserve Attributes, Reproject attributes onto the new mesh

smooth_normals (boolean, (optional)) – Smooth Normals, Set the output mesh normals to smooth

mode (enum in ['RATIO', 'EDGE', 'FACES'], (optional)) – Mode, How to specify the amount of detail for the new mesh RATIO Ratio – Specify target number of faces relative to the current mesh. EDGE Edge Length – Input target edge length in the new mesh. FACES Faces – Input target number of faces in the new mesh.

Mode, How to specify the amount of detail for the new mesh

RATIO Ratio – Specify target number of faces relative to the current mesh.

EDGE Edge Length – Input target edge length in the new mesh.

FACES Faces – Input target number of faces in the new mesh.

target_ratio (float in [0, inf], (optional)) – Ratio, Relative number of faces compared to the current mesh

target_edge_length (float in [1e-07, inf], (optional)) – Edge Length, Target edge length in the new mesh

target_faces (int in [1, inf], (optional)) – Number of Faces, Approximate number of faces (quads) in the new mesh

mesh_area (float in [-inf, inf], (optional)) – Old Object Face Area, This property is only used to cache the object area for later calculations

seed (int in [0, inf], (optional)) – Seed, Random seed to use with the solver. Different seeds will cause the remesher to come up with different quad layouts on the mesh

Make selected objects explode

style (enum in ['EXPLODE', 'BLEND'], (optional)) – Explode Style

amount (int in [2, 10000], (optional)) – Number of Pieces

frame_duration (int in [1, 300000], (optional)) – Duration

frame_start (int in [1, 300000], (optional)) – Start Frame

frame_end (int in [1, 300000], (optional)) – End Frame

velocity (float in [0, 300000], (optional)) – Outwards Velocity

fade (boolean, (optional)) – Fade, Fade the pieces over time

startup/bl_operators/object_quick_effects.py:273

Add a fur setup to the selected objects

density (enum in ['LOW', 'MEDIUM', 'HIGH'], (optional)) – Density

length (float in [0.001, 100], (optional)) – Length

radius (float in [0, 10], (optional)) – Hair Radius

view_percentage (float in [0, 1], (optional)) – View Percentage

apply_hair_guides (boolean, (optional)) – Apply Hair Guides

use_noise (boolean, (optional)) – Noise

use_frizz (boolean, (optional)) – Frizz

startup/bl_operators/object_quick_effects.py:92

Make selected objects liquid

show_flows (boolean, (optional)) – Render Liquid Objects, Keep the liquid objects visible during rendering

startup/bl_operators/object_quick_effects.py:553

Use selected objects as smoke emitters

style (enum in ['SMOKE', 'FIRE', 'BOTH'], (optional)) – Smoke Style

show_flows (boolean, (optional)) – Render Smoke Objects, Keep the smoke objects visible during rendering

startup/bl_operators/object_quick_effects.py:447

Randomize objects location, rotation, and scale

random_seed (int in [0, 10000], (optional)) – Random Seed, Seed value for the random generator

use_delta (boolean, (optional)) – Transform Delta, Randomize delta transform values instead of regular transform

use_loc (boolean, (optional)) – Randomize Location, Randomize the location values

loc (mathutils.Vector of 3 items in [-100, 100], (optional)) – Location, Maximum distance the objects can spread over each axis

use_rot (boolean, (optional)) – Randomize Rotation, Randomize the rotation values

rot (mathutils.Euler rotation of 3 items in [-3.14159, 3.14159], (optional)) – Rotation, Maximum rotation over each axis

use_scale (boolean, (optional)) – Randomize Scale, Randomize the scale values

scale_even (boolean, (optional)) – Scale Even, Use the same scale value for all axis

scale (float array of 3 items in [-100, 100], (optional)) – Scale, Maximum scale randomization over each axis

startup/bl_operators/object_randomize_transform.py:161

Reset the selected local overrides to their linked references values

Clear the object’s rotation

clear_delta (boolean, (optional)) – Clear Delta, Clear delta rotation in addition to clearing the normal rotation transform

Clear the object’s scale

clear_delta (boolean, (optional)) – Clear Delta, Clear delta scale in addition to clearing the normal scale transform

Change selection of all visible objects in scene

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select all visible objects that are of a type

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

type (enum in Object Type Items, (optional)) – Type

Select the active camera

extend (boolean, (optional)) – Extend, Extend the selection

startup/bl_operators/object.py:122

Select all visible objects grouped by various properties

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

type (enum in ['CHILDREN_RECURSIVE', 'CHILDREN', 'PARENT', 'SIBLINGS', 'TYPE', 'COLLECTION', 'HOOK', 'PASS', 'COLOR', 'KEYINGSET', 'LIGHT_TYPE'], (optional)) – Type CHILDREN_RECURSIVE Children. CHILDREN Immediate Children. PARENT Parent. SIBLINGS Siblings – Shared parent. TYPE Type – Shared object type. COLLECTION Collection – Shared collection. HOOK Hook. PASS Pass – Render pass index. COLOR Color – Object color. KEYINGSET Keying Set – Objects included in active Keying Set. LIGHT_TYPE Light Type – Matching light types.

CHILDREN_RECURSIVE Children.

CHILDREN Immediate Children.

SIBLINGS Siblings – Shared parent.

TYPE Type – Shared object type.

COLLECTION Collection – Shared collection.

PASS Pass – Render pass index.

COLOR Color – Object color.

KEYINGSET Keying Set – Objects included in active Keying Set.

LIGHT_TYPE Light Type – Matching light types.

Select object relative to the active object’s position in the hierarchy

direction (enum in ['PARENT', 'CHILD'], (optional)) – Direction, Direction to select in the hierarchy

extend (boolean, (optional)) – Extend, Extend the existing selection

startup/bl_operators/object.py:172

Deselect objects at the boundaries of parent/child relationships

Select all visible objects that are linked

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

type (enum in ['OBDATA', 'MATERIAL', 'DUPGROUP', 'PARTICLE', 'LIBRARY', 'LIBRARY_OBDATA'], (optional)) – Type

Select the mirror objects of the selected object e.g. “L.sword” and “R.sword”

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

Select connected parent/child objects

Select objects matching a naming pattern

pattern (string, (optional, never None)) – Pattern, Name filter using ‘*’, ‘?’ and ‘[abc]’ unix style wildcards

case_sensitive (boolean, (optional)) – Case Sensitive, Do a case sensitive compare

extend (boolean, (optional)) – Extend, Extend the existing selection

startup/bl_operators/object.py:45

Select or deselect random visible objects

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

Select object in the same collection

collection (string, (optional, never None)) – Collection, Name of the collection to select

Add modifier to automatically set the sharpness of mesh edges based on the angle between the neighboring faces

use_auto_smooth (boolean, (optional)) – Auto Smooth, Add modifier to set edge sharpness automatically

angle (float in [0, 3.14159], (optional)) – Angle, Maximum angle between face normals that will be considered as smooth

Render and display faces uniform, using face normals

keep_sharp_edges (boolean, (optional)) – Keep Sharp Edges, Don’t remove sharp edges, which are redundant with faces shaded smooth

Render and display faces smooth, using interpolated vertex normals

keep_sharp_edges (boolean, (optional)) – Keep Sharp Edges, Don’t remove sharp edges. Tagged edges will remain sharp

Set the sharpness of mesh edges based on the angle between the neighboring faces

angle (float in [0, 3.14159], (optional)) – Angle, Maximum angle between face normals that will be considered as smooth

keep_sharp_edges (boolean, (optional)) – Keep Sharp Edges, Only add sharp edges instead of clearing existing tags first

Add a visual effect to the active object

type (enum in Object Shaderfx Type Items, (optional)) – Type

Duplicate effect at the same position in the stack

shaderfx (string, (optional, never None)) – Shader, Name of the shaderfx to edit

Move effect down in the stack

shaderfx (string, (optional, never None)) – Shader, Name of the shaderfx to edit

Change the effect’s position in the list so it evaluates after the set number of others

shaderfx (string, (optional, never None)) – Shader, Name of the shaderfx to edit

index (int in [0, inf], (optional)) – Index, The index to move the effect to

Move effect up in the stack

shaderfx (string, (optional, never None)) – Shader, Name of the shaderfx to edit

Remove a effect from the active Grease Pencil object

shaderfx (string, (optional, never None)) – Shader, Name of the shaderfx to edit

report (boolean, (optional)) – Report, Create a notification after the operation

Add shape key to the object

from_mix (boolean, (optional)) – From Mix, Create the new shape key from the existing mix of keys

Reset the weights of all shape keys to 0 or to the closest value respecting the limits

Duplicate the active shape key

Change the lock state of all shape keys of active object

action (enum in ['LOCK', 'UNLOCK'], (optional)) – Action, Lock action to execute on vertex groups LOCK Lock – Lock all shape keys. UNLOCK Unlock – Unlock all shape keys.

Action, Lock action to execute on vertex groups

LOCK Lock – Lock all shape keys.

UNLOCK Unlock – Unlock all shape keys.

Make this shape key the new basis key, effectively applying it to the mesh. Note that this applies the shape key at its 100% value

Mirror the current shape key along the local X axis

use_topology (boolean, (optional)) – Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)

Move selected shape keys up/down in the list

type (enum in ['TOP', 'UP', 'DOWN', 'BOTTOM'], (optional)) – Type TOP Top – Top of the list. UP Up. DOWN Down. BOTTOM Bottom – Bottom of the list.

TOP Top – Top of the list.

BOTTOM Bottom – Bottom of the list.

Remove shape key from the object

all (boolean, (optional)) – All, Remove all shape keys

apply_mix (boolean, (optional)) – Apply Mix, Apply current mix of shape keys to the geometry before removing them

Resets the timing for absolute shape keys

Copy the active shape key of another selected object to this one

mode (enum in ['OFFSET', 'RELATIVE_FACE', 'RELATIVE_EDGE'], (optional)) – Transformation Mode, Relative shape positions to the new shape method OFFSET Offset – Apply the relative positional offset. RELATIVE_FACE Relative Face – Calculate relative position (using faces). RELATIVE_EDGE Relative Edge – Calculate relative position (using edges).

Transformation Mode, Relative shape positions to the new shape method

OFFSET Offset – Apply the relative positional offset.

RELATIVE_FACE Relative Face – Calculate relative position (using faces).

RELATIVE_EDGE Relative Edge – Calculate relative position (using edges).

use_clamp (boolean, (optional)) – Clamp Offset, Clamp the transformation to the distance each vertex moves in the original shape

startup/bl_operators/object.py:502

Bake simulations in geometry nodes modifiers

selected (boolean, (optional)) – Selected, Bake cache on all selected objects

Calculate simulations in geometry nodes modifiers from the start to current frame

selected (boolean, (optional)) – Selected, Calculate all selected objects instead of just the active object

Delete cached/baked simulations in geometry nodes modifiers

selected (boolean, (optional)) – Selected, Delete cache on all selected objects

Create an armature that parallels the skin layout

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Mark/clear selected vertices as loose

action (enum in ['MARK', 'CLEAR'], (optional)) – Action MARK Mark – Mark selected vertices as loose. CLEAR Clear – Set selected vertices as not loose.

MARK Mark – Mark selected vertices as loose.

CLEAR Clear – Set selected vertices as not loose.

Make skin radii of selected vertices equal on each axis

Mark selected vertices as roots

Add a speaker object to the scene

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Sets a Subdivision Surface level (1 to 5)

level (int in [-100, 100], (optional)) – Level

relative (boolean, (optional)) – Relative, Apply the subdivision surface level as an offset relative to the current level

ensure_modifier (boolean, (optional)) – Ensure Modifier, Create the corresponding modifier if it does not exist

startup/bl_operators/object.py:245

Bind mesh to target in surface deform modifier

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

Add a text object to the scene

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Clear tracking constraint or flag from object

type (enum in ['CLEAR', 'CLEAR_KEEP_TRANSFORM'], (optional)) – Type

Make the object track another object, using various methods/constraints

type (enum in ['DAMPTRACK', 'TRACKTO', 'LOCKTRACK'], (optional)) – Type

Switches the active object and assigns the same mode to a new one under the mouse cursor, leaving the active mode in the current one

use_flash_on_transfer (boolean, (optional)) – Flash On Transfer, Flash the target object when transferring the mode

Apply the object’s transformation to its data

location (boolean, (optional)) – Location

rotation (boolean, (optional)) – Rotation

scale (boolean, (optional)) – Scale

properties (boolean, (optional)) – Apply Properties, Modify properties such as curve vertex radius, font size and bone envelope

isolate_users (boolean, (optional)) – Isolate Multi User Data, Create new object-data users if needed

Interactively point cameras and lights to a location (Ctrl translates)

Snap selected item(s) to the mouse location

name (string, (optional, never None)) – Name, Object name to place (uses the active object when this and ‘session_uid’ are unset)

session_uid (int in [-inf, inf], (optional)) – Session UUID, Session UUID of the object to place (uses the active object when this and ‘name’ are unset)

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – Matrix

drop_x (int in [-inf, inf], (optional)) – Drop X, X-coordinate (screen space) to place the new object under

drop_y (int in [-inf, inf], (optional)) – Drop Y, Y-coordinate (screen space) to place the new object under

Convert normal object transforms to delta transforms, any existing delta transforms will be included as well

mode (enum in ['ALL', 'LOC', 'ROT', 'SCALE'], (optional)) – Mode, Which transforms to transfer ALL All Transforms – Transfer location, rotation, and scale transforms. LOC Location – Transfer location transforms only. ROT Rotation – Transfer rotation transforms only. SCALE Scale – Transfer scale transforms only.

Mode, Which transforms to transfer

ALL All Transforms – Transfer location, rotation, and scale transforms.

LOC Location – Transfer location transforms only.

ROT Rotation – Transfer rotation transforms only.

SCALE Scale – Transfer scale transforms only.

reset_values (boolean, (optional)) – Reset Values, Clear transform values after transferring to deltas

startup/bl_operators/object.py:764

Undocumented, consider contributing.

Update existing shape keys with the vertex positions of selected objects with matching names

use_mirror (boolean, (optional)) – Mirror, Mirror the new shape key values

Add a new vertex group to the active object

Assign the selected vertices to the active vertex group

Assign the selected vertices to a new vertex group

Remove vertex group assignments which are not required

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

limit (float in [0, 1], (optional)) – Limit, Remove vertices which weight is below or equal to this limit

keep_single (boolean, (optional)) – Keep Single, Keep verts assigned to at least one group when cleaning

Make a copy of the active vertex group

Replace vertex groups of selected objects by vertex groups of active object

Deselect all selected vertices assigned to the active vertex group

Invert active vertex group’s weights

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

auto_assign (boolean, (optional)) – Add Weights, Add vertices from groups that have zero weight before inverting

auto_remove (boolean, (optional)) – Remove Weights, Remove vertices from groups that have zero weight after inverting

Add some offset and multiply with some gain the weights of the active vertex group

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

offset (float in [-1, 1], (optional)) – Offset, Value to add to weights

gain (float in [0, inf], (optional)) – Gain, Value to multiply weights by

Limit deform weights associated with a vertex to a specified number by removing lowest weights

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

limit (int in [1, 32], (optional)) – Limit, Maximum number of deform weights

Change the lock state of all or some vertex groups of active object

action (enum in ['TOGGLE', 'LOCK', 'UNLOCK', 'INVERT'], (optional)) – Action, Lock action to execute on vertex groups TOGGLE Toggle – Unlock all vertex groups if there is at least one locked group, lock all in other case. LOCK Lock – Lock all vertex groups. UNLOCK Unlock – Unlock all vertex groups. INVERT Invert – Invert the lock state of all vertex groups.

Action, Lock action to execute on vertex groups

TOGGLE Toggle – Unlock all vertex groups if there is at least one locked group, lock all in other case.

LOCK Lock – Lock all vertex groups.

UNLOCK Unlock – Unlock all vertex groups.

INVERT Invert – Invert the lock state of all vertex groups.

mask (enum in ['ALL', 'SELECTED', 'UNSELECTED', 'INVERT_UNSELECTED'], (optional)) – Mask, Apply the action based on vertex group selection ALL All – Apply action to all vertex groups. SELECTED Selected – Apply to selected vertex groups. UNSELECTED Unselected – Apply to unselected vertex groups. INVERT_UNSELECTED Invert Unselected – Apply the opposite of Lock/Unlock to unselected vertex groups.

Mask, Apply the action based on vertex group selection

ALL All – Apply action to all vertex groups.

SELECTED Selected – Apply to selected vertex groups.

UNSELECTED Unselected – Apply to unselected vertex groups.

INVERT_UNSELECTED Invert Unselected – Apply the opposite of Lock/Unlock to unselected vertex groups.

Mirror vertex group, flip weights and/or names, editing only selected vertices, flipping when both sides are selected otherwise copy from unselected

mirror_weights (boolean, (optional)) – Mirror Weights, Mirror weights

flip_group_names (boolean, (optional)) – Flip Group Names, Flip vertex group names

all_groups (boolean, (optional)) – All Groups, Mirror all vertex groups weights

use_topology (boolean, (optional)) – Topology Mirror, Use topology based mirroring (for when both sides of mesh have matching, unique topology)

Move the active vertex group up/down in the list

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active vertex group towards

Normalize weights of the active vertex group, so that the highest ones are now 1.0

Normalize all weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

lock_active (boolean, (optional)) – Lock Active, Keep the values of the active group while normalizing others

Set weights to a fixed number of steps

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

steps (int in [1, 1000], (optional)) – Steps, Number of steps between 0 and 1

Delete the active or all vertex groups from the active object

all (boolean, (optional)) – All, Remove all vertex groups

all_unlocked (boolean, (optional)) – All Unlocked, Remove all unlocked vertex groups

Remove the selected vertices from active or all vertex group(s)

use_all_groups (boolean, (optional)) – All Groups, Remove from all groups

use_all_verts (boolean, (optional)) – All Vertices, Clear the active group

Select all the vertices assigned to the active vertex group

Set the active vertex group

group (enum in [], (optional)) – Group, Vertex group to set as active

Smooth weights for selected vertices

group_select_mode (enum in [], (optional)) – Subset, Define which subset of groups shall be used

factor (float in [0, 1], (optional)) – Factor

repeat (int in [1, 10000], (optional)) – Iterations

expand (float in [-1, 1], (optional)) – Expand/Contract, Expand/contract weights

sort_type (enum in ['NAME', 'BONE_HIERARCHY'], (optional)) – Sort Type, Sort type

Parent selected objects to the selected vertices

Copy weights from active to selected

Delete this weight from the vertex (disabled if vertex group is locked)

weight_group (int in [-1, inf], (optional)) – Weight Index, Index of source weight in active vertex group

Normalize active vertex’s weights

Copy this group’s weight to other selected vertices (disabled if vertex group is locked)

weight_group (int in [-1, inf], (optional)) – Weight Index, Index of source weight in active vertex group

Set as active vertex group

weight_group (int in [-1, inf], (optional)) – Weight Index, Index of source weight in active vertex group

Convert geometry and instances into editable objects and collections

Apply the object’s visual transformation to its data

Add a volume object to the scene

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Import OpenVDB volume file

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_sequence_detection (boolean, (optional)) – Detect Sequences, Automatically detect animated sequences in selected volume files (based on file names)

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Calculates a new manifold mesh based on the volume of the current mesh. All data layers will be lost

Modify the mesh voxel size interactively used in the voxel remesher

---

## Paint Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.paint.html

**Contents:**
- Paint Operators¶

Add cube map UVs on mesh

type (enum in ['BASE_COLOR', 'SPECULAR', 'ROUGHNESS', 'METALLIC', 'NORMAL', 'BUMP', 'DISPLACEMENT'], (optional)) – Material Layer Type, Material layer type of new paint slot

slot_type (enum in ['IMAGE', 'COLOR_ATTRIBUTE'], (optional)) – Slot Type, Type of new paint slot

name (string, (optional, never None)) – Name, Name for new paint slot source

color (float array of 4 items in [0, inf], (optional)) – Color, Default fill color

width (int in [1, inf], (optional)) – Width, Image width

height (int in [1, inf], (optional)) – Height, Image height

alpha (boolean, (optional)) – Alpha, Create an image with an alpha channel

generated_type (enum in Image Generated Type Items, (optional)) – Generated Type, Fill the image with a grid for UV map testing

float (boolean, (optional)) – 32-bit Float, Create image with 32-bit floating-point bit depth

domain (enum in Color Attribute Domain Items, (optional)) – Domain, Type of element that attribute is stored on

data_type (enum in Color Attribute Type Items, (optional)) – Data Type, Type of data stored in attribute

Swap primary and secondary brush colors

Change selection for all faces

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected objects

Deselect Faces connected to existing selection

face_step (boolean, (optional)) – Face Step, Also deselect faces that only touch on a corner

Select linked faces under the cursor

deselect (boolean, (optional)) – Deselect, Deselect rather than select items

Select face loop under the cursor

select (boolean, (optional)) – Select, If false, faces will be deselected

extend (boolean, (optional)) – Extend, Extend the selection

Select Faces connected to existing selection

face_step (boolean, (optional)) – Face Step, Also select faces that only touch on a corner

Reveal hidden faces and vertices

select (boolean, (optional)) – Select, Specifies whether the newly revealed geometry should be selected

Move the clone source image

delta (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Delta, Delta offset of clone image in 0.0 to 1.0 coordinates

Hide/show some vertices

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

area (enum in ['OUTSIDE', 'Inside'], (optional)) – Visibility Area, Which vertices to hide or show OUTSIDE Outside – Hide or show vertices outside the selection. Inside Inside – Hide or show vertices inside the selection.

Visibility Area, Which vertices to hide or show

OUTSIDE Outside – Hide or show vertices outside the selection.

Inside Inside – Hide or show vertices inside the selection.

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Hide/show all vertices

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

Hide/show some vertices

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

area (enum in ['OUTSIDE', 'Inside'], (optional)) – Visibility Area, Which vertices to hide or show OUTSIDE Outside – Hide or show vertices outside the selection. Inside Inside – Hide or show vertices inside the selection.

Visibility Area, Which vertices to hide or show

OUTSIDE Outside – Hide or show vertices outside the selection.

Inside Inside – Hide or show vertices inside the selection.

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Hide/show some vertices

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

area (enum in ['OUTSIDE', 'Inside'], (optional)) – Visibility Area, Which vertices to hide or show OUTSIDE Outside – Hide or show vertices outside the selection. Inside Inside – Hide or show vertices inside the selection.

Visibility Area, Which vertices to hide or show

OUTSIDE Outside – Hide or show vertices outside the selection.

Inside Inside – Hide or show vertices inside the selection.

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

use_limit_to_segment (boolean, (optional)) – Limit to Segment, Apply the gesture action only to the area that is contained within the segment without extending its effect to the entire line

Hide/show all masked vertices above a threshold

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

Hide/show some vertices

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

action (enum in ['HIDE', 'SHOW'], (optional)) – Visibility Action, Whether to hide or show vertices HIDE Hide – Hide vertices. SHOW Show – Show vertices.

Visibility Action, Whether to hide or show vertices

HIDE Hide – Hide vertices.

SHOW Show – Show vertices.

area (enum in ['OUTSIDE', 'Inside'], (optional)) – Visibility Area, Which vertices to hide or show OUTSIDE Outside – Hide or show vertices outside the selection. Inside Inside – Hide or show vertices inside the selection.

Visibility Area, Which vertices to hide or show

OUTSIDE Outside – Hide or show vertices outside the selection.

Inside Inside – Hide or show vertices inside the selection.

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Make an image from biggest 3D view for reprojection

filepath (string, (optional, never None)) – File Path, Name of the file

Paint a stroke into the image

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Mask within a rectangle defined by the cursor

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

mode (enum in ['VALUE', 'VALUE_INVERSE', 'INVERT'], (optional)) – Mode VALUE Value – Set mask to the level specified by the ‘value’ property. VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property. INVERT Invert – Invert the mask.

VALUE Value – Set mask to the level specified by the ‘value’ property.

VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property.

INVERT Invert – Invert the mask.

value (float in [0, 1], (optional)) – Value, Mask level to use when mode is ‘Value’; zero means no masking and one is fully masked

Fill the whole mask with a given value, or invert its values

mode (enum in ['VALUE', 'VALUE_INVERSE', 'INVERT'], (optional)) – Mode VALUE Value – Set mask to the level specified by the ‘value’ property. VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property. INVERT Invert – Invert the mask.

VALUE Value – Set mask to the level specified by the ‘value’ property.

VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property.

INVERT Invert – Invert the mask.

value (float in [0, 1], (optional)) – Value, Mask level to use when mode is ‘Value’; zero means no masking and one is fully masked

Mask within a shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

mode (enum in ['VALUE', 'VALUE_INVERSE', 'INVERT'], (optional)) – Mode VALUE Value – Set mask to the level specified by the ‘value’ property. VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property. INVERT Invert – Invert the mask.

VALUE Value – Set mask to the level specified by the ‘value’ property.

VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property.

INVERT Invert – Invert the mask.

value (float in [0, 1], (optional)) – Value, Mask level to use when mode is ‘Value’; zero means no masking and one is fully masked

Mask to one side of a line defined by the cursor

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

use_limit_to_segment (boolean, (optional)) – Limit to Segment, Apply the gesture action only to the area that is contained within the segment without extending its effect to the entire line

mode (enum in ['VALUE', 'VALUE_INVERSE', 'INVERT'], (optional)) – Mode VALUE Value – Set mask to the level specified by the ‘value’ property. VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property. INVERT Invert – Invert the mask.

VALUE Value – Set mask to the level specified by the ‘value’ property.

VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property.

INVERT Invert – Invert the mask.

value (float in [0, 1], (optional)) – Value, Mask level to use when mode is ‘Value’; zero means no masking and one is fully masked

Mask within a shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

mode (enum in ['VALUE', 'VALUE_INVERSE', 'INVERT'], (optional)) – Mode VALUE Value – Set mask to the level specified by the ‘value’ property. VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property. INVERT Invert – Invert the mask.

VALUE Value – Set mask to the level specified by the ‘value’ property.

VALUE_INVERSE Value Inverted – Set mask to the level specified by the inverted ‘value’ property.

INVERT Invert – Invert the mask.

value (float in [0, 1], (optional)) – Value, Mask level to use when mode is ‘Value’; zero means no masking and one is fully masked

Project an edited render from the active camera back onto the object

image (enum in [], (optional)) – Image

Use the mouse to sample a color in the image

location (int array of 2 items in [0, inf], (optional)) – Location

merged (boolean, (optional)) – Sample Merged, Sample the output display color

palette (boolean, (optional)) – Add to Palette

Toggle texture paint mode in 3D view

Change selection for all vertices

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Hide selected vertices

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected vertices

Deselect Vertices connected to existing selection

face_step (boolean, (optional)) – Face Step, Also deselect faces that only touch on a corner

Select linked vertices

Select linked vertices under the cursor

select (boolean, (optional)) – Select, Whether to select or deselect linked vertices under the cursor

Select Vertices connected to existing selection

face_step (boolean, (optional)) – Face Step, Also select faces that only touch on a corner

Select vertices without a group

extend (boolean, (optional)) – Extend, Extend the selection

Adjust vertex color brightness/contrast

brightness (float in [-100, 100], (optional)) – Brightness

contrast (float in [-100, 100], (optional)) – Contrast

Generate a dirt map gradient based on cavity

blur_strength (float in [0.01, 1], (optional)) – Blur Strength, Blur strength per iteration

blur_iterations (int in [0, 40], (optional)) – Blur Iterations, Number of times to blur the colors (higher blurs more)

clean_angle (float in [0, 3.14159], (optional)) – Highlight Angle, Less than 90 limits the angle used in the tonal range

dirt_angle (float in [0, 3.14159], (optional)) – Dirt Angle, Less than 90 limits the angle used in the tonal range

dirt_only (boolean, (optional)) – Dirt Only, Don’t calculate cleans for convex areas

normalize (boolean, (optional)) – Normalize, Normalize the colors, increasing the contrast

startup/bl_operators/vertexpaint_dirt.py:179

Convert active weight into gray scale vertex colors

Adjust vertex color Hue/Saturation/Value

h (float in [0, 1], (optional)) – Hue

s (float in [0, 2], (optional)) – Saturation

v (float in [0, 2], (optional)) – Value

Adjust levels of vertex colors

offset (float in [-1, 1], (optional)) – Offset, Value to add to colors

gain (float in [0, inf], (optional)) – Gain, Value to multiply colors by

Fill the active vertex color layer with the current paint color

use_alpha (boolean, (optional)) – Affect Alpha, Set color completely opaque instead of reusing existing alpha

Smooth colors across vertices

Paint a stroke in the active color attribute layer

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

override_location (boolean, (optional)) – Override Location, Override the given “location” array by recalculating object space positions from the provided “mouse_event” positions

Toggle the vertex paint mode in 3D view

Edit the visibility of the current mesh

action (enum in ['GROW', 'SHRINK'], (optional)) – Action GROW Grow Visibility – Grow the visibility by one face based on mesh topology. SHRINK Shrink Visibility – Shrink the visibility by one face based on mesh topology.

GROW Grow Visibility – Grow the visibility by one face based on mesh topology.

SHRINK Shrink Visibility – Shrink the visibility by one face based on mesh topology.

iterations (int in [1, 100], (optional)) – Iterations, Number of times that the filter is going to be applied

auto_iteration_count (boolean, (optional)) – Auto Iteration Count, Use an automatic number of iterations based on the number of vertices of the sculpt

Invert the visibility of all vertices

Set the weights of the groups matching the attached armature’s selected bones, using the distance between the vertices and the bones

type (enum in ['AUTOMATIC', 'ENVELOPES'], (optional)) – Type, Method to use for assigning weights AUTOMATIC Automatic – Automatic weights from bones. ENVELOPES From Envelopes – Weights from envelopes with user defined radius.

Type, Method to use for assigning weights

AUTOMATIC Automatic – Automatic weights from bones.

ENVELOPES From Envelopes – Weights from envelopes with user defined radius.

Draw a line to apply a weight gradient to selected vertices

type (enum in ['LINEAR', 'RADIAL'], (optional)) – Type

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

Paint a stroke in the current vertex group’s weights

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

override_location (boolean, (optional)) – Override Location, Override the given “location” array by recalculating object space positions from the provided “mouse_event” positions

Toggle weight paint mode in 3D view

Use the mouse to sample a weight in the 3D view

Select one of the vertex groups available under current mouse position

Fill the active vertex group with the current paint weight

---

## Paintcurve Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.paintcurve.html

**Contents:**
- Paintcurve Operators¶

Add New Paint Curve Point

location (int array of 2 items in [0, 32767], (optional)) – Location, Location of vertex in area space

Add new curve point and slide it

PAINTCURVE_OT_add_point (PAINTCURVE_OT_add_point, (optional)) – Add New Paint Curve Point, Add New Paint Curve Point

PAINTCURVE_OT_slide (PAINTCURVE_OT_slide, (optional)) – Slide Paint Curve Point, Select and slide paint curve point

Remove Paint Curve Point

Select a paint curve point

location (int array of 2 items in [0, 32767], (optional)) – Location, Location of vertex in area space

toggle (boolean, (optional)) – Toggle, (De)select all

extend (boolean, (optional)) – Extend, Extend selection

Select and slide paint curve point

align (boolean, (optional)) – Align Handles, Aligns opposite point handle during transform

select (boolean, (optional)) – Select, Attempt to select a point handle before transform

---

## Particle Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.particle.html

**Contents:**
- Particle Operators¶

Apply a stroke of brush to the particles

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Connect hair to the emitter mesh

all (boolean, (optional)) – All Hair, Connect all hair systems to the emitter mesh

Copy particle systems from the active object to selected objects

space (enum in ['OBJECT', 'WORLD'], (optional)) – Space, Space transform for copying from one object to another OBJECT Object – Copy inside each object’s local space. WORLD World – Copy in world space.

Space, Space transform for copying from one object to another

OBJECT Object – Copy inside each object’s local space.

WORLD World – Copy in world space.

remove_target_particles (boolean, (optional)) – Remove Target Particles, Remove particle systems on the target objects

use_active (boolean, (optional)) – Use Active, Use the active particle system from the context

Delete selected particles or keys

type (enum in ['PARTICLE', 'KEY'], (optional)) – Type, Delete a full particle or only keys

Disconnect hair from the emitter mesh

all (boolean, (optional)) – All Hair, Disconnect all hair systems from the emitter mesh

Duplicate particle system within the active object

use_duplicate_settings (boolean, (optional)) – Duplicate Settings, Duplicate settings as well, so the new particle system uses its own settings

Duplicate the current instance object

Move instance object down in the list

Move instance object up in the list

Refresh list of instance objects and their weights

Remove the selected instance object

Undo all edition performed on the particle system

Add or remove a Hair Dynamics Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Hide selected particles

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Duplicate and mirror the selected particles along the local X axis

Add new particle settings

Add a new particle target

Toggle particle edit mode

Remove all particle system within the active object

Change the number of keys of selected particles (root and tip keys included)

keys_number (int in [2, inf], (optional)) – Number of Keys

Remove selected particles close enough of others

threshold (float in [0, inf], (optional)) – Merge Distance, Threshold distance within which particles are removed

Show hidden particles

select (boolean, (optional)) – Select

(De)select all particles’ keys

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Deselect boundary selected keys of each particle

Select all keys linked to already selected ones

Select nearest particle from mouse pointer

deselect (boolean, (optional)) – Deselect, Deselect linked keys rather than selecting them

location (int array of 2 items in [0, inf], (optional)) – Location

Select keys linked to boundary selected keys of each particle

Select a randomly distributed set of hair or points

ratio (float in [0, 1], (optional)) – Ratio, Portion of items to select randomly

seed (int in [0, inf], (optional)) – Random Seed, Seed for the random number generator

action (enum in ['SELECT', 'DESELECT'], (optional)) – Action, Selection action to execute SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements.

Action, Selection action to execute

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

type (enum in ['HAIR', 'POINTS'], (optional)) – Type, Select either hair or points

Select roots of all visible particles

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select tips of all visible particles

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Cut hair to conform to the set shape object

Subdivide selected particles segments (adds keys)

Move particle target down in the list

Move particle target up in the list

Remove the selected particle target

Make selected hair the same length

Set the weight of selected keys

factor (float in [0, 1], (optional)) – Factor, Interpolation factor between current brush weight, and keys’ weights

---

## Palette Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.palette.html

**Contents:**
- Palette Operators¶

Add new color to active palette

Remove active color from palette

Move the active Color up/down in the list

type (enum in ['UP', 'DOWN'], (optional)) – Type

Extract all colors used in Image and create a Palette

threshold (int in [-inf, inf], (optional)) – Threshold

Join Palette Swatches

palette (string, (optional, never None)) – Palette, Name of the Palette

type (enum in ['HSV', 'SVH', 'VHS', 'LUMINANCE'], (optional)) – Type

---

## Pointcloud Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.pointcloud.html

**Contents:**
- Pointcloud Operators¶

Set values of the active attribute for selected elements

value_float (float in [-inf, inf], (optional)) – Value

value_float_vector_2d (float array of 2 items in [-inf, inf], (optional)) – Value

value_float_vector_3d (float array of 3 items in [-inf, inf], (optional)) – Value

value_int (int in [-inf, inf], (optional)) – Value

value_int_vector_2d (int array of 2 items in [-inf, inf], (optional)) – Value

value_color (float array of 4 items in [-inf, inf], (optional)) – Value

value_bool (boolean, (optional)) – Value

Remove selected points

Make copies of selected elements and move them

POINTCLOUD_OT_duplicate (POINTCLOUD_OT_duplicate, (optional)) – Duplicate, Copy selected points

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

(De)select all point cloud

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Randomizes existing selection or create new random selection

seed (int in [-inf, inf], (optional)) – Seed, Source of randomness

probability (float in [0, 1], (optional)) – Probability, Chance of every point being included in the selection

Separate selected geometry into a new point cloud

---

## Pose Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.pose.html

**Contents:**
- Pose Operators¶

Apply the current pose as the new rest pose

selected (boolean, (optional)) – Selected Only, Only apply the selected bones (with propagation to children)

Automatically renames the selected bones according to which side of the target axis they fall on

axis (enum in ['XAXIS', 'YAXIS', 'ZAXIS'], (optional)) – Axis, Axis to tag names with XAXIS X-Axis – Left/Right. YAXIS Y-Axis – Front/Back. ZAXIS Z-Axis – Top/Bottom.

Axis, Axis to tag names with

XAXIS X-Axis – Left/Right.

YAXIS Y-Axis – Front/Back.

ZAXIS Z-Axis – Top/Bottom.

Blend from current position to previous or next keyframe

factor (float in [0, 1], (optional)) – Factor, Weighting factor for which keyframe is favored more

prev_frame (int in [-1048574, 1048574], (optional)) – Previous Keyframe, Frame number of keyframe immediately before the current frame

next_frame (int in [-1048574, 1048574], (optional)) – Next Keyframe, Frame number of keyframe immediately after the current frame

channels (enum in ['ALL', 'LOC', 'ROT', 'SIZE', 'BBONE', 'CUSTOM'], (optional)) – Channels, Set of properties that are affected ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties. LOC Location – Location only. ROT Rotation – Rotation only. SIZE Scale – Scale only. BBONE Bendy Bone – Bendy Bone shape properties. CUSTOM Custom Properties – Custom properties.

Channels, Set of properties that are affected

ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties.

LOC Location – Location only.

ROT Rotation – Rotation only.

SIZE Scale – Scale only.

BBONE Bendy Bone – Bendy Bone shape properties.

CUSTOM Custom Properties – Custom properties.

axis_lock (enum in ['FREE', 'X', 'Y', 'Z'], (optional)) – Axis Lock, Transform axis to restrict effects to FREE Free – All axes are affected. X X – Only X-axis transforms are affected. Y Y – Only Y-axis transforms are affected. Z Z – Only Z-axis transforms are affected.

Axis Lock, Transform axis to restrict effects to

FREE Free – All axes are affected.

X X – Only X-axis transforms are affected.

Y Y – Only Y-axis transforms are affected.

Z Z – Only Z-axis transforms are affected.

Make the current pose more similar to, or further away from, the rest pose

factor (float in [0, 1], (optional)) – Factor, Weighting factor for which keyframe is favored more

prev_frame (int in [-1048574, 1048574], (optional)) – Previous Keyframe, Frame number of keyframe immediately before the current frame

next_frame (int in [-1048574, 1048574], (optional)) – Next Keyframe, Frame number of keyframe immediately after the current frame

channels (enum in ['ALL', 'LOC', 'ROT', 'SIZE', 'BBONE', 'CUSTOM'], (optional)) – Channels, Set of properties that are affected ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties. LOC Location – Location only. ROT Rotation – Rotation only. SIZE Scale – Scale only. BBONE Bendy Bone – Bendy Bone shape properties. CUSTOM Custom Properties – Custom properties.

Channels, Set of properties that are affected

ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties.

LOC Location – Location only.

ROT Rotation – Rotation only.

SIZE Scale – Scale only.

BBONE Bendy Bone – Bendy Bone shape properties.

CUSTOM Custom Properties – Custom properties.

axis_lock (enum in ['FREE', 'X', 'Y', 'Z'], (optional)) – Axis Lock, Transform axis to restrict effects to FREE Free – All axes are affected. X X – Only X-axis transforms are affected. Y Y – Only Y-axis transforms are affected. Z Z – Only Z-axis transforms are affected.

Axis Lock, Transform axis to restrict effects to

FREE Free – All axes are affected.

X X – Only X-axis transforms are affected.

Y Y – Only Y-axis transforms are affected.

Z Z – Only Z-axis transforms are affected.

Create a suitable breakdown pose on the current frame

factor (float in [0, 1], (optional)) – Factor, Weighting factor for which keyframe is favored more

prev_frame (int in [-1048574, 1048574], (optional)) – Previous Keyframe, Frame number of keyframe immediately before the current frame

next_frame (int in [-1048574, 1048574], (optional)) – Next Keyframe, Frame number of keyframe immediately after the current frame

channels (enum in ['ALL', 'LOC', 'ROT', 'SIZE', 'BBONE', 'CUSTOM'], (optional)) – Channels, Set of properties that are affected ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties. LOC Location – Location only. ROT Rotation – Rotation only. SIZE Scale – Scale only. BBONE Bendy Bone – Bendy Bone shape properties. CUSTOM Custom Properties – Custom properties.

Channels, Set of properties that are affected

ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties.

LOC Location – Location only.

ROT Rotation – Rotation only.

SIZE Scale – Scale only.

BBONE Bendy Bone – Bendy Bone shape properties.

CUSTOM Custom Properties – Custom properties.

axis_lock (enum in ['FREE', 'X', 'Y', 'Z'], (optional)) – Axis Lock, Transform axis to restrict effects to FREE Free – All axes are affected. X X – Only X-axis transforms are affected. Y Y – Only Y-axis transforms are affected. Z Z – Only Z-axis transforms are affected.

Axis Lock, Transform axis to restrict effects to

FREE Free – All axes are affected.

X X – Only X-axis transforms are affected.

Y Y – Only Y-axis transforms are affected.

Z Z – Only Z-axis transforms are affected.

Add a constraint to the active bone

type (enum in Constraint Type Items, (optional)) – Type

Add a constraint to the active bone, with target (where applicable) set to the selected Objects/Bones

type (enum in Constraint Type Items, (optional)) – Type

Clear all constraints from the selected bones

Copy constraints to other selected bones

Copy the current pose of the selected bones to the internal clipboard

Flips (and corrects) the axis suffixes of the names of selected bones

do_strip_numbers (boolean, (optional)) – Strip Numbers, Try to remove right-most dot-number from flipped names.Warning: May result in incoherent naming in some cases

Tag selected bones to not be visible in Pose Mode

unselected (boolean, (optional)) – Unselected

Add an IK Constraint to the active Bone. The target can be a selected bone or object

with_targets (boolean, (optional)) – With Targets, Assign IK Constraint with targets derived from the select bones/objects

Remove all IK Constraints from selected bones

Reset locations of selected bones to their default values

Paste the stored pose on to the current pose

flipped (boolean, (optional)) – Flipped on X-Axis, Paste the stored pose flipped on to current pose

selected_mask (boolean, (optional)) – On Selected Only, Only paste the stored pose on to selected bones in the current pose

Calculate paths for the selected bones

display_type (enum in Motionpath Display Type Items, (optional)) – Display Type

range (enum in Motionpath Range Items, (optional)) – Computation Range

bake_location (enum in Motionpath Bake Location Items, (optional)) – Bake Location, Which point on the bones is used when calculating paths

Undocumented, consider contributing.

only_selected (boolean, (optional)) – Only Selected, Only clear motion paths of selected bones

Update frame range for motion paths from the Scene’s current frame range

Recalculate paths for bones that already have them

Copy selected aspects of the current pose to subsequent poses already keyframed

mode (enum in ['NEXT_KEY', 'LAST_KEY', 'BEFORE_FRAME', 'BEFORE_END', 'SELECTED_KEYS', 'SELECTED_MARKERS'], (optional)) – Terminate Mode, Method used to determine when to stop propagating pose to keyframes NEXT_KEY To Next Keyframe – Propagate pose to first keyframe following the current frame only. LAST_KEY To Last Keyframe – Propagate pose to the last keyframe only (i.e. making action cyclic). BEFORE_FRAME Before Frame – Propagate pose to all keyframes between current frame and ‘Frame’ property. BEFORE_END Before Last Keyframe – Propagate pose to all keyframes from current frame until no more are found. SELECTED_KEYS On Selected Keyframes – Propagate pose to all selected keyframes. SELECTED_MARKERS On Selected Markers – Propagate pose to all keyframes occurring on frames with Scene Markers after the current frame.

Terminate Mode, Method used to determine when to stop propagating pose to keyframes

NEXT_KEY To Next Keyframe – Propagate pose to first keyframe following the current frame only.

LAST_KEY To Last Keyframe – Propagate pose to the last keyframe only (i.e. making action cyclic).

BEFORE_FRAME Before Frame – Propagate pose to all keyframes between current frame and ‘Frame’ property.

BEFORE_END Before Last Keyframe – Propagate pose to all keyframes from current frame until no more are found.

SELECTED_KEYS On Selected Keyframes – Propagate pose to all selected keyframes.

SELECTED_MARKERS On Selected Markers – Propagate pose to all keyframes occurring on frames with Scene Markers after the current frame.

end_frame (float in [1.17549e-38, inf], (optional)) – End Frame, Frame to stop propagating frames to (for ‘Before Frame’ mode)

Exaggerate the current pose in regards to the breakdown pose

factor (float in [0, 1], (optional)) – Factor, Weighting factor for which keyframe is favored more

prev_frame (int in [-1048574, 1048574], (optional)) – Previous Keyframe, Frame number of keyframe immediately before the current frame

next_frame (int in [-1048574, 1048574], (optional)) – Next Keyframe, Frame number of keyframe immediately after the current frame

channels (enum in ['ALL', 'LOC', 'ROT', 'SIZE', 'BBONE', 'CUSTOM'], (optional)) – Channels, Set of properties that are affected ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties. LOC Location – Location only. ROT Rotation – Rotation only. SIZE Scale – Scale only. BBONE Bendy Bone – Bendy Bone shape properties. CUSTOM Custom Properties – Custom properties.

Channels, Set of properties that are affected

ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties.

LOC Location – Location only.

ROT Rotation – Rotation only.

SIZE Scale – Scale only.

BBONE Bendy Bone – Bendy Bone shape properties.

CUSTOM Custom Properties – Custom properties.

axis_lock (enum in ['FREE', 'X', 'Y', 'Z'], (optional)) – Axis Lock, Transform axis to restrict effects to FREE Free – All axes are affected. X X – Only X-axis transforms are affected. Y Y – Only Y-axis transforms are affected. Z Z – Only Z-axis transforms are affected.

Axis Lock, Transform axis to restrict effects to

FREE Free – All axes are affected.

X X – Only X-axis transforms are affected.

Y Y – Only Y-axis transforms are affected.

Z Z – Only Z-axis transforms are affected.

Flip quaternion values to achieve desired rotations, while maintaining the same orientations

Make the current pose more similar to its breakdown pose

factor (float in [0, 1], (optional)) – Factor, Weighting factor for which keyframe is favored more

prev_frame (int in [-1048574, 1048574], (optional)) – Previous Keyframe, Frame number of keyframe immediately before the current frame

next_frame (int in [-1048574, 1048574], (optional)) – Next Keyframe, Frame number of keyframe immediately after the current frame

channels (enum in ['ALL', 'LOC', 'ROT', 'SIZE', 'BBONE', 'CUSTOM'], (optional)) – Channels, Set of properties that are affected ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties. LOC Location – Location only. ROT Rotation – Rotation only. SIZE Scale – Scale only. BBONE Bendy Bone – Bendy Bone shape properties. CUSTOM Custom Properties – Custom properties.

Channels, Set of properties that are affected

ALL All Properties – All properties, including transforms, bendy bone shape, and custom properties.

LOC Location – Location only.

ROT Rotation – Rotation only.

SIZE Scale – Scale only.

BBONE Bendy Bone – Bendy Bone shape properties.

CUSTOM Custom Properties – Custom properties.

axis_lock (enum in ['FREE', 'X', 'Y', 'Z'], (optional)) – Axis Lock, Transform axis to restrict effects to FREE Free – All axes are affected. X X – Only X-axis transforms are affected. Y Y – Only Y-axis transforms are affected. Z Z – Only Z-axis transforms are affected.

Axis Lock, Transform axis to restrict effects to

FREE Free – All axes are affected.

X X – Only X-axis transforms are affected.

Y Y – Only Y-axis transforms are affected.

Z Z – Only Z-axis transforms are affected.

Reveal all bones hidden in Pose Mode

select (boolean, (optional)) – Select

Reset rotations of selected bones to their default values

Set the rotation representation used by selected bones

type (enum in Object Rotation Mode Items, (optional)) – Rotation Mode

Reset scaling of selected bones to their default values

Toggle selection status of all bones

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select bones used as targets for the currently selected bones

Select all visible bones grouped by similar properties

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

type (enum in ['COLLECTION', 'COLOR', 'KEYINGSET', 'CHILDREN', 'CHILDREN_IMMEDIATE', 'PARENT', 'SIBLINGS'], (optional)) – Type COLLECTION Collection – Same collections as the active bone. COLOR Color – Same color as the active bone. KEYINGSET Keying Set – All bones affected by active Keying Set. CHILDREN Children – Select all children of currently selected bones. CHILDREN_IMMEDIATE Immediate Children – Select direct children of currently selected bones. PARENT Parents – Select the parents of currently selected bones. SIBLINGS Siblings – Select all bones that have the same parent as currently selected bones.

COLLECTION Collection – Same collections as the active bone.

COLOR Color – Same color as the active bone.

KEYINGSET Keying Set – All bones affected by active Keying Set.

CHILDREN Children – Select all children of currently selected bones.

CHILDREN_IMMEDIATE Immediate Children – Select direct children of currently selected bones.

PARENT Parents – Select the parents of currently selected bones.

SIBLINGS Siblings – Select all bones that have the same parent as currently selected bones.

Select immediate parent/children of selected bones

direction (enum in ['PARENT', 'CHILD'], (optional)) – Direction

extend (boolean, (optional)) – Extend, Extend the selection

Select all bones linked by parent/child connections to the current selection

Select bones linked by parent/child connections under the mouse cursor

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

Mirror the bone selection

only_active (boolean, (optional)) – Active Only, Only operate on the active bone

extend (boolean, (optional)) – Extend, Extend the selection

Select bones that are parents of the currently selected bones

Create a new empty Selection Set

startup/bl_operators/bone_selection_sets.py:147

Create a new Selection Set with the currently selected bones

startup/bl_operators/bone_selection_sets.py:278

Add selected bones to Selection Set

startup/bl_operators/bone_selection_sets.py:194

Copy the selected Selection Set(s) to the clipboard

startup/bl_operators/bone_selection_sets.py:290

Remove all Selection Sets from this Armature

startup/bl_operators/bone_selection_sets.py:77

Remove Selection Set bones from current selection

startup/bl_operators/bone_selection_sets.py:261

Move the active Selection Set up/down the list of sets

direction (enum in ['UP', 'DOWN'], (optional)) – Move Direction, Direction to move the active Selection Set: UP (default) or DOWN

startup/bl_operators/bone_selection_sets.py:126

Add new Selection Set(s) from the clipboard

startup/bl_operators/bone_selection_sets.py:302

Remove a Selection Set from this Armature

startup/bl_operators/bone_selection_sets.py:165

Remove the selected bones from all Selection Sets

startup/bl_operators/bone_selection_sets.py:89

Select the bones from this Selection Set

selection_set_index (int in [-inf, inf], (optional)) – Selection Set Index, Which Selection Set to select; -1 uses the active Selection Set

startup/bl_operators/bone_selection_sets.py:239

Remove selected bones from Selection Set

startup/bl_operators/bone_selection_sets.py:213

Reset location, rotation, and scaling of selected bones to their default values

Reset pose bone transforms to keyframed state

only_selected (boolean, (optional)) – Only Selected, Only visible/selected bones

Apply final constrained position of pose bones to their transform

---

## Preferences Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.preferences.html

**Contents:**
- Preferences Operators¶

module (string, (optional, never None)) – Module, Module name of the add-on to disable

startup/bl_operators/userpref.py:547

module (string, (optional, never None)) – Module, Module name of the add-on to enable

startup/bl_operators/userpref.py:483

Display information and preferences for this add-on

module (string, (optional, never None)) – Module, Module name of the add-on to expand

startup/bl_operators/userpref.py:924

overwrite (boolean, (optional)) – Overwrite, Remove existing add-ons with the same ID

enable_on_install (boolean, (optional)) – Enable on Install, Enable after installing

target (enum in [], (optional)) – Target Path

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_python (boolean, (optional)) – Filter Python

filter_glob (string, (optional, never None)) – filter_glob

startup/bl_operators/userpref.py:712

Scan add-on directories for new modules

startup/bl_operators/userpref.py:645

Delete the add-on from the file system

module (string, (optional, never None)) – Module, Module name of the add-on to remove

startup/bl_operators/userpref.py:873

Show add-on preferences

module (string, (optional, never None)) – Module, Module name of the add-on to expand

startup/bl_operators/userpref.py:950

Install an application template

overwrite (boolean, (optional)) – Overwrite, Remove existing template with the same ID

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_glob (string, (optional, never None)) – filter_glob

startup/bl_operators/userpref.py:1000

Add a directory to be used by the Asset Browser as source of assets

directory (string, (optional, never None)) – Directory, Directory of the file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Remove a path to a .blend file, so the Asset Browser will not attempt to show it anymore

index (int in [0, inf], (optional)) – Index

Use this installation for .blend files and to display thumbnails

Add path to exclude from auto-execution

Remove path to exclude from auto-execution

index (int in [0, inf], (optional)) – Index

Copy settings from previous version

startup/bl_operators/userpref.py:170

Add a new repository used to store extensions

name (string, (optional, never None)) – Name, Unique repository name

remote_url (string, (optional, never None)) – URL, Remote URL to the extension repository, the file-system may be referenced using the file URI scheme: “file://”

use_access_token (boolean, (optional)) – Requires Access Token, Repository requires an access token

access_token (string, (optional, never None)) – Secret, Personal access token, may be required by some repositories

use_sync_on_startup (boolean, (optional)) – Check for Updates on Startup, Allow Blender to check for updates upon launch

use_custom_directory (boolean, (optional)) – Custom Directory, Manually set the path for extensions to be stored. When disabled a user’s extensions directory is created.

custom_directory (string, (optional, never None)) – Custom Directory, The local directory containing extensions

type (enum in ['REMOTE', 'LOCAL'], (optional)) – Type, The kind of repository to add REMOTE Add Remote Repository – Add a repository referencing a remote repository with support for listing and updating extensions. LOCAL Add Local Repository – Add a repository managed manually without referencing an external repository.

Type, The kind of repository to add

REMOTE Add Remote Repository – Add a repository referencing a remote repository with support for listing and updating extensions.

LOCAL Add Local Repository – Add a repository managed manually without referencing an external repository.

Remove an extension repository

index (int in [0, inf], (optional)) – Index

remove_files (boolean, (optional)) – Remove Files, Remove extension files when removing the repository

Handle dropping an extension URL

url (string, (optional, never None)) – URL, Location of the extension to install

Undocumented, consider contributing.

filepath (string, (optional, never None)) – filepath

startup/bl_operators/userpref.py:91

Export key configuration to a Python script

all (boolean, (optional)) – All Keymaps, Write all keymaps (not just user modified)

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_text (boolean, (optional)) – Filter text

filter_python (boolean, (optional)) – Filter Python

startup/bl_operators/userpref.py:324

Import key configuration from a Python script

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_text (boolean, (optional)) – Filter text

filter_python (boolean, (optional)) – Filter Python

keep_original (boolean, (optional)) – Keep Original, Keep original file after copying to configuration folder

startup/bl_operators/userpref.py:259

startup/bl_operators/userpref.py:463

Test key configuration for conflicts

startup/bl_operators/userpref.py:194

startup/bl_operators/userpref.py:411

item_id (int in [-inf, inf], (optional)) – Item Identifier, Identifier of the item to remove

startup/bl_operators/userpref.py:443

item_id (int in [-inf, inf], (optional)) – Item Identifier, Identifier of the item to restore

startup/bl_operators/userpref.py:395

all (boolean, (optional)) – All Keymaps, Restore all keymaps to default

startup/bl_operators/userpref.py:366

Reset to the default theme colors

Undocumented, consider contributing.

directory (string, (optional, never None)) – directory

filter_folder (boolean, (optional)) – Filter Folders

startup/bl_operators/userpref.py:1256

Undocumented, consider contributing.

index (int in [-inf, inf], (optional)) – Index, Index of the script directory to remove

startup/bl_operators/userpref.py:1286

Copy Studio Light settings to the Studio Light editor

index (int in [-inf, inf], (optional)) – index

startup/bl_operators/userpref.py:1227

Install a user defined light

files (bpy_prop_collection of OperatorFileListElement, (optional)) – File Path

directory (string, (optional, never None)) – directory

filter_folder (boolean, (optional)) – Filter Folders

filter_glob (string, (optional, never None)) – filter_glob

type (enum in ['MATCAP', 'WORLD', 'STUDIO'], (optional)) – Type MATCAP MatCap – Install custom MatCaps. WORLD World – Install custom HDRIs. STUDIO Studio – Install custom Studio Lights.

MATCAP MatCap – Install custom MatCaps.

WORLD World – Install custom HDRIs.

STUDIO Studio – Install custom Studio Lights.

startup/bl_operators/userpref.py:1110

Save custom studio light from the studio light editor settings

filename (string, (optional, never None)) – Name

startup/bl_operators/userpref.py:1157

index (int in [-inf, inf], (optional)) – index

startup/bl_operators/userpref.py:1208

Load and apply a Blender XML theme file

overwrite (boolean, (optional)) – Overwrite, Remove existing theme file if exists

filepath (string, (optional, never None)) – filepath

filter_folder (boolean, (optional)) – Filter folders

filter_glob (string, (optional, never None)) – filter_glob

startup/bl_operators/userpref.py:598

Remove this installation’s associations with .blend files

---

## Poselib Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.poselib.html

**Contents:**
- Poselib Operators¶

Apply the given Pose Action to the rig

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

blend_factor (float in [-inf, inf], (optional)) – Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it

flipped (boolean, (optional)) – Apply Flipped, When enabled, applies the pose flipped over the X-axis

Delete the selected Pose Asset

Update the selected pose asset in the asset library from the currently selected bones. The mode defines how the asset is updated

mode (enum in ['ADJUST', 'REPLACE', 'ADD', 'REMOVE'], (optional)) – Overwrite Mode, Specify which parts of the pose asset are overwritten ADJUST Adjust – Update existing channels in the pose asset but don’t remove or add any channels. REPLACE Replace with Selection – Completely replace all channels in the pose asset with the current selection. ADD Add Selected Bones – Add channels of the selection to the pose asset. Existing channels will be updated. REMOVE Remove Selected Bones – Remove channels of the selection from the pose asset.

Overwrite Mode, Specify which parts of the pose asset are overwritten

ADJUST Adjust – Update existing channels in the pose asset but don’t remove or add any channels.

REPLACE Replace with Selection – Completely replace all channels in the pose asset with the current selection.

ADD Add Selected Bones – Add channels of the selection to the pose asset. Existing channels will be updated.

REMOVE Remove Selected Bones – Remove channels of the selection from the pose asset.

Blend the given Pose Action to the rig

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

blend_factor (float in [-inf, inf], (optional)) – Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it

flipped (boolean, (optional)) – Apply Flipped, When enabled, applies the pose flipped over the X-axis

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

Create a new pose asset on the clipboard, to be pasted into an Asset Browser

addons_core/pose_library/operators.py:116

Create a new asset from the selected bones in the scene

pose_name (string, (optional, never None)) – Pose Name, Name for the new pose asset

asset_library_reference (enum in [], (optional)) – Library, Asset library used to store the new pose

catalog_path (string, (optional, never None)) – Catalog, Catalog to use for the new asset

Paste the Asset that was previously copied using Copy As Asset

addons_core/pose_library/operators.py:190

Select those bones that are used in this pose

select (boolean, (optional)) – Select

flipped (boolean, (optional)) – Flipped

addons_core/pose_library/operators.py:228

Switch back to the previous Action, after creating a pose asset

addons_core/pose_library/operators.py:65

---

## Ptcache Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.ptcache.html

**Contents:**
- Ptcache Operators¶

bake (boolean, (optional)) – Bake

bake (boolean, (optional)) – Bake

Delete all baked caches of all objects in the current scene

---

## Render Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.render.html

**Contents:**
- Render Operators¶

Add or remove a white balance preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add an Integrator Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add an Performance Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add a Sampling Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add a Viewport Sampling Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add or remove an EEVEE ray-tracing preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Take a snapshot of the active viewport

animation (boolean, (optional)) – Animation, Render files from the animation range of this scene

render_keyed_only (boolean, (optional)) – Render Keyframes Only, Render only those frames where selected objects have a key in their animation data. Only used when rendering animation

sequencer (boolean, (optional)) – Sequencer, Render using the sequencer’s OpenGL display

write_still (boolean, (optional)) – Write Image, Save the rendered image to the output path (used only when animation is disabled)

view_context (boolean, (optional)) – View Context, Use the current 3D view for rendering, else use scene settings

Play back rendered frames/movies using an external player

startup/bl_operators/screen_play_rendered_anim.py:87

Add or remove a Render Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Undocumented, consider contributing.

animation (boolean, (optional)) – Animation, Render files from the animation range of this scene

write_still (boolean, (optional)) – Write Image, Save the rendered image to the output path (used only when animation is disabled)

use_viewport (boolean, (optional)) – Use 3D Viewport, When inside a 3D viewport, use layers and camera of the viewport

use_sequencer_scene (boolean, (optional)) – Use Sequencer Scene, Render the sequencer scene instead of the active scene

layer (string, (optional, never None)) – Render Layer, Single render layer to re-render (used only when animation is disabled)

scene (string, (optional, never None)) – Scene, Scene to render, current scene if not specified

frame_start (int in [-inf, inf], (optional)) – Start Frame, Frame to start rendering animation at. If not specified, the scene start frame will be assumed. This should only be specified if doing an animation render

frame_end (int in [-inf, inf], (optional)) – End Frame, Frame to end rendering animation at. If not specified, the scene end frame will be assumed. This should only be specified if doing an animation render

shape (enum in ['SHARP', 'SMOOTH', 'MAX', 'LINE', 'ROUND', 'ROOT'], (optional)) – Mode

Cancel show render view

Toggle show render view

---

## Rigidbody Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.rigidbody.html

**Contents:**
- Rigidbody Operators¶

Bake rigid body transformations of selected objects to keyframes

frame_start (int in [0, 300000], (optional)) – Start Frame, Start frame for baking

frame_end (int in [1, 300000], (optional)) – End Frame, End frame for baking

step (int in [1, 120], (optional)) – Frame Step, Frame Step

startup/bl_operators/rigidbody.py:108

Create rigid body constraints between selected rigid bodies

con_type (enum in ['FIXED', 'POINT', 'HINGE', 'SLIDER', 'PISTON', 'GENERIC', 'GENERIC_SPRING', 'MOTOR'], (optional)) – Type, Type of generated constraint FIXED Fixed – Glue rigid bodies together. POINT Point – Constrain rigid bodies to move around common pivot point. HINGE Hinge – Restrict rigid body rotation to one axis. SLIDER Slider – Restrict rigid body translation to one axis. PISTON Piston – Restrict rigid body translation and rotation to one axis. GENERIC Generic – Restrict translation and rotation to specified axes. GENERIC_SPRING Generic Spring – Restrict translation and rotation to specified axes with springs. MOTOR Motor – Drive rigid body around or along an axis.

Type, Type of generated constraint

FIXED Fixed – Glue rigid bodies together.

POINT Point – Constrain rigid bodies to move around common pivot point.

HINGE Hinge – Restrict rigid body rotation to one axis.

SLIDER Slider – Restrict rigid body translation to one axis.

PISTON Piston – Restrict rigid body translation and rotation to one axis.

GENERIC Generic – Restrict translation and rotation to specified axes.

GENERIC_SPRING Generic Spring – Restrict translation and rotation to specified axes with springs.

MOTOR Motor – Drive rigid body around or along an axis.

pivot_type (enum in ['CENTER', 'ACTIVE', 'SELECTED'], (optional)) – Location, Constraint pivot location CENTER Center – Pivot location is between the constrained rigid bodies. ACTIVE Active – Pivot location is at the active object position. SELECTED Selected – Pivot location is at the selected object position.

Location, Constraint pivot location

CENTER Center – Pivot location is between the constrained rigid bodies.

ACTIVE Active – Pivot location is at the active object position.

SELECTED Selected – Pivot location is at the selected object position.

connection_pattern (enum in ['SELECTED_TO_ACTIVE', 'CHAIN_DISTANCE'], (optional)) – Connection Pattern, Pattern used to connect objects SELECTED_TO_ACTIVE Selected to Active – Connect selected objects to the active object. CHAIN_DISTANCE Chain by Distance – Connect objects as a chain based on distance, starting at the active object.

Connection Pattern, Pattern used to connect objects

SELECTED_TO_ACTIVE Selected to Active – Connect selected objects to the active object.

CHAIN_DISTANCE Chain by Distance – Connect objects as a chain based on distance, starting at the active object.

startup/bl_operators/rigidbody.py:277

Add Rigid Body Constraint to active object

type (enum in Rigidbody Constraint Type Items, (optional)) – Rigid Body Constraint Type

Remove Rigid Body Constraint from Object

Automatically calculate mass values for Rigid Body Objects based on volume

material (enum in ['DEFAULT'], (optional)) – Material Preset, Type of material that objects are made of (determines material density)

density (float in [1.17549e-38, inf], (optional)) – Density, Density value (kg/m^3), allows custom value if the ‘Custom’ preset is used

Add active object as Rigid Body

type (enum in Rigidbody Object Type Items, (optional)) – Rigid Body Type

Remove Rigid Body settings from Object

Copy Rigid Body settings from active object to selected

startup/bl_operators/rigidbody.py:45

Add selected objects as Rigid Bodies

type (enum in Rigidbody Object Type Items, (optional)) – Rigid Body Type

Remove selected objects from Rigid Body simulation

Change collision shapes for selected Rigid Body Objects

type (enum in Rigidbody Object Shape Items, (optional)) – Rigid Body Shape

Add Rigid Body simulation world to the current scene

Remove Rigid Body simulation world from the current scene

---

## Screen Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.screen.html

**Contents:**
- Screen Operators¶

Handle area action zones for mouse actions/gestures

modifier (int in [0, 2], (optional)) – Modifier, Modifier state

Cancel animation, returning to the original frame

restore_frame (boolean, (optional)) – Restore Frame, Restore the frame when animation was initialized

reverse (boolean, (optional)) – Play in Reverse, Animation is played backwards

sync (boolean, (optional)) – Sync, Drop frames to maintain framerate

Step through animation by position

Duplicate selected area into new window

Join selected areas into new window

source_xy (int array of 2 items in [-inf, inf], (optional)) – Source location

target_xy (int array of 2 items in [-inf, inf], (optional)) – Target location

Move selected area edges

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

delta (int in [-inf, inf], (optional)) – Delta

Operations for splitting and merging

Split selected area into new windows

direction (enum in ['HORIZONTAL', 'VERTICAL'], (optional)) – Direction

factor (float in [0, 1], (optional)) – Factor

cursor (int array of 2 items in [-inf, inf], (optional)) – Cursor

Swap selected areas screen positions

cursor (int array of 2 items in [-inf, inf], (optional)) – Cursor

Revert back to the original screen layout, before fullscreen area overlay

Show drivers editor in a separate window

Jump to first/last frame in frame range

end (boolean, (optional)) – Last Frame, Jump to the last frame of the frame range

Move current frame forward/backward by a given number

delta (int in [-inf, inf], (optional)) – Delta

Expand or collapse the header pull-down menus

Show info log in a separate window

Jump to previous/next keyframe

next (boolean, (optional)) – Next Keyframe

Jump to previous/next marker

next (boolean, (optional)) – Next Marker

Display parameters for last action performed

Blend in and out overlapping region

Display region context menu

Toggle the region’s alignment (left/right or top/bottom)

Split selected area into camera, front, right, and top views

Hide or unhide the region

region_type (enum in Region Type Items, (optional)) – Region Type, Type of the region to toggle

Display menu for previous actions performed

index (int in [0, inf], (optional)) – Index

Toggle display selected area as fullscreen/maximized

use_hide_panels (boolean, (optional)) – Hide Panels, Hide all the panels (Focus Mode)

Cycle through available screens

delta (int in [-1, 1], (optional)) – Delta

Capture a picture of the whole Blender window

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Capture a picture of an editor

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Cycle through the editor context by activating the next/previous one

direction (enum in ['PREV', 'NEXT'], (optional)) – Direction, Direction to cycle through

Set the space type or cycle subtype

space_type (enum in Space Type Items, (optional)) – Type

Remove unused settings for invisible editors

Jump forward/backward by a given number of frames or seconds

backward (boolean, (optional)) – Backwards, Jump backwards in time

Edit user preferences and system settings

section (enum in Preference Section Items, (optional)) – Section to activate in the Preferences

Cycle through workspaces

direction (enum in ['PREV', 'NEXT'], (optional)) – Direction, Direction to cycle through

---

## Scene Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.scene.html

**Contents:**
- Scene Operators¶

Import scene and set it as the active one in the window

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Add the data paths to the Freestyle Edge Mark property of selected edges to the active keying set

startup/bl_operators/freestyle.py:139

Add the data paths to the Freestyle Face Mark property of selected polygons to the active keying set

startup/bl_operators/freestyle.py:170

Add an alpha transparency modifier to the line style associated with the active lineset

type (enum in Linestyle Alpha Modifier Type Items, (optional)) – Type

Add a line color modifier to the line style associated with the active lineset

type (enum in Linestyle Color Modifier Type Items, (optional)) – Type

Fill the Range Min/Max entries by the min/max distance between selected mesh objects and the source object (either a user-specified object or the active camera)

type (enum in ['COLOR', 'ALPHA', 'THICKNESS'], (optional)) – Type, Type of the modifier to work on COLOR Color – Color modifier type. ALPHA Alpha – Alpha modifier type. THICKNESS Thickness – Thickness modifier type.

Type, Type of the modifier to work on

COLOR Color – Color modifier type.

ALPHA Alpha – Alpha modifier type.

THICKNESS Thickness – Thickness modifier type.

name (string, (optional, never None)) – Name, Name of the modifier to work on

startup/bl_operators/freestyle.py:45

Add a stroke geometry modifier to the line style associated with the active lineset

type (enum in Linestyle Geometry Modifier Type Items, (optional)) – Type

Add a line set into the list of line sets

Copy the active line set to the internal clipboard

Change the position of the active line set within the list of line sets

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the active line set towards

Paste the internal clipboard content to the active line set

Remove the active line set from the list of line sets

Create a new line style, reusable by multiple line sets

Duplicate the modifier within the list of modifiers

Move the modifier within the list of modifiers

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the chosen modifier towards

Remove the modifier from the list of modifiers

Add a style module into the list of modules

Change the position of the style module within in the list of style modules

direction (enum in ['UP', 'DOWN'], (optional)) – Direction, Direction to move the chosen style module towards

Open a style module file

filepath (string, (optional, never None)) – filepath

make_internal (boolean, (optional)) – Make internal, Make module file internal after loading

startup/bl_operators/freestyle.py:215

Remove the style module from the stack

Create Freestyle stroke material for testing

Add a line thickness modifier to the line style associated with the active lineset

type (enum in Linestyle Thickness Modifier Type Items, (optional)) – Type

Refresh list of actions

addons_core/io_scene_gltf2/blender/com/gltf2_blender_ui.py:606

Add or remove Grease Pencil brush preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add or remove Grease Pencil material preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Add new scene by type

type (enum in ['NEW', 'EMPTY', 'LINK_COPY', 'FULL_COPY'], (optional)) – Type NEW New – Add a new, empty scene with default settings. EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene. LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy). FULL_COPY Full Copy – Make a full copy of the current scene.

NEW New – Add a new, empty scene with default settings.

EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene.

LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy).

FULL_COPY Full Copy – Make a full copy of the current scene.

Add new scene by type in the sequence editor and assign to active strip

type (enum in ['NEW', 'EMPTY', 'LINK_COPY', 'FULL_COPY'], (optional)) – Type NEW New – Add a new, empty scene with default settings. EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene. LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy). FULL_COPY Full Copy – Make a full copy of the current scene.

NEW New – Add a new, empty scene with default settings.

EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene.

LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy).

FULL_COPY Full Copy – Make a full copy of the current scene.

Add new scene to be used by the sequencer

type (enum in ['NEW', 'EMPTY', 'LINK_COPY', 'FULL_COPY'], (optional)) – Type NEW New – Add a new, empty scene with default settings. EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene. LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy). FULL_COPY Full Copy – Make a full copy of the current scene.

NEW New – Add a new, empty scene with default settings.

EMPTY Copy Settings – Add a new, empty scene, and copy settings from the current scene.

LINK_COPY Linked Copy – Link in the collections from the current scene (shallow copy).

FULL_COPY Full Copy – Make a full copy of the current scene.

Remove the selected render view

type (enum in ['NEW', 'COPY', 'EMPTY'], (optional)) – Type NEW New – Add a new view layer. COPY Copy Settings – Copy settings of current view layer. EMPTY Blank – Add a new view layer with all collections disabled.

NEW New – Add a new view layer.

COPY Copy Settings – Copy settings of current view layer.

EMPTY Blank – Add a new view layer with all collections disabled.

name (string, (optional, never None)) – Name, Name of newly created lightgroup

Add all used Light Groups

Remove the selected view layer

Remove Active Lightgroup

Remove all unused Light Groups

---

## Script Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.script.html

**Contents:**
- Script Operators¶

filepath (string, (optional, never None)) – filepath

menu_idname (string, (optional, never None)) – Menu ID Name, ID name of the menu this was called from

startup/bl_operators/presets.py:285

filepath (string, (optional, never None)) – Path

---

## Sculpt Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.sculpt.html

**Contents:**
- Sculpt Operators¶

Sculpt a stroke into the geometry

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

override_location (boolean, (optional)) – Override Location, Override the given “location” array by recalculating object space positions from the provided “mouse_event” positions

ignore_background_click (boolean, (optional)) – Ignore Background Click, Clicks on the background do not start the stroke

Applies a cloth simulation deformation to the entire mesh

start_mouse (int array of 2 items in [0, 16384], (optional)) – Starting Mouse

area_normal_radius (float in [0.001, 5], (optional)) – Normal Radius, Radius used for calculating area normal on initial click,in percentage of brush radius

strength (float in [-10, 10], (optional)) – Strength, Filter strength

iteration_count (int in [1, 10000], (optional)) – Repeat, How many times to repeat the filter

type (enum in ['GRAVITY', 'INFLATE', 'EXPAND', 'PINCH', 'SCALE'], (optional)) – Filter Type, Operation that is going to be applied to the mesh GRAVITY Gravity – Applies gravity to the simulation. INFLATE Inflate – Inflates the cloth. EXPAND Expand – Expands the cloth’s dimensions. PINCH Pinch – Pulls the cloth to the cursor’s start position. SCALE Scale – Scales the mesh as a soft body using the origin of the object as scale.

Filter Type, Operation that is going to be applied to the mesh

GRAVITY Gravity – Applies gravity to the simulation.

INFLATE Inflate – Inflates the cloth.

EXPAND Expand – Expands the cloth’s dimensions.

PINCH Pinch – Pulls the cloth to the cursor’s start position.

SCALE Scale – Scales the mesh as a soft body using the origin of the object as scale.

force_axis (enum set in {'X', 'Y', 'Z'}, (optional)) – Force Axis, Apply the force in the selected axis X X – Apply force in the X axis. Y Y – Apply force in the Y axis. Z Z – Apply force in the Z axis.

Force Axis, Apply the force in the selected axis

X X – Apply force in the X axis.

Y Y – Apply force in the Y axis.

Z Z – Apply force in the Z axis.

orientation (enum in ['LOCAL', 'WORLD', 'VIEW'], (optional)) – Orientation, Orientation of the axis to limit the filter force LOCAL Local – Use the local axis to limit the force and set the gravity direction. WORLD World – Use the global axis to limit the force and set the gravity direction. VIEW View – Use the view axis to limit the force and set the gravity direction.

Orientation, Orientation of the axis to limit the filter force

LOCAL Local – Use the local axis to limit the force and set the gravity direction.

WORLD World – Use the global axis to limit the force and set the gravity direction.

VIEW View – Use the view axis to limit the force and set the gravity direction.

cloth_mass (float in [0, 2], (optional)) – Cloth Mass, Mass of each simulation particle

cloth_damping (float in [0, 1], (optional)) – Cloth Damping, How much the applied forces are propagated through the cloth

use_face_sets (boolean, (optional)) – Use Face Sets, Apply the filter only to the Face Set under the cursor

use_collisions (boolean, (optional)) – Use Collisions, Collide with other collider objects in the scene

Applies a filter to modify the active color attribute

start_mouse (int array of 2 items in [0, 16384], (optional)) – Starting Mouse

area_normal_radius (float in [0.001, 5], (optional)) – Normal Radius, Radius used for calculating area normal on initial click,in percentage of brush radius

strength (float in [-10, 10], (optional)) – Strength, Filter strength

iteration_count (int in [1, 10000], (optional)) – Repeat, How many times to repeat the filter

type (enum in ['FILL', 'HUE', 'SATURATION', 'VALUE', 'BRIGHTNESS', 'CONTRAST', 'SMOOTH', 'RED', 'GREEN', 'BLUE'], (optional)) – Filter Type FILL Fill – Fill with a specific color. HUE Hue – Change hue. SATURATION Saturation – Change saturation. VALUE Value – Change value. BRIGHTNESS Brightness – Change brightness. CONTRAST Contrast – Change contrast. SMOOTH Smooth – Smooth colors. RED Red – Change red channel. GREEN Green – Change green channel. BLUE Blue – Change blue channel.

FILL Fill – Fill with a specific color.

HUE Hue – Change hue.

SATURATION Saturation – Change saturation.

VALUE Value – Change value.

BRIGHTNESS Brightness – Change brightness.

CONTRAST Contrast – Change contrast.

SMOOTH Smooth – Smooth colors.

RED Red – Change red channel.

GREEN Green – Change green channel.

BLUE Blue – Change blue channel.

fill_color (mathutils.Color of 3 items in [0, inf], (optional)) – Fill Color

Flood fill the mesh with the selected detail setting

Dynamic topology alters the mesh topology while sculpting

Modify the detail size of dyntopo interactively

Generic sculpt expand operator

target (enum in ['MASK', 'FACE_SETS', 'COLOR'], (optional)) – Data Target, Data that is going to be modified in the expand operation

falloff_type (enum in ['GEODESIC', 'TOPOLOGY', 'TOPOLOGY_DIAGONALS', 'NORMALS', 'SPHERICAL', 'BOUNDARY_TOPOLOGY', 'BOUNDARY_FACE_SET', 'ACTIVE_FACE_SET'], (optional)) – Falloff Type, Initial falloff of the expand operation

invert (boolean, (optional)) – Invert, Invert the expand active elements

use_mask_preserve (boolean, (optional)) – Preserve Previous, Preserve the previous state of the target data

use_falloff_gradient (boolean, (optional)) – Falloff Gradient, Expand Using a linear falloff

use_modify_active (boolean, (optional)) – Modify Active, Modify the active Face Set instead of creating a new one

use_reposition_pivot (boolean, (optional)) – Reposition Pivot, Reposition the sculpt transform pivot to the boundary of the expand active area

max_geodesic_move_preview (int in [0, inf], (optional)) – Max Vertex Count for Geodesic Move Preview, Maximum number of vertices in the mesh for using geodesic falloff when moving the origin of expand. If the total number of vertices is greater than this value, the falloff will be set to spherical when moving

use_auto_mask (boolean, (optional)) – Auto Create, Fill in mask if nothing is already masked

normal_falloff_smooth (int in [0, 10], (optional)) – Normal Smooth, Blurring steps for normal falloff

Add a face set in a rectangle defined by the cursor

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Change the visibility of the Face Sets of the sculpt

mode (enum in ['TOGGLE', 'SHOW_ACTIVE', 'HIDE_ACTIVE'], (optional)) – Mode TOGGLE Toggle Visibility – Hide all Face Sets except for the active one. SHOW_ACTIVE Show Active Face Set – Show Active Face Set. HIDE_ACTIVE Hide Active Face Sets – Hide Active Face Sets.

TOGGLE Toggle Visibility – Hide all Face Sets except for the active one.

SHOW_ACTIVE Show Active Face Set – Show Active Face Set.

HIDE_ACTIVE Hide Active Face Sets – Hide Active Face Sets.

Edits the current active Face Set

active_face_set (int in [0, inf], (optional)) – Active Face Set

mode (enum in ['GROW', 'SHRINK', 'DELETE_GEOMETRY', 'FAIR_POSITIONS', 'FAIR_TANGENCY'], (optional)) – Mode GROW Grow Face Set – Grows the Face Sets boundary by one face based on mesh topology. SHRINK Shrink Face Set – Shrinks the Face Sets boundary by one face based on mesh topology. DELETE_GEOMETRY Delete Geometry – Deletes the faces that are assigned to the Face Set. FAIR_POSITIONS Fair Positions – Creates a smooth as possible geometry patch from the Face Set minimizing changes in vertex positions. FAIR_TANGENCY Fair Tangency – Creates a smooth as possible geometry patch from the Face Set minimizing changes in vertex tangents.

GROW Grow Face Set – Grows the Face Sets boundary by one face based on mesh topology.

SHRINK Shrink Face Set – Shrinks the Face Sets boundary by one face based on mesh topology.

DELETE_GEOMETRY Delete Geometry – Deletes the faces that are assigned to the Face Set.

FAIR_POSITIONS Fair Positions – Creates a smooth as possible geometry patch from the Face Set minimizing changes in vertex positions.

FAIR_TANGENCY Fair Tangency – Creates a smooth as possible geometry patch from the Face Set minimizing changes in vertex tangents.

strength (float in [0, 1], (optional)) – Strength

modify_hidden (boolean, (optional)) – Modify Hidden, Apply the edit operation to hidden geometry

Create a new mesh object from the selected Face Set

add_boundary_loop (boolean, (optional)) – Add Boundary Loop, Add an extra edge loop to better preserve the shape when applying a subdivision surface modifier

smooth_iterations (int in [0, inf], (optional)) – Smooth Iterations, Smooth iterations applied to the extracted mesh

apply_shrinkwrap (boolean, (optional)) – Project to Sculpt, Project the extracted mesh into the original sculpt

add_solidify (boolean, (optional)) – Extract as Solid, Extract the mask as a solid object with a solidify modifier

Add a face set in a shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Add a face set to one side of a line defined by the cursor

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

use_limit_to_segment (boolean, (optional)) – Limit to Segment, Apply the gesture action only to the area that is contained within the segment without extending its effect to the entire line

Add a face set in a shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

Create a new Face Set

mode (enum in ['MASKED', 'VISIBLE', 'ALL', 'SELECTION'], (optional)) – Mode MASKED Face Set from Masked – Create a new Face Set from the masked faces. VISIBLE Face Set from Visible – Create a new Face Set from the visible vertices. ALL Face Set Full Mesh – Create an unique Face Set with all faces in the sculpt. SELECTION Face Set from Edit Mode Selection – Create an Face Set corresponding to the Edit Mode face selection.

MASKED Face Set from Masked – Create a new Face Set from the masked faces.

VISIBLE Face Set from Visible – Create a new Face Set from the visible vertices.

ALL Face Set Full Mesh – Create an unique Face Set with all faces in the sculpt.

SELECTION Face Set from Edit Mode Selection – Create an Face Set corresponding to the Edit Mode face selection.

Initializes all Face Sets in the mesh

mode (enum in ['LOOSE_PARTS', 'MATERIALS', 'NORMALS', 'UV_SEAMS', 'CREASES', 'BEVEL_WEIGHT', 'SHARP_EDGES', 'FACE_SET_BOUNDARIES'], (optional)) – Mode LOOSE_PARTS Face Sets from Loose Parts – Create a Face Set per loose part in the mesh. MATERIALS Face Sets from Material Slots – Create a Face Set per Material Slot. NORMALS Face Sets from Mesh Normals – Create Face Sets for Faces that have similar normal. UV_SEAMS Face Sets from UV Seams – Create Face Sets using UV Seams as boundaries. CREASES Face Sets from Edge Creases – Create Face Sets using Edge Creases as boundaries. BEVEL_WEIGHT Face Sets from Bevel Weight – Create Face Sets using Bevel Weights as boundaries. SHARP_EDGES Face Sets from Sharp Edges – Create Face Sets using Sharp Edges as boundaries. FACE_SET_BOUNDARIES Face Sets from Face Set Boundaries – Create a Face Set per isolated Face Set.

LOOSE_PARTS Face Sets from Loose Parts – Create a Face Set per loose part in the mesh.

MATERIALS Face Sets from Material Slots – Create a Face Set per Material Slot.

NORMALS Face Sets from Mesh Normals – Create Face Sets for Faces that have similar normal.

UV_SEAMS Face Sets from UV Seams – Create Face Sets using UV Seams as boundaries.

CREASES Face Sets from Edge Creases – Create Face Sets using Edge Creases as boundaries.

BEVEL_WEIGHT Face Sets from Bevel Weight – Create Face Sets using Bevel Weights as boundaries.

SHARP_EDGES Face Sets from Sharp Edges – Create Face Sets using Sharp Edges as boundaries.

FACE_SET_BOUNDARIES Face Sets from Face Set Boundaries – Create a Face Set per isolated Face Set.

threshold (float in [0, 1], (optional)) – Threshold, Minimum value to consider a certain attribute a boundary when creating the Face Sets

Generates a new set of random colors to render the Face Sets in the viewport

Creates a mask based on the active color attribute

contiguous (boolean, (optional)) – Contiguous, Mask only contiguous color areas

invert (boolean, (optional)) – Invert, Invert the generated mask

preserve_previous_mask (boolean, (optional)) – Preserve Previous Mask, Preserve the previous mask and add or subtract the new one generated by the colors

threshold (float in [0, 1], (optional)) – Threshold, How much changes in color affect the mask generation

location (int array of 2 items in [0, 32767], (optional)) – Location, Region coordinates of sampling

Applies a filter to modify the current mask

filter_type (enum in ['SMOOTH', 'SHARPEN', 'GROW', 'SHRINK', 'CONTRAST_INCREASE', 'CONTRAST_DECREASE'], (optional)) – Type, Filter that is going to be applied to the mask

iterations (int in [1, 100], (optional)) – Iterations, Number of times that the filter is going to be applied

auto_iteration_count (boolean, (optional)) – Auto Iteration Count, Use an automatic number of iterations based on the number of vertices of the sculpt

Creates a mask based on the boundaries of the surface

mix_mode (enum in ['MIX', 'MULTIPLY', 'DIVIDE', 'ADD', 'SUBTRACT'], (optional)) – Mode, Mix mode

mix_factor (float in [0, 5], (optional)) – Mix Factor

settings_source (enum in ['OPERATOR', 'BRUSH', 'SCENE'], (optional)) – Settings, Use settings from here OPERATOR Operator – Use settings from operator properties. BRUSH Brush – Use settings from brush. SCENE Scene – Use settings from scene.

Settings, Use settings from here

OPERATOR Operator – Use settings from operator properties.

BRUSH Brush – Use settings from brush.

SCENE Scene – Use settings from scene.

boundary_mode (enum in ['MESH', 'FACE_SETS'], (optional)) – Mode, Boundary type to mask MESH Mesh – Calculate the boundary mask based on disconnected mesh topology islands. FACE_SETS Face Sets – Calculate the boundary mask between face sets.

Mode, Boundary type to mask

MESH Mesh – Calculate the boundary mask based on disconnected mesh topology islands.

FACE_SETS Face Sets – Calculate the boundary mask between face sets.

propagation_steps (int in [1, 20], (optional)) – Propagation Steps

Creates a mask based on the curvature of the surface

mix_mode (enum in ['MIX', 'MULTIPLY', 'DIVIDE', 'ADD', 'SUBTRACT'], (optional)) – Mode, Mix mode

mix_factor (float in [0, 5], (optional)) – Mix Factor

settings_source (enum in ['OPERATOR', 'BRUSH', 'SCENE'], (optional)) – Settings, Use settings from here OPERATOR Operator – Use settings from operator properties. BRUSH Brush – Use settings from brush. SCENE Scene – Use settings from scene.

Settings, Use settings from here

OPERATOR Operator – Use settings from operator properties.

BRUSH Brush – Use settings from brush.

SCENE Scene – Use settings from scene.

factor (float in [0, 5], (optional)) – Factor, The contrast of the cavity mask

blur_steps (int in [0, 25], (optional)) – Blur, The number of times the cavity mask is blurred

use_curve (boolean, (optional)) – Custom Curve

invert (boolean, (optional)) – Cavity (Inverted)

Creates a new mask for the entire mesh

mode (enum in ['RANDOM_PER_VERTEX', 'RANDOM_PER_FACE_SET', 'RANDOM_PER_LOOSE_PART'], (optional)) – Mode

Applies a filter to modify the current mesh

start_mouse (int array of 2 items in [0, 16384], (optional)) – Starting Mouse

area_normal_radius (float in [0.001, 5], (optional)) – Normal Radius, Radius used for calculating area normal on initial click,in percentage of brush radius

strength (float in [-10, 10], (optional)) – Strength, Filter strength

iteration_count (int in [1, 10000], (optional)) – Repeat, How many times to repeat the filter

type (enum in ['SMOOTH', 'SCALE', 'INFLATE', 'SPHERE', 'RANDOM', 'RELAX', 'RELAX_FACE_SETS', 'SURFACE_SMOOTH', 'SHARPEN', 'ENHANCE_DETAILS', 'ERASE_DISPLACEMENT'], (optional)) – Filter Type, Operation that is going to be applied to the mesh SMOOTH Smooth – Smooth mesh. SCALE Scale – Scale mesh. INFLATE Inflate – Inflate mesh. SPHERE Sphere – Morph into sphere. RANDOM Random – Randomize vertex positions. RELAX Relax – Relax mesh. RELAX_FACE_SETS Relax Face Sets – Smooth the edges of all the Face Sets. SURFACE_SMOOTH Surface Smooth – Smooth the surface of the mesh, preserving the volume. SHARPEN Sharpen – Sharpen the cavities of the mesh. ENHANCE_DETAILS Enhance Details – Enhance the high frequency surface detail. ERASE_DISPLACEMENT Erase Displacement – Deletes the displacement of the Multires Modifier.

Filter Type, Operation that is going to be applied to the mesh

SMOOTH Smooth – Smooth mesh.

SCALE Scale – Scale mesh.

INFLATE Inflate – Inflate mesh.

SPHERE Sphere – Morph into sphere.

RANDOM Random – Randomize vertex positions.

RELAX Relax – Relax mesh.

RELAX_FACE_SETS Relax Face Sets – Smooth the edges of all the Face Sets.

SURFACE_SMOOTH Surface Smooth – Smooth the surface of the mesh, preserving the volume.

SHARPEN Sharpen – Sharpen the cavities of the mesh.

ENHANCE_DETAILS Enhance Details – Enhance the high frequency surface detail.

ERASE_DISPLACEMENT Erase Displacement – Deletes the displacement of the Multires Modifier.

deform_axis (enum set in {'X', 'Y', 'Z'}, (optional)) – Deform Axis, Apply the deformation in the selected axis X X – Deform in the X axis. Y Y – Deform in the Y axis. Z Z – Deform in the Z axis.

Deform Axis, Apply the deformation in the selected axis

X X – Deform in the X axis.

Y Y – Deform in the Y axis.

Z Z – Deform in the Z axis.

orientation (enum in ['LOCAL', 'WORLD', 'VIEW'], (optional)) – Orientation, Orientation of the axis to limit the filter displacement LOCAL Local – Use the local axis to limit the displacement. WORLD World – Use the global axis to limit the displacement. VIEW View – Use the view axis to limit the displacement.

Orientation, Orientation of the axis to limit the filter displacement

LOCAL Local – Use the local axis to limit the displacement.

WORLD World – Use the global axis to limit the displacement.

VIEW View – Use the view axis to limit the displacement.

surface_smooth_shape_preservation (float in [0, 1], (optional)) – Shape Preservation, How much of the original shape is preserved when smoothing

surface_smooth_current_vertex (float in [0, 1], (optional)) – Per Vertex Displacement, How much the position of each individual vertex influences the final result

sharpen_smooth_ratio (float in [0, 1], (optional)) – Smooth Ratio, How much smoothing is applied to polished surfaces

sharpen_intensify_detail_strength (float in [0, 10], (optional)) – Intensify Details, How much creases and valleys are intensified

sharpen_curvature_smooth_iterations (int in [0, 10], (optional)) – Curvature Smooth Iterations, How much smooth the resulting shape is, ignoring high frequency details

Recalculate the sculpt BVH to improve performance

Create a new mesh object from the current paint mask

mask_threshold (float in [0, 1], (optional)) – Threshold, Minimum mask value to consider the vertex valid to extract a face from the original mesh

add_boundary_loop (boolean, (optional)) – Add Boundary Loop, Add an extra edge loop to better preserve the shape when applying a subdivision surface modifier

smooth_iterations (int in [0, inf], (optional)) – Smooth Iterations, Smooth iterations applied to the extracted mesh

apply_shrinkwrap (boolean, (optional)) – Project to Sculpt, Project the extracted mesh into the original sculpt

add_solidify (boolean, (optional)) – Extract as Solid, Extract the mask as a solid object with a solidify modifier

Slices the paint mask from the mesh

mask_threshold (float in [0, 1], (optional)) – Threshold, Minimum mask value to consider the vertex valid to extract a face from the original mesh

fill_holes (boolean, (optional)) – Fill Holes, Fill holes after slicing the mask

new_object (boolean, (optional)) – Slice to New Object, Create a new object from the sliced mask

Project the geometry onto a plane defined by a line

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

use_limit_to_segment (boolean, (optional)) – Limit to Segment, Apply the gesture action only to the area that is contained within the segment without extending its effect to the entire line

Sample the vertex color of the active vertex

Sample the mesh detail on clicked point

location (int array of 2 items in [0, 32767], (optional)) – Location, Screen coordinates of sampling

mode (enum in ['DYNTOPO', 'VOXEL'], (optional)) – Detail Mode, Target sculpting workflow that is going to use the sampled size DYNTOPO Dyntopo – Sample dyntopo detail. VOXEL Voxel – Sample mesh voxel size.

Detail Mode, Target sculpting workflow that is going to use the sampled size

DYNTOPO Dyntopo – Sample dyntopo detail.

VOXEL Voxel – Sample mesh voxel size.

Toggle sculpt mode in 3D view

Reset the copy of the mesh that is being sculpted on

Sets the sculpt transform pivot position

mode (enum in ['ORIGIN', 'UNMASKED', 'BORDER', 'ACTIVE', 'SURFACE'], (optional)) – Mode ORIGIN Origin – Sets the pivot to the origin of the sculpt. UNMASKED Unmasked – Sets the pivot position to the average position of the unmasked vertices. BORDER Mask Border – Sets the pivot position to the center of the border of the mask. ACTIVE Active Vertex – Sets the pivot position to the active vertex position. SURFACE Surface – Sets the pivot position to the surface under the cursor.

ORIGIN Origin – Sets the pivot to the origin of the sculpt.

UNMASKED Unmasked – Sets the pivot position to the average position of the unmasked vertices.

BORDER Mask Border – Sets the pivot position to the center of the border of the mask.

ACTIVE Active Vertex – Sets the pivot position to the active vertex position.

SURFACE Surface – Sets the pivot position to the surface under the cursor.

mouse_x (float in [0, inf], (optional)) – Mouse Position X, Position of the mouse used for “Surface” and “Active Vertex” mode

mouse_y (float in [0, inf], (optional)) – Mouse Position Y, Position of the mouse used for “Surface” and “Active Vertex” mode

Symmetrize the topology modifications

merge_tolerance (float in [0, inf], (optional)) – Merge Distance, Distance within which symmetrical vertices are merged

Execute a boolean operation on the mesh and a rectangle defined by the cursor

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

trim_mode (enum in ['DIFFERENCE', 'UNION', 'JOIN'], (optional)) – Trim Mode DIFFERENCE Difference – Use a difference boolean operation. UNION Union – Use a union boolean operation. JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

DIFFERENCE Difference – Use a difference boolean operation.

UNION Union – Use a union boolean operation.

JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

use_cursor_depth (boolean, (optional)) – Use Cursor for Depth, Use cursor location and radius for the dimensions and position of the trimming shape

trim_orientation (enum in ['VIEW', 'SURFACE'], (optional)) – Shape Orientation VIEW View – Use the view to orientate the trimming shape. SURFACE Surface – Use the surface normal to orientate the trimming shape.

VIEW View – Use the view to orientate the trimming shape.

SURFACE Surface – Use the surface normal to orientate the trimming shape.

trim_extrude_mode (enum in ['PROJECT', 'FIXED'], (optional)) – Extrude Mode PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape. FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape.

FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

trim_solver (enum in ['EXACT', 'FLOAT', 'MANIFOLD'], (optional)) – Solver EXACT Exact – Slower solver with the best results for coplanar faces. FLOAT Float – Simple solver with good performance, without support for overlapping geometry. MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

EXACT Exact – Slower solver with the best results for coplanar faces.

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

Execute a boolean operation on the mesh and a shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

trim_mode (enum in ['DIFFERENCE', 'UNION', 'JOIN'], (optional)) – Trim Mode DIFFERENCE Difference – Use a difference boolean operation. UNION Union – Use a union boolean operation. JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

DIFFERENCE Difference – Use a difference boolean operation.

UNION Union – Use a union boolean operation.

JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

use_cursor_depth (boolean, (optional)) – Use Cursor for Depth, Use cursor location and radius for the dimensions and position of the trimming shape

trim_orientation (enum in ['VIEW', 'SURFACE'], (optional)) – Shape Orientation VIEW View – Use the view to orientate the trimming shape. SURFACE Surface – Use the surface normal to orientate the trimming shape.

VIEW View – Use the view to orientate the trimming shape.

SURFACE Surface – Use the surface normal to orientate the trimming shape.

trim_extrude_mode (enum in ['PROJECT', 'FIXED'], (optional)) – Extrude Mode PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape. FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape.

FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

trim_solver (enum in ['EXACT', 'FLOAT', 'MANIFOLD'], (optional)) – Solver EXACT Exact – Slower solver with the best results for coplanar faces. FLOAT Float – Simple solver with good performance, without support for overlapping geometry. MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

EXACT Exact – Slower solver with the best results for coplanar faces.

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

Remove a portion of the mesh on one side of a line

xstart (int in [-inf, inf], (optional)) – X Start

xend (int in [-inf, inf], (optional)) – X End

ystart (int in [-inf, inf], (optional)) – Y Start

yend (int in [-inf, inf], (optional)) – Y End

flip (boolean, (optional)) – Flip

cursor (int in [0, inf], (optional)) – Cursor, Mouse cursor style to use during the modal operator

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

use_limit_to_segment (boolean, (optional)) – Limit to Segment, Apply the gesture action only to the area that is contained within the segment without extending its effect to the entire line

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

trim_mode (enum in ['DIFFERENCE', 'UNION', 'JOIN'], (optional)) – Trim Mode DIFFERENCE Difference – Use a difference boolean operation. UNION Union – Use a union boolean operation. JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

DIFFERENCE Difference – Use a difference boolean operation.

UNION Union – Use a union boolean operation.

JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

use_cursor_depth (boolean, (optional)) – Use Cursor for Depth, Use cursor location and radius for the dimensions and position of the trimming shape

trim_orientation (enum in ['VIEW', 'SURFACE'], (optional)) – Shape Orientation VIEW View – Use the view to orientate the trimming shape. SURFACE Surface – Use the surface normal to orientate the trimming shape.

VIEW View – Use the view to orientate the trimming shape.

SURFACE Surface – Use the surface normal to orientate the trimming shape.

trim_extrude_mode (enum in ['PROJECT', 'FIXED'], (optional)) – Extrude Mode PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape. FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape.

FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

trim_solver (enum in ['EXACT', 'FLOAT', 'MANIFOLD'], (optional)) – Solver EXACT Exact – Slower solver with the best results for coplanar faces. FLOAT Float – Simple solver with good performance, without support for overlapping geometry. MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

EXACT Exact – Slower solver with the best results for coplanar faces.

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

Execute a boolean operation on the mesh and a polygonal shape defined by the cursor

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_front_faces_only (boolean, (optional)) – Front Faces Only, Affect only faces facing towards the view

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

trim_mode (enum in ['DIFFERENCE', 'UNION', 'JOIN'], (optional)) – Trim Mode DIFFERENCE Difference – Use a difference boolean operation. UNION Union – Use a union boolean operation. JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

DIFFERENCE Difference – Use a difference boolean operation.

UNION Union – Use a union boolean operation.

JOIN Join – Join the new mesh as separate geometry, without performing any boolean operation.

use_cursor_depth (boolean, (optional)) – Use Cursor for Depth, Use cursor location and radius for the dimensions and position of the trimming shape

trim_orientation (enum in ['VIEW', 'SURFACE'], (optional)) – Shape Orientation VIEW View – Use the view to orientate the trimming shape. SURFACE Surface – Use the surface normal to orientate the trimming shape.

VIEW View – Use the view to orientate the trimming shape.

SURFACE Surface – Use the surface normal to orientate the trimming shape.

trim_extrude_mode (enum in ['PROJECT', 'FIXED'], (optional)) – Extrude Mode PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape. FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

PROJECT Project – Align trim geometry with the perspective of the current view for a tapered shape.

FIXED Fixed – Align trim geometry orthogonally for a shape with 90 degree angles.

trim_solver (enum in ['EXACT', 'FLOAT', 'MANIFOLD'], (optional)) – Solver EXACT Exact – Slower solver with the best results for coplanar faces. FLOAT Float – Simple solver with good performance, without support for overlapping geometry. MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

EXACT Exact – Slower solver with the best results for coplanar faces.

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

use_invert (boolean, (optional)) – Invert, Invert action for the duration of the stroke

use_invert (boolean, (optional)) – Invert, Invert action for the duration of the stroke

use_invert (boolean, (optional)) – Invert, Invert action for the duration of the stroke

relax_method (enum in ['LAPLACIAN', 'HC', 'COTAN'], (optional)) – Relax Method, Algorithm used for UV relaxation LAPLACIAN Laplacian – Use Laplacian method for relaxation. HC HC – Use HC method for relaxation. COTAN Geometry – Use Geometry (cotangent) relaxation, making UVs follow the underlying 3D geometry.

Relax Method, Algorithm used for UV relaxation

LAPLACIAN Laplacian – Use Laplacian method for relaxation.

HC HC – Use HC method for relaxation.

COTAN Geometry – Use Geometry (cotangent) relaxation, making UVs follow the underlying 3D geometry.

---

## Sculpt Curves Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.sculpt_curves.html

**Contents:**
- Sculpt Curves Operators¶

Sculpt curves using a brush

stroke (bpy_prop_collection of OperatorStrokeElement, (optional)) – Stroke

mode (enum in ['NORMAL', 'INVERT', 'SMOOTH', 'ERASE'], (optional)) – Stroke Mode, Action taken when a paint stroke is made NORMAL Regular – Apply brush normally. INVERT Invert – Invert action of brush for duration of stroke. SMOOTH Smooth – Switch brush to smooth mode for duration of stroke. ERASE Erase – Switch brush to erase mode for duration of stroke.

Stroke Mode, Action taken when a paint stroke is made

NORMAL Regular – Apply brush normally.

INVERT Invert – Invert action of brush for duration of stroke.

SMOOTH Smooth – Switch brush to smooth mode for duration of stroke.

ERASE Erase – Switch brush to erase mode for duration of stroke.

pen_flip (boolean, (optional)) – Pen Flip, Whether a tablet’s eraser mode is being used

Change the minimum distance used by the density brush

Select curves which are close to curves that are selected already

distance (float in [-inf, inf], (optional)) – Distance, By how much to grow the selection

Randomizes existing selection or create new random selection

seed (int in [-inf, inf], (optional)) – Seed, Source of randomness

partial (boolean, (optional)) – Partial, Allow points or curves to be selected partially

probability (float in [0, 1], (optional)) – Probability, Chance of every point or curve being included in the selection

min (float in [0, 1], (optional)) – Min, Minimum value for the random selection

constant_per_curve (boolean, (optional)) – Constant per Curve, The generated random number is the same for every control point of a curve

---

## Sequencer Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.sequencer.html

**Contents:**
- Sequencer Operators¶

Add a strip using a duplicate of this scene asset as the source

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

asset_library_type (enum in Asset Library Type Items, (optional)) – Asset Library Type

asset_library_identifier (string, (optional, never None)) – Asset Library Identifier

relative_asset_identifier (string, (optional, never None)) – Relative Asset Identifier

Replace effect strip with another that takes the same number of inputs

type (enum in ['CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER', 'GAMMA_CROSS', 'MULTIPLY', 'WIPE', 'GLOW', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT', 'GAUSSIAN_BLUR', 'TEXT', 'COLORMIX'], (optional)) – Type, Strip effect type CROSS Crossfade – Fade out of one video, fading into another. ADD Add – Add together color channels from two videos. SUBTRACT Subtract – Subtract one strip’s color from another. ALPHA_OVER Alpha Over – Blend alpha on top of another video. ALPHA_UNDER Alpha Under – Blend alpha below another video. GAMMA_CROSS Gamma Crossfade – Crossfade with color correction. MULTIPLY Multiply – Multiply color channels from two videos. WIPE Wipe – Sweep a transition line across the frame. GLOW Glow – Add blur and brightness to light areas. COLOR Color – Add a simple color strip. SPEED Speed – Timewarp video strips, modifying playback speed. MULTICAM Multicam Selector – Control active camera angles. ADJUSTMENT Adjustment Layer – Apply nondestructive effects. GAUSSIAN_BLUR Gaussian Blur – Soften details along axes. TEXT Text – Add a simple text strip. COLORMIX Color Mix – Combine two strips using blend modes.

Type, Strip effect type

CROSS Crossfade – Fade out of one video, fading into another.

ADD Add – Add together color channels from two videos.

SUBTRACT Subtract – Subtract one strip’s color from another.

ALPHA_OVER Alpha Over – Blend alpha on top of another video.

ALPHA_UNDER Alpha Under – Blend alpha below another video.

GAMMA_CROSS Gamma Crossfade – Crossfade with color correction.

MULTIPLY Multiply – Multiply color channels from two videos.

WIPE Wipe – Sweep a transition line across the frame.

GLOW Glow – Add blur and brightness to light areas.

COLOR Color – Add a simple color strip.

SPEED Speed – Timewarp video strips, modifying playback speed.

MULTICAM Multicam Selector – Control active camera angles.

ADJUSTMENT Adjustment Layer – Apply nondestructive effects.

GAUSSIAN_BLUR Gaussian Blur – Soften details along axes.

TEXT Text – Add a simple text strip.

COLORMIX Color Mix – Combine two strips using blend modes.

Undocumented, consider contributing.

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_placeholders (boolean, (optional)) – Use Placeholders, Use placeholders for missing frames of the strip

Change Scene assigned to Strip

scene (enum in [], (optional)) – Scene

Link selected strips together for simplified group selection

toggle (boolean, (optional)) – Toggle, Toggle strip connections

Copy the selected strips to the internal clipboard

Do cross-fading volume animation of two selected sound strips

startup/bl_operators/sequencer.py:43

Set 2D cursor location

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in normalized preview coordinates

Deinterlace all selected movie sources

startup/bl_operators/sequencer.py:134

Delete selected strips from the sequencer

delete_data (boolean, (optional)) – Delete Data, After removing the Strip, delete the associated data also

Unlink selected strips so that they can be selected individually

Duplicate the selected strips

linked (boolean, (optional)) – Linked, Duplicate strip but not strip data, linking to the original data

Duplicate selected strips and move them

SEQUENCER_OT_duplicate (SEQUENCER_OT_duplicate, (optional)) – Duplicate Strips, Duplicate the selected strips

TRANSFORM_OT_seq_slide (TRANSFORM_OT_seq_slide, (optional)) – Sequence Slide, Slide a sequence strip in time

Duplicate selected strips, but not their data, and move them

SEQUENCER_OT_duplicate (SEQUENCER_OT_duplicate, (optional)) – Duplicate Strips, Duplicate the selected strips

TRANSFORM_OT_seq_slide (TRANSFORM_OT_seq_slide, (optional)) – Sequence Slide, Slide a sequence strip in time

Add an effect to the sequencer, most are applied on top of existing strips

type (enum in ['CROSS', 'ADD', 'SUBTRACT', 'ALPHA_OVER', 'ALPHA_UNDER', 'GAMMA_CROSS', 'MULTIPLY', 'WIPE', 'GLOW', 'COLOR', 'SPEED', 'MULTICAM', 'ADJUSTMENT', 'GAUSSIAN_BLUR', 'TEXT', 'COLORMIX'], (optional)) – Type, Sequencer effect type CROSS Crossfade – Fade out of one video, fading into another. ADD Add – Add together color channels from two videos. SUBTRACT Subtract – Subtract one strip’s color from another. ALPHA_OVER Alpha Over – Blend alpha on top of another video. ALPHA_UNDER Alpha Under – Blend alpha below another video. GAMMA_CROSS Gamma Crossfade – Crossfade with color correction. MULTIPLY Multiply – Multiply color channels from two videos. WIPE Wipe – Sweep a transition line across the frame. GLOW Glow – Add blur and brightness to light areas. COLOR Color – Add a simple color strip. SPEED Speed – Timewarp video strips, modifying playback speed. MULTICAM Multicam Selector – Control active camera angles. ADJUSTMENT Adjustment Layer – Apply nondestructive effects. GAUSSIAN_BLUR Gaussian Blur – Soften details along axes. TEXT Text – Add a simple text strip. COLORMIX Color Mix – Combine two strips using blend modes.

Type, Sequencer effect type

CROSS Crossfade – Fade out of one video, fading into another.

ADD Add – Add together color channels from two videos.

SUBTRACT Subtract – Subtract one strip’s color from another.

ALPHA_OVER Alpha Over – Blend alpha on top of another video.

ALPHA_UNDER Alpha Under – Blend alpha below another video.

GAMMA_CROSS Gamma Crossfade – Crossfade with color correction.

MULTIPLY Multiply – Multiply color channels from two videos.

WIPE Wipe – Sweep a transition line across the frame.

GLOW Glow – Add blur and brightness to light areas.

COLOR Color – Add a simple color strip.

SPEED Speed – Timewarp video strips, modifying playback speed.

MULTICAM Multicam Selector – Control active camera angles.

ADJUSTMENT Adjustment Layer – Apply nondestructive effects.

GAUSSIAN_BLUR Gaussian Blur – Soften details along axes.

TEXT Text – Add a simple text strip.

COLORMIX Color Mix – Combine two strips using blend modes.

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

length (int in [-inf, inf], (optional)) – Length, Length of the strip in frames, or the length of each strip if multiple are added

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

color (mathutils.Color of 3 items in [0, 1], (optional)) – Color, Initialize the strip with this color

Enable selected proxies on all selected Movie and Image strips

proxy_25 (boolean, (optional)) – 25%

proxy_50 (boolean, (optional)) – 50%

proxy_75 (boolean, (optional)) – 75%

proxy_100 (boolean, (optional)) – 100%

overwrite (boolean, (optional)) – Overwrite

Export .srt file containing text strips

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Adds or updates a fade animation for either visual or audio strips

duration_seconds (float in [0.01, inf], (optional)) – Fade Duration, Duration of the fade in seconds

type (enum in ['IN_OUT', 'IN', 'OUT', 'CURSOR_FROM', 'CURSOR_TO'], (optional)) – Fade Type, Fade in, out, both in and out, to, or from the current frame. Default is both in and out IN_OUT Fade In and Out – Fade selected strips in and out. IN Fade In – Fade in selected strips. OUT Fade Out – Fade out selected strips. CURSOR_FROM From Current Frame – Fade from the time cursor to the end of overlapping strips. CURSOR_TO To Current Frame – Fade from the start of strips under the time cursor to the current frame.

Fade Type, Fade in, out, both in and out, to, or from the current frame. Default is both in and out

IN_OUT Fade In and Out – Fade selected strips in and out.

IN Fade In – Fade in selected strips.

OUT Fade Out – Fade out selected strips.

CURSOR_FROM From Current Frame – Fade from the time cursor to the end of overlapping strips.

CURSOR_TO To Current Frame – Fade from the start of strips under the time cursor to the current frame.

startup/bl_operators/sequencer.py:221

Removes fade animation from selected strips

startup/bl_operators/sequencer.py:157

Insert gap at current frame to first strips at the right, independent of selection or locked state of strips

frames (int in [0, inf], (optional)) – Frames, Frames to insert after current strip

Remove gap at current frame to first strip at the right, independent of selection or locked state of strips

all (boolean, (optional)) – All Gaps, Do all gaps to right of current frame

Add an image or image sequence to the sequencer

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

length (int in [-inf, inf], (optional)) – Length, Length of the strip in frames, or the length of each strip if multiple are added

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

fit_method (enum in Strip Scale Method Items, (optional)) – Fit Method, Mode for fitting the image to the canvas

set_view_transform (boolean, (optional)) – Set View Transform, Set appropriate view transform based on media color space

image_import_type (enum in ['DETECT', 'SEQUENCE', 'INDIVIDUAL'], (optional)) – Import As, Mode for importing selected images DETECT Auto Detect – Add images as individual strips, unless their filenames match Blender’s numbered sequence pattern, in which case they are grouped into a single image sequence. SEQUENCE Image Sequence – Import all selected images as a single image sequence. The sequence of images does not have to match Blender’s numbered sequence pattern, so placeholders cannot be inferred. INDIVIDUAL Individual Images – Add each selected image as an individual strip.

Import As, Mode for importing selected images

DETECT Auto Detect – Add images as individual strips, unless their filenames match Blender’s numbered sequence pattern, in which case they are grouped into a single image sequence.

SEQUENCE Image Sequence – Import all selected images as a single image sequence. The sequence of images does not have to match Blender’s numbered sequence pattern, so placeholders cannot be inferred.

INDIVIDUAL Individual Images – Add each selected image as an individual strip.

use_sequence_detection (boolean, (optional)) – Detect Sequences, Automatically detect animated sequences in selected images (based on file names)

use_placeholders (boolean, (optional)) – Use Placeholders, Reserve placeholder frames for missing frames of the image sequence

On image sequence strips, it returns a strip for each image

length (int in [1, inf], (optional)) – Length, Length of each frame

Lock strips so they cannot be transformed

Add a mask strip to the sequencer

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

mask (enum in [], (optional)) – Mask

Group selected strips into a meta-strip

Put the contents of a meta-strip back in the sequencer

Toggle a meta-strip (to edit enclosed strips)

Add a movie strip to the sequencer

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

fit_method (enum in Strip Scale Method Items, (optional)) – Fit Method, Mode for fitting the image to the canvas

set_view_transform (boolean, (optional)) – Set View Transform, Set appropriate view transform based on media color space

adjust_playback_rate (boolean, (optional)) – Adjust Playback Rate, Play at normal speed regardless of scene FPS

sound (boolean, (optional)) – Sound, Load sound with the movie

use_framerate (boolean, (optional)) – Set Scene Frame Rate, Set frame rate of the current scene to the frame rate of the movie

Add a movieclip strip to the sequencer

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

clip (enum in [], (optional)) – Clip

Mute (un)selected strips

unselected (boolean, (optional)) – Unselected, Mute unselected rather than selected strips

Clear strip in/out offsets from the start and end of content

Paste strips from the internal clipboard

keep_offset (boolean, (optional)) – Keep Offset, Keep strip offset relative to the current frame when pasting

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

Duplicate selected strips and move them

SEQUENCER_OT_duplicate (SEQUENCER_OT_duplicate, (optional)) – Duplicate Strips, Duplicate the selected strips

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Duplicate selected strips, but not their data, and move them

SEQUENCER_OT_duplicate (SEQUENCER_OT_duplicate, (optional)) – Duplicate Strips, Duplicate the selected strips

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Reassign the inputs for the effect strip

Rebuild all selected proxies and timecode indices

Refresh the sequencer editor

Reload strips in the sequencer

adjust_length (boolean, (optional)) – Adjust Length, Adjust length of strips to their data length

Undocumented, consider contributing.

Set render size and aspect from active strip

Add freeze frame and move it

SEQUENCER_OT_retiming_freeze_frame_add (SEQUENCER_OT_retiming_freeze_frame_add, (optional)) – Add Freeze Frame, Add freeze frame

TRANSFORM_OT_seq_slide (TRANSFORM_OT_seq_slide, (optional)) – Sequence Slide, Slide a sequence strip in time

Add smooth transition between 2 retimed segments and change its duration

SEQUENCER_OT_retiming_transition_add (SEQUENCER_OT_retiming_transition_add, (optional)) – Add Speed Transition, Add smooth transition between 2 retimed segments

TRANSFORM_OT_seq_slide (TRANSFORM_OT_seq_slide, (optional)) – Sequence Slide, Slide a sequence strip in time

duration (int in [0, inf], (optional)) – Duration, Duration of freeze frame segment

timeline_frame (int in [0, inf], (optional)) – Timeline Frame, Frame where key will be added

Delete selected retiming keys from the sequencer

Set speed of retimed segment

speed (float in [0.001, inf], (optional)) – Speed, New speed of retimed segment

keep_retiming (boolean, (optional)) – Preserve Current Retiming, Keep speed of other segments unchanged, change strip length instead

Show retiming keys in selected strips

Add smooth transition between 2 retimed segments

duration (int in [0, inf], (optional)) – Duration, Duration of freeze frame segment

Use mouse to sample color in current frame

size (int in [1, 128], (optional)) – Sample Size

Update frame range of scene strip

Add a strip re-using this scene as the source

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

scene (enum in [], (optional)) – Scene

Add a strip using a new scene as the source

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

type (enum in ['NEW', 'EMPTY', 'LINK_COPY', 'FULL_COPY'], (optional)) – Type NEW New – Add new Strip with a new empty Scene with default settings. EMPTY Copy Settings – Add a new Strip, with an empty scene, and copy settings from the current scene. LINK_COPY Linked Copy – Add a Strip and link in the collections from the current scene (shallow copy). FULL_COPY Full Copy – Add a Strip and make a full copy of the current scene.

NEW New – Add new Strip with a new empty Scene with default settings.

EMPTY Copy Settings – Add a new Strip, with an empty scene, and copy settings from the current scene.

LINK_COPY Linked Copy – Add a Strip and link in the collections from the current scene (shallow copy).

FULL_COPY Full Copy – Add a Strip and make a full copy of the current scene.

Select a strip (last selected becomes the “active strip”)

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

center (boolean, (optional)) – Center, Use the object center when selecting, in edit mode used to extend object selection

linked_handle (boolean, (optional)) – Linked Handle, Select handles next to the active strip

linked_time (boolean, (optional)) – Linked Time, Select other strips or handles at the same time, or all retiming keys after the current in retiming mode

side_of_frame (boolean, (optional)) – Side of Frame, Select all strips on same side of the current frame as the mouse cursor

ignore_connections (boolean, (optional)) – Ignore Connections, Select strips individually whether or not they are connected

Select or deselect all strips

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select strips using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

tweak (boolean, (optional)) – Tweak, Make box select pass through to sequence slide when the cursor is hovering on a strip

include_handles (boolean, (optional)) – Select Handles, Select the strips and their handles

ignore_connections (boolean, (optional)) – Ignore Connections, Select strips individually whether or not they are connected

Select strips using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

ignore_connections (boolean, (optional)) – Ignore Connections, Select strips individually whether or not they are connected

Select all strips grouped by various properties

type (enum in ['TYPE', 'TYPE_BASIC', 'TYPE_EFFECT', 'DATA', 'EFFECT', 'EFFECT_LINK', 'OVERLAP'], (optional)) – Type TYPE Type – Shared strip type. TYPE_BASIC Global Type – All strips of same basic type (graphical or sound). TYPE_EFFECT Effect Type – Shared strip effect type (if active strip is not an effect one, select all non-effect strips). DATA Data – Shared data (scene, image, sound, etc.). EFFECT Effect – Shared effects. EFFECT_LINK Effect/Linked – Other strips affected by the active one (sharing some time, and below or effect-assigned). OVERLAP Overlap – Overlapping time.

TYPE Type – Shared strip type.

TYPE_BASIC Global Type – All strips of same basic type (graphical or sound).

TYPE_EFFECT Effect Type – Shared strip effect type (if active strip is not an effect one, select all non-effect strips).

DATA Data – Shared data (scene, image, sound, etc.).

EFFECT Effect – Shared effects.

EFFECT_LINK Effect/Linked – Other strips affected by the active one (sharing some time, and below or effect-assigned).

OVERLAP Overlap – Overlapping time.

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

use_active_channel (boolean, (optional)) – Same Channel, Only consider strips on the same channel as the active one

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

ignore_connections (boolean, (optional)) – Ignore Connections, Select strips individually whether or not they are connected

Select gizmo handles on the sides of the selected strip

side (enum in ['LEFT', 'RIGHT', 'BOTH', 'LEFT_NEIGHBOR', 'RIGHT_NEIGHBOR', 'BOTH_NEIGHBORS'], (optional)) – Side, The side of the handle that is selected

Select strips using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Shrink the current selection of adjacent selected strips

Select all strips adjacent to the current selection

Select a chain of linked strips nearest to the mouse pointer

extend (boolean, (optional)) – Extend, Extend the selection

Select more strips adjacent to the current selection

Select strips on the nominated side of the selected strips

side (enum in ['MOUSE', 'LEFT', 'RIGHT', 'BOTH', 'NO_CHANGE'], (optional)) – Side, The side to which the selection is applied

Select strips relative to the current frame

extend (boolean, (optional)) – Extend, Extend the selection

side (enum in ['LEFT', 'RIGHT', 'CURRENT'], (optional)) – Side LEFT Left – Select to the left of the current frame. RIGHT Right – Select to the right of the current frame. CURRENT Current Frame – Select intersecting with the current frame.

LEFT Left – Select to the left of the current frame.

RIGHT Right – Select to the right of the current frame.

CURRENT Current Frame – Select intersecting with the current frame.

Set the frame range to the selected strips start and end

preview (boolean, (optional)) – Preview, Set the preview range instead

Slip the contents of selected strips

offset (float in [-inf, inf], (optional)) – Offset, Offset to the data of the strip

slip_keyframes (boolean, (optional)) – Slip Keyframes, Move the keyframes alongside the media

use_cursor_position (boolean, (optional)) – Use Cursor Position, Slip strips under mouse cursor instead of all selected strips

ignore_connections (boolean, (optional)) – Ignore Connections, Do not slip connected strips if using cursor position

Frame where selected strips will be snapped

frame (int in [-inf, inf], (optional)) – Frame, Frame where selected strips will be snapped

Add a sound strip to the sequencer

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

move_strips (boolean, (optional)) – Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline

frame_start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the strip

channel (int in [1, 128], (optional)) – Channel, Channel to place this strip into

replace_sel (boolean, (optional)) – Replace Selection, Deselect previously selected strips after add operation completes

overlap (boolean, (optional)) – Allow Overlap, Don’t correct overlap on new strips

overlap_shuffle_override (boolean, (optional)) – Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips

skip_locked_or_muted_channels (boolean, (optional)) – Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips

cache (boolean, (optional)) – Cache, Cache the sound in memory

mono (boolean, (optional)) – Mono, Merge all the sound’s channels into one

Split the selected strips in two

frame (int in [-inf, inf], (optional)) – Frame, Frame where selected strips will be split

channel (int in [-inf, inf], (optional)) – Channel, Channel in which strip will be cut

type (enum in ['SOFT', 'HARD'], (optional)) – Type, The type of split operation to perform on strips

use_cursor_position (boolean, (optional)) – Use Cursor Position, Split at position of the cursor instead of current frame

side (enum in ['MOUSE', 'LEFT', 'RIGHT', 'BOTH', 'NO_CHANGE'], (optional)) – Side, The side that remains selected after splitting

ignore_selection (boolean, (optional)) – Ignore Selection, Make cut even if strip is not selected preserving selection state after cut

ignore_connections (boolean, (optional)) – Ignore Connections, Don’t propagate split to connected strips

Split multicam strip and select camera

camera (int in [1, 32], (optional)) – Camera

startup/bl_operators/sequencer.py:101

Set a color tag for the selected strips

color (enum in Strip Color Items, (optional)) – Color Tag

Move frame to previous edit point

next (boolean, (optional)) – Next Strip

center (boolean, (optional)) – Use Strip Center

Add a modifier to the strip

type (enum in [], (optional)) – Type

Copy modifiers of the active strip to all selected strips

type (enum in ['REPLACE', 'APPEND'], (optional)) – Type REPLACE Replace – Replace modifiers in destination. APPEND Append – Append active modifiers to selected strips.

REPLACE Replace – Replace modifiers in destination.

APPEND Append – Append active modifiers to selected strips.

Redefine equalizer graphs

graphs (enum in ['SIMPLE', 'DOUBLE', 'TRIPLE'], (optional)) – Graphs, Number of graphs SIMPLE Unique – One unique graphical definition. DOUBLE Double – Graphical definition in 2 sections. TRIPLE Triplet – Graphical definition in 3 sections.

Graphs, Number of graphs

SIMPLE Unique – One unique graphical definition.

DOUBLE Double – Graphical definition in 2 sections.

TRIPLE Triplet – Graphical definition in 3 sections.

name (string, (optional, never None)) – Name, Name of modifier to redefine

Move modifier up and down in the stack

name (string, (optional, never None)) – Name, Name of modifier to remove

direction (enum in ['UP', 'DOWN'], (optional)) – Type UP Up – Move modifier up in the stack. DOWN Down – Move modifier down in the stack.

UP Up – Move modifier up in the stack.

DOWN Down – Move modifier down in the stack.

Change the strip modifier’s index in the stack so it evaluates after the set number of others

modifier (string, (optional, never None)) – Modifier, Name of the modifier to edit

index (int in [0, inf], (optional)) – Index, The index to move the modifier to

Remove a modifier from the strip

name (string, (optional, never None)) – Name, Name of modifier to remove

Activate the strip modifier to use as the context

modifier (string, (optional, never None)) – Modifier, Name of the strip modifier to edit

Reset image transformation to default value

property (enum in ['POSITION', 'SCALE', 'ROTATION', 'ALL'], (optional)) – Property, Strip transform property to be reset POSITION Position – Reset strip transform location. SCALE Scale – Reset strip transform scale. ROTATION Rotation – Reset strip transform rotation. ALL All – Reset strip transform location, scale and rotation.

Property, Strip transform property to be reset

POSITION Position – Reset strip transform location.

SCALE Scale – Reset strip transform scale.

ROTATION Rotation – Reset strip transform rotation.

ALL All – Reset strip transform location, scale and rotation.

Undocumented, consider contributing.

fit_method (enum in Strip Scale Method Items, (optional)) – Fit Method, Mode for fitting the image to the canvas

Swap active strip with strip to the right or left

side (enum in ['LEFT', 'RIGHT'], (optional)) – Side, Side of the strip to swap

Swap 2 sequencer strips

Swap the two inputs of the effect strip

type (enum in ['LINE_BEGIN', 'LINE_END', 'TEXT_BEGIN', 'TEXT_END', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD', 'PREVIOUS_LINE', 'NEXT_LINE'], (optional)) – Type, Where to move cursor to, to make a selection

select_text (boolean, (optional)) – Select Text, Select text while moving cursor

Set cursor position in text

select_text (boolean, (optional)) – Select Text, Select text while moving cursor

Delete text at cursor position

type (enum in ['NEXT_OR_SELECTION', 'PREVIOUS_OR_SELECTION'], (optional)) – Type, Which part of the text to delete

Deselect all characters

Copy text to clipboard

Cut text to clipboard

Paste text from clipboard

Insert text at cursor position

string (string, (optional, never None)) – String, String to be inserted at cursor position

Insert line break at cursor position

Select all characters

Unlock strips so they can be transformed

Unmute (un)selected strips

unselected (boolean, (optional)) – Unselected, Unmute unselected rather than selected strips

View all the strips in the sequencer

Zoom preview to fit in the area

Move the view to the current frame

Set the boundaries of the border used for offset view

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Zoom the sequencer on the selected strips

Change zoom ratio of sequencer preview

ratio (float in [-inf, inf], (optional)) – Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out

---

## Spreadsheet Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.spreadsheet.html

**Contents:**
- Spreadsheet Operators¶

Add a filter to remove rows from the displayed data

Change visible data source in the spreadsheet

component_type (int in [0, 32767], (optional)) – Component Type

attribute_domain_type (int in [0, 32767], (optional)) – Attribute Domain Type

Resize a spreadsheet column to the width of the data

Remove a row filter from the rules

index (int in [0, inf], (optional)) – Index

Change the order of columns

Resize a spreadsheet column

Turn on or off pinning

startup/bl_operators/spreadsheet.py:21

---

## Surface Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.surface.html

**Contents:**
- Surface Operators¶

Construct a Nurbs surface Circle

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs surface Curve

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs surface Cylinder

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs surface Sphere

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs surface Patch

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

Construct a Nurbs surface Torus

radius (float in [0, inf], (optional)) – Radius

enter_editmode (boolean, (optional)) – Enter Edit Mode, Enter edit mode when adding this object

align (enum in ['WORLD', 'VIEW', 'CURSOR'], (optional)) – Align, The alignment of the new object WORLD World – Align the new object to the world. VIEW View – Align the new object to the view. CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

Align, The alignment of the new object

WORLD World – Align the new object to the world.

VIEW View – Align the new object to the view.

CURSOR 3D Cursor – Use the 3D cursor orientation for the new object.

location (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Location, Location for the newly added object

rotation (mathutils.Euler rotation of 3 items in [-inf, inf], (optional)) – Rotation, Rotation for the newly added object

scale (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale, Scale for the newly added object

---

## Text Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.text.html

**Contents:**
- Text Operators¶

Show a list of used text in the open document

Undocumented, consider contributing.

type (enum in ['TOGGLE', 'COMMENT', 'UNCOMMENT'], (optional)) – Type, Add or remove comments

Convert whitespaces by type

type (enum in ['SPACES', 'TABS'], (optional)) – Type, Type of whitespace to convert to

Copy selected text to clipboard

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

Cut selected text to clipboard

Delete text by cursor position

type (enum in ['NEXT_CHARACTER', 'PREVIOUS_CHARACTER', 'NEXT_WORD', 'PREVIOUS_WORD'], (optional)) – Type, Which part of the text to delete

Duplicate the current line

Find specified text and set as selected

Indent selected text or autocomplete

Insert text at cursor position

text (string, (optional, never None)) – Text, Text to insert at the cursor position

line (int in [1, inf], (optional)) – Line, Line number to jump to

Jump to a file for the text editor

filepath (string, (optional, never None)) – Filepath

line (int in [0, inf], (optional)) – Line, Line to jump to

column (int in [0, inf], (optional)) – Column, Column to jump to

Insert line break at cursor position

The current line number

Make active text file internal

Move cursor to position type

type (enum in ['LINE_BEGIN', 'LINE_END', 'FILE_TOP', 'FILE_BOTTOM', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD', 'PREVIOUS_LINE', 'NEXT_LINE', 'PREVIOUS_PAGE', 'NEXT_PAGE'], (optional)) – Type, Where to move cursor to

Move the currently selected line(s) up/down

direction (enum in ['UP', 'DOWN'], (optional)) – Direction

Move the cursor while selecting

type (enum in ['LINE_BEGIN', 'LINE_END', 'FILE_TOP', 'FILE_BOTTOM', 'PREVIOUS_CHARACTER', 'NEXT_CHARACTER', 'PREVIOUS_WORD', 'NEXT_WORD', 'PREVIOUS_LINE', 'NEXT_LINE', 'PREVIOUS_PAGE', 'NEXT_PAGE'], (optional)) – Type, Where to move cursor to, to make a selection

Create a new text data-block

Open a new text data-block

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in ['DEFAULT', 'FILE_SORT_ALPHA', 'FILE_SORT_EXTENSION', 'FILE_SORT_TIME', 'FILE_SORT_SIZE', 'ASSET_CATALOG'], (optional)) – File sorting mode DEFAULT Default – Automatically determine sort method for files. FILE_SORT_ALPHA Name – Sort the file list alphabetically. FILE_SORT_EXTENSION Extension – Sort the file list by extension/type. FILE_SORT_TIME Modified Date – Sort files by modification time. FILE_SORT_SIZE Size – Sort files by size. ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

DEFAULT Default – Automatically determine sort method for files.

FILE_SORT_ALPHA Name – Sort the file list alphabetically.

FILE_SORT_EXTENSION Extension – Sort the file list by extension/type.

FILE_SORT_TIME Modified Date – Sort files by modification time.

FILE_SORT_SIZE Size – Sort files by size.

ASSET_CATALOG Asset Catalog – Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..

internal (boolean, (optional)) – Make Internal, Make text file internal after loading

Toggle overwrite while typing

Paste text from clipboard

selection (boolean, (optional)) – Selection, Paste text selected elsewhere rather than copied (X11/Wayland only)

Reload active text data-block from its file

Replace text with the specified text

all (boolean, (optional)) – Replace All, Replace all occurrences

Replace text with specified text and set as selected

When external text is out of sync, resolve the conflict

resolution (enum in ['IGNORE', 'RELOAD', 'SAVE', 'MAKE_INTERNAL'], (optional)) – Resolution, How to solve conflict due to differences in internal and external text

Save active text data-block

Save active text file with options

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Undocumented, consider contributing.

lines (int in [-inf, inf], (optional)) – Lines, Number of lines to scroll

Undocumented, consider contributing.

lines (int in [-inf, inf], (optional)) – Lines, Number of lines to scroll

Select word under cursor

Create 3D text object from active text data-block

split_lines (boolean, (optional)) – Split Lines, Create one object per line in the text

Unindent selected text

Unlink active text data-block

Update users of this shader, such as custom cameras and script nodes, with its new sockets and options

---

## Sound Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.sound.html

**Contents:**
- Sound Operators¶

Update the audio animation cache

Mix the scene’s audio to a sound file

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

accuracy (int in [1, inf], (optional)) – Accuracy, Sample accuracy, important for animation data (the lower the value, the more accurate)

container (enum in ['AAC', 'AC3', 'FLAC', 'MATROSKA', 'MP2', 'MP3', 'OGG', 'WAV'], (optional)) – Container, File format AAC AAC – Advanced Audio Coding. AC3 AC3 – Dolby Digital ATRAC 3. FLAC FLAC – Free Lossless Audio Codec. MATROSKA MKV – Matroska. MP2 MP2 – MPEG-1 Audio Layer II. MP3 MP3 – MPEG-2 Audio Layer III. OGG OGG – Xiph.Org Ogg Container. WAV WAV – Waveform Audio File Format.

Container, File format

AAC AAC – Advanced Audio Coding.

AC3 AC3 – Dolby Digital ATRAC 3.

FLAC FLAC – Free Lossless Audio Codec.

MATROSKA MKV – Matroska.

MP2 MP2 – MPEG-1 Audio Layer II.

MP3 MP3 – MPEG-2 Audio Layer III.

OGG OGG – Xiph.Org Ogg Container.

WAV WAV – Waveform Audio File Format.

codec (enum in ['AAC', 'AC3', 'FLAC', 'MP2', 'MP3', 'PCM', 'VORBIS'], (optional)) – Codec, Audio Codec AAC AAC – Advanced Audio Coding. AC3 AC3 – Dolby Digital ATRAC 3. FLAC FLAC – Free Lossless Audio Codec. MP2 MP2 – MPEG-1 Audio Layer II. MP3 MP3 – MPEG-2 Audio Layer III. PCM PCM – Pulse Code Modulation (RAW). VORBIS Vorbis – Xiph.Org Vorbis Codec.

AAC AAC – Advanced Audio Coding.

AC3 AC3 – Dolby Digital ATRAC 3.

FLAC FLAC – Free Lossless Audio Codec.

MP2 MP2 – MPEG-1 Audio Layer II.

MP3 MP3 – MPEG-2 Audio Layer III.

PCM PCM – Pulse Code Modulation (RAW).

VORBIS Vorbis – Xiph.Org Vorbis Codec.

channels (enum in ['MONO', 'STEREO', 'STEREO_LFE', 'SURROUND4', 'SURROUND5', 'SURROUND51', 'SURROUND61', 'SURROUND71'], (optional)) – Channels, Audio channel count MONO Mono – Single audio channel. STEREO Stereo – Stereo audio channels. STEREO_LFE Stereo LFE – Stereo with LFE channel. SURROUND4 4 Channels – 4 channel surround sound. SURROUND5 5 Channels – 5 channel surround sound. SURROUND51 5.1 Surround – 5.1 surround sound. SURROUND61 6.1 Surround – 6.1 surround sound. SURROUND71 7.1 Surround – 7.1 surround sound.

Channels, Audio channel count

MONO Mono – Single audio channel.

STEREO Stereo – Stereo audio channels.

STEREO_LFE Stereo LFE – Stereo with LFE channel.

SURROUND4 4 Channels – 4 channel surround sound.

SURROUND5 5 Channels – 5 channel surround sound.

SURROUND51 5.1 Surround – 5.1 surround sound.

SURROUND61 6.1 Surround – 6.1 surround sound.

SURROUND71 7.1 Surround – 7.1 surround sound.

format (enum in ['U8', 'S16', 'S24', 'S32', 'F32', 'F64'], (optional)) – Format, Sample format U8 U8 – 8-bit unsigned. S16 S16 – 16-bit signed. S24 S24 – 24-bit signed. S32 S32 – 32-bit signed. F32 F32 – 32-bit floating-point. F64 F64 – 64-bit floating-point.

Format, Sample format

U8 U8 – 8-bit unsigned.

S16 S16 – 16-bit signed.

S24 S24 – 24-bit signed.

S32 S32 – 32-bit signed.

F32 F32 – 32-bit floating-point.

F64 F64 – 64-bit floating-point.

mixrate (int in [8000, 192000], (optional)) – Sample Rate, Sample rate in samples/s

bitrate (int in [32, 512], (optional)) – Bitrate, Bitrate in kbit/s

split_channels (boolean, (optional)) – Split channels, Each channel will be rendered into a mono file

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

cache (boolean, (optional)) – Cache, Cache the sound in memory

mono (boolean, (optional)) – Mono, Merge all the sound’s channels into one

Load a sound file as mono

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

show_multiview (boolean, (optional)) – Enable Multi-View

use_multiview (boolean, (optional)) – Use Multi-View

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

cache (boolean, (optional)) – Cache, Cache the sound in memory

mono (boolean, (optional)) – Mono, Mixdown the sound to mono

Pack the sound into the current blend file

Unpack the sound to the samples filename

method (enum in Unpack Method Items, (optional)) – Method, How to unpack

id (string, (optional, never None)) – Sound Name, Sound data-block name to unpack

Update animation flags

---

## Texture Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.texture.html

**Contents:**
- Texture Operators¶

Copy the material texture settings and nodes

Move texture slots up and down

type (enum in ['UP', 'DOWN'], (optional)) – Type

Copy the texture settings and nodes

---

## Transform Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.transform.html

**Contents:**
- Transform Operators¶

Scale selected bendy bones display size

value (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Display Size

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Bend selected items between the 3D cursor and the mouse

value (float array of 1 items in [-inf, inf], (optional)) – Angle

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Create transformation orientation from selection

name (string, (optional, never None)) – Name, Name of the new custom orientation

use_view (boolean, (optional)) – Use View, Use the current view instead of the active object to create the new orientation

use (boolean, (optional)) – Use After Creation, Select orientation after its creation

overwrite (boolean, (optional)) – Overwrite Previous, Overwrite previously created orientation with same name

Delete transformation orientation

Change the bevel weight of edges

value (float in [-1, 1], (optional)) – Factor

snap (boolean, (optional)) – Use Snapping Options

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Change the crease of edges

value (float in [-1, 1], (optional)) – Factor

snap (boolean, (optional)) – Use Snapping Options

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Slide an edge loop along a mesh

value (float in [-10, 10], (optional)) – Factor

single_side (boolean, (optional)) – Single Side

use_even (boolean, (optional)) – Even, Make the edge loop match the shape of the adjacent edge loop

flipped (boolean, (optional)) – Flipped, When Even mode is active, flips between the two adjacent edge loops

use_clamp (boolean, (optional)) – Clamp, Clamp within the edge extents

mirror (boolean, (optional)) – Mirror Editing

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

correct_uv (boolean, (optional)) – Correct UVs, Correct UV coordinates when transforming

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Transform selected items by mode type

Mirror selected items around one or more axes

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Push/Pull selected items

value (float in [-inf, inf], (optional)) – Distance

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Scale (resize) selected items

value (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale

mouse_dir_constraint (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Mouse Directional Constraint

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

texture_space (boolean, (optional)) – Edit Texture Space, Edit object data texture space

remove_on_cancel (boolean, (optional)) – Remove on Cancel, Remove elements on cancel

use_duplicated_keyframes (boolean, (optional)) – Duplicated Keyframes, Transform duplicated keyframes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Rotate selected items

value (float in [-inf, inf], (optional)) – Angle

orient_axis (enum in Axis Xyz Items, (optional)) – Axis

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Rotate custom normal of selected items

value (float in [-inf, inf], (optional)) – Angle

orient_axis (enum in Axis Xyz Items, (optional)) – Axis

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Select transformation orientation

orientation (enum in [], (optional)) – Orientation, Transformation orientation

Slide a sequence strip in time

value (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Offset

use_restore_handle_selection (boolean, (optional)) – Restore Handle Selection, Restore handle selection after tweaking

snap (boolean, (optional)) – Use Snapping Options

texture_space (boolean, (optional)) – Edit Texture Space, Edit object data texture space

remove_on_cancel (boolean, (optional)) – Remove on Cancel, Remove elements on cancel

use_duplicated_keyframes (boolean, (optional)) – Duplicated Keyframes, Transform duplicated keyframes

view2d_edge_pan (boolean, (optional)) – Edge Pan, Enable edge panning in 2D view

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Shear selected items along the given axis

value (float in [-inf, inf], (optional)) – Offset

orient_axis (enum in Axis Xyz Items, (optional)) – Axis

orient_axis_ortho (enum in Axis Xyz Items, (optional)) – Axis Ortho

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Shrink/fatten selected vertices along normals

value (float in [-inf, inf], (optional)) – Offset

use_even_offset (boolean, (optional)) – Offset Even, Scale the offset to give more even thickness

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Scale selected vertices’ skin radii

value (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Scale

orient_type (enum in [], (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in [], (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Tilt selected control vertices of 3D curve

value (float in [-inf, inf], (optional)) – Angle

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Move selected items outward in a spherical shape around geometric center

value (float in [0, 1], (optional)) – Factor

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Trackball style rotation of selected items

value (float array of 2 items in [-inf, inf], (optional)) – Angle

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Transform selected items by mode type

mode (enum in Transform Mode Type Items, (optional)) – Mode

value (mathutils.Vector of 4 items in [-inf, inf], (optional)) – Values

orient_axis (enum in Axis Xyz Items, (optional)) – Axis

orient_type (enum in Transform Orientation Items, (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in Transform Orientation Items, (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

snap_align (boolean, (optional)) – Align with Point Normal

snap_normal (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Normal

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

texture_space (boolean, (optional)) – Edit Texture Space, Edit object data texture space

remove_on_cancel (boolean, (optional)) – Remove on Cancel, Remove elements on cancel

use_duplicated_keyframes (boolean, (optional)) – Duplicated Keyframes, Transform duplicated keyframes

center_override (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center Override, Force using this center value (when set)

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

use_automerge_and_split (boolean, (optional)) – Auto Merge & Split, Forces the use of Auto Merge and Split

value (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Move

orient_type (enum in Transform Orientation Items, (optional)) – Orientation, Transformation orientation

orient_matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (optional)) – Matrix

orient_matrix_type (enum in Transform Orientation Items, (optional)) – Matrix Orientation

constraint_axis (boolean array of 3 items, (optional)) – Constraint Axis

mirror (boolean, (optional)) – Mirror Editing

use_proportional_edit (boolean, (optional)) – Proportional Editing

proportional_edit_falloff (enum in Proportional Falloff Items, (optional)) – Proportional Falloff, Falloff type for proportional editing mode

proportional_size (float in [1e-06, inf], (optional)) – Proportional Size

use_proportional_connected (boolean, (optional)) – Connected

use_proportional_projected (boolean, (optional)) – Projected (2D)

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

snap_align (boolean, (optional)) – Align with Point Normal

snap_normal (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Normal

gpencil_strokes (boolean, (optional)) – Edit Grease Pencil, Edit selected Grease Pencil strokes

cursor_transform (boolean, (optional)) – Transform Cursor

texture_space (boolean, (optional)) – Edit Texture Space, Edit object data texture space

remove_on_cancel (boolean, (optional)) – Remove on Cancel, Remove elements on cancel

use_duplicated_keyframes (boolean, (optional)) – Duplicated Keyframes, Transform duplicated keyframes

view2d_edge_pan (boolean, (optional)) – Edge Pan, Enable edge panning in 2D view

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

use_automerge_and_split (boolean, (optional)) – Auto Merge & Split, Forces the use of Auto Merge and Split

translate_origin (boolean, (optional)) – Translate Origin, Translate origin instead of selection

Change the crease of vertices

value (float in [-1, 1], (optional)) – Factor

snap (boolean, (optional)) – Use Snapping Options

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

Slide a vertex along a mesh

value (float in [-10, 10], (optional)) – Factor

use_even (boolean, (optional)) – Even, Make the edge loop match the shape of the adjacent edge loop

flipped (boolean, (optional)) – Flipped, When Even mode is active, flips between the two adjacent edge loops

use_clamp (boolean, (optional)) – Clamp, Clamp within the edge extents

mirror (boolean, (optional)) – Mirror Editing

snap (boolean, (optional)) – Use Snapping Options

snap_elements (enum set in Snap Element Items, (optional)) – Snap to Elements

use_snap_project (boolean, (optional)) – Project Individual Elements

snap_target (enum in Snap Source Items, (optional)) – Snap Base, Point on source that will snap to target

use_snap_self (boolean, (optional)) – Target: Include Active

use_snap_edit (boolean, (optional)) – Target: Include Edit

use_snap_nonedit (boolean, (optional)) – Target: Include Non-Edited

use_snap_selectable (boolean, (optional)) – Target: Exclude Non-Selectable

snap_point (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Point

correct_uv (boolean, (optional)) – Correct UVs, Correct UV coordinates when transforming

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

offset (float in [-inf, inf], (optional)) – Amount, Distance to offset

uniform (float in [0, 1], (optional)) – Uniform, Increase for uniform offset distance

normal (float in [0, 1], (optional)) – Normal, Align offset direction to normals

seed (int in [0, 10000], (optional)) – Random Seed, Seed for the random number generator

wait_for_input (boolean, (optional)) – Wait for Input

Warp vertices around the cursor

warp_angle (float in [-inf, inf], (optional)) – Warp Angle, Amount to warp about the cursor

offset_angle (float in [-inf, inf], (optional)) – Offset Angle, Angle to use as the basis for warping

min (float in [-inf, inf], (optional)) – Min

max (float in [-inf, inf], (optional)) – Max

viewmat (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – Matrix

center (mathutils.Vector of 3 items in [-inf, inf], (optional)) – Center

---

## Text Editor Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.text_editor.html

**Contents:**
- Text Editor Operators¶

Add or remove a Text Editor Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

---

## Ui Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.ui.html

**Contents:**
- Ui Operators¶

Set this property’s current value as the new default

Presses active button

skip_depressed (boolean, (optional)) – Skip Depressed

Unsets the text of the active button

Create a new driver with this property as input, and copy it to the internal clipboard. Use Paste Driver to add it to the target property, or Paste Driver Variables to extend an existing driver

Copy the RNA data path for this property to the clipboard

full_path (boolean, (optional)) – full_path, Copy full data path

Copy the property’s driver from the active item to the same property of all selected items, if the same property exists

all (boolean, (optional)) – All, Copy to selected the drivers of all elements of the array

Copy the Python command matching this button

Copy the property’s value from the active item to the same property of all selected items if the same property exists

all (boolean, (optional)) – All, Copy to selected all elements of the array

Drop colors to buttons

color (float array of 4 items in [0, inf], (optional)) – Color, Source color

gamma (boolean, (optional)) – Gamma Corrected, The source color is gamma corrected

has_alpha (boolean, (optional)) – Has Alpha, The source color contains an Alpha component

Drag material to Material slots in Properties

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

string (string, (optional, never None)) – String, The string value to drop into the button

Edit UI source code of the active button

Sample a bone from the 3D View or the Outliner to store in a property

Sample a color from the Blender window to store in a property

prop_data_path (string, (optional, never None)) – Data Path, Path of property to be set with the depth

Point-sample a color band

Sample depth from the 3D view

prop_data_path (string, (optional, never None)) – Data Path, Path of property to be set with the depth

Pick a property to use as a driver target

mapping_type (enum in ['SINGLE_MANY', 'DIRECT', 'MATCH', 'NONE_ALL', 'NONE_SINGLE'], (optional)) – Mapping Type, Method used to match target and driven properties SINGLE_MANY All from Target – Drive all components of this property using the target picked. DIRECT Single from Target – Drive this component of this property using the target picked. MATCH Match Indices – Create drivers for each pair of corresponding elements. NONE_ALL Manually Create Later – Create drivers for all properties without assigning any targets yet. NONE_SINGLE Manually Create Later (Single) – Create driver for this property only and without assigning any targets yet.

Mapping Type, Method used to match target and driven properties

SINGLE_MANY All from Target – Drive all components of this property using the target picked.

DIRECT Single from Target – Drive this component of this property using the target picked.

MATCH Match Indices – Create drivers for each pair of corresponding elements.

NONE_ALL Manually Create Later – Create drivers for all properties without assigning any targets yet.

NONE_SINGLE Manually Create Later (Single) – Create driver for this property only and without assigning any targets yet.

Sample a color from the Blender Window and create Grease Pencil material

mode (enum in ['MATERIAL', 'PALETTE', 'BRUSH'], (optional)) – Mode

material_mode (enum in ['STROKE', 'FILL', 'BOTH'], (optional)) – Material Mode

Sample a data-block from the 3D View to store in a property

Switch to the target object or bone

Start entering filter text for the list in focus

Create an override operation

all (boolean, (optional)) – All, Add overrides for all elements of the array

Delete the selected local override and relink its usages to the linked data-block if possible, else reset it and mark it as non editable

Create a local override of the selected linked data-block, and its hierarchy of dependencies

Reset the selected local override to its linked reference values

Remove an override operation

all (boolean, (optional)) – All, Reset to default values all elements of the array

Force a full reload of UI translation

Reset this property’s value to its default value

all (boolean, (optional)) – All, Reset to default values all elements of the array

Clear the property and use default or generated value in operators

Drag and drop onto a data-set or item within the data-set

Delete selected list item

Rename the active item in the data-set view

Activate selected view item

wait_to_deselect_others (boolean, (optional)) – Wait to Deselect Others

use_select_on_click (boolean, (optional)) – Act on Click, Instead of selecting on mouse press, wait to see if there’s drag event. Otherwise select on mouse release

mouse_x (int in [-inf, inf], (optional)) – Mouse X

mouse_y (int in [-inf, inf], (optional)) – Mouse Y

extend (boolean, (optional)) – extend, Extend Selection

range_select (boolean, (optional)) – Range Select, Select all between clicked and active items

Undocumented, consider contributing.

Start entering filter text for the data-set in focus

---

## Uilist Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.uilist.html

**Contents:**
- Uilist Operators¶

Add an entry to the list after the current active item

list_path (string, (optional, never None)) – list_path

active_index_path (string, (optional, never None)) – active_index_path

startup/bl_ui/generic_ui_list.py:210

Move an entry in the list up or down

list_path (string, (optional, never None)) – list_path

active_index_path (string, (optional, never None)) – active_index_path

direction (enum in ['UP', 'DOWN'], (optional)) – Direction UP UP – UP. DOWN DOWN – DOWN.

startup/bl_ui/generic_ui_list.py:238

Remove the selected entry from the list

list_path (string, (optional, never None)) – list_path

active_index_path (string, (optional, never None)) – active_index_path

startup/bl_ui/generic_ui_list.py:193

---

## View3D Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.view3d.html

**Contents:**
- View3D Operators¶

name (enum in [], (optional)) – Bone Name

extend (boolean, (optional)) – Extend

deselect (boolean, (optional)) – Deselect

toggle (boolean, (optional)) – Toggle

Add a new background image to the active camera

filepath (string, (optional, never None, blend relative // prefix supported)) – Filepath, Path to image file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Remove a background image from the camera

index (int in [0, inf], (optional)) – Index, Background image index to remove

Set camera view to active view

Move the camera so selected objects are framed

Clear the boundaries of the border render and disable border render

Set the view clipping region

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Copy the selected objects to the internal clipboard

Set the location of the 3D cursor

use_depth (boolean, (optional)) – Surface Project, Project onto the surface

orientation (enum in ['NONE', 'VIEW', 'XFORM', 'GEOM'], (optional)) – Orientation, Preset viewpoint to use NONE None – Leave orientation unchanged. VIEW View – Orient to the viewport. XFORM Transform – Orient to the current transform setting. GEOM Geometry – Match the surface normal.

Orientation, Preset viewpoint to use

NONE None – Leave orientation unchanged.

VIEW View – Orient to the viewport.

XFORM Transform – Orient to the current transform setting.

GEOM Geometry – Match the surface normal.

Dolly in/out in the view

mx (int in [0, inf], (optional)) – Region Position X

my (int in [0, inf], (optional)) – Region Position Y

delta (int in [-inf, inf], (optional)) – Delta

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Drop a world into the scene

name (string, (optional, never None)) – Name, Name of the data-block to use by the operator

session_uid (int in [-inf, inf], (optional)) – Session UID, Session UID of the data-block to use by the operator

Extrude each individual face separately along local normals

startup/bl_operators/view3d.py:30

Extrude manifold region along normals

startup/bl_operators/view3d.py:198

Extrude region together along the average normal

dissolve_and_intersect (boolean, (optional)) – dissolve_and_intersect, Dissolves adjacent faces and intersects new geometry

startup/bl_operators/view3d.py:166

Extrude region together along local normals

startup/bl_operators/view3d.py:182

Interactively fly around the scene

Interactively add an object

primitive_type (enum in ['CUBE', 'CYLINDER', 'CONE', 'SPHERE_UV', 'SPHERE_ICO'], (optional)) – Primitive

plane_origin_base (enum in ['EDGE', 'CENTER'], (optional)) – Origin, The initial position for placement EDGE Edge – Start placing the edge position. CENTER Center – Start placing the center position.

Origin, The initial position for placement

EDGE Edge – Start placing the edge position.

CENTER Center – Start placing the center position.

plane_origin_depth (enum in ['EDGE', 'CENTER'], (optional)) – Origin, The initial position for placement EDGE Edge – Start placing the edge position. CENTER Center – Start placing the center position.

Origin, The initial position for placement

EDGE Edge – Start placing the edge position.

CENTER Center – Start placing the center position.

plane_aspect_base (enum in ['FREE', 'FIXED'], (optional)) – Aspect, The initial aspect setting FREE Free – Use an unconstrained aspect. FIXED Fixed – Use a fixed 1:1 aspect.

Aspect, The initial aspect setting

FREE Free – Use an unconstrained aspect.

FIXED Fixed – Use a fixed 1:1 aspect.

plane_aspect_depth (enum in ['FREE', 'FIXED'], (optional)) – Aspect, The initial aspect setting FREE Free – Use an unconstrained aspect. FIXED Fixed – Use a fixed 1:1 aspect.

Aspect, The initial aspect setting

FREE Free – Use an unconstrained aspect.

FIXED Fixed – Use a fixed 1:1 aspect.

wait_for_input (boolean, (optional)) – Wait for Input

Toggle display of selected object(s) separately and centered in view

frame_selected (boolean, (optional)) – Frame Selected, Move the view to frame the selected objects

Move selected objects out of local view

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Interactively navigate around the scene (uses the mode (walk/fly) preference)

Pan and rotate the view with the 3D mouse

Orbit the view using the 3D mouse

Orbit and zoom the view using the 3D mouse

Pan the view with the 3D mouse

Set the active object as the active camera for this view or scene

Undocumented, consider contributing.

Paste objects from the internal clipboard

autoselect (boolean, (optional)) – Select, Select pasted objects

active_collection (boolean, (optional)) – Active Collection, Put pasted objects in the active collection

Set the boundaries of the border render and enable border render

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Undocumented, consider contributing.

Select and activate item(s)

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

center (boolean, (optional)) – Center, Use the object center when selecting, in edit mode used to extend object selection

enumerate (boolean, (optional)) – Enumerate, List objects under the mouse (object mode only)

object (boolean, (optional)) – Object, Use object selection (edit mode only)

location (int array of 2 items in [-inf, inf], (optional)) – Location, Mouse location

Select items using box selection

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB', 'XOR', 'AND'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection. XOR Difference – Invert existing selection. AND Intersect – Intersect existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

XOR Difference – Invert existing selection.

AND Intersect – Intersect existing selection.

Select items using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select items using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB', 'XOR', 'AND'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection. XOR Difference – Invert existing selection. AND Intersect – Intersect existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

XOR Difference – Invert existing selection.

AND Intersect – Intersect existing selection.

Menu object selection

name (enum in [], (optional)) – Object Name

extend (boolean, (optional)) – Extend

deselect (boolean, (optional)) – Deselect

toggle (boolean, (optional)) – Toggle

Undocumented, consider contributing.

Snap 3D cursor to the active item

Snap 3D cursor to the world origin

Snap 3D cursor to the nearest grid division

Snap 3D cursor to the middle of the selected item(s)

Snap selected item(s) to the active item

Snap selected item(s) to the 3D cursor

use_offset (boolean, (optional)) – Offset, If the selection should be snapped as a whole or by each object center

use_rotation (boolean, (optional)) – Rotation, If the selection should be rotated to match the cursor

Snap selected item(s) to their nearest grid division

Toggle shading type in 3D viewport

type (enum in ['WIREFRAME', 'SOLID', 'MATERIAL', 'RENDERED'], (optional)) – Type, Shading type to toggle WIREFRAME Wireframe – Toggle wireframe shading. SOLID Solid – Toggle solid shading. MATERIAL Material Preview – Toggle material preview shading. RENDERED Rendered – Toggle rendered shading.

Type, Shading type to toggle

WIREFRAME Wireframe – Toggle wireframe shading.

SOLID Solid – Toggle solid shading.

MATERIAL Material Preview – Toggle material preview shading.

RENDERED Rendered – Toggle rendered shading.

Transparent scene display. Allow selecting through items

Set the current transform gizmo

extend (boolean, (optional)) – Extend

type (enum set in {'TRANSLATE', 'ROTATE', 'SCALE'}, (optional)) – Type

startup/bl_operators/view3d.py:245

View all objects in scene

use_all_regions (boolean, (optional)) – All Regions, View selected for all regions

center (boolean, (optional)) – Center

Use a preset viewpoint

type (enum in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', 'BACK'], (optional)) – View, Preset viewpoint to use LEFT Left – View from the left. RIGHT Right – View from the right. BOTTOM Bottom – View from the bottom. TOP Top – View from the top. FRONT Front – View from the front. BACK Back – View from the back.

View, Preset viewpoint to use

LEFT Left – View from the left.

RIGHT Right – View from the right.

BOTTOM Bottom – View from the bottom.

TOP Top – View from the top.

FRONT Front – View from the front.

BACK Back – View from the back.

align_active (boolean, (optional)) – Align Active, Align to the active object’s axis

relative (boolean, (optional)) – Relative, Rotate relative to the current orientation

Toggle the camera view

Center the camera view, resizing the view to fit its bounds

Center the view so that the cursor is in the middle of the view

Center the view lock offset

Center the view to the Z-depth position under the mouse cursor

Clear all view locking

Lock the view to the active object/bone

angle (float in [-inf, inf], (optional)) – Roll

type (enum in ['ORBITLEFT', 'ORBITRIGHT', 'ORBITUP', 'ORBITDOWN'], (optional)) – Orbit, Direction of View Orbit ORBITLEFT Orbit Left – Orbit the view around to the left. ORBITRIGHT Orbit Right – Orbit the view around to the right. ORBITUP Orbit Up – Orbit the view up. ORBITDOWN Orbit Down – Orbit the view down.

Orbit, Direction of View Orbit

ORBITLEFT Orbit Left – Orbit the view around to the left.

ORBITRIGHT Orbit Right – Orbit the view around to the right.

ORBITUP Orbit Up – Orbit the view up.

ORBITDOWN Orbit Down – Orbit the view down.

Pan the view in a given direction

type (enum in ['PANLEFT', 'PANRIGHT', 'PANUP', 'PANDOWN'], (optional)) – Pan, Direction of View Pan PANLEFT Pan Left – Pan the view to the left. PANRIGHT Pan Right – Pan the view to the right. PANUP Pan Up – Pan the view up. PANDOWN Pan Down – Pan the view down.

Pan, Direction of View Pan

PANLEFT Pan Left – Pan the view to the left.

PANRIGHT Pan Right – Pan the view to the right.

PANUP Pan Up – Pan the view up.

PANDOWN Pan Down – Pan the view down.

Switch the current view from perspective/orthographic projection

angle (float in [-inf, inf], (optional)) – Roll

type (enum in ['ANGLE', 'LEFT', 'RIGHT'], (optional)) – Roll Angle Source, How roll angle is calculated ANGLE Roll Angle – Roll the view using an angle value. LEFT Roll Left – Roll the view around to the left. RIGHT Roll Right – Roll the view around to the right.

Roll Angle Source, How roll angle is calculated

ANGLE Roll Angle – Roll the view using an angle value.

LEFT Roll Left – Roll the view around to the left.

RIGHT Roll Right – Roll the view around to the right.

Move the view to the selection center

use_all_regions (boolean, (optional)) – All Regions, View selected for all regions

Interactively walk around the scene

Zoom in/out in the view

mx (int in [0, inf], (optional)) – Region Position X

my (int in [0, inf], (optional)) – Region Position Y

delta (int in [-inf, inf], (optional)) – Delta

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Zoom in the view to the nearest object contained in the border

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

zoom_out (boolean, (optional)) – Zoom Out

Match the camera to 1:1 to the render output

---

## Uv Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.uv.html

**Contents:**
- Uv Operators¶

Aligns selected UV vertices on a line

axis (enum in ['ALIGN_S', 'ALIGN_T', 'ALIGN_U', 'ALIGN_AUTO', 'ALIGN_X', 'ALIGN_Y'], (optional)) – Axis, Axis to align UV locations on ALIGN_S Straighten – Align UV vertices along the line defined by the endpoints. ALIGN_T Straighten X – Align UV vertices, moving them horizontally to the line defined by the endpoints. ALIGN_U Straighten Y – Align UV vertices, moving them vertically to the line defined by the endpoints. ALIGN_AUTO Align Auto – Automatically choose the direction on which there is most alignment already. ALIGN_X Align Vertically – Align UV vertices on a vertical line. ALIGN_Y Align Horizontally – Align UV vertices on a horizontal line.

Axis, Axis to align UV locations on

ALIGN_S Straighten – Align UV vertices along the line defined by the endpoints.

ALIGN_T Straighten X – Align UV vertices, moving them horizontally to the line defined by the endpoints.

ALIGN_U Straighten Y – Align UV vertices, moving them vertically to the line defined by the endpoints.

ALIGN_AUTO Align Auto – Automatically choose the direction on which there is most alignment already.

ALIGN_X Align Vertically – Align UV vertices on a vertical line.

ALIGN_Y Align Horizontally – Align UV vertices on a horizontal line.

position_mode (enum in ['MEAN', 'MIN', 'MAX'], (optional)) – Position Mode, Method of calculating the alignment position MEAN Mean – Align UVs along the mean position. MIN Minimum – Align UVs along the minimum position. MAX Maximum – Align UVs along the maximum position.

Position Mode, Method of calculating the alignment position

MEAN Mean – Align UVs along the mean position.

MIN Minimum – Align UVs along the minimum position.

MAX Maximum – Align UVs along the maximum position.

Align the UV island’s rotation

method (enum in ['AUTO', 'EDGE', 'GEOMETRY'], (optional)) – Method, Method to calculate rotation angle AUTO Auto – Align from all edges. EDGE Edge – Only selected edges. GEOMETRY Geometry – Align to Geometry axis.

Method, Method to calculate rotation angle

AUTO Auto – Align from all edges.

EDGE Edge – Only selected edges.

GEOMETRY Geometry – Align to Geometry axis.

axis (enum in ['X', 'Y', 'Z'], (optional)) – Axis, Axis to align to X X – X axis. Y Y – Y axis. Z Z – Z axis.

Axis, Axis to align to

correct_aspect (boolean, (optional)) – Correct Aspect, Take image aspect ratio into account

startup/bl_operators/uvcalc_transform.py:360

Arrange selected UV islands on a line

initial_position (enum in ['BOUNDING_BOX', 'UV_GRID', 'ACTIVE_UDIM', 'CURSOR'], (optional)) – Initial Position, Initial position to arrange islands from BOUNDING_BOX Bounding Box – Initial alignment based on the islands bounding box. UV_GRID UV Grid – Initial alignment based on UV Tile Grid. ACTIVE_UDIM Active UDIM – Initial alignment based on Active UDIM. CURSOR 2D Cursor – Initial alignment based on 2D cursor.

Initial Position, Initial position to arrange islands from

BOUNDING_BOX Bounding Box – Initial alignment based on the islands bounding box.

UV_GRID UV Grid – Initial alignment based on UV Tile Grid.

ACTIVE_UDIM Active UDIM – Initial alignment based on Active UDIM.

CURSOR 2D Cursor – Initial alignment based on 2D cursor.

axis (enum in ['X', 'Y'], (optional)) – Axis, Axis to arrange UV islands on X X – Align UV islands along the X axis. Y Y – Align UV islands along the Y axis.

Axis, Axis to arrange UV islands on

X X – Align UV islands along the X axis.

Y Y – Align UV islands along the Y axis.

align (enum in ['MIN', 'MAX', 'CENTER', 'NONE'], (optional)) – Align, Location to align islands on MIN Min – Align the islands to the min of the island. MAX Max – Align the islands to the left side of the island. CENTER Center – Align the islands to the center of the largest island. NONE None – Preserve island alignment.

Align, Location to align islands on

MIN Min – Align the islands to the min of the island.

MAX Max – Align the islands to the left side of the island.

CENTER Center – Align the islands to the center of the largest island.

NONE None – Preserve island alignment.

order (enum in ['LARGE_TO_SMALL', 'SMALL_TO_LARGE', 'Fixed'], (optional)) – Order, Order of islands LARGE_TO_SMALL Largest to Smallest – Sort islands from largest to smallest. SMALL_TO_LARGE Smallest to Largest – Sort islands from smallest to largest. Fixed Fixed – Preserve island order.

Order, Order of islands

LARGE_TO_SMALL Largest to Smallest – Sort islands from largest to smallest.

SMALL_TO_LARGE Smallest to Largest – Sort islands from smallest to largest.

Fixed Fixed – Preserve island order.

margin (float in [0, 1], (optional)) – Margin, Space between islands

Average the size of separate UV islands, based on their area in 3D space

scale_uv (boolean, (optional)) – Non-Uniform, Scale U and V independently

shear (boolean, (optional)) – Shear, Reduce shear within islands

Copy selected UV vertices

Copy mirror UV coordinates on the X axis based on a mirrored mesh

direction (enum in ['POSITIVE', 'NEGATIVE'], (optional)) – Axis Direction

precision (int in [1, 16], (optional)) – Precision, Tolerance for finding vertex duplicates

Project the UV vertices of the mesh over the six faces of a cube

cube_size (float in [0, inf], (optional)) – Cube Size, Size of the cube to project on

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

clip_to_bounds (boolean, (optional)) – Clip to Bounds, Clip UV coordinates to bounds after unwrapping

scale_to_bounds (boolean, (optional)) – Scale to Bounds, Scale UV coordinates to bounds after unwrapping

Set 2D cursor location

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Cursor location in normalized (0.0 to 1.0) coordinates

Set the boundaries of the user region

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

Project the UV vertices of the mesh over the curved wall of a cylinder

direction (enum in ['VIEW_ON_EQUATOR', 'VIEW_ON_POLES', 'ALIGN_TO_OBJECT'], (optional)) – Direction, Direction of the sphere or cylinder VIEW_ON_EQUATOR View on Equator – 3D view is on the equator. VIEW_ON_POLES View on Poles – 3D view is on the poles. ALIGN_TO_OBJECT Align to Object – Align according to object transform.

Direction, Direction of the sphere or cylinder

VIEW_ON_EQUATOR View on Equator – 3D view is on the equator.

VIEW_ON_POLES View on Poles – 3D view is on the poles.

ALIGN_TO_OBJECT Align to Object – Align according to object transform.

align (enum in ['POLAR_ZX', 'POLAR_ZY'], (optional)) – Align, How to determine rotation around the pole POLAR_ZX Polar ZX – Polar 0 is X. POLAR_ZY Polar ZY – Polar 0 is Y.

Align, How to determine rotation around the pole

POLAR_ZX Polar ZX – Polar 0 is X.

POLAR_ZY Polar ZY – Polar 0 is Y.

pole (enum in ['PINCH', 'FAN'], (optional)) – Pole, How to handle faces at the poles PINCH Pinch – UVs are pinched at the poles. FAN Fan – UVs are fanned at the poles.

Pole, How to handle faces at the poles

PINCH Pinch – UVs are pinched at the poles.

FAN Fan – UVs are fanned at the poles.

seam (boolean, (optional)) – Preserve Seams, Separate projections by islands isolated by seams

radius (float in [0, inf], (optional)) – Radius, Radius of the sphere or cylinder

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

clip_to_bounds (boolean, (optional)) – Clip to Bounds, Clip UV coordinates to bounds after unwrapping

scale_to_bounds (boolean, (optional)) – Scale to Bounds, Scale UV coordinates to bounds after unwrapping

Export UV layout to file

filepath (string, (optional, never None)) – filepath

export_all (boolean, (optional)) – All UVs, Export all UVs in this mesh (not just visible ones)

export_tiles (enum in ['NONE', 'UDIM', 'UV'], (optional)) – Export Tiles, Choose whether to export only the [0, 1] range, or all UV tiles NONE None – Export only UVs in the [0, 1] range. UDIM UDIM – Export tiles in the UDIM numbering scheme: 1001 + u_tile + 10*v_tile. UV UVTILE – Export tiles in the UVTILE numbering scheme: u(u_tile + 1)_v(v_tile + 1).

Export Tiles, Choose whether to export only the [0, 1] range, or all UV tiles

NONE None – Export only UVs in the [0, 1] range.

UDIM UDIM – Export tiles in the UDIM numbering scheme: 1001 + u_tile + 10*v_tile.

UV UVTILE – Export tiles in the UVTILE numbering scheme: u(u_tile + 1)_v(v_tile + 1).

modified (boolean, (optional)) – Modified, Exports UVs from the modified mesh

mode (enum in ['SVG', 'EPS', 'PNG'], (optional)) – Format, File format to export the UV layout to SVG Scalable Vector Graphic (.svg) – Export the UV layout to a vector SVG file. EPS Encapsulated PostScript (.eps) – Export the UV layout to a vector EPS file. PNG PNG Image (.png) – Export the UV layout to a bitmap image.

Format, File format to export the UV layout to

SVG Scalable Vector Graphic (.svg) – Export the UV layout to a vector SVG file.

EPS Encapsulated PostScript (.eps) – Export the UV layout to a vector EPS file.

PNG PNG Image (.png) – Export the UV layout to a bitmap image.

size (int array of 2 items in [8, 32768], (optional)) – Size, Dimensions of the exported file

opacity (float in [0, 1], (optional)) – Fill Opacity, Set amount of opacity for exported UV layout

check_existing (boolean, (optional)) – check_existing

addons_core/io_mesh_uv_layout/__init__.py:139

Follow UVs from active quads along continuous face loops

mode (enum in ['EVEN', 'LENGTH', 'LENGTH_AVERAGE'], (optional)) – Edge Length Mode, Method to space UV edge loops EVEN Even – Space all UVs evenly. LENGTH Length – Average space UVs edge length of each loop. LENGTH_AVERAGE Length Average – Average space UVs edge length of each loop.

Edge Length Mode, Method to space UV edge loops

EVEN Even – Space all UVs evenly.

LENGTH Length – Average space UVs edge length of each loop.

LENGTH_AVERAGE Length Average – Average space UVs edge length of each loop.

startup/bl_operators/uvcalc_follow_active.py:302

Hide (un)selected UV vertices

unselected (boolean, (optional)) – Unselected, Hide unselected rather than selected

Pack each face’s UVs into the UV bounds

PREF_CONTEXT (enum in ['SEL_FACES', 'ALL_FACES'], (optional)) – Selection SEL_FACES Selected Faces – Space all UVs evenly. ALL_FACES All Faces – Average space UVs edge length of each loop.

SEL_FACES Selected Faces – Space all UVs evenly.

ALL_FACES All Faces – Average space UVs edge length of each loop.

PREF_PACK_IN_ONE (boolean, (optional)) – Share Texture Space, Objects share texture space, map all objects into a single UV map

PREF_NEW_UVLAYER (boolean, (optional)) – New UV Map, Create a new UV map for every mesh packed

PREF_BOX_DIV (int in [1, 48], (optional)) – Pack Quality, Quality of the packing. Higher values will be slower but waste less space

PREF_MARGIN_DIV (float in [0.001, 1], (optional)) – Margin, Size of the margin as a division of the UV

startup/bl_operators/uvcalc_lightmap.py:662

Mark selected UV edges as seams

clear (boolean, (optional)) – Clear Seams, Clear instead of marking seams

Reduce UV stretching by relaxing angles

fill_holes (boolean, (optional)) – Fill Holes, Virtually fill holes in mesh before unwrapping, to better avoid overlaps and preserve symmetry

blend (float in [0, 1], (optional)) – Blend, Blend factor between stretch minimized and original

iterations (int in [0, inf], (optional)) – Iterations, Number of iterations to run, 0 is unlimited when run interactively

type (enum in ['DYNAMIC', 'PIXEL', 'UDIM'], (optional)) – Type, Move Type DYNAMIC Dynamic – Move by dynamic grid. PIXEL Pixel – Move by pixel. UDIM UDIM – Move by UDIM.

DYNAMIC Dynamic – Move by dynamic grid.

PIXEL Pixel – Move by pixel.

UDIM UDIM – Move by UDIM.

axis (enum in ['X', 'Y'], (optional)) – Axis, Axis to move UVs on X X axis – Move vertices on the X axis. Y Y axis – Move vertices on the Y axis.

Axis, Axis to move UVs on

X X axis – Move vertices on the X axis.

Y Y axis – Move vertices on the Y axis.

distance (int in [-inf, inf], (optional)) – Distance, Distance to move UVs

Transform all islands so that they fill up the UV/UDIM space as much as possible

udim_source (enum in ['CLOSEST_UDIM', 'ACTIVE_UDIM', 'ORIGINAL_AABB', 'CUSTOM_REGION'], (optional)) – Pack to CLOSEST_UDIM Closest UDIM – Pack islands to closest UDIM. ACTIVE_UDIM Active UDIM – Pack islands to active UDIM image tile or UDIM grid tile where 2D cursor is located. ORIGINAL_AABB Original bounding box – Pack to starting bounding box of islands. CUSTOM_REGION Custom Region – Pack islands to custom region.

CLOSEST_UDIM Closest UDIM – Pack islands to closest UDIM.

ACTIVE_UDIM Active UDIM – Pack islands to active UDIM image tile or UDIM grid tile where 2D cursor is located.

ORIGINAL_AABB Original bounding box – Pack to starting bounding box of islands.

CUSTOM_REGION Custom Region – Pack islands to custom region.

rotate (boolean, (optional)) – Rotate, Rotate islands to improve layout

rotate_method (enum in ['ANY', 'CARDINAL', 'AXIS_ALIGNED', 'AXIS_ALIGNED_X', 'AXIS_ALIGNED_Y'], (optional)) – Rotation Method ANY Any – Any angle is allowed for rotation. CARDINAL Cardinal – Only 90 degree rotations are allowed. AXIS_ALIGNED Axis-aligned – Rotated to a minimal rectangle, either vertical or horizontal. AXIS_ALIGNED_X Axis-aligned (Horizontal) – Rotate islands to be aligned horizontally. AXIS_ALIGNED_Y Axis-aligned (Vertical) – Rotate islands to be aligned vertically.

ANY Any – Any angle is allowed for rotation.

CARDINAL Cardinal – Only 90 degree rotations are allowed.

AXIS_ALIGNED Axis-aligned – Rotated to a minimal rectangle, either vertical or horizontal.

AXIS_ALIGNED_X Axis-aligned (Horizontal) – Rotate islands to be aligned horizontally.

AXIS_ALIGNED_Y Axis-aligned (Vertical) – Rotate islands to be aligned vertically.

scale (boolean, (optional)) – Scale, Scale islands to fill unit square

merge_overlap (boolean, (optional)) – Merge Overlapping, Overlapping islands stick together

margin_method (enum in ['SCALED', 'ADD', 'FRACTION'], (optional)) – Margin Method SCALED Scaled – Use scale of existing UVs to multiply margin. ADD Add – Just add the margin, ignoring any UV scale. FRACTION Fraction – Specify a precise fraction of final UV output.

SCALED Scaled – Use scale of existing UVs to multiply margin.

ADD Add – Just add the margin, ignoring any UV scale.

FRACTION Fraction – Specify a precise fraction of final UV output.

margin (float in [0, 1], (optional)) – Margin, Space between islands

pin (boolean, (optional)) – Lock Pinned Islands, Constrain islands containing any pinned UV’s

pin_method (enum in ['SCALE', 'ROTATION', 'ROTATION_SCALE', 'LOCKED'], (optional)) – Pin Method SCALE Scale – Pinned islands won’t rescale. ROTATION Rotation – Pinned islands won’t rotate. ROTATION_SCALE Rotation and Scale – Pinned islands will translate only. LOCKED All – Pinned islands are locked in place.

SCALE Scale – Pinned islands won’t rescale.

ROTATION Rotation – Pinned islands won’t rotate.

ROTATION_SCALE Rotation and Scale – Pinned islands will translate only.

LOCKED All – Pinned islands are locked in place.

shape_method (enum in ['CONCAVE', 'CONVEX', 'AABB'], (optional)) – Shape Method CONCAVE Exact Shape (Concave) – Uses exact geometry. CONVEX Boundary Shape (Convex) – Uses convex hull. AABB Bounding Box – Uses bounding boxes.

CONCAVE Exact Shape (Concave) – Uses exact geometry.

CONVEX Boundary Shape (Convex) – Uses convex hull.

AABB Bounding Box – Uses bounding boxes.

Paste selected UV vertices

Set/clear selected UV vertices as anchored between multiple unwrap operations

clear (boolean, (optional)) – Clear, Clear pinning for the selection instead of setting it

invert (boolean, (optional)) – Invert, Invert pinning for the selection instead of setting it

Project the UV vertices of the mesh as seen in current 3D view

orthographic (boolean, (optional)) – Orthographic, Use orthographic projection

camera_bounds (boolean, (optional)) – Camera Bounds, Map UVs to the camera region taking resolution and aspect into account

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

clip_to_bounds (boolean, (optional)) – Clip to Bounds, Clip UV coordinates to bounds after unwrapping

scale_to_bounds (boolean, (optional)) – Scale to Bounds, Scale UV coordinates to bounds after unwrapping

Randomize the UV island’s location, rotation, and scale

random_seed (int in [0, 10000], (optional)) – Random Seed, Seed value for the random generator

use_loc (boolean, (optional)) – Randomize Location, Randomize the location values

loc (mathutils.Vector of 2 items in [-100, 100], (optional)) – Location, Maximum distance the objects can spread over each axis

use_rot (boolean, (optional)) – Randomize Rotation, Randomize the rotation value

rot (float in [-6.28319, 6.28319], (optional)) – Rotation, Maximum rotation

use_scale (boolean, (optional)) – Randomize Scale, Randomize the scale values

scale_even (boolean, (optional)) – Scale Even, Use the same scale value for both axes

scale (float array of 2 items in [-100, 100], (optional)) – Scale, Maximum scale randomization over each axis

startup/bl_operators/uvcalc_transform.py:536

Selected UV vertices that are within a radius of each other are welded together

threshold (float in [0, 10], (optional)) – Merge Distance, Maximum distance between welded vertices

use_unselected (boolean, (optional)) – Unselected, Merge selected to other unselected vertices

use_shared_vertex (boolean, (optional)) – Shared Vertex, Weld UVs based on shared vertices

Reveal all hidden UV vertices

select (boolean, (optional)) – Select

Rip selected vertices or a selected region

mirror (boolean, (optional)) – Mirror Editing

release_confirm (boolean, (optional)) – Confirm on Release, Always confirm operation when releasing button

use_accurate (boolean, (optional)) – Accurate, Use accurate transformation

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Unstitch UVs and move the result

UV_OT_rip (UV_OT_rip, (optional)) – UV Rip, Rip selected vertices or a selected region

TRANSFORM_OT_translate (TRANSFORM_OT_translate, (optional)) – Move, Move selected items

Set mesh seams according to island setup in the UV editor

mark_seams (boolean, (optional)) – Mark Seams, Mark boundary edges as seams

mark_sharp (boolean, (optional)) – Mark Sharp, Mark boundary edges as sharp

extend (boolean, (optional)) – Extend, Extend selection instead of deselecting everything first

deselect (boolean, (optional)) – Deselect, Remove from selection

toggle (boolean, (optional)) – Toggle Selection, Toggle the selection

deselect_all (boolean, (optional)) – Deselect On Nothing, Deselect all when nothing under the cursor

select_passthrough (boolean, (optional)) – Only Select Unselected, Ignore the select action when the element is already selected

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Change selection of all UV vertices

action (enum in ['TOGGLE', 'SELECT', 'DESELECT', 'INVERT'], (optional)) – Action, Selection action to execute TOGGLE Toggle – Toggle selection for all elements. SELECT Select – Select all elements. DESELECT Deselect – Deselect all elements. INVERT Invert – Invert selection of all elements.

Action, Selection action to execute

TOGGLE Toggle – Toggle selection for all elements.

SELECT Select – Select all elements.

DESELECT Deselect – Deselect all elements.

INVERT Invert – Invert selection of all elements.

Select UV vertices using box selection

pinned (boolean, (optional)) – Pinned, Border select pinned UVs only

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select UV vertices using circle selection

x (int in [-inf, inf], (optional)) – X

y (int in [-inf, inf], (optional)) – Y

radius (int in [1, inf], (optional)) – Radius

wait_for_input (boolean, (optional)) – Wait for Input

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Select an edge ring of connected UV vertices

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Select UVs using lasso selection

path (bpy_prop_collection of OperatorMousePath, (optional)) – Path

use_smooth_stroke (boolean, (optional)) – Stabilize Stroke, Selection lags behind mouse and follows a smoother path

smooth_stroke_factor (float in [0.5, 0.99], (optional)) – Smooth Stroke Factor, Higher values gives a smoother stroke

smooth_stroke_radius (int in [10, 200], (optional)) – Smooth Stroke Radius, Minimum distance from last point before selection continues

mode (enum in ['SET', 'ADD', 'SUB'], (optional)) – Mode SET Set – Set a new selection. ADD Extend – Extend existing selection. SUB Subtract – Subtract existing selection.

SET Set – Set a new selection.

ADD Extend – Extend existing selection.

SUB Subtract – Subtract existing selection.

Deselect UV vertices at the boundary of each selection region

Select all UV vertices linked to the active UV map

Select all UV vertices linked under the mouse

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

deselect (boolean, (optional)) – Deselect, Deselect linked UV vertices rather than selecting them

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Select a loop of connected UV vertices

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

location (mathutils.Vector of 2 items in [-inf, inf], (optional)) – Location, Mouse location in normalized coordinates, 0.0 to 1.0 is within the image bounds

Change UV selection mode

type (enum in Mesh Select Mode Uv Items, (optional)) – Type

Select more UV vertices connected to initial selection

Select all UV faces which overlap each other

extend (boolean, (optional)) – Extend, Extend selection rather than clearing the existing selection

Select all pinned UV vertices

Select similar UVs by property types

type (enum in ['PIN', 'LENGTH', 'LENGTH_3D', 'AREA', 'AREA_3D', 'MATERIAL', 'OBJECT', 'SIDES', 'WINDING', 'FACE'], (optional)) – Type PIN Pinned. LENGTH Length – Edge length in UV space. LENGTH_3D Length 3D – Length of edge in 3D space. AREA Area – Face area in UV space. AREA_3D Area 3D – Area of face in 3D space. MATERIAL Material. OBJECT Object. SIDES Polygon Sides. WINDING Winding – Face direction defined by (clockwise or anti-clockwise winding (facing up or facing down). FACE Amount of Faces in Island.

LENGTH Length – Edge length in UV space.

LENGTH_3D Length 3D – Length of edge in 3D space.

AREA Area – Face area in UV space.

AREA_3D Area 3D – Area of face in 3D space.

WINDING Winding – Face direction defined by (clockwise or anti-clockwise winding (facing up or facing down).

FACE Amount of Faces in Island.

compare (enum in ['EQUAL', 'GREATER', 'LESS'], (optional)) – Compare

threshold (float in [0, 1], (optional)) – Threshold

Select only entirely selected faces

Select shortest path between two selections

use_face_step (boolean, (optional)) – Face Stepping, Traverse connected faces (includes diagonals and edge-rings)

use_topology_distance (boolean, (optional)) – Topology Distance, Find the minimum number of steps, ignoring spatial distance

use_fill (boolean, (optional)) – Fill Region, Select all paths between the source/destination elements

skip (int in [0, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Selected shortest path between two vertices/edges/faces

use_face_step (boolean, (optional)) – Face Stepping, Traverse connected faces (includes diagonals and edge-rings)

use_topology_distance (boolean, (optional)) – Topology Distance, Find the minimum number of steps, ignoring spatial distance

use_fill (boolean, (optional)) – Fill Region, Select all paths between the source/destination elements

skip (int in [0, inf], (optional)) – Deselected, Number of deselected elements in the repetitive sequence

nth (int in [1, inf], (optional)) – Selected, Number of selected elements in the repetitive sequence

offset (int in [-inf, inf], (optional)) – Offset, Offset from the starting point

Projection unwraps the selected faces of mesh objects

angle_limit (float in [0, 1.5708], (optional)) – Angle Limit, Lower for more projection groups, higher for less distortion

margin_method (enum in ['SCALED', 'ADD', 'FRACTION'], (optional)) – Margin Method SCALED Scaled – Use scale of existing UVs to multiply margin. ADD Add – Just add the margin, ignoring any UV scale. FRACTION Fraction – Specify a precise fraction of final UV output.

SCALED Scaled – Use scale of existing UVs to multiply margin.

ADD Add – Just add the margin, ignoring any UV scale.

FRACTION Fraction – Specify a precise fraction of final UV output.

rotate_method (enum in ['AXIS_ALIGNED', 'AXIS_ALIGNED_X', 'AXIS_ALIGNED_Y'], (optional)) – Rotation Method AXIS_ALIGNED Axis-aligned – Rotated to a minimal rectangle, either vertical or horizontal. AXIS_ALIGNED_X Axis-aligned (Horizontal) – Rotate islands to be aligned horizontally. AXIS_ALIGNED_Y Axis-aligned (Vertical) – Rotate islands to be aligned vertically.

AXIS_ALIGNED Axis-aligned – Rotated to a minimal rectangle, either vertical or horizontal.

AXIS_ALIGNED_X Axis-aligned (Horizontal) – Rotate islands to be aligned horizontally.

AXIS_ALIGNED_Y Axis-aligned (Vertical) – Rotate islands to be aligned vertically.

island_margin (float in [0, 1], (optional)) – Island Margin, Margin to reduce bleed from adjacent islands

area_weight (float in [0, 1], (optional)) – Area Weight, Weight projection’s vector by faces with larger areas

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

scale_to_bounds (boolean, (optional)) – Scale to Bounds, Scale UV coordinates to bounds after unwrapping

Snap cursor to target type

target (enum in ['PIXELS', 'SELECTED', 'ORIGIN'], (optional)) – Target, Target to snap the selected UVs to

Snap selected UV vertices to target type

target (enum in ['PIXELS', 'CURSOR', 'CURSOR_OFFSET', 'ADJACENT_UNSELECTED'], (optional)) – Target, Target to snap the selected UVs to

Project the UV vertices of the mesh over the curved surface of a sphere

direction (enum in ['VIEW_ON_EQUATOR', 'VIEW_ON_POLES', 'ALIGN_TO_OBJECT'], (optional)) – Direction, Direction of the sphere or cylinder VIEW_ON_EQUATOR View on Equator – 3D view is on the equator. VIEW_ON_POLES View on Poles – 3D view is on the poles. ALIGN_TO_OBJECT Align to Object – Align according to object transform.

Direction, Direction of the sphere or cylinder

VIEW_ON_EQUATOR View on Equator – 3D view is on the equator.

VIEW_ON_POLES View on Poles – 3D view is on the poles.

ALIGN_TO_OBJECT Align to Object – Align according to object transform.

align (enum in ['POLAR_ZX', 'POLAR_ZY'], (optional)) – Align, How to determine rotation around the pole POLAR_ZX Polar ZX – Polar 0 is X. POLAR_ZY Polar ZY – Polar 0 is Y.

Align, How to determine rotation around the pole

POLAR_ZX Polar ZX – Polar 0 is X.

POLAR_ZY Polar ZY – Polar 0 is Y.

pole (enum in ['PINCH', 'FAN'], (optional)) – Pole, How to handle faces at the poles PINCH Pinch – UVs are pinched at the poles. FAN Fan – UVs are fanned at the poles.

Pole, How to handle faces at the poles

PINCH Pinch – UVs are pinched at the poles.

FAN Fan – UVs are fanned at the poles.

seam (boolean, (optional)) – Preserve Seams, Separate projections by islands isolated by seams

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

clip_to_bounds (boolean, (optional)) – Clip to Bounds, Clip UV coordinates to bounds after unwrapping

scale_to_bounds (boolean, (optional)) – Scale to Bounds, Scale UV coordinates to bounds after unwrapping

Stitch selected UV vertices by proximity

use_limit (boolean, (optional)) – Use Limit, Stitch UVs within a specified limit distance

snap_islands (boolean, (optional)) – Snap Islands, Snap islands together (on edge stitch mode, rotates the islands too)

limit (float in [0, inf], (optional)) – Limit, Limit distance in normalized coordinates

static_island (int in [0, inf], (optional)) – Static Island, Island that stays in place when stitching islands

active_object_index (int in [0, inf], (optional)) – Active Object, Index of the active object

midpoint_snap (boolean, (optional)) – Snap at Midpoint, UVs are stitched at midpoint instead of at static island

clear_seams (boolean, (optional)) – Clear Seams, Clear seams of stitched edges

mode (enum in ['VERTEX', 'EDGE'], (optional)) – Operation Mode, Use vertex or edge stitching

stored_mode (enum in ['VERTEX', 'EDGE'], (optional)) – Stored Operation Mode, Use vertex or edge stitching

selection (bpy_prop_collection of SelectedUvElement, (optional)) – Selection

objects_selection_count (int array of 6 items in [0, inf], (optional)) – Objects Selection Count

Unwrap the mesh of the object being edited

method (enum in ['ANGLE_BASED', 'CONFORMAL', 'MINIMUM_STRETCH'], (optional)) – Method, Unwrapping method (Angle Based usually gives better results than Conformal, while being somewhat slower)

fill_holes (boolean, (optional)) – Fill Holes, Virtually fill holes in mesh before unwrapping, to better avoid overlaps and preserve symmetry

correct_aspect (boolean, (optional)) – Correct Aspect, Map UVs taking aspect ratio of the image associated with the material into account

use_subsurf_data (boolean, (optional)) – Use Subdivision Surface, Map UVs taking vertex position after Subdivision Surface modifier has been applied

margin_method (enum in ['SCALED', 'ADD', 'FRACTION'], (optional)) – Margin Method SCALED Scaled – Use scale of existing UVs to multiply margin. ADD Add – Just add the margin, ignoring any UV scale. FRACTION Fraction – Specify a precise fraction of final UV output.

SCALED Scaled – Use scale of existing UVs to multiply margin.

ADD Add – Just add the margin, ignoring any UV scale.

FRACTION Fraction – Specify a precise fraction of final UV output.

margin (float in [0, 1], (optional)) – Margin, Space between islands

no_flip (boolean, (optional)) – No Flip, Prevent flipping UV’s, flipping may lower distortion depending on the position of pins

iterations (int in [0, 10000], (optional)) – Iterations, Number of iterations when “Minimum Stretch” method is used

use_weights (boolean, (optional)) – Importance Weights, Whether to take into account per-vertex importance weights

weight_group (string, (optional, never None)) – Weight Group, Vertex group name for importance weights (modulating the deform)

weight_factor (float in [-10000, 10000], (optional)) – Weight Factor, How much influence the weightmap has for weighted parameterization, 0 being no influence

Weld selected UV vertices together

---

## View2D Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.view2d.html

**Contents:**
- View2D Operators¶

Pan the view when the mouse is held at an edge

inside_padding (float in [0, 100], (optional)) – Inside Padding, Inside distance in UI units from the edge of the region within which to start panning

outside_padding (float in [0, 100], (optional)) – Outside Padding, Outside distance in UI units from the edge of the region at which to stop panning

speed_ramp (float in [0, 100], (optional)) – Speed Ramp, Width of the zone in UI units where speed increases with distance from the edge

max_speed (float in [0, 10000], (optional)) – Max Speed, Maximum speed in UI units per second

delay (float in [0, 10], (optional)) – Delay, Delay in seconds before maximum speed is reached

zoom_influence (float in [0, 1], (optional)) – Zoom Influence, Influence of the zoom factor on scroll speed

Use a 3D mouse device to pan/zoom the view

deltax (int in [-inf, inf], (optional)) – Delta X

deltay (int in [-inf, inf], (optional)) – Delta Y

deltax (int in [-inf, inf], (optional)) – Delta X

deltay (int in [-inf, inf], (optional)) – Delta Y

page (boolean, (optional)) – Page, Scroll down one page

deltax (int in [-inf, inf], (optional)) – Delta X

deltay (int in [-inf, inf], (optional)) – Delta Y

Scroll the view right

deltax (int in [-inf, inf], (optional)) – Delta X

deltay (int in [-inf, inf], (optional)) – Delta Y

deltax (int in [-inf, inf], (optional)) – Delta X

deltay (int in [-inf, inf], (optional)) – Delta Y

page (boolean, (optional)) – Page, Scroll up one page

Scroll view by mouse click and drag

Undocumented, consider contributing.

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

deltax (float in [-inf, inf], (optional)) – Delta X

deltay (float in [-inf, inf], (optional)) – Delta Y

use_cursor_init (boolean, (optional)) – Use Mouse Position, Allow the initial mouse position to be used

Zoom in the view to the nearest item contained in the border

xmin (int in [-inf, inf], (optional)) – X Min

xmax (int in [-inf, inf], (optional)) – X Max

ymin (int in [-inf, inf], (optional)) – Y Min

ymax (int in [-inf, inf], (optional)) – Y Max

wait_for_input (boolean, (optional)) – Wait for Input

zoom_out (boolean, (optional)) – Zoom Out

zoomfacx (float in [-inf, inf], (optional)) – Zoom Factor X

zoomfacy (float in [-inf, inf], (optional)) – Zoom Factor Y

zoomfacx (float in [-inf, inf], (optional)) – Zoom Factor X

zoomfacy (float in [-inf, inf], (optional)) – Zoom Factor Y

---

## Workspace Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.workspace.html

**Contents:**
- Workspace Operators¶

Add a new workspace by duplicating the current one or appending one from the user configuration

Append a workspace and make it the active one in the current window

idname (string, (optional, never None)) – Identifier, Name of the workspace to append and activate

filepath (string, (optional, never None, blend relative // prefix supported)) – Filepath, Path to the library

Delete the active workspace

Delete all workspaces except this one

Reorder workspace to be last in the list

Reorder workspace to be first in the list

Remember the last used scene for the current workspace and switch to it whenever this workspace is activated again

---

## World Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.world.html

**Contents:**
- World Operators¶

Convert the volume of a world to a mesh. The world’s volume used to be rendered by EEVEE Legacy. Conversion is needed for it to render properly

startup/bl_operators/world.py:26

Create a new world Data-Block

---

## Wm Operators¶

**URL:** https://docs.blender.org/api/current/bpy.ops.wm.html

**Contents:**
- Wm Operators¶

Export current scene in an Alembic archive

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

start (int in [-inf, inf], (optional)) – Start Frame, Start frame of the export, use the default value to take the start frame of the current scene

end (int in [-inf, inf], (optional)) – End Frame, End frame of the export, use the default value to take the end frame of the current scene

xsamples (int in [1, 128], (optional)) – Transform Samples, Number of times per frame transformations are sampled

gsamples (int in [1, 128], (optional)) – Geometry Samples, Number of times per frame object data are sampled

sh_open (float in [-1, 1], (optional)) – Shutter Open, Time at which the shutter is open

sh_close (float in [-1, 1], (optional)) – Shutter Close, Time at which the shutter is closed

selected (boolean, (optional)) – Selected Objects Only, Export only selected objects

flatten (boolean, (optional)) – Flatten Hierarchy, Do not preserve objects’ parent/children relationship

collection (string, (optional, never None)) – Collection

uvs (boolean, (optional)) – UV Coordinates, Export UV coordinates

packuv (boolean, (optional)) – Merge UVs

normals (boolean, (optional)) – Normals, Export normals

vcolors (boolean, (optional)) – Color Attributes, Export color attributes

orcos (boolean, (optional)) – Generated Coordinates, Export undeformed mesh vertex coordinates

face_sets (boolean, (optional)) – Face Sets, Export per face shading group assignments

subdiv_schema (boolean, (optional)) – Use Subdivision Schema, Export meshes using Alembic’s subdivision schema

apply_subdiv (boolean, (optional)) – Apply Subdivision Surface, Export subdivision surfaces as meshes

curves_as_mesh (boolean, (optional)) – Curves as Mesh, Export curves and NURBS surfaces as meshes

use_instancing (boolean, (optional)) – Use Instancing, Export data of duplicated objects as Alembic instances; speeds up the export and can be disabled for compatibility with other software

global_scale (float in [0.0001, 1000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

triangulate (boolean, (optional)) – Triangulate, Export polygons (quads and n-gons) as triangles

quad_method (enum in Modifier Triangulate Quad Method Items, (optional)) – Quad Method, Method for splitting the quads into triangles

ngon_method (enum in Modifier Triangulate Ngon Method Items, (optional)) – N-gon Method, Method for splitting the n-gons into triangles

export_hair (boolean, (optional)) – Export Hair, Exports hair particle systems as animated curves

export_particles (boolean, (optional)) – Export Particles, Exports non-hair particle systems

export_custom_properties (boolean, (optional)) – Export Custom Properties, Export custom properties to Alembic .userProperties

as_background_job (boolean, (optional)) – Run as Background Job, Enable this to run the import in the background, disable to block Blender while importing. This option is deprecated; EXECUTE this operator to run in the foreground, and INVOKE it to run as a background job

evaluation_mode (enum in ['RENDER', 'VIEWPORT'], (optional)) – Settings, Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering RENDER Render – Use Render settings for object visibility, modifier settings, etc. VIEWPORT Viewport – Use Viewport settings for object visibility, modifier settings, etc.

Settings, Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering

RENDER Render – Use Render settings for object visibility, modifier settings, etc.

VIEWPORT Viewport – Use Viewport settings for object visibility, modifier settings, etc.

Load an Alembic archive

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

scale (float in [0.0001, 1000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

set_frame_range (boolean, (optional)) – Set Frame Range, If checked, update scene’s start and end frame to match those of the Alembic archive

validate_meshes (boolean, (optional)) – Validate Meshes, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing)

always_add_cache_reader (boolean, (optional)) – Always Add Cache Reader, Add cache modifiers and constraints to imported objects even if they are not animated so that they can be updated when reloading the Alembic archive

is_sequence (boolean, (optional)) – Is Sequence, Set to true if the cache is split into separate files

as_background_job (boolean, (optional)) – Run as Background Job, Enable this to run the export in the background, disable to block Blender while exporting. This option is deprecated; EXECUTE this operator to run in the foreground, and INVOKE it to run as a background job

Append from a Library .blend file

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

filename (string, (optional, never None)) – File Name, Name of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

link (boolean, (optional)) – Link, Link the objects or data-blocks rather than appending

do_reuse_local_id (boolean, (optional)) – Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy

clear_asset_data (boolean, (optional)) – Clear Asset Data, Don’t add asset meta-data or tags from the original data-block

autoselect (boolean, (optional)) – Select, Select new objects

active_collection (boolean, (optional)) – Active Collection, Put new objects on the active collection

instance_collections (boolean, (optional)) – Instance Collections, Create instances for collections, rather than adding them directly to the scene

instance_object_data (boolean, (optional)) – Instance Object Data, Create instances for object data which are not referenced by any objects

set_fake (boolean, (optional)) – Fake User, Set “Fake User” for appended items (except objects and collections)

use_recursive (boolean, (optional)) – Localize All, Localize all appended data, including those indirectly linked from other libraries

Rename multiple items at once

data_type (enum in ['OBJECT', 'COLLECTION', 'MATERIAL', 'MESH', 'CURVE', 'META', 'VOLUME', 'GREASEPENCIL', 'ARMATURE', 'LATTICE', 'LIGHT', 'LIGHT_PROBE', 'CAMERA', 'SPEAKER', 'BONE', 'NODE', 'SEQUENCE_STRIP', 'ACTION_CLIP', 'SCENE', 'BRUSH'], (optional)) – Type, Type of data to rename

data_source (enum in ['SELECT', 'ALL'], (optional)) – Source

actions (bpy_prop_collection of BatchRenameAction, (optional)) – actions

startup/bl_operators/wm.py:3280

Check and fix all strings in current .blend file to be valid UTF-8 Unicode (needed for some old, 2.4x area files)

startup/bl_operators/file.py:289

Open a predefined asset shelf in a popup

name (string, (optional, never None)) – Asset Shelf Name, Identifier of the asset shelf to display

Open a predefined menu

name (string, (optional, never None)) – Name, Name of the menu

Open a predefined pie menu

name (string, (optional, never None)) – Name, Name of the pie menu

Open a predefined panel

name (string, (optional, never None)) – Name, Name of the menu

keep_open (boolean, (optional)) – Keep Open

Clear the recent files list

remove (enum in ['ALL', 'MISSING'], (optional)) – Remove

Invoke all configured exporters for all collections

Set boolean values for a collection of items

data_path_iter (string, (optional, never None)) – data_path_iter, The data path relative to the context, must point to an iterable

data_path_item (string, (optional, never None)) – data_path_item, The data path from each iterable to the value (int or float)

type (enum in ['TOGGLE', 'ENABLE', 'DISABLE'], (optional)) – Type

startup/bl_operators/wm.py:875

Set a context array value (useful for cycling the active mesh edit mode)

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

reverse (boolean, (optional)) – Reverse, Cycle backwards

startup/bl_operators/wm.py:673

Toggle a context value

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

reverse (boolean, (optional)) – Reverse, Cycle backwards

wrap (boolean, (optional)) – Wrap, Wrap back to the first/last values

startup/bl_operators/wm.py:624

Set a context value (useful for cycling active material, shape keys, groups, etc.)

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

reverse (boolean, (optional)) – Reverse, Cycle backwards

wrap (boolean, (optional)) – Wrap, Wrap back to the first/last values

startup/bl_operators/wm.py:584

Undocumented, consider contributing.

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

startup/bl_operators/wm.py:703

Adjust arbitrary values with mouse input

data_path_iter (string, (optional, never None)) – data_path_iter, The data path relative to the context, must point to an iterable

data_path_item (string, (optional, never None)) – data_path_item, The data path from each iterable to the value (int or float)

header_text (string, (optional, never None)) – Header Text, Text to display in header during scale

input_scale (float in [-inf, inf], (optional)) – input_scale, Scale the mouse movement by this value before applying the delta

invert (boolean, (optional)) – invert, Invert the mouse input

initial_x (int in [-inf, inf], (optional)) – initial_x

startup/bl_operators/wm.py:1014

Undocumented, consider contributing.

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

startup/bl_operators/wm.py:735

Scale a float context value

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (float in [-inf, inf], (optional)) – Value, Assign value

startup/bl_operators/wm.py:338

Scale an int context value

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (float in [-inf, inf], (optional)) – Value, Assign value

always_step (boolean, (optional)) – Always Step, Always adjust the value by a minimum of 1 when ‘value’ is not 1.0

startup/bl_operators/wm.py:376

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (boolean, (optional)) – Value, Assignment value

startup/bl_operators/wm.py:267

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (string, (optional, never None)) – Value, Assignment value (as a string)

startup/bl_operators/wm.py:267

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (float in [-inf, inf], (optional)) – Value, Assignment value

relative (boolean, (optional)) – Relative, Apply relative to the current value (delta)

startup/bl_operators/wm.py:267

Set a context value to an ID data-block

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (string, (optional, never None)) – Value, Assign value

startup/bl_operators/wm.py:817

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (int in [-inf, inf], (optional)) – Value, Assign value

relative (boolean, (optional)) – Relative, Apply relative to the current value (delta)

startup/bl_operators/wm.py:267

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (string, (optional, never None)) – Value, Assign value

startup/bl_operators/wm.py:267

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value (string, (optional, never None)) – Value, Assignment value (as a string)

startup/bl_operators/wm.py:480

Toggle a context value

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

module (string, (optional, never None)) – Module, Optionally override the context with a module

startup/bl_operators/wm.py:504

Toggle a context value

data_path (string, (optional, never None)) – Context Attributes, Context data-path (expanded using visible windows in the current .blend file)

value_1 (string, (optional, never None)) – Value, Toggle enum

value_2 (string, (optional, never None)) – Value, Toggle enum

startup/bl_operators/wm.py:545

Open a popup to set the debug level

debug_value (int in [-32768, 32767], (optional)) – Debug Value

Open online reference docs in a web browser

doc_id (string, (optional, never None)) – Doc ID

startup/bl_operators/wm.py:1361

doc_id (string, (optional, never None)) – Doc ID

startup/bl_operators/wm.py:1334

View a context based online manual in a web browser

Undocumented, consider contributing.

filepath (string, (optional, never None)) – filepath

startup/bl_operators/wm.py:3655

Operator that allows file handlers to receive file drops

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

Import FBX file into current scene

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

global_scale (float in [1e-06, 1e+06], (optional)) – Scale

mtl_name_collision_mode (enum in ['MAKE_UNIQUE', 'REFERENCE_EXISTING'], (optional)) – Material Name Collision, Behavior when the name of an imported material conflicts with an existing material MAKE_UNIQUE Make Unique – Import each FBX material as a unique Blender material. REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

Material Name Collision, Behavior when the name of an imported material conflicts with an existing material

MAKE_UNIQUE Make Unique – Import each FBX material as a unique Blender material.

REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

import_colors (enum in ['NONE', 'SRGB', 'LINEAR'], (optional)) – Vertex Colors, Import vertex color attributes NONE None – Do not import color attributes. SRGB sRGB – Vertex colors in the file are in sRGB color space. LINEAR Linear – Vertex colors in the file are in linear color space.

Vertex Colors, Import vertex color attributes

NONE None – Do not import color attributes.

SRGB sRGB – Vertex colors in the file are in sRGB color space.

LINEAR Linear – Vertex colors in the file are in linear color space.

use_custom_normals (boolean, (optional)) – Custom Normals, Import custom normals, if available (otherwise Blender will compute them)

use_custom_props (boolean, (optional)) – Custom Properties, Import user properties as custom properties

use_custom_props_enum_as_string (boolean, (optional)) – Enums As Strings, Store custom property enumeration values as strings

import_subdivision (boolean, (optional)) – Subdivision Data, Import FBX subdivision information as subdivision surface modifiers

ignore_leaf_bones (boolean, (optional)) – Ignore Leaf Bones, Ignore the last bone at the end of each chain (used to mark the length of the previous bone)

validate_meshes (boolean, (optional)) – Validate Meshes, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing)

use_anim (boolean, (optional)) – Import Animation, Import FBX animation

anim_offset (float in [-1e+06, 1e+06], (optional)) – Offset, Offset to apply to animation timestamps, in frames

filter_glob (string, (optional, never None)) – Extension Filter

Export Grease Pencil to PDF

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_fill (boolean, (optional)) – Fill, Export strokes with fill enabled

selected_object_type (enum in ['ACTIVE', 'SELECTED', 'VISIBLE'], (optional)) – Object, Which objects to include in the export ACTIVE Active – Include only the active object. SELECTED Selected – Include selected objects. VISIBLE Visible – Include all visible objects.

Object, Which objects to include in the export

ACTIVE Active – Include only the active object.

SELECTED Selected – Include selected objects.

VISIBLE Visible – Include all visible objects.

frame_mode (enum in ['ACTIVE', 'SELECTED', 'SCENE'], (optional)) – Frames, Which frames to include in the export ACTIVE Active – Include only active frame. SELECTED Selected – Include selected frames. SCENE Scene – Include all scene frames.

Frames, Which frames to include in the export

ACTIVE Active – Include only active frame.

SELECTED Selected – Include selected frames.

SCENE Scene – Include all scene frames.

stroke_sample (float in [0, 100], (optional)) – Sampling, Precision of stroke sampling. Low values mean a more precise result, and zero disables sampling

use_uniform_width (boolean, (optional)) – Uniform Width, Export strokes with uniform width

Export Grease Pencil to SVG

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_fill (boolean, (optional)) – Fill, Export strokes with fill enabled

selected_object_type (enum in ['ACTIVE', 'SELECTED', 'VISIBLE'], (optional)) – Object, Which objects to include in the export ACTIVE Active – Include only the active object. SELECTED Selected – Include selected objects. VISIBLE Visible – Include all visible objects.

Object, Which objects to include in the export

ACTIVE Active – Include only the active object.

SELECTED Selected – Include selected objects.

VISIBLE Visible – Include all visible objects.

frame_mode (enum in ['ACTIVE', 'SELECTED', 'SCENE'], (optional)) – Frames, Which frames to include in the export ACTIVE Active – Include only active frame. SELECTED Selected – Include selected frames. SCENE Scene – Include all scene frames.

Frames, Which frames to include in the export

ACTIVE Active – Include only active frame.

SELECTED Selected – Include selected frames.

SCENE Scene – Include all scene frames.

stroke_sample (float in [0, 100], (optional)) – Sampling, Precision of stroke sampling. Low values mean a more precise result, and zero disables sampling

use_uniform_width (boolean, (optional)) – Uniform Width, Export strokes with uniform width

use_clip_camera (boolean, (optional)) – Clip Camera, Clip drawings to camera size when exporting in camera view

Import SVG into Grease Pencil

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

resolution (int in [1, 100000], (optional)) – Resolution, Resolution of the generated strokes

scale (float in [1e-06, 1e+06], (optional)) – Scale, Scale of the final strokes

use_scene_unit (boolean, (optional)) – Scene Unit, Apply current scene’s unit (as defined by unit scale) to imported data

Relocate a linked ID, i.e. select another ID to link, and remap its local usages to that newly linked data-block). Currently only designed as an internal operator, not directly exposed to the user

id_session_uid (int in [0, inf], (optional)) – Linked ID Session UID, Unique runtime identifier for the linked ID to relocate

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

filename (string, (optional, never None)) – File Name, Name of the file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

link (boolean, (optional)) – Link, Link the objects or data-blocks rather than appending

do_reuse_local_id (boolean, (optional)) – Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy

clear_asset_data (boolean, (optional)) – Clear Asset Data, Don’t add asset meta-data or tags from the original data-block

autoselect (boolean, (optional)) – Select, Select new objects

active_collection (boolean, (optional)) – Active Collection, Put new objects on the active collection

instance_collections (boolean, (optional)) – Instance Collections, Create instances for collections, rather than adding them directly to the scene

instance_object_data (boolean, (optional)) – Instance Object Data, Create instances for object data which are not referenced by any objects

Add a custom theme to the preset list

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Remove a custom theme from the preset list

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Save a custom theme in the preset list

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:711

Add a custom keymap configuration to the preset list

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Remove a custom keymap configuration from the preset list

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

startup/bl_operators/presets.py:119

Reload the given library

library (string, (optional, never None)) – Library, Library to reload

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

filename (string, (optional, never None)) – File Name, Name of the file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Relocate the given library to one or several others

library (string, (optional, never None)) – Library, Library to relocate

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

filename (string, (optional, never None)) – File Name, Name of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

Link from a Library .blend file

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

filename (string, (optional, never None)) – File Name, Name of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

link (boolean, (optional)) – Link, Link the objects or data-blocks rather than appending

do_reuse_local_id (boolean, (optional)) – Re-Use Local Data, Try to re-use previously matching appended data-blocks instead of appending a new copy

clear_asset_data (boolean, (optional)) – Clear Asset Data, Don’t add asset meta-data or tags from the original data-block

autoselect (boolean, (optional)) – Select, Select new objects

active_collection (boolean, (optional)) – Active Collection, Put new objects on the active collection

instance_collections (boolean, (optional)) – Instance Collections, Create instances for collections, rather than adding them directly to the scene

instance_object_data (boolean, (optional)) – Instance Object Data, Create instances for object data which are not referenced by any objects

Print memory statistics to the console

Save the scene to a Wavefront OBJ file

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

export_animation (boolean, (optional)) – Export Animation, Export multiple frames instead of the current frame only

start_frame (int in [-inf, inf], (optional)) – Start Frame, The first frame to be exported

end_frame (int in [-inf, inf], (optional)) – End Frame, The last frame to be exported

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

global_scale (float in [0.0001, 10000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

apply_modifiers (boolean, (optional)) – Apply Modifiers, Apply modifiers to exported meshes

apply_transform (boolean, (optional)) – Apply Transform, Apply object transforms to exported vertices

export_eval_mode (enum in ['DAG_EVAL_RENDER', 'DAG_EVAL_VIEWPORT'], (optional)) – Object Properties, Determines properties like object visibility, modifiers etc., where they differ for Render and Viewport DAG_EVAL_RENDER Render – Export objects as they appear in render. DAG_EVAL_VIEWPORT Viewport – Export objects as they appear in the viewport.

Object Properties, Determines properties like object visibility, modifiers etc., where they differ for Render and Viewport

DAG_EVAL_RENDER Render – Export objects as they appear in render.

DAG_EVAL_VIEWPORT Viewport – Export objects as they appear in the viewport.

export_selected_objects (boolean, (optional)) – Export Selected Objects, Export only selected objects instead of all supported objects

export_uv (boolean, (optional)) – Export UVs

export_normals (boolean, (optional)) – Export Normals, Export per-face normals if the face is flat-shaded, per-face-corner normals if smooth-shaded

export_colors (boolean, (optional)) – Export Colors, Export per-vertex colors

export_materials (boolean, (optional)) – Export Materials, Export MTL library. There must be a Principled-BSDF node for image textures to be exported to the MTL file

export_pbr_extensions (boolean, (optional)) – Export Materials with PBR Extensions, Export MTL library using PBR extensions (roughness, metallic, sheen, coat, anisotropy, transmission)

path_mode (enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'MATCH', 'STRIP', 'COPY'], (optional)) – Path Mode, Method used to reference paths AUTO Auto – Use relative paths with subdirectories only. ABSOLUTE Absolute – Always write absolute paths. RELATIVE Relative – Write relative paths where possible. MATCH Match – Match absolute/relative setting with input path. STRIP Strip – Write filename only. COPY Copy – Copy the file to the destination path.

Path Mode, Method used to reference paths

AUTO Auto – Use relative paths with subdirectories only.

ABSOLUTE Absolute – Always write absolute paths.

RELATIVE Relative – Write relative paths where possible.

MATCH Match – Match absolute/relative setting with input path.

STRIP Strip – Write filename only.

COPY Copy – Copy the file to the destination path.

export_triangulated_mesh (boolean, (optional)) – Export Triangulated Mesh, All ngons with four or more vertices will be triangulated. Meshes in the scene will not be affected. Behaves like Triangulate Modifier with ngon-method: “Beauty”, quad-method: “Shortest Diagonal”, min vertices: 4

export_curves_as_nurbs (boolean, (optional)) – Export Curves as NURBS, Export curves in parametric form instead of exporting as mesh

export_object_groups (boolean, (optional)) – Export Object Groups, Append mesh name to object name, separated by a ‘_’

export_material_groups (boolean, (optional)) – Export Material Groups, Generate an OBJ group for each part of a geometry using a different material

export_vertex_groups (boolean, (optional)) – Export Vertex Groups, Export the name of the vertex group of a face. It is approximated by choosing the vertex group with the most members among the vertices of a face

export_smooth_groups (boolean, (optional)) – Export Smooth Groups, Generate smooth groups identifiers for each group of smooth faces, as unique integer values by default

smooth_group_bitflags (boolean, (optional)) – Bitflags Smooth Groups, If exporting smoothgroups, generate ‘bitflags’ values for the groups, instead of unique integer values. The same bitflag value can be re-used for different groups of smooth faces, as long as they have no common sharp edges or vertices

filter_glob (string, (optional, never None)) – Extension Filter

collection (string, (optional, never None)) – Collection

Load a Wavefront OBJ scene

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

global_scale (float in [0.0001, 10000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

clamp_size (float in [0, 1000], (optional)) – Clamp Bounding Box, Resize the objects to keep bounding box under this value. Value 0 disables clamping

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

use_split_objects (boolean, (optional)) – Split By Object, Import each OBJ ‘o’ as a separate object

use_split_groups (boolean, (optional)) – Split By Group, Import each OBJ ‘g’ as a separate object

import_vertex_groups (boolean, (optional)) – Vertex Groups, Import OBJ groups as vertex groups

validate_meshes (boolean, (optional)) – Validate Meshes, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing)

close_spline_loops (boolean, (optional)) – Detect Cyclic Curves, Join curve endpoints if overlapping control points are detected (if disabled, no curves will be cyclic)

collection_separator (string, (optional, never None)) – Path Separator, Character used to separate objects name into hierarchical structure

mtl_name_collision_mode (enum in ['MAKE_UNIQUE', 'REFERENCE_EXISTING'], (optional)) – Material Name Collision, How to handle naming collisions when importing materials MAKE_UNIQUE Make Unique – Create new materials with unique names for each OBJ file. REFERENCE_EXISTING Reference Existing – Use existing materials with same name instead of creating new ones.

Material Name Collision, How to handle naming collisions when importing materials

MAKE_UNIQUE Make Unique – Create new materials with unique names for each OBJ file.

REFERENCE_EXISTING Reference Existing – Use existing materials with same name instead of creating new ones.

filter_glob (string, (optional, never None)) – Extension Filter

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

load_ui (boolean, (optional)) – Load UI, Load user interface setup in the .blend file

use_scripts (boolean, (optional)) – Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences

display_file_selector (boolean, (optional)) – Display File Selector

state (int in [-inf, inf], (optional)) – State

List all the operators in a text-block, useful for scripting

startup/bl_operators/wm.py:2254

Set the active operator to its default values

Undocumented, consider contributing.

data_path (string, (optional, never None)) – Operator, Operator name (in Python as string)

prop_string (string, (optional, never None)) – Property, Property name (as a string)

startup/bl_operators/wm.py:777

Add or remove an Operator Preset

name (string, (optional, never None)) – Name, Name of the preset, used to make the path name

remove_name (boolean, (optional)) – remove_name

remove_active (boolean, (optional)) – remove_active

operator (string, (optional, never None)) – Operator

startup/bl_operators/presets.py:119

Remove outdated operator properties from presets that may cause problems

operator (string, (optional, never None)) – operator

properties (bpy_prop_collection of OperatorFileListElement, (optional)) – properties

startup/bl_operators/presets.py:924

Disable add-on for workspace

owner_id (string, (optional, never None)) – UI Tag

startup/bl_operators/wm.py:2302

Enable add-on for workspace

owner_id (string, (optional, never None)) – UI Tag

startup/bl_operators/wm.py:2287

Open a path in a file browser

filepath (string, (optional, never None)) – filepath

startup/bl_operators/wm.py:1167

Save the scene to a PLY file

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

global_scale (float in [0.0001, 10000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

apply_modifiers (boolean, (optional)) – Apply Modifiers, Apply modifiers to exported meshes

export_selected_objects (boolean, (optional)) – Export Selected Objects, Export only selected objects instead of all supported objects

collection (string, (optional, never None)) – Source Collection, Export only objects from this collection (and its children)

export_uv (boolean, (optional)) – Export UVs

export_normals (boolean, (optional)) – Export Vertex Normals, Export specific vertex normals if available, export calculated normals otherwise

export_colors (enum in ['NONE', 'SRGB', 'LINEAR'], (optional)) – Export Vertex Colors, Export vertex color attributes NONE None – Do not import/export color attributes. SRGB sRGB – Vertex colors in the file are in sRGB color space. LINEAR Linear – Vertex colors in the file are in linear color space.

Export Vertex Colors, Export vertex color attributes

NONE None – Do not import/export color attributes.

SRGB sRGB – Vertex colors in the file are in sRGB color space.

LINEAR Linear – Vertex colors in the file are in linear color space.

export_attributes (boolean, (optional)) – Export Vertex Attributes, Export custom vertex attributes

export_triangulated_mesh (boolean, (optional)) – Export Triangulated Mesh, All ngons with four or more vertices will be triangulated. Meshes in the scene will not be affected. Behaves like Triangulate Modifier with ngon-method: “Beauty”, quad-method: “Shortest Diagonal”, min vertices: 4

ascii_format (boolean, (optional)) – ASCII Format, Export file in ASCII format, export as binary otherwise

filter_glob (string, (optional, never None)) – Extension Filter

Import an PLY file as an object

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

global_scale (float in [1e-06, 1e+06], (optional)) – Scale

use_scene_unit (boolean, (optional)) – Scene Unit, Apply current scene’s unit (as defined by unit scale) to imported data

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

merge_verts (boolean, (optional)) – Merge Vertices, Merges vertices by distance

import_colors (enum in ['NONE', 'SRGB', 'LINEAR'], (optional)) – Vertex Colors, Import vertex color attributes NONE None – Do not import/export color attributes. SRGB sRGB – Vertex colors in the file are in sRGB color space. LINEAR Linear – Vertex colors in the file are in linear color space.

Vertex Colors, Import vertex color attributes

NONE None – Do not import/export color attributes.

SRGB sRGB – Vertex colors in the file are in sRGB color space.

LINEAR Linear – Vertex colors in the file are in linear color space.

import_attributes (boolean, (optional)) – Vertex Attributes, Import custom vertex attributes

filter_glob (string, (optional, never None)) – Extension Filter

Clear selected .blend file’s previews

files (bpy_prop_collection of OperatorFileListElement, (optional)) – files

directory (string, (optional, never None)) – directory

filter_blender (boolean, (optional)) – filter_blender

filter_folder (boolean, (optional)) – filter_folder

use_scenes (boolean, (optional)) – Scenes, Clear scenes’ previews

use_collections (boolean, (optional)) – Collections, Clear collections’ previews

use_objects (boolean, (optional)) – Objects, Clear objects’ previews

use_intern_data (boolean, (optional)) – Materials & Textures, Clear ‘internal’ previews (materials, textures, images, etc.)

use_trusted (boolean, (optional)) – Trusted Blend Files, Enable Python evaluation for selected files

use_backups (boolean, (optional)) – Save Backups, Keep a backup (.blend1) version of the files when saving with cleared previews

startup/bl_operators/file.py:204

Generate selected .blend file’s previews

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Collection of file paths with common directory root

directory (string, (optional, never None)) – Root path of all files listed in files collection

filter_blender (boolean, (optional)) – Show Blender files in the File Browser

filter_folder (boolean, (optional)) – Show folders in the File Browser

use_scenes (boolean, (optional)) – Scenes, Generate scenes’ previews

use_collections (boolean, (optional)) – Collections, Generate collections’ previews

use_objects (boolean, (optional)) – Objects, Generate objects’ previews

use_intern_data (boolean, (optional)) – Materials & Textures, Generate ‘internal’ previews (materials, textures, images, etc.)

use_trusted (boolean, (optional)) – Trusted Blend Files, Enable Python evaluation for selected files

use_backups (boolean, (optional)) – Save Backups, Keep a backup (.blend1) version of the files when saving with generated previews

startup/bl_operators/file.py:95

Clear data-block previews (only for some types like objects, materials, textures, etc.)

id_type (enum set in {'ALL', 'GEOMETRY', 'SHADING', 'SCENE', 'COLLECTION', 'OBJECT', 'MATERIAL', 'LIGHT', 'WORLD', 'TEXTURE', 'IMAGE'}, (optional)) – Data-Block Type, Which data-block previews to clear ALL All Types. GEOMETRY All Geometry Types – Clear previews for scenes, collections and objects. SHADING All Shading Types – Clear previews for materials, lights, worlds, textures and images. SCENE Scenes. COLLECTION Collections. OBJECT Objects. MATERIAL Materials. LIGHT Lights. WORLD Worlds. TEXTURE Textures. IMAGE Images.

Data-Block Type, Which data-block previews to clear

GEOMETRY All Geometry Types – Clear previews for scenes, collections and objects.

SHADING All Shading Types – Clear previews for materials, lights, worlds, textures and images.

COLLECTION Collections.

Ensure data-block previews are available and up-to-date (to be saved in .blend file, only for some types like materials, textures, etc.)

Add your own property to the data-block

data_path (string, (optional, never None)) – Property Edit, Property data_path edit

startup/bl_operators/wm.py:2136

Jump to a different tab inside the properties editor

context (string, (optional, never None)) – Context

startup/bl_operators/wm.py:2179

Change a custom property’s type, or adjust how it is displayed in the interface

data_path (string, (optional, never None)) – Property Edit, Property data_path edit

property_name (string, (optional, never None)) – Property Name, Property name edit

property_type (enum in ['FLOAT', 'FLOAT_ARRAY', 'INT', 'INT_ARRAY', 'BOOL', 'BOOL_ARRAY', 'STRING', 'DATA_BLOCK', 'PYTHON'], (optional)) – Type FLOAT Float – A single floating-point value. FLOAT_ARRAY Float Array – An array of floating-point values. INT Integer – A single integer. INT_ARRAY Integer Array – An array of integers. BOOL Boolean – A true or false value. BOOL_ARRAY Boolean Array – An array of true or false values. STRING String – A string value. DATA_BLOCK Data-Block – A data-block value. PYTHON Python – Edit a Python value directly, for unsupported property types.

FLOAT Float – A single floating-point value.

FLOAT_ARRAY Float Array – An array of floating-point values.

INT Integer – A single integer.

INT_ARRAY Integer Array – An array of integers.

BOOL Boolean – A true or false value.

BOOL_ARRAY Boolean Array – An array of true or false values.

STRING String – A string value.

DATA_BLOCK Data-Block – A data-block value.

PYTHON Python – Edit a Python value directly, for unsupported property types.

is_overridable_library (boolean, (optional)) – Library Overridable, Allow the property to be overridden when the data-block is linked

description (string, (optional, never None)) – Description

use_soft_limits (boolean, (optional)) – Soft Limits, Limits the Property Value slider to a range, values outside the range must be inputted numerically

array_length (int in [1, 32], (optional)) – Array Length

default_int (int array of 32 items in [-inf, inf], (optional)) – Default Value

min_int (int in [-inf, inf], (optional)) – Min

max_int (int in [-inf, inf], (optional)) – Max

soft_min_int (int in [-inf, inf], (optional)) – Soft Min

soft_max_int (int in [-inf, inf], (optional)) – Soft Max

step_int (int in [1, inf], (optional)) – Step

default_bool (boolean array of 32 items, (optional)) – Default Value

default_float (float array of 32 items in [-inf, inf], (optional)) – Default Value

min_float (float in [-inf, inf], (optional)) – Min

max_float (float in [-inf, inf], (optional)) – Max

soft_min_float (float in [-inf, inf], (optional)) – Soft Min

soft_max_float (float in [-inf, inf], (optional)) – Soft Max

precision (int in [0, 8], (optional)) – Precision

step_float (float in [0.001, inf], (optional)) – Step

subtype (enum in [], (optional)) – Subtype

default_string (string, (optional, never None)) – Default Value

id_type (enum in ['ACTION', 'ARMATURE', 'BRUSH', 'CACHEFILE', 'CAMERA', 'COLLECTION', 'CURVE', 'CURVES', 'FONT', 'GREASEPENCIL', 'GREASEPENCIL_V3', 'IMAGE', 'KEY', 'LATTICE', 'LIBRARY', 'LIGHT', 'LIGHT_PROBE', 'LINESTYLE', 'MASK', 'MATERIAL', 'MESH', 'META', 'MOVIECLIP', 'NODETREE', 'OBJECT', 'PAINTCURVE', 'PALETTE', 'PARTICLE', 'POINTCLOUD', 'SCENE', 'SCREEN', 'SOUND', 'SPEAKER', 'TEXT', 'TEXTURE', 'VOLUME', 'WINDOWMANAGER', 'WORKSPACE', 'WORLD'], (optional)) – ID Type

eval_string (string, (optional, never None)) – Value, Python value for unsupported custom property types

startup/bl_operators/wm.py:1869

Edit the value of a custom property

data_path (string, (optional, never None)) – Property Edit, Property data_path edit

property_name (string, (optional, never None)) – Property Name, Property name edit

eval_string (string, (optional, never None)) – Value, Value for custom property types that can only be edited as a Python expression

startup/bl_operators/wm.py:2093

Internal use (edit a property data_path)

data_path (string, (optional, never None)) – Property Edit, Property data_path edit

property_name (string, (optional, never None)) – Property Name, Property name edit

startup/bl_operators/wm.py:2193

Set some size property (e.g. brush size) with mouse wheel

data_path_primary (string, (optional, never None)) – Primary Data Path, Primary path of property to be set by the radial control

data_path_secondary (string, (optional, never None)) – Secondary Data Path, Secondary path of property to be set by the radial control

use_secondary (string, (optional, never None)) – Use Secondary, Path of property to select between the primary and secondary data paths

rotation_path (string, (optional, never None)) – Rotation Path, Path of property used to rotate the texture display

color_path (string, (optional, never None)) – Color Path, Path of property used to set the color of the control

fill_color_path (string, (optional, never None)) – Fill Color Path, Path of property used to set the fill color of the control

fill_color_override_path (string, (optional, never None)) – Fill Color Override Path

fill_color_override_test_path (string, (optional, never None)) – Fill Color Override Test

zoom_path (string, (optional, never None)) – Zoom Path, Path of property used to set the zoom level for the control

image_id (string, (optional, never None)) – Image ID, Path of ID that is used to generate an image for the control

secondary_tex (boolean, (optional)) – Secondary Texture, Tweak brush secondary/mask texture

release_confirm (boolean, (optional)) – Confirm On Release, Finish operation on key release

Load factory default startup file and preferences. To make changes permanent, use “Save Startup File” and “Save Preferences”

use_factory_startup_app_template_only (boolean, (optional)) – Factory Startup App-Template Only

use_empty (boolean, (optional)) – Empty, After loading, remove everything except scenes, windows, and workspaces. This makes it possible to load the startup file with its scene configuration and window layout intact, but no objects, materials, animations, …

Load factory default preferences. To make changes to preferences permanent, use “Save Preferences”

use_factory_startup_app_template_only (boolean, (optional)) – Factory Startup App-Template Only

Reloads history and bookmarks

Open the default file

filepath (string, (optional, never None)) – File Path, Path to an alternative start-up file

load_ui (boolean, (optional)) – Load UI, Load user interface setup from the .blend file

use_splash (boolean, (optional)) – Splash

use_factory_startup (boolean, (optional)) – Factory Startup, Load the default (‘factory startup’) blend file. This is independent of the normal start-up file that the user can save

use_factory_startup_app_template_only (boolean, (optional)) – Factory Startup App-Template Only

use_empty (boolean, (optional)) – Empty, After loading, remove everything except scenes, windows, and workspaces. This makes it possible to load the startup file with its scene configuration and window layout intact, but no objects, materials, animations, …

Load last saved preferences

Open an automatically saved file to recover it

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

use_scripts (boolean, (optional)) – Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences

Open the last closed file (“quit.blend”)

use_scripts (boolean, (optional)) – Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences

Simple redraw timer to test the speed of updating the interface

type (enum in ['DRAW', 'DRAW_SWAP', 'DRAW_WIN', 'DRAW_WIN_SWAP', 'ANIM_STEP', 'ANIM_PLAY', 'UNDO'], (optional)) – Type DRAW Draw Region – Draw region. DRAW_SWAP Draw Region & Swap – Draw region and swap. DRAW_WIN Draw Window – Draw window. DRAW_WIN_SWAP Draw Window & Swap – Draw window and swap. ANIM_STEP Animation Step – Animation steps. ANIM_PLAY Animation Play – Animation playback. UNDO Undo/Redo – Undo and redo.

DRAW Draw Region – Draw region.

DRAW_SWAP Draw Region & Swap – Draw region and swap.

DRAW_WIN Draw Window – Draw window.

DRAW_WIN_SWAP Draw Window & Swap – Draw window and swap.

ANIM_STEP Animation Step – Animation steps.

ANIM_PLAY Animation Play – Animation playback.

UNDO Undo/Redo – Undo and redo.

iterations (int in [1, inf], (optional)) – Iterations, Number of times to redraw

time_limit (float in [0, inf], (optional)) – Time Limit, Seconds to run the test for (override iterations)

Reload the saved file

use_scripts (boolean, (optional)) – Trusted Source, Allow .blend file to execute scripts automatically, default available from system preferences

Save the current file in the desired location

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

compress (boolean, (optional)) – Compress, Write compressed .blend file

relative_remap (boolean, (optional)) – Remap Relative, Remap relative paths when saving to a different directory

copy (boolean, (optional)) – Save Copy, Save a copy of the actual working state but does not make saved file active

Make the current file the default startup file

Save the current Blender file

filepath (string, (optional, never None)) – File Path, Path to file

hide_props_region (boolean, (optional)) – Hide Operator Properties, Collapse the region displaying the operator settings

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

compress (boolean, (optional)) – Compress, Write compressed .blend file

relative_remap (boolean, (optional)) – Remap Relative, Remap relative paths when saving to a different directory

exit (boolean, (optional)) – Exit, Exit Blender after saving

incremental (boolean, (optional)) – Incremental, Save the current Blender file with a numerically incremented name that does not overwrite any existing files

Make the current preferences default

Pop-up a search over all menus in the current context

Pop-up a search over all available operators in current context

Pop-up a search for a menu in current context

menu_idname (string, (optional, never None)) – Menu Name, Menu to search in

initial_query (string, (optional, never None)) – Initial Query, Query to insert into the search box

Toggle 3D stereo support for current window (or change the display mode)

display_mode (enum in Stereo3D Display Items, (optional)) – Display Mode

anaglyph_type (enum in Stereo3D Anaglyph Type Items, (optional)) – Anaglyph Type

interlace_type (enum in Stereo3D Interlace Type Items, (optional)) – Interlace Type

use_interlace_swap (boolean, (optional)) – Swap Left/Right, Swap left and right stereo channels

use_sidebyside_crosseyed (boolean, (optional)) – Cross-Eyed, Right eye should see left image and vice versa

Change the working color space of all colors in this blend file

convert_colors (boolean, (optional)) – Convert Colors in All Data-blocks, Change colors in all data-blocks to the new working space

working_space (enum in [], (optional)) – Working Space, Color space to set

Open the splash screen with release info

Open a window with information about Blender

Save the scene to an STL file

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

ascii_format (boolean, (optional)) – ASCII Format, Export file in ASCII format, export as binary otherwise

use_batch (boolean, (optional)) – Batch Export, Export each object to a separate file

export_selected_objects (boolean, (optional)) – Export Selected Objects, Export only selected objects instead of all supported objects

collection (string, (optional, never None)) – Source Collection, Export only objects from this collection (and its children)

global_scale (float in [1e-06, 1e+06], (optional)) – Scale

use_scene_unit (boolean, (optional)) – Scene Unit, Apply current scene’s unit (as defined by unit scale) to exported data

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

apply_modifiers (boolean, (optional)) – Apply Modifiers, Apply modifiers to exported meshes

filter_glob (string, (optional, never None)) – Extension Filter

Import an STL file as an object

filepath (string, (optional, never None)) – File Path, Path to file

directory (string, (optional, never None)) – Directory, Directory of the file

files (bpy_prop_collection of OperatorFileListElement, (optional)) – Files

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

global_scale (float in [1e-06, 1e+06], (optional)) – Scale

use_scene_unit (boolean, (optional)) – Scene Unit, Apply current scene’s unit (as defined by unit scale) to imported data

use_facet_normal (boolean, (optional)) – Facet Normals, Use (import) facet normals (note that this will still give flat shading)

forward_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

up_axis (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

use_mesh_validate (boolean, (optional)) – Validate Mesh, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing)

filter_glob (string, (optional, never None)) – Extension Filter

Generate system information, saved into a text file

filepath (string, (optional, never None)) – filepath

startup/bl_operators/wm.py:2222

Look up the most appropriate tool for the given brush type and activate that

brush_type (string, (optional, never None)) – Brush Type, Brush type identifier for which the most appropriate tool will be looked up

space_type (enum in ['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES'], (optional)) – Type

startup/bl_operators/wm.py:2436

Set the tool by name (for key-maps)

name (string, (optional, never None)) – Identifier, Identifier of the tool

cycle (boolean, (optional)) – Cycle, Cycle through tools in this group

as_fallback (boolean, (optional)) – Set Fallback, Set the fallback tool instead of the primary tool

space_type (enum in ['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES'], (optional)) – Type

startup/bl_operators/wm.py:2345

Set the tool by index (for key-maps)

index (int in [-inf, inf], (optional)) – Index in Toolbar

cycle (boolean, (optional)) – Cycle, Cycle through tools in this group

expand (boolean, (optional)) – expand, Include tool subgroups

as_fallback (boolean, (optional)) – Set Fallback, Set the fallback tool instead of the primary

space_type (enum in ['EMPTY', 'VIEW_3D', 'IMAGE_EDITOR', 'NODE_EDITOR', 'SEQUENCE_EDITOR', 'CLIP_EDITOR', 'DOPESHEET_EDITOR', 'GRAPH_EDITOR', 'NLA_EDITOR', 'TEXT_EDITOR', 'CONSOLE', 'INFO', 'TOPBAR', 'STATUSBAR', 'OUTLINER', 'PROPERTIES', 'FILE_BROWSER', 'SPREADSHEET', 'PREFERENCES'], (optional)) – Type

startup/bl_operators/wm.py:2395

Undocumented, consider contributing.

startup/bl_operators/wm.py:2503

Undocumented, consider contributing.

startup/bl_operators/wm.py:2527

Leader key like functionality for accessing tools

startup/bl_operators/wm.py:2627

Open a website in the web browser

url (string, (optional, never None)) – URL, URL to open

startup/bl_operators/wm.py:1074

Open a preset website in the web browser

type (enum in [], (optional)) – Site

startup/bl_operators/wm.py:1144

Export current scene in a USD archive

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

selected_objects_only (boolean, (optional)) – Selection Only, Only export selected objects. Unselected parents of selected objects are exported as empty transform

collection (string, (optional, never None)) – Collection

export_animation (boolean, (optional)) – Animation, Export all frames in the render frame range, rather than only the current frame

export_hair (boolean, (optional)) – Hair, Export hair particle systems as USD curves

export_uvmaps (boolean, (optional)) – UV Maps, Include all mesh UV maps in the export

rename_uvmaps (boolean, (optional)) – Rename UV Maps, Rename active render UV map to “st” to match USD conventions

export_mesh_colors (boolean, (optional)) – Color Attributes, Include mesh color attributes in the export

export_normals (boolean, (optional)) – Normals, Include normals of exported meshes in the export

export_materials (boolean, (optional)) – Materials, Export viewport settings of materials as USD preview materials, and export material assignments as geometry subsets

export_subdivision (enum in ['IGNORE', 'TESSELLATE', 'BEST_MATCH'], (optional)) – Subdivision, Choose how subdivision modifiers will be mapped to the USD subdivision scheme during export IGNORE Ignore – Scheme = None. Export base mesh without subdivision. TESSELLATE Tessellate – Scheme = None. Export subdivided mesh. BEST_MATCH Best Match – Scheme = Catmull-Clark, when possible. Reverts to exporting the subdivided mesh for the Simple subdivision type.

Subdivision, Choose how subdivision modifiers will be mapped to the USD subdivision scheme during export

IGNORE Ignore – Scheme = None. Export base mesh without subdivision.

TESSELLATE Tessellate – Scheme = None. Export subdivided mesh.

BEST_MATCH Best Match – Scheme = Catmull-Clark, when possible. Reverts to exporting the subdivided mesh for the Simple subdivision type.

export_armatures (boolean, (optional)) – Armatures, Export armatures and meshes with armature modifiers as USD skeletons and skinned meshes

only_deform_bones (boolean, (optional)) – Only Deform Bones, Only export deform bones and their parents

export_shapekeys (boolean, (optional)) – Shape Keys, Export shape keys as USD blend shapes

use_instancing (boolean, (optional)) – Instancing, Export instanced objects as references in USD rather than real objects

evaluation_mode (enum in ['RENDER', 'VIEWPORT'], (optional)) – Use Settings for, Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering RENDER Render – Use Render settings for object visibility, modifier settings, etc. VIEWPORT Viewport – Use Viewport settings for object visibility, modifier settings, etc.

Use Settings for, Determines visibility of objects, modifier settings, and other areas where there are different settings for viewport and rendering

RENDER Render – Use Render settings for object visibility, modifier settings, etc.

VIEWPORT Viewport – Use Viewport settings for object visibility, modifier settings, etc.

generate_preview_surface (boolean, (optional)) – USD Preview Surface Network, Generate an approximate USD Preview Surface shader representation of a Principled BSDF node network

generate_materialx_network (boolean, (optional)) – MaterialX Network, Generate a MaterialX network representation of the materials

convert_orientation (boolean, (optional)) – Convert Orientation, Convert orientation axis to a different convention to match other applications

export_global_forward_selection (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Forward Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

export_global_up_selection (enum in ['X', 'Y', 'Z', 'NEGATIVE_X', 'NEGATIVE_Y', 'NEGATIVE_Z'], (optional)) – Up Axis X X – Positive X axis. Y Y – Positive Y axis. Z Z – Positive Z axis. NEGATIVE_X -X – Negative X axis. NEGATIVE_Y -Y – Negative Y axis. NEGATIVE_Z -Z – Negative Z axis.

X X – Positive X axis.

Y Y – Positive Y axis.

Z Z – Positive Z axis.

NEGATIVE_X -X – Negative X axis.

NEGATIVE_Y -Y – Negative Y axis.

NEGATIVE_Z -Z – Negative Z axis.

export_textures_mode (enum in ['KEEP', 'PRESERVE', 'NEW'], (optional)) – Export Textures, Texture export method KEEP Keep – Use original location of textures. PRESERVE Preserve – Preserve file paths of textures from already imported USD files. Export remaining textures to a ‘textures’ folder next to the USD file. NEW New Path – Export textures to a ‘textures’ folder next to the USD file.

Export Textures, Texture export method

KEEP Keep – Use original location of textures.

PRESERVE Preserve – Preserve file paths of textures from already imported USD files. Export remaining textures to a ‘textures’ folder next to the USD file.

NEW New Path – Export textures to a ‘textures’ folder next to the USD file.

overwrite_textures (boolean, (optional)) – Overwrite Textures, Overwrite existing files when exporting textures

relative_paths (boolean, (optional)) – Relative Paths, Use relative paths to reference external files (i.e. textures, volumes) in USD, otherwise use absolute paths

xform_op_mode (enum in ['TRS', 'TOS', 'MAT'], (optional)) – Xform Ops, The type of transform operators to write TRS Translate, Rotate, Scale – Export with translate, rotate, and scale Xform operators. TOS Translate, Orient, Scale – Export with translate, orient quaternion, and scale Xform operators. MAT Matrix – Export matrix operator.

Xform Ops, The type of transform operators to write

TRS Translate, Rotate, Scale – Export with translate, rotate, and scale Xform operators.

TOS Translate, Orient, Scale – Export with translate, orient quaternion, and scale Xform operators.

MAT Matrix – Export matrix operator.

root_prim_path (string, (optional, never None)) – Root Prim, If set, add a transform primitive with the given path to the stage as the parent of all exported data

export_custom_properties (boolean, (optional)) – Custom Properties, Export custom properties as USD attributes

custom_properties_namespace (string, (optional, never None)) – Namespace, If set, add the given namespace as a prefix to exported custom property names. This only applies to property names that do not already have a prefix (e.g., it would apply to name ‘bar’ but not ‘foo:bar’) and does not apply to blender object and data names which are always exported in the ‘userProperties:blender’ namespace

author_blender_name (boolean, (optional)) – Blender Names, Author USD custom attributes containing the original Blender object and object data names

convert_world_material (boolean, (optional)) – World Dome Light, Convert the world material to a USD dome light. Currently works for simple materials, consisting of an environment texture connected to a background shader, with an optional vector multiply of the texture color

allow_unicode (boolean, (optional)) – Allow Unicode, Preserve UTF-8 encoded characters when writing USD prim and property names (requires software utilizing USD 24.03 or greater when opening the resulting files)

export_meshes (boolean, (optional)) – Meshes, Export all meshes

export_lights (boolean, (optional)) – Lights, Export all lights

export_cameras (boolean, (optional)) – Cameras, Export all cameras

export_curves (boolean, (optional)) – Curves, Export all curves

export_points (boolean, (optional)) – Point Clouds, Export all point clouds

export_volumes (boolean, (optional)) – Volumes, Export all volumes

triangulate_meshes (boolean, (optional)) – Triangulate Meshes, Triangulate meshes during export

quad_method (enum in Modifier Triangulate Quad Method Items, (optional)) – Quad Method, Method for splitting the quads into triangles

ngon_method (enum in Modifier Triangulate Ngon Method Items, (optional)) – N-gon Method, Method for splitting the n-gons into triangles

usdz_downscale_size (enum in ['KEEP', '256', '512', '1024', '2048', '4096', 'CUSTOM'], (optional)) – USDZ Texture Downsampling, Choose a maximum size for all exported textures KEEP Keep – Keep all current texture sizes. 256 256 – Resize to a maximum of 256 pixels. 512 512 – Resize to a maximum of 512 pixels. 1024 1024 – Resize to a maximum of 1024 pixels. 2048 2048 – Resize to a maximum of 2048 pixels. 4096 4096 – Resize to a maximum of 4096 pixels. CUSTOM Custom – Specify a custom size.

USDZ Texture Downsampling, Choose a maximum size for all exported textures

KEEP Keep – Keep all current texture sizes.

256 256 – Resize to a maximum of 256 pixels.

512 512 – Resize to a maximum of 512 pixels.

1024 1024 – Resize to a maximum of 1024 pixels.

2048 2048 – Resize to a maximum of 2048 pixels.

4096 4096 – Resize to a maximum of 4096 pixels.

CUSTOM Custom – Specify a custom size.

usdz_downscale_custom_size (int in [64, 16384], (optional)) – USDZ Custom Downscale Size, Custom size for downscaling exported textures

merge_parent_xform (boolean, (optional)) – Merge parent Xform, Merge USD primitives with their Xform parent if possible. USD does not allow nested UsdGeomGprims, intermediary Xform prims will be defined to keep the USD file valid when encountering object hierarchies.

convert_scene_units (enum in ['METERS', 'KILOMETERS', 'CENTIMETERS', 'MILLIMETERS', 'INCHES', 'FEET', 'YARDS', 'CUSTOM'], (optional)) – Units, Set the USD Stage meters per unit to the chosen measurement, or a custom value METERS Meters – Scene meters per unit to 1.0. KILOMETERS Kilometers – Scene meters per unit to 1000.0. CENTIMETERS Centimeters – Scene meters per unit to 0.01. MILLIMETERS Millimeters – Scene meters per unit to 0.001. INCHES Inches – Scene meters per unit to 0.0254. FEET Feet – Scene meters per unit to 0.3048. YARDS Yards – Scene meters per unit to 0.9144. CUSTOM Custom – Specify a custom scene meters per unit value.

Units, Set the USD Stage meters per unit to the chosen measurement, or a custom value

METERS Meters – Scene meters per unit to 1.0.

KILOMETERS Kilometers – Scene meters per unit to 1000.0.

CENTIMETERS Centimeters – Scene meters per unit to 0.01.

MILLIMETERS Millimeters – Scene meters per unit to 0.001.

INCHES Inches – Scene meters per unit to 0.0254.

FEET Feet – Scene meters per unit to 0.3048.

YARDS Yards – Scene meters per unit to 0.9144.

CUSTOM Custom – Specify a custom scene meters per unit value.

meters_per_unit (float in [0.0001, 1000], (optional)) – Meters Per Unit, Custom value for meters per unit in the USD Stage

Import USD stage into current scene

filepath (string, (optional, never None)) – File Path, Path to file

check_existing (boolean, (optional)) – Check Existing, Check and warn on overwriting existing files

filter_blender (boolean, (optional)) – Filter .blend files

filter_backup (boolean, (optional)) – Filter .blend files

filter_image (boolean, (optional)) – Filter image files

filter_movie (boolean, (optional)) – Filter movie files

filter_python (boolean, (optional)) – Filter Python files

filter_font (boolean, (optional)) – Filter font files

filter_sound (boolean, (optional)) – Filter sound files

filter_text (boolean, (optional)) – Filter text files

filter_archive (boolean, (optional)) – Filter archive files

filter_btx (boolean, (optional)) – Filter btx files

filter_alembic (boolean, (optional)) – Filter Alembic files

filter_usd (boolean, (optional)) – Filter USD files

filter_obj (boolean, (optional)) – Filter OBJ files

filter_volume (boolean, (optional)) – Filter OpenVDB volume files

filter_folder (boolean, (optional)) – Filter folders

filter_blenlib (boolean, (optional)) – Filter Blender IDs

filemode (int in [1, 9], (optional)) – File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file

relative_path (boolean, (optional)) – Relative Path, Select the file relative to the blend file

display_type (enum in ['DEFAULT', 'LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], (optional)) – Display Type DEFAULT Default – Automatically determine display type for files. LIST_VERTICAL Short List – Display files as short list. LIST_HORIZONTAL Long List – Display files as a detailed list. THUMBNAIL Thumbnails – Display files as thumbnails.

DEFAULT Default – Automatically determine display type for files.

LIST_VERTICAL Short List – Display files as short list.

LIST_HORIZONTAL Long List – Display files as a detailed list.

THUMBNAIL Thumbnails – Display files as thumbnails.

sort_method (enum in [], (optional)) – File sorting mode

scale (float in [0.0001, 1000], (optional)) – Scale, Value by which to enlarge or shrink the objects with respect to the world’s origin

set_frame_range (boolean, (optional)) – Set Frame Range, Update the scene’s start and end frame to match those of the USD archive

import_cameras (boolean, (optional)) – Cameras

import_curves (boolean, (optional)) – Curves

import_lights (boolean, (optional)) – Lights

import_materials (boolean, (optional)) – Materials

import_meshes (boolean, (optional)) – Meshes

import_volumes (boolean, (optional)) – Volumes

import_shapes (boolean, (optional)) – USD Shapes

import_skeletons (boolean, (optional)) – Armatures

import_blendshapes (boolean, (optional)) – Shape Keys

import_points (boolean, (optional)) – Point Clouds

import_subdivision (boolean, (optional)) – Import Subdivision Scheme, Create subdivision surface modifiers based on the USD SubdivisionScheme attribute

support_scene_instancing (boolean, (optional)) – Scene Instancing, Import USD scene graph instances as collection instances

import_visible_only (boolean, (optional)) – Visible Primitives Only, Do not import invisible USD primitives. Only applies to primitives with a non-animated visibility attribute. Primitives with animated visibility will always be imported

create_collection (boolean, (optional)) – Create Collection, Add all imported objects to a new collection

read_mesh_uvs (boolean, (optional)) – UV Coordinates, Read mesh UV coordinates

read_mesh_colors (boolean, (optional)) – Color Attributes, Read mesh color attributes

read_mesh_attributes (boolean, (optional)) – Mesh Attributes, Read USD Primvars as mesh attributes

prim_path_mask (string, (optional, never None)) – Path Mask, Import only the primitive at the given path and its descendants. Multiple paths may be specified in a list delimited by commas or semicolons

import_guide (boolean, (optional)) – Guide, Import guide geometry

import_proxy (boolean, (optional)) – Proxy, Import proxy geometry

import_render (boolean, (optional)) – Render, Import final render geometry

import_all_materials (boolean, (optional)) – Import All Materials, Also import materials that are not used by any geometry. Note that when this option is false, materials referenced by geometry will still be imported

import_usd_preview (boolean, (optional)) – Import USD Preview, Convert UsdPreviewSurface shaders to Principled BSDF shader networks

set_material_blend (boolean, (optional)) – Set Material Blend, If the Import USD Preview option is enabled, the material blend method will automatically be set based on the shader’s opacity and opacityThreshold inputs

light_intensity_scale (float in [0.0001, 10000], (optional)) – Light Intensity Scale, Scale for the intensity of imported lights

mtl_purpose (enum in ['MTL_ALL_PURPOSE', 'MTL_PREVIEW', 'MTL_FULL'], (optional)) – Material Purpose, Attempt to import materials with the given purpose. If no material with this purpose is bound to the primitive, fall back on loading any other bound material MTL_ALL_PURPOSE All Purpose – Attempt to import ‘allPurpose’ materials.. MTL_PREVIEW Preview – Attempt to import ‘preview’ materials. Load ‘allPurpose’ materials as a fallback. MTL_FULL Full – Attempt to import ‘full’ materials. Load ‘allPurpose’ or ‘preview’ materials, in that order, as a fallback.

Material Purpose, Attempt to import materials with the given purpose. If no material with this purpose is bound to the primitive, fall back on loading any other bound material

MTL_ALL_PURPOSE All Purpose – Attempt to import ‘allPurpose’ materials..

MTL_PREVIEW Preview – Attempt to import ‘preview’ materials. Load ‘allPurpose’ materials as a fallback.

MTL_FULL Full – Attempt to import ‘full’ materials. Load ‘allPurpose’ or ‘preview’ materials, in that order, as a fallback.

mtl_name_collision_mode (enum in ['MAKE_UNIQUE', 'REFERENCE_EXISTING'], (optional)) – Material Name Collision, Behavior when the name of an imported material conflicts with an existing material MAKE_UNIQUE Make Unique – Import each USD material as a unique Blender material. REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

Material Name Collision, Behavior when the name of an imported material conflicts with an existing material

MAKE_UNIQUE Make Unique – Import each USD material as a unique Blender material.

REFERENCE_EXISTING Reference Existing – If a material with the same name already exists, reference that instead of importing.

import_textures_mode (enum in ['IMPORT_NONE', 'IMPORT_PACK', 'IMPORT_COPY'], (optional)) – Import Textures, Behavior when importing textures from a USDZ archive IMPORT_NONE None – Don’t import textures. IMPORT_PACK Packed – Import textures as packed data. IMPORT_COPY Copy – Copy files to textures directory.

Import Textures, Behavior when importing textures from a USDZ archive

IMPORT_NONE None – Don’t import textures.

IMPORT_PACK Packed – Import textures as packed data.

IMPORT_COPY Copy – Copy files to textures directory.

import_textures_dir (string, (optional, never None)) – Textures Directory, Path to the directory where imported textures will be copied

tex_name_collision_mode (enum in ['USE_EXISTING', 'OVERWRITE'], (optional)) – File Name Collision, Behavior when the name of an imported texture file conflicts with an existing file USE_EXISTING Use Existing – If a file with the same name already exists, use that instead of copying. OVERWRITE Overwrite – Overwrite existing files.

File Name Collision, Behavior when the name of an imported texture file conflicts with an existing file

USE_EXISTING Use Existing – If a file with the same name already exists, use that instead of copying.

OVERWRITE Overwrite – Overwrite existing files.

property_import_mode (enum in ['NONE', 'USER', 'ALL'], (optional)) – Custom Properties, Behavior when importing USD attributes as Blender custom properties NONE None – Do not import USD custom attributes. USER User – Import USD attributes in the ‘userProperties’ namespace as Blender custom properties. The namespace will be stripped from the property names. ALL All Custom – Import all USD custom attributes as Blender custom properties. Namespaces will be retained in the property names.

Custom Properties, Behavior when importing USD attributes as Blender custom properties

NONE None – Do not import USD custom attributes.

USER User – Import USD attributes in the ‘userProperties’ namespace as Blender custom properties. The namespace will be stripped from the property names.

ALL All Custom – Import all USD custom attributes as Blender custom properties. Namespaces will be retained in the property names.

validate_meshes (boolean, (optional)) – Validate Meshes, Ensure the data is valid (when disabled, data may be imported which causes crashes displaying or editing)

create_world_material (boolean, (optional)) – World Dome Light, Convert the first discovered USD dome light to a world background shader

import_defined_only (boolean, (optional)) – Defined Primitives Only, Import only defined USD primitives. When disabled this allows importing USD primitives which are not defined, such as those with an override specifier

merge_parent_xform (boolean, (optional)) – Merge parent Xform, Allow USD primitives to merge with their Xform parent if they are the only child in the hierarchy

apply_unit_conversion_scale (boolean, (optional)) – Apply Unit Conversion Scale, Scale the scene objects by the USD stage’s meters per unit value. This scaling is applied in addition to the value specified in the Scale option

Close the current window

Toggle the current window full-screen

Create a new main window with its own workspace and scene selection

Move/turn relative to the VR viewer or controller

mode (enum in ['FORWARD', 'BACK', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'TURNLEFT', 'TURNRIGHT', 'VIEWER_FORWARD', 'VIEWER_BACK', 'VIEWER_LEFT', 'VIEWER_RIGHT', 'CONTROLLER_FORWARD'], (optional)) – Mode, Fly mode FORWARD Forward – Move along navigation forward axis. BACK Back – Move along navigation back axis. LEFT Left – Move along navigation left axis. RIGHT Right – Move along navigation right axis. UP Up – Move along navigation up axis. DOWN Down – Move along navigation down axis. TURNLEFT Turn Left – Turn counter-clockwise around navigation up axis. TURNRIGHT Turn Right – Turn clockwise around navigation up axis. VIEWER_FORWARD Viewer Forward – Move along viewer’s forward axis. VIEWER_BACK Viewer Back – Move along viewer’s back axis. VIEWER_LEFT Viewer Left – Move along viewer’s left axis. VIEWER_RIGHT Viewer Right – Move along viewer’s right axis. CONTROLLER_FORWARD Controller Forward – Move along controller’s forward axis.

FORWARD Forward – Move along navigation forward axis.

BACK Back – Move along navigation back axis.

LEFT Left – Move along navigation left axis.

RIGHT Right – Move along navigation right axis.

UP Up – Move along navigation up axis.

DOWN Down – Move along navigation down axis.

TURNLEFT Turn Left – Turn counter-clockwise around navigation up axis.

TURNRIGHT Turn Right – Turn clockwise around navigation up axis.

VIEWER_FORWARD Viewer Forward – Move along viewer’s forward axis.

VIEWER_BACK Viewer Back – Move along viewer’s back axis.

VIEWER_LEFT Viewer Left – Move along viewer’s left axis.

VIEWER_RIGHT Viewer Right – Move along viewer’s right axis.

CONTROLLER_FORWARD Controller Forward – Move along controller’s forward axis.

snap_turn_threshold (float in [0, 1], (optional)) – Snap Turn Threshold, Input state threshold when using snap turn

lock_location_z (boolean, (optional)) – Lock Elevation, Prevent changes to viewer elevation

lock_direction (boolean, (optional)) – Lock Direction, Limit movement to viewer’s initial direction

speed_frame_based (boolean, (optional)) – Frame Based Speed, Apply fixed movement deltas every update

turn_speed_factor (float in [0, 1], (optional)) – Turn Speed Factor, Ratio between the min and max turn speed

fly_speed_factor (float in [0, 1], (optional)) – Fly Speed Factor, Ratio between the min and max fly speed

speed_interpolation0 (mathutils.Vector of 2 items in [0, 1], (optional)) – Speed Interpolation 0, First cubic spline control point between min/max speeds

speed_interpolation1 (mathutils.Vector of 2 items in [0, 1], (optional)) – Speed Interpolation 1, Second cubic spline control point between min/max speeds

alt_mode (enum in ['FORWARD', 'BACK', 'LEFT', 'RIGHT', 'UP', 'DOWN', 'TURNLEFT', 'TURNRIGHT', 'VIEWER_FORWARD', 'VIEWER_BACK', 'VIEWER_LEFT', 'VIEWER_RIGHT', 'CONTROLLER_FORWARD'], (optional)) – Mode (Alt), Fly mode when hands are swapped FORWARD Forward – Move along navigation forward axis. BACK Back – Move along navigation back axis. LEFT Left – Move along navigation left axis. RIGHT Right – Move along navigation right axis. UP Up – Move along navigation up axis. DOWN Down – Move along navigation down axis. TURNLEFT Turn Left – Turn counter-clockwise around navigation up axis. TURNRIGHT Turn Right – Turn clockwise around navigation up axis. VIEWER_FORWARD Viewer Forward – Move along viewer’s forward axis. VIEWER_BACK Viewer Back – Move along viewer’s back axis. VIEWER_LEFT Viewer Left – Move along viewer’s left axis. VIEWER_RIGHT Viewer Right – Move along viewer’s right axis. CONTROLLER_FORWARD Controller Forward – Move along controller’s forward axis.

Mode (Alt), Fly mode when hands are swapped

FORWARD Forward – Move along navigation forward axis.

BACK Back – Move along navigation back axis.

LEFT Left – Move along navigation left axis.

RIGHT Right – Move along navigation right axis.

UP Up – Move along navigation up axis.

DOWN Down – Move along navigation down axis.

TURNLEFT Turn Left – Turn counter-clockwise around navigation up axis.

TURNRIGHT Turn Right – Turn clockwise around navigation up axis.

VIEWER_FORWARD Viewer Forward – Move along viewer’s forward axis.

VIEWER_BACK Viewer Back – Move along viewer’s back axis.

VIEWER_LEFT Viewer Left – Move along viewer’s left axis.

VIEWER_RIGHT Viewer Right – Move along viewer’s right axis.

CONTROLLER_FORWARD Controller Forward – Move along controller’s forward axis.

alt_lock_location_z (boolean, (optional)) – Lock Elevation (Alt), When hands are swapped, prevent changes to viewer elevation

alt_lock_direction (boolean, (optional)) – Lock Direction (Alt), When hands are swapped, limit movement to viewer’s initial direction

Navigate the VR scene by grabbing with controllers

lock_location (boolean, (optional)) – Lock Location, Prevent changes to viewer location

lock_location_z (boolean, (optional)) – Lock Elevation, Prevent changes to viewer elevation

lock_rotation (boolean, (optional)) – Lock Rotation, Prevent changes to viewer rotation

lock_rotation_z (boolean, (optional)) – Lock Up Orientation, Prevent changes to viewer up orientation

lock_scale (boolean, (optional)) – Lock Scale, Prevent changes to viewer scale

Reset VR navigation deltas relative to session base pose

location (boolean, (optional)) – Location, Reset location deltas

rotation (boolean, (optional)) – Rotation, Reset rotation deltas

scale (boolean, (optional)) – Scale, Reset scale deltas

Swap VR navigation controls between left / right controllers

Set VR viewer location to controller raycast hit location

teleport_axes (boolean array of 3 items, (optional)) – Teleport Axes, Enabled teleport axes in navigation space

interpolation (float in [0, 1], (optional)) – Interpolation, Interpolation factor between viewer and hit locations

offset (float in [0, inf], (optional)) – Offset, Offset along hit normal to subtract from final location

selectable_only (boolean, (optional)) – Selectable Only, Only allow selectable objects to influence raycast result

distance (float in [0, inf], (optional)) – Maximum raycast distance

gravity (float in [0, inf], (optional)) – Gravity, Downward curvature applied to raycast

raycast_scale (float in [0, inf], (optional)) – Raycast Scale, Width of the raycast visualization

destination_scale (float in [0, inf], (optional)) – Destination Scale, Width of the destination visualization

sample_count (int in [2, inf], (optional)) – Sample Count, Number of interpolation samples for the raycast visualization

from_viewer (boolean, (optional)) – From Viewer, Use viewer pose as raycast origin

axis (mathutils.Vector of 3 items in [-1, 1], (optional)) – Axis, Raycast axis in controller/viewer space

hit_color (float array of 4 items in [0, 1], (optional)) – Hit Color, Color of raycast when it succeeds

miss_color (float array of 4 items in [0, 1], (optional)) – Miss Color, Color of raycast when it misses

fallback_color (float array of 4 items in [0, 1], (optional)) – Fallback Color, Color of raycast when a fallback case succeeds

Open a view for use with virtual reality headsets, or close it if already opened

---
