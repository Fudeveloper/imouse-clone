# iMouse XP 核心能力对标矩阵

更新时间：2026-06-09

网页核对：2026-06-09。下表只记录公开信号和研发假设，不等于能力验收；实机结论仍以本轮 evidence、acceptance 和 readiness 为准。

目标：把 iMouse XP 公开能力、行业壁垒、当前仓库实现、验收证据和下一步研发动作放到同一张表里。它服务于研发排期和现场验收，不用于宣称已经完成 XP 对标。

## 公开来源快照

| 来源 | 当前可用信息 | 用法 |
|---|---|---|
| `https://www.imouse.cc/` | 官网说明路线基于 iMouse 虚拟鼠键硬件、AirPlay 镜像、内核服务端/控制台端、HTTP/WebSocket API、OpenCV 找图和百度飞桨 OCR，并强调专注 iOS；当前兼容宣传包含 iPhone17、iOS 26.4 这类最新口径。 | 高可信；用于确认产品定位和总架构；兼容宣传只进入本地 device/iOS 测试矩阵。 |
| `https://www.imouse.cc/python-xp/` | Python XP 页说明只适用于 XP 版、需配套专用硬件；helper 层覆盖 Device、AirPlay、USB、Group、ImConfig、User，device 层覆盖 Image、KeyBoard、Mouse、Shortcut。 | 高可信；用于确认 SDK/Helper 分层和功能边界。 |
| `https://www.imouse.cc/XP版API文档/` | 官方 XP API 概述说明 HTTP/WebSocket 端口为 `9911`，HTTP 入口为 `/api`，支持 GET、POST JSON、POST 表单；WebSocket 请求为 JSON，并依赖 `msgid` 做异步结果对应。 | 高可信；用于确认 API 兼容层、WebSocket 和错误码语义。 |
| `https://pypi.org/project/imouse-py/` | PyPI 上存在 `imouse-py` 包名，与官网 Python XP 页的安装提示一致；当前公开版本线索为 0.0.4 / 2025-11-16。 | 中可信；只作为 SDK 包名/版本/API 漂移线索，不作为 iOS 控制能力证明。 |
| `https://www.iosautot.cn/XP版API文档/图色相关/截取屏幕/` | 截图 API 使用 `fun=/pic/screenshot`，支持 GET、multipart POST、JSON POST/WebSocket 同 JSON，响应包含 `status/msgid/fun/data`。 | 高可信；用于确认 XP API 形态和字段语义。 |
| `https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version` | XP 新版资料强调 Windows 10+、8GB+ 内存、硬件加速、控制台/内核分离、内核是 Windows service。 | 中可信；用于推断现场部署和性能方向。 |
| `https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings` | iPhone farm 设置强调 iPhone 6s+ / iOS 13.4+、AssistiveTouch、Full Keyboard Access、Trackpad & Mouse、亮度/锁屏设置、同网段投屏。 | 中可信；用于补充现场 SOP，不直接作为产品能力验收。 |
| `https://www.imouse.cc/XP版帮助文档/` | XP 首次配置/鼠标参数资料提示手机设置、旋转/锁屏、AssistiveTouch/全键盘、投屏身份、鼠标参数/通用库、二维码扫描策略等现场细节。 | 高可信；转入 `iOS SOP` 和 Route Decision 字段，不作为控制成功证明。 |

公开资料可能随版本变化；每次进入 P1/P3 前应重新跑一次 `imouse.field_packet`，并把本轮采用的 receiver、硬件、SDK/文档版本写入 evidence。

## 对标矩阵

