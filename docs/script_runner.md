# JSON 脚本运行器

更新时间：2026-06-08

脚本运行器用于把“单设备闭环”和“群控回归”沉淀成可复用 JSON 场景。它不替代 GUI，作用是让同一套步骤可以在 1 台、4 台、10 台设备上重复执行，并自动写入 evidence。稳定性测试中可用 `metrics` 记录每轮 PC 资源和人工指标模板。

入口：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --run-id single_dev1_YYYYMMDD
```

P1 实机首测请结合 `docs/p1_single_device_runbook.md`。P1 通过后的 30 分钟单台、4 台试点和 10 台 2 小时稳定性流程请结合 `docs/p2_p3_stability_runbook.md`。脚本只能调 API 和写 evidence，不能替代真实 iPhone 人工观察。

每轮实跑前建议先生成执行包，把本轮脚本、GUI 步骤、组件台账和验收命令合在一份 Markdown：

```powershell
.\.venv\Scripts\python -m imouse.field_packet --stage p1 --run-id single_dev1_YYYYMMDD --devices dev_1 --output evidence\single_dev1_YYYYMMDD_field_packet.md
```

先做 dry-run：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\single_device_smoke.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_receiver_capture_probe.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p2_single_device_stability.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\pilot_4_group_smoke.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\p3_pilot4_30min_watchdog.json --dry-run
.\.venv\Scripts\python -m imouse.script_runner scripts\stable_10_group_watchdog.json --dry-run
```

也可以在 GUI 里运行：

1. 启动 `python -m imouse.gui`。
2. 顶部填写本轮 `Evidence run_id`，保持 `Record` 勾选。
3. 底部 `Scenario` 选择场景 JSON。
4. 先保持 `Dry Run` 勾选点击 `Run`，确认场景结构无误。
5. 实机准备完成后取消 `Dry Run` 再运行。

GUI 与命令行使用同一套 evidence 文件，输出路径仍是 `evidence/<run_id>.jsonl` 和 `evidence/<run_id>.md`。

仓库已提供七个可加载、可 dry-run 的样例：

- `scripts/p1_single_device_control_probe.json`：P1 默认单台控制探针，强制记录组件台账、10 次截图质量、点击、滑动、输入和最终人工结论。
- `scripts/single_device_smoke.json`：轻量单台 smoke 样例，适合调 runner，不作为 P1 默认验收脚本。
- `scripts/p1_receiver_capture_probe.json`：P1 投屏/截图专项采集探针，强制记录 receiver 元数据、10 次截图质量和人工观察。
- `scripts/p2_single_device_stability.json`：P2 单设备 30 分钟稳定性模板，6 轮、每轮间隔 5 分钟。
- `scripts/pilot_4_group_smoke.json`：4 台设备分组保存和批量点击/滑动/输入。
- `scripts/p3_pilot4_30min_watchdog.json`：P3 4 台 30 分钟 watchdog 模板，6 轮、每轮间隔 5 分钟。
- `scripts/stable_10_group_watchdog.json`：10 台稳定性巡检的一轮动作模板，建议 2 小时测试中每 30 分钟跑一轮。

实机运行前必须把坐标、设备 ID、模板、receiver/provider 信息和人工 `record` 备注改成本轮现场真实值。dry-run 只证明 JSON 结构和 runner 调度可用。

## 场景格式

```json
{
  "name": "single device smoke",
  "run_id": "single_dev1_20260608",
  "stop_on_error": true,
  "steps": [
    {"action": "call", "fun": "/device/list"},
    {"action": "screenshot", "device_id": "dev_1"},
    {
      "action": "find_image_then_click",
      "name": "click settings",
      "device_id": "dev_1",
      "template_path": "templates/settings_button.png",
      "threshold": 0.86,
      "region": [80, 360, 420, 180]
    },
    {"action": "wait", "seconds": 1},
    {
      "action": "record",
      "name": "manual observation",
      "status": "pass",
      "note": "dev_1 actually opened Settings"
    }
  ]
}
```

运行后会生成：

```text
evidence/<run_id>.jsonl
evidence/<run_id>.md
```

## 支持动作

| action | 说明 |
|---|---|
| `call` | 直接调用 XP 风格 `fun`，用于还没封装 helper 的接口 |
| `wait` | 等待指定秒数 |
| `repeat` | 重复执行一组子步骤，可设置轮数和轮间等待 |
| `metrics` / `system_metrics` | 记录主机平台、Python、CPU 核数、内存、磁盘和现场人工指标模板 |
| `record` | 写入人工观察或备注 |
| `click` | 单设备点击 |
| `swipe` | 单设备滑动 |
| `type` | 单设备输入 |
| `group_click` | 按分组批量点击 |
| `group_swipe` | 按分组批量滑动 |
| `group_type` | 按分组批量输入 |
| `screenshot` | 单设备截图；实跑时会自动保存图片 artifact |
| `find_image` | 找图 |
| `find_image_then_click` | 找图成功后点击命中坐标 |
| `find_color` | 找色 |
| `find_colors` | 多点找色，按锚点和相对偏移颜色匹配 |
| `ocr` | OCR |
| `find_text` | 查找文字 |

