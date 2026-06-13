# 逐步跟测方法

本文件给操作者逐步跟测。它不证明已经实现 iOS 完美控制，也不替代 GUI、JSONL evidence、Acceptance 或 Readiness。它的作用是让每一轮测试都按同一顺序执行、记录、失败分类和复盘。

## 0. 当前边界

截至本轮验证，仓库离线测试可通过，但现场 P1 仍被阻断：

- `uxplay` 缺失时，默认 AirPlay prototype route 不能通过 Doctor。
- 没有真实 iPhone JSONL evidence 时，Readiness P1 必须失败。
- GUI reports、Source Refresh、XP Drill、XP Lab、Roadmap 和 Pack 不是真实设备控制 evidence。

只有同一 `run_id` 下同时具备截图质量、真实 iPhone 手工观察、JSONL evidence、Acceptance PASS、Readiness PASS，才能讨论 P1 控制通过。

## 1. P0 本地自检

在 PowerShell 里从仓库根目录执行：

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.main --check
```

通过标准：

- 单元测试输出 `OK`。
- `compileall` 无输出且退出 0。
- dependency check 中 Python 依赖可用；如果 `uxplay MISSING`，记录为 receiver 阻断，不要进入默认 AirPlay 实跑。

失败处理：

- 测试或 compileall 失败：先修代码。
- 只有 `uxplay` 缺失：进入 receiver 选型，不要宣称 P1 可跑。

## 2. 建立本轮 run_id

GUI 操作：

1. 启动 GUI：`.\.venv\Scripts\python -m imouse.gui`
2. 设置 `Evidence run_id`，例如 `p1_iphone12_20260609_a`。
3. 设置 `Stage=p1`。
4. 选择一个真实设备 ID。
5. 点击 `Prepare`。

记录要求：

- 本轮所有 JSONL、Route、Doctor、截图、Acceptance、Readiness 都使用同一个 `run_id`。
- 如果 receiver/HID/iPhone/Hub/cable 换了，或者失败的 Route Decision 已经写入 evidence，修复后换新 `run_id`。

## 3. 刷新行业/XP 知识层

GUI 顺序：

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Industry -> Routes -> Kit Gate
```

检查点：

- `Src Refresh` 只确认公开来源刷新责任，不抓网页、不写 evidence。
- `Src Audit` 可在 GUI 中离线或联网生成 URL/PyPI 状态快照，但仍不写 JSONL evidence、不证明真机。
- `XP Drill` 把 XP 迭代细节落到验证 drill，不证明我们已支持。
- `XP Lab` 把 XP 硬件/receiver 信号转化为采购和实验室验证门；它仍不证明我们已支持。
- `Procure` 用来把主流路线转成供应商问题、采购停线、实验室 SOP 和证据门。
- `Industry` 和 `Routes` 用来确认主线仍是 receiver/capture + USB HID + vision/OCR + local API。
- WDA/Appium/MDM/Shortcuts 只能作为辅助，不作为 XP-style 黑盒主线。

失败处理：

- 任一行是 `fail/pending/warn` 时，点 `Run Selected` 去对应 GUI 面板处理，不要跳过。

## 4. 锁定 receiver 和 HID 路线

GUI 顺序：

```text
Rx Score -> Rx Bootstrap -> Route Init/Edit -> Checklist -> Validate -> Rx Setup -> Rx Evidence -> Receiver
```

必须填写真实值：

- receiver route、名称、版本、路径、启动命令、AirPlay 名称、capture method、window/process binding。
- HID route、serial/device、firmware/module ID、Hub port、cable label。
- iPhone ID、型号、iOS 版本、方向、AssistiveTouch、pointer speed、mouse parameter profile、QR policy。

说明：

- `Rx Bootstrap` 只把替代 receiver 路线写成草案，默认仍是 `allowed_to_run_p1=false`。
- 只有在 Route Init/Edit、Checklist、Validate 把 receiver、HID、iPhone、bench 全部补齐后，才允许检查 `allowed_to_run_p1=true`。
- `Rx Setup` 解决安装/启动/窗口绑定问题；`Rx Evidence` 解决接收端截图证据、route-aware Doctor、日志和 HID handoff 停线问题。

通过标准：

- Route Decision 没有 placeholder。
- `allowed_to_run_p1=true`。
- 无 open blocker。
- Receiver Gate 不把 `uxplay` fail 误当成通过；如果使用 Windows/wired/capture-card 替代，必须写清替代链路。
- Rx Evidence 的第一阻断项已经处理；它本身不证明实机控制。

## 5. Doctor 和本地命令复核

GUI 操作：

```text
Doctor -> Local -> Run Selected
```

命令：

```powershell
.\.venv\Scripts\python -m imouse.doctor --json
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --json
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id <run_id>
```

通过标准：

- Doctor 没有 `fail`，或 route-aware Doctor 对明确的非 UxPlay 路线给出可解释 warn。
- dry-run 只证明脚本结构，不证明实机控制。

停止线：

- Doctor fail 时停止所有真实 HID 操作。
- route-aware Doctor 不能定位 receiver provider 时，回到 `Rx Score/Rx Bootstrap/Rx Setup/Route Edit`。

## 6. 投屏和截图质量

GUI 顺序：

