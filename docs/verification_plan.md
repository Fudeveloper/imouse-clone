# 当前代码验证结果与逐步测试方法

更新时间：2026-06-08

本仓库原代码不能视为已验证产品。当前目标是严谨区分：

- 已验证：本地命令已经跑通，有命令证据。
- 未验证：需要 AirPlay 服务、HID 硬件、iPhone 实机。
- 已发现问题：已复现并修复或记录。

实机下一步优先读：

- `docs/follow_along_test_method.md`：从本地自检、run_id、路线锁定、Doctor、截图、HID、Acceptance、Readiness 到 XP 对标复盘的跟测手册。
- `docs/mainstream_route_decision.md`：P1 前先决定主流路线、receiver、HID、采购和开测停止线。
- `docs/industry_current_state_snapshot_2026.md`：把 2026-06-09 公开来源、主流路线、SOP 门禁、行业壁垒和 GUI 承载边界汇成当前快照。
- `docs/p1_single_device_runbook.md`：P1 单台 iPhone 首测，按步骤拿到第一份真实 evidence。
- `docs/p2_p3_stability_runbook.md`：P1 通过后的 30 分钟单台、4 台试点、10 台 2 小时稳定性流程。
- `docs/hardware_test_bench_checklist.md`：采购、搭台、编号和 XP 专用硬件/CH9329 对比测试。
- `docs/receiver_capture_selection.md`：投屏 receiver、截图采集、有线投屏、采集卡的路线选择和证据要求。
- `docs/hid_hardware_protocol_benchmark.md`：CH9329、XP 专用硬件、自研 HID 的同场对标测试表。
- `docs/xp_parity_matrix.md`：XP 公开能力、当前实现、验收证据、差距和下一步动作的同表对标。
- `docs/field_test_matrix.md`：阶段门、指标和失败分类。
- `docs/xp_core_backlog.md`：按 iMouse XP 公开能力拆出的研发差距和优先级。
- `docs/xp_gap_audit.md`：机器可读 XP 核心能力差距审计和 GUI/CLI 使用方式。
- `docs/readiness_audit.md`：项目阶段审计，汇总文档、脚本、doctor 和 acceptance gate。

P1 真机前新增一条硬门：

```powershell
.\.venv\Scripts\python -m imouse.route_decision init --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_route_decision.json
.\.venv\Scripts\python -m imouse.route_decision validate evidence\p1_dev1_YYYYMMDD_route_decision.json --require-ready --markdown evidence\p1_dev1_YYYYMMDD_route_decision.md --record-evidence evidence\p1_dev1_YYYYMMDD.jsonl
```

这只验证路线决策记录完整，并向 evidence 写入组件台账；不证明 iPhone 已响应。真正通过仍看截图质量、人工观察、acceptance 和 readiness。

注意：如果失败路线决策已经写入 evidence，该 run_id 就是一次失败/阻断记录。修复后请换新的 run_id，不要在同一个 evidence 文件里继续追加通过证据来抵消失败。

## 当前本地验证结论

### 已验证

1. Python 3.13 虚拟环境可安装依赖

命令：

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

结果：

- Python 3.13.9。
- `requirements.txt` 安装成功。
- PaddlePaddle 3.3.1 和 PaddleOCR 3.6.0 可安装到 Python 3.13。

2. 默认 Python 3.14 不适合作为当前主环境

已观察：

- 默认 `python` 是 3.14.5。
- `python -m pip index versions paddlepaddle` 返回没有匹配发行包。

结论：

- 开发和测试统一使用 Python 3.13。

3. 语法编译通过

命令：

```powershell
.\.venv\Scripts\python -m compileall -q imouse tests
```

结果：

- 通过。

4. 依赖检查入口通过，但投屏组件缺失

命令：

```powershell
.\.venv\Scripts\python -m imouse.main --check
```

结果：

- `serial`、`cv2`、`numpy`、`PIL`、`fastapi`、`uvicorn` 为 OK。
- `uxplay` 为 MISSING。

结论：

- Python 依赖层可用。
- 当前机器没有安装当前代码依赖的 UxPlay，因此 AirPlay 投屏链路未验证。

5. FastAPI 应用可导入

命令：

```powershell
@'
import imouse.server
print(imouse.server.app.title)
print(len(imouse.server.app.routes))
'@ | .\.venv\Scripts\python -
```

结果：

- 应用标题为 `iMouse Clone`。
- 路由数量为 26。

6. HTTP 服务冒烟测试通过

验证内容：

- 启动本地 uvicorn。
- `GET /api/devices` 返回 200。
- `POST /api/device/register` 返回 200。

结果：

- 设备列表初始为空。
- 注册 `smoke_1` 后返回 `offline`。

结论：

- API 服务框架可运行。
- 这不代表硬件、投屏、截图、点击已通过。

7. 串口扫描可运行

命令：

```powershell
@'
from imouse.hardware import list_devices
print(list_devices())
'@ | .\.venv\Scripts\python -
```

结果：

- 当前只看到 `COM1`。

结论：

- 没有识别到 CH9329 或 XP 专用硬件。
- 硬件控制未验证。

8. HID 协议帧构造可运行

命令：

