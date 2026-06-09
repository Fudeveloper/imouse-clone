# iOS 群控实机测试矩阵

更新时间：2026-06-08

这份矩阵用于把“iOS 完美控制”拆成可验收、可复盘的现场证据。当前仓库只能证明离线协议层、GUI 原型、脚本调度和 evidence 记录可运行；AirPlay、HID、真实 iPhone 响应必须按本矩阵逐项补证据后，才能进入“可交付”判断。

公开资料边界：

- iMouse 官方入口说明其路线是 iPhone AirPlay 镜像 + iMouse 虚拟鼠键硬件 + 内核服务端/控制台 + HTTP/WebSocket API。
- iMouse XP 帮助文档强调 Windows 10+、4.4 固件、有线投屏、自动绑定、单一投屏服务、硬件解码、多窗口分离和分组/子账号等运营能力。
- Apple 支持文档确认 iPhone 可通过 AirPlay 做屏幕镜像，也支持鼠标/触控板等指针设备；这些能力不等于第三方群控产品已经稳定，只说明路线在 iOS 系统能力边界内有现实基础。

## 总原则

- 先单机闭环，再 4 台，再 10 台，再 20 台以上。
- API 返回成功只能算“软件链路响应”，不能算“iPhone 已被控制”。
- 每个实机 pass 必须有 evidence JSONL、Markdown 汇总、人工观察记录和必要的截图/录屏。
- 每台设备必须固定编号：手机、HID 硬件、线材、Hub 口、AirPlay 名称、串口号都要一一对应。
- 同一问题连续出现 3 次以上时，不要继续扩大设备数，先归类并复现。

## 现场台账模板

| 字段 | 填写示例 | 是否必填 |
|---|---|---|
| test_date | 2026-06-08 | 是 |
| run_id | single_dev1_20260608 | 是 |
| git_revision | `git rev-parse --short HEAD` 输出 | 是 |
| PC 型号/系统 | Windows 11 / 32GB / Intel i7 | 是 |
| Python | 3.13.9 | 是 |
| 投屏组件 | UxPlay / Windows Receiver / XP Receiver | 是 |
| 投屏组件版本 | 版本号或安装包日期 | 是 |
| 网络 | PC 有线 + iPhone 同 VLAN | 是 |
| Hub | 品牌、供电规格、口编号 | 是 |
| HID 硬件 | CH9329 / XP 专用硬件 / 其他 | 是 |
| 固件版本 | 4.4 / 自研版本号 / 未知 | 是 |
| iPhone 型号 | iPhone 13 / iPhone 16 Pro | 是 |
| iOS 版本 | 17.7 / 18.x / 最新系统 | 是 |
| AirPlay 名称 | imouse-dev-01 | 是 |
| 串口 | COM3 | 是 |
| 校准文件 | `state/calibration.json` | 是 |
| evidence | `evidence/<run_id>.jsonl` | 是 |
| summary | `evidence/<run_id>.md` | 是 |
| 失败附件 | 截图、录屏、doctor 报告 | 失败时必填 |

## 设备覆盖矩阵

| 维度 | 最低覆盖 | 扩展覆盖 | 通过标准 |
|---|---|---|---|
| iOS 版本 | iOS 13.4+、iOS 16、iOS 17、iOS 18 或当前最新 | 每个大版本至少 1 台 | 点击、滑动、输入、投屏、截图均通过 |
| 机型 | 1 台刘海/灵动岛机型、1 台旧比例机型 | 高分辨率 Pro 机型、横屏场景 | 坐标误差和截图尺寸记录清楚 |
| HID 路线 | CH9329 或自研 HID | XP 专用硬件/4.4 固件 | iPhone 真实响应，不出现按下不释放 |
| 投屏路线 | 当前原型路线 1 台 | Windows 原生接收、有线投屏、硬解路线 | 画面清晰、低延迟、断线可恢复 |
| 设备数量 | 1、4、10 | 20+ | 单台失败不拖垮全局 |
| 网络拓扑 | PC 有线，同 VLAN | 多交换机、不同 AP、弱网 | AirPlay 发现和重连可记录 |

## 阶段门

