# GUI Verification Walkthrough

`Verify` 是一个 `run_id` 和一个阶段的 GUI 逐步验证走查。它是冗长跟随 SOP 与当前 GUI 状态之间面向操作者的桥梁。

它不执行命令，不写入 JSONL 证据，也不证明真实 iPhone 响应。它告诉操作者下一步运行什么、预期什么结果、保留什么证据以及在哪里停止。

## 何时打开

在设置 `Evidence run_id` 之后、声明任何 P1/P2/P3/P4 结果之前打开 `Verify`。

与以下内容一起使用：

- `Local` 用于可复制的 PowerShell 命令重放。
- `Coach`、`Transcript`、`Wizard` 和 `Runner` 用于现场执行。
- `Proof Map`、`Claim Scope`、`Acceptance`、`Readiness` 和 `Pack` 用于交付前。

## 行

每行包含：

| 列 | 含义 |
|---|---|
| `Phase` | 验证阶段，如离线自检、运行身份、路由决策、Doctor、接收器采集、HID Manual 控制、Acceptance/Readiness、稳定性、群控规模、XP 对标审查或交付 Pack。 |
| `Scope` | 该行影响的阶段或操作范围。 |
| `Status` | `pass`、`ready`、`warn`、`fail` 或 `pending`；后面的行不能覆盖前面的 `fail`。 |
| `Current` | GUI 当前从路由报告、Doctor、JSONL 摘要、Acceptance、Readiness 和工件清单中已知的信息。 |
| `Command / GUI path` | 要重放的精确命令或 GUI 路径。命令包含当前 `run_id` 和阶段。 |
| `Expected result` | 继续前进之前必须为真的条件。 |
| `Evidence to keep` | 交付所需的工件、JSONL 事件、报告、截图、日志或 Manual 观察。 |
| `Stop rule` | 阻止提升或强制重跑的条件。 |
| `GUI action` | 由 `Run Selected` 打开的面板。 |

## P1 顺序

从上到下运行 P1 走查：

1. 离线自检：单元测试、compileall、依赖检查。
2. 运行身份：稳定的 `run_id`、精确设备 ID、阶段、操作者。
3. 路由决策：接收器、采集、HID、iPhone、iOS、Hub、线缆和阻塞项为真实值。
4. Doctor：无 `fail`，或路由感知的非 UxPlay 接收器决策解释了警告。
5. 接收器采集：当前截图不是黑屏、过期、裁剪、错误窗口或错误设备。
6. HID Manual 控制：点击、滑动释放和文字输入各有通道分离的 Manual 通过/失败观察。
7. Acceptance 和 Readiness：对相同证据 JSONL 和当前阶段均通过。
8. 交付 Pack：必需工件存在，推荐的差距已确认，声明措辞遵循 `Claim Scope`。

## 停止线

- 如果路由、Doctor、接收器身份、采集绑定、iPhone 设置或截图质量不清洁，则在 HID 之前停止。
- 如果 API/HID 命令成功与可见的真实 iPhone 行为不匹配，则停止。
- 如果通用 Manual 备注被用于同时关闭点击、滑动和文字通道，则停止。
- 如果 Acceptance 或 Readiness 失败，则停止。
- 如果 `real_ios_verified=False`，则停止。
- 除非相同声明范围存在 XP 专用硬件/接收器/固件/绑定证据，否则停止 XP 对标措辞。

## 导出

在 `Verify` 中点击 `Export` 写入：

```text
evidence/<run_id>_<stage>_verification_walkthrough.md
```

导出是测试指南和交付检查清单。它只有在与实际 JSONL 证据、截图、Manual 观察、Doctor、Acceptance、Readiness 和精确设备/iOS 范围配对时才有用。
