# GUI Live Probe 现场工作台

更新时间：2026-06-09

`Live Probe` 是 Python GUI 里的现场总控层，用来把 P1/P2/P3/P4 真机验证拆成可刷新、可导出的状态表。它不会直接证明 iPhone 已经被控制，也不会把报告本身写成 evidence；它只负责告诉操作者当前还缺哪类现场证据。

## 入口

启动 GUI：

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

底部 `Operation Log` 区域有 `Live Probe` 面板：

- `Prepare`：设置当前阶段和 gate，加载默认探针脚本，并为当前 `run_id` 创建 route decision JSON。
- `Load Probe Script`：按当前阶段加载默认 JSON 场景，默认保持 `Dry Run`。
- `Dry Run`：加载默认探针脚本并执行 dry-run。
- `Doctor`：运行 preflight doctor，并把结果同步到状态表。
- `Acceptance`：读取当前 `evidence/<run_id>.jsonl`，执行阶段门验收。
- `Readiness`：生成 readiness 审计报告。
- `Refresh`：只读当前路线、evidence、doctor 缓存和验收状态，刷新状态表。
- `Report`：导出 `evidence/<run_id>_<stage>_live_probe.md` 快照。
- `Dashboard`：打开 P0/P1/P2/P3/P4 阶段驾驶舱，显示每一阶段的状态、设备数、证据概况、默认脚本、阻断项和下一步动作。
- `Pack`：导出 `evidence/<run_id>_<stage>_evidence_pack.md`，列出本轮必须/建议存在的 evidence、route、doctor、worksheet、acceptance、gap、readiness 等产物。
- `XP Gap`：导出 `evidence/<run_id>_<stage>_xp_gap_audit.md`，按 XP 核心能力域列出当前实现、差距、证据门和下一步研发动作。
- `Core`：打开并导出 `evidence/<run_id>_<stage>_xp_core_functions.md`，把 XP 核心功能拆成 API/SDK、receiver、截图、HID、校准、视觉、脚本、GUI、可观测性和商业运维等证据门。
- `Verify`：打开并导出 `evidence/<run_id>_<stage>_verification_walkthrough.md`，把 P0/P1/P2/P3/P4 验证步骤、命令、预期、证据和停止线集中成逐步测试方法。
- `Industry`：打开并导出 `evidence/<run_id>_<stage>_industry_sop_radar.md`，把行业主流路线、XP 产品壁垒、iPhone 现场设置、receiver/HID/视觉/运维/扩容和声明边界映射到 GUI 动作。
- `Snapshot`: opens and exports `evidence/<run_id>_<stage>_industry_current_snapshot.md`, turning current industry/source/SOP state into procurement, route, setup, evidence, and claim-boundary actions.
- `Procure`: opens and exports `evidence/<run_id>_<stage>_route_procurement_sop.md`, turning route knowledge into supplier questions, buying stop lines, lab SOP, source/package hygiene, and evidence gates.
- `API Cov`: opens and exports `evidence/<run_id>_<stage>_xp_api_coverage.md`, mapping XP fun/helper domains to local tests, runtime gates, field evidence and claim boundaries.
- `Script Cov`: opens and exports `evidence/<run_id>_<stage>_script_coverage.md`, mapping XP-style stage scripts, dry-run, real-run guard, metadata, screenshot, HID lanes, vision/OCR, metrics, group scripts, failure replay, and claim boundaries.
- `Proof Map`: opens and exports `evidence/<run_id>_<stage>_proof_map.md`, mapping each Acceptance/Readiness gate to the required JSONL evidence, GUI action, artifact, next command, and stop rule.
- `Claim Scope`: opens and exports `evidence/<run_id>_<stage>_claim_scope.md`, turning the current proof state into allowed and forbidden handoff wording. It does not write JSONL evidence or prove real iPhone response.
- `Runbook`：打开并导出 `evidence/<run_id>_<stage>_field_runbook.md`，把现场执行顺序、停止线和晋级门放到一张操作者向导里。
- `Sources`：打开并导出 `evidence/<run_id>_<stage>_xp_public_sources.md`，把官网、Python XP、XP API、XP 帮助页的公开信号映射到研发影响、验证缺口和下一步 GUI 动作。
- `Action Map`: opens and exports `evidence/<run_id>_<stage>_xp_source_action_map.md`, turning public XP/package/Apple signals into R&D decisions, SOP gates, stop rules, and GUI owners.
- `Coach`: opens and exports `evidence/<run_id>_<stage>_p1_test_coach.md`, guiding the first real-iPhone run step by step with commands, pass criteria, failure handling, and evidence rules.
- `Routes`：打开并导出 `evidence/<run_id>_<stage>_mainstream_routes.md`，把 XP 式黑盒控制主线、UxPlay/Windows/wired/capture receiver、CH9329/XP hardware HID、WDA/Appium 和 MDM/Shortcuts 辅助路线映射到 P1 证据门和停止线。
- `Pitfalls`：打开并导出 `evidence/<run_id>_<stage>_pitfall_library.md`，把 receiver、HID、校准、视觉、群控、性能、业务状态、claim boundary 和 XP 硬件对标常见坑映射到 SOP 探针、停止线和 GUI 动作。
- `Rerun`：打开并导出 `evidence/<run_id>_<stage>_rerun_playbook.md`，把失败类别和阶段 gate 转成最小重跑动作、fresh run_id 规则、证据保留项和停止线。
- `Recovery`：打开并导出 `evidence/<run_id>_<stage>_recovery_drill.md`，把 receiver/HID/校准/视觉/群控/性能恢复动作、验证步骤、证据保留项和停止线集中成演练表；`Record Pass` / `Record Fail` 可记录选中恢复 lane 的执行结果。
- `Iter Radar`：打开并导出 `evidence/<run_id>_<stage>_xp_iteration_radar.md`，把 XP 公开迭代线索转成研发优先级、SOP 测试路径和停止线。
- `XP Timeline`: opens and exports `evidence/<run_id>_<stage>_xp_iteration_timeline.md`, turning public XP iteration signals into chronological lessons, pitfalls, SOP gates, and stop rules.
- `XP Drill`：打开并导出 `evidence/<run_id>_<stage>_xp_iteration_drill.md`，把 XP 迭代细节转成验证 drill、所需证据、失败分类和停止线。
- `XP Arch`: opens and exports `evidence/<run_id>_<stage>_xp_architecture.md`, mapping the inferred XP implementation stack to local surfaces, proof gates, gaps, and stop rules.
- `XP Lab`: opens and exports `evidence/<run_id>_<stage>_xp_hardware_lab.md`, mapping XP hardware/receiver signals to procurement decisions, lab tests, evidence gates, and parity stop rules.
- `Roadmap`：打开并导出 `evidence/<run_id>_<stage>_xp_roadmap.md`，把 XP 公开信号、行业 SOP、本地实现、证据门和下一步研发动作合成闭环路线图。
- `Compat`：打开并导出 `evidence/<run_id>_<stage>_device_ios_matrix.md`，把本轮设备和 JSONL evidence 按 iPhone model + iOS version 聚合，显示本地兼容覆盖和未验证缺口。
- `Goals`：打开并导出 `evidence/<run_id>_<stage>_gui_goal_gate.md`，把四条用户验收目标映射到当前证据、缺口和下一步 GUI 动作。
- `Kit Gate`：打开并导出 `evidence/<run_id>_<stage>_field_kit_gate.md`，在真实 P1 开跑前检查采购/SOP 文档、设备范围、receiver、HID、iPhone 设置、Hub/线材/网络、证据计划、Route/Doctor 停线和 XP 硬件对比边界。
- `iOS SOP`：打开并导出 `evidence/<run_id>_<stage>_ios_field_sop.md`，逐项核对真实 iPhone 设置、rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy、AirPlay/网络、Hub/Cable、baseline screenshot、manual observation 和声明边界。
- `Bench`：打开并导出 `evidence/<run_id>_<stage>_hardware_bench.md`，把 receiver、HID、iPhone、Hub、Cable、XP 硬件对比和日志分流映射到测试方法。
- `Wizard`：打开并导出 `evidence/<run_id>_<stage>_field_wizard.md`，把 run_id、设备范围、物理台账、Route、Doctor、截图、HID、日志、脚本、验收和 Readiness 串成按顺序执行的现场证据步骤。
- `Runner`：打开并导出 `evidence/<run_id>_<stage>_field_runner.md`，把同一 run_id 下的 Route、Doctor、截图、click、swipe、text、Acceptance、Gap、Readiness 和声明边界变成可复制命令与现场停止线。
- `Start Pack`：打开并导出 `evidence/<run_id>_<stage>_first_run_packet.md`，把 Sources、Industry、Procure、API Cov、Script Cov、Proof Map、Roadmap、Verify、Local、Core、Routes、Rx Score、Rx Bootstrap、Rx Setup、Pitfalls、Rerun、Recovery、Compat、Goals、Kit Gate、iOS SOP、Bench、Wizard、Runner、Ctrl Ledger、P1 Trial、脚本命令、Acceptance 和 Readiness 串成首轮实机验证包。
- `Problems`：打开并导出 `evidence/<run_id>_<stage>_sop_problem_ledger.md`，把 Pitfalls、Triage、Rerun 和本轮 evidence 失败合成长期 SOP 问题台账。
- `Shot Bench`：连续采集默认 10 张截图，分析黑屏、白屏、低纹理、尺寸漂移和保存 artifact，导出 `evidence/<run_id>_<stage>_capture_bench.md`，用于 receiver/capture 稳定性首测。
- `Control Bench`：打开并导出 `evidence/<run_id>_<stage>_control_bench.md`，按点击、滑动、文本输入三条 lane 审计 API/HID 命令、人工 pass/fail、失败类别和 artifact，防止把命令成功误认为真实 iPhone 响应。

