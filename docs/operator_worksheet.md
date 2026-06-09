# Operator Worksheet 使用说明

更新时间：2026-06-08

`imouse.operator_worksheet` 用来给现场操作员生成可填写的 Markdown 表单。它和 `field_packet` 的区别是：

- `field_packet` 偏执行包：汇总当前 doctor/readiness、命令和流程。
- `operator_worksheet` 偏现场填表：逐项记录结果、附件、失败分类和证据路径。

两者都不是 evidence，不会证明真实 iPhone 已响应；真实结论仍以 `evidence/<run_id>.jsonl`、Acceptance 和 Readiness 为准。

## 命令行生成

P1 单台：

```powershell
.\.venv\Scripts\python -m imouse.operator_worksheet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1
```

P3 四台：

```powershell
.\.venv\Scripts\python -m imouse.operator_worksheet --stage p3 --run-id pilot_4_YYYYMMDD --devices dev_1,dev_2,dev_3,dev_4
```

默认输出：

```text
evidence/<run_id>_<stage>_operator_worksheet.md
```

也可以指定输出路径：

```powershell
.\.venv\Scripts\python -m imouse.operator_worksheet --stage p1 --run-id p1_dev1_YYYYMMDD --devices dev_1 --output evidence\p1_dev1_YYYYMMDD_operator.md
```

## GUI 生成

启动 GUI：

```powershell
.\.venv\Scripts\python -m imouse.gui
```

在底部 `SOP` 行：

1. 设置 `Evidence run_id`。
2. 选择阶段 `p1`、`p2`、`p3` 或 `p4`。
3. 选中目标设备。
4. 点击 `Worksheet`。

GUI 会生成：

```text
evidence/<run_id>_<stage>_operator_worksheet.md
```

## 表单内容

生成的 worksheet 包含：

- Bench Ledger：每台设备的 iPhone、receiver、capture、HID、Hub、线材和 operator note。
- Operator Checklist：每一步的执行动作、结果、附件和失败分类。
- Script Commands：当前阶段应 dry-run 和 real-run 的脚本命令。
- Acceptance Commands：Review、Acceptance、Gap、Readiness 命令。
- Failure Taxonomy：现场失败分类。
- Promotion Rule：进入下一阶段的硬门槛。

## 使用原则

- 每个 `pass` 都必须能对应 evidence JSONL 事件或 artifact。
- `fail` 必须填写失败分类，优先从表单里的 Failure Taxonomy 选择。
- API 成功、dry-run 成功、worksheet 全部勾选，都不能替代真实 iPhone 人工观察。
- 如果 route decision 失败已经写入 evidence，本轮 run_id 视为 blocked，修复后换新 run_id。

