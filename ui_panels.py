import bpy

# 翻译支持
from bpy.app.translations import pgettext_iface as _
from .i18n.translations import panel_label, operator_label

# 依赖管理
from .codes.dependency_manager import litemapy, amulet


class MBM_PT_main_panel(bpy.types.Panel):
    bl_label = panel_label("MBM_workflow")
    bl_idname = "MBM_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    # Note: Previously __init__ called directory read operations, but this is problematic
    # because Blender creates panel instances frequently. These operations should be
    # called explicitly by the user or triggered when needed.

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="MBM_workflow", icon="BOLD")


# 导入面板
class MBM_PT_import_panel(bpy.types.Panel):
    bl_label = panel_label("导入")
    bl_idname = "MBM_PT_import_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        amulet_ok = amulet is not None

        row = layout.row()
        row.label(text="导入", icon="IMPORT")
        if not amulet_ok:
            layout.label(text=".schem/.nbt/世界导入导出需 amulet，当前 Blender 版本暂不可用", icon='ERROR')
        # 创建一个框
        box = layout.box()
        box.enabled = amulet_ok
        box.label(text="导入.schem文件")
        box.operator("mbm.schem_import_panel", text="导入.schem文件")
        layout.split()

        # Litematic 导入（仅依赖纯 Python 的 litemapy，amulet 缺失时仍可用）
        if litemapy is not None:
            box = layout.box()
            box.label(text="导入.litematic文件")
            box.operator("mbm.import_litematic", text="导入.litematic文件")
        else:
            box = layout.box()
            box.label(text="导入.litematic文件 (依赖缺失)")
            box.enabled = False

        box = layout.box()
        box.label(text="导入方块")
        box.operator("mbm.import_block", text="导入方块")
        box.operator("mbm.import_json", text="导入.json文件")
        box.operator("mbm.reload_blocks", text="重载失效方块", icon="FILE_REFRESH")

        box = layout.box()
        box.enabled = amulet_ok

        box.label(text="导入.nbt文件")
        box.operator("mbm.import_nbt", text="导入.nbt文件")

        box = layout.box()
        box.enabled = amulet_ok
        row = box.row()
        col = box.column()
        row.label(text="导入MC地图")
        # 添加min [x, y, z]输入框
        row = box.row()
        row.label(text="最小坐标")
        row.prop(context.scene, "min_coordinates", text="")

        # 添加max [x, y, z]输入框
        row = box.row()
        row.label(text="最大坐标")
        row.prop(context.scene, "max_coordinates", text="")
        col.operator("mbm.import_world", text="导入世界")

        row = layout.row()
        row.operator("object.add_sway_animation", text="植物摇摆")

        row = layout.row()
        row.operator("mbm.map_optimize", text="执行优化")

        # 添加布尔属性的选项
        row = layout.row()
        row.prop(scene, "is_weld", text="合并重叠顶点")

        box = layout.box()
        row = box.row()
        row.operator("mbm.merge_overlapping_faces", text="合并重叠面")


# 导出面板
class MBM_PT_export_panel(bpy.types.Panel):
    bl_label = panel_label("导出")
    bl_idname = "MBM_PT_export_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        amulet_ok = amulet is not None
        if not amulet_ok:
            layout.label(text="导出需 amulet_nbt，当前 Blender 版本暂不可用", icon='ERROR')
        row = layout.row()
        row.enabled = amulet_ok
        row.prop(scene, "schem_filename", text="文件名")
        row = layout.row()
        row.enabled = amulet_ok
        row.operator("mbm.export_schem", text="导出结构")
        box = layout.box()
        box.prop(scene, "save_list", text="选择世界")
        box.label(
            text="长:"
            + str(scene.schem_size[0])
            + " 宽:"
            + str(scene.schem_size[1])
            + " 高:"
            + str(scene.schem_size[2])
            + " (blender坐标系)"
        )
        box.label(
            text="位置:("
            + str(scene.schem_location[0])
            + ","
            + str(scene.schem_location[1])
            + ","
            + str(scene.schem_location[2])
            + ")"
        )

        box.operator("mbm.calculate_size", text="计算结构大小")
        box.operator("mbm.export_to_save", text="导出结构到存档")


