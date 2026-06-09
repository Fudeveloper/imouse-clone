# iMouse XP 对标研发作战手册

更新时间：2026-06-09

本文是给研发、采购和现场测试一起看的总手册。它优先沉淀行业知识、SOP、主流路线和踩坑点；代码和 GUI 只是验证这些判断的工具。

现场逐步跟测入口：`docs/follow_along_test_method.md`。每轮测试先按该文件建立 `run_id`、锁定 receiver/HID/iPhone/Hub/cable，再使用 GUI 的 `Verify`、`Local`、`Coach`、`Transcript`、`Acceptance`、`Readiness` 和 `Pack` 完成闭环。当前行业现状快照和采购/现场 SOP 决策表见 `docs/industry_current_state_snapshot_2026.md`。

## 公开信号复核

本轮复核时间：2026-06-09。

| 来源 | 当前公开信号 | 对研发的含义 |
|---|---|---|
| `https://www.imouse.cc/` | 官网首页继续强调 iMouse 虚拟鼠键硬件、AirPlay 镜像、iPhone 端无需安装 App、Kernel/Console、HTTP/WebSocket API、OpenCV 找图和 OCR；同时有 iPhone17、iOS 26.4 这类最新兼容宣传。 | 架构主线仍是 receiver/capture + HID + vision + API + evidence；兼容宣传只能进本地 Device/iOS Matrix，不能外推为我们已兼容。 |
| `https://www.imouse.cc/python-xp/` | Python XP 文档说明仅适用于 XP 版，标准 iOS 无越狱、无需手机端 App，但必须配套 iMouse 硬件；helper 分为 console 和 device，覆盖 Device、AirPlay、USB、Group、ImConfig、User、Image、KeyBoard、Mouse、Shortcut 和事件回调。 | 我们的对标重点不是 Appium 式元素自动化，而是“内核服务 + 硬件 + 投屏 + 图色 + API/SDK”的整套链路。 |
| `https://www.imouse.cc/XP版API文档/` | XP API 支持 HTTP 和 WebSocket，端口 `9911`，HTTP 入口 `/api`，支持 GET、POST JSON、POST 表单；WebSocket 用 `msgid` 对应异步结果；返回 `status/data/code`。 | 当前 `XpApiClient` 和 `/api + fun` 兼容方向正确，已补 WebSocket `/api`、callback ledger 初版，以及截图 multipart/binary/save_path；还要继续补真实 receiver/HID 事件和更多官方 fun 覆盖。 |
| `https://www.imouse.cc/XP版帮助文档/` | 首次配置和鼠标参数资料把手机设置、旋转/锁屏、AssistiveTouch/全键盘、投屏身份、鼠标参数/通用库和二维码扫描策略放在控制链路前面。 | 这些属于现场 SOP，已进入 GUI `iOS SOP` 和 Route Decision；它们只能开放测试，不能证明真实控制。 |
| `https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version` | XP 新版资料强调 Windows 10+、8GB+、硬件加速优先；Core/Console 分离，Kernel 是 Windows service；Console 异常时通常重启 Kernel。 | 产品化不能只做 GUI。P2/P3 后必须做服务化、日志、重启、权限和运维控制台。 |

## 行业主流路线结论

对标 iMouse XP，主线应保持：

```text
iPhone 免越狱零安装
-> AirPlay/有线投屏/receiver 取画面
-> 截图采集
-> 图色/OCR/模板识别
-> USB HID 鼠标键盘注入
-> 本地内核服务 API
-> GUI/SDK/脚本调度
-> evidence/acceptance/readiness 验收
```

不建议把 WDA/Appium/XCUITest 当主线。它们适合自家 App 测试，优点是元素定位和断言清楚；但不符合 XP 类产品“手机端零安装、跨 App、跨系统 UI、黑盒像素级控制”的目标。MDM、Apple Configurator、快捷指令适合作为设备初始化和合规配置辅助，不是像素级群控方案。

## 三条研发线

| 线 | 目标 | 当前状态 | 下一步 |
|---|---|---|---|
| P1 最小闭环 | 一台 iPhone 能看、能点、能滑、能输，并留下证据 | GUI、API、script、doctor、evidence、acceptance 已有离线闭环；无真实 iPhone evidence | 选定 receiver 和 HID，按 Live Probe 跑实机 |
| XP 对标线 | 专用硬件、4.4 固件、有线投屏、自动绑定、Windows service、硬解、多窗口 | 仅有公开资料拆解和原型替代路线 | 尽早采购 XP 硬件，同场对比 CH9329 |
| 群控产品线 | 4 台、10 台、20+ 的稳定、日志、分组、失败隔离 | 本地分组和批量 API 原型已做；未实机 | P1/P2 通过后进入 P3/P4，不提前扩台 |

