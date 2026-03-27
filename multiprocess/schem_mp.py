import bpy
import addon_utils
import json
import os

loaded_default, loaded_state = addon_utils.check("MBM_Workflow")
if not loaded_state:
    addon_utils.enable("MBM_Workflow")

VAR_CACHE_PATH = os.path.join(
    bpy.utils.script_path_user(), "addons", "MBM_Workflow", "schemcache", "var.json"
)
with open(VAR_CACHE_PATH, 'r') as f:
    data = json.load(f)

chunk_index = int(os.environ.get("MBM_CHUNK_INDEX", 0))
bpy.ops.mbm.import_schem_mp(filepath=data["schempath"], chunk_index=chunk_index)