```powershell
@'
from imouse.hardware import _build_frame, DEFAULT_ADDR, CMD_KEYBOARD
print(_build_frame(DEFAULT_ADDR, CMD_KEYBOARD, bytes(8)).hex(' '))
'@ | .\.venv\Scripts\python -
```

结果：

```text
57 ab 00 02 08 00 00 00 00 00 00 00 00 0a
```

结论：

- 当前 CH9329 帧构造函数可运行。
- 未证明真实硬件会接受或 iPhone 会响应。

9. 找色函数离线测试通过

结果：

- 精确颜色能找到坐标。
- 错误颜色返回 None。
- 容差扩大后能找到坐标。

10. OpenCV 找图函数离线测试有条件通过

结果：

- 纯白单色模板会误判到左上角。
- 有纹理模板能返回正确坐标。

结论：

- 找图函数可用，但必须制定模板资产规范。

11. PaddleOCR 兼容层已做基础验证

已发现：

- PaddleX 默认缓存目录为用户 Home 下 `.paddlex`，受限环境会 PermissionError。
- 已改为默认使用项目内 `.cache/paddlex`。
- PaddleOCR 3.6 构造签名已变化，`show_log` 和 `use_angle_cls` 不再是显式参数。
- 已增加 PaddleOCR 2.x 和 3.x 返回结构兼容解析。

已验证：

- PaddleOCR 2.x 风格假数据解析通过。
- PaddleOCR 3.x 风格假数据解析通过。

未验证：

- 真实 OCR 模型下载和真实图片识别尚未运行。

12. XP 风格 `/api` + `fun` 兼容入口已做离线测试

已实现：

- `GET /api?fun=/dev/list`。
- `POST /api` JSON，支持 `{"fun": "...", "data": {...}}`。
- `POST /api` JSON，支持把 `id` 等字段放在顶层。
- WebSocket `/api` 支持发送带 `fun` 的 JSON 请求，`/ws` 保留为 legacy/debug alias。
- `/callback/list`、`/callback/poll`、`/callback/push`、`/callback/clear` 已有离线 callback ledger 骨架。
- 自动把 XP 常用字段 `id` 映射为内部 `device_id`。
- 支持本地分组：`/group/list`、`/group/save`、`/group/remove`。
- 批量接口支持传 `group` / `group_name`，由分组展开设备列表。
- 返回体包含 `status`、`message`、`data`、`msgid`、`fun`。

测试命令：

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

当前结果：

- 最近一次本地验证以实际 `python -m unittest discover -s tests -v` 输出为准；不要把旧测试数量当成固定验收结论。
- 覆盖设备列表、设备注册、顶层字段兼容、未知 fun 错误格式、WebSocket `/api`/`/ws` fun 请求和 callback list/poll/push。
- 覆盖批量点击接口的逐设备错误汇总。
- 覆盖分组保存、列表、删除、未知分组 404，以及按分组名称批量点击。
- 覆盖校准保存、读取、列表，以及设备点击/滑动坐标映射。
- 覆盖 XP API 客户端 payload 构造、helper 字段映射、错误处理。
- 覆盖 XP API 客户端找图、找色、OCR、找文字 helper。
- 覆盖 XP API 客户端批量点击、批量滑动、批量输入 helper。
- 覆盖 XP API 客户端分组 helper 和按分组批量 helper。
- 覆盖 XP API 客户端 ImConfig/User/Shortcut runtime helper；这些 helper 只证明本地兼容状态和 payload，不证明 XP 云用户、权限或快捷指令真实执行。
- 覆盖 GUI 截图预览缩放、画布点击到原图坐标、拖拽选区到原图矩形的映射。
- 覆盖 GUI doctor/scenario 状态摘要、Live Probe、GUI Operator Home、GUI Control Center、GUI Knowledge Center、GUI Industry Current Snapshot、GUI Industry SOP Radar、GUI Mainstream Route Matrix、GUI Verification Walkthrough、GUI Local Verification、XP Architecture Map、XP Core Function Matrix、XP API Coverage Board、GUI Script Coverage Board、Acceptance Proof Map、Claim Scope、XP Event/Error Contract、GUI Pitfall Library、GUI SOP Problem Ledger、Attach Log triage、Rerun Playbook、Recovery Drill、XP Public Source Ledger、XP Source Refresh Board、XP Public Source Audit、XP Iteration Radar、XP Iteration Timeline、XP Iteration Drill Board、XP Roadmap、Device/iOS Compatibility Matrix、Goal Gate、Field Kit Gate、iOS Field Settings SOP、Hardware Bench、Capture Quality Bench、Control Response Bench、Control Evidence Ledger、Field Evidence Wizard、Field Evidence Runner、First Run Packet、Receiver Candidate Scorecard、Receiver Route Bootstrap、Receiver Setup Wizard、P1 Test Coach、P1 Field Transcript、Stage Dashboard、Evidence Pack、XP Gap Audit，以及 doctor fail 不误记为 pass 的证据状态判断。
- 覆盖验证证据 JSONL 写入、读取、汇总和 Markdown 报告。
- 覆盖 acceptance gate 对 P1/P3 evidence 的通过、缺人工观察、缺设备追踪、Markdown 输出和失败退出码。
- 覆盖 JSON 脚本运行器调度、失败中断、dry-run 和 evidence 写入。
- 覆盖 preflight doctor 的模块检查、server 探测、状态聚合和 Markdown 报告。
- 覆盖现场执行包生成器的阶段脚本选择、设备默认值、Markdown 输出和 CLI 写文件。

