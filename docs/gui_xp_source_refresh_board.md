# GUI XP Source Refresh Board

`Src Refresh` 是 Python GUI 中的公开来源刷新 SOP 看板。它帮助团队确定在路由、路线图、依赖、兼容性或演示声明之前何时必须刷新公开的 iMouse XP、包注册表、Apple/iOS 和行业路由信号。

使用 Live Probe 工作流：

```text
Home -> Action Map -> Src Refresh -> Src Audit -> Pkg Guard -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

在 `Action Map` 之后、在更改硬件范围、采用 Python 包、更新 iOS 兼容性措辞或展示 XP 对标进展之前打开 `Src Refresh`。

## 行

- `official_homepage_refresh`：重新检查首页产品型号、兼容性措辞、无应用/无越狱定位、硬件和 API 声明。
- `official_api_refresh`：重新检查 XP API 信封、`/api`、`fun`、`msgid`、WebSocket、callback 和错误形状。
- `official_help_iteration_refresh`：重新检查帮助/新版本文档中的经验，如 Windows 10+、Core/Console 拆分、4.4 固件、有线投屏、硬解码、日志、云端/群控、子账户、LAN 规则和快捷键。
- `package_registry_refresh`：在任何包安装或 SDK 比较之前重新检查 `imouse-py`、`imouse-xp` 和 `py-imouse-xp`。
- `apple_ios_pointer_refresh`：在添加型号/iOS 兼容性声明之前重新检查 iOS 指针/AssistiveTouch/鼠标/键盘设置。
- `industry_route_refresh`：在采购或路由切换之前重新检查主流接收器/采集/HID 路由选择。
- `source_to_sop_commit`：将每个来源增量映射到 GUI 负责方、测试、工件或明确拒绝。
- `source_claim_boundary_refresh`：降级任何缺乏 JSONL 现场证据、Acceptance 和 Readiness 的纯来源声明。

## SOP

1. 点击 `Src Refresh`。
2. 从第一个 `fail`、`pending` 或 `warn` 行开始。
3. 在浏览器中手动打开列出的来源并与本地文档进行比较。
4. 如果措辞、版本、API 形状、帮助页面行为、包元数据或 iOS 指导发生变化，更新本地文档和受该变化影响的测试/SOP 行。
5. 点击 `Run Selected` 将来源增量落地到 Sources、Action Map、XP Timeline、Iter Radar、Events、Local、iOS SOP、Rx Score 或 Goals。
6. 点击 `Src Audit`；无网络时保留离线报告，或点击 `Run Live` 获取 URL/PyPI 状态。
7. 在任何依赖采用或 SDK 对标措辞之前点击 `Pkg Guard`。
8. 为运行交付导出 `Src Refresh`、`Src Audit`、`Pkg Guard`、Sources、Action Map、XP Timeline、Iter Radar 和 `Pack`。
9. 仅在真实设备证据存在后重新运行 Acceptance 和 Readiness。

## 包命名空间守卫

`package_registry_refresh` 必须将 `imouse-py`、`imouse-xp` 和 `py-imouse-xp` 视为独立命名空间。相似包名是依赖混淆和 SDK 漂移信号，不是可互换的安装目标。

在精确版本和哈希固定、来源/维护者/授权/API 行为审查、本地 API 回归测试通过，以及精确接收器/HID/iPhone 范围具有基于硬件的证据之前，不要在现场机器上安装相似外观的包。

## 边界

- `Src Refresh` 不自动浏览。
- `Src Refresh` 不写入 JSONL 证据。
- `Src Audit` 可以获取公开 URL，但仍仅记录来源新鲜度。
- 新鲜的公开来源不能证明真实 iPhone 响应。
- 新鲜的包版本不能证明 SDK 对标或硬件控制。
- 新鲜的 iOS/Apple 支持页面不能证明本地兼容性。
- XP 对标仍需要本地 API 行为、接收器/采集证明、HID 证明、SOP 覆盖率、声明的并排硬件证据、Acceptance 和 Readiness。

导出路径：

```text
evidence/<run_id>_<stage>_xp_source_refresh.md
```
