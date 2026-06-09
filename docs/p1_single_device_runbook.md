# P1 单设备实机首测 Runbook

更新时间：2026-06-08

目标：用一台 iPhone、一套 HID 硬件和一个投屏组件，证明最小闭环成立：能看到画面、能截图、能校准、能点击、能滑动、能输入、能记录 evidence。

这份 runbook 是现场操作手册。它不替代 `field_test_matrix.md`，而是把 P1 这一格拆成可逐步执行的动作。

## 通过定义

P1 通过必须同时满足：

- `doctor` 没有阻断实机链路的 fail；如果使用替代投屏组件，必须记录组件名称、版本、路径。
- GUI 能注册 `dev_1`、扫描到真实 HID 串口、绑定硬件。
- iPhone 能连接投屏接收端，截图不是黑屏，尺寸能记录。
- 五点校准完成，点击误差小于 8 像素。
- 点击、滑动、输入在 iPhone 上真实生效。
- `scripts/p1_single_device_control_probe.json` 能实跑，所有带占位符的人工 `record` 都已改成真实观察。
- 本轮有 `evidence/<run_id>.jsonl`、`evidence/<run_id>.md`、`evidence/<run_id>_doctor.md`。

不能只看 API 返回成功。只要没有人工观察记录，就不算 iPhone 实机通过。

## 物料

| 物料 | 要求 |
|---|---|
| Windows PC | Windows 10+，推荐 16GB 内存起步，多设备后再升到 32GB |
| iPhone | 已授权自有设备，记录型号和 iOS 版本 |
| HID 硬件 | CH9329、自研 HID 或 XP 专用硬件，记录固件版本 |
| 转接线 | Lightning/USB-C OTG 或对应连接方案 |
| USB Hub | 带独立供电，记录 Hub 口编号 |
| 投屏组件 | 当前原型 UxPlay，或明确记录的 Windows AirPlay Receiver/有线投屏组件 |
| 网络 | PC 优先有线，iPhone 和 PC 同 VLAN，关闭 AP 隔离 |

## 0. 设置本轮编号

建议 run_id：

```text
p1_dev1_YYYYMMDD
```

示例：

```text
p1_dev1_20260608
```

现场台账先填写：

```text
run_id:
git_revision:
PC:
Python:
投屏组件/版本/路径:
HID 硬件/固件:
Hub 口:
iPhone 型号:
iOS 版本:
AirPlay 名称:
串口:
```

## 0.5 路线决策记录

先生成本轮路线决策模板：

```powershell
.\.venv\Scripts\python -m imouse.route_decision init --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_route_decision.json
```

打开 `evidence\p1_dev1_YYYYMMDD_route_decision.json`，把 receiver、HID、iPhone、Hub、线材、截图计划、人工观察计划和是否允许 P1 实跑填成真实值。

填完后校验：

```powershell
.\.venv\Scripts\python -m imouse.route_decision validate evidence\p1_dev1_YYYYMMDD_route_decision.json --require-ready --markdown evidence\p1_dev1_YYYYMMDD_route_decision.md --record-evidence evidence\p1_dev1_YYYYMMDD.jsonl
```

通过标准：

- `receiver.route` 是 `uxplay`、`windows_receiver`、`wired` 或 `capture_card` 之一。
- `hid.route` 是 `ch9329`、`xp_hardware`、`self_built` 或 `bluetooth` 之一。
- 没有 `EDIT_ME`、`TODO`、`COM_EDIT_ME` 等占位值。
- `decision.allowed_to_run_p1` 为 `true`，且 `open_blockers` 为空。

失败处理：

- 路线决策校验失败时，不进入实机通过判断。
- 如果只是为了记录“暂不允许开测”的原因，可以保留 blocker，但不能把这轮当作 P1 pass。
- 如果失败结果已经通过 `--record-evidence` 写入 `evidence\p1_dev1_YYYYMMDD.jsonl`，这轮 run_id 应视为阻断复盘，不要修完后继续用同一个 run_id 宣称通过；改完路线后换新的 run_id 重跑。
- 路线决策写入 evidence 只证明组件台账完整，不证明 iPhone 已经响应；P1 仍必须有截图质量和人工观察。

## 1. 本地代码健康检查

```powershell
cd D:\codex-projects\imouse-clone
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python -m compileall -q imouse tests
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run
```

通过标准：

- 单元测试全绿。
- `compileall` 无输出并返回 0。
- `p1_single_device_control_probe.json --dry-run` 返回 `"ok": true`。

失败处理：

- Python 依赖失败：先停在 P0，不接硬件。
- dry-run 失败：先修 JSON 或 runner，不做实机。

## 2. Preflight Doctor

```powershell
.\.venv\Scripts\python -m imouse.doctor --route-decision evidence\p1_dev1_YYYYMMDD_route_decision.json --markdown evidence\p1_dev1_YYYYMMDD_doctor.md
```

