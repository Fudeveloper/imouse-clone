# GUI XP Package Namespace Guard

`Pkg Guard` 是 iMouse XP 包名的 GUI 供应链和 SDK 漂移看板。它与 `Src Refresh` 和 `Src Audit` 配对，但将包采用与真实设备证据分开。

## 范围

看板将三个 PyPI 命名空间作为独立包身份跟踪：

| 包 | 公开来源 | GUI 含义 |
|---|---|---|
| `imouse-py` | `https://pypi.org/project/imouse-py/` | 主要 SDK 形状线索，因为公开 Python XP 材料指向 `pip install imouse-py`。 |
| `imouse-xp` | `https://pypi.org/project/imouse-xp/` | 相似命名空间；作为依赖混淆风险审查。 |
| `py-imouse-xp` | `https://pypi.org/project/py-imouse-xp/` | 相似命名空间；作为 SDK 漂移和第三方风险审查。 |

## GUI 工作流

1. 从主工具栏、`Src Refresh` 或 `Src Audit` 打开 `Pkg Guard`。
2. 在网络访问不稳定的现场环境中，保持 `Run Offline` 为默认。
3. 仅在操作者被允许获取公开 PyPI/来源元数据时点击 `Run Live`。
4. 在采用包、更改 SDK 文档或声明 XP SDK 对标措辞之前导出 `evidence/<run_id>_<stage>_xp_package_namespace_guard.md`。
5. 使用 `Src Audit` 保留原始 URL/PyPI 报告，使用 `Action Map` 将接受的来源增量落地到测试、文档、SOP 或明确拒绝。

## 状态规则

- `fail`：审计行缺失或公开来源获取/解析失败。停止依赖采用。
- `pending`：离线模式或有意跳过的获取。视为审查任务，不是通过。
- `warn`：包来源可能可达，但在审查和现场证明完成之前采用仍被阻止。

`ok` 的来源元数据在 `Pkg Guard` 中被有意降级为 `warn`，因为包可用性不能证明接收器、HID、iPhone 响应、XP 硬件授权或广泛兼容性。

## 采用 SOP

在任何包触碰现场机器之前：

1. 固定精确包名、版本和哈希。
2. 审查维护者、源仓库、授权、发布历史和 API 面。
3. 将辅助域与本地 XP API/客户端测试进行比较。
4. 在隔离环境中运行本地 API 回归测试。
5. 在使用包行为进行对标措辞之前，要求对精确设备/iOS/接收器/HID 范围具有基于硬件的接收器/HID/iPhone 证据。

## 边界

`Pkg Guard` 不安装包，不写入 JSONL 证据，不证明截图新鲜度，不证明真实 iPhone 移动，不证明 XP 硬件对标，也不证明 iOS 兼容性。它是一个包风险 SOP 看板。