详细协议见：

- `docs/xp_api_compat.md`

13. XP API Python 客户端已做离线测试

已实现：

- `imouse.xp_client.XpApiClient`。
- 基于标准库 `urllib`，不额外引入 requests 依赖。
- 支持 `/api` JSON POST。
- 提供设备列表、注册、移除、硬件扫描、绑定/解绑、投屏、采集、截图、点击、滑动、输入文本等 helper 方法。
- 提供分组列表、保存、删除，以及按分组点击、滑动、输入 helper 方法。

测试覆盖：

- 请求 URL 和 JSON payload 构造。
- `register_device()` 使用 XP 字段 `id`。
- 错误响应抛出 `XpApiError`。
- 分组 helper 的 payload 构造。

14. Python GUI 原型已做基础验证

已实现：

- `python -m imouse.gui` 启动入口。
- 标准库 Tkinter GUI，不增加新依赖。
- 可启动/停止本地内核服务。
- 可刷新设备、注册/移除设备、扫描/绑定硬件、启动投屏/采集、点击/滑动/输入。
- 可显示截图预览、点击预览取原图坐标、保存最近一次截图。
- 可拖拽截图选区保存模板、调用找图、取色/找色、OCR、查找文字。
- 设备表支持多选，多选时点击、滑动、输入走 `/batch/*` 批量接口。
- 可保存当前多选设备为本地分组、刷新/加载/删除分组。
- 可从截图填充坐标校准，保存/加载每台设备校准。
- 可自动记录 GUI/API 操作证据到 `evidence/<run_id>.jsonl`，并生成 Markdown 汇总。
- 可在 GUI 顶部运行 `Doctor`，生成 `evidence/<run_id>_doctor.md`，doctor fail 会作为失败事件写入 evidence。
- 可在 GUI 底部选择 JSON `Scenario`，支持 `Dry Run` 和实跑，复用 `imouse.script_runner` 写入场景 evidence。
- 可手动记录人工观察结果、状态、备注和附件路径到同一份 evidence。
- 可在 GUI 底部打开 P0-P4 Stage Dashboard，导出 `evidence/<run_id>_<stage>_stage_dashboard.md`。
- 可在 GUI 底部导出 `evidence/<run_id>_<stage>_evidence_pack.md`，索引本轮 evidence、route、doctor、worksheet、acceptance、gap、readiness 等产物。
- 可在 GUI 顶部 `Attach Log` 导入 receiver/HID 文本日志，导出 `evidence/<run_id>_callback_log.md`；勾选 `Record` 时写入 `Attach Log triage` JSONL，把日志 severity/category 和样例行带入 Triage/Recovery，但不替代真实 iPhone 控制观察。
- 可在 Live Probe 点击 `Events` 导出 `evidence/<run_id>_<stage>_xp_event_error_contract.md`，把 XP API envelope、WebSocket/msgid、callback lifecycle、receiver/HID/capture 错误、Attach Log 接入和 claim boundary 放到同一张审计表；它不写 JSONL evidence，也不证明真实 iOS 控制。
- 可在 Live Probe 点击 `API Cov` 导出 `evidence/<run_id>_<stage>_xp_api_coverage.md`，把 XP fun/helper 域映射到本地测试、runtime gate、field evidence、scaffolding/backlog 边界和 claim boundary；它只关闭 P0 兼容性，不证明真实 iOS 控制。
- 可在 Live Probe 点击 `Proof Map` 导出 `evidence/<run_id>_<stage>_proof_map.md`，把 Acceptance/Readiness gate 映射到 GUI 动作、JSONL/event 要求、artifact、下一条命令和停止线；它只做导航，不写 evidence，也不证明真实 iOS 控制。
- 可在 GUI 顶部/Live Probe 打开并导出 `evidence/<run_id>_<stage>_rerun_playbook.md`，把失败类别和阶段 gate 转成最小重跑动作、fresh run_id 规则、证据保留项和停止线。
- 可在 GUI 顶部/Live Probe 打开并导出 `evidence/<run_id>_<stage>_recovery_drill.md`，把 receiver/HID/校准/视觉/群控/性能恢复步骤、验证步骤、证据保留项和停止线集中到恢复演练表；弹窗 `Record Pass` / `Record Fail` 可把选中恢复 lane 的执行结果写入 JSONL，但不替代 `Manual` / `P1 Trial` 的真实 iPhone 控制观察。
- 可在 GUI 底部打开/导出 `evidence/<run_id>_<stage>_verification_walkthrough.md`，把 P0/P1/P2/P3/P4 的逐步测试方法、命令、预期、证据和停止线集中到一张表。
- 可在 GUI 底部打开/导出 `evidence/<run_id>_<stage>_local_verification.md`，把 unittest、compileall、dependency check、Doctor、route-aware Doctor、scenario dry-run 和 Readiness 拆成操作者可逐条跟跑的 PowerShell 命令；它不运行命令、不写 JSONL evidence、不证明真实 iOS 控制。
- 可在 GUI 底部打开/导出 `evidence/<run_id>_<stage>_xp_core_functions.md`，把 XP 核心功能拆成本地实现、证据门、XP Gap 状态和下一步 GUI 动作。
- 可在 GUI 底部打开/导出 `evidence/<run_id>_<stage>_ios_field_sop.md`，把真实 iPhone 设置、AirPlay/网络、Hub/Cable、baseline screenshot、manual observation 和声明边界集中到一张表。
- 可在 GUI 底部导出 `evidence/<run_id>_<stage>_xp_gap_audit.md`，按 XP 核心能力域列出当前实现、差距、证据门和下一步研发动作。
- GUI 使用 `XpApiClient` 调用 XP 风格接口。

