# XP Roadmap

本页描述 GUI 里的 `Roadmap` 面板。它的目的不是证明已经对标 iMouse XP，而是把公开 XP 信号、行业 SOP、本地实现、实机证据门和下一步研发动作压到同一张表里。

## GUI 入口

- `Live Probe -> Roadmap` 打开研发路线面板。
- `Export` 导出 `evidence/<run_id>_<stage>_xp_roadmap.md`。
- `Run Selected` 会跳到当前行对应的 GUI 动作，例如 Verify、Kit Gate、Shot Bench、Control Bench、P1 Trial、Bench、Library、Attach Log、Dashboard 或 Goals。
- Sources、Industry、Core、Iter Radar、XP Timeline 和 Start Pack footer 也提供 Roadmap 快捷入口。

## Roadmap 行

| Lane | 目标 | 研发含义 | 证据门 |
|---|---|---|---|
| P0 offline/API base | P0 | API、SDK、GUI、脚本、callback、evidence helper 保持离线可验证。 | 单元测试、compileall、API/client 测试、XP Gap；不能证明实机控制。 |
| P1 route and bench lock | P1 | 先锁定 receiver、HID、iPhone、Hub、Cable、operator。 | Route Decision、Doctor、Hardware Bench、组件元数据。 |
| P1 receiver/capture proof | P1 | 先证明画面真实、当前、非黑屏、绑定正确，再做 HID。 | Shot Bench、截图质量、receiver 身份、日志。 |
| P1 HID click/swipe/type proof | P1 | 证明真实 iPhone 上可见点击、滑动、输入和释放行为。 | P1 Trial、Control Bench、manual observation、HID id/firmware。 |
| P1 calibration and input matrix | P1 | 把截图坐标稳定映射到设备坐标。 | 五点校准、像素误差、输入矩阵、方向/安全区记录。 |
| XP hardware/wired/4.4 parity lane | XP parity | 把 generic HID/receiver 进展和 XP 专用硬件、有线投屏、4.4 固件、硬解码对标分开。 | XP 侧旁证、固件/绑定日志、receiver/decoder 指标；没有旁证不能通过。 |
| P2 vision/script replay | P2 | 从真实截图沉淀模板、区域、阈值、OCR 和可回放场景。 | Template Asset Index、Scenario JSON、Timeline、Triage、Review。 |
| P2 observability and recovery | P2 | 每个失败都能分流到设备、receiver、HID、Hub/Cable、脚本、业务状态或环境，并有恢复演练记录。 | Callback、Attach Log、Matrix、Issue Triage、Rerun Playbook、Recovery Drill、metrics、Review。 |
| P3/P4 scale and ops | P3/P4 | 单机稳定后再做 4 台试点、10 台稳定和运维能力。 | per-device artifacts、metrics、logs、recovery notes、Dashboard、Readiness。 |
| Claim, SOP, and docs closure | P0-P4 | 文档、SOP、验收目标只能写到当前证据能支撑的阶段。 | Goal Gate、Start Pack、Evidence Pack、Acceptance、Readiness、manual observations。 |

## 使用顺序

1. 打开 Sources 和 Industry，确认公开来源和行业路线只是研发输入。
2. 打开 Core 和 XP Gap，确认 API/SDK ready 没有被当成 receiver/HID/iPhone 通过。
3. 打开 Roadmap，找到第一个 `fail`、`pending` 或 `warn` 行。
4. 点 `Run Selected` 进入对应 GUI 工具补证据。
5. 回到 Start Pack，把 Roadmap、Verify、Core、Routes、Kit Gate、Bench、Wizard、Acceptance、Readiness 串成首轮实机测试。

## 边界

- Roadmap 不写 JSONL evidence。
- Roadmap 不证明真实 iOS 控制。
- Roadmap 不证明 XP parity。
- `real_ios_verified=False` 时，HID、校准、输入、claim closure 只能是 `warn` 或 `fail`，不能被 Roadmap 提升为通过。
- 即便 generic HID 或本地 API 通过，XP 专用硬件、有线投屏、4.4 固件、自动绑定、硬解码仍然需要单独旁证。
