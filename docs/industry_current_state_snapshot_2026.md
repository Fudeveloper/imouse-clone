# iOS 群控行业现状快照 2026-06-09

本文回答一个比代码更重要的问题：对标 iMouse XP 时，行业现在到底在解决什么，主流路线为什么这样选，哪些 SOP 是研发前必须固化的。

结论边界：

- 本文是公开来源情报和研发判断，不是实机 evidence。
- 任何 iOS 完美控制、广泛兼容、XP parity 结论，都必须由同一轮 `evidence/<run_id>.jsonl`、截图质量、Manual/P1 Trial、Acceptance PASS、Readiness PASS、组件台账和必要的 XP 硬件侧比证明。
- 官网、第三方安装文档、Apple 支持文档只能定义测试输入和 SOP 闸门，不能替代本项目验收。
- 2026-06-09 已重新复核官网、XP Python、XP API、Some3C 安装/设置文档、PyPI、Apple AirPlay/AssistiveTouch 支持页；下面所有“支持”“兼容”均指公开声称或平台能力，不代表本项目已覆盖。

## 当前公开来源

| 来源 | 当前可用信号 | 研发用途 |
|---|---|---|
| `https://www.imouse.cc/` | iMouse 使用虚拟鼠键硬件；通过 AirPlay 镜像传屏；手机端无需安装 App；产品由内核服务端和控制台端组成；API 可用 HTTP/WebSocket；提供 OpenCV 找图和 OCR；官网还公开声称支持 iPhone17、iOS 13.4 以上含 26.4。 | 确认 XP 类主线是 receiver/capture + HID + vision + local API + console，不是 Appium/WDA 主线；官网兼容口径只能转成 Device/iOS Compatibility Matrix 的待测范围。 |
| `https://www.imouse.cc/python-xp/` | Python XP 只适用于 XP 版，需配套专用硬件；helper 分 console 和 device；覆盖 Device、AirPlay、USB、Group、Image、Keyboard、Mouse、Shortcut、事件、日志等。 | SDK 形态要围绕本地内核服务；但安装 SDK 不证明 receiver、HID、硬件授权或真实 iPhone 控制。 |
| `https://www.imouse.cc/XP版API文档/` | XP API 通过 `9911/api` 支持 HTTP 和 WebSocket；WebSocket 使用 `msgid` 做异步对应；错误码覆盖设备、硬件绑定、采集、OCR、分组、插件、超时等失败域。 | API 兼容必须包含 envelope、msgid、callback/error taxonomy 和逐设备失败，不只做 click/screenshot happy path。 |
| `https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version` | XP 新版资料强调 Windows 10+、8GB+、硬件加速；Core/Console 分离；Kernel 是无界面的 Windows service；Console 异常时重启 Kernel 是常见恢复动作。 | 产品化重点必须落到 service、日志、重启、权限、安装、运维，而不是只做 GUI 按钮。 |
| `https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings` | iPhone 设置包含 AssistiveTouch、Full Keyboard Access、Trackpad & Mouse、亮度/锁屏、旋转锁、控制中心布局、同网段投屏、硬件绑定、日志窗口和鼠标参数。 | iOS 设置不是附属项，而是 P1 前置闸门；必须进 Route Decision、Kit Gate、iOS SOP、Transcript。 |
| `https://pypi.org/project/imouse-py/` | PyPI index 当前显示 `imouse-py 0.0.4`；项目描述仍强调客户端-服务端 Python 库、XP 版和配套硬件。 | 研发迭代要跟踪 SDK 发布节奏、helper 域、事件/日志变化；但包版本不代表本地 receiver/HID/硬件兼容。 |
| Apple AirPlay 支持 | AirPlay 镜像要求 iPhone/iPad 与接收端在同一 Wi-Fi 网络，用户从控制中心选择屏幕镜像。 | receiver 发现、同网段、mDNS/Bonjour、防火墙和投屏身份必须成为现场 SOP。 |
| Apple AssistiveTouch 指针支持 | iPhone 支持有线鼠标/触控板/蓝牙辅助设备，AssistiveTouch、Pointer Style、Trackpad & Mouse 速度、按钮映射等会影响控制。 | HID 成功必须和 iOS 指针设置、速度、释放、输入法、按键映射一起验，不只看串口写入成功。 |