已验证：

- `imouse.gui` 模块可导入。
- 截图预览缩放、取点、拖拽选区坐标映射、doctor/scenario 摘要、Live Probe、GUI Operator Home、GUI Control Center、GUI Knowledge Center、GUI Industry Current Snapshot、GUI Industry SOP Radar、GUI Mainstream Route Matrix、GUI Verification Walkthrough、GUI Local Verification、XP Architecture Map、XP Core Function Matrix、XP API Coverage Board、GUI Script Coverage Board、Acceptance Proof Map、Claim Scope、XP Event/Error Contract、GUI Pitfall Library、GUI SOP Problem Ledger、Attach Log triage、Rerun Playbook、Recovery Drill、XP Public Source Ledger、XP Source Refresh Board、XP Public Source Audit、XP Iteration Radar、XP Iteration Timeline、XP Iteration Drill Board、XP Roadmap、Device/iOS Compatibility Matrix、Goal Gate、Field Kit Gate、iOS Field Settings SOP、Hardware Bench、Capture Quality Bench、Control Response Bench、Field Evidence Wizard、First Run Packet、Receiver Candidate Scorecard、Receiver Route Bootstrap、Receiver Setup Wizard、P1 Test Coach、P1 Field Transcript、Stage Dashboard、Evidence Pack、XP Gap Audit 和状态判定有单元测试覆盖。
- 代码编译通过。

未验证：

- 真实桌面点击流程尚未人工操作。
- 坐标校准尚未做真实点位验证。
- 没有实时投屏画面预览。
- 真实 iPhone 点击、滑动、输入仍需硬件和手机。

详细说明见：

- `docs/gui_prototype.md`

15. 验证证据记录工具已做离线测试

已实现：

- `imouse.validation.ValidationRecorder`。
- 支持 `pass`、`fail`、`info`、`skip` 状态。
- 自动清洗 `run_id`，设备 ID 去重。
- JSONL 追加记录，适合长时间实机测试中途崩溃后的复盘。
- 可生成 `evidence/<run_id>.md` Markdown 汇总。
- GUI 操作默认自动写入证据记录，截图 base64 会压缩成长度标记，避免证据文件过大；GUI Screenshot 也会记录 `screenshot_quality`，黑屏、白屏、无效图或过小图会作为失败证据。
- `python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1|p2|p3|p4` 可对现场 evidence 做阶段门判定，检查失败事件、设备追踪、组件追踪、人工 pass 观察、截图质量样本和 metrics 样本。
- `python -m imouse.readiness --target p1 --evidence evidence\<run_id>.jsonl` 可把文档、脚本、doctor 和 acceptance gate 汇总成项目阶段状态。
- `python -m imouse.field_packet --stage p1 --run-id <run_id>` 可生成本轮现场执行包，把 doctor/readiness、组件台账、GUI 步骤、脚本命令、验收命令和失败分流表汇总到一份 Markdown。
- `python -m imouse.xp_gap_audit --target p1 --run-id <run_id> --markdown evidence\<run_id>_p1_xp_gap_audit.md` 可生成 XP 核心能力差距审计；它不写 evidence，也不证明实机通过。

已验证：

- JSONL 写入和读取通过单元测试。
- 状态汇总、设备事件计数、失败列表通过单元测试。
- Markdown 汇总生成通过单元测试。
- Acceptance gate 的 pass/fail 判定、Markdown 输出和失败退出码通过单元测试。
- Readiness audit 的 P0/P1 判定、doctor fail 阻断和 Markdown 输出通过单元测试。
- Field packet 的 P1/P3 输出、脚本选择、设备列表和 CLI 写文件通过单元测试。

详细说明见：

- `docs/validation_evidence.md`

16. JSON 脚本运行器已做离线测试

已实现：

- `python -m imouse.script_runner <scenario.json>`。
- 支持 `call`、`wait`、`record`、`click`、`swipe`、`type`。
- 支持 `group_click`、`group_swipe`、`group_type`。
- 支持 `screenshot`、`find_image`、`find_image_then_click`、`find_color`、`find_colors`、`ocr`、`find_text`。
- `find_image` / `find_image_then_click` 支持 `region: [x, y, w, h]`，离线测试已覆盖区域内命中返回全屏坐标、区域外不命中、区域过小不匹配、client/runner 透传 payload。
- `find_colors` 支持锚点 + 相对偏移颜色点，离线测试已覆盖底层匹配、区域约束、XP API alias、client payload 和 runner 透传。
- 支持 `--dry-run`。
- 每步自动写入 evidence，运行结束生成场景汇总。

已验证：

- fake client 下的步骤调度通过单元测试。
- 找图后点击的命中路径和模板缺失失败路径通过单元测试。
- 默认遇到失败停止，`dry-run` 不调用 client，通过单元测试。
- 场景 JSON 根节点校验通过单元测试。