```text
Screenshot -> Shot Bench -> Timeline
```

通过标准：

- 截图来自当前选中的真实 iPhone。
- 非黑屏、非白屏、非 stale、非错窗口、非裁剪错误。
- P1 至少保留一组可解释截图；P2 前做 100-screenshot stability。

失败分类：

- 找不到 receiver：`airplay_discovery`
- 黑屏/断流：`airplay_stream`
- 截图错窗口/裁剪/尺寸漂移：`capture`

## 7. iOS 设置和坐标校准

GUI 顺序：

```text
iOS SOP -> P1 Trial -> Ctrl Ledger -> Control Bench
```

核对：

- AssistiveTouch 开启。
- pointer speed/profile 被记录。
- rotation lock、auto-lock、brightness、keyboard behavior 被记录。
- 当前截图和当前方向一致。

通过标准：

- 能从当前截图解释点击点。
- 校准不是凭经验口述，而是保存到当前 run 的证据链。

失败分类：

- 坐标偏移、方向错误、安全区错误：`calibration`

## 8. 真实 HID 控制

GUI 顺序：

```text
P1 Trial -> Ctrl Ledger -> Control Bench -> Transcript -> Runner
```

动作：

1. 只点一个安全、可见、低风险位置。
2. 做一次可观察 swipe，并确认 release。
3. 在明确输入框里输入短 ASCII 文本。
4. 每一步都用 `Manual pass/fail` 记录操作者亲眼看到的 iPhone 响应。

通过标准：

- API/HID command success 和真实 iPhone 可见响应一致。
- click、swipe、text 三类都有手工观察。
- Ctrl Ledger 中 `HID click`、`HID swipe`、`Keyboard input` 三行分别通过，且 `Generic Manual quarantine` 没有把一条泛化 Manual 当作三条 lane 的证明。
- Runner 中 `HID click`、`HID swipe`、`Keyboard input` 三行分别通过。

停止线：

- API 返回 OK 但 iPhone 没反应，记录 `hid` fail，不得记 pass。
- 只看到电脑端日志，不算真实控制。

## 9. Acceptance 和 Readiness

GUI 顺序：

```text
Runner -> Acceptance -> Gap -> Readiness -> Goals -> Pack
```

命令：

```powershell
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1 --markdown evidence\<run_id>_p1_acceptance.md
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1 --gap-markdown evidence\<run_id>_p1_gap.md
.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\<run_id>.jsonl --markdown evidence\<run_id>_readiness.md
```

通过标准：

- `component_traceability` pass。
- `screenshot_quality` pass。
- `manual_observation` pass。
- Doctor 无 fail。
- Readiness 中 `real_ios_control_verified=True`。

停止线：

- Acceptance 或 Readiness 任一失败，不得称 P1 通过。
- `real_ios_verified=False` 时，不得称 iOS 完美控制。

## 10. P2/P3/P4 递进

只有 P1 通过后再做：

- P2：单台稳定性、100 截图、metrics、恢复演练。
- P3：4 台 pilot，必须有 per-device evidence。
- P4：10 台稳定性，必须有 metrics、日志、失败隔离、Recovery 记录。

停止线：

- 任何 group fail 没有 device id、artifact、failure category、receiver/HID/Hub/cable 上下文时，停止扩容。

## 11. XP 对标复盘

GUI 顺序：

```text
Sources -> Src Refresh -> Action Map -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> XP Timeline -> Iter Radar -> XP Drill -> XP Arch -> XP Lab -> Core -> XP Gap -> Roadmap
```

结论边界：

- API/SDK 通过不等于 XP 对标完成。
- CH9329/generic HID 通过不等于 XP 专用硬件、4.4 固件、自动绑定通过。
- Windows/wired/hardware decode 没有同场证据时，只能写 `unverified`。
- Public source 是研发输入，不是本地 evidence。

`API Cov` closes only local XP API/fun/helper compatibility. It does not close receiver, HID, real iPhone, cloud/account, or XP dedicated-hardware parity evidence gates.

`Script Cov` closes only scenario/dry-run/guard visibility for the current GUI layer. It does not close real-run control, lane-separated Manual proof, group-control, or XP script parity without same-run field evidence.

`Proof Map` closes no evidence by itself. It tells the operator which Acceptance/Readiness gate is blocked, which GUI action to run next, which JSONL/artifact is required, and which stop rule applies.

`Claim Scope` closes no evidence by itself. It turns the current gate state into allowed and forbidden handoff wording so P0/GUI/API/source progress is not described as real iPhone control, group control, XP hardware parity, or broad compatibility.

## 12. 最小交付包

每轮结束至少导出：

- Evidence JSONL
- Route Decision JSON/Markdown
- Doctor report
- Acceptance/Gap report
- Readiness report
- Evidence Pack
- Transcript 或 Operator Worksheet
- Timeline/Matrix/Triage
- XP Gap

交付话术必须按最强证据写：

- P0：离线原型可运行。
- P1：单台真实 iPhone 当前 run 控制通过。
- P2：单台稳定性通过。
- P3：4 台 pilot 通过。
- P4：10 台稳定性通过。
- XP parity：必须另有 XP 硬件/receiver/firmware/自动绑定/硬解同场证据。
