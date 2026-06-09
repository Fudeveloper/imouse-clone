# iMouse Clone

> 当前研发目标锁定 iMouse XP 版对标。原仓库代码仍是未完成、未实机验证的 Python 原型，不能视为已达到 XP 版能力。
>
> 先读这些文档：
>
> - `docs/imouse_xp_research.md`：iMouse XP 公开能力、行业路线、实现架构和研发启示。
> - `docs/xp_public_source_refresh.md`：2026-06-09 公开资料复核，沉淀 XP Python/API、硬件、Kernel/Console 和 SOP 影响。
> - `docs/xp_public_source_audit.md`：可重复执行的公开源审计命令，记录 URL 状态、PyPI 版本、关键词漂移、SOP owner 和声明边界。
> - `docs/imouse_xp_iteration_lessons.md`：iMouse XP 迭代路径、现场踩坑点和转化成我们研发任务的路线。
> - `docs/industry_current_state_snapshot_2026.md`：当前公开来源、行业主路线、SOP 门禁、GUI 承载边界和术语口径快照。
> - `docs/industry_landscape_2026.md`：iOS 群控行业现状、主流路线、XP 类产品壁垒和研发顺序。
> - `docs/industry_sop_playbook.md`：iMouse XP 对标研发作战手册，集中回答主流路线、P1 决策、现场 SOP、晋级门和失败分流。
> - `docs/industry_sop_radar.md`：iOS 群控行业现状、XP 公开信号、现场 SOP、研发优先级和 GUI Industry 雷达。
> - `docs/ios_field_settings_sop.md`：真实 iPhone 开跑前的 AssistiveTouch、键盘/鼠标、亮度/锁屏、网络、Hub/Cable 和证据门核对表。
> - `docs/xp_roadmap.md`：XP 对标研发路线图，把公开信号、行业 SOP、本地实现、证据门和下一步研发动作合成 GUI Roadmap。
> - `docs/mainstream_route_decision.md`：iOS 群控主流路线、P1 receiver/HID/采购决策和开测停止线。
> - `docs/ios_group_control_sop.md`：iOS 群控 SOP、验收流程和常见问题。
> - `docs/xp_parity_matrix.md`：iMouse XP 公开信号、当前实现、证据、差距和下一步研发动作的对标矩阵。
> - `docs/field_test_matrix.md`：实机测试矩阵、阶段门、指标和失败归类。
> - `docs/p1_single_device_runbook.md`：P1 单台 iPhone 实机首测手册，按步骤跑 doctor、GUI、HID、投屏、校准、脚本和 evidence。
> - `docs/p2_p3_stability_runbook.md`：P2/P3/P4 稳定性实机手册，覆盖 30 分钟单台、4 台试点、10 台 2 小时和失败复盘。
> - `docs/hardware_test_bench_checklist.md`：硬件采购、测试台搭建、物料编号、XP 专用硬件对比和常见现场坑。
> - `docs/receiver_capture_selection.md`：投屏 receiver、截图采集、有线投屏和采集卡路线的选型矩阵。
> - `docs/hid_hardware_protocol_benchmark.md`：CH9329、XP 专用硬件和自研 HID 的同场对标测试表。
> - `docs/xp_core_backlog.md`：按 iMouse XP 公开能力拆出的核心功能差距与研发 backlog。
> - `docs/xp_gap_audit.md`：XP 核心能力差距审计工具，输出机器可读 JSON/Markdown，辅助判断下一轮研发优先级。
> - `docs/verification_plan.md`：当前代码验证结论，以及你后续可逐步执行的实机测试方法。
> - `docs/xp_api_compat.md`：当前已实现的 XP 风格 `/api` + `fun` 兼容入口。
> - `docs/gui_prototype.md`：当前 Python GUI 原型的启动方式、能力边界和实机测试路径。
> - `docs/gui_live_probe.md`：GUI Live Probe 现场工作台，用于把 P1/P2/P3/P4 缺口、证据和阶段门集中到一张可导出的状态表。
> - `docs/gui_industry_current_snapshot.md`：GUI `Snapshot` 板，把当前行业/source/SOP 快照转成采购、路线、设置、证据和声明边界动作。
> - `docs/gui_route_procurement_sop.md`：GUI `Procure` 板，把行业路线知识转成供应商问题、采购停线、实验室 SOP、来源/包卫生和证据门。
> - `docs/operator_worksheet.md`：现场操作员可填写 worksheet，记录逐步结果、附件、失败分类和验收命令。
> - `docs/sop_problem_ledger.md`：GUI Problems 问题台账，把行业坑点、field failure、最小重跑和证据停止线沉淀成 SOP。
> - `docs/coordinate_calibration.md`：坐标校准、点偏排查和校准 API。
> - `docs/validation_evidence.md`：现场测试证据 JSONL、Markdown 汇总和失败复盘方法。
> - `docs/script_runner.md`：JSON 脚本运行器，用于单机闭环和群控回归。
> - `docs/preflight_doctor.md`：实机前环境、依赖、串口、服务端口检查。
> - `docs/readiness_audit.md`：项目阶段审计，汇总文档、脚本、doctor 和 evidence gate，防止把离线通过误判为实机通过。

