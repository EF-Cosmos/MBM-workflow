import bpy
import os
import time
import pickle
import re

from .block import block
from .functions.get_data import get_all_data
from .classification_files.block_type import exclude
from .schem import schem_chunk,schem_liquid,schem,remove_brackets,separate_vertices_by_blockid,separate_vertices_by_chunk,litematic_to_mesh
from .functions.mesh_to_mc import create_mesh_from_dictionary,create_or_clear_collection
from .register import register_blocks
from . import dependency_manager
import json
import threading

# 使用依赖管理器导入
amulet = dependency_manager.amulet
amulet_nbt = dependency_manager.amulet_nbt


class ImportBlock(bpy.types.Operator):
    """导入方块"""
    bl_label = "导入方块"
    bl_idname = 'mbm.import_block'

    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.json文件
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}) # type: ignore

    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    def execute(self, context):
        id_list = []
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            # 使用 for 循环逐级向上查找，直到找到名为 'blockstates' 的目录
            dir_name = os.path.dirname(self.filepath)
            while os.path.basename(dir_name) != 'blockstates':
                dir_name = os.path.dirname(dir_name)
            # 获取 'blockstates' 目录的上一级目录名作为命名空间
            namespace = os.path.basename(os.path.dirname(dir_name)) + ":"
            # 读取JSON文件
            with open(self.filepath, 'r') as file:
                data = json.load(file)
            
            # 提取所需内容
            variants = data.get("variants", {})
            # 提取所需内容
            multipart = data.get("multipart", [])
            
            if variants != {}:
                for key, value in variants.items():
                    if key !="":
                        id_list.append(namespace+os.path.basename(self.filepath).replace(".json","") + "[" + key + "]")
                    else:
                        id_list.append(namespace+os.path.basename(self.filepath).replace(".json",""))
            if multipart !=[]:
                # 获取所有when可能的属性
                all_when_keys = set()
                for entry in multipart:
                    when_data = entry.get("when", {})
                    all_when_keys.update(when_data.keys())

                # 遍历multipart数组
                for i, entry in enumerate(multipart):
                    when_data = entry.get("when", {})

                    # 补充默认为False的属性
                    for key in all_when_keys:
                        if key not in when_data:
                            when_data[key] = "false"

                    # 将when数据按字母顺序排序
                    sorted_when_data = dict(sorted(when_data.items()))

                    # 生成[]内的字符串
                    when_string = ','.join([f'{key}={value}' for key, value in sorted_when_data.items()])

                    # 构建文件名
                    filename = os.path.basename(self.filepath).replace(".json","") + "[" + when_string + "]"

                    # 添加到结果列表
                    id_list.append(namespace+filename)
        register_blocks(id_list)


            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class ImportNBT(bpy.types.Operator):
    bl_idname = "mbm.import_nbt"
    bl_label = "导入.nbt文件"
    
    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.nbt文件
    filter_glob: bpy.props.StringProperty(default="*.nbt", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore
    # 定义操作的执行函数
    def execute(self, context):
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            # 获取文件路径
            filepath = self.filepath
            filename = os.path.basename(filepath)
            data = amulet_nbt.load(filepath)
            
            blocks =data["blocks"]
            entities = data["entities"]
            if "palette" in data:
                palette = data["palette"]
            elif "palettes" in data:
                palette = data["palettes"][0]
            

            size = data["size"]
            d = {}  

            for block in blocks:
                pos_tags = block['pos']  
                pos = tuple(tag.value for tag in pos_tags)  
                state = block['state'].value 
                block_name = palette[state]['Name'].value if 'Name' in palette[state] else palette[state]['nbt']['name'].value
                if 'Properties' in palette[state]:
                    block_state = palette[state]['Properties'].value
                    block_state = ','.join([f'{k}={v}' for k, v in block_state.items()])
                elif 'nbt' in palette[state] and 'name' in palette[state]['nbt']:
                    block_state = palette[state]['nbt']['name'].value
                    block_state = ','.join([f'{k}={v}' for k, v in block_state.items()])
                else:
                    block_state = None
                if block_name !="minecraft:air":
                    if block_state is not None:
                        d[(pos[0],pos[2],pos[1])] = str(block_name)+"["+block_state+"]"
                    else:
                        d[(pos[0],pos[2],pos[1])] = block_name

            #普通方法，有面剔除，速度较慢。
            # start_time = time.time()
            # nbt(d,filename)
            # end_time = time.time()
            #print("代码块执行时间：", end_time - start_time, "秒")

            #py+几何节点做法，无面剔除，但速度快。
            create_mesh_from_dictionary(d,filename.replace(".nbt",""))
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# 定义一个导入.schem文件的操作类
class ImportSchem(bpy.types.Operator):
    bl_idname = "mbm.import_schem"
    bl_label = "导入.schem文件"
    
    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    # 定义一个属性来过滤文件类型，只显示.schem文件
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore

    # 定义操作的执行函数
    def execute(self, context):
        for f in self.files:
            # 从文件路径中提取文件名            
            self.filepath=str(str(os.path.dirname(self.filepath))+"\\"+str(f.name))
            name=os.path.basename(self.filepath)
            folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+ "/schemcache"
            file_names = os.listdir(folder_path)
            for file_name in file_names:
                file_path = os.path.join(folder_path, file_name)
                os.remove(file_path)
            level = amulet.load_level(self.filepath)
            chunks = [list(point) for point in level.bounds("main").bounds]
            # 使用公共 API 加载 NBT 数据
            with open(self.filepath, "rb") as f:
                nbt_data = amulet_nbt.load(f)
            
            #data=nbt_data["BlockEntities"][0]["data"]["data"]
            # 解析数据为坐标点
            # coordinates = []
            # for i in range(0, len(data), 3):
            #     x = data[i]
            #     y = data[i + 1]
            #     z = data[i + 2]
            #     coordinates.append((x, y, z))

            # # 构建字典
            # coordinates_dict = {f"Point {index + 1}": point for index, point in enumerate(coordinates)}

            size = {
                "x":int(nbt_data["Width"]),
                "y":int(nbt_data["Height"]),
                "z":int(nbt_data["Length"])
            }
            
            # 设置图片的大小和颜色
            image_width = int(size["z"])
            image_height = int(size["x"])
            default_color = (0.47, 0.75, 0.35, 1.0)  # RGBA颜色，对应#79c05a

            # 创建一个新的图片
            image = bpy.data.images.new("colormap", width=image_width, height=image_height)
            image.use_fake_user = True

            def set_default_color(image, image_width, image_height, default_color):
                # 设置默认颜色
                for y in range(image_height):
                    for x in range(image_width):
                        pixel_index = (y * image_width + x) * 4  # RGBA每个通道都是4个值
                        image.pixels[pixel_index : pixel_index + 4] = default_color
            # 创建一个新的线程来执行 set_default_color 函数
            thread = threading.Thread(target=set_default_color, args=(image, image_width, image_height, default_color))
            # 启动新的线程
            thread.start()
            start_time = time.time()

            obj=schem(level,chunks,False,name)
            if context.scene.separate_vertices_by_blockid ==True:
                separate_vertices_by_blockid(obj)
            elif context.scene.separate_vertices_by_chunk ==True:
                separate_vertices_by_chunk(obj)
            schem_liquid(level,chunks)

            end_time = time.time()
            execution_time = end_time - start_time

            print("程序运行时间为：", execution_time, "秒")
            materials = bpy.data.materials
            for material in materials:
                try:
                    node_tree = material.node_tree
                    nodes = node_tree.nodes
                    for node in nodes:
                        if node.type == 'TEX_IMAGE':
                            if node.name == '色图':
                                node.image = bpy.data.images.get("colormap")
                except Exception as e:
                    print("材质出错了:", e)

            

        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ReloadBlocks(bpy.types.Operator):
    """重载失效或空的方块缓存，使插件重新尝试读取模型"""
    bl_idname = "mbm.reload_blocks"
    bl_label = "重载失效方块"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        text_data = bpy.data.texts.get("Blocks.py")
        if not text_data:
            self.report({'WARNING'}, "未找到 Blocks.py 数据")
            return {'FINISHED'}

        try:
            id_map = eval(text_data.as_string())
        except Exception as e:
            self.report({'ERROR'}, f"无法解析方块数据: {e}")
            return {'CANCELLED'}

        collection = bpy.data.collections.get("Blocks")
        if not collection:
            self.report({'WARNING'}, "未找到 Blocks 集合")
            return {'FINISHED'}

        to_remove = []
        # 不需要重载的方块列表（确实是空的或特殊的）
        skip_list = ["minecraft:air", "minecraft:barrier", "minecraft:structure_void", "minecraft:light"]

        for id_str, index in id_map.items():
            if id_str in skip_list:
                continue
            
            # 对象命名格式: "index#id"
            # 查找以 "index#" 开头的对象
            target_obj = None
            prefix = f"{index}#"
            
            found = False
            for obj in collection.objects:
                if obj.name.startswith(prefix):
                    target_obj = obj
                    found = True
                    break
            
            is_broken = False
            if not found:
                # 记录在案但对象丢失 -> 需要重置
                is_broken = True
            elif target_obj and hasattr(target_obj.data, 'vertices') and len(target_obj.data.vertices) == 0:
                # 有对象但没有顶点数据 -> 可能是之前导入失败生成的空对象
                is_broken = True
                bpy.data.objects.remove(target_obj, do_unlink=True)
            
            if is_broken:
                to_remove.append(id_str)

        # 更新 id_map
        if to_remove:
            for id_str in to_remove:
                if id_str in id_map:
                    del id_map[id_str]
            
            # 写回 Blocks.py
            text_data.clear()
            text_data.write("{\n")
            # 保持排序以便查看
            for key, value in sorted(id_map.items(), key=lambda item: item[1]):
                text_data.write(f"    \"{key}\": {value},\n")
            text_data.write("}\n")
            
            context.view_layer.update()
            self.report({'INFO'}, f"已清理 {len(to_remove)} 个失效方块记录。下次导入时将重新加载。")
        else:
            self.report({'INFO'}, "未发现需要重载的失效方块。")

        return {'FINISHED'}


# 导入.litematic文件的操作类
class ImportLitematic(bpy.types.Operator):
    bl_idname = "mbm.import_litematic"
    bl_label = "导入.litematic文件"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.litematic", options={'HIDDEN'}) # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup) # type: ignore


    def _safe_load_nbt(self, context):
        """Safe wrapper to define Region.from_nbt before litemapy loads"""
         # Monkey-patch litemapy's Region.from_nbt to handle list index out of range errors
        try:
             # We need to import litemapy here (it's already loaded via dependency_manager but we need the module object)
            from . import dependency_manager
            import math
            litemapy_mod = dependency_manager.litemapy

            
            # The error 'list index out of range' in Region.from_nbt usually happens at:
            # region.__blocks[x][y][z] = bit_array[ind]
            # or
            # del region.__palette[0]
            
            # Let's verify if we can access schem.py's Region class
            if hasattr(litemapy_mod.schematic, 'Region'):
                RegionClass = litemapy_mod.schematic.Region
                
                # Check if we already patched it
                if getattr(RegionClass, '_is_patched_safe', False):
                    return

                original_from_nbt = RegionClass.from_nbt

                @staticmethod
                def safe_from_nbt(nbt):
                    try:
                        return original_from_nbt(nbt)
                    except IndexError as e:
                        # If list index out of range happens, try to inspect why or return a dummy region
                        # But returning dummy region might break Schematic.from_nbt structure.
                        # Instead, we want to fix the data if possible.
                        # Since we can't easily fix the NBT data on the fly without parsing logic...
                        
                        # Let's try a robust implementation of reading the region
                        # This requires re-implementing part of Region.from_nbt
                        
                        print(f"Litematic Fix: Detected malformed region data ({e}). Attempting to recover...")
                        
                        # Re-impl minimal parts
                        pos = nbt["Position"]
                        x, y, z = int(pos["x"]), int(pos["y"]), int(pos["z"])
                        size = nbt["Size"]
                        w, h, l = int(size["x"]), int(size["y"]), int(size["z"])
                        
                        region = RegionClass(x, y, z, w, h, l)
                        
                        # Populate palette safely
                        # Access private member if needed, or use public methods if available?
                        # Region attributes are __palette (private).
                        # We need to use name mangling: _Region__palette
                        
                        palette_list = getattr(region, "_Region__palette")
                        if len(palette_list) > 0 and palette_list[0].id == "minecraft:air":
                             del palette_list[0]
                        
                        from . import dependency_manager
                        BlockState = dependency_manager.litemapy.minecraft.BlockState
                        
                        for block_nbt in nbt["BlockStatePalette"]:
                             try:
                                block = BlockState.from_nbt(block_nbt)
                                palette_list.append(block)
                             except Exception as block_err:
                                print(f"Skipping bad block in palette: {block_err}")
                                # Add AIR to keep index alignment if possible, or just skip
                                palette_list.append(BlockState("minecraft:air"))

                        # Skip entities for now to minimize errors
                        
                        # Process blocks
                        blocks = nbt["BlockStates"]
                        nbits = max(math.ceil(math.log(len(palette_list), 2)), 2)
                        
                        LitematicaBitArray = dependency_manager.litemapy.storage.LitematicaBitArray
                        bit_array = LitematicaBitArray.from_nbt_long_array(blocks, abs(w*h*l), nbits)
                        
                        block_grid = getattr(region, "_Region__blocks")
                        
                        # Safe assignment
                        total_blocks = abs(w * h * l)
                        palette_len = len(palette_list)
                        
                        for i in range(total_blocks):
                            # Calc coords
                            # ind = (y * abs(width * length)) + z * abs(width) + x
                            # We can just iterate linearly if we match the loop order
                            pass
                            
                        # The original code loop:
                        # for x in range(abs(width)):
                        #     for y in range(abs(height)):
                        #         for z in range(abs(length)):
                        #             ind = (y * abs(width * length)) + z * abs(width) + x
                        #             bit_array[ind]
                        
                        # If bit_array[ind] fails, it means ind >= len(bit_array).
                        # If assigning fails, it means block_grid is not right shape (unlikely if init correct)
                        # Or palette index is out of range? block_grid stores indices.
                        
                        width_abs, height_abs, length_abs = abs(w), abs(h), abs(l)
                        
                        # Using try-except inside loop is slow but safe
                        for x_i in range(width_abs):
                            for y_i in range(height_abs):
                                for z_i in range(length_abs):
                                    ind = (y_i * width_abs * length_abs) + z_i * width_abs + x_i
                                    try:
                                        val = bit_array[ind]
                                        # Clamp value to palette range
                                        if val >= palette_len:
                                            val = 0 # Air
                                        block_grid[x_i][y_i][z_i] = val
                                    except IndexError:
                                        block_grid[x_i][y_i][z_i] = 0 # Default/Air

                        return region

                RegionClass.from_nbt = safe_from_nbt
                setattr(RegionClass, '_is_patched_safe', True)
                print("Litemapy patched for safe loading.")
                
        except Exception as e:
            print(f"Failed to patch litemapy: {e}")

    def execute(self, context):
        from . import dependency_manager
        import math
        
        # Apply patch before loading
        self._safe_load_nbt(context)

        litemapy = dependency_manager.litemapy


        if litemapy is None:
            self.report({'ERROR'}, "litemapy 库未安装")
            return {'CANCELLED'}

        for f in self.files:
            self.filepath = str(os.path.dirname(self.filepath)) + "\\" + str(f.name)
            base_filename = os.path.basename(self.filepath).replace(".litematic", "")

            try:
                schem = litemapy.Schematic.load(self.filepath)
            except Exception as e:
                self.report({'ERROR'}, f"无法加载文件: {str(e)}")
                return {'CANCELLED'}

            if not schem.regions:
                self.report({'WARNING'}, "文件不包含任何区域")
                return {'CANCELLED'}

            region_count = len(schem.regions)

            for region_name, region in schem.regions.items():
                # 尝试修复 invalid index issues (导致 list index out of range)
                try:
                    # 访问私有属性 (name mangling: Region -> _Region)
                    blocks = getattr(region, "_Region__blocks", None)
                    palette = getattr(region, "_Region__palette", None)
                    
                    if blocks is not None and palette is not None:
                        import numpy as np
                        p_len = len(palette)
                        if p_len > 0 and isinstance(blocks, np.ndarray):
                             # 检查是否有超出调色板范围的索引
                             # 注意: numpy.any() 可能会比较慢，但比起崩溃要好
                             if np.any(blocks >= p_len):
                                 print(f"[Import Fix] 在区域 '{region_name}' 中发现无效的方块索引。正在修正...")
                                 # 将无效索引重置为 0 (通常是 minecraft:air)
                                 blocks[blocks >= p_len] = 0
                except Exception as e:
                    print(f"[Import Fix] 尝试修复区域数据时出错: {e}")

                # 处理单个区域数据
                block_dict, bounds = self._process_single_region(region, region_name)

                if not block_dict:
                    print(f"区域 '{region_name}' 不包含任何方块，跳过")
                    continue

                # 生成对象名称：单区域使用原文件名，多区域添加区域后缀
                if region_count == 1:
                    obj_filename = base_filename
                else:
                    obj_filename = f"{base_filename}_{region_name}"

                # 创建网格对象
                obj = litematic_to_mesh(block_dict, bounds, obj_filename)

                # 应用可选的顶点分离
                if context.scene.separate_vertices_by_blockid:
                    separate_vertices_by_blockid(obj)
                elif context.scene.separate_vertices_by_chunk:
                    separate_vertices_by_chunk(obj)

            print(f"成功导入 {region_count} 个区域")

        return {'FINISHED'}

    def _process_single_region(self, region, region_name):
        """处理单个区域，返回方块字典和边界"""
        from .classification_files.block_type import exclude

        block_dict = {}
        all_coords = []

        for x, y, z in region.block_positions():
            block = region[x, y, z]

            if block.id == "minecraft:air":
                continue

            block_str = self._format_block_state(block)
            base_block = self._remove_brackets(block_str)

            if base_block in exclude:
                continue

            # 使用区域相对坐标
            block_dict[(x, y, z)] = block_str
            all_coords.append((x, y, z))

        # 计算边界
        if all_coords:
            min_coords = tuple(min(coords[i] for coords in all_coords) for i in range(3))
            max_coords = tuple(max(coords[i] for coords in all_coords) for i in range(3))
        else:
            min_coords = (0, 0, 0)
            max_coords = (0, 0, 0)

        return block_dict, (min_coords, max_coords)

    def _format_block_state(self, block):
        """格式化方块状态字符串"""
        block_str = block.id
        if hasattr(block, 'properties') and block.properties:
            props = ','.join(f"{k}={v}" for k, v in block.properties.items())
            block_str = f"{block.id}[{props}]"
        return block_str

    def _remove_brackets(self, input_string):
        """移除方括号内容获取基础方块名"""
        output_string = ""
        inside_brackets = False
        for char in input_string:
            if char == '[':
                inside_brackets = True
            elif char == ']' and inside_brackets:
                inside_brackets = False
            elif not inside_brackets:
                output_string += char
        return output_string

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


#多进程结束后导入模型
class MultiprocessImport(bpy.types.Operator):
    bl_idname = "mbm.multiprocess_import"
    bl_label = "导入.schem文件"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        VarCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/var.pkl"
        with open(VarCachePath, 'rb') as file:
            schempath,chunks,name,x_list,processnum = pickle.load(file)
        level = amulet.load_level(schempath)
        schem(level,chunks,True,name)

        materials = bpy.data.materials
        for material in materials:
            try:
                node_tree = material.node_tree
                nodes = node_tree.nodes
                for node in nodes:
                    if node.type == 'TEX_IMAGE':
                        if node.name == '色图':
                            node.image = bpy.data.images.get("colormap")
            except Exception as e:
                print("材质出错了:", e)

        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#每个进程分别处理一个区块
class MultiprocessSchem(bpy.types.Operator):
    bl_idname = "mbm.import_schem_mp"
    bl_label = "导入.schem文件"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        VarCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/var.pkl"
        with open(VarCachePath, 'rb') as file:
            schempath,chunks,name,x_list,processnum = pickle.load(file)
        level = amulet.load_level(schempath)
        schem_chunk(level,chunks,x_list,name)

        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    

class ImportSchemLiquid(bpy.types.Operator):
    bl_idname = "mbm.import_schem_liquid"
    bl_label = "导入.schem文件"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.schem", options={'HIDDEN'}) # type: ignore

    def execute(self, context):
        VarCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/var.pkl"
        with open(VarCachePath, 'rb') as file:
            chunks,mp_chunks,schempath,interval,processnum = pickle.load(file)
        level = amulet.load_level(schempath)
        schem_liquid(level,chunks)
        ModelCachePath = bpy.utils.script_path_user() + "/addons/MBM_Workflow/schemcache/liquid.blend"
        bpy.ops.wm.save_as_mainfile(filepath=ModelCachePath)
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class Importjson(bpy.types.Operator):
    """导入选定的json文件"""
    bl_idname = "mbm.import_json"
    bl_label = "导入json文件"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore

    def execute(self, context):
        # 检查文件路径是否有效
        if os.path.isfile(self.filepath) and self.filepath.endswith(".json"):
            # 获取文件名
            filename = os.path.basename(self.filepath)
            textures, elements,parent = get_all_data(os.path.dirname(self.filepath)+"\\", filename)
            position = [0, 0, 0]
            has_air = [True, True, True, True, True, True]
            block(textures, elements, position,[0,0,0], filename, has_air)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "请选择有效的.json文件")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # 打开文件选择对话框
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class SNA_AddonPreferences_F35F8(bpy.types.AddonPreferences):
    bl_idname = 'MBM_Workflow'
    sna_processnumber: bpy.props.IntProperty(name='ProcessNumber', description='最大进程数，同时处理这么多个区块', default=6, subtype='NONE', min=1, max=64) # type: ignore
    sna_intervaltime: bpy.props.FloatProperty(name='IntervalTime', description='处理完每个区块，间隔一段时间再导入进来。较小值减少总时间；较大值能避免blender卡住，边导边用', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=10.0, step=3, precision=1) # type: ignore
    sna_minsize: bpy.props.IntProperty(name='MinSize', description='超过这个数就会启用多进程分区块导入', default=1000000, subtype='NONE', min=1000, max=99999999) # type: ignore

    def draw(self, context):
        if not (False):
            layout = self.layout 


