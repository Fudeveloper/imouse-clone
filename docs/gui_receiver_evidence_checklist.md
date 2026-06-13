# GUI Receiver Evidence Checklist

`Rx Evidence` 是 Python GUI 中的接收器/采集证明检查清单。在 `Rx Setup` 之后、`P1 Trial` 之前使用，特别是当默认 UxPlay 路由被阻止且运行使用 `windows_receiver`、`wired` 或 `capture_card` 时。

此看板是 SOP 和交付工件。导出本身不写入 JSONL 证据，不证明真实 iPhone 响应，也不证明 XP 对标。

## GUI 流程

使用 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> Pkg Guard -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

当接收器路由已选定且操作者在 HID 操作之前需要逐步采集证明顺序时，点击 `Rx Evidence`。

## 检查内容

`Rx Evidence` 读取与现场 GUI 其余部分相同的当前状态：

- Route Decision JSON 路径、接收器路由、接收器身份、采集方法、窗口绑定、HID id、iPhone 型号和 iOS 版本。
- 路由验证结果和未解决阻塞项。
- 接收器提供者预检。
- 路由感知的 Doctor 状态，包括 `binary:uxplay` 是否仍为硬失败或路由特定警告。
- Acceptance 截图质量、组件元数据和 Manual 观察行。
- Readiness 声明状态。
- 证据 JSONL 摘要、失败事件计数和指标计数。

## 检查清单顺序

看板将接收器路由与 HID 和声明措辞分开：

| 顺序 | 含义 | 停止线 |
|---|---|---|
| 锁定一个接收器路由 | 一个 run_id 仅使用一个接收器通道。 | 在占位符、混合路由、未解决阻塞项或已为该 run_id 记录的失败路由决策时停止。 |
| 接收器提供者预检 | 提供者字段可以在真实采集工作之前评估。 | 如果路径、AirPlay 名称、采集方法或窗口绑定缺失，则停止。 |
| 路由感知 Doctor | 使用 Route Decision 路径运行 Doctor。 | 在任何失败时停止；不要绕过 Real-run Guard。 |
| 绑定接收器身份 | iPhone、接收器窗口/来源、采集方法、HID 和 device_id 可一起追溯。 | 如果可见的接收器窗口无法与代码采集的帧关联，则停止。 |
| 基线截图证明 | HID 之前存在一个当前、非黑屏的截图。 | 在黑屏、过期、错误窗口、错误设备、裁剪或仅 Manual 帧时停止。 |
| 接收器采集探测集 | 收集重复截图、工件、指标和日志。 | 如果占位符元数据被记录为通过或接收器失败被隐藏，则停止。 |
| 重连和日志分类 | 失败的发现/流/采集/绑定/性能路径有日志和重跑决策。 | 如果失败无法隔离到设备、接收器、路由、窗口、线缆或日志行，则停止扩展。 |
| HID 交付停止线 | 只有清洁的接收器证明才能进入 P1 Trial。 | 如果 Manual 观察为通用或截图证明缺失，则停止。 |
| Acceptance 和声明关闭 | Acceptance 和 Readiness 决定声明措辞。 | 在两者都通过之前，停止所有完美控制、群控、广泛兼容性或 XP 对标措辞。 |

## 可复制命令

导出包含以下命令：

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\<run_id>_route_decision.json --require-ready --markdown evidence\<run_id>_<stage>_route_decision.md
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json --markdown evidence\<run_id>_<stage>_doctor.md
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --run-id <run_id> --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --run-id <run_id>
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1 --markdown evidence\<run_id>_p1_acceptance.md --gap-markdown evidence\<run_id>_p1_acceptance_gap.md
.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\<run_id>.jsonl --markdown evidence\<run_id>_p1_readiness.md
```

脚本运行器命令在对真实服务运行并使用真实元数据编辑时可以写入现场证据。GUI 导出本身不运行它们。

## 边界

- `Rx Evidence` 本身不安装、启动或验证接收器。
- `Rx Evidence` 不能替代 `Shot Bench`、`P1 Trial`、`Ctrl Ledger`、`Acceptance` 或 `Readiness`。
- 清洁的接收器检查清单不是 iOS 控制通过。
- Windows/有线/采集卡备选路由仅在路由感知的 Doctor 无失败检查时才能移除本地 UxPlay 阻塞项。
- XP 对标仍需要 XP 硬件/固件/有线/硬解码证据和并排工件。

