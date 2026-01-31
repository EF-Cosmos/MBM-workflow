import bpy
import addon_utils
import pickle
import socket
import time
import threading
import os
from collections import defaultdict

loaded_default, loaded_state = addon_utils.check("MBM_Workflow")
if not loaded_state:
    addon_utils.enable("MBM_Workflow")
VarCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/var.pkl"
with open(VarCachePath, 'rb') as file:
    schempath,chunks,name,x_list,processnum = pickle.load(file)
bpy.ops.mbm.import_schem_mp(filepath=schempath)