每个阶段开始前先生成本轮执行包，作为现场人员逐步执行的入口：

```powershell
.\.venv\Scripts\python -m imouse.field_packet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_field_packet.md
.\.venv\Scripts\python -m imouse.field_packet --stage p3 --run-id pilot_4_YYYYMMDD --devices dev_1,dev_2,dev_3,dev_4 --output evidence\pilot_4_YYYYMMDD_field_packet.md
```

执行包会汇总当前 doctor/readiness 阻断项、组件台账、GUI 步骤、脚本命令、验收命令和失败分流表。它只用于指导测试，不替代 evidence。

| 阶段 | 目标 | 必跑命令/动作 | 通过标准 | 不通过时停止条件 |
|---|---|---|---|---|
| P0 离线 | 证明代码和依赖可运行 | `unittest`、`compileall`、`doctor`、脚本 dry-run | 代码测试全绿，doctor 阻断项已知 | Python 依赖失败、API 无法启动 |
| P1 单机可控 | 证明一台 iPhone 能看、能点、能滑、能输 | GUI + `scripts/p1_single_device_control_probe.json` | 人工观察 pass，evidence 完整 | 投屏无画面、HID 无响应、坐标不可校准 |
| P2 单机稳定 | 证明 1 台连续 30 分钟稳定 | 截图 100 次、点击 100 次、滑动 80 次、输入 20 次 | 无漂移、无卡死、失败可复现 | 点击误差 > 8 像素或投屏频繁断线 |
| P3 4 台试点 | 证明并发调度和分组可用 | `scripts/pilot_4_group_smoke.json` | 4 台结果逐台可追踪 | 单台失败导致全组无返回 |
| P4 10 台稳定 | 证明现场可用性 | 2 小时运行，每 30 分钟一轮 group 操作 | 失败率、断线率、资源占用有记录 | 无法定位失败设备或 evidence 不完整 |
| P5 20+ 压力 | 对标 XP 体验 | 双分组并发、批量重连、UI 日志过滤 | UI 不假死，失败隔离，资源曲线可解释 | 投屏服务、Hub、网络任一层不可控 |

每个阶段结束后都要运行对应验收器：

```powershell
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p1
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p2
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p3
.\.venv\Scripts\python -m imouse.acceptance evidence\<run_id>.jsonl --gate p4
```

验收器只检查证据完整性的硬门槛：无 fail、设备 ID 可追踪、人工 pass 观察、截图质量样本和 metrics 样本。它不能证明 iPhone 已响应，人工观察和截图/录屏仍是实机通过的核心证据。

## 单设备测试用例

| ID | 用例 | 操作 | 通过证据 | 失败分类 |
|---|---|---|---|---|
| S1 | Doctor | `python -m imouse.doctor --markdown evidence/preflight.md` | 无阻断 fail，或替代组件有说明 | `env` |
| S2 | 注册设备 | GUI Register `dev_1` 或 API `/device/register` | 设备列表出现 `dev_1` | `api` |
| S3 | 扫描 HID | 插拔硬件后 Scan | 新串口出现并记录 COM 号 | `hid_discovery` |
| S4 | 绑定 HID | Bind COM 口 | 设备状态和日志记录绑定成功 | `hid_bind` |
| S5 | 投屏发现 | 启动 AirPlay，iPhone 选择接收端 | iPhone 能看到接收端并连接 | `airplay_discovery` |
| S6 | 截图 | Start Capture + Screenshot | 截图非黑屏、尺寸正确 | `capture` |
| S7 | 坐标校准 | 五点校准 | 误差 < 8 像素 | `calibration` |
| S8 | 点击 | 10 个坐标点，每点 10 次 | iPhone 真实点击，无漂移 | `hid_click` |
| S9 | 滑动 | 上下左右、长短滑动各 20 次 | 方向正确，无按下不释放 | `hid_swipe` |
| S10 | 输入 | 英文、数字、符号 | 文本真实输入，焦点正确 | `hid_keyboard` |
| S11 | 找图 | 有纹理模板命中 | 坐标正确，阈值和模板保存 | `vision_template` |
| S12 | 找色 | 固定区域找色 | 坐标命中，容差记录 | `vision_color` |
| S13 | OCR | 区域 OCR | 中文/英文/数字返回正确 | `ocr` |
| S14 | 场景回放 | 运行单设备 JSON | 每步有 API 结果和人工 record | `scenario` |