未验证：

- 真实 iPhone 脚本闭环未跑。
- 脚本中的人工 `record` 仍需要人眼观察真实设备。

详细说明见：

- `docs/script_runner.md`

17. 坐标校准层已做离线测试

已实现：

- `imouse.calibration.CalibrationProfile`。
- 支持 source 截图空间、active 有效区域、target 硬件控制空间、orientation 和 safe area 记录。
- 设备点击和滑动会在启用校准时先做坐标映射。
- XP API 支持 `/calibration/list`、`/calibration/get`、`/calibration/set`。
- XP API 支持 `/profile/list`、`/profile/get`、`/profile/set` 和 `/metadata/*` 别名，设备组件档案持久化到 `state/device_profiles.json`。
- XP API 支持 `/config/*`、`/imconfig/*`、`/user/*`、`/shortcut/*` 本地 runtime 兼容入口，默认持久化到 `state/xp_runtime.json` 并写 callback ledger；它不证明真实 XP 账号、权限、授权或快捷指令执行。
- GUI 支持从截图填充校准、保存和加载设备校准。

已验证：

- active 区域到 target 空间映射通过单元测试。
- 启用校准时 `Device.click()` 和 `Device.swipe()` 使用映射后的坐标。
- 未启用校准时保持旧的屏幕尺寸行为。
- 校准配置可持久化并在设备注册时加载。
- API 和 client helper 的 payload 通过单元测试。

未验证：

- 真实 iPhone 五点校准未跑。
- 横屏和 iOS 17+ 快准狠鼠标模式未实测。

详细说明见：

- `docs/coordinate_calibration.md`

18. Preflight doctor 已做离线测试

已实现：

- `python -m imouse.doctor`。
- 支持 `--json` 输出机器检查结果。
- 支持 `--markdown <path>` 输出 Markdown 报告。
- 支持 `--server-url` 探测 XP 风格 API 服务。
- 支持 `--route-decision` 或 `--receiver-config` 做替代 receiver provider 预检。
- 检查 Python 版本、关键模块、receiver provider、`uxplay`、`Xvfb`、串口、工作区可写性、运行目录和状态文件；状态文件包含分组、校准和设备组件档案。

已验证：

- 模块存在/缺失检查通过单元测试。
- server 探测通过 fake HTTP 响应单元测试。
- 默认 UxPlay 缺失仍为 fail；有效 Windows Receiver route decision 会把 UxPlay 缺失降为 warn，并保留 receiver_provider ok。
- `fail/warn/ok` 聚合逻辑通过单元测试。
- Markdown 报告生成通过单元测试。

未验证：

- 当前机器仍缺 `uxplay`，doctor 会把 AirPlay 原型链路判为 `fail`。
- 真实 HID 硬件插拔变化未验证。

详细说明见：

- `docs/preflight_doctor.md`

### 已修复的问题

1. Windows 控制台 emoji 输出崩溃

现象：

- `python -m imouse.main --check` 在 GBK 控制台输出 emoji 时触发 `UnicodeEncodeError`。

修复：

- 入口 banner 和依赖检查状态改为 ASCII 输出。

2. PaddleOCR 缓存目录权限

现象：

- PaddleOCR/PaddleX 导入时尝试写 `C:\Users\Administrator\.paddlex`。

修复：

- 默认设置 `PADDLE_PDX_CACHE_HOME` 到项目内 `.cache/paddlex`。
- `.cache/` 已加入 `.gitignore`。

3. PaddleOCR 版本兼容

现象：

- PaddleOCR 3.6 构造参数与旧代码不一致。

修复：

- 根据构造签名自动选择旧版或新版初始化参数。
- 统一 OCR 返回结构。

## 当前代码与 iMouse XP 的差距

1. 投屏链路差距

当前仓库：

- 依赖 UxPlay。
- 代码里包含 Xvfb/X11 思路。

iMouse XP 对标目标：

- Windows 原生产品体验。
- 单一投屏服务。
- 有线投屏优先。
- H264/H265 硬解。
- 多设备窗口分离和多进程显示。

结论：

- 当前投屏实现只能作为早期原型，不能代表 XP 版核心能力。

2. API 协议差距

当前仓库：

- 已保留 REST 风格，例如 `/api/click`、`/api/find_image`。
- 已新增 XP 风格统一入口 `/api` + `fun`。

iMouse XP：

- 官方 XP API 示例包含统一 `/api` 入口和 `fun` 功能名，例如 `/pic/ocr`。
- GET、POST multipart、POST JSON、WebSocket 可复用功能名；当前原型已补 WebSocket `/api`、callback ledger 骨架，以及 `/pic/screenshot` 的 `binary/jpg/rect/region/save_path` 兼容。
- 2026-06-09 update: `XpApiClient.screenshot_bytes()` is covered for raw `binary=true` image bytes, `screenshot(binary=True)` delegates to that path, and binary HTTP error JSON is converted to `XpApiError`.

结论：

- XP 兼容协议层已有初版；截图 fun 的 GET/JSON/multipart/binary/save_path 已有自动化覆盖，但更多官方 fun、字段语义和真实 receiver/HID 事件仍需继续对照官方文档扩展。
- 协议通过不等于真实投屏、硬件、OCR、点击已经实机通过。

