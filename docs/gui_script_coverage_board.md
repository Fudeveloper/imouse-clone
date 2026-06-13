# GUI Script Coverage Board

`Script Cov` 是用于 XP 风格自动化/脚本就绪的 GUI 看板。它将阶段场景文件、dry-run、real-run 守卫、元数据记录、截图探测、HID 点击/滑动/文字通道、视觉/OCR、指标、群控脚本、失败回放和声明边界映射到一个操作者表中。

在运行真实场景之前、从 P1 扩展到 P3/P4 之前、以及在声称脚本或队列是 XP 风格自动化之前使用。

## GUI 流程

```text
Home -> Snapshot -> Procure -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

`Script Cov` 导出：

```text
evidence/<run_id>_<stage>_script_coverage.md
```

## 检查内容

| 域 | 目的 | 提升边界 |
|---|---|---|
| 场景清单 | 确认阶段脚本可解析且当前阶段默认值存在。 | 场景文件是计划，不是设备证据。 |
| Dry-run 契约 | 在触碰硬件之前确认运行器调度形状。 | Dry-run 仅关闭脚本结构信心。 |
| Real-run 守卫 | 在路由、Doctor 和设备数量清洁之前阻止实时脚本。 | 守卫允许意味着"可以开始"，不是"手机已响应"。 |
| 组件元数据 | 确保接收器、HID、iPhone、Hub、线缆和操作者可追溯。 | 元数据是可追溯性，不是控制证明。 |
| 截图探测 | 要求截图动作和现场截图质量门控。 | 截图证明不是 HID 证明。 |
| HID 通道 | 要求点击、滑动和文字脚本加上独立的 Manual 观察。 | API/HID 成功不是可见的 iPhone 响应。 |
| 视觉/OCR | 跟踪 find-image、颜色、OCR、文字、模板、区域和回放资产。 | 辅助覆盖率不是业务流可靠性。 |
| 指标/稳定性 | 跟踪 P2/P3/P4 的重复和指标脚本。 | 指标诊断稳定性，不诊断 Manual 响应。 |
| 群控批次 | 跟踪群控点击/滑动/输入和 P3/P4 证据需求。 | 本地群控 API 或 dry-run 不是群控证明。 |
| 失败回放 | 将失败与设备、分类、工件和重跑规则绑定。 | 重跑计划不能提升已失败的运行。 |

## 现场规则

在 `API Cov` 之后、禁用 Dry Run 之前运行 `Script Cov`。如果任何行为 `fail`、`pending` 或未解释的 `warn`，使用 `Run Selected` 并先修复该通道。

在 `Script Cov` 之后，打开 `Proof Map` 将脚本/运行器层面连接到精确的 Acceptance 和 Readiness 证明行。然后在交付前打开 `Claim Scope`，以免脚本/API/源码进展被表述为真实 iPhone 控制、群控、XP 硬件对标或广泛兼容性。

只有在相同 `run_id` 具有当前截图质量、通道分离的 Manual 点击/滑动/文字观察、无未解释的失败事件、Acceptance PASS、Readiness PASS 和精确设备/iOS 范围时，P1 才可以讨论。
