# GUI P1 Field Transcript

`Transcript` 是首次真实 iPhone P1 运行的可填写现场日志。它将 `Coach`、`Rx Bootstrap` 和 `Rx Setup` 状态转换为操作者记录，包含观察提示、预期结果、失败分类、工件路径、重跑规则和停止规则。

它不是 JSONL 证据。它本身不记录 Manual 通过，也不证明真实 iPhone 控制。

## GUI 路径

使用 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

在 `Src Refresh`、`Coach`、`Rx Score`、任何需要的 `Rx Bootstrap` 和 `Rx Setup` 之后打开 `Transcript`，然后在首次真实 HID 操作之前导出。在操作者观察物理 iPhone 时保持其打开或打印。

该对话框还具有 `Prefill Manual`、`Record Pass` 和 `Record Fail` 辅助功能。它们将选定的记录行复制到底部 Manual 控件中。`Record Pass` 有意限制为点击、滑动和键盘输入检查点；设置或路由行预填为 `info`，因此它们不会意外满足 Manual 控制门控。

## 操作者填写内容

每行包含：

- 检查点和当前状态；
- 在物理 iPhone 上观察什么；
- 预期结果；
- 可能的失败分类；
- 要附加的工件/日志路径；
- 操作者填写栏；
- 重跑规则；
- 停止规则；
- 下一步探针的 GUI 操作。

操作者应记录物理 iPhone 的实际行为，而不仅仅是 API 返回的内容。

## 所需现场纪律

- 通过行必须提及可见的 iPhone 响应。
- 失败行必须包含一个失败分类和一个工件/日志路径。
- 截图行必须说明帧是否为当前、非空白、正确窗口、正确设备和正确方向。
- 点击/滑动/输入行必须提及可见响应、焦点、指针行为、释放行为和文字结果。
- 任何路由、接收器、HID、线缆、Hub 端口、iPhone、所选设备或 iOS 设置在失败证据后的更改需要新的 run_id。
- 使用 `P1 Trial` 或 Manual 控制将真实 Manual 观察写入 JSONL。
- 当操作者想在记录前编辑备注时使用 `Prefill Manual`。
- 仅在物理 iPhone 可见响应了点击、滑动或键盘输入后使用 `Record Pass`。
- 对任何需要分类失败和工件/日志路径的行使用 `Record Fail`。

## 导出

`Export` 写入：

```text
evidence/<run_id>_<stage>_p1_field_transcript.md
```

此导出是现场记录和交付辅助工具。它支持审查，但 Acceptance 和 Readiness 仍然决定声明边界。

## 通过边界

记录仅当相同 run_id 具有以下条件时才能支持 P1 声明：

- Route Decision 就绪；
- 当运行不使用 UxPlay 时，备选接收器引导已记录；
- 接收器设置通道已记录；
- Doctor 无失败；
- 截图质量证据；
- JSONL 中的 Manual 点击、滑动和文字观察；
- 无未解释的失败事件；
- Acceptance PASS；
- Readiness PASS 且 `real_ios_control_verified=true`。

没有这些条件，记录应指向第一个缺失或失败的行，而不是提升该运行。