# 创建存档面板
class MBM_PT_create_level(bpy.types.Panel):
    bl_label = panel_label("创建存档")
    bl_idname = "MBM_PT_create_level"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        if amulet is None:
            layout.label(text="创建存档需 amulet_nbt，当前 Blender 版本暂不可用", icon='ERROR')
            return

        row = layout.row()
        row.label(text="存档", icon="WORLD")
        row = layout.row()
        box = layout.box()
        row = box.row()
        box.prop(scene, "world_name", text="存档名称")
        row = box.row()
        row.label(text="出生点坐标")
        row = box.row()
        row.prop(scene, "spawn_x", text="X")
        row.prop(scene, "spawn_y", text="Y")
        row.prop(scene, "spawn_z", text="Z")
        row = box.row()
        row.prop(scene, "difficulty", text="难度")
        row = box.row()
        row.prop(scene, "gametype", text="游戏模式")
        row = box.row()
        row.prop(scene, "overworld_generator_type", text="世界类型")
        row = box.row()
        row.prop(scene, "hardcore", text="极限模式")
        row = box.row()
        row.prop(scene, "allow_commands", text="允许指令")
        row = box.row()
        row.prop(scene, "breaking_the_height_limit", text="突破限高？")
        row = box.row()
        row.prop(scene, "day_time", text="时间")
        row = box.row()
        row.prop(scene, "seed", text="种子")
        row = layout.row()
        row.operator("mbm.create_world", text="创建存档")


# 编辑面板
class MBM_PT_edit_panel(bpy.types.Panel):
    bl_label = panel_label("编辑")
    bl_idname = "MBM_PT_edit_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(scene, "color_list", text="对照表")
        row = layout.row()
        row.operator("mbm.color_to_block_panel", text="制作颜色-方块字典")
        row = layout.row()
        row.operator("mbm.switch_blocks_panel", text="替换方块")
        row = layout.row()
        row.operator(
            "mbm.merge_schem_pointclouds", text=operator_label("合并+规范化点云")
        )
        row = layout.row()
        row.label(text="可视化编辑：")
        row = layout.row()
        row.prop(scene.my_properties, "brush_block_enum", text="")
        row.prop(scene.my_properties, "brush_radius", text="半径")
        row.operator("mbm.block_brush", text="启动方块笔刷", icon="BRUSH_DATA")
        row = layout.row()
        row.operator("mbm.get_average_color", text="得到图片平均颜色值")
        row = layout.row()
        row.operator("mbm.objtoblocks", text="生成点云(转楼梯/台阶方块所需)")
        row = layout.row()
        row.operator("mbm.blockblender", text="转换网格体(方块)")
        row = layout.row()
        row.operator("mbm.paint_block", text="应用顶点色到方块")


# 更多设置面板
class MBM_PT_more_level_settings(bpy.types.Panel):
    bl_label = panel_label("更多设置")
    bl_idname = "MBM_PT_more_level_settings"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_create_level"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()

        box.label(text="指定单次命令执行可更改的最大方块数")
        box.prop(scene, "command_modification_block_limit", text="")

        box.label(text="决定了连锁型命令方块能连锁执行的总数量。	")
        box.prop(scene, "max_command_chain_length", text="")

        box.label(text="下雪时可在一格方块空间内堆积的雪的最高层数")
        box.prop(scene, "snow_accumulation_height", text="")

        box.label(
            text="首次进入服务器的玩家和没有重生点的死亡玩家在重生时与世界重生点坐标的距离"
        )
        box.prop(scene, "spawn_radius", text="")

        box.label(text="每游戏刻每区段中随机的方块刻发生的频率")
        box.prop(scene, "random_tick_speed", text="")

        box.label(text="设置跳过夜晚所需的入睡玩家所占百分比。")
        box.prop(scene, "players_sleeping_percentage", text="")

        box.label(text="将一方块空间内挤压到一起的实体的最大数量")
        box.prop(scene, "max_entity_cramming", text="")


