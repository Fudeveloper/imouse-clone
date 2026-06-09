# 项目 Readiness 审计

更新时间：2026-06-08

`imouse.readiness` 用于回答一个严肃问题：当前仓库和当前 evidence 到底能证明什么，不能证明什么。

它不会替代实机测试，也不会把 dry-run 当作 iPhone 已响应。它只是把文档、脚本、模块、doctor 和 acceptance gate 汇总成阶段状态，避免研发复盘时口径漂移。

P0 文档资产包含 `docs/mainstream_route_decision.md` 和 `docs/xp_parity_matrix.md`。前者决定 P1 前的主流路线、receiver、HID、采购和停止线；后者把 iMouse XP 公开信号、当前实现、验收证据、差距和下一步动作放在一张表里，用来防止研发排期和验收口径脱节。

## 什么时候用

- 每次准备 P1 单台实机前。
- 每次实机测试结束、准备判断是否晋级 P2/P3 前。
- 每次有人问“现在是不是已经实现 iOS 完美控制”时。
- 每次更换 receiver、HID、Hub、线材或 iOS 版本后。

## 基本命令

只看当前是否具备 P1 条件：

```powershell
.\.venv\Scripts\python -m imouse.readiness --target p1
```

当前本机如果仍缺 `uxplay` 且没有实机 evidence，预期结果是 `FAIL`。这不是坏事，它是在保护结论。

带 evidence 跑 P1 判断：

```powershell
.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\p1_dev1_YYYYMMDD.jsonl --markdown evidence\p1_dev1_YYYYMMDD_readiness.md
```

只检查离线资产是否齐全，不跑 doctor：

```powershell
.\.venv\Scripts\python -m imouse.readiness --target p0 --skip-doctor
```

输出完整 JSON：

```powershell
.\.venv\Scripts\python -m imouse.readiness --target p1 --evidence evidence\p1_dev1_YYYYMMDD.jsonl --json
```

## 阶段语义

| 阶段 | 通过含义 | 不代表 |
|---|---|---|
| P0 | 文档、脚本、核心模块存在 | iPhone 已被控制 |
| P1 | P1 evidence 通过，doctor 无 fail | 4 台群控稳定 |
| P2 | 单设备稳定 evidence 通过，doctor 无 fail | 4 台/10 台可扩展 |
| P3 | 4 台 group evidence 通过，doctor 无 fail | 10 台长稳 |
| P4 | 10 台稳定 evidence 通过，doctor 无 fail | XP 全商业能力 |

## 输出字段

关键字段：

- `stage_status.p0.ok`：离线文档、脚本、模块是否齐。
- `stage_status.p1.ok`：是否有 P1 实机 evidence 且 doctor 无 fail。
- `claims.real_ios_control_verified`：只有 P1 通过才为 `true`。
- `claims.ios_group_control_verified`：只有 P3 或 P4 通过才为 `true`。
- `claims.do_not_claim_perfect_ios_control`：为 `true` 时，不能说已经实现 iOS 完美控制。
- `blockers`：当前阻断项，例如缺 evidence、doctor fail、acceptance fail。

P1/P2/P3/P4 的 acceptance gate 会检查组件追踪：receiver/capture provider、capture method、HID provider、HID 标识或串口、iPhone 标识和 iOS 版本。缺这些字段时，即使有截图和人工 pass，也不能晋级。

## 和现有工具的关系

| 工具 | 职责 |
|---|---|
| `imouse.doctor` | 环境、依赖、receiver、串口、目录状态 |
| `imouse.script_runner` | 执行 JSON 场景并写 evidence |
| `imouse.field_packet` | 生成本轮现场执行包，串联 doctor、GUI、脚本、验收和失败分流 |
| `imouse.route_decision` | 生成/校验 P1 receiver/HID 路线决策记录，可写入组件台账 evidence，但不替代截图和人工观察 |
| `imouse.evidence_report` | 汇总某次 evidence |
| `imouse.acceptance` | 判断某份 evidence 是否通过 P1/P2/P3/P4 |
| `imouse.readiness` | 汇总仓库资产、doctor 和 acceptance，给出阶段状态 |

## 当前项目的预期状态

截至 2026-06-08，在没有 UxPlay、没有 HID 硬件、没有真实 iPhone evidence 的机器上：

- P0 可以用于检查离线资产是否齐全。
- P1 必须失败，因为真实 iPhone 投屏、截图、点击、滑动、输入还没有 evidence。
- `binary:uxplay` fail 会阻断默认 UxPlay 原型路线。
- 串口只有 `COM1` 时，不能证明 CH9329 或 XP 专用硬件已接入。

这类失败要保留，不要绕过。真正的下一步是先用 `python -m imouse.field_packet --stage p1 --run-id <run_id>` 生成本轮执行包，再按 `p1_single_device_runbook.md` 和 `p1_single_device_control_probe.json` 拿第一份实机 evidence；`p1_receiver_capture_probe.json` 只作为投屏/截图专项排障探针。
