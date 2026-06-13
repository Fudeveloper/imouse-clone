# iMouse XP 架构拆解图

本文是对 iMouse XP 对标的架构级拆解。基于以下公开信号：

- https://www.imouse.cc/
- https://www.imouse.cc/python-xp/
- https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/
- https://www.imouse.cc/XP%E7%89%88%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3/

本文不证明我们的原型能控制真实 iPhone。它是设计和验证参考图。

## 推断的 XP 技术栈

| 层级 | 推断的实现原理 | 本地原型覆盖 | 证据门 |
|---|---|---|---|
| 产品边界 | 无 iPhone App、无越狱；通过投屏加硬件输入实现黑盒 iPhone 控制。 | Sources、Industry、Routes、Core、XP Gap、Goals。 | 同轮 receiver、HID、截图、人工观察、Acceptance、Readiness。 |
| 硬件与 USB/HID | 专用虚拟鼠标/键盘硬件是输入权威。 | CH9329/通用 HID 原型、Hardware Bench、Control Bench、P1 Trial。 | HID 身份、固件、Hub/线材、click/swipe/type Manual pass；XP 对标需要 XP 硬件同场对比。 |
| 投屏与 receiver | AirPlay/投屏 receiver 必须稳定、可绑定、可采集、可观察。 | UxPlay/Windows/有线/采集卡路线、Rx Score、Rx Bootstrap、Rx Setup、Receiver Gate、Shot Bench。 | Route 元数据、Doctor/provider 检查、非黑屏新截图、窗口/设备绑定、日志。 |
| 截图、视觉、OCR | 自动化读取当前截图、图像/颜色/OCR 区域和可回放 artifact。 | Screenshot API、GUI 预览、Template Asset Index、find-image/color/OCR、Scenario Library。 | 已保存截图 artifact、区域、阈值、真实识别事件、可回放失败。 |
| 内核/API 服务 | 控制台、脚本、GUI 和 helper 走同一个本地服务协议。 | FastAPI XP 兼容服务、`/api + fun`、WebSocket、XpApiClient、Events。 | API/client/WebSocket 测试加保留 receiver/HID/采集真相的现场错误。 |
| Python helper/脚本运行时 | SDK 形态是集成协议，不是硬件证明。 | XpApiClient、JSON runner、dry-run guard、批量 helper、metrics/artifact。 | 固定的 helper 行为、本地测试，然后使用相同 helper 的真实运行 JSONL。 |
| 控制台/GUI 操作层 | GUI 是操作控制台和 SOP 展示面，不是证明生成器。 | Tkinter GUI、Live Probe、Home、Verify、Local、Coach、Transcript、Pack。 | 第二个操作员能从导出的 artifact 和相同 run_id 复现本轮运行。 |
| 证据与就绪 | 声明基于只追加的 evidence 和阶段门。 | JSONL evidence、Acceptance、Readiness、Timeline、Matrix、Triage、Recovery。 | 组件元数据、截图质量、Manual 观察、无无法解释的 fail、Acceptance PASS、Readiness PASS。 |
| 群控与运维 | 只在单设备证明后才扩规模；失败保持逐设备可解释。 | Groups、Matrix、Stage Dashboard、metrics、callback/日志接入、P2/P3/P4 runbook。 | P2 稳定性、P3 pilot_4、P4 stable_10、逐设备 artifact、metrics、日志、恢复记录。 |

## GUI 入口

在 Python GUI 中，点击：

```text
Live Probe -> XP Arch
```

导出生成：

```text
evidence/<run_id>_<stage>_xp_architecture.md
```

在 `Core`、`Roadmap` 和 `XP Gap` 复审之前先使用 `XP Arch`。

## 状态解读

- API/SDK 或 GUI 层显示 `ready` 表示本地结构可用于当前阶段。
- `ready` 不表示 receiver、HID、iPhone、XP 硬件、有线投屏或硬解已证明。
- 硬件/evidence 层显示 `fail` 是预期情况，直到真实 iPhone JSONL evidence 存在。
- `pass` 只对支持它的精确阶段和 run_id 有效。

## 研发指导

1. 保持 WDA/Appium/MDM/Shortcuts 在 XP 风格主声明之外。
2. 把 receiver/采集和 HID 作为独立的产品 lane，各自保留独立 evidence。
3. 把 XP 专用硬件、4.4 固件、有线投屏、自动绑定和硬解作为独立对标 lane。
4. 让每个 GUI 快捷操作都经过 evidence 感知的服务路径。
5. 在 receiver、截图、HID、校准、人工观察、Acceptance 和 Readiness 为 P1 闭合之前，不要扩到一台 iPhone 以上。

## 声明边界

不要从本文声称 iOS 完美控制、广泛兼容或 XP 对标。这些声明需要同轮现场 evidence、精确设备/iOS 覆盖、Acceptance、Readiness 和无无法解释的失败。
