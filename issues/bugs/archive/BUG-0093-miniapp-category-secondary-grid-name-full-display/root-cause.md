---
bug_id: BUG-0093-miniapp-category-secondary-grid-name-full-display
status: done
created_at: 2026-07-30 23:05:45
updated_at: 2026-07-31 00:08:23
---

# 根因分析

## 直接原因

微信小程序分类页右侧二级类目列表使用固定 3 列网格：

- `src/miniapp/pages/category/index.wxss` 中 `.secondary-grid` 设置为 `grid-template-columns: repeat(3, minmax(0, 1fr))`。
- 单个 `.secondary-card` 宽度被 3 列布局压缩，较长规格类目名称没有足够横向展示空间。
- `.secondary-name` 设置了 `overflow: hidden`、`display: -webkit-box`、`-webkit-line-clamp: 2`，当名称超过 2 行可容纳范围时会被截断。

## 根本原因

历史修复已关注“长名称不应被省略”的问题，但分类页二级类目卡片仍保留偏密集的 3 列布局和 2 行截断规则。当前样式没有把真实业务类目名称长度纳入布局验收，尤其没有覆盖包含规格数字与中文描述组合的名称，例如 `600X1200 仿古精雕...`。

## 触发条件

- 页面：微信小程序 `pages/category/index`。
- 区域：右侧二级类目卡片列表。
- 数据：二级类目名称包含较长规格和工艺描述。
- 样式条件：3 列布局 + 卡片固定最小高度 + 文本最多 2 行且隐藏溢出。

## 根因分类

- 类型：`design` / `code`
- 子类：响应式布局与长文本展示规则不匹配
- 非根因：接口未返回完整名称、数据库类目名称缺失、路由参数丢失

## 修复方向

- 将二级类目卡片网格从每行 3 个调整为每行 2 个。
- 同步调整 skeleton 网格，避免加载态和完成态列数跳变。
- 取消或放宽二级类目名称的截断限制，保证所有类目名称完整展示。
- 长名称允许自然换行，并通过卡片高度、内边距和对齐方式保证布局稳定。
