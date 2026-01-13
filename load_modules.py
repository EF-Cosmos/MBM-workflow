import bpy
import importlib

# 依赖管理：必须首先加载
if "dependency_manager" in locals():
	importlib.reload(dependency_manager)
else:
	from .codes import dependency_manager

# install.py 在 Blender 5.0+ 中不再需要
# Blender 会自动处理 blender_manifest.toml 中的 wheels
# if "install" in locals():
# 	importlib.reload(install)
# else:
# 	from . import install

if "property" in locals():
	importlib.reload(property)
else:
	from .codes import property
if "color_dict" in locals():
	importlib.reload(color_dict)
else:
	from .codes import color_dict
if "sway_animation" in locals():
	importlib.reload(sway_animation)
else:
	from .codes.functions import sway_animation
	
if "importfile" in locals():
	importlib.reload(importfile)
else:
	from .codes import importfile

if "exportfile" in locals():
	importlib.reload(exportfile)
else:
	from .codes import exportfile

if "create_world" in locals():
	importlib.reload(create_world)
else:
	from .codes import create_world

if "search_file" in locals():
	importlib.reload(search_file)
else:
	from .codes.functions import search_file

if "mesh_to_mc" in locals():
	importlib.reload(mesh_to_mc)
else:
	from .codes.functions import mesh_to_mc

if "surface_optimization" in locals():
	importlib.reload(surface_optimization)
else:
	from .codes.functions import surface_optimization

if "ui" in locals():
	importlib.reload(ui)
else:
	from . import ui
	
module_list = (
	property,
	color_dict,
	sway_animation,
	surface_optimization,
	search_file,
	importfile,
	exportfile,
	create_world,
	mesh_to_mc,
	ui
)


def register():
	# 首先检查依赖
	missing = dependency_manager.DependencyManager.check_dependencies()
	if missing:
		dependency_manager.DependencyManager.show_dependency_error(missing)
		return  # 不继续注册，但 Blender 不会崩溃

	# 检查可选依赖并显示警告
	optional_missing = dependency_manager.DependencyManager.check_optional_dependencies()
	if optional_missing:
		dependency_manager.DependencyManager.show_optional_warning(optional_missing)

	# 所有依赖可用，继续注册模块
	for mod in module_list:
		mod.register()



def unregister():
	for mod in reversed(module_list):
		mod.unregister()