如果本地服务已经启动，也跑一次带服务探测：

```powershell
.\.venv\Scripts\python -m imouse.doctor --server-url http://127.0.0.1:9911 --markdown evidence\p1_dev1_YYYYMMDD_doctor_server.md
```

通过标准：

- Python 和核心模块 OK。
- 能看到真实 HID 串口；只看到 `COM1` 通常不是目标硬件通过。
- 投屏组件可用。如果当前原型使用 UxPlay，则 `uxplay` 必须可找到；如果改用 Windows 原生接收器或其他组件，必须先在 route decision 里写清楚替代链路，让 doctor 预检 receiver provider，再在 evidence 里证明截图质量和人工观察。

当前本机已知状态：

- Python 依赖 OK。
- `uxplay` 缺失，会阻断当前 UxPlay/AirPlay 原型链路。
- 尚未看到真实 HID 硬件。

## 3. iPhone 基础设置

在 iPhone 上检查：

- 关闭或延长自动锁屏。
- 亮度固定，避免自动亮度影响找图/找色。
- 关闭会干扰画面的系统弹窗和自动更新提示。
- 确认鼠标/键盘接入后 iOS 能响应。
- 记录是否开启 `设置 > 辅助功能 > 触控 > 辅助触控`。
- 记录 `设置 > 通用 > 触控板与鼠标` 里的跟踪速度。
- 如果要横屏测试，先在台账里写明方向策略；P1 首测建议先固定竖屏。

iOS 鼠标控制的坑：

- 鼠标速度、辅助触控、指针显示和键盘焦点都会影响观测。
- 输入中文、Emoji、组合键不作为 P1 刚需，先验证英文、数字、符号。
- iOS 17+ 与 XP 4.4 固件相关的快准狠鼠标模式必须单独实测，不能由 CH9329 dry-run 推断。

## 4. 启动 GUI 和本地服务

```powershell
.\.venv\Scripts\python -m imouse.gui
```

GUI 操作：

1. 顶部 `Evidence` 填 `p1_dev1_YYYYMMDD`。
2. 保持 `Record` 勾选。
3. 点击 `Start Local`。
4. 点击 `Doctor`，确认生成 `evidence/p1_dev1_YYYYMMDD_doctor.md`。
5. 点击 `Ping`，确认服务可用。

失败处理：

- `Start Local` 失败：检查 9911 端口是否被占用。
- `Doctor` fail：先处理 fail，不继续做实机通过判断。

## 5. 注册设备

GUI 操作：

1. `Device ID` 输入 `dev_1`。
2. 点击 `Register`。
3. 点击 `Ping`。
4. 设备表应出现 `dev_1`，初始状态通常是 `offline`。

API 备用检查：

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/dev/list&msgid=1"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/device/register\",\"data\":{\"id\":\"dev_1\"}}"
```

通过标准：

- 返回中能看到 `dev_1`。
- evidence 里有注册或刷新记录。

## 6. 接入并绑定 HID

先不接 HID，点一次 `Scan`，记录串口列表。

接入 HID 后再点 `Scan`，记录新增串口。

命令行辅助：

```powershell
@'
from imouse.hardware import list_devices
for item in list_devices():
    print(item)