iOS 免越狱群控方案原型 —— AirPlay 投屏 + HID 硬件键鼠 + OpenCV/PaddleOCR 视觉识别。

> iPhone 端零安装，仅需开启 AirPlay 屏幕镜像。
> 当前仓库只完成了协议层、GUI 原型和离线测试；真实 iPhone 完美控制必须按 SOP 接硬件验证。

## 当前验证命令

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.main --check
.\.venv\Scripts\python -m imouse.doctor --json
.\.venv\Scripts\python -m imouse.readiness --target p1
```

当前本机结论：

- 需要以当前 `python -m unittest discover -s tests -v` 输出为准；最近一次本地验证为 332 个离线测试通过。
- Python 依赖检查通过，但 `uxplay` 缺失，所以 AirPlay 投屏链路还未在本机验证。
- HID 硬件、iMouse XP 专用硬件、4.4 固件、真实 iPhone 点击/滑动/输入尚未实测。

## 现场执行包

每轮实机测试前，先生成一份本轮执行包。它会汇总当前 doctor/readiness 状态、必须填写的设备组件台账、GUI 步骤、脚本 dry-run/实跑命令、验收命令和失败分流表：

```powershell
.\.venv\Scripts\python -m imouse.field_packet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_field_packet.md
```

P3 示例：

```powershell
.\.venv\Scripts\python -m imouse.field_packet --stage p3 --run-id pilot_4_YYYYMMDD --devices dev_1,dev_2,dev_3,dev_4 --output evidence\pilot_4_YYYYMMDD_field_packet.md
```

执行包只是 checklist，不是通过证明；真实通过仍以 evidence、acceptance 和 readiness 为准。

## Python GUI 原型

```powershell
.\.venv\Scripts\python -m imouse.gui
```

新增 `Receiver` / Receiver Route Gate：在 Live Probe 中检查 Route Decision、receiver provider、UxPlay 替代路线降级、窗口/采集绑定、截图证据和声明边界；导出 `evidence/<run_id>_<stage>_receiver_route_gate.md`。它只做接收链路预检，不写 evidence，也不证明真实 iOS 控制。

新增 `Rx Bootstrap`：在 GUI 或 CLI 中为 Windows Receiver、有线投屏、采集卡等替代路线生成 `evidence/<run_id>_route_decision.json` 草案和 `evidence/<run_id>_<stage>_receiver_bootstrap.md`，让 Doctor 可以按替代 receiver 预检并把缺 `uxplay` 降为 route-specific warning。它仍不允许 P1，也不证明截图质量、HID 响应或真实 iPhone 控制。

新增 `Runner` / Field Evidence Runner：在同一个 `run_id` 下逐项跟踪 Route Decision、route-aware Doctor、截图质量、HID click/swipe/text 三条人工观察、Acceptance、Gap、Readiness、Evidence Pack 和最终声明边界；导出 `evidence/<run_id>_<stage>_field_runner.md`，并提供可复制 PowerShell 命令。它是现场执行台，不写 evidence，也不替代真实 iPhone 观察。

新增 `Procure` / Route Procurement SOP：把 iMouse XP 与主流行业路线知识转成供应商问题、采购停线、实验室 SOP、来源/包卫生和证据门；导出 `evidence/<run_id>_<stage>_route_procurement_sop.md`。它不采购硬件、不安装包、不写 JSONL evidence，也不证明 iOS 控制或 XP parity。

GUI 当前支持启动/停止本地服务、设备注册、硬件扫描/绑定、AirPlay/截图入口、截图预览取点、模板裁剪、模板资产检查、找图、找色、OCR、找文字、多选批量点击/滑动/输入、Command Queue、本地设备分组、坐标校准、preflight doctor、Route Decision 生成/编辑/补齐清单/校验、Metadata 一键带入、占位符/必填项提示、Field Packet 生成、Operator Worksheet 生成、Acceptance 阶段门报告、Acceptance Gap 补证据清单、Live Probe 状态表、GUI Control Center 总控层、GUI Knowledge Center 行业/SOP/XP 对标知识层、GUI Industry SOP Radar 行业现状/SOP 决策雷达、GUI Route Procurement SOP 采购/供应商问题/停线台账、GUI Mainstream Route Matrix 主流路线决策矩阵、GUI Verification Walkthrough 逐步验证工作台、XP Core Function Matrix 核心功能覆盖矩阵、XP API Coverage Board API/SDK/fun 覆盖边界看板、GUI Script Coverage Board 脚本覆盖/实跑边界看板、Acceptance Proof Map 验收证据闭环地图、GUI Pitfall Library 群控坑点/SOP 风险库、GUI SOP Problem Ledger 问题沉淀台账、XP Public Source Ledger 公开来源审计台账、XP Source Refresh Board 公开来源刷新看板、XP Public Source Audit 公开源 URL/PyPI 可重复审计、XP Package Namespace Guard 包名/供应链/SDK 漂移守卫、XP Iteration Radar 迭代路线/踩坑雷达、XP Iteration Timeline 迭代时间线/踩坑复盘板、GUI XP Roadmap 对标研发路线/证据闭环看板、Device/iOS Compatibility Matrix 本地兼容覆盖矩阵、GUI Goal Gate 四项验收目标看板、GUI Field Kit Gate 采购/现场准备闸门、GUI iOS Field Settings SOP 真实 iPhone 设置核对表、GUI Hardware Bench 硬件测试台、GUI Capture Quality Bench 连续截图质量压测、GUI Control Response Bench 点击/滑动/文本输入响应审计、GUI Control Evidence Ledger 分 lane 实控证据台账、Field Evidence Wizard 现场证据向导、Field Evidence Runner 现场证据执行台、GUI First Run Packet 首轮实机验证包、P1 Trial 单机实测执行板、SOP Board 八步执行台和 `Run Selected` 主命令、Scenario Library 阶段脚本选择、GUI Session Snapshot、Field Runbook 现场向导、P0-P4 Stage Dashboard、GUI Evidence Pack 索引、Evidence Timeline 事件流水、Callback Monitor 回调事件监控、Attach Log 接收器/HID 日志接入与日志分流证据、Device Evidence Matrix 按设备证据覆盖、Issue Triage 失败类别复盘、Rerun Playbook 最小重跑决策表、Recovery Drill 恢复演练表与恢复执行记录、Real-run Guard 实跑拦截、XP Gap 核心能力差距审计、JSON 场景 dry-run/实跑、测试证据记录与汇总、Review 复盘报告、Readiness 阶段审计、带失败分类的人工观察留痕；行业现状快照见 `docs/industry_current_state_snapshot_2026.md`，API 和脚本层已支持多点找色、WebSocket `/api` XP fun 调用和 callback ledger 初版。

新增 `iOS SOP` 面板用于核对真实 iPhone 开跑前的 AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、Auto-Lock、brightness、network、AirPlay、Hub/Cable、baseline screenshot 和 manual observation 边界。

详细步骤见 `docs/gui_prototype.md` 和 `docs/verification_plan.md`。

### GUI Local Verification

`Local` in the Live Probe panel opens a command-by-command local verification board and exports `evidence/<run_id>_<stage>_local_verification.md`.

It covers:

- `.\.venv\Scripts\python -m unittest discover -s tests -v`
- `.\.venv\Scripts\python -m compileall -q imouse tests`
- `.\.venv\Scripts\python -m imouse.main --check`
- `.\.venv\Scripts\python -m imouse.doctor --json`
- `.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --json`
- `.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id <run_id>`
- `.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\<run_id>.jsonl`

Boundary: Local Verification is a terminal guide only. It does not run commands, does not write JSONL evidence, and does not prove real iOS control.

### XP Event/Error Contract

`Events` in the Live Probe panel opens the XP event/error contract board and exports `evidence/<run_id>_<stage>_xp_event_error_contract.md`.

It audits `/api` envelope fields, HTTP/WebSocket `msgid`, callbacks, Attach Log ingestion, receiver/capture/HID error taxonomy, and claim boundaries. It is a SOP/compatibility audit only; JSONL evidence, screenshot quality, Manual observation, Acceptance, and Readiness still decide real iOS control claims.

### XP API Coverage Board

`API Cov` in the Live Probe panel opens the XP API/SDK coverage board and exports `evidence/<run_id>_<stage>_xp_api_coverage.md`.

It maps XP-style fun/helper domains to local API coverage, tests, runtime gates, field evidence and claim boundaries. Local API tests close only P0 compatibility; receiver, HID, click, swipe, text, screenshot, group, cloud and XP hardware parity claims still require their own evidence gates.

### GUI Script Coverage Board

`Script Cov` in the Live Probe panel opens the script coverage board and exports `evidence/<run_id>_<stage>_script_coverage.md`.

It maps stage scenario files, dry-run, Real-run Guard, metadata records, screenshot probes, HID click/swipe/text lanes, vision/OCR, metrics, group scripts, failure replay, and claim boundaries. Dry-run or scenario success closes only script readiness; it does not prove real iPhone response, group control, or XP script parity.

### GUI Acceptance Proof Map

`Proof Map` in the Live Probe panel opens the acceptance proof map and exports `evidence/<run_id>_<stage>_proof_map.md`.

It maps every Acceptance/Readiness row to the exact GUI action, JSONL/event requirement, artifact, next command, and stop rule. Proof Map is navigation only: same-run screenshot quality, lane-separated Manual click/swipe/text observations, Acceptance PASS, Readiness PASS, and exact device/iOS/receiver/HID scope still decide real iOS control claims.

### GUI Claim Scope

`Claim Scope` in the Live Probe panel opens the handoff wording board and exports `evidence/<run_id>_<stage>_claim_scope.md`.

It turns the current Readiness, Acceptance, Proof Map, Evidence Pack, API/Core coverage, compatibility, and XP gap signals into allowed claims and forbidden claims. Claim Scope is wording guidance only: it does not write JSONL evidence, prove real iPhone response, prove group control, prove XP hardware parity, or prove broad iPhone/iOS compatibility.

### GUI Goal Gate

`Goals` in the Live Probe panel opens the four-goal acceptance board and exports `evidence/<run_id>_<stage>_gui_goal_gate.md`.

It now treats Proof Map and Claim Scope as closure inputs for the iOS control and SOP goals, so a clean-looking Acceptance/Readiness run still cannot become a completion claim while proof rows or handoff wording remain blocked.

## Preflight Doctor

```powershell
.\.venv\Scripts\python -m imouse.doctor --markdown evidence\preflight.md
```

Doctor 会检查 Python 版本、模块依赖、receiver provider、`uxplay`、`Xvfb`、串口、工作区可写性、分组/校准/设备组件档案状态文件和可选 API 服务。使用替代 receiver 时传入 `--route-decision evidence\<run_id>_route_decision.json`。详见 `docs/preflight_doctor.md`。

## Evidence 复盘

```powershell
.\.venv\Scripts\python -m imouse.evidence_report evidence\pilot_4_YYYYMMDD.jsonl
.\.venv\Scripts\python -m imouse.acceptance evidence\single_dev1_YYYYMMDD.jsonl --gate p1 --markdown evidence\single_dev1_YYYYMMDD_acceptance.md
.\.venv\Scripts\python -m imouse.acceptance evidence\single_dev1_YYYYMMDD.jsonl --gate p1 --gap-markdown evidence\single_dev1_YYYYMMDD_p1_gap.md
```

报告会聚合状态、设备、失败分类、metrics 指标和下一轮排查建议；`imouse.acceptance` 会按 P1/P2/P3/P4 阶段门做机器可判定的晋级检查，包含设备追踪、组件追踪、人工观察、截图质量和 metrics；`--gap-markdown` 会把失败 check 转成补证据动作。详见 `docs/validation_evidence.md`。

## JSON 脚本运行器

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\single_device_smoke.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run
```

