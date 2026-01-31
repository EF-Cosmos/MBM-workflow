import bpy
import addon_utils
import pickle
import socket
import time

loaded_default, loaded_state = addon_utils.check("MBM_Workflow")
if not loaded_state:
    addon_utils.enable("MBM_Workflow")

VarCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/var.pkl"
with open(VarCachePath, 'rb') as file:
    chunks,mp_chunks,schempath,interval,processnum = pickle.load(file)
bpy.ops.mbm.import_schem_liquid(filepath=schempath)