## 人工记录校验

`record` 可以开启现场元数据校验，避免把未修改的模板占位符写成 pass。这个校验只在实跑时执行；dry-run 仍用于检查 JSON 结构和步骤展开。

```json
{
  "action": "record",
  "name": "receiver metadata",
  "status": "pass",
  "required_details": ["receiver_provider", "receiver_name", "ios_version"],
  "forbid_placeholder_values": ["EDIT_ME", "uxplay_or_windows_receiver_or_wired_capture"],
  "details": {
    "receiver_provider": "uxplay",
    "receiver_name": "imouse-dev-01",
    "ios_version": "17.7"
  }
}
```

字段说明：

- `required_details`：要求 `details` 中必须存在且非空的字段；支持 `receiver.version` 这类一层或多层点路径。
- `forbid_placeholder_values`：禁止出现在 `details` 任意字符串值里的占位文本；实跑时如果命中会让步骤失败。
- `forbid_placeholder_values: true` 会使用默认占位值：`EDIT_ME`、`TODO`、`TBD`。

## 重复轮次

`repeat` 用于把 30 分钟、2 小时巡检沉淀成脚本。它会把子步骤逐条写入 evidence，索引形如 `2.1.3`，表示第 2 个顶层步骤、第 1 轮、第 3 个子步骤。

```json
{
  "action": "repeat",
  "name": "six five-minute rounds",
  "count": 6,
  "wait_between": 300,
  "stop_on_error": false,
  "steps": [
    {"action": "screenshot", "device_id": "dev_1"},
    {"action": "click", "device_id": "dev_1", "x": 100, "y": 100},
    {
      "action": "record",
      "name": "manual round observation",
      "status": "info",
      "note": "replace with real round observation"
    }
  ]
}
```

字段说明：

- `count` 或 `rounds`：重复轮数，必须大于等于 1。
- `wait_between`、`wait_between_seconds` 或 `interval_seconds`：轮间等待秒数。
- `stop_on_error`：子步骤失败时是否提前停止，默认 `true`。
- dry-run 会校验并展开子步骤，但不会执行轮间等待。

## 系统指标

`metrics` 用于 P2/P3 稳定性测试。它不依赖新包；如果现场机器装了 `psutil`，会额外记录内存百分比和进程 RSS；没有 `psutil` 时会用标准库和系统接口记录可用信息。

```json
{
  "action": "metrics",
  "name": "round system metrics",
  "label": "p2_dev1_round",
  "extra": {
    "device_count": 1,
    "expected_online_count": 1,
    "manual_fields": ["online_count", "airplay_disconnects", "hid_failures"]
  }
}
```

通过标准：

- evidence 中能看到 `platform`、`python`、`cpu`、`memory`、`disk`。
- `extra.manual_fields` 提醒现场人员把在线数、投屏断线、HID 失败等人工指标补进同轮 `record`。
- 指标只能帮助定位瓶颈，不能证明 iPhone 已响应；仍要配合人工 observation。

## 单设备闭环样例

```json
{
  "name": "single device visual click",
  "run_id": "single_dev1_20260608",
  "stop_on_error": true,
  "steps": [
    {"action": "screenshot", "device_id": "dev_1"},
    {
      "action": "find_image_then_click",
      "device_id": "dev_1",
      "template_path": "templates/dev_1_template.png",
      "threshold": 0.85,
      "region": [0, 300, 1170, 600]
    },
    {"action": "wait", "seconds": 1},
    {
      "action": "record",
      "name": "manual click observation",
      "status": "pass",
      "note": "iPhone UI changed after click"
    }
  ]
}
```

通过标准：

- `find_image_then_click` 找到目标并返回点击结果。
- evidence 中有 API 结果，也有人工观察 `record`。
- 如果模板找不到，脚本返回失败并停止，失败信息写入 evidence。
- `find_image` / `find_image_then_click` 支持 `region: [x, y, w, h]`，坐标基于原始截图；命中结果仍返回全屏坐标，适合把查找限制在导航栏、弹窗或固定按钮区域，减少误判和加速匹配。
- `find_image` 和 `find_image_then_click` 如果模板文件在本地存在，会先做模板质量校验；过小或低纹理模板会提前失败，避免纯色模板误判。
- `screenshot` 步骤在实跑时会把截图保存到 `evidence/<run_id>_artifacts/*_capture.png`，并把 `base64` 压缩成文件引用，避免 evidence JSONL 过大。
- `screenshot` 默认会做轻量画质校验：缺失 base64、无效图片、尺寸过小、黑屏、白屏或低纹理空白图都会让该步骤失败，并在 `details.screenshot_quality` 中记录原因。

