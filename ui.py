import bpy

from .ui_dialogs import ColorToBlockPanel, SchemImportPanel, SwitchBlocks
from .ui_lists import MBM_UL_color_to_block_list, MBM_UL_mod_list, MBM_UL_resourcepack_list, MBM_UL_switch_block_list
from .ui_panels import (
    MBM_PT_ability,
    MBM_PT_block_panel,
    MBM_PT_create_level,
    MBM_PT_edit_panel,
    MBM_PT_export_panel,
    MBM_PT_game_rules,
    MBM_PT_import_panel,
    MBM_PT_main_panel,
    MBM_PT_mod,
    MBM_PT_more_level_settings,
    MBM_PT_resourcepacks,
)

classes = [
    SchemImportPanel,
    ColorToBlockPanel,
    SwitchBlocks,
    MBM_UL_resourcepack_list,
    MBM_UL_color_to_block_list,
    MBM_UL_switch_block_list,
    MBM_UL_mod_list,
    MBM_PT_main_panel,
    MBM_PT_block_panel,
    MBM_PT_import_panel,
    MBM_PT_export_panel,
    MBM_PT_edit_panel,
    MBM_PT_create_level,
    MBM_PT_mod,
    MBM_PT_resourcepacks,
    MBM_PT_more_level_settings,
    MBM_PT_game_rules,
    MBM_PT_ability,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