## 状态表含义

状态表会检查：

- 设备选择数量是否满足当前阶段。
- Route Decision 是否已用真实 receiver、HID、iPhone、Hub、线材、operator 信息校验通过。
- Doctor 是否存在 fail。
- 默认探针脚本是否已经 dry-run 或实跑。
- 当前 run 是否已有 JSONL evidence。
- Acceptance 里的组件台账、截图质量、人工观察和 metrics 是否满足 gate。
- Readiness 是否允许晋级。

`pending` 和 `fail` 都不能用于宣称 P1 通过。只有 route、doctor、acceptance、readiness 都为 `pass`，且操作者在 `Manual` 中记录了真实 iPhone 响应，才允许进入下一阶段讨论。

## Follow-Along Test Method

`docs/follow_along_test_method.md` is the operator-facing step-by-step test method. In the GUI, use these entries as the live version of that document:

- `Verify`: P0/P1/P2/P3/P4 command path, expected result, evidence, and stop rule.
- `Local`: PowerShell command replay for local validation.
- `Coach`: first real-iPhone P1 execution sequence.
- `Snapshot`: current industry/source/SOP state, procurement gates, route choice, and claim boundaries.
- `Procure`: supplier questions, procurement stop lines, route spend boundaries, and source/package hygiene.
- `API Cov`: XP fun/helper coverage, local test status, field gates, scaffolding boundaries, and claim limits.
- `Script Cov`: scenario coverage, dry-run status, real-run guard, lane evidence, group script boundaries, and script claim limits.
- `Proof Map`: Acceptance/Readiness proof rows, exact evidence requirements, GUI owners, next commands, and stop rules.
- `Claim Scope`: allowed claims, forbidden claims, current scope, evidence required, and handoff wording.
- `XP Timeline`: iMouse XP iteration path, pitfalls, R&D lessons, and claim boundaries.
- `XP Lab`: hardware procurement, receiver/HID lab validation, and XP parity stop rules.
- `Rx Score`, `Rx Bootstrap`, and `Rx Setup`: receiver route selection, route-decision draft, and setup split.
- `Transcript`: fillable human observation log for the physical iPhone.
- `Ctrl Ledger`: lane-separated Manual proof board for HID click, HID swipe, and Keyboard input.
- `Acceptance`, `Readiness`, `Goals`, and `Pack`: final gate and handoff.

Do not skip from a later GUI board to a claim when the follow-along document has an earlier fail/pending row.

## Stage Dashboard

`Dashboard` 弹窗会把 P0-P4 放到同一张矩阵里：

- `P0`：文档、脚本、模块等离线资产是否齐全。
- `P1`：单台 iPhone 真机控制 evidence、doctor 和 acceptance 是否过门。
- `P2`：单台稳定性是否有足够人工观察、截图和 metrics。
- `P3`：4 台试点群控是否满足设备追踪和稳定性证据。
- `P4`：10 台稳定性是否满足长时间运行证据。

导出按钮会生成 `evidence/<run_id>_<stage>_stage_dashboard.md`。这仍然只是快照，不写 JSONL evidence。

## Operator Home

`Home` opens the operator workflow map and exports `evidence/<run_id>_<stage>_operator_home.md`.

Use it as the first board in a field session:

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Rows group knowledge, route/kit/iPhone settings, local command replay, receiver screenshot proof, HID click/swipe/text proof, repeatable scripts, XP event/error parity, problem/rerun handling, and handoff gates.

Use `Run Selected` from the first `fail`, `pending`, or `warn` row, then refresh Home after the artifact or JSONL evidence is created.

Boundary:

- Home is a workflow map, not JSONL evidence.
- Exported Home Markdown does not prove real iPhone response.
- Passing Home does not replace current screenshot quality, Manual/P1 Trial observations, Acceptance, Readiness, or categorized failure triage.

## Local Verification

`Local` opens the local command verification board and exports `evidence/<run_id>_<stage>_local_verification.md`.

It is for the operator to reproduce the current local state step by step in PowerShell:

1. Run the full unit-test suite.
2. Run `compileall`.
3. Run `imouse.main --check`.
4. Run Doctor without a route decision.
5. Run Doctor again with `--route-decision evidence\<run_id>_route_decision.json` after the route is filled.
6. Run the stage scenario with `--dry-run --run-id <run_id>`.
7. Run Readiness for the current stage.

Boundary:

- Local Verification does not execute those commands from the GUI.
- It does not write JSONL evidence.
- Passing local commands only proves the prototype is locally runnable; real iOS control still needs receiver screenshots, visible click/swipe/text response, Acceptance, and Readiness.

## XP Event/Error Contract

`Events` opens the XP event/error contract board and exports `evidence/<run_id>_<stage>_xp_event_error_contract.md`.

It audits:

- XP API response envelope: `status`, `message`, `data.code`, `msgid`, and `fun`.
- HTTP/WebSocket `/api` replay boundary.
- Callback lifecycle from `/callback/list`, `/callback/poll`, `/callback/push`, `/callback/clear`, and `/event/*` aliases.
- Receiver, capture, HID, vision/OCR/script, group, and ops error taxonomy.
- Attach Log ingestion and callback bridge.
- Claim boundary for API success, callbacks, logs, markdown exports, Acceptance, and Readiness.

Boundary:

- Events is an audit board, not JSONL evidence.
- Callback rows and logs are diagnostic context until tied to screenshot quality, Manual observation, Acceptance, and Readiness.
- Passing Events does not prove XP hardware, wired projection, auto-binding, licensing, broad compatibility, or real iOS control.

## Receiver Route Gate

`Receiver` opens the receiver-route readiness gate and exports `evidence/<run_id>_<stage>_receiver_route_gate.md`.

It checks:

- whether the current Route Decision JSON is loaded and validated;
- whether receiver provider config can pass preflight;
- whether a valid Windows/wired/capture-card route downgrades missing `uxplay` from blocker to warning;
- whether window/display/SDK/capture-card binding is specific enough for screenshot capture;
- whether screenshot quality and manual/Readiness evidence are still missing before any real-control claim.

Boundary:

- Receiver Route Gate is a preflight board, not JSONL evidence.
- It does not start the receiver and does not prove real iOS control.
- Passing this gate only means the operator can move to Shot Bench, P1 Trial, Acceptance, and Readiness with a clearer route.

## Receiver Candidate Scorecard

