# Blender5_Addons - Types

**Pages:** 398

---

## Types (bpy.types)¶

**URL:** https://docs.blender.org/api/current/bpy.types.html

**Contents:**
- Types (bpy.types)¶

---

## Context Access (bpy.context)¶

**URL:** https://docs.blender.org/api/current/bpy.context.html

**Contents:**
- Context Access (bpy.context)¶
- Global Context¶
- Buttons Context¶
- Clip Context¶
- File Context¶
- Image Context¶
- Node Context¶
- Screen Context¶
- Sequencer Context¶
- Text Context¶

The context members available depend on the area of Blender which is currently being accessed.

Note that all context values are read-only, but may be modified through the data API or by running operators.

These properties are available in any contexts.

bpy.types.Area, (readonly)

bpy.types.AssetRepresentation, (readonly)

bpy.types.BlendData, (readonly)

bpy.types.Collection, (readonly)

string, default “”, (readonly, never None)

bpy.types.GizmoGroup, (readonly)

bpy.types.LayerCollection, (readonly)

enum in Context Mode Items, default 'EDIT_MESH', (readonly)

bpy.types.Preferences, (readonly)

bpy.types.Region, (readonly)

bpy.types.RegionView3D, (readonly)

The temporary region for pop-ups (including menus and pop-overs)

bpy.types.Region, (readonly)

bpy.types.Scene, (readonly)

bpy.types.Screen, (readonly)

The current space, may be None in background-mode, when the cursor is outside the window or when using menu-search

bpy.types.Space, (readonly)

bpy.types.ToolSettings, (readonly)

bpy.types.ViewLayer, (readonly)

bpy.types.Window, (readonly)

bpy.types.WindowManager, (readonly)

bpy.types.WorkSpace, (readonly)

bpy.types.TextureSlot

bpy.types.MaterialSlot

bpy.types.ParticleSystem

bpy.types.ParticleSystem

bpy.types.ParticleSettings

bpy.types.ClothModifier

bpy.types.SoftBodyModifier

bpy.types.FluidSimulationModifier

bpy.types.CollisionModifier

bpy.types.DynamicPaintModifier

bpy.types.FreestyleLineStyle

bpy.types.LayerCollection

bpy.types.GreasePencil

bpy.types.GreasePencil

bpy.types.StripModifier

bpy.types.FileSelectEntry

sequence of bpy.types.FileSelectEntry

bpy.types.AssetLibraryReference

bpy.types.AssetRepresentation

sequence of bpy.types.AssetRepresentation

sequence of bpy.types.ID

sequence of bpy.types.Node

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.Object

sequence of bpy.types.EditBone

sequence of bpy.types.EditBone

sequence of bpy.types.EditBone

sequence of bpy.types.EditBone

sequence of bpy.types.PoseBone

sequence of bpy.types.PoseBone

sequence of bpy.types.PoseBone

bpy.types.EditBone or bpy.types.Bone

sequence of bpy.types.NlaStrip

sequence of bpy.types.MovieTrackingTrack

bpy.types.GreasePencil

bpy.types.GPencilLayer

bpy.types.GreasePencil

sequence of bpy.types.Action

sequence of bpy.types.Action

sequence of bpy.types.FCurve

sequence of bpy.types.FCurve

sequence of bpy.types.FCurve

sequence of bpy.types.FCurve

sequence of bpy.types.Keyframe

bpy.types.AnyType or str or int

Get the property associated with a hovered button. Returns a tuple of the data-block, data path to the property, and array index.

When the property doesn’t have an associated bpy.types.ID non-ID data may be returned. This may occur when accessing windowing data, for example, operator properties.

bpy.types.AssetLibraryReference

sequence of bpy.types.Strip

sequence of bpy.types.Strip

sequence of bpy.types.Strip

bpy.types.ToolSettings

sequence of bpy.types.ID

**Examples:**

Example 1 (markdown):
```markdown
# Example inserting keyframe for the hovered property.
active_property = bpy.context.property
if active_property:
    datablock, data_path, index = active_property
    datablock.keyframe_insert(data_path=data_path, index=index, frame=1)
```

---

## API Reference Usage¶

**URL:** https://docs.blender.org/api/current/info_api_reference.html

**Contents:**
- API Reference Usage¶
- Reference API Scope¶
- Data Access¶
  - ID Data¶
  - Simple Data Access¶
  - Nested Properties¶
  - Copy Data Path¶
  - Indirect Data Access¶
- Operators¶
  - Info Editor¶

Blender has many interlinking data types which have an auto-generated reference API which often has the information you need to write a script, but can be difficult to use. This document is designed to help you understand how to use the reference API.

The reference API covers bpy.types, which stores types accessed via bpy.context – the user context or bpy.data – blend-file data.

Other modules such as bmesh and aud are not using Blender’s data API so this document doesn’t apply to those modules.

The most common case for using the reference API is to find out how to access data in the blend-file. Before going any further it’s best to be aware of ID data-blocks in Blender since you will often find properties relative to them.

ID data-blocks are used in Blender as top-level data containers. From the user interface this isn’t so obvious, but when developing you need to know about ID data-blocks. ID data types include Scene, Group, Object, Mesh, Workspace, World, Armature, Image and Texture. For a full list see the subclasses of bpy.types.ID.

Here are some characteristics ID data-blocks share:

IDs are blend-file data, so loading a new blend-file reloads an entire new set of data-blocks.

IDs can be accessed in Python from bpy.data.*.

Each data-block has a unique .name attribute, displayed in the interface.

Animation data is stored in IDs .animation_data.

IDs are the only data types that can be linked between blend-files.

IDs can be added/copied and removed via Python.

IDs have their own garbage-collection system which frees unused IDs when saving.

When a data-block has a reference to some external data, this is typically an ID data-block.

In this simple case a Python script is used to adjust the object’s location. Start by collecting the information where the data is located.

First find this setting in the interface Properties editor -> Object -> Transform -> Location. From the button context menu select Online Python Reference, this will link you to: bpy.types.Object.location. Being an API reference, this link often gives little more information than the tooltip, though some of the pages include examples (normally at the top of the page). But you now know that you have to use .location and that it’s an array of three floats.

So the next step is to find out where to access objects, go down to the bottom of the page to the references section, for objects there are many references, but one of the most common places to access objects is via the context. It’s easy to be overwhelmed at this point since there Object get referenced in so many places: modifiers, functions, textures and constraints. But if you want to access any data the user has selected you typically only need to check the bpy.context references.

Even then, in this case there are quite a few though if you read over these you’ll notice that most are mode specific. If you happen to be writing a tool that only runs in Weight Paint Mode, then using weight_paint_object would be appropriate. However, to access an item the user last selected, look for the active members, Having access to a single active member the user selects is a convention in Blender: e.g. active_bone, active_pose_bone, active_node, etc. and in this case you can use active_object.

So now you have enough information to find the location of the active object.

You can type this into the Python console to see the result. The other common place to access objects in the reference is bpy.types.BlendData.objects.

This is not listed as bpy.data.objects, this is because bpy.data is an instance of the bpy.types.BlendData class, so the documentation points there.

With bpy.data.objects, this is a collection of objects so you need to access one of its members:

The previous example is quite straightforward because location is a property of Object which can be accessed from the context directly.

Here are some more complex examples:

As you can see there are times when you want to access data which is nested in a way that causes you to go through a few indirections. The properties are arranged to match how data is stored internally (in Blender’s C code) which is often logical but not always quite what you would expect from using Blender. So this takes some time to learn, it helps you understand how data fits together in Blender which is important to know when writing scripts.

When starting out scripting you will often run into the problem where you’re not sure how to access the data you want. There are a few ways to do this:

Use the Python console’s auto-complete to inspect properties. This can be hit-and-miss but has the advantage that you can easily see the values of properties and assign them to interactively see the results.

Copy the data path from the user interface. Explained further in Copy Data Path.

Using the documentation to follow references. Explained further in Indirect Data Access.

Blender can compute the Python string to a property which is shown in the tooltip, on the line below Python: .... This saves having to open the API references to find where data is accessed from. In the context menu is a copy data-path tool which gives the path from an bpy.types.ID data-block, to its property.

To see how this works you’ll get the path to the Subdivision Surface modifiers Levels setting. Start with the default scene and select the Modifiers tab, then add a Subdivision Surface modifier to the cube. Now hover your mouse over the button labeled Levels Viewport, The tooltip includes bpy.types.SubsurfModifier.levels but you want the path from the object to this property.

Note that the text copied won’t include the bpy.data.collection["name"]. component since its assumed that you won’t be doing collection look-ups on every access and typically you’ll want to use the context rather than access each bpy.types.ID instance by name.

Type in the ID path into a Python console bpy.context.active_object. Include the trailing dot and don’t execute the code, yet.

Now in the button’s context menu select Copy Data Path, then paste the result into the console:

Press Return and you’ll get the current value of 1. Now try changing the value to 2:

You can see the value update in the Subdivision Surface modifier’s UI as well as the cube.

This more advanced example shows the steps to access the active sculpt brushes texture. For example, if you want to access the texture of a brush via Python to adjust its contrast.

Start in the default scene and enable Sculpt Mode from the 3D Viewport header.

From the Sidebar expand the Brush Settings panel’s Texture subpanel and add a new texture. Notice the texture data-block menu itself doesn’t have very useful links (you can check the tooltips).

The contrast setting isn’t exposed in the Sidebar, so view the texture in the Properties Editor.

Open the context menu of the contrast field and select Online Python Reference. This takes you to bpy.types.Texture.contrast. Now you can see that contrast is a property of texture.

To find out how to access the texture from the brush check on the references at the bottom of the page. Sometimes there are many references, and it may take some guesswork to find the right one, but in this case it’s tool_settings.sculpt.brush.texture.

Now you know that the texture can be accessed from bpy.data.brushes["BrushName"].texture but normally you won’t want to access the brush by name, instead you want to access the active brush. So the next step is to check on where brushes are accessed from via the references.

Now you can use the Python console to form the nested properties needed to access brush textures contrast: Context ‣ Tool Settings ‣ Sculpt ‣ Brush ‣ Texture ‣ Contrast.

Since the attribute for each is given along the way you can compose the data path in the Python console:

Or access the brush directly:

If you are writing a user tool normally you want to use the bpy.context since the user normally expects the tool to operate on what they have selected. For automation you are more likely to use bpy.data since you want to be able to access specific data and manipulate it, no matter what the user currently has the view set at.

Most hotkeys and buttons in Blender call an operator which is also exposed to Python via bpy.ops.

To see the Python equivalent hover your mouse over the button and see the tooltip, e.g Python: bpy.ops.render.render(), If there is no tooltip or the Python: line is missing then this button is not using an operator and can’t be accessed from Python.

If you want to use this in a script you can press Ctrl-C while your mouse is over the button to copy it to the clipboard. You can also use button’s context menu and view the Online Python Reference, this mainly shows arguments and their defaults, however, operators written in Python show their file and line number which may be useful if you are interested to check on the source code.

Not all operators can be called usefully from Python, for more on this see using operators.

Blender records operators you run and displays them in the Info editor. Select the Scripting workspace that comes default with Blender to see its output. You can perform some actions and see them show up – delete a vertex for example.

Each entry can be selected, then copied Ctrl-C, usually to paste in the text editor or Python console.

Not all operators get registered for display, zooming the view for example isn’t so useful to repeat so it’s excluded from the output.

To display every operator that runs see Show All Operators.

**Examples:**

Example 1 (unknown):
```unknown
bpy.context.active_object.location
```

Example 2 (unknown):
```unknown
bpy.data.objects["Cube"].location
```

Example 3 (markdown):
```markdown
# Access the number of samples for the Cycles render engine.
bpy.context.scene.cycles.samples

# Access to the current weight paint brush size.
bpy.context.tool_settings.weight_paint.brush.size

# Check if the window is full-screen.
bpy.context.window.screen.show_fullscreen
```

Example 4 (unknown):
```unknown
bpy.context.active_object.modifiers["Subdivision"].levels
```

---

## Modes and Mesh Access¶

**URL:** https://docs.blender.org/api/current/info_gotchas_meshes.html

**Contents:**
- Modes and Mesh Access¶
- N-Gons and Tessellation¶
  - Support Overview¶
  - Creating¶
  - Editing¶
  - Exporting¶

When working with mesh data you may run into the problem where a script fails to run as expected in Edit-Mode. This is caused by Edit-Mode having its own data which is only written back to the mesh when exiting Edit-Mode.

A common example is that exporters may access a mesh through obj.data (a bpy.types.Mesh) when the user is in Edit-Mode, where the mesh data is available but out of sync with the edit mesh.

In this situation you can…

Exit Edit-Mode before running the tool.

Explicitly update the mesh by calling bmesh.types.BMesh.to_mesh.

Modify the script to support working on the edit-mode data directly, see: bmesh.from_edit_mesh.

Report the context as incorrect and only allow the script to run outside Edit-Mode.

Since 2.63 n-gons are supported, this adds some complexity since in some cases you need to access triangles still (some exporters for example).

There are now three ways to access faces:

bpy.types.MeshPolygon – this is the data structure which now stores faces in Object-Mode (access as mesh.polygons rather than mesh.faces).

bpy.types.MeshLoopTriangle – the result of tessellating polygons into triangles (access as mesh.loop_triangles).

bmesh.types.BMFace – the polygons as used in Edit-Mode.

For the purpose of the following documentation, these will be referred to as polygons, loop triangles and BMesh-faces respectively.

Faces with five or more sides will be referred to as ngons.

bpy.types.MeshPolygon

bpy.types.MeshLoopTriangle

Unusable (read-only).

Unusable (read-only).

Good (When n-gons cannot be used)

Good (n-gons, extra memory overhead)

Using the bmesh API is completely separate API from bpy, typically you would use one or the other based on the level of editing needed, not simply for a different way to access faces.

All three data types can be used for face creation:

Polygons are the most efficient way to create faces but the data structure is very rigid and inflexible, you must have all your vertices and faces ready and create them all at once. This is further complicated by the fact that each polygon does not store its own vertices, rather they reference an index and size in bpy.types.Mesh.loops which are a fixed array too.

BMesh-faces are most likely the easiest way to create faces in new scripts, since faces can be added one by one and the API has features intended for mesh manipulation. While bmesh.types.BMesh uses more memory it can be managed by only operating on one mesh at a time.

Editing is where the three data types vary most.

Polygons are very limited for editing, changing materials and options like smooth works, but for anything else they are too inflexible and are only intended for storage.

Loop-triangles should not be used for editing geometry because doing so will cause existing n-gons to be tessellated.

BMesh-faces are by far the best way to manipulate geometry.

All three data types can be used for exporting, the choice mostly depends on whether the target format supports n-gons or not.

Polygons are the most direct and efficient way to export providing they convert into the output format easily enough.

Loop-triangles work well for exporting to formats which don’t support n-gons, in fact this is the only place where their use is encouraged.

BMesh-Faces can work for exporting too but may not be necessary if polygons can be used since using BMesh gives some overhead because it’s not the native storage format in Object-Mode.

---

## Change Log¶

**URL:** https://docs.blender.org/api/current/change_log.html

**Contents:**
- Change Log¶
- 4.5 to 5.0¶
  - bpy.types.Action¶
    - Removed¶
    - Function Arguments¶
  - bpy.types.ActionChannelbagFCurves¶
    - Added¶
    - Function Arguments¶
  - bpy.types.AddonPreferences¶
    - Added¶

Changes in Blender’s Python API between releases.

bpy.types.Action.fcurve_ensure_for_datablock (datablock, data_path, index, group_name), was (datablock, data_path, index)

bpy.types.ActionChannelbagFCurves.ensure

bpy.types.ActionChannelbagFCurves.new_from_fcurve

bpy.types.ActionChannelbagFCurves.new (data_path, index, group_name), was (data_path, index)

bpy.types.AddonPreferences.bl_system_properties_get

bpy.types.AreaLight.inline_shader_nodes

bpy.types.AssetShelf.bl_drag_operator

bpy.types.AssetShelf.filter_action

bpy.types.AssetShelf.filter_annotations

bpy.types.AssetShelf.filter_armature

bpy.types.AssetShelf.filter_brush

bpy.types.AssetShelf.filter_cachefile

bpy.types.AssetShelf.filter_camera

bpy.types.AssetShelf.filter_curve

bpy.types.AssetShelf.filter_curves

bpy.types.AssetShelf.filter_font

bpy.types.AssetShelf.filter_grease_pencil

bpy.types.AssetShelf.filter_group

bpy.types.AssetShelf.filter_image

bpy.types.AssetShelf.filter_lattice

bpy.types.AssetShelf.filter_light

bpy.types.AssetShelf.filter_light_probe

bpy.types.AssetShelf.filter_linestyle

bpy.types.AssetShelf.filter_mask

bpy.types.AssetShelf.filter_material

bpy.types.AssetShelf.filter_mesh

bpy.types.AssetShelf.filter_metaball

bpy.types.AssetShelf.filter_movie_clip

bpy.types.AssetShelf.filter_node_tree

bpy.types.AssetShelf.filter_object

bpy.types.AssetShelf.filter_paint_curve

bpy.types.AssetShelf.filter_palette

bpy.types.AssetShelf.filter_particle_settings

bpy.types.AssetShelf.filter_pointcloud

bpy.types.AssetShelf.filter_scene

bpy.types.AssetShelf.filter_sound

bpy.types.AssetShelf.filter_speaker

bpy.types.AssetShelf.filter_text

bpy.types.AssetShelf.filter_texture

bpy.types.AssetShelf.filter_volume

bpy.types.AssetShelf.filter_work_space

bpy.types.AssetShelf.filter_world

bpy.types.Attribute.storage_type

bpy.types.BakeSettings.displacement_space

bpy.types.BakeSettings.type

bpy.types.BakeSettings.use_lores_mesh

bpy.types.BakeSettings.use_multires

bpy.types.BlExtDummyGroup.name

bpy.types.BlExtDummyGroup.show_tag

bpy.types.BlendData.colorspace

bpy.types.BlendData.pack_linked_ids_hierarchy

grease_pencils_v3 -> bpy.types.BlendData.annotations

bpy.types.Bone.bl_system_properties_get

bpy.types.BoneCollection.bl_system_properties_get

bpy.types.BrightContrastModifier.open_mask_input_panel

bpy.types.Brush.unprojected_size

curve -> bpy.types.Brush.curve_distance_falloff

curve -> bpy.types.Brush.curve_jitter

curve -> bpy.types.Brush.curve_size

curve -> bpy.types.Brush.curve_strength

vertex_tool -> bpy.types.Brush.curve_distance_falloff_preset

vertex_tool -> bpy.types.Brush.curves_sculpt_brush_type

vertex_tool -> bpy.types.Brush.gpencil_brush_type

vertex_tool -> bpy.types.Brush.gpencil_sculpt_brush_type

vertex_tool -> bpy.types.Brush.gpencil_vertex_brush_type

vertex_tool -> bpy.types.Brush.gpencil_weight_brush_type

vertex_tool -> bpy.types.Brush.image_brush_type

vertex_tool -> bpy.types.Brush.sculpt_brush_type

vertex_tool -> bpy.types.Brush.vertex_brush_type

vertex_tool -> bpy.types.Brush.weight_brush_type

bpy.types.BrushCapabilitiesSculpt.has_auto_smooth_pressure

bpy.types.BrushCapabilitiesSculpt.has_hardness_pressure

bpy.types.BrushCapabilitiesSculpt.has_size_pressure

use_render_procedural

bpy.types.Camera.composition_guide_color

bpy.types.ColorBalanceModifier.open_mask_input_panel

bpy.types.ColorManagedDisplaySettings.emulation

use_hdr_view -> bpy.types.ColorManagedViewSettings.is_hdr

use_hdr_view -> bpy.types.ColorManagedViewSettings.support_emulation

highlights_saturation

use_straight_alpha_output

edge_kernel_tolerance

bpy.types.CompositorNodeOutputFile.active_item_index

base_path -> bpy.types.CompositorNodeOutputFile.directory

base_path -> bpy.types.CompositorNodeOutputFile.file_name

file_slots -> bpy.types.CompositorNodeOutputFile.file_output_items

bpy.types.CurvesModifier.open_mask_input_panel

use_adaptive_subdivision

bpy.types.CyclesRenderLayerSettings.pass_render_time

bpy.types.CyclesRenderLayerSettings.use_pass_volume_majorant

bpy.types.CyclesRenderLayerSettings.use_pass_volume_scatter

bpy.types.CyclesRenderLayerSettings.use_pass_volume_transmit

bpy.types.CyclesRenderSettings.volume_biased

bpy.types.EditBone.bl_system_properties_get

experimental_filter_scene -> bpy.types.FileAssetSelectIDFilter.experimental_filter_annotations

experimental_filter_scene -> bpy.types.FileAssetSelectIDFilter.filter_scene

bpy.types.FileSelectIDFilter.filter_annotations

bpy.types.GPENCIL_UL_annotation_layer.draw_item (self, _context, layout, _data, item, _icon, _active_data, _active_propname, _index), was (self, _context, layout, _data, item, icon, _active_data, _active_propname, _index)

bpy.types.GeometryNodeTree.show_modifier_manage_panel

bpy.types.GeometryNodeViewer.active_index

bpy.types.GeometryNodeViewer.active_item

bpy.types.GeometryNodeViewer.viewer_items

bpy.types.GizmoGroupProperties.bl_system_properties_get

bpy.types.GizmoProperties.bl_system_properties_get

bpy.types.GreasePencil.after_color

bpy.types.GreasePencil.attributes

bpy.types.GreasePencil.before_color

bpy.types.GreasePencil.color_attributes

bpy.types.GreasePencil.ghost_after_range

bpy.types.GreasePencil.ghost_before_range

bpy.types.GreasePencil.layer_groups

bpy.types.GreasePencil.materials

bpy.types.GreasePencil.onion_factor

bpy.types.GreasePencil.onion_keyframe_type

bpy.types.GreasePencil.onion_mode

bpy.types.GreasePencil.stroke_depth_order

bpy.types.GreasePencil.use_autolock_layers

bpy.types.GreasePencil.use_ghost_custom_colors

bpy.types.GreasePencil.use_onion_fade

bpy.types.GreasePencil.use_onion_loop

bpy.types.HueCorrectModifier.open_mask_input_panel

bpy.types.ID.bl_system_properties_get

bpy.types.ID.is_linked_packed

bpy.types.IDPropertyWrapPtr.bl_system_properties_get

bpy.types.ImageFormatSettings.media_type

bpy.types.ImageFormatSettings.use_exr_interleave

bpy.types.KeyConfigPreferences.bl_system_properties_get

bpy.types.Lattice.unit_test_compare

bpy.types.Library.archive_libraries

bpy.types.Library.archive_parent_library

bpy.types.Library.is_archive

bpy.types.Light.inline_shader_nodes

bpy.types.Material.inline_shader_nodes

bpy.types.Menu.path_menu (self, searchpaths, operator, props_default, prop_filepath, filter_ext, filter_path, display_name, add_operator, add_operator_props, translate), was (self, searchpaths, operator, props_default, prop_filepath, filter_ext, filter_path, display_name, add_operator, add_operator_props)

bpy.types.Mesh.radial_symmetry

bpy.types.MeshUVLoopLayer.pin_ensure

grease_pencil -> bpy.types.MovieClip.annotation

grease_pencil -> bpy.types.MovieTrackingTrack.annotation

bpy.types.Node.bl_system_properties_get

bpy.types.NodeSocket.bl_system_properties_get

bpy.types.NodeSocket.inferred_structure_type

grease_pencil -> bpy.types.NodeTree.annotation

bpy.types.NodeTreeInterfaceSocket.bl_system_properties_get

bpy.types.NodeTreeInterfaceSocket.optional_label

bpy.types.NodesModifier.bl_system_properties_get

bpy.types.NodesModifier.show_manage_panel

bpy.types.Object.hide_surface_pick

bpy.types.OperatorProperties.bl_system_properties_get

bpy.types.Paint.show_jitter_curve

bpy.types.Paint.show_size_curve

bpy.types.Paint.show_strength_curve

bpy.types.Paint.unified_paint_settings

bpy.types.PointLight.inline_shader_nodes

bpy.types.PoseBone.bl_system_properties_get

bpy.types.PoseBone.hide

bpy.types.PoseBone.select

bpy.types.PoseBone.use_transform_around_custom_shape

bpy.types.PoseBone.use_transform_at_custom_shape

use_sequencer_simplified_tweaking

use_attribute_storage_write

use_bundle_and_closure_nodes

use_socket_structure_type

write_large_blend_file_blocks -> bpy.types.PreferencesExperimental.no_data_block_packing

write_large_blend_file_blocks -> bpy.types.PreferencesExperimental.use_geometry_nodes_lists

write_large_blend_file_blocks -> bpy.types.PreferencesExperimental.write_legacy_blend_file_format

bpy.types.PreferencesInput.ndof_fly_speed_auto

bpy.types.PreferencesInput.xr_navigation

ndof_orbit_sensitivity -> bpy.types.PreferencesInput.ndof_rotation_sensitivity

ndof_orbit_sensitivity -> bpy.types.PreferencesInput.ndof_translation_sensitivity

use_select_pick_depth

bpy.types.PreferencesView.menu_close_leave

bpy.types.PreferencesView.preferences_display_type

bpy.types.PreferencesView.show_area_handle

bpy.types.PreferencesView.show_number_arrows

bpy.types.PreferencesView.use_reduce_motion

bpy.types.Property.deprecated_note

bpy.types.Property.deprecated_removal_version

bpy.types.Property.deprecated_version

bpy.types.Property.is_deprecated

bpy.types.PropertyGroup.bl_system_properties_get

bl_use_alembic_procedural

use_bake_selected_to_active

bpy.types.Scene.time_jump_delta

bpy.types.Scene.time_jump_unit

grease_pencil -> bpy.types.Scene.annotation

grease_pencil -> bpy.types.Scene.compositing_node_group

bpy.types.SceneGpencil.motion_blur_steps

bpy.types.SequencerTonemapModifierData.open_mask_input_panel

bpy.types.ShaderNodeTexSky.aerosol_density

bpy.types.SoundStrip.pitch_correction

bpy.types.SpaceClipEditor.overlay

bpy.types.SpaceDopeSheetEditor.show_region_footer

action -> bpy.types.SpaceDopeSheetEditor.overlays

bpy.types.SpaceGraphEditor.show_region_footer

bpy.types.SpaceImageEditor.show_sequencer_scene

grease_pencil -> bpy.types.SpaceImageEditor.annotation

bpy.types.SpaceNLA.show_region_footer

bpy.types.SpaceNodeEditor.show_region_asset_shelf

geometry_nodes_tool_tree -> bpy.types.SpaceNodeEditor.selected_node_group

geometry_nodes_type -> bpy.types.SpaceNodeEditor.node_tree_sub_type

bpy.types.SpacePreferences.show_region_ui

bpy.types.SpaceProperties.show_properties_strip

bpy.types.SpaceProperties.show_properties_strip_modifier

bpy.types.SpaceSequenceEditor.show_region_footer

grease_pencil -> bpy.types.SpaceSequenceEditor.annotation

bpy.types.SpotLight.inline_shader_nodes

bpy.types.SpreadsheetRowFilter.value_int3

bpy.types.Strip.bl_system_properties_get

bpy.types.StripModifier.enable

bpy.types.StripModifier.is_active

bpy.types.StripModifiers.active

bpy.types.StripsMeta.new_effect (name, type, channel, frame_start, length, input1, input2), was (name, type, channel, frame_start, frame_end, input1, input2)

bpy.types.StripsTopLevel.new_effect (name, type, channel, frame_start, length, input1, input2), was (name, type, channel, frame_start, frame_end, input1, input2)

bpy.types.SubsurfModifier.adaptive_object_edge_length

bpy.types.SubsurfModifier.adaptive_pixel_size

bpy.types.SubsurfModifier.adaptive_space

bpy.types.SubsurfModifier.use_adaptive_subdivision

bpy.types.SunLight.inline_shader_nodes

bpy.types.Theme.common

bpy.types.Theme.regions

handle_sel_auto_clamped

time_marker_line_selected

time_scrub_background

active_channels_group

keyframe_breakdown_selected

keyframe_extreme_selected

keyframe_generated_selected

keyframe_jitter_selected

keyframe_movehold_selected

time_marker_line_selected

time_scrub_background

active_channels_group

handle_sel_auto_clamped

time_marker_line_selected

time_scrub_background

handle_sel_auto_clamped

time_marker_line_selected

time_scrub_background

bpy.types.ThemeNodeEditor.node_outline

keyframe_breakdown_selected

keyframe_generated_selected

keyframe_movehold_selected

time_marker_line_selected

time_scrub_background

bpy.types.ThemeUserInterface.axis_w

bpy.types.ThemeUserInterface.panel_active

bpy.types.ThemeUserInterface.panel_back

bpy.types.ThemeUserInterface.panel_header

bpy.types.ThemeUserInterface.panel_outline

bpy.types.ThemeUserInterface.panel_sub_back

bpy.types.ThemeUserInterface.panel_text

bpy.types.ThemeUserInterface.panel_title

bpy.types.ThemeUserInterface.wcol_curve

handle_align -> bpy.types.ThemeView3D.bevel

handle_align -> bpy.types.ThemeView3D.crease

handle_align -> bpy.types.ThemeView3D.seam

handle_align -> bpy.types.ThemeView3D.sharp

paint_curve_handle -> bpy.types.ThemeView3D.freestyle

bpy.types.ThemeWidgetColors.outline_sel

bpy.types.TimelineMarker.bl_system_properties_get

bpy.types.ToolSettings.anim_fix_to_cam_use_loc

bpy.types.ToolSettings.anim_fix_to_cam_use_rot

bpy.types.ToolSettings.anim_fix_to_cam_use_scale

bpy.types.ToolSettings.anim_mirror_bone

bpy.types.ToolSettings.use_uv_custom_region

bpy.types.ToolSettings.use_uv_select_island

unified_paint_settings -> bpy.types.ToolSettings.anim_mirror_object

unified_paint_settings -> bpy.types.ToolSettings.anim_relative_object

bpy.types.UILayout.template_shape_key_tree

bpy.types.UILayout.template_strip_modifiers

template_cache_file_procedural -> bpy.types.UILayout.template_matrix

bpy.types.UILayout.prop_search (data, property, search_data, search_property, text, text_ctxt, translate, icon, results_are_suggestions, item_search_property), was (data, property, search_data, search_property, text, text_ctxt, translate, icon, results_are_suggestions)

bpy.types.UILayout.template_curve_mapping (data, property, type, levels, brush, use_negative_slope, show_tone, show_presets), was (data, property, type, levels, brush, use_negative_slope, show_tone)

bpy.types.UILayout.template_modifier_asset_menu_items (catalog_path, skip_essentials), was (catalog_path)

bpy.types.UILayout.template_node_asset_menu_items (catalog_path, operator), was (catalog_path)

bpy.types.UIList.bl_system_properties_get

bpy.types.UnifiedPaintSettings.unprojected_size

curve_preset -> bpy.types.UvSculpt.curve_distance_falloff_preset

strength_curve -> bpy.types.UvSculpt.curve_distance_falloff

bpy.types.View3DShading.bl_system_properties_get

bpy.types.ViewLayer.bl_system_properties_get

bpy.types.ViewLayerEEVEE.ambient_occlusion_distance

bpy.types.WhiteBalanceModifier.open_mask_input_panel

bpy.types.Window.support_hdr_color

bpy.types.WorkSpace.sequencer_scene

bpy.types.WorkSpace.use_scene_time_sync

bpy.types.World.inline_shader_nodes

bpy.types.XrSessionSettings.fly_speed

---

## AOV(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AOV.html

**Contents:**
- AOV(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Is the name of the AOV conflicting

boolean, default False

string, default “”, (never None)

enum in ['COLOR', 'VALUE'], default 'COLOR'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AOVs(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AOVs.html

**Contents:**
- AOVs(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

aov (AOV, (never None)) – AOV to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Action(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Action.html

**Contents:**
- Action(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

A collection of F-Curves for animation

The combined frame range of all F-Curves within this action

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0), (readonly)

The end frame of the manually set intended playback range

float in [-1.04857e+06, 1.04857e+06], default 0.0

The intended playback frame range of this action, using the manually set range if available, or the combined frame range of all F-Curves within this action if not (assigning sets the manual frame range)

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

The start frame of the manually set intended playback range

float in [-1.04857e+06, 1.04857e+06], default 0.0

Return whether this is a layered Action. An empty Action is considered as both a ‘legacy’ and a ‘layered’ Action.

boolean, default False, (readonly)

Return whether this is a legacy Action. Legacy Actions have no layers or slots. An empty Action is considered as both a ‘legacy’ and a ‘layered’ Action. Since Blender 4.4 actions are automatically updated to layered actions, and thus this will only return True when the action is empty

boolean, default False, (readonly)

False when there is any Layer, Slot, or legacy F-Curve

boolean, default False, (readonly)

The list of layers that make up this Action

ActionLayers bpy_prop_collection of ActionLayer, (readonly)

Markers specific to this action, for labeling poses

ActionPoseMarkers bpy_prop_collection of TimelineMarker, (readonly)

The list of slots in this Action

ActionSlots bpy_prop_collection of ActionSlot, (readonly)

The action is intended to be used as a cycle looping over its manually set playback frame range (enabling this does not automatically make it loop)

boolean, default False

Manually specify the intended playback frame range for the action (this range is used by some tools, but does not affect animation evaluation)

boolean, default False

Deselects all keys of the Action. The selection status of F-Curves is unchanged.

Ensure that an F-Curve exists, with the given data path and array index, for the given data-block. This action must already be assigned to the data-block. This function will also create the layer, keyframe strip, and action slot if necessary, and take care of assigning the action slot too

datablock (ID, (never None)) – The data-block animated by this action, for which to ensure the F-Curve exists. This action must already be assigned to the data-block

data_path (string, (never None)) – Data Path, F-Curve data path

index (int in [0, inf], (optional)) – Index, Array index

group_name (string, (optional, never None)) – Group Name, Name of the group for this F-Curve, if any. If the F-Curve already exists, this parameter is ignored

The found or created F-Curve

Flip the action around the X axis using a pose

object (Object, (never None)) – The reference armature object to use when flipping

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

bpy.context.active_action

bpy.context.selected_editable_actions

bpy.context.selected_visible_actions

ActionConstraint.action

AnimData.action_tweak_storage

BlendDataActions.remove

GLTF2_filter_action.action

Pose.apply_pose_from_action

Pose.blend_pose_from_action

WindowManager.poselib_previous_action

---

## ASSETBROWSER_UL_metadata_tags(UIList)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ASSETBROWSER_UL_metadata_tags.html

**Contents:**
- ASSETBROWSER_UL_metadata_tags(UIList)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, UIList

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

UIList.use_filter_show

UIList.use_filter_invert

UIList.use_filter_sort_alpha

UIList.use_filter_sort_reverse

UIList.use_filter_sort_lock

UIList.bitflag_filter_item

UIList.bitflag_item_never_show

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

UIList.bl_system_properties_get

UIList.bl_rna_get_subclass

UIList.bl_rna_get_subclass_py

---

## ActionChannelbag(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionChannelbag.html

**Contents:**
- ActionChannelbag(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of animation channels, typically associated with an action slot

The individual F-Curves that animate the slot

ActionChannelbagFCurves bpy_prop_collection of FCurve, (readonly)

Groupings of F-Curves for display purposes, in e.g. the dopesheet and graph editor

ActionChannelbagGroups bpy_prop_collection of ActionGroup, (readonly)

The Slot that the Channelbag’s animation data is for

ActionSlot, (readonly)

int in [-inf, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionChannelbags.new

ActionChannelbags.remove

ActionKeyframeStrip.channelbag

ActionKeyframeStrip.channelbags

---

## ActionChannelbagFCurves(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionChannelbagFCurves.html

**Contents:**
- ActionChannelbagFCurves(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of F-Curves for a specific action slot, on a specific strip

Add an F-Curve to the channelbag

data_path (string, (never None)) – Data Path, F-Curve data path to use

index (int in [0, inf], (optional)) – Index, Array index

group_name (string, (optional, never None)) – Group Name, Name of the Group for this F-Curve, will be created if it does not exist yet

Newly created F-Curve

Copy an F-Curve into the channelbag. The original F-Curve is unchanged

source (FCurve) – Source F-Curve, The F-Curve to copy

data_path (string, (optional, never None)) – Data Path, F-Curve data path to use. If not provided, this will use the same data path as the given F-Curve

Newly created F-Curve

Returns the F-Curve if it already exists, and creates it if necessary

data_path (string, (never None)) – Data Path, F-Curve data path to use

index (int in [0, inf], (optional)) – Index, Array index

group_name (string, (optional, never None)) – Group Name, Name of the Group for this F-Curve, will be created if it does not exist yet. This parameter is ignored if the F-Curve already exists

Found or newly created F-Curve

Find an F-Curve. Note that this function performs a linear scan of all F-Curves in the channelbag.

data_path (string, (never None)) – Data Path, F-Curve data path

index (int in [0, inf], (optional)) – Index, Array index

The found F-Curve, or None if it does not exist

fcurve (FCurve, (never None)) – F-Curve to remove

Remove all F-Curves from this channelbag

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionChannelbag.fcurves

---

## ActionChannelbagGroups(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionChannelbagGroups.html

**Contents:**
- ActionChannelbagGroups(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of f-curve groups

Create a new action group and add it to the action

name (string, (never None)) – New name for the action group

Newly created action group

action_group (ActionGroup, (never None)) – Action group to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionChannelbag.groups

---

## ActionChannelbags(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionChannelbags.html

**Contents:**
- ActionChannelbags(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

For each action slot, a list of animation channels that are meant for that slot

Add a new channelbag to the strip, to contain animation channels for a specific slot

slot (ActionSlot) – Action Slot, The slot that should be animated by this channelbag

Newly created channelbag

Remove the channelbag from the strip

channelbag (ActionChannelbag) – The channelbag to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionKeyframeStrip.channelbags

---

## ActionConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionConstraint.html

**Contents:**
- ActionConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Map an action to the transform axes of a bone

The constraining action

The slot identifies which sub-set of the Action is considered to be for this strip, and its name is used to find the right slot when assigning another Action

A number that identifies which sub-set of the Action is considered to be for this Action Constraint

int in [-inf, inf], default 0

The list of action slots suitable for this NLA strip

bpy_prop_collection of ActionSlot, (readonly)

Interpolates between Action Start and End frames

float in [0, 1], default 0.0

Last frame of the Action to use

int in [-1048574, 1048574], default 0

First frame of the Action to use

int in [-1048574, 1048574], default 0

The identifier of the most recently assigned action slot. The slot identifies which sub-set of the Action is considered to be for this constraint, and its identifier is used to find the right slot when assigning an Action.

string, default “”, (never None)

Maximum value for target channel range

float in [-1000, 1000], default 0.0

Minimum value for target channel range

float in [-1000, 1000], default 0.0

Specify how existing transformations and the action channels are combined

REPLACE Replace – Replace the original transformation with the action channels.

BEFORE_FULL Before Original (Full) – Apply the action channels before the original transformation, as if applied to an imaginary parent in Full Inherit Scale mode. Will create shear when combining rotation and non-uniform scale..

BEFORE Before Original (Aligned) – Apply the action channels before the original transformation, as if applied to an imaginary parent in Aligned Inherit Scale mode. This effectively uses Full for location and Split Channels for rotation and scale..

BEFORE_SPLIT Before Original (Split Channels) – Apply the action channels before the original transformation, handling location, rotation and scale separately.

AFTER_FULL After Original (Full) – Apply the action channels after the original transformation, as if applied to an imaginary child in Full Inherit Scale mode. Will create shear when combining rotation and non-uniform scale..

AFTER After Original (Aligned) – Apply the action channels after the original transformation, as if applied to an imaginary child in Aligned Inherit Scale mode. This effectively uses Full for location and Split Channels for rotation and scale..

AFTER_SPLIT After Original (Split Channels) – Apply the action channels after the original transformation, handling location, rotation and scale separately.

enum in ['REPLACE', 'BEFORE_FULL', 'BEFORE', 'BEFORE_SPLIT', 'AFTER_FULL', 'AFTER', 'AFTER_SPLIT'], default 'AFTER_FULL'

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Transformation channel from the target that is used to key the Action

enum in ['LOCATION_X', 'LOCATION_Y', 'LOCATION_Z', 'ROTATION_X', 'ROTATION_Y', 'ROTATION_Z', 'SCALE_X', 'SCALE_Y', 'SCALE_Z'], default 'ROTATION_X'

Bones only: apply the object’s transformation channels of the action to the constrained bone, instead of bone’s channels

boolean, default False

Interpolate between Action Start and End frames, with the Evaluation Time slider instead of the Target object/bone

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## ActionGroup(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionGroup.html

**Contents:**
- ActionGroup(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

F-Curves in this group

bpy_prop_collection of FCurve, (readonly)

Custom color set to use

enum in Color Sets Items, default 'DEFAULT'

Copy of the colors associated with the group’s color set

ThemeBoneColorSet, (readonly, never None)

Color set is user-defined instead of a fixed theme color set

boolean, default False, (readonly)

Action group is locked

boolean, default False

Action group is muted

boolean, default False

string, default “”, (never None)

Action group is selected

boolean, default False

Action group is expanded except in graph editor

boolean, default False

Action group is expanded in graph editor

boolean, default False

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionChannelbag.groups

ActionChannelbagGroups.new

ActionChannelbagGroups.remove

---

## ActionLayer(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionLayer.html

**Contents:**
- ActionLayer(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

string, default “”, (never None)

The list of strips that are on this animation layer

ActionStrips bpy_prop_collection of ActionStrip, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ActionKeyframeStrip(ActionStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionKeyframeStrip.html

**Contents:**
- ActionKeyframeStrip(ActionStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ActionStrip

Strip with a set of F-Curves for each action slot

ActionChannelbags bpy_prop_collection of ActionChannelbag, (readonly)

Find the ActionChannelbag for a specific Slot

slot (ActionSlot) – Slot, The slot for which to find the channelbag

ensure (boolean, (optional)) – Create if necessary, Ensure the channelbag exists for this slot, creating it if necessary

slot (ActionSlot) – Slot, The slot that identifies which ‘thing’ should be keyed

data_path (string, (never None)) – Data Path, F-Curve data path

array_index (int in [-inf, inf]) – Array Index, Index of the animated array element, or -1 if the property is not an array

value (float in [-inf, inf]) – Value to key, Value of the animated property

time (float in [-inf, inf]) – Time of the key, Time, in frames, of the key

Success, Whether the key was successfully inserted

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionStrip.bl_rna_get_subclass

ActionStrip.bl_rna_get_subclass_py

---

## ActionLayers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionLayers.html

**Contents:**
- ActionLayers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of animation layers

Add a layer to the Animation. Currently an Animation can only have at most one layer.

name (string, (never None)) – Name, Name of the layer, will be made unique within the Action

Newly created animation layer

Remove the layer from the animation

anim_layer (ActionLayer) – Animation Layer, The layer to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ActionPoseMarkers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionPoseMarkers.html

**Contents:**
- ActionPoseMarkers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of timeline markers

Active pose marker for this action

Index of active pose marker

int in [0, inf], default 0

Add a pose marker to the action

name (string, (never None)) – New name for the marker (not unique)

Remove a timeline marker

marker (TimelineMarker, (never None)) – Timeline marker to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ActionSlot(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionSlot.html

**Contents:**
- ActionSlot(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Identifier for a set of channels in this Action, that can be used by a data-block to specify what it gets animated by

Whether this is the active slot, can be set by assigning to action.slots.active

boolean, default False, (readonly)

Number specific to this Slot, unique within the Action. This is used, for example, on a ActionKeyframeStrip to look up the ActionChannelbag for this Slot

int in [-inf, inf], default 0, (readonly)

Used when connecting an Action to a data-block, to find the correct slot handle. This is the display name, prefixed by two characters determined by the slot’s ID type

string, default “”, (never None)

Name of the slot, for display in the user interface. This name combined with the slot’s data-block type is unique within its Action

string, default “”, (never None)

Selection state of the slot

boolean, default False

Expanded state of the slot

boolean, default False

Type of data-block that this slot is intended to animate; can be set when ‘UNSPECIFIED’ but is otherwise read-only

CACHEFILE Cache File.

COLLECTION Collection.

GREASEPENCIL Grease Pencil.

GREASEPENCIL_V3 Grease Pencil v3.

LIGHT_PROBE Light Probe.

LINESTYLE Line Style.

MOVIECLIP Movie Clip.

PAINTCURVE Paint Curve.

POINTCLOUD Point Cloud.

WINDOWMANAGER Window Manager.

UNSPECIFIED Unspecified – Not yet specified. When this slot is first assigned to a data-block, this will be set to the type of that data-block.

enum in ['ACTION', 'ARMATURE', 'BRUSH', 'CACHEFILE', 'CAMERA', 'COLLECTION', 'CURVE', 'CURVES', 'FONT', 'GREASEPENCIL', 'GREASEPENCIL_V3', 'IMAGE', 'KEY', 'LATTICE', 'LIBRARY', 'LIGHT', 'LIGHT_PROBE', 'LINESTYLE', 'MASK', 'MATERIAL', 'MESH', 'META', 'MOVIECLIP', 'NODETREE', 'OBJECT', 'PAINTCURVE', 'PALETTE', 'PARTICLE', 'POINTCLOUD', 'SCENE', 'SCREEN', 'SOUND', 'SPEAKER', 'TEXT', 'TEXTURE', 'VOLUME', 'WINDOWMANAGER', 'WORKSPACE', 'WORLD', 'UNSPECIFIED'], default 'UNSPECIFIED'

int in [-inf, inf], default 0, (readonly)

Return the data-blocks that are animated by this slot of this action

bpy_prop_collection of ID

Duplicate this slot, including all the animation data associated with it

Duplicated Slot, The slot created by duplicating this one

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ActionChannelbag.slot

ActionChannelbags.new

ActionConstraint.action_slot

ActionConstraint.action_suitable_slots

ActionKeyframeStrip.channelbag

ActionKeyframeStrip.key_insert

AnimData.action_suitable_slots

NlaStrip.action_suitable_slots

---

## ActionSlots(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionSlots.html

**Contents:**
- ActionSlots(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of action slots

Active slot for this action

Add a slot to the Action

id_type (enum in Id Type Items) – Data-block Type, The data-block type that the slot is intended for. This is combined with the slot name to create the slot’s unique identifier, and is also used to limit (on a best-effort basis) which data-blocks the slot can be assigned to.

name (string, (never None)) – Name, Name of the slot. This will be made unique within the Action among slots of the same type

Newly created action slot

Remove the slot from the Action, including all animation that is associated with that slot

action_slot (ActionSlot) – Action Slot, The slot to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ActionStrip(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionStrip.html

**Contents:**
- ActionStrip(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

subclasses — ActionKeyframeStrip

KEYFRAME Keyframe – Strip with a set of F-Curves for each action slot.

enum in ['KEYFRAME'], default 'KEYFRAME', (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ActionStrips(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ActionStrips.html

**Contents:**
- ActionStrips(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of animation strips

Add a new strip to the layer. Currently a layer can only have one strip, with infinite boundaries.

type (enum in ['KEYFRAME'], (optional)) – Type, The type of strip to create KEYFRAME Keyframe – Strip containing keyframes on F-Curves.

Type, The type of strip to create

KEYFRAME Keyframe – Strip containing keyframes on F-Curves.

Newly created animation strip

Remove the strip from the animation layer

anim_strip (ActionStrip) – Animation Strip, The strip to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AddStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AddStrip.html

**Contents:**
- AddStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

First input for the effect strip

Second input for the effect strip

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## Addon(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Addon.html

**Contents:**
- Addon(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Python add-ons to be loaded automatically

string, default “”, (never None)

AddonPreferences, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AddonPreferences(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AddonPreferences.html

**Contents:**
- AddonPreferences(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

string, default “”, (never None)

DEBUG ONLY. Internal access to runtime-defined RNA data storage, intended solely for testing and debugging purposes. Do not access it in regular scripting work, and in particular, do not assume that it contains writable data

do_create (boolean, (optional)) – Ensure that system properties are created if they do not exist yet

The system properties root container, or None if there are no system properties stored in this data yet, and its creation was not requested

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

**Examples:**

Example 1 (swift):
```swift
bl_info = {
    "name": "Example Add-on Preferences",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "SpaceBar Search -> Add-on Preferences Example",
    "description": "Example Add-on",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}


import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty


class ExampleAddonPreferences(AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a Python package.
    bl_idname = __name__

    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    number: IntProperty(
        name="Example Number",
        default=4,
    )
    boolean: BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "filepath")
        layout.prop(self, "number")
        layout.prop(self, "boolean")


class OBJECT_OT_addon_prefs_example(Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = "Path: {:s}, Number: {:d}, Boolean {!r}".format(
            addon_prefs.filepath, addon_prefs.number, addon_prefs.boolean,
        )
        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}


# Registration
def register():
    bpy.utils.register_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.register_class(ExampleAddonPreferences)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_addon_prefs_example)
    bpy.utils.unregister_class(ExampleAddonPreferences)
```

---

## Addons(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Addons.html

**Contents:**
- Addons(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of add-ons

addon (Addon, (never None)) – Add-on to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AdjustmentStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AdjustmentStrip.html

**Contents:**
- AdjustmentStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

Sequence strip to perform filter adjustments to layers below

Animation end offset (trim end)

int in [0, inf], default 0

Animation start offset (trim start)

int in [0, inf], default 0

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## AlphaOverStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AlphaOverStrip.html

**Contents:**
- AlphaOverStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

First input for the effect strip

Second input for the effect strip

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## AlphaUnderStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AlphaUnderStrip.html

**Contents:**
- AlphaUnderStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

First input for the effect strip

Second input for the effect strip

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## AnimViz(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnimViz.html

**Contents:**
- AnimViz(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Settings for the visualization of motion

Motion Path settings for visualization

AnimVizMotionPaths, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Object.animation_visualization

Pose.animation_visualization

---

## AnimDataDrivers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnimDataDrivers.html

**Contents:**
- AnimDataDrivers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Driver F-Curves

data_path (string, (never None)) – Data Path, F-Curve data path to use

index (int in [0, inf], (optional)) – Index, Array index

Add a new driver given an existing one

src_driver (FCurve, (optional)) – Existing Driver F-Curve to use as template for a new one

Find a driver F-Curve. Note that this function performs a linear scan of all driver F-Curves.

data_path (string, (never None)) – Data Path, F-Curve data path

index (int in [0, inf], (optional)) – Index, Array index

The found F-Curve, or None if it doesn’t exist

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AnimData(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnimData.html

**Contents:**
- AnimData(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Animation data for data-block

Active Action for this data-block

Method used for combining Active Action’s result with result of NLA stack

REPLACE Replace – The strip values replace the accumulated results by amount specified by influence.

COMBINE Combine – The strip values are combined with accumulated results by appropriately using addition, multiplication, or quaternion math, based on channel type.

ADD Add – Weighted result of strip is added to the accumulated results.

SUBTRACT Subtract – Weighted result of strip is removed from the accumulated results.

MULTIPLY Multiply – Weighted result of strip is multiplied with the accumulated results.

enum in ['REPLACE', 'COMBINE', 'ADD', 'SUBTRACT', 'MULTIPLY'], default 'REPLACE'

Action to take for gaps past the Active Action’s range (when evaluating with NLA)

NOTHING Nothing – Strip has no influence past its extents.

HOLD Hold – Hold the first frame if no previous strips in track, and always hold last frame.

HOLD_FORWARD Hold Forward – Only hold last frame.

enum in ['NOTHING', 'HOLD', 'HOLD_FORWARD'], default 'HOLD'

Amount the Active Action contributes to the result of the NLA stack

float in [0, 1], default 1.0

The slot identifies which sub-set of the Action is considered to be for this data-block, and its name is used to find the right slot when assigning an Action

A number that identifies which sub-set of the Action is considered to be for this data-block

int in [-inf, inf], default 0

Storage to temporarily hold the main action slot while in tweak mode

int in [-inf, inf], default 0

The list of slots in this animation data-block

bpy_prop_collection of ActionSlot, (readonly)

Storage to temporarily hold the main action while in tweak mode

The Drivers/Expressions for this data-block

AnimDataDrivers bpy_prop_collection of FCurve, (readonly)

The identifier of the most recently assigned action slot. The slot identifies which sub-set of the Action is considered to be for this data-block, and its identifier is used to find the right slot when assigning an Action.

string, default “”, (never None)

NLA Tracks (i.e. Animation Layers)

NlaTracks bpy_prop_collection of NlaTrack, (readonly)

NLA stack is evaluated when evaluating this block

boolean, default False

boolean, default False

Whether to enable or disable tweak mode in NLA

boolean, default False

Convert a time value from the local time of the tweaked strip to scene time, exactly as done by built-in key editing tools. Returns the input time unchanged if not tweaking.

frame (float in [-1.04857e+06, 1.04857e+06]) – Input time

invert (boolean, (optional)) – Invert, Convert scene time to action time

float in [-1.04857e+06, 1.04857e+06]

Rename the property paths in the animation system, since properties are animated via string paths, it’s needed to keep them valid after properties has been renamed

prefix (string, (optional, never None)) – Prefix, Name prefix

old_name (string, (optional, never None)) – Old Name, Old name

new_name (string, (optional, never None)) – New Name, New name

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Annotation.animation_data

Armature.animation_data

CacheFile.animation_data

Camera.animation_data

Curves.animation_data

FreestyleLineStyle.animation_data

GreasePencil.animation_data

ID.animation_data_create

Lattice.animation_data

LightProbe.animation_data

Material.animation_data

MetaBall.animation_data

MovieClip.animation_data

NodeTree.animation_data

Object.animation_data

ParticleSettings.animation_data

PointCloud.animation_data

Speaker.animation_data

Texture.animation_data

Volume.animation_data

---

## AnimVizMotionPaths(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnimVizMotionPaths.html

**Contents:**
- AnimVizMotionPaths(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Motion Path settings for animation visualization

When calculating Bone Paths, use Head or Tips

enum in Motionpath Bake Location Items, default 'TAILS'

Number of frames to show after the current frame (only for ‘Around Frame’ Onion-skinning method)

int in [1, 524287], default 0

Number of frames to show before the current frame (only for ‘Around Frame’ Onion-skinning method)

int in [1, 524287], default 0

End frame of range of paths to display/calculate (not for ‘Around Frame’ Onion-skinning method)

int in [-inf, inf], default 0

Starting frame of range of paths to display/calculate (not for ‘Around Frame’ Onion-skinning method)

int in [-inf, inf], default 0

Number of frames between paths shown (not for ‘On Keyframes’ Onion-skinning method)

int in [1, 100], default 0

Are there any bone paths that will need updating (read-only)

boolean, default False, (readonly)

Type of range to calculate for Motion Paths

enum in Motionpath Range Items, default 'SCENE'

Show frame numbers on Motion Paths

boolean, default False

For bone motion paths, search whole Action for keyframes instead of in group with matching name only (is slower)

boolean, default False

Emphasize position of keyframes on Motion Paths

boolean, default False

Show frame numbers of Keyframes on Motion Paths

boolean, default False

Type of range to show for Motion Paths

enum in Motionpath Display Type Items, default 'RANGE'

Motion path points will be baked into the camera space of the active camera. This means they will only look right when looking through that camera. Switching cameras using markers is not supported.

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Annotation(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Annotation.html

**Contents:**
- Annotation(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Freehand annotation sketchbook

Animation data for this data-block

AnnotationLayers bpy_prop_collection of AnnotationLayer, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendData.annotations

BlendDataAnnotations.new

BlendDataAnnotations.remove

MovieTrackingTrack.annotation

SpaceImageEditor.annotation

SpaceSequenceEditor.annotation

---

## AnnotationFrame(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationFrame.html

**Contents:**
- AnnotationFrame(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of related sketches on a particular frame

The frame on which this sketch appears

int in [-1048574, 1048574], default 0

Frame is selected for editing in the Dope Sheet

boolean, default False

Freehand curves defining the sketch on this frame

bpy_prop_collection of AnnotationStroke, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AnnotationFrames.copy

AnnotationFrames.copy

AnnotationFrames.remove

AnnotationLayer.active_frame

AnnotationLayer.frames

---

## AnnotationFrames(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationFrames.html

**Contents:**
- AnnotationFrames(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of annotation frames

Add a new annotation frame

frame_number (int in [-1048574, 1048574]) – Frame Number, The frame on which this sketch appears

active (boolean, (optional)) – Active

The newly created frame

Remove an annotation frame

frame (AnnotationFrame, (never None)) – Frame, The frame to remove

Copy an annotation frame

source (AnnotationFrame, (never None)) – Source, The source frame

The newly copied frame

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AnnotationLayer.frames

---

## AnnotationLayer(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationLayer.html

**Contents:**
- AnnotationLayer(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of related sketches

Frame currently being displayed for this layer

AnnotationFrame, (readonly)

Set annotation Visibility

boolean, default False

Base color for ghosts after the active frame

mathutils.Color of 3 items in [0, 1], default (0.25, 0.1, 1.0)

Maximum number of frames to show after current frame

int in [-1, 120], default 0

Base color for ghosts before the active frame

mathutils.Color of 3 items in [0, 1], default (0.302, 0.851, 0.302)

Maximum number of frames to show before current frame

int in [-1, 120], default 0

Use custom colors for onion skinning instead of the theme

boolean, default False

Annotation Layer Opacity

float in [0, 1], default 0.0

Color for all strokes in this layer

mathutils.Color of 3 items in [0, 1], default (0.0, 0.0, 0.0)

Sketches for this layer on different frames

AnnotationFrames bpy_prop_collection of AnnotationFrame, (readonly)

string, default “”, (never None)

This is a special ruler layer

boolean, default False, (readonly)

Protect layer from further editing and/or frame changes

boolean, default False

Lock current frame displayed by layer

boolean, default False

Layer is selected for editing in the Dope Sheet

boolean, default False

Make the layer display in front of objects

boolean, default False

Thickness of annotation strokes

int in [1, 10], default 0

Display annotation onion skins before and after the current frame

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AnnotationLayers.remove

---

## AnnotationLayers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationLayers.html

**Contents:**
- AnnotationLayers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of annotation layers

Index of active annotation layer

int in [0, inf], default 0

Note/Layer to add annotation strokes to

enum in ['DEFAULT'], default 'DEFAULT'

Add a new annotation layer

name (string, (never None)) – Name, Name of the layer

set_active (boolean, (optional)) – Set Active, Set the newly created layer to the active layer

The newly created layer

Remove a annotation layer

layer (AnnotationLayer, (never None)) – The layer to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AnnotationStroke(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationStroke.html

**Contents:**
- AnnotationStroke(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Freehand curve defining part of a sketch

bpy_prop_collection of AnnotationStrokePoint, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AnnotationFrame.strokes

---

## AnnotationStrokePoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnnotationStrokePoint.html

**Contents:**
- AnnotationStrokePoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Data point for freehand stroke curve

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AnnotationStroke.points

---

## AnyType(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AnyType.html

**Contents:**
- AnyType(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

RNA type used for pointers to any possible data

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoneCollection.assign

BoneCollection.unassign

FCurve.update_autoflags

Gizmo.target_set_prop

KeyingSetInfo.generate

UILayout.context_pointer_set

UILayout.enum_item_description

UILayout.enum_item_icon

UILayout.enum_item_name

UILayout.prop_decorator

UILayout.prop_menu_enum

UILayout.prop_tabs_enum

UILayout.prop_tabs_enum

UILayout.prop_with_menu

UILayout.prop_with_popover

UILayout.template_ID_preview

UILayout.template_ID_tabs

UILayout.template_any_ID

UILayout.template_cache_file

UILayout.template_cache_file_layers

UILayout.template_cache_file_time_settings

UILayout.template_cache_file_velocity

UILayout.template_color_picker

UILayout.template_color_ramp

UILayout.template_colormanaged_view_settings

UILayout.template_colorspace_settings

UILayout.template_component_menu

UILayout.template_curve_mapping

UILayout.template_curveprofile

UILayout.template_greasepencil_color

UILayout.template_histogram

UILayout.template_icon_view

UILayout.template_image

UILayout.template_layers

UILayout.template_layers

UILayout.template_light_linking_collection

UILayout.template_list

UILayout.template_list

UILayout.template_marker

UILayout.template_matrix

UILayout.template_movieclip

UILayout.template_movieclip_information

UILayout.template_palette

UILayout.template_path_builder

UILayout.template_search

UILayout.template_search

UILayout.template_search_preview

UILayout.template_search_preview

UILayout.template_track

UILayout.template_vectorscope

UILayout.template_waveform

---

## Area(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Area.html

**Contents:**
- Area(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Area in a subdivided screen, containing an editor

int in [0, 32767], default 0, (readonly)

Regions this area is subdivided in

bpy_prop_collection of Region, (readonly)

Show menus in the header

boolean, default False

Spaces contained in this area, the first being the active space (NOTE: Useful for example to restore a previously used 3D view space in a certain area to get the old view orientation)

AreaSpaces bpy_prop_collection of Space, (readonly)

Current editor type for this area

enum in Space Type Items, default 'VIEW_3D'

Current editor type for this area

int in [0, 32767], default 0, (readonly)

The window relative vertical location of the area

int in [-inf, inf], default 0, (readonly)

The window relative horizontal location of the area

int in [-inf, inf], default 0, (readonly)

Set the header status text

text (string) – Text, New string for the header, None clears the text

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AreaLight(Light)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AreaLight.html

**Contents:**
- AreaLight(Light)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ID, Light

Directional area Light

Light energy emitted over the entire area of the light in all directions, in units of radiant power (W)

float in [-inf, inf], default 10.0

Shadow map clip start, below which objects will not generate shadows

float in [1e-06, inf], default 0.05

Blur shadow aliasing using Percentage Closer Filtering

float in [0, inf], default 1.0

Apply shadow tracing to each jittered sample to reduce under-sampling artifacts

float in [0, 100], default 10.0

Minimum size of a shadow map pixel. Higher values use less memory at the cost of shadow quality.

float in [0, inf], default 0.001

Light size for ray shadow sampling (Raytraced shadows)

float in [0, inf], default 0.0

Shape of the area Light

enum in ['SQUARE', 'RECTANGLE', 'DISK', 'ELLIPSE'], default 'SQUARE'

Size of the area of the area light, X direction size for rectangle shapes

float in [0, inf], default 0.25

Size of the area of the area light in the Y direction for rectangle shapes

float in [0, inf], default 0.25

How widely the emitted light fans out, as in the case of a gridded softbox

float in [0, 3.14159], default 3.14159

Limit the resolution at 1 unit from the light origin instead of relative to the shadowed pixel

boolean, default False

Enable jittered soft shadows to increase shadow precision (disabled in viewport unless enabled in the render settings). Has a high performance impact.

boolean, default False

Get the inlined shader nodes of this light. This preprocesses the node tree to remove nested groups, repeat zones and more.

The inlined shader nodes.

bpy.types.InlineShaderNodes

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

Light.use_temperature

Light.temperature_color

Light.specular_factor

Light.transmission_factor

Light.use_custom_distance

Light.cutoff_distance

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

Light.inline_shader_nodes

Light.bl_rna_get_subclass

Light.bl_rna_get_subclass_py

---

## AreaSpaces(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AreaSpaces.html

**Contents:**
- AreaSpaces(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Space currently being displayed in this area

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Armature(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Armature.html

**Contents:**
- Armature(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Armature data-block containing a hierarchy of bones, usually used for rigging characters

Animation data for this data-block

The position for the axes on the bone. Increasing the value moves it closer to the tip; decreasing moves it closer to the root.

float in [0, 1], default 0.0

ArmatureBones bpy_prop_collection of Bone, (readonly)

BoneCollections bpy_prop_collection of BoneCollection

List of all bone collections of the armature

bpy_prop_collection of BoneCollection, (readonly)

OCTAHEDRAL Octahedral – Display bones as octahedral shape (default).

STICK Stick – Display bones as simple 2D lines with dots.

BBONE B-Bone – Display bones as boxes, showing subdivision and B-Splines.

ENVELOPE Envelope – Display bones as extruded spheres, showing deformation influence volume.

WIRE Wire – Display bones as thin wires, showing subdivision and B-Splines.

enum in ['OCTAHEDRAL', 'STICK', 'BBONE', 'ENVELOPE', 'WIRE'], default 'OCTAHEDRAL'

ArmatureEditBones bpy_prop_collection of EditBone, (readonly)

True when used in editmode

boolean, default False, (readonly)

Show armature in binding pose or final posed state

POSE Pose Position – Show armature in posed state.

REST Rest Position – Show Armature in binding pose state (no posing possible).

enum in ['POSE', 'REST'], default 'POSE'

The start position of the relation lines from parent to child bones

TAIL Tail – Draw the relationship line from the parent tail to the child head.

HEAD Head – Draw the relationship line from the parent head to the child head.

enum in ['TAIL', 'HEAD'], default 'TAIL'

boolean, default False

boolean, default True

Display bones with their custom shapes

boolean, default True

boolean, default False

Apply changes to matching bone on opposite side of X-Axis

boolean, default False

Transform armature bones by a matrix

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf]) – Matrix

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendDataArmatures.new

BlendDataArmatures.remove

---

## ArmatureConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArmatureConstraint.html

**Contents:**
- ArmatureConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Applies transformations done by the Armature modifier

ArmatureConstraintTargets bpy_prop_collection of ConstraintTargetBone, (readonly)

Multiply weights by envelope for all bones, instead of acting like Vertex Group based blending. The specified weights are still used, and only the listed bones are considered.

boolean, default False

Use the current bone location for envelopes and choosing B-Bone segments instead of rest position

boolean, default False

Deform rotation interpolation with quaternions

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## ArmatureConstraintTargets(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArmatureConstraintTargets.html

**Contents:**
- ArmatureConstraintTargets(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of target bones and weights

Add a new target to the constraint

Delete target from the constraint

target (ConstraintTargetBone, (never None)) – Target to remove

Delete all targets from object

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ArmatureConstraint.targets

---

## ArmatureEditBones(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArmatureEditBones.html

**Contents:**
- ArmatureEditBones(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of armature edit bones

Armatures active edit bone

name (string, (never None)) – New name for the bone

Newly created edit bone

Remove an existing bone from the armature

bone (EditBone, (never None)) – EditBone to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ArmatureBones(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArmatureBones.html

**Contents:**
- ArmatureBones(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of armature bones

Armature’s active bone

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ArmatureModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArmatureModifier.html

**Contents:**
- ArmatureModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Armature deformation modifier

Invert vertex group influence

boolean, default False

Armature object to deform with

Bind Bone envelopes to armature modifier

boolean, default False

Deform rotation interpolation with quaternions

boolean, default False

Use same input as previous modifier, and mix results using overall vgroup

boolean, default False

Bind vertex groups to armature modifier

boolean, default True

Name of Vertex Group which determines influence of modifier per point

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## ArrayModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ArrayModifier.html

**Contents:**
- ArrayModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Array duplication modifier

Value for the distance between arrayed items

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 0.0, 0.0)

Number of duplicates to make

int in [1, inf], default 2

Curve object to fit array length to

Mesh object to use as an end cap

Length to fit array within

float in [0, inf], default 0.0

Array length calculation method

FIXED_COUNT Fixed Count – Duplicate the object a certain number of times.

FIT_LENGTH Fit Length – Duplicate the object as many times as fits in a certain length.

FIT_CURVE Fit Curve – Fit the duplicated objects to a curve.

enum in ['FIXED_COUNT', 'FIT_LENGTH', 'FIT_CURVE'], default 'FIXED_COUNT'

Limit below which to merge vertices

float in [0, inf], default 0.01

Use the location and rotation of another object to determine the distance and rotational change between arrayed items

Amount to offset array UVs on the U axis

float in [-1, 1], default 0.0

Amount to offset array UVs on the V axis

float in [-1, 1], default 0.0

The size of the geometry will determine the distance between arrayed items

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 0.0, 0.0)

Mesh object to use as a start cap

Add a constant offset

boolean, default False

Merge vertices in adjacent duplicates

boolean, default False

Merge vertices in first and last duplicates

boolean, default False

Add another object’s transformation to the total offset

boolean, default False

Add an offset relative to the object’s bounding box

boolean, default True

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## AssetLibraryCollection(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetLibraryCollection.html

**Contents:**
- AssetLibraryCollection(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of user asset libraries

Add a new Asset Library

name (string, (optional, never None)) – Name

directory (string, (optional, never None)) – Directory

Newly added asset library

Remove an Asset Library

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

PreferencesFilePaths.asset_libraries

---

## AssetLibraryReference(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetLibraryReference.html

**Contents:**
- AssetLibraryReference(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

Identifier to refer to the asset library

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AssetMetaData(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetMetaData.html

**Contents:**
- AssetMetaData(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Additional data stored for an asset data-block

Index of the tag set for editing

int in [-32768, 32767], default 0

Name of the creator of the asset

string, default “”, (never None)

Identifier for the asset’s catalog, used by Blender to look up the asset’s catalog path. Must be a UUID according to RFC4122.

string, default “”, (never None)

Simple name of the asset’s catalog, for debugging and data recovery purposes

string, default “”, (readonly, never None)

Copyright notice for this asset. An empty copyright notice does not necessarily indicate that this is copyright-free. Contact the author if any clarification is needed.

string, default “”, (never None)

A description of the asset to be displayed for the user

string, default “”, (never None)

The type of license this asset is distributed under. An empty license name does not necessarily indicate that this is free of licensing terms. Contact the author if any clarification is needed.

string, default “”, (never None)

Custom tags (name tokens) for the asset, used for filtering and general asset management

AssetTags bpy_prop_collection of AssetTag, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AssetRepresentation.metadata

FileSelectEntry.asset_data

---

## AssetShelf(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetShelf.html

**Contents:**
- AssetShelf(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

subclasses — IMAGE_AST_brush_paint, NODE_AST_compositor, VIEW3D_AST_brush_gpencil_paint, VIEW3D_AST_brush_gpencil_sculpt, VIEW3D_AST_brush_gpencil_vertex, VIEW3D_AST_brush_gpencil_weight, VIEW3D_AST_brush_sculpt, VIEW3D_AST_brush_sculpt_curves, VIEW3D_AST_brush_texture_paint, VIEW3D_AST_brush_vertex_paint, VIEW3D_AST_brush_weight_paint, VIEW3D_AST_pose_library

Regions for quick access to assets

Choose the asset library to display assets from

ALL All Libraries – Show assets from all of the listed asset libraries.

LOCAL Current File – Show the assets currently available in this Blender session.

ESSENTIALS Essentials – Show the basic building blocks and utilities coming with Blender.

CUSTOM Custom – Show assets from the asset libraries configured in the Preferences.

enum in ['ALL', 'LOCAL', 'ESSENTIALS', 'CUSTOM'], default 'ALL'

Operator to call when activating an item with asset reference properties

string, default “”, (never None)

Default size of the asset preview thumbnails in pixels

int in [32, 256], default 0

Operator to call when dragging an item with asset reference properties

string, default “”, (never None)

If this is set, the asset gets a custom ID, otherwise it takes the name of the class used to define the asset (for example, if the class name is “OBJECT_AST_hello”, and bl_idname is not set by the script, then bl_idname = “OBJECT_AST_hello”)

string, default “”, (never None)

Options for this asset shelf type

NO_ASSET_DRAG No Asset Dragging – Disable the default asset dragging on drag events. Useful for implementing custom dragging via custom key-map items..

DEFAULT_VISIBLE Visible by Default – Unhide the asset shelf when it’s available for the first time, otherwise it will be hidden.

STORE_ENABLED_CATALOGS_IN_PREFERENCES Store Enabled Catalogs in Preferences – Store the shelf’s enabled catalogs in the preferences rather than the local asset shelf settings.

ACTIVATE_FOR_CONTEXT_MENU When spawning a context menu for an asset, activate the asset and call `bl_activate_operator` if present, rather than just highlighting the asset.

enum set in {'NO_ASSET_DRAG', 'DEFAULT_VISIBLE', 'STORE_ENABLED_CATALOGS_IN_PREFERENCES', 'ACTIVATE_FOR_CONTEXT_MENU'}, default set()

The space where the asset shelf will show up in. Ignored for popup asset shelves which can be displayed in any space.

enum in Space Type Items, default 'EMPTY'

Show Action data-blocks

boolean, default False

Show Annotation data-blocks

boolean, default False

Show Armature data-blocks

boolean, default False

Show Brushes data-blocks

boolean, default False

Show Cache File data-blocks

boolean, default False

Show Camera data-blocks

boolean, default False

Show Curve data-blocks

boolean, default False

Show/hide Curves data-blocks

boolean, default False

Show Font data-blocks

boolean, default False

Show Grease Pencil data-blocks

boolean, default False

Show Collection data-blocks

boolean, default False

Show Image data-blocks

boolean, default False

Show Lattice data-blocks

boolean, default False

Show Light data-blocks

boolean, default False

Show Light Probe data-blocks

boolean, default False

Show Freestyle’s Line Style data-blocks

boolean, default False

Show Mask data-blocks

boolean, default False

Show Material data-blocks

boolean, default False

Show Mesh data-blocks

boolean, default False

Show Metaball data-blocks

boolean, default False

Show Movie Clip data-blocks

boolean, default False

Show Node Tree data-blocks

boolean, default False

Show Object data-blocks

boolean, default False

Show Paint Curve data-blocks

boolean, default False

Show Palette data-blocks

boolean, default False

Show Particle Settings data-blocks

boolean, default False

Show/hide Point Cloud data-blocks

boolean, default False

Show Scene data-blocks

boolean, default False

Show Sound data-blocks

boolean, default False

Show Speaker data-blocks

boolean, default False

Show Text data-blocks

boolean, default False

Show Texture data-blocks

boolean, default False

Show/hide Volume data-blocks

boolean, default False

Show workspace data-blocks

boolean, default False

Show World data-blocks

boolean, default False

Size of the asset preview thumbnails in pixels

int in [32, 256], default 0

Filter assets by name

string, default “”, (never None)

Show the asset name together with the preview. Otherwise only the preview will be visible.

boolean, default False

If this method returns a non-null output, the asset shelf will be visible

Determine if an asset should be visible in the asset shelf. If this method returns a non-null output, the asset will be visible.

Return a reference to the asset that should be highlighted as active in the asset shelf

The weak reference to the asset to be highlighted as active, or None

Draw UI elements into the context menu UI layout displayed on right click

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AssetRepresentation(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetRepresentation.html

**Contents:**
- AssetRepresentation(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Information about an entity that makes it possible for the asset system to deal with the entity as asset

Absolute path to the .blend file containing this asset

string, default “”, (readonly, never None)

Absolute path to the .blend file containing this asset extended with the path of the asset inside the file

string, default “”, (readonly, never None)

The type of the data-block, if the asset represents one (‘NONE’ otherwise)

enum in Id Type Items, default 'ACTION', (readonly)

The local data-block this asset represents; only valid if that is a data-block in this file

Additional information about the asset

AssetMetaData, (readonly)

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

bpy.context.selected_assets

AssetShelf.asset_poll

AssetShelf.draw_context_menu

---

## AssetTag(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetTag.html

**Contents:**
- AssetTag(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

User defined tag (name token)

The identifier that makes up this tag

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## AssetWeakReference(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetWeakReference.html

**Contents:**
- AssetWeakReference(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Weak reference to some asset

string, default “”, (readonly, never None)

ALL All Libraries – Show assets from all of the listed asset libraries.

LOCAL Current File – Show the assets currently available in this Blender session.

ESSENTIALS Essentials – Show the basic building blocks and utilities coming with Blender.

CUSTOM Custom – Show assets from the asset libraries configured in the Preferences.

enum in ['ALL', 'LOCAL', 'ESSENTIALS', 'CUSTOM'], default 'ALL', (readonly)

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AssetShelf.get_active_asset

Paint.brush_asset_reference

Paint.eraser_brush_asset_reference

---

## AssetTags(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AssetTags.html

**Contents:**
- AssetTags(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of custom asset tags

Add a new tag to this asset

name (string, (never None)) – Name

skip_if_exists (boolean, (optional)) – Skip if Exists, Do not add a new tag if one of the same type already exists

Remove an existing tag from this asset

tag (AssetTag, (never None)) – Removed tag

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Attribute(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Attribute.html

**Contents:**
- Attribute(bpy_struct)¶
- Using Attributes¶
  - Inherited Properties¶
  - Inherited Functions¶
  - References¶

Attributes are used to store data that corresponds to geometry elements. Geometry elements are items in one of the geometry domains like points, curves, or faces.

An attribute has a name, a type, and is stored on a domain.

The name of this attribute. Names have to be unique within the same geometry. If the name starts with a ., the attribute is hidden from the UI.

The type of data that this attribute stores, e.g. a float, integer, color, etc. See Attribute Type Items.

The geometry domain that the attribute is stored on. See Attribute Domain Items.

Attributes can be stored on geometries like Mesh, Curves, PointCloud, etc. These geometries have attribute groups (usually called attributes). Using the groups, attributes can then be accessed by their name:

Creating and storing custom attributes is done using the attributes.new function:

Removing attributes can be done like so:

Some attributes are required and cannot be removed, like "position".

Attribute values are read by accessing their attribute.data collection property. However, in cases where multiple values should be read at once, it is better to use the bpy_prop_collection.foreach_get function and read the values into a numpy buffer.

Some attribute types use different named properties to access their value. Instead of value, vectors use vector, and colors use color.

Writing to different attribute types is very similar. You can simply assign to a value directly. Again, when writing to multiple values, it is recommended to use the bpy_prop_collection.foreach_set function to write the values from a numpy buffer.

The bpy_prop_collection.foreach_get / bpy_prop_collection.foreach_set methods require a flat array. This is sometimes not desirable, e.g. when reading/writing positions, which are 3D vectors. In these cases, it’s possible to use np.ravel to pass the data as a flat array:

base class — bpy_struct

subclasses — BoolAttribute, ByteColorAttribute, ByteIntAttribute, Float2Attribute, Float4x4Attribute, FloatAttribute, FloatColorAttribute, FloatVectorAttribute, Int2Attribute, IntAttribute, QuaternionAttribute, Short2Attribute, StringAttribute

Type of data stored in attribute

enum in Attribute Type Items, default 'FLOAT', (readonly)

Domain of the Attribute

enum in Attribute Domain Items, default 'POINT', (readonly)

The attribute is meant for internal use by Blender

boolean, default False, (readonly)

Whether the attribute can be removed or renamed

boolean, default False, (readonly)

Name of the Attribute

string, default “”, (never None)

Method used to store the data

ARRAY Array – Store a value for every element.

SINGLE Single – Store a single value for the entire domain.

enum in ['ARRAY', 'SINGLE'], default 'ARRAY', (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AttributeGroupCurves.active

AttributeGroupCurves.new

AttributeGroupCurves.remove

AttributeGroupGreasePencil.active

AttributeGroupGreasePencil.new

AttributeGroupGreasePencil.remove

AttributeGroupGreasePencilDrawing.active

AttributeGroupGreasePencilDrawing.new

AttributeGroupGreasePencilDrawing.remove

AttributeGroupMesh.active

AttributeGroupMesh.active_color

AttributeGroupMesh.new

AttributeGroupMesh.remove

AttributeGroupPointCloud.active

AttributeGroupPointCloud.new

AttributeGroupPointCloud.remove

Curves.color_attributes

GreasePencil.attributes

GreasePencil.color_attributes

GreasePencilDrawing.attributes

GreasePencilDrawing.color_attributes

Mesh.color_attributes

PointCloud.attributes

PointCloud.color_attributes

**Examples:**

Example 1 (unknown):
```unknown
radii = curves.attributes["radius"]
```

Example 2 (markdown):
```markdown
# Add a new attribute named `my_attribute_name` of type `float` on the point domain of the geometry.
my_attribute = curves.attributes.new("my_attribute_name", 'FLOAT', 'POINT')
```

Example 3 (unknown):
```unknown
attribute = drawing.attributes["some_attribute"]
drawing.attributes.remove(attribute)
```

Example 4 (swift):
```swift
import numpy as np

# Get the radius attribute.
radii = curves.attributes["radius"]
# Print the radius of the first point.
print(radii.data[0].value)
# Output: 0.005

# Get the total number of points.
num_points = attributes.domain_size('POINT')
# Create an empty buffer to read all the radii into.
radii_data = np.zeros(num_points, dtype=np.float32)
# Read all the radii of the curves into `radii_data` at once.
radii.data.foreach_get('value', radii_data)
# Print all the radii.
print(radii_data)
# Output: [0.1, 0.2, 0.3, 0.4, ... ]
```

---

## AttributeGroupCurves(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AttributeGroupCurves.html

**Contents:**
- AttributeGroupCurves(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Group of geometry attributes

Active attribute index or -1 when none are active

int in [-1, inf], default 0

Add attribute to geometry

name (string, (never None)) – Name, Name of geometry attribute

type (enum in Attribute Type Items) – Type, Attribute type

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

New geometry attribute

Remove attribute from geometry

attribute (Attribute, (never None)) – Geometry Attribute

Get the size of a given domain

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

Size, Size of the domain

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Curves.color_attributes

---

## AttributeGroupGreasePencil(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AttributeGroupGreasePencil.html

**Contents:**
- AttributeGroupGreasePencil(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Group of geometry attributes

Active attribute index or -1 when none are active

int in [-1, inf], default 0

Add attribute to geometry

name (string, (never None)) – Name, Name of geometry attribute

type (enum in Attribute Type Items) – Type, Attribute type

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

New geometry attribute

Remove attribute from geometry

attribute (Attribute, (never None)) – Geometry Attribute

Get the size of a given domain

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

Size, Size of the domain

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

GreasePencil.attributes

GreasePencil.color_attributes

---

## AttributeGroupMesh(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AttributeGroupMesh.html

**Contents:**
- AttributeGroupMesh(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Group of geometry attributes

Active color attribute for display and editing

Active color attribute index

int in [-inf, inf], default 0

The name of the active color attribute for display and editing

string, default “”, (never None)

Active attribute index or -1 when none are active

int in [-1, inf], default 0

The name of the default color attribute used as a fallback for rendering

string, default “”, (never None)

The index of the color attribute used as a fallback for rendering

int in [-inf, inf], default 0

Add attribute to geometry

name (string, (never None)) – Name, Name of geometry attribute

type (enum in Attribute Type Items) – Type, Attribute type

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

New geometry attribute

Remove attribute from geometry

attribute (Attribute, (never None)) – Geometry Attribute

Get the size of a given domain

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

Size, Size of the domain

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Mesh.color_attributes

---

## AttributeGroupGreasePencilDrawing(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AttributeGroupGreasePencilDrawing.html

**Contents:**
- AttributeGroupGreasePencilDrawing(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Group of geometry attributes

Active attribute index or -1 when none are active

int in [-1, inf], default 0

Add attribute to geometry

name (string, (never None)) – Name, Name of geometry attribute

type (enum in Attribute Type Items) – Type, Attribute type

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

New geometry attribute

Remove attribute from geometry

attribute (Attribute, (never None)) – Geometry Attribute

Get the size of a given domain

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

Size, Size of the domain

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

GreasePencilDrawing.attributes

GreasePencilDrawing.color_attributes

---

## AttributeGroupPointCloud(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.AttributeGroupPointCloud.html

**Contents:**
- AttributeGroupPointCloud(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Group of geometry attributes

Active attribute index or -1 when none are active

int in [-1, inf], default 0

Add attribute to geometry

name (string, (never None)) – Name, Name of geometry attribute

type (enum in Attribute Type Items) – Type, Attribute type

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

New geometry attribute

Remove attribute from geometry

attribute (Attribute, (never None)) – Geometry Attribute

Get the size of a given domain

domain (enum in Attribute Domain Items) – Domain, Type of element that attribute is stored on

Size, Size of the domain

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

PointCloud.attributes

PointCloud.color_attributes

---

## BakeSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BakeSettings.html

**Contents:**
- BakeSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Bake data for a Scene data-block

Inflate the active object by the specified distance for baking. This helps matching to points nearer to the outside of the selected object meshes.

float in [0, inf], default 0.0

Object to use as cage instead of calculating the cage from the active object with cage extrusion

Choose displacement space for baking

OBJECT Object – Bake the displacement in object space.

TANGENT Tangent – Bake the displacement in tangent space.

enum in ['OBJECT', 'TANGENT'], default 'OBJECT'

Image filepath to use when saving externally

string, default “”, (never None, blend relative // prefix supported)

Vertical dimension of the baking map

int in [4, 10000], default 512

ImageFormatSettings, (readonly, never None)

Extends the baked result as a post process filter

int in [0, 32767], default 16

Algorithm to extend the baked result

enum in Bake Margin Type Items, default 'ADJACENT_FACES'

The maximum ray distance for matching points between the active and selected objects. If zero, there is no limit.

float in [0, inf], default 0.0

Axis to bake in blue channel

enum in Normal Swizzle Items, default 'POS_X'

Axis to bake in green channel

enum in Normal Swizzle Items, default 'POS_X'

Axis to bake in red channel

enum in Normal Swizzle Items, default 'POS_X'

Choose normal space for baking

enum in Normal Space Items, default 'TANGENT'

Passes to include in the active baking pass

enum set in Bake Pass Filter Type Items, default {'COLOR', 'DIFFUSE', 'DIRECT', 'EMIT', 'GLOSSY', 'INDIRECT', 'TRANSMISSION'}, (readonly)

Where to save baked image textures

enum in Bake Save Mode Items, default 'INTERNAL'

Where to output the baked map

enum in Bake Target Items, default 'IMAGE_TEXTURES'

Choose shading information to bake into the image

NORMALS Normals – Bake normals.

DISPLACEMENT Displacement – Bake displacement.

VECTOR_DISPLACEMENT Vector Displacement – Bake vector displacement.

enum in ['NORMALS', 'DISPLACEMENT', 'VECTOR_DISPLACEMENT'], default 'NORMALS'

Automatically name the output file with the pass type (external only)

boolean, default False

Cast rays to active object from a cage

boolean, default False

Clear Images before baking (internal only)

boolean, default True

Calculate heights against unsubdivided low resolution mesh

boolean, default False

Bake directly from multires object

boolean, default False

boolean, default True

Add diffuse contribution

boolean, default True

Add direct lighting contribution

boolean, default True

Add emission contribution

boolean, default True

Add glossy contribution

boolean, default True

Add indirect lighting contribution

boolean, default True

Add transmission contribution

boolean, default True

Bake shading on the surface of selected objects to the active object

boolean, default False

Split external images per material (external only)

boolean, default False

Source of reflection ray directions

ABOVE_SURFACE Above Surface – Cast rays from above the surface.

ACTIVE_CAMERA Active Camera – Use the active camera’s position to cast rays.

enum in ['ABOVE_SURFACE', 'ACTIVE_CAMERA'], default 'ABOVE_SURFACE'

Horizontal dimension of the baking map

int in [4, 10000], default 512

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BevelModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BevelModifier.html

**Contents:**
- BevelModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Bevel modifier to make edges and vertices more rounded

Affect edges or vertices

VERTICES Vertices – Affect only vertices.

EDGES Edges – Affect only edges.

enum in ['VERTICES', 'EDGES'], default 'EDGES'

Angle above which to bevel edges

float in [0, 3.14159], default 0.523599

The path for the custom profile

CurveProfile, (readonly)

Attribute name for edge weight

string, default “”, (never None)

Whether to set face strength, and which faces to set it on

FSTR_NONE None – Do not set face strength.

FSTR_NEW New – Set face strength on new faces only.

FSTR_AFFECTED Affected – Set face strength on new and affected faces only.

FSTR_ALL All – Set face strength on all faces.

enum in ['FSTR_NONE', 'FSTR_NEW', 'FSTR_AFFECTED', 'FSTR_ALL'], default 'FSTR_NONE'

Match normals of new faces to adjacent faces

boolean, default False

Invert vertex group influence

boolean, default False

NONE None – Bevel the entire mesh by a constant amount.

ANGLE Angle – Only bevel edges with sharp enough angles between faces.

WEIGHT Weight – Use bevel weights to determine how much bevel is applied in edge mode.

VGROUP Vertex Group – Use vertex group weights to select whether vertex or edge is beveled.

enum in ['NONE', 'ANGLE', 'WEIGHT', 'VGROUP'], default 'ANGLE'

Prefer sliding along edges to having even widths

boolean, default True

Mark Seams along beveled edges

boolean, default False

Mark beveled edges as sharp

boolean, default False

Material index of generated faces, -1 for automatic

int in [-1, 32767], default -1

Pattern to use for inside of miters

MITER_SHARP Sharp – Inside of miter is sharp.

MITER_ARC Arc – Inside of miter is arc.

enum in ['MITER_SHARP', 'MITER_ARC'], default 'MITER_SHARP'

Pattern to use for outside of miters

MITER_SHARP Sharp – Outside of miter is sharp.

MITER_PATCH Patch – Outside of miter is squared-off patch.

MITER_ARC Arc – Outside of miter is arc.

enum in ['MITER_SHARP', 'MITER_PATCH', 'MITER_ARC'], default 'MITER_SHARP'

What distance Width measures

OFFSET Offset – Amount is offset of new edges from original.

WIDTH Width – Amount is width of new face.

DEPTH Depth – Amount is perpendicular distance from original edge to bevel face.

PERCENT Percent – Amount is percent of adjacent edge length.

ABSOLUTE Absolute – Amount is absolute distance along adjacent edge.

enum in ['OFFSET', 'WIDTH', 'DEPTH', 'PERCENT', 'ABSOLUTE'], default 'OFFSET'

The profile shape (0.5 = round)

float in [0, 1], default 0.5

The type of shape used to rebuild a beveled section

SUPERELLIPSE Superellipse – The profile can be a concave or convex curve.

CUSTOM Custom – The profile can be any arbitrary path between its endpoints.

enum in ['SUPERELLIPSE', 'CUSTOM'], default 'SUPERELLIPSE'

Number of segments for round edges/verts

int in [1, 1000], default 1

Spread distance for inner miter arcs

float in [0, inf], default 0.1

Clamp the width to avoid overlap

boolean, default True

string, default “”, (never None)

Attribute name for vertex weight

string, default “”, (never None)

The method to use to create the mesh at intersections

ADJ Grid Fill – Default patterned fill.

CUTOFF Cutoff – A cut-off at the end of each profile before the intersection.

enum in ['ADJ', 'CUTOFF'], default 'ADJ'

float in [0, inf], default 0.1

Bevel amount for percentage method

float in [0, inf], default 0.1

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## BezierSplinePoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BezierSplinePoint.html

**Contents:**
- BezierSplinePoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Bézier curve point with two handles

Coordinates of the control point

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

Coordinates of the first handle

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

enum in ['FREE', 'VECTOR', 'ALIGNED', 'AUTO'], default 'FREE'

Coordinates of the second handle

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

enum in ['FREE', 'VECTOR', 'ALIGNED', 'AUTO'], default 'FREE'

boolean, default False

float in [0, inf], default 0.0

Control point selection status

boolean, default False

Handle 1 selection status

boolean, default False

Handle 2 selection status

boolean, default False

float in [-376.991, 376.991], default 0.0

float in [0.01, 100], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendData(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendData.html

**Contents:**
- BlendData(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Main data structure representing a .blend file and all its data-blocks

BlendDataActions bpy_prop_collection of Action, (readonly)

Annotation data-blocks (legacy Grease Pencil)

BlendDataAnnotations bpy_prop_collection of Annotation, (readonly)

BlendDataArmatures bpy_prop_collection of Armature, (readonly)

BlendDataBrushes bpy_prop_collection of Brush, (readonly)

Cache Files data-blocks

BlendDataCacheFiles bpy_prop_collection of CacheFile, (readonly)

BlendDataCameras bpy_prop_collection of Camera, (readonly)

Collection data-blocks

BlendDataCollections bpy_prop_collection of Collection, (readonly)

Information about the color space used for data-blocks in a blend file

BlendFileColorspace, (readonly, never None)

BlendDataCurves bpy_prop_collection of Curve, (readonly)

Path to the .blend file

string, default “”, (readonly, never None)

Vector font data-blocks

BlendDataFonts bpy_prop_collection of VectorFont, (readonly)

Grease Pencil data-blocks

BlendDataGreasePencilsV3 bpy_prop_collection of GreasePencil, (readonly)

Hair curve data-blocks

BlendDataHairCurves bpy_prop_collection of Curves, (readonly)

BlendDataImages bpy_prop_collection of Image, (readonly)

Have recent edits been saved to disk

boolean, default False, (readonly)

Has the current session been saved to disk as a .blend file

boolean, default False, (readonly)

BlendDataLattices bpy_prop_collection of Lattice, (readonly)

BlendDataLibraries bpy_prop_collection of Library, (readonly)

Light Probe data-blocks

BlendDataProbes bpy_prop_collection of LightProbe, (readonly)

BlendDataLights bpy_prop_collection of Light, (readonly)

Line Style data-blocks

BlendDataLineStyles bpy_prop_collection of FreestyleLineStyle, (readonly)

BlendDataMasks bpy_prop_collection of Mask, (readonly)

BlendDataMaterials bpy_prop_collection of Material, (readonly)

BlendDataMeshes bpy_prop_collection of Mesh, (readonly)

BlendDataMetaBalls bpy_prop_collection of MetaBall, (readonly)

Movie Clip data-blocks

BlendDataMovieClips bpy_prop_collection of MovieClip, (readonly)

Node group data-blocks

BlendDataNodeTrees bpy_prop_collection of NodeTree, (readonly)

BlendDataObjects bpy_prop_collection of Object, (readonly)

Paint Curves data-blocks

BlendDataPaintCurves bpy_prop_collection of PaintCurve, (readonly)

BlendDataPalettes bpy_prop_collection of Palette, (readonly)

BlendDataParticles bpy_prop_collection of ParticleSettings, (readonly)

Point cloud data-blocks

BlendDataPointClouds bpy_prop_collection of PointCloud, (readonly)

BlendDataScenes bpy_prop_collection of Scene, (readonly)

BlendDataScreens bpy_prop_collection of Screen, (readonly)

Shape Key data-blocks

bpy_prop_collection of Key, (readonly)

BlendDataSounds bpy_prop_collection of Sound, (readonly)

BlendDataSpeakers bpy_prop_collection of Speaker, (readonly)

BlendDataTexts bpy_prop_collection of Text, (readonly)

BlendDataTextures bpy_prop_collection of Texture, (readonly)

Automatically pack all external data into .blend file

boolean, default False

File format version the .blend file was saved with

int array of 3 items in [0, inf], default (0, 0, 0), (readonly)

BlendDataVolumes bpy_prop_collection of Volume, (readonly)

Window manager data-blocks

BlendDataWindowManagers bpy_prop_collection of WindowManager, (readonly)

Workspace data-blocks

BlendDataWorkSpaces bpy_prop_collection of WorkSpace, (readonly)

BlendDataWorlds bpy_prop_collection of World, (readonly)

Pack the given linked ID and its dependencies into current blendfile

root_id (ID) – Root linked ID to pack

The packed ID matching the given root ID

Remove (delete) several IDs at once.

Note that this function is quicker than individual calls to remove() (from bpy.types.BlendData ID collections), but less safe/versatile (it can break Blender, e.g. by removing all scenes…).

ids (Sequence[bpy.types.ID]) – Sequence of IDs (types can be mixed).

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Call visit_path_fn for the file paths used by all ID data-blocks in current bpy.data.

For list of valid set members for visit_types, see: bpy.types.KeyingSetPath.id_type.

visit_path_fn (Callable[[bpy.types.ID, str, Any], str|None]) – function that takes three parameters: the data-block, a file path, and a placeholder for future use. The function should return either None or a str. In the latter case, the visited file path will be replaced with the returned string.

subset (set[str]) – When given, only these data-blocks and their used file paths will be visited.

visit_types (set[str]) – When given, only visit data-blocks of these types. Ignored if subset is also given.

flags (set[str]) – Set of flags that influence which data-blocks are visited. See File Path Foreach Flag Items.

Returns a mapping of all ID data-blocks in current bpy.data to a set of all file paths used by them.

For list of valid set members for key_types, see: bpy.types.KeyingSetPath.id_type.

subset (sequence) – When given, only these data-blocks and their used file paths will be included as keys/values in the map.

key_types (set[str]) – When given, filter the keys mapped by ID types. Ignored if subset is also given.

include_libraries (bool) – Include library file paths of linked data. False by default.

dictionary of bpy.types.ID instances, with sets of file path strings as their values.

Remove (delete) all IDs with no user.

do_local_ids (bool, optional) – Include unused local IDs in the deletion, defaults to True

do_linked_ids (bool, optional) – Include unused linked IDs in the deletion, defaults to True

do_recursive (bool, optional) – Recursively check for unused IDs, ensuring no orphaned one remain after a single run of that function, defaults to False

The number of deleted IDs.

A context manager that temporarily creates blender file data.

filepath (str | bytes | None) – The file path for the newly temporary data. When None, the path of the currently open file is used.

Blend file data which is freed once the context exists.

Returns a mapping of all ID data-blocks in current bpy.data to a set of all data-blocks using them.

For list of valid set members for key_types & value_types, see: bpy.types.KeyingSetPath.id_type.

subset (Sequence[bpy.types.ID]) – When passed, only these data-blocks and their users will be included as keys/values in the map.

key_types (set[str]) – Filter the keys mapped by ID types.

value_types (set[str]) – Filter the values in the set by ID types.

dictionary that maps data-blocks ID’s to their users.

dict[bpy.types.ID, set[bpy.types.ID]]

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataAnnotations(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataAnnotations.html

**Contents:**
- BlendDataAnnotations(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of annotations

value (boolean) – Value

Add a new annotation data-block to the main database

name (string, (never None)) – New name for the data-block

New annotation data-block

Remove annotation instance from the current blendfile

annotation (Annotation, (never None)) – Grease Pencil to remove

do_unlink (boolean, (optional)) – Unlink all usages of this annotation before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this annotation

do_ui_user (boolean, (optional)) – Make sure interface does not reference this annotation

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.annotations

---

## BlendDataArmatures(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataArmatures.html

**Contents:**
- BlendDataArmatures(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of armatures

Add a new armature to the main database

name (string, (never None)) – New name for the data-block

New armature data-block

Remove an armature from the current blendfile

armature (Armature, (never None)) – Armature to remove

do_unlink (boolean, (optional)) – Unlink all usages of this armature before deleting it (WARNING: will also delete objects instancing that armature data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this armature data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this armature data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataActions(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataActions.html

**Contents:**
- BlendDataActions(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of actions

Add a new action to the main database

name (string, (never None)) – New name for the data-block

New action data-block

Remove an action from the current blendfile

action (Action, (never None)) – Action to remove

do_unlink (boolean, (optional)) – Unlink all usages of this action before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this action

do_ui_user (boolean, (optional)) – Make sure interface does not reference this action

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataBrushes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataBrushes.html

**Contents:**
- BlendDataBrushes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of brushes

Add a new brush to the main database

name (string, (never None)) – New name for the data-block

mode (enum in Object Mode Items, (optional)) – Paint Mode for the new brush

Remove a brush from the current blendfile

brush (Brush, (never None)) – Brush to remove

do_unlink (boolean, (optional)) – Unlink all usages of this brush before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this brush

do_ui_user (boolean, (optional)) – Make sure interface does not reference this brush

value (boolean) – Value

Add Grease Pencil brush settings

brush (Brush, (never None)) – Brush

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataCacheFiles(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataCacheFiles.html

**Contents:**
- BlendDataCacheFiles(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of cache files

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.cache_files

---

## BlendDataCameras(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataCameras.html

**Contents:**
- BlendDataCameras(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of cameras

Add a new camera to the main database

name (string, (never None)) – New name for the data-block

New camera data-block

Remove a camera from the current blendfile

camera (Camera, (never None)) – Camera to remove

do_unlink (boolean, (optional)) – Unlink all usages of this camera before deleting it (WARNING: will also delete objects instancing that camera data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this camera

do_ui_user (boolean, (optional)) – Make sure interface does not reference this camera

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataCollections(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataCollections.html

**Contents:**
- BlendDataCollections(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of collections

Add a new collection to the main database

name (string, (never None)) – New name for the data-block

New collection data-block

Remove a collection from the current blendfile

collection (Collection, (never None)) – Collection to remove

do_unlink (boolean, (optional)) – Unlink all usages of this collection before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this collection

do_ui_user (boolean, (optional)) – Make sure interface does not reference this collection

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.collections

---

## BlendDataCurves(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataCurves.html

**Contents:**
- BlendDataCurves(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new curve to the main database

name (string, (never None)) – New name for the data-block

type (enum in Object Type Curve Items) – Type, The type of curve to add

Remove a curve from the current blendfile

curve (Curve, (never None)) – Curve to remove

do_unlink (boolean, (optional)) – Unlink all usages of this curve before deleting it (WARNING: will also delete objects instancing that curve data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this curve data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this curve data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataHairCurves(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataHairCurves.html

**Contents:**
- BlendDataHairCurves(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of hair curves

Add a new hair to the main database

name (string, (never None)) – New name for the data-block

New curves data-block

Remove a curves data-block from the current blendfile

curves (Curves, (never None)) – Curves data-block to remove

do_unlink (boolean, (optional)) – Unlink all usages of this curves before deleting it (WARNING: will also delete objects instancing that curves data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this curves data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this curves data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.hair_curves

---

## BlendDataGreasePencilsV3(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataGreasePencilsV3.html

**Contents:**
- BlendDataGreasePencilsV3(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Grease Pencils

value (boolean) – Value

Add a new Grease Pencil data-block to the main database

name (string, (never None)) – New name for the data-block

New Grease Pencil data-block

Remove a Grease Pencil instance from the current blendfile

grease_pencil (GreasePencil, (never None)) – Grease Pencil to remove

do_unlink (boolean, (optional)) – Unlink all usages of this Grease Pencil before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this Grease Pencil

do_ui_user (boolean, (optional)) – Make sure interface does not reference this Grease Pencil

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.grease_pencils

---

## BlendDataFonts(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataFonts.html

**Contents:**
- BlendDataFonts(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Load a new font into the main database

filepath (string, (never None, blend relative // prefix supported)) – path of the font to load

check_existing (boolean, (optional)) – Using existing data-block if this file is already loaded

Remove a font from the current blendfile

vfont (VectorFont, (never None)) – Font to remove

do_unlink (boolean, (optional)) – Unlink all usages of this font before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this font

do_ui_user (boolean, (optional)) – Make sure interface does not reference this font

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataImages(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataImages.html

**Contents:**
- BlendDataImages(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new image to the main database

name (string, (never None)) – New name for the data-block

width (int in [1, inf]) – Width of the image

height (int in [1, inf]) – Height of the image

alpha (boolean, (optional)) – Alpha, Use alpha channel

float_buffer (boolean, (optional)) – Float Buffer, Create an image with floating-point color

stereo3d (boolean, (optional)) – Stereo 3D, Create left and right views

is_data (boolean, (optional)) – Is Data, Create image with non-color data color space

tiled (boolean, (optional)) – Tiled, Create a tiled image

Load a new image into the main database

filepath (string, (never None, blend relative // prefix supported)) – Path of the file to load

check_existing (boolean, (optional)) – Using existing data-block if this file is already loaded

Remove an image from the current blendfile

image (Image, (never None)) – Image to remove

do_unlink (boolean, (optional)) – Unlink all usages of this image before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this image

do_ui_user (boolean, (optional)) – Make sure interface does not reference this image

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataLattices(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataLattices.html

**Contents:**
- BlendDataLattices(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of lattices

Add a new lattice to the main database

name (string, (never None)) – New name for the data-block

New lattice data-block

Remove a lattice from the current blendfile

lattice (Lattice, (never None)) – Lattice to remove

do_unlink (boolean, (optional)) – Unlink all usages of this lattice before deleting it (WARNING: will also delete objects instancing that lattice data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this lattice data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this lattice data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataLights(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataLights.html

**Contents:**
- BlendDataLights(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new light to the main database

name (string, (never None)) – New name for the data-block

type (enum in Light Type Items) – Type, The type of light to add

Remove a light from the current blendfile

light (Light, (never None)) – Light to remove

do_unlink (boolean, (optional)) – Unlink all usages of this light before deleting it (WARNING: will also delete objects instancing that light data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this light data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this light data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataLibraries(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html

**Contents:**
- BlendDataLibraries(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of libraries

value (boolean) – Value

Remove a library from the current blendfile

library (Library, (never None)) – Library to remove

do_unlink (boolean, (optional)) – Unlink all usages of this library before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this library

do_ui_user (boolean, (optional)) – Make sure interface does not reference this library

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Returns a context manager which exposes 2 library objects on entering. Each object has attributes matching bpy.data which are lists of strings to be linked.

filepath (str | bytes) – The path to a blend file.

link (bool) – When False reference to the original file is lost.

pack (bool) – If True, and link is also True, pack linked data-blocks into the current blend-file.

relative (bool) – When True the path is stored relative to the open blend file.

set_fake (bool) – If True, set fake user on appended IDs.

recursive (bool) – If True, also make indirect dependencies of appended libraries local.

reuse_local_id (bool) – If True,try to re-use previously appended matching ID on new append.

assets_only (bool) – If True, only list data-blocks marked as assets.

clear_asset_data (bool) – If True, clear the asset data on append (it is always kept for linked data).

create_liboverrides (bool) – If True and link is True, liboverrides will be created for linked data.

reuse_liboverrides (bool) – If True and create_liboverride is True, search for existing liboverride first.

create_liboverrides_runtime (bool) – If True and create_liboverride is True, create (or search for existing) runtime liboverride.

Write data-blocks into a blend file.

Indirectly referenced data-blocks will be expanded and written too.

filepath (str | bytes) – The path to write the blend-file.

datablocks (set[bpy.types.ID]) – set of data-blocks.

path_remap (str) – Optionally remap paths when writing the file: NONE No path manipulation (default). RELATIVE Remap paths that are already relative to the new location. RELATIVE_ALL Remap all paths to be relative to the new location. ABSOLUTE Make all paths absolute on writing.

Optionally remap paths when writing the file:

NONE No path manipulation (default).

RELATIVE Remap paths that are already relative to the new location.

RELATIVE_ALL Remap all paths to be relative to the new location.

ABSOLUTE Make all paths absolute on writing.

fake_user (bool) – When True, data-blocks will be written with fake-user flag enabled.

compress (bool) – When True, write a compressed blend file.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

**Examples:**

Example 1 (python):
```python
import bpy

filepath = "//link_library.blend"

# Load a single scene we know the name of.
with bpy.data.libraries.load(filepath) as (data_src, data_dst):
    data_dst.scenes = ["Scene"]


# Load all meshes.
with bpy.data.libraries.load(filepath) as (data_src, data_dst):
    data_dst.meshes = data_src.meshes


# Link all objects starting with "A".
with bpy.data.libraries.load(filepath, link=True) as (data_src, data_dst):
    data_dst.objects = [name for name in data_src.objects if name.startswith("A")]


# Append everything.
with bpy.data.libraries.load(filepath) as (data_src, data_dst):
    for attr in dir(data_dst):
        setattr(data_dst, attr, getattr(data_src, attr))


# The loaded objects can be accessed from `data_dst` outside of the context
# since loading the data replaces the strings for the data-blocks or None
# if the data-block could not be loaded.
with bpy.data.libraries.load(filepath) as (data_src, data_dst):
    data_dst.meshes = data_src.meshes
# Now operate directly on the loaded data.
for mesh in data_dst.meshes:
    if mesh is not None:
        print(mesh.name)
```

Example 2 (markdown):
```markdown
import bpy

filepath = "//new_library.blend"

# Write selected objects and their data to a blend file.
data_blocks = set(bpy.context.selected_objects)
bpy.data.libraries.write(filepath, data_blocks)


# Write all meshes starting with a capital letter and
# set them with fake-user enabled so they aren't lost on re-saving.
data_blocks = {mesh for mesh in bpy.data.meshes if mesh.name[:1].isupper()}
bpy.data.libraries.write(filepath, data_blocks, fake_user=True)


# Write all materials, textures and node groups to a library.
data_blocks = {*bpy.data.materials, *bpy.data.textures, *bpy.data.node_groups}
bpy.data.libraries.write(filepath, data_blocks)
```

---

## BlendDataLineStyles(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataLineStyles.html

**Contents:**
- BlendDataLineStyles(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of line styles

value (boolean) – Value

Add a new line style instance to the main database

name (string, (never None)) – New name for the data-block

New line style data-block

Remove a line style instance from the current blendfile

linestyle (FreestyleLineStyle, (never None)) – Line style to remove

do_unlink (boolean, (optional)) – Unlink all usages of this line style before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this line style

do_ui_user (boolean, (optional)) – Make sure interface does not reference this line style

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataMetaBalls(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataMetaBalls.html

**Contents:**
- BlendDataMetaBalls(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of metaballs

Add a new metaball to the main database

name (string, (never None)) – New name for the data-block

New metaball data-block

Remove a metaball from the current blendfile

metaball (MetaBall, (never None)) – Metaball to remove

do_unlink (boolean, (optional)) – Unlink all usages of this metaball before deleting it (WARNING: will also delete objects instancing that metaball data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this metaball data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this metaball data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataMasks(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataMasks.html

**Contents:**
- BlendDataMasks(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

value (boolean) – Value

Add a new mask with a given name to the main database

name (string, (never None)) – Mask, Name of new mask data-block

Remove a mask from the current blendfile

mask (Mask, (never None)) – Mask to remove

do_unlink (boolean, (optional)) – Unlink all usages of this mask before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this mask

do_ui_user (boolean, (optional)) – Make sure interface does not reference this mask

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataMeshes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataMeshes.html

**Contents:**
- BlendDataMeshes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new mesh to the main database

name (string, (never None)) – New name for the data-block

Add a new mesh created from given object (undeformed geometry if object is original, and final evaluated geometry, with all modifiers etc., if object is evaluated)

object (Object, (never None)) – Object to create mesh from

preserve_all_data_layers (boolean, (optional)) – Preserve all data layers in the mesh, like UV maps and vertex groups. By default Blender only computes the subset of data layers needed for viewport display and rendering, for better performance.

depsgraph (Depsgraph, (optional)) – Dependency Graph, Evaluated dependency graph which is required when preserve_all_data_layers is true

Mesh created from object, remove it if it is only used for export

Remove a mesh from the current blendfile

mesh (Mesh, (never None)) – Mesh to remove

do_unlink (boolean, (optional)) – Unlink all usages of this mesh before deleting it (WARNING: will also delete objects instancing that mesh data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this mesh data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this mesh data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataMaterials(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataMaterials.html

**Contents:**
- BlendDataMaterials(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of materials

Add a new material to the main database

name (string, (never None)) – New name for the data-block

New material data-block

Add Grease Pencil material settings

material (Material, (never None)) – Material

Remove Grease Pencil material settings

material (Material, (never None)) – Material

Remove a material from the current blendfile

material (Material, (never None)) – Material to remove

do_unlink (boolean, (optional)) – Unlink all usages of this material before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this material

do_ui_user (boolean, (optional)) – Make sure interface does not reference this material

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataMovieClips(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataMovieClips.html

**Contents:**
- BlendDataMovieClips(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of movie clips

value (boolean) – Value

Remove a movie clip from the current blendfile.

clip (MovieClip, (never None)) – Movie clip to remove

do_unlink (boolean, (optional)) – Unlink all usages of this movie clip before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this movie clip

do_ui_user (boolean, (optional)) – Make sure interface does not reference this movie clip

Add a new movie clip to the main database from a file (while check_existing is disabled for consistency with other load functions, behavior with multiple movie-clips using the same file may incorrectly generate proxies)

filepath (string, (never None, blend relative // prefix supported)) – path for the data-block

check_existing (boolean, (optional)) – Using existing data-block if this file is already loaded

New movie clip data-block

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataNodeTrees(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataNodeTrees.html

**Contents:**
- BlendDataNodeTrees(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of node trees

Add a new node tree to the main database

name (string, (never None)) – New name for the data-block

type (enum in ['GeometryNodeTree', 'CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']) – Type, The type of node_group to add GeometryNodeTree Geometry Node Editor – Advanced geometry editing and tools creation using nodes. CompositorNodeTree Compositor – Create effects and post-process renders, images, and the 3D Viewport. ShaderNodeTree Shader Editor – Edit materials, lights, and world shading using nodes. TextureNodeTree Texture Node Editor – Edit textures using nodes.

Type, The type of node_group to add

GeometryNodeTree Geometry Node Editor – Advanced geometry editing and tools creation using nodes.

CompositorNodeTree Compositor – Create effects and post-process renders, images, and the 3D Viewport.

ShaderNodeTree Shader Editor – Edit materials, lights, and world shading using nodes.

TextureNodeTree Texture Node Editor – Edit textures using nodes.

New node tree data-block

Remove a node tree from the current blendfile

tree (NodeTree, (never None)) – Node tree to remove

do_unlink (boolean, (optional)) – Unlink all usages of this node tree before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this node tree

do_ui_user (boolean, (optional)) – Make sure interface does not reference this node tree

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.node_groups

---

## BlendDataObjects(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataObjects.html

**Contents:**
- BlendDataObjects(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of objects

Add a new object to the main database

name (string, (never None)) – New name for the data-block

object_data (ID) – Object data or None for an empty object

New object data-block

Remove an object from the current blendfile

object (Object, (never None)) – Object to remove

do_unlink (boolean, (optional)) – Unlink all usages of this object before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this object

do_ui_user (boolean, (optional)) – Make sure interface does not reference this object

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataPaintCurves(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataPaintCurves.html

**Contents:**
- BlendDataPaintCurves(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of paint curves

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.paint_curves

---

## BlendDataProbes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataProbes.html

**Contents:**
- BlendDataProbes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of light probes

Add a new light probe to the main database

name (string, (never None)) – New name for the data-block

type (enum in Lightprobes Type Items) – Type, The type of light probe to add

New light probe data-block

Remove a light probe from the current blendfile

lightprobe (LightProbe, (never None)) – Light probe to remove

do_unlink (boolean, (optional)) – Unlink all usages of this light probe before deleting it (WARNING: will also delete objects instancing that light probe data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this light probe

do_ui_user (boolean, (optional)) – Make sure interface does not reference this light probe

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.lightprobes

---

## BlendDataPalettes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataPalettes.html

**Contents:**
- BlendDataPalettes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of palettes

Add a new palette to the main database

name (string, (never None)) – New name for the data-block

New palette data-block

Remove a palette from the current blendfile

palette (Palette, (never None)) – Palette to remove

do_unlink (boolean, (optional)) – Unlink all usages of this palette before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this palette

do_ui_user (boolean, (optional)) – Make sure interface does not reference this palette

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataParticles(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataParticles.html

**Contents:**
- BlendDataParticles(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of particle settings

Add a new particle settings instance to the main database

name (string, (never None)) – New name for the data-block

New particle settings data-block

Remove a particle settings instance from the current blendfile

particle (ParticleSettings, (never None)) – Particle Settings to remove

do_unlink (boolean, (optional)) – Unlink all usages of those particle settings before deleting them

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this particle settings

do_ui_user (boolean, (optional)) – Make sure interface does not reference this particle settings

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataPointClouds(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataPointClouds.html

**Contents:**
- BlendDataPointClouds(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of point clouds

Add a new point cloud to the main database

name (string, (never None)) – New name for the data-block

New point cloud data-block

Remove a point cloud from the current blendfile

pointcloud (PointCloud, (never None)) – Point cloud to remove

do_unlink (boolean, (optional)) – Unlink all usages of this point cloud before deleting it (WARNING: will also delete objects instancing that point cloud data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this point cloud data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this point cloud data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.pointclouds

---

## BlendDataScenes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataScenes.html

**Contents:**
- BlendDataScenes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new scene to the main database

name (string, (never None)) – New name for the data-block

Remove a scene from the current blendfile

scene (Scene, (never None)) – Scene to remove

do_unlink (boolean, (optional)) – Unlink all usages of this scene before deleting it

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataScreens(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataScreens.html

**Contents:**
- BlendDataScreens(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of screens

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataSounds(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataSounds.html

**Contents:**
- BlendDataSounds(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new sound to the main database from a file

filepath (string, (never None, blend relative // prefix supported)) – path for the data-block

check_existing (boolean, (optional)) – Using existing data-block if this file is already loaded

Remove a sound from the current blendfile

sound (Sound, (never None)) – Sound to remove

do_unlink (boolean, (optional)) – Unlink all usages of this sound before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this sound

do_ui_user (boolean, (optional)) – Make sure interface does not reference this sound

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataSpeakers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataSpeakers.html

**Contents:**
- BlendDataSpeakers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of speakers

Add a new speaker to the main database

name (string, (never None)) – New name for the data-block

New speaker data-block

Remove a speaker from the current blendfile

speaker (Speaker, (never None)) – Speaker to remove

do_unlink (boolean, (optional)) – Unlink all usages of this speaker before deleting it (WARNING: will also delete objects instancing that speaker data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this speaker data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this speaker data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataTexts(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataTexts.html

**Contents:**
- BlendDataTexts(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new text to the main database

name (string, (never None)) – New name for the data-block

Remove a text from the current blendfile

text (Text, (never None)) – Text to remove

do_unlink (boolean, (optional)) – Unlink all usages of this text before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this text

do_ui_user (boolean, (optional)) – Make sure interface does not reference this text

Add a new text to the main database from a file

filepath (string, (never None, blend relative // prefix supported)) – path for the data-block

internal (boolean, (optional)) – Make internal, Make text file internal after loading

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataVolumes(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataVolumes.html

**Contents:**
- BlendDataVolumes(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of volumes

Add a new volume to the main database

name (string, (never None)) – New name for the data-block

New volume data-block

Remove a volume from the current blendfile

volume (Volume, (never None)) – Volume to remove

do_unlink (boolean, (optional)) – Unlink all usages of this volume before deleting it (WARNING: will also delete objects instancing that volume data)

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this volume data

do_ui_user (boolean, (optional)) – Make sure interface does not reference this volume data

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataTextures(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataTextures.html

**Contents:**
- BlendDataTextures(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of textures

Add a new texture to the main database

name (string, (never None)) – New name for the data-block

type (enum in Texture Type Items) – Type, The type of texture to add

New texture data-block

Remove a texture from the current blendfile

texture (Texture, (never None)) – Texture to remove

do_unlink (boolean, (optional)) – Unlink all usages of this texture before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this texture

do_ui_user (boolean, (optional)) – Make sure interface does not reference this texture

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataWindowManagers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataWindowManagers.html

**Contents:**
- BlendDataWindowManagers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of window managers

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendData.window_managers

---

## BlendDataWorkSpaces(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataWorkSpaces.html

**Contents:**
- BlendDataWorkSpaces(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of workspaces

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendDataWorlds(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendDataWorlds.html

**Contents:**
- BlendDataWorlds(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Add a new world to the main database

name (string, (never None)) – New name for the data-block

Remove a world from the current blendfile

world (World, (never None)) – World to remove

do_unlink (boolean, (optional)) – Unlink all usages of this world before deleting it

do_id_user (boolean, (optional)) – Decrement user counter of all data-blocks used by this world

do_ui_user (boolean, (optional)) – Make sure interface does not reference this world

value (boolean) – Value

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendFileColorspace(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendFileColorspace.html

**Contents:**
- BlendFileColorspace(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Information about the color space used for data-blocks in a blend file

A color space, view or display was not found, which likely means the OpenColorIO config used to create this blend file is missing

boolean, default False, (readonly)

Color space used for all scene linear colors in this file, and for compositing, shader and geometry nodes processing

Linear Rec.709 Linear Rec.709 – Linear BT.709 with illuminant D65 white point.

Linear Rec.2020 Linear Rec.2020 – Linear BT.2020 with illuminant D65 white point.

ACEScg ACEScg – Linear AP1 with ACES white point.

enum in ['Linear Rec.709', 'Linear Rec.2020', 'ACEScg'], (readonly)

Unique identifier for common color spaces, as defined by the Color Interop Forum. May be empty if there is no interop ID for the working space. Common values are lin_rec709_scene, lin_rec2020_scene and lin_ap1_scene (for ACEScg)

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendImportContext(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendImportContext.html

**Contents:**
- BlendImportContext(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

Contextual data for a blendfile library/linked-data related operation. Currently only exposed as read-only data for the pre/post blendimport handlers

BlendImportContextItems bpy_prop_collection of BlendImportContextItem, (readonly)

Options for this blendfile import operation

LINK Only link data, instead of appending it.

MAKE_PATHS_RELATIVE Make paths of used library blendfiles relative to current blendfile.

USE_PLACEHOLDERS Generate a placeholder (empty ID) if not found in any library files.

FORCE_INDIRECT Force loaded ID to be tagged as indirectly linked (used in reload context only).

APPEND_SET_FAKEUSER Set fake user on appended IDs.

APPEND_RECURSIVE Append (make local) also indirect dependencies of appended IDs coming from other libraries. NOTE: All IDs (including indirectly linked ones) coming from the same initial library are always made local.

APPEND_LOCAL_ID_REUSE Try to re-use previously appended matching IDs when appending them again, instead of creating local duplicates.

APPEND_ASSET_DATA_CLEAR Clear the asset data on append (it is always kept for linked data).

SELECT_OBJECTS Automatically select imported objects.

USE_ACTIVE_COLLECTION Use the active Collection of the current View Layer to instantiate imported collections and objects.

OBDATA_INSTANCE Instantiate object data IDs (i.e. create objects for them if needed).

COLLECTION_INSTANCE Instantiate collections as empties, instead of linking them into the current view layer.

enum set in {'LINK', 'MAKE_PATHS_RELATIVE', 'USE_PLACEHOLDERS', 'FORCE_INDIRECT', 'APPEND_SET_FAKEUSER', 'APPEND_RECURSIVE', 'APPEND_LOCAL_ID_REUSE', 'APPEND_ASSET_DATA_CLEAR', 'SELECT_OBJECTS', 'USE_ACTIVE_COLLECTION', 'OBDATA_INSTANCE', 'COLLECTION_INSTANCE'}, default set(), (readonly)

Current stage of the import process

INIT Blendfile import context has been initialized and filled with a list of items to import, no data has been linked or appended yet.

DONE All data has been imported and is available in the list of “import_items”.

enum in ['INIT', 'DONE'], default 'INIT', (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BlendImportContextItem(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendImportContextItem.html

**Contents:**
- BlendImportContextItem(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

An item (representing a data-block) in a BlendImportContext data. Currently only exposed as read-only data for the pre/post linking handlers

How this item has been handled by the append operation. Only set if the data has been appended

UNSET Not yet defined.

KEEP_LINKED ID has been kept linked.

REUSE_LOCAL An existing matching local ID has been re-used.

MAKE_LOCAL The newly linked ID has been made local.

COPY_LOCAL The linked ID had other unrelated usages, so it has been duplicated into a local copy.

enum in ['UNSET', 'KEEP_LINKED', 'REUSE_LOCAL', 'MAKE_LOCAL', 'COPY_LOCAL'], default 'UNSET', (readonly)

The imported ID. None until it has been linked or appended. May be the same as reusable_local_id when appended

enum in Id Type Items, default 'ACTION', (readonly)

Various status info about an item after it has been imported

INDIRECT_USAGE That item was added for an indirectly imported ID, as a dependency of another data-block.

LIBOVERRIDE_DEPENDENCY That item represents an ID also used as liboverride dependency (either directly, as a liboverride reference, or indirectly, as data used by a liboverride reference). It should never be directly made local. Mutually exclusive with `LIBOVERRIDE_DEPENDENCY_ONLY`.

LIBOVERRIDE_DEPENDENCY_ONLY That item represents an ID only used as liboverride dependency (either directly or indirectly, see `LIBOVERRIDE_DEPENDENCY` for precisions). It should not be considered during the ‘make local’ (append) process, and remain purely linked data. Mutually exclusive with `LIBOVERRIDE_DEPENDENCY`.

enum set in {'INDIRECT_USAGE', 'LIBOVERRIDE_DEPENDENCY', 'LIBOVERRIDE_DEPENDENCY_ONLY'}, default set(), (readonly)

The library override of the linked ID. None until it has been created

string, default “”, (readonly, never None)

The already existing local ID that may be reused in append & reuse case. None until it has been found

List of libraries to search and import that ID from. The ID will be imported from the first file in that list that contains it

BlendImportContextLibraries bpy_prop_collection of BlendImportContextLibrary, (readonly)

Library ID representing the blendfile from which the ID was imported. None until the ID has been linked or appended

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendImportContext.import_items

---

## BlendImportContextItems(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendImportContextItems.html

**Contents:**
- BlendImportContextItems(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of blendfile import context items

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendImportContext.import_items

---

## BlendImportContextLibraries(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendImportContextLibraries.html

**Contents:**
- BlendImportContextLibraries(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of source libraries, i.e. blendfile paths

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendImportContextItem.source_libraries

---

## BlendImportContextLibrary(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendImportContextLibrary.html

**Contents:**
- BlendImportContextLibrary(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Library (blendfile) reference in a BlendImportContext data. Currently only exposed as read-only data for the pre/post blendimport handlers

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendImportContextItem.source_libraries

---

## BlendTexture(Texture)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlendTexture.html

**Contents:**
- BlendTexture(Texture)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ID, Texture

Procedural color blending texture

Style of the color blending

LINEAR Linear – Create a linear progression.

QUADRATIC Quadratic – Create a quadratic progression.

EASING Easing – Create a progression easing from one step to the next.

DIAGONAL Diagonal – Create a diagonal progression.

SPHERICAL Spherical – Create a spherical progression.

QUADRATIC_SPHERE Quadratic Sphere – Create a quadratic progression in the shape of a sphere.

RADIAL Radial – Create a radial progression.

enum in ['LINEAR', 'QUADRATIC', 'EASING', 'DIAGONAL', 'SPHERICAL', 'QUADRATIC_SPHERE', 'RADIAL'], default 'LINEAR'

Flip the texture’s X and Y axis

HORIZONTAL Horizontal – No flipping.

VERTICAL Vertical – Flip the texture’s X and Y axis.

enum in ['HORIZONTAL', 'VERTICAL'], default 'HORIZONTAL'

Materials that use this texture

Takes O(len(bpy.data.materials) * len(material.texture_slots)) time.

Object modifiers that use this texture

Takes O(len(bpy.data.objects) * len(obj.modifiers)) time.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

Texture.use_color_ramp

Texture.use_preview_alpha

Texture.animation_data

Texture.users_material

Texture.users_object_modifier

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

Texture.bl_rna_get_subclass

Texture.bl_rna_get_subclass_py

---

## BoidRule(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRule.html

**Contents:**
- BoidRule(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

subclasses — BoidRuleAverageSpeed, BoidRuleAvoid, BoidRuleAvoidCollision, BoidRuleFight, BoidRuleFollowLeader, BoidRuleGoal

string, default “”, (never None)

enum in Boidrule Type Items, default 'GOAL', (readonly)

Use rule when boid is flying

boolean, default False

Use rule when boid is on land

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidSettings.active_boid_state

BoidState.active_boid_rule

---

## BlenderRNA(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BlenderRNA.html

**Contents:**
- BlenderRNA(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

Blender RNA structure definitions

bpy_prop_collection of Struct, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BoidRuleAverageSpeed(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleAverageSpeed.html

**Contents:**
- BoidRuleAverageSpeed(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

How much velocity’s z-component is kept constant

float in [0, 1], default 0.0

Percentage of maximum speed

float in [0, 1], default 0.0

How fast velocity’s direction is randomized

float in [0, 1], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidRuleAvoid(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleAvoid.html

**Contents:**
- BoidRuleAvoid(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

Avoid object if danger from it is above this threshold

float in [0, 100], default 0.0

Predict target movement

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidRuleAvoidCollision(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleAvoidCollision.html

**Contents:**
- BoidRuleAvoidCollision(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

Time to look ahead in seconds

float in [0, 100], default 0.0

Avoid collision with other boids

boolean, default False

Avoid collision with deflector objects

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidRuleFight(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleFight.html

**Contents:**
- BoidRuleFight(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

Attack boids at max this distance

float in [0, 100], default 0.0

Flee to this distance

float in [0, 100], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidRuleFollowLeader(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleFollowLeader.html

**Contents:**
- BoidRuleFollowLeader(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

Distance behind leader to follow

float in [0, 100], default 0.0

Follow this object instead of a boid

How many boids in a line

int in [0, 100], default 0

Follow leader in a line

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidRuleGoal(BoidRule)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidRuleGoal.html

**Contents:**
- BoidRuleGoal(BoidRule)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, BoidRule

Predict target movement

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BoidRule.bl_rna_get_subclass

BoidRule.bl_rna_get_subclass_py

---

## BoidSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidSettings.html

**Contents:**
- BoidSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Settings for boid physics

float in [0, 1], default 0.0

int in [0, inf], default 0

Boid will fight this times stronger enemy

float in [0, 100], default 0.0

Maximum acceleration in air (relative to maximum speed)

float in [0, 1], default 0.0

Maximum angular velocity in air (relative to 180 degrees)

float in [0, 1], default 0.0

Radius of boids personal space in air (% of particle size)

float in [0, 10], default 0.0

float in [0, 100], default 0.0

Minimum speed in air (relative to maximum speed)

float in [0, 1], default 0.0

Amount of rotation around velocity vector on turns

float in [0, 2], default 0.0

Initial boid health when born

float in [0, 100], default 0.0

Boid height relative to particle size

float in [0, 2], default 0.0

Maximum acceleration on land (relative to maximum speed)

float in [0, 1], default 0.0

Maximum angular velocity on land (relative to 180 degrees)

float in [0, 1], default 0.0

Maximum speed for jumping

float in [0, 100], default 0.0

Radius of boids personal space on land (% of particle size)

float in [0, 10], default 0.0

How smoothly the boids land

float in [0, 10], default 0.0

Maximum speed on land

float in [0, 100], default 0.0

How strong a force must be to start effecting a boid on land

float in [0, 1000], default 0.0

Amount of rotation around side vector

float in [0, 2], default 0.0

Maximum distance from which a boid can attack

float in [0, 100], default 0.0

bpy_prop_collection of BoidState, (readonly)

Maximum caused damage on attack per second

float in [0, 100], default 0.0

Allow boids to climb goal objects

boolean, default False

Allow boids to move in air

boolean, default False

Allow boids to move on land

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ParticleSettings.boids

---

## BoidState(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoidState.html

**Contents:**
- BoidState(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Boid state for boid physics

int in [0, inf], default 0

float in [0, 10], default 0.0

string, default “”, (never None)

float in [0, 1], default 0.0

bpy_prop_collection of BoidRule, (readonly)

How the rules in the list are evaluated

FUZZY Fuzzy – Rules are gone through top to bottom (only the first rule which effect is above fuzziness threshold is evaluated).

RANDOM Random – A random rule is selected for each boid.

AVERAGE Average – All rules are averaged.

enum in ['FUZZY', 'RANDOM', 'AVERAGE'], default 'FUZZY'

float in [0, 100], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Bone(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Bone.html

**Contents:**
- Bone(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Bone in an Armature data-block

X-axis handle offset for start of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Z-axis handle offset for start of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

X-axis handle offset for end of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Z-axis handle offset for end of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Bone that serves as the end handle for the B-Bone curve

Bone that serves as the start handle for the B-Bone curve

Length of first Bézier Handle (for B-Bones only)

float in [-inf, inf], default 1.0

Length of second Bézier Handle (for B-Bones only)

float in [-inf, inf], default 1.0

Selects how the end handle of the B-Bone is computed

AUTO Automatic – Use connected parent and children to compute the handle.

ABSOLUTE Absolute – Use the position of the specified bone to compute the handle.

RELATIVE Relative – Use the offset of the specified bone from rest pose to compute the handle.

TANGENT Tangent – Use the orientation of the specified bone to compute the handle, ignoring the location.

enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'TANGENT'], default 'AUTO'

Selects how the start handle of the B-Bone is computed

AUTO Automatic – Use connected parent and children to compute the handle.

ABSOLUTE Absolute – Use the position of the specified bone to compute the handle.

RELATIVE Relative – Use the offset of the specified bone from rest pose to compute the handle.

TANGENT Tangent – Use the orientation of the specified bone to compute the handle, ignoring the location.

enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'TANGENT'], default 'AUTO'

Multiply the B-Bone Ease Out channel by the local Y scale value of the end handle. This is done after the Scale Easing option and isn’t affected by it.

boolean, default False

Multiply the B-Bone Ease In channel by the local Y scale value of the start handle. This is done after the Scale Easing option and isn’t affected by it.

boolean, default False

Multiply B-Bone Scale Out channels by the local scale values of the end handle. This is done after the Scale Easing option and isn’t affected by it.

boolean array of 3 items, default (False, False, False)

Multiply B-Bone Scale In channels by the local scale values of the start handle. This is done after the Scale Easing option and isn’t affected by it.

boolean array of 3 items, default (False, False, False)

Selects how the vertices are mapped to B-Bone segments based on their position

STRAIGHT Straight – Fast mapping that is good for most situations, but ignores the rest pose curvature of the B-Bone.

CURVED Curved – Slower mapping that gives better deformation for B-Bones that are sharply curved in rest pose.

enum in ['STRAIGHT', 'CURVED'], default 'STRAIGHT'

Roll offset for the start of the B-Bone, adjusts twist

float in [-inf, inf], default 0.0

Roll offset for the end of the B-Bone, adjusts twist

float in [-inf, inf], default 0.0

Scale factors for the start of the B-Bone, adjusts thickness (for tapering effects)

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

Scale factors for the end of the B-Bone, adjusts thickness (for tapering effects)

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

Number of subdivisions of bone (for B-Bones only)

int in [1, 32], default 0

float in [-inf, inf], default 0.0

float in [-inf, inf], default 0.0

Bones which are children of this bone

bpy_prop_collection of Bone, (readonly)

Bone Collections that contain this bone

BoneCollectionMemberships bpy_prop_collection of BoneCollection, (readonly)

BoneColor, (readonly)

ARMATURE_DEFINED Armature Defined – Use display mode from armature (default).

OCTAHEDRAL Octahedral – Display bones as octahedral shape.

STICK Stick – Display bones as simple 2D lines with dots.

BBONE B-Bone – Display bones as boxes, showing subdivision and B-Splines.

ENVELOPE Envelope – Display bones as extruded spheres, showing deformation influence volume.

WIRE Wire – Display bones as thin wires, showing subdivision and B-Splines.

enum in ['ARMATURE_DEFINED', 'OCTAHEDRAL', 'STICK', 'BBONE', 'ENVELOPE', 'WIRE'], default 'OCTAHEDRAL'

Bone deformation distance (for Envelope deform only)

float in [0, 1000], default 0.0

Bone deformation weight (for Envelope deform only)

float in [0, 1000], default 0.0

Location of head end of the bone relative to its parent

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Location of head end of the bone relative to armature

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Radius of head of bone (for Envelope deform only)

float in [-inf, inf], default 0.0

Bone is not visible when it is in Edit Mode

boolean, default False

Bone is able to be selected

boolean, default False

Specifies how the bone inherits scaling from the parent bone

FULL Full – Inherit all effects of parent scaling.

FIX_SHEAR Fix Shear – Inherit scaling, but remove shearing of the child in the rest orientation.

ALIGNED Aligned – Rotate non-uniform parent scaling to align with the child, applying parent X scale to child X axis, and so forth.

AVERAGE Average – Inherit uniform scaling representing the overall change in the volume of the parent.

NONE None – Completely ignore parent scaling.

NONE_LEGACY None (Legacy) – Ignore parent scaling without compensating for parent shear. Replicates the effect of disabling the original Inherit Scale checkbox..

enum in ['FULL', 'FIX_SHEAR', 'ALIGNED', 'AVERAGE', 'NONE', 'NONE_LEGACY'], default 'FULL'

float in [-inf, inf], default 0.0, (readonly)

mathutils.Matrix of 3 * 3 items in [-inf, inf], default ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)), (readonly)

4×4 bone matrix relative to armature

mathutils.Matrix of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)), (readonly)

string, default “”, (never None)

Parent bone (in same Armature)

Bone is always displayed in wireframe regardless of viewport shading mode (useful for non-obstructive custom bone shapes)

boolean, default False

Location of tail end of the bone relative to its parent

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Location of tail end of the bone relative to armature

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Radius of tail of bone (for Envelope deform only)

float in [-inf, inf], default 0.0

When bone has a parent, bone’s head is stuck to the parent’s tail

boolean, default False, (readonly)

When bone does not have a parent, it receives cyclic offset effects (Deprecated)

boolean, default False

Enable Bone to deform geometry

boolean, default False

Add Roll Out of the Start Handle bone to the Roll In value

boolean, default False

When deforming bone, multiply effects of Vertex Group weights with Envelope influence

boolean, default False

Bone inherits rotation or scale from parent bone

boolean, default False

Bone location is set in local space

boolean, default False

Object children will use relative transform, like deform

boolean, default False

Multiply the final easing values by the Scale In/Out Y factors

boolean, default False

The name of this bone before any . character.

The midpoint between the head and the tail.

A list of all children from this bone.

Takes O(len(bones)**2) time.

Returns a chain of children with the same base name as this bone. Only direct chains are supported, forks caused by multiple children with matching base names will terminate the function and not be returned.

Takes O(len(bones)**2) time.

A list of parents, starting with the immediate parent.

The direction this bone is pointing. Utility function for (tail - head)

Vector pointing down the x-axis of the bone.

Vector pointing down the y-axis of the bone.

Vector pointing down the z-axis of the bone.

DEBUG ONLY. Internal access to runtime-defined RNA data storage, intended solely for testing and debugging purposes. Do not access it in regular scripting work, and in particular, do not assume that it contains writable data

do_create (boolean, (optional)) – Ensure that system properties are created if they do not exist yet

The system properties root container, or None if there are no system properties stored in this data yet, and its creation was not requested

Calculate bone envelope at given point

point (mathutils.Vector of 3 items in [-inf, inf]) – Point, Position in 3d space to evaluate

Factor, Envelope factor

Transform a matrix from Local to Pose space (or back), taking into account options like Inherit Scale and Local Location. Unlike Object.convert_space, this uses custom rest and pose matrices provided by the caller. If the parent matrices are omitted, the bone is assumed to have no parent.

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf]) – The matrix to transform

matrix_local (mathutils.Matrix of 4 * 4 items in [-inf, inf]) – The custom rest matrix of this bone (Bone.matrix_local)

parent_matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – The custom pose matrix of the parent bone (PoseBone.matrix)

parent_matrix_local (mathutils.Matrix of 4 * 4 items in [-inf, inf], (optional)) – The custom rest matrix of the parent bone (Bone.matrix_local)

invert (boolean, (optional)) – Convert from Pose to Local space

The transformed matrix

mathutils.Matrix of 4 * 4 items in [-inf, inf]

This method enables conversions between Local and Pose space for bones in the middle of updating the armature without having to update dependencies after each change, by manually carrying updated matrices in a recursive walk.

Convert the axis + roll representation to a matrix

axis (mathutils.Vector of 3 items in [-inf, inf], (never None)) – The main axis of the bone (tail - head)

roll (float in [-inf, inf]) – The roll of the bone

The resulting orientation matrix

mathutils.Matrix of 3 * 3 items in [-inf, inf]

Convert a rotational matrix to the axis + roll representation. Note that the resulting value of the roll may not be as expected if the matrix has shear or negative determinant.

matrix (mathutils.Matrix of 3 * 3 items in [-inf, inf], (never None)) – The orientation matrix of the bone

axis (float array of 3 items in [-inf, inf], (optional)) – The optional override for the axis (finds closest approximation for the matrix)

result_axis, The main axis of the bone, mathutils.Vector of 3 items in [-inf, inf] result_roll, The roll of the bone, float in [-inf, inf]

result_axis, The main axis of the bone, mathutils.Vector of 3 items in [-inf, inf]

result_roll, The roll of the bone, float in [-inf, inf]

(mathutils.Vector of 3 items in [-inf, inf], float in [-inf, inf])

The same as ‘bone in other_bone.parent_recursive’ but saved generating a list.

Utility function to add vec to the head and tail of this bone.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

bpy.context.active_bone

Bone.bbone_custom_handle_end

Bone.bbone_custom_handle_start

**Examples:**

Example 1 (python):
```python
def set_pose_matrices(obj, matrix_map):
    "Assign pose space matrices of all bones at once, ignoring constraints."

    def rec(pbone, parent_matrix):
        if pbone.name in matrix_map:
            matrix = matrix_map[pbone.name]

            # # Instead of:
            # pbone.matrix = matrix
            # bpy.context.view_layer.update()

            # Compute and assign local matrix, using the new parent matrix.
            if pbone.parent:
                pbone.matrix_basis = pbone.bone.convert_local_to_pose(
                    matrix,
                    pbone.bone.matrix_local,
                    parent_matrix=parent_matrix,
                    parent_matrix_local=pbone.parent.bone.matrix_local,
                    invert=True
                )
            else:
                pbone.matrix_basis = pbone.bone.convert_local_to_pose(
                    matrix,
                    pbone.bone.matrix_local,
                    invert=True
                )
        else:
            # Compute the updated pose matrix from local and new parent matrix.
            if pbone.parent:
                matrix = pbone.bone.convert_local_to_pose(
                    pbone.matrix_basis,
                    pbone.bone.matrix_local,
                    parent_matrix=parent_matrix,
                    parent_matrix_local=pbone.parent.bone.matrix_local,
                )
            else:
                matrix = pbone.bone.convert_local_to_pose(
                    pbone.matrix_basis,
                    pbone.bone.matrix_local,
                )

        # Recursively process children, passing the new matrix through.
        for child in pbone.children:
            rec(child, matrix)

    # Scan all bone trees from their roots.
    for pbone in obj.pose.bones:
        if not pbone.parent:
            rec(pbone, None)
```

---

## BoneCollection(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoneCollection.html

**Contents:**
- BoneCollection(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Bone collection in an Armature data-block

Bones assigned to this bone collection. In armature edit mode this will always return an empty list of bones, as the bone collection memberships are only synchronized when exiting edit mode.

bpy_prop_collection of Bone, (readonly)

Index of this collection into its parent’s list of children. Note that finding this index requires a scan of all the bone collections, so do access this with care.

int in [-inf, inf], default 0

bpy_prop_collection of BoneCollection, (readonly)

Index of this bone collection in the armature.collections_all array. Note that finding this index requires a scan of all the bone collections, so do access this with care.

int in [-inf, inf], default 0, (readonly)

This collection is owned by a local Armature, or was added via a library override in the current blend file

boolean, default False, (readonly)

This bone collection is expanded in the bone collections tree view

boolean, default False

This collection was added via a library override in the current blend file

boolean, default False, (readonly)

Show only this bone collection, and others also marked as ‘solo’

boolean, default False

Bones in this collection will be visible in pose/object mode

boolean, default False

True when all of the ancestors of this bone collection are marked as visible; always True for root bone collections

boolean, default False, (readonly)

Whether this bone collection is effectively visible in the viewport. This is True when this bone collection and all of its ancestors are visible, or when it is marked as ‘solo’.

boolean, default False, (readonly)

Unique within the Armature

string, default “”, (never None)

Parent bone collection. Note that accessing this requires a scan of all the bone collections to find the parent.

A set of all bones assigned to this bone collection and its child collections.

DEBUG ONLY. Internal access to runtime-defined RNA data storage, intended solely for testing and debugging purposes. Do not access it in regular scripting work, and in particular, do not assume that it contains writable data

do_create (boolean, (optional)) – Ensure that system properties are created if they do not exist yet

The system properties root container, or None if there are no system properties stored in this data yet, and its creation was not requested

Assign the given bone to this collection

bone (AnyType) – Bone, PoseBone, or EditBone to assign to this collection

Assigned, Whether the bone was actually assigned; will be false if the bone was already member of the collection

Remove the given bone from this collection

bone (AnyType) – Bone, PoseBone, or EditBone to remove from this collection

Unassigned, Whether the bone was actually removed; will be false if the bone was not a member of the collection to begin with

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Armature.collections_all

BoneCollection.children

BoneCollection.parent

BoneCollections.active

BoneCollections.remove

---

## BoneCollectionMemberships(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoneCollectionMemberships.html

**Contents:**
- BoneCollectionMemberships(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

The Bone Collections that contain this Bone

Remove this bone from all bone collections

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BoneCollections(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoneCollections.html

**Contents:**
- BoneCollections(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

The Bone Collections of this Armature

Armature’s active bone collection

The index of the Armature’s active bone collection; -1 when there is no active collection. Note that this is indexing the underlying array of bone collections, which may not be in the order you expect. Root collections are listed first, and siblings are always sequential. Apart from that, bone collections can be in any order, and thus incrementing or decrementing this index can make the active bone collection jump around in unexpected ways. For a more predictable interface, use active or active_name.

int in [-inf, inf], default 0

The name of the Armature’s active bone collection; empty when there is no active collection

string, default “”, (never None)

Read-only flag that indicates there is at least one bone collection marked as ‘solo’

boolean, default False, (readonly)

Add a new empty bone collection to the armature

name (string, (never None)) – Name, Name of the new collection. Blender will ensure it is unique within the collections of the Armature.

parent (BoneCollection, (optional)) – Parent Collection, If not None, the new bone collection becomes a child of this collection

Newly created bone collection

Remove the bone collection from the armature. If this bone collection has any children, they will be reassigned to their grandparent; in other words, the children will take the place of the removed bone collection.

bone_collection (BoneCollection) – Bone Collection, The bone collection to remove

Move a bone collection to a different position in the collection list. This can only be used to reorder siblings, and not to change parent-child relationships.

from_index (int in [-inf, inf]) – From Index, Index to move

to_index (int in [-inf, inf]) – To Index, Target index

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BoneColor(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoneColor.html

**Contents:**
- BoneColor(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Theme color or custom color of a bone

The custom bone colors, used when palette is ‘CUSTOM’

ThemeBoneColorSet, (readonly, never None)

A color palette is user-defined, instead of using a theme-defined one

boolean, default False, (readonly)

enum in ['DEFAULT', 'THEME01', 'THEME02', 'THEME03', 'THEME04', 'THEME05', 'THEME06', 'THEME07', 'THEME08', 'THEME09', 'THEME10', 'THEME11', 'THEME12', 'THEME13', 'THEME14', 'THEME15', 'THEME16', 'THEME17', 'THEME18', 'THEME19', 'THEME20', 'CUSTOM'], default 'DEFAULT'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BoolAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoolAttribute.html

**Contents:**
- BoolAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, Attribute

Geometry attribute that stores booleans

bpy_prop_collection of BoolAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

MeshUVLoopLayer.pin_ensure

---

## BoolAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoolAttributeValue.html

**Contents:**
- BoolAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Bool value in geometry attribute

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## BoolProperty(Property)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BoolProperty.html

**Contents:**
- BoolProperty(Property)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Property

RNA boolean property definition

Length of each dimension of the array

int array of 3 items in [0, inf], default (0, 0, 0), (readonly)

Maximum length of the array, 0 means unlimited

int in [0, inf], default 0, (readonly)

Default value for this number

boolean, default False, (readonly)

Default value for this array

boolean array of 3 items, default (False, False, False), (readonly)

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Property.translation_context

Property.is_animatable

Property.is_overridable

Property.is_argument_optional

Property.is_never_none

Property.is_skip_save

Property.is_skip_preset

Property.is_registered

Property.is_registered_optional

Property.is_enum_flag

Property.is_library_editable

Property.is_path_output

Property.is_path_supports_blend_relative

Property.is_path_supports_templates

Property.is_deprecated

Property.deprecated_note

Property.deprecated_version

Property.deprecated_removal_version

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Property.bl_rna_get_subclass

Property.bl_rna_get_subclass_py

---

## BooleanModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BooleanModifier.html

**Contents:**
- BooleanModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Boolean operations modifier

Use mesh objects in this collection for Boolean operation

Debugging options, only when started with ‘-d’

enum set in {'SEPARATE', 'NO_DISSOLVE', 'NO_CONNECT_REGIONS'}, default set()

Threshold for checking overlapping geometry

float in [0, 1], default 1e-06

Method for setting materials on the new faces

INDEX Index Based – Set the material on new faces based on the order of the material slot lists. If a material does not exist on the modifier object, the face will use the same material slot or the first if the object does not have enough slots..

TRANSFER Transfer – Transfer materials from non-empty slots to the result mesh, adding new materials as necessary. For empty slots, fall back to using the same material index as the operand mesh..

enum in ['INDEX', 'TRANSFER'], default 'INDEX'

Mesh object to use for Boolean operation

OBJECT Object – Use a mesh object as the operand for the Boolean operation.

COLLECTION Collection – Use a collection of mesh objects as the operand for the Boolean operation.

enum in ['OBJECT', 'COLLECTION'], default 'OBJECT'

INTERSECT Intersect – Keep the part of the mesh that is common between all operands.

UNION Union – Combine meshes in an additive way.

DIFFERENCE Difference – Combine meshes in a subtractive way.

enum in ['INTERSECT', 'UNION', 'DIFFERENCE'], default 'DIFFERENCE'

Method for calculating booleans

FLOAT Float – Simple solver with good performance, without support for overlapping geometry.

EXACT Exact – Slower solver with the best results for coplanar faces.

MANIFOLD Manifold – Fastest solver that works only on manifold meshes but gives better results.

enum in ['FLOAT', 'EXACT', 'MANIFOLD'], default 'EXACT'

Better results when there are holes (slower)

boolean, default False

Allow self-intersection in operands

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## BrushCapabilities(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCapabilities.html

**Contents:**
- BrushCapabilities(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Read-only indications of supported operations

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.brush_capabilities

---

## BrushCapabilitiesImagePaint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCapabilitiesImagePaint.html

**Contents:**
- BrushCapabilitiesImagePaint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Read-only indications of supported operations

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.image_paint_capabilities

---

## BrightContrastModifier(StripModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrightContrastModifier.html

**Contents:**
- BrightContrastModifier(StripModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, StripModifier

Bright/contrast modifier data for sequence strip

Adjust the luminosity of the colors

float in [-inf, inf], default 0.0

Adjust the difference in luminosity between pixels

float in [-100, 100], default 0.0

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

StripModifier.show_expanded

StripModifier.input_mask_type

StripModifier.mask_time

StripModifier.input_mask_strip

StripModifier.input_mask_id

StripModifier.is_active

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

StripModifier.bl_rna_get_subclass

StripModifier.bl_rna_get_subclass_py

---

## Brush(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Brush.html

**Contents:**
- Brush(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Brush data-block for storing brush settings for painting and sculpting

Ratio between the brush radius and the radius that is going to be used to sample the area center

float in [0, 2], default 0.5

Amount of smoothing to automatically apply to each stroke

float in [0, 1], default 0.0

Distance where boundary edge automasking is going to protect vertices from the fully masked edge

int in [1, 20], default 1

The number of times the cavity mask is blurred

int in [0, 25], default 0

Curve used for the sensitivity

CurveMapping, (readonly)

The contrast of the cavity mask

float in [0, 5], default 1.0

Extend the angular range with a falloff gradient

float in [0.0001, 1], default 0.25

The range of angles that will be affected

float in [0.0001, 3.14159], default 0.349066

Extend the angular range with a falloff gradient

float in [0.0001, 1], default 0.25

The range of angles that will be affected

float in [0.0001, 3.14159], default 1.5708

MIX Mix – Use Mix blending mode while painting.

DARKEN Darken – Use Darken blending mode while painting.

MUL Multiply – Use Multiply blending mode while painting.

COLORBURN Color Burn – Use Color Burn blending mode while painting.

LINEARBURN Linear Burn – Use Linear Burn blending mode while painting.

LIGHTEN Lighten – Use Lighten blending mode while painting.

SCREEN Screen – Use Screen blending mode while painting.

COLORDODGE Color Dodge – Use Color Dodge blending mode while painting.

ADD Add – Use Add blending mode while painting.

OVERLAY Overlay – Use Overlay blending mode while painting.

SOFTLIGHT Soft Light – Use Soft Light blending mode while painting.

HARDLIGHT Hard Light – Use Hard Light blending mode while painting.

VIVIDLIGHT Vivid Light – Use Vivid Light blending mode while painting.

LINEARLIGHT Linear Light – Use Linear Light blending mode while painting.

PINLIGHT Pin Light – Use Pin Light blending mode while painting.

DIFFERENCE Difference – Use Difference blending mode while painting.

EXCLUSION Exclusion – Use Exclusion blending mode while painting.

SUB Subtract – Use Subtract blending mode while painting.

HUE Hue – Use Hue blending mode while painting.

SATURATION Saturation – Use Saturation blending mode while painting.

COLOR Color – Use Color blending mode while painting.

LUMINOSITY Value – Use Value blending mode while painting.

ERASE_ALPHA Erase Alpha – Erase alpha while painting.

ADD_ALPHA Add Alpha – Add alpha while painting.

enum in ['MIX', 'DARKEN', 'MUL', 'COLORBURN', 'LINEARBURN', 'LIGHTEN', 'SCREEN', 'COLORDODGE', 'ADD', 'OVERLAY', 'SOFTLIGHT', 'HARDLIGHT', 'VIVIDLIGHT', 'LINEARLIGHT', 'PINLIGHT', 'DIFFERENCE', 'EXCLUSION', 'SUB', 'HUE', 'SATURATION', 'COLOR', 'LUMINOSITY', 'ERASE_ALPHA', 'ADD_ALPHA'], default 'MIX'

Radius of kernel used for soften and sharpen in pixels

int in [1, 10000], default 2

enum in ['BOX', 'GAUSSIAN'], default 'GAUSSIAN'

Deformation type that is used in the brush

enum in ['BEND', 'EXPAND', 'INFLATE', 'GRAB', 'TWIST', 'SMOOTH'], default 'BEND'

How the brush falloff is applied across the boundary

CONSTANT Constant – Applies the same deformation in the entire boundary.

RADIUS Brush Radius – Applies the deformation in a localized area limited by the brush radius.

LOOP Loop – Applies the brush falloff in a loop pattern.

LOOP_INVERT Loop and Invert – Applies the falloff radius in a loop pattern, inverting the displacement direction in each pattern repetition.

enum in ['CONSTANT', 'RADIUS', 'LOOP', 'LOOP_INVERT'], default 'CONSTANT'

Offset of the boundary origin in relation to the brush radius

float in [0, 30], default 0.0

BrushCapabilities, (readonly, never None)

How much the cloth preserves the original shape, acting as a soft body

float in [0, 1], default 0.0

How much the applied forces are propagated through the cloth

float in [0.01, 1], default 0.01

Deformation type that is used in the brush

enum in ['DRAG', 'PUSH', 'PINCH_POINT', 'PINCH_PERPENDICULAR', 'INFLATE', 'GRAB', 'EXPAND', 'SNAKE_HOOK'], default 'DRAG'

Shape used in the brush to apply force to the cloth

enum in ['RADIAL', 'PLANE'], default 'RADIAL'

Mass of each simulation particle

float in [0.01, 2], default 1.0

Area to apply deformation falloff to the effects of the simulation

float in [0, 1], default 0.75

Factor added relative to the size of the radius to limit the cloth simulation effects

float in [0.1, 10], default 2.5

Part of the mesh that is going to be simulated when the stroke is active

LOCAL Local – Simulates only a specific area around the brush limited by a fixed radius.

GLOBAL Global – Simulates the entire mesh.

DYNAMIC Dynamic – The active simulation area moves with the brush.

enum in ['LOCAL', 'GLOBAL', 'DYNAMIC'], default 'LOCAL'

mathutils.Color of 3 items in [0, inf], default (1.0, 1.0, 1.0)

Use single color or gradient when painting

COLOR Color – Paint with a single color.

GRADIENT Gradient – Paint with a gradient.

enum in ['COLOR', 'GRADIENT'], default 'COLOR'

How much the crease brush pinches

float in [0, 1], default 0.5

Color of cursor when adding

float array of 4 items in [0, inf], default (1.0, 0.39, 0.39, 0.9)

Color of cursor when subtracting

float array of 4 items in [0, inf], default (0.39, 0.39, 1.0, 0.9)

int in [0, 100], default 33

Editable falloff curve

CurveMapping, (readonly, never None)

enum in Brush Curve Preset Items, default 'CUSTOM'

Curve used to map pressure to brush jitter

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used to map pressure to brush size

CurveMapping, (readonly)

Curve used to map pressure to brush strength

CurveMapping, (readonly)

enum in Brush Curves Sculpt Brush Type Items, default 'COMB'

BrushCurvesSculptSettings, (readonly)

Ratio of samples in a cycle that the brush is enabled

float in [0, 1], default 1.0

Length of a dash cycle measured in stroke samples

int in [1, 10000], default 20

How the deformation of the brush will affect the object

GEOMETRY Geometry – Brush deformation displaces the vertices of the mesh.

CLOTH_SIM Cloth Simulation – Brush deforms the mesh by deforming the constraints of a cloth simulation.

enum in ['GEOMETRY', 'CLOTH_SIM'], default 'GEOMETRY'

Amount of random elements that are going to be affected by the brush

float in [0, 1], default 0.0

ADD Add – Add effect of brush.

SUBTRACT Subtract – Subtract effect of brush.

enum in ['ADD', 'SUBTRACT'], default 'ADD'

Maximum distance to search for disconnected loose parts in the mesh

float in [0, 10], default 0.1

Deformation type that is used in the brush

enum in ['GRAB', 'GRAB_BISCALE', 'GRAB_TRISCALE', 'SCALE', 'TWIST'], default 'GRAB'

Poisson ratio for elastic deformation. Higher values preserve volume more, but also lead to more bulging.

float in [0, 0.9], default 0.0

Paint most on faces pointing towards the view according to this angle

float in [0, 1.5708], default 0.0

Use projected or spherical falloff

SPHERE Sphere – Apply brush influence in a Sphere, outwards from the center.

PROJECTED Projected – Apply brush influence in a 2D circle, projected from the view.

enum in ['SPHERE', 'PROJECTED'], default 'SPHERE'

Threshold above which filling is not propagated

float in [0, 100], default 0.2

Amount of paint that is applied per stroke sample

float in [0, 1], default 0.0

enum in Brush Gpencil Types Items, default 'DRAW'

enum in Brush Gpencil Sculpt Types Items, default 'SMOOTH'

BrushGpencilSettings, (readonly)

enum in Brush Gpencil Vertex Types Items, default 'DRAW'

enum in Brush Gpencil Weight Types Items, default 'WEIGHT'

Spacing before brush gradient goes full circle

int in [1, 10000], default 0

ColorRamp, (readonly)

enum in ['LINEAR', 'RADIAL'], default 'LINEAR'

enum in ['PRESSURE', 'SPACING_REPEAT', 'SPACING_CLAMP'], default 'PRESSURE'

How close the brush falloff starts from the edge of the brush

float in [0, 1], default 0.0

Indicates that there are any user visible changes since the brush has been imported or read from the file

boolean, default False, (readonly)

Affectable height of brush (i.e. the layer height for the layer tool)

float in [0, 1], default 0.5

Color jitter effect on hue

float in [0, 1], default 0.0

enum in Brush Image Brush Type Items, default 'DRAW'

BrushCapabilitiesImagePaint, (readonly, never None)

Number of input samples to average together to smooth the brush stroke

int in [1, 64], default 1

Invert the modulation of pressure in density

boolean, default False

Invert the modulation of pressure in flow

boolean, default False

Invert the modulation of pressure in hardness

boolean, default False

Use Scrape or Fill brush when inverting this brush instead of inverting its displacement direction

boolean, default False

Invert the modulation of pressure in wet mix

boolean, default False

Invert the modulation of pressure in wet persistence

boolean, default False

Jitter the position of the brush while painting

float in [0, 1000], default 0.0

Jitter the position of the brush in pixels while painting

int in [0, 1000000], default 0

Jitter in screen space or relative to brush size

VIEW View – Jittering happens in screen space, in pixels.

BRUSH Brush – Jittering happens relative to the brush size.

enum in ['VIEW', 'BRUSH'], default 'VIEW'

int in [0, 100], default 33

Dimensions of mask stencil in viewport

mathutils.Vector of 2 items in [-inf, inf], default (256.0, 256.0)

Position of mask stencil in viewport

mathutils.Vector of 2 items in [-inf, inf], default (256.0, 256.0)

BrushTextureSlot, (readonly)

enum in ['DRAW', 'SMOOTH'], default 'DRAW'

Angle between the planes of the crease

float in [0, 160], default 0.0

Ratio between the brush radius and the radius that is going to be used to sample the normal

float in [0, 2], default 0.5

How much grab will pull vertices out of surface during a grab

float in [0, 1], default 0.0

The maximum distance below the plane for affected vertices. Increasing the depth affects vertices farther below the plane.

float in [0, 1], default 0.0

The maximum distance above the plane for affected vertices. Increasing the height affects vertices farther above the plane.

float in [0, 1], default 1.0

INVERT_DISPLACEMENT Invert Displacement – Displace the vertices away from the plane..

SWAP_DEPTH_AND_HEIGHT Swap Height and Depth – Swap the roles of Height and Depth..

enum in ['INVERT_DISPLACEMENT', 'SWAP_DEPTH_AND_HEIGHT'], default 'INVERT_DISPLACEMENT'

Adjust plane on which the brush acts towards or away from the object surface

float in [-2, 2], default 0.0

If a vertex is further away from offset plane than this, then it is not affected

float in [0, 1], default 0.5

Deformation type that is used in the brush

enum in ['ROTATE_TWIST', 'SCALE_TRANSLATE', 'SQUASH_STRETCH'], default 'ROTATE_TWIST'

Number of segments of the inverse kinematics chain that will deform the mesh

int in [1, 20], default 1

Offset of the pose origin in relation to the brush radius

float in [0, 2], default 0.0

Method to set the rotation origins for the segments of the brush

TOPOLOGY Topology – Sets the rotation origin automatically using the topology and shape of the mesh as a guide.

FACE_SETS Face Sets – Creates a pose segment per face sets, starting from the active face set.

FACE_SETS_FK Face Sets FK – Simulates an FK deformation using the Face Set under the cursor as control.

enum in ['TOPOLOGY', 'FACE_SETS', 'FACE_SETS_FK'], default 'TOPOLOGY'

Smooth iterations applied after calculating the pose factor of each vertex

int in [0, 100], default 4

How much grab will follow cursor rotation

float in [0, 10], default 0.0

Interval between paints for Airbrush

float in [0.0001, 10000], default 0.1

Color jitter effect on saturation

float in [0, 1], default 0.0

enum in Brush Sculpt Brush Type Items, default 'DRAW'

BrushCapabilitiesSculpt, (readonly, never None)

enum in ['AREA', 'VIEW', 'X', 'Y', 'Z'], default 'AREA'

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

Threshold below which, no sharpening is done

float in [0, 100], default 0.0

Preview the scrape planes in the cursor during the stroke

boolean, default False

Diameter of the brush in pixels

int in [1, 10000], default 70

Deformation type that is used in the brush

enum in ['DRAG', 'PINCH', 'EXPAND'], default 'DRAG'

Deformation type that is used in the brush

enum in ['DRAG', 'PINCH', 'EXPAND'], default 'DRAG'

Deformation type that is used in the brush

LAPLACIAN Laplacian – Smooths the surface and the volume.

SURFACE Surface – Smooths the surface of the mesh, preserving the volume.

enum in ['LAPLACIAN', 'SURFACE'], default 'LAPLACIAN'

Higher values give a smoother stroke

float in [0.5, 0.99], default 0.9

Minimum distance from last point before stroke continues

int in [10, 200], default 75

Deformation type that is used in the brush

FALLOFF Radius Falloff – Applies the brush falloff in the tip of the brush.

ELASTIC Elastic – Modifies the entire mesh using elastic deform.

enum in ['FALLOFF', 'ELASTIC'], default 'FALLOFF'

Spacing between brush daubs as a percentage of brush diameter

int in [1, 1000], default 10

Stabilize the orientation of the brush plane.

float in [0, 1], default 0.0

Stabilize the center of the brush plane.

float in [0, 1], default 0.0

Dimensions of stencil in viewport

mathutils.Vector of 2 items in [-inf, inf], default (256.0, 256.0)

Position of stencil in viewport

mathutils.Vector of 2 items in [-inf, inf], default (256.0, 256.0)

How powerful the effect of the brush is when applied

float in [0, 10], default 1.0

DOTS Dots – Apply paint on each mouse move step.

DRAG_DOT Drag Dot – Allows a single dot to be carefully positioned.

SPACE Space – Limit brush application to the distance specified by spacing.

AIRBRUSH Airbrush – Keep applying paint effect while holding mouse (spray).

ANCHORED Anchored – Keep the brush anchored to the initial location.

LINE Line – Draw a line with dabs separated according to spacing.

CURVE Curve – Define the stroke curve with a Bézier curve (dabs are separated according to spacing).

enum in ['DOTS', 'DRAG_DOT', 'SPACE', 'AIRBRUSH', 'ANCHORED', 'LINE', 'CURVE'], default 'DOTS'

How much the position of each individual vertex influences the final result

float in [0, 1], default 0.0

Number of smoothing iterations per brush step

int in [1, 10], default 0

How much of the original shape is preserved when smoothing

float in [0, 1], default 0.0

int in [0, 100], default 33

Value added to texture samples

float in [-1, 1], default 0.0

BrushTextureSlot, (readonly)

How much the tilt of the pen will affect the brush. Negative values indicate inverting the tilt directions.

float in [-1, 1], default 0.0

Roundness of the brush tip

float in [0, 1], default 1.0

Scale of the brush tip in the X axis

float in [0.0001, 1], default 1.0

Automatically align edges to the brush direction to generate cleaner topology and define sharp features. Best used on low-poly meshes as it has a performance impact.

float in [0, 1], default 0.0

Diameter of brush in Blender units

float in [0.001, inf], default 0.1

Accumulate stroke daubs on top of each other

boolean, default False

Space daubs according to surface orientation instead of screen space

boolean, default False

Keep applying paint effect while holding mouse (spray)

boolean, default False

When this is disabled, lock alpha while painting

boolean, default True

Keep the brush anchored to the initial location

boolean, default False

Do not affect non manifold boundary edges

boolean, default False

Do not affect vertices that belong to a Face Set boundary

boolean, default False

Do not affect vertices on peaks, based on the surface curvature

boolean, default False

Do not affect vertices within crevices, based on the surface curvature

boolean, default False

boolean, default False

Affect only vertices that share Face Sets with the active vertex

boolean, default False

Affect only vertices with a similar normal to where the stroke starts

boolean, default False

Affect only vertices connected to the active vertex under the brush

boolean, default False

Affect only vertices with a normal that faces the viewer

boolean, default False

Only affect vertices that are not occluded by other faces (slower performance)

boolean, default False

Collide with objects during the simulation

boolean, default False

Lock the position of the vertices in the simulation falloff area to avoid artifacts and create a softer transition with unaffected areas

boolean, default False

Handle each pixel color as individual vector for displacement (area plane mapping only)

boolean, default False

boolean, default False

Affect only topologically connected elements

boolean, default False

Show cursor in viewport

boolean, default False

Don’t show overlay during a stroke

boolean, default False

Define the stroke curve with a Bézier curve. Dabs are separated according to spacing.

boolean, default False

Use pressure to modulate density

boolean, default False

Drag anchor brush from edge-to-edge

boolean, default False

Use pressure to modulate flow

boolean, default False

Brush only affects vertices that face the viewer

boolean, default False

Blend brush influence by how much they face the front

boolean, default False

Apply the maximum grab strength to the active vertex instead of the cursor location

boolean, default False

Grabs trying to automask the silhouette of the object

boolean, default False

Use pressure to modulate hardness

boolean, default False

Lighter pressure causes more smoothing to be applied

boolean, default False

Draw a line with dabs separated according to spacing

boolean, default False

Measure brush size relative to the view or the scene

VIEW View – Measure brush size relative to the view.

SCENE Scene – Measure brush size relative to the scene.

enum in ['VIEW', 'SCENE'], default 'VIEW'

The angle between the planes changes during the stroke to fit the surface under the cursor

boolean, default False

Enable tablet pressure sensitivity for offset

boolean, default False

When locked keep using normal of surface where stroke was initiated

boolean, default False

When locked keep using the plane origin of surface where stroke was initiated

boolean, default False

Smooths the edges of the strokes

boolean, default True

Use this brush in Grease Pencil drawing mode

boolean, default False

Use this brush in texture paint mode

boolean, default True

Use this brush in sculpt mode

boolean, default True

Use this brush in sculpt curves mode

boolean, default False

Use this brush in UV sculpt mode

boolean, default False

Use this brush in vertex paint mode

boolean, default True

Use this brush in weight paint mode

boolean, default True

Sculpt on a persistent layer of the mesh

boolean, default False

Limit the distance from the offset plane that a vertex can be affected

boolean, default False

Keep the position of the last segment in the IK chain fixed

boolean, default False

Do not rotate the segment when using the scale deform mode

boolean, default False

Enable tablet pressure sensitivity for area radius

boolean, default False

Enable tablet pressure sensitivity for jitter

boolean, default False

Pen pressure makes texture influence smaller

enum in ['NONE', 'RAMP', 'CUTOFF'], default 'NONE'

Enable tablet pressure sensitivity for size

boolean, default False

Enable tablet pressure sensitivity for spacing

boolean, default False

Enable tablet pressure sensitivity for strength

boolean, default True

Show texture in viewport

boolean, default False

Don’t show overlay during a stroke

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Allow a single dot to be carefully positioned

boolean, default False

Calculate the brush spacing using view or scene distance

VIEW View – Calculate brush spacing relative to the view.

SCENE Scene – Calculate brush spacing relative to the scene using the stroke location.

enum in ['VIEW', 'SCENE'], default 'VIEW'

Show texture in viewport

boolean, default False

Don’t show overlay during a stroke

boolean, default False

Brush lags behind mouse and follows a smoother path

boolean, default False

Limit brush application to the distance specified by spacing

boolean, default True

Automatically adjust strength to give consistent results for different spacings

boolean, default True

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use this brush in Grease Pencil vertex color mode

boolean, default False

Use pressure to modulate wet mix

boolean, default False

Use pressure to modulate wet persistence

boolean, default False

Color jitter effect on value

float in [0, 1], default 0.0

enum in Brush Vertex Brush Type Items, default 'DRAW'

BrushCapabilitiesVertexPaint, (readonly, never None)

Vertex weight when brush is applied

float in [0, 1], default 1.0

enum in Brush Weight Brush Type Items, default 'DRAW'

BrushCapabilitiesWeightPaint, (readonly, never None)

Amount of paint that is picked from the surface into the brush color

float in [0, 1], default 0.0

Ratio between the brush radius and the radius that is going to be used to sample the color to blend in wet paint

float in [0, 2], default 0.5

Amount of wet paint that stays in the brush after applying paint to the surface

float in [0, 1], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendDataBrushes.create_gpencil_data

BlendDataBrushes.remove

---

## BrushCapabilitiesSculpt(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCapabilitiesSculpt.html

**Contents:**
- BrushCapabilitiesSculpt(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Read-only indications of which brush operations are supported by the current sculpt tool

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.sculpt_capabilities

---

## BrushCapabilitiesVertexPaint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCapabilitiesVertexPaint.html

**Contents:**
- BrushCapabilitiesVertexPaint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Read-only indications of supported operations

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.vertex_paint_capabilities

---

## BrushCapabilitiesWeightPaint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCapabilitiesWeightPaint.html

**Contents:**
- BrushCapabilitiesWeightPaint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Read-only indications of supported operations

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.weight_paint_capabilities

---

## BrushCurvesSculptSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushCurvesSculptSettings.html

**Contents:**
- BrushCurvesSculptSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Number of curves added by the Add brush

int in [1, inf], default 0

Length of newly added curves when it is not interpolated from other curves

float in [0, inf], default 0.0

Falloff that is applied from the tip to the root of each curve

CurveMapping, (readonly)

Radius of newly added curves when it is not interpolated from other curves

float in [0, inf], default 0.01

How many times the Density brush tries to add a new curve

int in [0, inf], default 0

Determines whether the brush adds or removes curves

AUTO Auto – Either add or remove curves depending on the minimum distance of the curves under the cursor.

ADD Add – Add new curves between existing curves, taking the minimum distance into account.

REMOVE Remove – Remove curves whose root points are too close.

enum in ['AUTO', 'ADD', 'REMOVE'], default 'AUTO'

Goal distance between curve roots for the Density brush

float in [0, inf], default 0.0

Avoid shrinking curves shorter than this length

float in [0, inf], default 0.0

Number of control points in a newly added curve

int in [2, inf], default 0

Use length of the curves in close proximity

boolean, default False

Use the number of points from the curves in close proximity

boolean, default False

Use radius of the curves in close proximity

boolean, default True

Use shape of the curves in close proximity

boolean, default False

Grow or shrink curves by changing their size uniformly instead of using trimming or extrapolation

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.curves_sculpt_settings

---

## BrushTextureSlot(TextureSlot)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushTextureSlot.html

**Contents:**
- BrushTextureSlot(TextureSlot)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, TextureSlot

Texture slot for textures in a Brush data-block

Brush texture rotation

float in [0, 6.28319], default 0.0

boolean, default False, (readonly)

boolean, default False, (readonly)

boolean, default False, (readonly)

enum in ['VIEW_PLANE', 'AREA_PLANE', 'TILED', '3D', 'RANDOM', 'STENCIL'], default 'VIEW_PLANE'

enum in ['VIEW_PLANE', 'TILED', 'RANDOM', 'STENCIL'], default 'VIEW_PLANE'

Brush texture random angle

float in [0, 6.28319], default 6.28319

boolean, default False

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

TextureSlot.blend_type

TextureSlot.default_value

TextureSlot.output_node

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

TextureSlot.bl_rna_get_subclass

TextureSlot.bl_rna_get_subclass_py

Brush.mask_texture_slot

---

## BuildModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BuildModifier.html

**Contents:**
- BuildModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Build effect modifier

Total time the build effect requires

float in [1, 1.04857e+06], default 100.0

Start frame of the effect

float in [-1.04857e+06, 1.04857e+06], default 1.0

Seed for random if used

int in [1, 1048574], default 0

Randomize the faces or edges during build

boolean, default False

Deconstruct the mesh instead of building it

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## BrushGpencilSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.BrushGpencilSettings.html

**Contents:**
- BrushGpencilSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Settings for Grease Pencil brush

Amount of smoothing while drawing

float in [0, 1], default 0.0

Direction of the stroke at which brush gives maximal thickness (0° for horizontal)

float in [-1.5708, 1.5708], default 0.0

Reduce brush thickness by this factor when stroke is perpendicular to ‘Angle’ direction

float in [0, 1], default 0.0

mathutils.Vector of 2 items in [0.01, 1], default (1.0, 1.0)

Preselected mode when using this brush

ACTIVE Active – Use current mode.

MATERIAL Material – Use always material mode.

VERTEXCOLOR Vertex Color – Use always Vertex Color mode.

enum in ['ACTIVE', 'MATERIAL', 'VERTEXCOLOR'], default 'ACTIVE'

The shape of the start and end of the stroke

enum in ['ROUND', 'FLAT'], default 'ROUND'

Curve used for the jitter effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for modulating effect

CurveMapping, (readonly)

Curve used for the sensitivity

CurveMapping, (readonly)

Curve used for the strength

CurveMapping, (readonly)

Number of pixels to expand or contract fill area

int in [-40, 40], default 1

SOFT Dissolve – Erase strokes, fading their points strength and thickness.

HARD Point – Erase stroke points.

STROKE Stroke – Erase entire strokes.

enum in ['SOFT', 'HARD', 'STROKE'], default 'SOFT'

Amount of erasing for strength

float in [0, 100], default 0.0

Amount of erasing for thickness

float in [0, 100], default 0.0

Strokes end extension for closing gaps, use zero to disable

float in [0, 10], default 0.0

Direction of the fill

NORMAL Normal – Fill internal area.

INVERT Inverted – Fill inverted area.

enum in ['NORMAL', 'INVERT'], default 'NORMAL'

Mode to draw boundary limits

BOTH All – Use both visible strokes and edit lines as fill boundary limits.

STROKE Strokes – Use visible strokes as fill boundary limits.

CONTROL Edit Lines – Use edit lines as fill boundary limits.

enum in ['BOTH', 'STROKE', 'CONTROL'], default 'BOTH'

Types of stroke extensions used for closing gaps

EXTEND Extend – Extend strokes in straight lines.

RADIUS Radius – Connect endpoints that are close together.

enum in ['EXTEND', 'RADIUS'], default 'EXTEND'

Factor for fill boundary accuracy, higher values are more accurate but slower

float in [0.05, 8], default 0.0

Layers used as boundaries

VISIBLE Visible – Visible layers.

ACTIVE Active – Only active layer.

ABOVE Layer Above – Layer above active.

BELOW Layer Below – Layer below active.

ALL_ABOVE All Above – All layers above active.

ALL_BELOW All Below – All layers below active.

enum in ['VISIBLE', 'ACTIVE', 'ABOVE', 'BELOW', 'ALL_ABOVE', 'ALL_BELOW'], default 'VISIBLE'

Number of simplify steps (large values reduce fill accuracy)

int in [0, 10], default 0

Threshold to consider color transparent for filling

float in [0, 1], default 0.0

Gradient from the center of Dot and Box strokes (set to 1 for a solid stroke)

float in [0.001, 1], default 1.0

Generated intermediate points for very fast mouse movements (Set to 0 to disable)

int in [0, 10], default 0

Material used for strokes drawn using this brush

Material used for secondary uses for this brush

Thickness of the outline stroke relative to current brush thickness

float in [0, 1], default 0.0

Jitter factor of brush radius for new strokes

float in [0, 100], default 0.0

Amount of smoothing to apply after finish newly created strokes, to reduce jitter/noise

float in [0, 2], default 0.0

Number of times to smooth newly created strokes

int in [0, 100], default 0

Color strength for new strokes (affect alpha factor of color)

float in [0, 1], default 0.0

Number of times to subdivide newly created strokes, for less jagged strokes

int in [0, 3], default 0

Pin the mode to the brush

boolean, default False

Random factor to modify original hue

float in [0, 1], default 0.0

Randomness factor for pressure in new strokes

float in [0, 1], default 0.0

Random factor to modify original saturation

float in [0, 1], default 0.0

Randomness factor strength in new strokes

float in [0, 1], default 0.0

Random factor to modify original value

float in [0, 1], default 0.0

Show transparent lines to use as boundary for filling

boolean, default True

Show help lines for filling to see boundaries

boolean, default True

Show help lines for stroke extension

boolean, default True

Do not display fill color while drawing the stroke

boolean, default False

Factor of Simplify using adaptive algorithm

float in [0, 100], default 0.0

Threshold in screen space used for the simplify algorithm. Points within this threshold are treated as if they were in a straight line.

float in [0, 10], default 0.0

Only edit the active layer of the object

boolean, default False

Automatically remove fill guide strokes after fill operation

boolean, default True

Check if extend lines collide with strokes

boolean, default False

The brush affects the position of the point

boolean, default False

The brush affects the color strength of the point

boolean, default False

The brush affects the thickness of the point

boolean, default False

The brush affects the UV rotation of the point

boolean, default False

Fill only visible areas in viewport

boolean, default True

Use tablet pressure for jitter

boolean, default False

Keep the caps as they are and don’t flatten them when erasing

boolean, default False

Keep material assigned to brush

boolean, default False

Erase only strokes visible and not occluded

boolean, default False

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Use pressure to modulate randomness

boolean, default False

Convert stroke to outline

boolean, default False

Additional post processing options for new strokes

boolean, default False

Random brush settings

boolean, default False

Draw lines with a delay to allow smooth strokes (press Shift key to override while drawing)

boolean, default True

Use tablet pressure for color strength

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Use randomness at stroke level

boolean, default False

Trim intersecting stroke ends

boolean, default False

Random factor for auto-generated UV rotation

float in [0, 1], default 0.0

Factor used to mix vertex color to get final color

float in [0, 1], default 0.0

Defines how vertex color affect to the strokes

STROKE Stroke – Vertex Color affects to Stroke only.

FILL Fill – Vertex Color affects to Fill only.

BOTH Stroke & Fill – Vertex Color affects to Stroke and Fill.

enum in ['STROKE', 'FILL', 'BOTH'], default 'STROKE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.gpencil_settings

---

## ByteColorAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ByteColorAttribute.html

**Contents:**
- ByteColorAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores RGBA colors as positive integer values using 8-bits per channel

bpy_prop_collection of ByteColorAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## ByteColorAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ByteColorAttributeValue.html

**Contents:**
- ByteColorAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color value in geometry attribute

RGBA color in scene linear color space

float array of 4 items in [0, 1], default (0.0, 0.0, 0.0, 0.0)

RGBA color in sRGB color space

float array of 4 items in [0, 1], default (0.0, 0.0, 0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ByteColorAttribute.data

---

## ByteIntAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ByteIntAttribute.html

**Contents:**
- ByteIntAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores 8-bit integers

bpy_prop_collection of ByteIntAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## ByteIntAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ByteIntAttributeValue.html

**Contents:**
- ByteIntAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

8-bit value in geometry attribute

int in [-128, 127], default 0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ByteIntAttribute.data

---

## CLIP_UL_tracking_objects(UIList)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CLIP_UL_tracking_objects.html

**Contents:**
- CLIP_UL_tracking_objects(UIList)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, UIList

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

UIList.use_filter_show

UIList.use_filter_invert

UIList.use_filter_sort_alpha

UIList.use_filter_sort_reverse

UIList.use_filter_sort_lock

UIList.bitflag_filter_item

UIList.bitflag_item_never_show

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

UIList.bl_system_properties_get

UIList.bl_rna_get_subclass

UIList.bl_rna_get_subclass_py

---

## CacheFile(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CacheFile.html

**Contents:**
- CacheFile(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

int in [0, inf], default 0

Animation data for this data-block

Path to external displacements file

string, default “”, (never None, blend relative // prefix supported)

enum in Object Axis Items, default 'POS_X'

The time to use for looking up the data in the cache file, or to determine which file to use in a file sequence

float in [-1.04857e+06, 1.04857e+06], default 0.0

Subtracted from the current frame to use for looking up the data in the cache file, or to determine which file to use in a file sequence

float in [-1.04857e+06, 1.04857e+06], default 0.0

Whether the cache is separated in a series of files

boolean, default False

CacheFileLayers bpy_prop_collection of CacheFileLayer, (readonly)

Paths of the objects inside the Alembic archive

CacheObjectPaths bpy_prop_collection of CacheObjectPath, (readonly)

Whether to use a custom frame for looking up data in the cache file, instead of using the current scene frame

boolean, default False

Value by which to enlarge or shrink the object with respect to the world’s origin (only applicable through a Transform Cache constraint)

float in [0.0001, 1000], default 1.0

enum in Object Axis Items, default 'POS_X'

Name of the Alembic attribute used for generating motion blur data

string, default “”, (never None)

Define how the velocity vectors are interpreted with regard to time, ‘frame’ means the delta time is 1 frame, ‘second’ means the delta time is 1 / FPS

enum in Velocity Unit Items, default 'FRAME'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendData.cache_files

MeshSequenceCacheModifier.cache_file

TransformCacheConstraint.cache_file

---

## CacheFileLayer(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CacheFileLayer.html

**Contents:**
- CacheFileLayer(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Layer of the cache, used to load or override data from the first the first layer

string, default “”, (never None, blend relative // prefix supported)

Do not load data from this layer

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CacheFileLayers.active

CacheFileLayers.remove

---

## CURVES_UL_attributes(UIList)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CURVES_UL_attributes.html

**Contents:**
- CURVES_UL_attributes(UIList)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, UIList

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

UIList.use_filter_show

UIList.use_filter_invert

UIList.use_filter_sort_alpha

UIList.use_filter_sort_reverse

UIList.use_filter_sort_lock

UIList.bitflag_filter_item

UIList.bitflag_item_never_show

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

UIList.bl_system_properties_get

UIList.bl_rna_get_subclass

UIList.bl_rna_get_subclass_py

---

## CacheFileLayers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CacheFileLayers.html

**Contents:**
- CacheFileLayers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of cache layers

Active layer of the CacheFile

filepath (string, (never None)) – File path to the archive used as a layer

Remove an existing layer from the cache file

layer (CacheFileLayer, (never None)) – Layer to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CacheObjectPath(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CacheObjectPath.html

**Contents:**
- CacheObjectPath(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Path of an object inside of an Alembic archive

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CacheFile.object_paths

---

## CacheObjectPaths(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CacheObjectPaths.html

**Contents:**
- CacheObjectPaths(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of object paths

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CacheFile.active_index

CacheFile.object_paths

---

## Camera(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Camera.html

**Contents:**
- Camera(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Camera data-block for storing camera settings

Camera lens field of view

float in [0.00640536, 3.01675], default 0.69115

Camera lens horizontal field of view

float in [0.00640536, 3.01675], default 0.0

Camera lens vertical field of view

float in [0.00640536, 3.01675], default 0.0

Animation data for this data-block

List of background images

CameraBackgroundImages bpy_prop_collection of CameraBackgroundImage, (readonly)

Radius of the virtual cylinder

float in [1e-05, inf], default 1.0

Maximum Longitude value for the central cylindrical lens

float in [-inf, inf], default 3.14159

Minimum Longitude value for the central cylindrical lens

float in [-inf, inf], default -3.14159

Maximum Height value for the central cylindrical lens

float in [-inf, inf], default 1.0

Minimum Height value for the central cylindrical lens

float in [-inf, inf], default -1.0

Camera far clipping distance

float in [1e-06, inf], default 1000.0

Camera near clipping distance

float in [1e-06, inf], default 0.1

Color and alpha for compositional guide overlays

float array of 4 items in [0, inf], default (0.5, 0.5, 0.5, 1.0)

Compiled bytecode of the custom shader

string, default “”, (never None)

Hash of the compiled bytecode of the custom shader, for quick equality checking

string, default “”, (never None)

Path to the shader defining the custom camera

string, default “”, (never None)

INTERNAL Internal – Use internal text data-block.

EXTERNAL External – Use external file.

enum in ['INTERNAL', 'EXTERNAL'], default 'INTERNAL'

Shader defining the custom camera

Parameters for custom (OSL-based) cameras

CyclesCustomCameraSettings, (readonly)

Apparent size of the Camera object in the 3D View

float in [0.01, 1000], default 1.0

CameraDOFSettings, (readonly)

Field of view for the fisheye lens

float in [0.1745, 31.4159], default 3.14159

Lens focal length (mm)

float in [0.01, 100], default 10.5

Coefficient K0 of the lens polynomial

float in [-inf, inf], default -1.17351e-05

Coefficient K1 of the lens polynomial

float in [-inf, inf], default -0.0199887

Coefficient K2 of the lens polynomial

float in [-inf, inf], default -3.3525e-06

Coefficient K3 of the lens polynomial

float in [-inf, inf], default 3.0993e-06

Coefficient K4 of the lens polynomial

float in [-inf, inf], default -2.61e-08

Maximum latitude (vertical angle) for the equirectangular lens

float in [-1.5708, 1.5708], default 1.5708

Minimum latitude (vertical angle) for the equirectangular lens

float in [-1.5708, 1.5708], default -1.5708

Perspective Camera focal length value in millimeters

float in [1, inf], default 50.0

Unit to edit lens in for the user interface

MILLIMETERS Millimeters – Specify focal length of the lens in millimeters.

FOV Field of View – Specify the lens as the field of view’s angle.

enum in ['MILLIMETERS', 'FOV'], default 'MILLIMETERS'

Maximum longitude (horizontal angle) for the equirectangular lens

float in [-inf, inf], default 3.14159

Minimum longitude (horizontal angle) for the equirectangular lens

float in [-inf, inf], default -3.14159

Orthographic Camera scale (similar to zoom)

float in [0, inf], default 6.0

Distortion to use for the calculation

EQUIRECTANGULAR Equirectangular – Spherical camera for environment maps, also known as Lat Long panorama.

EQUIANGULAR_CUBEMAP_FACE Equiangular Cubemap Face – Single face of an equiangular cubemap.

MIRRORBALL Mirror Ball – Mirror ball mapping for environment maps.

FISHEYE_EQUIDISTANT Fisheye Equidistant – Ideal for fulldomes, ignore the sensor dimensions.

FISHEYE_EQUISOLID Fisheye Equisolid – Similar to most fisheye modern lens, takes sensor dimensions into consideration.

FISHEYE_LENS_POLYNOMIAL Fisheye Lens Polynomial – Defines the lens projection as polynomial to allow real world camera lenses to be mimicked.

CENTRAL_CYLINDRICAL Central Cylindrical – Projection onto a virtual cylinder from its center, similar as a rotating panoramic camera.

enum in ['EQUIRECTANGULAR', 'EQUIANGULAR_CUBEMAP_FACE', 'MIRRORBALL', 'FISHEYE_EQUIDISTANT', 'FISHEYE_EQUISOLID', 'FISHEYE_LENS_POLYNOMIAL', 'CENTRAL_CYLINDRICAL'], default 'FISHEYE_EQUISOLID'

Opacity (alpha) of the darkened overlay in Camera view

float in [0, 1], default 0.5

Method to fit image and field of view angle inside the sensor

AUTO Auto – Fit to the sensor width or height depending on image resolution.

HORIZONTAL Horizontal – Fit to the sensor width.

VERTICAL Vertical – Fit to the sensor height.

enum in ['AUTO', 'HORIZONTAL', 'VERTICAL'], default 'AUTO'

Vertical size of the image sensor area in millimeters

float in [1, inf], default 24.0

Horizontal size of the image sensor area in millimeters

float in [1, inf], default 36.0

Camera horizontal shift

float in [-inf, inf], default 0.0

Camera vertical shift

float in [-inf, inf], default 0.0

Display reference images behind objects in the 3D View

boolean, default False

Display center composition guide inside the camera view

boolean, default False

Display diagonal center composition guide inside the camera view

boolean, default False

Display golden ratio composition guide inside the camera view

boolean, default False

Display golden triangle A composition guide inside the camera view

boolean, default False

Display golden triangle B composition guide inside the camera view

boolean, default False

Display harmony A composition guide inside the camera view

boolean, default False

Display harmony B composition guide inside the camera view

boolean, default False

Display rule of thirds composition guide inside the camera view

boolean, default False

Display the clipping range and focus point on the camera

boolean, default False

Display a line from the Camera to indicate the mist area

boolean, default False

Show the active Camera’s name in Camera view

boolean, default False

Show a darkened overlay outside the image area in Camera view

boolean, default True

Show TV title safe and action safe areas in Camera view

boolean, default False

Show safe areas to fit content in a different aspect ratio

boolean, default False

Show sensor size (film gate) in Camera view

boolean, default False

CameraStereoData, (readonly, never None)

enum in ['PERSP', 'ORTHO', 'PANO', 'CUSTOM'], default 'PERSP'

Return 4 points for the cameras frame (before object transformation)

scene (Scene, (optional)) – Scene to use for aspect calculation, when omitted 1:1 aspect is used

result_1, Result, mathutils.Vector of 3 items in [-inf, inf] result_2, Result, mathutils.Vector of 3 items in [-inf, inf] result_3, Result, mathutils.Vector of 3 items in [-inf, inf] result_4, Result, mathutils.Vector of 3 items in [-inf, inf]

result_1, Result, mathutils.Vector of 3 items in [-inf, inf]

result_2, Result, mathutils.Vector of 3 items in [-inf, inf]

result_3, Result, mathutils.Vector of 3 items in [-inf, inf]

result_4, Result, mathutils.Vector of 3 items in [-inf, inf]

(mathutils.Vector of 3 items in [-inf, inf], mathutils.Vector of 3 items in [-inf, inf], mathutils.Vector of 3 items in [-inf, inf], mathutils.Vector of 3 items in [-inf, inf])

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendDataCameras.remove

RenderEngine.update_custom_camera

---

## CameraBackgroundImage(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CameraBackgroundImage.html

**Contents:**
- CameraBackgroundImage(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Image and settings for display in the 3D View background

Image opacity to blend the image against the background color

float in [0, 1], default 0.0

Movie clip displayed and edited in this space

Parameters defining which frame of the movie clip is displayed

MovieClipUser, (readonly, never None)

Display under or over everything

enum in ['BACK', 'FRONT'], default 'BACK'

How the image fits in the camera frame

enum in ['STRETCH', 'FIT', 'CROP'], default 'FIT'

Image displayed and edited in this space

Parameters defining which layer, pass and frame of the image is displayed

ImageUser, (readonly, never None)

In a local override camera, whether this background image comes from the linked reference camera, or is local to the override

boolean, default False, (readonly)

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

Rotation for the background image (ortho view only)

float in [-inf, inf], default 0.0

Scale the background image

float in [0, inf], default 0.0

Show this image as background

boolean, default False

Show the details in the user interface

boolean, default False

Show this image in front of objects in viewport

boolean, default False

Data source used for background

enum in ['IMAGE', 'MOVIE_CLIP'], default 'IMAGE'

Use movie clip from active scene camera

boolean, default False

Flip the background image horizontally

boolean, default False

Flip the background image vertically

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Camera.background_images

CameraBackgroundImages.new

CameraBackgroundImages.remove

---

## CameraBackgroundImages(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CameraBackgroundImages.html

**Contents:**
- CameraBackgroundImages(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of background images

Add new background image

Image displayed as viewport background

CameraBackgroundImage

Remove background image

image (CameraBackgroundImage, (never None)) – Image displayed as viewport background

Remove all background images

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Camera.background_images

---

## CameraDOFSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CameraDOFSettings.html

**Contents:**
- CameraDOFSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Depth of Field settings

Number of blades in aperture for polygonal bokeh (at least 3)

int in [0, 16], default 0

F-Stop ratio (lower numbers give more defocus, higher numbers give a sharper image)

float in [0, inf], default 2.8

Distortion to simulate anamorphic lens bokeh

float in [0.01, inf], default 1.0

Rotation of blades in aperture

float in [-3.14159, 3.14159], default 0.0

Distance to the focus point for depth of field

float in [0, inf], default 10.0

Use this object to define the depth of field focal point

Use this armature bone to define the depth of field focal point

string, default “”, (never None)

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CameraSolverConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CameraSolverConstraint.html

**Contents:**
- CameraSolverConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Lock motion to the reconstructed camera movement

Movie Clip to get tracking data from

Use active clip defined in scene

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## CameraStereoData(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CameraStereoData.html

**Contents:**
- CameraStereoData(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Stereoscopy settings for a Camera data-block

The converge point for the stereo cameras (often the distance between a projector and the projection screen)

float in [1e-05, inf], default 1.95

OFFAXIS Off-Axis – Off-axis frustums converging in a plane.

PARALLEL Parallel – Parallel cameras with no convergence.

TOE Toe-in – Rotated cameras, looking at the same point at the convergence distance.

enum in ['OFFAXIS', 'PARALLEL', 'TOE'], default 'OFFAXIS'

Set the distance between the eyes - the stereo plane distance / 30 should be fine

float in [0, inf], default 0.065

enum in ['LEFT', 'RIGHT', 'CENTER'], default 'LEFT'

Angle at which interocular distance starts to fade to 0

float in [0, 1.5708], default 1.0472

Angle at which interocular distance is 0

float in [0, 1.5708], default 1.309

Fade interocular distance to 0 after the given cutoff angle

boolean, default False

Render every pixel rotating the camera around the middle of the interocular distance

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CastModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CastModifier.html

**Contents:**
- CastModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Modifier to cast to other shapes

enum in ['SPHERE', 'CYLINDER', 'CUBOID'], default 'SPHERE'

float in [-inf, inf], default 0.5

Invert vertex group influence

boolean, default False

Control object: if available, its location determines the center of the effect

Only deform vertices within this distance from the center of the effect (leave as 0 for infinite.)

float in [0, inf], default 0.0

Size of projection shape (leave as 0 for auto)

float in [0, inf], default 0.0

Use radius as size of projection shape (0 = auto)

boolean, default True

Use object transform to control projection shape

boolean, default False

boolean, default True

boolean, default True

boolean, default True

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## ChannelDriverVariables(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ChannelDriverVariables.html

**Contents:**
- ChannelDriverVariables(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of channel driver Variables

Add a new variable for the driver

Newly created Driver Variable

Remove an existing variable from the driver

variable (DriverVariable, (never None)) – Variable to remove from the driver

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ChildOfConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ChildOfConstraint.html

**Contents:**
- ChildOfConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Create constraint-based parent-child relationship

Transformation matrix to apply before

mathutils.Matrix of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))

Set to true to request recalculation of the inverse matrix

boolean, default False

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Use X Location of Parent

boolean, default False

Use Y Location of Parent

boolean, default False

Use Z Location of Parent

boolean, default False

Use X Rotation of Parent

boolean, default False

Use Y Rotation of Parent

boolean, default False

Use Z Rotation of Parent

boolean, default False

Use X Scale of Parent

boolean, default False

Use Y Scale of Parent

boolean, default False

Use Z Scale of Parent

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## ChildParticle(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ChildParticle.html

**Contents:**
- ChildParticle(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Child particle interpolated from simulated or edited particles

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ParticleSystem.child_particles

---

## ClothCollisionSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ClothCollisionSettings.html

**Contents:**
- ClothCollisionSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Cloth simulation settings for self collision and collision with other objects

Limit colliders to this Collection

How many collision iterations should be done (higher is better quality but slower)

int in [1, 32767], default 2

Amount of velocity lost on collision

float in [0, 1], default 1.0

Minimum distance between collision objects before collision response takes effect

float in [0.001, 1], default 0.015

Friction force if a collision happened (higher = less movement)

float in [0, 80], default 5.0

Clamp collision impulses to avoid instability (0.0 to disable clamping)

float in [0, 100], default 0.0

Minimum distance between cloth faces before collision response takes effect

float in [0.001, 0.1], default 0.015

Friction with self contact

float in [0, 80], default 5.0

Clamp collision impulses to avoid instability (0.0 to disable clamping)

float in [0, 100], default 0.0

Enable collisions with other objects

boolean, default True

Enable self collisions

boolean, default False

Triangles with all vertices in this group are not used during object collisions

string, default “”, (never None)

Triangles with all vertices in this group are not used during self collisions

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ClothModifier.collision_settings

---

## ClothModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ClothModifier.html

**Contents:**
- ClothModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, Modifier

Cloth simulation modifier

ClothCollisionSettings, (readonly, never None)

float array of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

float array of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

int array of 3 items in [-inf, inf], default (0, 0, 0), (readonly)

PointCache, (readonly, never None)

ClothSettings, (readonly, never None)

ClothSolverResult, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## ClothSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ClothSettings.html

**Contents:**
- ClothSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Cloth simulation settings for an object

Air has normally some thickness which slows falling things down

float in [0, 10], default 1.0

Amount of damping in bending behavior

float in [0, 1000], default 0.5

Physical model for simulating bending forces

ANGULAR Angular – Cloth model with angular bending springs.

LINEAR Linear – Cloth model with linear bending springs (legacy).

enum in ['ANGULAR', 'LINEAR'], default 'ANGULAR'

How much the material resists bending

float in [0, 10000], default 0.5

Maximum bending stiffness value

float in [0, 10000], default 0.5

float in [0, 1], default 0.0

Amount of damping in compression behavior

float in [0, 50], default 5.0

How much the material resists compression

float in [0, 10000], default 15.0

Maximum compression stiffness value

float in [0, 10000], default 15.0

Influence of target density on the simulation

float in [0, 1], default 0.0

Maximum density of hair

float in [0, 10000], default 0.0

EffectorWeights, (readonly)

Density (kg/l) of the fluid contained inside the object, used to create a hydrostatic pressure gradient simulating the weight of the internal fluid, or buoyancy from the surrounding fluid if negative

float in [-inf, inf], default 0.0

Default Goal (vertex target position) value, when no Vertex Group used

float in [0, 1], default 0.0

Goal (vertex target position) friction

float in [0, 50], default 0.0

Goal maximum, vertex group weights are scaled to match this range

float in [0, 1], default 1.0

Goal minimum, vertex group weights are scaled to match this range

float in [0, 1], default 0.0

Goal (vertex target position) spring stiffness

float in [0, 0.999], default 1.0

Gravity or external force vector

mathutils.Vector of 3 items in [-100, 100], default (0.0, 0.0, -9.81)

How much the material resists compression

float in [0, 10000], default 15.0

Maximum compression stiffness value

float in [0, 10000], default 15.0

float in [0, 1], default 0.0

How much the rays used to connect the internal points can diverge from the vertex normal

float in [0, 0.785398], default 0.785398

The maximum length an internal spring can have during creation. If the distance between internal points is greater than this, no internal spring will be created between these points. A length of zero means that there is no length limit.

float in [0, 1000], default 0.0

Require the points the internal springs connect to have opposite normal directions

boolean, default True

How much the material resists stretching

float in [0, 10000], default 15.0

Maximum tension stiffness value

float in [0, 10000], default 15.0

The mass of each vertex on the cloth material

float in [0, inf], default 0.3

Pin (vertex target position) spring stiffness

float in [0, 50], default 1.0

Ambient pressure (kPa) that balances out between the inside and outside of the object when it has the target volume

float in [0, 10000], default 1.0

Quality of the simulation in steps per frame (higher is better quality but slower)

int in [1, inf], default 5

Shape key to use the rest spring lengths from

float in [0, 10000], default 0.0

Amount of damping in shearing behavior

float in [0, 50], default 5.0

How much the material resists shearing

float in [0, 10000], default 5.0

Maximum shear scaling value

float in [0, 10000], default 5.0

Max amount to shrink cloth by

float in [-inf, 1], default 0.0

Factor by which to shrink cloth

float in [-inf, 1], default 0.0

The mesh volume where the inner/outer pressure will be the same. If set to zero the change in volume will not affect pressure.

float in [0, 10000], default 0.0

Amount of damping in stretching behavior

float in [0, 50], default 5.0

How much the material resists stretching

float in [0, 10000], default 15.0

Maximum tension stiffness value

float in [0, 10000], default 15.0

Cloth speed is multiplied by this value

float in [0, inf], default 1.0

The uniform pressure that is constantly applied to the mesh, in units of Pressure Scale. Can be negative.

float in [-10000, 10000], default 0.0

Make simulation respect deformations in the base mesh

boolean, default False

Simulate an internal volume structure by creating springs connecting the opposite sides of the mesh

boolean, default False

Simulate pressure inside a closed cloth mesh

boolean, default False

Use the Target Volume parameter as the initial volume, instead of calculating it from the mesh itself

boolean, default False

Pulls loose edges together

boolean, default False

Vertex group for fine control over bending stiffness

string, default “”, (never None)

Vertex group for fine control over the internal spring stiffness

string, default “”, (never None)

Vertex Group for pinning of vertices

string, default “”, (never None)

Vertex Group for where to apply pressure. Zero weight means no pressure while a weight of one means full pressure. Faces with a vertex that has zero weight will be excluded from the volume calculation.

string, default “”, (never None)

Vertex group for fine control over shear stiffness

string, default “”, (never None)

Vertex Group for shrinking cloth

string, default “”, (never None)

Vertex group for fine control over structural stiffness

string, default “”, (never None)

Size of the voxel grid cells for interaction effects

float in [0.0001, 10000], default 0.1

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ClothModifier.settings

---

## ClampToConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ClampToConstraint.html

**Contents:**
- ClampToConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Constrain an object’s location to the nearest point along the target path

Main axis of movement

enum in ['CLAMPTO_AUTO', 'CLAMPTO_X', 'CLAMPTO_Y', 'CLAMPTO_Z'], default 'CLAMPTO_AUTO'

Target Object (Curves only)

Treat curve as cyclic curve (no clamping to curve bounding box)

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## ClothSolverResult(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ClothSolverResult.html

**Contents:**
- ClothSolverResult(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Result of cloth solver iteration

Average error during substeps

float in [-inf, inf], default 0.0, (readonly)

Average iterations during substeps

float in [-inf, inf], default 0.0, (readonly)

Maximum error during substeps

float in [-inf, inf], default 0.0, (readonly)

Maximum iterations during substeps

int in [-inf, inf], default 0, (readonly)

Minimum error during substeps

float in [-inf, inf], default 0.0, (readonly)

Minimum iterations during substeps

int in [-inf, inf], default 0, (readonly)

Status of the solver iteration

SUCCESS Success – Computation was successful.

NUMERICAL_ISSUE Numerical Issue – The provided data did not satisfy the prerequisites.

NO_CONVERGENCE No Convergence – Iterative procedure did not converge.

INVALID_INPUT Invalid Input – The inputs are invalid, or the algorithm has been improperly called.

enum set in {'SUCCESS', 'NUMERICAL_ISSUE', 'NO_CONVERGENCE', 'INVALID_INPUT'}, default set(), (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ClothModifier.solver_result

---

## CloudsTexture(Texture)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CloudsTexture.html

**Contents:**
- CloudsTexture(Texture)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ID, Texture

Procedural noise texture

Determine whether Noise returns grayscale or RGB values

enum in ['GRAYSCALE', 'COLOR'], default 'GRAYSCALE'

Size of derivative offset used for calculating normal

float in [0.001, 0.1], default 0.025

Noise basis used for turbulence

BLENDER_ORIGINAL Blender Original – Noise algorithm - Blender original: Smooth interpolated noise.

ORIGINAL_PERLIN Original Perlin – Noise algorithm - Original Perlin: Smooth interpolated noise.

IMPROVED_PERLIN Improved Perlin – Noise algorithm - Improved Perlin: Smooth interpolated noise.

VORONOI_F1 Voronoi F1 – Noise algorithm - Voronoi F1: Returns distance to the closest feature point.

VORONOI_F2 Voronoi F2 – Noise algorithm - Voronoi F2: Returns distance to the 2nd closest feature point.

VORONOI_F3 Voronoi F3 – Noise algorithm - Voronoi F3: Returns distance to the 3rd closest feature point.

VORONOI_F4 Voronoi F4 – Noise algorithm - Voronoi F4: Returns distance to the 4th closest feature point.

VORONOI_F2_F1 Voronoi F2-F1 – Noise algorithm - Voronoi F1-F2.

VORONOI_CRACKLE Voronoi Crackle – Noise algorithm - Voronoi Crackle: Voronoi tessellation with sharp edges.

CELL_NOISE Cell Noise – Noise algorithm - Cell Noise: Square cell tessellation.

enum in ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN', 'IMPROVED_PERLIN', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2_F1', 'VORONOI_CRACKLE', 'CELL_NOISE'], default 'BLENDER_ORIGINAL'

Depth of the cloud calculation

int in [0, 30], default 2

Scaling for noise input

float in [0.0001, inf], default 0.25

SOFT_NOISE Soft – Generate soft noise (smooth transitions).

HARD_NOISE Hard – Generate hard noise (sharp transitions).

enum in ['SOFT_NOISE', 'HARD_NOISE'], default 'SOFT_NOISE'

Materials that use this texture

Takes O(len(bpy.data.materials) * len(material.texture_slots)) time.

Object modifiers that use this texture

Takes O(len(bpy.data.objects) * len(obj.modifiers)) time.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

Texture.use_color_ramp

Texture.use_preview_alpha

Texture.animation_data

Texture.users_material

Texture.users_object_modifier

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

Texture.bl_rna_get_subclass

Texture.bl_rna_get_subclass_py

---

## Collection(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Collection.html

**Contents:**
- Collection(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Collection of Object data-blocks

Active index in the exporters list

int in [0, inf], default 0

Objects that are in this collection and its child collections

bpy_prop_collection of Object, (readonly)

Collections that are immediate children of this collection

CollectionChildren bpy_prop_collection of Collection, (readonly)

Children collections with their parent-collection-specific settings

bpy_prop_collection of CollectionChild, (readonly)

Objects of the collection with their parent-collection-specific settings

bpy_prop_collection of CollectionObject, (readonly)

Color tag for a collection

enum in Collection Color Items, default 'COLOR_01'

Export Handlers configured for the collection

CollectionExports bpy_prop_collection of CollectionExport, (readonly)

Globally disable in renders

boolean, default False

Disable selection in viewport

boolean, default False

Globally disable in viewports

boolean, default False

Offset from the origin to use when instancing

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

Intersection generated by this collection will have this mask value

boolean array of 8 items, default (False, False, False, False, False, False, False, False)

The intersection line will be included into the object with the higher intersection priority value

int in [0, 255], default 0

How to use this collection in Line Art calculation

INCLUDE Include – Generate feature lines for this collection.

OCCLUSION_ONLY Occlusion Only – Only use the collection to produce occlusion.

EXCLUDE Exclude – Don’t use this collection in Line Art.

INTERSECTION_ONLY Intersection Only – Only generate intersection lines for this collection.

NO_INTERSECTION No Intersection – Include this collection but do not generate intersection lines.

FORCE_INTERSECTION Force Intersection – Generate intersection lines even with objects that disabled intersection.

enum in ['INCLUDE', 'OCCLUSION_ONLY', 'EXCLUDE', 'INTERSECTION_ONLY', 'NO_INTERSECTION', 'FORCE_INTERSECTION'], default 'INCLUDE'

Use custom intersection mask for faces in this collection

boolean, default False

Objects that are directly in this collection

CollectionObjects bpy_prop_collection of Object, (readonly)

Assign intersection priority value for this collection

boolean, default False

A list of all children from this collection.

Takes O(n) time, where n is the total number of all descendant collections.

The collection instance objects this collection is used in

Takes O(len(bpy.data.objects)) time.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendData.collections

BlendDataCollections.new

BlendDataCollections.remove

BooleanModifier.collection

ClothCollisionSettings.collection

CollectionChildren.link

CollectionChildren.unlink

DopeSheet.filter_collection

DynamicPaintSurface.brush_collection

EffectorWeights.collection

FluidDomainSettings.effector_group

FluidDomainSettings.fluid_group

FluidDomainSettings.force_collection

FreestyleLineSet.collection

GeometryNodeInputCollection.collection

GreasePencilLineartModifier.source_collection

IDOverrideLibrary.resync

LayerCollection.collection

LightProbe.visibility_collection

NodeSocketCollection.default_value

NodeTreeInterfaceSocketCollection.default_value

ObjectLightLinking.blocker_collection

ObjectLightLinking.receiver_collection

Object.instance_collection

ParticleSettings.collision_collection

ParticleSettings.instance_collection

RigidBodyWorld.collection

RigidBodyWorld.constraints

SoftBodySettings.collision_collection

---

## CollectionChild(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionChild.html

**Contents:**
- CollectionChild(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Child collection with its collection related settings

Light linking settings of the collection object

CollectionLightLinking, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Collection.collection_children

---

## CollectionChildren(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionChildren.html

**Contents:**
- CollectionChildren(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of child collections

Add this collection as child of this collection

child (Collection, (never None)) – Collection to add

Remove this child collection from a collection

child (Collection) – Collection to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CollectionExports(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionExports.html

**Contents:**
- CollectionExports(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of export handlers

Add an export handler to the collection

type (enum in ['IO_FH_alembic', 'IO_FH_usd', 'IO_FH_obj', 'IO_FH_ply', 'IO_FH_stl', 'IO_FH_fbx', 'IO_FH_gltf2']) – Type, The type of export handler to add

name (string, (optional, never None)) – Name, Name of the new export handler

Newly created export handler

Remove an export handler from the collection

exporter (CollectionExport) – Export Handler to remove

Move an export handler

from_index (int in [-inf, inf]) – From Index, Index to move

to_index (int in [-inf, inf]) – To Index, Target index

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CollectionExport(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionExport.html

**Contents:**
- CollectionExport(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Properties associated with the configured exporter

PropertyGroup, (readonly)

The file path used for exporting

string, default “”, (never None, blend relative // prefix supported)

Whether the panel is expanded or closed

boolean, default False

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CollectionExports.new

CollectionExports.remove

---

## CollectionLightLinking(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionLightLinking.html

**Contents:**
- CollectionLightLinking(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Light linking settings of objects and children collections of a collection

Light or shadow receiving state of the object or collection

enum in ['INCLUDE', 'EXCLUDE'], default 'INCLUDE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CollectionChild.light_linking

CollectionObject.light_linking

---

## CollectionObject(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionObject.html

**Contents:**
- CollectionObject(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Object of a collection with its collection related settings

Light linking settings of the collection

CollectionLightLinking, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Collection.collection_objects

---

## CollectionObjects(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionObjects.html

**Contents:**
- CollectionObjects(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of collection objects

Add this object to a collection

object (Object, (never None)) – Object to add

Remove this object from a collection

object (Object) – Object to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CollectionProperty(Property)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollectionProperty.html

**Contents:**
- CollectionProperty(Property)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Property

RNA collection property to define lists, arrays and mappings

Fixed pointer type, empty if variable type

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Property.translation_context

Property.is_animatable

Property.is_overridable

Property.is_argument_optional

Property.is_never_none

Property.is_skip_save

Property.is_skip_preset

Property.is_registered

Property.is_registered_optional

Property.is_enum_flag

Property.is_library_editable

Property.is_path_output

Property.is_path_supports_blend_relative

Property.is_path_supports_templates

Property.is_deprecated

Property.deprecated_note

Property.deprecated_version

Property.deprecated_removal_version

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Property.bl_rna_get_subclass

Property.bl_rna_get_subclass_py

---

## CollisionModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollisionModifier.html

**Contents:**
- CollisionModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Collision modifier defining modifier stack position used for collision

CollisionSettings, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## CollisionSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CollisionSettings.html

**Contents:**
- CollisionSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collision settings for object in physics simulation

How much of effector force gets lost during collision with this object (in percent)

float in [0, 1], default 0.0

Friction for cloth collisions

float in [0, 80], default 0.0

Amount of damping during collision

float in [0, 1], default 0.0

Amount of damping during particle collision

float in [0, 1], default 0.0

Random variation of damping

float in [0, 1], default 0.0

Amount of friction during particle collision

float in [0, 1], default 0.0

Random variation of friction

float in [0, 1], default 0.0

Chance that the particle will pass through the mesh

float in [0, 1], default 0.0

Amount of stickiness to surface collision

float in [0, 10], default 0.0

Inner face thickness (only used by softbodies)

float in [0.001, 1], default 0.0

float in [0.001, 1], default 0.0

Enable this object as a collider for physics systems

boolean, default False

Cloth collision acts with respect to the collider normals (improves penetration recovery)

boolean, default False

Cloth collision impulses act in the direction of the collider normals (more reliable in some cases)

boolean, default False

Kill collided particles

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CollisionModifier.settings

---

## ColorManagedDisplaySettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorManagedDisplaySettings.html

**Contents:**
- ColorManagedDisplaySettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color management specific to display device

Display name. For viewing, this is the display device that will be emulated by limiting the gamut and HDR colors. For image and video output, this is the display space used for writing.

enum in ['NONE'], default 'NONE'

Control how images in the chosen display are mapped to the physical display

OFF Off – Directly output image as produced by OpenColorIO. This is not correct in general, but may be used when the system configuration and actual display device is known to match the chosen display.

AUTO Automatic – Display images consistent with most other applications, to preview images and video for export. A best effort is made to emulate the chosen display on the actual display device..

enum in ['OFF', 'AUTO'], default 'AUTO'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CompositorNodeConvertToDisplay.display_settings

ImageFormatSettings.display_settings

Scene.display_settings

---

## ColorBalanceModifier(StripModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorBalanceModifier.html

**Contents:**
- ColorBalanceModifier(StripModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, StripModifier

Color balance modifier for sequence strip

StripColorBalanceData, (readonly)

Multiply the intensity of each pixel

float in [0, 20], default 1.0

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

StripModifier.show_expanded

StripModifier.input_mask_type

StripModifier.mask_time

StripModifier.input_mask_strip

StripModifier.input_mask_id

StripModifier.is_active

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

StripModifier.bl_rna_get_subclass

StripModifier.bl_rna_get_subclass_py

---

## ColorManagedInputColorspaceSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorManagedInputColorspaceSettings.html

**Contents:**
- ColorManagedInputColorspaceSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Input color space settings

Treat image as non-color data without color management, like normal or displacement maps

boolean, default False

Color space in the image file, to convert to and from when saving and loading the image

enum in Color Space Convert Default Items, default 'NONE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Image.colorspace_settings

ImageStrip.colorspace_settings

MovieClip.colorspace_settings

MovieStrip.colorspace_settings

ImageFormatSettings.linear_colorspace_settings

---

## ColorManagedSequencerColorspaceSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorManagedSequencerColorspaceSettings.html

**Contents:**
- ColorManagedSequencerColorspaceSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Input color space settings

Color space that the sequencer operates in

enum in Color Space Convert Default Items, default 'NONE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Scene.sequencer_colorspace_settings

---

## ColorManagedViewSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorManagedViewSettings.html

**Contents:**
- ColorManagedViewSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color management settings used for displaying images on the display

Color curve mapping applied before display transform

CurveMapping, (readonly)

Exposure (stops) applied before display transform, multiplying by 2^exposure

float in [-32, 32], default 0.0

Additional gamma encoding after display transform, for output with custom gamma

float in [0, 5], default 1.0

The display and view transform supports high dynamic range colors

boolean, default False, (readonly)

Additional transform applied before view transform for artistic needs

NONE None – Do not modify image in an artistic manner.

enum in ['NONE'], default 'NONE'

The display and view transform supports automatic emulation for another display device, using the display color spaces mechanism in OpenColorIO v2 configurations

boolean, default False, (readonly)

Use RGB curved for pre-display transformation

boolean, default False

Perform chromatic adaption from a different white point

boolean, default False

View used when converting image to a display space

NONE None – Do not perform any color transform on display, use old non-color managed technique for display.

enum in ['NONE'], default 'NONE'

Color temperature of the scene’s white point

float in [1800, 100000], default 6500.0

Color tint of the scene’s white point (the default of 10 matches daylight)

float in [-500, 500], default 10.0

The color which gets mapped to white (automatically converted to/from temperature and tint)

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CompositorNodeConvertToDisplay.view_settings

ImageFormatSettings.view_settings

---

## ColorMapping(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorMapping.html

**Contents:**
- ColorMapping(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color mapping settings

Blend color to mix with texture output color

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

float in [-inf, inf], default 0.0

Mode used to mix with texture output color

enum in ['MIX', 'DARKEN', 'MULTIPLY', 'LIGHTEN', 'SCREEN', 'ADD', 'OVERLAY', 'SOFT_LIGHT', 'LINEAR_LIGHT', 'DIFFERENCE', 'SUBTRACT', 'DIVIDE', 'HUE', 'SATURATION', 'COLOR', 'VALUE'], default 'MIX'

Adjust the brightness of the texture

float in [0, 2], default 0.0

ColorRamp, (readonly)

Adjust the contrast of the texture

float in [0, 5], default 0.0

Adjust the saturation of colors in the texture

float in [0, 2], default 0.0

Toggle color ramp operations

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ShaderNodeTexBrick.color_mapping

ShaderNodeTexChecker.color_mapping

ShaderNodeTexEnvironment.color_mapping

ShaderNodeTexGabor.color_mapping

ShaderNodeTexGradient.color_mapping

ShaderNodeTexImage.color_mapping

ShaderNodeTexMagic.color_mapping

ShaderNodeTexNoise.color_mapping

ShaderNodeTexSky.color_mapping

ShaderNodeTexVoronoi.color_mapping

ShaderNodeTexWave.color_mapping

---

## ColorMixStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorMixStrip.html

**Contents:**
- ColorMixStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

Method for controlling how the strip combines with other strips

enum in ['DARKEN', 'MULTIPLY', 'BURN', 'LINEAR_BURN', 'LIGHTEN', 'SCREEN', 'DODGE', 'ADD', 'OVERLAY', 'SOFT_LIGHT', 'HARD_LIGHT', 'VIVID_LIGHT', 'LINEAR_LIGHT', 'PIN_LIGHT', 'DIFFERENCE', 'EXCLUSION', 'SUBTRACT', 'HUE', 'SATURATION', 'COLOR', 'VALUE'], default 'DARKEN'

Percentage of how much the strip’s colors affect other strips

float in [0, 1], default 0.0

First input for the effect strip

Second input for the effect strip

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## ColorRampElements(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorRampElements.html

**Contents:**
- ColorRampElements(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Color Ramp Elements

Add element to Color Ramp

position (float in [0, 1]) – Position, Position to add element

Delete element from Color Ramp

element (ColorRampElement, (never None)) – Element to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ColorRampElement(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorRampElement.html

**Contents:**
- ColorRampElement(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Element defining a color at a position in the color ramp

Set alpha of selected color stop

float in [0, inf], default 0.0

Set color of selected color stop

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0)

Set position of selected color stop

float in [0, 1], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ColorRampElements.new

ColorRampElements.remove

---

## ColorRamp(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorRamp.html

**Contents:**
- ColorRamp(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color ramp mapping a scalar value to a color

Set color mode to use for interpolation

enum in ['RGB', 'HSV', 'HSL'], default 'RGB'

ColorRampElements bpy_prop_collection of ColorRampElement, (readonly)

Set color interpolation

enum in ['NEAR', 'FAR', 'CW', 'CCW'], default 'NEAR'

Set interpolation between color stops

enum in ['EASE', 'CARDINAL', 'LINEAR', 'B_SPLINE', 'CONSTANT'], default 'LINEAR'

position (float in [0, 1]) – Position, Evaluate Color Ramp at position

Color, Color at given position

float array of 4 items in [-inf, inf]

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ColorMapping.color_ramp

DynamicPaintBrushSettings.paint_ramp

DynamicPaintBrushSettings.velocity_ramp

FluidDomainSettings.color_ramp

GreasePencilTintModifier.color_ramp

LineStyleColorModifier_AlongStroke.color_ramp

LineStyleColorModifier_CreaseAngle.color_ramp

LineStyleColorModifier_Curvature_3D.color_ramp

LineStyleColorModifier_DistanceFromCamera.color_ramp

LineStyleColorModifier_DistanceFromObject.color_ramp

LineStyleColorModifier_Material.color_ramp

LineStyleColorModifier_Noise.color_ramp

LineStyleColorModifier_Tangent.color_ramp

PreferencesView.weight_color_range

ShaderNodeValToRGB.color_ramp

TextureNodeValToRGB.color_ramp

---

## ColorStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ColorStrip.html

**Contents:**
- ColorStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

Sequence strip creating an image filled with a single color

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## CompositorNode(NodeInternal)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNode.html

**Contents:**
- CompositorNode(NodeInternal)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal

subclasses — CompositorNodeAlphaOver, CompositorNodeAntiAliasing, CompositorNodeBilateralblur, CompositorNodeBlur, CompositorNodeBokehBlur, CompositorNodeBokehImage, CompositorNodeBoxMask, CompositorNodeBrightContrast, CompositorNodeChannelMatte, CompositorNodeChromaMatte, CompositorNodeColorBalance, CompositorNodeColorCorrection, CompositorNodeColorMatte, CompositorNodeColorSpill, CompositorNodeCombineColor, CompositorNodeConvertColorSpace, CompositorNodeConvertToDisplay, CompositorNodeConvolve, CompositorNodeCornerPin, CompositorNodeCrop, CompositorNodeCryptomatte, CompositorNodeCryptomatteV2, CompositorNodeCurveRGB, CompositorNodeCustomGroup, CompositorNodeDBlur, CompositorNodeDefocus, CompositorNodeDenoise, CompositorNodeDespeckle, CompositorNodeDiffMatte, CompositorNodeDilateErode, CompositorNodeDisplace, CompositorNodeDistanceMatte, CompositorNodeDoubleEdgeMask, CompositorNodeEllipseMask, CompositorNodeExposure, CompositorNodeFilter, CompositorNodeFlip, CompositorNodeGamma, CompositorNodeGlare, CompositorNodeGroup, CompositorNodeHueCorrect, CompositorNodeHueSat, CompositorNodeIDMask, CompositorNodeImage, CompositorNodeImageCoordinates, CompositorNodeImageInfo, CompositorNodeInpaint, CompositorNodeInvert, CompositorNodeKeying, CompositorNodeKeyingScreen, CompositorNodeKuwahara, CompositorNodeLensdist, CompositorNodeLevels, CompositorNodeLumaMatte, CompositorNodeMapUV, CompositorNodeMask, CompositorNodeMovieClip, CompositorNodeMovieDistortion, CompositorNodeNormal, CompositorNodeNormalize, CompositorNodeOutputFile, CompositorNodePixelate, CompositorNodePlaneTrackDeform, CompositorNodePosterize, CompositorNodePremulKey, CompositorNodeRGB, CompositorNodeRGBToBW, CompositorNodeRLayers, CompositorNodeRelativeToPixel, CompositorNodeRotate, CompositorNodeScale, CompositorNodeSceneTime, CompositorNodeSeparateColor, CompositorNodeSetAlpha, CompositorNodeSplit, CompositorNodeStabilize, CompositorNodeSwitch, CompositorNodeSwitchView, CompositorNodeTime, CompositorNodeTonemap, CompositorNodeTrackPos, CompositorNodeTransform, CompositorNodeTranslate, CompositorNodeVecBlur, CompositorNodeViewer, CompositorNodeZcombine

Tag the node for compositor update

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

---

## CompositorNodeAlphaOver(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeAlphaOver.html

**Contents:**
- CompositorNodeAlphaOver(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Overlay a foreground image onto a background image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeAntiAliasing(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeAntiAliasing.html

**Contents:**
- CompositorNodeAntiAliasing(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Smooth away jagged edges

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBilateralblur(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBilateralblur.html

**Contents:**
- CompositorNodeBilateralblur(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adaptively blur image, while retaining sharp edges

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBlur(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBlur.html

**Contents:**
- CompositorNodeBlur(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Blur an image, using several blur modes

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBokehBlur(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBokehBlur.html

**Contents:**
- CompositorNodeBokehBlur(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Generate a bokeh type blur similar to Defocus. Unlike defocus an in-focus region is defined in the compositor

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBokehImage(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBokehImage.html

**Contents:**
- CompositorNodeBokehImage(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Generate image with bokeh shape for use with the Bokeh Blur filter node

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBoxMask(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBoxMask.html

**Contents:**
- CompositorNodeBoxMask(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create rectangular mask suitable for use as a simple matte

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeBrightContrast(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeBrightContrast.html

**Contents:**
- CompositorNodeBrightContrast(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adjust brightness and contrast

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeChannelMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeChannelMatte.html

**Contents:**
- CompositorNodeChannelMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create matte based on differences in color channels

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeChromaMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeChromaMatte.html

**Contents:**
- CompositorNodeChromaMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create matte based on chroma values

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeColorBalance(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeColorBalance.html

**Contents:**
- CompositorNodeColorBalance(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adjust color and values

The color which gets mapped to white (automatically converted to/from temperature and tint)

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

The color which gets white gets mapped to (automatically converted to/from temperature and tint)

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeColorCorrection(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeColorCorrection.html

**Contents:**
- CompositorNodeColorCorrection(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adjust the color of an image, separately in several tonal ranges (highlights, midtones and shadows)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeColorMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeColorMatte.html

**Contents:**
- CompositorNodeColorMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create matte using a given color, for green or blue screen footage

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeColorSpill(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeColorSpill.html

**Contents:**
- CompositorNodeColorSpill(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Remove colors from a blue or green screen, by reducing one RGB channel compared to the others

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCombineColor(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCombineColor.html

**Contents:**
- CompositorNodeCombineColor(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Combine an image from its composite color channels

Mode of color processing

RGB RGB – Use RGB (Red, Green, Blue) color processing.

HSV HSV – Use HSV (Hue, Saturation, Value) color processing.

HSL HSL – Use HSL (Hue, Saturation, Lightness) color processing.

YCC YCbCr – Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing.

YUV YUV – Use YUV (Y - luma, U V - chroma) color processing.

enum in ['RGB', 'HSV', 'HSL', 'YCC', 'YUV'], default 'RGB'

Color space used for YCbCrA processing

enum in ['ITUBT601', 'ITUBT709', 'JFIF'], default 'ITUBT601'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeConvertColorSpace(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeConvertColorSpace.html

**Contents:**
- CompositorNodeConvertColorSpace(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Convert between color spaces

Color space of the input image

enum in Color Space Convert Default Items, default 'NONE'

Color space of the output image

enum in Color Space Convert Default Items, default 'NONE'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeConvertToDisplay(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeConvertToDisplay.html

**Contents:**
- CompositorNodeConvertToDisplay(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Convert from scene linear to display color space, with a view transform and look for tone mapping

Color management display device settings

ColorManagedDisplaySettings, (readonly)

Color management view transform settings

ColorManagedViewSettings, (readonly)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeConvolve(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeConvolve.html

**Contents:**
- CompositorNodeConvolve(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Convolves an image with a kernel

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCornerPin(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCornerPin.html

**Contents:**
- CompositorNodeCornerPin(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Plane warp transformation using explicit corner values

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCrop(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCrop.html

**Contents:**
- CompositorNodeCrop(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Crops image to a smaller region, either making the cropped area transparent or resizing the image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCryptomatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCryptomatte.html

**Contents:**
- CompositorNodeCryptomatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Deprecated. Use Cryptomatte Node instead

Add object or material to matte, by picking a color from the Pick output

mathutils.Color of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

List of object and material crypto IDs to include in matte

string, default “”, (never None)

Remove object or material from matte, by picking a color from the Pick output

mathutils.Color of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCryptomatteV2(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCryptomatteV2.html

**Contents:**
- CompositorNodeCryptomatteV2(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Generate matte for individual objects and materials using Cryptomatte render passes

Add object or material to matte, by picking a color from the Pick output

mathutils.Color of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

bpy_prop_collection of CryptomatteEntry, (readonly)

Number of images of a movie to use

int in [0, 1048574], default 0

Offset the number of the frame to use in the animation

int in [-1048574, 1048574], default 0

Global starting frame of the movie/sequence, assuming first picture has a #1

int in [-1048574, 1048574], default 0

True if this image has any named layer

boolean, default False, (readonly)

True if this image has multiple views

boolean, default False, (readonly)

enum in ['PLACEHOLDER'], default 'PLACEHOLDER'

What Cryptomatte layer is used

CryptoObject Object – Use Object layer.

CryptoMaterial Material – Use Material layer.

CryptoAsset Asset – Use Asset layer.

enum in ['CryptoObject', 'CryptoMaterial', 'CryptoAsset'], default 'CryptoObject'

List of object and material crypto IDs to include in matte

string, default “”, (never None)

Remove object or material from matte, by picking a color from the Pick output

mathutils.Color of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

Where the Cryptomatte passes are loaded from

RENDER Render – Use Cryptomatte passes from a render.

IMAGE Image – Use Cryptomatte passes from an image.

enum in ['RENDER', 'IMAGE'], default 'RENDER'

Always refresh image on frame changes

boolean, default False

Cycle the images in the movie

boolean, default False

enum in ['ALL'], default 'ALL'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCurveRGB(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCurveRGB.html

**Contents:**
- CompositorNodeCurveRGB(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Perform level adjustments on each color channel of an image

CurveMapping, (readonly)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeCustomGroup(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeCustomGroup.html

**Contents:**
- CompositorNodeCustomGroup(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Custom Compositor Group Node for Python nodes

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDBlur(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDBlur.html

**Contents:**
- CompositorNodeDBlur(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Blur an image along a direction

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDefocus(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDefocus.html

**Contents:**
- CompositorNodeDefocus(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Apply depth of field in 2D, using a Z depth map or mask

Bokeh shape rotation offset

float in [0, 1.5708], default 0.0

Blur limit, maximum CoC radius

float in [0, 10000], default 0.0

OCTAGON Octagonal – 8 sides.

HEPTAGON Heptagonal – 7 sides.

HEXAGON Hexagonal – 6 sides.

PENTAGON Pentagonal – 5 sides.

SQUARE Square – 4 sides.

TRIANGLE Triangular – 3 sides.

enum in ['OCTAGON', 'HEPTAGON', 'HEXAGON', 'PENTAGON', 'SQUARE', 'TRIANGLE', 'CIRCLE'], default 'CIRCLE'

Amount of focal blur, 128 (infinity) is perfect focus, half the value doubles the blur radius

float in [0, 128], default 0.0

Scene from which to select the active camera (render scene if undefined)

Disable when using an image as input instead of actual z-buffer (auto enabled if node not image based, eg. time node)

boolean, default False

Scale the Z input when not using a z-buffer, controls maximum blur designated by the color white or input value 1

float in [0, 1000], default 0.0

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDenoise(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDenoise.html

**Contents:**
- CompositorNodeDenoise(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Denoise renders from Cycles and other ray tracing renderers

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDespeckle(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDespeckle.html

**Contents:**
- CompositorNodeDespeckle(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Smooth areas of an image in which noise is noticeable, while leaving complex areas untouched

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDiffMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDiffMatte.html

**Contents:**
- CompositorNodeDiffMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Produce a matte that isolates foreground content by comparing it with a reference background image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDilateErode(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDilateErode.html

**Contents:**
- CompositorNodeDilateErode(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Expand and shrink masks

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDisplace(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDisplace.html

**Contents:**
- CompositorNodeDisplace(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Displace pixel position using an offset vector

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDistanceMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDistanceMatte.html

**Contents:**
- CompositorNodeDistanceMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create matte based on 3D distance between colors

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeDoubleEdgeMask(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeDoubleEdgeMask.html

**Contents:**
- CompositorNodeDoubleEdgeMask(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create a gradient between two masks

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeEllipseMask(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeEllipseMask.html

**Contents:**
- CompositorNodeEllipseMask(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create elliptical mask suitable for use as a simple matte or vignette mask

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeExposure(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeExposure.html

**Contents:**
- CompositorNodeExposure(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adjust brightness using a camera exposure parameter

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeFilter(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeFilter.html

**Contents:**
- CompositorNodeFilter(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Apply common image enhancement filters

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeFlip(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeFlip.html

**Contents:**
- CompositorNodeFlip(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Flip an image along a defined axis

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeGamma(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeGamma.html

**Contents:**
- CompositorNodeGamma(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeGlare(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeGlare.html

**Contents:**
- CompositorNodeGlare(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Add lens flares, fog and glows around bright parts of the image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeGroup(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeGroup.html

**Contents:**
- CompositorNodeGroup(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeHueCorrect(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeHueCorrect.html

**Contents:**
- CompositorNodeHueCorrect(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Adjust hue, saturation, and value with a curve

CurveMapping, (readonly)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeHueSat(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeHueSat.html

**Contents:**
- CompositorNodeHueSat(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Apply a color transformation in the HSV color model

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeIDMask(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeIDMask.html

**Contents:**
- CompositorNodeIDMask(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create a matte from an object or material index pass

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeImageCoordinates(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeImageCoordinates.html

**Contents:**
- CompositorNodeImageCoordinates(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Returns the coordinates of the pixels of an image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeImageInfo(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeImageInfo.html

**Contents:**
- CompositorNodeImageInfo(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Returns information about an image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeInpaint(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeInpaint.html

**Contents:**
- CompositorNodeInpaint(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Extend borders of an image into transparent or masked regions

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeImage(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeImage.html

**Contents:**
- CompositorNodeImage(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input image or movie file

Number of images of a movie to use

int in [0, 1048574], default 0

Offset the number of the frame to use in the animation

int in [-1048574, 1048574], default 0

Global starting frame of the movie/sequence, assuming first picture has a #1

int in [-1048574, 1048574], default 0

True if this image has any named layer

boolean, default False, (readonly)

True if this image has multiple views

boolean, default False, (readonly)

enum in ['PLACEHOLDER'], default 'PLACEHOLDER'

Always refresh image on frame changes

boolean, default False

Cycle the images in the movie

boolean, default False

enum in ['ALL'], default 'ALL'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeInvert(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeInvert.html

**Contents:**
- CompositorNodeInvert(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Invert colors, producing a negative

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeKeying(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeKeying.html

**Contents:**
- CompositorNodeKeying(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Perform both chroma keying (to remove the backdrop) and despill (to correct color cast from the backdrop)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeKeyingScreen(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeKeyingScreen.html

**Contents:**
- CompositorNodeKeyingScreen(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create plates for use as a color reference for keying nodes

string, default “”, (never None)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeKuwahara(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeKuwahara.html

**Contents:**
- CompositorNodeKuwahara(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Apply smoothing filter that preserves edges, for stylized and painterly effects

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeMapUV(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeMapUV.html

**Contents:**
- CompositorNodeMapUV(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Map a texture using UV coordinates, to apply a texture to objects in compositing

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeLumaMatte(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeLumaMatte.html

**Contents:**
- CompositorNodeLumaMatte(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Create a matte based on luminance (brightness) difference

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeLevels(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeLevels.html

**Contents:**
- CompositorNodeLevels(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Compute average and standard deviation of pixel values

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeLensdist(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeLensdist.html

**Contents:**
- CompositorNodeLensdist(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Simulate distortion and dispersion from camera lenses

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeMask(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeMask.html

**Contents:**
- CompositorNodeMask(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input mask from a mask data-block, created in the image editor

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeMovieClip(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeMovieClip.html

**Contents:**
- CompositorNodeMovieClip(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input image or movie from a movie clip data-block, typically used for motion tracking

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeMovieDistortion(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeMovieDistortion.html

**Contents:**
- CompositorNodeMovieDistortion(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Remove lens distortion from footage, using motion tracking camera lens settings

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeNormal(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeNormal.html

**Contents:**
- CompositorNodeNormal(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input normalized normal values to other nodes in the tree

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeOutputFile(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeOutputFile.html

**Contents:**
- CompositorNodeOutputFile(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Write image file to disk

Index of the active item

int in [0, inf], default 0

The directory where the image will be written

string, default “”, (never None, blend relative // prefix supported, Supports template expressions)

The base name of the file. Other information might be included in the final file name depending on the node options

string, default “”, (never None, Supports template expressions)

NodeCompositorFileOutputItems bpy_prop_collection of NodeCompositorFileOutputItem, (readonly)

ImageFormatSettings, (readonly)

Apply render part of display transform when saving byte image

boolean, default False

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodePixelate(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodePixelate.html

**Contents:**
- CompositorNodePixelate(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Reduce detail in an image by making individual pixels more prominent, for a blocky or mosaic-like appearance

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodePlaneTrackDeform(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodePlaneTrackDeform.html

**Contents:**
- CompositorNodePlaneTrackDeform(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Replace flat planes in footage by another image, detected by plane tracks from motion tracking

string, default “”, (never None)

string, default “”, (never None)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeNormalize(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeNormalize.html

**Contents:**
- CompositorNodeNormalize(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Map values to 0 to 1 range, based on the minimum and maximum pixel values

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodePosterize(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodePosterize.html

**Contents:**
- CompositorNodePosterize(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Reduce number of colors in an image, converting smooth gradients into sharp transitions

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodePremulKey(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodePremulKey.html

**Contents:**
- CompositorNodePremulKey(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Convert to and from premultiplied (associated) alpha

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeRGB(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeRGB.html

**Contents:**
- CompositorNodeRGB(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeRGBToBW(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeRGBToBW.html

**Contents:**
- CompositorNodeRGBToBW(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Convert RGB input into grayscale using luminance

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeRLayers(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeRLayers.html

**Contents:**
- CompositorNodeRLayers(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input render passes from a scene render

enum in ['PLACEHOLDER'], default 'PLACEHOLDER'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeRelativeToPixel(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeRelativeToPixel.html

**Contents:**
- CompositorNodeRelativeToPixel(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Converts values that are relative to the image size to be in terms of pixels

FLOAT Float – Float value.

VECTOR Vector – Vector value.

enum in ['FLOAT', 'VECTOR'], default 'FLOAT'

Defines the dimension of the image that the relative value is in reference to

PER_DIMENSION Per Dimension – The value is relative to each of the dimensions of the image independently.

X X – The value is relative to the X dimension of the image.

Y Y – The value is relative to the Y dimension of the image.

Greater Greater – The value is relative to the greater dimension of the image.

Smaller Smaller – The value is relative to the smaller dimension of the image.

Diagonal Diagonal – The value is relative to the diagonal of the image.

enum in ['PER_DIMENSION', 'X', 'Y', 'Greater', 'Smaller', 'Diagonal'], default 'X'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeScale(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeScale.html

**Contents:**
- CompositorNodeScale(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Change the size of the image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeRotate(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeRotate.html

**Contents:**
- CompositorNodeRotate(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Rotate image by specified angle

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSceneTime(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSceneTime.html

**Contents:**
- CompositorNodeSceneTime(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Input the current scene time in seconds or frames

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSeparateColor(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSeparateColor.html

**Contents:**
- CompositorNodeSeparateColor(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Split an image into its composite color channels

Mode of color processing

RGB RGB – Use RGB (Red, Green, Blue) color processing.

HSV HSV – Use HSV (Hue, Saturation, Value) color processing.

HSL HSL – Use HSL (Hue, Saturation, Lightness) color processing.

YCC YCbCr – Use YCbCr (Y - luma, Cb - blue-difference chroma, Cr - red-difference chroma) color processing.

YUV YUV – Use YUV (Y - luma, U V - chroma) color processing.

enum in ['RGB', 'HSV', 'HSL', 'YCC', 'YUV'], default 'RGB'

Color space used for YCbCrA processing

enum in ['ITUBT601', 'ITUBT709', 'JFIF'], default 'ITUBT601'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSetAlpha(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSetAlpha.html

**Contents:**
- CompositorNodeSetAlpha(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Add an alpha channel to an image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSplit(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSplit.html

**Contents:**
- CompositorNodeSplit(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Combine two images for side-by-side display. Typically used in combination with a Viewer node

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeStabilize(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeStabilize.html

**Contents:**
- CompositorNodeStabilize(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Stabilize footage using 2D stabilization motion tracking settings

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSwitch(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSwitch.html

**Contents:**
- CompositorNodeSwitch(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Switch between two images using a checkbox

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeSwitchView(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeSwitchView.html

**Contents:**
- CompositorNodeSwitchView(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Combine the views (left and right) into a single stereo 3D output

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTime(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTime.html

**Contents:**
- CompositorNodeTime(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Generate a factor value (from 0.0 to 1.0) between scene start and end time, using a curve mapping

CurveMapping, (readonly)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTonemap(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTonemap.html

**Contents:**
- CompositorNodeTonemap(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Map one set of colors to another in order to approximate the appearance of high dynamic range

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTrackPos(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTrackPos.html

**Contents:**
- CompositorNodeTrackPos(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Provide information about motion tracking points, such as x and y values

string, default “”, (never None)

string, default “”, (never None)

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTransform(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTransform.html

**Contents:**
- CompositorNodeTransform(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Scale, translate and rotate an image

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTranslate(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTranslate.html

**Contents:**
- CompositorNodeTranslate(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeTree(NodeTree)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeTree.html

**Contents:**
- CompositorNodeTree(NodeTree)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ID, NodeTree

Node tree consisting of linked nodes used for compositing

Use boundaries for viewer nodes and composite backdrop

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

NodeTree.default_group_node_width

NodeTree.animation_data

NodeTree.bl_description

NodeTree.bl_use_group_interface

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

NodeTree.interface_update

NodeTree.contains_tree

NodeTree.get_from_context

NodeTree.valid_socket_type

NodeTree.debug_lazy_function_graph

NodeTree.bl_rna_get_subclass

NodeTree.bl_rna_get_subclass_py

---

## CompositorNodeVecBlur(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeVecBlur.html

**Contents:**
- CompositorNodeVecBlur(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Uses the vector speed render pass to blur the image pixels in 2D

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeZcombine(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeZcombine.html

**Contents:**
- CompositorNodeZcombine(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Combine two images using depth maps

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## CompositorNodeViewer(CompositorNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CompositorNodeViewer.html

**Contents:**
- CompositorNodeViewer(CompositorNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, CompositorNode

Visualize data from inside a node graph, in the image editor or as a backdrop

int in [-32768, 32767], default 0

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

CompositorNode.tag_need_exec

CompositorNode.update

CompositorNode.bl_rna_get_subclass

CompositorNode.bl_rna_get_subclass_py

---

## Constraint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Constraint.html

**Contents:**
- Constraint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

subclasses — ActionConstraint, ArmatureConstraint, CameraSolverConstraint, ChildOfConstraint, ClampToConstraint, CopyLocationConstraint, CopyRotationConstraint, CopyScaleConstraint, CopyTransformsConstraint, DampedTrackConstraint, FloorConstraint, FollowPathConstraint, FollowTrackConstraint, GeometryAttributeConstraint, KinematicConstraint, LimitDistanceConstraint, LimitLocationConstraint, LimitRotationConstraint, LimitScaleConstraint, LockedTrackConstraint, MaintainVolumeConstraint, ObjectSolverConstraint, PivotConstraint, ShrinkwrapConstraint, SplineIKConstraint, StretchToConstraint, TrackToConstraint, TransformCacheConstraint, TransformConstraint

Constraint modifying the transformation of objects and bones

Constraint is the one being edited

boolean, default False

Use the results of this constraint

boolean, default False

Amount of residual error in Blender space unit for constraints that work on position

float in [-inf, inf], default 0.0, (readonly)

Amount of residual error in radians for constraints that work on orientation

float in [-inf, inf], default 0.0, (readonly)

Amount of influence constraint will have on the final solution

float in [0, 1], default 0.0

In a local override object, whether this constraint comes from the linked reference object, or is local to the override

boolean, default False, (readonly)

Constraint has valid settings and can be evaluated

boolean, default False, (readonly)

Enable/Disable Constraint

boolean, default False

string, default “”, (never None)

Space that owner is evaluated in

WORLD World Space – The constraint is applied relative to the world coordinate system.

CUSTOM Custom Space – The constraint is applied in local space of a custom object/bone/vertex group.

POSE Pose Space – The constraint is applied in Pose Space, the object transformation is ignored.

LOCAL_WITH_PARENT Local With Parent – The constraint is applied relative to the rest pose local coordinate system of the bone, thus including the parent-induced transformation.

LOCAL Local Space – The constraint is applied relative to the local coordinate system of the object.

enum in ['WORLD', 'CUSTOM', 'POSE', 'LOCAL_WITH_PARENT', 'LOCAL'], default 'WORLD'

Constraint’s panel is expanded in UI

boolean, default False

Object for Custom Space

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Space that target is evaluated in

WORLD World Space – The transformation of the target is evaluated relative to the world coordinate system.

CUSTOM Custom Space – The transformation of the target is evaluated relative to a custom object/bone/vertex group.

POSE Pose Space – The transformation of the target is only evaluated in the Pose Space, the target armature object transformation is ignored.

LOCAL_WITH_PARENT Local With Parent – The transformation of the target bone is evaluated relative to its rest pose local coordinate system, thus including the parent-induced transformation.

LOCAL Local Space – The transformation of the target is evaluated relative to its local coordinate system.

LOCAL_OWNER_ORIENT Local Space (Owner Orientation) – The transformation of the target bone is evaluated relative to its local coordinate system, followed by a correction for the difference in target and owner rest pose orientations. When applied as local transform to the owner produces the same global motion as the target if the parents are still in rest pose..

enum in ['WORLD', 'CUSTOM', 'POSE', 'LOCAL_WITH_PARENT', 'LOCAL', 'LOCAL_OWNER_ORIENT'], default 'WORLD'

enum in Constraint Type Items, default 'CAMERA_SOLVER', (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ObjectConstraints.active

ObjectConstraints.copy

ObjectConstraints.copy

ObjectConstraints.new

ObjectConstraints.remove

PoseBoneConstraints.active

PoseBoneConstraints.copy

PoseBoneConstraints.copy

PoseBoneConstraints.new

PoseBoneConstraints.remove

UILayout.template_constraint_header

---

## ConstraintTarget(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ConstraintTarget.html

**Contents:**
- ConstraintTarget(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

Target object for multi-target constraints

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## ConsoleLine(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ConsoleLine.html

**Contents:**
- ConsoleLine(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Input line for the interactive console

string, default “”, (never None)

int in [-inf, inf], default 0

Console line type when used in scrollback

enum in ['OUTPUT', 'INPUT', 'INFO', 'ERROR'], default 'OUTPUT'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

SpaceConsole.scrollback

---

## ConstraintTargetBone(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ConstraintTargetBone.html

**Contents:**
- ConstraintTargetBone(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Target bone for multi-target constraints

string, default “”, (never None)

Blending weight of this bone

float in [0, 1], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ArmatureConstraint.targets

ArmatureConstraintTargets.new

ArmatureConstraintTargets.remove

---

## CopyRotationConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CopyRotationConstraint.html

**Contents:**
- CopyRotationConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Copy the rotation of the target

Explicitly specify the euler rotation order

AUTO Default – Euler using the default rotation order.

XYZ XYZ Euler – Euler using the XYZ rotation order.

XZY XZY Euler – Euler using the XZY rotation order.

YXZ YXZ Euler – Euler using the YXZ rotation order.

YZX YZX Euler – Euler using the YZX rotation order.

ZXY ZXY Euler – Euler using the ZXY rotation order.

ZYX ZYX Euler – Euler using the ZYX rotation order.

enum in ['AUTO', 'XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'], default 'AUTO'

Invert the X rotation

boolean, default False

Invert the Y rotation

boolean, default False

Invert the Z rotation

boolean, default False

Specify how the copied and existing rotations are combined

REPLACE Replace – Replace the original rotation with copied.

ADD Add – Add euler component values together.

BEFORE Before Original – Apply copied rotation before original, as if the constraint target is a parent.

AFTER After Original – Apply copied rotation after original, as if the constraint target is a child.

OFFSET Offset (Legacy) – Combine rotations like the original Offset checkbox. Does not work well for multiple axis rotations..

enum in ['REPLACE', 'ADD', 'BEFORE', 'AFTER', 'OFFSET'], default 'REPLACE'

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

DEPRECATED: Add original rotation into copied rotation

boolean, default False

Copy the target’s X rotation

boolean, default False

Copy the target’s Y rotation

boolean, default False

Copy the target’s Z rotation

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## Context(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Context.html

**Contents:**
- Context(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Current windowmanager and data context

AssetRepresentation, (readonly)

BlendData, (readonly)

Collection, (readonly)

string, default “”, (readonly, never None)

GizmoGroup, (readonly)

LayerCollection, (readonly)

enum in Context Mode Items, default 'EDIT_MESH', (readonly)

Preferences, (readonly)

RegionView3D, (readonly)

The temporary region for pop-ups (including menus and pop-overs)

The current space, may be None in background-mode, when the cursor is outside the window or when using menu-search

ToolSettings, (readonly)

ViewLayer, (readonly)

WindowManager, (readonly)

WorkSpace, (readonly)

Get the dependency graph for the current scene and view layer, to access to data-blocks with animation and modifiers applied. If any data-blocks have been edited, the dependency graph will be updated. This invalidates all references to evaluated data-blocks from the dependency graph.

Evaluated dependency graph

Get context members as a dictionary.

Returns the property from the path, raise an exception when not found.

path (str) – patch which this property resolves.

coerce (bool) – optional argument, when True, the property will be converted into its Python representation.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Context manager to temporarily override members in the context.

window (bpy.types.Window) – Window override or None.

screen (bpy.types.Screen) – Screen override or None. Note Switching to or away from full-screen areas & temporary screens isn’t supported. Passing in these screens will raise an exception, actions that leave the context such screens won’t restore the prior screen. Note Changing the screen has wider implications than other arguments as it will also change the works-space and potentially the scene (when pinned).

Screen override or None.

Switching to or away from full-screen areas & temporary screens isn’t supported. Passing in these screens will raise an exception, actions that leave the context such screens won’t restore the prior screen.

Changing the screen has wider implications than other arguments as it will also change the works-space and potentially the scene (when pinned).

area (bpy.types.Area) – Area override or None.

region (bpy.types.Region) – Region override or None.

keywords – Additional keywords override context members.

The context manager .

Overriding the context can be used to temporarily activate another window / area & region, as well as other members such as the active_object or bone.

When overriding window, area and regions: the arguments must be consistent, so any region argument that’s passed in must be contained by the current area or the area passed in. The same goes for the area needing to be contained in the current window.

Temporary context overrides may be nested, when this is done, members will be added to the existing overrides.

Context members are restored outside the scope of the context-manager. The only exception to this is when the data is no longer available.

In the event windowing data was removed (for example), the state of the context is left as-is. While this isn’t likely to happen, explicit window operation such as closing windows or loading a new file remove the windowing data that was set before the temporary context was created.

Overriding the context can be useful to set the context after loading files (which would otherwise be None). For example:

This example shows how it’s possible to add an object to the scene in another window.

Logging Context Member Access

Context members can be logged by calling logging_set(True) on the “with” target of a temporary override. This will log the members that are being accessed during the operation and may assist in debugging when it is unclear which members need to be overridden.

In the event an operator fails to execute because of a missing context member, logging may help identify which member is required.

This example shows how to log which context members are being accessed. Log statements are printed to your system’s console.

Not all operators rely on Context Members and therefore will not be affected by bpy.types.Context.temp_override, use logging to what members if any are accessed.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

AssetShelf.draw_context_menu

FileHandler.poll_drop

GizmoGroup.draw_prepare

GizmoGroup.invoke_prepare

KeyingSetInfo.generate

KeyingSetInfo.iterator

Node.draw_buttons_ext

Node.socket_value_update

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeSocket.draw_color

NodeSocketStandard.draw

NodeSocketStandard.draw_color

NodeTree.get_from_context

NodeTree.interface_update

NodeTreeInterfaceSocket.draw

NodeTreeInterfaceSocketBool.draw

NodeTreeInterfaceSocketBundle.draw

NodeTreeInterfaceSocketClosure.draw

NodeTreeInterfaceSocketCollection.draw

NodeTreeInterfaceSocketColor.draw

NodeTreeInterfaceSocketFloat.draw

NodeTreeInterfaceSocketFloatAngle.draw

NodeTreeInterfaceSocketFloatColorTemperature.draw

NodeTreeInterfaceSocketFloatDistance.draw

NodeTreeInterfaceSocketFloatFactor.draw

NodeTreeInterfaceSocketFloatFrequency.draw

NodeTreeInterfaceSocketFloatPercentage.draw

NodeTreeInterfaceSocketFloatTime.draw

NodeTreeInterfaceSocketFloatTimeAbsolute.draw

NodeTreeInterfaceSocketFloatUnsigned.draw

NodeTreeInterfaceSocketFloatWavelength.draw

NodeTreeInterfaceSocketGeometry.draw

NodeTreeInterfaceSocketImage.draw

NodeTreeInterfaceSocketInt.draw

NodeTreeInterfaceSocketIntFactor.draw

NodeTreeInterfaceSocketIntPercentage.draw

NodeTreeInterfaceSocketIntUnsigned.draw

NodeTreeInterfaceSocketMaterial.draw

NodeTreeInterfaceSocketMatrix.draw

NodeTreeInterfaceSocketMenu.draw

NodeTreeInterfaceSocketObject.draw

NodeTreeInterfaceSocketRotation.draw

NodeTreeInterfaceSocketShader.draw

NodeTreeInterfaceSocketString.draw

NodeTreeInterfaceSocketStringFilePath.draw

NodeTreeInterfaceSocketTexture.draw

NodeTreeInterfaceSocketVector.draw

NodeTreeInterfaceSocketVector2D.draw

NodeTreeInterfaceSocketVector4D.draw

NodeTreeInterfaceSocketVectorAcceleration.draw

NodeTreeInterfaceSocketVectorAcceleration2D.draw

NodeTreeInterfaceSocketVectorAcceleration4D.draw

NodeTreeInterfaceSocketVectorDirection.draw

NodeTreeInterfaceSocketVectorDirection2D.draw

NodeTreeInterfaceSocketVectorDirection4D.draw

NodeTreeInterfaceSocketVectorEuler.draw

NodeTreeInterfaceSocketVectorEuler2D.draw

NodeTreeInterfaceSocketVectorEuler4D.draw

NodeTreeInterfaceSocketVectorFactor.draw

NodeTreeInterfaceSocketVectorFactor2D.draw

NodeTreeInterfaceSocketVectorFactor4D.draw

NodeTreeInterfaceSocketVectorPercentage.draw

NodeTreeInterfaceSocketVectorPercentage2D.draw

NodeTreeInterfaceSocketVectorPercentage4D.draw

NodeTreeInterfaceSocketVectorTranslation.draw

NodeTreeInterfaceSocketVectorTranslation2D.draw

NodeTreeInterfaceSocketVectorTranslation4D.draw

NodeTreeInterfaceSocketVectorVelocity.draw

NodeTreeInterfaceSocketVectorVelocity2D.draw

NodeTreeInterfaceSocketVectorVelocity4D.draw

NodeTreeInterfaceSocketVectorXYZ.draw

NodeTreeInterfaceSocketVectorXYZ2D.draw

NodeTreeInterfaceSocketVectorXYZ4D.draw

Panel.draw_header_preset

RenderEngine.view_draw

RenderEngine.view_update

XrSessionState.action_binding_create

XrSessionState.action_create

XrSessionState.action_set_create

XrSessionState.action_state_get

XrSessionState.active_action_set_set

XrSessionState.controller_aim_location_get

XrSessionState.controller_aim_rotation_get

XrSessionState.controller_grip_location_get

XrSessionState.controller_grip_rotation_get

XrSessionState.controller_pose_actions_set

XrSessionState.haptic_action_apply

XrSessionState.haptic_action_stop

XrSessionState.is_running

XrSessionState.reset_to_base_pose

**Examples:**

Example 1 (sql):
```sql
import bpy
from bpy import context

# Reload the current file and select all.
bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)
window = context.window_manager.windows[0]
with context.temp_override(window=window):
    bpy.ops.mesh.primitive_uv_sphere_add()
    # The context override is needed so it's possible to set edit-mode.
    bpy.ops.object.mode_set(mode='EDIT')
```

Example 2 (python):
```python
import bpy
from bpy import context

win_active = context.window
win_other = None
for win_iter in context.window_manager.windows:
    if win_iter != win_active:
        win_other = win_iter
        break

# Add cube in the other window.
with context.temp_override(window=win_other):
    bpy.ops.mesh.primitive_cube_add()
```

Example 3 (python):
```python
import bpy
from bpy import context

my_objects = [context.scene.camera]

with context.temp_override(selected_objects=my_objects) as override:
    override.logging_set(True)  # Enable logging.
    bpy.ops.object.delete()
```

---

## CopyLocationConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CopyLocationConstraint.html

**Contents:**
- CopyLocationConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Copy the location of the target

Target along length of bone: Head is 0, Tail is 1

float in [0, 1], default 0.0

Invert the X location

boolean, default False

Invert the Y location

boolean, default False

Invert the Z location

boolean, default False

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Follow shape of B-Bone segments when calculating Head/Tail position

boolean, default False

Add original location into copied location

boolean, default False

Copy the target’s X location

boolean, default False

Copy the target’s Y location

boolean, default False

Copy the target’s Z location

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## CopyScaleConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CopyScaleConstraint.html

**Contents:**
- CopyScaleConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Copy the scale of the target

Raise the target’s scale to the specified power

float in [-inf, inf], default 1.0

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Use addition instead of multiplication to combine scale (2.7 compatibility)

boolean, default False

Redistribute the copied change in volume equally between the three axes of the owner

boolean, default False

Combine original scale with copied scale

boolean, default False

Copy the target’s X scale

boolean, default False

Copy the target’s Y scale

boolean, default False

Copy the target’s Z scale

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## CopyTransformsConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CopyTransformsConstraint.html

**Contents:**
- CopyTransformsConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Copy all the transforms of the target

Target along length of bone: Head is 0, Tail is 1

float in [0, 1], default 0.0

Specify how the copied and existing transformations are combined

REPLACE Replace – Replace the original transformation with copied.

BEFORE_FULL Before Original (Full) – Apply copied transformation before original, using simple matrix multiplication as if the constraint target is a parent in Full Inherit Scale mode. Will create shear when combining rotation and non-uniform scale..

BEFORE Before Original (Aligned) – Apply copied transformation before original, as if the constraint target is a parent in Aligned Inherit Scale mode. This effectively uses Full for location and Split Channels for rotation and scale..

BEFORE_SPLIT Before Original (Split Channels) – Apply copied transformation before original, handling location, rotation and scale separately, similar to a sequence of three Copy constraints.

AFTER_FULL After Original (Full) – Apply copied transformation after original, using simple matrix multiplication as if the constraint target is a child in Full Inherit Scale mode. Will create shear when combining rotation and non-uniform scale..

AFTER After Original (Aligned) – Apply copied transformation after original, as if the constraint target is a child in Aligned Inherit Scale mode. This effectively uses Full for location and Split Channels for rotation and scale..

AFTER_SPLIT After Original (Split Channels) – Apply copied transformation after original, handling location, rotation and scale separately, similar to a sequence of three Copy constraints.

enum in ['REPLACE', 'BEFORE_FULL', 'BEFORE', 'BEFORE_SPLIT', 'AFTER_FULL', 'AFTER', 'AFTER_SPLIT'], default 'REPLACE'

Remove shear from the target transformation before combining

boolean, default False

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Follow shape of B-Bone segments when calculating Head/Tail position

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## CorrectiveSmoothModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CorrectiveSmoothModifier.html

**Contents:**
- CorrectiveSmoothModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Correct distortion caused by deformation

float in [-inf, inf], default 0.5

Invert vertex group influence

boolean, default False

boolean, default False, (readonly)

int in [0, 32767], default 5

Select the source of rest positions

ORCO Original Coords – Use base mesh vertex coordinates as the rest position.

BIND Bind Coords – Use bind vertex coordinates for rest position.

enum in ['ORCO', 'BIND'], default 'ORCO'

Compensate for scale applied by other modifiers

float in [-inf, inf], default 1.0

Method used for smoothing

SIMPLE Simple – Use the average of adjacent edge-vertices.

LENGTH_WEIGHTED Length Weight – Use the average of adjacent edge-vertices weighted by their length.

enum in ['SIMPLE', 'LENGTH_WEIGHTED'], default 'SIMPLE'

Apply smoothing without reconstructing the surface

boolean, default False

Excludes boundary vertices from being smoothed

boolean, default False

Name of Vertex Group which determines influence of modifier per point

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## CrossStrip(EffectStrip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CrossStrip.html

**Contents:**
- CrossStrip(EffectStrip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip, EffectStrip

First input for the effect strip

Second input for the effect strip

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

EffectStrip.use_deinterlace

EffectStrip.alpha_mode

EffectStrip.use_flip_x

EffectStrip.use_flip_y

EffectStrip.use_float

EffectStrip.use_reverse_frames

EffectStrip.color_multiply

EffectStrip.multiply_alpha

EffectStrip.color_saturation

EffectStrip.transform

EffectStrip.use_proxy

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

EffectStrip.bl_rna_get_subclass

EffectStrip.bl_rna_get_subclass_py

---

## CryptomatteEntry(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CryptomatteEntry.html

**Contents:**
- CryptomatteEntry(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

float in [-inf, inf], default 0.0, (readonly)

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CompositorNodeCryptomatteV2.entries

---

## Curve(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Curve.html

**Contents:**
- Curve(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

subclasses — SurfaceCurve, TextCurve

Curve data-block storing curves, splines and NURBS

Animation data for this data-block

Radius of the bevel geometry, not including extrusion

float in [-inf, inf], default 0.0

Define where along the spline the curve geometry ends (0 for the beginning, 1 for the end)

float in [0, 1], default 1.0

Determine how the geometry end factor is mapped to a spline

RESOLUTION Resolution – Map the geometry factor to the number of subdivisions of a spline (U resolution).

SEGMENTS Segments – Map the geometry factor to the length of a segment and to the number of subdivisions of a segment.

SPLINE Spline – Map the geometry factor to the length of a spline.

enum in ['RESOLUTION', 'SEGMENTS', 'SPLINE'], default 'RESOLUTION'

Determine how the geometry start factor is mapped to a spline

RESOLUTION Resolution – Map the geometry factor to the number of subdivisions of a spline (U resolution).

SEGMENTS Segments – Map the geometry factor to the length of a segment and to the number of subdivisions of a segment.

SPLINE Spline – Map the geometry factor to the length of a spline.

enum in ['RESOLUTION', 'SEGMENTS', 'SPLINE'], default 'RESOLUTION'

Define where along the spline the curve geometry starts (0 for the beginning, 1 for the end)

float in [0, 1], default 0.0

Determine how to build the curve’s bevel geometry

ROUND Round – Use circle for the section of the curve’s bevel geometry.

OBJECT Object – Use an object for the section of the curve’s bevel geometry segment.

PROFILE Profile – Use a custom profile for each quarter of curve’s bevel geometry.

enum in ['ROUND', 'OBJECT', 'PROFILE'], default 'ROUND'

The name of the Curve object that defines the bevel shape

The path for the curve’s custom profile

CurveProfile, (readonly)

The number of segments in each quarter-circle of the bevel

int in [0, 32], default 4

CyclesMeshSettings, (readonly)

Select 2D or 3D curve type

2D 2D – Clamp the Z axis of the curve.

3D 3D – Allow editing on the Z axis of this curve, also allows tilt and curve radius to be used.

enum in ['2D', '3D'], default '2D'

Parametric position along the length of the curve that Objects ‘following’ it should be at (position is evaluated by dividing by the ‘Path Length’ value)

float in [-inf, inf], default 0.0

Length of the depth added in the local Z direction along the curve, perpendicular to its normals

float in [0, inf], default 0.0

Mode of filling curve

enum in ['FULL', 'BACK', 'FRONT', 'HALF'], default 'FULL'

True when used in editmode

boolean, default False, (readonly)

IDMaterials bpy_prop_collection of Material, (readonly)

Distance to move the curve parallel to its normals

float in [-inf, inf], default 0.0

The number of frames that are needed to traverse the path, defining the maximum value for the ‘Evaluation Time’ setting

int in [1, 1048574], default 100

Surface resolution in U direction used while rendering (zero uses preview resolution)

int in [0, 1024], default 0

Surface resolution in V direction used while rendering (zero uses preview resolution)

int in [0, 1024], default 0

Number of computed points in the U direction between every pair of control points

int in [1, 1024], default 12

The number of computed points in the V direction between every pair of control points

int in [1, 1024], default 12

Collection of splines in this curve data object

CurveSplines bpy_prop_collection of Spline, (readonly)

Curve object name that defines the taper (width)

Determine how the effective radius of the spline point is computed when a taper object is specified

OVERRIDE Override – Override the radius of the spline point with the taper radius.

MULTIPLY Multiply – Multiply the radius of the spline point by the taper radius.

ADD Add – Add the radius of the bevel point to the taper radius.

enum in ['OVERRIDE', 'MULTIPLY', 'ADD'], default 'OVERRIDE'

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

The type of tilt calculation for 3D Curves

Z_UP Z-Up – Use Z-Up axis to calculate the curve twist at each point.

MINIMUM Minimum – Use the least twist over the entire curve.

TANGENT Tangent – Use the tangent to calculate twist.

enum in ['Z_UP', 'MINIMUM', 'TANGENT'], default 'MINIMUM'

Smoothing iteration for tangents

float in [-inf, inf], default 0.0

Adjust active object’s texture space automatically when transforming object

boolean, default True

Option for curve-deform: Use the mesh bounds to clamp the deformation

boolean, default False

Fill caps for beveled curves

boolean, default False

Map effect of the taper object to the beveled part of the curve

boolean, default False

Enable the curve to become a translation path

boolean, default False

Clamp the curve path children so they cannot travel past the start/end point of the curve

boolean, default False

Make curve path children rotate along the path

boolean, default False

Option for paths and curve-deform: apply the curve radius to objects following it and to deformed objects

boolean, default True

Option for curve-deform: make deformed child stretch along entire path

boolean, default False

Transform curve by a matrix

matrix (mathutils.Matrix of 4 * 4 items in [-inf, inf]) – Matrix

shape_keys (boolean, (optional)) – Transform Shape Keys

Validate material indices of splines or letters, return True when the curve has had invalid indices corrected (to default 0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendDataCurves.remove

---

## CurveMapPoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveMapPoint.html

**Contents:**
- CurveMapPoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Point of a curve used for a curve mapping

Curve interpolation at this point: Bézier or vector

enum in ['AUTO', 'AUTO_CLAMPED', 'VECTOR'], default 'AUTO'

X/Y coordinates of the curve point

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

Selection state of the curve point

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CurveMapPoints.remove

---

## CurveMapPoints(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveMapPoints.html

**Contents:**
- CurveMapPoints(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Curve Map Points

Add point to CurveMap

position (float in [-inf, inf]) – Position, Position to add point

value (float in [-inf, inf]) – Value, Value of point

Delete point from CurveMap

point (CurveMapPoint, (never None)) – PointElement to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CurveMap(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveMap.html

**Contents:**
- CurveMap(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Curve in a curve mapping

CurveMapPoints bpy_prop_collection of CurveMapPoint, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CurveMapping.evaluate

---

## CurveMapping(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveMapping.html

**Contents:**
- CurveMapping(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Curve mapping to map color, vector and scalar values to other values using a user defined curve

For RGB curves, the color that black is mapped to

mathutils.Color of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

float in [-100, 100], default 0.0

float in [-100, 100], default 0.0

float in [-100, 100], default 0.0

float in [-100, 100], default 0.0

bpy_prop_collection of CurveMap, (readonly)

Extrapolate the curve or extend it horizontally

enum in ['HORIZONTAL', 'EXTRAPOLATED'], default 'HORIZONTAL'

STANDARD Standard – Combined curve is applied to each channel individually, which may result in a change of hue.

FILMLIKE Filmlike – Keeps the hue constant.

enum in ['STANDARD', 'FILMLIKE'], default 'STANDARD'

Force the curve view to fit a defined boundary

boolean, default False

For RGB curves, the color that white is mapped to

mathutils.Color of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

Update curve mapping after making changes

Reset the curve mapping grid to its clipping size

Evaluate curve at given location

curve (CurveMap, (never None)) – curve, Curve to evaluate

position (float in [-inf, inf]) – Position, Position to evaluate curve at

Value, Value of curve at given location

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Brush.automasking_cavity_curve

Brush.curve_distance_falloff

Brush.curve_random_hue

Brush.curve_random_saturation

Brush.curve_random_value

BrushCurvesSculptSettings.curve_parameter_falloff

BrushGpencilSettings.curve_jitter

BrushGpencilSettings.curve_random_hue

BrushGpencilSettings.curve_random_pressure

BrushGpencilSettings.curve_random_saturation

BrushGpencilSettings.curve_random_strength

BrushGpencilSettings.curve_random_uv

BrushGpencilSettings.curve_random_value

BrushGpencilSettings.curve_sensitivity

BrushGpencilSettings.curve_strength

ColorManagedViewSettings.curve_mapping

CompositorNodeCurveRGB.mapping

CompositorNodeHueCorrect.mapping

CompositorNodeTime.curve

CurvesModifier.curve_mapping

EQCurveMappingData.curve_mapping

GPencilInterpolateSettings.interpolation_curve

GPencilSculptSettings.multiframe_falloff_curve

GPencilSculptSettings.thickness_primitive_curve

GreasePencilColorModifier.custom_curve

GreasePencilHookModifier.custom_curve

GreasePencilNoiseModifier.custom_curve

GreasePencilOpacityModifier.custom_curve

GreasePencilSmoothModifier.custom_curve

GreasePencilThickModifierData.custom_curve

GreasePencilTintModifier.custom_curve

HookModifier.falloff_curve

HueCorrectModifier.curve_mapping

LineStyleAlphaModifier_AlongStroke.curve

LineStyleAlphaModifier_CreaseAngle.curve

LineStyleAlphaModifier_Curvature_3D.curve

LineStyleAlphaModifier_DistanceFromCamera.curve

LineStyleAlphaModifier_DistanceFromObject.curve

LineStyleAlphaModifier_Material.curve

LineStyleAlphaModifier_Noise.curve

LineStyleAlphaModifier_Tangent.curve

LineStyleThicknessModifier_AlongStroke.curve

LineStyleThicknessModifier_CreaseAngle.curve

LineStyleThicknessModifier_Curvature_3D.curve

LineStyleThicknessModifier_DistanceFromCamera.curve

LineStyleThicknessModifier_DistanceFromObject.curve

LineStyleThicknessModifier_Material.curve

LineStyleThicknessModifier_Tangent.curve

ParticleSettings.clump_curve

ParticleSettings.roughness_curve

ParticleSettings.twist_curve

RenderSettings.motion_blur_shutter_curve

Sculpt.automasking_cavity_curve

Sculpt.automasking_cavity_curve_op

ShaderNodeFloatCurve.mapping

ShaderNodeRGBCurve.mapping

ShaderNodeVectorCurve.mapping

TextureNodeCurveRGB.mapping

TextureNodeCurveTime.curve

UvSculpt.curve_distance_falloff

VertexWeightEditModifier.map_curve

VertexWeightProximityModifier.map_curve

WarpModifier.falloff_curve

---

## CurveModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveModifier.html

**Contents:**
- CurveModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Curve deformation modifier

The axis that the curve deforms along

enum in ['POS_X', 'POS_Y', 'POS_Z', 'NEG_X', 'NEG_Y', 'NEG_Z'], default 'POS_X'

Invert vertex group influence

boolean, default False

Curve object to deform with

Name of Vertex Group which determines influence of modifier per point

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## CurvePaintSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurvePaintSettings.html

**Contents:**
- CurvePaintSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Angles above this are considered corners

float in [0, 3.14159], default 1.22173

Type of curve to use for new strokes

enum in ['POLY', 'BEZIER'], default 'BEZIER'

Method of projecting depth

enum in ['CURSOR', 'SURFACE'], default 'CURSOR'

Allow deviation for a smoother, less precise line

int in [1, 100], default 8

enum in Curve Fit Method Items, default 'REFIT'

Radius to use when the maximum pressure is applied (or when a tablet isn’t used)

float in [0, 100], default 1.0

Minimum radius when the minimum pressure is applied (also the minimum when tapering)

float in [0, 100], default 0.0

Taper factor for the radius of each point along the curve

float in [0, 10], default 0.0

Taper factor for the radius of each point along the curve

float in [0, 1], default 0.0

Offset the stroke from the surface

float in [-10, 10], default 0.0

Plane for projected stroke

NORMAL_VIEW Normal to Surface – Draw in a plane perpendicular to the surface.

NORMAL_SURFACE Tangent to Surface – Draw in the surface plane.

VIEW View – Draw in a plane aligned to the viewport.

enum in ['NORMAL_VIEW', 'NORMAL_SURFACE', 'VIEW'], default 'NORMAL_VIEW'

Detect corners and use non-aligned handles

boolean, default True

Apply a fixed offset (don’t scale by the radius)

boolean, default False

Map tablet pressure to curve radius

boolean, default False

Project the strokes only onto selected objects

boolean, default False

Use the start of the stroke for the depth

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ToolSettings.curve_paint_settings

---

## CurvePoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurvePoint.html

**Contents:**
- CurvePoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

int in [0, inf], default 0, (readonly)

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

float in [-inf, inf], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CurveProfile(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveProfile.html

**Contents:**
- CurveProfile(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Profile Path editor used to build a profile path

Profile control points

CurveProfilePoints bpy_prop_collection of CurveProfilePoint, (readonly)

SUPPORTS Support Loops – Loops on each side of the profile.

CORNICE Cornice Molding.

STEPS Steps – A number of steps defined by the segments.

enum in ['LINE', 'SUPPORTS', 'CORNICE', 'CROWN', 'STEPS'], default 'LINE'

Segments sampled from control points

bpy_prop_collection of CurveProfilePoint, (readonly)

Force the path view to fit a defined boundary

boolean, default False

Sample edges with even lengths

boolean, default False

Sample edges with vector handles

boolean, default False

Refresh internal data, remove doubles and clip points

Reset the curve profile grid to its clipping size

Set the number of display segments and fill tables

totsegments (int in [1, 1000], (never None)) – The number of segment values to initialize the segments table with

Evaluate the at the given portion of the path length

length_portion (float in [0, 1]) – Length Portion, Portion of the path length to travel before evaluation

Location, The location at the given portion of the profile

mathutils.Vector of 2 items in [-100, 100]

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BevelModifier.custom_profile

ToolSettings.custom_bevel_profile_preset

---

## CurveSlice(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveSlice.html

**Contents:**
- CurveSlice(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

A single curve from a curves data-block

The index of this curve’s first control point

int in [0, inf], default 0, (readonly)

int in [0, inf], default 0, (readonly)

Control points of the curve

bpy_prop_collection of CurvePoint, (readonly)

Number of control points in the curve

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CurveProfilePoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveProfilePoint.html

**Contents:**
- CurveProfilePoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Point of a path used to define a profile

Path interpolation at this point

enum in ['AUTO', 'VECTOR', 'FREE', 'ALIGN'], default 'FREE'

Path interpolation at this point

enum in ['AUTO', 'VECTOR', 'FREE', 'ALIGN'], default 'FREE'

X/Y coordinates of the path point

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

Selection state of the path point

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

CurveProfile.segments

CurveProfilePoints.add

CurveProfilePoints.remove

---

## CurveProfilePoints(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveProfilePoints.html

**Contents:**
- CurveProfilePoints(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Profile Points

Add point to the profile

x (float in [-inf, inf]) – X Position, X Position for new point

y (float in [-inf, inf]) – Y Position, Y Position for new point

Delete point from the profile

point (CurveProfilePoint, (never None)) – Point to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CurveSplines(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurveSplines.html

**Contents:**
- CurveSplines(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of curve splines

Add a new spline to the curve

type (enum in ['POLY', 'BEZIER', 'NURBS']) – type for the new spline

The newly created spline

Remove a spline from a curve

spline (Spline, (never None)) – The spline to remove

Remove all splines from a curve

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## CurvesModifier(StripModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurvesModifier.html

**Contents:**
- CurvesModifier(StripModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, StripModifier

RGB curves modifier for sequence strip

CurveMapping, (readonly)

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

StripModifier.show_expanded

StripModifier.input_mask_type

StripModifier.mask_time

StripModifier.input_mask_strip

StripModifier.input_mask_id

StripModifier.is_active

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

StripModifier.bl_rna_get_subclass

StripModifier.bl_rna_get_subclass_py

---

## Curves(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Curves.html

**Contents:**
- Curves(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Hair data-block for hair curves

Animation data for this data-block

AttributeGroupCurves bpy_prop_collection of Attribute, (readonly)

Geometry color attributes

AttributeGroupCurves bpy_prop_collection of Attribute, (readonly)

bpy_prop_collection of IntAttributeValue, (readonly)

All curves in the data-block

bpy_prop_collection of CurveSlice, (readonly)

IDMaterials bpy_prop_collection of Material, (readonly)

The curve normal value at each of the curve’s control points

bpy_prop_collection of FloatVectorValueReadOnly, (readonly)

Control points of all curves

bpy_prop_collection of CurvePoint, (readonly)

bpy_prop_collection of FloatVectorAttributeValue, (readonly)

enum in Attribute Curves Domain Items, default 'POINT'

Mesh object that the curves can be attached to

Distance to keep the curves away from the surface

float in [1.192e-07, inf], default 0.005

The name of the attribute on the surface mesh used to define the attachment of each curve

string, default “”, (never None)

Enable symmetry in the X axis

boolean, default False

Enable symmetry in the Y axis

boolean, default False

Enable symmetry in the Z axis

boolean, default False

Enable collision with the surface while sculpting

boolean, default False

sizes (int array of 1 items in [0, inf]) – Sizes, The number of points in each curve

Remove all curves. If indices are provided, remove only the curves with the given indices.

indices (int array of 1 items in [0, inf], (optional)) – Indices, The indices of the curves to remove

Resize all existing curves. If indices are provided, resize only the curves with the given indices. If the new size for a curve is smaller, the curve is trimmed. If the new size for a curve is larger, the new end values are default initialized.

sizes (int array of 1 items in [1, inf]) – Sizes, The number of points in each curve

indices (int array of 1 items in [0, inf], (optional)) – Indices, The indices of the curves to resize

Reorder the curves by the new indices.

new_indices (int array of 1 items in [0, inf]) – New indices, The new index for each of the curves

Set the curve type. If indices are provided, set only the types with the given curve indices.

type (enum in Curves Type Items, (optional)) – Type

indices (int array of 1 items in [0, inf], (optional)) – Indices, The indices of the curves to resize

curves (Curves, (optional)) – Curves to compare to

threshold (float in [0, inf], (optional)) – Threshold, Comparison tolerance threshold

Return value, String description of result of comparison

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

BlendData.hair_curves

BlendDataHairCurves.new

BlendDataHairCurves.remove

Curves.unit_test_compare

---

## CurvesSculpt(Paint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.CurvesSculpt.html

**Contents:**
- CurvesSculpt(Paint)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, Paint

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Paint.brush_asset_reference

Paint.eraser_brush_asset_reference

Paint.show_brush_on_surface

Paint.show_low_resolution

Paint.use_sculpt_delay_updates

Paint.use_symmetry_feather

Paint.show_strength_curve

Paint.show_size_curve

Paint.show_jitter_curve

Paint.unified_paint_settings

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Paint.bl_rna_get_subclass

Paint.bl_rna_get_subclass_py

ToolSettings.curves_sculpt

---

## DATA_UL_bone_collections(UIList)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DATA_UL_bone_collections.html

**Contents:**
- DATA_UL_bone_collections(UIList)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, UIList

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

UIList.use_filter_show

UIList.use_filter_invert

UIList.use_filter_sort_alpha

UIList.use_filter_sort_reverse

UIList.use_filter_sort_lock

UIList.bitflag_filter_item

UIList.bitflag_item_never_show

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

UIList.bl_system_properties_get

UIList.bl_rna_get_subclass

UIList.bl_rna_get_subclass_py

---

## DampedTrackConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DampedTrackConstraint.html

**Contents:**
- DampedTrackConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Point toward target by taking the shortest rotation path

Target along length of bone: Head is 0, Tail is 1

float in [0, 1], default 0.0

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Axis that points to the target object

enum in ['TRACK_X', 'TRACK_Y', 'TRACK_Z', 'TRACK_NEGATIVE_X', 'TRACK_NEGATIVE_Y', 'TRACK_NEGATIVE_Z'], default 'TRACK_X'

Follow shape of B-Bone segments when calculating Head/Tail position

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## DataTransferModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DataTransferModifier.html

**Contents:**
- DataTransferModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Modifier transferring some data from a source mesh

Which edge data layers to transfer

SHARP_EDGE Sharp – Transfer sharp mark.

SEAM UV Seam – Transfer UV seam mark.

CREASE Crease – Transfer subdivision crease values.

BEVEL_WEIGHT_EDGE Bevel Weight – Transfer bevel weights.

FREESTYLE_EDGE Freestyle – Transfer Freestyle edge mark.

enum set in {'SHARP_EDGE', 'SEAM', 'CREASE', 'BEVEL_WEIGHT_EDGE', 'FREESTYLE_EDGE'}, default set()

Which face corner data layers to transfer

CUSTOM_NORMAL Custom Normals – Transfer custom normals.

COLOR_CORNER Colors – Transfer color attributes.

UV UVs – Transfer UV layers.

enum set in {'CUSTOM_NORMAL', 'COLOR_CORNER', 'UV'}, default set()

Which face data layers to transfer

SMOOTH Smooth – Transfer flat/smooth mark.

FREESTYLE_FACE Freestyle Mark – Transfer Freestyle face mark.

enum set in {'SMOOTH', 'FREESTYLE_FACE'}, default set()

Which vertex data layers to transfer

VGROUP_WEIGHTS Vertex Groups – Transfer active or all vertex groups.

BEVEL_WEIGHT_VERT Bevel Weight – Transfer bevel weights.

COLOR_VERTEX Colors – Transfer color attributes.

enum set in {'VGROUP_WEIGHTS', 'BEVEL_WEIGHT_VERT', 'COLOR_VERTEX'}, default set()

Method used to map source edges to destination ones

enum in Dt Method Edge Items, default 'NEAREST'

Invert vertex group influence

boolean, default False

Factor controlling precision of islands handling (typically, 0.1 should be enough, higher values can make things really slow)

float in [0, 1], default 0.0

How to match source and destination layers

enum in Dt Layers Select Dst Items, default 'NAME'

Which layers to transfer, in case of multi-layers types

enum in Dt Layers Select Src Items, default 'ALL'

How to match source and destination layers

enum in Dt Layers Select Dst Items, default 'NAME'

Which layers to transfer, in case of multi-layers types

enum in Dt Layers Select Src Items, default 'ALL'

How to match source and destination layers

enum in Dt Layers Select Dst Items, default 'NAME'

Which layers to transfer, in case of multi-layers types

enum in Dt Layers Select Src Items, default 'ALL'

How to match source and destination layers

enum in Dt Layers Select Dst Items, default 'NAME'

Which layers to transfer, in case of multi-layers types

enum in Dt Layers Select Src Items, default 'ALL'

Method used to map source faces’ corners to destination ones

enum in Dt Method Loop Items, default 'NEAREST_POLYNOR'

Maximum allowed distance between source and destination element, for non-topology mappings

float in [0, inf], default 1.0

Factor to use when applying data to destination (exact behavior depends on mix mode, multiplied with weights from vertex group when defined)

float in [0, 1], default 0.0

How to affect destination elements with source values

enum in Dt Mix Mode Items, default 'REPLACE'

Object to transfer data from

Method used to map source faces to destination ones

enum in Dt Method Poly Items, default 'NEAREST'

‘Width’ of rays (especially useful when raycasting against vertices or edges)

float in [0, inf], default 0.0

Enable edge data transfer

boolean, default False

Enable face corner data transfer

boolean, default False

Source elements must be closer than given distance from destination one

boolean, default False

Evaluate source and destination meshes in global space

boolean, default True

Enable face data transfer

boolean, default False

Enable vertex data transfer

boolean, default False

Method used to map source vertices to destination ones

enum in Dt Method Vertex Items, default 'NEAREST'

Vertex group name for selecting the affected areas

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## DecimateModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DecimateModifier.html

**Contents:**
- DecimateModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Only dissolve angles below this (planar only)

float in [0, 3.14159], default 0.0872665

COLLAPSE Collapse – Use edge collapsing.

UNSUBDIV Un-Subdivide – Use un-subdivide face reduction.

DISSOLVE Planar – Dissolve geometry to form planar polygons.

enum in ['COLLAPSE', 'UNSUBDIV', 'DISSOLVE'], default 'COLLAPSE'

Limit merging geometry

enum set in Mesh Delimit Mode Items, default set()

The current number of faces in the decimated mesh

int in [-inf, inf], default 0, (readonly)

Invert vertex group influence (collapse only)

boolean, default False

Number of times reduce the geometry (unsubdivide only)

int in [0, 32767], default 0

Ratio of triangles to reduce to (collapse only)

float in [0, 1], default 1.0

enum in Axis Xyz Items, default 'X'

Keep triangulated faces resulting from decimation (collapse only)

boolean, default False

Dissolve all vertices in between face boundaries (planar only)

boolean, default False

Maintain symmetry on an axis

boolean, default False

Vertex group name (collapse only)

string, default “”, (never None)

Vertex group strength

float in [0, 1000], default 1.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## Depsgraph(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Depsgraph.html

**Contents:**
- Depsgraph(bpy_struct)¶
- Dependency graph: Evaluated ID example¶
- Dependency graph: Original object example¶
- Dependency graph: Iterate over all object instances¶
- Dependency graph: Object.to_mesh()¶
- Dependency graph: bpy.data.meshes.new_from_object()¶
- Dependency graph: Simple exporter¶
- Dependency graph: Object.to_curve()¶
  - Inherited Properties¶
  - Inherited Functions¶

This example demonstrates access to the evaluated ID (such as object, material, etc.) state from an original ID. This is needed every time one needs to access state with animation, constraints, and modifiers taken into account.

This example demonstrates access to the original ID. Such access is needed to check whether object is selected, or to compare pointers.

Sometimes it is needed to know all the instances with their matrices (for example, when writing an exporter or a custom render engine). This example shows how to access all objects and instances in the scene.

Function to get a mesh from any object with geometry. It is typically used by exporters, render engines and tools that need to access the evaluated mesh as displayed in the viewport.

Object.to_mesh() is closely interacting with dependency graph: its behavior depends on whether it is used on original or evaluated object.

When is used on original object, the result mesh is calculated from the object without taking animation or modifiers into account:

For meshes this is similar to duplicating the source mesh.

For curves this disables own modifiers, and modifiers of objects used as bevel and taper.

For meta-balls this produces an empty mesh since polygonization is done as a modifier evaluation.

When is used on evaluated object all modifiers are taken into account.

The result mesh is owned by the object. It can be freed by calling to_mesh_clear().

The result mesh must be treated as temporary, and cannot be referenced from objects in the main database. If the mesh intended to be used in a persistent manner use new_from_object() instead.

If object does not have geometry (i.e. camera) the functions returns None.

Function to copy a new mesh from any object with geometry. The mesh is added to the main database and can be referenced by objects. Typically used by tools that create new objects or apply modifiers.

When is used on original object, the result mesh is calculated from the object without taking animation or modifiers into account:

For meshes this is similar to duplicating the source mesh.

For curves this disables own modifiers, and modifiers of objects used as bevel and taper.

For meta-balls this produces an empty mesh since polygonization is done as a modifier evaluation.

When is used on evaluated object all modifiers are taken into account.

All the references (such as materials) are re-mapped to original. This ensures validity and consistency of the main database.

If object does not have geometry (i.e. camera) the functions returns None.

This example is a combination of all previous ones, and shows how to write a simple exporter script.

Function to get a curve from text and curve objects. It is typically used by exporters, render engines, and tools that need to access the curve representing the object.

The function takes the evaluated dependency graph as a required parameter and optionally a boolean apply_modifiers which defaults to false. If apply_modifiers is true and the object is a curve object, the spline deform modifiers are applied on the control points. Note that constructive modifiers and modifiers that are not spline-enabled will not be applied. So modifiers like Array will not be applied and deform modifiers that have Apply On Spline disabled will not be applied.

If the object is a text object. The text will be converted into a 3D curve and returned. Modifiers are never applied on text objects and apply_modifiers will be ignored. If the object is neither a curve nor a text object, an error will be reported.

The resulting curve is owned by the object. It can be freed by calling to_curve_clear().

The resulting curve must be treated as temporary, and cannot be referenced from objects in the main database.

base class — bpy_struct

All evaluated data-blocks

bpy_prop_collection of ID, (readonly)

VIEWPORT Viewport – Viewport non-rendered mode.

RENDER Render – Render.

enum in ['VIEWPORT', 'RENDER'], default 'VIEWPORT', (readonly)

All object instances to display or render (Warning: Only use this as an iterator, never as a sequence, and do not keep any references to its items)

bpy_prop_collection of DepsgraphObjectInstance, (readonly)

Evaluated objects in the dependency graph

bpy_prop_collection of Object, (readonly)

Original scene dependency graph is built for

Scene at its evaluated state

Updates to data-blocks

bpy_prop_collection of DepsgraphUpdate, (readonly)

Original view layer dependency graph is built for

ViewLayer, (readonly)

View layer at its evaluated state

ViewLayer, (readonly)

debug_relations_graphviz

filepath (string, (optional, never None)) – File Name, Optional output path for the graphviz debug file

Dot Graph, Graph in dot format

filepath (string, (never None)) – File Name, Output path for the gnuplot debug file

output_filepath (string, (never None)) – Output File Name, File name where gnuplot script will save the result

Report the number of elements in the Dependency Graph

Re-evaluate any modified data-blocks, for example for animation or modifiers. This invalidates all references to evaluated data-blocks from this dependency graph.

id (ID) – Original ID to get evaluated complementary part for

Evaluated ID for the given original one

id_type (enum in Id Type Items) – ID Type

Updated, True if any data-block with this type was added, updated or removed

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

BlendDataMeshes.new_from_object

Context.evaluated_depsgraph_get

Object.calc_matrix_camera

Object.camera_fit_coords

Object.closest_point_on_mesh

Object.crazyspace_eval

RenderEngine.view_draw

RenderEngine.view_update

**Examples:**

Example 1 (swift):
```swift
import bpy


class OBJECT_OT_evaluated_example(bpy.types.Operator):
    """Access evaluated object state and do something with it"""
    bl_label = "DEG Access Evaluated Object"
    bl_idname = "object.evaluated_example"

    def execute(self, context):
        # This is an original object. Its data does not have any modifiers applied.
        obj = context.object
        if obj is None or obj.type != 'MESH':
            self.report({'INFO'}, "No active mesh object to get info from")
            return {'CANCELLED'}
        # Evaluated object exists within a specific dependency graph.
        # We will request evaluated object from the dependency graph which corresponds to the
        # current scene and view layer.
        #
        # NOTE: This call ensure the dependency graph is fully evaluated. This might be expensive
        # if changes were made to the scene, but is needed to ensure no dangling or incorrect
        # pointers are exposed.
        depsgraph = context.evaluated_depsgraph_get()
        # Actually request evaluated object.
        #
        # This object has animation and drivers applied on it, together with constraints and
        # modifiers.
        #
        # For mesh objects the object.data will be a mesh with all modifiers applied.
        # This means that in access to vertices or faces after modifier stack happens via fields of
        # object_eval.object.
        #
        # For other types of objects the object_eval.data does not have modifiers applied on it,
        # but has animation applied.
        #
        # NOTE: All ID types have `evaluated_get()`, including materials, node trees, worlds.
        object_eval = obj.evaluated_get(depsgraph)
        mesh_eval = object_eval.data
        self.report({'INFO'}, f"Number of evaluated vertices: {len(mesh_eval.vertices)}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_evaluated_example)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_evaluated_example)


if __name__ == "__main__":
    register()
```

Example 2 (swift):
```swift
import bpy


class OBJECT_OT_original_example(bpy.types.Operator):
    """Access original object and do something with it"""
    bl_label = "DEG Access Original Object"
    bl_idname = "object.original_example"

    def check_object_selected(self, object_eval):
        # Selection depends on a context and is only valid for original objects. This means we need
        # to request the original object from the known evaluated one.
        #
        # NOTE: All ID types have an `original` field.
        obj = object_eval.original
        return obj.select_get()

    def execute(self, context):
        # NOTE: It seems redundant to iterate over original objects to request evaluated ones
        # just to get original back. But we want to keep example as short as possible, but in real
        # world there are cases when evaluated object is coming from a more meaningful source.
        depsgraph = context.evaluated_depsgraph_get()
        for obj in context.editable_objects:
            object_eval = obj.evaluated_get(depsgraph)
            if self.check_object_selected(object_eval):
                self.report({'INFO'}, f"Object is selected: {object_eval.name}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_original_example)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_original_example)


if __name__ == "__main__":
    register()
```

Example 3 (swift):
```swift
import bpy


class OBJECT_OT_object_instances(bpy.types.Operator):
    """Access original object and do something with it"""
    bl_label = "DEG Iterate Object Instances"
    bl_idname = "object.object_instances"

    def execute(self, context):
        depsgraph = context.evaluated_depsgraph_get()
        for object_instance in depsgraph.object_instances:
            # This is an object which is being instanced.
            obj = object_instance.object
            # `is_instance` denotes whether the object is coming from instances (as an opposite of
            # being an emitting object. )
            if not object_instance.is_instance:
                print(f"Object {obj.name} at {object_instance.matrix_world}")
            else:
                # Instanced will additionally have fields like uv, random_id and others which are
                # specific for instances. See Python API for DepsgraphObjectInstance for details,
                print(f"Instance of {obj.name} at {object_instance.matrix_world}")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_object_instances)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_object_instances)


if __name__ == "__main__":
    register()
```

Example 4 (swift):
```swift
import bpy


class OBJECT_OT_object_to_mesh(bpy.types.Operator):
    """Convert selected object to mesh and show number of vertices"""
    bl_label = "DEG Object to Mesh"
    bl_idname = "object.object_to_mesh"

    def execute(self, context):
        # Access input original object.
        obj = context.object
        if obj is None:
            self.report({'INFO'}, "No active mesh object to convert to mesh")
            return {'CANCELLED'}
        # Avoid annoying None checks later on.
        if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
            self.report({'INFO'}, "Object cannot be converted to mesh")
            return {'CANCELLED'}
        depsgraph = context.evaluated_depsgraph_get()
        # Invoke to_mesh() for original object.
        mesh_from_orig = obj.to_mesh()
        self.report({'INFO'}, f"{len(mesh_from_orig.vertices)} in new mesh without modifiers.")
        # Remove temporary mesh.
        obj.to_mesh_clear()
        # Invoke to_mesh() for evaluated object.
        object_eval = obj.evaluated_get(depsgraph)
        mesh_from_eval = object_eval.to_mesh()
        self.report({'INFO'}, f"{len(mesh_from_eval.vertices)} in new mesh with modifiers.")
        # Remove temporary mesh.
        object_eval.to_mesh_clear()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_OT_object_to_mesh)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_object_to_mesh)


if __name__ == "__main__":
    register()
```

---

## DepsgraphObjectInstance(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DepsgraphObjectInstance.html

**Contents:**
- DepsgraphObjectInstance(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Extended information about dependency graph object iterator (Warning: All data here is ‘evaluated’ one, not original .blend IDs)

Evaluated object which is being instanced by this iterator

Denotes if the object is generated by another object

boolean, default False, (readonly)

Generated transform matrix in world space

mathutils.Matrix of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)), (readonly)

Evaluated object the iterator points to

Generated coordinates in parent object space

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

If the object is an instance, the parent object that generated it

Evaluated particle system that this object was instanced from

ParticleSystem, (readonly)

Persistent identifier for inter-frame matching of objects with motion blur

int array of 8 items in [-inf, inf], default (0, 0, 0, 0, 0, 0, 0, 0), (readonly)

Random id for this instance, typically for randomized shading

int in [0, inf], default 0, (readonly)

Particles part of the object should be visible in the render

boolean, default False, (readonly)

The object geometry itself should be visible in the render

boolean, default False, (readonly)

UV coordinates in parent object space

float array of 2 items in [-inf, inf], default (0.0, 0.0), (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Depsgraph.object_instances

---

## DepsgraphUpdate(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DepsgraphUpdate.html

**Contents:**
- DepsgraphUpdate(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Information about ID that was updated

Object geometry is updated

boolean, default False, (readonly)

Object shading is updated

boolean, default False, (readonly)

Object transformation is updated

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## DisplaceModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DisplaceModifier.html

**Contents:**
- DisplaceModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Displacement modifier

X X – Use the texture’s intensity value to displace in the X direction.

Y Y – Use the texture’s intensity value to displace in the Y direction.

Z Z – Use the texture’s intensity value to displace in the Z direction.

NORMAL Normal – Use the texture’s intensity value to displace along the vertex normal.

CUSTOM_NORMAL Custom Normal – Use the texture’s intensity value to displace along the (averaged) custom normal (falls back to vertex).

RGB_TO_XYZ RGB to XYZ – Use the texture’s RGB values to displace the mesh in the XYZ direction.

enum in ['X', 'Y', 'Z', 'NORMAL', 'CUSTOM_NORMAL', 'RGB_TO_XYZ'], default 'NORMAL'

Invert vertex group influence

boolean, default False

Material value that gives no displacement

float in [-inf, inf], default 0.5

LOCAL Local – Direction is defined in local coordinates.

GLOBAL Global – Direction is defined in global coordinates.

enum in ['LOCAL', 'GLOBAL'], default 'LOCAL'

Amount to displace geometry

float in [-inf, inf], default 1.0

LOCAL Local – Use the local coordinate system for the texture coordinates.

GLOBAL Global – Use the global coordinate system for the texture coordinates.

OBJECT Object – Use the linked object’s local coordinate system for the texture coordinates.

UV UV – Use UV coordinates for the texture coordinates.

enum in ['LOCAL', 'GLOBAL', 'OBJECT', 'UV'], default 'LOCAL'

Bone to set the texture coordinates

string, default “”, (never None)

Object to set the texture coordinates

string, default “”, (never None)

Name of Vertex Group which determines influence of modifier per point

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## DisplaySafeAreas(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DisplaySafeAreas.html

**Contents:**
- DisplaySafeAreas(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Safe areas used in 3D view and the sequencer

Safe area for general elements

mathutils.Vector of 2 items in [0, 1], default (0.035, 0.035)

Safe area for general elements in a different aspect ratio

mathutils.Vector of 2 items in [0, 1], default (0.15, 0.05)

Safe area for text and graphics

mathutils.Vector of 2 items in [0, 1], default (0.1, 0.05)

Safe area for text and graphics in a different aspect ratio

mathutils.Vector of 2 items in [0, 1], default (0.175, 0.05)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## DistortedNoiseTexture(Texture)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DistortedNoiseTexture.html

**Contents:**
- DistortedNoiseTexture(Texture)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ID, Texture

Procedural distorted noise texture

float in [0, 10], default 1.0

Size of derivative offset used for calculating normal

float in [0.001, 0.1], default 0.025

Noise basis used for turbulence

BLENDER_ORIGINAL Blender Original – Noise algorithm - Blender original: Smooth interpolated noise.

ORIGINAL_PERLIN Original Perlin – Noise algorithm - Original Perlin: Smooth interpolated noise.

IMPROVED_PERLIN Improved Perlin – Noise algorithm - Improved Perlin: Smooth interpolated noise.

VORONOI_F1 Voronoi F1 – Noise algorithm - Voronoi F1: Returns distance to the closest feature point.

VORONOI_F2 Voronoi F2 – Noise algorithm - Voronoi F2: Returns distance to the 2nd closest feature point.

VORONOI_F3 Voronoi F3 – Noise algorithm - Voronoi F3: Returns distance to the 3rd closest feature point.

VORONOI_F4 Voronoi F4 – Noise algorithm - Voronoi F4: Returns distance to the 4th closest feature point.

VORONOI_F2_F1 Voronoi F2-F1 – Noise algorithm - Voronoi F1-F2.

VORONOI_CRACKLE Voronoi Crackle – Noise algorithm - Voronoi Crackle: Voronoi tessellation with sharp edges.

CELL_NOISE Cell Noise – Noise algorithm - Cell Noise: Square cell tessellation.

enum in ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN', 'IMPROVED_PERLIN', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2_F1', 'VORONOI_CRACKLE', 'CELL_NOISE'], default 'BLENDER_ORIGINAL'

Noise basis for the distortion

BLENDER_ORIGINAL Blender Original – Noise algorithm - Blender original: Smooth interpolated noise.

ORIGINAL_PERLIN Original Perlin – Noise algorithm - Original Perlin: Smooth interpolated noise.

IMPROVED_PERLIN Improved Perlin – Noise algorithm - Improved Perlin: Smooth interpolated noise.

VORONOI_F1 Voronoi F1 – Noise algorithm - Voronoi F1: Returns distance to the closest feature point.

VORONOI_F2 Voronoi F2 – Noise algorithm - Voronoi F2: Returns distance to the 2nd closest feature point.

VORONOI_F3 Voronoi F3 – Noise algorithm - Voronoi F3: Returns distance to the 3rd closest feature point.

VORONOI_F4 Voronoi F4 – Noise algorithm - Voronoi F4: Returns distance to the 4th closest feature point.

VORONOI_F2_F1 Voronoi F2-F1 – Noise algorithm - Voronoi F1-F2.

VORONOI_CRACKLE Voronoi Crackle – Noise algorithm - Voronoi Crackle: Voronoi tessellation with sharp edges.

CELL_NOISE Cell Noise – Noise algorithm - Cell Noise: Square cell tessellation.

enum in ['BLENDER_ORIGINAL', 'ORIGINAL_PERLIN', 'IMPROVED_PERLIN', 'VORONOI_F1', 'VORONOI_F2', 'VORONOI_F3', 'VORONOI_F4', 'VORONOI_F2_F1', 'VORONOI_CRACKLE', 'CELL_NOISE'], default 'BLENDER_ORIGINAL'

Scaling for noise input

float in [0.0001, inf], default 0.25

Materials that use this texture

Takes O(len(bpy.data.materials) * len(material.texture_slots)) time.

Object modifiers that use this texture

Takes O(len(bpy.data.objects) * len(obj.modifiers)) time.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

Texture.use_color_ramp

Texture.use_preview_alpha

Texture.animation_data

Texture.users_material

Texture.users_object_modifier

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

Texture.bl_rna_get_subclass

Texture.bl_rna_get_subclass_py

---

## DopeSheet(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DopeSheet.html

**Contents:**
- DopeSheet(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Settings for filtering the channels shown in animation editors

Collection that included object should be a member of

F-Curve live filtering string

string, default “”, (never None)

Live filtering string

string, default “”, (never None)

Include visualization of armature related animation data

boolean, default False

Include visualization of cache file related animation data

boolean, default False

Include visualization of camera related animation data

boolean, default False

Include visualization of curve related animation data

boolean, default False

Show options for whether channels related to certain types of data are included

boolean, default False

Include drivers that relied on any fallback values for their evaluation in the Only Show Errors filter, even if the driver evaluation succeeded

boolean, default False

Collapse summary when shown, so all other channels get hidden (Dope Sheet editors only)

boolean, default False

Include visualization of Grease Pencil related animation data and frames

boolean, default False

Include visualization of hair related animation data

boolean, default False

Include channels from objects/bone that are not visible

boolean, default False

Include visualization of lattice related animation data

boolean, default False

Include visualization of lightprobe related animation data

boolean, default False

Include visualization of light related animation data

boolean, default False

Include visualization of Line Style related Animation data

boolean, default False

Include visualization of material related animation data

boolean, default False

Include visualization of mesh related animation data

boolean, default False

Include visualization of metaball related animation data

boolean, default False

Include animation data-blocks with no NLA data (NLA editor only)

boolean, default False

Include visualization of animation data related to data-blocks linked to modifiers

boolean, default False

Include visualization of movie clip related animation data

boolean, default False

Include visualization of node related animation data

boolean, default False

Only include F-Curves and drivers that are disabled or have errors

boolean, default False

Only include channels relating to selected objects and data

boolean, default False

Only show the slot of the active Object. Otherwise show all the Action’s Slots

boolean, default False

Include visualization of particle related animation data

boolean, default False

Include visualization of point cloud related animation data

boolean, default False

Include visualization of scene related animation data

boolean, default False

Include visualization of shape key related animation data

boolean, default False

Include visualization of speaker related animation data

boolean, default False

Display an additional ‘summary’ line (Dope Sheet editors only)

boolean, default False

Include visualization of texture related animation data

boolean, default False

Include visualization of object-level animation data (mostly transforms)

boolean, default False

Include visualization of volume related animation data

boolean, default False

Include visualization of world related animation data

boolean, default False

ID-Block representing source data, usually ID_SCE (i.e. Scene)

Alphabetically sorts data-blocks - mainly objects in the scene (disable to increase viewport speed)

boolean, default False

boolean, default False

Perform fuzzy/multi-word matching. Warning: May be slow

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

SpaceDopeSheetEditor.dopesheet

SpaceGraphEditor.dopesheet

---

## Driver(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Driver.html

**Contents:**
- Driver(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Driver for the value of a setting based on an external value

Expression to use for Scripted Expression

string, default “”, (never None)

The scripted expression can be evaluated without using the full Python interpreter

boolean, default False, (readonly)

Driver could not be evaluated in past, so should be skipped

boolean, default False

enum in ['AVERAGE', 'SUM', 'SCRIPTED', 'MIN', 'MAX'], default 'AVERAGE'

Include a ‘self’ variable in the name-space, so drivers can easily reference the data being modified (object, bone, etc…)

boolean, default False

Properties acting as inputs for this driver

ChannelDriverVariables bpy_prop_collection of DriverVariable, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## DriverTarget(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DriverTarget.html

**Contents:**
- DriverTarget(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Source of input values for driver variables

Name of PoseBone to use as target

string, default “”, (never None)

Type of a context-dependent data-block to access property from

ACTIVE_SCENE Active Scene – Currently evaluating scene.

ACTIVE_VIEW_LAYER Active View Layer – Currently evaluating view layer.

enum in ['ACTIVE_SCENE', 'ACTIVE_VIEW_LAYER'], default 'ACTIVE_SCENE'

RNA Path (from ID-block) to property used

string, default “”, (never None)

The value to use if the data path cannot be resolved

float in [-inf, inf], default 0.0

ID-block that the specific property used can be found from (id_type property must be set first)

Type of ID-block that can be used

enum in Id Type Items, default 'OBJECT'

Indicates that the most recent variable evaluation used the fallback value

boolean, default False, (readonly)

Mode for calculating rotation channel values

enum in Driver Target Rotation Mode Items, default 'AUTO'

Space in which transforms are used

WORLD_SPACE World Space – Transforms include effects of parenting/restpose and constraints.

TRANSFORM_SPACE Transform Space – Transforms don’t include parenting/restpose or constraints.

LOCAL_SPACE Local Space – Transforms include effects of constraints but not parenting/restpose.

enum in ['WORLD_SPACE', 'TRANSFORM_SPACE', 'LOCAL_SPACE'], default 'WORLD_SPACE'

enum in ['LOC_X', 'LOC_Y', 'LOC_Z', 'ROT_X', 'ROT_Y', 'ROT_Z', 'ROT_W', 'SCALE_X', 'SCALE_Y', 'SCALE_Z', 'SCALE_AVG'], default 'LOC_X'

Use the fallback value if the data path cannot be resolved, instead of failing to evaluate the driver

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

DriverVariable.targets

---

## DriverVariable(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DriverVariable.html

**Contents:**
- DriverVariable(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Variable from some source/target for driver relationship

Is this a valid name for a driver variable

boolean, default False, (readonly)

Name to use in scripted expressions/functions (no spaces or dots are allowed, and must start with a letter)

string, default “”, (never None)

Sources of input data for evaluating this variable

bpy_prop_collection of DriverTarget, (readonly)

SINGLE_PROP Single Property – Use the value from some RNA property.

TRANSFORMS Transform Channel – Final transformation value of object or bone.

ROTATION_DIFF Rotational Difference – Use the angle between two bones.

LOC_DIFF Distance – Distance between two bones or objects.

CONTEXT_PROP Context Property – Use the value from some RNA property within the current evaluation context.

enum in ['SINGLE_PROP', 'TRANSFORMS', 'ROTATION_DIFF', 'LOC_DIFF', 'CONTEXT_PROP'], default 'SINGLE_PROP'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ChannelDriverVariables.new

ChannelDriverVariables.remove

---

## DynamicPaintBrushSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DynamicPaintBrushSettings.html

**Contents:**
- DynamicPaintBrushSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Proximity falloff is applied inside the volume

boolean, default False

float in [0, 1], default 0.0

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

Maximum distance from brush to mesh surface to affect paint

float in [0, 500], default 0.0

Color ramp used to define proximity falloff

ColorRamp, (readonly)

enum in ['PARTICLE_SYSTEM', 'POINT', 'DISTANCE', 'VOLUME_DISTANCE', 'VOLUME'], default 'VOLUME'

Paint wetness, visible in wetmap (some effects only affect wet paint)

float in [0, 1], default 0.0

The particle system to paint with

Proximity falloff type

enum in ['SMOOTH', 'CONSTANT', 'RAMP'], default 'CONSTANT'

Ray direction to use for projection (if brush object is located in that direction it’s painted)

enum in ['CANVAS', 'BRUSH', 'Z_AXIS'], default 'CANVAS'

Smooth falloff added after solid radius

float in [0, 10], default 0.0

Smudge effect strength

float in [0, 1], default 0.0

Radius that will be painted solid

float in [0.01, 10], default 0.0

Only increase alpha value if paint alpha is higher than existing

boolean, default False

Negate influence inside the volume

boolean, default False

Erase / remove paint instead of adding it

boolean, default False

Use radius from particle settings

boolean, default False

Brush is projected to canvas from defined direction within brush proximity

boolean, default False

Only read color ramp alpha

boolean, default False

Make this brush to smudge existing paint as it moves

boolean, default False

Multiply brush influence by velocity color ramp alpha

boolean, default False

Replace brush color by velocity color ramp

boolean, default False

Multiply brush intersection depth (displace, waves) by velocity ramp alpha

boolean, default False

Velocity considered as maximum influence (Blender units per frame)

float in [0.0001, 10], default 0.0

Color ramp used to define brush velocity effect

ColorRamp, (readonly)

Maximum level of surface intersection used to influence waves (use 0.0 to disable)

float in [0, 50], default 0.0

Multiplier for wave influence of this brush

float in [-2, 2], default 0.0

enum in ['CHANGE', 'DEPTH', 'FORCE', 'REFLECT'], default 'DEPTH'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

DynamicPaintModifier.brush_settings

---

## DynamicPaintCanvasSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DynamicPaintCanvasSettings.html

**Contents:**
- DynamicPaintCanvasSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Dynamic Paint canvas settings

DynamicPaintSurfaces bpy_prop_collection of DynamicPaintSurface, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

DynamicPaintModifier.canvas_settings

---

## DynamicPaintModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DynamicPaintModifier.html

**Contents:**
- DynamicPaintModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Dynamic Paint modifier

DynamicPaintBrushSettings, (readonly)

DynamicPaintCanvasSettings, (readonly)

enum in Prop Dynamicpaint Type Items, default 'CANVAS'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## DynamicPaintSurfaces(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DynamicPaintSurfaces.html

**Contents:**
- DynamicPaintSurfaces(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of Dynamic Paint Canvas surfaces

Active Dynamic Paint surface being displayed

DynamicPaintSurface, (readonly)

int in [0, inf], default 0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

DynamicPaintCanvasSettings.canvas_surfaces

---

## DynamicPaintSurface(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.DynamicPaintSurface.html

**Contents:**
- DynamicPaintSurface(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

A canvas surface layer

Only use brush objects from this collection

Adjust influence brush objects have on this surface

float in [0, 1], default 0.0

Adjust radius of proximity brushes or particles for this surface

float in [0, 10], default 0.0

The wetness level when colors start to shift to the background

float in [0, 1], default 0.0

How fast colors get mixed within wet paint

float in [0, 2], default 0.0

Maximum level of depth intersection in object space (use 0.0 to disable)

float in [0, 50], default 0.0

Strength of displace when applied to the mesh

float in [-50, 50], default 0.0

enum in ['DISPLACE', 'DEPTH'], default 'DISPLACE'

Approximately in how many frames should dissolve happen

int in [1, 10000], default 0

How much surface acceleration affects dripping

float in [-200, 200], default 0.0

How much surface velocity affects dripping

float in [-200, 200], default 0.0

Approximately in how many frames should drying happen

int in [1, 10000], default 0

enum in ['SPREAD', 'DRIP', 'SHRINK'], default 'SPREAD'

EffectorWeights, (readonly)

int in [1, 1048574], default 0

Simulation start frame

int in [1, 1048574], default 0

Do extra frames between scene frames to ensure smooth motion

int in [0, 20], default 0

enum in ['PNG', 'OPENEXR'], default 'PNG'

Directory to save the textures

string, default “”, (never None, blend relative // prefix supported)

Output image resolution

int in [16, 4096], default 0

Initial color of the surface

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0)

enum in ['NONE', 'COLOR', 'TEXTURE', 'VERTEX_COLOR'], default 'NONE'

string, default “”, (never None)

Toggle whether surface is processed or ignored

boolean, default False

boolean, default False, (readonly)

string, default “”, (never None)

Name used to save output from this surface

string, default “”, (never None)

Name used to save output from this surface

string, default “”, (never None)

PointCache, (readonly, never None)

How fast shrink effect moves on the canvas surface

float in [0.001, 10], default 0.0

How fast spread effect moves on the canvas surface

float in [0.001, 10], default 0.0

enum in ['VERTEX', 'IMAGE'], default 'VERTEX'

enum in ['PAINT'], default 'PAINT'

Use 5× multisampling to smooth paint edges

boolean, default False

Enable to make surface changes disappear over time

boolean, default False

Use logarithmic dissolve (makes high values to fade faster than low values)

boolean, default False

Process drip effect (drip wet paint to gravity direction)

boolean, default False

Use logarithmic drying (makes high values to dry faster than low values)

boolean, default False

Enable to make surface wetness dry over time

boolean, default False

New displace is added cumulatively on top of existing

boolean, default False

Save this output layer

boolean, default False

Save this output layer

boolean, default False

Multiply color by alpha (recommended for Blender input)

boolean, default False

Process shrink effect (shrink paint areas)

boolean, default False

Process spread effect (spread wet paint around surface)

boolean, default False

Pass waves through mesh edges

boolean, default False

string, default “”, (never None)

float in [0, 1], default 0.0

Limit maximum steepness of wave slope between simulation points (use higher values for smoother waves at expense of reduced detail)

float in [0, 10], default 0.0

Wave propagation speed

float in [0.01, 5], default 0.0

Spring force that pulls water level back to zero

float in [0, 1], default 0.0

Wave time scaling factor

float in [0.01, 3], default 0.0

Checks if surface output layer of given name exists

index (int in [0, 1]) – Index

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

DynamicPaintCanvasSettings.canvas_surfaces

DynamicPaintSurfaces.active

---

## EQCurveMappingData(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EQCurveMappingData.html

**Contents:**
- EQCurveMappingData(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

CurveMapping, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

SoundEqualizerModifier.graphics

SoundEqualizerModifier.new_graphic

---

## EdgeSplitModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EdgeSplitModifier.html

**Contents:**
- EdgeSplitModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Edge splitting modifier to create sharp edges

Angle above which to split edges

float in [0, 3.14159], default 0.523599

Split edges with high angle between faces

boolean, default True

Split edges that are marked as sharp

boolean, default True

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## EditBone(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EditBone.html

**Contents:**
- EditBone(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Edit mode bone in an armature data-block

X-axis handle offset for start of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Z-axis handle offset for start of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

X-axis handle offset for end of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Z-axis handle offset for end of the B-Bone’s curve, adjusts curvature

float in [-inf, inf], default 0.0

Bone that serves as the end handle for the B-Bone curve

Bone that serves as the start handle for the B-Bone curve

Length of first Bézier Handle (for B-Bones only)

float in [-inf, inf], default 1.0

Length of second Bézier Handle (for B-Bones only)

float in [-inf, inf], default 1.0

Selects how the end handle of the B-Bone is computed

AUTO Automatic – Use connected parent and children to compute the handle.

ABSOLUTE Absolute – Use the position of the specified bone to compute the handle.

RELATIVE Relative – Use the offset of the specified bone from rest pose to compute the handle.

TANGENT Tangent – Use the orientation of the specified bone to compute the handle, ignoring the location.

enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'TANGENT'], default 'AUTO'

Selects how the start handle of the B-Bone is computed

AUTO Automatic – Use connected parent and children to compute the handle.

ABSOLUTE Absolute – Use the position of the specified bone to compute the handle.

RELATIVE Relative – Use the offset of the specified bone from rest pose to compute the handle.

TANGENT Tangent – Use the orientation of the specified bone to compute the handle, ignoring the location.

enum in ['AUTO', 'ABSOLUTE', 'RELATIVE', 'TANGENT'], default 'AUTO'

Multiply the B-Bone Ease Out channel by the local Y scale value of the end handle. This is done after the Scale Easing option and isn’t affected by it.

boolean, default False

Multiply the B-Bone Ease In channel by the local Y scale value of the start handle. This is done after the Scale Easing option and isn’t affected by it.

boolean, default False

Multiply B-Bone Scale Out channels by the local scale values of the end handle. This is done after the Scale Easing option and isn’t affected by it.

boolean array of 3 items, default (False, False, False)

Multiply B-Bone Scale In channels by the local scale values of the start handle. This is done after the Scale Easing option and isn’t affected by it.

boolean array of 3 items, default (False, False, False)

Selects how the vertices are mapped to B-Bone segments based on their position

STRAIGHT Straight – Fast mapping that is good for most situations, but ignores the rest pose curvature of the B-Bone.

CURVED Curved – Slower mapping that gives better deformation for B-Bones that are sharply curved in rest pose.

enum in ['STRAIGHT', 'CURVED'], default 'STRAIGHT'

Roll offset for the start of the B-Bone, adjusts twist

float in [-inf, inf], default 0.0

Roll offset for the end of the B-Bone, adjusts twist

float in [-inf, inf], default 0.0

Scale factors for the start of the B-Bone, adjusts thickness (for tapering effects)

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

Scale factors for the end of the B-Bone, adjusts thickness (for tapering effects)

mathutils.Vector of 3 items in [-inf, inf], default (1.0, 1.0, 1.0)

Number of subdivisions of bone (for B-Bones only)

int in [1, 32], default 0

float in [-inf, inf], default 0.0

float in [-inf, inf], default 0.0

Bone Collections that contain this bone

bpy_prop_collection of BoneCollection, (readonly)

BoneColor, (readonly)

ARMATURE_DEFINED Armature Defined – Use display mode from armature (default).

OCTAHEDRAL Octahedral – Display bones as octahedral shape.

STICK Stick – Display bones as simple 2D lines with dots.

BBONE B-Bone – Display bones as boxes, showing subdivision and B-Splines.

ENVELOPE Envelope – Display bones as extruded spheres, showing deformation influence volume.

WIRE Wire – Display bones as thin wires, showing subdivision and B-Splines.

enum in ['ARMATURE_DEFINED', 'OCTAHEDRAL', 'STICK', 'BBONE', 'ENVELOPE', 'WIRE'], default 'OCTAHEDRAL'

Bone deformation distance (for Envelope deform only)

float in [0, 1000], default 0.0

Bone deformation weight (for Envelope deform only)

float in [0, 1000], default 0.0

Location of head end of the bone

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

Radius of head of bone (for Envelope deform only)

float in [-inf, inf], default 0.0

Bone is not visible when in Edit Mode

boolean, default False

Bone is able to be selected

boolean, default False

Specifies how the bone inherits scaling from the parent bone

FULL Full – Inherit all effects of parent scaling.

FIX_SHEAR Fix Shear – Inherit scaling, but remove shearing of the child in the rest orientation.

ALIGNED Aligned – Rotate non-uniform parent scaling to align with the child, applying parent X scale to child X axis, and so forth.

AVERAGE Average – Inherit uniform scaling representing the overall change in the volume of the parent.

NONE None – Completely ignore parent scaling.

NONE_LEGACY None (Legacy) – Ignore parent scaling without compensating for parent shear. Replicates the effect of disabling the original Inherit Scale checkbox..

enum in ['FULL', 'FIX_SHEAR', 'ALIGNED', 'AVERAGE', 'NONE', 'NONE_LEGACY'], default 'FULL'

Length of the bone. Changing moves the tail end.

float in [0, inf], default 0.0

Bone is not able to be transformed when in Edit Mode

boolean, default False

Matrix combining location and rotation of the bone (head position, direction and roll), in armature space (does not include/support bone’s length/size)

mathutils.Matrix of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))

string, default “”, (never None)

Parent edit bone (in same Armature)

Bone rotation around head-tail axis

float in [-inf, inf], default 0.0

boolean, default False

boolean, default False

boolean, default False

Bone is always displayed in wireframe regardless of viewport shading mode (useful for non-obstructive custom bone shapes)

boolean, default False

Location of tail end of the bone

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

Radius of tail of bone (for Envelope deform only)

float in [-inf, inf], default 0.0

When bone has a parent, bone’s head is stuck to the parent’s tail

boolean, default False

When bone does not have a parent, it receives cyclic offset effects (Deprecated)

boolean, default False

Enable Bone to deform geometry

boolean, default False

Add Roll Out of the Start Handle bone to the Roll In value

boolean, default False

When deforming bone, multiply effects of Vertex Group weights with Envelope influence

boolean, default False

Bone inherits rotation or scale from parent bone

boolean, default False

Bone location is set in local space

boolean, default False

Object children will use relative transform, like deform

boolean, default False

Multiply the final easing values by the Scale In/Out Y factors

boolean, default False

The name of this bone before any . character.

The midpoint between the head and the tail.

A list of all the bones children.

Takes O(len(bones)) time.

A list of all children from this bone.

Takes O(len(bones)**2) time.

Returns a chain of children with the same base name as this bone. Only direct chains are supported, forks caused by multiple children with matching base names will terminate the function and not be returned.

Takes O(len(bones)**2) time.

A list of parents, starting with the immediate parent.

The direction this bone is pointing. Utility function for (tail - head)

Vector pointing down the x-axis of the bone.

Vector pointing down the y-axis of the bone.

Vector pointing down the z-axis of the bone.

DEBUG ONLY. Internal access to runtime-defined RNA data storage, intended solely for testing and debugging purposes. Do not access it in regular scripting work, and in particular, do not assume that it contains writable data

do_create (boolean, (optional)) – Ensure that system properties are created if they do not exist yet

The system properties root container, or None if there are no system properties stored in this data yet, and its creation was not requested

Align the bone to a local-space roll so the Z axis points in the direction of the vector given

vector (mathutils.Vector of 3 items in [-inf, inf]) – Vector

Align this bone to another by moving its tail and settings its roll the length of the other bone is not used.

The same as ‘bone in other_bone.parent_recursive’ but saved generating a list.

Transform the bones head, tail, roll and envelope (when the matrix has a scale component).

matrix (mathutils.Matrix) – 3x3 or 4x4 transformation matrix.

scale (bool) – Scale the bone envelope by the matrix.

roll (bool) – Correct the roll to point in the same relative direction to the head and tail.

Utility function to add vec to the head and tail of this bone.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

bpy.context.active_bone

bpy.context.edit_bone

bpy.context.editable_bones

bpy.context.selected_bones

bpy.context.selected_editable_bones

bpy.context.visible_bones

ArmatureEditBones.active

ArmatureEditBones.new

ArmatureEditBones.remove

EditBone.bbone_custom_handle_end

EditBone.bbone_custom_handle_start

---

## EffectStrip(Strip)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EffectStrip.html

**Contents:**
- EffectStrip(Strip)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Strip

subclasses — AddStrip, AdjustmentStrip, AlphaOverStrip, AlphaUnderStrip, ColorMixStrip, ColorStrip, CrossStrip, GammaCrossStrip, GaussianBlurStrip, GlowStrip, MulticamStrip, MultiplyStrip, SpeedControlStrip, SubtractStrip, TextStrip, WipeStrip

Sequence strip applying an effect on the images created by other strips

Representation of alpha information in the RGBA pixels

STRAIGHT Straight – RGB channels in transparent pixels are unaffected by the alpha channel.

PREMUL Premultiplied – RGB channels in transparent pixels are multiplied by the alpha channel.

enum in ['STRAIGHT', 'PREMUL'], default 'STRAIGHT'

float in [0, 20], default 1.0

Adjust the intensity of the input’s color

float in [0, 20], default 1.0

StripCrop, (readonly)

Multiply alpha along with color channels

boolean, default False

StripProxy, (readonly)

Only display every nth frame

float in [1, 30], default 0.0

StripTransform, (readonly)

Remove fields from video movies

boolean, default False

boolean, default False

boolean, default False

Convert input to float data

boolean, default False

Use a preview proxy and/or time-code index for this strip

boolean, default False

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Strip.select_left_handle

Strip.select_right_handle

Strip.frame_final_duration

Strip.frame_final_start

Strip.frame_final_end

Strip.frame_offset_start

Strip.frame_offset_end

Strip.use_linear_modifiers

Strip.use_default_fade

Strip.show_retiming_keys

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Strip.bl_system_properties_get

Strip.strip_elem_from_frame

Strip.invalidate_cache

Strip.bl_rna_get_subclass

Strip.bl_rna_get_subclass_py

---

## EffectorWeights(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EffectorWeights.html

**Contents:**
- EffectorWeights(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Effector weights for physics simulation

All effector’s weight

float in [-200, 200], default 0.0

Use force fields when growing hair

boolean, default False

float in [-200, 200], default 0.0

Charge effector weight

float in [-200, 200], default 0.0

Limit effectors to this collection

Curve guide effector weight

float in [-200, 200], default 0.0

float in [-200, 200], default 0.0

Force effector weight

float in [-200, 200], default 0.0

Global gravity weight

float in [-200, 200], default 0.0

Harmonic effector weight

float in [-200, 200], default 0.0

Lennard-Jones effector weight

float in [-200, 200], default 0.0

Magnetic effector weight

float in [-200, 200], default 0.0

Fluid Flow effector weight

float in [-200, 200], default 0.0

Texture effector weight

float in [-200, 200], default 0.0

Turbulence effector weight

float in [-200, 200], default 0.0

Vortex effector weight

float in [-200, 200], default 0.0

float in [-200, 200], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ClothSettings.effector_weights

DynamicPaintSurface.effector_weights

FluidDomainSettings.effector_weights

ParticleSettings.effector_weights

RigidBodyWorld.effector_weights

SoftBodySettings.effector_weights

---

## EnumProperty(Property)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EnumProperty.html

**Contents:**
- EnumProperty(Property)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Property

RNA enumeration property definition, to choose from a number of predefined options

Default value for this enum

enum in ['DEFAULT'], default 'DEFAULT', (readonly)

Default value for this enum

enum set in {'DEFAULT'}, default set(), (readonly)

Possible values for the property

bpy_prop_collection of EnumPropertyItem, (readonly)

Possible values for the property (never calls optional dynamic generation of those)

bpy_prop_collection of EnumPropertyItem, (readonly)

Possible values for the property (never calls optional dynamic generation of those). Includes UI elements (separators and section headings).

bpy_prop_collection of EnumPropertyItem, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Property.translation_context

Property.is_animatable

Property.is_overridable

Property.is_argument_optional

Property.is_never_none

Property.is_skip_save

Property.is_skip_preset

Property.is_registered

Property.is_registered_optional

Property.is_enum_flag

Property.is_library_editable

Property.is_path_output

Property.is_path_supports_blend_relative

Property.is_path_supports_templates

Property.is_deprecated

Property.deprecated_note

Property.deprecated_version

Property.deprecated_removal_version

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Property.bl_rna_get_subclass

Property.bl_rna_get_subclass_py

---

## Event(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Event.html

**Contents:**
- Event(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

True when the Alt/Option key is held

boolean, default False, (readonly)

Single ASCII character for this event

string, default “”, (readonly, never None)

True when the Ctrl key is held

boolean, default False, (readonly)

The direction (only applies to drag events)

enum in Event Direction Items, default 'ANY', (readonly)

True when the Hyper key is held

boolean, default False, (readonly)

Part of a trackpad or NDOF motion, interrupted by cursor motion, button or key press events

boolean, default False, (readonly)

The last motion event was an absolute input

boolean, default False, (readonly)

The event is generated by holding a key down

boolean, default False, (readonly)

The event has tablet data

boolean, default False, (readonly)

The window relative horizontal location of the last press event

int in [-inf, inf], default 0, (readonly)

The window relative vertical location of the last press event

int in [-inf, inf], default 0, (readonly)

The window relative horizontal location of the mouse

int in [-inf, inf], default 0, (readonly)

The window relative vertical location of the mouse

int in [-inf, inf], default 0, (readonly)

The region relative horizontal location of the mouse

int in [-inf, inf], default 0, (readonly)

The region relative vertical location of the mouse

int in [-inf, inf], default 0, (readonly)

The window relative horizontal location of the mouse

int in [-inf, inf], default 0, (readonly)

The window relative vertical location of the mouse

int in [-inf, inf], default 0, (readonly)

NDOF motion event data

NDOFMotionEventData, (readonly)

True when the Cmd key is held

boolean, default False, (readonly)

The pressure of the tablet or 1.0 if no tablet present

float in [0, 1], default 1.0, (readonly)

True when the Shift key is held

boolean, default False, (readonly)

The pressure of the tablet or zeroes if no tablet present

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0), (readonly)

enum in Event Type Items, default 'NONE', (readonly)

enum in Event Type Items, default 'NONE', (readonly)

Single unicode character for this event

string, default “”, (readonly, never None)

The type of event, only applies to some

enum in Event Value Items, default 'NOTHING', (readonly)

The type of event, only applies to some

enum in Event Value Items, default 'NOTHING', (readonly)

XrEventData, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

KeyMapItems.match_event

Window.event_simulate

WindowManager.invoke_confirm

WindowManager.invoke_props_popup

WindowManager.piemenu_begin__internal

---

## EvaluateClosureNodeViewerPathElem(ViewerPathElem)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EvaluateClosureNodeViewerPathElem.html

**Contents:**
- EvaluateClosureNodeViewerPathElem(ViewerPathElem)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ViewerPathElem

int in [-inf, inf], default 0

int in [-inf, inf], default 0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ViewerPathElem.ui_name

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ViewerPathElem.bl_rna_get_subclass

ViewerPathElem.bl_rna_get_subclass_py

---

## EnumPropertyItem(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.EnumPropertyItem.html

**Contents:**
- EnumPropertyItem(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Definition of a choice in an RNA enum property

Description of the item’s purpose

string, default “”, (readonly, never None)

enum in Icon Items, default 'NONE', (readonly)

Unique name used in the code and scripting

string, default “”, (readonly, never None)

string, default “”, (readonly, never None)

int in [0, inf], default 0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

EnumProperty.enum_items

EnumProperty.enum_items_static

EnumProperty.enum_items_static_ui

KeyMap.modal_event_values

---

## ExplodeModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ExplodeModifier.html

**Contents:**
- ExplodeModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Explosion effect modifier based on a particle system

Invert vertex group influence

boolean, default False

UV map to change with particle age

string, default “”, (never None)

Clean vertex group edges

float in [0, 1], default 0.0

Show mesh when particles are alive

boolean, default True

Show mesh when particles are dead

boolean, default True

Show mesh when particles are unborn

boolean, default True

Cut face edges for nicer shrapnel

boolean, default False

Use particle size for the shrapnel

boolean, default False

string, default “”, (never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## FCurve(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FCurve.html

**Contents:**
- FCurve(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

F-Curve defining values of a period of time

Index to the specific property affected by F-Curve if applicable

int in [0, inf], default 0

Algorithm used to compute automatic handles

enum in Fcurve Auto Smoothing Items, default 'NONE'

Color of the F-Curve in the Graph Editor

mathutils.Color of 3 items in [0, 1], default (0.0, 0.0, 0.0)

Method used to determine color of F-Curve in Graph Editor

AUTO_RAINBOW Auto Rainbow – Cycle through the rainbow, trying to give each curve a unique color.

AUTO_RGB Auto XYZ to RGB – Use axis colors for transform and color properties, and auto-rainbow for the rest.

AUTO_YRGB Auto WXYZ to YRGB – Use WXYZ axis colors for quaternion/axis-angle rotations, XYZ axis colors for other transform and color properties, and auto-rainbow for the rest.

CUSTOM User Defined – Use custom hand-picked color for F-Curve.

enum in ['AUTO_RAINBOW', 'AUTO_RGB', 'AUTO_YRGB', 'CUSTOM'], default 'AUTO_RAINBOW'

RNA Path to property affected by F-Curve

string, default “”, (never None)

Channel Driver (only set for Driver F-Curves)

Method used for evaluating value of F-Curve outside first and last keyframes

CONSTANT Constant – Hold values of endpoint keyframes.

LINEAR Linear – Use slope of curve leading in/out of endpoint keyframes.

enum in ['CONSTANT', 'LINEAR'], default 'CONSTANT'

Action Group that this F-Curve belongs to

F-Curve and its keyframes are hidden in the Graph Editor graphs

boolean, default False

True if the curve contributes no animation due to lack of keyframes or useful modifiers, and should be deleted

boolean, default False, (readonly)

False when F-Curve could not be evaluated in past, so should be skipped when evaluating

boolean, default False

User-editable keyframes

FCurveKeyframePoints bpy_prop_collection of Keyframe, (readonly)

F-Curve’s settings cannot be edited

boolean, default False

Modifiers affecting the shape of the F-Curve

FCurveModifiers bpy_prop_collection of FModifier, (readonly)

Disable F-Curve evaluation

boolean, default False

Sampled animation data

bpy_prop_collection of FCurveSample, (readonly)

F-Curve is selected for editing

boolean, default False

frame (float in [-inf, inf]) – Frame, Evaluate F-Curve at given frame

Value, Value of F-Curve specific frame

Ensure keyframes are sorted in chronological order and handles are set correctly

Get the time extents for F-Curve

Range, Min/Max values

mathutils.Vector of 2 items in [-inf, inf]

Update FCurve flags set automatically from affected property (currently, integer/discrete flags set when the property is not a float)

data (AnyType, (never None)) – Data, Data containing the property controlled by given FCurve

Convert current FCurve from keyframes to sample points, if necessary

start (int in [-1048574, 1048574]) – Start Frame

end (int in [-1048574, 1048574]) – End Frame

Convert current FCurve from sample points to keyframes (linear interpolation), if necessary

start (int in [-1048574, 1048574]) – Start Frame

end (int in [-1048574, 1048574]) – End Frame

Place keys at even intervals on the existing curve.

start (int in [-1048574, 1048574]) – Start Frame, Frame at which to start baking

end (int in [-1048574, 1048574]) – End Frame, Frame at which to end baking (inclusive)

step (float in [0.01, inf], (optional)) – Step, At which interval to add keys

remove (enum in ['NONE', 'IN_RANGE', 'OUT_RANGE', 'ALL'], (optional)) – Remove Options, Choose which keys should be automatically removed by the bake NONE None – Keep all keys. IN_RANGE In Range – Remove all keys within the defined range. OUT_RANGE Outside Range – Remove all keys outside the defined range. ALL All – Remove all existing keys.

Remove Options, Choose which keys should be automatically removed by the bake

NONE None – Keep all keys.

IN_RANGE In Range – Remove all keys within the defined range.

OUT_RANGE Outside Range – Remove all keys outside the defined range.

ALL All – Remove all existing keys.

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

bpy.context.active_editable_fcurve

bpy.context.editable_fcurves

bpy.context.selected_editable_fcurves

bpy.context.selected_visible_fcurves

bpy.context.visible_fcurves

Action.fcurve_ensure_for_datablock

ActionChannelbag.fcurves

ActionChannelbagFCurves.ensure

ActionChannelbagFCurves.find

ActionChannelbagFCurves.new

ActionChannelbagFCurves.new_from_fcurve

ActionChannelbagFCurves.new_from_fcurve

ActionChannelbagFCurves.remove

AnimDataDrivers.from_existing

AnimDataDrivers.from_existing

AnimDataDrivers.remove

---

## FCurveKeyframePoints(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FCurveKeyframePoints.html

**Contents:**
- FCurveKeyframePoints(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of keyframe points

Add a keyframe point to a F-Curve

frame (float in [-inf, inf]) – X Value of this keyframe point

value (float in [-inf, inf]) – Y Value of this keyframe point

options (enum set in {'REPLACE', 'NEEDED', 'FAST'}, (optional)) – Keyframe options REPLACE Replace – Don’t add any new keyframes, but just replace existing ones. NEEDED Needed – Only adds keyframes that are needed. FAST Fast – Fast keyframe insertion to avoid recalculating the curve each time.

REPLACE Replace – Don’t add any new keyframes, but just replace existing ones.

NEEDED Needed – Only adds keyframes that are needed.

FAST Fast – Fast keyframe insertion to avoid recalculating the curve each time.

keyframe_type (enum in Beztriple Keyframe Type Items, (optional)) – Type of keyframe to insert

Newly created keyframe

Add a keyframe point to a F-Curve

count (int in [0, inf]) – Number, Number of points to add to the spline

Remove keyframe from an F-Curve

keyframe (Keyframe, (never None)) – Keyframe to remove

fast (boolean, (optional)) – Fast, Fast keyframe removal to avoid recalculating the curve each time

Remove all keyframes from an F-Curve

Ensure all keyframe points are chronologically sorted

Ensure there are no duplicate keys. Assumes that the points have already been sorted

Update handles after modifications to the keyframe points, to update things like auto-clamping

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FCurve.keyframe_points

---

## FCurveModifiers(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FCurveModifiers.html

**Contents:**
- FCurveModifiers(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Collection of F-Curve Modifiers

Active F-Curve Modifier

Add a constraint to this object

type (enum in Fmodifier Type Items) – Constraint type to add

Remove a modifier from this F-Curve

modifier (FModifier, (never None)) – Removed modifier

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## FCurveSample(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FCurveSample.html

**Contents:**
- FCurveSample(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Sample point for F-Curve

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FCurve.sampled_points

---

## FILEBROWSER_UL_dir(UIList)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FILEBROWSER_UL_dir.html

**Contents:**
- FILEBROWSER_UL_dir(UIList)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, UIList

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

UIList.use_filter_show

UIList.use_filter_invert

UIList.use_filter_sort_alpha

UIList.use_filter_sort_reverse

UIList.use_filter_sort_lock

UIList.bitflag_filter_item

UIList.bitflag_item_never_show

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

UIList.bl_system_properties_get

UIList.bl_rna_get_subclass

UIList.bl_rna_get_subclass_py

---

## FFmpegSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FFmpegSettings.html

**Contents:**
- FFmpegSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

FFmpeg related settings for the scene

int in [32, 384], default 192

MONO Mono – Set audio channels to mono.

STEREO Stereo – Set audio channels to stereo.

SURROUND4 4 Channels – Set audio channels to 4 channels.

SURROUND51 5.1 Surround – Set audio channels to 5.1 surround sound.

SURROUND71 7.1 Surround – Set audio channels to 7.1 surround sound.

enum in ['MONO', 'STEREO', 'SURROUND4', 'SURROUND51', 'SURROUND71'], default 'STEREO'

FFmpeg audio codec to use

NONE No Audio – Disables audio output, for video-only renders.

enum in ['NONE', 'AAC', 'AC3', 'FLAC', 'MP2', 'MP3', 'OPUS', 'PCM', 'VORBIS'], default 'NONE'

Audio sample rate (samples/s)

int in [8000, 192000], default 48000

float in [0, 1], default 1.0

Rate control: buffer size (kb)

int in [0, 2000], default 0

FFmpeg codec to use for video output

NONE No Video – Disables video output, for audio-only renders.

FFV1 FFmpeg video codec #1.

QTRLE QuickTime Animation.

enum in ['NONE', 'AV1', 'H264', 'H265', 'WEBM', 'DNXHD', 'DV', 'FFV1', 'FLASH', 'HUFFYUV', 'MPEG1', 'MPEG2', 'MPEG4', 'PNG', 'PRORES', 'QTRLE', 'THEORA'], default 'H264'

Constant Rate Factor (CRF); tradeoff between video quality and file size

NONE Constant Bitrate – Configure constant bit rate, rather than constant output quality.

PERC_LOSSLESS Perceptually Lossless.

MEDIUM Medium Quality.

VERYLOW Very Low Quality.

LOWEST Lowest Quality.

enum in ['NONE', 'LOSSLESS', 'PERC_LOSSLESS', 'HIGH', 'MEDIUM', 'LOW', 'VERYLOW', 'LOWEST'], default 'MEDIUM'

Tradeoff between encoding speed and compression ratio

BEST Slowest – Recommended if you have lots of time and want the best compression efficiency.

GOOD Good – The default and recommended for most applications.

REALTIME Realtime – Recommended for fast encoding.

enum in ['BEST', 'GOOD', 'REALTIME'], default 'GOOD'

enum in ['422_PROXY', '422_LT', '422_STD', '422_HQ', '4444', '4444_XQ'], default '422_STD'

Output file container

enum in ['MPEG4', 'MKV', 'WEBM', 'AVI', 'DV', 'FLASH', 'MPEG1', 'MPEG2', 'OGG', 'QUICKTIME'], default 'MKV'

Distance between key frames, also known as GOP size; influences file size and seekability

int in [0, 500], default 25

Maximum number of B-frames between non-B-frames; influences file size and seekability

int in [0, 16], default 0

Rate control: max rate (kbit/s)

int in [-inf, inf], default 0

Rate control: min rate (kbit/s)

int in [-inf, inf], default 0

Mux rate (bits/second)

int in [0, inf], default 0

Mux packet size (byte)

int in [0, 16384], default 0

Autosplit output at 2GB boundary

boolean, default False

Use lossless output for video streams

boolean, default False

Set a maximum number of B-frames

boolean, default False

Video bitrate (kbit/s)

int in [-inf, inf], default 0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

RenderSettings.ffmpeg

---

## FModifier(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifier.html

**Contents:**
- FModifier(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

subclasses — FModifierCycles, FModifierEnvelope, FModifierFunctionGenerator, FModifierGenerator, FModifierLimits, FModifierNoise, FModifierStepped

Modifier for values of F-Curve

F-Curve modifier will show settings in the editor

boolean, default False

Number of frames from start frame for influence to take effect

float in [-inf, inf], default 0.0

Number of frames from end frame for influence to fade out

float in [-inf, inf], default 0.0

Frame that modifier’s influence ends (if Restrict Frame Range is in use)

float in [-inf, inf], default 0.0

Frame that modifier’s influence starts (if Restrict Frame Range is in use)

float in [-inf, inf], default 0.0

Amount of influence F-Curve Modifier will have when not fading in/out

float in [0, 1], default 1.0

F-Curve Modifier has invalid settings and will not be evaluated

boolean, default False, (readonly)

Enable F-Curve modifier evaluation

boolean, default False

F-Curve Modifier name

string, default “”, (never None)

F-Curve Modifier’s panel is expanded in UI

boolean, default False

F-Curve Modifier Type

enum in Fmodifier Type Items, default 'NULL', (readonly)

F-Curve Modifier’s effects will be tempered by a default factor

boolean, default False

F-Curve Modifier is only applied for the specified frame range to help mask off effects in order to chain them

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FCurveModifiers.active

FCurveModifiers.remove

---

## FModifierCycles(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierCycles.html

**Contents:**
- FModifierCycles(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Repeat the values of the modified F-Curve

Maximum number of cycles to allow after last keyframe (0 = infinite)

int in [-32768, 32767], default 0

Maximum number of cycles to allow before first keyframe (0 = infinite)

int in [-32768, 32767], default 0

Cycling mode to use after last keyframe

NONE No Cycles – Don’t do anything.

REPEAT Repeat Motion – Repeat keyframe range as-is.

REPEAT_OFFSET Repeat with Offset – Repeat keyframe range, but with offset based on gradient between start and end values.

MIRROR Repeat Mirrored – Alternate between forward and reverse playback of keyframe range.

enum in ['NONE', 'REPEAT', 'REPEAT_OFFSET', 'MIRROR'], default 'NONE'

Cycling mode to use before first keyframe

NONE No Cycles – Don’t do anything.

REPEAT Repeat Motion – Repeat keyframe range as-is.

REPEAT_OFFSET Repeat with Offset – Repeat keyframe range, but with offset based on gradient between start and end values.

MIRROR Repeat Mirrored – Alternate between forward and reverse playback of keyframe range.

enum in ['NONE', 'REPEAT', 'REPEAT_OFFSET', 'MIRROR'], default 'NONE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierEnvelopeControlPoint(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierEnvelopeControlPoint.html

**Contents:**
- FModifierEnvelopeControlPoint(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Control point for envelope F-Modifier

Frame this control-point occurs on

float in [-inf, inf], default 0.0

Upper bound of envelope at this control-point

float in [-inf, inf], default 0.0

Lower bound of envelope at this control-point

float in [-inf, inf], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifierEnvelope.control_points

FModifierEnvelopeControlPoints.add

FModifierEnvelopeControlPoints.remove

---

## FModifierEnvelope(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierEnvelope.html

**Contents:**
- FModifierEnvelope(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Scale the values of the modified F-Curve

Control points defining the shape of the envelope

FModifierEnvelopeControlPoints bpy_prop_collection of FModifierEnvelopeControlPoint, (readonly)

Upper distance from Reference Value for 1:1 default influence

float in [-inf, inf], default 1.0

Lower distance from Reference Value for 1:1 default influence

float in [-inf, inf], default -1.0

Value that envelope’s influence is centered around / based on

float in [-inf, inf], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierEnvelopeControlPoints(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierEnvelopeControlPoints.html

**Contents:**
- FModifierEnvelopeControlPoints(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Control points defining the shape of the envelope

Add a control point to a FModifierEnvelope

frame (float in [-inf, inf]) – Frame to add this control-point

Newly created control-point

FModifierEnvelopeControlPoint

Remove a control-point from an FModifierEnvelope

point (FModifierEnvelopeControlPoint, (never None)) – Control-point to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifierEnvelope.control_points

---

## FModifierFunctionGenerator(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierFunctionGenerator.html

**Contents:**
- FModifierFunctionGenerator(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Generate values using a built-in function

Scale factor determining the maximum/minimum values

float in [-inf, inf], default 1.0

Type of built-in function to use

LN Natural Logarithm.

SINC Normalized Sine – sin(x) / x.

enum in ['SIN', 'COS', 'TAN', 'SQRT', 'LN', 'SINC'], default 'SIN'

Scale factor determining the ‘speed’ of the function

float in [-inf, inf], default 1.0

Constant factor to offset time by for function

float in [-inf, inf], default 0.0

Values generated by this modifier are applied on top of the existing values instead of overwriting them

boolean, default False

Constant factor to offset values by

float in [-inf, inf], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierGenerator(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierGenerator.html

**Contents:**
- FModifierGenerator(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Deterministically generate values for the modified F-Curve

Coefficients for ‘x’ (starting from lowest power of x^0)

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

Type of generator to use

enum in ['POLYNOMIAL', 'POLYNOMIAL_FACTORISED'], default 'POLYNOMIAL'

The highest power of ‘x’ for this polynomial (number of coefficients - 1)

int in [1, 100], default 0

Values generated by this modifier are applied on top of the existing values instead of overwriting them

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierLimits(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierLimits.html

**Contents:**
- FModifierLimits(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Limit the time/value ranges of the modified F-Curve

Highest X value to allow

float in [-inf, inf], default 0.0

Highest Y value to allow

float in [-inf, inf], default 0.0

Lowest X value to allow

float in [-inf, inf], default 0.0

Lowest Y value to allow

float in [-inf, inf], default 0.0

Use the maximum X value

boolean, default False

Use the maximum Y value

boolean, default False

Use the minimum X value

boolean, default False

Use the minimum Y value

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierNoise(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierNoise.html

**Contents:**
- FModifierNoise(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Give randomness to the modified F-Curve

Method of modifying the existing F-Curve

enum in ['REPLACE', 'ADD', 'SUBTRACT', 'MULTIPLY'], default 'REPLACE'

Amount of fine level detail present in the noise

int in [0, 32767], default 0

Gap between successive frequencies. Depth needs to be greater than 0 for this to have an effect

float in [-inf, inf], default 2.0

Time offset for the noise effect

float in [-inf, inf], default 0.0

A random seed for the noise effect

float in [-inf, inf], default 1.0

Amount of high frequency detail. Depth needs to be greater than 0 for this to have an effect

float in [-inf, inf], default 0.5

Scaling (in time) of the noise

float in [-inf, inf], default 1.0

Amplitude of the noise - the amount that it modifies the underlying curve

float in [-inf, inf], default 1.0

Use the legacy way of generating noise. Has the issue that it can produce values outside of -1/1

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FModifierStepped(FModifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FModifierStepped.html

**Contents:**
- FModifierStepped(FModifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FModifier

Hold each interpolated value from the F-Curve for several frames without changing the timing

Frame that modifier’s influence ends (if applicable)

float in [-inf, inf], default 0.0

Reference number of frames before frames get held (use to get hold for ‘1-3’ vs ‘5-7’ holding patterns)

float in [-inf, inf], default 0.0

Frame that modifier’s influence starts (if applicable)

float in [-inf, inf], default 0.0

Number of frames to hold each value

float in [-inf, inf], default 2.0

Restrict modifier to only act before its ‘end’ frame

boolean, default False

Restrict modifier to only act after its ‘start’ frame

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FModifier.show_expanded

FModifier.use_restricted_range

FModifier.frame_start

FModifier.use_influence

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FModifier.bl_rna_get_subclass

FModifier.bl_rna_get_subclass_py

---

## FieldSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FieldSettings.html

**Contents:**
- FieldSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Field settings for an object in physics simulation

Affect particle’s location

boolean, default False

Affect particle’s dynamic rotation

boolean, default False

Maximum distance for the field to work

float in [0, inf], default 0.0

Minimum distance for the field’s falloff

float in [0, 1000], default 0.0

How quickly strength falls off with distance from the force field

float in [0, 10], default 0.0

enum in ['CONE', 'SPHERE', 'TUBE'], default 'SPHERE'

Convert effector force into air flow velocity

float in [-inf, inf], default 0.0

float in [-1, 1], default 0.0

float in [-0.999, 0.999], default 0.0

Guide-free time from particle life’s end

float in [0, 0.99], default 0.0

The amplitude of the offset

float in [0, 10], default 0.0

Which axis to use for offset

enum in Axis Xyz Items, default 'X'

The frequency of the offset (1/total length)

float in [0, 10], default 0.0

Adjust the offset to the beginning/end

float in [-0.999, 0.999], default 0.0

Type of periodic offset on the curve

enum in ['NONE', 'BRAID', 'CURL', 'RADIAL', 'ROLL', 'ROTATION', 'WAVE'], default 'NONE'

The distance from which particles are affected fully

float in [-inf, inf], default 0.0

Damping of the harmonic force

float in [-inf, inf], default 0.0

Inwards component of the vortex force

float in [-inf, inf], default 0.0

Drag component proportional to velocity

float in [-inf, inf], default 0.0

Amount of noise for the force strength

float in [0, 10], default 0.0

Drag component proportional to the square of velocity

float in [-inf, inf], default 0.0

Radial falloff power (real gravitational falloff = 2)

float in [0, 10], default 0.0

Maximum radial distance for the field to work

float in [0, 1000], default 0.0

Minimum radial distance for the field’s falloff

float in [0, 1000], default 0.0

Rest length of the harmonic force

float in [0, inf], default 0.0

int in [1, 128], default 0

Which direction is used to calculate the effector force

POINT Point – Field originates from the object center.

LINE Line – Field originates from the local Z axis of the object.

PLANE Plane – Field originates from the local XY plane of the object.

SURFACE Surface – Field originates from the surface of the object.

POINTS Every Point – Field originates from all of the vertices of the object.

enum in ['POINT', 'LINE', 'PLANE', 'SURFACE', 'POINTS'], default 'POINT'

Size of the turbulence

float in [0, inf], default 0.0

Select domain object of the smoke simulation

Strength of force field

float in [-inf, inf], default 0.0

Texture to use as force

How the texture effect is calculated (RGB and Curl need a RGB texture, else Gradient will be used instead)

enum in ['CURL', 'GRADIENT', 'RGB'], default 'RGB'

Defines size of derivative offset used for calculating gradient and curl

float in [0.0001, 1], default 0.0

BOID Boid – Create a force that acts as a boid’s predators or target.

CHARGE Charge – Spherical forcefield based on the charge of particles, only influences other charge force fields.

GUIDE Curve Guide – Create a force along a curve object.

DRAG Drag – Create a force that dampens motion.

FLUID_FLOW Fluid Flow – Create a force based on fluid simulation velocities.

FORCE Force – Radial field toward the center of object.

HARMONIC Harmonic – The source of this force field is the zero point of a harmonic oscillator.

LENNARDJ Lennard-Jones – Forcefield based on the Lennard-Jones potential.

MAGNET Magnetic – Forcefield depends on the speed of the particles.

TEXTURE Texture – Force field based on a texture.

TURBULENCE Turbulence – Create turbulence with a noise field.

VORTEX Vortex – Spiraling force that twists the force object’s local Z axis.

WIND Wind – Constant force along the force object’s local Z axis.

enum in ['NONE', 'BOID', 'CHARGE', 'GUIDE', 'DRAG', 'FLUID_FLOW', 'FORCE', 'HARMONIC', 'LENNARDJ', 'MAGNET', 'TEXTURE', 'TURBULENCE', 'VORTEX', 'WIND'], default 'NONE'

Apply force only in 2D

boolean, default False

Force gets absorbed by collision objects

boolean, default False

Use effector/global coordinates for turbulence

boolean, default False

Multiply force by 1/distance²

boolean, default False

Based on distance/falloff it adds a portion of the entire path

boolean, default False

Use curve weights to influence the particle influence along the curve

boolean, default False

Use a maximum distance for the field to work

boolean, default False

Use a minimum distance for the field’s falloff

boolean, default False

Every point is affected by multiple springs

boolean, default False

Use object/global coordinates for texture

boolean, default False

Use a maximum radial distance for the field to work

boolean, default False

Use a minimum radial distance for the field’s falloff

boolean, default False

Texture coordinates from root particle locations

boolean, default False

Adjust force strength based on smoke density

boolean, default False

How much the force is reduced when acting parallel to a surface, e.g. cloth

float in [0, 1], default 0.0

Effect in full or only positive/negative Z direction

enum in ['POSITIVE', 'NEGATIVE', 'BOTH'], default 'BOTH'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ParticleSettings.force_field_1

ParticleSettings.force_field_2

---

## FileAssetSelectIDFilter(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileAssetSelectIDFilter.html

**Contents:**
- FileAssetSelectIDFilter(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Which asset types to show/hide, when browsing an asset library

Show Annotation data-blocks

boolean, default False

Show Armature data-blocks

boolean, default False

Show Cache File data-blocks

boolean, default False

Show Camera data-blocks

boolean, default False

Show Curve data-blocks

boolean, default False

Show/hide Curves data-blocks

boolean, default False

Show Font data-blocks

boolean, default False

Show Grease Pencil data-blocks

boolean, default False

Show Image data-blocks

boolean, default False

Show Lattice data-blocks

boolean, default False

Show Light data-blocks

boolean, default False

Show Light Probe data-blocks

boolean, default False

Show Freestyle’s Line Style data-blocks

boolean, default False

Show Mask data-blocks

boolean, default False

Show Mesh data-blocks

boolean, default False

Show Metaball data-blocks

boolean, default False

Show Movie Clip data-blocks

boolean, default False

Show Paint Curve data-blocks

boolean, default False

Show Palette data-blocks

boolean, default False

Show Particle Settings data-blocks

boolean, default False

Show/hide Point Cloud data-blocks

boolean, default False

Show Sound data-blocks

boolean, default False

Show Speaker data-blocks

boolean, default False

Show Text data-blocks

boolean, default False

Show Texture data-blocks

boolean, default False

Show/hide Volume data-blocks

boolean, default False

Show workspace data-blocks

boolean, default False

Show Action data-blocks

boolean, default False

Show Brushes data-blocks

boolean, default False

Show Collection data-blocks

boolean, default False

Show Material data-blocks

boolean, default False

Show Node Tree data-blocks

boolean, default False

Show Object data-blocks

boolean, default False

Show Scene data-blocks

boolean, default False

Show World data-blocks

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FileAssetSelectParams.filter_asset_id

---

## FileAssetSelectParams(FileSelectParams)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileAssetSelectParams.html

**Contents:**
- FileAssetSelectParams(FileSelectParams)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, FileSelectParams

Settings for the file selection in Asset Browser mode

ALL All Libraries – Show assets from all of the listed asset libraries.

LOCAL Current File – Show the assets currently available in this Blender session.

ESSENTIALS Essentials – Show the basic building blocks and utilities coming with Blender.

CUSTOM Custom – Show assets from the asset libraries configured in the Preferences.

enum in ['ALL', 'LOCAL', 'ESSENTIALS', 'CUSTOM'], default 'ALL'

The UUID of the catalog shown in the browser

string, default “”, (never None)

Which asset types to show/hide, when browsing an asset library

FileAssetSelectIDFilter, (readonly, never None)

Determine how the asset will be imported

FOLLOW_PREFS Follow Preferences – Use the import method set in the Preferences for this asset library, don’t override it for this Asset Browser.

LINK Link – Import the assets as linked data-block.

APPEND Append – Import the asset as copied data-block, with no link to the original asset data-block.

APPEND_REUSE Append (Reuse Data) – Import the asset as copied data-block while avoiding multiple copies of nested, typically heavy data. For example the textures of a material asset, or the mesh of an object asset, don’t have to be copied every time this asset is imported. The instances of the asset share the data instead.

PACK Pack – Import the asset as linked data-block, and pack it in the current file (ensures that it remains unchanged in case the library data is modified, is not available anymore, etc.).

enum in ['FOLLOW_PREFS', 'LINK', 'APPEND', 'APPEND_REUSE', 'PACK'], default 'LINK'

Create instances for collections when appending, rather than adding them directly to the scene

boolean, default False

Create instances for collections when linking, rather than adding them directly to the scene

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

FileSelectParams.title

FileSelectParams.directory

FileSelectParams.filename

FileSelectParams.use_library_browsing

FileSelectParams.display_type

FileSelectParams.recursion_level

FileSelectParams.show_details_size

FileSelectParams.show_details_datetime

FileSelectParams.use_filter

FileSelectParams.show_hidden

FileSelectParams.sort_method

FileSelectParams.use_sort_invert

FileSelectParams.use_filter_image

FileSelectParams.use_filter_blender

FileSelectParams.use_filter_backup

FileSelectParams.use_filter_movie

FileSelectParams.use_filter_script

FileSelectParams.use_filter_font

FileSelectParams.use_filter_sound

FileSelectParams.use_filter_text

FileSelectParams.use_filter_volume

FileSelectParams.use_filter_folder

FileSelectParams.use_filter_blendid

FileSelectParams.use_filter_asset_only

FileSelectParams.filter_id

FileSelectParams.filter_glob

FileSelectParams.filter_search

FileSelectParams.display_size

FileSelectParams.display_size_discrete

FileSelectParams.list_display_size

FileSelectParams.list_column_size

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FileSelectParams.bl_rna_get_subclass

FileSelectParams.bl_rna_get_subclass_py

---

## FileBrowserFSMenuEntry(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileBrowserFSMenuEntry.html

**Contents:**
- FileBrowserFSMenuEntry(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

File Select Parameters

int in [-inf, inf], default 0

string, default “”, (never None)

string, default “”, (never None)

Whether this path is saved in bookmarks, or generated from OS

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

SpaceFileBrowser.bookmarks

SpaceFileBrowser.recent_folders

SpaceFileBrowser.system_bookmarks

SpaceFileBrowser.system_folders

---

## FileHandler(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileHandler.html

**Contents:**
- FileHandler(bpy_struct)¶
- Basic FileHandler for importing a single file¶
- FileHandler for Importing multiple files and exposing Operator options¶
- Inherited Properties¶
- Inherited Functions¶

A file handler allows custom drag-and-drop behavior to be associated with a given Operator (FileHandler.bl_import_operator) and set of file extensions (FileHandler.bl_file_extensions). Control over which area of the UI accepts the drag-in-drop action is specified using the FileHandler.poll_drop method.

Similar to operators that use a file select window, operators participating in drag-and-drop, and only accepting a single file, must define the following property:

This filepath property will be set to the full path of the file dropped by the user.

Operators which support being executed with multiple files from drag-and-drop require the following properties be defined:

These directory and files properties will be set with the necessary data from the drag-and-drop operation.

Additionally, if the operator provides operator properties that need to be accessible to the user, the ImportHelper.invoke_popup method can be used to show a dialog leveraging the standard Operator.draw method for layout and display.

base class — bpy_struct

subclasses — IMAGE_FH_drop_handler, IO_FH_gltf2, IO_FH_svg_as_curves, NODE_FH_image_node, SEQUENCER_FH_image_strip, SEQUENCER_FH_movie_strip, SEQUENCER_FH_sound_strip, VIEW3D_FH_camera_background_image, VIEW3D_FH_empty_image, VIEW3D_FH_vdb_volume

Extends functionality to operators that manages files, such as adding drag and drop support

Operator that can handle export for files with the extensions given in bl_file_extensions

string, default “”, (never None)

Formatted string of file extensions supported by the file handler, each extension should start with a “.” and be separated by “;”. For Example: ".blend;.ble"

string, default “”, (never None)

If this is set, the file handler gets a custom ID, otherwise it takes the name of the class used to define the file handler (for example, if the class name is “OBJECT_FH_hello”, and bl_idname is not set by the script, then bl_idname = “OBJECT_FH_hello”)

string, default “”, (never None)

Operator that can handle import for files with the extensions given in bl_file_extensions

string, default “”, (never None)

The file handler label

string, default “”, (never None)

If this method returns True, can be used to handle the drop of a drag-and-drop action

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

**Examples:**

Example 1 (yaml):
```yaml
filepath: bpy.props.StringProperty(subtype='FILE_PATH', options={'SKIP_SAVE'})
```

Example 2 (python):
```python
import bpy


class CurveTextImport(bpy.types.Operator):
    """
    Creates a text object from a text file.
    """
    bl_idname = "curve.text_import"
    bl_label = "Import a text file as text object"

    # This Operator supports processing one `.txt` file at a time. The following file-path
    # property must be defined.
    filepath: bpy.props.StringProperty(subtype='FILE_PATH', options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return (context.area and context.area.type == "VIEW_3D")

    def execute(self, context):
        # Direct calls to this Operator may use unsupported file-paths. Ensure the incoming
        # file-path is one that is supported.
        if not self.filepath or not self.filepath.endswith(".txt"):
            return {'CANCELLED'}

        # Create a Blender Text object from the contents of the provided file.
        with open(self.filepath) as file:
            text_curve = bpy.data.curves.new(type="FONT", name="Text")
            text_curve.body = ''.join(file.readlines())
            text_object = bpy.data.objects.new(name="Text", object_data=text_curve)
            bpy.context.scene.collection.objects.link(text_object)
        return {'FINISHED'}

    # By default the file handler invokes the operator with the file-path property set. If the
    # operator also supports being invoked with no file-path set, and allows the user to pick from a
    # file select window instead, the following logic can be used.
    #
    # Note: It is important to use `options={'SKIP_SAVE'}` when defining the file-path property to
    # avoid prior values from being reused on subsequent calls.

    def invoke(self, context, event):
        if self.filepath:
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# Define a file handler that supports the following set of conditions:
#  - Execute the `curve.text_import` operator
#  - When `.txt` files are dropped in the 3D Viewport
class CURVE_FH_text_import(bpy.types.FileHandler):
    bl_idname = "CURVE_FH_text_import"
    bl_label = "File handler for curve text object import"
    bl_import_operator = "curve.text_import"
    bl_file_extensions = ".txt"

    @classmethod
    def poll_drop(cls, context):
        return (context.area and context.area.type == 'VIEW_3D')


bpy.utils.register_class(CurveTextImport)
bpy.utils.register_class(CURVE_FH_text_import)
```

Example 3 (yaml):
```yaml
directory: StringProperty(subtype='DIR_PATH', options={'SKIP_SAVE', 'HIDDEN'})
files: CollectionProperty(type=OperatorFileListElement, options={'SKIP_SAVE', 'HIDDEN'})
```

Example 4 (python):
```python
import bpy
from bpy_extras.io_utils import ImportHelper
from mathutils import Vector


class ShaderScriptImport(bpy.types.Operator, ImportHelper):
    """
    Creates one or more Shader Script nodes from text files.
    """
    bl_idname = "shader.script_import"
    bl_label = "Import a text file as a script node"

    # This Operator supports processing multiple `.txt` files at a time. The following properties
    # must be defined.
    directory: bpy.props.StringProperty(subtype='DIR_PATH', options={'SKIP_SAVE', 'HIDDEN'})
    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement, options={'SKIP_SAVE', 'HIDDEN'})

    # Allow the user to choose whether the node's label is set or not
    set_label: bpy.props.BoolProperty(name="Set Label", default=False)

    @classmethod
    def poll(cls, context):
        return (
            context.region and context.region.type == 'WINDOW' and
            context.area and context.area.ui_type == 'ShaderNodeTree' and
            context.object and context.object.type == 'MESH' and
            context.material
        )

    def execute(self, context):
        # The directory property must be set.
        if not self.directory:
            return {'CANCELLED'}

        x = 0.0
        y = 0.0
        for file in self.files:
            # Direct calls to this Operator may use unsupported file-paths. Ensure the incoming
            # files are ones that are supported.
            if file.name.endswith(".txt"):
                import os
                filepath = os.path.join(self.directory, file.name)

                node_tree = context.material.node_tree
                text_node = node_tree.nodes.new(type="ShaderNodeScript")
                text_node.mode = 'EXTERNAL'
                text_node.filepath = filepath
                text_node.location = Vector((x, y))

                # Set the node's title to the file name.
                if self.set_label:
                    text_node.label = file.name

                x += 20.0
                y -= 20.0

        return {'FINISHED'}

    # Use ImportHelper's invoke_popup() to handle the invocation so that this operator's properties
    # are shown in a popup. This allows the user to configure additional settings on the operator
    # like the `set_label` property. Consider having a draw() method on the operator in order to
    # layout the properties in the UI appropriately.
    #
    # If filepath information is not provided the file select window will be invoked instead.

    def invoke(self, context, event):
        return self.invoke_popup(context)


# Define a file handler that supports the following set of conditions:
#  - Execute the `shader.script_import` operator
#  - When `.txt` files are dropped in the Shader Editor
class SHADER_FH_script_import(bpy.types.FileHandler):
    bl_idname = "SHADER_FH_script_import"
    bl_label = "File handler for shader script node import"
    bl_import_operator = "shader.script_import"
    bl_file_extensions = ".txt"

    @classmethod
    def poll_drop(cls, context):
        return (
            context.region and context.region.type == 'WINDOW' and
            context.area and context.area.ui_type == 'ShaderNodeTree'
        )


bpy.utils.register_class(ShaderScriptImport)
bpy.utils.register_class(SHADER_FH_script_import)
```

---

## FileSelectIDFilter(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileSelectIDFilter.html

**Contents:**
- FileSelectIDFilter(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Which ID types to show/hide, when browsing a library

boolean, default False

Show worlds, lights, cameras and speakers

boolean, default False

Show meshes, curves, lattice, armatures and metaballs data

boolean, default False

Show images, movie clips, sounds and masks

boolean, default False

Show other data types

boolean, default False

Show objects and collections

boolean, default False

boolean, default False

Show materials, node-trees, textures and Freestyle’s line-styles

boolean, default False

Show Action data-blocks

boolean, default False

Show Annotation data-blocks

boolean, default False

Show Armature data-blocks

boolean, default False

Show Brushes data-blocks

boolean, default False

Show Cache File data-blocks

boolean, default False

Show Camera data-blocks

boolean, default False

Show Curve data-blocks

boolean, default False

Show/hide Curves data-blocks

boolean, default False

Show Font data-blocks

boolean, default False

Show Grease Pencil data-blocks

boolean, default False

Show Collection data-blocks

boolean, default False

Show Image data-blocks

boolean, default False

Show Lattice data-blocks

boolean, default False

Show Light data-blocks

boolean, default False

Show Light Probe data-blocks

boolean, default False

Show Freestyle’s Line Style data-blocks

boolean, default False

Show Mask data-blocks

boolean, default False

Show Material data-blocks

boolean, default False

Show Mesh data-blocks

boolean, default False

Show Metaball data-blocks

boolean, default False

Show Movie Clip data-blocks

boolean, default False

Show Node Tree data-blocks

boolean, default False

Show Object data-blocks

boolean, default False

Show Paint Curve data-blocks

boolean, default False

Show Palette data-blocks

boolean, default False

Show Particle Settings data-blocks

boolean, default False

Show/hide Point Cloud data-blocks

boolean, default False

Show Scene data-blocks

boolean, default False

Show Sound data-blocks

boolean, default False

Show Speaker data-blocks

boolean, default False

Show Text data-blocks

boolean, default False

Show Texture data-blocks

boolean, default False

Show/hide Volume data-blocks

boolean, default False

Show workspace data-blocks

boolean, default False

Show World data-blocks

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FileSelectParams.filter_id

---

## FileSelectEntry(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileSelectEntry.html

**Contents:**
- FileSelectEntry(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶

base class — bpy_struct

A file viewable in the File Browser

Asset data, valid if the file represents an asset

AssetMetaData, (readonly)

string, default “”, (readonly, never None)

Unique integer identifying the preview of this file as an icon (zero means invalid)

int in [-inf, inf], default 0, (readonly)

Path relative to the directory currently displayed in the File Browser (includes the file name)

string, default “”, (readonly, never None)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## FileSelectParams(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FileSelectParams.html

**Contents:**
- FileSelectParams(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

subclasses — FileAssetSelectParams

File Select Parameters

Directory displayed in the file browser

byte string, default “”, (never None)

Change the size of thumbnails

int in [16, 256], default 96

Change the size of thumbnails in discrete steps

enum in ['TINY', 'SMALL', 'NORMAL', 'BIG', 'LARGE'], default 'TINY'

Display mode for the file list

LIST_VERTICAL Vertical List – Display files as a vertical list.

LIST_HORIZONTAL Horizontal List – Display files as a horizontal list.

THUMBNAIL Thumbnails – Display files as thumbnails.

enum in ['LIST_VERTICAL', 'LIST_HORIZONTAL', 'THUMBNAIL'], default 'LIST_VERTICAL'

Active file in the file browser

string, default “”, (never None)

UNIX shell-like filename patterns matching, supports wildcards (‘*’) and list of patterns separated by ‘;’

string, default “”, (never None)

Which ID types to show/hide, when browsing a library

FileSelectIDFilter, (readonly, never None)

Filter by name or tag, supports ‘*’ wildcard

string, default “”, (never None)

The width of columns in horizontal list views

int in [32, 750], default 32

Change the size of thumbnails in list views

int in [16, 128], default 32

Numbers of dirtree levels to show simultaneously

NONE None – Only list current directory’s content, with no recursion.

BLEND Blend File – List .blend files’ content.

ALL_1 One Level – List all sub-directories’ content, one level of recursion.

ALL_2 Two Levels – List all sub-directories’ content, two levels of recursion.

ALL_3 Three Levels – List all sub-directories’ content, three levels of recursion.

enum in ['NONE', 'BLEND', 'ALL_1', 'ALL_2', 'ALL_3'], default 'NONE'

Show a column listing the date and time of modification for each file

boolean, default False

Show a column listing the size of each file

boolean, default False

Show hidden dot files

boolean, default False

enum in Fileselect Params Sort Items, default 'FILE_SORT_ALPHA'

Title for the file browser

string, default “”, (readonly, never None)

Enable filtering of files

boolean, default False

Hide .blend files items that are not data-blocks with asset metadata

boolean, default False

Show .blend1, .blend2, etc. files

boolean, default False

boolean, default False

Show .blend files items (objects, materials, etc.)

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

Whether we may browse Blender files’ content or not

boolean, default False, (readonly)

Sort items descending, from highest value to lowest

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

SpaceFileBrowser.params

UILayout.template_file_select_path

---

## Float2Attribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Float2Attribute.html

**Contents:**
- Float2Attribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores floating-point 2D vectors

bpy_prop_collection of Float2AttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## Float2AttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Float2AttributeValue.html

**Contents:**
- Float2AttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

2D Vector value in geometry attribute

mathutils.Vector of 2 items in [-inf, inf], default (0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## Float4x4Attribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Float4x4Attribute.html

**Contents:**
- Float4x4Attribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores a 4 by 4 float matrix

bpy_prop_collection of Float4x4AttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## Float4x4AttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Float4x4AttributeValue.html

**Contents:**
- Float4x4AttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Matrix value in geometry attribute

mathutils.Matrix of 4 * 4 items in [-inf, inf], default ((0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0))

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Float4x4Attribute.data

---

## FloatAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatAttribute.html

**Contents:**
- FloatAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores floating-point values

bpy_prop_collection of FloatAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## FloatAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatAttributeValue.html

**Contents:**
- FloatAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Floating-point value in geometry attribute

float in [-inf, inf], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## FloatColorAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatColorAttribute.html

**Contents:**
- FloatColorAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores RGBA colors as floating-point values using 32-bits per channel

bpy_prop_collection of FloatColorAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## FloatColorAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatColorAttributeValue.html

**Contents:**
- FloatColorAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color value in geometry attribute

RGBA color in scene linear color space

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0)

RGBA color in sRGB color space

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FloatColorAttribute.data

---

## FloatProperty(Property)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatProperty.html

**Contents:**
- FloatProperty(Property)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Property

RNA floating-point number (single precision) property definition

Length of each dimension of the array

int array of 3 items in [0, inf], default (0, 0, 0), (readonly)

Maximum length of the array, 0 means unlimited

int in [0, inf], default 0, (readonly)

Default value for this number

float in [-inf, inf], default 0.0, (readonly)

Default value for this array

float array of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Maximum value used by buttons

float in [-inf, inf], default 0.0, (readonly)

Minimum value used by buttons

float in [-inf, inf], default 0.0, (readonly)

boolean, default False, (readonly)

Number of digits after the dot used by buttons. Fraction is automatically hidden for exact integer values of fields with unit ‘NONE’ or ‘TIME’ (frame count) and step divisible by 100.

int in [0, inf], default 0, (readonly)

Maximum value used by buttons

float in [-inf, inf], default 0.0, (readonly)

Minimum value used by buttons

float in [-inf, inf], default 0.0, (readonly)

Step size used by number buttons, for floats 1/100th of the step size

float in [0, inf], default 0.0, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Property.translation_context

Property.is_animatable

Property.is_overridable

Property.is_argument_optional

Property.is_never_none

Property.is_skip_save

Property.is_skip_preset

Property.is_registered

Property.is_registered_optional

Property.is_enum_flag

Property.is_library_editable

Property.is_path_output

Property.is_path_supports_blend_relative

Property.is_path_supports_templates

Property.is_deprecated

Property.deprecated_note

Property.deprecated_version

Property.deprecated_removal_version

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Property.bl_rna_get_subclass

Property.bl_rna_get_subclass_py

---

## FloatVectorAttribute(Attribute)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatVectorAttribute.html

**Contents:**
- FloatVectorAttribute(Attribute)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Attribute

Geometry attribute that stores floating-point 3D vectors

bpy_prop_collection of FloatVectorAttributeValue, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Attribute.storage_type

Attribute.is_internal

Attribute.is_required

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Attribute.bl_rna_get_subclass

Attribute.bl_rna_get_subclass_py

---

## FloatVectorAttributeValue(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatVectorAttributeValue.html

**Contents:**
- FloatVectorAttributeValue(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Vector value in geometry attribute

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FloatVectorAttribute.data

---

## FloatVectorValueReadOnly(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloatVectorValueReadOnly.html

**Contents:**
- FloatVectorValueReadOnly(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## FloorConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FloorConstraint.html

**Contents:**
- FloorConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Use the target object for location limitation

Location of target that object will not pass through

enum in ['FLOOR_X', 'FLOOR_Y', 'FLOOR_Z', 'FLOOR_NEGATIVE_X', 'FLOOR_NEGATIVE_Y', 'FLOOR_NEGATIVE_Z'], default 'FLOOR_X'

Offset of floor from object origin

float in [-inf, inf], default 0.0

Armature bone, mesh or lattice vertex group, …

string, default “”, (never None)

Use the target’s rotation to determine floor

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## FluidDomainSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FluidDomainSettings.html

**Contents:**
- FluidDomainSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Fluid domain settings

Margin added around fluid to minimize boundary interference

int in [2, 24], default 4

Minimum amount of fluid grid values (smoke density, fuel and heat) a cell can contain, before it is considered empty

float in [0, 1], default 0.002

Maximum number of additional cells

int in [0, 512], default 0

Buoyant force based on smoke density (higher value results in faster rising smoke)

float in [-5, 5], default 1.0

Buoyant force based on smoke heat (higher value results in faster rising smoke)

float in [-5, 5], default 1.0

Speed of the burning reaction (higher value results in smaller flames)

float in [0.01, 4], default 0.75

Select the file format to be used for caching volumetric data

UNI Uni Cache – Uni file format (.uni).

OPENVDB OpenVDB – OpenVDB file format (.vdb).

RAW Raw Cache – Raw file format (.raw).

enum in ['UNI', 'OPENVDB', 'RAW'], default 'OPENVDB'

Directory that contains fluid cache files

string, default “”, (never None, blend relative // prefix supported)

Frame on which the simulation stops (last frame baked)

int in [-1048574, 1048574], default 250

Frame offset that is used when loading the simulation from the cache. It is not considered when baking the simulation, only when loading it.

int in [-1048574, 1048574], default 0

int in [-inf, inf], default 0

int in [-inf, inf], default 0

int in [-inf, inf], default 0

int in [-inf, inf], default 0

int in [-inf, inf], default 0

Frame on which the simulation starts (first frame baked)

int in [-1048574, 1048574], default 1

Select the file format to be used for caching surface data

UNI Uni Cache – Uni file format (.uni).

OPENVDB OpenVDB – OpenVDB file format (.vdb).

RAW Raw Cache – Raw file format (.raw).

enum in ['UNI', 'OPENVDB', 'RAW'], default 'UNI'

Select the file format to be used for caching noise data

UNI Uni Cache – Uni file format (.uni).

OPENVDB OpenVDB – OpenVDB file format (.vdb).

RAW Raw Cache – Raw file format (.raw).

enum in ['UNI', 'OPENVDB', 'RAW'], default 'OPENVDB'

Select the file format to be used for caching particle data

UNI Uni Cache – Uni file format (.uni).

OPENVDB OpenVDB – OpenVDB file format (.vdb).

RAW Raw Cache – Raw file format (.raw).

enum in ['UNI', 'OPENVDB', 'RAW'], default 'OPENVDB'

Additional data will be saved so that the bake jobs can be resumed after pausing. Because more data will be written to disk it is recommended to avoid enabling this option when baking at high resolutions.

boolean, default False

Change the cache type of the simulation

REPLAY Replay – Use the timeline to bake the scene.

MODULAR Modular – Bake every stage of the simulation separately.

ALL All – Bake all simulation settings at once.

enum in ['REPLAY', 'MODULAR', 'ALL'], default 'REPLAY'

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Maximal velocity per cell (greater CFL numbers will minimize the number of simulation steps and the computation time.)

float in [0, 10], default 2.0

Value under which voxels are considered empty space to optimize rendering

float in [0, 1], default 1e-06

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

ColorRamp, (readonly)

Simulation field to color map

enum in ['NONE'], default 'NONE'

Multiplier for scaling the selected field to color map

float in [0.001, 100000], default 1.0

Delete fluid inside obstacles

boolean, default False

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

Interpolation method to use for smoke/fire volumes in solid mode

LINEAR Linear – Good smoothness and speed.

CUBIC Cubic – Smoothed high quality interpolation, but slower.

CLOSEST Closest – No interpolation.

enum in ['LINEAR', 'CUBIC', 'CLOSEST'], default 'LINEAR'

Thickness of smoke display in the viewport

float in [0.001, 1000], default 1.0

Determine how quickly the smoke dissolves (lower value makes smoke disappear faster)

int in [1, 10000], default 5

Smoke Grid Resolution

int array of 3 items in [-inf, inf], default (0, 0, 0), (readonly)

Change domain type of the simulation

GAS Gas – Create domain for gases.

LIQUID Liquid – Create domain for liquids.

enum in ['GAS', 'LIQUID'], default 'GAS'

Limit effectors to this collection

EffectorWeights, (readonly)

Generate and export Mantaflow script from current domain settings during bake. This is only needed if you plan to analyze the cache (e.g. view grids, velocity vectors, particles) in Mantaflow directly (outside of Blender) after baking the simulation.

boolean, default False

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

Minimum temperature of the flames (higher value results in faster rising flames)

float in [0.5, 5], default 1.5

Maximum temperature of the flames (higher value results in faster rising flames)

float in [1, 10], default 3.0

Amount of smoke created by burning fuel

float in [0, 8], default 1.0

Color of smoke emitted from burning fuel

mathutils.Color of 3 items in [0, inf], default (0.7, 0.7, 0.7)

Additional vorticity for the flames

float in [0, 2], default 0.5

PIC/FLIP Ratio. A value of 1.0 will result in a completely FLIP based simulation. Use a lower value for simulations which should produce smaller splashes.

float in [0, 1], default 0.97

Limit fluid objects to this collection

Limit forces to this collection

Determines how far apart fluid and obstacle are (higher values will result in fluid being further away from obstacles, smaller values will let fluid move towards the inside of obstacles)

float in [-5, 5], default 0.5

Determines how much fluid is allowed in an obstacle cell (higher values will tag a boundary cell as an obstacle easier and reduce the boundary smoothening effect)

float in [0.001, 1], default 0.05

Gravity in X, Y and Z direction

mathutils.Vector of 3 items in [-1000.1, 1000.1], default (0.0, 0.0, -9.81)

Cell type to be highlighted

NONE None – Highlight the cells regardless of their type.

FLUID Fluid – Highlight only the cells of type Fluid.

OBSTACLE Obstacle – Highlight only the cells of type Obstacle.

EMPTY Empty – Highlight only the cells of type Empty.

INFLOW Inflow – Highlight only the cells of type Inflow.

OUTFLOW Outflow – Highlight only the cells of type Outflow.

enum in ['NONE', 'FLUID', 'OBSTACLE', 'EMPTY', 'INFLOW', 'OUTFLOW'], default 'NONE'

Simulation field to color map onto gridlines

FLAGS Flags – Flag grid of the fluid domain.

RANGE Highlight Range – Highlight the voxels with values of the color mapped field within the range.

enum in ['NONE', 'FLAGS', 'RANGE'], default 'NONE'

Lower bound of the highlighting range

float in [-inf, inf], default 0.0

Color used to highlight the range

float array of 4 items in [0, inf], default (1.0, 0.0, 0.0, 1.0)

Upper bound of the highlighting range

float in [-inf, inf], default 1.0

Guiding weight (higher value results in greater lag)

float in [1, 100], default 2.0

Guiding size (higher value results in larger vortices)

int in [1, 50], default 5

Use velocities from this object for the guiding effect (object needs to have fluid modifier and be of type domain))

Choose where to get guiding velocities from

DOMAIN Domain – Use a fluid domain for guiding (domain needs to be baked already so that velocities can be extracted). Guiding domain can be of any type (i.e. gas or liquid)..

EFFECTOR Effector – Use guiding (effector) objects to create fluid guiding (guiding objects should be animated and baked once set up completely).

enum in ['DOMAIN', 'EFFECTOR'], default 'DOMAIN'

Guiding velocity factor (higher value results in greater guiding velocities)

float in [0, 100], default 2.0

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

Method for sampling the high resolution flow

enum in ['FULLSAMPLE', 'LINEAR', 'NEAREST'], default 'FULLSAMPLE'

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

boolean, default False

Lower mesh concavity bound (high values tend to smoothen and fill out concave regions)

float in [0, 10], default 0.4

Upper mesh concavity bound (high values tend to smoothen and fill out concave regions)

float in [0, 10], default 3.5

Which particle level set generator to use

IMPROVED Final – Use improved particle level set (slower but more precise and with mesh smoothening options).

UNION Preview – Use union particle level set (faster but lower quality).

enum in ['IMPROVED', 'UNION'], default 'IMPROVED'

Particle radius factor (higher value results in larger (meshed) particles). Needs to be adjusted after changing the mesh scale.

float in [0, 10], default 2.0

The mesh simulation is scaled up by this factor (compared to the base resolution of the domain). For best meshing, it is recommended to adjust the mesh particle radius alongside this value.

int in [1, 100], default 2

Negative mesh smoothening

int in [0, 100], default 1

Positive mesh smoothening

int in [0, 100], default 1

Scale of noise (higher value results in larger vortices)

float in [0.0001, 10], default 2.0

The noise simulation is scaled up by this factor (compared to the base resolution of the domain)

int in [1, 100], default 2

float in [0, 10], default 1.0

Animation time of noise

float in [0.0001, 10], default 0.1

Compression method to be used

ZIP Zip – Effective but slow compression.

NONE None – Do not use any compression.

enum in ['ZIP', 'NONE'], default 'ZIP'

Bit depth for fluid particles and grids (lower bit values reduce file size)

enum in ['NONE'], default 'NONE'

Particle (narrow) band width (higher value results in thicker band and more particles)

float in [0, 1000], default 3.0

Maximum number of particles per cell (ensures that each cell has at most this amount of particles)

int in [0, 1000], default 16

Minimum number of particles per cell (ensures that each cell has at least this amount of particles)

int in [0, 1000], default 8

Particle number factor (higher value results in more particles)

int in [1, 5], default 2

Particle radius factor. Increase this value if the simulation appears to leak volume, decrease it if the simulation seems to gain volume.

float in [0, 10], default 1.0

Randomness factor for particle sampling

float in [0, 10], default 0.1

The particle simulation is scaled up by this factor (compared to the base resolution of the domain)

int in [1, 100], default 1

Resolution used for the fluid domain. Value corresponds to the longest domain side (resolution for other domain sides is calculated automatically).

int in [6, 10000], default 32

boolean, default False

Visualize vector fields

boolean, default False

Change the underlying simulation method

FLIP FLIP – Use FLIP as the simulation method (more splashy behavior).

APIC APIC – Use APIC as the simulation method (more energetic and stable behavior).

enum in ['FLIP', 'APIC'], default 'FLIP'

AUTO Auto – Adjust slice direction according to the view direction.

X X – Slice along the X axis.

Y Y – Slice along the Y axis.

Z Z – Slice along the Z axis.

enum in ['AUTO', 'X', 'Y', 'Z'], default 'AUTO'

Position of the slice

float in [0, 1], default 0.5

How many slices per voxel should be generated

float in [0, 100], default 5.0

How particles that left the domain are treated

DELETE Delete – Delete secondary particles that are inside obstacles or left the domain.

PUSHOUT Push Out – Push secondary particles that left the domain back into the domain.

enum in ['DELETE', 'PUSHOUT'], default 'DELETE'

Amount of buoyancy force that rises bubbles (high value results in bubble movement mainly upwards)

float in [0, 100], default 0.5

Amount of drag force that moves bubbles along with the fluid (high value results in bubble movement mainly along with the fluid)

float in [0, 100], default 0.6

Determines which particle systems are created from secondary particles

OFF Off – Create a separate particle system for every secondary particle type.

SPRAY_FOAM Spray + Foam – Spray and foam particles are saved in the same particle system.

SPRAY_BUBBLES Spray + Bubbles – Spray and bubble particles are saved in the same particle system.

FOAM_BUBBLES Foam + Bubbles – Foam and bubbles particles are saved in the same particle system.

SPRAY_FOAM_BUBBLES Spray + Foam + Bubbles – Create one particle system that contains all three secondary particle types.

enum in ['OFF', 'SPRAY_FOAM', 'SPRAY_BUBBLES', 'FOAM_BUBBLES', 'SPRAY_FOAM_BUBBLES'], default 'OFF'

Highest possible particle lifetime

float in [0, 10000], default 25.0

Lowest possible particle lifetime

float in [0, 10000], default 10.0

Upper clamping threshold that indicates the fluid speed where cells no longer emit more particles (higher value results in generally less particles)

float in [0, 1000], default 5.0

Upper clamping threshold for marking fluid cells where air is trapped (higher value results in less marked cells)

float in [0, 1000], default 20.0

Upper clamping threshold for marking fluid cells as wave crests (higher value results in less marked cells)

float in [0, 1000], default 8.0

Lower clamping threshold that indicates the fluid speed where cells start to emit particles (lower values result in generally more particles)

float in [0, 1000], default 1.0

Lower clamping threshold for marking fluid cells where air is trapped (lower value results in more marked cells)

float in [0, 1000], default 5.0

Lower clamping threshold for marking fluid cells as wave crests (lower value results in more marked cells)

float in [0, 1000], default 2.0

Radius to compute potential for each cell (higher values are slower but create smoother potential grids)

int in [1, 4], default 2

Maximum number of particles generated per trapped air cell per frame

int in [0, 10000], default 40

Maximum number of particles generated per wave crest cell per frame

int in [0, 10000], default 200

Radius to compute position update for each particle (higher values are slower but particles move less chaotic)

int in [1, 4], default 2

mathutils.Vector of 3 items in [-inf, inf], default (0.0, 0.0, 0.0), (readonly)

Surface tension of liquid (higher value results in greater hydrophobic behavior)

float in [0, 100], default 0.0

Maximum number of fluid particles that are allowed in this simulation

int in [0, inf], default 0

Smoke temperature grid, range 0 to 1 represents 0 to 1000K

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

Adjust simulation speed

float in [0.0001, 10], default 1.0

Maximum number of simulation steps to perform for one frame

int in [1, 100], default 4

Minimum number of simulation steps to perform for one frame

int in [1, 100], default 1

Adapt simulation resolution and size to fluid

boolean, default False

Automatically decide when to perform multiple simulation steps per frame

boolean, default True

Create bubble particle system

boolean, default False

Enable collisions with back domain border

boolean, default False

Enable collisions with bottom domain border

boolean, default False

Enable collisions with front domain border

boolean, default False

Enable collisions with left domain border

boolean, default False

Enable collisions with right domain border

boolean, default False

Enable collisions with top domain border

boolean, default False

Render a simulation field while mapping its voxels values to the colors of a ramp or using a predefined color code

boolean, default False

Enable fluid diffusion settings (e.g. viscosity, surface tension)

boolean, default False

Let smoke disappear over time

boolean, default False

Dissolve smoke in a logarithmic fashion. Dissolves quickly at first, but lingers longer.

boolean, default True

Create liquid particle system

boolean, default False

Create foam particle system

boolean, default False

Fractional obstacles improve and smoothen the fluid-obstacle boundary

boolean, default False

boolean, default False

Enable fluid mesh (using amplification)

boolean, default True

Enable fluid noise (using amplification)

boolean, default False

Perform a single slice of the domain object

boolean, default False

Caches velocities of mesh vertices. These will be used (automatically) when rendering with motion blur enabled.

boolean, default False

Create spray particle system

boolean, default False

Create tracer particle system

boolean, default False

Simulate fluids with high viscosity using a special solver

boolean, default False

NEEDLE Needle – Display vectors as needles.

STREAMLINE Streamlines – Display vectors as streamlines.

MAC MAC Grid – Display vector field as MAC grid.

enum in ['NEEDLE', 'STREAMLINE', 'MAC'], default 'NEEDLE'

Vector field to be represented by the display vectors

FLUID_VELOCITY Fluid Velocity – Velocity field of the fluid domain.

GUIDE_VELOCITY Guide Velocity – Guide velocity field of the fluid domain.

FORCE Force – Force field of the fluid domain.

enum in ['FLUID_VELOCITY', 'GUIDE_VELOCITY', 'FORCE'], default 'FLUID_VELOCITY'

Multiplier for scaling the vectors

float in [0, 1000], default 1.0

Scale vectors with their magnitudes

boolean, default False

Show X-component of MAC Grid

boolean, default True

Show Y-component of MAC Grid

boolean, default True

Show Z-component of MAC Grid

boolean, default True

float array of 32 items in [-inf, inf], default (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (readonly)

Factor to control the amount of motion blur

float in [0, inf], default 1.0

Viscosity setting: value that is multiplied by 10 to the power of (exponent*-1)

float in [0, 10], default 1.0

Negative exponent for the viscosity value (to simplify entering small values e.g. 5*10^-6)

int in [0, 10], default 6

Viscosity of liquid (higher values result in more viscous fluids, a value of 0 will still apply some viscosity)

float in [0, 10], default 0.05

Amount of turbulence and rotation in smoke

float in [0, 4], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FluidModifier.domain_settings

---

## FluidEffectorSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FluidEffectorSettings.html

**Contents:**
- FluidEffectorSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Smoke collision settings

Change type of effector in the simulation

COLLISION Collision – Create collision object.

GUIDE Guide – Create guide object.

enum in ['COLLISION', 'GUIDE'], default 'COLLISION'

How to create guiding velocities

MAXIMUM Maximize – Compare velocities from previous frame with new velocities from current frame and keep the maximum.

MINIMUM Minimize – Compare velocities from previous frame with new velocities from current frame and keep the minimum.

OVERRIDE Override – Always write new guide velocities for every frame (each frame only contains current velocities from guiding objects).

AVERAGED Averaged – Take average of velocities from previous frame and new velocities from current frame.

enum in ['MAXIMUM', 'MINIMUM', 'OVERRIDE', 'AVERAGED'], default 'OVERRIDE'

Number of additional samples to take between frames to improve quality of fast moving effector objects

int in [0, 200], default 0

Additional distance around mesh surface to consider as effector

float in [0, 10], default 0.0

Control when to apply the effector

boolean, default True

Treat this object as a planar, unclosed mesh

boolean, default False

Multiplier of obstacle velocity

float in [-100, 100], default 1.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FluidModifier.effector_settings

---

## FluidFlowSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FluidFlowSettings.html

**Contents:**
- FluidFlowSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

float in [0, 10], default 1.0

Name of vertex group which determines surface emission rate

string, default “”, (never None)

Change flow behavior in the simulation

INFLOW Inflow – Add fluid to simulation.

OUTFLOW Outflow – Delete fluid from simulation.

GEOMETRY Geometry – Only use given geometry for fluid.

enum in ['INFLOW', 'OUTFLOW', 'GEOMETRY'], default 'GEOMETRY'

Change how fluid is emitted

enum in ['NONE'], default 'NONE'

Change type of fluid in the simulation

SMOKE Smoke – Add smoke.

BOTH Fire + Smoke – Add fire and smoke.

FIRE Fire – Add fire.

LIQUID Liquid – Add liquid.

enum in ['SMOKE', 'BOTH', 'FIRE', 'LIQUID'], default 'SMOKE'

float in [0, 10], default 1.0

Texture that controls emission strength

Particle size in simulation cells

float in [0.1, inf], default 1.0

Particle systems emitted from the object

mathutils.Color of 3 items in [0, inf], default (0.7, 0.7, 0.7)

Number of additional samples to take between frames to improve quality of fast moving flows

int in [0, 200], default 0

Height (in domain grid units) of fluid emission above the mesh surface. Higher values result in emission further away from the mesh surface. If this value and the emitter size are smaller than the domain grid unit, fluid will not be created

float in [0, 10], default 1.0

Temperature difference to ambient temperature

float in [-10, 10], default 1.0

AUTO Generated – Generated coordinates centered to flow object.

UV UV – Use UV layer for texture coordinates.

enum in ['AUTO', 'UV'], default 'AUTO'

Z-offset of texture mapping

float in [0, 200], default 0.0

Size of texture mapping

float in [0.01, 10], default 1.0

Only allow given density value in emitter area and will not add up

boolean, default True

Control when to apply fluid flow

boolean, default True

Fluid has some initial velocity when it is emitted

boolean, default False

Set particle size in simulation cells or use nearest cell

boolean, default True

Treat this object as a planar and unclosed mesh. Fluid will only be emitted from the mesh surface and based on the surface emission value.

boolean, default False

Use a texture to control emission strength

boolean, default False

string, default “”, (never None)

Additional initial velocity in X, Y and Z direction (added to source velocity)

mathutils.Vector of 3 items in [-1000.1, 1000.1], default (0.0, 0.0, 0.0)

Multiplier of source velocity passed to fluid (source velocity is non-zero only if object is moving)

float in [-100, 100], default 1.0

Amount of normal directional velocity

float in [-100, 100], default 0.0

Amount of random velocity

float in [0, 10], default 0.0

Controls fluid emission from within the mesh (higher value results in greater emissions from inside the mesh)

float in [0, 1], default 0.0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FluidModifier.flow_settings

---

## FluidModifier(Modifier)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FluidModifier.html

**Contents:**
- FluidModifier(Modifier)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Modifier

Fluid simulation modifier

FluidDomainSettings, (readonly)

FluidEffectorSettings, (readonly)

FluidFlowSettings, (readonly)

DOMAIN Domain – Container of the fluid simulation.

FLOW Flow – Add or remove fluid to a domain object.

EFFECTOR Effector – Deflect fluids and influence the fluid flow.

enum in ['NONE', 'DOMAIN', 'FLOW', 'EFFECTOR'], default 'NONE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Modifier.show_viewport

Modifier.show_in_editmode

Modifier.show_on_cage

Modifier.show_expanded

Modifier.use_pin_to_last

Modifier.is_override_data

Modifier.use_apply_on_spline

Modifier.execution_time

Modifier.persistent_uid

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Modifier.bl_rna_get_subclass

Modifier.bl_rna_get_subclass_py

---

## FollowPathConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FollowPathConstraint.html

**Contents:**
- FollowPathConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Lock motion to the target path

Axis that points forward along the path

enum in ['FORWARD_X', 'FORWARD_Y', 'FORWARD_Z', 'TRACK_NEGATIVE_X', 'TRACK_NEGATIVE_Y', 'TRACK_NEGATIVE_Z'], default 'FORWARD_X'

Offset from the position corresponding to the time frame

float in [-1.04857e+06, 1.04857e+06], default 0.0

Percentage value defining target position along length of curve

float in [-inf, inf], default 0.0

Axis that points upward

enum in ['UP_X', 'UP_Y', 'UP_Z'], default 'UP_X'

Object will follow the heading and banking of the curve

boolean, default False

Object is scaled by the curve radius

boolean, default False

Object will stay locked to a single point somewhere along the length of the curve regardless of time

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## FollowTrackConstraint(Constraint)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FollowTrackConstraint.html

**Contents:**
- FollowTrackConstraint(Constraint)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Constraint

Lock motion to the target motion track

Camera to which motion is parented (if empty active scene camera is used)

Movie Clip to get tracking data from

Object used to define depth in camera space by projecting onto surface of this object

How the footage fits in the camera frame

enum in ['STRETCH', 'FIT', 'CROP'], default 'STRETCH'

Movie tracking object to follow (if empty, camera object is used)

string, default “”, (never None)

Movie tracking track to follow

string, default “”, (never None)

Use 3D position of track to parent to

boolean, default False

Use active clip defined in scene

boolean, default False

Parent to undistorted position of 2D track

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Constraint.is_override_data

Constraint.owner_space

Constraint.target_space

Constraint.space_object

Constraint.space_subtarget

Constraint.show_expanded

Constraint.error_location

Constraint.error_rotation

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Constraint.bl_rna_get_subclass

Constraint.bl_rna_get_subclass_py

---

## ForeachGeometryElementGenerationItem(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ForeachGeometryElementGenerationItem.html

**Contents:**
- ForeachGeometryElementGenerationItem(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color of the corresponding socket type in the node editor

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0), (readonly)

Domain that the field is evaluated on

enum in Attribute Domain Items, default 'POINT'

string, default “”, (never None)

enum in Node Socket Data Type Items, default 'FLOAT'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

GeometryNodeForeachGeometryElementOutput.generation_items

NodeGeometryForeachGeometryElementGenerationItems.new

NodeGeometryForeachGeometryElementGenerationItems.remove

---

## ForeachGeometryElementZoneViewerPathElem(ViewerPathElem)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ForeachGeometryElementZoneViewerPathElem.html

**Contents:**
- ForeachGeometryElementZoneViewerPathElem(ViewerPathElem)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, ViewerPathElem

int in [-inf, inf], default 0

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ViewerPathElem.ui_name

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ViewerPathElem.bl_rna_get_subclass

ViewerPathElem.bl_rna_get_subclass_py

---

## ForeachGeometryElementMainItem(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ForeachGeometryElementMainItem.html

**Contents:**
- ForeachGeometryElementMainItem(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color of the corresponding socket type in the node editor

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0), (readonly)

string, default “”, (never None)

enum in Node Socket Data Type Items, default 'FLOAT'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

GeometryNodeForeachGeometryElementOutput.main_items

NodeGeometryForeachGeometryElementMainItems.new

NodeGeometryForeachGeometryElementMainItems.remove

---

## ForeachGeometryElementInputItem(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.ForeachGeometryElementInputItem.html

**Contents:**
- ForeachGeometryElementInputItem(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Color of the corresponding socket type in the node editor

float array of 4 items in [0, inf], default (0.0, 0.0, 0.0, 0.0), (readonly)

string, default “”, (never None)

enum in Node Socket Data Type Items, default 'FLOAT'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

GeometryNodeForeachGeometryElementOutput.input_items

NodeGeometryForeachGeometryElementInputItems.new

NodeGeometryForeachGeometryElementInputItems.remove

---

## FreestyleLineSet(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FreestyleLineSet.html

**Contents:**
- FreestyleLineSet(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Line set for associating lines and style parameters

A collection of objects based on which feature edges are selected

Specify either inclusion or exclusion of feature edges belonging to a collection of objects

INCLUSIVE Inclusive – Select feature edges belonging to some object in the group.

EXCLUSIVE Exclusive – Select feature edges not belonging to any object in the group.

enum in ['INCLUSIVE', 'EXCLUSIVE'], default 'INCLUSIVE'

Specify a logical combination of selection conditions on feature edge types

OR Logical OR – Select feature edges satisfying at least one of edge type conditions.

AND Logical AND – Select feature edges satisfying all edge type conditions.

enum in ['OR', 'AND'], default 'OR'

Specify either inclusion or exclusion of feature edges selected by edge types

INCLUSIVE Inclusive – Select feature edges satisfying the given edge type conditions.

EXCLUSIVE Exclusive – Select feature edges not satisfying the given edge type conditions.

enum in ['INCLUSIVE', 'EXCLUSIVE'], default 'INCLUSIVE'

boolean, default False

boolean, default False

boolean, default False

boolean, default False

Exclude external contours

boolean, default False

Exclude edges at material boundaries

boolean, default False

Exclude ridges and valleys

boolean, default False

Exclude silhouette edges

boolean, default False

Exclude suggestive contours

boolean, default False

Specify a feature edge selection condition based on face marks

ONE One Face – Select a feature edge if either of its adjacent faces is marked.

BOTH Both Faces – Select a feature edge if both of its adjacent faces are marked.

enum in ['ONE', 'BOTH'], default 'ONE'

Specify either inclusion or exclusion of feature edges selected by face marks

INCLUSIVE Inclusive – Select feature edges satisfying the given face mark conditions.

EXCLUSIVE Exclusive – Select feature edges not satisfying the given face mark conditions.

enum in ['INCLUSIVE', 'EXCLUSIVE'], default 'INCLUSIVE'

FreestyleLineStyle, (never None)

string, default “”, (never None)

Last QI value of the QI range

int in [0, inf], default 0

First QI value of the QI range

int in [0, inf], default 0

Select border edges (open mesh edges)

boolean, default False

Select feature edges based on a collection of objects

boolean, default False

Select feature edges based on edge types

boolean, default False

Select feature edges by face marks

boolean, default False

Select feature edges by image border (less memory consumption)

boolean, default False

Select feature edges based on visibility

boolean, default False

Select contours (outer silhouettes of each object)

boolean, default False

Select crease edges (those between two faces making an angle smaller than the Crease Angle)

boolean, default False

Select edge marks (edges annotated by Freestyle edge marks)

boolean, default False

Select external contours (outer silhouettes of occluding and occluded objects)

boolean, default False

Select edges at material boundaries

boolean, default False

Select ridges and valleys (boundary lines between convex and concave areas of surface)

boolean, default False

Select silhouettes (edges at the boundary of visible and hidden faces)

boolean, default False

Select suggestive contours (almost silhouette/contour edges)

boolean, default False

Enable or disable this line set during stroke rendering

boolean, default False

Determine how to use visibility for feature edge selection

VISIBLE Visible – Select visible feature edges.

HIDDEN Hidden – Select hidden feature edges.

RANGE Quantitative Invisibility – Select feature edges within a range of quantitative invisibility (QI) values.

enum in ['VISIBLE', 'HIDDEN', 'RANGE'], default 'VISIBLE'

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FreestyleSettings.linesets

---

## FreestyleLineStyle(ID)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FreestyleLineStyle.html

**Contents:**
- FreestyleLineStyle(ID)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base classes — bpy_struct, ID

Freestyle line style, reusable by multiple line sets

Active texture slot being displayed

Index of active texture slot

int in [0, 17], default 0

Base alpha transparency, possibly modified by alpha transparency modifiers

float in [0, 1], default 1.0

List of alpha transparency modifiers

LineStyleAlphaModifiers bpy_prop_collection of LineStyleAlphaModifier, (readonly)

Maximum 2D angle for splitting chains

float in [0, 3.14159], default 0.0

Minimum 2D angle for splitting chains

float in [0, 3.14159], default 0.0

Animation data for this data-block

Select the shape of both ends of strokes

BUTT Butt – Butt cap (flat).

ROUND Round – Round cap (half-circle).

SQUARE Square – Square cap (flat and extended).

enum in ['BUTT', 'ROUND', 'SQUARE'], default 'BUTT'

Chain count for the selection of first N chains

int in [0, inf], default 10

Select the way how feature edges are jointed to form chains

PLAIN Plain – Plain chaining.

SKETCHY Sketchy – Sketchy chaining with a multiple touch.

enum in ['PLAIN', 'SKETCHY'], default 'PLAIN'

Base line color, possibly modified by line color modifiers

mathutils.Color of 3 items in [0, inf], default (0.0, 0.0, 0.0)

List of line color modifiers

LineStyleColorModifiers bpy_prop_collection of LineStyleColorModifier, (readonly)

Length of the 1st dash for dashed lines

int in [0, 65535], default 0

Length of the 2nd dash for dashed lines

int in [0, 65535], default 0

Length of the 3rd dash for dashed lines

int in [0, 65535], default 0

Length of the 1st gap for dashed lines

int in [0, 65535], default 0

Length of the 2nd gap for dashed lines

int in [0, 65535], default 0

Length of the 3rd gap for dashed lines

int in [0, 65535], default 0

List of stroke geometry modifiers

LineStyleGeometryModifiers bpy_prop_collection of LineStyleGeometryModifier, (readonly)

Select the way how the sort key is computed for each chain

MEAN Mean – The value computed for the chain is the mean of the values obtained for chain vertices.

MIN Min – The value computed for the chain is the minimum of the values obtained for chain vertices.

MAX Max – The value computed for the chain is the maximum of the values obtained for chain vertices.

FIRST First – The value computed for the chain is the value obtained for the first chain vertex.

LAST Last – The value computed for the chain is the value obtained for the last chain vertex.

enum in ['MEAN', 'MIN', 'MAX', 'FIRST', 'LAST'], default 'MEAN'

Maximum curvilinear 2D length for the selection of chains

float in [0, 10000], default 10000.0

Minimum curvilinear 2D length for the selection of chains

float in [0, 10000], default 0.0

If true, chains of feature edges are split at material boundaries

boolean, default False

Node tree for node-based shaders

Select the property panel to be shown

STROKES Strokes – Show the panel for stroke construction.

COLOR Color – Show the panel for line color options.

ALPHA Alpha – Show the panel for alpha transparency options.

THICKNESS Thickness – Show the panel for line thickness options.

GEOMETRY Geometry – Show the panel for stroke geometry options.

TEXTURE Texture – Show the panel for stroke texture options.

enum in ['STROKES', 'COLOR', 'ALPHA', 'THICKNESS', 'GEOMETRY', 'TEXTURE'], default 'STROKES'

Number of rounds in a sketchy multiple touch

int in [1, 1000], default 3

Select the sort key to determine the stacking order of chains

DISTANCE_FROM_CAMERA Distance from Camera – Sort by distance from camera (closer lines lie on top of further lines).

2D_LENGTH 2D Length – Sort by curvilinear 2D length (longer lines lie on top of shorter lines).

PROJECTED_X Projected X – Sort by the projected X value in the image coordinate system.

PROJECTED_Y Projected Y – Sort by the projected Y value in the image coordinate system.

enum in ['DISTANCE_FROM_CAMERA', '2D_LENGTH', 'PROJECTED_X', 'PROJECTED_Y'], default 'DISTANCE_FROM_CAMERA'

Select the sort order

DEFAULT Default – Default order of the sort key.

REVERSE Reverse – Reverse order.

enum in ['DEFAULT', 'REVERSE'], default 'DEFAULT'

Length of the 1st dash for splitting

int in [0, 65535], default 0

Length of the 2nd dash for splitting

int in [0, 65535], default 0

Length of the 3rd dash for splitting

int in [0, 65535], default 0

Length of the 1st gap for splitting

int in [0, 65535], default 0

Length of the 2nd gap for splitting

int in [0, 65535], default 0

Length of the 3rd gap for splitting

int in [0, 65535], default 0

Curvilinear 2D length for chain splitting

float in [0, 10000], default 100.0

Texture slots defining the mapping and influence of textures

LineStyleTextureSlots bpy_prop_collection of LineStyleTextureSlot, (readonly)

Spacing for textures along stroke length

float in [0.01, 100], default 1.0

Base line thickness, possibly modified by line thickness modifiers

float in [0, 10000], default 3.0

List of line thickness modifiers

LineStyleThicknessModifiers bpy_prop_collection of LineStyleThicknessModifier, (readonly)

Thickness position of silhouettes and border edges (applicable when plain chaining is used with the Same Object option)

CENTER Center – Silhouettes and border edges are centered along stroke geometry.

INSIDE Inside – Silhouettes and border edges are drawn inside of stroke geometry.

OUTSIDE Outside – Silhouettes and border edges are drawn outside of stroke geometry.

RELATIVE Relative – Silhouettes and border edges are shifted by a user-defined ratio.

enum in ['CENTER', 'INSIDE', 'OUTSIDE', 'RELATIVE'], default 'CENTER'

A number between 0 (inside) and 1 (outside) specifying the relative position of stroke thickness

float in [0, 1], default 0.5

Split chains at points with angles larger than the maximum 2D angle

boolean, default False

Split chains at points with angles smaller than the minimum 2D angle

boolean, default False

Enable the selection of first N chains

boolean, default False

Enable chaining of feature edges

boolean, default True

Enable or disable dashed line

boolean, default False

Enable the selection of chains by a maximum 2D length

boolean, default False

Enable the selection of chains by a minimum 2D length

boolean, default False

Use shader nodes for the line style

boolean, default False

If true, only feature edges of the same object are joined

boolean, default True

Arrange the stacking order of strokes

boolean, default False

Enable chain splitting by curvilinear 2D length

boolean, default False

Enable chain splitting by dashed line patterns

boolean, default False

Enable or disable textured strokes

boolean, default True

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

ID.is_library_indirect

ID.library_weak_reference

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ID.bl_system_properties_get

ID.asset_generate_preview

ID.override_hierarchy_create

ID.animation_data_create

ID.animation_data_clear

ID.bl_rna_get_subclass

ID.bl_rna_get_subclass_py

bpy.context.line_style

BlendDataLineStyles.new

BlendDataLineStyles.remove

FreestyleLineSet.linestyle

---

## FreestyleModuleSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FreestyleModuleSettings.html

**Contents:**
- FreestyleModuleSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Style module configuration for specifying a style module

Python script to define a style module

Enable or disable this style module during stroke rendering

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FreestyleModules.remove

FreestyleSettings.modules

---

## FreestyleModules(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FreestyleModules.html

**Contents:**
- FreestyleModules(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

A list of style modules (to be applied from top to bottom)

Add a style module to scene render layer Freestyle settings

Newly created style module

FreestyleModuleSettings

Remove a style module from scene render layer Freestyle settings

module (FreestyleModuleSettings, (never None)) – Style module to remove

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

FreestyleSettings.modules

---

## FreestyleSettings(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FreestyleSettings.html

**Contents:**
- FreestyleSettings(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

Freestyle settings for a ViewLayer data-block

Renders Freestyle output to a separate pass instead of overlaying it on the Combined pass

boolean, default False

Angular threshold for detecting crease edges

float in [0, 3.14159], default 0.0

Kr derivative epsilon for computing suggestive contours

float in [-1000, 1000], default 0.0

Linesets bpy_prop_collection of FreestyleLineSet, (readonly)

Select the Freestyle control mode

SCRIPT Python Scripting – Advanced mode for using style modules written in Python.

EDITOR Parameter Editor – Basic mode for interactive style parameter editing.

enum in ['SCRIPT', 'EDITOR'], default 'SCRIPT'

A list of style modules (to be applied from top to bottom)

FreestyleModules bpy_prop_collection of FreestyleModuleSettings, (readonly)

Sphere radius for computing curvatures

float in [0, 1000], default 1.0

If enabled, out-of-view edges are ignored

boolean, default False

Enable material boundaries

boolean, default False

Enable ridges and valleys

boolean, default False

Take face smoothness into account in view map calculation

boolean, default False

Enable suggestive contours

boolean, default False

Keep the computed view map and avoid recalculating it if mesh geometry is unchanged

boolean, default False

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

ViewLayer.freestyle_settings

---

## Function(bpy_struct)¶

**URL:** https://docs.blender.org/api/current/bpy.types.Function.html

**Contents:**
- Function(bpy_struct)¶
- Inherited Properties¶
- Inherited Functions¶
- References¶

base class — bpy_struct

RNA function definition

Description of the Function’s purpose

string, default “”, (readonly, never None)

Unique name used in the code and scripting

string, default “”, (readonly, never None)

Function is registered as callback as part of type registration

boolean, default False, (readonly)

Function is optionally registered as callback part of type registration

boolean, default False, (readonly)

Parameters for the function

bpy_prop_collection of Property, (readonly)

Function does not pass itself as an argument (becomes a static method in Python)

boolean, default False, (readonly)

Function passes itself type as an argument (becomes a class method in Python if use_self is false)

boolean, default False, (readonly)

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

---

## FunctionNodeAlignEulerToVector(FunctionNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNodeAlignEulerToVector.html

**Contents:**
- FunctionNodeAlignEulerToVector(FunctionNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, FunctionNode

Orient an Euler rotation along the given direction

Axis to align to the vector

X X – Align the X axis with the vector.

Y Y – Align the Y axis with the vector.

Z Z – Align the Z axis with the vector.

enum in ['X', 'Y', 'Z'], default 'X'

Axis to rotate around

AUTO Auto – Automatically detect the best rotation axis to rotate towards the vector.

X X – Rotate around the local X axis.

Y Y – Rotate around the local Y axis.

Z Z – Rotate around the local Z axis.

enum in ['AUTO', 'X', 'Y', 'Z'], default 'AUTO'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

FunctionNode.bl_rna_get_subclass

FunctionNode.bl_rna_get_subclass_py

---

## FunctionNode(NodeInternal)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNode.html

**Contents:**
- FunctionNode(NodeInternal)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal

subclasses — FunctionNodeAlignEulerToVector, FunctionNodeAlignRotationToVector, FunctionNodeAxesToRotation, FunctionNodeAxisAngleToRotation, FunctionNodeBitMath, FunctionNodeBooleanMath, FunctionNodeCombineColor, FunctionNodeCombineMatrix, FunctionNodeCombineTransform, FunctionNodeCompare, FunctionNodeEulerToRotation, FunctionNodeFindInString, FunctionNodeFloatToInt, FunctionNodeFormatString, FunctionNodeHashValue, FunctionNodeInputBool, FunctionNodeInputColor, FunctionNodeInputInt, FunctionNodeInputRotation, FunctionNodeInputSpecialCharacters, FunctionNodeInputString, FunctionNodeInputVector, FunctionNodeIntegerMath, FunctionNodeInvertMatrix, FunctionNodeInvertRotation, FunctionNodeMatchString, FunctionNodeMatrixDeterminant, FunctionNodeMatrixMultiply, FunctionNodeProjectPoint, FunctionNodeQuaternionToRotation, FunctionNodeRandomValue, FunctionNodeReplaceString, FunctionNodeRotateEuler, FunctionNodeRotateRotation, FunctionNodeRotateVector, FunctionNodeRotationToAxisAngle, FunctionNodeRotationToEuler, FunctionNodeRotationToQuaternion, FunctionNodeSeparateColor, FunctionNodeSeparateMatrix, FunctionNodeSeparateTransform, FunctionNodeSliceString, FunctionNodeStringLength, FunctionNodeStringToValue, FunctionNodeTransformDirection, FunctionNodeTransformPoint, FunctionNodeTransposeMatrix, FunctionNodeValueToString

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

---

## FunctionNodeAlignRotationToVector(FunctionNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNodeAlignRotationToVector.html

**Contents:**
- FunctionNodeAlignRotationToVector(FunctionNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, FunctionNode

Orient a rotation along the given direction

Axis to align to the vector

X X – Align the X axis with the vector.

Y Y – Align the Y axis with the vector.

Z Z – Align the Z axis with the vector.

enum in ['X', 'Y', 'Z'], default 'X'

Axis to rotate around

AUTO Auto – Automatically detect the best rotation axis to rotate towards the vector.

X X – Rotate around the local X axis.

Y Y – Rotate around the local Y axis.

Z Z – Rotate around the local Z axis.

enum in ['AUTO', 'X', 'Y', 'Z'], default 'AUTO'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

FunctionNode.bl_rna_get_subclass

FunctionNode.bl_rna_get_subclass_py

---

## FunctionNodeAxesToRotation(FunctionNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNodeAxesToRotation.html

**Contents:**
- FunctionNodeAxesToRotation(FunctionNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, FunctionNode

Create a rotation from a primary and (ideally orthogonal) secondary axis

Axis that is aligned exactly to the provided primary direction

enum in ['X', 'Y', 'Z'], default 'X'

Axis that is aligned as well as possible given the alignment of the primary axis

enum in ['X', 'Y', 'Z'], default 'X'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

FunctionNode.bl_rna_get_subclass

FunctionNode.bl_rna_get_subclass_py

---

## FunctionNodeAxisAngleToRotation(FunctionNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNodeAxisAngleToRotation.html

**Contents:**
- FunctionNodeAxisAngleToRotation(FunctionNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, FunctionNode

Build a rotation from an axis and a rotation around that axis

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

FunctionNode.bl_rna_get_subclass

FunctionNode.bl_rna_get_subclass_py

---

## FunctionNodeBitMath(FunctionNode)¶

**URL:** https://docs.blender.org/api/current/bpy.types.FunctionNodeBitMath.html

**Contents:**
- FunctionNodeBitMath(FunctionNode)¶
- Inherited Properties¶
- Inherited Functions¶

base classes — bpy_struct, Node, NodeInternal, FunctionNode

Perform bitwise operations on 32-bit integers

AND And – Returns a value where the bits of A and B are both set.

OR Or – Returns a value where the bits of either A or B are set.

XOR Exclusive Or – Returns a value where only one bit from A and B is set.

NOT Not – Returns the opposite bit value of A, in decimal it is equivalent of A = -A - 1.

SHIFT Shift – Shifts the bit values of A by the specified Shift amount. Positive values shift left, negative values shift right..

ROTATE Rotate – Rotates the bit values of A by the specified Shift amount. Positive values rotate left, negative values rotate right..

enum in ['AND', 'OR', 'XOR', 'NOT', 'SHIFT', 'ROTATE'], default 'AND'

True if a registered node type

Input socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

Output socket template

index (int in [0, inf]) – Index

NodeInternalSocketTemplate

id (str) – The RNA type identifier.

The RNA type or default when not found.

bpy.types.Struct subclass

id (str) – The RNA type identifier.

The class or default when not found.

Node.location_absolute

Node.warning_propagation

Node.use_custom_color

Node.bl_width_default

Node.bl_height_default

bpy_struct.as_pointer

bpy_struct.driver_add

bpy_struct.driver_remove

bpy_struct.id_properties_clear

bpy_struct.id_properties_ensure

bpy_struct.id_properties_ui

bpy_struct.is_property_hidden

bpy_struct.is_property_overridable_library

bpy_struct.is_property_readonly

bpy_struct.is_property_set

bpy_struct.keyframe_delete

bpy_struct.keyframe_insert

bpy_struct.path_from_id

bpy_struct.path_from_module

bpy_struct.path_resolve

bpy_struct.property_overridable_library_set

bpy_struct.property_unset

bpy_struct.rna_ancestors

bpy_struct.type_recast

Node.bl_system_properties_get

Node.socket_value_update

Node.is_registered_node_type

Node.draw_buttons_ext

Node.debug_zone_body_lazy_function_graph

Node.debug_zone_lazy_function_graph

Node.bl_rna_get_subclass

Node.bl_rna_get_subclass_py

NodeInternal.poll_instance

NodeInternal.draw_buttons

NodeInternal.draw_buttons_ext

NodeInternal.bl_rna_get_subclass

NodeInternal.bl_rna_get_subclass_py

FunctionNode.bl_rna_get_subclass

FunctionNode.bl_rna_get_subclass_py

---
