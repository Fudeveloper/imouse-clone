# Python GUI 原型说明

更新时间：2026-06-09

当前 GUI 是 iMouse XP 对标项目的第一版 Python 桌面控制台，用于把 SOP 里的单设备测试步骤落到可点击界面。它不是最终 XP 多窗口投屏控制台，也不代表实时投屏、硬解、多设备窗口分离已经完成。

## 启动方式

推荐先启动 GUI，再用 GUI 里的 `Start Local` 按钮启动本地内核服务：

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

也可以先手动启动服务：

```powershell
.\.venv\Scripts\python -m uvicorn imouse.server:app --host 127.0.0.1 --port 9911
.\.venv\Scripts\python -m imouse.gui
```

## 当前能力

GUI 当前通过 `imouse.xp_client.XpApiClient` 调用 XP 风格 `/api` + `fun` 兼容入口。

已提供界面能力：

- 设置服务地址。
- 启动/停止本地内核服务。
- Ping/刷新设备列表。
- 注册设备。
- 移除设备。
- 扫描硬件串口。
- 绑定/解绑硬件。
- 启动/停止 AirPlay。
- 启动截图采集。
- 请求截图。
- 显示截图预览。
- 点击截图预览自动填入原图坐标到 `Click X/Y`。
- 保存最近一次截图到 `screenshots/`。
- 在截图预览上拖拽选区，保存模板到 `templates/`；过小或低纹理模板会被拒绝，避免 OpenCV 误判。
- 用保存的模板调用找图接口，命中后自动填入 `Click X/Y`。
- 点击截图预览时取 RGB 颜色，并调用找色接口。
- 调用 OCR 和查找文字接口。
- 点击坐标。
- 滑动。
- 输入文本。
- 设备表支持多选；多选时点击、滑动、输入会自动走批量接口。
- 设备分组：刷新分组、保存当前多选设备为分组、加载分组到设备表选择、删除分组。
- 坐标校准：从当前截图填充 active/target 坐标空间，保存/加载每台设备校准。
- 组件元数据档案：底部 `Metadata` 行可记录 receiver provider、capture method、HID provider、HID/串口、iPhone 和 iOS 版本；点击 `Record Metadata` 会先保存到 `state/device_profiles.json`，再写入当前 evidence，供 P1/P2/P3/P4 acceptance gate 做组件追踪。
- 测试证据记录：顶部 `Evidence` 输入本轮 `run_id`，勾选 `Record` 后自动写入 `evidence/<run_id>.jsonl`，`Screenshot` 会记录 `screenshot_quality`，黑屏、白屏、无效图或过小图会记为 fail，`Summary` 可生成 Markdown 汇总，`Timeline` 可查看和导出本轮事件流水，`Matrix` 可按设备查看证据覆盖，`Triage` 可按失败类别聚合问题和下一步动作，`Rerun` 可把失败类别、Route/Doctor/Acceptance/Readiness gate 转成最小重跑决策，`Recovery` 可把 receiver/HID/校准/视觉/群控/性能恢复动作转成演练表，`Review` 可生成带失败分类、metrics 和建议的复盘报告。
- 环境自检：顶部 `Doctor` 会运行 preflight doctor，检查 Python、依赖、receiver provider、投屏组件、串口、状态文件和当前 API 服务，并输出 `evidence/<run_id>_doctor.md`；如果当前已选择 route decision，GUI 会把它传给 doctor，用于预检 Windows Receiver/有线投屏/采集卡等替代路线。
- 阶段审计：顶部 `Readiness` 会汇总文档、脚本、doctor 和当前 evidence 的 acceptance gate，输出 `evidence/<run_id>_readiness.md`，用于判断是否真的达到 P1。
- 场景执行：底部 `Scenario` 可选择 JSON 场景，`Library` 会列出 `scripts/` 下的阶段脚本、动作数、设备/分组和 dry-run 建议，支持 `Dry Run` 和实跑；实跑前会经过 Real-run Guard，只有 Route Decision ready、Doctor 无 fail、设备数量满足阶段要求时才允许执行。替代 receiver 路线下的 route-aware Doctor warn 可以继续进入实跑尝试，但仍不证明截图质量或 iPhone 响应。运行结果写入同一轮 evidence，并生成 Markdown 场景汇总。
- SOP 工具：底部 `SOP` 行可按本轮 `run_id` 生成/浏览/编辑 `Route Decision`，导出路线补齐 `Checklist`，校验路线，生成 `Field Packet`，生成操作员 `Worksheet`，运行 P1/P2/P3/P4 `Acceptance` 报告，并用 `Gap` 导出补证据清单。
- Live Probe、Control Center、Knowledge Center、Verification Walkthrough、XP Core Function Matrix、Mainstream Route Matrix、Pitfall Library、XP Public Source Ledger、XP Iteration Radar、XP Iteration Timeline、Device/iOS Compatibility Matrix、Goal Gate、Field Kit Gate、Hardware Bench、Capture Quality Bench、Control Response Bench、Control Evidence Ledger、Field Evidence Wizard、P1 Trial、SOP Board 与阶段驾驶舱：底部 `Live Probe` 面板可 `Prepare`、加载默认探针脚本、dry-run、刷新状态、导出 live probe 报告；`Center` 会打开 GUI 总控层，把设备范围、Route/Doctor、真实 iPhone 证据、Callback/Attach Log、Scenario/Queue、Vision assets、Evidence Pack、SOP Board 和 Promotion boundary 汇总成可点击的下一步动作；`Knowledge` 会打开行业/SOP/XP 对标知识层，把 XP 公开产品模型、主流路线、P1 路线决策、现场 SOP、硬件测试台、API/helper 差距、迭代坑点和 claim boundary 映射到 GUI 下一步动作；`Verify` 会打开逐步验证工作台，把 P0/P1/P2/P3/P4 的测试命令、预期、证据和停止线按顺序映射到 GUI 动作；`Core` 会打开 XP 核心功能覆盖矩阵，把 API/SDK、receiver、截图、HID、校准、视觉、脚本、GUI、可观测性和商业运维拆成本地实现、证据门和 XP Gap 状态；`Routes` 会打开主流路线矩阵，把 XP 式黑盒控制主线、receiver/HID 候选、非主线自动化框架和辅助运维工具映射到 P1 证据门、停止线和 GUI 动作；`Pitfalls` 会打开群控坑点/SOP 风险库，把 receiver、HID、校准、视觉、群控、性能、业务状态、claim boundary 和 XP 硬件对标常见坑映射到探针、停止线和 GUI 动作；`Rerun` 会打开最小重跑决策表，把 Issue Triage 和各阶段 gate 转成是否换 run_id、保留什么证据、何时停止的操作行；`Recovery` 会打开恢复演练表，把 receiver/capture、HID、校准、视觉/业务状态、群控隔离、性能 watchdog 和 handoff claim boundary 转成恢复、验证、证据和停止线；`Sources` 会打开公开来源审计台账，把官网、Python XP、XP API、XP 帮助页的公开说法映射到可信层级、研发影响、验证缺口和下一步 GUI 动作；`Iter Radar` 会打开 XP 迭代雷达，把公开迭代线索转成研发优先级、SOP 测试路径和停止线；`XP Timeline` 会打开 XP 迭代时间线，把公开演进信号按阶段转成踩坑点、研发借鉴、SOP 闸门、证据要求和停止线；`Compat` 会打开本地机型/iOS 覆盖矩阵，把当前设备和 JSONL evidence 按 iPhone model + iOS version 聚合，防止把单机证据外推成广泛兼容；`Goals` 会打开四条用户验收目标看板，把 iOS 完美控制、SOP/问题沉淀、XP 核心功能/文档和 XP 迭代踩坑映射到当前证据、缺口、测试方法和下一步 GUI 动作；`Kit Gate` 会打开采购/现场准备闸门，判断今天能否打开 P1 实跑；`Bench` 会打开硬件测试台，把 receiver、HID、iPhone、Hub、Cable、XP 硬件对比和日志分流映射到台账、证据、测试方法和下一步 GUI 动作；`Rx Bootstrap` 会为替代 receiver 生成 route decision 草案和 bootstrap 报告，让 Doctor 能按 Windows/wired/capture-card 路线预检；`Wizard` 会打开现场证据向导，把 run_id、设备范围、物理台账、Route、Doctor、截图、校准、HID、日志、脚本、验收和 Readiness 串成必须按顺序执行的步骤；`P1 Trial` 会打开单台真实 iPhone 首测执行板，串联台账、Route、Doctor、截图、校准、点击、滑动、输入、日志、Acceptance 和 Readiness，并支持选中行后记录 Manual pass/fail；`Runbook` 会打开并导出本阶段现场执行向导，串联设备范围、Route、Doctor、截图、HID、视觉、场景、Guard、metrics、Triage 和晋级门；`SOP` 会打开当前阶段的八步执行工作台，选中一行后可点 `Run Selected` 执行该行主命令，`SOP MD` 会导出 `evidence/<run_id>_<stage>_gui_sop_board.md`；`Dashboard` 会打开 P0/P1/P2/P3/P4 阶段矩阵，`Pack` 会导出本轮 GUI evidence pack 索引，`XP Gap` 会导出 XP 核心能力差距审计。
- `Kit Gate` 会打开并导出 `evidence/<run_id>_<stage>_field_kit_gate.md`，把采购/SOP 文档、设备范围、receiver、HID、iPhone 设置、Hub/线材/网络、证据计划、Route/Doctor 停线和 XP 硬件对比边界集中到 P1 开跑前的闸门；它不写 JSONL evidence。
- `Core` 会打开并导出 `evidence/<run_id>_<stage>_xp_core_functions.md`，把 XP 核心功能域映射到本地实现、当前证据门、XP Gap 状态、下一步 GUI 动作和“不等于实机通过”的边界；它不写 JSONL evidence，也不证明 XP 对标完成。
- `Script Cov` opens and exports `evidence/<run_id>_<stage>_script_coverage.md`, mapping stage scenario files, dry-run, real-run guard, metadata records, screenshot probes, HID lanes, vision/OCR, metrics, group scripts, failure replay, and claim boundaries. It does not run scripts, write JSONL evidence, prove real iPhone control, or prove XP script parity.
- `Proof Map` opens and exports `evidence/<run_id>_<stage>_proof_map.md`, mapping every Acceptance/Readiness gate to its required JSONL evidence, GUI action, artifact, next command, and stop rule. It does not write evidence or prove real iPhone control.
- `Claim Scope` opens and exports `evidence/<run_id>_<stage>_claim_scope.md`, converting Readiness, Acceptance, Proof Map, Evidence Pack, API/Core coverage, compatibility, and XP gap signals into allowed and forbidden handoff wording. It does not write JSONL evidence, prove real iPhone control, prove group control, prove XP hardware parity, or prove broad iPhone/iOS compatibility.
- `XP Arch` opens and exports `evidence/<run_id>_<stage>_xp_architecture.md`, mapping the inferred XP implementation stack to local surfaces, proof gates, gaps, and stop rules. It explains implementation principles; it does not write JSONL evidence or prove XP parity.
- `Verify` 会打开并导出 `evidence/<run_id>_<stage>_verification_walkthrough.md`，把离线自检、设备范围、Route、Doctor、截图、HID、Acceptance/Readiness、P2/P3/P4 扩容和 XP parity review 写成逐步测试方法；它不写 JSONL evidence。
- `Industry` 会打开并导出 `evidence/<run_id>_<stage>_industry_sop_radar.md`，把行业主流路线、XP 产品壁垒、iPhone 现场设置、receiver/HID/视觉/运维/扩容和声明边界映射到 GUI 下一步动作；它不写 JSONL evidence。
- `Procure` opens and exports `evidence/<run_id>_<stage>_route_procurement_sop.md`, turning route knowledge into supplier questions, buying stop lines, lab SOP, source/package hygiene, and evidence gates. It does not buy hardware, install packages, write JSONL evidence, prove real iPhone control, or prove XP parity.
- `Start Pack` 会打开并导出 `evidence/<run_id>_<stage>_first_run_packet.md`，把 Sources、Industry、Procure、API Cov、Script Cov、Proof Map、Claim Scope、Roadmap、Verify、Local、Core、Routes、Rx Score、Rx Bootstrap、Rx Setup、Pitfalls、Rerun、Recovery、Compat、Goals、Kit Gate、iOS SOP、Bench、Wizard、Runner、Ctrl Ledger、P1 Trial、脚本命令、Acceptance、Gap、Readiness 和 handoff 边界串成首轮实机验证包；它是操作员向导，不写 JSONL evidence，也不证明真实 iOS 控制。
- `Action Map` opens and exports `evidence/<run_id>_<stage>_xp_source_action_map.md`, converting public XP/package/Apple signals into R&D decisions, SOP gates, stop rules, and GUI owners. It does not write JSONL evidence and does not prove real iPhone control.
- `Src Refresh` opens and exports `evidence/<run_id>_<stage>_xp_source_refresh.md`, turning homepage/API/help/package/Apple/industry source refresh duties into GUI owners and SOP landing actions. It does not browse automatically, write JSONL evidence, or prove real iPhone control.
- `Src Audit` opens and exports `evidence/<run_id>_<stage>_xp_public_source_audit.md`, recording URL status, PyPI versions, keyword drift, local doc stamps, SOP owner, and claim boundary for the same source-refresh loop. It starts offline and can run live fetch from the GUI. It is source intelligence only and does not prove real iPhone control.
- `python -m imouse.source_audit --markdown evidence/<run_id>_<stage>_xp_public_source_audit.md --allow-failures` is the command-line companion for the same audit when GUI is not available.
- `docs/follow_along_test_method.md` is the step-by-step operator test method. The GUI entry points that mirror it are `Snapshot`, `Procure`, `Verify`, `Local`, `Coach`, `Rx Score`, `Rx Bootstrap`, `Rx Setup`, `Transcript`, `Acceptance`, `Readiness`, `Goals`, and `Pack`.
- `Coach` opens and exports `evidence/<run_id>_<stage>_p1_test_coach.md`, giving the operator a step-by-step P1 real-device test path with current status, GUI owner, optional command, pass criteria, failure handling, evidence to keep, and stop rule. It does not execute commands and does not prove real iPhone control.
- `Iter Radar` 会打开并导出 `evidence/<run_id>_<stage>_xp_iteration_radar.md`，把 P1 黑盒控制、Kernel/API、receiver/capture、XP 硬件/4.4/自动绑定、视觉脚本产品化、运维扩容和 claim boundary 映射成 GUI 下一步动作；它是研发雷达，不写 evidence。
- `XP Timeline` opens and exports `evidence/<run_id>_<stage>_xp_iteration_timeline.md`, turning public XP evolution signals into chronological lessons, pitfalls, R&D actions, SOP gates, required evidence, and stop rules. It does not write JSONL evidence, prove real iPhone control, or prove XP parity.
- `XP Drill` opens and exports `evidence/<run_id>_<stage>_xp_iteration_drill.md`, turning XP iteration details into concrete validation drills, required evidence, failure categories, stop rules, and GUI owners. It does not browse automatically, write JSONL evidence, prove real iPhone control, or prove XP parity.
- `Roadmap` 会打开并导出 `evidence/<run_id>_<stage>_xp_roadmap.md`，把 XP 公开信号、行业 SOP、本地实现、证据门、下一步研发动作和停止线合成 P0-P4/XP parity 闭环路线图；它不写 JSONL evidence，也不证明 XP 对标完成。
- `iOS SOP` 会打开并导出 `evidence/<run_id>_<stage>_ios_field_sop.md`，把真实 iPhone 设置、rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy、AirPlay/网络、Hub/Cable、baseline screenshot、manual observation 和 claim boundary 做成现场核对表；它不写 JSONL evidence。
- `Shot Bench` 会对当前选中设备连续采集默认 10 张截图，复用 `screenshot_quality` 判断黑屏、白屏、低纹理、尺寸漂移并保存 artifact，导出 `evidence/<run_id>_<stage>_capture_bench.md`；它只证明 receiver/capture 截图质量，不证明 HID 或完整 iOS 控制。
- `Control Bench` 会读取当前 JSONL evidence，把点击、滑动、文本输入拆成三条控制响应 lane，区分 API/HID 命令 ready、Manual pass、Manual fail 和 command fail，导出 `evidence/<run_id>_<stage>_control_bench.md`；它是审计面板，不写 evidence，也不能替代真实 iPhone 人工观察。
- `Ctrl Ledger` 会读取当前 JSONL evidence，把 HID click、HID swipe、Keyboard input 三条 Manual proof lane 分开显示，并把笼统 Manual 记录放进 `Generic Manual quarantine`；`Record Pass` / `Record Fail` 只应在操作者看到真实 iPhone 对该 lane 响应后使用，导出 `evidence/<run_id>_<stage>_control_ledger.md`。
- `Rerun` 会打开并导出 `evidence/<run_id>_<stage>_rerun_playbook.md`，把 Triage 中的失败类别和 Route/Doctor/Acceptance/Readiness gate 变成最小重跑动作、fresh run_id 规则、证据保留项和停止线；它不写 JSONL evidence，也不证明实机通过。
- `Recovery` 会打开并导出 `evidence/<run_id>_<stage>_recovery_drill.md`，把 receiver 重启/截图复测、HID 释放/重绑、校准重做、视觉回放、单设备隔离、metrics watchdog 和 handoff 边界写成恢复演练；弹窗里的 `Record Pass` / `Record Fail` 可把选中恢复 lane 的执行结果写入 JSONL，但不替代 `Manual` / `P1 Trial` 的真实 iPhone 控制观察。
- `Problems` 会打开并导出 `evidence/<run_id>_<stage>_sop_problem_ledger.md`，把行业坑点、Issue Triage 失败类别、Rerun 最小重跑规则、fresh run_id 判断、证据保留项和停止线合成长期 SOP 问题台账；它不写 JSONL evidence，也不证明真实 iOS 控制。
- 路线决策闭环：`Route Init` 会生成 `evidence/<run_id>_route_decision.json`，`Edit` 可在 GUI 内填写 receiver、HID、iPhone、Hub、线材、operator、允许实跑和阻断项；表单里的 `Use Metadata` 会把底部 Metadata 行和当前设备选择带入路线字段，`Scan Issues` 会提示 `missing`、`placeholder`、`not allowed`、`open blocker`。`Validate` 会输出 `evidence/<run_id>_route_decision.md`，并按现有规则把组件台账或路线失败写入 `evidence/<run_id>.jsonl`。
- 路线补齐清单：`Checklist` 会生成 `evidence/<run_id>_route_checklist.md`，列出每个问题字段、当前值和处理动作；它不会写 evidence，也不会把本轮 run_id 标记为失败。
- 外场与验收报告：`Field Packet` 只生成现场执行 checklist；`Worksheet` 生成 `evidence/<run_id>_<stage>_operator_worksheet.md`，用于操作员逐项填写结果、附件和失败分类；`Center` 可导出 `evidence/<run_id>_<stage>_gui_control_center.md`；`Industry` 可导出 `evidence/<run_id>_<stage>_industry_sop_radar.md`；`Roadmap` 可导出 `evidence/<run_id>_<stage>_xp_roadmap.md`；`iOS SOP` 可导出 `evidence/<run_id>_<stage>_ios_field_sop.md`；`Verify` 可导出 `evidence/<run_id>_<stage>_verification_walkthrough.md`；`Core` 可导出 `evidence/<run_id>_<stage>_xp_core_functions.md`；`Dashboard` 可导出 `evidence/<run_id>_<stage>_stage_dashboard.md`；`Pack` 可导出 `evidence/<run_id>_<stage>_evidence_pack.md`；`XP Gap` 可导出 `evidence/<run_id>_<stage>_xp_gap_audit.md`；`Acceptance` 只读取本轮 JSONL 并生成 `evidence/<run_id>_<gate>_acceptance.md`；`Gap` 会生成 `evidence/<run_id>_<gate>_gap.md`，把失败的 acceptance check 转成 GUI 操作和需要补的 evidence；这些报告都不会把自身伪装成实机成功证据。
- 人工观察记录：底部 `Manual` 行可记录实机观察到的 pass/fail/info/skip、失败分类、备注和失败截图路径。
- 操作日志。

