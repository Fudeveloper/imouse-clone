# GUI P1 Test Coach

更新时间：2026-06-09

`Coach` 是 Python GUI 中面向操作者的真实设备 P1 测试指南。它将首次 iPhone 运行转换为固定序列，包含当前状态、GUI 入口、命令、通过标准、失败处理、需保留的证据和停止规则。

它不是证据。它本身不执行命令，不写入 JSONL 证据，也不证明真实 iPhone 控制。

## GUI 路径

启动 GUI：

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m imouse.gui
```

使用 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

点击 `Coach`，选择第一个 `fail`、`pending` 或 `warn` 行，然后点击 `Run Selected`。

## 导出

`Export` 写入：

```text
evidence/<run_id>_<stage>_p1_test_coach.md
```

导出内容作为 `P1 Test Coach` 包含在 GUI Evidence Pack 中。

## 步骤顺序

1. 运行身份和设备范围。
2. 来源衍生的 SOP 门控。
3. Route Decision。
4. 本地命令重放。
5. 预检 Doctor。
6. 现场套件和 iOS 设置。
7. 接收器截图和 Shot Bench。
8. 坐标校准。
9. HID 点击。
10. HID 滑动。
11. 键盘输入。
12. 可重复脚本和日志。
13. Acceptance。
14. Readiness 和交付。

`Coach` 负责端到端的 P1 运行。`Src Refresh` 负责路由或声明更改之前的公开来源新鲜度。`XP Lab` 负责购买或声明对标之前的硬件采购和实验室验证边界。`Rx Score` 负责当操作者必须在 `uxplay`、`windows_receiver`、`wired` 和 `capture_card` 之间选择时的接收器候选选择。`Rx Bootstrap` 负责备选接收器通道的路由决策草案，同时保持 P1 阻塞。`Rx Setup` 负责步骤 7 之前的路由特定的接收器安装/绑定拆分。`Transcript` 负责可填写的人工观察日志；它仍然不能替代 JSONL Manual 证据。

## 通过规则

P1 运行在相同 `run_id` 具有以下条件之前不算完成：

- Route Decision 就绪。
- Doctor 无失败。
- 当前非空白截图证据。
- 点击、滑动和文字输入的 Manual 通过观察。
- Acceptance PASS。
- Readiness PASS 且真实 iOS 控制已验证。
- 无未解释的失败事件。

## 失败规则

从第一个未通过的 Coach 行开始处理。如果接收器、HID、线缆、Hub、iPhone 设置、所选设备或路由身份发生变化，在修复阻塞项后启动新的 `run_id`。

API/HID 命令成功不算通过，除非操作者看到真实 iPhone 响应并为相同运行记录 Manual 证据。
