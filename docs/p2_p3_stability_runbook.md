# P2/P3/P4 稳定性实机 Runbook

更新时间：2026-06-08

目标：把 P1 单台 iPhone 首测之后的稳定性验证拆成可执行、可复盘、可扩容的现场流程。这里的核心不是把脚本“跑完”，而是证明真实 iPhone 在连续运行、分组调度、单台故障隔离和资源压力下仍然可控。

本 runbook 适用于三个阶段：

- P2：1 台 iPhone 连续 30 分钟稳定性。
- P3：4 台 iPhone 试点群控，连续 30 分钟。
- P4：10 台 iPhone 稳定性，连续 2 小时。

P1 未通过前不要进入本 runbook。P1 通过定义见 `docs/p1_single_device_runbook.md`。

## 通过定义

P2/P3/P4 通过必须同时满足：

- 每轮都有 `evidence/<run_id>.jsonl` 和 Markdown 汇总。
- 每台设备都有固定编号，能追溯 iPhone、HID、Hub 口、AirPlay 名称、串口和校准文件。
- 脚本里的点击、滑动、输入都由现场人员人工观察确认，不能只看 API 返回。
- 失败必须显式记录 `category`，并尽量关联设备 ID、自动失败截图、人工截图或录屏路径。
- 单台失败不会导致整组脚本无返回；失败设备必须能在 30 秒内定位。
- 所有失败 Top 3 在复盘表中变成下一轮研发任务，而不是继续盲目扩设备数量。

## 0. 阶段门

| 阶段 | 前置条件 | 进入条件 | 退出条件 |
|---|---|---|---|
| P2 | P1 单台闭环通过 | 同一设备可截图、校准、点击、滑动、输入 | 30 分钟无阻断故障，失败可分类 |
| P3 | P2 连续两轮通过 | 4 台设备都完成 P1 基础项 | 4 台 30 分钟稳定，单台失败可隔离 |
| P4 | P3 至少一轮通过 | 10 台设备物料和编号完整 | 2 小时运行，资源和失败曲线可解释 |

停止扩容条件：

- 同一失败分类连续出现 3 次。
- 点击误差超过阶段阈值且无法通过校准解释。
- 投屏断线后不能恢复或恢复耗时无法记录。
- evidence 缺失人工观察，导致结果不可复盘。

## 1. 测试台准备

每轮开始前填写现场台账：

```text
run_id:
stage: P2/P3/P4
git_revision:
PC 型号/系统/内存:
Python:
投屏组件/版本/路径:
网络: PC 有线/无线, VLAN, AP 隔离状态
Hub 品牌/供电/端口编号:
HID 硬件型号/固件:
设备清单: dev_id, iPhone 型号, iOS 版本, AirPlay 名称, 串口, Hub 口
校准文件:
脚本文件:
现场负责人:
```

测试台要求：

- PC 优先有线网络，iPhone 和 PC 在同一 VLAN。
- USB Hub 使用独立供电，端口贴编号。
- 每条线材和每个 HID 模块贴编号，避免失败后无法复现拓扑。
- iPhone 关闭自动锁屏或延长锁屏时间，固定亮度，关闭会遮挡页面的弹窗。
- 每台设备先单独完成五点校准，再加入分组。
- 录屏或人工补充截图目录提前建好，例如 `evidence_artifacts/<run_id>/`；脚本自动截图会保存到 `evidence/<run_id>_artifacts/`。

## 2. 每轮通用 preflight

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.doctor --markdown evidence\<run_id>_doctor.md
```

启动 GUI：

```powershell
.\.venv\Scripts\python -m imouse.gui
```

GUI 中确认：

- 顶部 `Evidence` 填入本轮 `run_id`。
- `Record` 保持勾选。
- `Doctor` 报告已经生成。
- 每台设备注册、绑定 HID、投屏、采集、截图都完成。
- 每台设备都保存或加载了校准。
- 底部 `Manual` 行可以正常写入人工观察。

如果 doctor 仍提示 `uxplay` 缺失，但现场使用的是 Windows Receiver 或有线投屏替代路线，必须在人工记录中写清楚替代组件名称、版本、路径、截图采集方式和限制。

## 3. P2 单台 30 分钟稳定性

推荐 run_id：

```text
p2_dev1_YYYYMMDD_r1
```

dry-run：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p2_single_device_stability.json --dry-run --run-id p2_dev1_YYYYMMDD_r1
```

实跑前修改或确认：

- `dev_1` 是当前真实设备 ID。
- 点击坐标来自当前截图中的安全区域。
- 滑动起止点不会触发危险业务动作。
- 输入框已聚焦，或脚本中已有聚焦动作。
- 脚本末尾 `manual P2 final decision` 不要保留默认占位结论。

