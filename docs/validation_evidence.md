# 验证证据记录说明

更新时间：2026-06-08

本项目不能只靠“我点了一下好像能用”来验收。每轮实验都要留下可复盘证据，至少能回答：

- 这轮测试是什么时间跑的？
- 哪些设备参与了？
- 哪一步通过、哪一步失败？
- 失败时是投屏、截图、视觉识别、HID、业务页面还是分组调度问题？
- 后续研发能否根据日志和截图复现？

## 证据文件

GUI 和验证工具会把记录写到：

```text
evidence/<run_id>.jsonl
```

每行是一个 JSON 事件：

```json
{
  "ts": "2026-06-08T12:00:00Z",
  "run_id": "gui_20260608_120000",
  "step": "Batch click",
  "status": "pass",
  "device_ids": ["dev_1", "dev_2"],
  "details": {"ok": true, "count": 2},
  "artifacts": []
}
```

字段说明：

- `ts`：UTC 时间。
- `run_id`：本轮测试 ID。
- `step`：测试步骤或 GUI 操作名称。
- `status`：`pass`、`fail`、`info`、`skip`。
- `device_ids`：参与设备。
- `details`：接口返回、错误信息、坐标、分组名等。
- `artifacts`：截图、模板、日志路径。

GUI 和脚本都会记录 `details.screenshot_quality`。脚本实跑时，`screenshot` 步骤会自动保存图片到 `evidence/<run_id>_artifacts/`，并把路径写入 `artifacts`；黑屏、白屏、过小图或无效图会让截图步骤失败。如果失败步骤能确定单台 `device_id`，运行器也会尽力自动保存一张失败截图。截图失败不会覆盖原始错误，失败截图错误会进入 `details.failure_screenshot_error`。

运行产生的 `evidence/` 已加入 `.gitignore`，避免现场数据混进代码仓库。

## GUI 使用方式

启动：

```powershell
.\.venv\Scripts\python -m imouse.gui
```

顶部 `Evidence` 行包含：

- 输入框：当前 `run_id`，默认自动生成，例如 `gui_20260608_120000`。
- `Record`：勾选后自动记录 GUI API 操作。
- `Summary`：把当前 JSONL 汇总成 `evidence/<run_id>.md`。
- `Review`：在已有 JSONL 时生成 `evidence/<run_id>_review.md`，并在日志里显示失败分类、metrics 样本数和总失败数。
- `Attach Log`：导入 receiver/HID 文本日志，生成 `evidence/<run_id>_callback_log.md`；勾选 `Record` 时会追加 `Attach Log triage` JSONL，记录日志 severity/category 统计和样例行。它用于 Triage/Recovery 分流，不替代真实 iPhone 人工观察。
- `Rerun`：读取已有 JSONL、Triage 和阶段 gate，生成 `evidence/<run_id>_<stage>_rerun_playbook.md`；它不写 JSONL，只指导下一轮最小复测。
- `Recovery`：读取已有 JSONL、Triage 和阶段 gate，生成 `evidence/<run_id>_<stage>_recovery_drill.md`；导出本身不写 JSONL，但 GUI 弹窗里的 `Record Pass` / `Record Fail` 会把选中恢复 lane 的执行结果写成 `recovery_drill` evidence。该证据只证明恢复动作和验证结果被记录，不能替代 `Manual` / `P1 Trial` 的真实点击、滑动、输入观察。

底部 `Operation Log` 上方的 `Manual` 行用于记录人工观察：

- `Manual`：步骤名，例如 `click observed on dev_1`。
- `Status`：`pass`、`fail`、`info`、`skip`。
- `Category`：失败分类，例如 `hid`、`airplay_stream`、`capture`；通过或普通信息可留空。
- `Note`：人工观察结果，例如 `iPhone actually opened Settings`。
- `Artifact`：失败截图、模板、录屏或外部日志路径。
- `Record`：写入同一个 evidence JSONL。

建议命名：

- 单设备首轮：`single_dev1_YYYYMMDD`
- 4 台小规模：`pilot_4_YYYYMMDD`
- 10 台稳定性：`stable_10_YYYYMMDD`
- 失败复现：`repro_<issue>_YYYYMMDD`

## 单设备留痕步骤

