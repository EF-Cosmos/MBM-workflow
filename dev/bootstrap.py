# MBM_workflow 开发引导脚本（运行在 Blender 内部）
#
# 用法（由 dev/start_blender.py 自动完成，也可手动执行）:
#   blender --python dev/bootstrap.py
#
# 功能:
#   1. 注入: 把仓库父目录加入 sys.path 并注册 MBM_workflow
#      （等效 VS Code Blender 插件的启动方式）
#   2. 热重载: 监视源码文件，保存稳定 1.5s 后自动
#      unregister -> importlib.reload -> register
#   3. 执行桥: 监视 temp/zcode_cmd.json，执行其中的 Python 代码，
#      把 stdout/stderr/traceback 写回 temp/zcode_out.json
#
# 控制口（通过执行桥或 Blender Python 控制台）:
#   import mbm_dev
#   mbm_dev.pause_reload()    # 暂停热重载（长任务导入时建议暂停）
#   mbm_dev.resume_reload()   # 恢复热重载
#   mbm_dev.reload_addon()    # 手动触发一次完整重载
#
# 所有输出（含插件的 print/traceback）都会进入 Blender 的 stdout，
# dev 模式下即 temp/blender_dev.log。

import contextlib
import importlib
import io
import json
import os
import sys
import time
import traceback
import types
from pathlib import Path

import bpy

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_PARENT = str(REPO_ROOT.parent)
ADDON_NAME = "MBM_workflow"
TEMP_DIR = REPO_ROOT / "temp"
CMD_FILE = TEMP_DIR / "zcode_cmd.json"
OUT_FILE = TEMP_DIR / "zcode_out.json"
HEARTBEAT_FILE = TEMP_DIR / "dev_heartbeat.txt"

SCAN_INTERVAL = 0.5      # 文件扫描周期（秒）
RELOAD_SETTLE = 1.5      # 变更后的稳定等待（秒），容忍连续多文件写入
HEARTBEAT_INTERVAL = 5.0

# 这些目录下的 .py 不触发热重载
WATCH_EXCLUDE_DIRS = {
    ".git", "__pycache__", ".vscode", ".claude", ".zcode",
    "dist", "temp", "doc", "scripts", "dev",
    "mods", "datapacks", "resourcepacks", "wheels", "unuse",
}


class _State:
    """共享可变状态。发布为 mbm_dev 模块后，本文件命名空间与模块副本
    持有的是同一个 _State 实例，因此控制口修改对 timer 立即可见。"""

    reload_paused = False
    mtimes = None          # 上次扫描的 {相对路径: mtime}
    pending = None         # {"deadline": ts, "files": [...]} 待稳定触发的变更
    bridge_ns = None       # 执行桥持久命名空间
    last_cmd_id = -1
    last_heartbeat = 0.0


STATE = _State()


def log(msg):
    print(f"[mbm-dev] {msg}", flush=True)


# ---------------------------------------------------------------------------
# 注入与注册
# ---------------------------------------------------------------------------

def _publish_module():
    """把控制接口挂到 sys.modules['mbm_dev']（--python 脚本本身不在 sys.modules）"""
    existing = sys.modules.get("mbm_dev")
    if existing is not None:
        return existing
    mod = types.ModuleType("mbm_dev")
    mod.__dict__.update({k: v for k, v in globals().items() if not k.startswith("__")})
    mod.__file__ = str(Path(__file__).resolve())
    sys.modules["mbm_dev"] = mod
    return mod


def _disable_installed_copies():
    """停用已作为扩展/插件启用的安装副本，避免与 dev 副本双重注册"""
    import addon_utils
    targets = [key for key in list(sys.modules)
               if key != ADDON_NAME and key.split(".")[-1] == ADDON_NAME]
    for key in targets:
        log(f"检测到已启用的安装副本: {key}，自动停用以避免双重注册")
        try:
            addon_utils.disable(key, default_set=False)
        except Exception:
            log("停用失败，可能出现类重复注册报错:")
            traceback.print_exc()


def _dependency_fallback():
    """dev 注入模式下 Blender 扩展系统不会自动装 wheels。
    若 amulet 不可用，尝试复用已安装扩展副本的 modules 目录。"""
    try:
        __import__("amulet")
        return True
    except ImportError:
        pass

    added = []
    try:
        ext_root = Path(bpy.utils.user_resource("EXTENSIONS"))
    except Exception:
        ext_root = None
    if ext_root and ext_root.is_dir():
        for modules_dir in ext_root.glob(f"*/{ADDON_NAME}/modules"):
            sys.path.append(str(modules_dir))
            added.append(modules_dir)
    if added:
        log("依赖兜底: 已把已安装扩展的 modules 目录加入 sys.path:")
        for p in added:
            log(f"  {p}")

    try:
        __import__("amulet")
        return True
    except ImportError:
        log("警告: amulet 不可用。请先在该 Blender 中安装一次 release 扩展"
            "（dist/MBM_workflow-*.zip），或手动安装 wheels/ 下的依赖。")
        return False


def _register_addon():
    if ADDON_PARENT not in sys.path:
        sys.path.insert(0, ADDON_PARENT)
    import MBM_workflow
    MBM_workflow.load_modules.register()
    version = getattr(MBM_workflow, "bl_info", {}).get("version", "?")
    log(f"MBM_workflow 已注册（版本 {version}）")