## P1 开测决策

### Receiver 只能先选一条

| 路线 | 可进入 P1 的最低条件 | 不能接受的情况 | 必填 evidence |
|---|---|---|---|
| UxPlay | doctor 不再有 `binary:uxplay` fail；iPhone 能发现唯一接收端；截图非黑屏 | 只能看见窗口但代码采不到图 | provider、版本、路径、启动命令、AirPlay 名称、截图质量 |
| Windows Receiver | 窗口/进程/句柄可固定绑定；能被截图链路采集 | 只适合人工看屏、没有可自动采集画面 | provider、版本、窗口标题、进程、capture method、许可证状态 |
| 有线投屏/专用驱动 | 能拿到帧或稳定窗口；设备唯一标识可追踪 | 闭源 UI 无日志、无采集接口、无法绑定设备 | 驱动版本、线材、端口、采集方式、延迟和断线记录 |
| 采集卡 | 可作为截图质量对照 | 不能证明 XP 式自动绑定，也不宜当主线 | 采集卡型号、延迟、分辨率、稳定性 |

### HID 先证明真实响应

| 路线 | P1 作用 | 关键风险 | 必填 evidence |
|---|---|---|---|
| CH9329/通用 HID | 低成本验证 iOS 指针/键盘最小闭环 | 坐标、释放、滑动、输入法、多设备稳定性要自研 | 串口、固件/模块编号、Hub 口、线材、50 次点击释放 |
| XP 专用硬件 | 最接近对标目标 | 协议、授权、固件不可控 | 硬件编号、固件版本、授权状态、是否暴露串口/API、同场误差 |
| 自研 HID | 产品化长期方向 | 周期长，需要固件能力 | 固件版本、设备唯一 ID、HID report 能力 |
| 蓝牙 HID | 只做探索 | 多台配对和断连管理复杂 | 不作为主线 |

## P1 现场 SOP

1. 生成现场执行包：`python -m imouse.field_packet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1`。
2. 打开 `docs/gui_live_probe.md`，按 Live Probe 的 `Prepare -> Edit -> Checklist -> Validate -> Doctor -> Dry Run` 做开测前检查。
3. 路线表里不能留 `EDIT_ME`、`TODO`、`COM_EDIT_ME` 或共享硬件编号。
4. 设备、receiver、capture、HID、Hub、线材、iPhone、iOS 必须一一编号。
5. doctor 有 fail 时停止，不进入“实机通过”判断。
6. 接入真实 iPhone 后，先证明投屏和截图质量，再做点击/滑动/输入。
7. 点击、滑动、输入后必须由操作者在 GUI `Manual` 中记录真实 iPhone 观察。
8. GUI `SOP` Board 只作为阶段执行台；它能告诉操作员缺什么证据，但不能替代 JSONL evidence。
9. `Acceptance` FAIL 时点 `Gap`，逐项补 component metadata、screenshot quality、manual observation 或 metrics。
10. 每次失败后按 `Triage -> Rerun -> Recovery` 处理：先分类，再决定最小复测路径，最后执行 receiver/HID/校准/群控/性能恢复演练。
11. `Readiness` P1 PASS 前，不允许进入 P2/P3。
12. 如果路线校验失败并写入 evidence，这个 run_id 只用于复盘；修复后换新 run_id。

## P1 到 P3 的晋级门

| 阶段 | 必须证明 | 不允许用来替代 |
|---|---|---|
| P1 | 单台 iPhone 投屏、截图、校准、点击、滑动、输入、人工观察和组件台账 | API success、dry-run、路线表通过 |
| P2 | 单台 30 分钟稳定，截图成功率、HID 失败、资源指标可解释 | P1 的一次性成功 |
| P3 | 4 台设备的分组、批量动作、失败隔离和逐设备 evidence | 单台稳定外推 |
| P4 | 10 台 2 小时稳定，资源、网络、Hub、receiver 断线都有记录 | 4 台短测外推 |

## 常见坑和分流