1. 设置 `run_id`，保持 `Record` 勾选。
2. 运行 `python -m imouse.doctor --markdown evidence\preflight_<run_id>.md`，把 preflight 报告作为本轮附件。
3. `Start Local`，确认服务启动。
4. `Ping`，记录设备列表。
5. 注册设备，记录设备状态。
6. `Scan`，记录串口列表。
7. `Bind`，记录端口和状态变化。
8. `Start AirPlay`、`Start Capture`、`Screenshot`，记录截图结果。
9. 点击截图预览取坐标，记录坐标和 RGB。
10. `Save Crop` 保存模板，记录模板路径。
11. `Find`、`Find Color`、`OCR`、`Find Text`，记录识别结果。
12. `Click`、`Swipe`、`Type` 后，人工观察 iPhone 是否真实响应。
13. 用底部 `Manual` 行记录观察结果，失败时选择分类并填写截图或录屏路径。
14. 点击 `Summary` 生成 Markdown 汇总。
15. 点击 `Review` 生成复盘报告；如果 GUI 提示 evidence JSONL 不存在，说明本轮还没有可复盘证据。
16. 如有 receiver、capture、HID、USB、iPhone 或系统日志，点击 `Attach Log` 导入；确认 `Attach Log triage` 已写入 JSONL，失败日志应进入对应 category。
17. 点击 `Rerun` 生成下一轮最小复测表，确认失败类别、fresh run_id 规则、证据保留项和停止线。
18. 点击 `Recovery` 生成恢复演练表，按恢复步骤执行后必须把验证结果重新写入 JSONL 或附件。

通过标准：

- JSONL 中每个关键步骤都有记录。
- 失败步骤必须有 `fail` 事件和错误文本。
- 截图、模板、自动失败截图或人工失败截图路径要能在记录中追溯；截图步骤必须有 `screenshot_quality.ok=true` 才能作为有效画面证据。
- 找图模板不能是纯色或低纹理模板；GUI Save Crop 和脚本本地模板校验都会记录或提示质量问题。

## 群控留痕步骤

4 台小规模：

1. 设置 `run_id=pilot_4_YYYYMMDD`。
2. 注册并绑定 4 台设备。
3. 保存分组 `pilot_4`。
4. 加载分组后执行批量 `Click`、`Swipe`、`Type`。
5. 用 `Manual` 行记录每台设备的真实响应情况。
6. 单台断开后再执行一轮，确认其它设备仍返回结果。
7. 生成 Markdown 汇总和 Review 复盘报告。

10 台稳定性：

1. 设置 `run_id=stable_10_YYYYMMDD`。
2. 保存分组 `stable_10`。
3. 连续运行 2 小时。
4. 每 30 分钟执行一轮分组批量操作。
5. 每轮记录 CPU、内存、网络、FPS、投屏断线次数、HID 失败次数。
6. 结束后生成 Markdown 汇总和 Review 复盘报告，并把失败截图路径写入记录。

## Python 调用

优先使用 JSON 脚本运行器：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\pilot_4.json --run-id pilot_4_YYYYMMDD
```

需要在自定义 Python 脚本里记录时，可以直接使用：

```python
from imouse.validation import ValidationRecorder

