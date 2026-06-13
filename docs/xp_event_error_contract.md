# XP Event/Error 协议

更新时间：2026-06-09

本文定义 XP 风格 API 事件、callback、日志和错误的 GUI/SOP 协议。它是实现指南和审计清单。它不是现场 evidence，也不证明 XP 对标或真实 iOS 控制。

## 协议目标

XP 版对标不仅是 click API。产品协议需要这些层保持一致：

- API 信封：HTTP 和 WebSocket `/api` 调用使用 `fun`，回显 `msgid`，返回 `status`、`message` 和 `data.code`。
- 请求传输：GET、POST JSON、POST 表单、multipart 截图和 WebSocket 请求必须在 GUI 外可回放。
- Callback 生命周期：callback/事件在搭配 JSONL evidence 之前只是调试和运维信号。
- 现场事件来源：receiver、采集、HID、设备、分组和运维事件必须携带设备/组件上下文。
- 错误分类：receiver/采集/HID、视觉/OCR/脚本、分组和运维错误必须保持明确。
- 日志接入：原始 receiver/HID 日志应被导入、分类并关联到重跑决策。
- 声明边界：API 成功、callback、日志或 Markdown 导出本身不证明真实 iPhone 响应。

## GUI 入口

使用 Live Probe 的 `Events` 按钮打开事件/错误协议面板。导出生成：

```text
evidence/<run_id>_<stage>_xp_event_error_contract.md
```

该面板读取当前 Route Decision 状态、Doctor 结果、Acceptance/Readiness 预览、evidence JSONL 汇总、XP Gap 审计和 callback 行。它不写 JSONL evidence。

## 状态含义

| 状态 | 含义 |
|---|---|
| `pass` | 该协议由当前阶段门和真实 evidence 支持。这很少见，且仅限于同一 run_id。 |
| `ready` | 本地实现或支持 evidence 可用于现场，但不是产品声明。 |
| `warn` | 该层存在但有证明边界、callback/日志警告、部分 XP gap 或 real_ios_verified 为 false。 |
| `pending` | 必需的路线、callback、evidence 或门数据尚未生成。 |
| `fail` | 存在硬阻断项，如 Doctor fail、路线 fail、缺少必需文档或门失败。 |

## 错误分类

在 JSONL evidence、Attach Log triage、Problems、Rerun 和 Recovery 中一致使用这些分类：

| 分类 | 含义 | 首选 GUI 动作 |
|---|---|---|
| `airplay_discovery` | iPhone 无法找到或保持 receiver 身份。 | Receiver、Doctor、Route Edit |
| `airplay_stream` | AirPlay 已连接但帧为黑屏、过时、错误或不稳定。 | Shot Bench、Attach Log |
| `capture` | 截图采集、窗口绑定、裁剪、方向或 artifact 失败。 | Shot Bench、Receiver |
| `hid` | 鼠标/键盘命令已发送但真实 iPhone 响应缺失或错误。 | Control Bench、P1 Trial |
| `calibration` | 坐标映射、方向、active area 或安全点漂移。 | P1 Trial、calibration |
| `vision_template` | 模板匹配漏判或误判。 | Assets、Scenario Library |
| `vision_color` | 颜色或多颜色匹配漂移。 | Assets、Scenario Library |
| `ocr` | OCR/文字识别漏判、模型问题或裁剪漂移。 | Assets、Scenario Library |
| `group_dispatch` | 批量/分组结果隐藏了逐设备失败。 | Matrix、Rerun |
| `performance` | 延迟、重连、fps、资源或长跑不稳定。 | Dashboard、Recovery |
| `business_state` | 页面、键盘、弹窗、登录、语言或 App 状态漂移。 | Timeline、Triage |
| `route_decision` | 路线/台架元数据缺失、形状为占位值或被阻断。 | Route Edit、Doctor |
| `uncategorized` | 失败尚未能关联到已知 lane。 | Triage、Problems |

## SOP

1. 代码变更后运行 `Local` 命令。
2. 在任何真实 HID 操作之前验证 Route Decision 和 Doctor。
3. 重跑前使用 `Events` 审查 API 信封、callback 状态、错误分类和声明边界。
4. 使用 `Callback` 和 `Attach Log` 检查或导入原始事件/日志上下文。
5. 使用 `Timeline`、`Matrix` 和 `Triage` 把每个失败关联到设备 ID、步骤、分类和 artifact。
6. 使用 `Problems`、`Rerun` 和 `Recovery` 决定最小重放路径以及是否需要 fresh run_id。
7. 只有在同一 run_id 具备截图质量、人工观察和组件元数据后才运行 Acceptance 和 Readiness。

## 边界

- Callback 行是诊断上下文，不是控制证明。
- Attach Log 可以写 log-triage JSONL evidence，但日志仍不替代截图质量或 Manual 观察。
- 本地 config/user/shortcut helper 只是兼容脚手架。
- CH9329/通用 HID evidence 不证明 XP 专用硬件、4.4 固件、有线投屏、自动绑定或授权对标。
- 公开 XP API 和帮助页是 backlog 输入，直到它们转化为本地 evidence 和阶段门。
