# GUI SOP Problem Ledger

`Problems` 是 GUI 里的长期问题沉淀层。它把行业常见坑、当前 JSONL 失败、Issue Triage、Rerun Playbook 和证据停止线合并到一张可导出的 SOP 问题台账。

它解决的问题不是“再做一个报表”，而是防止现场问题只停留在聊天记录或某次失败截图里。每个问题行都要回答：

- 这属于行业风险还是本轮 field failure；
- 当前失败次数和 failure category；
- 预防 SOP；
- 第一条最小复现/重跑路径；
- 是否需要 fresh `run_id`；
- 必须保留什么 evidence；
- 什么条件下必须停止宣传或扩容；
- 下一步应该打开哪个 GUI 工具。

## GUI 入口

在底部 `Live Probe` 行点击 `Problems`。

常用顺序：

1. 跑 `Timeline` 和 `Triage`，确认失败类别。
2. 打开 `Pitfalls`，确认这类问题是否已在行业/SOP 风险库里。
3. 打开 `Problems`，把行业风险和本轮失败合成台账。
4. 选中一行点 `Run Selected`，跳到 Control Bench、Shot Bench、Route、Doctor、Matrix、Scenario Library 等最小重跑入口。
5. 点 `Export` 生成 `evidence/<run_id>_<stage>_sop_problem_ledger.md`。

## 边界

- Problem Ledger 不写 JSONL evidence。
- Problem Ledger 不证明真实 iOS 控制。
- Problem Ledger 不证明 XP parity。
- `field_failure` 行只能说明问题已经被归类；关闭问题仍需要重跑证据、人工观察、Acceptance 和 Readiness。
- `industry_risk` 行是预防 SOP；没有失败不代表风险不存在。

## P1 使用方式

P1 首测后优先看这些行：

| 问题 | 首看证据 | 最小动作 |
|---|---|---|
| Receiver/capture | screenshot_quality、截图 artifact、receiver log | Shot Bench + Attach Log |
| HID no response | manual_observation、Control Bench、HID/serial ledger | Control Bench + Manual |
| Calibration drift | 当前截图、active area、五点校准记录 | P1 Trial + calibration |
| Vision drift | template asset、region、failure screenshot | Assets + Scenario Library |
| Claim boundary | Acceptance、Readiness、real_ios_verified | Goals + Readiness |

## 关闭规则

不要只因为“下一次脚本跑过了”就关闭问题。关闭必须满足：

- 同一 `run_id` 或明确 fresh `run_id` 的问题重跑路径已经执行；
- 失败类别、设备、组件台账、截图/日志 artifact 都能追溯；
- 操作者写入真实 iPhone 观察；
- Acceptance 和 Readiness 的结果支持当前阶段；
- 如果涉及 XP 专用硬件或 4.4 固件，必须保留合法硬件同场证据。
