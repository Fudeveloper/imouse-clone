# iMouse XP Public Source Refresh

更新时间：2026-06-09

本文只记录公开资料带来的研发判断，不把任何宣传语当成已验收能力。实机结论仍以本项目 `evidence/<run_id>.jsonl`、Acceptance、Readiness、人工观察和硬件记录为准。

## Source Tiers

| 等级 | 来源 | 用法 |
|---|---|---|
| 高 | `https://www.imouse.cc/`、`https://www.imouse.cc/python-xp/`、XP API 文档、XP 帮助文档 | 确认 XP 对标能力、SDK/API 形态、硬件依赖、首次配置和现场 SOP。 |
| 中 | `https://www.iosautot.cn/XP版API文档/`、`https://bestmoon-doc.gitbook.io/bestmoon/xp-tool-ios/imouse-xp-new-version`、`https://pypi.org/project/imouse-py/` | 补充接口细节、部署方式、SDK 包版本和现场运维线索；进入研发前需要再复核。 |
| 低 | 第三方转载、非官方包名、论坛经验 | 只作为问题假设，不进入架构结论。 |

## 2026-06-09 Public Refresh

| 公开信号 | 来源 | 研发处理 |
|---|---|---|
| 官网首页继续呈现 XP 类核心模型：iMouse 虚拟鼠键硬件、AirPlay 镜像、iPhone 端无需安装 App、Kernel/Console 分离、HTTP/WebSocket API、OpenCV 找图和 OCR。 | `https://www.imouse.cc/` | 主线仍是 receiver/capture + HID + vision + API + evidence；不能改成 WDA/Appium 主控路线。 |
| 官网首页出现最新机型/系统兼容宣传口径，例如 iPhone17、iOS 26.4 和宽 iOS 版本覆盖这类广告口径。 | `https://www.imouse.cc/` | 只作为设备/iOS 测试矩阵输入；必须用 GUI `Compat` 形成本地 model/iOS coverage，不能从官网宣传外推为本项目已兼容。 |
| Python XP 页继续指向 XP 版专用 Python 库和 helper 分层，且强调配套 iMouse 专用硬件。 | `https://www.imouse.cc/python-xp/` | `XpApiClient`/GUI/helper 只是协议骨架；XP 专用硬件、授权、固件和事件回调必须实测。 |
| PyPI `imouse-py` 当前公开版本线索为 0.0.4，发布日期 2025-11-16，包描述仍指向 XP-only、client-server 和 dedicated hardware。 | `https://pypi.org/project/imouse-py/` | 只作为 SDK/API 漂移和包名锁定线索；接入前必须固定版本/hash，并通过 XP Gap、API tests 和真实 receiver/HID/iPhone evidence。 |
| XP API 文档公开本地 `9911`、`/api`、HTTP/WebSocket、`msgid`、状态/错误码、设备/配置/用户/键鼠/图色/快捷指令/插件/callback 等分类。 | `https://www.imouse.cc/XP版API文档/` | XP Gap 必须按产品域审计；不能只因为 click/screenshot 通过就声称核心功能完成。 |
| XP 帮助页继续把 XP 新版重点放在 Windows、窗口分离、4.4 固件、有线投屏自动绑定、投屏速度、单投屏服务、硬解、分辨率自适应、日志、云分组、子账号等运维体验。 | `https://www.imouse.cc/XP版帮助文档/软件简介/` | 下一阶段重点是 receiver/HID/日志/metrics/恢复/SOP，而不是继续堆装饰性 GUI。 |
| XP 首次配置/鼠标参数资料强调手机设置、旋转/锁屏纪律、AssistiveTouch/全键盘、投屏身份、鼠标参数/通用库和二维码扫描流程。 | `https://www.imouse.cc/XP版帮助文档/` | 已转成 GUI `iOS SOP` 字段：rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy；这些只能开放测试，不证明控制成功。 |

本轮已经把这些公开信号接入 GUI `Sources` / XP Public Source Ledger，并用 `Compat` / Device-iOS Compatibility Matrix 承接公开兼容性宣传到本地 model/iOS 覆盖。两者只生成审计台账和覆盖矩阵，不写 JSONL evidence，也不证明 XP parity、广泛兼容或真实 iOS 控制。

## Package Namespace Drift Guard

Track these PyPI namespaces separately during every source refresh:

| Package | Public URL | SOP decision |
|---|---|---|
| `imouse-py` | `https://pypi.org/project/imouse-py/` | Treat as the primary SDK-shape clue because the public Python XP page uses `pip install imouse-py`. |
| `imouse-xp` | `https://pypi.org/project/imouse-xp/` | Treat as a similar-name package and dependency-confusion risk until the artifact is pinned and reviewed. |
| `py-imouse-xp` | `https://pypi.org/project/py-imouse-xp/` | Treat as a similar-name package and SDK-drift risk until maintainer/source/API behavior/license are reviewed. |

Do not install any lookalike package on field machines until version, hash, source, maintainer, license, and API surface are reviewed. Package import success is not XP parity, not iOS compatibility, and not real iPhone control evidence; it only opens the next API regression and hardware-backed field test.

## Repeatable Audit Command

静态文档必须配套可重复复核。每次 route、package、兼容口径、roadmap 或 demo 说法变化前，先运行：

```powershell
.\.venv\Scripts\python -m imouse.source_audit --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md --allow-failures
```

离线或现场网络不稳定时运行：

```powershell
.\.venv\Scripts\python -m imouse.source_audit --offline --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md
```

审计结果只记录 URL 状态、PyPI 版本、关键词命中、local doc 时间戳、SOP owner 和 claim boundary。`ok` 只代表公开源可达且关键词未漂移，不代表本项目已控制真实 iPhone，不代表广泛 iOS 兼容，也不代表 XP parity。

## Confirmed Public Signals

| 信号 | 公开来源 | 对我们的影响 |
|---|---|---|
| iMouse 用 AirPlay 镜像传输屏幕，目标是 iOS 免越狱、无需手机端 App 控制。 | `https://www.imouse.cc/` | 主线仍是投屏/截图/图色/HID，而不是 WDA/Appium。 |
| Python XP 文档明确只适用于 XP 版，必须配套 iMouse 专用硬件；包名线索为 `imouse-py`。 | `https://www.imouse.cc/python-xp/` | 不能只仿 API；必须采购/对照硬件，验证专用硬件、固件和授权。 |
| `imouse-py` 包版本存在公开 release 节奏，但安装成功只证明 SDK 可被导入，不证明硬件、授权、投屏、截图或 HID 控制成功。 | `https://pypi.org/project/imouse-py/` | GUI `Sources` 将它归入 package_registry；只有 API 兼容测试和实机 evidence 同时过门，才能把它用于对标结论。 |
| Python helper 分成 console/device：console 覆盖 Device、AirPlay、USB、Group、ImConfig、User；device 覆盖 Image、KeyBoard、Mouse、Shortcut。 | `https://www.imouse.cc/python-xp/` | 当前 GUI 的设备、投屏、HID、图色、脚本、分组方向正确；callback ledger/helper 已有初版，并新增本地 ImConfig/User/Shortcut runtime 兼容骨架；后续还缺真实事件接入、云用户/权限和快捷指令真实执行。 |
| XP API 是本地服务形态，围绕 `/api` 和 `fun` 功能名；截图示例使用 `/pic/screenshot`，响应包含 `status`、`msgid`、`fun`、`data`。 | `https://www.iosautot.cn/XP版API文档/图色相关/截取屏幕/` | `XpApiClient` 的 `/api + fun` 兼容层方向正确；已补 WebSocket `/api`、`msgid` 响应、callback ledger 初版，以及截图 `binary/jpg/rect/save_path/multipart` 兼容；后续还要补真实 receiver/HID 事件接入和更多官方 fun。 |
| XP 新版资料强调 Console/Core 分离，Kernel 作为 Windows service，Console 异常时通常重启 Kernel。 | `https://bestmoon-doc.gitbook.io/bestmoon/xp-tool-ios/imouse-xp-new-version` | GUI 不是最终产品核心；P2/P3 后必须补服务化、日志、重启、升级、权限和运维控制台。 |
| XP 首次配置和鼠标参数相关资料把“手机先配置好”放在控制前面：锁屏/旋转/辅助触控菜单、投屏身份、鼠标参数库和扫码策略会直接影响坐标、画面和业务流程。 | `https://www.imouse.cc/XP版帮助文档/` | `iOS SOP` 必须在 Bench 前运行；设置齐全最多是 `ready`，仍需截图、人工观察、Acceptance 和 Readiness。 |