'@ | .\.venv\Scripts\python -
```

GUI 操作：

1. 选中 `dev_1`。
2. 选中真实 HID 串口，例如 `COM3`。
3. 点击 `Bind`。
4. 点击 `Ping`。

通过标准：

- 插拔前后串口列表有变化。
- 绑定日志无异常。
- iPhone 系统层能识别鼠标/键盘或至少能响应后续 HID 动作。

失败处理：

- 新串口不出现：换线、换 Hub 口、检查驱动和供电。
- 绑定成功但 iPhone 无响应：检查 OTG、固件、波特率、鼠标/键盘识别状态。
- XP 专用硬件若不是 CH9329 协议，当前原型可能无法控制，需要单独做硬件协议适配。

## 7. 投屏和截图

GUI 操作：

1. 选中 `dev_1`。
2. 点击 `Start AirPlay`。
3. 在 iPhone 控制中心选择对应 AirPlay 接收端。
4. 点击 `Start Capture`。
5. 点击 `Screenshot`。

通过标准：

- iPhone 能看到接收端并连接。
- GUI 右侧出现截图预览。
- 截图不是黑屏、不是空白、尺寸记录到台账。
- 如果投屏断开后重连，重连过程和耗时写入 evidence。

失败处理：

- 找不到接收端：查同网段、AP 隔离、Bonjour/mDNS、防火墙、服务名冲突。
- 黑屏/花屏：查编码格式、硬解、显卡驱动、投屏组件版本、锁屏状态。
- 当前机器缺 `uxplay`：不能验证当前 UxPlay 原型路线；可以先替换投屏组件，但必须记录替代链路，并承认代码截图集成仍需适配。

## 8. 坐标校准

GUI 操作：

1. 点击 `Screenshot`。
2. 在 `Coordinate Calibration` 点击 `Use Screenshot`。
3. 如有黑边/标题栏/裁剪，调整 `Active x/y/w/h`。
4. 如硬件坐标空间和截图不同，调整 `Target w/h`。
5. 勾选 `Enabled`。
6. 点击 `Save`。
7. 依次点击五个安全点：
   - 左上角附近。
   - 右下角附近。
   - 中心点。
   - 底部 Home Indicator 附近但不触发危险动作。
   - 灵动岛/刘海附近或顶部安全区。

每个点都在 GUI 底部 `Manual` 写一条：

```text
step: calibration point 1
status: pass/fail
note: expected=(x,y), observed=(x,y), error_px=?
artifact: screenshots/dev_1_calibration_p1.png
```

通过标准：

- 误差 < 8 像素。
- 连续 50 次点击无明显漂移。
- `state/calibration.json` 有 `dev_1` 配置。
- evidence 中能追到校准点和人工观察。

## 9. 点击、滑动、输入实测

GUI 先手工跑：

1. 在截图预览点一个安全区域，自动填入 `Click X/Y`。
2. 点击 `Click`，观察 iPhone。
3. 填写滑动起止点，点击 `Swipe`。
4. 把光标放到安全输入框，点击 `Type` 输入 `imouse-smoke`。
5. 每一步都用 `Manual` 记录真实观察。

命令行备用：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/mouse/click\",\"data\":{\"id\":\"dev_1\",\"x\":100,\"y\":100}}"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/mouse/swipe\",\"data\":{\"id\":\"dev_1\",\"x1\":300,\"y1\":900,\"x2\":300,\"y2\":500,\"steps\":20}}"
curl.exe -X POST http://127.0.0.1:9911/api -H "Content-Type: application/json" -d "{\"fun\":\"/keyboard/type\",\"data\":{\"id\":\"dev_1\",\"text\":\"imouse-smoke\"}}"
```

通过标准：

- 点击 10 个点，每点 10 次，不误点。
- 上下左右滑动方向正确。
- 输入英文、数字、符号成功。
- 无鼠标按下未释放。

## 10. 图色和 OCR

GUI 操作：

1. 在截图上拖拽一个有纹理的按钮区域，点击 `Save Crop`；如果模板质量失败，换更大、更有纹理的区域。
2. 点击 `Find`，确认能找回模板坐标。
3. 点击截图上一个颜色点，点击 `Find Color`。
4. 点击 `OCR`。
5. 输入页面上能看到的文字，点击 `Find Text`。

通过标准：

- 模板不是纯色块。
- 阈值、模板路径、命中坐标写入 evidence。
- 找色写明 RGB、容差和区域。
- OCR 首次模型下载、缓存目录和返回数量都有记录。

失败处理：

- 纯色模板误判：重截有纹理模板。
- OCR 启动失败：检查 `.cache/paddlex` 可写性和 PaddleOCR 版本。

## 11. 跑单设备脚本

先 dry-run：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --dry-run --run-id p1_dev1_YYYYMMDD
```

实跑前把 `scripts/p1_single_device_control_probe.json` 里的坐标改成本轮从 GUI 截图取到的安全点，并把所有 `EDIT_ME`、`COM_EDIT_ME` 和人工 `record` 观察改成真实值。

实跑：

```powershell
.\.venv\Scripts\python -m imouse.script_runner scripts\p1_single_device_control_probe.json --run-id p1_dev1_YYYYMMDD
```

通过标准：

- summary 中 `ok=true`。
- evidence 中每一步都有结果。
- 最后一条人工 `record` 是真实观察，不是默认占位文本。

## 12. 生成汇总并复盘

GUI 点击 `Summary`，或命令行由脚本自动生成：

```text
evidence/p1_dev1_YYYYMMDD.jsonl
evidence/p1_dev1_YYYYMMDD.md
evidence/p1_dev1_YYYYMMDD_doctor.md
```

复盘表：

| 项 | 结果 |
|---|---|
| Doctor | pass/fail |
| 串口扫描 | pass/fail |
| HID 绑定 | pass/fail |
| 投屏发现 | pass/fail |
| 截图 | pass/fail |
| 校准 | pass/fail |
| 点击 | pass/fail |
| 滑动 | pass/fail |
| 输入 | pass/fail |
| 找图 | pass/fail |
| 找色 | pass/fail |
| OCR | pass/fail |
| 脚本实跑 | pass/fail |
| 阻断问题 Top 3 | 1/2/3 |

P1 通过后，下一步才进入 P2 单机 30 分钟稳定性测试。