## 行业主路线判断

对标 XP 的主路线：

```text
真实 iPhone
-> AirPlay/有线投屏/Windows receiver/采集卡取得画面
-> 稳定截图与窗口/设备绑定
-> OpenCV/OCR/图色/坐标校准
-> USB HID 或 XP 专用硬件输入
-> 本地 Kernel API + WebSocket/callback
-> Console/GUI/SDK/脚本
-> JSONL evidence + Acceptance + Readiness
```

辅助路线：

| 路线 | 行业定位 | 本项目处理 |
|---|---|---|
| WDA/Appium/XCUITest | 自家 App 自动化、元素级测试 | 只做辅助测试，不作为 XP 类黑盒群控主线。 |
| MDM/Apple Configurator | 初始化、配置、网络、证书、合规 | 作为设备准备 SOP，不证明业务页面可控。 |
| Shortcuts | 单机系统内流程 | 只做辅助动作或设备初始化，不承载跨 App 黑盒群控。 |
| 越狱/私有 API | 特殊能力探索 | 不作为商业主线，版本和合规风险过高。 |

## 行业壁垒拆解

### 1. Receiver/capture 是第一壁垒

最难不是“能看到一次画面”，而是：

- iPhone 能稳定发现唯一接收端；
- 投屏名、窗口、进程、设备 ID 能绑定；
- 截图非黑屏、非白屏、非旧帧；
- 横竖屏、分辨率、黑边和 safe area 可解释；
- 断线、重连、延迟、CPU/内存、日志能沉淀。

P1 只需要证明 1 台；P2 才做 30 分钟；P3/P4 才谈多设备。

### 2. HID/硬件不是 click API

普通 CH9329 能证明通用 HID 最小闭环，但不能证明：

- XP 专用硬件；
- 4.4 固件；
- 有线投屏自动绑定；
- XP 鼠标参数库；
- 多设备绑定不串线；
- iOS 版本差异已覆盖。

每次 HID 验证必须记录串口、硬件编号、Hub 口、线材、iPhone 型号、iOS 版本、AssistiveTouch 状态、鼠标速度、释放行为和人工观察。

### 3. iOS 设置是控制链路的一部分

P1 前必须逐项核对：

- AssistiveTouch 开启；
- AssistiveTouch menu 显示策略；
- Full Keyboard Access；
- Trackpad & Mouse 是否出现和速度；
- Auto-Lock、亮度、显示缩放；
- 旋转锁和横竖屏纪律；
- 控制中心屏幕镜像入口；
- 同网段和 AirPlay 目标；
- 业务 App 登录态、二维码/扫码策略、输入法。

这些设置只能让测试可开始，不能证明控制成功。

### 4. Kernel/Console/API 分离是产品化信号

XP 和 Some3C 文档都指向一个现实：GUI 不是内核。可产品化系统至少需要：

- Kernel/service 可独立启动和重启；
- Console/GUI 只是 API 客户端；
- HTTP/WebSocket/callback 可复用；
- 请求/响应/错误码有日志；
- 设备、硬件、投屏、分组、用户、配置、快捷指令有统一模型；
- Console 异常时可以只重启 Console 或 Kernel，不能丢 evidence。

当前 Python GUI 应继续作为现场验证台，而不是最终 Windows 产品形态。

### 5. 视觉/OCR 的壁垒是资产和回放

找图/OCR 不要以“调用库成功”为完成标准。真实门槛是：

- 模板有纹理；
- 区域、阈值、语言、主题、亮度可追溯；
- 截图 artifact 可回放；
- 失败分类能进入 Triage/Rerun/Recovery；
- 同一动作能 dry-run、实跑、复跑。

### 6. 群控壁垒是失败隔离

4 台以后，最重要的是“谁坏了、坏在哪、能不能最小复测”。因此所有批量能力必须满足：

