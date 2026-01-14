# Blender5_Addons - Other

**Pages:** 9

---

## Blender 5.0 Python API Documentation¶

**URL:** https://docs.blender.org/api/current/index.html

**Contents:**
- Blender 5.0 Python API Documentation¶
- Documentation¶
- Indices¶

Welcome to the Python API documentation for Blender, the free and open source 3D creation suite.

This site can be used offline: Download the full documentation (zipped HTML files)

Quickstart: New to Blender or scripting and want to get your feet wet?

API Overview: A more complete explanation of Python integration.

API Reference Usage: Examples of how to use the API reference docs.

Best Practice: Conventions to follow for writing good scripts.

Tips and Tricks: Hints to help you while writing scripts for Blender.

Gotchas: Some of the problems you may encounter when writing scripts.

Advanced: Topics which may not be required for typical usage.

Change Log: List of changes since last Blender release

---

## API Overview¶

**URL:** https://docs.blender.org/api/current/info_overview.html

**Contents:**
- API Overview¶
- Python in Blender¶
- The Default Environment¶
- Script Loading¶
  - Add-ons¶
- Integration through Classes¶
  - Construction & Destruction¶
- Registration¶
  - Module Registration¶
  - Class Registration¶

The purpose of this document is to explain how Python and Blender fit together, covering some of the functionality that may not be obvious from reading the API references and example scripts.

Blender has an embedded Python interpreter which is loaded when Blender is started and stays active while Blender is running. This interpreter runs scripts to draw the user interface and is used for some of Blender’s internal tools as well.

Blender’s embedded interpreter provides a typical Python environment, so code from tutorials on how to write Python scripts can also be run with Blender’s interpreter. Blender provides its Python modules, such as bpy and mathutils, to the embedded interpreter so they can be imported into a script and give access to Blender’s data, classes, and functions. Scripts that deal with Blender data will need to import the modules to work.

Here is a simple example which moves a vertex attached to an object named “Cube”:

This modifies Blender’s internal data directly. When you run this in the interactive console you will see the 3D Viewport update.

When developing your own scripts it may help to understand how Blender sets up its Python environment. Many Python scripts come bundled with Blender and can be used as a reference because they use the same API that script authors write tools in. Typical usage for scripts include: user interface, import/export, scene manipulation, automation, defining your own tool set and customization.

On startup Blender scans the scripts/startup/ directory for Python modules and imports them. The exact location of this directory depends on your installation. See the directory layout docs.

This may seem obvious, but it is important to note the difference between executing a script directly and importing a script as a module.

Extending Blender by executing a script directly means the classes that the script defines remain available inside Blender after the script finishes execution. Using scripts this way makes future access to their classes (to unregister them for example) more difficult compared to importing the scripts as modules. When a script is imported as a module, its class instances will remain inside the module and can be accessed later on by importing that module again.

For this reason it is preferable to avoid directly executing scripts that extend Blender by registering classes.

Here are some ways to run scripts directly in Blender:

Loaded in the text editor and press Run Script.

Typed or pasted into the interactive console.

Execute a Python file from the command line with Blender, e.g:

The obvious way, import some_module command from the text editor or interactive console.

Open as a text data-block and check the Register option, this will load with the blend-file.

Copy into one of the directories scripts/startup, where they will be automatically imported on startup.

Define as an add-on, enabling the add-on will load it as a Python module.

Some of Blender’s functionality is best kept optional, alongside scripts loaded at startup there are add-ons which are kept in their own directory scripts/addons, They are only loaded on startup if selected from the user preferences.

The only difference between add-ons and built-in Python modules is that add-ons must contain a bl_info variable which Blender uses to read metadata such as name, author, category and project link. The User Preferences add-on listing uses bl_info to display information about each add-on. See Add-ons for details on the bl_info dictionary.

Running Python scripts in the text editor is useful for testing but you’ll want to extend Blender to make tools accessible like other built-in functionality.

The Blender Python API allows integration for:

bpy.types.PropertyGroup

bpy.types.RenderEngine

This is intentionally limited. Currently, for more advanced features such as mesh modifiers, object types, or shader nodes, C/C++ must be used.

For Python integration Blender defines methods which are common to all types. This works by creating a Python subclass of a Blender class which contains variables and functions specified by the parent class which are predefined to interface with Blender.

First note that it defines a subclass as a member of bpy.types, this is common for all classes which can be integrated with Blender and is used to distinguish an Operator from a Panel when registering.

Both class properties start with a bl_ prefix. This is a convention used to distinguish Blender properties from those you add yourself. Next see the execute function, which takes an instance of the operator and the current context. A common prefix is not used for functions. Lastly the register function is called, this takes the class and loads it into Blender. See Class Registration.