运行器支持单设备点击/滑动/输入、按分组批量操作、找图后点击、OCR/找字、等待、重复轮次、系统指标和人工记录，并自动写入 evidence。详见 `docs/script_runner.md`。

可直接 dry-run 的样例在 `scripts/`：

- `scripts/p1_single_device_control_probe.json`
- `scripts/single_device_smoke.json`
- `scripts/p1_receiver_capture_probe.json`
- `scripts/p2_single_device_stability.json`
- `scripts/pilot_4_group_smoke.json`
- `scripts/p3_pilot4_30min_watchdog.json`
- `scripts/stable_10_group_watchdog.json`

## 架构

```
iPhone → AirPlay 投屏 → PC (UxPlay) → 截图 → OpenCV/PaddleOCR → CH9329 键鼠注入
```

这张图是当前原型路线。对标 iMouse XP 时，后续必须把 Windows 投屏服务、有线投屏、硬件解码、XP 专用硬件/固件和多设备窗口分离单独验证。

| 层 | 技术 |
|---|------|
| 硬件 | CH9329 HID 芯片 (¥15/个), USB Hub, Lightning OTG |
| 投屏 | UxPlay (C++ AirPlay 接收器) |
| 截图 | mss / PIL |
| 找图 | OpenCV matchTemplate |
| 找色 | OpenCV inRange |
| OCR | PaddleOCR (百度飞桨) |
| API | FastAPI + WebSocket (port 9911) |