| 现象 | 优先归类 | 先查什么 | 证据要求 |
|---|---|---|---|
| iPhone 看不到接收端 | `airplay_discovery` | 同网段、AP 隔离、Bonjour/mDNS、防火墙、接收端名称冲突 | 网络说明、receiver 日志、手机侧照片/录屏 |
| 投屏黑屏/白屏/花屏 | `airplay_stream` 或 `capture` | receiver 版本、窗口绑定、锁屏、分辨率、采集区域 | 截图 artifact、screenshot_quality、receiver 元数据 |
| API 成功但手机没动 | `hid` | 串口、HID 绑定、OTG、AssistiveTouch、硬件供电、按下释放 | 人工 fail、HID 编号、串口日志、视频 |
| 坐标偏移 | `calibration` | active area、target size、横竖屏、safe area、黑边 | 五点误差表、校准 profile、截图 |
| 找图误判 | `vision_template` | 模板纹理、区域、阈值、主题/亮度变化 | 模板文件、失败截图、阈值 |
| OCR 不稳定 | `ocr` | 模型缓存、区域、语言、截图清晰度 | OCR 输出、截图、耗时 |
| 4 台里一台卡住 | `group_dispatch` 或 `isolation` | 设备 ID 映射、Hub 口、receiver 绑定、HID 绑定 | 逐设备结果和失败设备 ID |
| 长跑后掉线 | `performance` | CPU、内存、receiver 进程、网络、Hub 供电 | metrics、断线次数、receiver 日志 |

## GUI 应该承载什么

P1 阶段 GUI 不追求“漂亮多窗口控制台”，先做现场验证台：

- 设备注册、硬件绑定、receiver/capture 入口。
- 截图预览、取点、模板裁剪、找图、找色、OCR。
- Route Decision、Field Packet、Acceptance、Gap、Readiness。
- Live Probe 状态表。
- GUI Control Center 总控层，用一张表串联设备范围、Route/Doctor、真实 iPhone evidence、Callback/Attach Log、Scenario/Queue、Vision assets、Evidence Pack、SOP Board 和 Promotion boundary。
- GUI First Run Packet 首测包，把 Sources、Industry、Roadmap、Verify、Core、Routes、Pitfalls、Compat、Goals、Kit Gate、iOS SOP、Bench、Wizard、P1 Trial、脚本命令、Acceptance、Readiness 和 handoff 边界合成一张现场执行表。
- GUI Field Kit Gate 采购/现场准备闸门，在真实 P1 开跑前集中检查采购/SOP 文档、设备范围、receiver、HID、iPhone 设置、Hub/线材/网络、证据计划、Route/Doctor 停线和 XP 硬件对比边界。
- GUI iOS Field Settings SOP 真实手机设置核对表，在 Kit Gate 和 Bench 之间确认 AssistiveTouch、rotation lock、AssistiveTouch menu、Full Keyboard Access、Trackpad & Mouse、mouse parameter profile、QR scan policy、锁屏/亮度、网络/AirPlay、Hub/Cable、baseline screenshot 和 manual observation 边界。
- GUI Knowledge Center 知识层，用一张表把 XP 公开模型、行业主流路线、P1 路线决策、现场 SOP、硬件坑点、API/helper 差距、迭代问题和 claim boundary 映射到 GUI 下一步动作。
- GUI Industry SOP Radar 行业雷达，把行业主流路线、XP 产品壁垒、iPhone 现场设置、receiver/HID/视觉/运维/扩容和声明边界映射到当前状态、证据门、停止线和 GUI 下一步动作。
- GUI XP Architecture Map 架构拆解图，把 XP 公开实现信号拆成产品边界、硬件/HID、投屏/receiver、截图/视觉/OCR、Kernel/API、Python helper、Console/GUI、evidence/readiness 和群控运维层。
- GUI Mainstream Route Matrix 主流路线矩阵，把 XP 式黑盒控制、UxPlay/Windows/wired/capture receiver、CH9329/XP hardware HID、WDA/Appium 和 MDM/Shortcuts 的定位、证据门和停止线放到同一张表。
- GUI Verification Walkthrough 逐步验证工作台，把 P0/P1/P2/P3/P4 的命令、GUI 路径、预期、证据和停止线放到一张表，保证现场人员按顺序验证而不是跳过阻断项。
- XP Core Function Matrix 核心功能覆盖矩阵，把 API/SDK、receiver、截图、HID、校准、视觉、脚本、GUI、可观测性和商业运维拆成本地实现、证据门、XP Gap 状态和下一步动作，防止把 local ready 当成实机通过。
- GUI Pitfall Library 坑点库，把 receiver、HID、校准、视觉、群控隔离、性能稳定、业务状态、claim boundary 和 XP 硬件对标风险映射到首个探针、停止线和 GUI 下一步动作。
- GUI SOP Problem Ledger 问题沉淀台账，把行业坑点、Issue Triage 失败类别、Rerun 最小重跑规则、fresh run_id 判断、证据保留项和停止线合成长期 SOP 资产。
- GUI Capture Quality Bench 连续截图质量压测，先证明 receiver/capture 路线能稳定拿到可用画面。
- GUI Control Response Bench 控制响应审计，区分 API/HID 命令 ready、Manual pass、Manual fail 和 command fail，防止把软件命令成功当成 iPhone 真响应。
- Attach Log triage 把 receiver/HID/capture/USB/device 文本日志分流成 callback rows，并在 `Record` 开启时写入 JSONL，供 Triage/Rerun/Recovery 使用。
- XP Public Source Ledger 来源审计层，用一张表把官网、Python XP、XP API 和 XP 帮助页的公开说法映射到可信层级、研发影响和验证缺口，防止把宣传口径当成本地验收结论。
- XP Iteration Radar 迭代雷达，把 XP 公开迭代路径、踩坑点和产品化重点转成研发优先级、SOP 测试路径和停止线。
- XP Iteration Timeline 迭代时间线，把 XP 公开演进信号按产品阶段拆成实现假设、踩坑点、研发借鉴、SOP 闸门和停止线；它只用于行业知识沉淀，不能替代真实 iPhone JSONL 证据或 XP 硬件侧比。
- XP Roadmap 研发闭环路线图，把 XP 公开信号、行业 SOP、本地实现、证据门和下一步动作压成 P0-P4/XP parity lanes，防止把 local ready 当成对标完成。
- Device/iOS Compatibility Matrix 本地兼容覆盖层，用一张表按 iPhone model + iOS version 聚合 evidence，只允许对有本地证据的精确机型/系统组合做阶段覆盖判断。
- SOP Board 八步执行台、`Run Selected` 主命令和 Markdown 导出。
- Scenario Library 阶段脚本选择，默认 dry-run，防止现场手选错脚本。
- Field Runbook 现场执行向导，把设备范围、Route、Doctor、截图、HID、视觉、场景、Guard、metrics、Triage、Acceptance/Readiness 串成一张可导出的停止线清单。
- Evidence Timeline 事件流水，用于逐条核对设备、失败分类和附件。
- Device Evidence Matrix 按设备核对证据覆盖，用于 P3/P4 防止漏测单台设备。
- Issue Triage 按失败类别沉淀问题、影响设备、附件和下一步 SOP 动作。
- Rerun Playbook 把失败类别和 Route/Doctor/Acceptance/Readiness gate 转成最小重跑动作、fresh run_id 规则、证据保留项和停止线。
- Recovery Drill 把 receiver/capture、HID、校准、视觉/业务状态、群控隔离、performance watchdog 和 handoff 边界转成恢复步骤、验证步骤、证据保留项和停止线，并可用 `Record Pass` / `Record Fail` 写入恢复执行证据；真实控制仍必须通过 Manual/P1 Trial、Acceptance 和 Readiness 闭合。
- Real-run Guard 在取消 dry-run 前拦截路线、Doctor 或设备范围不满足的实跑。
- 每个动作自动记录 evidence，人工观察必须可分类、可附 artifact。

