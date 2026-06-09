# Preflight Doctor 环境检查

更新时间：2026-06-08

`imouse.doctor` 用于在实机测试前检查当前机器是否具备跑 iMouse XP 对标原型的基本条件。它不会证明 iOS 已经可控，但能提前暴露环境问题，避免现场一上来就卡在依赖、串口或服务端口上。

## 基本命令

```powershell
.\.venv\Scripts\python -m imouse.doctor
```

输出 JSON：

```powershell
.\.venv\Scripts\python -m imouse.doctor --json
```

写入 Markdown 报告：

```powershell
.\.venv\Scripts\python -m imouse.doctor --markdown evidence\preflight_YYYYMMDD.md
```

如果本轮已经填写 `Route Decision`，建议把它传给 doctor。这样使用 `windows_receiver`、`wired` 或 `capture_card` 替代 UxPlay 时，doctor 会检查 receiver 名称、版本、路径、启动命令、AirPlay 名称、采集方式和窗口绑定，而不是只盯着 `uxplay`：

```powershell
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\p1_dev1_YYYYMMDD_route_decision.json --markdown evidence\p1_dev1_YYYYMMDD_doctor.md
```

也可以直接传 receiver config JSON：

```powershell
.\.venv\Scripts\python -m imouse.doctor --receiver-config state\receiver_provider.json --json
```

如果本地 API 服务已经启动，也检查服务：

```powershell
.\.venv\Scripts\python -m uvicorn imouse.server:app --host 127.0.0.1 --port 9911
.\.venv\Scripts\python -m imouse.doctor --server-url http://127.0.0.1:9911
```

GUI 里也有同等入口：

1. 启动 `python -m imouse.gui`。
2. 顶部 `Evidence` 填写本轮 `run_id`。
3. 如需检查本地服务，先点击 `Start Local`。
4. 点击 `Doctor`。
5. 如果使用 Windows Receiver、有线投屏或采集卡替代 UxPlay，再点 Live Probe 里的 `Receiver`，确认 provider、`binary:uxplay` 降级、采集绑定和证据边界。

GUI 会把报告写到 `evidence/<run_id>_doctor.md`。如果 doctor 总体为 `fail`，GUI evidence 也会记录为失败事件，而不是把“按钮执行成功”误记成通过。

## 检查项

| 检查项 | 含义 |
|---|---|
| `python` | 当前 Python 版本。推荐 Python 3.13，Python 3.14 可能缺 PaddlePaddle wheel |
| `module:*` | Python 依赖是否可导入 |
| `receiver_provider` | 可选检查，验证 route decision 或 receiver config 里的 receiver 路线是否可预检 |
| `binary:uxplay` | 当前 UxPlay/AirPlay 原型链路是否可用 |
| `binary:xvfb` | 当前 X11/UxPlay 原型链路可能需要；Windows 原生路线可作为警告处理 |
| `serial_ports` | 当前系统能否看到串口/HID 硬件 |
| `workspace:writable` | 工作区是否可写 |
| `dir:*` | 运行目录是否存在，缺失时运行时会创建 |
| `state:*` | 分组、校准、设备组件档案状态文件是否已存在 |
| `server` | 可选检查，探测 XP 风格 `/api` 服务是否响应 |

## 状态解释

- `ok`：当前项可用。
- `warn`：不是立即阻断，但需要关注，例如没有串口、状态文件还没创建。
- `fail`：会阻断对应链路，例如默认 UxPlay 路线缺失会阻断当前 AirPlay 原型验证。

如果 `--route-decision` 中的替代 receiver 通过预检，`binary:uxplay` 会从硬失败变成 `warn`，表示本轮不走默认 UxPlay 原型。但这只证明替代 receiver 配置可预检，不证明截图或 iPhone 响应已经通过。GUI `Receiver` / Receiver Route Gate 会把这条规则可视化，但仍不写 JSONL evidence，也不证明真实 iOS 控制。

整体状态：

- 只要有 `fail`，整体就是 `fail`。
- 没有 `fail` 但有 `warn`，整体是 `warn`。
- 全部 `ok` 才是 `ok`。

## 当前仓库的典型结论

在没有安装 UxPlay、没有接 HID 硬件的机器上，doctor 预期会看到：

- Python 模块大多为 `ok`。
- `binary:uxplay` 为 `fail`。
- `serial_ports` 可能为 `warn` 或只看到系统串口。
- `state/groups.json`、`state/calibration.json`、`state/device_profiles.json` 未创建时为 `warn`。

这代表：可以继续做 API/GUI/脚本离线验证，但不能宣称投屏、截图、点击、滑动、输入实机通过。

## 实机前通过标准

进入真实 iPhone 控制测试前，至少满足：

- Python 使用 3.13。
- Python 模块检查全部 `ok`。
- `binary:uxplay` 或替代投屏服务可用，并记录版本/路径。
- 能看到目标 HID 硬件串口，插拔时列表有变化。
- 工作区可写。
- 启动服务后 `--server-url` 检查为 `ok`。

如果使用 XP 专用硬件或 Windows 原生投屏服务替代当前 UxPlay/X11 原型，也要在 route decision 和 evidence 中记录替代组件名称、版本、路径和操作方式。替代 receiver 预检通过后，仍必须用 GUI `Screenshot`、`Manual`、`Acceptance` 和 `Readiness` 证明真实链路。
