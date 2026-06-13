# XP 公开来源行动映射

最后检查：2026-06-09 亚洲/上海。

本文把公开的 iMouse XP 和行业信号转化为研发动作、SOP 闸门和 GUI 归属。它仅作为来源情报。它不写 JSONL evidence，不证明真实 iPhone 控制，也不证明 XP 对标。

## 当前定位

iMouse XP 对标仍然是一个黑盒 iOS 控制产品形态：

```text
iPhone 免越狱零安装
-> AirPlay 或有线投屏 receiver
-> 截图/采集管线
-> 图像/OCR 识别
-> USB HID 鼠标/键盘注入
-> 本地 Kernel/Core API
-> 控制台、SDK、脚本、GUI
-> evidence、Acceptance、Readiness、SOP 复盘
```

WDA、Appium、XCUITest、MDM、Apple Configurator 和 Shortcuts 仍然是有用的辅助 lane，但当产品目标是跨 App、系统级、像素驱动的无 iPhone 端 App 群控时，它们不替代 XP 风格的 receiver 加 HID 主线。

## 行动映射

| 公开信号 | 来源 | 研发决策 | SOP 闸门 | 停止线 | GUI 归属 |
|---|---|---|---|---|---|
| iMouse 公开描述专用虚拟鼠标/键盘硬件、AirPlay 镜像、无 iPhone App、Kernel/Core 服务、控制台、HTTP/WebSocket API、OpenCV 找图和 OCR。 | `https://www.imouse.cc/` | 保持 receiver/采集、HID、视觉、API 和 evidence 为独立 lane。不要把主线转向 WDA/Appium。 | P1 必须证明一台真实 iPhone 能被看到、点击、滑动、输入并人工观察。 | 在同一 run 内截图、HID 响应、人工观察、Acceptance 和 Readiness 通过之前，停止所有"iOS 完美控制"声明。 | `Home -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Acceptance/Readiness` |
| 首页宣传广泛的 iPhone/iOS 兼容性，包括当前高端机型和 iOS 世代声明。 | `https://www.imouse.cc/` | 将兼容性声明仅作为测试矩阵输入。建立我们自己的 model/iOS 覆盖表。 | 每个声称的型号加 iOS 组合需要本地 evidence。 | 当精确的 model/iOS/方向组合在 evidence 中缺失时，停止广泛兼容声明。 | `Compat`、`Bench`、`Goals` |
| Python XP 文档说明客户端仅适用于 XP 版且需要专用 iMouse 硬件。 | `https://www.imouse.cc/python-xp/` 和 `https://pypi.org/project/imouse-py/` | 用 SDK 形态设计 client helper，但不要把安装/导入成功当作硬件证明。 | SDK 对标声明之前，固定包版本/hash 并通过 API 测试加真实 receiver/HID/iPhone evidence。 | 如果 helper 调用本地通过但在 iPhone 上没有硬件支持的动作被观察到，停止 SDK 对标声明。 | `Sources`、`Events`、`XP Gap`、`Core` |
| 公开 Python helper 域包括 console 级 device、AirPlay、USB、分组、config、user 和 device 级 image、keyboard、mouse、shortcut、events 和 logging。 | `https://www.imouse.cc/python-xp/` | Backlog 必须基于域，而不是基于按钮。只在 helper 的 evidence 门已知时才实现。 | XP Gap 行必须显示当前阶段的已实现、已测试和有 evidence 支持的状态。 | 如果 config/user/group/callback/log gap 被隐藏在 click/screenshot 演示后面，停止"核心功能完成"声明。 | `Core`、`XP Gap`、`Events`、`Roadmap` |
| XP API 使用本地端口 `9911`、`/api`、HTTP/WebSocket、`msgid`、`status/message/data` 和设备执行码。 | `https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/` | 保持 `/api + fun` 兼容、WebSocket 回显行为和结构化错误分类。 | API 测试必须覆盖成功、设备未找到、硬件未绑定、采集失败、超时和 callback/日志路径。 | 如果 HTTP 200 隐藏了设备、采集、HID 或 callback 失败，停止集成。 | `Events`、`Attach Log`、`XP Gap`、`Verify` |
| XP 新版资料强调 Windows service 分离、控制台/内核重启、有线投屏、4.4 固件、自动绑定、快速投屏、硬解、日志、云分组、子账号、LAN 可见范围和自定义快捷指令。 | XP 帮助镜像和官方帮助页 | 在 P1 之后规划 service/进程/日志/恢复工作，而不是添加更多装饰性 GUI。 | P2/P3 必须收集 metrics、日志、重启记录、receiver/HID 恢复记录和逐设备失败隔离。 | 如果一个设备失败无法隔离到 receiver、采集、HID、校准、视觉、脚本或运维，停止 P3/P4 晋级。 | `Recovery`、`Rerun`、`Dashboard`、`Matrix`、`Roadmap` |
| Apple 通过 AssistiveTouch 支持指针设备，并公开指针样式、跟踪速度、按钮分配、Mouse Keys 和屏幕键盘设置。 | `https://support.apple.com/en-us/111775` | iOS 设置是产品 lane，不是备注。记录 AssistiveTouch、指针速度、鼠标 profile、键盘行为、锁屏/旋转状态和 baseline 截图。 | P1 在 iOS SOP 字段填写且 baseline 截图证明预期手机状态之前不能开始。 | 当 iPhone 设置 profile 未知或未关联到 evidence 时，停止 HID 测试。 | `iOS SOP`、`Kit Gate`、`P1 Trial`、`Control Bench` |
| Apple AirPlay 屏幕镜像是用户级屏幕输出路径，不是 receiver 实现保证。 | Apple AirPlay 支持文档加本地 receiver 测试 | Receiver 选择必须本地测试：UxPlay、Windows receiver、有线投屏或采集卡备选。 | Doctor 必须通过 receiver 检查且截图质量必须非空且可重复，然后才能进行 HID 控制测试。 | 当采集为黑屏、过时、错窗口、裁剪或未绑定到一个设备 ID 时，停止真实运行控制。 | `Receiver`、`Shot Bench`、`Local`、`Doctor` |
| PyPI 还包含 `imouse-xp 0.0.7` 和 `py-imouse-xp 1.0.1`，与 `imouse-py 0.0.4` 分开。 | `https://pypi.org/project/imouse-xp/`、`https://pypi.org/project/py-imouse-xp/`、`https://pypi.org/project/imouse-py/` | 将包名视为漂移和供应链信号。使用任何包之前审查命名空间、维护者、来源、hash、API 形态和许可证。 | 包采用需要固定版本、hash、来源审查、本地 API 回归测试和硬件支持的 smoke evidence。 | 如果包身份、来源或 API 形态不清楚，停止依赖采用。不要在未固定 artifact 的情况下在现场机器上安装包。 | `Sources`、`XP Gap`、`Local`、`Verify` |
| XP 价值从单个命令成功转向群组操作、日志、恢复、账号/权限和可重复 SOP。 | iMouse 公开文档、XP 帮助镜像和本地 SOP 文档 | 让 P1/P2/P3/P4 阶段门明确。产品化在 evidence 之后，而不是之前。 | P3 需要 4 台设备逐设备 evidence 和失败隔离。P4 需要更长的稳定性 metrics 和恢复日志。 | 当一个设备的 evidence 被外推到多台设备时，停止群控声明。 | `Dashboard`、`Matrix`、`SOP`、`Pack`、`Goals` |
| 公开 API/来源文档可能过时或宣传性。 | 所有公开来源 | 保持来源声明在台账中，保持验收声明在 JSONL evidence 中。 | 每个公开声明必须映射到路线字段、测试、artifact 和停止线才能影响范围。 | 当仅有来源的声明没有本地验证路径时，停止研发决策。 | `Sources`、`Operator Home`、`Goal Gate` |

