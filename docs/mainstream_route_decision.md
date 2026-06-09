# iOS 群控主流路线与 P1 决策表

更新时间：2026-06-08

目标：把行业主流路线、iMouse XP 公开信号、前期 Python GUI 原型边界和 P1 真机首测决策放在一张表里。它用于决定“先买什么、先接什么、先测什么、什么条件不满足就停止”，不是用来宣称已经实现 iOS 控制。

## 一句话结论

对标 iMouse XP 的主路线应保持为：

```text
iPhone 免越狱零安装 -> AirPlay/投屏取画面 -> 截图采集 -> OpenCV/OCR 识别 -> USB HID 鼠标键盘注入 -> 本地 API/GUI/脚本调度 -> evidence 验收
```

当前仓库的 Python GUI 是 P0/P1 验证工具。真正的产品壁垒在 receiver、HID 固件、自动绑定、坐标校准、失败隔离、日志证据和现场 SOP，不在“能发出一个 click API”。

## 主流路线取舍

| 路线 | 行业定位 | 适合本项目的用途 | 不适合做什么 | P1 决策 |
|---|---|---|---|---|
| AirPlay/投屏 + USB HID | XP 类黑盒群控主线 | 跨 App、系统 UI、手机端零安装 | 不提供元素树，稳定性全靠工程 | 主线 |
| XCUITest/WDA/Appium | 自家 App 自动化测试 | 回归测试、辅助校准、业务断言 | 不适合零安装、跨 App、系统级黑盒群控 | 辅助，不做主线 |
| MDM/Apple Configurator | 批量初始化和设备管理 | Wi-Fi、证书、安装包、合规配置 | 不能像素级点击业务页面 | 辅助 SOP |
| 快捷指令 | 单机轻量自动化 | 简单系统动作 | 难群控、难黑盒、难证据闭环 | 辅助 |
| 越狱/私有 API | 特殊实验 | 探索系统能力边界 | 版本、合规、售后风险高 | 不建议 |

## P1 Receiver 决策

P1 只能选一条 receiver 路线，不要混跑。

| 候选 | 进入 P1 的最低条件 | 失败时怎么处理 | 证据字段 |
|---|---|---|---|
| UxPlay | `doctor` 不再报 `binary:uxplay` fail；能启动并让 iPhone 发现接收端 | 如果 Windows 安装阻塞超过 1 天，切到 Windows Receiver 路线先拿实机证据 | `receiver_provider=uxplay`、版本、路径、启动命令 |
| Windows Receiver | 能固定窗口/设备绑定；能被当前截图链路采集到非黑屏画面 | 若只能显示不能截图，不算 P1 通过，只能做人工观察对照 | `receiver_provider=windows_receiver`、窗口标题/句柄、许可证状态 |
| 有线投屏/专用驱动 | 能拿到帧或稳定窗口；能记录设备唯一标识 | 若只有闭源 UI、无日志、无截图接口，先做专项，不扩到多台 | `receiver_provider=wired`、驱动版本、线材/端口 |
| HDMI 采集卡 | 能采到稳定画面，用作截图质量对照 | 不证明 XP 类自动绑定，也不建议做主线 | `receiver_provider=capture_card`、采集卡型号、延迟 |

P1 receiver 必须证明：

- iPhone 能连接指定接收端。
- 截图非黑屏、非纯白、尺寸稳定。
- 连续 100 次截图有成功率和耗时。
- 断线重连至少 5 次有日志。
- evidence 里写明 receiver 名称、版本、路径和采集方式。

## P1 HID 决策

| 候选 | 进入 P1 的最低条件 | 风险 | P1 用法 |
|---|---|---|---|
| CH9329/通用 HID | 插拔前后串口可见；iPhone 能响应鼠标/键盘 | 坐标、释放、滑动、输入法、批量稳定性要自研 | 当前原型优先使用，验证最小闭环 |
| XP 专用硬件 | 能采购并记录固件/授权；明确是否暴露串口/API | 协议可能不兼容 CH9329，不能靠猜 | 同场对比，回答 4.4、自动绑定、鼠标模式差距 |
| 自研 HID | 有可烧录固件、可追踪设备 ID、可发鼠标键盘报告 | 研发周期长 | P2/P3 后作为产品化方向 |
| 蓝牙 HID | 能配对并稳定输入 | 多台配对、断连、延迟和管理困难 | 不作为主线 |

P1 HID 必须证明：

