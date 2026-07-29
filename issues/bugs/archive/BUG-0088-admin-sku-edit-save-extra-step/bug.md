---
bug_id: BUG-0088-admin-sku-edit-save-extra-step
title: 管理端 SKU 编辑保存成功后未直接关闭弹窗
severity: medium
status: done
owner: product
discovered_at: 2026-07-28 23:23:36
environment: local
related_requirement: REQ-0006-tile-sku-management
related_change: fix-admin-sku-edit-save-extra-step
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-29 08:05:05
---

# 现象

管理端商品 SKU 编辑弹窗中，修改字段后点击“保存”，保存成功时没有直接关闭弹窗，而是在弹窗内出现额外的成功/任务追踪反馈。

# 复现步骤

1. 进入管理端瓷砖 SKU 列表。
2. 打开任一 SKU 的编辑弹窗。
3. 修改商品名称、价格、图片等任一可正常保存的字段。
4. 点击“保存”。

# 期望行为

- 更新接口成功返回后直接关闭编辑弹窗。
- 列表刷新并显示必要的全局 toast。
- 商品名称上方不显示“SKU 已更新...”任务追踪 tips。

# 实际行为

- 更新接口成功且返回 task_trace_id 时，弹窗内展示任务追踪反馈。
- 弹窗未关闭，用户还需要额外操作关闭。
- 商品名称上方显示多余的“SKU 已更新...”tips。

# 影响范围

- 管理端：瓷砖 SKU 编辑弹窗。
- 后端/API/数据库/小程序：无直接影响。

# 严重等级说明

严重等级为 medium。该问题不阻断数据保存，但造成编辑流程多一步并产生不必要提示，影响运营效率与体验一致性。