3. 硬件差距

当前仓库：

- 实现 CH9329 通用串口协议。

iMouse XP：

- 依赖专用硬件和 4.4 固件。
- 自动绑定、快准狠鼠标模式与固件强相关。

结论：

- 当前硬件层必须实机确认，不能假设已对标 XP。

## 你可以按这个步骤继续实机测试

### 第 1 步：确认 Python 环境

```powershell
cd D:\codex-projects\imouse-clone
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m imouse.main --check
.\.venv\Scripts\python -m imouse.doctor --markdown evidence\preflight_YYYYMMDD.md
```

通过标准：

- 除 `uxplay` 外 Python 依赖全部 OK。
- doctor 报告能明确列出 `ok/warn/fail`，并保存到 evidence。
- 进入实机投屏测试前，doctor 不应有阻断项；当前缺 `uxplay` 时只能继续离线验证。

### 第 2 步：确认服务能启动

```powershell
.\.venv\Scripts\python -m uvicorn imouse.server:app --host 127.0.0.1 --port 9911
```

另开一个 PowerShell：

```powershell
curl.exe http://127.0.0.1:9911/api/devices
curl.exe -X POST http://127.0.0.1:9911/api/device/register -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\"}"
```

通过标准：

- 两个请求都返回 200。
- `dev_1` 状态为 `offline`。

### 第 2.5 步：确认 XP 风格 API 入口

运行自动化测试：

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

