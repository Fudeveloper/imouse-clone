# iMouse XP 核心功能差距与研发 Backlog

更新时间：2026-06-08

目标：把 iMouse XP 公开能力拆成研发 backlog，并明确当前仓库已实现、未实现、必须实机验证的部分。

XP 公开迭代路径和踩坑点的专项复盘见 `imouse_xp_iteration_lessons.md`。本文只保留可执行 backlog。

优先级定义：

- P0：没有它就无法做实机闭环或无法证明结果。
- P1：单设备可用和 4 台试点必须具备。
- P2：10 台稳定和 XP 类体验需要。
- P3：商业化、运营和规模化体验增强。

## 总体差距

| 模块 | XP 公开/可推断能力 | 当前仓库状态 | 差距 | 优先级 | 验收证据 |
|---|---|---|---|---|---|
| 内核服务 | 内核服务端 + 控制台端，HTTP/WebSocket API | FastAPI + WebSocket 原型，WebSocket `/api` 和 callback ledger 初版 | 真实 receiver/HID 事件、权限、配置、性能日志仍弱 | P0 | API 测试 + 实机 evidence |
| XP API | `/api` + `fun`，GET/POST/multipart/WebSocket | 已有 `/api` + `fun` 初版 | 官方 fun 覆盖不完整，字段语义需继续对照 | P0 | `xp_api_compat.md` + 单测 |
| Event/error contract | `msgid`、callback、request/response logs、device/capture/HID errors | GUI `Events` board、callback ledger、Attach Log、Problems/Rerun/Recovery linkage | 真实 receiver/HID callbacks、per-device log filters、XP hardware errors、account/license errors remain unverified | P1 | `xp_event_error_contract.md` + callback/log/evidence audit |
| Python SDK | `imouse-py`，API/helper 分层 | `XpApiClient` 初版，含 callback list/push/clear、ImConfig/User/Shortcut runtime helper | 真实事件订阅、云用户/权限、快捷指令真实执行、错误码映射缺失 | P1 | SDK 示例 + 单测 |
| 设备管理 | 设备列表、状态、分组、配置 | 本地设备注册、状态、分组 JSON | 云端分组、子账号、LAN 可见范围没有 | P2 | 4/10 台分组实测 |
| USB/HID | 专用硬件、4.4 固件、自动绑定 | CH9329 协议原型 | XP 专用硬件协议和 4.4 固件未验证 | P0 | P1 HID 实机通过 |
| 投屏 | AirPlay/有线投屏、单一服务、硬解、快速连接 | UxPlay/X11 原型入口 | Windows 产品级投屏、有线投屏、硬解未实现 | P0 | 投屏截图 evidence |
| 截图采集 | 多设备截图、窗口分离、高分辨率 | 截图 API + GUI 静态预览 | 实时画面、窗口句柄、帧率、重连不足 | P1 | 100 次截图成功率 |
| 坐标校准 | 自适应分辨率，4.4 自动绑定 | 本地 calibration profile | 自动识别、横屏、safe area 大量实测缺失 | P0 | 五点校准 evidence |
| 鼠标模式 | 普通/快准狠等模式 | 普通点击/滑动原型 | iOS 17+ 和固件强相关，未实测 | P1 | 10 点点击和滑动矩阵 |
| 键盘输入 | 文本、快捷键、组合键、Emoji | 英文文本、key/combo API 原型 | 中文输入法、Emoji、组合键未实测 | P1 | 输入矩阵 evidence |
| 图色 | 截图、普通找图、OpenCV 找图、多点找色 | 找图/找色/多点找色/模板裁剪初版 | 资产库、透明图、阈值策略、失败回放缺失 | P1 | 模板资产记录 |
| OCR | OCR、找文字 | PaddleOCR 兼容层 | 真实模型下载、区域 OCR、性能未实测 | P1 | OCR evidence |
| 脚本 | Python/API 自动化，批量流程 | JSON runner 初版 | 循环、变量、条件、失败截图自动采集缺失 | P2 | 场景回归 |
| GUI | 控制台、多窗口、调试工具、日志 | Tkinter 原型 | 实时画面网格、快捷键、日志过滤不足 | P2 | GUI 试点记录 |
| 诊断 | 请求/返回日志、调试工具 | doctor + evidence 初版 | 性能指标、系统资源、投屏日志采集不足 | P1 | doctor + metrics |

## P0：单设备闭环必做

1. 明确投屏路线

现状：

- 当前代码依赖 `uxplay`，本机 doctor 已判定缺失。
- 对标 XP 时，Windows 原生投屏、有线投屏、硬解都必须另立专项。
- 投屏 receiver 和截图采集路线的决策表见 `receiver_capture_selection.md`。

任务：

- 选择 P1 首测投屏组件：UxPlay 或 Windows AirPlay Receiver。
- 记录安装路径、版本、启动命令、服务名、AirPlay 名称。
- 接入截图采集，确认 GUI 能显示真实截图。

验收：

- `doctor` 不再因投屏组件阻断，或 evidence 明确记录替代组件。
- `Screenshot` 返回非黑屏图片。
- 断开后能手动重连并记录耗时。

2. 验证 HID 链路

现状：

- 当前硬件层实现 CH9329 串口 HID 帧。
- 没有真实 HID 插拔和 iPhone 响应证据。
- CH9329、XP 专用硬件、自研 HID 的同场对标表见 `hid_hardware_protocol_benchmark.md`。