`Rx Score` compares UxPlay, Windows receiver, wired projection, and capture-card lanes before the operator locks one receiver route. Export creates `evidence/<run_id>_<stage>_receiver_candidate_scorecard.md`.

Use it when `uxplay` is missing, when an alternate Windows receiver is available, or when the team needs a written reason for choosing a receiver lane. Start from the first `fail` or selected-route gap, then use `Run Selected` to open Route, Doctor, Receiver, Rx Bootstrap, Rx Setup, Bench, Shot Bench, or P1 Trial.

Validation expectation:

- Rx Score is a selection scorecard, not JSONL evidence.
- A `recommended` row only chooses the next receiver lane to validate.
- Passing or exporting Rx Score does not prove screenshot quality, real iPhone response, iOS perfect control, broad compatibility, or XP parity.

## Receiver Route Bootstrap

`Rx Bootstrap` creates a receiver-focused Route Decision draft and exports `evidence/<run_id>_<stage>_receiver_bootstrap.md`.

Use it after `Rx Score` when `uxplay` is missing and a Windows receiver, wired projection tool, or capture-card app is available. Fill a real receiver path, name, version, AirPlay/display name, capture method, and window binding. The generated route decision can be passed to Doctor so alternate routes do not fail only because UxPlay is missing.

Boundary:

- Rx Bootstrap is receiver preflight only.
- It keeps `allowed_to_run_p1=false` and open blockers for HID, iPhone settings, bench ledger, screenshots, manual observation, Acceptance, and Readiness.
- It does not prove screenshot quality, real iPhone response, or XP parity.

## Receiver Setup Wizard

`Rx Setup` opens the route-aware receiver install and binding wizard and exports `evidence/<run_id>_<stage>_receiver_setup_wizard.md`.

Use it after `Coach`, `Rx Score`, and any needed `Rx Bootstrap`, and before screenshot/HID tests. It reads Route Decision, Doctor, Acceptance, Readiness, and evidence summary state, then shows one setup row per lane:

- run identity and route file;
- route validation before setup;
- selected receiver lane;
- UxPlay install lane;
- Windows receiver lane;
- wired or capture-card lane;
- capture binding;
- iPhone-to-receiver binding;
- screenshot bench before HID;
- reconnect/log attachment;
- handoff and claim boundary.

Boundary:

- Receiver Setup Wizard is an operator guide, not JSONL evidence.
- It does not install software or start receiver processes.
- It does not prove screenshot quality, HID response, real iPhone control, broad iOS compatibility, or XP parity.
- If a selected lane changes after a failed route/evidence write, use a fresh run_id.

## Evidence Pack

`Pack` 会生成本轮 artifact index，方便现场复盘时检查文件是否齐全。它会列出：

- `evidence/<run_id>.jsonl`
- `evidence/<run_id>.md`
- `evidence/<run_id>_review.md`
- `evidence/<run_id>_callback_monitor.md`
- `evidence/<run_id>_callback_log.md`
- `evidence/<run_id>_<stage>_xp_event_error_contract.md`
- `evidence/<run_id>_route_decision.json`
- `evidence/<run_id>_route_decision.md`
- `evidence/<run_id>_doctor.md`
- `evidence/<run_id>_<stage>_acceptance.md`
- `evidence/<run_id>_<stage>_gap.md`
- `evidence/<run_id>_<stage>_field_runbook.md`
- `evidence/<run_id>_<stage>_receiver_route_gate.md`
- `evidence/<run_id>_<stage>_operator_home.md`
- `evidence/<run_id>_<stage>_local_verification.md`
- `evidence/<run_id>_<stage>_gui_control_center.md`
- `evidence/<run_id>_<stage>_gui_knowledge_center.md`
- `evidence/<run_id>_<stage>_industry_sop_radar.md`
- `evidence/<run_id>_<stage>_industry_current_snapshot.md`
- `docs/industry_current_state_snapshot_2026.md`
- `evidence/<run_id>_<stage>_mainstream_routes.md`
- `evidence/<run_id>_<stage>_verification_walkthrough.md`
- `evidence/<run_id>_<stage>_xp_core_functions.md`
- `evidence/<run_id>_<stage>_pitfall_library.md`
- `evidence/<run_id>_<stage>_rerun_playbook.md`
- `evidence/<run_id>_<stage>_recovery_drill.md`
- `evidence/<run_id>_<stage>_xp_public_sources.md`
- `evidence/<run_id>_<stage>_xp_source_refresh.md`
- `evidence/<run_id>_<stage>_xp_public_source_audit.md`
- `evidence/<run_id>_<stage>_xp_source_action_map.md`
- `evidence/<run_id>_<stage>_xp_iteration_radar.md`
- `evidence/<run_id>_<stage>_xp_iteration_drill.md`
- `evidence/<run_id>_<stage>_xp_architecture.md`
- `evidence/<run_id>_<stage>_xp_roadmap.md`
- `evidence/<run_id>_<stage>_device_ios_matrix.md`
- `evidence/<run_id>_<stage>_gui_goal_gate.md`
- `evidence/<run_id>_<stage>_field_kit_gate.md`
- `evidence/<run_id>_<stage>_ios_field_sop.md`
- `evidence/<run_id>_<stage>_hardware_bench.md`
- `evidence/<run_id>_<stage>_capture_bench.md`
- `evidence/<run_id>_<stage>_control_bench.md`
- `evidence/<run_id>_<stage>_field_wizard.md`
- `evidence/<run_id>_<stage>_first_run_packet.md`
- `evidence/<run_id>_<stage>_receiver_candidate_scorecard.md`
- `evidence/<run_id>_<stage>_receiver_bootstrap.md`
- `evidence/<run_id>_<stage>_receiver_setup_wizard.md`
- `evidence/<run_id>_<stage>_p1_test_coach.md`
- `evidence/<run_id>_<stage>_p1_field_transcript.md`
- `evidence/<run_id>_p1_trial.md`
- `evidence/<run_id>_<stage>_xp_gap_audit.md`
- `evidence/<run_id>_readiness.md`

文件存在不代表实机通过；它只表示本轮复盘材料已经被收集到索引里。

## Callback Monitor

The top `Callback` button opens the XP callback ledger and exports `evidence/<run_id>_callback_monitor.md`.
Use it to inspect API/ops events such as device registration, group changes, profile/calibration saves, receiver logs, HID binding, and future real receiver/HID callbacks.

Boundary:

- Callback Monitor is not JSONL evidence.
- Callback Monitor does not prove real iOS control.
- It is a debug/ops companion to Timeline, Matrix, Acceptance, and Readiness.

## Attach Log

The top `Attach Log` button imports receiver/HID text logs, classifies lines into callback events, pushes them to `/callback/push` when the local API is reachable, exports `evidence/<run_id>_callback_log.md`, and writes an `Attach Log triage` JSONL event when `Record` is enabled.

Typical mappings:

- AirPlay/receiver reconnect, warning, or stream lines -> `airplay_log`.
- screenshot/frame/decoder/black-screen lines -> `capture_log`.
- CH9329/HID/serial/mouse/keyboard lines -> `hid_log`.
- USB/iPhone/iOS/UDID lines -> `device_log`.
- generic failure lines -> `receiver_error`.

Boundary:

- The exported callback log report is debug context, not proof by itself.
- With `Record` enabled, Attach Log writes log-triage JSONL evidence with severity/category counts and sample lines.
- It helps isolate receiver, capture, HID, USB, and device problems before rerun.
- It does not prove real iOS control or replace screenshot quality and Manual/P1 Trial observations.

## Control Center

The `Center` button opens the GUI control center and exports `evidence/<run_id>_<stage>_gui_control_center.md`.

It is the operator-facing dashboard for deciding what to click next. It merges:

- stage/device scope;
- Route Decision and Doctor;
- live iPhone evidence;
- Callback and Attach Log status;
- Scenario Library or Command Queue state;
- Vision assets;
- Evidence Pack and SOP docs;
- Live Probe and SOP Board blockers;
- Acceptance/Readiness claim boundary.

Use `Run Selected` to jump into the existing GUI action for a row. The dashboard is allowed to say "next action"; it is not allowed to say "real iOS control is proven" unless JSONL evidence, Acceptance, Readiness, and manual real-iPhone observation all support that claim.

