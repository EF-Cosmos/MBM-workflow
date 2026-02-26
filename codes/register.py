import bpy
import re
from .block import block
from .blockstates import get_model
from .block_map_store import get_block_map_text, load_block_map_safe, save_block_map

def create_or_clear_collection(collection_name):
    # 检查集合是否已存在
    if collection_name in bpy.data.collections:
        existing_collection = bpy.data.collections.get(collection_name)
        try:
            bpy.context.scene.collection.children.link(existing_collection)
        except:
            pass

    else:
        # 创建一个新的集合
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
        
def register_blocks(ids):
    collection_name = "Blocks"
    create_or_clear_collection(collection_name)
    collection = bpy.data.collections.get(collection_name)
    collection.hide_render = False
    collection.hide_viewport = False
    
    # 尝试从 .blend 文件中获取文本数据
    text_data = get_block_map_text(create=True)

    # 从文本数据中读取字典 id_map
    id_map = load_block_map_safe(text_data, default={})

    # 更新 id_map
    if id_map and collection.objects: # 如果id_map不为空
        next_id = max(id_map.values()) + 1
    else:
        next_id=0
        id_map={}
        filename=str(next_id)+"#"+str("minecraft:air")
        textures,elements,rotation,uvlock =get_model("minecraft:air")
        position = [0, 0, 0]
        has_air = [True, True, True, True, True, True]
        obj=block(textures, elements, position,rotation, filename, has_air,collection,uvlock)
        obj["文本数据"] = text_data
        obj["id"] = "minecraft:air"
        id_map["minecraft:air"] = next_id
        next_id =1
    if ids != None and ids!=[]:
        ids = [id for id in ids if id not in id_map]
        for id in ids:
            filename=str(next_id)+"#"+str(id)
            # 获取模型数据
            textures, elements, rotation, uvlock = get_model(id)
            position = [0, 0, 0]
            has_air = [True, True, True, True, True, True]

            # 创建 block 对象
            obj=block(textures, elements, position, rotation, filename, has_air, collection, uvlock)
            obj["文本数据"] = text_data
            obj["id"] = id
            id = re.escape(id)
            id_map[id] = next_id
            next_id += 1  # 修改这里，确保每次迭代都递增 next_id

    # 将更新后的 id_map 字典内容以分行形式写入到当前 .blend 文件中的文本数据中
    save_block_map(text_data, id_map)

    collection.hide_render = True
    collection.hide_viewport = True
    return id_map


def registered_blocks(id_map):
    collection_name = "Blocks"
    create_or_clear_collection(collection_name)
    collection = bpy.data.collections.get(collection_name)
    collection.hide_render = False
    collection.hide_viewport = False
    
    for id in id_map:
        # 获取模型数据
        textures, elements, rotation, uvlock = get_model(id)
        position = [0, 0, 0]
        has_air = [True, True, True, True, True, True]
        filename=str(id_map[id])+"#"+str(id)
        # 创建 block 对象
        obj=block(textures, elements, position, rotation, filename, has_air, collection, uvlock)

    collection.hide_render = True
    collection.hide_viewport = True
    return id_map
