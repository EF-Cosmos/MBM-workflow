import bpy
import importlib

# 依赖管理：必须首先加载
from .codes import dependency_manager
importlib.reload(dependency_manager)

# install.py 在 Blender 5.0+ 中不再需要
# Blender 会自动处理 blender_manifest.toml 中的 wheels

# 加载国际化模块（必须在其他模块之前）
from . import i18n
importlib.reload(i18n)

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

from .codes import block_palette
importlib.reload(block_palette)

from .codes.functions import paint
importlib.reload(paint)

from . import ui
importlib.reload(ui)

from .codes import block_palette_panel
importlib.reload(block_palette_panel)

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
	block_palette,
	paint,
	ui,
	block_palette_panel,
	i18n  # 翻译模块最后注册
)


_modules_loaded = False

def register():
	global _modules_loaded
	# 注册依赖管理器（用于显示弹窗）
	dependency_manager.register()

	# 检查依赖：amulet 等缺失时降级运行（UI/编辑/笔刷可用，导入/导出禁用），
	# 不再整体 return——各模块已对 amulet 缺失做条件化处理。
	missing = dependency_manager.DependencyManager.check_dependencies()
	if missing:
		print(f"[MBM] 依赖缺失，导入/导出将禁用: {[m[0] for m in missing]}")

	# 检查可选依赖并显示警告
	optional_missing = dependency_manager.DependencyManager.check_optional_dependencies()
	if optional_missing:
		dependency_manager.DependencyManager.show_optional_warning(optional_missing)

	# 注册所有模块（依赖缺失的子功能在各自 UI/操作符中降级）
	for mod in module_list:
		try:
			mod.register()
		except Exception as e:
			print(f"[MBM] 注册模块失败 {mod.__name__}: {e}")
	
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