Boundary:

- Control Center is an operator dashboard, not evidence.
- `warn` on the promotion row means the team must not market or report "perfect control" yet.
- Exporting the dashboard only creates a review artifact.

## Knowledge Center

The `Knowledge` button opens the industry/SOP/XP benchmark knowledge layer and exports `evidence/<run_id>_<stage>_gui_knowledge_center.md`.

It translates research into field actions:

- XP public product model;
- mainstream no-jailbreak iOS group-control route;
- P1 receiver/HID route decision;
- field SOP and stage gates;
- hardware bench and procurement pitfalls;
- XP API/helper parity gaps;
- iteration pitfalls and failure triage;
- claim boundary.

Use `Run Selected` to jump from the selected knowledge row into the existing GUI action: XP Gap, Control Center, Route Edit, Runbook, Attach Log, Triage, or Readiness.

Boundary:

- Knowledge Center is a research/SOP dashboard, not evidence.
- A source doc can be present while the product is still blocked by missing receiver/HID/iPhone evidence.
- Exporting the dashboard only creates a review artifact.

## Industry SOP Radar

The `Industry` button opens the current-state industry/SOP radar and exports `evidence/<run_id>_<stage>_industry_sop_radar.md`.

It turns public XP signals and mainstream iOS group-control practice into execution rows:

- mainstream route boundary;
- iMouse XP product boundary;
- iPhone field settings SOP;
- receiver/capture product lane;
- HID hardware and firmware lane;
- API and SDK compatibility lane;
- vision/OCR asset lane;
- observability and recovery lane;
- scale and operations lane;
- claim and compliance boundary.

Use `Run Selected` to jump from a radar row into Routes, Core, Kit Gate, Shot Bench, Control Bench, XP Gap, Assets, Attach Log, Dashboard, or Goals.

Boundary:

- Industry Radar is a current-state/SOP map, not evidence.
- It can make the next GUI action obvious, but cannot prove real iPhone response, XP hardware parity, wired projection, auto-binding, or hardware decode.
- Exporting the radar does not write JSONL evidence.

## Verification Walkthrough

The `Verify` button opens the step-by-step verification walkthrough and exports `evidence/<run_id>_<stage>_verification_walkthrough.md`.

It turns the project validation plan into operator rows:

- P0 offline self-check: unit tests, compileall, dependency check;
- run identity and selected-device scope;
- Route Decision validation;
- preflight Doctor;
- receiver and screenshot proof;
- HID click/swipe/text proof with Manual observation;
- Acceptance and Readiness;
- P2 single-device stability;
- P3 four-device group pilot;
- XP parity review through Industry, Core, Routes, Sources, Iter Radar, XP Timeline, Roadmap, and XP Gap;
- review handoff pack.

Use `Run Selected` to jump from a verification step into Start Pack, Prepare, Route Edit, Doctor, Shot Bench, Control Bench, Readiness, Dashboard, Matrix, Core, or Pack. The footer also links Roadmap for R&D closure review.

Boundary:

- Verify is a step-by-step test guide, not evidence.
- Offline tests and GUI exports can be `ready` while P1 remains blocked.
- A later pass row cannot bypass an earlier fail row.
- Real iPhone control still requires screenshot quality, Manual observations, JSONL evidence, Acceptance, and Readiness.

## Mainstream Route Matrix

The `Routes` button opens the industry route decision matrix and exports `evidence/<run_id>_<stage>_mainstream_routes.md`.

It turns mainstream iOS group-control routes into P1 gate rows:

- XP-style black-box route: receiver + screenshot + USB HID + local kernel API;
- UxPlay AirPlay receiver;
- Windows receiver/window capture;
- wired projection or vendor SDK;
- capture-card visual lane;
- CH9329/general USB HID;
- XP dedicated hardware;
- WDA/Appium/XCUITest as non-mainline;
- MDM/Configurator/Shortcuts as auxiliary setup tooling.

Use `Run Selected` to jump from a route row into Wizard, Doctor, Route Edit, Bench, Shot Bench, Control Bench, Knowledge, or Kit Gate.

Boundary:

- Routes is a decision matrix, not evidence.
- CH9329 rows can support generic P1 exploration, but cannot close XP dedicated hardware/4.4/auto-binding parity.
- WDA/Appium and MDM/Shortcuts must not be counted as no-phone-app, cross-app, pixel-level iOS control proof.

## XP Architecture Map

The `XP Arch` button opens the XP architecture map and exports `evidence/<run_id>_<stage>_xp_architecture.md`.

It decomposes the XP-style implementation stack into:

- product boundary;
- dedicated hardware and USB/HID;
- projection and receiver;
- capture, vision, and OCR;
- Kernel/API service;
- Python helper and script runtime;
- Console/GUI operator layer;
- evidence/readiness;
- group control and ops.

Use `Run Selected` to jump from an architecture row into Goals, Control Bench, Rx Score, Assets, Events, Local, Home, Readiness, or Dashboard.

Boundary:

- XP Arch explains implementation principles and proof gates; it is not evidence.
- API/SDK readiness can be local-ready while receiver/HID/iPhone proof remains blocked.
- XP hardware, 4.4 firmware, wired projection, auto-binding, and hardware decode require side-by-side artifacts before parity wording.

## XP Hardware Lab

The `XP Lab` button opens the hardware procurement and lab validation board and exports `evidence/<run_id>_<stage>_xp_hardware_lab.md`.

It covers receiver candidates, Windows/wired/decode routes, CH9329/general HID, XP dedicated hardware parity, iPhone settings, hub/cable/power mapping, capture stability, logs/recovery, and scale procurement boundaries.

Use `Run Selected` to jump from a lab row into Route Edit, Rx Score, Bench, Control Bench, XP Arch, iOS SOP, Shot Bench, Attach Log, or Dashboard.

Boundary:

- XP Lab is a procurement and lab validation board, not JSONL evidence.
- CH9329/self-built HID proof does not prove XP dedicated hardware, 4.4 firmware, or auto-binding.
- XP hardware parity needs legal side-by-side hardware evidence and same-run artifacts.
- A ready lab row cannot override Manual observation, screenshot quality, Acceptance, Readiness, or real-device evidence.

## XP Core Function Matrix

The `Core` button opens the XP core function coverage matrix and exports `evidence/<run_id>_<stage>_xp_core_functions.md`.

It converts the XP parity backlog into GUI-ready function rows:

- product route boundary: receiver/capture + HID + kernel/API + console;
- Kernel/API and WebSocket;
- Python SDK/helper;
- device/group ledger and component traceability;
- receiver/capture and screenshot acquisition;
- USB/HID, coordinate calibration, mouse/keyboard input;
- vision/image/color and OCR/text recognition;
- script/batch runtime;
- GUI console and SOP surface;
- config/user/shortcut compatibility;
- observability/callback/logs;
- commercial/cloud ops.

Use `Run Selected` to jump from a core row into Goals, XP Gap, Matrix, Shot Bench, Control Bench, P1 Trial, Assets, Scenario Library, Start Pack, Attach Log, or Dashboard.

Boundary:

- Core is a coverage matrix, not evidence.
- API/SDK rows can be `ready` while real iPhone control is still blocked.
- HID, receiver, screenshot, calibration and input rows need JSONL evidence, artifacts, Acceptance, Readiness and manual observation before promotion.
- Config/User/Shortcut rows are local compatibility scaffolding until account, permission, licensing and real shortcut execution are designed and field-tested.

## XP Public Source Ledger

The `Sources` button opens the public-source audit ledger and exports `evidence/<run_id>_<stage>_xp_public_sources.md`.

It turns current public XP signals into verification work:

- official product model: dedicated hardware, AirPlay, no iPhone app, kernel server, console, HTTP/WebSocket API, OpenCV/OCR;
- public device/iOS support claims;
- Python XP helper domains;
- `/api` + `fun` + WebSocket protocol shape;
- API domain categories;
- XP new-version iteration claims: Windows, 4.4 firmware, wired projection, auto-binding, hardware decode, separate windows, logs, groups, subaccounts;
- project claim boundary.