## Iteration Lessons

1. 第一阶段不是“写更多按钮”，而是证明一台 iPhone 的看、点、滑、输全链路。
2. XP 的壁垒不是单个鼠标 API，而是投屏稳定性、硬件绑定、鼠标参数、截图/图色质量、批量调度和现场运维。
3. 公开 API 支持截图、找图、OCR、鼠标、键盘、设备和分组；这说明 GUI 必须把模板资产、截图质量、失败回放、人工观察和 acceptance gate 放在同一工作台里。
4. 如果没有 XP 专用硬件，不要把 CH9329 结果包装成 XP 4.4 固件兼容；只能说“通用 HID 路线验证”。
5. 如果没有 Windows receiver 或有线投屏实测，不要声称已经达到 XP 的窗口分离、硬解、自动绑定体验。

## SOP Impact

2026-06-09 GUI addition:

- `Knowledge Center` maps XP public model, mainstream industry route, P1 route decision, field SOP, hardware pitfalls, API/helper gaps, iteration lessons, and claim boundary into GUI next actions.
- `Sources` maps current public XP claims into source tier, R&D impact, verification gap, and next GUI action.
- `Iter Radar` maps XP iteration lessons into R&D priority, SOP/test path, stop rule, and next GUI action.
- `XP Timeline` maps XP public evolution signals into chronological lessons, pitfalls, SOP gates, required evidence, and claim stop rules.
- `iOS SOP` maps real-phone settings, rotation lock, AssistiveTouch menu, mouse parameter profile, QR scan policy, network/AirPlay identity, Hub/Cable ledger, baseline artifacts, and claim boundary into the same pre-P1 field workflow.
- `Rerun Playbook` maps failed categories and stage gates into smallest rerun action, fresh run_id rule, evidence-to-keep, and stop rule so public-source lessons become executable field SOP.
- `Recovery Drill` maps XP-style operational lessons around receiver restart, HID rebinding, group isolation, watchdog metrics, and handoff stop rules into a GUI recovery board.
- `Events` maps XP API envelope, WebSocket/msgid, callback lifecycle, Attach Log ingestion, error taxonomy, and claim boundary into a single GUI audit board before rerun or SDK parity claims.
- These research/SOP dashboards do not write evidence and do not prove XP parity or real iOS control.

P1 前 GUI 要服务现场 SOP，而不是追求多窗口观感：

- `Route Decision` 固化 receiver/HID/iPhone/Hub/线材/operator。
- `Doctor` 拦截环境、服务、投屏、串口和状态文件问题。
- `Live Probe` 显示当前阻断。
- `iOS SOP` 在 Kit Gate 和 Bench 之间核对真实 iPhone 设置、rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy、AirPlay/网络、Hub/Cable、baseline screenshot 和 manual observation 边界。
- `Rerun Playbook` 在 Triage/Review 之后决定最小复测路径、是否换 run_id、保留哪些截图/日志/台账和何时停线。
- `Recovery Drill` 在 Rerun 之后把 receiver/HID/校准/群控/性能恢复动作、验证步骤和证据保留项变成演练表。
- `SOP Board` 把设备、路线、Doctor、证据、脚本/队列、模板、Acceptance、Readiness 串成八步执行台。
- `Manual` 必须记录真实 iPhone 观察，尤其是 API 成功但手机不动、坐标偏移、输入法异常、断线等问题。
- `Pack`/`Session`/`Dashboard` 只能做索引和复盘，不允许当成实机通过证据。

## Procurement Questions

采购 XP 专用硬件或 receiver 时先问清：

1. 硬件型号、固件版本、授权方式和是否可升级。
2. 是否支持有线投屏，是否需要 4.4 固件，是否有自动绑定机制。
3. API 服务端口、WebSocket、截图 binary、multipart、日志路径是否开放。
4. 多设备时如何保证窗口、投屏名、USB/HID、设备 ID 一一绑定。
5. Windows service 的服务名、重启方式、日志位置、异常恢复策略。
6. 是否支持导出请求/返回日志，是否能按设备过滤。
7. 同一 iOS 版本、机型、横竖屏、AssistiveTouch、指针速度下的推荐鼠标参数。
8. 二维码/扫码流程是否要求先断开投屏，是否有通用库参数、按机型/iOS 导入规则和失败回滚方法。
