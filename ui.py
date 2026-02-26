import bpy

from .ui_dialogs import ColorToBlockPanel, SchemImportPanel, SwitchBlocks
from .ui_lists import ColorToBlockList, ModList, ResourcepackList, SwitchBlockList
from .ui_panels import (
    Ability,
    BlockPanel,
    CreateLevel,
    EditPanel,
    ExportPanel,
    GameRules,
    ImportPanel,
    MainPanel,
    ModPanel,
    MoreLevelSettings,
    ResourcepacksPanel,
)

classes = [
    SchemImportPanel,
    ColorToBlockPanel,
    SwitchBlocks,
    ResourcepackList,
    ColorToBlockList,
    SwitchBlockList,
    ModList,
    MainPanel,
    BlockPanel,
    ImportPanel,
    ExportPanel,
    EditPanel,
    CreateLevel,
    ModPanel,
    ResourcepacksPanel,
    MoreLevelSettings,
    GameRules,
    Ability,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