## 现场 SOP 转化

P1 真机运行前：

1. 打开 `Home`，确认操作工作流从 Route/Kit 开始，而不是"全部运行"。
2. 打开 `Sources`，确认每个公开信号都有验证缺口或 evidence 支持的状态。
3. 打开 `Kit Gate`，填写 receiver、HID、iPhone、Hub、线材、网络和备用硬件字段。
4. 打开 `iOS SOP`，记录 AssistiveTouch、指针速度、键盘行为、旋转锁、锁屏策略、二维码扫描策略和 baseline 截图预期。
5. 打开 `Receiver` 和 `Shot Bench`；在截图是最新、非空且绑定到正确设备之前不要测试 HID。
6. 打开 `P1 Trial`；只在路线和 Doctor 通过后才点击、滑动和输入。
7. 每次 HID 动作后记录人工观察。API 成功但没有可见 iPhone 响应是失败分类。
8. 运行 `Acceptance` 和 `Readiness`；只有这些门能把 run 推向 P2。

## 包注册表边界

包注册表数据对 API 漂移和命名空间风险有用：

| 包 | 公开信号 | 研发用途 | 边界 |
|---|---|---|---|
| `imouse-py` | 公开版本信号 `0.0.4`，发布于 2025-11-16；仅限 XP 硬件支持的定位。 | 主要 SDK 形态参考。 | 导入/安装不证明硬件、receiver、HID 或 iPhone 响应。 |
| `imouse-xp` | 公开版本信号 `0.0.7`，发布于 2025-08-10。 | 需要来源审查时比较包命名空间和 API 形态。 | 除非固定、审查、测试和有硬件支持，否则不是证明来源。 |
| `py-imouse-xp` | 公开版本信号 `1.0.1`，发布于 2025-09-05；客户端库定位，具有 HTTP/WebSocket 风格控制语言。 | 关注命名/API 漂移和依赖混淆风险。 | 在来源、维护者、hash 和行为被审查之前视为第三方。 |

## 研发优先级

1. P1 证明：一台真实 iPhone、一条 receiver 路线、一条 HID 路线、截图、点击、滑动、文本输入、人工观察、Acceptance、Readiness。
2. XP 对标硬件：购买或借用一套 XP 硬件；记录型号、固件、授权、绑定流程、鼠标 profile 和日志。
3. Receiver/采集 bench：通过截图稳定性和设备绑定比较 UxPlay、Windows receiver、有线投屏和采集卡备选。
4. HID bench：通过释放行为、坐标误差、输入法行为和恢复比较 CH9329、XP 硬件和未来自研 HID。
5. 可观测性：按设备 ID 保留请求/响应、callback、receiver、HID、采集、截图和人工观察 artifact。
6. P3/P4 群控：只在 P1/P2 evidence 可重复后才扩规模；每个失败必须隔离设备加组件。

## 非证据边界

本映射是必需的规划资产。缺失时会阻断就绪，但它本身不能通过就绪。真实 iOS 控制的唯一有效证明路径是带有 JSONL evidence、artifact、人工观察、Acceptance 和 Readiness 的真机运行。

## 来源链接

- https://www.imouse.cc/
- https://www.imouse.cc/python-xp/
- https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/
- https://pypi.org/project/imouse-py/
- https://pypi.org/project/imouse-xp/
- https://pypi.org/project/py-imouse-xp/
- https://support.apple.com/en-us/111775
- https://support.apple.com/en-us/102661