class SNA_OT_My_Generic_Operator_A38B8(bpy.types.Operator):
    bl_idname = "sna.my_generic_operator_a38b8"
    bl_label = "刷新"
    bl_description = "自动设置以下参数"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        Variable = None
        Variable=int(os.cpu_count()/2)
        bpy.context.preferences.addons['MBM_Workflow'].preferences.sna_processnumber = Variable
        bpy.context.preferences.addons['MBM_Workflow'].preferences.sna_intervaltime = 1
        bpy.context.preferences.addons['MBM_Workflow'].preferences.sna_minsize = 1000000
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


    
# class SelectArea(bpy.types.Operator):
#     """选择区域（性能有问题）"""
#     bl_label = "选择区域"
#     bl_idname = 'mbm.select'
    
#     def execute(self, context):
#         # 获取当前场景的名称
#         current_scene = bpy.context.scene.name
#         # 如果场景名称不为"地图"，则返回
#         if current_scene != "地图":
#             button_callback(self, context,"地图仍未创建！")
#             return {'CANCELLED'}
#         # 检查当前场景是否已经有名为"Map"的集合
#         existing_collections = bpy.data.collections.values()
#         for coll in existing_collections:
#             if coll.name == "Map":
#                 button_callback(self, context,"已经存在选择框！(如果你删除了一些东西请连同集合一起删除）")
#                 return {'CANCELLED'}
#         # 获取当前文件的路径
#         current_path = os.path.dirname(os.path.abspath(__file__))
#         # 拼接路径和文件名
#         filepath = os.path.join(current_path, "blend_files","Map.blend")
#         # 从文件中加载名为"Map"的集合
#         with bpy.data.libraries.load(filepath) as (data_from, data_to):
#             data_to.collections = ["Map"]
#         # 将集合链接到当前场景
#         for coll in data_to.collections:
#             if coll is not None:
#                 bpy.context.scene.collection.children.link(coll)
#         return {'FINISHED'}

