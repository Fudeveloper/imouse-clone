# GUI XP Hardware Lab

`XP Lab` 是用于硬件采购和实验室验证的 GUI 看板。它将 XP 风格的公开硬件、接收器、投屏、HID 和群控信号转换为实际购买决策、工作台测试、所需证据和停止规则。

它有意不是一个成功屏幕。`ready` 行表示实验室通道在当前运行中可审查；它不证明真实 iPhone 响应、广泛兼容性或 XP 专用硬件对标。

## 操作者路径

Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness

在购买接收器/HID 硬件之前、在更改 Route Decision 之前、以及在声明 XP 对标之前打开 `XP Lab`。

## 通道

| 通道 | 目的 | 证据门控 |
|---|---|---|
| 路由和采购账本 | 锁定一个接收器、一个 HID 通道、一个 iPhone、一个 Hub/线缆路径和一个操作者。 | Route Decision JSON/报告和 Doctor。 |
| 接收器/采集装置 | 比较 UxPlay、Windows 接收器、有线投屏和采集卡备选。 | 接收器元数据、截图工件、窗口/设备绑定、日志。 |
| Windows/有线/解码通道 | 将产品接收器工作与 UxPlay 原型分离。 | fps/延迟/重连记录和截图稳定性样本。 |
| HID 控制器装置 | 将通用 CH9329/自制证明与 XP 专用硬件分离。 | HID 身份、固件、序列号、Manual 点击/滑动/输入观察。 |
| XP 专用硬件对标 | 将 XP 硬件、固件和自动绑定声明分开。 | 合法的并排 XP 硬件工件。 |
| iPhone 设置夹具 | 使 iPhone 设置可复现。 | 型号/iOS、AssistiveTouch、指针配置文件、基线截图。 |
| Hub、线缆和电源映射 | 防止物理漂移被误诊为脚本失败。 | Hub ID、端口、线缆 ID、电源路径、操作者备注。 |
| 采集稳定性和指标 | 从第一张截图到可重复的产品证据。 | 截图样本、指标、重连时机、仪表板。 |
| 日志和恢复桥梁 | 使接收器/HID/脚本失败可解释。 | 原始日志、解析的 callback、分类、恢复、重跑决策。 |
| 规模采购边界 | 阻止过早的群控购买和群控声明。 | P2/P3/P4 按设备工件、指标、日志、Readiness。 |

## 跟随测试

1. 点击 `Route Init` 或 `Route Edit`；用真实工作台值替换每个占位符。
2. 点击 `Validate`，然后 `Doctor`。
3. 打开 `XP Lab` 并从第一个 `fail`、`pending` 或 `warn` 行开始。
4. 使用 `Run Selected` 打开所属看板，如 `Rx Score`、`Rx Bootstrap`、`Bench`、`Control Bench`、`iOS SOP`、`Shot Bench`、`Attach Log` 或 `Dashboard`。
5. 将 `XP Lab` 导出到 `evidence/<run_id>_<stage>_xp_hardware_lab.md`。
6. 仅当当前行对相同 `run_id` 具有所需工件时才继续。

## 边界

- `XP Lab` 是一个采购和实验室验证看板；它不写入 JSONL 现场证据。
- CH9329 或自制 HID 成功仅为通用 HID 证明。
- XP 专用硬件对标需要合法的并排硬件证据。
- Windows 接收器、有线投屏、硬件解码和自动绑定声明需要测量的本地工件。
- 没有任何行可以覆盖 Acceptance、Readiness、Manual 观察、截图质量或相同运行证据。
