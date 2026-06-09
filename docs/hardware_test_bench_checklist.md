# iOS 群控硬件采购与测试台 Checklist

更新时间：2026-06-08

目标：在研发早期就把硬件、投屏、网络、线材和现场编号标准化，避免后面出现“代码看起来没问题，但现场随机掉线、点偏、无法复现”的典型群控坑。

本 checklist 服务于 iMouse XP 版对标。XP 公开资料显示，其路线是 Windows 内核服务 + 控制台 + HTTP/WebSocket API + 专用硬件 + 投屏/截图 + 鼠标键盘/图色/OCR 能力。我们前期 Python GUI 可以先验证链路，但真正能否交付取决于这份清单里的现场变量是否被控制住。

GUI 对应入口：先在 Live Probe 点击 `Kit Gate`，确认采购/SOP 文档、Route、Doctor、HID 扫描、证据计划和 Open P1 stop line 没有 fail/pending；再点击 `Bench` 执行实际 receiver/HID/iPhone/Hub/Cable 台架检查。`Kit Gate` 和 `Bench` 都不是 evidence，真实通过仍以 JSONL、Acceptance、Readiness 和人工真机观察为准。

## 1. 主流路线判断

| 路线 | 适用阶段 | 优点 | 主要风险 | 当前建议 |
|---|---|---|---|---|
| XP 专用硬件/固件 | 对标目标 | 最接近 iMouse XP 真实体验，可能支持自动绑定和优化鼠标模式 | 协议不公开、采购和授权受限、固件强依赖 | 作为最终对标路线，尽早采购一套做协议和体验比对 |
| CH9329/通用 HID | P1/P2 原型 | 成本低，能验证 iOS 指针/HID 控制闭环 | 坐标、滑动、释放、中文输入和多设备稳定性要自研打磨 | 当前 Python 原型优先用它证明最小闭环 |
| 蓝牙 HID | 概念验证 | 接线少 | 配对、断连、延迟、批量管理难 | 不建议作为群控主线 |
| 无障碍/设备端 App | 非 XP 对标 | 能做更高层 API | iPhone 端需要安装或授权，不符合免越狱零安装目标 | 本项目不作为主线 |

关键判断：

- iPhone 端不装 App、免越狱时，控制通常依赖系统已有能力：屏幕镜像/采集 + 外接指针/键盘/HID。
- Apple 官方支持通过 Lightning/USB-C 或蓝牙连接指针设备，并通过 AssistiveTouch 和指针设置控制行为；这说明路线有系统能力基础，但不等于群控产品已经稳定。
- CH9329 这类芯片可作为串口转标准 USB HID 键盘/鼠标设备，用于原型验证；是否达到 XP 的快准狠鼠标模式和自动绑定体验，需要实机证据。

## 2. 首批采购清单

P1/P2 最小采购：

| 物料 | 数量 | 要求 | 验收方法 |
|---|---:|---|---|
| iPhone | 1-2 | 覆盖一个当前主力 iOS 版本和一个旧机型 | 记录型号、iOS、屏幕分辨率、接口类型 |
| CH9329 HID 模块或等价硬件 | 2 | 有文档、可串口控制、可模拟鼠标键盘 | 插拔前后串口变化，iPhone 有指针/点击响应 |
| XP 专用硬件 | 1 套 | 如能采购，记录固件版本和授权方式 | 与 CH9329 同场景对比点击/滑动/输入 |
| Lightning/USB-C 转接 | 每机 2 | 优先官方或稳定品牌，带供电更好 | 连续 30 分钟不掉线 |
| USB Hub | 1 | 独立供电，端口稳定，最好 10 口以上 | 逐口编号，插拔不影响其他口 |
| USB 数据线 | 每机 2 | 数据/供电分清，贴编号 | 换线复现掉线问题 |
| 投屏接收组件 | 1-2 | UxPlay、Windows Receiver 或有线投屏方案 | 截图非黑屏，断线可恢复 |
| 有线网络 | 1 | PC 优先有线，同 VLAN | AirPlay 发现稳定 |

P3/P4 扩容采购：

- 4 台试点：每台 iPhone 独立 HID、线材、Hub 口、AirPlay 名称。
- 10 台稳定：至少两套 Hub 或分组供电，避免单点供电瓶颈。
- 20+ 压力：需要单独评估投屏服务、硬解、窗口采集、多进程和网络拓扑。

## 3. 编号规则

每个物料必须贴编号：

```text
iPhone: ip01, ip02
Device ID: dev_1, dev_2
HID: hid01, hid02
Hub: hub-a
Hub Port: hub-a-01, hub-a-02
Cable: cable-usbc-01
AirPlay: imouse-dev-01
Serial Port: COM3
Calibration: state/calibration.json:dev_1
```

现场台账示例：

| device_id | iPhone | iOS | HID | 固件 | Hub 口 | 线材 | AirPlay | 串口 | 校准 |
|---|---|---|---|---|---|---|---|---|---|
| dev_1 | ip01/iPhone 13 | 17.7 | hid01 | ch9329-v? | hub-a-01 | cable-01 | imouse-dev-01 | COM3 | yes |
| dev_2 | ip02/iPhone 15 | 18.x | hid02 | xp-4.4? | hub-a-02 | cable-02 | imouse-dev-02 | COM4 | yes |

没有编号的失败不进入研发排期，因为无法复现。

## 4. 测试台搭建 SOP

