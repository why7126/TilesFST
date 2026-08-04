---
bug_id: BUG-0114-miniapp-brand-list-category-column-alignment
title: 小程序品牌列表页品牌类目两列未分别左对齐
acceptance_status: passed
severity: medium
created_at: 2026-08-04 09:00:52
updated_at: 2026-08-04 23:12:32
source_change: fix-miniapp-brand-list-category-column-alignment
source_sprint: sprint-019
---

# Acceptance

## 验收范围

- 端：微信小程序
- 页面：`pages/brand-list/index`
- 区域：品牌矩阵卡片下方类目胶囊
- 不涉及：后端 API、数据库、对象存储、Web 展示端、管理端

## 回归验收项

| AC | 验收点 | 预期 |
|---|---|---|
| AC-001 | 两列布局 | 品牌卡片下方类目区固定为两列展示，不再依赖胶囊内容宽度形成自然流式排布。 |
| AC-002 | 左列对齐 | 左侧列所有类目胶囊起始位置保持一致。 |
| AC-003 | 右列对齐 | 右侧列所有类目胶囊起始位置保持一致，形成稳定纵向对齐线。 |
| AC-004 | 单行省略号 | 类目名称超出所在胶囊可用宽度时单行显示省略号，不换行、不撑破边框、不横向溢出。 |
| AC-005 | 点击行为 | 点击任一类目胶囊仍跳转 `pages/product-list/index`，并携带完整 `brandId`、`categoryId`、`categoryLevel=secondary`、完整 `categoryName` 与 `sourcePage=brand-list-category`。 |
| AC-006 | 空类目 | 无类目的品牌仍展示 `暂无类目`，不出现空白错位或异常占位。 |
| AC-007 | 视觉回归 | 品牌 Logo、品牌名称、商品数量、进入箭头、卡片边框、底部返回首页悬浮按钮不发生重叠或错位。 |
| AC-008 | 多视口 | 在小程序常见宽度下，两列对齐与省略号策略保持一致。 |

## 建议验证数据

- 短类目：`400X800亮光`、`800X800亮光`
- 中等类目：`600X1200金丝绒`、`750X1500莱姆石`
- 长类目：`600X1200金丝绒木纹`、`750X1500精雕木纹`

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-miniapp-brand-list-category-column-alignment
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