手动测试：

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/dev/list&msgid=1"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/device/register\",\"data\":{\"id\":\"dev_xp\"}}"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/group/save\",\"data\":{\"name\":\"g1\",\"ids\":[\"dev_1\",\"dev_xp\"]}}"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/batch/click\",\"data\":{\"group\":\"g1\",\"x\":100,\"y\":100}}"
```

通过标准：

- 自动化测试全部通过。
- GET 返回 XP 风格 JSON，包含 `fun` 和 `msgid`。
- POST 注册设备后，返回 `id=dev_xp` 和 `device_id=dev_xp`。
- `/group/save` 返回分组名、设备列表和数量。
- 按 `group` 批量点击时，即使硬件未连接，也要返回每台设备的失败明细，而不是整个请求崩溃。

Receiver Route Gate offline coverage:

- GUI helper tests cover missing Route Decision as a blocker.
- GUI helper tests cover a valid Windows Receiver provider where Doctor can treat missing `uxplay` as a route-specific warning instead of a hard blocker.
- Markdown export must state that Receiver Route Gate does not write evidence and does not prove real iOS control.

Receiver Setup Wizard offline coverage:

- GUI helper tests cover selected `uxplay` with missing `binary:uxplay` as a hard setup blocker.
- GUI helper tests cover valid `windows_receiver` setup where missing UxPlay is documented as not required.
- Markdown export must include copy-ready commands and state that the wizard does not install software, write evidence, or prove real iPhone response.

P1 Field Transcript offline coverage:

- GUI helper tests cover transcript rows built from Coach and Receiver Setup rows.
- Transcript must include a receiver setup split row, one fillable operator row per Coach checkpoint, and a sign-off row.
- Markdown export must state that Transcript does not write JSONL evidence, does not record Manual pass by itself, and does not prove real iPhone response.
- Tests must keep the Readiness command aligned with the real CLI `--evidence` option.

Local Verification offline coverage:

- GUI helper tests cover command-by-command rows for unittest, compileall, dependency check, Doctor, route-aware Doctor, scenario dry-run, and Readiness.
- Missing `uxplay` remains visible as a dependency/receiver blocker and must not become a real iOS control pass.
- Markdown export must state that Local Verification does not run commands, does not write evidence, and does not prove real iOS control.
- Field validation still requires Shot Bench, Manual/P1 Trial, Acceptance, and Readiness after this gate.

Script Coverage Board offline coverage:

- GUI helper tests cover stage scenario inventory, dry-run summary status, Real-run Guard blocking, component metadata, screenshot probes, HID click/swipe/text lanes, group-script boundaries, and the script claim boundary.
- Markdown export must state that Script Cov does not run scripts, write JSONL evidence, prove real iPhone control, or prove XP script parity.
- Field validation still requires same-run screenshots, lane-separated Manual observations, Acceptance, Readiness, and exact device/iOS scope after this board.

Acceptance Proof Map offline coverage:

- GUI helper tests cover missing JSONL/route/Doctor evidence, Acceptance check to GUI-action mapping, lane-separated click/swipe/text proof boundaries, Readiness claim boundaries, next commands, and Markdown export.
- Markdown export must state that Proof Map does not run scripts, write JSONL evidence, or prove real iPhone control.
- Field validation still requires same-run JSONL evidence, screenshots, lane-separated Manual observations, Acceptance, Readiness, and exact device/iOS scope.

Claim Scope offline coverage:

- GUI helper tests cover P0-only wording, P1 boundaries when Acceptance/Readiness look clean but `real_ios_control_verified=false`, API/Core local coverage wording, XP hardware parity blockers, compatibility boundaries, and Markdown export.
- Markdown export must state that Claim Scope writes wording guidance only, does not write JSONL evidence, and does not prove real iPhone response.
- Field validation still requires the Proof Map evidence rows plus Acceptance PASS, Readiness PASS, and exact device/iOS/receiver/HID scope before any real-control claim.

Goal Gate closure coverage:

- GUI helper tests cover the four user acceptance goals and now include Proof Map and Claim Scope as closure inputs for the iOS control and SOP rows.
- If Acceptance/Readiness and real-device claims look clean but Claim Scope is still `warn`, Goal Gate must stay `warn` and send the operator to `Open Claim Scope`.
- Markdown export must state that project completion requires real-device evidence, Proof Map closure, Claim Scope pass wording, Acceptance PASS, Readiness PASS, and no unexplained fail events.

### 第 2.6 步：启动 Python GUI 原型

```powershell
.\.venv\Scripts\python -m imouse.gui
```

离线通过标准：

- GUI 能启动。
- 顶部 `Evidence` 可以设置本轮 `run_id`，`Record` 保持勾选。
- 点击 `Start Local` 后本地服务能启动。
- 点击 `Doctor` 后能生成 `evidence/<run_id>_doctor.md`；当前机器缺 UxPlay 时预期为 fail，不能当作实机投屏通过。
- 点击 `Ping` 能刷新设备列表。
- 注册 `dev_1` 后设备列表出现 `dev_1`，状态为 `offline`。
- 再注册 `dev_2`，多选两台设备后保存分组，刷新分组、加载分组、删除分组均可操作。
- 如果实机截图接口可用，截图会显示在右侧预览；点击预览可自动填入 `Click X/Y`。
- 点击 `Kit Gate` 后能看到采购/SOP 文档、Route、Doctor、HID 扫描、证据计划和 Open P1 stop line；模板路线或未跑 Doctor 时必须显示 fail/pending。
- 点击 `iOS SOP` 后能看到 AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、Auto-Lock、brightness、network、AirPlay、Hub/Cable、baseline artifact 和 claim boundary；离线或 `real_ios_verified=False` 时不得显示为实机控制通过。
- 接入真实 receiver 后，`Shot Bench` 能导出连续截图质量审计；离线或未接 receiver 时失败是预期结果。
- 可以拖拽截图区域保存模板，并用 `Find` 调用找图接口。
- 可以点击截图取色，并用 `Find Color` 调用找色接口。
- 可以用 `OCR` 和 `Find Text` 做基础文字识别验证。
- 多选设备列表中的多台设备后，可以批量点击、滑动、输入，并查看每台结果。
- 底部 `Scenario` 选择 `tests/fixtures_script_runner_dry_run.json`，保持 `Dry Run` 勾选运行，应出现 `Scenario ok` 并生成场景汇总。
- 点击 `Summary` 后能生成 `evidence/<run_id>.md`。
- 底部 `Manual` 行能记录人工观察事件，例如 `Click observed` + `pass/fail` + 备注。
- 顶部 `Attach Log` 导入含 receiver/HID/capture 失败的日志后，勾选 `Record` 时应产生 `Attach Log triage` JSONL；失败 severity 应进入 Triage 的对应 failure category，但不能让 Acceptance 的 `manual_observation` 通过。
- `Control Bench` 能把点击、滑动、文本输入区分为 pending/ready/pass/fail；只有 Manual pass 才能证明该 lane 有真实 iPhone 响应。
- `Ctrl Ledger` 能把 HID click、HID swipe、Keyboard input 三条 Manual proof lane 分开审计；一条泛化 Manual 记录不能关闭三条 lane。
- 点击 `Rerun` 后能看到失败类别、Route/Doctor/Acceptance/Readiness gate、fresh run_id 规则、证据保留项和停止线；离线或 `real_ios_verified=False` 时不得显示为实机控制通过。
- 点击 `Recovery` 后能看到 receiver/capture、HID、校准、视觉/业务状态、群控隔离、performance watchdog 和 handoff lane；每行必须有恢复步骤、验证步骤、证据保留项和停止线。
- 从截图填充并保存校准后，`/calibration/get` 能返回同一份配置。

实机通过标准：

- 扫描到真实硬件串口。
- 能绑定硬件。
- 能启动投屏和采集。
- `Kit Gate` 的 Open P1 stop line 为 pass；如果 XP hardware comparison 仍为 warn，只能声明通用 P1 探索，不得声明 XP 专用硬件/4.4/自动绑定对标完成。
- `iOS SOP` 的设备身份、AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、锁屏/亮度、网络/AirPlay、Hub/Cable 和 baseline artifact 都已填写；该表只能开放测试，不能替代控制证据。
- 能完成连续截图质量审计，且不存在黑屏、低纹理或尺寸漂移。
- 能完成点击、滑动、输入的人工确认。
- `Control Bench` 中点击、滑动、文本输入均为 pass；如果只显示 ready，说明 API/HID 命令存在但还缺人工真机确认。
- 点击、滑动、输入后的人工观察必须写入 evidence；API 返回成功不能单独作为实机通过证据。
- 能完成左上、右下、中心、刘海/灵动岛附近、底部 Home Indicator 附近五点校准，并把结果写入 evidence。
- 能加载 4 台设备分组并执行批量点击、滑动、输入；单台失败不影响其他设备返回结果。
- 能用 GUI 执行单设备闭环 JSON 场景：截图、识别、操作、等待、人工观察记录都落到同一个 `run_id`。
- 每轮测试都有 JSONL 证据和 Markdown 汇总；失败项能追溯到设备 ID、步骤、错误文本和截图/模板路径。

### 第 3 步：接入 HID 硬件

```powershell
@'
from imouse.hardware import list_devices
for item in list_devices():
    print(item)
