"""Blender 版本兼容工具

为本插件提供跨 Blender 版本（5.0 ~ 5.2+）的运行时判断与适配 helper。
结束此前「零版本分支」状态——几何节点修改器 socket 访问等 API 在 5.2 有破坏性变更，
需据此分流。
"""
import bpy


def blender_version_gte(major, minor=0, patch=0):
    """当前 Blender 版本是否 >= major.minor.patch。

    例：blender_version_gte(5, 2) 在 5.2.0 / 5.3.0 上为 True，在 5.1.0 上为 False。
    """
    return bpy.app.version >= (major, minor, patch)


def is_blender_52_plus():
    """是否运行在 Blender 5.2 及以上（几何节点 modifier socket API 变更点）。"""
    return bpy.app.version >= (5, 2, 0)