Regarding inheritance, Blender doesn’t impose restrictions on the kinds of class inheritance used, the registration checks will use attributes and functions defined in parent classes.

Class mix-in example:

Modal operators are an exception, keeping their instance variable as Blender runs, see modal operator template.

So once the class is registered with Blender, instancing the class and calling the functions is left up to Blender. In fact you cannot instance these classes from the script as you would expect with most Python API’s. To run operators you can call them through the operator API, e.g:

User interface classes are given a context in which to draw, buttons, window, file header, toolbar, etc., then they are drawn when that area is displayed so they are never called by Python scripts directly.

In the examples above, the classes don’t define an __init__(self) function. In general, defining custom constructors or destructors should not be needed, and is not recommended.

The lifetime of class instances is usually very short (also see the dedicated section), a panel for example will have a new instance for every redraw. Some other types, like bpy.types.Operator, have an even more complex internal handling, which can lead to several instantiations for a single operator execution.

There are a few cases where defining __init__() does make sense, e.g. when sub-classing a bpy.types.RenderEngine. When doing so, the parent matching function must always be called, otherwise Blender’s internal initialization won’t happen properly:

The Blender-defined parent constructor must be called before any data access to the object, including from other potential parent types __init__() functions.

Calling the parent’s __init__() function is a hard requirement since Blender 4.4. The ‘generic’ signature is the recommended one here, as Blender internal BPY code is typically the only caller of these functions. The actual arguments passed to the constructor are fully internal data, and may change depending on the implementation.

Unfortunately, the error message, generated in case the expected constructor is not called, can be fairly cryptic and unhelping. Generally they should be about failure to create a (python) object:

MemoryError: couldn’t create bpy_struct object_

With Operators, it might be something like that:

RuntimeError: could not create instance of <OPERATOR_OT_identifier> to call callback function execute

In case you are using complex/multi-inheritance, super() may not work (as the Blender-defined parent may not be the first type in the MRO). It is best then to first explicitly invoke the Blender-defined parent class constructor, before any other. For example:

Defining a custom __new__() function is strongly discouraged, not tested, and not considered as supported currently. Doing so presents a very high risk of crashes or otherwise corruption of Blender internal data. But if defined, it must take the same two generic positional and keyword arguments, and call the parent’s __new__() with them if actually creating a new object.

Due to internal CPython implementation details, C++-defined Blender types do not define or use a __del__() (aka tp_finalize()) destructor currently. As this function does not exist if not explicitly defined, that means that calling super().__del__() in the __del__() function of a sub-class will fail with the following error: AttributeError: 'super' object has no attribute '__del__'. If a call to the MRO ‘parent’ destructor is needed for some reason, the caller code must ensure that the destructor does exist, e.g. using something like that: getattr(super(), "__del__", lambda self: None)(self)

Blender modules loaded at startup require register() and unregister() functions. These are the only functions that Blender calls from your code, which is otherwise a regular Python module.

A simple Blender Python module can look like this:

These functions usually appear at the bottom of the script containing class registration sometimes adding menu items. You can also use them for internal purposes setting up data for your own tools but take care since register won’t re-run when a new blend-file is loaded.

The register/unregister calls are used so it’s possible to toggle add-ons and reload scripts while Blender runs. If the register calls were placed in the body of the script, registration would be called on import, meaning there would be no distinction between importing a module or loading its classes into Blender. This becomes problematic when a script imports classes from another module making it difficult to manage which classes are being loaded and when.

The last two lines are only for testing:

This allows the script to be run directly in the text editor to test changes. This register() call won’t run when the script is imported as a module since __main__ is reserved for direct execution.

Registering a class with Blender results in the class definition being loaded into Blender, where it becomes available alongside existing functionality. Once this class is loaded you can access it from bpy.types, using the bl_idname rather than the classes original name.

There are some exceptions to this for class names which aren’t guarantee to be unique. In this case use: bpy.types.Struct.bl_rna_get_subclass_py().

When loading a class, Blender performs sanity checks making sure all required properties and functions are found, that properties have the correct type, and that functions have the right number of arguments.

Mostly you will not need concern yourself with this but if there is a problem with the class definition it will be raised on registering:

Using the function arguments def execute(self, context, spam), will raise an exception:

ValueError: expected Operator, SimpleOperator class "execute" function to have 2 args, found 3

Using bl_idname = 1 will raise:

TypeError: validating class error: Operator.bl_idname expected a string type, not int

When customizing Blender you may want to group your own settings together, after all, they will likely have to co-exist with other scripts. To group these properties classes need to be defined, for groups within groups or collections within groups you can’t avoid having to deal with the order of registration/unregistration.

Custom properties groups are themselves classes which need to be registered.

