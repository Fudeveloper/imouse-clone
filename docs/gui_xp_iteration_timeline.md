# GUI XP Iteration Timeline

`XP Timeline` 是用于审查推断的 iMouse XP 产品迭代路径的 GUI 看板。它将公开的 XP 信号转换为按时间排列的研发经验、常见陷阱、SOP 门控、所需证据和停止规则。

它位于来源刷新和实现规划之间：

```text
Sources -> Src Refresh -> Action Map -> XP Timeline -> Iter Radar -> XP Drill -> XP Arch -> XP Lab -> Roadmap
```

## 操作者路径

Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness

在 `Src Refresh` 和 `Action Map` 之后、在更改路线图优先级、硬件采购或对标措辞之前打开 `XP Timeline`。

## 时间线阶段

| # | 阶段 | 为何重要 |
|---|---|---|
| 01 | 无应用黑盒控制 | 将真实 iPhone 响应与 API/HID 成功分开。 |
| 02 | Kernel/API 和 Console 拆分 | 保持 GUI、脚本、callback、客户端辅助和证据在一个服务边界内。 |
| 03 | 接收器/投屏产品化 | 使 AirPlay/有线接收器、窗口绑定、解码、重连和日志成为产品通道。 |
| 04 | 固件、有线投屏和绑定 | 防止 CH9329 证明成为 XP 硬件或 4.4 固件对标措辞。 |
| 05 | 视觉、OCR 和脚本资产 | 将 OpenCV/OCR 调用转换为可回放资产、区域、阈值和工件。 |
| 06 | 日志、恢复和群控规模 | 在失败按设备、组件、日志和指标隔离之前阻止群控声明。 |
| 07 | 来源刷新和声明治理 | 保持公开声明、包信号和 GUI 导出不在验收措辞中。 |

## 跟随测试

1. 运行 `Sources` 和 `Src Refresh`。
2. 运行 `Action Map`。
3. 点击 `XP Timeline`。
4. 从第一个 `fail`、`pending` 或 `warn` 行开始。
5. 使用 `Run Selected` 打开所属 GUI 看板。
6. 将 `XP Timeline` 导出到 `evidence/<run_id>_<stage>_xp_iteration_timeline.md`。
7. 在该行有足够的相同运行证据后重新打开 `Iter Radar`、`XP Drill`、`XP Arch`、`XP Lab` 和 `Roadmap`。

## 边界

- `XP Timeline` 是产品迭代情报，不是 JSONL 证据。
- 公开的 XP 信号永远不能证明我们的接收器、HID、截图、OCR、群控或对标行为。
- `ready` 行仅对当前阶段和证据范围可审查。
- 完美控制、广泛 iOS 兼容性和 XP 对标措辞仍需要相同运行的现场证据、Acceptance、Readiness 和精确设备/iOS 覆盖率。
