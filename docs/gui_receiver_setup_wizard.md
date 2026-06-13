# GUI Receiver Setup Wizard

`Rx Setup` 是 Python GUI 中的路由感知接收器设置指南。它将当前的 Route Decision 转换为操作者检查清单，用于安装、启动、绑定和分类所选接收器通道。

它仅是一个指南。它不安装软件，不启动接收器，不写入 JSONL 证据，也不证明真实 iPhone 控制。

## GUI 路径

打开 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Rx Evidence -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

在 `Coach` 之后点击 `Rx Score`，当备选接收器路由需要路由决策草案时使用 `Rx Bootstrap`，点击 `Rx Setup` 进行路由安装/绑定，然后在 HID 控制测试之前点击 `Rx Evidence`。选择第一个非 `pass` 的行，然后使用 `Run Selected` 或该行中显示的命令。

## 检查内容

向导读取与现场 GUI 其余部分相同的状态：

- Route Decision JSON 路径、run_id、接收器路由、接收器名称、版本、路径、启动命令、AirPlay 名称、采集方法、窗口绑定、授权/状态以及任何 `Rx Bootstrap` 草案值。
- 路由验证报告和未解决阻塞项。
- Doctor 对 `receiver_provider` 和 `binary:uxplay` 的检查。
- Acceptance 中截图质量和 Manual 真实 iPhone 观察的行。
- Readiness 声明 `real_ios_control_verified`。
- 证据摘要计数和失败事件计数。

## 路由通道

所选路由必须恰好是以下之一：

| 路由 | 主要用途 | P1 门控 |
|---|---|---|
| `uxplay` | 开源 AirPlay 接收器原型 | `binary:uxplay` 通过，唯一 AirPlay 名称可见，截图质量通过 |
| `windows_receiver` | Windows 产品级接收器备选 | 提供者预检通过，授权/版本/路径已记录，窗口绑定稳定 |
| `wired` | 有线投屏或供应商 SDK 路径 | 驱动/设备/线缆身份已记录，帧自动采集 |
| `capture_card` | HDMI/采集卡诊断或备选路径 | 卡/输入/分辨率已记录，工件映射到所选 device_id |

不要在一个运行内混合路由。如果已经记录了失败的路由决策或失败的真实设备证据，请在新的 run_id 下修复设置。

## 停止规则

- 如果无法为 run_id 识别路由文件，则停止。
- 如果 Route Decision 验证失败或仍有占位符，则停止。
- 如果所选 `uxplay` 通道有 `binary:uxplay=fail`，则停止。
- 如果备选接收器路由仍然使 Doctor 有 `binary:uxplay=fail`，则停止；Doctor 必须使用 Route Decision 路径运行，以便缺失的 UxPlay 依赖项变为路由特定警告。
- 如果采集可能指向错误窗口、过期显示、隐藏窗口或仅 Manual 截图，则停止。
- 在截图质量通过之前停止 HID 测试。
- 在 JSONL 证据、Manual 观察、Acceptance 和 Readiness 全部通过之前，停止任何完美控制、广泛 iOS 兼容性或 XP 对标声明。

## 导出

`Export` 写入：

```text
evidence/<run_id>_<stage>_receiver_setup_wizard.md
```

导出包含设置表和 `Copy-Ready Commands` 块，用于路由初始化、路由验证、Doctor 和所选接收器通道。此文件是操作者指南和交付工件，不是真实 iPhone 响应的证据。

## 后续测试

在清洁的设置通道后：

1. 运行 `Receiver` 确认路由门控状态。
2. 运行 `Rx Evidence` 以锁定接收器/采集证明命令、工件和停止线。
3. 使用 Route Decision 路径运行 `Doctor`。
4. 运行 `Shot Bench` 并保留帧工件。
5. 运行 `P1 Trial` 进行点击、滑动和文字输入。
6. 为每个失败附加接收器/HID 日志。
7. 运行 Acceptance。
8. 运行 Readiness。

只有最终的证据、Acceptance 和 Readiness 报告才能支持 P1 控制声明。