多点找色示例：

```json
{
  "action": "find_colors",
  "device_id": "dev_1",
  "points": [
    {"dx": 0, "dy": 0, "color": [255, 80, 80]},
    {"dx": 12, "dy": 0, "color": [255, 255, 255]},
    {"dx": 0, "dy": 8, "color": [180, 20, 20]}
  ],
  "tolerance": 8,
  "region": [0, 300, 1170, 600]
}
```

`points` 的 `color` 使用 RGB；底层会转换为 OpenCV BGR。返回的 `x/y` 是锚点全屏坐标，`points` 会记录每个相对点的全屏坐标。

## 4 台分组样例

```json
{
  "name": "pilot 4 batch input",
  "run_id": "pilot_4_20260608",
  "stop_on_error": false,
  "steps": [
    {
      "action": "call",
      "name": "save pilot group",
      "fun": "/group/save",
      "data": {"name": "pilot_4", "ids": ["dev_1", "dev_2", "dev_3", "dev_4"]}
    },
    {"action": "group_click", "group": "pilot_4", "x": 100, "y": 100},
    {"action": "group_swipe", "group": "pilot_4", "x1": 300, "y1": 900, "x2": 300, "y2": 300},
    {"action": "group_type", "group": "pilot_4", "text": "hello"},
    {
      "action": "record",
      "name": "manual group observation",
      "status": "pass",
      "note": "all four devices responded"
    }
  ]
}
```

通过标准：

- 分组保存成功。
- 批量动作返回每台设备的结果。
- 任一单台失败时，返回中能看到失败设备 ID 和错误文本。
- 人工观察结果写入 `record`，不能只看 API 返回。

## 失败处理

- `stop_on_error=true`：遇到失败立即停止，适合单设备闭环。
- `stop_on_error=false`：继续执行后续步骤，适合群控压测。
- 每个失败会写入 evidence；带 `artifacts` 的步骤会把截图/模板/日志路径写入汇总。
- 非 dry-run 实跑时，成功的 `screenshot` 步骤会自动保存到 `evidence/<run_id>_artifacts/*_capture.png`，用于证明当时画面确实可采集。
- 非 dry-run 实跑时，失败步骤如果能确定单个 `device_id`，脚本运行器会尽力调用截图接口并保存到 `evidence/<run_id>_artifacts/*_failure.png`，同时把路径写入 artifacts。
- 如果自动截图失败，原始失败仍会保留，`details.failure_screenshot_error` 会记录截图失败原因。
- 对分组或自定义 `call` 步骤，可用 `failure_screenshot_device_id` 指定失败时抓哪台设备。
- 如果某个步骤不适合自动截图，可设置 `"failure_screenshot": false`。
- 如果某个截图步骤不适合画质校验，可设置 `"validate_screenshot": false`；也可用 `screenshot_min_width`、`screenshot_min_height`、`screenshot_min_stddev`、`black_luma`、`white_luma` 微调阈值。
- 如果某个本地模板确实需要跳过质量校验，可设置 `"validate_template": false`；也可用 `template_min_width`、`template_min_height`、`template_min_stddev` 微调阈值。

失败步骤示例：

```json
{
  "action": "record",
  "name": "manual failure",
  "status": "fail",
  "category": "hid",
  "note": "dev_2 did not move after group_swipe",
  "details": {"port": "COM3", "failure_count": 1},
  "artifacts": ["screenshots/dev_2_swipe_fail.png"]
}
```

分组失败时指定截图设备：

```json
{
  "action": "group_click",
  "name": "group click with failure capture",
  "group": "pilot_4",
  "x": 100,
  "y": 100,
  "failure_screenshot_device_id": "dev_2"
}
```

`record` 会把 `note`、`category`、`failure_category`、`error_type`、`observation` 和 `details` 写入 evidence。建议实机失败都显式写 `category`，这样 `imouse.evidence_report` 不需要只靠关键词猜测。

## 当前限制

- 脚本运行器只调用现有 XP API，不会自动启动 GUI。
- GUI 入口只是调用同一个脚本运行器，不会改变场景语义。
- 它不能自动判断 iPhone 是否真的响应，所以实机脚本必须包含 `record` 步骤或 GUI 人工观察记录。
- 已支持 `repeat` 重复轮次、`metrics` 系统指标、截图步骤自动落盘、基础截图画质校验、本地模板质量校验和失败截图尽力采集；但还没有变量、条件分支、模板资产库、重复帧检测和业务状态校验。
- 真实投屏、HID、OCR 仍依赖实机环境；离线测试只证明调度和记录逻辑可用。