## XP 风格 API

启动服务：

```powershell
.\.venv\Scripts\python -m uvicorn imouse.server:app --host 127.0.0.1 --port 9911
```

XP 兼容入口：

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/dev/list&msgid=1"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/device/register\",\"data\":{\"id\":\"dev_1\"}}"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/group/save\",\"data\":{\"name\":\"pilot_4\",\"ids\":[\"dev_1\",\"dev_2\"]}}"
```

详细协议见 `docs/xp_api_compat.md`。

## REST API 参考

保留旧 REST 接口作为调试兼容层，响应格式：

```json
{
  "status": 200,
  "message": "成功",
  "data": { "code": 0, "..." }
}
```

### 设备管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/devices` | 设备列表 |
| POST | `/api/device/register` | 注册设备 |
| POST | `/api/device/bind` | 绑定 CH9329 硬件 |
| GET | `/api/hardware/scan` | 扫描可用硬件 |
| POST | `/api/device/airplay/start` | 启动 AirPlay |
| POST | `/api/device/capture/start` | 开始截图采集 |

### 键鼠操作

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/click` | 点击坐标 |
| POST | `/api/swipe` | 滑动 |
| POST | `/api/type` | 输入文字 |
| POST | `/api/key` | 单键 |
| POST | `/api/combo` | 组合键 |

### 图像识别

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/find_image` | 找图（模板匹配） |
| POST | `/api/find_color` | 找色 |
| POST | `/api/find_colors` | 多点找色 |
| POST | `/api/ocr` | OCR 文字识别 |
| POST | `/api/find_text` | 找文字 |
| POST | `/api/screenshot` | 截图（base64/binary，可裁剪和保存） |

