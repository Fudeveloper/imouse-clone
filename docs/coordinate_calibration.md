# 坐标校准与点偏排查

更新时间：2026-06-08

iOS 群控里，API 返回成功不等于真实点准。常见点偏来源：

- 投屏画面被裁剪、黑边、窗口标题栏或缩放影响。
- 截图坐标空间和 HID 绝对坐标空间不一致。
- iPhone 型号、分辨率、横竖屏、刘海/灵动岛、安全区不同。
- 有线/无线投屏链路返回的帧尺寸不同。
- 固件或鼠标模式改变了坐标解释方式。

因此每台设备都要保存一份校准配置，并把校准前后的测试写入 evidence。

## 校准模型

当前配置字段：

```json
{
  "enabled": true,
  "source_width": 1170,
  "source_height": 2532,
  "active_x": 0,
  "active_y": 0,
  "active_width": 1170,
  "active_height": 2532,
  "target_width": 1170,
  "target_height": 2532,
  "safe_left": 0,
  "safe_top": 80,
  "safe_right": 0,
  "safe_bottom": 40,
  "orientation": "portrait",
  "notes": "iPhone 14 Pro portrait AirPlay"
}
```

含义：

- `source_width/source_height`：截图坐标空间。
- `active_x/active_y/active_width/active_height`：截图里真实手机画面的有效区域。
- `target_width/target_height`：硬件控制坐标空间。
- `safe_*`：安全区边距，先用于记录和复盘，后续可扩展成强制避让。
- `orientation`：`portrait`、`landscape_left`、`landscape_right`、`portrait_upside_down`。

默认无校准时保持旧行为：直接按截图坐标和当前 `screen_width/screen_height` 下发。

## GUI 校准流程

1. 启动 GUI，设置本轮 `Evidence run_id`。
2. 注册设备并完成投屏/截图。
3. 点击 `Screenshot`，确认预览不是黑屏。
4. 在 `Coordinate Calibration` 面板点击 `Use Screenshot`。
5. 如果截图有黑边或裁剪，手动调整 `Active x/y/w/h`。
6. 如果硬件坐标空间不是截图尺寸，手动调整 `Target w/h`。
7. 勾选 `Enabled`。
8. 点击 `Save`。
9. 在 5 个点位做实测：左上、右下、中心、刘海/灵动岛附近、底部 Home Indicator 附近。
10. 用底部 `Manual` 行记录每个点位是否点准，失败时保存截图/录屏路径。

通过标准：

- 5 个点位都能稳定命中安全区域。
- 连续 50 次点击无明显漂移。
- 横屏和竖屏必须分别保存校准或记录方向策略。

## XP API 示例

保存校准：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/calibration/set\",\"data\":{\"id\":\"dev_1\",\"calibration\":{\"enabled\":true,\"source_width\":1170,\"source_height\":2532,\"active_width\":1170,\"active_height\":2532,\"target_width\":1170,\"target_height\":2532}}}"
```

读取校准：

```powershell
curl.exe -X POST http://127.0.0.1:9911/api `
  -H "Content-Type: application/json" `
  -d "{\"fun\":\"/calibration/get\",\"data\":{\"id\":\"dev_1\"}}"
```

列出校准：

```powershell
curl.exe "http://127.0.0.1:9911/api?fun=/calibration/list"
```

校准默认持久化到：

```text
state/calibration.json
```

## 点偏排查

按顺序查：

1. 截图尺寸是否与 `source_width/source_height` 一致。
2. 预览图里手机真实画面是否从 `active_x/active_y` 开始。
3. `active_width/active_height` 是否排除了黑边和窗口边框。
4. `target_width/target_height` 是否等于硬件真实坐标空间。
5. 横竖屏方向是否和 `orientation` 一致。
6. 是否误把 Retina 逻辑点、物理像素、投屏帧尺寸混在一起。
7. 是否点击到了刘海、安全区、系统手势区域。
8. 单点点击是否准，滑动是否存在按下未释放。

每次点偏都要记录：

- 设备 ID。
- iPhone 型号和 iOS 版本。
- 截图尺寸。
- 校准 JSON。
- 期望点位和实际响应。
- 失败截图/录屏。
- evidence run id。
