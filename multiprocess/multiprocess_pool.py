import bpy
import addon_utils
import pickle
import socket
import time

loaded_default, loaded_state = addon_utils.check("MBM_Workflow")
if not loaded_state:
    addon_utils.enable("MBM_Workflow")
loaded_default, loaded_state = addon_utils.check("blender_command_port")
if not loaded_state:
    addon_utils.enable("Blender_Command_Port")
bpy.ops.mbm.multiprocess_pool()