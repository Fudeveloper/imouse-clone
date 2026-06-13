# GUI Real-run Guard

`Real-run Guard` 是非 dry-run 场景或命令队列触碰硬件之前的最后一个 GUI 停止线。它保护现场运行免受未验证的路由、Doctor 或设备范围状态的影响。

它不运行场景，不写入成功证据，也不证明真实 iPhone 响应。它只决定 GUI 是否被允许尝试真实运行。

## 何时运行

当以下情况时自动检查守卫：

- `Dry Run` 被禁用且操作者点击场景的 `Run`。
- `Dry Run` 被禁用且操作者运行命令队列。

如果被阻止，GUI 导出：

```text
evidence/<run_id>_<stage>_real_run_guard.md
```

且不启动真实操作。

## 检查项

| 检查 | 真实运行前要求 | 首选修复路径 |
|---|---|---|
| `device_scope` | 所选物理设备数量满足当前阶段要求。 | 选择设备 ID，然后刷新 Live Probe 和 Runner。 |
| `route_decision` | Route Decision 已加载、有效、就绪，且无占位符/未解决阻塞项。 | Route Edit、Receiver、Rx Score、Rx Bootstrap、Rx Setup。 |
| `doctor` | Doctor 无硬失败。路由感知的非 UxPlay 警告仅在备选接收器路由明确时才允许。 | Doctor、Local、Receiver、Rx Setup。 |

## 状态含义

- `blocked`：不要运行真实硬件操作。先修复阻塞项。
- `allow`：GUI 可以尝试真实运行。这不是通过。

允许的守卫报告仅证明运行前停止线足够清晰可以尝试。实际运行仍需要 JSONL 事件、截图工件、通道分离的 Manual 观察、Acceptance、Readiness 和精确的设备/iOS/接收器/HID 范围。

## 所需操作者行为

1. 保持 `Dry Run` 启用，直到 `Route Decision`、`Doctor` 和所选设备正确。
2. 如果守卫阻止，打开导出的守卫报告并遵循 `Next Actions`。
3. 在更改接收器、HID、iPhone、Hub、线缆、路由或之前记录的失败后，启动新的 `run_id`。
4. 在守卫允许后，运行场景一次，检查 Timeline/Triage，然后运行 Acceptance 和 Readiness。
5. 永远不要将 `guard ok` 用作 iOS 控制的演示措辞。

## 停止线

- 如果路由占位符仍然存在，则停止。
- 如果 `allowed_to_run_p1` 为 false，则停止。
- 如果 Doctor 有任何硬失败，则停止。
- 如果所选设备列表与物理工作台不匹配，则停止。
- 如果操作者无法说出精确的接收器、HID、Hub 端口、线缆、iPhone 型号和 iOS 版本，则停止。
- 如果团队试图通过直接调用底层 API 绕过 GUI 守卫，则停止。

## 边界

Real-run Guard 是一个运行前安全门控。它不是截图新鲜度、HID 移动、文字输入、XP 硬件对标、广泛 iOS 兼容性或 iOS 完美控制的证据。
