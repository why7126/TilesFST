---
bug_id: BUG-0088-admin-sku-edit-save-extra-step
status: done
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-29 08:05:05
severity_hint: medium
environment: local
related_requirement: REQ-0006-tile-sku-management
related_bug:
captured_via: capture
classification_rationale: 已有管理端 SKU 编辑弹窗保存流程下的行为偏差，成功保存后出现额外反馈步骤且弹窗未直接关闭，归类为 BUG。
---

# 现象

管理端商品 SKU 编辑弹窗中，修改字段后点击保存，在可以正常保存时没有直接保存并关闭弹窗，而是多了一步成功提示/任务追踪反馈。

同时，商品名称上方不需要显示“SKU 已更新...”一类 tips，该提示对编辑流程是多余的。

# 复现步骤

1. 进入管理端瓷砖 SKU 列表。
2. 打开任一商品 SKU 的编辑弹窗。
3. 修改可正常通过校验并保存的字段。
4. 点击“保存”。

# 期望 vs 实际

- 期望：保存成功后直接关闭编辑弹窗，并刷新列表；不在商品名称上方显示“SKU 已更新...”tips。
- 实际：保存成功后弹窗内出现额外成功/任务追踪反馈，用户还需要额外操作才能离开弹窗；商品名称上方出现多余 tips。

# 附件

暂无。