## 群控测试用例

| ID | 用例 | 操作 | 通过证据 | 失败分类 |
|---|---|---|---|---|
| G1 | 保存分组 | 保存 `pilot_4`、`stable_10` | `state/groups.json` 和 API 返回一致 | `group_state` |
| G2 | 分组点击 | group click | 每台设备有独立结果 | `group_dispatch` |
| G3 | 分组滑动 | group swipe | 单台失败不影响其他设备返回 | `group_dispatch` |
| G4 | 分组输入 | group type | 每台真实输入结果有人工观察 | `hid_keyboard` |
| G5 | 单台断开 | 人工断开 1 台投屏或 HID | 其他设备继续执行，失败设备可定位 | `isolation` |
| G6 | 30 分钟试跑 | 4 台每 5 分钟保存状态 | 断线、截图、HID 失败次数完整 | `stability` |
| G7 | 2 小时稳定 | 10 台每 30 分钟跑场景 | CPU/内存/网络/FPS 有记录 | `stability` |
| G8 | 压力分组 | 20+ 拆成 A/B 组 | UI 不假死，日志可过滤 | `performance` |

## 关键指标

| 指标 | 单设备目标 | 4 台目标 | 10 台目标 | 20+ 观察 |
|---|---:|---:|---:|---:|
| 截图成功率 | 99%+ | 98%+ | 95%+ | 记录瓶颈 |
| 点击误差 | < 8 px | < 10 px | < 12 px | 按机型分层 |
| HID 命令失败率 | < 1% | < 2% | < 5% | 按 Hub 分层 |
| 投屏断线 | 30 分钟 0 次 | 30 分钟 <= 1 次 | 2 小时可恢复 | 记录重连耗时 |
| 单台失败隔离 | 必须 | 必须 | 必须 | 必须 |
| evidence 完整率 | 100% | 100% | 100% | 100% |

指标只是第一版门槛。真实业务上线前要按场景提高要求，例如支付、账号、订单等高风险页面必须人工复核。

## 失败归类

统一把失败写入 evidence `details` 或备注：

- `env`：Python、依赖、路径、权限、缓存目录。
- `api`：HTTP/WebSocket、fun 映射、字段语义。
- `airplay_discovery`：接收端不可见、mDNS/Bonjour、网络隔离。
- `airplay_stream`：黑屏、花屏、断线、延迟异常、硬解异常。
- `capture`：截图失败、尺寸错误、裁剪错误。
- `calibration`：坐标映射错误、横竖屏、黑边、safe area。
- `hid_discovery`：串口不可见、驱动、Hub 供电。
- `hid_bind`：端口占用、波特率、固件不匹配。
- `hid_click`：点击无响应、漂移、越界、按下未释放。
- `hid_swipe`：方向错误、轨迹异常、未释放。
- `hid_keyboard`：焦点错误、输入法策略、字符不支持。
- `vision_template`：模板误判、阈值、语言/主题变化。
- `vision_color`：颜色容差、区域错误、亮度变化。
- `ocr`：模型下载、缓存、返回结构、识别错误。
- `group_state`：分组丢失、重复设备、持久化失败。
- `group_dispatch`：批量结果不完整、单台失败影响全局。
- `performance`：CPU、内存、网络、UI 卡死。
- `business_state`：业务页面变化、弹窗、登录态、账号风控。

## 每轮结束复盘

每轮测试结束后必须产出：

1. `evidence/<run_id>.jsonl`
2. `evidence/<run_id>.md`
3. `evidence/<run_id>_doctor.md`
4. 失败截图或录屏路径
5. 当前矩阵里已通过/未通过的行
6. 下一轮只解决排名前三的阻断问题

可以继续扩大规模的最低条件：

- P1 通过后才进 P2。
- P2 连续两轮通过后才进 P3。
- P3 至少 30 分钟稳定后才进 P4。
- P4 至少 2 小时稳定、失败可定位后才进 P5。
