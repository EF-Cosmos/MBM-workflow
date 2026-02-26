import bpy
import os
import zipfile
import threading
import functools
import shutil
try:
    import tomllib as toml
except ImportError:
    import toml

import json
import random
import importlib

from .. import config
from .block_map_store import load_block_map

# 翻译支持
from bpy.app.translations import pgettext_iface as _
from ..i18n.translations import property_name, enum_item, operator_label


def get_mc_version(context):
    """
    从 Blender 场景属性获取 Minecraft 版本配置
    返回: (platform, version_tuple)
    例如: ("java", (1, 21, 11))
    """
    scene = context.scene
    platform = scene.mc_platform
    version_tuple = (
        scene.mc_version_major,
        scene.mc_version_minor,
        scene.mc_version_patch
    )
    return platform, version_tuple


def switch_block_update(self, context):
    scene = context.scene
    my_properties = scene.my_properties
    switch_block_list = my_properties.switch_block_list

    # 假设你已经选择了包含几何节点组的对象
    obj = bpy.context.active_object
    # 获取几何节点树
    geometry_nodes = obj.modifiers.get("模型转换")
    node_group = geometry_nodes.node_group
    
    id_to_target = {str(blockid.id): blockid.target_id for blockid in switch_block_list}

    for node in node_group.nodes:
        if node.name == '改变id组':
            # 查找匹配的节点
            for sub_node in node.node_tree.nodes:
                if sub_node.name in id_to_target:
                    # 获取第一个输入口的值
                    input_socket = sub_node.inputs[1]
                    input_value = input_socket.default_value
                    target_value = id_to_target[sub_node.name]
                    
                    # 检查 input_value 是否与 target_value 不同
                    if input_value != target_value:
                        # 修改第一个输入口的值为 target_value
                        input_socket.default_value = target_value

                    
    return



def get_block_items(self, context):
    items = []
    try:
        text_data = bpy.data.texts.get("Blocks.py")
        if text_data:
            block_map = load_block_map(text_data)
            for name, id_val in block_map.items():
                items.append((str(id_val), name, f"ID: {id_val}"))
            items.sort(key=lambda x: x[1])
    except Exception:
        pass
        
    if not items:
        items = [("0", "None", "No blocks found")]
    return items

def update_target_id_from_enum(self, context):
    try:
        if self.target_block_enum:
            self.target_id = int(self.target_block_enum)
    except ValueError:
        pass

class ModInfo(bpy.types.PropertyGroup):
    icon: bpy.props.StringProperty(name=property_name("图标")) # type: ignore
    name: bpy.props.StringProperty(name=property_name("名称")) # type: ignore
    description: bpy.props.StringProperty(name=property_name("描述")) # type: ignore

class BlockInfo(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name=property_name("名称")) # type: ignore
    filepath: bpy.props.StringProperty(name=property_name("文件位置")) # type: ignore
    type: bpy.props.IntProperty(name=property_name("种类"), min=-1, max=2) # type: ignore
    color: bpy.props.FloatVectorProperty(
        name=property_name("颜色"),
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0)
    )  # type: ignore

class SwitchBlockInfo(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name=property_name("名称")) # type: ignore
    id: bpy.props.IntProperty(name=property_name("ID")) # type: ignore
    target_id: bpy.props.IntProperty(name=property_name("TargetID"),update=switch_block_update) # type: ignore
    target_block_enum: bpy.props.EnumProperty(
        name=property_name("选择方块"),
        items=get_block_items,
        update=update_target_id_from_enum,
        description=property_name("选择要替换成的目标方块")
    )  # type: ignore