| 能力域 | XP 公开信号 | 当前实现 | 当前证据 | 差距/风险 | 下一步 |
|---|---|---|---|---|---|
| 产品路线 | AirPlay 取画面 + iMouse 虚拟鼠键硬件 + 内核服务/API | 原型采用 AirPlay/UxPlay 入口 + CH9329 HID + FastAPI | 离线单测、doctor；无实机 evidence | `uxplay` 缺失，真实 HID/iPhone 未接入 | P1 执行包先锁定 receiver/HID/iPhone 台账 |
| 内核/控制台分离 | 官网说明内核服务端和控制台端分离，控制台基于 API | `imouse.server` + `imouse.gui` 分离，GUI 走 `XpApiClient` | API/GUI helper 单测 | Windows service、配置、权限、日志弱 | P1 先稳定 API，P2 再做 Windows service 化 |
| HTTP/WebSocket API | 官网说明 HTTP/WebSocket 均可调用 | `/api` + `fun`，GET/POST JSON/multipart，WebSocket `/api`/`/ws` | `tests/test_xp_api.py` | 官方 fun 覆盖不完整，真实事件语义仍弱 | 按 XP 文档逐类补 fun 和字段兼容 |
| Event/error contract | XP API/help signals include `msgid`, callbacks, logs, errors, device/group/helper domains | GUI `Events` board, callback ledger, Attach Log, Problems/Rerun/Recovery linkage | GUI helper tests and `docs/xp_event_error_contract.md` | Real receiver/HID callbacks, XP hardware errors, account/license errors, and per-device log filters are unverified | Use Events before rerun; convert callbacks/logs/errors into JSONL evidence and stage gates |
| Python SDK/helper | XP Python 页有 api/helper/console/device 分层 | `XpApiClient` 初版，覆盖设备、分组、校准、profile、图色、批量、callback list/push/clear，以及本地 ImConfig/User/Shortcut runtime helper | `tests/test_xp_client.py` | 真实 receiver/HID callback 事件、云用户/权限、快捷指令真实执行仍未验证 | P1 后接入真实事件回调；P3 后再设计账号权限和快捷指令执行模型 |
| 设备/分组 | Helper 有 Device/Group/User；XP 资料有云端分组/子账号线索 | 本地注册、状态、分组 JSON | API 单测、GUI dry-run | 云端分组、账号、LAN 可见范围未做 | P3 前只保留本地分组，P3 后设计权限模型 |
| 组件台账 | 公开资料强调硬件、投屏、设备设置强相关 | `state/device_profiles.json` + GUI Record Metadata + evidence | profile/API/GUI helper 测试 | 台账不等于实机通过；现场易填错 | P1 执行包强制逐设备填写 receiver/capture/HID/iOS |
| 投屏发现/连接 | AirPlay 镜像，XP 新版强调 Windows 和单一服务 | UxPlay/X11 原型入口 | doctor 当前 `binary:uxplay` fail | Windows receiver、有线投屏、硬解未实现 | 先选 P1 receiver；替代路线必须记录版本/路径 |
| 截图采集 | `/pic/screenshot` 支持 rect、binary/jpg、save_path 等字段 | 截图 API、GUI 静态预览、画质检查；XP 截图 fun 已支持 GET/JSON/multipart、binary、jpg、rect、region、save_path | 视觉/脚本/API 单测，未实机 | 真实窗口采集、帧率、黑屏/花屏未验证 | P1 跑 10 次截图探针，P2 跑 100 次截图成功率 |
| HID 点击/滑动 | iMouse 必须配套硬件；XP 4.4/快准狠与固件强相关 | CH9329 点击、滑动、键盘协议原型 | 校准/HID 映射单测；无硬件 evidence | XP 专用硬件协议未知，iOS 鼠标行为未实测 | CH9329 与 XP 硬件同场对比，记录误差/释放状态 |
| 坐标校准 | XP 强调自适应分辨率和设备配置 | 本地 calibration profile，GUI 保存/加载 | `tests/test_calibration.py` | 横屏、safe area、灵动岛、高分辨率未实测 | P1 五点校准，P2 横屏/机型矩阵 |
| 键盘输入 | Python XP device 层有 KeyBoard，公开资料提到 Emoji/多语言 | 文本、key、combo 初版 | XP client/API 测试 | 中文输入、Emoji、焦点、组合键未实测 | P1 英文/数字/符号；P2 中文/Emoji |
| 图色能力 | 官网提 OpenCV/OCR；XP API 有截图、找图、OCR、找文字、多点找色 | 找图、找色、多点找色、OCR、找文字、GUI 裁剪 | vision/API/client/runner 单测 | 真实模板库、透明图、阈值策略、失败回放不足 | 建立模板资产规范和失败截图回放 |
| OCR | 官网提百度飞桨 OCR；XP 图色类有 OCR/找文字 | PaddleOCR 兼容层，项目内缓存 | OCR 结构兼容单测 | 模型下载、真实截图、性能未实测 | P1 做真实截图 OCR；P2 区域 OCR 和性能 |
| 脚本运行时 | Python XP 支持 API/helper 自动化 | JSON runner 支持 call/wait/repeat/metrics/record/图色/批量 | runner 单测、6 脚本 dry-run | 变量、条件、业务断言、失败回放还弱 | P2 补变量/条件和业务状态断言 |
| 现场执行/SOP | iPhone 设置、同网段、硬件方向、rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy | `field_packet`、runbook、doctor、readiness、acceptance、GUI dashboard/pack、XP gap audit、iOS SOP | 以当前 `python -m unittest discover -s tests -v` 输出为准 | 执行包、GUI 索引、iOS SOP 和差距审计不证明实机通过 | 每轮实机先生成执行包，跑 Kit Gate -> iOS SOP -> Bench -> evidence gate |
| 运维可观测性 | XP 新版强调日志、调试工具、分组/用户 | evidence_report、Review、doctor、metrics、Recovery Drill | evidence/readiness/GUI helper 测试 | 设备日志过滤、真实 receiver 日志采集和自动恢复写证据不足 | P2/P3 增加按设备日志、receiver 日志附件和恢复结果自动留痕 |
| 商业化能力 | 云端分组、子账号、局域网可见范围、自动更新 | 暂无，仅本地 JSON/文档 | 无 | 提前做会分散 P1/P3 主线 | P3 通过后再立项 |

