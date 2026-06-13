# GUI Route Procurement SOP

`Procure` 是 Live Probe 中用于路由选择、供应商问题、购买停止线和实验室 SOP 的看板。它位于 `Snapshot` 和 `Routes` 之间，使公开的 XP 和行业信号在购买硬件、接收器软件、SDK 或设备批次之前成为具体的采购检查。

在以下情况之前使用：

- 购买接收器、HID、XP 对比硬件、Hub、线缆或额外 iPhone；
- 从 UxPlay 切换到 Windows 接收器、有线投屏或采集卡通道；
- 在现场机器上安装 SDK/包候选；
- 措辞任何 XP 对标、广泛 iOS 兼容性、完美控制或群控规模声明。

## 操作者路径

```text
Home -> Snapshot -> Procure -> Routes -> Rx Score -> Rx Bootstrap -> Rx Setup -> XP Lab -> Kit Gate -> iOS SOP -> Start Pack -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Acceptance/Readiness
```

## 跟随测试

1. 使用 `python -m imouse.gui` 启动 GUI。
2. 设置 `Evidence`、`Stage` 和所选设备列表。
3. 点击 `Snapshot`，然后点击 `Procure`。
4. 选择第一个 `fail`、`pending` 或 `warn` 行并点击 `Run Selected`。
5. 用真实工作台值填写 Route Decision、接收器、HID、iPhone、Hub、线缆、操作者和证据字段。
6. 导出 `evidence/<run_id>_<stage>_route_procurement_sop.md`。
7. 继续通过 `Routes`、`Rx Score`、`XP Lab`、`Kit Gate`、`iOS SOP`、`Start Pack`、`Runner`、`P1 Trial`、`Acceptance` 和 `Readiness`。

## 看板检查内容

- 主流路由锁定：一个接收器通道、一个 HID 通道、一个 iPhone 范围，不将仅辅助路由计为 XP 风格控制。
- 接收器采购：版本、路径、AirPlay/窗口身份、采集方法、截图质量、日志、授权和重连行为。
- HID 采购：芯片组/提供者、固件、序列号/API 协议、波特率、Hub/线缆绑定、Manual 点击/滑动/输入行为和释放时机。
- XP 对标采购：合法 XP 硬件、固件、授权、并排工件、有线/自动绑定证据和对标停止规则。
- iPhone 夹具 Matrix：精确型号、iOS 版本、设置配置文件、方向、基线截图和本地兼容性证据。
- 工作台材料：Hub、端口、线缆、电源、接收器 PC、网络、操作者、日志、更换策略和恢复记录。
- 来源/包卫生：来源刷新、包身份、哈希、授权、文档漂移和安装边界。
- 声明/支出停止线：相同运行证据、Acceptance、Readiness、指标、日志和精确设备/iOS 范围，在规模支出之前。

## 边界

- `Procure` 不写入 JSONL 证据，不购买硬件，不安装包，不自动浏览，也不证明真实 iPhone 响应。
- `ready` 的采购行仅表示该通道在当前运行中可审查；它不是控制声明。
- XP 硬件对标即使通用 HID P1 工作也仍需要合法的并排 XP 硬件工件。
- 公开来源和供应商声明是测试输入。本地声明需要相同运行的截图质量、Manual 真实 iPhone 点击/滑动/文字观察、Acceptance PASS、Readiness PASS、日志和精确设备/iOS 范围。
