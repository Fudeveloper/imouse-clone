# GUI Goal Gate

`Goals` 是四个用户目标的 GUI 验收看板：

1. iOS 完美控制。
2. iOS 群控 SOP 和问题日志。
3. iMouse XP 核心功能和文档。
4. XP 迭代经验和教训。

它导出：

```text
evidence/<run_id>_<stage>_gui_goal_gate.md
```

## 关闭输入

Goal Gate 读取当前证据状态和周围的 GUI 看板：

| 输入 | 为何重要 |
|---|---|
| Acceptance 和 Readiness | 阶段门控结果和 `real_ios_control_verified`。 |
| Proof Map | 仍然阻止 iOS 控制声明的精确证据行。 |
| Claim Scope | 允许和禁止的演示/交付措辞。 |
| Evidence Pack | 相同 `run_id` 的必需和推荐工件。 |
| XP 差距审计 | 仍被阻止、部分完成或未启动的 XP 核心域。 |
| SOP 工件 | Runbook、工作表、SOP 看板、问题分类、重跑、恢复、Matrix 和差距报告。 |

## 操作者规则

在现场会议接近结束时使用 `Goals`，在 `Proof Map` 和 `Claim Scope` 之后，在任何完成摘要之前。

iOS 控制行不能通过，除非相同运行具有真实设备证据、Proof Map 关闭、Claim Scope 通过措辞、Acceptance PASS、Readiness PASS，且无未解释的失败事件。

Goal Gate 是一个验收映射，而非证据。它不写入 JSONL 证据，也不能单独证明真实 iPhone 响应。
