# Blender5_Addons - Data Access

**Pages:** 4

---

## Internal Data & Their Python Objects¶

**URL:** https://docs.blender.org/api/current/info_gotchas_internal_data_and_python_objects.html

**Contents:**
- Internal Data & Their Python Objects¶
- Life-Time of Python Objects Wrapping Blender Data¶
- Data Names¶
  - Naming Limitations¶
  - Library Collisions¶
- Stale Data¶
  - No updates after setting values¶
  - No updates after changing UI context¶
- Can I redraw during script execution?¶

The Python objects wrapping Blender internal data have some limitations and constraints, compared to ‘pure Python’ data. The most common things to keep in mind are documented here.

Typically, Python objects representing (wrapping) Blender data have a limited life-time. They are created on-demand, and deleted as soon as they are not used in Python anymore.

This means that storing python-only data in these objects should not be done for anything that requires some form of persistence.

There are some exceptions to this rule. For example, IDs do store their Python instance, once created, and re-use it instead of re-creating a new Python object every time they are accessed from Python. And modal operators will keep their instance as long as the operator is running. However, this is done for performances purpose and is considered an internal implementation detail. Relying on this behavior from Python code side for any purpose is not recommended.

Further more, Blender may free its internal data, in which case it will try to invalidate a known Python object wrapping it. But this is not always possible, which can lead to invalid memory access and is another good reason to never store these in Python code in any persistent way. See also the troubleshooting crashes documentation.

A common mistake is to assume newly created data is given the requested name. This can cause bugs when you add data (normally imported) then reference it later by name:

Or with name assignment:

Data names may not match the assigned values if they exceed the maximum length, are already used or an empty string.

It’s better practice not to reference objects by names at all, once created you can store the data in a list, dictionary, on a class, etc; there is rarely a reason to have to keep searching for the same data by name.

If you do need to use name references, it’s best to use a dictionary to maintain a mapping between the names of the imported assets and the newly created data, this way you don’t run this risk of referencing existing data from the blend-file, or worse modifying it.

Blender keeps data names unique (bpy.types.ID.name) so you can’t name two objects, meshes, scenes, etc., the same by accident. However, when linking in library data from another blend-file naming collisions can occur, so it’s best to avoid referencing data by name at all.

This can be tricky at times and not even Blender handles this correctly in some cases (when selecting the modifier object for example, you can’t select between multiple objects with the same name), but it’s still good to try avoiding these problems in this area. If you need to select between local and library data, there is a feature in bpy.data members to allow for this.

Sometimes you want to modify values from Python and immediately access the updated values, e.g: Once changing the objects bpy.types.Object.location you may want to access its transformation right after from bpy.types.Object.matrix_world, but this doesn’t work as you might expect. There are similar issues with changes to the UI, that are covered in the next section.

Consider the calculations that might contribute to the object’s final transformation, this includes:

Animation function curves.

Drivers and their Python expressions.

Parent objects and all of their F-Curves, constraints, etc.

To avoid expensive recalculations every time a property is modified, Blender defers the evaluation until the results are needed. However, while the script runs you may want to access the updated values. In this case you need to call bpy.types.ViewLayer.update after modifying values, for example:

Now all dependent data (child objects, modifiers, drivers, etc.) have been recalculated and are available to the script within the active view layer.

Similar to the previous issue, some changes to the UI may also not have an immediate effect. For example, setting bpy.types.Window.workspace doesn’t seem to cause an observable effect in the immediately following code (bpy.types.Window.workspace is still the same), but the UI will in fact reflect the change. Some of the properties that behave that way are:

bpy.types.Window.workspace

bpy.types.Window.screen

bpy.types.Window.scene

bpy.types.Area.uitype

Such changes impact the UI, and with that the context (bpy.context) quite drastically. This can break Blender’s context management. So Blender delays this change until after operators have run and just before the UI is redrawn, making sure that context can be changed safely.

If you rely on executing code with an updated context this can be worked around by executing the code in a delayed fashion as well. Possible options include:

It’s also possible to depend on drawing callbacks although these should generally be avoided as failure to draw a hidden panel, region, cursor, etc. could cause your script to be unreliable

The official answer to this is no, or… “You don’t want to do that”. To give some background on the topic:

While a script executes, Blender waits for it to finish and is effectively locked until it’s done; while in this state Blender won’t redraw or respond to user input. Normally this is not such a problem because scripts distributed with Blender tend not to run for an extended period of time, nevertheless scripts can take a long time to complete and it would be nice to see progress in the viewport.

