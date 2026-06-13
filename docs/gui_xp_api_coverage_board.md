# GUI XP API Coverage Board

更新时间：2026-06-09

GUI `API Cov` 看板将 iMouse XP 风格 API 和 Python 辅助域映射到本地实现、本地测试、运行时门控、现场证据和声明边界。

它是操作者和研发规划层面。它不记录 JSONL 证据，不证明真实 iPhone 响应，也不证明 XP 专用硬件对标。

## 覆盖内容

看板分离以下通道：

- API 信封和传输：本地 9911 `/api`、HTTP/WebSocket、`fun`、`msgid`、`status`、`message`、`data`、`data.code`。
- 设备注册和配置文件：设备列表/注册/移除、配置文件和元数据辅助。
- AirPlay/接收器/采集：投屏启动、采集启动和截图新鲜度门控。
- USB/HID 绑定：硬件扫描、绑定/解绑、HID 身份和物理路由证明。
- 鼠标点击/滑动：点击和滑动 API 覆盖率加上通道分离的 Manual 证据。
- 键盘文字/按键输入：文字/按键/组合 API 覆盖率加上可见的物理 iPhone 输入。
- 图片/图像/颜色：截图、图像和颜色匹配绑定到可回放工件。
- OCR/查找文字：OCR 和文字匹配绑定到裁剪的真实截图和误报审查。
- 群控和批量控制：本地群控/批量 API 覆盖率与 P3/P4 按设备证明的对比。
- 配置/用户/快捷键：仅本地运行时脚手架。
- Callback/事件通道：诊断 callback 行，不是控制证明。
- 日志和失败分类：接收器/HID/脚本日志绑定到失败分类和重跑决策。
- 云端/LAN/账户操作：在核心控制和群控证据稳定之前仅为待办事项。

## 状态语义

- `p0_api_covered`：本地兼容性可从测试和源码审查，但它仅关闭 P0 API 形状。
- `local_api_covered`：本地 fun/helper 路由存在，但现场证明可能仍然缺失。
- `field_blocked`：接收器、HID、截图或 Manual 真实 iPhone 门控仍然未关闭。
- `lane_manual_required`：点击、滑动或文字仍需要各自的 Manual 观察通道。
- `scaffolding_only`：本地状态仅为保持兼容性形状可见。
- `backlog_only`：产品范围作为路线图/待办事项存在，不是实现或证明。

## 操作者 SOP

1. 从 Live Probe、Home、Core 或 Events 打开 `API Cov`。
2. 从第一个 `fail`、`pending` 或 `warn` 行开始。
3. 使用 `Run Selected` 跳转到所属 GUI 面板。
4. 将看板导出到 `evidence/<run_id>_<stage>_xp_api_coverage.md`。
5. 在审查备注中将本地 API 测试与现场证据分开。

## 声明边界

本地 API 或 SDK 辅助成功不是真实 iOS 控制。接收器、HID、鼠标、键盘、截图、视觉和群控行需要在任何控制声明之前具有相同运行的 JSONL 证据、保存的工件、通道分离的 Manual 观察、Acceptance PASS 和 Readiness PASS。配置/用户/快捷键和云端/账户行需要在核心控制证明后进行单独的产品验证。
