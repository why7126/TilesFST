---
bug_id: BUG-0093-miniapp-category-secondary-grid-name-full-display
status: done
created_at: 2026-07-30 23:05:45
updated_at: 2026-07-31 00:08:23
---

# 临时规避方案

## 用户侧规避

暂无可靠用户侧规避方案。用户可以点击被截断的二级类目进入商品列表后，通过列表标题或商品内容辅助判断是否选择了正确类目，但这不能解决分类页入口可读性问题。

## 运营侧规避

短期内可临时缩短二级类目名称，减少规格和工艺描述长度。但该方式会牺牲类目信息表达，不建议作为正式解决方案。

## 开发侧临时处理

如需快速止血，可优先调整小程序分类页样式：

- 将 `.secondary-grid` 和 `.skeleton-grid` 改为每行 2 个。
- 移除 `.secondary-name` 的 2 行截断限制，允许完整换行。
- 保持点击事件、`data-id`、`data-name` 和 `aria-label` 不变，避免影响分类商品列表入口。

该处理仍需通过 OpenSpec Change 和代码评审后实施。
