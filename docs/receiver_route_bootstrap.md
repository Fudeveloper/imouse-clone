# Receiver 路线引导

`imouse.receiver_bootstrap` 为 receiver/采集 lane 创建路线决策草案。当默认 UxPlay 路线被阻断且现场团队想先测试 Windows Receiver、有线投屏或采集卡路线时使用。

它不是 P1 通过。它只是填充 receiver 字段到足够进行 provider 预检和 Doctor 路由。HID、iPhone、台架台账、截图质量、人工观察、Acceptance 和 Readiness 仍然决定 P1 是否可以运行或通过。

## 命令

```powershell
.\.venv\Scripts\python -m imouse.receiver_bootstrap `
  --run-id p1_dev1_YYYYMMDD `
  --route windows_receiver `
  --receiver-path "C:\Program Files\ReceiverX\receiverx.exe" `
  --receiver-name ReceiverX `
  --version 1.2.3 `
  --airplay-name imouse-dev-01 `
  --window-title imouse-dev-01 `
  --window-process receiverx.exe `
  --output evidence\p1_dev1_YYYYMMDD_route_decision.json `
  --markdown evidence\p1_dev1_YYYYMMDD_receiver_bootstrap.md
```

然后运行：

```powershell
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\p1_dev1_YYYYMMDD_route_decision.json --markdown evidence\p1_dev1_YYYYMMDD_doctor.md
```

如果 receiver 路径和必需的 receiver 字段是真实的，Doctor 可以把缺失的 `uxplay` 从硬 `fail` 降为路线特定的 `warn`。这只表示所选路线不需要 UxPlay；不证明帧可以被采集。

## GUI 路径

```text
Rx Score -> Rx Bootstrap -> Rx Setup -> Doctor -> Receiver -> Shot Bench -> P1 Trial -> Acceptance -> Readiness
```

在以下情况使用 `Rx Bootstrap`：

- Windows 机器上缺失 `uxplay`；
- 已安装商业 Windows Receiver、有线投屏工具或采集卡应用；
- 操作员能提供真实路径、receiver 名称、版本、AirPlay/显示名称、采集方法和窗口标题/进程。

## 停止线

- 如果 `receiver.path` 不存在，停止。
- 如果路线决策 JSON 仍包含 receiver 占位值，停止。
- 如果截图是黑屏、过时、错窗口、裁剪或未绑定到所选 iPhone，在 HID 操作前停止。
- 直到同轮 JSONL evidence、截图质量、人工观察、Acceptance PASS 和 Readiness PASS 一致，停止任何 iOS 完美控制、广泛兼容或 XP 对标声明。

## 它能证明什么

| 能证明 | 不能证明 |
|---|---|
| Receiver 路线字段足够具体用于 provider 预检 | Receiver 正在显示真实 iPhone |
| 所选路线可以避免默认 UxPlay 硬失败 | 截图质量或帧新鲜度 |
| 路线决策文件已准备好用于 Doctor 路由 | 点击、滑动、文本输入、HID 响应或 XP 硬件对标 |

将其用作从 receiver 选择到真实 P1 evidence 的桥梁，而不是证据本身。
