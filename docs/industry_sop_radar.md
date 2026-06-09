# iOS 群控行业现状与 SOP Radar

更新时间：2026-06-09

目标：把 iMouse XP 版对标、行业主流路线、现场 SOP、研发优先级和声明边界收敛到一张 GUI 可执行雷达。本文是研发/现场决策资料，不是真机控制证据。

## 公开资料刷新

| 来源 | 当前信号 | 对研发的影响 |
|---|---|---|
| `https://www.imouse.cc/` | 官网仍把 XP 类产品描述为虚拟鼠标键盘硬件、AirPlay 镜像、iPhone 端无需安装 App、Kernel/Console、本地 HTTP/WebSocket API、OpenCV 找图和 OCR。 | 主线仍是 receiver/capture + HID + vision/OCR + local API + SOP；不能把 WDA/Appium/MDM 当作 XP 对标主控路线。 |
| `https://www.imouse.cc/python-xp/` | Python XP 辅助库指向 XP 版专用硬件和 helper/API 分层。 | SDK 兼容层只是集成入口；硬件、固件、授权、回调和真实 iOS 响应必须实测。 |
| `https://www.imouse.cc/XP版API文档/` | XP API 公开本地 `9911`、`/api`、`fun`、HTTP/WebSocket、`msgid` 和图色/键鼠/设备/配置/用户/快捷指令/callback 等域。 | 当前 `/api + fun` 方向正确，但必须继续按域补齐字段语义和真实事件。 |
| `https://www.imouse.cc/XP版帮助文档/软件简介/` | XP 新版资料强调 Windows、窗口分离、4.4 固件、有线投屏自动绑定、投屏速度、单投屏服务、硬解、分辨率自适应、日志、云分组和子账号。 | 下一阶段重点不是堆 GUI 外观，而是 receiver/HID/日志/metrics/恢复和现场 SOP。 |
| `https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings` | iPhone farm 设置强调机型/iOS、辅助触控、全键盘访问、鼠标/触控板、亮度/锁屏、同网段和硬件连接。 | P1 前必须把手机设置、Hub/线材、网络、接收器和 HID 绑定写入 Route Decision 和 evidence。 |

## 主流路线判断

| 路线 | 行业定位 | 是否作为主线 | SOP 结论 |
|---|---|---|---|
| receiver/capture + USB HID + vision/OCR + local API | 最接近 XP 的无越狱、无手机 App、跨 App 黑盒控制路线。 | 是 | P1 必须先证明单台真实 iPhone 截图、点击、滑动、文本输入。 |
| Windows receiver/window capture | 更接近 XP 桌面产品化路线。 | 候选主线 | 必须记录窗口/进程/版本/采集方式/日志，不能只靠人工可见窗口。 |
| Wired projection/vendor SDK | 可能带来更低延迟和更稳绑定。 | 候选主线 | 必须能自动拿帧、绑定设备身份并留下日志；封闭观看器不能算。 |
| CH9329/general USB HID | 低成本 P1 验证路线。 | 原型主线 | 只能证明通用 HID；不能证明 XP 专用硬件、4.4 固件或自动绑定。 |
| XP dedicated hardware | 严格 XP 硬件对标路线。 | 专项 | 需要合法样品和同页同机 side-by-side evidence。 |
| WDA/Appium/XCUITest | 自有 App 测试路线。 | 非主线 | 可做辅助 QA，不能证明 XP 式跨 App 黑盒控制。 |
| MDM/Configurator/Shortcuts | 初始化/运维辅助。 | 辅助 | 只负责设备准备，不替代截图、HID 和人工观察证据。 |

## 现场 SOP 雷达顺序

1. Sources：复核公开资料，只把公开说法转成研发假设。
2. Industry：确认主流路线、XP 壁垒、iPhone 设置、receiver/HID/视觉/运维/扩容和声明边界。
3. Routes：选定本轮 receiver lane 和 HID lane，写入真实 Route Decision。
4. Doctor：硬件动作前必须跑，fail 时停止实跑。
5. Shot Bench：先证明当前截图不是黑屏、白屏、错窗口、过期帧或错设备。
6. P1 Trial / Control Bench：再证明真实 iPhone 可见地响应点击、滑动释放和文本输入。
7. Acceptance / Readiness：只有 JSONL、截图质量、人工观察、组件元数据和 readiness 同时通过，才允许阶段声明。
8. Timeline / Matrix / Triage / Review：失败必须可按设备、组件、日志、截图和脚本步骤复盘。

## 研发优先级

| 优先级 | 工作 | 验收方式 |
|---|---|---|
| P0 | 保持离线测试、GUI/SOP/文档、XP API 兼容层、证据门。 | 单元测试、compileall、doctor/readiness 不误放行。 |
| P1 | 选择 receiver/HID，完成单台真实 iPhone 截图、点击、滑动、输入。 | P1 Acceptance PASS + Readiness PASS + real_ios_verified true。 |
| P2 | 单设备稳定性，100 张截图、重复 HID、metrics、日志和失败复盘。 | P2 Acceptance PASS，无无法解释失败。 |
| P3 | 4 台群控试点，按设备隔离 receiver/HID/Hub/cable/脚本失败。 | P3 Acceptance PASS + Device Matrix 完整。 |
| P4 | 10 台稳定性、恢复、运维、权限、升级和商业化控制台专项。 | P4 Acceptance PASS + 长跑证据。 |

## 停线

- 没有真实截图，就不执行 HID 成功声明。
- 没有人工观察，就不声明真实 iPhone 响应。
- 没有 Acceptance/Readiness，就不声明阶段完成。
- 没有 side-by-side evidence，就不声明 XP 专用硬件、4.4 固件、有线投屏、自动绑定或硬解对标完成。
- 没有机型/iOS 覆盖矩阵，就不继承官网广泛兼容宣传。
- 没有按设备日志和 artifact，就不扩容。

