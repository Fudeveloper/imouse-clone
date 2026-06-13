# GUI Control Evidence Ledger

在 Route/Doctor/Screenshot 就绪之后、Acceptance/Readiness 交付之前，在 P1 真实 iPhone 测试期间使用 `Ctrl Ledger`。

## 目的

`Ctrl Ledger` 是真实 iPhone 控制的通道分离证明看板。它读取与 Control Bench 相同的 `evidence/<run_id>.jsonl`，但要求操作者分别关闭以下通道：

| 通道 | 最低证明 | 停止线 |
|---|---|---|
| HID 点击 | 一个 Manual 通过记录，其步骤/备注名称包含 `HID click`，包含目标、操作前状态、操作后状态、可见指针/点击行为，以及有用的工件路径。 | 在以下情况停止：缺失点击、目标错误、按压卡住、指针漂移或采集不匹配。 |
| HID 滑动 | 一个 Manual 通过记录，其步骤/备注名称包含 `HID swipe`，包含方向、距离、释放、操作前后屏幕移动以及工件路径。 | 在以下情况停止：方向反转、距离错误、无释放、按压卡住或校准漂移。 |
| 键盘输入 | 一个 Manual 通过记录，其步骤/备注名称包含 `Keyboard input`，包含聚焦字段、预期文本、实际可见文本、输入法状态以及工件路径。 | 在以下情况停止：焦点错误、文字缺失/重复、键盘语言/输入法不匹配或 HID 绑定失败。 |

## 操作者流程

1. 运行 `Prepare`，填写 Route Decision，运行 Doctor，并拍摄当前截图。
2. 打开 `P1 Trial` 进行物理动作序列。
3. 打开 `Ctrl Ledger`。
4. 选择 `HID click`、`HID swipe` 或 `Keyboard input`。
5. 仅在观察到物理 iPhone 响应后点击 `Record Pass`。
6. 当可见结果错误时点击 `Record Fail`，然后保留分类和工件/日志路径。
7. 刷新 `Ctrl Ledger`，然后对相同的 `run_id` 运行 Acceptance 和 Readiness。

## 通用 Manual 规则

类似"控制冒烟测试看起来正常"的通用 Manual 行仅为上下文信息。它不能同时关闭点击、滑动和文字通道。

如果 `Generic Manual quarantine` 为 fail 或 warn，则将现场观察重写为三个明确的 Manual 行：

- `Control ledger - HID click`
- `Control ledger - HID swipe`
- `Control ledger - Keyboard input`

每行应描述物理 iPhone 的操作前/后状态。API 成功、SDK 成功、导出的 Markdown、公开来源研究或 dry-run 输出不能替代此记录。

## 失败 SOP

当一个通道失败时：

| 失败分类 | 首先检查 | 需保留的证据 | 重跑规则 |
|---|---|---|---|
| `hid` | HID 序列号、固件、Hub 电源、线缆、AssistiveTouch 指针状态。 | HID id、COM/USB 日志、操作前后屏幕工件。 | 重新绑定 HID 后仅重跑受影响通道。 |
| `calibration` | 活动区域、方向、安全点、坐标变换。 | 带有标记点的截图、校准配置文件、观察到的偏移。 | 重新校准，然后在脚本之前重跑点击/滑动。 |
| `capture` | 接收器窗口、过期/黑帧、方向、错误设备。 | 当前截图、接收器日志、窗口/显示 ID。 | 在 HID 通道之前重跑 Shot Bench。 |
| `business_state` | 应用/页面焦点、弹窗、键盘/输入状态。 | 页面截图和操作者备注。 | 重置页面状态，然后仅重跑受影响通道。 |
| `claim_boundary` | Acceptance、Readiness、精确设备/iOS 范围。 | 报告和 Evidence Pack。 | 不得升级；收集缺失的相同运行证据。 |

## 声明边界

`Ctrl Ledger` 可以使证据审查更严格，但它本身不能证明真实 iOS 控制。在相同运行具有当前截图质量、通道特定的 Manual 点击/滑动/文字通过记录、无未解释的失败事件、Acceptance PASS、Readiness PASS 以及精确的设备/iOS 范围之前，P1 仍然未经验证。
