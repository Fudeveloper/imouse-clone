# GUI Field Evidence Runner

`Runner` 是一个 `run_id` 的现场检查清单。在 `Wizard` 构建完成后、任何 P1 声明之前使用它。

它检查相同运行路径中的以下内容：

| 门控 | 证明内容 | 停止线 |
|---|---|---|
| 运行范围 | 已知所选设备和证据路径。 | 如果物理 iPhone、HID、接收器、Hub 端口、线缆或 run_id 无法追溯，则停止。 |
| 路由决策 | 接收器、采集、HID、iPhone、iOS、工作台和阻塞项已记录。 | 如果验证失败或占位符仍然存在，则停止。 |
| 路由感知 Doctor | 本地依赖项和所选接收器路由已预检。 | 在任何 Doctor 失败时停止；warn 需要操作者备注。 |
| 截图质量 | 从目标 iPhone 捕获了当前可用的帧。 | 如果帧为黑屏、过期、裁剪、错误窗口或错误方向，则停止。 |
| HID 点击/滑动/文字 | 每个控制通道都有各自的 Manual 通过/失败观察。 | 如果 API 成功与可见的真实 iPhone 行为不匹配，则停止。 |
| Acceptance 和 Readiness | JSONL 证据通过了相同 run_id 的机器门控。 | 如果命令输出与 GUI 状态不一致，则停止。 |

Runner 导出 `evidence/<run_id>_<stage>_field_runner.md`，包含可复制的 PowerShell 命令：

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\<run_id>_route_decision.json --require-ready --markdown evidence\<run_id>_<stage>_route_decision.md --record-evidence evidence\<run_id>.jsonl
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --markdown evidence\<run_id>_<stage>_doctor.md
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate <stage> --markdown evidence\<run_id>_<stage>_acceptance.md
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate <stage> --gap-markdown evidence\<run_id>_<stage>_gap.md
.\.venv\Scripts\python -m imouse.readiness --target <stage> --evidence evidence\<run_id>.jsonl --markdown evidence\<run_id>_readiness.md
```

Runner 本身不是证据。真实 iOS 控制仍需要 JSONL 事件、截图工件、点击/滑动/文字的独立 Manual 观察、Acceptance PASS、Readiness PASS 以及精确的设备/iOS 范围。
