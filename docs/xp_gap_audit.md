# XP Gap Audit 使用说明

更新时间：2026-06-08

`imouse.xp_gap_audit` 用来把 iMouse XP 公开核心能力拆成机器可读的研发差距表。它回答的是：

- 当前 Python GUI 原型已经覆盖了哪些 XP 能力域。
- 哪些只是离线能力或原型能力。
- 哪些必须补真实 iPhone、receiver、HID、截图、人工观察或 metrics evidence。
- 当前阶段最硬的 blocker 是什么。

它不是 evidence，不会写 JSONL，也不能证明 iPhone 已经响应。

## 命令行

无实机 evidence 时：

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.xp_gap_audit --target p1 --run-id p1_dev1_YYYYMMDD --markdown evidence\p1_dev1_YYYYMMDD_p1_xp_gap_audit.md
```

已有 evidence 后：

```powershell
.\.venv\Scripts\python -m imouse.xp_gap_audit --target p1 --run-id p1_dev1_YYYYMMDD --evidence evidence\p1_dev1_YYYYMMDD.jsonl --markdown evidence\p1_dev1_YYYYMMDD_p1_xp_gap_audit.md
```

如果只想看 JSON：

```powershell
.\.venv\Scripts\python -m imouse.xp_gap_audit --target p1 --run-id p1_dev1_YYYYMMDD --json
```

当目标阶段仍有硬阻断时，CLI 会返回非 0；这用于提醒外场不要把审计报告当成通过证明。

## GUI 入口

启动 GUI：

```powershell
.\.venv\Scripts\python -m imouse.gui
```

在底部 `Live Probe` 面板点击 `XP Gap`，会生成：

```text
evidence/<run_id>_<stage>_xp_gap_audit.md
```

报告会列出：

- `Kernel/API`
- `Python SDK`
- `Device/Group`
- `Component Ledger`
- `Receiver/Capture`
- `USB/HID`
- `Coordinate Calibration`
- `Mouse/Keyboard`
- `Vision/Image/Color`
- `OCR`
- `Script Runtime`
- `GUI Console`
- `Observability`
- `Commercial/Ops`

每一行都有 `priority`、`status`、`field_gate`、`current_state`、`gap`、`required_evidence` 和 `next_action`。

## 状态解释

- `pass`：该能力域对应的当前阶段证据门已经满足。
- `partial`：已有离线/原型能力，但还没达到 XP 商业级能力。
- `blocked`：当前阶段需要的证据不满足，必须先补。
- `not_started`：当前阶段或后续阶段需要的 evidence 尚未开始记录。

`partial` 不等于失败，也不等于完成。它表示已有研发基础，但仍要继续对标 XP 的产品化体验。

## P1 重点看什么

P1 首轮重点看这些域：

- `Component Ledger`：是否每台设备都有 receiver/capture/HID/iPhone/iOS 台账。
- `Receiver/Capture`：是否有非黑屏真实截图。
- `USB/HID`：是否有真实 iPhone 点击/滑动/输入人工观察。
- `Coordinate Calibration`：是否完成五点校准和误差记录。
- `Observability`：失败是否有 doctor、review、metrics、附件和分类。

P1 如果这些域还是 `blocked` 或 `not_started`，就不能进入 P2/P3。

## 边界

- XP Gap Audit 不会启动 receiver。
- XP Gap Audit 不会连接 HID。
- XP Gap Audit 不会生成真实截图。
- XP Gap Audit 不会替代 `Acceptance` 和 `Readiness`。
- XP Gap Audit 不会把 `partial` 当成“XP 对标完成”。

真正通过仍以 `evidence/<run_id>.jsonl`、截图附件、人工观察、Acceptance 和 Readiness 为准。
