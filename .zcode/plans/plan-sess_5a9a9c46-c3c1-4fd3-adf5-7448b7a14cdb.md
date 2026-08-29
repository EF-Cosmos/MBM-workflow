# ZCode 实时调试方案（复刻 VS Code Blender 插件工作流）

VS Code 那套「命令启动 Blender + 项目注入插件列表」在本仓库没有任何配置残留，但项目自带可复用的核心：`load_modules.py` 的 importlib 全模块重载模式。本方案用 3 个零依赖脚本把它变成 ZCode 驱动的实时调试循环。

## 新增文件（全部放 `dev/`，`scripts/package.py` 是白名单打包，天然不会进发布包）

### 1. `dev/bootstrap.py` — 注入 + 热重载 + 执行桥（核心，运行在 Blender 内）
通过 `blender --python dev/bootstrap.py` 启动时执行：
- **注入**：把仓库父目录加入 `sys.path` → `import MBM_workflow` 并注册；把自身挂到 `sys.modules['mbm_dev']` 供后续控制
- **依赖兜底**：`dependency_manager` 只检查不安装；若 `amulet` 不可用，best-effort 把 Blender 用户扩展目录下已安装副本的 modules 路径加入 sys.path，仍失败则在日志中给出明确指引
- **防冲突**：检测到 MBM_workflow 已作为扩展启用时打印警告（避免双重注册）
- **热重载监视器**（`bpy.app.timers`，主线程执行，满足 CLAUDE.md 的 bpy 主线程约束）：
  - 每 0.5s 递归扫描 `*.py`（排除 `.git/__pycache__/dist/temp/doc/scripts/dev/mods/datapacks/resourcepacks/wheels/.claude/codes/unuse`）
  - 防抖：变更文件 mtime 稳定 1.5s 后才触发一次（适配 agent 连续写多个文件的场景）
  - 重载循环：旧模块引用 `unregister()` → `importlib.reload(MBM_workflow)`（其内部已 reload 全部子模块）→ `register()`；异常打印完整 traceback 并继续监视，下次保存可自愈
  - 暂停/恢复：`python dev/send_cmd.py -c "import mbm_dev; mbm_dev.reload_paused = True"`
- **执行桥**（同一 timer 兼职）：监视 `temp/zcode_cmd.json`（`{"id": n, "code": "..."}`），id 递增时以 `redirect_stdout/stderr` 捕获执行（持久化命名空间，预导入 bpy/sys/os），结果写 `temp/zcode_out.json`，流量同时镜像进主日志

### 2. `dev/start_blender.py` — 启动器（纯 stdlib，任意 Python 3.8+）
- 解析 blender.exe 优先级：`BLENDER_PATH` 环境变量 > `dev/blender_path.txt` 缓存 > 自动探测：`Program Files\Blender Foundation\Blender*` + **解析 Steam `libraryfolders.vdf` 遍历所有库找 `steamapps\common\Blender\blender.exe`**（覆盖 Steam 版）+ 新版 Steam 默认路径；找到后写缓存，`--reset-path` 清除
- 启动方式：`Popen` 分离进程（DETACHED_PROCESS），stdout/stderr 重定向到 `temp/blender_dev.log` —— 与 ZCode 会话生命周期解耦，关掉会话 Blender 不死
- 参数：`--blend FILE`、`--foreground`（手动在终端跑时实时看输出）、日志截断/追加选项、`--` 透传其余 Blender 参数

### 3. `dev/send_cmd.py` — ZCode 侧执行桥客户端（纯 stdlib）
- `python dev/send_cmd.py -c "print(list(bpy.data.objects))"` 或 `-f script.py`
- 读 out 文件当前 id → 原子写入 id+1 的命令 → 轮询 out 文件至 id 匹配（15s 超时）→ 回显 stdout/stderr/error，异常退出码 1

### 4. 文档：改造 `CLAUDE.md`「开发调试」小节
- 修正现有 `MBM_worflow` 拼写错误
- 新增「ZCode 实时调试」流程 + 注意事项（勿同时启用已安装的 release 扩展；schem_mp 多进程仍走已安装副本路径，维持现状）

### 5. （可选）`.zcode/commands/mbm-dev.md` 斜杠命令
实施时先用 zcode-guide 技能确认 ZCode 项目级命令的路径约定，再写入调试循环说明，让 `/mbm-dev` 一键引导 agent 走完整流程。

## 最终调试循环
1. `python dev/start_blender.py` 拉起 Steam 版 Blender，日志落盘
2. ZCode 改代码 → 约 1.5s 后 Blender 自动卸载/重载/重注册，结果进日志
3. ZCode 读 `temp/blender_dev.log` 尾部看 print 输出与 traceback
4. ZCode 用 `send_cmd.py` 在运行中的 Blender 里执行任意 bpy 代码并取回输出
5. 已有的 blender-mcp（`.mcp.json`）保持为可选补充通道

## 验证步骤
- 启动脚本能探测到 Steam 版 Blender 并成功拉起，日志出现注册横幅
- 修改一个 py 文件 → 日志出现自动重载记录、插件 UI 正常
- `send_cmd.py` 往返正常：普通输出、异常 traceback、超时路径
- 暂停/恢复热重载生效