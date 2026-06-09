# 投屏与截图采集路线选型矩阵

更新时间：2026-06-08

目标：把 iMouse XP 版对标里最关键、也最容易走弯路的“怎么看到手机画面、怎么稳定截图、怎么扩到多台”拆成可决策、可实测、可复盘的路线。当前仓库默认实现是 UxPlay 原型，但它不能直接代表 XP 产品级投屏能力。

## 结论先行

- P1 单台实机必须先选定一条投屏/采集路线，不要一边用 UxPlay，一边手工截图，一边又用第三方投屏窗口混跑。
- 当前 Python 原型的默认路线是 `UxPlay -> 窗口/显示采集 -> OpenCV/OCR`，本机 doctor 已确认 `uxplay` 缺失，所以默认路线还没有实机验证。
- 对标 iMouse XP 时，最终路线大概率要走 Windows 产品级 receiver 或有线投屏/硬解专项；UxPlay 更适合 P0/P1 证明链路。
- 任何 receiver 能不能用，都只看证据：非黑屏截图、固定尺寸、重连耗时、100 次截图成功率、CPU/内存曲线、失败日志、设备 ID 追踪。
- 投屏路线的验收不能只看“iPhone 能看到接收端”。群控真正吃亏的地方在多设备、窗口绑定、采集帧率、断线恢复和资源占用。

## 公开资料约束

这些公开资料决定了本项目的对标方向：

- iMouse XP Python 文档明确 XP 版需要配套专用硬件，并提供 Device、AirPlay、USB、Group、Image、Mouse、Keyboard 等 helper 能力。
- iMouse XP API 文档说明本地服务端口为 `9911`，支持 HTTP 和 WebSocket，并有设备、配置、鼠标键盘、图色、回调等分类。
- XP 新版资料把软件拆成 Core 和 Console，其中 Core 是无界面的 Windows 服务，负责硬件和手机通信。
- Apple 官方 AirPlay 文档说明 iPhone/iPad 可通过 AirPlay 镜像屏幕，且镜像时通常要求设备与接收端在同一 Wi-Fi 网络。
- UxPlay 是开源 AirPlay 镜像接收器，依赖 GStreamer 渲染管线，可作为早期验证组件，但它的安装、窗口采集和多设备资源曲线仍需单独验证。

资料只说明“路线可成立”，不说明“我们的环境已通过”。所有结论必须回到 evidence。

## 路线总览

| 路线 | 推荐阶段 | 价值 | 最大风险 | 是否接近 XP |
|---|---|---|---|---|
| UxPlay + 窗口/显示采集 | P0/P1 | 开源、可控、便于 Python 集成 | Windows 安装复杂，窗口句柄/黑屏/编解码问题多 | 中 |
| Windows 商业/专用 AirPlay Receiver + 窗口采集 | P1/P2 | 更接近现场 Windows 使用形态 | API 不透明、授权和窗口采集不稳定 | 中高 |
| 有线投屏/专用驱动 + 截图采集 | P2/P3 | 低延迟、弱依赖 Wi-Fi，可能支持自动绑定 | 驱动闭源、采集接口不确定、采购门槛高 | 高 |
| HDMI 转接 + 采集卡 | P1 辅助/P2 对照 | 画面链路直观，适合做截图质量对照 | 线材多、延迟和成本高，不等于 XP 自动绑定 | 中 |
| macOS AirPlay Receiver | P1 诊断 | 快速验证 iPhone AirPlay 本身是否正常 | 不适合作为 Windows XP 对标主线 | 低 |
| WDA/Appium/XCUITest 截图 | 测试辅助 | 可做自家 App 验证和坐标校准辅助 | 手机端部署和权限要求，不符合 XP 黑盒主线 | 低 |

## 选型评分表

每条路线进入 P1 前先按 1-5 分打分，低于 24 分不要扩到多台。

| 指标 | 权重 | UxPlay | Windows Receiver | 有线投屏 | HDMI 采集 |
|---|---:|---:|---:|---:|---:|
| 安装可复制 | 3 | 待测 | 待测 | 待测 | 待测 |
| 截图非黑屏稳定 | 5 | 待测 | 待测 | 待测 | 待测 |
| 断线恢复可控 | 5 | 待测 | 待测 | 待测 | 待测 |
| 多设备资源占用 | 5 | 待测 | 待测 | 待测 | 待测 |
| Python 可集成 | 4 | 待测 | 待测 | 待测 | 待测 |
| 窗口/设备绑定可追踪 | 5 | 待测 | 待测 | 待测 | 待测 |
| 许可证和交付风险 | 3 | 待测 | 待测 | 待测 | 待测 |
| XP 体验接近度 | 4 | 待测 | 待测 | 待测 | 待测 |

记录模板：