Tools that lock Blender in a loop redraw are highly discouraged since they conflict with Blender’s ability to run multiple operators at once and update different parts of the interface as the tool runs.

So the solution here is to write a modal operator, which is an operator that defines a modal() function, See the modal operator template in the text editor. Modal operators execute on user input or setup their own timers to run frequently, they can handle the events or pass through to be handled by the keymap or other modal operators. Examples of modal operators are Transform, Painting, Fly Navigation and File Select.

Writing modal operators takes more effort than a simple for loop that contains draw calls but is more flexible and integrates better with Blender’s design.

Ok, Ok! I still want to draw from Python

If you insist – yes it’s possible, but scripts that use this hack will not be considered for inclusion in Blender and any issue with using it will not be considered a bug, there is also no guaranteed compatibility in future releases.

**Examples:**

Example 1 (markdown):
```markdown
bpy.data.meshes.new(name=meshid)

# Normally some code, function calls, etc.
bpy.data.meshes[meshid]
```

Example 2 (markdown):
```markdown
obj.name = objname

# Normally some code, function calls, etc.
obj = bpy.data.meshes[objname]
```

Example 3 (markdown):
```markdown
# Typically declared in the main body of the function.
mesh_name_mapping = {}

mesh = bpy.data.meshes.new(name=meshid)
mesh_name_mapping[meshid] = mesh

# Normally some code, or function calls, etc.

# Use own dictionary rather than `bpy.data`.
mesh = mesh_name_mapping[meshid]
```

Example 4 (sql):
```sql
# Typical name lookup, could be local or library.
obj = bpy.data.objects["my_obj"]

# Library object name lookup using a pair,
# where the second argument is the library path matching bpy.types.Library.filepath.
obj = bpy.data.objects["my_obj", "//my_lib.blend"]

# Local object name look up using a pair,
# where the second argument excludes library data from being returned.
obj = bpy.data.objects["my_obj", None]

# Both the examples above also works for `get`.
obj = bpy.data.objects.get(("my_obj", None))
```

---

## Bones & Armatures¶

**URL:** https://docs.blender.org/api/current/info_gotchas_armatures_and_bones.html

**Contents:**
- Bones & Armatures¶
- Edit Bones, Pose Bones, Bone… Bones¶
  - Edit Bones¶
  - Bones (Object-Mode)¶
  - Pose Bones¶
- Armature Mode Switching¶

Armature Bones in Blender have three distinct data structures that contain them. If you are accessing the bones through one of them, you may not have access to the properties you really need.

In the following examples bpy.context.object is assumed to be an armature object.

bpy.context.object.data.edit_bones contains an edit bones; to access them you must set the armature mode to Edit-Mode first (edit bones do not exist in Object or Pose-Mode). Use these to create new bones, set their head/tail or roll, change their parenting relationships to other bones, etc.

Example using bpy.types.EditBone in armature Edit-Mode which is only possible in Edit-Mode:

This will be empty outside of Edit-Mode:

Returns an edit bone only in Edit-Mode:

bpy.context.object.data.bones contains bones. These live in Object-Mode, and have various properties you can change, note that the head and tail properties are read-only.

Example using bpy.types.Bone in Object or Pose-Mode returning a bone (not an edit bone) outside of Edit-Mode:

This works, as with Blender the setting can be edited in any mode:

Accessible but read-only:

bpy.context.object.pose.bones contains pose bones. This is where animation data resides, i.e. animatable transformations are applied to pose bones, as are constraints and IK-settings.

Examples using bpy.types.PoseBone in Object or Pose-Mode:

Notice the pose is accessed from the object rather than the object data, this is why Blender can have two or more objects sharing the same armature in different poses.

Strictly speaking pose bones are not bones, they are just the state of the armature, stored in the bpy.types.Object rather than the bpy.types.Armature, yet the real bones are accessible from the pose bones via bpy.types.PoseBone.bone.

While writing scripts that deal with armatures you may find you have to switch between modes, when doing so take care when switching out of Edit-Mode not to keep references to the edit bones or their head/tail vectors. Further access to these will crash Blender so it’s important that the script clearly separates sections of the code which operate in different modes.

This is mainly an issue with Edit-Mode since pose data can be manipulated without having to be in Pose-Mode, yet for operator access you may still need to enter Pose-Mode.

**Examples:**

Example 1 (unknown):
```unknown
>>> bpy.context.object.data.edit_bones["Bone"].head = Vector((1.0, 2.0, 3.0))
```