For example, if you want to store material settings for a custom engine:

The class must be registered before being used in a property, failing to do so will raise an error:

ValueError: bpy_struct "Material" registration error: my_custom_props could not register

The lower most class needs to be registered first and that unregister() is a mirror of register().

Properties can be added and removed as Blender runs, normally done on register or unregister but for some special cases it may be useful to modify types as the script runs.

This works just as well for PropertyGroup subclasses you define yourself.

This is equivalent to:

In some cases the specifier for data may not be in Blender, for example a external render engines shader definitions, and it may be useful to define them as types and remove them on the fly.

type() is called to define the class. This is an alternative syntax for class creation in Python, better suited to constructing classes dynamically.

To call the operators from the previous example:

**Examples:**

Example 1 (python):
```python
import bpy
bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
```

Example 2 (unknown):
```unknown
blender --python /home/me/my_script.py
```

Example 3 (swift):
```swift
import bpy
class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Tool Name"

    def execute(self, context):
        print("Hello World")
        return {'FINISHED'}

bpy.utils.register_class(SimpleOperator)
```

Example 4 (python):
```python
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

---

## Best Practice¶

**URL:** https://docs.blender.org/api/current/info_best_practice.html

**Contents:**
- Best Practice¶
- Style Conventions¶
- User Interface Layout¶
- Script Efficiency¶
  - List Manipulation (General Python Tips)¶
    - Searching for List Items¶
    - Modifying Lists¶
    - Adding List Items¶
    - Removing List Items¶
    - Avoid Copying Lists¶

When writing your own scripts Python is great for new developers to pick up and become productive, but you can also pick up bad practices or at least write scripts that are not easy for others to understand. For your own work this is of course fine, but if you want to collaborate with others or have your work included with Blender there are practices we encourage.

For Blender Python development we have chosen to follow Python suggested style guide to avoid mixing styles among our own scripts and make it easier to use Python scripts from other projects. Using our style guide for your own scripts makes it easier if you eventually want to contribute them to Blender.

This style guide is known as pep8 and here is a brief listing of pep8 criteria:

Camel caps for class names: MyClass

All lower case underscore separated module names: my_module

Indentation of 4 spaces (no tabs)

Spaces around operators: 1 + 1, not 1+1

Only use explicit imports (no wildcard importing *)

Don’t use multiple statements on a single line: if val: body, separate onto two lines instead.

As well as pep8 we have additional conventions used for Blender Python scripts:

Use single quotes for enums, and double quotes for strings.

Both are of course strings, but in our internal API enums are unique items from a limited set, e.g:

pep8 also defines that lines should not exceed 79 characters, we have decided that this is too restrictive so it is optional per script.

Some notes to keep in mind when writing UI layouts:

UI code is quite simple. Layout declarations are there to easily create a decent layout. The general rule here is: If you need more code for the layout declaration, than for the actual properties, then you are doing it wrong.

The basic layout is a simple top-to-bottom layout.

Use row(), when you want more than one property in a single line.

Use column(), when you want your properties in a column.

This can be used to create more complex layouts. For example, you can split the layout and create two column() layouts next to each other. Do not use split, when you simply want two properties in a row. Use row() instead.

Try to only use these variable names for layout declarations:

for a column() layout

for a column_flow() layout

for a sub layout (a column inside a column for example)

In Python there are some handy list functions that save you having to search through the list. Even though you are not looping on the list data Python is, so you need to be aware of functions that will slow down your script by searching the whole list.

In Python you can add and remove from a list, this is slower when the list length is modified, especially at the start of the list, since all the data after the index of modification needs to be moved up or down one place.

The fastest way to add onto the end of the list is to use my_list.append(list_item) or my_list.extend(some_list) and to remove an item is my_list.pop() or del my_list[-1].

To use an index you can use my_list.insert(index, list_item) or list.pop(index) for list removal, but these are slower.

Sometimes it’s faster (but less memory efficient) to just rebuild the list. For example if you want to remove all triangular polygons in a list. Rather than:

It’s faster to build a new list with list comprehension:

If you have a list that you want to add onto another list, rather than:

Note that insert can be used when needed, but it is slower than append especially when inserting at the start of a long list. This example shows a very suboptimal way of making a reversed list:

Python provides more convenient ways to reverse a list using the slice method, but you may want to time this before relying on it too much:

Use my_list.pop(index) rather than my_list.remove(list_item). This requires you to have the index of the list item but is faster since remove() will search the list. Here is an example of how to remove items in one loop, removing the last items first, which is faster (as explained above):

This example shows a fast way of removing items, for use in cases where you can alter the list order without breaking the script’s functionality. This works by swapping two list items, so the item you remove is always last:

When removing many items in a large list this can provide a good speed-up.

When passing a list or dictionary to a function, it is faster to have the function modify the list rather than returning a new list so Python doesn’t have to duplicate the list in memory.

Functions that modify a list in-place are more efficient than functions that create new lists. This is generally slower so only use for functions when it makes sense not to modify the list in place:

This is generally faster since there is no re-assignment and no list duplication:

Also note that, passing a sliced list makes a copy of the list in Python memory:

If my_list was a large array containing 10,000’s of items, a copy could use a lot of extra memory.

Here are three ways of joining multiple strings into one string for writing. This also applies to any area of your code that involves a lot of string joining:

This is the slowest option, do not use this if you can avoid it, especially when writing data in a loop.

Use this when you are writing string data from floats and ints.

Use this to join a list of strings (the list may be temporary). In the following example, the strings are joined with a space “ “ in between, other examples are “” or “, “.

Join is fastest on many strings, string formatting is quite fast too (better for converting data types). String concatenation is the slowest.

Since many file formats are ASCII, the way you parse/export strings can make a large difference in how fast your script runs.

There are a few ways to parse strings when importing them into Blender.

Use float(string) rather than eval(string), if you know the value will be an int then int(string), float() will work for an int too but it is faster to read ints with int().

If you are checking the start of a string for a keyword, rather than:

Using startswith() is slightly faster (around 5%) and also avoids a possible error with the slice length not matching the string length.

my_string.endswith("foo_bar") can be used for line endings too.

If you are unsure whether the text is upper or lower case, use the lower() or upper() string function:

The try statement is useful to save time writing error checking code. However, try is significantly slower than an if since an exception has to be set each time, so avoid using try in areas of your code that execute in a loop and runs many times.

There are cases where using try is faster than checking whether the condition will raise an error, so it is worth experimenting.

Python has two ways to compare values a == b and a is b, the difference is that == may run the objects comparison function __cmp__() whereas is compares identity, this is, that both variables reference the same item in memory.

In cases where you know you are checking for the same value which is referenced from multiple places, is is faster.

While developing a script it is good to time it to be aware of any changes in performance, this can be done simply:

**Examples:**

Example 1 (unknown):
```unknown
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "//render_out"
```

Example 2 (unknown):
```unknown
layout.prop()
layout.prop()
```

Example 3 (unknown):
```unknown
row = layout.row()
row.prop()
row.prop()
```

Example 4 (unknown):
```unknown
col = layout.column()
col.prop()
col.prop()
```

---

## Tips and Tricks¶

**URL:** https://docs.blender.org/api/current/info_tips_and_tricks.html

**Contents:**
- Tips and Tricks¶
- Use the Terminal¶
- Interface Tricks¶
  - Access Operator Commands¶
  - Access Data Path¶
- Show All Operators¶
- Use an External Editor¶
  - Executing External Scripts¶
  - Executing Modules¶
- Use Blender without it’s User Interface¶

Here are various suggestions that you might find useful when writing scripts. Some of these are just Python features that you may not have thought to use with Blender, others are Blender-specific.

When writing Python scripts, it’s useful to have a terminal open, this is not the built-in Python console but a terminal application which is used to start Blender.

The three main use cases for the terminal are:

You can see the output of print() as your script runs, which is useful to view debug info.

The error traceback is printed in full to the terminal which won’t always generate an report message in Blender’s user interface (depending on how the script is executed).

If the script runs for too long or you accidentally enter an infinite loop, Ctrl-C in the terminal (Ctrl-Break on Windows) will quit the script early.

Launching from the Command Line.

You may have noticed that the tooltip for menu items and buttons includes the bpy.ops.[...] command to run that button, a handy (hidden) feature is that you can press Ctrl-C over any menu item or button to copy this command into the clipboard.

To find the path from an ID data-block to its setting isn’t always so simple since it may be nested away. To get this quickly open the context menu of the setting and select Copy Data Path, if this can’t be generated, only the property name is copied.

This uses the same method for creating the animation path used by bpy.types.FCurve.data_path and bpy.types.DriverTarget.data_path drivers.

While Blender logs operators in the Info editor, this only reports operators with the REGISTER option enabled so as not to flood the Info view with calls to bpy.ops.view3d.smoothview and bpy.ops.view3d.zoom. Yet for testing it can be useful to see every operator called in a terminal, do this by enabling the debug option either by passing the --debug-wm argument when starting Blender or by setting bpy.app.debug_wm to True while Blender is running.

Blender’s text editor is fine for small changes and writing tests but its not full featured, for larger projects you’ll probably want to use a standalone editor or Python IDE. Editing a text file externally and having the same text open in Blender does work but isn’t that optimal so here are two ways you can use an external file from Blender. Using the following examples you’ll still need text data-block in Blender to execute, but reference an external file rather than including it directly.

This is the equivalent to running the script directly, referencing a script’s path from a two line code block.

You might want to reference a script relative to the blend-file.

This example shows loading a script in as a module and executing a module function.

Notice that the script is reloaded every time, this forces use of the modified version, otherwise the cached one in sys.modules would be used until Blender was restarted.

The important difference between this and executing the script directly is it has to call a function in the module, in this case main() but it can be any function, an advantage with this is you can pass arguments to the function from this small script which is often useful for testing different settings quickly.

The other issue with this is the script has to be in Python’s module search path. While this is not best practice – for testing purposes you can extend the search path, this following example adds the current blend-file’s directory to the search path and then loads the script as a module.

While developing your own scripts Blender’s interface can get in the way, manually reloading, running the scripts, opening file import, etc. adds overhead. For scripts that are not interactive it can end up being more efficient not to use Blender’s interface at all and instead execute the script on the command line.

You might want to run this with a blend-file so the script has some data to operate on.

Depending on your setup you might have to enter the full path to the Blender executable.

Once the script is running properly in background mode, you’ll want to check the output of the script, this depends completely on the task at hand, however, here are some suggestions:

Render the output to an image, use an image viewer and keep writing over the same image each time.

Save a new blend-file, or export the file using one of Blender’s exporters.

If the results can be displayed as text then print them or write them to a file.

While this can take a little time to setup, it can be well worth the effort to reduce the time it takes to test changes. You can even have Blender running the script every few seconds with a viewer updating the results, so no need to leave your text editor to see changes.

When there are no readily available Python modules to perform specific tasks it’s worth keeping in mind you may be able to have Python execute an external command on your data and read the result back in.

Using external programs adds an extra dependency and may limit who can use the script but to quickly setup your own custom pipeline or writing one-off scripts this can be handy.

Run Gimp in batch mode to execute custom scripts for advanced image processing.

Write out 3D models to use external mesh manipulation tools and read back in the results.

Convert files into recognizable formats before reading.

The Blender releases distributed from blender.org include a complete Python installation on all platforms, this has the disadvantage that any extensions you have installed on your system’s Python environment will not be found by Blender.

There are two ways to work around this:

Remove Blender Python subdirectory, Blender will then fall back on the system’s Python and use that instead.

Depending on your platform, you may need to explicitly reference the location of your Python installation using the PYTHONPATH environment variable, e.g:

The Python (major, minor) version must match the one that Blender comes with. Therefor you can’t use Python 3.6 with Blender built to use Python 3.7.

Copy or link the extensions into Blender’s Python subdirectory so Blender can access them, you can also copy the entire Python installation into Blender’s subdirectory, replacing the one Blender comes with. This works as long as the Python versions match and the paths are created in the same relative locations. Doing this has the advantage that you can redistribute this bundle to others with Blender including any extensions you rely on.

In the middle of a script you may want to inspect variables, run functions and inspect the flow.

If you want to access both global and local variables run this:

The next example is an equivalent single line version of the script above which is easier to paste into your code:

code.interact can be added at any line in the script and will pause the script to launch an interactive interpreter in the terminal, when you’re done you can quit the interpreter and the script will continue execution.

If you have IPython installed you can use its embed() function which uses the current namespace. The IPython prompt has auto-complete and some useful features that the standard Python eval-loop doesn’t have.

Admittedly this highlights the lack of any Python debugging support built into Blender, but its still a handy thing to know.

From a Python perspective it’s nicer to have everything as an extension which lets the Python script combine many components.

You can use external editors or IDEs with Blender’s Python API and execute scripts within the IDE (step over code, inspect variables as the script runs).

Editors or IDEs can auto-complete Blender modules and variables.

Existing scripts can import Blender APIs without having to be run inside of Blender.

This is marked advanced because to run Blender as a Python module requires a special build option. For instructions on building see Building Blender as a Python module.

Since it’s possible to access data which has been removed (see Gotchas), it can be hard to track down the cause of crashes. To raise Python exceptions on accessing freed data (rather than crashing), enable the CMake build option WITH_PYTHON_SAFETY. This enables data tracking which makes data access about two times slower which is why the option isn’t enabled in release builds.

**Examples:**

Example 1 (unknown):
```unknown
filename = "/full/path/to/myscript.py"
exec(compile(open(filename).read(), filename, 'exec'))
```

Example 2 (python):
```python
import bpy
import os