```text
路线:
组件名称:
版本:
安装路径:
启动命令:
AirPlay 名称:
采集方式:
截图 API/窗口句柄:
单台 100 次截图成功率:
重连耗时:
CPU/内存峰值:
失败分类:
证据路径:
是否允许进入 P1/P2:
```

## 路线 1：UxPlay 原型

适用：

- P0/P1 单台闭环。
- 需要开源组件验证 AirPlay + 截图 + 图色/OCR 的最小链路。
- 团队需要理解 AirPlay discovery、receiver 日志、窗口采集、黑屏判断这些基础坑。

当前状态：

- 代码里已有 `imouse.airplay` 和 `imouse.doctor` 对 UxPlay 的检查。
- 当前机器 `doctor` 预期失败点是 `binary:uxplay`。
- 在安装并接入 UxPlay 前，不能声称当前投屏路线可用。

P1 验收：

1. `.\.venv\Scripts\python -m imouse.doctor --markdown evidence\<run_id>_doctor.md` 不再因 `uxplay` 缺失阻断，或明确记录替代 receiver。
2. GUI `Start AirPlay` 后，iPhone 能看到唯一且可识别的接收端名称。
3. `Screenshot` 连续 100 次非黑屏、非纯白、尺寸稳定。
4. 断开 AirPlay 后手动重连 5 次，记录每次耗时。
5. 运行 `scripts\p1_single_device_control_probe.json` 实跑并产生 evidence；如果只排查投屏/采集，再运行 `scripts\p1_receiver_capture_probe.json`。

主要坑：

- Windows 上安装链路比 Linux/macOS 更复杂，可能涉及 MSYS2/GStreamer/防火墙。
- 多台设备每台一个 receiver 进程时，CPU、内存、窗口管理会快速成为瓶颈。
- receiver 窗口能看见画面，不代表截图 API 抓到的是同一画面。
- H264/H265、显卡驱动、GStreamer sink 选择会影响黑屏和花屏。

研发动作：

- 保留 UxPlay provider，但不要把 GUI 绑定死到 UxPlay。
- 抽象 `CaptureProvider`：`start`、`stop`、`screenshot`、`health`、`logs`、`reconnect`。
- evidence 中强制记录 `receiver_provider=uxplay`、版本、启动命令和日志路径。

## 路线 2：Windows Receiver

适用：

- P1 如果 UxPlay 安装受阻，可以用来先拿真实 iPhone 投屏和截图证据。
- P2/P3 评估 Windows 产品级交付路线。
- 对标 XP Core/Console 的 Windows 使用形态。

必须确认：

- 接收器是否允许商业使用。
- 是否能固定 AirPlay 名称。
- 是否能稳定暴露窗口标题、窗口句柄或截图接口。
- 多开方式是一个进程多设备，还是每台设备一个进程。
- 日志能否按设备拆分。

P1 验收：

1. 记录 receiver 名称、版本、安装路径、许可证状态。
2. iPhone 手动投屏到指定 receiver。
3. 用当前 GUI 或临时采集脚本抓到真实截图。
4. 100 次截图质量通过。
5. failure evidence 明确写 `receiver_provider=windows_receiver`。

主要坑：

- 商业 receiver 往往能显示，但不提供稳定截图接口。
- 窗口标题可能随语言、设备名、重连变化。
- 多设备窗口排列变化会导致截图绑定错设备。
- 自动更新可能改变窗口类名、渲染方式或许可证行为。

研发动作：

- 增加窗口枚举和绑定表：`device_id -> receiver window handle/title/process id`。
- GUI 设备表增加 receiver 状态列：`provider`、`window`、`last_frame_at`、`last_error`。
- 对每个 receiver 版本做截图回归，不允许无记录升级。

## 路线 3：有线投屏/专用驱动

适用：

- P2/P3 开始追求 XP 类低延迟、稳定性和自动绑定。
- 无线 AirPlay 因网络、mDNS、防火墙或多设备资源成为瓶颈。
- 已能稳定完成单台和 4 台试点，需要向 10 台以上扩展。

必须确认：

- 是标准系统能力、厂商驱动，还是 XP 专用硬件/固件的一部分。
- 能否拿到截图帧，还是只能看窗口。
- 是否支持设备唯一 ID 与 HID 自动绑定。
- 是否有 SDK/API、日志、错误码和重连控制。

P2 验收：

1. 同一台 iPhone 分别跑 AirPlay 和有线投屏，对比截图成功率、延迟、CPU/内存。
2. 断线/拔线/锁屏/旋转各 10 次，记录恢复策略。
3. 4 台并发 30 分钟，所有截图和 HID 操作可追踪到设备 ID。
4. 若声称自动绑定，必须给出从“接线到设备/HID 绑定完成”的完整日志。

主要坑：

- 闭源驱动可能短期跑通，长期卡在授权、崩溃和升级。
- 自动绑定若只有 UI 表象，没有可读设备 ID，后续无法做稳定调度。
- 有线链路会把 Hub 供电、接口类型、转接线质量放大成核心风险。

