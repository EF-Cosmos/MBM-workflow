import logging
logging.getLogger("amulet").setLevel(logging.FATAL)
logging.getLogger("PyMCTranslate").setLevel(logging.FATAL)
import importlib
# 检查是否在 Blender 环境内执行
try:
    import bpy
except ImportError:
    raise ImportError("This script must be run within Blender.")

import sys
import os

# 将当前目录加入 sys.path，以便 amulet 等库能找到内置的 mutf8 等模块
addon_dir = os.path.dirname(__file__)
if addon_dir not in sys.path:
    # 放置在末尾以防干扰核心库
    sys.path.append(addon_dir)

bl_info={
    "name":"MBM_workflow",
    "author":"EF_Cosmos",
    "version":(1, 0),
    "blender":(5, 0, 0),
    "location":"View3d > Tool",
    "warning":"如果有任何问题请联系我~我的GitHub:EF-Cosmos",
    "category":"MBM_workflow"
}

from . import load_modules
importlib.reload(load_modules)


def register():
	load_modules.register()


def unregister():
	load_modules.unregister()
	# 清理 sys.path
	addon_dir = os.path.dirname(__file__)
	if addon_dir in sys.path:
		sys.path.remove(addon_dir)
	

if __name__ == "__main__":
	register()