实跑：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p2_single_device_stability.json --run-id p2_dev1_YYYYMMDD_r1
.\.venv\Scripts\python -m imouse.evidence_report evidence\p2_dev1_YYYYMMDD_r1.jsonl
```

现场人员每 5 分钟记录一次：

```json
{
  "action": "record",
  "name": "manual P2 round observation",
  "status": "pass",
  "category": "",
  "note": "round=3, screenshot ok, click ok, swipe ok, type ok, no AirPlay disconnect, no HID failure",
  "details": {
    "online_count": 1,
    "screenshot_success": true,
    "airplay_disconnects": 0,
    "hid_failures": 0,
    "click_error_px": 4
  },
  "artifacts": ["evidence_artifacts/p2_dev1_YYYYMMDD_r1/round3.png"]
}
```

P2 通过标准：

- 连续 30 分钟完成 6 轮。
- 截图成功率 99% 以上。
- 每轮自动截图 artifact 可打开，且 `screenshot_quality.ok=true`；黑屏、白屏、过小图或空白图都不能算截图通过。
- 点击误差小于 8 px。
- 投屏断线 0 次，或断线可恢复且记录了原因和耗时。
- HID 无按下不释放、方向错误、重复输入。
- 至少两轮 P2 通过后再进入 P3。

P2 不通过时：

- 不要扩到 4 台。
- 用 `python -m imouse.evidence_report` 生成复盘。
- 把 Top 3 分类写成研发任务，例如 `airplay_stream: 30 分钟内黑屏 2 次`、`hid_click: 第 4 轮点击偏移 15 px`。

## 4. P3 4 台试点群控

推荐 run_id：

```text
p3_pilot4_YYYYMMDD_r1
```

设备命名：

```text
dev_1, dev_2, dev_3, dev_4
group: pilot_4
```

先跑 4 台基础冒烟：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\pilot_4_group_smoke.json --dry-run --run-id p3_pilot4_smoke_YYYYMMDD
.\.venv\Scripts\python -m imouse.script_runner scripts\pilot_4_group_smoke.json --run-id p3_pilot4_smoke_YYYYMMDD
```

再跑 30 分钟 watchdog：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p3_pilot4_30min_watchdog.json --dry-run --run-id p3_pilot4_YYYYMMDD_r1
.\.venv\Scripts\python -m imouse.script_runner scripts\p3_pilot4_30min_watchdog.json --run-id p3_pilot4_YYYYMMDD_r1
.\.venv\Scripts\python -m imouse.evidence_report evidence\p3_pilot4_YYYYMMDD_r1.jsonl
```

每轮人工观察模板：

```text
round=2
online_count=4
screenshot_success_count=4
all_click_observed=yes/no
all_swipe_observed=yes/no
all_type_observed=yes/no
failed_device_ids=
airplay_disconnects=0
hid_failures=0
artifacts=
```

P3 必测故障隔离：

1. 在一轮稳定后，人工断开 `dev_3` 的投屏或 HID。
2. 再跑一轮 `group_click`、`group_swipe`、`group_type`。
3. 观察 `dev_1/dev_2/dev_4` 是否继续返回并真实响应。
4. 在 Manual 记录 `dev_3` 的失败分类和其他设备状态。
5. 恢复 `dev_3`，记录恢复耗时。

P3 通过标准：

- 4 台连续 30 分钟完成 6 轮。
- 单台失败不会拖垮全组。
- 每台设备的失败次数、投屏断线次数、HID 失败次数都能追溯。
- 4 台截图、点击、滑动、输入都有人工观察。
- 失败分类集中在可解释范围内；未知错误不能超过 1 个。

## 5. P4 10 台 2 小时稳定性

推荐 run_id：

```text
p4_stable10_YYYYMMDD_r1
```

设备命名：

```text
dev_1 ... dev_10
group: stable_10
```

P4 不是把 P3 脚本机械放大。10 台时要重点看资源、Hub、网络、投屏重连和日志可读性。

运行方式：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\stable_10_group_watchdog.json --dry-run --run-id p4_stable10_YYYYMMDD_r1
```

