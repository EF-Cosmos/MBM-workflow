import bpy
import bmesh
from bpy.props import EnumProperty
import bpy_extras.view3d_utils as view3d_utils
import math


class MBM_OT_BlockBrush(bpy.types.Operator):
    bl_idname = "mbm.block_brush"
    bl_label = "方块笔刷"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vertex_map = {}
        self.target_obj = None
        self.left_mouse_down = False

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {"MIDDLEMOUSE", "WHEELUPMOUSE", "WHEELDOWNMOUSE"}:
            return {"PASS_THROUGH"}

        if event.type == "LEFTMOUSE" and event.value == "PRESS":
            self.left_mouse_down = True
            self.brush_action(context, event)
            return {"RUNNING_MODAL"}

        if event.type == "LEFTMOUSE" and event.value == "RELEASE":
            self.left_mouse_down = False
            return {"RUNNING_MODAL"}

        if event.type == "MOUSEMOVE" and self.left_mouse_down:
            self.brush_action(context, event)
            return {"RUNNING_MODAL"}

        elif event.type in {"RIGHTMOUSE", "ESC"}:
            context.window.cursor_modal_restore()
            self.vertex_map = {}
            self.target_obj = None
            self.left_mouse_down = False
            return {"FINISHED"}

        return {"RUNNING_MODAL"}

    def invoke(self, context, event):
        if context.area.type == "VIEW_3D":
            obj = context.active_object
            if not obj or obj.type != "MESH":
                self.report({"WARNING"}, "请选择一个网格对象")
                return {"CANCELLED"}

            # 检查 blockid 属性是否存在
            if "blockid" not in obj.data.attributes:
                self.report({"WARNING"}, "对象没有 blockid 属性")
                return {"CANCELLED"}

            blockid_attr = obj.data.attributes["blockid"]
            if blockid_attr.domain != "POINT":
                self.report({"WARNING"}, "blockid 属性必须是 POINT 域")
                return {"CANCELLED"}

            # 检查属性数据是否为空
            if not blockid_attr.data or len(blockid_attr.data) == 0:
                self.report(
                    {"WARNING"}, "blockid 属性数据为空，可能已应用几何节点修改器"
                )
                return {"CANCELLED"}

            # 检查几何节点修改器状态
            has_nodes_modifier = any(mod.type == "NODES" for mod in obj.modifiers)
            if has_nodes_modifier:
                self.report({"INFO"}, "检测到几何节点修改器，修改点云会自动更新显示")

            self.target_obj = obj
            self.report({"INFO"}, "构建索引中...")

            mesh = obj.data
            self.vertex_map = {}
            for i, v in enumerate(mesh.vertices):
                coord = (math.floor(v.co.x), math.floor(v.co.y), math.floor(v.co.z))
                self.vertex_map.setdefault(coord, []).append(i)

            self.report(
                {"INFO"}, "方块笔刷已就绪 (左键: 绘制, Shift+左键: 吸管, 右键: 退出)"
            )

            context.window.cursor_modal_set("PAINT_BRUSH")
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            self.report({"WARNING"}, "View3D not found")
            return {"CANCELLED"}

    def _nearest_coord_fallback(self, center_coord, local_location):
        best_coord = center_coord
        best_dist_sq = float("inf")

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    candidate = (
                        center_coord[0] + dx,
                        center_coord[1] + dy,
                        center_coord[2] + dz,
                    )
                    if candidate not in self.vertex_map:
                        continue

                    dist_sq = (
                        (candidate[0] - local_location.x) ** 2
                        + (candidate[1] - local_location.y) ** 2
                        + (candidate[2] - local_location.z) ** 2
                    )
                    if dist_sq < best_dist_sq:
                        best_dist_sq = dist_sq
                        best_coord = candidate

        return best_coord

    def _collect_vertex_indices(self, center_coord, brush_radius):
        indices = []
        radius = max(0, int(brush_radius))

        if radius == 0:
            return list(self.vertex_map.get(center_coord, []))

        radius_sq = radius * radius
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    if dx * dx + dy * dy + dz * dz > radius_sq:
                        continue
                    coord = (
                        center_coord[0] + dx,
                        center_coord[1] + dy,
                        center_coord[2] + dz,
                    )
                    indices.extend(self.vertex_map.get(coord, []))

        return indices

    def brush_action(self, context, event):
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y

        # 获取世界空间的射线
        direction = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

        # 使用 scene.ray_cast 检测 evaluated 对象（实例化后的网格）
        depsgraph = context.evaluated_depsgraph_get()
        result, location, normal, index, obj, matrix = context.scene.ray_cast(
            depsgraph, origin, direction
        )

        if result and obj == self.target_obj:
            # 将击中位置和法线转换到对象局部空间
            matrix_inv = self.target_obj.matrix_world.inverted()
            local_location = matrix_inv @ location
            local_normal = matrix_inv.to_3x3() @ normal  # 法线只需要旋转，不需要平移

            epsilon = 0.001
            if local_normal.length_squared > 0:
                adjusted_location = local_location - local_normal.normalized() * epsilon
            else:
                adjusted_location = local_location

            block_coord = (
                math.floor(adjusted_location.x),
                math.floor(adjusted_location.y),
                math.floor(adjusted_location.z),
            )

            if block_coord not in self.vertex_map:
                block_coord = self._nearest_coord_fallback(
                    block_coord, adjusted_location
                )

            brush_radius = context.scene.my_properties.brush_radius
            target_indices = self._collect_vertex_indices(block_coord, brush_radius)

            if target_indices:
                is_sample = event.shift
                blockid_data = self.target_obj.data.attributes["blockid"].data

                if is_sample:
                    sample_index = target_indices[0]
                    if sample_index < len(blockid_data):
                        val = blockid_data[sample_index].value
                        self.report({"INFO"}, f"吸取 ID: {val}")
                        try:
                            context.scene.my_properties.brush_block_enum = str(val)
                        except (TypeError, ValueError):
                            self.report({"WARNING"}, "吸管写入枚举失败")
                    else:
                        self.report({"WARNING"}, f"索引 {sample_index} 超出范围")
                else:
                    try:
                        target_id = int(context.scene.my_properties.brush_block_enum)
                        changed = False
                        for vertex_index in target_indices:
                            if vertex_index < len(blockid_data):
                                blockid_data[vertex_index].value = target_id
                                changed = True
                        if changed:
                            self.target_obj.data.update_tag()  # 标记数据更新，触发几何节点重新计算
                    except ValueError:
                        self.report({"WARNING"}, "无效的目标方块 ID")


def register():
    bpy.utils.register_class(MBM_OT_BlockBrush)


def unregister():
    bpy.utils.unregister_class(MBM_OT_BlockBrush)
