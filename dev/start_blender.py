#!/usr/bin/env python3
# MBM_workflow dev 启动器：定位并启动 Blender（Steam / 标准安装），注入 dev 引导脚本。
#
# 用法（纯标准库，任意 Python 3.8+ 均可运行）:
#   python dev/start_blender.py                 # 后台启动，日志写入 temp/blender_dev.log
#   python dev/start_blender.py --foreground    # 前台启动，日志直接打到当前终端
#   python dev/start_blender.py --blend a.blend # 启动后打开指定 .blend
#   python dev/start_blender.py --detect-only   # 只探测并打印 blender.exe 路径
#   python dev/start_blender.py --reset-path    # 清除路径缓存，强制重新探测
#
# blender.exe 定位优先级:
#   BLENDER_PATH 环境变量 > dev/blender_path.txt 缓存 > 自动探测
#   （Program Files\Blender Foundation\* 与 Steam libraryfolders.vdf 所有库）
# 探测结果会写入 dev/blender_path.txt（该文件是机器相关缓存，已加入 .gitignore）。

import argparse
import glob
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

DEV_DIR = Path(__file__).resolve().parent
REPO_ROOT = DEV_DIR.parent
BOOTSTRAP = DEV_DIR / "bootstrap.py"
PATH_CACHE = DEV_DIR / "blender_path.txt"
LOG_FILE = REPO_ROOT / "temp" / "blender_dev.log"
HEARTBEAT_FILE = REPO_ROOT / "temp" / "dev_heartbeat.txt"

CREATE_FLAGS = 0
if os.name == "nt":
    CREATE_FLAGS = (getattr(subprocess, "DETACHED_PROCESS", 0)
                    | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))


def _steam_root_from_registry():
    """从注册表读 Steam 安装目录（覆盖自定义安装位置，如 D:\\steam）"""
    try:
        import winreg
    except ImportError:
        return None
    for hive, key in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
                      (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")):
        try:
            with winreg.OpenKey(hive, key) as k:
                value, _ = winreg.QueryValueEx(k, "SteamPath")
                path = Path(value)
                if path.is_dir():
                    return path
        except OSError:
            continue
    return None


def _steam_libraries():
    """解析 Steam libraryfolders.vdf，返回所有 Steam 库根目录（含 Steam 本体目录）"""
    roots = []
    reg_root = _steam_root_from_registry()
    if reg_root is not None:
        roots.append(reg_root)
    for env in ("ProgramFiles(x86)", "ProgramFiles", "ProgramW6432"):
        base = os.environ.get(env)
        if base:
            roots.append(Path(base) / "Steam")
    libs = []
    for root in roots:
        vdf = root / "steamapps" / "libraryfolders.vdf"
        if not vdf.is_file():
            continue
        libs.append(root)
        try:
            text = vdf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in re.findall(r'"path"\s+"([^"]+)"', text):
            libs.append(Path(match.replace("\\\\", "\\")))
    seen, out = set(), []
    for lib in libs:
        key = str(lib).lower()
        if key not in seen:
            seen.add(key)
            out.append(lib)
    return out


def _probe_blender():
    candidates = []
    for base in {os.environ.get("ProgramFiles", r"C:\Program Files")}:
        # 标准安装（取版本号最大的一个）
        candidates += sorted(
            glob.glob(os.path.join(base, "Blender Foundation", "Blender*", "blender.exe")),
            reverse=True)
    # Steam 版：注册表/默认位置解析出的所有库
    for lib in _steam_libraries():
        candidates.append(lib / "steamapps" / "common" / "Blender" / "blender.exe")
    # 自定义盘符兜底：D:\steam、X:\SteamLibrary 等常见命名
    for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        for name in ("steam", "Steam", "SteamLibrary"):
            candidates.append(Path(f"{letter}:/{name}/steamapps/common/Blender/blender.exe"))
    for c in candidates:
        if Path(c).is_file():
            return Path(c)
    return None


def find_blender(use_cache=True):
    env = os.environ.get("BLENDER_PATH")
    if env and Path(env).is_file():
        return Path(env), "环境变量 BLENDER_PATH"
    if use_cache and PATH_CACHE.is_file():
        cached = Path(PATH_CACHE.read_text(encoding="utf-8").strip())
        if cached.is_file():
            return cached, f"缓存 {PATH_CACHE.name}"
    found = _probe_blender()
    if found is not None:
        try:
            PATH_CACHE.write_text(str(found), encoding="utf-8")
        except OSError:
            pass
        return found, "自动探测"
    return None, None


def _warn_if_running():
    try:
        age = time.time() - HEARTBEAT_FILE.stat().st_mtime
    except OSError:
        return
    if age < 15:
        print(f"[!] 已有一个 dev 实例在运行（心跳 {age:.0f}s 前仍活跃），"
              "继续启动会导致两个实例争用同一个执行桥。")


def main():
    ap = argparse.ArgumentParser(
        description="启动 Blender 并注入 MBM_workflow dev 环境",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--blend", help="启动后打开的 .blend 文件")
    ap.add_argument("--foreground", action="store_true",
                    help="前台运行，日志直接输出到当前终端")
    ap.add_argument("--append-log", action="store_true",
                    help="追加而非截断 temp/blender_dev.log")
    ap.add_argument("--detect-only", action="store_true",
                    help="只探测并打印 blender.exe 路径")
    ap.add_argument("--reset-path", action="store_true",
                    help="清除 dev/blender_path.txt 缓存，强制重新探测")
    ap.add_argument("extra", nargs="*",
                    help="透传给 blender 的额外参数")
    args = ap.parse_args()

    if args.reset_path and PATH_CACHE.is_file():
        PATH_CACHE.unlink()

    blender, source = find_blender()
    if args.detect_only:
        print(blender if blender else "未找到 blender.exe")
        return 0 if blender else 1
    if blender is None:
        print("未找到 blender.exe。请任选其一：")
        print("  1) 设置环境变量 BLENDER_PATH 指向 blender.exe")
        print("  2) 把完整路径写入 dev/blender_path.txt")
        return 1
    print(f"blender.exe: {blender}  (来源: {source})")

    cmd = [str(blender), "--python", str(BOOTSTRAP)]
    if args.blend:
        cmd.append(str(Path(args.blend).resolve()))
    cmd += args.extra

    if args.foreground:
        print(f"[mbm-dev] 前台启动: {' '.join(cmd)}")
        return subprocess.call(cmd)

    _warn_if_running()
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    with open(LOG_FILE, "a" if args.append_log else "w",
              encoding="utf-8", errors="replace") as log_fh:
        log_fh.write(f"\n==== {datetime.now():%Y-%m-%d %H:%M:%S} 启动 ====\n")
        log_fh.write(f"==== {' '.join(cmd)} ====\n")
        log_fh.flush()
        proc = subprocess.Popen(
            cmd,
            stdout=log_fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
            cwd=str(REPO_ROOT), env=env,
            creationflags=CREATE_FLAGS, close_fds=True)

    time.sleep(1.5)
    if proc.poll() is not None:
        print(f"[!] Blender 启动后立即退出 (code={proc.returncode})，详情见日志: {LOG_FILE}")
        return 1
    print(f"[mbm-dev] Blender 已后台启动 (pid {proc.pid})")
    print(f"  日志:       {LOG_FILE}")
    print(f"  执行代码:   python dev/send_cmd.py -c \"print('hello')\"")
    print(f"  暂停热重载: python dev/send_cmd.py -c \"import mbm_dev as d; d.pause_reload()\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