'@ | .\.venv\Scripts\python -
```

记录：

- 端口号，例如 `COM3`。
- 描述。
- 硬件 ID。

通过标准：

- 除 `COM1` 外能看到新串口。
- 拔插硬件时端口列表有变化。

### 第 4 步：绑定硬件

假设硬件端口为 `COM3`：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api/device/bind -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\",\"port\":\"COM3\",\"baudrate\":9600}"
```

通过标准：

- 返回 `state=online`。

风险：

- 如果 XP 专用硬件不是 CH9329 公开串口协议，这一步会失败或无响应。

### 第 5 步：单独验证 HID 点击

先不要接投屏，先确认 iPhone 端是否识别鼠标：

- iPhone 接入 HID 硬件。
- 屏幕上是否出现鼠标指针或可点击迹象。
- 调用点击接口时，是否有实际响应。

示例：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api/click -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\",\"x\":100,\"y\":100}"
```

通过标准：

- iPhone 有点击反馈。
- 多次点击不会卡住鼠标按钮。

### 第 6 步：安装或替换投屏组件

当前代码要求能找到 `uxplay`：

```powershell
where.exe uxplay
```

如果要严格对标 XP，建议另起专项：

- Windows 原生 AirPlay Receiver。
- 有线投屏链路。
- 多设备单服务。
- 硬解。

当前仓库的 UxPlay/X11 路线只适合先证明画面采集闭环。

投屏路线选择、评分表、receiver 元数据和失败分类见 `docs/receiver_capture_selection.md`。如果现场使用替代 receiver，必须把 `receiver_provider`、版本、路径、启动命令和截图采集方式写入 evidence。

也可以先 dry-run P1 单机控制探针脚本：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run
```

实机运行前必须把脚本里的 `EDIT_ME` 和 provider 信息改成现场真实值。
该脚本的组件台账、截图复核、点击、滑动、输入和最终结论 `record` 已启用 `required_details` 和 `forbid_placeholder_values`，所以实跑时如果仍保留占位值，会直接失败并写入 evidence。

### 第 7 步：启动投屏和采集

```powershell
curl.exe -X POST http://127.0.0.1:9911/api/device/airplay/start -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\"}"
curl.exe -X POST http://127.0.0.1:9911/api/device/capture/start -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\"}"
curl.exe -X POST http://127.0.0.1:9911/api/screenshot -H "Content-Type: application/json" -d "{\"device_id\":\"dev_1\"}"
```

通过标准：

- 返回截图 base64。
- 宽高正确。
- 图像不是黑屏。

### 第 8 步：视觉识别测试

找图：

- 先从真实截图裁剪一个有纹理的按钮模板。
- 不要用纯色块。
- 记录阈值和命中坐标。

OCR：

- 首次运行前确认 `.cache/paddlex` 可写。
- 第一次可能下载模型，需要联网。
- 优先只识别局部区域。

### 第 9 步：单设备闭环脚本

标准闭环：

- 截图。
- 连续截图质量 bench。
- 找目标。
- 点击。
- 再截图确认状态变化。
- Control Bench 审计 click/swipe/type lane。
- 失败保存截图和日志。
- 脚本步骤和人工观察写入 evidence。

通过标准：

- 连续 50 次成功。
- 失败时能定位是投屏、识别、点击还是业务页面变化。
- JSON 脚本可重复运行；`--dry-run`、实跑、失败复现三类记录都可追溯。

### 第 10 步：群控递增测试

顺序：

- 1 台跑通。
- 4 台建组 `pilot_4`，跑 30 分钟。
- 10 台建组 `stable_10`，跑 2 小时。
- 20 台以上再评估性能瓶颈。

每轮都记录：

- CPU。
- 内存。
- 网络。
- FPS。
- 投屏断线次数。
- HID 失败次数。
- 脚本失败截图。
- 分组名、组内设备数、失败设备 ID。
- 每轮开始和结束时导出 `state/groups.json`，确认分组没有丢失或重复设备。

## 下一轮研发建议

优先级从高到低：

1. 先按 `docs/p1_single_device_runbook.md` 跑一台 iPhone，拿到真实投屏、HID、截图、校准、点击、滑动、输入 evidence。
2. P1 通过后按 `docs/p2_p3_stability_runbook.md` 连续跑两轮 P2，再进入 4 台 P3 试点。
3. 明确 Windows 投屏路线：当前 UxPlay/X11 不足以对标 XP；如果使用替代投屏组件，必须把组件名称、版本、路径和截图采集方式写入 evidence。
4. 对照 `docs/receiver_capture_selection.md` 和 `docs/hid_hardware_protocol_benchmark.md` 做投屏/硬件路线决策，不要在路线未定时扩到多台。
5. 对照 `docs/xp_core_backlog.md` 处理 P0 项：投屏路线、HID 链路、坐标校准、evidence 标准化。
6. 做图像资产规范：模板裁剪、阈值、区域、失败截图、版本管理。