Use `Run Selected` to jump from a source row into Wizard, Bench, XP Gap, or Goals.

Boundary:

- Sources is public intelligence, not evidence.
- Public compatibility claims stay `warn` until covered by our own device/iOS matrix.
- XP hardware, 4.4 firmware, wired projection, Windows receiver, hardware decode, and auto-binding stay unverified until hardware-bench evidence exists.

## XP Source Refresh Board

`Src Refresh` opens the public-source refresh SOP board and exports `evidence/<run_id>_<stage>_xp_source_refresh.md`.

It checks whether the team must refresh:

- iMouse homepage product/compatibility claims;
- XP API protocol and API domains;
- XP help/new-version iteration lessons;
- PyPI/package registry versions and namespace risk;
- Apple/iOS pointer setup guidance;
- mainstream receiver/capture/HID route assumptions;
- source-to-SOP landing actions;
- source-only claim boundaries.

Use it after `Action Map` and before route changes, package adoption, compatibility wording, roadmap prioritization, or demos.

Boundary:

- Source Refresh is a checklist, not a crawler.
- It does not write JSONL evidence.
- A fresh public source does not prove real iPhone response, iOS perfect control, broad compatibility, or XP parity.

`Src Audit` opens the repeatable public-source audit dialog. It starts in offline mode, can run a live fetch, and exports `evidence/<run_id>_<stage>_xp_public_source_audit.md`.

Repeatable audit companion:

```powershell
.\.venv\Scripts\python -m imouse.source_audit --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md --allow-failures
```

Use this command to capture URL status, PyPI versions, keyword drift, local doc stamps, SOP owner, and claim boundary before updating source-derived docs or demo wording. The audit is still source intelligence only.

## XP Public Source Action Map

The `Action Map` button opens the public-source to R&D/SOP action board and exports `evidence/<run_id>_<stage>_xp_source_action_map.md`.

It converts each public signal into:

- public signal;
- R&D decision;
- SOP gate;
- stop rule;
- current local state;
- GUI owner.

Use it immediately after `Home` and before Route/Kit changes. Start from the first `fail`, `pending`, or `warn` row, run the selected GUI owner, then refresh Action Map after evidence or artifacts are created.

Boundary:

- Action Map is source intelligence and SOP routing, not JSONL evidence.
- It does not prove real iPhone control, broad compatibility, XP hardware parity, or group-control stability.
- Package registry rows such as `imouse-py`, `imouse-xp`, and `py-imouse-xp` are SDK drift and supply-chain signals until pinned, reviewed, tested, and hardware-backed.

## Pitfall Library

The `Pitfalls` button opens the operator pitfall library and exports `evidence/<run_id>_<stage>_pitfall_library.md`.

It is a pre-rerun SOP surface. It lists common iOS group-control failure patterns:

- receiver discovery and AirPlay naming;
- black screen, stale frame, or wrong capture window;
- HID command success but no real iPhone response;
- coordinate drift, wrong orientation, or inverted swipe;
- template, color, OCR, or text recognition drift;
- group run hiding per-device failure;
- latency, reconnect, resource, or long-run instability;
- business page state changes underneath the script;
- offline/API/GUI success being treated as a control claim;
- CH9329 prototype result being mistaken for XP hardware parity.

Use `Run Selected` to jump from a pitfall row into Doctor, Shot Bench, Control Bench, P1 Trial, Assets, Matrix, Dashboard, Scenario Library, Goals, XP Gap, Triage, or Attach Log.

Boundary:

- Pitfalls is an SOP risk library, not evidence.
- If a row is `fail`, fix the smallest reproducible failure bucket and attach artifacts before rerunning.
- `XP hardware parity=warn` means generic P1 may continue, but XP dedicated hardware/4.4/auto-binding claims remain blocked.

## Rerun Playbook

The `Rerun` button opens the rerun decision playbook and exports `evidence/<run_id>_<stage>_rerun_playbook.md`.

It converts current failures into field actions:

- Issue Triage failure category;
- Route Decision, Doctor, Acceptance, and Readiness gate state;
- affected devices and failed steps;
- smallest rerun rule;
- fresh `run_id` rule;
- evidence to keep;
- stop rule;
- next GUI action.

Use it after Timeline, Matrix, Triage, and Review. Rerun the smallest failing path first, then rerun Acceptance and Readiness only after the missing evidence is recorded.

Boundary:

- Rerun Playbook is a field decision table, not evidence.
- It does not write JSONL evidence and does not prove real iOS control.
- A fresh `run_id` is required when route, wiring, receiver identity, selected devices, or iPhone settings changed.

## Recovery Drill

The `Recovery` button opens the recovery drill board and exports `evidence/<run_id>_<stage>_recovery_drill.md`.

It converts recovery risks into operator lanes:

- route/doctor recovery;
- receiver/capture recovery;
- HID control recovery;
- calibration recovery;
- vision/business-state recovery;
- group isolation recovery;
- performance watchdog recovery;
- handoff/claim recovery.

Use it after Triage and Rerun, especially before P2/P3/P4 stability runs. Each lane states the trigger, recovery step, verification step, evidence to keep, stop rule, and next GUI action. Use `Record Pass` / `Record Fail` only after the recovery step has actually been executed and its verification result is known.

Boundary:

- Recovery Drill Markdown export is an operations/SOP board, not evidence by itself.
- `Record Pass` / `Record Fail` writes recovery execution evidence with `recovery_drill=true`.
- It does not prove real iOS control.
- A recovery is closed only after the operator records the recovery action and verification result as evidence or artifact; click/swipe/text control still requires Manual/P1 Trial real-iPhone observation.

## XP Iteration Radar

The `Iter Radar` button opens the XP iteration radar and exports `evidence/<run_id>_<stage>_xp_iteration_radar.md`.

It converts XP public iteration lessons into R&D and SOP work:

- P1 black-box control: prove one iPhone can be seen, clicked, swiped, and typed before scaling.
- Kernel/API split: keep GUI, scripts, callbacks, and evidence behind the service boundary.
- Receiver/capture evolution: compare UxPlay, Windows receiver, wired projection, hardware decode, fps, reconnect, and logs.
- XP hardware and binding: separate generic CH9329 proof from XP hardware, 4.4 firmware, auto-binding, release behavior, and coordinate error.
- Vision/script productization: require replayable assets, thresholds, regions, screenshots, and failure triage.
- Ops and group scaling: defer cloud/account polish until P2/P3/P4 metrics, logs, and per-device isolation exist.
- Claim boundary: keep compatibility, perfect-control, and XP-parity language behind evidence gates.

Use `Run Selected` to jump from a radar row into Start Pack, XP Gap, Bench, Control Bench, Scenario Library, Dashboard, or Goals.

Boundary:

- Iteration Radar is R&D prioritization, not evidence.
- It does not write JSONL and does not prove XP parity.
- A `pass` row only means the current local evidence supports that radar item for this stage; it does not generalize to XP hardware, wired projection, hardware decode, broad iOS compatibility, or perfect control.

## XP Iteration Timeline

The `XP Timeline` button opens the XP iteration timeline and exports `evidence/<run_id>_<stage>_xp_iteration_timeline.md`.

It maps the inferred public XP evolution into chronological review rows:

- no-app black-box control;
- Kernel/API and Console split;
- receiver/projection productization;
- firmware, wired projection, and binding;
- vision/OCR/script assets;
- logs, recovery, and group scale;
- source refresh and claim governance.

Boundary:

- XP Timeline is product-iteration intelligence, not evidence.
- Public XP iteration signals must become local route, bench, evidence, Acceptance, and Readiness gates before claims.
- A ready row does not prove XP parity, broad compatibility, or real iPhone control.

## XP Iteration Drill Board

The `XP Drill` button opens the XP iteration drill board and exports `evidence/<run_id>_<stage>_xp_iteration_drill.md`.

It turns XP iteration details into field validation drills:

- service/API split and callback/error contract;
- iOS settings, mouse parameter profile, QR policy, orientation, and calibration context;
- receiver projection, window binding, wired route, hard decode, screenshot stability, and logs;
- XP hardware, 4.4 firmware, auto-binding, release behavior, and HID response;
- package namespace/version/hash drift before dependency adoption;
- restart, recovery, log attachment, failure category, and rerun rules;
- P3/P4 multi-device projection and per-device failure isolation;
- claim boundary before demo, handoff, compatibility, or XP parity wording.

Use `Run Selected` to jump from a drill row into Events, iOS SOP, Rx Score, Control Bench, Local, Recovery, Dashboard, or Goals.

Boundary:

- XP Drill is a validation checklist, not evidence.
- It does not browse, install packages, start receiver/HID, write JSONL, prove real iPhone response, or prove XP parity.
- Same-run JSONL, screenshot quality, manual observation, Acceptance, Readiness, logs, and exact device/iOS coverage still decide claims.

## XP Roadmap

The `Roadmap` button opens the XP R&D closure roadmap and exports `evidence/<run_id>_<stage>_xp_roadmap.md`.

It turns public XP signals, industry SOP, local implementation, and evidence gates into a staged plan:

- P0 offline/API base: keep protocol, GUI, script, callback, and evidence helpers verified without claiming real control.
- P1 route and bench lock: require Route Decision, Doctor, Hardware Bench, and component metadata before HID.
- P1 receiver/capture proof: require fresh, non-black, correctly bound screenshots before input control.
- P1 HID click/swipe/type proof: require manual real-iPhone observations and Control Bench.
- P1 calibration/input matrix: require saved calibration profile and repeatable coordinates.
- XP hardware/wired/4.4 parity lane: keep XP dedicated hardware, wired projection, auto-binding, firmware, and hard-decode proof separate.
- P2 vision/script replay: require real screenshots, templates, regions, thresholds, OCR, scenario JSON, and replay artifacts.
- P2 observability/recovery: require logs, callbacks, Timeline, Matrix, Triage, Rerun, Recovery, metrics, and smallest-path rerun.
- P3/P4 scale and ops: require per-device evidence, metrics, logs, and failure isolation before group UX.
- Claim/SOP/docs closure: sync docs only to the strongest stage proven by Acceptance and Readiness.

Use `Run Selected` to jump from a roadmap row into Verify, Kit Gate, Shot Bench, Control Bench, P1 Trial, Bench, Library, Attach Log, Dashboard, or Goals.

Boundary:

- Roadmap is an R&D closure plan, not evidence.
- It does not write JSONL and does not prove iOS control or XP parity.
- `real_ios_verified=False` keeps HID, calibration, input, and claim closure from becoming pass.

## Device/iOS Compatibility Matrix

The `Compat` button opens the local device/iOS coverage matrix and exports `evidence/<run_id>_<stage>_device_ios_matrix.md`.

It groups local evidence by:

- iPhone model;
- iOS version;
- selected devices;
- events and failures;
- pass/pending/fail device coverage;
- local claim, such as `covered_for_p1` or `not_covered`;
- remaining gaps.

Boundary:

- Compat is local coverage, not a public compatibility claim.
- `covered_for_p1` only applies to the exact model/iOS row with local evidence.
- Unknown model/iOS rows remain blocked until component metadata records the real iPhone model and iOS version.
- A clean row for one iPhone/iOS version does not prove all models, latest iOS, XP hardware, wired projection, Windows receiver, or hardware decode support.

## Goal Gate

The `Goals` button opens the acceptance-goal gate and exports `evidence/<run_id>_<stage>_gui_goal_gate.md`.

It maps the four project goals to GUI evidence:

- iOS perfect control: real screenshot quality, click, swipe, text input, manual observation, Acceptance PASS, Readiness PASS, Proof Map closure, and Claim Scope pass wording.
- iOS group-control SOP: SOP docs, field runbook, worksheet, issue triage, rerun playbook, recovery drill, device matrix, acceptance gap, Claim Scope, and replayable failure notes.
- iMouse XP core functions and docs: XP API/helper parity, receiver/capture, HID, vision, scripts, GUI docs, and evidence pack coverage.
- XP iteration lessons and pitfalls: public-source refresh, route selection, receiver/HID benchmark, and pitfall-driven backlog.

Use `Run Selected` to jump from a goal row into the next GUI action: Proof Map, Claim Scope, P1 Trial, Runbook, XP Gap, Knowledge, or Triage.

Boundary:

- Goal Gate is an acceptance map, not evidence.
- A row is not complete until its required proof exists; especially the iOS control row still depends on real-device evidence, Proof Map closure, Claim Scope pass wording, Acceptance, Readiness, and no unexplained fail events.

## Field Kit Gate

The `Kit Gate` button opens the pre-run procurement and field-readiness gate and exports `evidence/<run_id>_<stage>_field_kit_gate.md`.

It answers one operational question: can the team open the P1 real-device run today?

Rows cover:

- procurement and SOP source docs;
- run identity and selected device scope;
- receiver procurement and capture route;
- HID procurement, firmware, serial binding, and GUI scan status;
- iPhone model/iOS/orientation/AssistiveTouch/pointer settings;
- Hub, cable, network, and operator ledger;
- evidence plan and artifact ledger;
- Open P1 stop line from Route Decision and Doctor;
- XP hardware comparison question.

Use `Run Selected` to jump from a gate row into Knowledge, Route Edit, Record Metadata, Doctor, Scan Hardware, P1 Trial, Pack, Start Pack, or XP Gap.

Boundary:

- Kit Gate is a pre-run gate, not evidence.
- `Open P1 stop line` must be `pass` before real HID actions.
- `XP hardware comparison question=warn` means generic P1 may continue on CH9329, but XP dedicated hardware/4.4/auto-binding parity is still unproven.

## iOS Field Settings SOP

The `iOS SOP` button opens the real-iPhone settings checklist and exports `evidence/<run_id>_<stage>_ios_field_sop.md`.

Rows cover:

- device identity, iPhone model, iOS version, orientation, and selected device id;
- AssistiveTouch and pointer profile;
- Full Keyboard Access and Trackpad & Mouse settings;
- Auto-Lock, brightness, focus/notification policy, and screen state;
- network, AirPlay identity, receiver path/version/window binding;
- Hub, cable, power, HID firmware/serial, and operator ledger;
- baseline screenshot and manual click/swipe/type observation;
- settings replay and operator handoff;
- claim boundary.

Use `Run Selected` to jump from a settings row into Route Edit, Shot Bench, P1 Trial, Control Bench, Bench, Start Pack, or Goals.

Boundary:

- iOS SOP is a field settings checklist, not evidence.
- Settings rows can open the next test, but they do not prove real iOS control.
- `real_ios_verified=False` keeps baseline/control and claim rows from becoming pass.

## Hardware Bench

The `Bench` button opens the hardware bench checklist and exports `evidence/<run_id>_<stage>_hardware_bench.md`.

It turns the hardware/SOP docs into runnable GUI checks:

- bench ledger and physical labels;
- receiver/capture route;
- HID binding and real iPhone response;
- iPhone settings;
- Hub/cable/network isolation;
- screenshot and control evidence;
- XP dedicated hardware comparison;
- callback/log triage.

Use `Run Selected` to jump from a bench row into Route Edit, Record Metadata, Scan Hardware, P1 Trial, Runbook, XP Gap, Attach Log, or Triage.

Boundary:

- Hardware Bench is a field checklist, not evidence.
- A clean bench ledger does not prove iPhone control; real screenshot quality and manual observations must still be recorded.
- XP dedicated hardware remains pending until legally acquired and compared against CH9329 on the same iPhone/page.

## Capture Quality Bench

The `Shot Bench` button runs a repeated screenshot quality probe for the selected device and exports `evidence/<run_id>_<stage>_capture_bench.md`.

It records one JSONL evidence event for the bench result and writes frame artifacts under `evidence/<run_id>_artifacts/`. The table checks:

- missing or invalid base64;
- invalid image bytes;
- too-small frames;
- black, white, or blank/low-texture frames;
- screenshot dimension drift across samples;
- artifact save errors.

Boundary:

- Shot Bench proves repeated screenshot quality only.
- The default GUI run is a quick 10-sample smoke bench; XP-level receiver/capture confidence still needs a 100-screenshot stability run before expanding to more devices.
- Passing Shot Bench does not prove HID click, swipe, text input, business-flow success, or full iOS control.

## Control Response Bench

The `Control Bench` button opens the click/swipe/text response audit and exports `evidence/<run_id>_<stage>_control_bench.md`.

It reads the current JSONL evidence and separates:

- API/HID command events that reached the software layer;
- Manual pass observations after the operator saw the real iPhone respond;
- Manual fail observations with failure category and artifact context;
- command failures such as HID/keyboard errors that happened before a real response could be observed.

Status meaning:

- `pass`: the lane has enough Manual pass observations for the selected stage.
- `ready`: at least one API/HID command event exists, but no Manual pass has confirmed real iPhone response yet.
- `fail`: a Manual fail or command fail exists and must be triaged before rerun.
- `pending`: no usable event exists for that lane.

Boundary:

- Control Bench is an audit and review artifact, not evidence by itself.
- API/HID command success is not enough; click, swipe, and text input each need Manual pass evidence on a real iPhone.
- Any fail row must keep category and screenshot/log artifact context before the operator reruns the lane.

## Field Evidence Wizard

The `Wizard` button opens the ordered field evidence sequence and exports `evidence/<run_id>_<stage>_field_wizard.md`.

It gives the operator a strict run order:

- run identity and selected device scope;
- physical ledger;
- route gate;
- preflight doctor;
- receiver screenshot;
- coordinate calibration;
- HID click, swipe, and text;
- receiver and HID logs;
- repeatable action path;
- vision assets;
- stage acceptance;
- readiness and handoff.

Use `Run Selected` to jump from a wizard row into Record Metadata, Route Edit, Doctor, Screenshot, P1 Trial, Runbook, Attach Log, Triage, Load Probe Script, Run Queue, Acceptance, Gap, Assets, Readiness, or Pack.

Boundary:

- Field Evidence Wizard is an execution sequence, not evidence.
- `real_ios_verified=False` remains a `warn` even when route, doctor, screenshot, manual observation, and acceptance rows look good.
- Any fail/pending/unexplained warn row means the field run should stop until the smallest useful evidence is attached and reviewed.

## Field Evidence Runner

The `Runner` button opens the same-run field evidence runner and exports `evidence/<run_id>_<stage>_field_runner.md`.

It tracks:

- run scope and selected device count;
- Route Decision validation command;
- route-aware Doctor command;
- screenshot quality and Shot Bench artifact status;
- separate Manual observations for HID click, HID swipe, and keyboard input;
- Acceptance, Gap, and Readiness commands;
- Evidence Pack handoff;
- the final claim boundary.

Use `Run Selected` to jump into the GUI action for a row, or `Copy Command` to copy the exact PowerShell command shown in the row.

Boundary:

- Runner is an execution and evidence checklist, not evidence by itself.
- One generic Manual pass is not enough for P1 field confidence; click, swipe, and text each need their own visible real-iPhone observation before the final claim row can be clean.
- Do not claim iOS perfect control, broad compatibility, or XP parity unless Runner, Acceptance, Readiness, JSONL evidence, screenshots, and exact device/iOS scope all agree.

## Control Evidence Ledger

The `Ctrl Ledger` button opens the lane-separated control evidence ledger and exports `evidence/<run_id>_<stage>_control_ledger.md`.

Use it after `Runner` or `P1 Trial` when the blocker is HID click, HID swipe, or Keyboard input. It reads JSONL evidence, shows the three control lanes separately, and keeps broad Manual notes in `Generic Manual quarantine` until they are rewritten as action-specific observations.

Boundary:

- `Ctrl Ledger` does not prove real iOS control by itself.
- `Record Pass` should only be used after the operator watches the physical iPhone respond for that one lane.
- A single Manual note cannot close click, swipe, and text together.

## First Run Packet

The `Start Pack` button opens the first real-device run packet and exports `evidence/<run_id>_<stage>_first_run_packet.md`.

It is the most direct operator entry for a new bench run. It pulls together:

- Industry Current Snapshot, Procure, Sources, Industry, Roadmap, Verify, Local, Core, Routes, Rx Score, Rx Bootstrap, Rx Setup, Goals, and Pitfalls, so current public-source state, procurement stop lines, current-state SOP, public XP claims, R&D closure lanes, step-by-step test method, local command replay, core functions, route decisions, receiver lane selection, alternate receiver bootstrap, setup split, and known field risks become test work;
- Compat, so the exact iPhone model and iOS version are not generalized;
- Kit Gate, iOS SOP, Bench, Wizard, Runner, and Ctrl Ledger, so receiver/HID/iPhone settings/cable/Hub blockers, copy-ready commands, and lane-separated click/swipe/text evidence gates stay visible before and during the run;
- P1 Trial or Runbook, so screenshot, click, swipe, and text input have a manual-observation path;
- Scenario or GUI queue state, so dry-run and real-run commands can be reproduced;
- Local command verification;
- Pack, Acceptance, Gap, Readiness, Dashboard, and Session handoff.

Boundary:

- First Run Packet is an operator guide, not JSONL evidence.
- Rx Bootstrap rows only create a receiver route draft and do not allow P1 by themselves.
- It includes exact PowerShell commands, but those commands are reproduction steps, not proof.
- Any fail, pending, or unexplained warn row should stop the run before real HID actions or promotion claims.

## P1 Trial

The `P1 Trial` button opens the first real-iPhone control board and exports `evidence/<run_id>_p1_trial.md`.

It focuses on the minimum single-device acceptance path:

- bench ledger for one selected iPhone;
- Route Decision;
- Doctor;
- receiver/capture screenshot quality;
- coordinate calibration;
- HID click;
- HID swipe;
- keyboard input;
- callback/log triage;
- Acceptance;
- Readiness.

Use `Run Selected` to launch the highlighted GUI action. Use `Record Pass` or `Record Fail` only after the operator has observed the real iPhone; those buttons write Manual evidence for the selected trial row.

Boundary:

- P1 Trial is an execution board, not a pass certificate.
- A Manual pass means the operator observed the real iPhone behavior for that row.
- It still depends on Acceptance, Readiness, screenshot quality, component metadata, and clean JSONL evidence before promotion.

## Field Runbook

`Runbook` 会生成本阶段的现场执行向导，适合交给操作者按顺序开测。它覆盖：

- 设备范围和阶段所需数量。
- receiver/capture/HID/iPhone 路线台账。
- preflight doctor。
- 投屏/截图质量。
- HID 点击/滑动/输入和人工真机观察。
- 模板、找色、OCR 资产。
- 阶段脚本或 Command Queue dry-run。
- Real-run Guard。
- metrics/stability。
- Timeline/Matrix/Triage/Review。
- Acceptance 与 Readiness 晋级门。

`Runbook` 不写 JSONL evidence，也不证明 iPhone 已经响应；它的价值是把 fail/pending stop rule 集中给现场人员，不让大家跳过阻断项。

## XP Gap

`XP Gap` 把 XP 对标能力拆成 `Kernel/API`、`Receiver/Capture`、`USB/HID`、`Vision/Image/Color`、`Script Runtime`、`GUI Console` 等域。它适合研发负责人每轮复盘时判断：

- 哪些域已有离线原型。
- 哪些域只是 `partial`，还没达到 XP 产品体验。
- 哪些域因为缺 field evidence 而 `blocked`。
- 下一轮应该优先补 receiver、HID、截图、校准、脚本还是可观测性。

这张报告不写 evidence，不替代 Acceptance/Readiness。

## P1 Test Coach

`Coach` opens the P1 real-device test coach and exports `evidence/<run_id>_<stage>_p1_test_coach.md`.

Use it after `Home` and `Action Map`. It shows one row per field step: current status, operator action, GUI owner, optional command, pass criteria, failure handling, evidence to keep, and stop rule.

Boundary:

- Coach does not execute commands.
- Coach does not write JSONL evidence.
- Coach does not prove real iPhone control.

## P1 Field Transcript

`Transcript` opens and exports `evidence/<run_id>_<stage>_p1_field_transcript.md`.