## 阶段结论

| 阶段 | 当前判断 | 证据 |
|---|---|---|
| P0 离线准备 | 通过 | 最近一次本地验证以 README 和当前 unittest 输出为准；compileall、7 个场景 dry-run 仍需每轮复核。 |
| P1 单台 iPhone 实控 | 未通过 | doctor 仍有 `binary:uxplay` fail，且没有真实 iPhone evidence。 |
| P2 单台稳定 | 未通过 | P1 未通过，不能外推稳定性。 |
| P3 4 台群控 | 未通过 | 没有 4 台实机 evidence。 |
| XP 商业化体验 | 未通过 | 有线投屏、硬解、自动绑定、XP 专用硬件、云端分组均未验证。 |

## 2026-06-09 API client delta

- `XpApiClient.screenshot_bytes()` now covers XP raw screenshot downloads from `/pic/screenshot` with `binary=true`.
- `XpApiClient.screenshot(binary=True)` is kept as a compatibility shortcut and returns raw bytes through the same path.
- This only proves local API/client behavior. It does not prove receiver capture quality, frame rate, HID response, or real iPhone control.

## 下一步研发动作

1. 生成 P1 执行包：`python -m imouse.field_packet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1`。
2. 先解决投屏路线：安装 UxPlay 或明确 Windows Receiver/有线投屏替代组件，并把版本、路径、启动方式写入 evidence。
3. 接一套 HID：记录插拔前后串口、HID 编号、固件、Hub 口和线材。
4. 跑 `scripts/p1_single_device_control_probe.json`，人工观察必须写入 evidence；`scripts/p1_receiver_capture_probe.json` 只用于 receiver/capture 专项排障。
5. P1 acceptance/readiness 都 PASS 后，再进入 P2/P3；不要用 API success 或 dry-run 替代真实 iPhone 响应。