# 玩家能力面板
class MBM_PT_ability(bpy.types.Panel):
    bl_label = panel_label("玩家能力")
    bl_idname = "MBM_PT_ability"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_create_level"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        box.prop(scene, "flySpeed", text="飞行速度")
        box.prop(scene, "walkSpeed", text="行走速度")
        # box.prop(scene, "flying", text="正在飞行？")
        # box.prop(scene, "mayfly", text="能飞行？")
        # box.prop(scene, "mayBuild", text="能建造？")
        # box.prop(scene, "instabuild", text="表示玩家是否可以瞬间摧毁方块")
        # box.prop(scene, "invulnerable", text="表示玩家是否能抵消除虚空伤害所有伤害和有害的效果")
        box.prop(scene, "luck", text="幸运值")
        box.prop(scene, "max_health", text="最大生命值")
        box.prop(scene, "knockback_resistance", text="击退抗性")
        # box.prop(scene, "movement_speed", text="移动加速度")
        box.prop(scene, "armor", text="盔甲值")
        box.prop(scene, "armor_toughness", text="盔甲韧性")
        box.prop(scene, "attack_damage", text="攻击伤害")
        box.prop(scene, "attack_speed", text="攻击速度")


# 创建游戏规则面板
class MBM_PT_game_rules(bpy.types.Panel):
    bl_label = panel_label("游戏规则")
    bl_idname = "MBM_PT_game_rules"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_more_level_settings"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()

        box.label(text="是否在聊天框中公告玩家进度的达成")
        box.prop(scene, "announce_advancements", text="")

        box.label(text="由方块源（除TNT）爆炸炸毁的方块是否会有概率不掉落")
        box.prop(scene, "block_explosion_drop_decay", text="")

        box.label(text="命令方块执行命令时是否在聊天框中向管理员显示")
        box.prop(scene, "command_block_output", text="")

        box.label(text="是否让服务器停止检查使用鞘翅玩家的移动速度。")
        box.prop(scene, "disable_elytra_movement_check", text="")

        box.label(text="是否禁用袭击")
        box.prop(scene, "disable_raids", text="")

        box.label(text="是否进行昼夜更替和月相变化")
        box.prop(scene, "do_daylight_cycle", text="")

        box.label(text="非生物实体是否掉落物品")
        box.prop(scene, "do_entity_drops", text="")

        box.label(text="火是否蔓延及自然熄灭")
        box.prop(scene, "do_fire_tick", text="")

        box.label(text="玩家死亡时是否不显示死亡界面直接重生")
        box.prop(scene, "do_immediate_respawn", text="")

        box.label(text="幻翼是否在夜晚生成")
        box.prop(scene, "do_insomnia", text="")

        box.label(text="玩家的合成配方是否需要解锁才能使用")
        box.prop(scene, "do_limited_crafting", text="")

        box.label(text="生物在死亡时是否掉落物品")
        box.prop(scene, "do_mob_loot", text="")

        box.label(text="生物是否自然生成。不影响刷怪笼")
        box.prop(scene, "do_mob_spawning", text="")

        box.label(text="控制灾厄巡逻队的生成")
        box.prop(scene, "do_patrol_spawning", text="")

        box.label(text="方块被破坏时是否掉落物品")
        box.prop(scene, "do_tile_drops", text="")

        box.label(text="控制流浪商人的生成")
        box.prop(scene, "do_trader_spawning", text="")

        box.label(text="决定藤蔓是否会向周围扩散，不影响洞穴藤蔓、缠怨藤和垂泪藤")
        box.prop(scene, "do_vines_spread", text="")

        box.label(text="监守者是否生成")
        box.prop(scene, "do_warden_spawning", text="")

        box.label(text="天气是否变化")
        box.prop(scene, "do_weather_cycle", text="")

        box.label(text="玩家是否承受窒息伤害")
        box.prop(scene, "drowning_damage", text="")

        box.label(text="玩家是否承受跌落伤害")
        box.prop(scene, "fall_damage", text="")

        box.label(text="玩家是否承受火焰伤害[仅Java版][1]")
        box.prop(scene, "fire_damage", text="")

        box.label(
            text="当被激怒的条件敌对生物的目标玩家死亡时，该生物是否恢复未激怒状态"
        )
        box.prop(scene, "forgive_dead_players", text="")

        box.label(text="玩家是否承受冰冻伤害")
        box.prop(scene, "freeze_damage", text="")

        box.label(text="玩家是否能听到可无视距离播放给全部玩家的特定游戏事件音效")
        box.prop(scene, "global_sound_events", text="")

        box.label(
            text="玩家死亡后是否保留物品栏物品、经验（死亡时物品不掉落、经验不清空）"
        )
        box.prop(scene, "keep_inventory", text="")

        box.label(text="流动的熔岩是否可产生熔岩源")
        box.prop(scene, "lava_source_conversion", text="")

        box.label(text="是否在服务器日志中记录管理员使用过的命令")
        box.prop(scene, "log_admin_commands", text="")

        box.label(text="由生物源爆炸炸毁的方块是否会有概率不掉落")
        box.prop(scene, "mob_explosion_drop_decay", text="")

        box.label(text="生物是否能够进行破坏性行为")
        box.prop(scene, "mob_griefing", text="")

        box.label(text="玩家是否能在饥饿值足够时自然恢复生命值")
        box.prop(scene, "natural_regeneration", text="")

        box.label(text="调试屏幕是否简化而非显示详细信息")
        box.prop(scene, "reduced_debug_info", text="")

        box.label(text="玩家执行命令的返回信息是否在聊天框中显示。")
        box.prop(scene, "send_command_feedback", text="")

        box.label(text="是否在聊天框中显示玩家的死亡信息。")
        box.prop(scene, "show_death_messages", text="")

        box.label(text="是否允许旁观模式的玩家生成区块")
        box.prop(scene, "spectators_generate_chunks", text="")

        box.label(text="由TNT爆炸炸毁的方块是否会有概率不掉落")
        box.prop(scene, "tnt_explosion_drop_decay", text="")

        box.label(text="被激怒的条件敌对生物是否攻击附近任何玩家")
        box.prop(scene, "universal_anger", text="")

        box.label(text="流动的水是否可产生水源")
        box.prop(scene, "water_source_conversion", text="")