P2/P3 后才做：

- 多窗口实时画面网格。
- 设备状态列：投屏、HID、截图、校准、最后错误。
- 真实 receiver 日志过滤已具备离线分流和 JSONL 记录入口；自动重连、实时 tail、多设备日志过滤和恢复结果自动写证据仍需继续做。
- 快捷键、分组脚本、失败截图自动采集。
- Windows service 化、配置、账号/权限、自动更新。

## 当前未完成结论

当前仓库不能证明：

- 真实 iPhone 已被完美控制。
- UxPlay/Windows Receiver/有线投屏任一路线在本机通过。
- CH9329 或 XP 专用硬件已经控制 iPhone。
- XP 4.4 固件、自动绑定、硬解、多窗口分离已经实现。
- 4 台、10 台、20+ 群控已稳定。

当前仓库可以证明：

- 对标路线、SOP、阶段门和证据模型已形成。
- Python GUI 已能承载 P1/P3 前的现场验证流程。
- XP 风格 API、SDK、脚本、evidence、acceptance、readiness 可以离线验证。

## 下一轮硬件实测清单

最小 P1 物料：

- 1 台已解锁并配置好的 iPhone。
- 1 套 CH9329 或等价 HID。
- 1 套稳定 OTG/转接线。
- 1 个可落地 receiver 路线。
- 1 个备用 HID/线材/Hub 口，用于交叉排查。

强烈建议：

- 采购 1 套 XP 专用硬件，同场记录固件、自动绑定、鼠标模式和输入体验。
- 如果 UxPlay 在 Windows 上继续阻塞，优先验证 Windows Receiver 或有线投屏能否被代码稳定截图。