研发动作：

- 把有线投屏作为 provider 接入，不要重写 GUI。
- 台账增加 `capture_link`、`cable_id`、`driver_version`、`auto_bind_evidence`。
- P2 以后所有稳定性报告都必须区分无线/有线数据。

## 路线 4：HDMI 转接 + 采集卡

适用：

- 做截图质量对照。
- 排除 AirPlay receiver 导致的黑屏、花屏、色彩偏差。
- 在软件 receiver 不稳定时，临时拿到视觉算法样本。

不适用：

- 不适合作为 XP 软件产品主线。
- 不适合证明自动绑定。
- 不适合高密度群控，线材、转接、采集卡成本太高。

验收价值：

- 对同一页面保存 AirPlay 截图和采集卡截图，比较尺寸、黑边、色彩、延迟。
- 用采集卡截图验证模板资产是否本身可靠。
- 若 AirPlay 黑屏但采集卡正常，优先排 receiver/编解码。

## P1 推荐执行顺序

1. 先决定 P1 路线：`UxPlay` 或 `Windows Receiver`。
2. 按 `hardware_test_bench_checklist.md` 给 iPhone、HID、线材、Hub、AirPlay 名称编号。
3. 跑 doctor，保存 `evidence\<run_id>_doctor.md`。
4. 启动 receiver，记录版本、路径、启动命令。
5. iPhone 手动连接 AirPlay。
6. 在 GUI 中注册 `dev_1`，绑定 receiver 和 HID。
7. 截图 1 次，人工确认不是黑屏。
8. 截图 100 次，统计成功率和耗时。
9. 做五点校准。
10. 跑点击、滑动、输入、找图、找色、OCR。
11. 生成 evidence summary。
12. 跑 `python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1`，不通过就不扩到 4 台。

## 失败分类

| 分类 | 现象 | 优先排查 |
|---|---|---|
| `airplay_discovery` | iPhone 找不到接收端 | 同网段、AP 隔离、防火墙、mDNS、服务名 |
| `airplay_pairing` | 能看到但连不上或验证码失败 | receiver 日志、系统权限、同名设备 |
| `airplay_stream` | 黑屏、花屏、卡住、断线 | 编解码、receiver 版本、GPU、锁屏、网络 |
| `capture` | receiver 有画面但截图错 | 窗口句柄、DPI、遮挡、最小化、采集 API |
| `capture_quality` | 截图纯黑/纯白/低纹理 | 画面源、黑边裁剪、质量检查阈值 |
| `binding` | 截图和 HID 对不上设备 | 设备台账、窗口绑定、串口绑定、分组 |
| `performance` | 多台后掉帧或延迟飙升 | CPU、内存、GPU、GStreamer sink、进程数 |

## 不允许进入下一阶段的情况

- 没有 receiver 版本和路径记录。
- 只有人工口头说“能看到”，没有截图文件。
- 100 次截图没有统计。
- 截图与 device_id 无法对应。
- 断线恢复没有测试。
- 失败截图没有保存。
- 使用了替代 receiver，但 evidence 没记录 provider。
- doctor 失败被忽略，没有人工说明替代链路。

## 和当前仓库的接口对应

| 需求 | 当前仓库入口 | 后续增强 |
|---|---|---|
| 环境检查 | `python -m imouse.doctor --route-decision evidence\<run_id>_route_decision.json` | 增加更多 provider-specific runtime probes |
| 启停 UxPlay | GUI AirPlay / `/airplay/connect` | provider 抽象 |
| 截图 | GUI Screenshot / `/api/screenshot` | 窗口句柄绑定和帧率统计 |
| 截图质量 | script runner screenshot step | GUI 批量质量测试按钮 |
| evidence | GUI / `imouse.validation` | 自动写 receiver 元数据 |
| 阶段门 | `python -m imouse.acceptance` | provider-specific checks |

`--route-decision` 只检查 receiver provider 配置是否可预检。它可以让 Windows Receiver、有线投屏或采集卡路线不再被默认 `uxplay` 缺失阻断，但不能替代截图质量、人工观察和 readiness。

GUI `Receiver` / Receiver Route Gate 把这条规则变成现场面板：同一张表显示 Route Decision 是否加载/校验、provider 是否可预检、`binary:uxplay` 是否因为替代路线降级、窗口/采集绑定是否明确、以及截图/人工观察/Readiness 是否仍然缺失。该面板不写 JSONL evidence，也不证明真实 iOS 控制。

## 参考资料

- iMouse XP Python 文档：`https://www.imouse.cc/python-xp/`
- iMouse XP API 文档：`https://www.imouse.cc/XP版API文档/`
- Some3C iMouse XP New version：`https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version`
- Apple AirPlay 屏幕镜像文档：`https://support.apple.com/en-us/102661`
- UxPlay 项目：`https://github.com/FDH2/UxPlay`
