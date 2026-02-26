# -*- coding: utf-8 -*-
"""
编译翻译文件

此脚本将 .po 文件编译为 .mo 文件，供 Blender 使用。
使用纯 Python 实现，不需要安装 gettext 工具。

用法：
    python compile_translations.py
"""
import os
import struct

def parse_po(po_path):
    """解析 .po 文件，返回翻译字典"""
    translations = {}
    current_msgid = ''
    current_msgstr = ''
    current_msgctxt = ''
    in_msgid = False
    in_msgstr = False
    in_msgctxt = False

    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue

            # 处理 msgctxt
            if line.startswith('msgctxt'):
                in_msgctxt = True
                in_msgid = False
                in_msgstr = False
                # 提取 msgctxt 内容
                if current_msgid or current_msgstr:
                    # 保存之前的条目
                    key = current_msgctxt + '|' + current_msgid if current_msgctxt else current_msgid
                    translations[key] = current_msgstr
                current_msgctxt = line[7:].strip().strip('"')
                current_msgid = ''
                current_msgstr = ''
                continue

            # 处理 msgid
            if line.startswith('msgid'):
                in_msgid = True
                in_msgstr = False
                in_msgctxt = False
                # 提取 msgid 内容
                if current_msgid or current_msgstr:
                    # 保存之前的条目
                    key = current_msgctxt + '|' + current_msgid if current_msgctxt else current_msgid
                    translations[key] = current_msgstr
                current_msgid = line[6:].strip().strip('"')
                current_msgstr = ''
                continue

            # 处理 msgstr
            if line.startswith('msgstr'):
                in_msgstr = True
                in_msgid = False
                in_msgctxt = False
                # 提取 msgstr 内容
                current_msgstr = line[6:].strip().strip('"')
                continue

            # 处理多行字符串
            if line.startswith('"') and line.endswith('"'):
                content = line[1:-1]
                if in_msgid:
                    current_msgid += content
                elif in_msgstr:
                    current_msgstr += content
                elif in_msgctxt:
                    current_msgctxt += content

        # 保存最后一个条目
        if current_msgid or current_msgstr:
            key = current_msgctxt + '|' + current_msgid if current_msgctxt else current_msgid
            translations[key] = current_msgstr

    return translations

def create_mo_file(translations, mo_path):
    """创建 .mo 二进制文件"""
    # 创建翻译键值对列表
    keys = []
    values = []

    for key, value in translations.items():
        keys.append(key.encode('utf-8'))
        values.append(value.encode('utf-8'))

    # 计算偏移量
    keyoffsets = []
    valueoffsets = []

    offset = 0
    for key in keys:
        keyoffsets.append((len(key), offset))
        offset += len(key) + 1  # +1 for null terminator

    for value in values:
        valueoffsets.append((len(value), offset))
        offset += len(value) + 1  # +1 for null terminator

    # 写入 .mo 文件
    with open(mo_path, 'wb') as f:
        # MO 文件头
        f.write(struct.pack('<I', 0x950412de))  # 魔术数字
        f.write(struct.pack('<I', 0))           # 版本号
        f.write(struct.pack('<I', len(keys)))   # 字符串数量
        f.write(struct.pack('<I', 28))          # 键偏移表起始位置
        f.write(struct.pack('<I', 28 + len(keys) * 8))  # 值偏移表起始位置
        f.write(struct.pack('<I', 0))           # 哈希表大小
        f.write(struct.pack('<I', 0))           # 哈希表偏移

        # 写入键偏移表
        for length, offset in keyoffsets:
            f.write(struct.pack('<II', length, offset))

        # 写入值偏移表
        for length, offset in valueoffsets:
            f.write(struct.pack('<II', length, offset))

        # 写入键和值
        for key in keys:
            f.write(key)
            f.write(b'\x00')

        for value in values:
            f.write(value)
            f.write(b'\x00')

def compile_po_to_mo(po_path, mo_path):
    """将 .po 文件编译为 .mo 文件"""
    try:
        translations = parse_po(po_path)
        create_mo_file(translations, mo_path)
        print(f"[OK] Compiled: {po_path} -> {mo_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to compile: {po_path}")
        print(f"  Reason: {e}")
        return False

def main():
    """编译所有翻译文件"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    locales_dir = os.path.join(script_dir, 'locales')

    print("Compiling translation files...")
    print("=" * 50)

    for locale in ['zh_CN', 'en_US']:
        po_path = os.path.join(locales_dir, locale, 'LC_MESSAGES', 'mbm_workflow.po')
        mo_path = os.path.join(locales_dir, locale, 'LC_MESSAGES', 'mbm_workflow.mo')

        if os.path.exists(po_path):
            compile_po_to_mo(po_path, mo_path)
        else:
            print(f"[SKIP] File not found: {po_path}")

    print("=" * 50)
    print("Done! Blender can now use these translations.")

if __name__ == '__main__':
    main()
