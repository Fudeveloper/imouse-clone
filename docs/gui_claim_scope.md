# GUI Claim Scope

`Claim Scope` 是用于演示、交付和验收措辞的 GUI 看板。它将当前的 Readiness、Acceptance、Proof Map、Evidence Pack、API/Core 覆盖率、兼容性和 XP 差距信号转换为精确的允许声明和禁止声明。

在向用户演示、发布说明、现场交付或验收摘要之前立即使用。

## GUI 流程

```text
Home -> API Cov -> Script Cov -> Proof Map -> Claim Scope -> Start Pack -> Wizard -> Runner -> Acceptance/Readiness
```

`Claim Scope` 导出：

```text
evidence/<run_id>_<stage>_claim_scope.md
```

## 声明行

| 声明行 | 保护内容 | 关闭边界 |
|---|---|---|
| P0 离线资产 | 本地 GUI/API/SOP/源码工作 | 仅 Readiness P0 PASS。这不是现场控制。 |
| P1 单 iPhone 控制 | 真实 iPhone 响应措辞 | 相同运行的 JSONL、截图质量、点击/滑动/文字 Manual 观察、Acceptance PASS、Readiness PASS 以及精确的设备/iOS/接收器/HID 范围。 |
| P2 单设备稳定性 | 稳定性措辞 | 重复证据、指标、日志、恢复记录、P2 Acceptance/Readiness，以及无未解决失败事件。 |
| P3/P4 iOS 群控 | 群控措辞 | 按设备通道证据、Matrix、指标、工件、恢复/分类、以及 P3/P4 Readiness。 |
| XP API/SDK 兼容性 | XP 风格的辅助/API 声明 | 仅经过测试的本地端点；基于硬件的声明需要接收器/HID/iPhone 证据。 |
| XP 硬件/有线/固件/解码对标 | XP 专用硬件对标 | 并排硬件或等效工作台证据、固件/绑定日志、解码指标和现场工件。 |
| 设备和 iOS 兼容性 | 支持的机型/iOS 措辞 | 仅限精确机型/iOS/方向组合证据。不得从一台手机推而广之。 |
| 文档和 SOP 交付措辞 | 最终交付范围 | Evidence Pack、Start Pack、Proof Map、Goal Gate、Readiness、Acceptance、记录/工作表以及阻塞项列表。 |

## 操作者规则

`Claim Scope` 仅编写措辞指导。它不写入 JSONL 证据，也不证明真实 iPhone 响应。

允许措辞仅限于标记为 `pass` 的行。标记为 `ready`、`warn`、`pending` 或 `fail` 的行必须作为未完成工作呈现，并排除列出的禁止措辞。

在相同运行具有该行中指定的现场证据和门控结果之前，不得声明 iOS 完美控制、XP 等效控制、群控、硬件对标或广泛的 iPhone/iOS 兼容性。