## 测试路径

### 离线测试

不接 iPhone 和硬件时，可以验证：

1. 启动 GUI。
2. 顶部 `Evidence` 输入 `offline_smoke_YYYYMMDD`，保持 `Record` 勾选。
3. 点击 `Start Local`。
4. 点击 `Doctor`，当前机器如果未安装 UxPlay，预期会提示 doctor fail，并生成 `evidence/offline_smoke_YYYYMMDD_doctor.md`。
5. 点击 `Ping`。
6. 输入 `dev_1`，点击 `Register`。
7. 设备列表出现 `dev_1`，状态为 `offline`。
8. 再注册 `dev_2`，在设备表里同时选中 `dev_1` 和 `dev_2`。
9. 在 `Groups` 旁输入 `smoke_group`，点击 `Save Selected`。
10. 点击 `Groups` 刷新，确认下拉框能看到 `smoke_group`。
11. 点击 `Load`，确认设备表重新选中该分组里的设备。
12. 点击 `Delete` 删除分组，再点击 `Groups` 确认它消失。
13. 点击 `Scan`，当前机器如果没有硬件，通常只会看到系统串口或空列表。
14. 在底部 `SOP` 行保持阶段为 `p1`，点击 `Route Init`，确认生成 `evidence/offline_smoke_YYYYMMDD_route_decision.json`。
15. 点击 `Edit` 打开路线表单；点击 `Scan Issues`，确认占位符和未允许实跑会被提示；离线测试时不要伪造真实 receiver/HID/iPhone 字段，只确认表单能打开并保存。
16. 点击 `Checklist`，确认生成 `evidence/offline_smoke_YYYYMMDD_route_checklist.md`；这一步不写 evidence，也不会把 run_id 标成 blocked。
17. 不填写真实硬件时点击 `Validate`，预期路线校验 FAIL，并把 `route_decision` 失败写入本轮 JSONL；这轮 run_id 应视为 blocked，不可用于宣称 P1。
18. 点击 `Field Packet`，确认生成 `evidence/offline_smoke_YYYYMMDD_field_packet.md`，里面会列出当前 doctor/readiness 阻断项。
19. 点击 `Worksheet`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_operator_worksheet.md`；这一步不写 evidence，只生成现场填表。
20. 点击 `Dashboard`，确认弹出 P0-P4 阶段矩阵；点击弹窗里的 `Export`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_stage_dashboard.md`。
21. 点击 `Pack`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_evidence_pack.md`；它会列出 required missing 项，但不写 evidence。
22. 点击 `XP Gap`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_xp_gap_audit.md`；它会列出 XP 核心能力域的当前差距，但不写 evidence。
23. 点击 `Verify`，确认弹出 GUI Verification Walkthrough；离线时 P0 自检可以 ready，但 Run identity、Route、Doctor、截图、HID 和 handoff 仍会按真实缺口显示 fail/pending。
24. 点击 `Industry`，确认弹出 GUI Industry SOP Radar；离线时行业主流路线、XP 产品壁垒、iPhone 设置、receiver/HID 和声明边界应显示 pending/warn/fail，不能当成实机通过。
25. 点击 `Procure`，确认弹出 GUI Route Procurement SOP；离线时 route lock、receiver/HID procurement、XP parity purchase、iPhone fixture 和 claim/spend stop line 应保持 pending/warn/fail，不能当成采购或实机通过。
26. 点击 `Core`，确认弹出 XP Core Function Matrix；离线时 API/SDK 可以显示 ready/pending，但 receiver、HID、截图、校准、输入等真机域不能显示为实机通过。
27. 点击 `Routes`，确认弹出 GUI Mainstream Route Matrix；离线时 XP 式黑盒控制主线、receiver/HID 候选应显示 pending/fail，WDA/Appium 和 MDM/Shortcuts 应显示为非主线或辅助路线，不能当成控制证据。
28. 点击 `Pitfalls`，确认弹出 GUI Pitfall Library；离线时 receiver、HID、校准、视觉、群控、性能、业务状态、claim boundary 和 XP 硬件对标风险应保持 pending/warn/fail，并显示首个探针、停止线和下一步 GUI 动作。
29. 点击 `Sources`，确认弹出 XP Public Source Ledger；离线时官网兼容性、XP 硬件/4.4/Windows/wired/硬解等公开说法应保持 warn/fail/pending，不能当成我们已支持。
29a. 点击 `Src Refresh`，确认弹出 XP Source Refresh Board；离线时公开来源刷新、package registry、Apple/iOS 设置和 source-to-SOP 落地应保持 warn/pending/fail，不能当成资料已经当前或实机能力已通过。
29b. 点击 `Src Audit`，确认弹出 XP Public Source Audit；默认 offline 行应为 pending，可点 `Run Live` 抓取 URL/PyPI 状态并导出 `evidence/<run_id>_<stage>_xp_public_source_audit.md`，但它仍不能当成实机证据。
30. 点击 `Iter Radar`，确认弹出 XP Iteration Radar；离线时 P1 黑盒控制、XP 硬件/4.4/自动绑定、receiver/capture 等应显示 pending/warn/fail，不能当成研发已完成。
30a. 点击 `XP Timeline`，确认弹出 XP Iteration Timeline；离线时公开迭代阶段可以作为研发线索，但 receiver/capture、XP 硬件、firmware/wired binding、ops scale 和 claim governance 不能显示为实机通过或 XP parity。
30b. 点击 `XP Drill`，确认弹出 XP Iteration Drill Board；离线时 iOS settings、receiver binding、XP hardware/4.4、restart/logs、P3/P4 scale 和 claim boundary 不能显示为实机通过。
30c. 点击 `XP Arch`，确认弹出 XP Architecture Map；离线时 hardware/HID、projection/receiver、capture/vision、evidence/readiness 和 group ops 不能显示为 XP 对标完成。
31. 点击 `Roadmap`，确认弹出 XP Roadmap；离线时 P1 receiver/HID、校准输入、XP hardware/wired/4.4/hard-decode 和 claim closure 不能显示为实机通过。
32. 点击 `Compat`，确认弹出 Device/iOS Compatibility Matrix；离线时未知机型/iOS 或未实测机型应显示 not_covered，不能把官网兼容性宣传当成本地通过。
33. 点击 `Goals`，确认弹出四条验收目标看板；离线时 iOS perfect control 和 XP core functions 应显示 fail/pending/warn，不能当成 P1 通过。
34. 点击 `Kit Gate`，确认弹出 P1 开跑前闸门；离线/模板路线下 Open P1 stop line 应显示 fail/pending，XP 硬件对标不能被 CH9329 路线误判为 pass。
35. 点击 `iOS SOP`，确认弹出真实 iPhone 设置核对表；离线时 AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、Auto-Lock、brightness、network、AirPlay、Hub/Cable 和 baseline artifact 都必须有状态和停止线，不能因为设置项 ready 就宣称实机控制通过。
36. 点击 `Bench`，确认弹出硬件测试台；离线时 receiver、HID、截图/控制证据和 XP 硬件对比应显示 fail/pending，不能当成硬件通过。
37. 点击 `Start Pack`，确认弹出首轮实机验证包；离线时应把 sources/industry/procure/api_cov/roadmap/verify/local/core/routes/rx_score/rx_bootstrap/rx_setup/pitfalls/rerun/recovery/goals/kit_gate/ios_sop/route/doctor/截图/HID/acceptance/readiness 阻断项串成 operator guide，不写 evidence。
38. 点击 `Shot Bench`，离线或未接 receiver 时预期失败或报错；接入真实 receiver 后才允许把导出的 capture bench 当成截图质量审计。
39. 点击 `Control Bench`，确认弹出点击、滑动、文本输入三条控制响应 lane；离线时应显示 pending/ready/fail，不能因为 API 命令存在就宣称 iPhone 已响应。
39a. 点击 `Ctrl Ledger`，确认弹出 HID click、HID swipe、Keyboard input 三条分 lane 实控证据台账；离线时不能用一条泛化 Manual pass 关闭三条 lane。
40. 点击 `Wizard`，确认弹出现场证据向导；离线时 Run identity、Physical ledger、Route、Doctor、Receiver screenshot、HID 控制等步骤会显示 fail/pending，不能当成实机通过。
40a. 点击 `Runner`，确认弹出现场证据执行台；离线时 Route/Doctor/截图/HID click/HID swipe/Keyboard input/Acceptance/Readiness/Claim boundary 会显示 fail/pending，`Copy Command` 只能复制命令，不等于执行或通过。
41. 点击 `SOP`，确认弹出当前 P1 八步 SOP Board；离线时应看到 Device scope、Route decision、Doctor、Capture/control evidence 等阻断项。
42. 在 SOP Board 里选中 `Route decision` 行，确认 `Primary command` 为 `Edit Route`；点 `Run Selected` 应打开 Route Decision Editor。
43. 点击 `SOP MD`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_gui_sop_board.md`；它只是一张执行/复盘工作台，不写 evidence，也不证明实机通过。
43. 在底部 `Scenario` 点击 `Library`，确认弹出脚本库，能看到 `p1_single_device_control_probe`、`p1_receiver_capture_probe`、`p2_single_device_stability`、`pilot_4_group_smoke` 等阶段脚本。
44. 在 Library 里选中 P1 脚本，点击 `Use Selected`，确认 `Scenario` 路径被填入且 `Dry Run` 自动勾选。
45. 也可以选择 `tests/fixtures_script_runner_dry_run.json`，保持 `Dry Run` 勾选，点击 `Run`。
46. 取消 `Dry Run` 后再点 `Run`，离线时应被 Real-run Guard 拦截，并生成 `evidence/offline_smoke_YYYYMMDD_p1_real_run_guard.md`。
47. 重新勾选 `Dry Run`，确认日志出现 `Scenario ok`，并生成 `evidence/<run_id>.md` 场景汇总。
48. 点击顶部 `Summary`，确认生成 `evidence/offline_smoke_YYYYMMDD.md`。
49. 点击顶部 `Timeline`，确认弹出本轮 JSONL 事件流水；点击弹窗里的 `Export`，确认生成 `evidence/offline_smoke_YYYYMMDD_timeline.md`。
50. 点击顶部 `Matrix`，确认弹出按设备聚合的 evidence matrix；离线时 dev_1/dev_2 应显示缺 component metadata、screenshot quality 或 manual observation。
51. 点击顶部 `Triage`，确认弹出按失败类别聚合的问题表；如果没有非聚合失败事件，应显示空问题桶。
52. 点击顶部 `Rerun`，确认弹出最小重跑决策表；离线时 Route/Doctor/Acceptance/Readiness 应显示 fail/pending/warn，并提示是否需要 fresh run_id、要保留什么证据和何时停止。
53. 点击顶部 `Recovery`，确认弹出恢复演练表；离线时 receiver、HID、校准、群控、performance 和 handoff lane 应显示 fail/pending/warn，并给出恢复步骤、验证步骤和停止线；弹窗底部应有 `Record Pass` / `Record Fail`，但离线时不要把它当成真实 iPhone 控制证据。
54. 点击顶部 `Review`，确认生成 `evidence/offline_smoke_YYYYMMDD_review.md`；如果还没有 JSONL，GUI 应提示先记录 evidence。
55. 点击底部 `Gap`，确认生成 `evidence/offline_smoke_YYYYMMDD_p1_gap.md`，里面会提示缺 evidence、device traceability、component metadata、manual observation 和 screenshot quality。
56. 点击底部 `Acceptance` 或顶部 `Readiness`，当前无实机 evidence 或 doctor fail 时预期生成 FAIL 报告，不能把它当成 P1 通过。

这只能证明 GUI、客户端、XP API、内核服务之间能连通。

### 实机测试

接入 iPhone 和硬件后，按顺序测试：

1. 在底部 `SOP` 行选择阶段 `p1`，点击 `Route Init`。
2. 先在底部 `Metadata` 行填 receiver provider、capture method、HID provider、HID/串口、iPhone 和 iOS 版本，必要时点击 `Record Metadata` 写入本轮 evidence。
3. 点击 `Edit`，再点击 `Use Metadata`，把当前设备选择和 Metadata 行带入 route decision 表单。
4. 补齐 receiver path/start command/AirPlay name、HID firmware、iPhone model、Hub、线材、operator、`Decision reason`；确认无阻断项时保持 `Open blockers` 为空，并把 `Allow P1 real run` 设为 `true`。
5. 点击 `Scan Issues`，清理所有 `missing`、`placeholder`、`not allowed` 和非预期 `open blocker`。
6. 点击 `Checklist` 导出补齐清单，留给外场人员复核。
7. 点击 `Save + Validate` 或关闭表单后点击 `Validate`；如果失败，本轮 run_id 视为 blocked，修完后换新 run_id 再开测。
8. 点击 `Field Packet`，按生成的执行包逐项测试。
9. 点击 `Worksheet`，把生成的操作员表单给现场人员逐项填写结果、附件和失败分类。
10. `Scan` 确认新串口出现。
11. 选择串口，点击 `Bind`。
12. 确认设备状态从 `offline` 进入 `online`。
13. 点击 `Start AirPlay`。
14. 在 iPhone 上选择对应 AirPlay 接收端。
15. 点击 `Start Capture`。
16. 点击 `Screenshot`，确认服务端能返回截图数据。
17. GUI 右侧出现截图预览，并确认底部状态不是 `screenshot quality failed`。
18. 点击 `Shot Bench`，确认连续截图没有黑屏、低纹理或尺寸漂移。
19. 在截图预览上点击一个安全区域，确认 `Click X/Y` 自动更新为原图坐标。
20. 在截图预览上拖拽一个有纹理的按钮区域，点击 `Save Crop`；如果提示 `Template quality failed`，换一个更大、更有纹理的区域。
21. 在 `Coordinate Calibration` 面板点击 `Use Screenshot`，必要时手动调整 `Active x/y/w/h` 和 `Target w/h`。
22. 勾选 `Enabled`，点击 `Save` 保存设备校准。
23. 点击 `Find`，确认能找回模板位置并填入 `Click X/Y`。
24. 点击一个颜色点，点击 `Find Color`，确认找色结果。
25. 点击 `OCR`，确认 OCR 返回数量。
26. 输入文字，点击 `Find Text`，确认找到后填入坐标。
27. 点击 `Click`，观察 iPhone 是否响应。
28. 测试 `Swipe`。
29. 测试 `Type`。
30. 多选两台或更多设备，测试批量 `Click`、`Swipe`、`Type`，确认每台设备结果都写入日志。
31. 把 4 台设备保存为一个分组，关闭并重启 GUI 后刷新分组，确认 `state/groups.json` 里的分组仍可加载；重新选中设备后确认 `state/device_profiles.json` 里的 Metadata 能回填到输入框。
32. 加载分组后执行批量 `Click`、`Swipe`、`Type`，确认任意单台失败不会阻塞其他设备返回结果。
33. 每次人工观察 iPhone 响应后，在底部 `Manual` 行记录 `pass` 或 `fail`。失败时选择 `Category`，例如 `hid`、`airplay_stream`、`capture`，并填写截图/录屏路径。
34. 点击 `Control Bench`，确认点击、滑动、文本输入都有 Manual pass；只显示 `ready` 时继续补人工观察。
35. 在底部 `Scenario` 点击 `Library`，按当前阶段选脚本；P3/P4 脚本只能在 P1/P2 通过后使用。
36. 先勾选 `Dry Run` 跑一遍；取消 `Dry Run` 前确认 Real-run Guard 需要的 Route Decision、Doctor 无 fail 和设备数量都已经通过；替代 receiver 的 Doctor warn 必须能解释为 route-specific warn。
37. 取消 `Dry Run` 实跑；如果被 Real-run Guard 拦截，先打开生成的 guard report 修 blocker，不要绕过。
38. 实跑场景必须包含截图、识别、点击/滑动/输入、等待、人工观察 `record`。
39. 点击 `Gap` 生成补证据清单，逐项确认是否还缺设备追踪、组件台账、人工观察、截图质量或 metrics。
40. 点击 `Acceptance` 生成本轮阶段门报告；FAIL 时按 `Gap` 清单继续补截图质量、人工观察、组件台账或失败分类证据。
41. 点击 `Summary`，把本轮证据汇总保存，失败项必须能追溯到设备 ID、步骤、错误文本和附件路径。
42. 点击 `Timeline`，逐条检查事件顺序、设备 ID、失败分类、附件和详情；缺设备 ID 或附件的事件必须补记。
43. 点击 `Matrix`，确认每台目标设备都有事件、组件台账、截图质量 pass、人工观察 pass；P3/P4 任一设备不是 PASS 都不能晋级。
44. 点击 `Triage`，按失败类别看影响设备、附件和 SOP 下一步动作，先修最高频或最阻塞的一类。
45. 点击 `Rerun`，把失败类别、影响设备、gate 状态和 fresh run_id 规则转成下一轮最小复测动作；Route/硬件/receiver/iPhone 设置改变时必须换新 `run_id`。
46. 点击 `Recovery`，把 receiver 重启/截图复测、HID 释放/重绑、校准重做、单设备隔离和 metrics watchdog 转成恢复演练；恢复步骤完成并验证后，对选中 lane 点击 `Record Pass` / `Record Fail` 写入恢复执行证据，然后仍需用 `Manual` / `P1 Trial` 记录真实 iPhone 点击、滑动、输入观察。
47. 点击 `Review`，用失败分类、metrics 和建议决定下一轮是扩容、复测还是转研发修复。
48. 点击 `Readiness`，只有报告中 P1 为 PASS 时，才允许讨论进入 P2；P1 FAIL 时按 blockers 继续补投屏、HID 或人工 observation 证据。
49. 点击 `Dashboard`，确认当前阶段行没有 pending/fail；如果仍有 blocker，按 `Next action` 回到 GUI 对应入口补证据。
50. 点击 `Pack` 导出本轮证据包索引，检查 required artifacts 是否都为 present，再交给复盘人员确认。
51. 点击 `Verify` 导出逐步验证工作台，确认本轮没有跳过 Route、Doctor、截图、HID、Acceptance 或 Readiness 的停线。
52. 点击 `Core` 导出核心功能覆盖矩阵，确认 API/SDK ready 没有被误解成 receiver/HID/截图/输入真机通过。
53. 点击 `XP Gap` 导出核心差距审计，确认 P1 相关的 `Receiver/Capture`、`USB/HID`、`Component Ledger` 和 `Coordinate Calibration` 不再是 blocked/not_started。

实机测试要同步记录：

- iPhone 型号。
- iOS 版本。
- 硬件型号和固件版本。
- 串口号。
- 投屏组件版本。
- 是否成功。
- 失败截图和日志。

## 当前限制

- GUI 只显示手动刷新后的截图预览，还不是实时投屏画面。
- 当前投屏后端仍依赖原型里的 UxPlay/X11 思路，Windows XP 级投屏服务尚未实现。
- HID 控制仍依赖当前 CH9329 协议实现，XP 专用硬件和 4.4 固件未实测。
- 模板裁剪会做基础质量校验，拒绝过小或低纹理模板；但模板资产管理、阈值推荐、透明图处理和失败用例库仍未完成。
- 分组管理是本地 JSON 原型，不包含 XP 官方的云端分组、子账号、局域网可见范围规则。
- 坐标校准是本地映射配置，不等于 XP 官方 4.4 固件的自动绑定和自动分辨率适配。
- 证据记录会覆盖 GUI/API 操作、组件元数据和人工观察，Manual 支持失败分类，Screenshot 支持基础画质校验，Review 会汇总失败分类、metrics 和建议，Readiness 会汇总阶段状态；但它不会自动判断 iPhone 是否真实响应，实机验收仍要人工观察并记录。
- `Route Edit` 只负责把路线台账填到同一份 JSON；`Use Metadata` 只复制 GUI 当前字段，不判断硬件真假；`Checklist`、`Worksheet`、`Dashboard`、`Pack`、`Verify`、`Core`、`Procure`、`Roadmap`、`Kit Gate`、`iOS SOP`、`Rerun`、`XP Gap` 和 `Gap` 是补齐/填写/索引/研发审计清单，不写 evidence；`Recovery` 的 `Record Pass` / `Record Fail` 只写恢复执行证据，不会自动生成真实点击、滑动、输入控制证据；`Field Packet` 和 `Acceptance` 是报告入口，不会自动生成真实控制证据；`Route Validate` 写入的路线证据只能证明组件台账，不替代截图质量和人工观察。
- GUI 场景执行只是 JSON 脚本运行器的入口，还没有循环、变量、条件分支和失败截图自动采集。
- 同步节拍控制、多窗口分离、快捷键还未做。

## 下一步 GUI 迭代

建议顺序：

1. 增加透明图、多点找色调试和失败截图回放。
2. 增加按分组运行脚本的变量、条件和同步节拍控制。
3. 增加真实 receiver 日志附件、按设备日志过滤和自动恢复结果写证据。
4. 增加路线决策表单按问题字段跳转。
5. 明确 Windows 投屏路线后，再做实时画面网格。
## 2026-06-08 GUI Layer Additions

This section is intentionally ASCII-only to avoid Windows console encoding drift during field handoff.

## 2026-06-09 iOS SOP Additions

- Route Decision now captures rotation lock, AssistiveTouch menu state, mouse parameter profile, and QR scan policy.
- `iOS SOP` treats those fields as pre-P1 setup gates. They can make a desk ready for testing, but they do not prove screenshot quality, click/swipe/type response, or XP parity.
- `Sources` adds an official setup/mouse-parameter source row so XP first-configuration lessons become GUI actions instead of untracked tribal knowledge.

### Operator Home

The `Home` button in the Live Probe workflow row opens the operator workflow map and exports `evidence/<run_id>_<stage>_operator_home.md`.

Use it as the first GUI board in a field session:

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

Rows group knowledge, route/kit/iPhone settings, local command replay, receiver screenshot proof, HID click/swipe/text proof, repeatable scripts, XP event/error parity, problem/rerun handling, and handoff gates.

Use `Run Selected` from the first `fail`, `pending`, or `warn` row, then refresh Home after the artifact or JSONL evidence is created.

Boundary:

- Home does not run commands by itself.
- Home does not write JSONL evidence.
- Exported Home Markdown does not prove real iPhone response.
- Real iOS control still requires current screenshots, Manual/P1 Trial observations, Acceptance, Readiness, and categorized failure triage for the same run_id.

### Local Verification

The `Local` button in `Live Probe` opens a local verification board and exports `evidence/<run_id>_<stage>_local_verification.md`.

It splits the previous one-line offline check into operator-facing rows:

1. `.\.venv\Scripts\python -m unittest discover -s tests -v`
2. `.\.venv\Scripts\python -m compileall -q imouse tests`
3. `.\.venv\Scripts\python -m imouse.main --check`
4. `.\.venv\Scripts\python -m imouse.doctor --json`
5. `.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --json`
6. `.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id <run_id>`
7. `.\.venv\Scripts\python -m imouse.readiness --target <stage> --evidence evidence\<run_id>.jsonl`

Use it before Receiver Gate when you want a second operator to reproduce local state without guessing command order.

Boundary:

- Local Verification does not run the commands.
- Local Verification does not write JSONL evidence.
- Local green checks do not prove screenshot quality, HID response, XP parity, or real iOS control.

### Receiver Route Gate

The `Receiver` button in `Live Probe` opens the receiver-route gate and exports `evidence/<run_id>_<stage>_receiver_route_gate.md`.

Rows cover Route Decision source, route validation/open blockers, receiver provider config, `uxplay` dependency vs alternate receiver route, capture binding, screenshot proof boundary, and claim boundary.

Expected field use:

1. Click `Route Init` or `Edit` and fill real receiver fields.
2. Click `Validate`.
3. Click `Doctor` with the same route decision selected.
4. Click `Receiver`.
5. If the selected route is `windows_receiver`, `wired`, or `capture_card` and provider preflight is valid, missing `uxplay` should show as a non-blocking route-specific warning rather than a hard blocker.
6. Continue to `Shot Bench`, `P1 Trial`, `Acceptance`, and `Readiness`; do not treat Receiver Gate as real iPhone control evidence.

Boundary:

- Receiver Gate does not write JSONL evidence.
- Receiver Gate does not start AirPlay/receiver capture by itself.
- Passing Receiver Gate does not prove screenshot quality, HID response, click/swipe/text input, XP parity, or real iOS control.

### Receiver Candidate Scorecard

The `Rx Score` button in `Live Probe` opens the receiver candidate scorecard and exports `evidence/<run_id>_<stage>_receiver_candidate_scorecard.md`.

Use it when the team must choose between UxPlay, a Windows AirPlay receiver, wired projection, and capture-card routes.

Expected field use:

1. Click `Coach`.
2. Click `Rx Score`.
3. Inspect `Status`, `Recommendation`, `Selected`, `Score`, `Strengths`, and `Gaps`.
4. Select the first `fail` or selected-route gap, then click `Run Selected`.
5. If `UxPlay open receiver` is blocked by `binary:uxplay=fail`, either install UxPlay or choose a valid alternate route under a fresh run_id.
6. Continue to `Rx Bootstrap`, `Rx Setup`, `Doctor`, `Shot Bench`, `P1 Trial`, `Acceptance`, and `Readiness`.

Boundary:

- Rx Score does not write JSONL evidence.
- Rx Score does not install, start, or prove a receiver.
- A recommended receiver route does not prove screenshot quality, real iPhone response, iOS perfect control, broad compatibility, or XP parity.

### Receiver Route Bootstrap

The `Rx Bootstrap` button in `Live Probe` opens a form for turning an alternate receiver candidate into a draft Route Decision JSON and a bootstrap report.

Use it after `Rx Score` when `uxplay` is missing and the team has a real Windows receiver, wired projection app, or capture-card path to test.

Expected field use:

1. Click `Coach`.
2. Click `Rx Score`.
3. Click `Rx Bootstrap`.
4. Fill real receiver path, name, version, start command, AirPlay/display name, capture method, window title/process binding, and device id.
5. Click `Write Bootstrap`.
6. Confirm the GUI selected the generated Route Decision JSON.
7. Continue to `Rx Setup`, `Doctor`, `Receiver`, `Shot Bench`, `P1 Trial`, `Acceptance`, and `Readiness`.

Boundary:

- Receiver Route Bootstrap only fills receiver/capture metadata for preflight.
- It keeps `allowed_to_run_p1=false`.
- It does not write JSONL evidence.
- It does not prove screenshot quality, HID response, visible iPhone click/swipe/text response, iOS perfect control, broad compatibility, or XP parity.

### Receiver Setup Wizard

The `Rx Setup` button in `Live Probe` opens the route-aware receiver setup wizard and exports `evidence/<run_id>_<stage>_receiver_setup_wizard.md`.

Rows cover run identity, route validation, selected receiver lane, UxPlay install, Windows receiver, wired/capture-card setup, capture binding, iPhone-to-receiver binding, screenshot bench, reconnect/log attachment, and claim boundary.

Expected field use:

1. Click `Coach`.
2. Click `Rx Score`.
3. Click `Rx Bootstrap` if the selected lane is a Windows receiver, wired route, or capture-card route that needs a route-decision draft.
4. Click `Rx Setup`.
5. Fix the first row that is not `pass`.
6. Use the command column or `Run Selected`.
7. Export the wizard for handoff.
8. Continue to `Rx Evidence`, `Receiver`, `Shot Bench`, `P1 Trial`, `Acceptance`, and `Readiness`.

Boundary:

- Receiver Setup Wizard does not install software.
- Receiver Setup Wizard does not write JSONL evidence.
- Passing Receiver Setup Wizard does not prove real iPhone response, broad iOS compatibility, or XP parity.

### Receiver Evidence Checklist

The `Rx Evidence` button in `Live Probe` opens the receiver/capture proof checklist and exports `evidence/<run_id>_<stage>_receiver_evidence_checklist.md`.

Rows cover route lock, receiver provider preflight, route-aware Doctor, receiver identity binding, baseline screenshot, receiver capture probe set, reconnect/log triage, HID handoff, and Acceptance/Readiness claim closure.

Expected field use:

1. Complete `Rx Setup` for the selected route.
2. Click `Rx Evidence`.
3. Fix the first row that is `fail`, `pending`, or `warn`.
4. Run the route-aware Doctor command from the export.
5. Dry-run and then real-run `scripts/p1_receiver_capture_probe.json` only after replacing placeholder metadata.
6. Attach receiver/HID logs for failures.
7. Continue to `P1 Trial` only after baseline screenshot and receiver capture proof are clean.
8. Run Acceptance and Readiness for the same run_id.

Boundary:

- Receiver Evidence Checklist does not start or install a receiver by itself.
- The export itself does not write JSONL evidence.
- A clean receiver evidence checklist is not a real iPhone control pass.
- It does not prove broad iOS compatibility, group control, XP hardware parity, or iOS perfect control.

### P1 Field Transcript

The `Transcript` button in `Live Probe` opens the fillable P1 field transcript and exports `evidence/<run_id>_<stage>_p1_field_transcript.md`.

Rows cover the transcript header, receiver setup split, every Coach checkpoint, and operator sign-off. Each row includes an observation prompt, expected result, likely failure categories, artifact path, rerun rule, stop rule, and GUI action.

Expected field use:

1. Click `Coach`.
2. Click `Rx Score`.
3. Click `Rx Bootstrap` if an alternate receiver route needs a fresh route-decision draft.
4. Click `Rx Setup`.
5. Click `Transcript`.
6. Export or keep the transcript open while watching the physical iPhone.
7. Use `P1 Trial` or Manual recording to write real observations into JSONL.
8. Use transcript fail rows to decide the smallest rerun.

Boundary:

- Transcript does not write JSONL evidence.
- Transcript does not record Manual pass by itself.
- Passing or filling Transcript does not prove real iPhone response, iOS perfect control, broad compatibility, or XP parity.
- `Prefill Manual` only prepares the Manual controls; non-control checkpoints are downgraded to `info` so setup rows cannot accidentally satisfy the real-control Manual gate.

### Command Queue

The right-side `Command Queue` panel is for building a short repeatable operation from the current GUI controls:

1. Select one or more devices in the device table, or type a fallback `Device ID`.
2. Fill the current click/swipe/text/template controls.
3. Use `Add Click`, `Add Swipe`, `Add Type`, `Add Shot`, or `Add Find+Click`.
4. Keep `Dry Run` enabled for the first run.
5. Set `Repeat` and `Wait`.
6. Click `Save JSON` to export `evidence/<run_id>_gui_queue.json`.
7. Click `Run`; the queue is executed by `ScriptRunner`, so every step and screenshot quality result is appended to `evidence/<run_id>.jsonl`.
8. Only disable `Dry Run` after Route Decision, Doctor, and receiver/HID checks are clean.

Validation expectation:

- Dry-run queue should produce a scenario summary without touching real devices.
- Real-run queue should record per-device step evidence.
- `Add Shot` records screenshot quality and saves screenshot artifacts through `ScriptRunner`.
- `Add Find+Click` validates the local template quality before attempting the live match.

### Scenario Library

The `Library` button beside the `Scenario` path scans `scripts/*.json` and opens a script picker.

Rows include:

- inferred stage;
- scenario name;
- load status;
- flattened step count;
- action counts;
- referenced device ids and groups;
- dry-run policy;
- file path;
- note.

Validation expectation:

- Library always loads a script with `Dry Run` enabled.
- Bad JSON scripts must remain visible as failed rows instead of disappearing.
- P3/P4 scripts should not be used before P1/P2 evidence gates pass.
- Exporting the library only writes `evidence/<run_id>_scenario_library.md`; it does not run scripts or prove real iOS control.

### Evidence Timeline

The top `Timeline` button opens a read-only event table for `evidence/<run_id>.jsonl`.
The Timeline dialog can export `evidence/<run_id>_timeline.md`.

Rows include:

- event index and timestamp;
- status;
- step;
- device ids;
- failure category for failed events;
- artifact paths;
- compact details.

Validation expectation:

- Timeline must not create evidence events.
- Failed events must show a failure category when the details contain one or match known failure keywords.
- Missing device ids, screenshot artifacts, or manual observations should be treated as acceptance gaps, not silently ignored.

### Callback Monitor

The top `Callback` button opens an XP callback ledger monitor and can export `evidence/<run_id>_callback_monitor.md`.

Rows include:

- callback sequence;
- event time;
- event/type name;
- device id;
- source;
- severity;
- compact callback data.

Validation expectation:

- Callback Monitor reads XP API/WebSocket callback events through `/callback/list`.
- It is useful for API, receiver, HID, and console debugging.
- It does not write JSONL evidence.
- It does not prove real iOS control.
- Promotion still requires Timeline/Matrix evidence, Acceptance, Readiness, screenshot quality, component metadata, and manual real-iPhone observation.

### Attach Log

The top `Attach Log` button imports a receiver/HID text log, classifies non-empty lines into XP callback events, pushes them through `/callback/push` when the local API is reachable, exports `evidence/<run_id>_callback_log.md`, and writes an `Attach Log triage` JSONL event when `Record` is enabled.

It is intended for field debugging:

- AirPlay/receiver lines become `airplay_log` callback rows.
- screenshot/frame/decoder lines become `capture_log` callback rows.
- CH9329/HID/serial/mouse/keyboard lines become `hid_log` callback rows.
- USB/iPhone/iOS/UDID lines become `device_log` callback rows.
- generic failure lines become `receiver_error` callback rows.

Validation expectation:

- The callback log Markdown is debug data, not proof by itself.
- With `Record` enabled, Attach Log writes log-triage JSONL evidence with severity/category counts and sample lines.
- It helps separate receiver, capture, HID, USB, and device problems before a rerun.
- It does not prove real iOS control or replace screenshot quality and Manual/P1 Trial observations.
- Promotion still requires JSONL evidence, Acceptance, Readiness, screenshot quality, component metadata, and manual real-iPhone observation.

### XP Event/Error Contract

The `Events` button in `Live Probe` opens the XP event/error contract board and can export `evidence/<run_id>_<stage>_xp_event_error_contract.md`.

Rows audit:

- XP API envelope: `status`, `message`, `data.code`, `msgid`, and `fun`;
- HTTP, form, multipart, and WebSocket `/api` replay shape;
- callback lifecycle and `/event/*` aliases;
- receiver/capture/HID error categories;
- vision/OCR/script and group-operation error categories;
- Attach Log ingestion and callback bridge;
- claim boundary for API success, callbacks, logs, reports, Acceptance, and Readiness.

Use `Run Selected` to jump from the selected contract row into XP Gap, Verify, Callback, Matrix, Problems, Assets, Dashboard, Attach Log, or Goals.

Validation expectation:

- Events is an audit board, not JSONL evidence.
- Callback rows and logs are diagnostic context until tied to device id, screenshot quality, Manual observation, Acceptance, and Readiness.
- Passing Events does not prove XP hardware, wired projection, auto-binding, licensing, broad compatibility, or real iOS control.

### Device Evidence Matrix

The top `Matrix` button opens a per-device evidence coverage table for the current run.
The dialog can export `evidence/<run_id>_device_matrix.md`.

Rows are built from current device rows, selected devices, and JSONL evidence events.
Each row checks:

- component metadata;
- event count;
- failure count and category;
- latest event;
- screenshot quality coverage;
- manual observation coverage;
- artifact coverage through Timeline/detail review.

Validation expectation:

- P1 should have the target device PASS before promotion review.
- P3/P4 should have every target device PASS; one pending or failed device blocks group-control promotion.
- `unassigned` rows mean at least one evidence event has no device id and must be fixed or re-recorded.
- Matrix is read-only and does not prove real iOS control by itself.

### Issue Triage

The top `Triage` button groups failed non-aggregate evidence events by failure category.
The dialog can export `evidence/<run_id>_issue_triage.md`.

Rows include:

- failure category;
- count;
- affected devices;
- failed steps;
- first and last timestamps;
- artifact paths;
- SOP next action;
- recommendation.

Validation expectation:

- Aggregate failures such as `scenario summary` should not hide the root failed step category.
- Triage is for deciding the next fix order; it does not replace Timeline, Matrix, Acceptance, or Readiness.
- Route-decision failures that were written to evidence should lead to a fresh run id after blockers are fixed.

### Rerun Playbook

The `Rerun` button turns Issue Triage rows plus Route/Doctor/Acceptance/Readiness gates into an executable rerun decision table.
The dialog can export `evidence/<run_id>_<stage>_rerun_playbook.md`.

Rows include:

- failure category or gate;
- current status and event count;
- affected devices and failed steps;
- current blocker summary;
- smallest rerun rule;
- whether a fresh `run_id` is required;
- evidence to keep;
- stop rule;
- GUI action for the next probe.

Validation expectation:

- Use it after Timeline, Matrix, Triage, and Review, then rerun the smallest failing path first.
- Start a fresh `run_id` when route, wiring, receiver identity, selected devices, or iPhone settings changed.
- A clean rerun table still cannot prove real iOS control unless JSONL evidence, Acceptance, Readiness, and manual real-iPhone observation support the claim.

### Recovery Drill

The `Recovery` button turns current failure categories and stage gates into a recovery drill table.
The dialog can export `evidence/<run_id>_<stage>_recovery_drill.md`.

Rows include:

- route/doctor recovery;
- receiver/capture recovery;
- HID control recovery;
- calibration recovery;
- vision/business-state recovery;
- group isolation recovery;
- performance watchdog recovery;
- handoff/claim recovery.

Each row shows the trigger, current blocker, recovery step, verification step, evidence to keep, stop rule, and next GUI action.
Use `Record Pass` or `Record Fail` after the operator has completed the selected recovery step and verified its result. The recorded JSONL details include `recovery_drill=true`, lane key, categories, recovery step, verify step, stop rule, selected device, note, and optional artifact.

Validation expectation:

- Use it after `Triage` and `Rerun`, before long P2/P3/P4 runs.
- Recovery Markdown export is not evidence by itself. Recovery `Record Pass` / `Record Fail` writes execution evidence, but it does not count as `manual_observation` for click, swipe, or text input unless the operator also records the real iPhone response through Manual/P1 Trial.
- `real_ios_verified=False` keeps handoff/claim recovery from becoming a pass claim even when local gates look clean.

### Real-run Guard

When `Scenario` or `Command Queue` runs with `Dry Run` disabled, GUI checks the Real-run Guard first.
If blocked, it exports `evidence/<run_id>_<stage>_real_run_guard.md` and does not start the real action.

Checks:

- selected device count must satisfy the current stage;
- Route Decision must be loaded, validated, `ok`, and `ready`;
- Doctor must have been run for the current run id and have no `fail`. A route-aware `warn` can be allowed for a documented alternate receiver route, but it is not evidence of screenshot quality or iPhone response.

Validation expectation:

- Offline runs should be blocked.
- A blocked guard report is not evidence of failure on iPhone; it is a stop sign before hardware actions.
- An allowed guard report is only permission to attempt the real run; JSONL evidence, Manual observation, Acceptance, and Readiness still decide claims.
- Do not bypass the guard by calling low-level APIs manually during field acceptance.

### Template Assets

The screenshot preview panel now has `Assets` and `Browse`:

1. Click `Assets`.
2. Click `Refresh` to scan `templates/`.
3. Review `status`, `reason`, `size`, and `stddev`.
4. Select an OK template and click `Use Selected`.
5. Click `Write Index` to export `evidence/<run_id>_template_assets.md`.

Validation expectation:

- Low-texture and too-small crops must stay visible as failed assets.
- A template asset index is not proof of live recognition; it is only a local quality gate.

### Session Snapshot

The `Session` button in `Live Probe` exports `evidence/<run_id>_<stage>_gui_session.md`.
It is a handoff index for the current GUI state:

- selected devices;
- current Live Probe rows;
- SOP Board rows;
- command queue rows;
- local template asset quality rows;
- evidence pack presence/missing status;
- route, doctor, and readiness brief text.

Validation expectation:

- The snapshot must say that it does not write evidence and does not verify real iOS control.
- Use it for handoff and review, not for promotion by itself.
- Promotion still requires Route Decision, Doctor, Acceptance, Readiness, screenshot quality, component metadata, and manual real-iPhone observation evidence.

### Field Runbook

The `Runbook` button in `Live Probe` opens an operator-facing stage guide and can export `evidence/<run_id>_<stage>_field_runbook.md`.

Rows cover:

- bench scope and device-count requirement;
- receiver/capture/HID/iPhone route ledger;
- preflight doctor;
- receiver/capture screenshot quality;
- HID/manual real-iPhone observation;
- template/color/OCR assets;
- stage scenario or command queue dry-run;
- Real-run Guard;
- metrics and stability evidence;
- Timeline/Matrix/Triage/Review;
- Acceptance and Readiness promotion gate.

Validation expectation:

- The runbook must keep fail/pending stop rules visible.
- It does not write JSONL evidence.
- It does not prove real iOS control.
- Use it as the operator checklist before Field Packet and SOP Board review.
- Promotion still requires clean JSONL evidence, Acceptance PASS, Readiness PASS, screenshot quality, component metadata, and manual real-iPhone observation.

### P1 Trial

The `P1 Trial` button in `Live Probe` opens a single-iPhone real-device trial board and can export `evidence/<run_id>_p1_trial.md`.

Rows cover:

- bench ledger and exactly one selected target iPhone;
- Route Decision gate;
- preflight Doctor;
- receiver/capture screenshot quality;
- coordinate calibration;
- HID click;
- HID swipe;
- keyboard text input;
- callback/log triage;
- P1 Acceptance;
- Readiness and promotion review.

The dialog supports:

- `Run Selected` to launch the row's primary GUI command;
- `Record Pass` to write a Manual observation for the selected row;
- `Record Fail` to write a Manual failure with a default failure category;
- `Callback` and `Gap` shortcuts for field triage.

Validation expectation:

- P1 Trial is an operator board, not a success claim.
- Its Manual buttons write JSONL evidence only for what the operator actually observed on the real iPhone.
- It does not prove real iOS control by itself.
- Promotion still requires clean JSONL evidence, Acceptance PASS, Readiness PASS, screenshot quality, component metadata, and manual real-iPhone observation.

### Control Center

The `Center` button in `Live Probe` opens the GUI control center and can export `evidence/<run_id>_<stage>_gui_control_center.md`.

It is the main operator dashboard for choosing the next action. Rows combine:

- stage and device scope;
- route decision and doctor;
- live iPhone evidence from screenshot quality and manual observation;
- receiver/HID callback and attached logs;
- scenario or command queue state;
- vision template assets;
- evidence pack and SOP docs;
- live probe/SOP board blockers;
- promotion claim boundary.

Use `Run Selected` to launch the row's existing GUI action. The control center does not duplicate execution logic; it points to Route Edit, Doctor, P1 Trial, Callback, Scenario Library, Assets, Pack, SOP Board, or Readiness depending on the blocker.

Validation expectation:

- The first `fail` or `pending` row is the next thing the operator should fix.
- A `warn` promotion row means reports may be clean but `real_ios_verified` is still false.
- Exporting the control center does not write JSONL evidence and does not prove real iOS control.

### Knowledge Center

The `Knowledge` button in `Live Probe` opens the industry/SOP/XP benchmark knowledge layer and can export `evidence/<run_id>_<stage>_gui_knowledge_center.md`.

Rows connect research to action:

- XP public product model;
- mainstream iOS group-control route;
- P1 receiver/HID decision;
- field SOP and stage gates;
- hardware bench and procurement;
- XP API and helper parity;
- iteration pitfalls;
- claim boundary.

Use `Run Selected` to jump from a knowledge row into the existing GUI action, such as XP Gap, Control Center, Route Edit, Field Runbook, Attach Log, Triage, or Readiness.

Validation expectation:

- Missing knowledge/source docs stay visible as `fail`.
- Public/industry knowledge can be `pass` while product parity remains `warn` or `fail`.
- Exporting the knowledge center does not write JSONL evidence and does not prove real iOS control.

### Industry SOP Radar

The `Industry` button in `Live Probe` opens the current-state industry/SOP radar and can export `evidence/<run_id>_<stage>_industry_sop_radar.md`.

Rows include:

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

Each row shows current local gate, public/current-state signal, SOP decision, evidence gate, stop rule, source doc, and the next GUI action.

Use `Run Selected` to jump from a radar row into Routes, Core, Kit Gate, Shot Bench, Control Bench, XP Gap, Assets, Attach Log, Dashboard, or Goals.

Validation expectation:

- Industry Radar is a current-state/SOP map, not evidence.
- API/SDK compatibility can be `ready` while HID, receiver, XP hardware, or real iPhone control remain `warn` or `fail`.
- XP hardware, 4.4 firmware, wired projection, auto-binding, Windows receiver, and hardware decode claims remain blocked until the exact side-by-side or receiver evidence exists.

### Route Procurement SOP

The `Procure` button in `Live Probe` opens the route procurement SOP board and can export `evidence/<run_id>_<stage>_route_procurement_sop.md`.

Rows include:

- mainstream route lock;
- receiver and capture procurement;
- HID hardware procurement;
- XP hardware parity purchase;
- iPhone fixture and iOS matrix;
- bench materials and replacement policy;
- source refresh and package hygiene;
- claim, scale, and spend stop line.

Each row shows current local gate, industry signal, supplier questions, local SOP, required evidence, stop rule, source doc, and the next GUI action.

Use `Run Selected` to jump from a procurement row into Routes, Rx Score, Control Bench, XP Lab, iOS SOP, Bench, Src Refresh, or Goals.

Validation expectation:

- Procure is a route and buying SOP, not evidence.
- A `ready` procurement row means the lane is reviewable, not that real iPhone control works.
- XP parity purchase remains blocked without legal side-by-side XP hardware artifacts.
- Source/package rows can guide procurement, but package install or public docs cannot prove receiver, HID, or iPhone behavior.

### Mainstream Route Matrix

The `Routes` button in `Live Probe` opens the industry route decision matrix and can export `evidence/<run_id>_<stage>_mainstream_routes.md`.

Rows map route choices to P1 gates:

- XP-style black-box route: receiver + screenshot + USB HID + local kernel API;
- UxPlay AirPlay receiver;
- Windows receiver/window capture;
- wired projection or vendor SDK;
- capture-card visual lane;
- CH9329/general USB HID;
- XP dedicated hardware;
- WDA/Appium/XCUITest as non-mainline;
- MDM/Configurator/Shortcuts as auxiliary setup tooling.

Use `Run Selected` to jump from a route row into the existing GUI action, such as Wizard, Doctor, Route Edit, Bench, Shot Bench, Control Bench, Knowledge, or Kit Gate.

Validation expectation:

- Routes is a decision matrix, not evidence.
- One run should pick one receiver lane and one HID lane; unresolved route rows should block P1 rather than be hidden.
- CH9329 proof can support generic P1 exploration, but XP dedicated hardware, 4.4 firmware, and auto-binding parity require legal side-by-side evidence.
- WDA/Appium and MDM/Shortcuts are auxiliary/non-mainline for this XP-style product goal and cannot replace receiver + screenshot + HID proof.

### Verification Walkthrough

The `Verify` button in `Live Probe` opens the step-by-step verification walkthrough and can export `evidence/<run_id>_<stage>_verification_walkthrough.md`.

Rows cover:

- P0 offline self-check commands;
- run identity and device scope;
- Route Decision validation;
- preflight Doctor;
- receiver and screenshot proof;
- HID click/swipe/text proof with Manual observation;
- Acceptance and Readiness;
- P2 single-device stability;
- P3 four-device group pilot;
- XP parity review;
- review handoff pack.

Each row shows current state, command or GUI path, expected result, evidence to keep, stop rule, and a GUI jump target.

Validation expectation:

- Verify is a step-by-step test guide, not evidence.
- A later pass row cannot bypass an earlier fail row.
- Offline tests, API success, GUI exports, and public XP claims remain supporting material only.
- Real iPhone control still requires screenshot quality, manual observations, JSONL evidence, Acceptance, and Readiness.

### XP Architecture Map

The `XP Arch` button in `Live Probe` opens the architecture map and can export `evidence/<run_id>_<stage>_xp_architecture.md`.

Rows cover:

- product boundary;
- dedicated hardware and USB/HID;
- projection and receiver;
- capture, vision, and OCR;
- Kernel/API service;
- Python helper and script runtime;
- Console/GUI operator layer;
- evidence and readiness;
- group control and ops.

Validation expectation:

- XP Arch is an implementation-principle map, not evidence.
- API/SDK and GUI rows can be locally ready while real iPhone control remains blocked.
- XP hardware, 4.4 firmware, wired projection, auto-binding, Windows receiver, and hardware decode stay unverified until side-by-side field artifacts exist.

### XP Core Function Matrix

The `Core` button in `Live Probe` opens the XP core function coverage matrix and can export `evidence/<run_id>_<stage>_xp_core_functions.md`.

Rows include:

- XP-style product route boundary;
- Kernel/API and WebSocket;
- Python SDK/helper;
- device/group ledger;
- receiver/capture route and screenshot acquisition;
- USB/HID control, coordinate calibration, and mouse/keyboard input;
- vision/image/color and OCR/text recognition;
- script/batch runtime;
- GUI console and SOP surface;
- config/user/shortcut compatibility;
- observability/callback/logs;
- commercial/cloud ops.

Each row shows local support, current evidence gate, required evidence, XP Gap status, source doc, and the next GUI action.

Validation expectation:

- Core is a coverage matrix, not evidence.
- API/SDK rows can be `ready` while receiver/HID/manual evidence is still missing.
- Config/User/Shortcut rows are local compatibility scaffolding, not XP cloud account or shortcut parity.
- HID, receiver, screenshot, calibration and input rows need JSONL evidence, artifacts, Acceptance, Readiness and manual real-iPhone observation before promotion.

### XP API Coverage Board

The `API Cov` button in `Live Probe` opens the XP API/SDK coverage board and can export `evidence/<run_id>_<stage>_xp_api_coverage.md`.

Rows include API envelope, device registry, AirPlay/receiver/capture, USB/HID binding, mouse click/swipe, keyboard text/key input, picture/image/color, OCR/find text, group/batch, config/user/shortcut, callback/event, logs/triage, and cloud/account ops.

Validation expectation:

- API Cov is a compatibility and R&D planning board, not evidence.
- Local helper tests close only P0 API shape.
- Receiver, HID, mouse, keyboard, screenshot, vision and group rows still need same-run field evidence before promotion.
- Config/User/Shortcut rows are `scaffolding_only`; Cloud/Ops rows are `backlog_only`.

### Pitfall Library

The `Pitfalls` button in `Live Probe` opens the operator pitfall library and can export `evidence/<run_id>_<stage>_pitfall_library.md`.

Rows map known iOS group-control failure patterns into execution work:

- receiver discovery and AirPlay naming;
- black screen, stale frame, or wrong capture window;
- HID command success without visible iPhone response;
- coordinate drift, orientation, and swipe direction errors;
- template, color, OCR, or text recognition drift;
- group runs hiding per-device failure;
- latency, reconnect, resource, or long-run instability;
- business page state changes underneath the script;
- claim boundary and XP hardware parity mistakes.

Use `Run Selected` to jump from a pitfall row into the existing GUI action, such as Doctor, Shot Bench, Control Bench, P1 Trial, Assets, Matrix, Dashboard, Scenario Library, Goals, XP Gap, Triage, or Attach Log.

Validation expectation:

- Pitfalls is a SOP risk library, not evidence.
- Existing failed evidence should lift the matching pitfall rows to `fail` and keep failure categories visible.
- A pitfall row cannot be closed by export alone; it needs a probe, artifact, manual observation, Acceptance/Readiness result, or an Issue Triage entry.

### XP Public Source Ledger

The `Sources` button in `Live Probe` opens the public-source audit ledger and can export `evidence/<run_id>_<stage>_xp_public_sources.md`.

It maps current public XP signals into verification work:

- official product model: dedicated hardware, AirPlay, no iPhone app, kernel server, console, HTTP/WebSocket API, OpenCV/OCR;
- current public device/iOS support claims;
- Python XP helper domains;
- `/api` + `fun` + WebSocket protocol shape;
- API domain categories;
- XP new-version iteration claims: Windows, 4.4 firmware, wired projection, auto-binding, hardware decode, separate windows, logs, groups, subaccounts;
- project claim boundary.

Use `Run Selected` to jump from a source row into Wizard, Bench, XP Gap, or Goals.

Validation expectation:

- Sources is public intelligence, not evidence.
- Public compatibility claims stay `warn` until the same device/iOS class is covered by our own matrix.
- XP hardware, 4.4 firmware, wired projection, Windows receiver, hardware decode, and auto-binding stay unverified until hardware-bench evidence exists.

### XP Source Refresh Board

The `Src Refresh` button in `Live Probe` opens the source refresh board and can export `evidence/<run_id>_<stage>_xp_source_refresh.md`.

Rows cover homepage/product wording, XP API, XP help/iteration pages, PyPI package namespace/version drift, Apple/iOS pointer setup, industry route assumptions, source-to-SOP landing, and source-only claim boundaries.

Validation expectation:

- Source Refresh is a manual refresh checklist, not a crawler.
- Source freshness does not write JSONL evidence.
- A refreshed public source or package version does not prove real iPhone response, iOS perfect control, compatibility coverage, or XP parity.

### XP Iteration Radar

The `Iter Radar` button in `Live Probe` opens the XP iteration radar and can export `evidence/<run_id>_<stage>_xp_iteration_radar.md`.

It turns the XP iteration/pitfall summary into execution rows:

- P1 black-box control;
- Kernel/API split;
- receiver/capture evolution;
- XP hardware, 4.4 firmware, wired projection, and auto-binding;
- vision/script productization;
- ops and group scaling;
- claim boundary.

Each row shows public signal, current local gap, R&D action, SOP/test path, stop rule, source, and the next GUI action.

Validation expectation:

- Iteration Radar is R&D prioritization, not evidence.
- A public iteration lesson can be `pass` as a documented learning while the corresponding hardware, receiver, or control capability remains `warn` or `fail`.
- Exporting the radar does not write JSONL evidence and does not prove XP parity, broad compatibility, or perfect iOS control.

### XP Iteration Timeline

The `XP Timeline` button in `Live Probe` opens the XP iteration timeline and can export `evidence/<run_id>_<stage>_xp_iteration_timeline.md`.

It turns public XP evolution signals into chronological product-review rows:

- black-box product model;
- Kernel/Console/API split;
- receiver projection productization;
- firmware, wired projection, and hardware binding;
- vision, script, and asset productization;
- ops logs, group control, and scale boundaries;
- source freshness and claim governance.

Each row shows phase, public signal, inferred lesson, pitfall, R&D action, SOP gate, required evidence, stop rule, source, and next GUI action.

Validation expectation:

- XP Timeline is industry/product intelligence, not JSONL evidence.
- Offline rows must not close receiver, HID, XP hardware, firmware, wired projection, scale, or parity claims.
- Same-run real iPhone evidence, Acceptance, Readiness, logs, and legally acquired XP side-by-side evidence are still required before any XP parity wording.

### XP Iteration Drill Board

The `XP Drill` button in `Live Probe` opens the XP iteration drill board and can export `evidence/<run_id>_<stage>_xp_iteration_drill.md`.

It turns XP iteration/help/package details into validation rows:

- Windows service/API/Console split;
- iOS settings and mouse parameter profile;
- receiver projection, binding, hard decode, and screenshot stability;
- XP hardware, 4.4 firmware, wired projection, and HID release behavior;
- SDK/package namespace drift and dependency adoption;
- restart, logs, recovery, and rerun categories;
- P3/P4 multi-device projection and performance isolation;
- claim boundary before demo or handoff.

Each row shows current local gap, drill, required evidence, failure category, stop rule, source, and the next GUI action.

Validation expectation:

- XP Drill is a checklist, not JSONL evidence.
- It does not browse automatically, install packages, connect receiver/HID, prove real iPhone response, or prove XP parity.
- Same-run evidence, Acceptance, Readiness, logs, and exact device/iOS coverage still decide whether a claim can move.

### XP Roadmap

The `Roadmap` button in `Live Probe` opens the XP R&D closure roadmap and can export `evidence/<run_id>_<stage>_xp_roadmap.md`.

It turns public XP signals, industry SOP, local implementation, evidence gates, and next actions into rows:

- P0 offline/API base;
- P1 route and hardware bench lock;
- P1 receiver/capture proof;
- P1 HID click/swipe/type proof;
- P1 calibration and input matrix;
- XP hardware/wired/4.4 parity lane;
- P2 vision/script replay;
- P2 observability/recovery;
- P3/P4 scale and ops;
- claim, SOP, and docs closure.

Validation expectation:

- Roadmap is an R&D closure plan, not JSONL evidence.
- `real_ios_verified=False` prevents HID, calibration, input, and claim closure rows from becoming pass.
- XP dedicated hardware, wired projection, 4.4 firmware, auto-binding, and hard decode need separate side-by-side evidence even when generic HID or local API rows are ready.

### Device/iOS Compatibility Matrix

The `Compat` button in `Live Probe` opens the local compatibility coverage matrix and can export `evidence/<run_id>_<stage>_device_ios_matrix.md`.

It groups current devices and JSONL evidence by:

- iPhone model;
- iOS version;
- selected devices;
- event count and failure count;
- pass/pending/fail device coverage;
- local stage claim such as `covered_for_p1` or `not_covered`;
- remaining evidence gaps.

Validation expectation:

- Compat is local coverage, not a public compatibility claim.
- A row can say `covered_for_p1` only for the exact model/iOS combination represented in local evidence.
- Unknown model/iOS rows must stay blocked until component metadata records real model and iOS version.
- A clean iPhone 13/iOS 17.7 row does not imply iPhone 16/iOS 18.x, iOS 26.x, XP hardware, wired projection, or Windows receiver support.

### Goal Gate

The `Goals` button in `Live Probe` opens the acceptance-goal gate and can export `evidence/<run_id>_<stage>_gui_goal_gate.md`.

It maps the four user acceptance goals to proof:

- iOS perfect control;
- iOS group-control SOP and issue log;
- iMouse XP core functions and docs;
- XP iteration lessons and pitfalls.

Each row shows current evidence, required evidence, next GUI action, and a concrete test method. Use `Run Selected` to jump into Proof Map, Claim Scope, P1 Trial, Runbook, XP Gap, Knowledge, or Triage.

Validation expectation:

- Goal Gate is a target-to-evidence map, not evidence.
- The iOS control row cannot pass without real-device evidence, Proof Map closure, Claim Scope pass wording, Acceptance PASS, Readiness PASS, and no unexplained fail events.
- Docs/SOP rows can be ready while receiver, HID, XP hardware, or real iPhone control remain unverified.

### Field Kit Gate

The `Kit Gate` button in `Live Probe` opens the procurement and pre-run field gate and can export `evidence/<run_id>_<stage>_field_kit_gate.md`.

It is deliberately earlier than `Bench`: Kit Gate decides whether the operator may open P1 today, while Hardware Bench tells the operator how to test the already prepared bench.

Rows include:

- procurement and SOP source docs;
- run identity and selected device scope;
- receiver procurement and capture route;
- HID procurement, firmware, serial binding, and hardware scan status;
- iPhone model/iOS/orientation/AssistiveTouch/pointer settings;
- Hub, cable, network, and operator ledger;
- evidence plan and artifact ledger;
- Open P1 stop line from Route Decision and Doctor;
- XP hardware comparison question.

Validation expectation:

- Kit Gate is not JSONL evidence.
- `Open P1 stop line` must be `pass` before real HID actions.
- CH9329 can be enough for generic P1 exploration, but it must keep XP dedicated hardware/4.4/auto-binding parity as `warn` until a legal side-by-side comparison exists.

### iOS Field Settings SOP

The `iOS SOP` button in `Live Probe` opens the real-iPhone settings checklist and can export `evidence/<run_id>_<stage>_ios_field_sop.md`.

It sits between `Kit Gate` and `Bench`: Kit Gate asks whether the field kit may open P1, iOS SOP checks the phone and desk settings, and Bench then runs the receiver/HID hardware tests.

Rows include:

- device identity, iPhone model, iOS version, orientation, and selected GUI device id;
- AssistiveTouch, pointer profile, rotation lock, AssistiveTouch menu, Full Keyboard Access, Trackpad & Mouse, mouse parameter profile, and QR scan policy status;
- Auto-Lock, brightness, Focus/notification policy, and screen-interruption risks;
- network, AirPlay name, receiver identity, capture method, and window binding;
- Hub, cable, power, HID serial/firmware, and operator ledger;
- baseline screenshot, P1 Trial, Control Bench, Acceptance, and manual-observation artifacts;
- settings replay, operator handoff, and claim boundary.

Use `Run Selected` to jump from a settings row into Route Edit, Shot Bench, P1 Trial, Control Bench, Bench, Start Pack, or Goals.

Validation expectation:

- iOS SOP is a field settings checklist, not JSONL evidence.
- Complete settings can make the desk ready for P1, but do not prove click, swipe, text input, XP hardware parity, or perfect iOS control.
- `real_ios_verified=False` must stay visible until screenshots, logs, manual observation, Acceptance, and Readiness all support the claim.

### Hardware Bench

The `Bench` button in `Live Probe` opens the hardware bench checklist and can export `evidence/<run_id>_<stage>_hardware_bench.md`.

It turns the hardware test documents into GUI rows:

- bench ledger and physical labels;
- receiver/capture route;
- HID binding and real iPhone response;
- iPhone settings;
- Hub/cable/network isolation;
- screenshot and control evidence;
- XP dedicated hardware comparison;
- callback/log triage.

Each row gives current state, required evidence, test method, next action, and a GUI jump target.

Validation expectation:

- Hardware Bench is a checklist and review index, not evidence.
- A clean bench row only means the operator knows what to test next; real iPhone control still requires screenshot quality and manual observation evidence.
- XP dedicated hardware stays pending until legally acquired and compared with CH9329 or the chosen HID route on the same iPhone/page.

### Capture Quality Bench

The `Shot Bench` button in `Live Probe` runs repeated screenshot quality probes for the selected device and exports `evidence/<run_id>_<stage>_capture_bench.md`.

The GUI saves each returned frame under `evidence/<run_id>_artifacts/` and records one bench event into `evidence/<run_id>.jsonl`.

It checks:

- missing or invalid screenshot base64;
- invalid image bytes;
- too-small frames;
- black, white, blank, or low-texture frames;
- screenshot dimension drift;
- artifact save errors.

Validation expectation:

- Shot Bench is receiver/capture evidence, not HID evidence.
- The default GUI run is a 10-sample smoke bench; before scaling toward XP-level field confidence, run a 100-screenshot stability pass on the same receiver/iPhone route.
- A passing Shot Bench does not prove click, swipe, text input, business flow, or full iOS control.

### Control Response Bench

The `Control Bench` button in `Live Probe` opens the control-response audit and exports `evidence/<run_id>_<stage>_control_bench.md`.

It reads the current JSONL evidence and creates one row for each minimum P1 control lane:

- HID click;
- HID swipe;
- keyboard/text input.

Status model:

- `pending`: no usable command or manual event exists yet.
- `ready`: a command event exists, but the operator has not recorded a real-iPhone Manual pass.
- `pass`: the lane has at least one Manual pass observation.
- `fail`: either a command fail or Manual fail exists; category and artifact context must stay attached before rerun.

Validation expectation:

- API/HID command success is only software-chain evidence.
- Real iOS control requires the operator to see the iPhone respond and record Manual pass for click, swipe, and text input.
- Control Bench is an audit surface; exporting it does not write JSONL evidence and does not prove XP-level parity.

### Field Evidence Wizard

The `Wizard` button in `Live Probe` opens the ordered field evidence sequence and can export `evidence/<run_id>_<stage>_field_wizard.md`.

It turns the current GUI state into a strict run order:

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

Use `Run Selected` to jump from the selected step into the existing GUI action: Record Metadata, Route Edit, Doctor, Screenshot, P1 Trial, Runbook, Attach Log, Triage, Load Probe Script, Run Queue, Acceptance, Gap, Assets, Readiness, or Pack.

Validation expectation:

- Field Evidence Wizard is an execution sequence, not evidence.
- It keeps `real_ios_verified=False` visible as `warn`; a green route, doctor, and acceptance report still do not prove perfect iOS control without readiness claims and manual real-iPhone observations.
- When any row is fail/pending/warn, the operator should stop and attach the smallest useful evidence before rerunning.

### Field Evidence Runner

The `Runner` button in `Live Probe` opens the same-run field evidence runner and can export `evidence/<run_id>_<stage>_field_runner.md`.

It turns the current run into a row-by-row execution board:

- run scope and evidence path;
- Route Decision validation command;
- route-aware Doctor command;
- screenshot quality and Shot Bench artifact status;
- separate Manual gates for HID click, HID swipe, and keyboard input;
- Acceptance and Acceptance Gap commands;
- Readiness command;
- Evidence Pack handoff;
- final claim boundary.

Use `Run Selected` to jump from a row into the matching GUI action. Use `Copy Command` to copy the exact PowerShell command for route validation, Doctor, Acceptance, Gap, Readiness, or real script replay.

Validation expectation:

- Field Evidence Runner is a checklist and command surface, not evidence.
- It intentionally requires click, swipe, and text to pass as separate Manual lanes; one generic Manual pass is not enough for the final claim row.
- It cannot prove real iOS control without same-run JSONL evidence, screenshot artifacts, manual observations, Acceptance PASS, Readiness PASS, and exact device/iOS scope.

### First Run Packet

The `Start Pack` button in `Live Probe` opens the first real-device run packet and can export `evidence/<run_id>_<stage>_first_run_packet.md`.

It combines the current GUI state into one operator-facing checklist:

- run identity and device scope;
- Industry Current Snapshot GUI board, Route Procurement SOP, static industry snapshot doc, XP public sources, step-by-step verification method, core function coverage, route matrix, receiver scorecard/bootstrap/setup split, pitfall library, and goal boundary;
- Device/iOS compatibility coverage;
- Rx Score, Rx Bootstrap, Rx Setup, Route, Doctor, Kit Gate, iOS SOP, Receiver Gate, and hardware bench status;
- ordered Wizard rows;
- Runner command/evidence gate status;
- P1 real-control proof rows;
- repeatable script or queue path;
- Evidence Pack export coverage;
- Acceptance, Readiness, and handoff boundary;
- Local command verification;
- exact local PowerShell commands for second-person reproduction.

Use `Run Selected` to jump from a packet row into the existing GUI action: Prepare, Sources, Industry, Procure, Roadmap, Verify, Local, Core, Routes, Rx Score, Rx Bootstrap, Rx Setup, Receiver, Pitfalls, Goals, Compat, Kit Gate, iOS SOP, Bench, Wizard, Runner, Ctrl Ledger, P1 Trial, Runbook, Load Probe Script, Run Queue, Pack, Acceptance, Gap, or Readiness.

Validation expectation:

- First Run Packet is an operator guide, not evidence.
- Rx Bootstrap rows only prepare a receiver route-decision draft; they never prove P1 or real iPhone response.
- It keeps `real_ios_verified=False` visible when gates look clean but the readiness claim is still not proven.
- A generated packet should be handed to the field operator before the first real HID action, then attached to the review pack after the run.

### SOP Board

The `SOP` button in `Live Probe` opens an eight-step execution board for the current stage.
The `SOP MD` button exports `evidence/<run_id>_<stage>_gui_sop_board.md`.
Select a row and click `Run Selected` to run that row's primary GUI command.

Rows are computed from current GUI state:

- Device scope.
- Route decision.
- Preflight doctor.
- Capture/control evidence.
- Probe script or command queue.
- Vision assets.
- Acceptance gate.
- Promotion review.

Primary command mapping:

- Device scope -> `Record Metadata`.
- Route decision -> `Edit Route`.
- Preflight doctor -> `Run Doctor`.
- Capture/control evidence -> `Screenshot`.
- Probe script -> `Load Probe Script`, or `Run Queue` when a command queue exists.
- Vision assets -> `Open Assets`.
- Acceptance gate -> `Run Acceptance`.
- Promotion review -> `Run Readiness`, or `Export Session` after readiness already passed.

Validation expectation:

- Offline runs must keep blockers visible and must not mark real iOS control as verified.
- `Run Selected` only launches the mapped GUI operation; it does not bypass route/doctor/acceptance/readiness gates.
- A queued command can make the Probe script row `ready`, but it is not a pass until a dry-run or real-run scenario summary exists.
- A SOP Board export is only a field guide and review index; promotion still depends on JSONL evidence, acceptance, readiness, and manual observation.

### Route Decision Form Feedback

`Route Decision Editor` now highlights fields with GUI-detected issues after `Scan Issues` or save:

- `missing`: fill the real bench value.
- `placeholder`: replace template text with real component metadata.
- `not allowed`: set `Allow P1 real run` only when the route is actually ready.
- `open blocker`: resolve the blocker or keep the run stopped.

### Local Verification Commands

Run these before field use:

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m unittest tests.test_gui_helpers
.\.venv\Scripts\python -m unittest tests.test_receiver_provider tests.test_route_decision
.\.venv\Scripts\python -m compileall imouse tests
```

Latest full local run: `332 tests OK`.

Do not use the system Python for this repo unless dependencies such as `pyserial`, OpenCV, FastAPI, and Pillow are installed there.