recorder = ValidationRecorder("pilot_4_20260608")
recorder.append(
    "batch click",
    "pass",
    device_ids=["dev_1", "dev_2"],
    details={"x": 100, "y": 100, "ok": True},
)
recorder.write_summary_markdown()
```

脚本运行器格式见 `docs/script_runner.md`。

## 命令行复盘

已有 evidence JSONL 时，可以不用打开 GUI，直接生成 Markdown 复盘报告：

```powershell
.\.venv\Scripts\python -m imouse.evidence_report evidence\pilot_4_YYYYMMDD.jsonl
```

指定输出路径：

```powershell
.\.venv\Scripts\python -m imouse.evidence_report evidence\pilot_4_YYYYMMDD.jsonl --markdown evidence\pilot_4_YYYYMMDD_review.md
```

输出 JSON 摘要：

```powershell
.\.venv\Scripts\python -m imouse.evidence_report evidence\pilot_4_YYYYMMDD.jsonl --json
```

GUI 顶部 `Review` 调用的是同一套汇总逻辑，适合现场测试结束后立即看失败分类和下一轮排查建议；命令行适合把报告纳入批处理或 CI。

## 阶段门验收

生成 evidence 后，再跑机器可判定的阶段门。它不会替代人工观察，但能防止“没有设备 ID、没有组件元数据、没有人工 pass、没有截图质量样本、没有 metrics”这类证据缺口被误认为通过。

P1 单设备：

```powershell
.\.venv\Scripts\python -m imouse.acceptance evidence\single_dev1_YYYYMMDD.jsonl --gate p1 --markdown evidence\single_dev1_YYYYMMDD_acceptance.md
.\.venv\Scripts\python -m imouse.acceptance evidence\single_dev1_YYYYMMDD.jsonl --gate p1 --gap-markdown evidence\single_dev1_YYYYMMDD_p1_gap.md
```

P2/P3/P4：

```powershell
.\.venv\Scripts\python -m imouse.acceptance evidence\p2_dev1_YYYYMMDD.jsonl --gate p2
.\.venv\Scripts\python -m imouse.acceptance evidence\pilot_4_YYYYMMDD.jsonl --gate p3
.\.venv\Scripts\python -m imouse.acceptance evidence\stable_10_YYYYMMDD.jsonl --gate p4
```

当前内置硬门槛：

| gate | 设备追踪 | 组件追踪 | 人工 pass | 截图质量 pass | metrics |
|---|---:|---:|---:|---:|---:|
| P1 | >= 1 | >= 1 | >= 1 | >= 1 | 0 |
| P2 | >= 1 | >= 1 | >= 2 | >= 2 | >= 1 |
| P3 | >= 4 | >= 4 | >= 1 | 0 | >= 1 |
| P4 | >= 10 | >= 10 | >= 2 | 0 | >= 1 |

所有阶段都要求 evidence 非空、没有 `fail` 事件，并且每台晋级设备都能追到组件元数据。组件追踪至少要包含 receiver/capture provider、capture method、HID provider、HID 标识或串口、iPhone 标识和 iOS 版本。P3/P4 的截图样本不强制每台设备都有，是因为群控阶段可能通过分组返回和人工观察证明；但如果现场有投屏/截图不稳定，仍应在场景脚本里显式加入截图步骤，并把失败截图写入 artifacts。

`--gap-markdown` 会把失败的 acceptance check 转成补证据清单，例如提示到 GUI 里补 `Record Metadata`、`Screenshot`、`Manual`、分组设备追踪或 metrics。它不写 evidence，不证明实机通过，只用于指导下一轮补证据。

组件元数据可以通过 GUI 底部 `Metadata` 行点击 `Record Metadata` 写入，也可以通过 `scripts/p1_single_device_control_probe.json` 或 `scripts/p1_receiver_capture_probe.json` 的首个 `record` 步骤写入。GUI 会同时把组件档案持久化到 `state/device_profiles.json`，但 acceptance 仍以本轮 evidence JSONL 中的 `Component metadata` 事件为准；每台设备必须单独记录，不要把一组设备共用同一套 HID/iPhone 元数据。

复盘报告会包含：

- 状态计数：`pass/fail/info/skip`。
- 设备事件计数。
- 失败分类计数。
- metrics 样本数、最新指标、最大内存占用、最大磁盘占用。
- 失败列表：时间、步骤、分类、设备、附件、details。
- 自动建议：根据失败分类和资源指标给出下一轮排查方向。

## 复盘分类

失败原因建议统一归类：

- `airplay_discovery`：找不到投屏接收端。
- `airplay_stream`：黑屏、花屏、断线、延迟异常。
- `capture`：截图失败或尺寸异常。
- `vision_template`：找图误判或漏判。
- `vision_color`：找色误判或漏判。
- `ocr`：模型、缓存、识别结果异常。
- `hid`：鼠标/键盘无响应、按下未释放、坐标偏移。
- `group_dispatch`：分组缺设备、重复设备、单台失败影响全局。
- `business_state`：业务页面变化导致脚本目标不存在。

每个失败都要关联至少一个设备 ID、一个步骤、一个错误文本，最好再关联截图或模板路径。

如果能主动写分类，建议在 `details` 里加入：

```json
{
  "action": "record",
  "status": "fail",
  "category": "hid",
  "note": "dev_1 did not move after click",
  "details": {
    "error": "hardware not connected",
    "port": "COM3"
  },
  "artifacts": ["screenshots/dev_1_click_fail.png"]
}
```

如果没有显式分类，报告工具会根据 step、details 和 artifacts 里的关键词做 best-effort 归类。自动归类只能帮助复盘，不能替代现场人员判断。
