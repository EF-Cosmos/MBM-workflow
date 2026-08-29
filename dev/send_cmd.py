#!/usr/bin/env python3
# MBM_workflow 执行桥客户端：把 Python 代码送进正在运行的 dev Blender 并取回输出。
#
# 用法（纯标准库，任意 Python 3.8+ 均可运行）:
#   python dev/send_cmd.py -c "print(list(bpy.data.objects))"
#   python dev/send_cmd.py -f some_script.py
#   python dev/send_cmd.py --json -c "..."      # 以 JSON 输出原始结果
#   python dev/send_cmd.py --timeout 60 -f ...  # 长任务的等待上限
#
# 执行桥的命名空间在多次调用间持久保留（bpy/sys/os 等已预导入），
# 可以分多步构建调试状态。代码在 Blender 主线程的 timer 中执行。

import argparse
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CMD_FILE = REPO_ROOT / "temp" / "zcode_cmd.json"
OUT_FILE = REPO_ROOT / "temp" / "zcode_out.json"


def _read_out():
    try:
        return json.loads(OUT_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write(text, stream):
    if text:
        stream.write(text if text.endswith("\n") else text + "\n")


def main():
    ap = argparse.ArgumentParser(
        description="在运行中的 dev Blender 里执行 Python 代码并取回输出",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("-c", "--code", help="要执行的 Python 代码")
    src.add_argument("-f", "--file", help="要执行的 Python 脚本路径")
    ap.add_argument("--timeout", type=float, default=15.0,
                    help="等待响应的秒数（默认 15）")
    ap.add_argument("--json", action="store_true",
                    help="以 JSON 输出原始结果，便于程序化处理")
    args = ap.parse_args()

    if args.file:
        code = Path(args.file).read_text(encoding="utf-8")
    else:
        code = args.code

    last = _read_out()
    last_id = last.get("id", 0) if isinstance(last, dict) else 0
    new_id = last_id + 1

    CMD_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CMD_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps({"id": new_id, "code": code, "sent": time.time()},
                              ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, CMD_FILE)

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        payload = _read_out()
        if isinstance(payload, dict) and payload.get("id") == new_id:
            if args.json:
                print(json.dumps(payload, ensure_ascii=False))
            else:
                _write(payload.get("stdout"), sys.stdout)
                _write(payload.get("stderr"), sys.stderr)
                _write(payload.get("error"), sys.stderr)
            return 1 if payload.get("error") else 0
        time.sleep(0.1)

    print(f"[!] 超时（{args.timeout:.0f}s）：dev Blender 未响应。", file=sys.stderr)
    print("    确认已运行: python dev/start_blender.py", file=sys.stderr)
    print("    排查: temp/blender_dev.log / temp/dev_heartbeat.txt", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
