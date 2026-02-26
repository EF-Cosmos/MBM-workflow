import ast
import json

import bpy


BLOCKS_TEXT_NAME = "Blocks.py"


def get_block_map_text(create=False):
    text_data = bpy.data.texts.get(BLOCKS_TEXT_NAME)
    if text_data is None and create:
        text_data = bpy.data.texts.new(BLOCKS_TEXT_NAME)
    return text_data


def parse_block_map(raw_text):
    content = (raw_text or "").strip()
    if not content:
        return {}

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        try:
            data = ast.literal_eval(content)
        except (ValueError, SyntaxError) as exc:
            raise ValueError(f"Invalid {BLOCKS_TEXT_NAME} content") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{BLOCKS_TEXT_NAME} must be a dict")

    return data


def load_block_map(text_data):
    return parse_block_map(text_data.as_string())


def load_block_map_safe(text_data, default=None):
    if default is None:
        default = {}
    try:
        return load_block_map(text_data)
    except ValueError:
        return default


def dump_block_map(block_map, sort_by_value=False):
    items = block_map.items()
    if sort_by_value:
        items = sorted(items, key=lambda item: item[1])

    data = {}
    for key, value in items:
        try:
            normalized_value = int(value)
        except (TypeError, ValueError):
            normalized_value = value
        data[str(key)] = normalized_value

    return json.dumps(data, ensure_ascii=False, indent=4) + "\n"


def save_block_map(text_data, block_map, sort_by_value=False):
    text_data.clear()
    text_data.write(dump_block_map(block_map, sort_by_value=sort_by_value))
