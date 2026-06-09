# iOS Field Settings SOP

本页描述 GUI 里的 `iOS SOP` 面板。它用于把真实 iPhone 开跑前必须确认的现场设置、物理台账和证据门集中到一张表里。

## GUI 入口

- `Live Probe -> iOS SOP` 打开设置核对表。
- `Export` 导出 `evidence/<run_id>_<stage>_ios_field_sop.md`。
- `Run Selected` 会跳到当前行对应的 GUI 动作，例如 Route Edit、P1 Trial、Control Bench、Shot Bench、Hardware Bench、Start Pack 或 Goals。

## 必查设置

| 检查项 | 必须记录 | 为什么重要 |
|---|---|---|
| Device identity and iOS version | iPhone id、model、iOS version、orientation、selected device id | 防止把官网兼容性或另一台手机的证据当成本机通过。 |
| AssistiveTouch and pointer profile | AssistiveTouch、pointer speed、可见指针响应 | HID 写入成功不等于 iPhone 鼠标响应。 |
| Rotation lock and AssistiveTouch menu | Rotation lock、AssistiveTouch floating menu state | 旋转漂移和悬浮菜单遮挡会导致截图、坐标、二维码流程和点击结果不可复现。 |
| Full Keyboard Access and mouse settings | Full Keyboard Access、Trackpad & Mouse | 键盘输入、组合键、焦点和鼠标行为都依赖这些设置。 |
| Mouse parameter profile and calibration library | pointer speed、mouse parameter profile、model/iOS/orientation、QR scan policy | 鼠标参数和通用库必须按机型/iOS/方向复现；扫码流程可能需要先断开投屏或记录替代策略。 |
| Screen lock, brightness, and interruptions | Auto-Lock、brightness、Focus/notification policy | 黑屏、旧帧、弹窗遮挡和长跑失败常来自锁屏/亮度/通知。 |
| Network and AirPlay identity | PC/iPhone 网络、AirPlay name、receiver name/version/path、capture method、window binding | 防止投错设备、截错窗口、使用未记录 receiver。 |
| Hub, cable, power, and port ledger | Hub id、Hub port、cable id、HID serial/firmware、operator | 断连、漂移、按键不释放和延迟通常靠端口/线材/供电定位。 |
| Baseline screenshot and manual observation | Shot Bench、P1 Trial、Control Bench、Acceptance screenshot/manual checks | 先证明画面和人工响应，再谈脚本、图色、OCR 和群控。 |
| Settings replay and operator handoff | Operator Worksheet、Start Pack、Evidence Pack、Readiness | SOP 必须能被第二个操作员复现。 |
| Settings claim boundary | Acceptance、Readiness、real_ios_verified、no unexplained failures | 设置齐全只是前置条件，不证明真实控制或 XP parity。 |

## 推荐执行顺序

1. `Prepare` 生成本轮 Route Decision。
2. `Edit Route` 填写 iPhone、receiver、HID、Hub、Cable、network、operator、rotation lock、AssistiveTouch menu、mouse parameter profile、QR scan policy 和设置字段。
3. `iOS SOP` 找第一条 `fail`、`pending` 或 `warn`。
4. `Run Selected` 回到对应 GUI 工具补台账或实测。
5. `Shot Bench` 和 `P1 Trial` 补 baseline screenshot 与 click/swipe/type manual observation。
6. `Acceptance` 和 `Readiness` 决定是否允许阶段声明。

## 边界

- iOS SOP 不写 JSONL evidence。
- iOS SOP 不证明真实 iOS 控制。
- iOS SOP 不证明 XP parity。
- 设置字段齐全最多说明可以进入下一步测试；真实通过仍需要 JSONL、截图、日志、manual observation、Acceptance 和 Readiness。