class ImportWorld(bpy.types.Operator):
    """导入世界(性能有问题)"""
    bl_label = "导入世界"
    bl_idname = 'mbm.import_world'

    current_chunk_index = 0  # 当前处理的区块索引

    # 定义一个属性来存储文件路径
    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore


    def execute(self, context):
        # 获取配置的版本
        platform = context.scene.mc_platform
        version = (
            context.scene.mc_version_major,
            context.scene.mc_version_minor,
            context.scene.mc_version_patch
        )

        filename = "world"
        level = amulet.load_level(self.filepath)
        min_coords=context.scene.min_coordinates
        max_coords=context.scene.max_coordinates
        # 创建一个新的网格对象
        mesh = bpy.data.meshes.new(name=filename)
        mesh.attributes.new(name='blockid', type="INT", domain="POINT")
        mesh.attributes.new(name='biome', type="FLOAT_COLOR", domain="POINT")
        obj = bpy.data.objects.new(filename, mesh)

        # 将对象添加到场景中
        scene = bpy.context.scene
        scene.collection.objects.link(obj)
        # 创建一个新的集合
        collection_name="Blocks"
        create_or_clear_collection(collection_name)
        collection =bpy.data.collections.get(collection_name)
        nodetree_target = "Schem"

        #导入几何节点
        try:
            nodes_modifier.node_group = bpy.data.node_groups[collection_name]
        except:
            file_path =bpy.context.scene.geometrynodes_blend_path
            inner_path = 'NodeTree'
            object_name = nodetree_target
            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, object_name),
                directory=os.path.join(file_path, inner_path),
                filename=object_name
            )
        # 创建顶点和顶点索引
        vertices = []
        ids = []  # 存储顶点id
        # 遍历范围内所有的坐标
        for x in range(min_coords[0], max_coords[0] + 1):
            for y in range(min_coords[1], max_coords[1] + 1):
                for z in range(min_coords[2], max_coords[2] + 1):
                    # 获取坐标处的方块       
                    blc = level.get_version_block(x, y, z, "minecraft:overworld", (platform, version))
                    id =blc[0]
                    if isinstance(id,amulet.api.block.Block):
                        id = str(id).replace('"', '')
                        result = remove_brackets(id) 
                        if result not in exclude:  
                            # 将字符串id映射到数字，如果id已经有对应的数字id，则使用现有的数字id
                            vertices.append((x-min_coords[0],-(z-min_coords[2]),y-min_coords[1]))
                            # 将字符串id转换为相应的数字id
                            ids.append(id)

        id_map=register_blocks(list(set(ids)))
        # 将顶点和顶点索引添加到网格中
        mesh.from_pydata(vertices, [], [])
        for i, item in enumerate(obj.data.attributes['blockid'].data):
            id =re.escape(ids[i])
            item.value=id_map[id]
        #群系上色
        for i, item in enumerate(obj.data.attributes['biome'].data):
            item.color[:]=(0.149,0.660,0.10,0.00)
        # 设置顶点索引
        mesh.update()
        
        # 检查是否有节点修改器，如果没有则添加一个
        has_nodes_modifier = False
        for modifier in obj.modifiers:
            if modifier.type == 'NODES':
                has_nodes_modifier = True
                break
        if not has_nodes_modifier:
            obj.modifiers.new(name="Schem",type="NODES")
        nodes_modifier=obj.modifiers[0]
        
        # 复制 Schem 节点组并重命名为 CollectionName
        try:
            original_node_group = bpy.data.node_groups['Schem']
            new_node_group = original_node_group.copy()
            new_node_group.name = collection_name
        except KeyError:
            print("error")
        #设置几何节点        
        nodes_modifier.node_group = bpy.data.node_groups[collection_name]
        bpy.data.node_groups[collection_name].nodes["集合信息"].inputs[0].default_value = collection
        nodes_modifier.show_viewport = True    
        level.close()
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


classes=[ImportBlock,ImportSchem,ImportLitematic,MultiprocessSchem,Importjson,ImportWorld,#SelectArea,
         ImportNBT,SNA_AddonPreferences_F35F8,SNA_OT_My_Generic_Operator_A38B8,ImportSchemLiquid,MultiprocessImport,
         ReloadBlocks]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    