# ---------------------------------------------------------------------------
# 热重载
# ---------------------------------------------------------------------------

def reload_addon():
    t0 = time.time()
    log("热重载开始 ...")
    mod = sys.modules.get(ADDON_NAME)
    if mod is not None:
        try:
            mod.load_modules.unregister()
        except Exception:
            log("旧模块卸载异常（已忽略，继续重载）:")
            traceback.print_exc()
    try:
        if mod is not None:
            mod = importlib.reload(mod)
        else:
            mod = importlib.import_module(ADDON_NAME)
        mod.load_modules.register()
        log(f"热重载完成，耗时 {time.time() - t0:.2f}s")
        return True
    except Exception:
        log("热重载失败（修复并保存后将自动重试）:")
        traceback.print_exc()
        return False


def pause_reload():
    STATE.reload_paused = True
    log("热重载已暂停（恢复: mbm_dev.resume_reload()）")


def resume_reload():
    STATE.reload_paused = False
    log("热重载已恢复")


def _scan_mtimes():
    snap = {}
    for path in REPO_ROOT.rglob("*.py"):
        rel = path.relative_to(REPO_ROOT)
        if any(part in WATCH_EXCLUDE_DIRS for part in rel.parts):
            continue
        try:
            snap[str(rel).replace("\\", "/")] = path.stat().st_mtime
        except OSError:
            continue
    return snap


def _watch_poll():
    # 即使暂停也保持快照更新，避免恢复时把暂停期间的修改变成一次突发的全量重载
    snap = _scan_mtimes()
    if STATE.mtimes is None:
        STATE.mtimes = snap
        return
    prev = STATE.mtimes
    changed = [k for k in set(snap) | set(prev) if snap.get(k) != prev.get(k)]
    STATE.mtimes = snap

    if STATE.reload_paused:
        STATE.pending = None
        return
    if changed:
        STATE.pending = {"deadline": time.time() + RELOAD_SETTLE, "files": sorted(changed)}
    elif STATE.pending is not None and time.time() >= STATE.pending["deadline"]:
        files = STATE.pending["files"]
        STATE.pending = None
        shown = ", ".join(files[:5]) + (" ..." if len(files) > 5 else "")
        log(f"检测到 {len(files)} 个文件变更: {shown}")
        reload_addon()


# ---------------------------------------------------------------------------
# 执行桥
# ---------------------------------------------------------------------------

def _init_bridge():
    ns = {"__name__": "zcode_bridge"}
    for name in ("bpy", "mathutils", "bmesh", "sys", "os", "time", "json", "math"):
        try:
            ns[name] = importlib.import_module(name)
        except ImportError:
            pass
    STATE.bridge_ns = ns


def _run_bridge_code(cid, code):
    if STATE.bridge_ns is None:
        _init_bridge()
    out_buf, err_buf = io.StringIO(), io.StringIO()
    error = None
    try:
        with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
            exec(compile(code, f"<zcode-bridge #{cid}>", "exec"), STATE.bridge_ns)
    except Exception:
        error = traceback.format_exc()
    payload = {
        "id": cid,
        "stdout": out_buf.getvalue(),
        "stderr": err_buf.getvalue(),
        "error": error,
    }
    try:
        tmp = OUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, OUT_FILE)
    except OSError:
        log("执行桥: 写回结果失败:")
        traceback.print_exc()

    log(f"──── 执行桥 #{cid} 完成 ────")
    for line in payload["stdout"].splitlines():
        print(line, flush=True)
    for line in payload["stderr"].splitlines():
        print(line, flush=True)
    if not payload["stdout"] and not payload["stderr"] and not error:
        log("(无输出)")
    if error:
        print(error, flush=True)


def _bridge_poll():
    try:
        cmd = json.loads(CMD_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return
    cid = cmd.get("id")
    if not isinstance(cid, int) or cid <= STATE.last_cmd_id:
        return
    STATE.last_cmd_id = cid
    _run_bridge_code(cid, str(cmd.get("code", "")))


# ---------------------------------------------------------------------------
# timer 主循环
# ---------------------------------------------------------------------------

def _heartbeat():
    now = time.time()
    if now - STATE.last_heartbeat >= HEARTBEAT_INTERVAL:
        STATE.last_heartbeat = now
        try:
            HEARTBEAT_FILE.write_text(str(int(now)), encoding="ascii")
        except OSError:
            pass


def _tick():
    try:
        _heartbeat()
        _bridge_poll()
        _watch_poll()
    except Exception:
        # timer 回调抛异常会被 Blender 静默注销，必须吞掉并保持心跳
        traceback.print_exc()
    return SCAN_INTERVAL


def main():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    log("=" * 62)
    log(f"MBM_workflow dev 引导启动  Blender {bpy.app.version_string}  "
        f"Python {sys.version.split()[0]}")
    log(f"仓库: {REPO_ROOT}")
    _publish_module()
    _disable_installed_copies()
    _dependency_fallback()
    try:
        _register_addon()
    except Exception:
        log("初始注册失败（修复源码保存后将自动重试）:")
        traceback.print_exc()
    _init_bridge()
    if not bpy.app.timers.is_registered(_tick):
        bpy.app.timers.register(_tick, first_interval=SCAN_INTERVAL, persistent=True)
        log(f"热重载监视器已启动（扫描 {SCAN_INTERVAL}s / 稳定 {RELOAD_SETTLE}s）")
    log("=" * 62)


main()