1. PC 固定到有线网络。
2. 关闭或记录 Windows 防火墙/安全软件对投屏接收器的影响。
3. Hub 接独立供电，端口贴编号。
4. 每台 iPhone 固定支架位置，避免人工触碰造成误判。
5. 每台 iPhone 设置：
   - 关闭或延长自动锁屏。
   - 固定亮度。
   - 关闭会遮挡业务页面的系统弹窗。
   - 确认 AssistiveTouch、指针样式、跟踪速度、键盘显示策略。
6. 插入 HID，先确认 iPhone 系统层能识别指针或键盘。
7. 启动投屏接收器，iPhone 连接指定 AirPlay 名称。
8. 启动 Python GUI，填写 run_id，运行 doctor。
9. 注册设备、绑定串口、启动采集、截图。
10. 做五点校准并写入 evidence。

## 5. 单物料验收

HID 验收：

```powershell
@'
from imouse.hardware import list_devices
for item in list_devices():
    print(item)
'@ | .\.venv\Scripts\python -
```

通过标准：

- 插入前后串口列表有变化。
- GUI Bind 后设备状态可追溯。
- iPhone 上点击、滑动、输入真实生效。
- 连续 50 次点击无按下不释放。

投屏验收：

- iPhone 能发现接收端。
- 截图非黑屏、非空白。
- 截图尺寸和 iPhone 方向一致。
- 断开后能重连，重连耗时写入 evidence。

Hub/线材验收：

- 每个端口单独插拔测试。
- 连续 30 分钟不断连。
- 断开单台设备不影响其他端口。
- 对失败端口拍照并记录编号。

## 6. XP 专用硬件对比测试

如果拿到 XP 专用硬件，不要直接替换当前代码假设它能用。按这个顺序比对：

| 项目 | CH9329 原型 | XP 专用硬件 | 结论 |
|---|---|---|---|
| 电脑端是否暴露串口 | yes/no | yes/no | 决定是否能复用当前 serial 协议 |
| 绑定方式 | 手动 COM | 自动/手动 | 决定自动绑定研发方向 |
| iPhone 指针表现 | 普通 | 普通/快准狠 | 决定鼠标模式差距 |
| 点击误差 | px | px | 决定校准模型 |
| 滑动释放 | pass/fail | pass/fail | 决定 HID 帧适配 |
| 输入文本 | 英文/数字/符号 | 英文/中文/符号 | 决定键盘策略 |
| 断线恢复 | 手动/自动 | 手动/自动 | 决定 watchdog |

如果 XP 专用硬件不暴露标准串口或不兼容 CH9329 协议，研发任务应改成“硬件协议适配”，而不是继续修 GUI。

## 7. 采购验收报告模板

```text
采购批次:
供应商:
到货日期:
物料清单:
固件/版本:
测试 run_id:
通过物料:
失败物料:
失败分类:
可复现步骤:
证据路径:
是否允许进入 P1/P2:
```

失败物料不要混回生产测试台。所有坏件、疑似坏件、线材问题都单独收纳。

## 8. 常见坑

- 只看 API 返回成功，没看 iPhone 是否真实响应。
- 没贴编号，导致换线/换 Hub 后无法复盘。
- iPhone 锁屏、弹窗、亮度变化造成截图和 OCR 不稳定。
- 纯色模板导致 OpenCV 找图误判。
- 鼠标速度、AssistiveTouch、指针样式不同，导致同一坐标表现不同。
- Hub 供电不足，4 台能跑，10 台开始随机掉。
- 投屏接收器黑屏但 API 仍返回截图对象。
- 设备分组里有重复 ID 或已下线设备。
- XP 专用硬件协议未知，却按 CH9329 继续排查。
- 没记录投屏组件版本，后续升级后问题无法对比。

## 9. 和当前仓库的对应关系

| 现场项 | 当前仓库工具 | 证据 |
|---|---|---|
| Python/依赖/串口/投屏 preflight | `python -m imouse.doctor` | `evidence/<run_id>_doctor.md` |
| 设备注册/绑定/投屏/截图 | `python -m imouse.gui` | GUI log + JSONL |
| XP API 对接 | `/api` + `fun`, `imouse.xp_client` | 单测 + curl |
| 坐标校准 | GUI Calibration, `/calibration/*` | `state/calibration.json` + evidence |
| 单台脚本 | `scripts/p1_single_device_control_probe.json` | JSONL + Markdown |
| P2 稳定 | `scripts/p2_single_device_stability.json` | metrics + Manual |
| P3 试点 | `scripts/p3_pilot4_30min_watchdog.json` | 分组返回 + Manual |
| P4 稳定 | `scripts/stable_10_group_watchdog.json` | metrics + review |

## 10. 参考资料

- iMouse XP Python 文档说明 XP 版需配套专用硬件，且提供 Device、AirPlay、USB、Group、Image、Mouse、Keyboard 等 helper 能力：`https://www.imouse.cc/python-xp/`
- iMouse XP API 文档说明接口通过 `9911/api` 和 WebSocket 调用，并包含设备、配置、鼠标键盘、图色、回调等分类：`https://www.imouse.cc/XP版API文档/`
- BestMoon iMouse XP New version 文档描述 Windows 10+、内核/控制台分离等 XP 使用形态：`https://bestmoon-doc.gitbook.io/bestmoon/xp-tool-ios/imouse-xp-new-version`
- Apple 指针设备文档说明 iPhone 可通过 Lightning/USB-C 或蓝牙连接指针设备，并在 AssistiveTouch 中设置：`https://support.apple.com/en-us/111775`
- CH9329 公开资料说明其定位为串口转 USB HID 键盘/鼠标芯片：`https://www.alldatasheet.com/datasheet-pdf/pdf/1148630/WCH/CH9329.html`