Example 2 (unknown):
```unknown
>>> mybones = bpy.context.selected_editable_bones
```

Example 3 (unknown):
```unknown
>>> bpy.context.active_bone
```

Example 4 (unknown):
```unknown
>>> bpy.context.active_bone
```

---

## Data Access (bpy.data)¶

**URL:** https://docs.blender.org/api/current/bpy.data.html

**Contents:**
- Data Access (bpy.data)¶

This module is used for all Blender/Python access.

Access to Blender’s internal data

**Examples:**

Example 1 (typescript):
```typescript
import bpy


# Print all objects.
for obj in bpy.data.objects:
    print(obj.name)


# Print all scene names in a list.
print(bpy.data.scenes.keys())


# Remove mesh Cube.
if "Cube" in bpy.data.meshes:
    mesh = bpy.data.meshes["Cube"]
    print("removing mesh", mesh)
    bpy.data.meshes.remove(mesh)


# Write images into a file next to the blend.
import os
with open(os.path.splitext(bpy.data.filepath)[0] + ".txt", 'w') as fs:
    for image in bpy.data.images:
        fs.write("{:s} {:d} x {:d}\n".format(image.filepath, image.size[0], image.size[1]))
```

---

## Message Bus (bpy.msgbus)¶

**URL:** https://docs.blender.org/api/current/bpy.msgbus.html

**Contents:**
- Message Bus (bpy.msgbus)¶
- Limitations¶
- Example Use¶

The message bus system can be used to receive notifications when properties of Blender data-blocks are changed via the data API.

The message bus system is triggered by updates via the RNA system. This means that the following updates will result in a notification on the message bus:

Changes via the Python API, for example some_object.location.x += 3.

Changes via the sliders, fields, and buttons in the user interface.

The following updates do not trigger message bus notifications:

Moving objects in the 3D Viewport.

Changes performed by the animation system.

Changes done from msgbus callbacks are not included in related undo steps, so users can easily skip their effects by using Undo followed by Redo.

Unlike properties update callbacks, message bus update callbacks are postponed until all operators have finished executing. Additionally, for each property the callback is only triggered once per update cycle, even if the property was changed multiple times during that period.

Below is an example of subscription to changes in the active object’s location.

Some properties are converted to Python objects when you retrieve them. This needs to be avoided in order to create the subscription, by using datablock.path_resolve("property_name", False):

It is also possible to create subscriptions on a property of all instances of a certain type:

Clear all subscribers using this owner.

key (bpy.types.Property | bpy.types.Struct | tuple[bpy.types.Struct, str]) – Represents the type of data being subscribed to Arguments include - A property instance. - A struct type. - A tuple representing a (struct, property name) pair.

Represents the type of data being subscribed to

Arguments include - A property instance. - A struct type. - A tuple representing a (struct, property name) pair.

Notify subscribers of changes to this property (this typically doesn’t need to be called explicitly since changes will automatically publish updates). In some cases it may be useful to publish changes explicitly using more general keys.

Register a message bus subscription. It will be cleared when another blend file is loaded, or can be cleared explicitly via bpy.msgbus.clear_by_owner().

key (bpy.types.Property | bpy.types.Struct | tuple[bpy.types.Struct, str]) – Represents the type of data being subscribed to Arguments include - A property instance. - A struct type. - A tuple representing a (struct, property name) pair.

Represents the type of data being subscribed to

Arguments include - A property instance. - A struct type. - A tuple representing a (struct, property name) pair.

owner (Any) – Handle for this subscription (compared by identity).

options (set[str]) – Change the behavior of the subscriber. PERSISTENT when set, the subscriber will be kept when remapping ID data.

Change the behavior of the subscriber.

PERSISTENT when set, the subscriber will be kept when remapping ID data.

All subscribers will be cleared on file-load. Subscribers can be re-registered on load, see bpy.app.handlers.load_post.

**Examples:**

Example 1 (swift):
```swift
import bpy

# Any Python object can act as the subscription's owner.
owner = object()

subscribe_to = bpy.context.object.location


def msgbus_callback(*args):
    # This will print:
    # Something changed! (1, 2, 3)
    print("Something changed!", args)


bpy.msgbus.subscribe_rna(
    key=subscribe_to,
    owner=owner,
    args=(1, 2, 3),
    notify=msgbus_callback,
)
```

Example 2 (unknown):
```unknown
subscribe_to = bpy.context.object.path_resolve("name", False)
```

Example 3 (unknown):
```unknown
subscribe_to = (bpy.types.Object, "location")
```

---
