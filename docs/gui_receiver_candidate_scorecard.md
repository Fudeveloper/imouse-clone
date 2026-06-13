# GUI Receiver Candidate Scorecard

`Rx Score` 是 Python GUI 中的接收器路由选择记分卡。它在操作者为现场运行锁定接收器通道之前比较 `uxplay`、`windows_receiver`、`wired` 和 `capture_card`。

使用 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

在以下情况下，在 `Coach` 之后、`Rx Bootstrap`/`Rx Setup` 之前打开 `Rx Score`：

- `uxplay` 缺失或不稳定。
- 有商业 Windows 接收器可用但需要授权/窗口绑定审查。
- 有线路由或采集卡可能对首次真实 iPhone 证明更稳定。
- 团队需要书面理由说明为什么选择了一个接收器路由。

记分卡读取当前 GUI 状态和缓存报告：

- Route Decision JSON 和路由验证报告。
- Doctor 报告，特别是 `binary:uxplay` 和 `receiver_provider`。
- 有证据时的 Acceptance 截图/Manual 行。
- Readiness 预览或最终 Readiness 报告。
- 证据摘要计数和失败计数。

## 列

- `Candidate`：正在比较的接收器通道。
- `Status`：`fail`、`pending`、`warn`、`ready` 或 `pass`。
- `Recommendation`：`recommended`、`blocked`、`route-needed`、`selected-needs-proof` 或 `backup`。
- `Selected`：当前 Route Decision 是否选择了此通道。
- `Score`：可解释的评分，来自来源、路由、安装、绑定、截图、日志、Python 集成、授权/产品风险和 XP 对标程度。
- `Current signal`：当前路由/提供者/Doctor/截图/Manual/证据状态。
- `Strengths`：为什么该候选方案对当前运行有吸引力。
- `Gaps`：什么仍然阻止或削弱该候选方案。
- `Next action`：下一个 GUI 步骤。
- `Stop rule`：何时停止并避免混合接收器证据。

## 路由选择 SOP

1. 点击 `Rx Score`。
2. 从任何 `fail` 行开始，特别是所选路由的失败。
3. 如果没有路由文件，点击 `Edit Route` 并填写真实接收器/HID/iPhone 值。
4. 如果 `UxPlay open receiver` 被 `binary:uxplay=fail` 阻止，要么安装 UxPlay，要么在新的 run_id 下选择有效的备选路由。
5. 如果推荐 `Windows AirPlay receiver`，点击 `Rx Bootstrap` 并在设置之前填写版本/授权、路径、启动命令、AirPlay 名称、采集方法和窗口绑定。
6. 如果推荐 `wired` 或 `capture_card`，点击 `Rx Bootstrap`，标记线缆/卡/驱动/输入，并在 HID 之前证明自动帧采集。
7. 为所选路由点击 `Rx Setup`。
8. 点击 `Rx Evidence` 以组织接收器/采集证明命令、工件和停止线。
9. 使用相同的 Route Decision 路径运行 Doctor。
10. 在 P1 Trial 之前运行 Screenshot/Shot Bench。
11. 在 JSONL 证据存在后使用 Acceptance 和 Readiness。

## 边界

- `Rx Score` 不写入 JSONL 证据。
- `Rx Score` 不启动或安装接收器。
- `Rx Bootstrap` 可能为备选接收器创建 Route Decision 草案，但仍保持 P1 阻塞。
- `recommended` 行不是真实 iPhone 通过。
- `ready` 行不是 iOS 完美控制。
- XP 对标仍需要并排能力证据、API 行为、接收器/采集/HID 证明、SOP 覆盖率和现场稳定性证据。

导出路径：

```text
evidence/<run_id>_<stage>_receiver_candidate_scorecard.md
```
