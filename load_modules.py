import bpy
import importlib

# 依赖管理：必须首先加载
from .codes import dependency_manager
importlib.reload(dependency_manager)

# install.py 在 Blender 5.0+ 中不再需要
# Blender 会自动处理 blender_manifest.toml 中的 wheels

# 加载其他模块
from .codes import property
importlib.reload(property)

from .codes import color_dict
importlib.reload(color_dict)

from .codes.functions import sway_animation
importlib.reload(sway_animation)

from .codes import importfile
importlib.reload(importfile)

from .codes import exportfile
importlib.reload(exportfile)

from .codes import create_world
importlib.reload(create_world)

from .codes.functions import search_file
importlib.reload(search_file)

from .codes.functions import mesh_to_mc
importlib.reload(mesh_to_mc)

from .codes.functions import surface_optimization
importlib.reload(surface_optimization)

from .codes.functions import brush
importlib.reload(brush)

from .codes.functions import paint
importlib.reload(paint)

from . import ui
importlib.reload(ui)

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
	brush,
	paint,
	ui
)


_modules_loaded = False

def register():
	global _modules_loaded
	# 注册依赖管理器（用于显示弹窗）
	dependency_manager.register()

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
	
	_modules_loaded = True


def unregister():
	global _modules_loaded
	if _modules_loaded:
		for mod in reversed(module_list):
			try:
				mod.unregister()
			except Exception:
				pass
		_modules_loaded = False
	
	try:
		dependency_manager.unregister()
	except Exception:
		pass