实跑时每 30 分钟跑一轮 watchdog，并在 GUI Manual 补现场观察：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\stable_10_group_watchdog.json --run-id p4_stable10_YYYYMMDD_r1
```

建议时间轴：

| 时间 | 动作 |
|---|---|
| T+0 | doctor、设备注册、分组保存、全量截图 |
| T+30 | 跑一轮 stable_10 watchdog，记录 metrics 和人工观察 |
| T+60 | 跑第二轮，记录失败设备和资源曲线 |
| T+90 | 跑第三轮，人工断开 1 台验证隔离 |
| T+120 | 跑第四轮，生成 evidence report 和复盘 |

P4 通过标准：

- 10 台连续 2 小时可运行。
- 每 30 分钟至少有一次 metrics 和人工观察。
- 截图成功率 95% 以上。
- 投屏断线可恢复，且恢复步骤和耗时有记录。
- HID 失败率低于 5%，且按 Hub 口、线材、设备 ID 可定位。
- GUI 或日志能在 30 秒内定位失败设备。

## 6. 失败分类与现场动作

| category | 现场先做 | 研发需要的证据 |
|---|---|---|
| `airplay_discovery` | 查同网段、AP 隔离、防火墙、服务名冲突 | 网络拓扑、receiver 日志、iPhone 录屏 |
| `airplay_stream` | 查黑屏、花屏、断线、延迟、硬解 | 断线时间点、截图、投屏组件日志 |
| `capture` | 查截图尺寸、窗口句柄、黑屏 | 原始截图、窗口标题、设备 ID |
| `calibration` | 重做五点校准，记录 active/target | 校准文件、误差表、横竖屏状态 |
| `hid_discovery` | 换线、换 Hub 口、查驱动和供电 | 插拔前后串口列表、Hub 口编号 |
| `hid_bind` | 查端口占用、波特率、固件协议 | 绑定请求、错误文本、硬件版本 |
| `hid_click` | 查偏移、按下不释放、越界 | 点击坐标、观察位置、录屏 |
| `hid_swipe` | 查方向、轨迹、释放动作 | 起止点、步数、录屏 |
| `hid_keyboard` | 查焦点、输入法、字符集 | 输入文本、焦点截图、iOS 键盘状态 |
| `group_dispatch` | 查组内设备、重复 ID、单台隔离 | 分组 JSON、逐设备返回 |
| `performance` | 查 CPU、内存、磁盘、网络 | metrics、任务管理器截图、设备数 |
| `business_state` | 查业务页面弹窗、登录态、风控 | 页面截图、账号状态、业务步骤 |

记录失败时优先使用这种结构：

```json
{
  "action": "record",
  "name": "manual failure triage",
  "status": "fail",
  "category": "airplay_stream",
  "note": "dev_2 black screen at round 4, recovered after receiver restart",
  "details": {
    "device_id": "dev_2",
    "round": 4,
    "recover_seconds": 42,
    "receiver": "Windows Receiver",
    "hub_port": "hub-a-03"
  },
  "artifacts": [
    "evidence_artifacts/p3_pilot4_YYYYMMDD_r1/dev_2_black_screen.png",
    "evidence_artifacts/p3_pilot4_YYYYMMDD_r1/dev_2_receiver.log"
  ]
}
```

## 7. 复盘输出

每轮结束后执行：

```powershell
.\.venv\Scripts\python -m imouse.evidence_report evidence\<run_id>.jsonl --markdown evidence\<run_id>_review.md
.\.venv\Scripts\python -m imouse.evidence_report evidence\<run_id>.jsonl --json
```

复盘会议只看四件事：

- 本轮是否达到阶段门。
- 失败 Top 3 是什么分类。
- 哪些失败可以现场配置解决，哪些必须研发改代码或换硬件。
- 下一轮是否允许扩容，还是必须先复现并修复。

研发任务模板：

```text
标题: [P3][airplay_stream] dev_2 第 4 轮黑屏，receiver 重启后恢复
环境: run_id, git_revision, PC, 投屏组件, iOS, iPhone 型号
复现步骤: 1/2/3
期望结果:
实际结果:
证据: evidence jsonl, review md, 截图/录屏/日志路径
影响范围: P2/P3/P4
下一步建议:
```

## 8. 当前仓库边界

截至 2026-06-08，本仓库已能离线验证 API、GUI、脚本运行器、evidence 和 doctor；但仍不能证明真实 iPhone 已被完美控制。

已知阻断：

- 当前机器缺 `uxplay`，所以默认 UxPlay 投屏链路未验证。
- 当前只看到 `COM1`，尚未接入真实 HID 硬件。
- XP 专用硬件和 4.4 固件协议未验证。
- 真实 iOS 17/18/26、横屏、快准狠鼠标模式和长期稳定性都需要现场证据。

行业经验上，iOS 群控能否交付主要卡在投屏稳定性、HID 坐标与固件、截图采集、失败隔离、现场证据闭环，而不是单纯的 GUI 功能数量。因此 P2/P3/P4 的核心产出是证据和问题分类，不是脚本运行次数。

## 9. 参考资料

- iMouse 官网产品概述：`https://www.imouse.cc/`
- iMouse XP API 文档：`https://www.imouse.cc/XP版API文档/`
- iMouse XP Python 开发文档：`https://www.imouse.cc/python-xp/`
- BestMoon iMouse XP New version：`https://bestmoon-doc.gitbook.io/bestmoon/xp-tool-ios/imouse-xp-new-version`
- Apple AirPlay 屏幕镜像说明：`https://support.apple.com/en-us/ht201343`
- Apple iPhone 指针设备说明：`https://support.apple.com/en-us/111775`
