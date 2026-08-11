import bpy
import addon_utils
import json
import os

# 启用插件：5.x extensions 下 addon 名可能是 MBM_workflow 或 bl_ext.<repo>.MBM_workflow
_ADDON_NAME_CANDIDATES = [
    "MBM_workflow",
    "bl_ext.user_default.MBM_workflow",
    "bl_ext.blender_org.MBM_workflow",
]


def _ensure_addon():
    for name in _ADDON_NAME_CANDIDATES:
        try:
            if addon_utils.check(name)[1]:
                return True
        except Exception:
            pass
    for name in _ADDON_NAME_CANDIDATES:
        try:
            addon_utils.enable(name)
            return True
        except Exception:
            pass
    return False


_ensure_addon()

# var.json 路径：优先用主进程通过环境变量传入的绝对路径（5.x extensions 安装路径已变），
# 回退到旧 script_path_user()/addons/ 推断（legacy 安装方式）。
VAR_CACHE_PATH = os.environ.get("MBM_VAR_CACHE_PATH") or os.path.join(
    bpy.utils.script_path_user(), "addons", "MBM_workflow", "schemcache", "var.json"
)
with open(VAR_CACHE_PATH, 'r') as f:
    data = json.load(f)

chunk_index = int(os.environ.get("MBM_CHUNK_INDEX", 0))
bpy.ops.mbm.import_schem_mp(filepath=data["schempath"], chunk_index=chunk_index)