filename = os.path.join(os.path.dirname(bpy.data.filepath), "myscript.py")
exec(compile(open(filename).read(), filename, 'exec'))
```

Example 3 (python):
```python
import myscript
import importlib

importlib.reload(myscript)
myscript.main()
```

Example 4 (python):
```python
import sys
import os
import bpy

blend_dir = os.path.dirname(bpy.data.filepath)
if blend_dir not in sys.path:
   sys.path.append(blend_dir)

import myscript
import importlib
importlib.reload(myscript)
myscript.main()
```

---

## Gotchas¶

**URL:** https://docs.blender.org/api/current/info_gotcha.html

**Contents:**
- Gotchas¶

This document attempts to help you work with the Blender API in areas that can be troublesome and avoid practices that are known to cause instability.

---

## Troubleshooting Errors & Crashes¶

**URL:** https://docs.blender.org/api/current/info_gotchas_crashes.html

**Contents:**
- Troubleshooting Errors & Crashes¶
- Help! My script crashes Blender¶
  - Undo/Redo¶
    - Modifying Blender Data & Undo¶
    - Undo & Library Data¶
  - Abusing RNA property callbacks¶
  - Edit-Mode / Memory Access¶
  - Array Re-Allocation¶
  - Removing Data¶
  - Unfortunate Corner Cases¶

TL;DR Do not keep direct references to Blender data (of any kind) when modifying the container of that data, and/or when some undo/redo may happen (e.g. during modal operators execution…). Instead, use indices (or other data always stored by value in Python, like string keys…), that allow you to get access to the desired data.

Ideally it would be impossible to crash Blender from Python, however, there are some problems with the API where it can be made to crash. Strictly speaking this is a bug in the API but fixing it would mean adding memory verification on every access since most crashes are caused by the Python objects referencing Blender’s memory directly, whenever the memory is freed or re-allocated, further Python access to it can crash the script. But fixing this would make the scripts run very slow, or writing a very different kind of API which doesn’t reference the memory directly.

Here are some general hints to avoid running into these problems:

Be aware of memory limits, especially when working with large lists since Blender can crash simply by running out of memory.

Many hard to fix crashes end up being because of referencing freed data, when removing data be sure not to hold any references to it.

Re-allocation can lead to the same issues (e.g. if you add a lot of items to some Collection, this can lead to re-allocating the underlying container’s memory, invalidating all previous references to existing items).

Modules or classes that remain active while Blender is used, should not hold references to data the user may remove, instead, fetch data from the context each time the script is activated.

Crashes may not happen every time, they may happen more on some configurations or operating systems.

Be careful with recursive patterns, those are very efficient at hiding the issues described here.

See last subsection about Unfortunate Corner Cases for some known breaking exceptions.

To find the line of your script that crashes you can use the faulthandler module. See the Faulthandler docs.

While the crash may be in Blender’s C/C++ code, this can help a lot to track down the area of the script that causes the crash.

Some container modifications are actually safe, because they will never re-allocate existing data (e.g. linked lists containers will never re-allocate existing items when adding or removing others).

But knowing which cases are safe and which aren’t implies a deep understanding of Blender’s internals. That’s why, unless you are willing to dive into the RNA C implementation, it’s simpler to always assume that data references will become invalid when modifying their containers, in any possible way.

For safety, you should assume that undo and redo always invalidates all bpy.types.ID instances (Object, Scene, Mesh, Light, etc.), as well obviously as all of their sub-data.

This example shows how you can tell undo changes the memory locations:

Delete the active object, then undo:

As suggested above, simply not holding references to data when Blender is used interactively by the user is the only way to make sure that the script doesn’t become unstable.

Modern undo/redo system does not systematically invalidate all pointers anymore. Some data (in fact, most data, in typical cases), which were detected as unchanged for a particular history step, may remain unchanged and hence their pointers may remain valid.

Be aware that if you want to take advantage of this behavior for some reason, there is no guarantee of any kind that it will be safe and consistent. Use it at your own risk.

In general, when Blender data is modified, there should always be an undo step created for it. Otherwise, there will be issues, ranging from invalid/broken undo stack, to crashes on undo/redo.

This is especially true when modifying Blender data in operators.

One of the advantages with Blender’s library linking system that undo can skip checking changes in library data since it is assumed to be static. Tools in Blender are not allowed to modify library data. But Python does not enforce this restriction.

This can be useful in some cases, using a script to adjust material values for example. But it’s also possible to use a script to make library data point to newly created local data, which is not supported since a call to undo will remove the local data but leave the library referencing it and likely crash.

So it’s best to consider modifying library data an advanced usage of the API and only to use it when you know what you’re doing.

Python-defined RNA properties can have custom callbacks. Trying to perform complex operations from there, like calling an operator, may work, but is not officially recommended nor supported.

Main reason is that those callback should be very fast, but additionally, it may for example create issues with undo/redo system (most operators store an history step, and editing an RNA property does so as well), trigger infinite update loops, and so on.

Switching mode bpy.ops.object.mode_set(mode='EDIT') or bpy.ops.object.mode_set(mode='OBJECT') will re-allocate objects data, any references to a meshes vertices/polygons/UVs, armatures bones, curves points, etc. cannot be accessed after switching mode.

Only the reference to the data itself can be re-accessed, the following example will crash.

So after switching mode you need to re-access any object data variables, the following example shows how to avoid the crash above.

These kinds of problems can happen for any functions which re-allocate the object data but are most common when switching mode.

When adding new points to a curve or vertices/edges/polygons to a mesh, internally the array which stores this data is re-allocated.

This can be avoided by re-assigning the point variables after adding the new one or by storing indices to the points rather than the points themselves.

The best way is to sidestep the problem altogether by adding all the points to the curve at once. This means you don’t have to worry about array re-allocation and it’s faster too since re-allocating the entire array for every added point is inefficient.

Any data that you remove shouldn’t be modified or accessed afterwards, this includes: F-Curves, drivers, render layers, timeline markers, modifiers, constraints along with objects, scenes, collections, bones, etc.

The remove() API calls will invalidate the data they free to prevent common mistakes. The following example shows how this precaution works:

But take care because this is limited to scripts accessing the variable which is removed, the next example will still crash:

Besides all expected cases listed above, there are a few others that should not be an issue but, due to internal implementation details, currently are:

Changing: Object.hide_viewport, Object.hide_select or Object.hide_render will trigger a rebuild of Collection caches, thus breaking any current iteration over Collection.all_objects.

Data-blocks accessed from bpy.data are sorted when their name is set. Any loop that iterates of a data such as bpy.data.objects for example, and sets the objects name must get all items from the iterator first (typically by converting to a list or tuple) to avoid missing some objects and iterating over others multiple times.

Some Python modules will call sys.exit() themselves when an error occurs, while not common behavior this is something to watch out for because it may seem as if Blender is crashing since sys.exit() will close Blender immediately.

For example, the argparse module will print an error and exit if the arguments are invalid.

An dirty way of troubleshooting this is to set sys.exit = None and see what line of Python code is quitting, you could of course replace sys.exit with your own function but manipulating Python in this way is bad practice.

**Examples:**

Example 1 (php):
```php
class TestItems(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

bpy.utils.register_class(TestItems)
bpy.types.Scene.test_items = bpy.props.CollectionProperty(type=TestItems)

first_item = bpy.context.scene.test_items.add()
for i in range(100):
    bpy.context.scene.test_items.add()

# This is likely to crash, as internal code may re-allocate
# the whole container (the collection) memory at some point.
first_item.name = "foobar"
```

Example 2 (php):
```php
class TestItems(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

bpy.utils.register_class(TestItems)
bpy.types.Scene.test_items = bpy.props.CollectionProperty(type=TestItems)

first_item = bpy.context.scene.test_items.add()
for i in range(100):
    bpy.context.scene.test_items.add()

# This is safe, we are getting again desired data *after*
# all modifications to its container are done.
first_item = bpy.context.scene.test_items[0]
first_item.name = "foobar"
```

Example 3 (unknown):
```unknown
>>> hash(bpy.context.object)
-9223372036849950810
>>> hash(bpy.context.object)
-9223372036849950810
```

Example 4 (unknown):
```unknown
>>> hash(bpy.context.object)
-9223372036849951740
```

---

## Advanced¶

**URL:** https://docs.blender.org/api/current/info_advanced.html

**Contents:**
- Advanced¶

This chapter covers advanced use (topics which may not be required for typical usage).

---

## Blender as a Python Module¶

**URL:** https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html

**Contents:**
- Blender as a Python Module¶
- Use Cases¶
- Usage¶
- Limitations¶

Blender supports being built as a Python module, allowing import bpy to be added to any Python script, providing access to Blender’s features.

Blender as a Python Module isn’t provided on Blender’s official download page.

A pre-compiled bpy module is available via PIP.

Or you may compile this yourself using the build instructions.

Python developers may wish to integrate Blender scripts which don’t center around Blender.

Possible uses include:

Visualizing data by rendering images and animations.

Image processing using Blender’s compositor.

Video editing (using Blender’s sequencer).

Development, accessing bpy from Python IDE’s and debugging tools for example.

For the most part using Blender as a Python module is equivalent to running a script in background-mode (passing the command-line arguments --background or -b), however there are some differences to be aware of.

The attribute bpy.app.binary_path defaults to an empty string.

If you wish to point this to the location of a known executable you may set the value.

This example searches for the binary, setting it when found:

There are many modules included with Blender such as gpu and mathuils. It’s important that these are imported after bpy or they will not be found.

Functionality controlled by command line arguments (shown by calling blender --help aren’t accessible).

Typically this isn’t such a limitation although there are some command line arguments that don’t have equivalents in Blender’s Python API (--threads and --log for example).

Access to these settings may be added in the future as needed.

It’s possible other Python modules make use of the GPU in a way that prevents Blender/Cycles from accessing the GPU.

Blender’s typical signal handlers are not initialized, so there is no special handling for Control-C to cancel a render and a crash log is not written in the event of a crash.

When the bpy module loads it contains the default startup scene (instead of an “empty” blend-file as you might expect), so there is a default cube, camera and light.

If you wish to start from an empty file use: bpy.ops.wm.read_factory_settings(use_empty=True).

The users startup and preferences are ignored to prevent your local configuration from impacting scripts behavior. The Python module behaves as if --factory-startup was passed as a command line argument.

The users preferences and startup can be loaded using operators:

Most constraints of Blender as an application still apply:

Reloading the bpy module via importlib.reload will raise an exception instead of reloading and resetting the module.

Instead, the operator bpy.ops.wm.read_factory_settings() can be used to reset the internal state.

Only a single .blend file can be edited at a time.

As with the application it’s possible to start multiple instances, each with their own bpy and therefor Blender state. Python provides the multiprocessing module to make communicating with sub-processes more convenient.

In some cases the library API may be an alternative to starting separate processes, although this API operates on reading and writing ID data-blocks and isn’t a complete substitute for loading .blend files, see:

bpy.types.BlendDataLibraries.load()

bpy.types.BlendDataLibraries.write()

bpy.types.BlendData.temp_data() supports a temporary data-context to avoid manipulating the current .blend file.

**Examples:**

Example 1 (python):
```python
import bpy
import shutil

blender_bin = shutil.which("blender")
if blender_bin:
   print("Found:", blender_bin)
   bpy.app.binary_path = blender_bin
else:
   print("Unable to find blender!")
```

Example 2 (python):
```python
import bpy

bpy.ops.wm.read_userpref()
bpy.ops.wm.read_homefile()
```

---

## File Paths & String Encoding¶

**URL:** https://docs.blender.org/api/current/info_gotchas_file_paths_and_encoding.html

**Contents:**
- File Paths & String Encoding¶
- Relative File Paths¶
- Unicode Problems¶

Blender’s relative file paths are not compatible with standard Python modules such as sys and os. Built-in Python functions don’t understand Blender’s // prefix which denotes the blend-file path.

A common case where you would run into this problem is when exporting a material with associated image paths:

When using Blender data from linked libraries there is an unfortunate complication since the path will be relative to the library rather than the open blend-file. When the data block may be from an external blend-file pass the library argument from the bpy.types.ID.

These returns the absolute path which can be used with native Python modules.

Python supports many different encodings so there is nothing stopping you from writing a script in latin1 or iso-8859-15. See PEP 263.

However, this complicates matters for Blender’s Python API because .blend files don’t have an explicit encoding. To avoid the problem for Python integration and script authors we have decided that all strings in blend-files must be UTF-8, ASCII compatible. This means assigning strings with different encodings to an object name, for instance, will raise an error.

Paths are an exception to this rule since the existence of non-UTF-8 paths on the user’s file system cannot be ignored. This means seemingly harmless expressions can raise errors, e.g:

Here are two ways around file-system encoding issues:

Unicode encoding/decoding is a big topic with comprehensive Python documentation, to keep it short about encoding problems – here are some suggestions:

Always use UTF-8 encoding or convert to UTF-8 where the input is unknown.

Avoid manipulating file paths as strings directly, use os.path functions instead.

Use os.fsencode() or os.fsdecode() instead of built-in string decoding functions when operating on paths.

To print paths or to include them in the user interface use repr(path) first or "%r" % path with string formatting.

Sometimes it’s preferable to avoid string encoding issues by using bytes instead of Python strings, when reading some input it’s less trouble to read it as binary data though you will still need to decide how to treat any strings you want to use with Blender, some importers do this.

**Examples:**

Example 1 (unknown):
```unknown
>>> bpy.path.abspath(image.filepath)
```

Example 2 (unknown):
```unknown
>>> bpy.path.abspath(image.filepath, library=image.library)
```

Example 3 (yaml):
```yaml
>>> print(bpy.data.filepath)
UnicodeEncodeError: 'ascii' codec can't encode characters in position 10-21: ordinal not in range(128)
```

Example 4 (yaml):
```yaml
>>> bpy.context.object.name = bpy.data.filepath
Traceback (most recent call last):
  File "<blender_console>", line 1, in <module>
TypeError: bpy_struct: item.attr= val: Object.name expected a string type, not str
```

---
