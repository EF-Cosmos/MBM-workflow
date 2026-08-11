import bpy
import addon_utils
import json
import os

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

VAR_CACHE_PATH = os.environ.get("MBM_VAR_CACHE_PATH") or os.path.join(
    bpy.utils.script_path_user(), "addons", "MBM_workflow", "schemcache", "var.json"
)
with open(VAR_CACHE_PATH, 'r') as f:
    data = json.load(f)

bpy.ops.mbm.import_schem_liquid()
