# 场景脚本样例

这些 JSON 用于把 SOP 落成可重复步骤。第一次实机测试时先 dry-run，再根据 GUI 截图预览里的真实坐标、模板和设备 ID 修改脚本。

推荐顺序：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\single_device_smoke.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p2_single_device_stability.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\pilot_4_group_smoke.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p3_pilot4_30min_watchdog.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\stable_10_group_watchdog.json --dry-run
```

实机运行前必须确认：

- `python -m imouse.doctor --markdown evidence\preflight.md` 没有阻断项。
- GUI 或 API 已能注册设备、绑定 HID、启动投屏和截图。
- P1 默认用 `p1_single_device_control_probe.json`，它覆盖组件台账、10 次截图质量、点击、滑动、输入和最终人工结论。
- `p1_single_device_control_probe.json` 和 `p1_receiver_capture_probe.json` 里的 receiver/provider 信息已改成现场真实值；不要保留 `EDIT_ME` 就做实机结论。
- 两个 P1 探针的关键 `record` 开启了 `required_details` 和 `forbid_placeholder_values`；实跑时仍有占位值会直接失败，dry-run 不会失败。
- 脚本里的坐标是从当前设备截图取点得到的安全坐标。
- 每个实机脚本末尾的 `record` 要按真实观察改成 `pass` 或 `fail`。
- 带 `repeat.wait_between` 的脚本在 dry-run 时不会等待；实跑时才会按秒等待。
- 带 `metrics` 的脚本会把平台、Python、CPU 核数、内存、磁盘和人工指标模板写入 evidence。

P1 单台首测按 `docs/p1_single_device_runbook.md` 执行。P2/P3/P4 稳定性扩容按 `docs/p2_p3_stability_runbook.md` 执行，不要在 P1 没有真实 evidence 前直接跑 4 台或 10 台。