- 每台设备有独立 result；
- 单台失败不能让整组请求崩溃；
- 每个 fail 有 device id、component lane、failure category、artifact；
- metrics 和日志能按设备追踪；
- Rerun 决定是否换 run_id；
- Recovery 记录恢复动作，不冒充 Manual pass。

## SOP 总门禁

| 阶段 | 可继续条件 | 停止线 |
|---|---|---|
| P0 知识/离线 | 文档、API tests、GUI helper tests、doctor/readiness 工具存在 | 把 P0 green 写成真实控制成功 |
| P1 单机 | route ready、doctor 无 fail、真实 screenshot quality、click/swipe/type Manual pass、Acceptance PASS、Readiness PASS | 缺 receiver/HID/iPhone/Hub/cable 台账，或缺任何一条真实控制证据 |
| P2 单机稳定 | P1 通过后，30 分钟稳定、metrics、截图成功率、HID 释放、失败分类可解释 | 用 P1 一次成功外推稳定 |
| P3 四台 | 4 台逐设备 evidence、分组批量、单台失败隔离、日志和恢复记录 | 只看聚合成功，不知道哪台失败 |
| P4 十台 | 2 小时稳定、资源曲线、receiver/HID/网络/Hub 问题可复盘 | 用短测或 4 台证据外推商业可用 |
| XP parity | 合法取得 XP 硬件，同场对比 receiver、HID、固件、绑定、鼠标参数、日志、延迟和误差 | 用 CH9329、UxPlay、离线 API 或公开文档替代 XP 侧比 |

## 给研发的下一步优先级

1. 先把 P1 真实 iPhone 跑通，不再新增大面积 GUI 装饰。
2. 确定 receiver 路线：UxPlay、Windows receiver、有线投屏、采集卡至少选一条能被代码稳定截图的路线。
3. 固定 HID 路线：CH9329 先跑最小闭环，同时准备 XP 专用硬件采购和侧比表。
4. 把 iPhone 设置核对从口头 SOP 变成每轮 route/worksheet/transcript 字段。
5. 增加 receiver/HID 日志采集和 per-device 过滤，为 P2/P3 做准备。
6. 视觉/OCR 每个动作必须有 screenshot artifact、template、region、threshold 和 replay。
7. Readiness 继续保持严格：没有真实 evidence 就不能通过。

## 对 GUI 的要求

GUI 层应该服务行业 SOP：

- `Industry` 用来读行业现状和 XP 壁垒；
- `Routes` 用来选 receiver/HID 主路线；
- `Kit Gate` 用来判断今天能否开 P1；
- `iOS SOP` 用来核对手机设置；
- `Rx Score` / `Rx Bootstrap` / `Rx Setup` 用来选、生成替代路线草案并落地 receiver；
- `XP Timeline` / `XP Drill` / `XP Lab` 用来沉淀 XP 迭代、踩坑和硬件对标；
- `P1 Trial` / `Control Bench` / `Acceptance` / `Readiness` 才能闭合真实控制。

任何导出的 GUI Markdown 都是操作台账，不是控制证据。

## 术语口径

| 可以说 | 不能说 |
|---|---|
| 已完成 XP 风格 API/GUI/evidence 离线原型 | 已实现 iOS 完美控制 |
| 已沉淀主流路线和 P1/P3/P4 SOP | 已完成群控产品 |
| CH9329 可作为通用 HID 验证路线 | CH9329 等同 XP 专用硬件 |
| 公开来源显示 XP 强调 Kernel/Console/API、AirPlay、专用硬件和日志 | 我们已经达到 XP parity |
| 某一型号/iOS 通过了同 run_id evidence | 所有 iOS 版本都兼容 |

## 关联文档

- `docs/industry_landscape_2026.md`
- `docs/industry_sop_playbook.md`
- `docs/mainstream_route_decision.md`
- `docs/receiver_capture_selection.md`
- `docs/hid_hardware_protocol_benchmark.md`
- `docs/ios_field_settings_sop.md`
- `docs/gui_xp_iteration_timeline.md`
- `docs/gui_xp_hardware_lab.md`
- `docs/follow_along_test_method.md`
