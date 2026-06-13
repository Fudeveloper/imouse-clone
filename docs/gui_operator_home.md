# GUI Operator Home

更新时间：2026-06-09

`Home` 是 Python GUI 中面向操作者的工作流映射看板。它将拥挤的 Live Probe 按钮分组为一个有序看板：

1. 操作者信息录入。
2. 知识和验收边界。
3. 路由、套件和 iPhone 设置。
4. 本地可复现性。
5. 接收器截图证明。
6. HID 点击、滑动和文字证明。
7. 可重复脚本路径。
8. 验收证明映射。
9. 声明范围和交付措辞。
10. XP 核心、API 覆盖率和事件契约。
11. 问题账本和重跑路径。
12. Evidence Pack、验收和交付。

它是一个导航和审计看板。它不写入 JSONL 证据，也不证明真实 iPhone 响应。

## GUI 路径

启动 GUI：

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

在底部 `Live Probe` 区域，使用紧凑的工作流行：

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

点击 `Home` 打开看板。选择第一个 `fail`、`pending` 或 `warn` 行，然后点击 `Run Selected` 跳转到主要的 GUI 操作。创建工件或记录证据后，点击 `Refresh`。

## 导出

`Export` 按钮写入：

```text
evidence/<run_id>_<stage>_operator_home.md
```

导出内容作为 `GUI Operator Home` 包含在 Evidence Pack 中。

## 逐步使用

1. 设置 `Evidence` 运行 ID 并选择物理设备行。
2. 点击 `Prepare`。
3. 点击 `Home`。
4. 点击 `Action Map` 并在更改硬件范围之前解决第一个来源衍生的 SOP 门控。
5. 点击 `Coach` 并跟随第一个未通过的 P1 测试行。
6. 解决第一个未通过的 Home 行。
7. 当 `Route, kit, and iPhone settings` 被阻止时，填写 Route Decision，运行 Doctor，打开 Receiver、Kit Gate 和 iOS SOP。
8. 当 `Local reproducibility` 被阻止时，打开 `Local` 并重放列出的 PowerShell 命令。
9. 当 `Receiver screenshot proof` 被阻止时，运行 Screenshot、Shot Bench、校准、Wizard 和 Runner。
10. 当 `HID click, swipe, and text proof` 被阻止时，在观察真实 iPhone 的同时使用 Ctrl Ledger、P1 Trial 和 Control Bench，然后记录通道特定的 Manual 通过/失败。
11. 当 `Repeatable script path` 被阻止时，在禁用 dry-run 之前打开 Script Cov、Scenario Library、Dry Run、Runner 和 Real-run Guard。
12. 当 `Acceptance proof map` 被阻止时，在交付前打开 Proof Map 并跟随第一个失败的证据门控。
13. 当 `Claim scope and handoff wording` 被阻止时，打开 Claim Scope 并移除任何将 P0/GUI/API/源码进展表述为真实 iPhone 控制、群控、XP 硬件对标或广泛兼容性的措辞。
14. 当 `XP core, API coverage, and event contract` 被阻止时，在进行 API/SDK 对标声明之前打开 Core、API Cov、Events、Callback、Attach Log 和 XP Gap。
15. 当存在失败时，在更改脚本或扩展设备之前打开 Problems、Triage、Rerun、Recovery、Timeline 和 Review。
16. 以 Pack、Dashboard、Acceptance、Gap（如需要）、Readiness 和 Session 结束。

## 本地验证

在导出 Home 之后、进行真实 P1 运行之前使用以下命令：

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.main --check
.\.venv\Scripts\python -m imouse.doctor --json
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --json
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id <run_id>
.\.venv\Scripts\python -m imouse.readiness --target <stage> --evidence evidence\<run_id>.jsonl
```

当前原型上的预期离线结果：单元测试和 compileall 可以通过，但当 `uxplay`、真实接收器/HID 和真实证据缺失时，`main --check`、Doctor 和 Readiness 仍可能失败或发出警告。

## 声明边界

不得将 Home、Procure、Pack、Dashboard、Start Pack、Runner、Ctrl Ledger 导出、API Cov、Script Cov、Proof Map、Claim Scope、Events、Core、Roadmap 或 XP Gap 用作真实控制证明。

真实 iOS 控制需要对相同的 `run_id` 满足以下所有条件：

- 当前截图质量证据；
- 真实 iPhone 上可见的点击、滑动释放和文字输入；
- 包含设备 ID、分类、备注和工件（如需要）的 Manual 通过/失败记录；
- Acceptance PASS；
- Readiness PASS 且 `real_ios_control_verified=true`；
- 无未解决的失败事件，或有文档记录的 Rerun/Recovery 决策。

XP 对标声明需要单独的硬件/接收器比较。CH9329 或原型接收器的通过不能证明 iMouse XP 专用硬件、固件 4.4、有线投屏、自动绑定、授权或广泛兼容性。