# 资源包面板
class MBM_PT_resourcepacks(bpy.types.Panel):
    bl_label = panel_label("资源包")
    bl_idname = "MBM_PT_resourcepacks"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_mod"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "resourcepacks_dir", text="路径")  # 添加路径字段
        row = layout.row()
        scene = context.scene
        my_properties = scene.my_properties
        row.template_list(
            "MBM_UL_resourcepack_list",
            "",
            my_properties,
            "resourcepack_list",
            my_properties,
            "resourcepack_list_index",
        )

        col = row.column(align=True)
        # 上下移动按钮
        col.operator(
            "mbm.move_resourcepack_item", text="", icon="TRIA_UP"
        ).direction = "UP"
        col.operator(
            "mbm.move_resourcepack_item", text="", icon="TRIA_DOWN"
        ).direction = "DOWN"
        col.operator("mbm.add_resourcepack_operator", text="", icon="ADD")
        col.operator("mbm.delete_resourcepack_operator", text="", icon="REMOVE")
        # 添加打印选中项目的按钮
        layout.operator("mbm.unzip_resourcepacks_operator", text="刷新")


# 模组界面
class MBM_PT_mod(bpy.types.Panel):
    bl_label = panel_label("Mod 设置")
    bl_idname = "MBM_PT_mod"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MBM_workflow"
    bl_parent_id = "MBM_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_properties = scene.my_properties
        row = layout.row()
        # 添加 Minecraft 版本选择

        row = layout.row()
        row.prop(scene, "version_list", text="")
        row = layout.row()
        row.label(text="已加载的模组：")
        row = layout.row()
        # 使用template_list来显示模组列表
        row.template_list(
            "MBM_UL_mod_list",
            "",
            my_properties,
            "mod_list",
            my_properties,
            "mod_list_index",
        )
        col = row.column(align=True)
        # 上下移动按钮
        col.operator("mbm.move_mod_item", text="", icon="TRIA_UP").direction = "UP"
        col.operator("mbm.move_mod_item", text="", icon="TRIA_DOWN").direction = "DOWN"
        col.operator("mbm.add_mod_operator", text="", icon="ADD")
        col.operator("mbm.delete_mod_operator", text="", icon="REMOVE")
        # 添加一个按钮
        layout.operator("mbm.unzip_mods_operator", text="刷新")


# -----------------------------------------------------------------------------
# UIList
# -----------------------------------------------------------------------------

# 定义 UIList 类 ResourcepackList
