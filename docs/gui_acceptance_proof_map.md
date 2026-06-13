# GUI Acceptance Proof Map

`Proof Map` 是将每个 Acceptance 和 Readiness 门控与可以关闭它的具体现场证据、GUI 操作、工件、命令和停止规则关联起来的 GUI 看板。

在 `Script Cov` 之后、`Claim Scope` 之前使用它。面向需要了解哪些缺失证据阻止了 P1/P2/P3/P4，以及下一步该点击哪个 GUI 按钮的操作者。

## GUI 流程

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

`Proof Map` 导出：

```text
evidence/<run_id>_<stage>_proof_map.md
```

## 映射内容

| 证明行 | 关闭项 | 所需证据 |
|---|---|---|
| 运行范围 | 现场证据起点 | 相同 run_id、已选物理设备、阶段目标、JSONL 路径。 |
| 路由和 Doctor | 路由/Doctor 就绪 | Route Decision、组件元数据、路由感知的 Doctor 报告。 |
| 证据存在 | Acceptance `evidence_exists` | 包含现场事件的当前 JSONL。 |
| 无失败事件 | Acceptance `no_fail_events` | 零未解决失败事件的全新运行。 |
| 设备可追溯性 | Acceptance `device_traceability` | 设备 ID 与 P1/P2/P3/P4 阶段计数匹配。 |
| 组件可追溯性 | Acceptance `component_traceability` | 接收器、采集、HID、iPhone 身份、iOS 版本，无占位符。 |
| 截图质量 | Acceptance `screenshot_quality` | 当前、正确绑定、非空白的截图和工件。 |
| 人工观察 | Acceptance `manual_observation` | 操作者观察到真实 iPhone 响应。 |
| 通道分离 | 本地 P1 控制边界 | HID 点击、HID 滑动和键盘输入分别有独立的 Manual 通过行。 |
| 指标 | P2/P3/P4 稳定性 | 指标样本、重复截图、日志、恢复记录。 |
| Acceptance 门控 | 阶段验收 | Acceptance PASS，失败时导出 Gap。 |
| Readiness 门控 | 阶段就绪 | Readiness PASS，且 Doctor/证据/验收阻塞项已关闭。 |
| 声明边界 | 交付措辞 | 相同运行支持的精确设备/iOS/接收器/HID 范围。 |

## 现场规则

`Proof Map` 不写入证据，也不证明真实 iPhone 响应。它只告诉操作者缺失的证明应该放在哪里。

在 `Proof Map` 之后，在演示或交付之前打开 `Claim Scope`。`Claim Scope` 将当前的证明状态转换为允许和禁止的措辞，但它也不写入 JSONL 证据或证明真实 iPhone 响应。

除非相同的 `run_id` 具有当前截图质量、通道分离的 Manual 点击/滑动/文字观察、无未解决的失败事件、Acceptance PASS、Readiness PASS 以及精确的设备/iOS/接收器/HID 范围，否则不得声明 iOS 完美控制、XP 对标或广泛兼容性。