### 典型调用流程

```python
import requests

BASE = "http://localhost:9911"

# 1. 注册设备
r = requests.post(f"{BASE}/api/device/register", json={"device_id": "dev_1"})

# 2. 绑定硬件
r = requests.post(f"{BASE}/api/device/bind", json={
    "device_id": "dev_1", "port": "/dev/ttyUSB0"
})

# 3. 启动 AirPlay → iPhone 扫码投屏
r = requests.post(f"{BASE}/api/device/airplay/start", json={"device_id": "dev_1"})

# 4. 开始采集
r = requests.post(f"{BASE}/api/device/capture/start", json={"device_id": "dev_1"})

# 5. 找图 → 点击
r = requests.post(f"{BASE}/api/find_image", json={
    "device_id": "dev_1",
    "template_path": "templates/buy_button.png",
    "threshold": 0.8,
    "region": [0, 300, 1170, 600]
})
# → {"x": 320, "y": 640, "confidence": 0.95}

requests.post(f"{BASE}/api/click", json={
    "device_id": "dev_1", "x": 320, "y": 640
})
```

## WebSocket

```
ws://localhost:9911/ws
```

支持实时事件推送和设备状态订阅。

## 硬件接线

```
CH9329 模块:
  VCC → 5V (USB)
  GND → GND
  TX  → USB-TTL RX (CH340)
  RX  → USB-TTL TX (CH340)

CH9329 → Lightning OTG → iPhone
```

每台 iPhone 需要一个 CH9329 芯片 + 一条 Lightning OTG 线。多台通过 USB Hub 连接 PC。

## 项目结构

```
imouse/
├── main.py           # 入口，启动服务
├── server.py         # FastAPI + WebSocket API
├── gui.py            # Tkinter GUI 原型
├── xp_client.py      # XP 风格 /api + fun 客户端
├── script_runner.py  # JSON 场景脚本运行器
├── field_packet.py   # 现场执行包生成器
├── route_decision.py # P1 receiver/HID 路线决策记录生成与校验
├── validation.py     # 实机/现场测试证据记录
├── doctor.py         # 实机前环境检查
├── calibration.py    # 坐标校准和映射
├── hardware.py       # CH9329 串口控制
├── airplay.py        # UxPlay 子进程管理
├── capture.py        # 屏幕截图引擎
├── vision.py         # OpenCV + PaddleOCR
├── device_manager.py # 设备注册/绑定/状态/本地分组
└── __init__.py
```
