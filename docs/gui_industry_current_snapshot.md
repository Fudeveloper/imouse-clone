# GUI Industry Current Snapshot

`Snapshot` 是当前行业/来源/SOP 状态的 Live Probe 看板。它将 `docs/industry_current_state_snapshot_2026.md` 转换为操作者行，用于采购、路由选择、接收器设置、HID 证明、iPhone 设置、API/Console 边界、视觉回放、群控隔离和声明措辞。

在 `Routes`、`Kit Gate`、`iOS SOP`、`Start Pack`、采购审查或演示措辞之前使用。

## 操作者路径

```text
Home -> Snapshot -> Procure -> Action Map -> Src Refresh -> Src Audit -> XP Drill -> XP Timeline -> XP Arch -> XP Lab -> Coach -> Rx Score -> Rx Bootstrap -> Rx Setup -> Transcript -> Route/Kit -> Local -> Screenshot -> Wizard -> Runner -> Ctrl Ledger -> P1 Trial -> Events/Problems -> Acceptance/Readiness
```

## 跟随测试

1. 使用 `python -m imouse.gui` 启动 GUI。
2. 设置 `Evidence` 和 `Stage`。
3. 点击 `Snapshot`。
4. 确认离线行不声称接收器、HID、iOS 设置、群控规模或 XP 对标已被证明。
5. 选择第一个 `fail`、`pending` 或 `warn` 行并点击 `Run Selected`。
6. 将看板导出到 `evidence/<run_id>_<stage>_industry_current_snapshot.md`。
7. 继续通过 `Procure`、`Routes`、`Kit Gate`、`iOS SOP`、`Rx Bootstrap`、`Rx Setup`、`Shot Bench`、`P1 Trial`、`Acceptance` 和 `Readiness`。

## 边界

- `Snapshot` 是一个当前状态/SOP 映射，不是 JSONL 证据。
- 它不会自动浏览、安装接收器软件、连接 HID 硬件或证明真实 iPhone 响应。
- 它可以识别下一步操作，但只有相同运行的现场证据、保存的截图、Manual/P1 Trial 观察、Acceptance、Readiness、日志和精确设备/iOS 范围才能支持声明。
- 公开的 iMouse/XP/Apple/Some3C 信号是测试的输入，不是本地兼容性或对标证明。
- 当网站兼容性措辞变化时，先更新 `docs/industry_current_state_snapshot_2026.md`，然后使用 `Snapshot` 将其转换为测试行。
