---
description: MBM_workflow 实时调试环境：启动/检查 Blender dev 实例、执行代码、查看日志
---

# /mbm-dev — MBM_workflow 实时调试

按需执行以下步骤（完整说明见 CLAUDE.md「ZCode 实时调试」小节）：

## 1. 检查 dev 实例是否存活

读 `temp/dev_heartbeat.txt` 的修改时间；15 秒内有更新说明实例在运行。
若超时或文件不存在，继续第 2 步启动。

## 2. 启动（仅在未运行时）

```bash
python dev/start_blender.py
```

自动探测 Steam/标准安装的 Blender 并注入插件，日志写入 `temp/blender_dev.log`。

## 3. 在运行中的 Blender 里执行代码

```bash
python dev/send_cmd.py -c "<python 代码>"
```

- `bpy`/`sys`/`os` 等已预导入；命名空间跨调用持久，可分步构建调试状态
- 取回 stdout/stderr/traceback；出错时退出码为 1，超时为 2

## 4. 查看输出

读 `temp/blender_dev.log` 尾部：插件 print、热重载记录、执行桥镜像输出都在这里。

## 5. 热重载

- 修改仓库内任意源码 `.py`（`dev/`、`doc/`、`dist/`、`codes/unuse/` 等目录除外）后约 2 秒自动重载
- 跑长任务导入前先暂停：`python dev/send_cmd.py -c "import mbm_dev as d; d.pause_reload()"`
- 恢复：`python dev/send_cmd.py -c "import mbm_dev as d; d.resume_reload()"`
- 手动触发一次：`python dev/send_cmd.py -c "import mbm_dev as d; d.reload_addon()"`

## 注意事项

- 执行桥在 timer 上下文执行，`INVOKE_DEFAULT` 弹窗类操作符可能失败；优先用 execute 模式或让用户在界面手动触发
- dev 实例启动时会自动停用已安装的 release 扩展副本
- 同时只运行一个 dev 实例（执行桥是单通道）
