---
bug_id: BUG-0028-tile-spec-modal-form-layout
status: captured
created_at: 2026-06-28 13:13:16
updated_at: 2026-06-28 13:13:16
severity_hint: medium
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_bug:
---

# 现象

Web 管理端「瓷砖规格」新增/编辑弹窗表单布局与展示规范不符合预期：

1. **尺寸名称位置**：只读「尺寸名称」字段当前位于宽度/长度输入框下方，应置于宽度/长度**上方**。
2. **尺寸名称格式**：自动生成值带 `mm` 后缀（如 `600x1200mm`），应显示为 `600x1200`（单位已在宽/长字段标签中体现）。
3. **备注字段宽度**：「备注」文本框未占满整行，仅占部分列宽。

# 复现步骤

1. 以 admin 登录 Web 管理端，打开「瓷砖规格」列表页。
2. 点击「+ 新增瓷砖规格」或某行「编辑」。
3. 在宽度、长度输入框中填写数值（如 600、1200），观察只读尺寸名称位置与格式。
4. 观察「备注」文本框是否占满表单整行宽度。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 尺寸名称在宽/长字段上方；显示 `600x1200`（无 `mm`）；备注输入框占满整行。 |
| **实际** | 尺寸名称在宽/长下方；显示 `600x1200mm`；备注框宽度不足。 |

# 附件

- screenshots/tile-spec-modal-form-layout.png