- 插拔前后串口或 HID 标识有变化。
- 绑定关系能追到 `device_id -> HID -> Hub 口 -> iPhone`。
- 点击、滑动、输入在 iPhone 上真实生效。
- 连续 50 次点击无按下不释放。
- 错误能归类到 `hid_discovery`、`hid_bind`、`hid_click`、`hid_swipe` 或 `hid_keyboard`。

## P1 采购优先级

| 优先级 | 采购/准备 | 原因 | 不买/不准备的后果 |
|---|---|---|---|
| P0 必备 | 1 台已授权 iPhone、1 套 CH9329 或等价 HID、稳定 OTG/转接、PC 有线网络 | 先证明最小闭环 | 无法区分代码问题和硬件问题 |
| P0 必备 | 一个可落地 receiver 路线：UxPlay 或 Windows Receiver | 没画面就没有图色/OCR/校准 | GUI 和 API 只能离线空转 |
| P1 强烈建议 | 第二套 HID、第二根线、备用 Hub 口 | 用于交叉排查 | 现场失败无法判断是代码还是物料 |
| P1 强烈建议 | XP 专用硬件 1 套 | 同场对标真实体验、固件和自动绑定 | 后续容易按 CH9329 错误假设研发 |
| P2/P3 | 4 台 iPhone、4 套 HID、独立供电 Hub | 进入 4 台试点 | 单台通过无法外推群控 |
| P4 | 10 台、两套 Hub、receiver 资源监控 | 做 2 小时稳定性 | 无法发现资源、供电、网络瓶颈 |

## 开测前停止线

任一条件满足就不要进入“实机通过”判断：

- `doctor` 有未解释的 fail。
- 只看到 `COM1`，没有真实 HID 串口或 HID 标识。
- receiver 只能人工看到画面，但代码截图黑屏或尺寸不稳定。
- 设备、HID、Hub 口、线材、iPhone 没有编号。
- evidence 里仍有 `EDIT_ME`、`TODO`、`COM_EDIT_ME` 这类占位值。
- 没有人工观察记录。
- API 返回成功，但 iPhone 没有真实响应。
- P1 没有通过，就开始 4 台或 10 台测试。

## P1 决策记录模板

可以先生成可编辑 JSON 模板：

```powershell
.\.venv\Scripts\python -m imouse.route_decision init --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_route_decision.json
```

填完后做开测前硬校验：

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\p1_dev1_YYYYMMDD_route_decision.json --require-ready --markdown evidence\p1_dev1_YYYYMMDD_route_decision.md --record-evidence evidence\p1_dev1_YYYYMMDD.jsonl
```

`--record-evidence` 会写入一条组件台账事件，供 acceptance 检查 receiver/capture/HID/iPhone/iOS 追踪；它不会写人工 pass，也不会写截图质量。

如果校验失败并写入了 evidence，该 run_id 应当作为阻断复盘保留。修复路线、物料或 open blocker 后，换新的 run_id 再开 P1，避免同一份 evidence 里混有 fail 事件导致 acceptance 永远不能通过。

```text
run_id:
日期:
目标 XP 能力行:
本轮 receiver 路线:
receiver 名称/版本/路径:
采集方式:
本轮 HID 路线:
HID 编号/固件/串口:
iPhone 型号/iOS:
Hub/线材/端口:
是否有 XP 专用硬件对照:
开测前阻断项:
允许进入 P1 实跑: yes/no
原因:
```

## 和仓库资产的关系

| 问题 | 先读 | 执行工具 |
|---|---|---|
| XP 到底公开了什么能力 | `docs/xp_parity_matrix.md` | 无，作为对标口径 |
| 行业主路线怎么选 | 本文、`docs/industry_landscape_2026.md` | 无，作为路线决策 |
| 投屏/截图路线怎么选 | `docs/receiver_capture_selection.md` | `imouse.doctor`、GUI Screenshot |
| HID/硬件怎么测 | `docs/hid_hardware_protocol_benchmark.md` | GUI Bind/Click/Swipe/Type |
| P1 怎么一步步跑 | `docs/p1_single_device_runbook.md` | `imouse.field_packet`、GUI、script_runner |
| 是否可以宣称通过 | `docs/readiness_audit.md` | `imouse.acceptance`、`imouse.readiness` |

## 参考来源

- iMouse 官网：`https://www.imouse.cc/`
- iMouse XP Python 文档：`https://www.imouse.cc/python-xp/`
- iMouse XP API 文档：`https://www.imouse.cc/XP版API文档/`
- Apple AirPlay 屏幕镜像支持文档：`https://support.apple.com/en-us/102661`
- Apple iPhone 指针设备支持文档：`https://support.apple.com/en-us/111775`
