# XP 公开来源审计

`imouse.source_audit` 是 GUI `Src Refresh` 面板的可重复来源刷新配套工具。它抓取公开的 iMouse XP、Some3C 和 PyPI 端点，记录 HTTP 状态、预期术语匹配、PyPI 包版本元数据、本地文档时间戳、SOP owner 和声明边界。

它仅作为来源情报。它不写 JSONL 现场 evidence，不证明真实 iPhone 响应，不证明广泛 iOS 兼容性，也不证明 XP 对标。

## 命令

离线审计，适合现场运行前或网络阻断时使用：

```powershell
.\.venv\Scripts\python -m imouse.source_audit --offline --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md
```

在线审计，适合在变更来源驱动的文档、兼容性声明、包依赖、roadmap 优先级或演示声明之前使用：

```powershell
.\.venv\Scripts\python -m imouse.source_audit --markdown evidence\<run_id>_<stage>_xp_public_source_audit.md --allow-failures
```

JSON 审计用于自动化或差异审查：

```powershell
.\.venv\Scripts\python -m imouse.source_audit --json --allow-failures
```

## 行含义

- `ok`：URL 抓取成功且预期术语匹配。这表示公开来源可达，不表示本地原型控制了 iPhone。
- `warn`：URL 抓取成功但元数据或预期术语已漂移。手动审查来源并在使用声明前更新文档/测试/SOP。
- `pending`：离线模式或有意跳过的抓取。将其视为任务，不是通过。
- `fail`：抓取或 JSON 解析失败。在此问题解决或明确记录之前，不要更新公开来源驱动的声明。

## SOP

1. 在 GUI 中运行 `Src Refresh`，识别第一个为 `fail`、`pending` 或 `warn` 的来源/SOP 行。
2. 运行 `python -m imouse.source_audit`，将 Markdown 报告导出到 `evidence/`。
3. 对于每个 `warn` 或 `fail`，手动打开来源并判断是来源漂移、网络问题、站点布局变更、包注册表漂移还是无关噪声。
4. 将每个接受的来源变更转化为以下之一：本地文档更新、GUI 行更新、测试预期、路线决策字段、设备/iOS 矩阵条目、包固定/hash 审查或明确拒绝。
5. 重新运行 `Sources`、`Action Map`、`Snapshot`、`XP Timeline`、`Iter Radar` 和 `Pack`。
6. 保持 Acceptance 和 Readiness 严格：来源新鲜度永远不替代真实 iPhone 截图、点击、滑动、文本、人工观察、组件台账和 JSONL evidence。

## 当前来源集

- `https://www.imouse.cc/`
- `https://www.imouse.cc/python-xp/`
- `https://www.imouse.cc/XP%E7%89%88API%E6%96%87%E6%A1%A3/`
- `https://doc.some3c.com/iphone-farm-setup/imouse-xp-new-version`
- `https://doc.some3c.com/iphone-farm-setup/iphone-farm-settings`
- `https://pypi.org/pypi/imouse-py/json`
- `https://pypi.org/pypi/imouse-xp/json`
- `https://pypi.org/pypi/py-imouse-xp/json`

## 包命名空间漂移守卫

审计有意跟踪三个 PyPI 命名空间：

| 包 | JSON 端点 | 在 SOP 中的角色 |
|---|---|---|
| `imouse-py` | `https://pypi.org/pypi/imouse-py/json` | 主要公开 SDK 形态信号，因为 Python XP 页指向 `pip install imouse-py`。 |
| `imouse-xp` | `https://pypi.org/pypi/imouse-xp/json` | 相似名称包，在审查之前必须视为依赖混淆和漂移风险。 |
| `py-imouse-xp` | `https://pypi.org/pypi/py-imouse-xp/json` | 相似名称包，在维护者、来源、hash、许可证和 API 行为被审查之前必须视为第三方。 |

采用规则：在现场机器上不要安装任何相似包，直到确切 artifact 已固定版本、固定 hash、来源已审查、许可证已审查、有本地 API 回归覆盖并有 receiver/HID/iPhone evidence 支持所声明的精确范围。

包元数据可以指导 SDK 比较和供应链审查。它不能证明截图新鲜度、真实 iPhone 移动、XP 硬件授权、广泛 iOS 兼容性或 XP 对标。

## 边界

审计可以告诉团队公开页面或包注册表可达且仍包含预期关键词。它不能告诉团队 receiver 窗口是最新的、HID 命令移动了真实手机、SDK 是否能与 XP 硬件配合工作、或某个 model/iOS 组合在本地已覆盖。这些声明仍然需要同轮现场 evidence、Acceptance PASS、Readiness PASS 和精确设备/iOS 范围。