#属性
class Property(bpy.types.PropertyGroup):
    color_file_path: bpy.props.StringProperty(name=property_name("Color File Path"),default="") # type: ignore
    brush_block_enum: bpy.props.EnumProperty(
        name=property_name("笔刷方块"),
        items=get_block_items,
        description=property_name("笔刷使用的方块")
    )

    bpy.types.Scene.mods_dir = bpy.props.StringProperty(
        name=property_name("模组路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"temp")
    )
    bpy.types.Scene.jars_dir = bpy.props.StringProperty(
        name=property_name("jar文件路径"),
        default=os.path.join("mods")
    )
    bpy.types.Scene.versions_dir = bpy.props.StringProperty(
        name=property_name("版本路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"temp","minecraft")
    )
    bpy.types.Scene.saves_dir = bpy.props.StringProperty(
        name=property_name("存档路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"saves")
    )
    bpy.types.Scene.colors_dir = bpy.props.StringProperty(
        name=property_name("颜色路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"colors")
    )
    bpy.types.Scene.schems_dir = bpy.props.StringProperty(
        name=property_name(".schem文件路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"schem")
    )
    bpy.types.Scene.zips_dir = bpy.props.StringProperty(
        name=property_name("zip文件路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"resourcepacks")
    )
    bpy.types.Scene.resourcepacks_dir = bpy.props.StringProperty(
        name=property_name("资源包路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"temp", "资源包")
    )
    bpy.types.Scene.material_blend_path = bpy.props.StringProperty(
        name=property_name("材质节点路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"codes","blend_files","Material.blend")
    )
    bpy.types.Scene.geometrynodes_blend_path = bpy.props.StringProperty(
        name=property_name("几何节点路径"),
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"codes","blend_files","GeometryNodes.blend")
    )
    bpy.types.Scene.is_weld = bpy.props.BoolProperty(name=property_name("合并重叠顶点"), default=True)

    JsonImportSpeed: bpy.props.FloatProperty(name=property_name("导入速度(秒每个）"),description=property_name("Import speed"),min=0.01, max=2.0,default=1.0) # type: ignore
    resourcepack_list: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    resourcepack_list_index: bpy.props.IntProperty() # type: ignore

    # 定义 mod_list 属性
    mod_list: bpy.props.CollectionProperty(type=ModInfo) # type: ignore
    mod_list_index: bpy.props.IntProperty() # type: ignore

    # 定义 color_to_block_list 属性
    color_to_block_list: bpy.props.CollectionProperty(type=BlockInfo) # type: ignore
    color_to_block_list_index: bpy.props.IntProperty() # type: ignore

    switch_block_list: bpy.props.CollectionProperty(type=SwitchBlockInfo) # type: ignore
    switch_block_list_index: bpy.props.IntProperty() # type: ignore
    bpy.types.Scene.min_coordinates = bpy.props.IntVectorProperty(name=property_name("最小坐标"), size=3)
    bpy.types.Scene.max_coordinates = bpy.props.IntVectorProperty(name=property_name("最大坐标"), size=3)

    bpy.types.Scene.schem_size = bpy.props.IntVectorProperty(name=property_name("结构大小"), size=3)
    bpy.types.Scene.schem_location = bpy.props.IntVectorProperty(name=property_name("结构位置"), size=3)


    # 定义一个 EnumProperty 作为下拉列表的选项
    bpy.types.Scene.version_list = bpy.props.EnumProperty(
        name=property_name("版本"),
        description=property_name("选择一个版本"),
        items=(),
    )
    bpy.types.Scene.save_list = bpy.props.EnumProperty(
        name=property_name("存档"),
        description=property_name("选择一个存档"),
        items=(),
    )
    bpy.types.Scene.schem_list = bpy.props.EnumProperty(
        name=property_name(".schem文件"),
        description=property_name("选择一个.schem文件"),
        items=(),
    )
    bpy.types.Scene.color_list = bpy.props.EnumProperty(
        name=property_name("color文件"),
        description=property_name("选择一个颜色字典"),
        items=(),
    )
    bpy.types.Scene.separate_vertices_by_blockid = bpy.props.BoolProperty(
        name=property_name("按方块状态分离"),
        description=property_name("将导入的结构按照方块类型分离，每种方块类型生成一个独立的 Blender 对象"),
        default=False
    )
    bpy.types.Scene.separate_vertices_by_chunk = bpy.props.BoolProperty(
        name=property_name("按区块分离"),
        description=property_name("将导入的结构按照 Minecraft 区块（16x16x16）分离，每个区块生成一个独立的 Blender 对象"),
        default=False
    )
    bpy.types.Scene.schem_filename = bpy.props.StringProperty(name=property_name(".schem文件名"), default="file")

    # Minecraft 版本配置
    bpy.types.Scene.mc_platform = bpy.props.EnumProperty(
        name=property_name("MC 平台"),
        description=property_name("Minecraft 版本平台"),
        items=[
            enum_item("java", property_name("Java Edition"), property_name("Java 版本")),
            enum_item("bedrock", property_name("Bedrock Edition"), property_name("基岩版（主机/手机）"))
        ],
        default="java"
    )
    bpy.types.Scene.mc_version_major = bpy.props.IntProperty(
        name=property_name("主版本号"),
        description=property_name("Minecraft 主版本号（如 1.21.11 中的 1）"),
        default=1,
        min=1,
        max=2
    )
    bpy.types.Scene.mc_version_minor = bpy.props.IntProperty(
        name=property_name("次版本号"),
        description=property_name("Minecraft 次版本号（如 1.21.11 中的 21）"),
        default=21,
        min=7,
        max=21
    )
    bpy.types.Scene.mc_version_patch = bpy.props.IntProperty(
        name=property_name("补丁版本号"),
        description=property_name("Minecraft 补丁版本号（如 1.21.9 中的 9）"),
        default=9,
        min=0,
        max=10
    )

    bpy.types.Scene.world_name = bpy.props.StringProperty(name=property_name("World Name"), default="World1")
    bpy.types.Scene.spawn_x = bpy.props.IntProperty(name=property_name("Spawn X"), default=0)
    bpy.types.Scene.spawn_y = bpy.props.IntProperty(name=property_name("Spawn Y"), default=64)
    bpy.types.Scene.spawn_z = bpy.props.IntProperty(name=property_name("Spawn Z"), default=0)
    bpy.types.Scene.hardcore = bpy.props.EnumProperty(
        name=property_name("极限模式"),
        items=[
            enum_item("0", property_name("否"), property_name("否")),
            enum_item("1", property_name("是"), property_name("是"))
        ],
        default="0"
    )
    bpy.types.Scene.difficulty = bpy.props.EnumProperty(
        name=property_name("难度"),
        items=[
            enum_item("0", property_name("和平"), property_name("和平模式")),
            enum_item("1", property_name("简单"), property_name("简单模式")),
            enum_item("2", property_name("普通"), property_name("普通模式")),
            enum_item("3", property_name("困难"), property_name("困难模式"))
        ],
        default="0"
    )
    bpy.types.Scene.gametype = bpy.props.EnumProperty(
        name=property_name("游戏模式"),
        items=[
            enum_item("0", property_name("生存"), property_name("和平模式")),
            enum_item("1", property_name("创造"), property_name("创造模式")),
            enum_item("2", property_name("冒险"), property_name("冒险模式")),
            enum_item("3", property_name("旁观"), property_name("旁观模式"))
        ],
        default="1"
    )
    bpy.types.Scene.overworld_generator_type = bpy.props.EnumProperty(
        name=property_name("主世界生成类型"),
        items=[
            enum_item("noise", property_name("噪波"), property_name("一般世界")),
            enum_item("flat", property_name("平坦"), property_name("平坦世界")),
            enum_item("debug", property_name("DEBUG"), property_name("DEBUG"))
        ],
        default="noise"
    )
    bpy.types.Scene.allow_commands = bpy.props.EnumProperty(
        name=property_name("允许指令"),
        items=[
            enum_item("0", property_name("否"), property_name("否")),
            enum_item("1", property_name("是"), property_name("是"))
        ],
        default="1"
    )
    bpy.types.Scene.breaking_the_height_limit = bpy.props.EnumProperty(
        name=property_name("突破限高"),
        items=[
            enum_item("0", property_name("否"), property_name("否")),
            enum_item("1", property_name("是"), property_name("突破限高至2032！"))
        ],
        default="0"
    )

    # 布尔值游戏规则（辅助函数）
    def _true_false_enum_items():
        yes = property_name("是")
        no = property_name("否")
        return [
            enum_item("True", yes, yes),
            enum_item("False", no, no)
        ]

    def _false_true_enum_items():
        yes = property_name("是")
        no = property_name("否")
        return [
            enum_item("False", no, no),
            enum_item("True", yes, yes)
        ]

    # 游戏规则属性
    bpy.types.Scene.announce_advancements = bpy.props.EnumProperty(
        name=property_name("Announce Advancements"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.block_explosion_drop_decay = bpy.props.EnumProperty(
        name=property_name("Block Explosion Drop Decay"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.command_block_output = bpy.props.EnumProperty(
        name=property_name("Command Block Output"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.disable_elytra_movement_check = bpy.props.EnumProperty(
        name=property_name("Disable Elytra Movement Check"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.disable_raids = bpy.props.EnumProperty(
        name=property_name("Disable Raids"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_daylight_cycle = bpy.props.EnumProperty(
        name=property_name("Do Daylight Cycle"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_entity_drops = bpy.props.EnumProperty(
        name=property_name("Do Entity Drops"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_fire_tick = bpy.props.EnumProperty(
        name=property_name("Do Fire Tick"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_immediate_respawn = bpy.props.EnumProperty(
        name=property_name("Do Immediate Respawn"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_insomnia = bpy.props.EnumProperty(
        name=property_name("Do Insomnia"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_limited_crafting = bpy.props.EnumProperty(
        name=property_name("Do Limited Crafting"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_mob_loot = bpy.props.EnumProperty(
        name=property_name("Do Mob Loot"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_mob_spawning = bpy.props.EnumProperty(
        name=property_name("Do Mob Spawning"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_patrol_spawning = bpy.props.EnumProperty(
        name=property_name("Do Patrol Spawning"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_tile_drops = bpy.props.EnumProperty(
        name=property_name("Do Tile Drops"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_trader_spawning = bpy.props.EnumProperty(
        name=property_name("Do Trader Spawning"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_vines_spread = bpy.props.EnumProperty(
        name=property_name("Do Vines Spread"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_warden_spawning = bpy.props.EnumProperty(
        name=property_name("Do Warden Spawning"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.do_weather_cycle = bpy.props.EnumProperty(
        name=property_name("Do Weather Cycle"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.drowning_damage = bpy.props.EnumProperty(
        name=property_name("Drowning Damage"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.fall_damage = bpy.props.EnumProperty(
        name=property_name("Fall Damage"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.fire_damage = bpy.props.EnumProperty(
        name=property_name("Fire Damage"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.forgive_dead_players = bpy.props.EnumProperty(
        name=property_name("Forgive Dead Players"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.freeze_damage = bpy.props.EnumProperty(
        name=property_name("Freeze Damage"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.global_sound_events = bpy.props.EnumProperty(
        name=property_name("Global Sound Events"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.keep_inventory = bpy.props.EnumProperty(
        name=property_name("Keep Inventory"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.lava_source_conversion = bpy.props.EnumProperty(
        name=property_name("Lava Source Conversion"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.log_admin_commands = bpy.props.EnumProperty(
        name=property_name("Log Admin Commands"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.mob_explosion_drop_decay = bpy.props.EnumProperty(
        name=property_name("Mob Explosion Drop Decay"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.mob_griefing = bpy.props.EnumProperty(
        name=property_name("Mob Griefing"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.natural_regeneration = bpy.props.EnumProperty(
        name=property_name("Natural Regeneration"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.reduced_debug_info = bpy.props.EnumProperty(
        name=property_name("Reduced Debug Info"),
        items=_false_true_enum_items(),
        default="False"
    )

    bpy.types.Scene.send_command_feedback = bpy.props.EnumProperty(
        name=property_name("Send Command Feedback"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.show_death_messages = bpy.props.EnumProperty(
        name=property_name("Show Death Messages"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.spectators_generate_chunks = bpy.props.EnumProperty(
        name=property_name("Spectators Generate Chunks"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.tnt_explosion_drop_decay = bpy.props.EnumProperty(
        name=property_name("TNT Explosion Drop Decay"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.universal_anger = bpy.props.EnumProperty(
        name=property_name("Universal Anger"),
        items=_true_false_enum_items(),
        default="True"
    )

    bpy.types.Scene.water_source_conversion = bpy.props.EnumProperty(
        name=property_name("Water Source Conversion"),
        items=_true_false_enum_items(),
        default="True"
    )

    # 整数
    bpy.types.Scene.max_entity_cramming = bpy.props.IntProperty(name=property_name("Max Entity Cramming"),default=12)
    bpy.types.Scene.snow_accumulation_height = bpy.props.IntProperty(name=property_name("Snow Accumulation Height"),default=1)
    bpy.types.Scene.spawn_radius = bpy.props.IntProperty(name=property_name("Spawn Radius"),default=10)
    bpy.types.Scene.players_sleeping_percentage = bpy.props.IntProperty(name=property_name("Players Sleeping Percentage"),default=0)
    bpy.types.Scene.random_tick_speed = bpy.props.IntProperty(name=property_name("Random Tick Speed"),default=0)
    bpy.types.Scene.command_modification_block_limit = bpy.props.IntProperty(name=property_name("Command Modification Block Limit"),default=32768)
    bpy.types.Scene.max_command_chain_length = bpy.props.IntProperty(name=property_name("Max Command Chain Length"),default=65536)
    bpy.types.Scene.day_time = bpy.props.IntProperty(name=property_name("Day Time"), default=16000)
    bpy.types.Scene.seed = bpy.props.IntProperty(name=property_name("Seed"), default=random.randint(0, 10000))

    bpy.types.Scene.flySpeed = bpy.props.FloatProperty(name=property_name("FlySpeed"), default=0.05)
    bpy.types.Scene.flying = bpy.props.BoolProperty(name=property_name("Flying"), default=False)
    bpy.types.Scene.instabuild = bpy.props.BoolProperty(name=property_name("instabuild"), default=True)
    bpy.types.Scene.invulnerable = bpy.props.BoolProperty(name=property_name("invulnerable"), default=True)
    bpy.types.Scene.mayBuild = bpy.props.BoolProperty(name=property_name("mayBuild"), default=True)
    bpy.types.Scene.mayfly = bpy.props.BoolProperty(name=property_name("mayfly"), default=True)

    bpy.types.Scene.walkSpeed = bpy.props.FloatProperty(name=property_name("walkSpeed"), default=0.1)

    bpy.types.Scene.luck = bpy.props.FloatProperty(name=property_name("幸运值"), default=0, min=-1024, max=1024)
    bpy.types.Scene.max_health = bpy.props.FloatProperty(name=property_name("最大生命值"), default=20, min=1, max=1024)
    bpy.types.Scene.knockback_resistance = bpy.props.FloatProperty(name=property_name("击退抗性"), default=0, min=0, max=1)
    bpy.types.Scene.movement_speed = bpy.props.FloatProperty(name=property_name("移动加速度"), default=0, min=0, max=1024)
    bpy.types.Scene.armor = bpy.props.FloatProperty(name=property_name("盔甲值"), default=0, min=0, max=30)
    bpy.types.Scene.armor_toughness = bpy.props.FloatProperty(name=property_name("盔甲韧性"), default=0, min=0, max=20)
    bpy.types.Scene.attack_damage = bpy.props.FloatProperty(name=property_name("攻击伤害"), default=0, min=0, max=2048)
    bpy.types.Scene.attack_speed = bpy.props.FloatProperty(name=property_name("攻击速度"), default=0, min=0, max=1024)
    
def unzip_mods_files():
    # 指定的文件夹路径
    folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"mods")

    # 临时文件夹路径
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"temp")

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.jar'):
            # 构造完整的文件路径
            file_path = os.path.join(folder_path, file_name)

            # 解压文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                mod_id = None 
                for member in zip_ref.namelist():
                    if member == 'version.json':
                        with zip_ref.open(member) as mod_json_file:
                            mod_json_content = mod_json_file.read()
                            mod_data = json.loads(mod_json_content,strict=False)
                            # 读取 "id" 字段的值
                            mod_id = "minecraft"
                            version = mod_data.get("id","")
                            icon = None
                            name = mod_data.get("name","")
                            description = "我的世界原版"
                        new_folder_path = os.path.join(temp_dir,mod_id,version)
                        break  # 找到后终止循环
                    # 判断是否存在fabric.mod.json，若存在则读取其中的modid
                    elif member == 'fabric.mod.json':
                        with zip_ref.open(member) as mod_json_file:
                            mod_json_content = mod_json_file.read()
                            mod_data = json.loads(mod_json_content,strict=False)
                            # 读取 "id" 字段的值
                            mod_id = mod_data.get("id","")
                            icon = mod_data.get("icon","").replace("/", "\\")
                            name = mod_data.get("name","")
                            description = mod_data.get("description","")
                        try:
                            # 创建新文件夹以modid命名
                            new_folder_path = os.path.join(temp_dir, mod_id)
                        except:
                            pass
                        break  # 找到fabric.mod.json后终止循环
                    elif member == 'META-INF/mods.toml':
                        with zip_ref.open('META-INF/mods.toml') as mods_toml_file:
                            mods_toml_content = mods_toml_file.read().decode('utf-8')
                            mods_toml_data = toml.loads(mods_toml_content)
                            if "mods" in mods_toml_data:
                                for mod_entry in mods_toml_data["mods"]:
                                    mod_id = mod_entry["modId"]
                                    icon = mod_entry.get("logoFile", "").replace("/", "\\")  # 添加默认值，防止没有 "logoFile" 字段时报错
                                    name = mod_entry.get("displayName", "")  # 添加默认值，防止没有 "displayName" 字段时报错
                                    description = mod_entry.get("description", "")  # 添加默认值，防止没有 "description" 字段时报错
                            else:
                                print(f"在 {file_name} 中找不到 'mods' 条目")
                        try:
                            # 创建新文件夹以modid命名
                            new_folder_path = os.path.join(temp_dir, mod_id)
                        except:
                            pass
                        break
                    elif member == 'mcmod.info':
                        with zip_ref.open('mcmod.info') as mcmod_file:
                            mcmod_content = mcmod_file.read()
                            mcmod_data = json.loads(mcmod_content)
                            if mcmod_data:
                                mod_info = mcmod_data[0]  
                                mod_id = mod_info.get("modid", "")
                                icon = mod_info.get("logoFile", "").replace("/", "\\") 
                                name = mod_info.get("name", "")  
                                description = mod_info.get("description", "")  
                        try:
                            # 创建新文件夹以modid命名
                            new_folder_path = os.path.join(temp_dir, mod_id)
                        except:
                            pass
                        break

                    
                if mod_id:
                    try:
                        if not os.path.exists(new_folder_path):
                            os.makedirs(new_folder_path)
                        elif os.path.exists(new_folder_path):
                            continue
                    except:
                        pass

                    # 将文件解压到新文件夹中
                    for member in zip_ref.namelist():
                        try:
                            # 提取第一层目录下的 assets 和 data 文件夹以及第一层文件夹下的 .json 和 .png 文件
                            if member.startswith('assets/') or member.startswith('data/'):
                                # 构造解压路径
                                extract_path = os.path.join(new_folder_path, member)
                                dir_extract_path = os.path.dirname(extract_path)+"/"
                                # 如果目标文件夹不存在，则创建
                                try:
                                    if not os.path.exists(dir_extract_path):
                                        os.makedirs(dir_extract_path)
                                except:
                                    pass
                                if not os.path.exists(extract_path):
                                    with zip_ref.open(member) as file_in_zip, open(extract_path, 'wb') as output_file:
                                        shutil.copyfileobj(file_in_zip, output_file)

                            elif not '/' in member:  # 第一级目录下的文件
                                if member.endswith('.json') or member.endswith('.png'):
                                    extract_path = os.path.join(new_folder_path, member)
                                    with zip_ref.open(member) as file_in_zip, open(extract_path, 'wb') as output_file:
                                        shutil.copyfileobj(file_in_zip, output_file)
                        except Exception as e:
                            print(f"An error occurred3: {e}")
                            pass
                    try:
                        if mod_id!="minecraft":
                            new_name = os.path.join(folder_path, mod_id+".jar")
                            zip_ref.close()
                            os.rename(file_path, new_name)
                        elif mod_id == "minecraft":
                            new_name = os.path.join(folder_path, version+".jar")
                            zip_ref.close()
                            os.rename(file_path, new_name)
                    except Exception as e:
                        print(f"An error occurred while renaming: {e}")
        

def unzip_resourcepacks_files():
    # 指定的文件夹路径
    folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"resourcepacks")
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return

    # 临时文件夹路径
    temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"temp","资源包")

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.zip'):
            # 构造完整的文件路径
            file_path = os.path.join(folder_path, file_name)

            # 解压文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                new_folder_path=os.path.join(temp_dir,file_name.replace('.zip', ''))
                try:
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                    elif os.path.exists(new_folder_path):
                        continue
                except:
                    pass

                # 将文件解压到新文件夹中
                for member in zip_ref.namelist():
                    try:
                        # 提取第一层目录下的 assets 和 data 文件夹以及第一层文件夹下的 .json 和 .png 文件
                        if member.startswith('assets/') or member.startswith('data/'):
                            # 构造解压路径
                            extract_path = os.path.join(new_folder_path, member)
                            dir_extract_path = os.path.dirname(extract_path)+"/"
                            # 如果目标文件夹不存在，则创建
                            try:
                                if not os.path.exists(dir_extract_path):
                                    os.makedirs(dir_extract_path)
                            except:
                                pass
                            if not os.path.exists(extract_path):
                                with zip_ref.open(member) as file_in_zip, open(extract_path, 'wb') as output_file:
                                    shutil.copyfileobj(file_in_zip, output_file)

                        elif not '/' in member:  # 第一级目录下的文件
                            if member.endswith('.json') or member.endswith('.png'):
                                extract_path = os.path.join(new_folder_path, member)
                                with zip_ref.open(member) as file_in_zip, open(extract_path, 'wb') as output_file:
                                    shutil.copyfileobj(file_in_zip, output_file)
                    except Exception as e:
                        print(f"An error occurred4: {e}")
                        pass
                

        
class UnzipModOperator(bpy.types.Operator):
    bl_idname = "mbm.unzip_mods_operator"
    bl_label = operator_label("加载模组包")

    def execute(self, context):
        thread = threading.Thread(target=unzip_mods_files)
        thread.start()

        bpy.app.timers.register(functools.partial(self.check_thread, thread), first_interval=1.0)
        return {'RUNNING_MODAL'}

    def check_thread(self, thread):
        # 检查线程是否在运行
        if not thread.is_alive():
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

class UnzipResourcepacksOperator(bpy.types.Operator):
    bl_idname = "mbm.unzip_resourcepacks_operator"
    bl_label = operator_label("加载模组包")

    def execute(self, context):
        thread = threading.Thread(target=unzip_resourcepacks_files)
        thread.start()

        bpy.app.timers.register(functools.partial(self.check_thread, thread), first_interval=1.0)
        return {'RUNNING_MODAL'}

    def check_thread(self, thread):
        # 检查线程是否在运行
        if not thread.is_alive():
            return {'FINISHED'}
        return {'RUNNING_MODAL'}



    
classes=[ModInfo,BlockInfo,SwitchBlockInfo,Property,UnzipModOperator,UnzipResourcepacksOperator]




def register():
    threading.Thread(target=unzip_mods_files).start()
    threading.Thread(target=unzip_resourcepacks_files).start()
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)
    bpy.types.Scene.my_properties = bpy.props.PointerProperty(type=Property)
    importlib.reload(config)
    
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