Use it after `Coach`, `Rx Score`, any needed `Rx Bootstrap`, and `Rx Setup`. It creates a fillable field log with:

- one transcript header tied to run_id, stage, evidence path, event counts, and fail counts;
- one receiver setup split row;
- one row per Coach checkpoint;
- one operator sign-off row;
- observation prompts for screenshots, calibration, click, swipe, text, logs, Acceptance, and Readiness;
- failure category suggestions;
- artifact/log path prompts;
- smallest rerun rules and stop rules.

Boundary:

- Transcript is not JSONL evidence.
- Transcript does not record Manual pass by itself.
- Transcript does not prove real iPhone control, iOS perfect control, broad compatibility, or XP parity.
- The operator must use `P1 Trial` or Manual recording to write real observations into JSONL.
- `Prefill Manual` only copies row context into the bottom Manual controls; non-control rows are prefilled as `info`, not `pass`.
- API/HID command success is not a pass unless the operator sees the real iPhone respond and records Manual evidence for the same run.

## P1 推荐流程

1. 顶部 `Evidence` 输入本轮 `run_id`，保持 `Record` 勾选。
2. 点击 `Start Local`，再点击 `Ping`。
3. 在设备表注册并选中 `dev_1`。
4. 点击 `Prepare`。
5. 点击 `Edit`，用 `Use Metadata` 带入底部 Metadata，再补齐真实 receiver path、start command、AirPlay name、HID firmware、iPhone model、Hub、Cable、Operator。
6. 点击 `Checklist` 生成路线补齐清单。
7. 点击 `Validate`。如果失败并写入 evidence，这个 run_id 视为 blocked，修复后换新 run_id。
8. 点击 `Doctor`。有 fail 时先修环境或硬件。
9. 点击 `Dry Run`。dry-run 只证明脚本结构可执行，不证明 iPhone 响应。
10. 接入真实 iPhone、receiver 和 HID 后，按 GUI 的 AirPlay/Capture/Screenshot/Click/Swipe/Type 顺序实测。
11. 点击 `Shot Bench`，确认 receiver/capture 连续截图质量没有黑屏、低纹理或尺寸漂移。
12. 每次观察到 iPhone 真实响应后，在 `Manual` 行记录 pass/fail，并给 fail 选择分类和附件路径。
13. 点击 `Control Bench`，确认点击、滑动、文本输入不是只停留在 API/HID command ready，而是有 Manual pass 或明确 fail 分类。
14. 如果 receiver、capture、HID 或 USB 有日志，点击 `Attach Log` 导入，随后用 `Callback` 查看事件归类。
15. 点击 `Refresh` 查看缺口。
16. 点击 `Center`，按第一条 fail/pending 行回到对应 GUI 动作补证据。
17. 点击 `Knowledge`，确认公开资料、主流路线、SOP、硬件坑点和 claim boundary 没有被现场执行遗漏。
18. 点击 `Industry`，确认行业主流路线、XP 产品壁垒、iPhone 设置、receiver/HID/视觉/运维/扩容和声明边界都能映射到下一步 GUI 动作。
19. 点击 `Verify`，确认 P0/P1/P2/P3/P4 测试命令、预期结果、证据和停止线都能按顺序复述，不用后面的通过项覆盖前面的 fail。
20. 点击 `Core`，确认 API/SDK、receiver、截图、HID、校准、视觉、脚本、GUI 和运维域没有把本地 ready 误判为真机通过。
21. 点击 `Routes`，确认当前 receiver/HID 选择符合 XP 式黑盒控制主线；WDA/Appium、MDM/Shortcuts 只能显示为非主线或辅助路线，不能当成控制证据。
22. 点击 `Pitfalls`，确认 receiver、HID、校准、视觉、群控、性能、业务状态、claim boundary 和 XP 硬件对标常见坑都有 SOP 探针和停止线。
23. 点击 `Sources`，确认官网兼容性、XP 硬件/4.4/Windows/wired/硬解等公开说法仍然按本地证据显示 warn/fail/pending。
24. 点击 `Iter Radar`，确认 XP 迭代线索被转成研发优先级、SOP 测试路径和停止线，而不是产品宣传。
24a. 点击 `XP Timeline`，确认 XP 公开演进信号被转成阶段化踩坑、研发动作、SOP 闸门和停止线，而不是实机通过证据。
25. 点击 `Roadmap`，确认 P0/P1/P2/P3/P4 和 XP hardware/wired/4.4 parity lane 都有证据门、下一步和停止线；离线或 `real_ios_verified=False` 时不能显示为实机通过。
26. 点击 `Compat`，确认当前 iPhone model/iOS version 只显示本地覆盖，不把单机证据外推到未测机型或系统。
27. 点击 `Goals`，确认四条用户验收目标中没有把文档、GUI 或离线测试误判为真实 iOS 控制。
28. 点击 `Kit Gate`，确认采购/SOP 文档、Route、Doctor、HID 扫描、证据计划和 Open P1 stop line 没有 fail/pending。
29. 点击 `iOS SOP`，确认 AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、Auto-Lock、brightness、network、AirPlay、Hub/Cable 和 baseline artifact 都有状态和停止线。
30. 点击 `Bench`，确认 receiver、HID、iPhone、Hub、Cable 和日志分流没有缺台账或未验证项。
31. 点击 `Wizard`，按第一条 fail/pending/warn 步骤回到对应 GUI 动作，确认每一步都有明确证据和停止线。
31a. 点击 `Runner`，复制或核对当前行命令，确认 click、swipe、text 三条 Manual lane 没有被一个笼统 manual pass 合并。
32. 点击 `Rerun`，确认失败类别、gate 状态、fresh run_id 规则、证据保留项和停止线已经转成下一轮最小复测动作。
33. 点击 `Recovery`，确认 receiver/HID/校准/视觉/群控/性能恢复 lane 都有恢复步骤、验证步骤、证据保留项和停止线；恢复动作完成后可对选中 lane 点 `Record Pass` / `Record Fail` 写恢复执行证据。
34. 点击 `Acceptance` 和 `Gap`，按缺口补截图质量、组件台账、人工观察或 metrics。
35. 点击 `Readiness`。P1 FAIL 时继续补证据；P1 PASS 后再进入 P2。
36. 点击 `Start Pack`，导出首轮实机验证包，让现场人员按同一份 run_id、Route、Doctor 和停止线执行。
37. 再点一次 `Center`，确认 Promotion claim boundary 没有把 `real_ios_verified=False` 当成通过。
38. 点击 `Report` 导出本轮 GUI 状态快照。
39. 点击 `Dashboard` 查看 P0-P4 阶段矩阵，确认当前阶段没有 pending/fail。
40. 点击 `Pack` 导出证据包索引，交给复盘人员按 required missing 项补文件。
41. 点击 `XP Gap` 导出 XP 核心能力差距审计，确认 P1 阻断项没有被“GUI 已完成”掩盖。

## 不可混淆的边界

- `Report` 只是快照，不写 evidence。
- `Dashboard` 和 `Pack` 只是快照/索引，不写 evidence。
- `Rerun` 只是最小复测决策表，不写 evidence；它提示换 run_id、保留附件和停止线，但不能替代实机观察。
- `Recovery` 导出只是恢复演练表；`Record Pass` / `Record Fail` 会写恢复执行 evidence，但不能替代恢复后的截图质量、Manual/P1 Trial 真实控制观察、Acceptance 和 Readiness。
- `Problems` 是问题沉淀台账，不写 JSONL evidence；关闭问题仍要回到最小重跑、Manual/P1 Trial、Acceptance 和 Readiness。
- `XP Gap` 是研发差距图，不写 evidence，也不证明 XP 对标完成。
- `Dry Run` 只验证脚本结构，不验证 AirPlay、HID、截图或 iPhone 响应。
- `Route Validate` 只证明组件台账完整，不替代截图质量和人工观察。
- `Acceptance PASS` 仍需配合 `Readiness PASS` 和现场人工观察，不能单独宣称“完美控制”。
- 当前 Windows receiver、XP 专用硬件和 4.4 固件仍未完成实机验证。
