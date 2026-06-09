# iMouse XP 风格 API 兼容层

更新时间：2026-06-08

本仓库现在同时保留两类接口：

- 原型 REST 接口：例如 `/api/devices`、`/api/click`、`/api/find_image`。
- XP 风格统一入口：`GET /api`、`POST /api`、WebSocket `/api` 发送 `fun` JSON；`/ws` 保留为 legacy/debug alias。

后续 GUI、SDK 和脚本优先使用 XP 风格入口，REST 接口只作为内部调试或兼容保留。

## 响应格式

XP 风格入口统一返回：

```json
{
  "status": 200,
  "message": "成功",
  "data": {
    "code": 0,
    "message": "成功"
  },
  "msgid": 0,
  "fun": "/device/list"
}
```

错误示例：

```json
{
  "status": 404,
  "message": "Unsupported XP fun: /not/supported",
  "data": {
    "code": 404,
    "message": "Unsupported XP fun: /not/supported"
  },
  "msgid": 0,
  "fun": "/not/supported"
}
```

## 请求形态

### GET

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/dev/list&msgid=1"
```

### POST JSON

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/device/register\",\"msgid\":2,\"data\":{\"id\":\"dev_1\"}}"
```

也支持把字段放在顶层：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/device/register\",\"id\":\"dev_1\"}"
```

### WebSocket

连接：

```text
ws://127.0.0.1:9911/ws
```

XP-compatible WebSocket path:

```text
ws://127.0.0.1:9911/api
```

`/ws` is kept as a legacy/debug alias. New XP-facing clients should prefer WebSocket `/api` so HTTP and WebSocket share the same visible endpoint.

Callback push messages use this shape:

```json
{
  "event": "callback",
  "callback": {
    "seq": 1,
    "event": "device_registered",
    "type": "device_registered",
    "device_id": "dev_1",
    "source": "api",
    "severity": "info",
    "data": {"state": "offline"}
  }
}
```

Callback fun supported in this prototype:

| fun | Purpose |
|---|---|
| `/callback/list` | Return recent callback events after `after_seq`, with `limit`. |
| `/callback/poll` | Poll callback events; same response shape as list. |
| `/callback/push` | Append a manual/synthetic callback event for offline integration tests. |
| `/callback/clear` | Clear in-memory callback events for tests and fresh offline runs. |
| `/event/list` | Alias for `/callback/list`. |
| `/event/poll` | Alias for `/callback/poll`. |
| `/event/push` | Alias for `/callback/push`. |

Callback boundary: events are in-memory only, real receiver/HID/device events still need field integration, and callback events do not prove real iOS control.

GUI note: the top `Callback` button reads `/callback/list` and exports `evidence/<run_id>_callback_monitor.md` for field debugging. The top `Attach Log` button parses receiver/HID text logs, pushes classified rows through `/callback/push`, exports `evidence/<run_id>_callback_log.md`, and writes `Attach Log triage` JSONL when `Record` is enabled. Log triage supports failure classification; it does not prove real iOS control.

GUI event/error contract: the Live Probe `Events` button exports `evidence/<run_id>_<stage>_xp_event_error_contract.md`. It audits the XP response envelope, `/api` transport shape, `msgid`, callback lifecycle, `/event/*` aliases, Attach Log ingestion, receiver/capture/HID error taxonomy, and claim boundaries. It is a compatibility/SOP audit only; real iOS control still requires JSONL evidence, screenshot quality, Manual observation, Acceptance, and Readiness.

发送：

```json
{"fun":"/dev/list","msgid":3}
```

返回格式与 HTTP XP 入口一致。

## 字段兼容规则

- XP 文档常用 `id` 表示设备 ID。
- 当前内部模型使用 `device_id`。
- 兼容层会自动把 `id` 映射为 `device_id`。
- `msgid` 会原样返回，便于客户端匹配异步请求。
- GET 查询参数里的逗号列表会被解析为数组，例如 `color=255,0,0`。

## 已支持 fun

### 设备与硬件

| fun | 说明 |
|---|---|
| `/device/list` | 设备列表 |
| `/dev/list` | `/device/list` 别名 |
| `/devices` | `/device/list` 别名 |
| `/device/register` | 注册设备 |
| `/device/remove` | 移除设备 |
| `/hardware/scan` | 扫描串口硬件 |
| `/usb/list` | `/hardware/scan` 别名 |
| `/usb/scan` | `/hardware/scan` 别名 |
| `/device/bind` | 绑定硬件端口 |
| `/usb/bind` | `/device/bind` 别名 |
| `/device/unbind` | 解绑硬件 |

### 投屏与采集

| fun | 说明 |
|---|---|
| `/airplay/connect` | 启动 AirPlay 投屏接收 |
| `/airplay/start` | `/airplay/connect` 别名 |
| `/airplay/disconnect` | 停止 AirPlay |
| `/airplay/stop` | `/airplay/disconnect` 别名 |
| `/capture/start` | 启动截图采集 |

### 鼠标键盘

| fun | 说明 |
|---|---|
| `/mouse/click` | 点击坐标 |
| `/mouse/swipe` | 滑动 |
| `/keyboard/type` | 输入文本 |
| `/key/type` | `/keyboard/type` 别名 |
| `/keyboard/key` | 单键 |
| `/key/tap` | `/keyboard/key` 别名 |
| `/keyboard/combo` | 组合键 |
| `/key/combo` | `/keyboard/combo` 别名 |

### 批量控制

| fun | 说明 |
|---|---|
| `/batch/click` | 对多个设备点击同一坐标 |
| `/mouse/batch-click` | `/batch/click` 别名 |
| `/batch/swipe` | 对多个设备执行同一滑动 |
| `/mouse/batch-swipe` | `/batch/swipe` 别名 |
| `/batch/type` | 对多个设备输入同一文本 |
| `/batch/text` | `/batch/type` 别名 |
| `/keyboard/batch-type` | `/batch/type` 别名 |
| `/key/batch-type` | `/batch/type` 别名 |

批量接口支持两种选设备方式：

- 显式传 `ids` / `device_ids`。
- 传 `group` / `group_name`，由本地分组表展开为设备列表。

### 设备分组

| fun | 说明 |
|---|---|
| `/group/list` | 获取本地分组列表 |
| `/groups` | `/group/list` 别名 |
| `/group/save` | 保存或覆盖一个分组 |
| `/group/set` | `/group/save` 别名 |
| `/group/remove` | 删除一个分组 |
| `/group/delete` | `/group/remove` 别名 |

分组默认持久化到 `state/groups.json`。测试环境会关闭持久化，避免污染本地状态。

### 坐标校准

| fun | 说明 |
|---|---|
| `/calibration/list` | 列出所有本地校准 |
| `/calibration/get` | 获取设备校准 |
| `/device/calibration` | `/calibration/get` 别名 |
| `/calibration/set` | 保存设备校准 |
| `/calibration/save` | `/calibration/set` 别名 |

校准默认持久化到 `state/calibration.json`。校准用于把截图坐标映射到 HID 控制坐标，解决黑边、裁剪、横竖屏和分辨率不一致导致的点偏。

### 设备组件档案

| fun | 说明 |
|---|---|
| `/profile/list` | 列出所有设备组件档案 |
| `/profile/get` | 获取单台设备组件档案 |
| `/device/profile` | `/profile/get` 别名 |
| `/device/profile/get` | `/profile/get` 别名 |
| `/profile/set` | 保存单台设备组件档案 |
| `/device/profile/set` | `/profile/set` 别名 |
| `/metadata/list` | `/profile/list` 别名 |
| `/metadata/get` | `/profile/get` 别名 |
| `/metadata/set` | `/profile/set` 别名 |

组件档案默认持久化到 `state/device_profiles.json`，用于把每台设备绑定到具体 receiver/capture/HID/iPhone/iOS 组合。P1/P2/P3/P4 acceptance 仍以 evidence JSONL 为验收依据；档案是现场台账和 GUI 自动填充来源，不等于实机控制已通过。

### ImConfig / User / Shortcut runtime compatibility

These fun names are local compatibility scaffolding for the public XP Python helper domains `ImConfig`, `User`, and `Shortcut`.
They persist local runtime state to `state/xp_runtime.json` and push callback ledger events, but they do not prove XP cloud account behavior, permissions, licensing, or real shortcut execution.

| fun | Description |
|---|---|
| `/config/list` | Return all local XP runtime config values. |
| `/config/get` | Return all config, or one value when `key` / `name` is provided. |
| `/config/set` | Merge `config` / `imconfig` / `key=value` fields into local config. |
| `/imconfig/list` | `/config/list` alias. |
| `/imconfig/get` | `/config/get` alias. |
| `/imconfig/set` | `/config/set` alias. |
| `/imconfig/save` | `/config/set` alias. |
| `/im/config/list` | `/config/list` alias. |
| `/im/config/get` | `/config/get` alias. |
| `/im/config/set` | `/config/set` alias. |
| `/user/list` | Return local users and `active_user`. |
| `/user/get` | Return a local user by `id` / `user_id` / `name`. |
| `/user/current` | Return the active local user. |
| `/user/set` | Save a local user. |
| `/user/save` | `/user/set` alias. |
| `/user/switch` | Switch active user; missing users are auto-created as local placeholders. |
| `/user/login` | `/user/switch` alias. |
| `/user/remove` | Remove a local user. |
| `/user/delete` | `/user/remove` alias. |
| `/shortcut/list` | Return local shortcut registry. |
| `/shortcut/get` | Return one shortcut by `name` / `shortcut` / `id`. |
| `/shortcut/save` | Save a local shortcut definition. |
| `/shortcut/set` | `/shortcut/save` alias. |
| `/shortcut/remove` | Remove one local shortcut. |
| `/shortcut/delete` | `/shortcut/remove` alias. |
| `/shortcut/run` | Record a dry-run shortcut callback; does not execute real device behavior. |
| `/shortcut/call` | `/shortcut/run` alias. |
| `/shortcut/brightness` | Store local brightness value and record a dry-run callback. |
| `/shortcut/switch/bril` | `/shortcut/brightness` alias seen in XP-style shortcut naming. |

Write operations emit callback events such as `config_saved`, `user_saved`, `user_switched`, `shortcut_saved`, `shortcut_run`, and `shortcut_brightness`.

### GUI API Coverage Board

The Live Probe `API Cov` button exports `evidence/<run_id>_<stage>_xp_api_coverage.md`.
It maps XP-style fun/helper domains to local API coverage, local tests, runtime gates, required field evidence and claim boundaries.

This board is P0 compatibility/SOP material only. Local API tests do not prove receiver capture, HID response, real iPhone click/swipe/text behavior, XP dedicated hardware parity, XP cloud accounts, licensing or subaccount behavior.

### 图色 OCR

| fun | 说明 |
|---|---|
| `/pic/screenshot` | 截图，支持 base64、binary、jpg、rect、save_path |
| `/pic/screen` | `/pic/screenshot` 别名 |
| `/pic/capture` | `/pic/screenshot` 别名 |
| `/pic/find-image` | OpenCV 模板找图 |
| `/pic/find_image` | `/pic/find-image` 别名 |
| `/pic/find_color` | 找色 |
| `/pic/find-color` | `/pic/find_color` 别名 |
| `/pic/find_colors` | 多点找色 |
| `/pic/find-colors` | `/pic/find_colors` 别名 |
| `/pic/find_multi_color` | `/pic/find_colors` 别名 |
| `/pic/ocr` | OCR，返回 XP 风格 `list` 和内部 `texts` |
| `/pic/find-text` | 查找文字 |
| `/pic/find_text` | `/pic/find-text` 别名 |
| `/pic/findtext` | `/pic/find-text` 别名 |

`/pic/find-image` 和 `/pic/find_image` 支持可选 `region: [x, y, w, h]`，坐标基于原始截图。服务端只在该区域内做模板匹配，但返回的 `x/y` 仍是全屏坐标，便于后续直接传给点击接口。

`/pic/find_colors` 使用锚点 + 相对偏移点匹配 UI 小结构。请求里的 `points[].color` 使用 RGB，`dx/dy` 是相对锚点偏移；返回的 `x/y` 是全屏锚点坐标。

### Screenshot compatibility

`/pic/screenshot` accepts GET, POST JSON, and multipart/form-data fields. Supported XP-style fields:

- `id` / `device_id`: target device.
- `binary=true`: return raw image bytes instead of an XP JSON wrapper.
- Python client note: use `XpApiClient.screenshot()` for JSON/base64 or `save_path` metadata, and `XpApiClient.screenshot_bytes()` for raw image downloads. `screenshot(binary=True)` delegates to the raw bytes path for XP-field compatibility.
- `jpg=true` or `format=jpg`: encode JPEG; otherwise PNG.
- `rect: [x1, y1, x2, y2]`: crop using XP corner coordinates.
- `region: [x, y, w, h]`: crop using the local rectangle shape.
- `save_path`: save the encoded image under the workspace and return `image`/`save_path` as the resolved path.

Without `save_path`, JSON responses include both `base64` and `image` as the encoded image string. With `save_path`, JSON responses omit `base64` and set `image` to the saved file path. Binary responses include `X-iMouse-Fun`, `X-iMouse-Msgid`, and `X-iMouse-Device` headers for field debugging.

## 示例

### 注册设备

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/device/register\",\"data\":{\"id\":\"dev_1\"}}"
```

### 扫描硬件

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/usb/scan"
```

### 绑定硬件

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/device/bind\",\"data\":{\"id\":\"dev_1\",\"port\":\"COM3\",\"baudrate\":9600}}"
```

### 点击

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/mouse/click\",\"data\":{\"id\":\"dev_1\",\"x\":100,\"y\":100}}"
```

### 批量点击

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/batch/click\",\"data\":{\"ids\":[\"dev_1\",\"dev_2\"],\"x\":100,\"y\":100}}"
```

### 保存分组并按分组点击

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/group/save\",\"data\":{\"name\":\"test_group\",\"ids\":[\"dev_1\",\"dev_2\"]}}"

curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/batch/click\",\"data\":{\"group\":\"test_group\",\"x\":100,\"y\":100}}"
```

### 保存坐标校准

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/calibration/set\",\"data\":{\"id\":\"dev_1\",\"calibration\":{\"enabled\":true,\"source_width\":1170,\"source_height\":2532,\"active_width\":1170,\"active_height\":2532,\"target_width\":1170,\"target_height\":2532,\"orientation\":\"portrait\"}}}"
```

### 保存组件档案

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/metadata/set\",\"data\":{\"id\":\"dev_1\",\"metadata\":{\"receiver_provider\":\"uxplay\",\"capture_method\":\"window\",\"hid_provider\":\"ch9329\",\"hid_id\":\"hid01\",\"serial_port\":\"COM3\",\"iphone_id\":\"iphone01\",\"ios_version\":\"17.7\",\"receiver_name\":\"imouse-dev-01\"}}}"
```

### 区域找图

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/pic/find-image\",\"data\":{\"id\":\"dev_1\",\"template_path\":\"templates/buy_button.png\",\"threshold\":0.85,\"region\":[0,300,1170,600]}}"
```

### 多点找色

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/pic/find_colors\",\"data\":{\"id\":\"dev_1\",\"points\":[{\"dx\":0,\"dy\":0,\"color\":[255,80,80]},{\"dx\":12,\"dy\":0,\"color\":[255,255,255]}],\"tolerance\":8,\"region\":[0,300,1170,600]}}"
```

批量接口不会因为单台失败就中断，会返回每台设备的执行结果：

```json
{
  "ok": false,
  "count": 2,
  "success_count": 0,
  "failure_count": 2,
  "results": [
    {"id": "dev_1", "device_id": "dev_1", "ok": false, "error": "hardware not connected"},
    {"id": "dev_2", "device_id": "dev_2", "ok": false, "error": "hardware not connected"}
  ]
}
```

### OCR

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/pic/ocr\",\"data\":{\"id\":\"dev_1\"}}"
```

OCR 返回中：

- `list` 是 XP 风格字段：`text`、`centre`、`rect`、`similarity`。
- `texts` 是内部归一化字段：`text`、`confidence`、`bbox`。

## 当前限制

- 该兼容层只是协议适配，不代表 XP 专用硬件、4.4 固件、有线投屏、1 秒投屏、H264/H265 硬解已经实现。
- `/pic/*` 需要设备已经成功投屏并启动采集。
- `/mouse/*` 和 `/keyboard/*` 需要硬件已绑定且真实可用。
- `/group/*` 当前是本地分组，不等同于 XP 官方的云端分组、子账号和局域网可见范围规则。
- `/calibration/*` 当前是本地校准，不等同于 XP 官方固件的自动绑定和自动分辨率适配；仍需实机点位验证。
- GET、POST JSON、multipart/form-data、WebSocket 均有本地自动化覆盖；`/pic/screenshot` 另覆盖 `binary=true`、`jpg=true`、`rect`、`region` 和 `save_path`。
- `rect` 的坐标语义后续需要按 XP 文档进一步细化，目前多数接口仍沿用内部实现。

## 离线测试

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

当前覆盖：

- GET `/api?fun=/dev/list`。
- POST JSON 注册设备。
- 顶层 `id` 字段兼容。
- 未支持 fun 的 XP 错误格式。
- WebSocket 发送 `fun`。
- 批量点击的逐设备错误汇总。
- 分组保存、列表、删除。
- 批量接口按 `group` 名称展开设备。
- 未知分组返回 404，而不是服务端 500。
- 校准保存、读取、列表。
- 组件档案保存、读取、列表，并在设备列表中返回 `component_metadata`。
- 客户端批量 helper 的 payload 构造。
- 客户端分组 helper 和按分组批量 helper 的 payload 构造。
- 客户端校准 helper 的 payload 构造。
- 客户端组件档案 helper 的 payload 构造。