任务：

- 插拔硬件，记录新增串口。
- 绑定 `dev_1`。
- 点击、滑动、输入各跑 10 次以上。
- 如果使用 XP 专用硬件，确认是否兼容当前协议；不兼容则记录协议适配需求。

验收：

- iPhone 真实响应。
- 无按下不释放。
- 失败能归类到 `hid_discovery`、`hid_bind`、`hid_click`、`hid_swipe` 或 `hid_keyboard`。

3. 坐标校准

现状：

- 已有本地 calibration profile 和 GUI 面板。

任务：

- 五点校准。
- 记录 active 区域、target 尺寸、orientation、safe area。
- 横屏先不作为 P1 必须项，但要列入 P2。

验收：

- 误差 < 8 像素。
- 连续 50 次点击无漂移。
- evidence 有人工观察。

4. Evidence 标准化

现状：

- `ValidationRecorder`、GUI record、script runner 已可写 JSONL/Markdown。

任务：

- P1 所有实机观察必须写入 `Manual` 或脚本 `record`。
- 失败必须附截图/录屏路径。

验收：

- 任何 pass 都能追到设备 ID、步骤、API 返回、人工观察。

## P1：4 台试点必做

1. 批量命令隔离

现状：

- `/batch/click`、`/batch/swipe`、`/batch/type` 已返回逐设备结果。

任务：

- 用 `scripts/pilot_4_group_smoke.json` 实跑。
- 人工断开一台设备，确认其他设备仍有返回。

验收：

- 单台失败不影响整组响应。
- 失败设备 ID 和错误文本明确。

2. 图色资产规范

现状：

- GUI 可拖拽裁剪模板，OpenCV 找图可用。

任务：

- 建立模板命名规则：`templates/<app>/<screen>/<target>_<ios>_<theme>.png`。
- 禁止纯色或低纹理模板，当前 GUI 和脚本已做基础质量校验。
- 每次找图记录 threshold、region、命中坐标、原始截图。

验收：

- 找图误判有可回放证据。

3. OCR 路线验证

现状：

- PaddleOCR 2.x/3.x 返回结构兼容已有单测。

任务：

- 真实模型下载。
- 真实截图 OCR。
- 区域 OCR 优先，避免全屏 OCR 成本失控。

验收：

- 中文、英文、数字各至少 3 个样本通过。

## P2：10 台稳定必做

1. 投屏性能专项

任务：

- 记录 CPU、内存、网络、截图成功率、投屏断线。
- 对比 UxPlay/Windows Receiver/有线投屏。
- 评估 H264/H265 硬解。

验收：

- 2 小时内失败可定位。
- 资源曲线可解释。

2. GUI 可观测性

任务：

- 增加按设备过滤日志。
- 增加失败截图入口。
- 增加设备状态列：投屏、HID、截图、校准、最后错误。

验收：

- 10 台测试时能在 30 秒内定位失败设备。

3. 脚本运行时增强

任务：

- 已有基础 `repeat` 重复轮次。
- 已有基础 `metrics` 系统指标记录。
- 已有 `screenshot` 步骤自动落盘，路径写入 evidence artifacts。
- 已有基础截图画质校验，可识别缺失 base64、无效图、过小图、黑屏、白屏和低纹理空白图。
- 已有失败步骤的截图尽力自动保存，路径写入 evidence artifacts。
- 继续补变量。
- 继续补条件分支。
- 继续补重复帧检测、业务状态校验和失败前后对比。
- 继续补按分组循环执行的监控指标。

验收：

- 2 小时 watchdog 可无人值守运行，并保留人工抽检记录。

## P3：XP 商业化体验

1. 分组/账号/权限

XP 公开资料提到分组云端存储、子账号、局域网可见范围。当前仓库只有本地分组 JSON。

任务：

- 定义本地/云端分组模型。
- 子账号权限。
- LAN 可见范围。

2. 自动绑定

XP 4.4 固件和有线投屏后的自动绑定是关键体验。当前原型无法证明。

任务：

- 研究硬件 ID、USB 拓扑、投屏 ID 的关联方式。
- 实现绑定建议或自动绑定。

3. 多窗口/多进程显示

任务：

- 实时画面网格。
- 窗口分离。
- 多进程刷新。
- 低帧率预览和高帧率焦点窗口分层。

## 迭代过程启示

iMouse XP 的公开迭代路径说明：它不是先做漂亮 GUI，而是逐步解决现场痛点。

建议我们的顺序：

1. 单设备闭环：能看、能截图、能点、能滑、能输入。
2. 证据闭环：每个结论都有 evidence。
3. 小规模群控：4 台分组，失败隔离。
4. 稳定性：10 台 2 小时，指标可解释。
5. 投屏专项：Windows 原生、有线、硬解、快速重连。
6. 运营能力：账号、权限、云端分组、日志和调试工具。

## 下一轮可执行任务

按收益排序：

1. 跑 `p1_single_device_runbook.md`，拿到第一份真实 iPhone evidence。
2. 如果 `uxplay` 继续缺失，明确 P1 投屏替代组件，并把截图采集适配进 GUI。
3. 接入一套 HID，确认 CH9329 是否足够；如果目标是 XP 专用硬件，开始协议适配专项。
4. 把 P1 失败 Top 3 写回 `field_test_matrix.md` 的失败分类。
5. P1 通过后再跑 `pilot_4_group_smoke.json`。
