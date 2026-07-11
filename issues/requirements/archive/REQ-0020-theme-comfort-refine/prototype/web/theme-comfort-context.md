---
requirement_id: REQ-0020-theme-comfort-refine
title: 主题舒适度与主题切换 Prototype Context
status: pending_review
owner: product
source: requirement.md
created_at: 2026-07-11 17:22:09
updated_at: 2026-07-11 17:22:09
---

# Prototype Context

## 1. 原型文件

| 文件 | 用途 |
|---|---|
| `prototype/web/theme-comfort-matrix.html` | 静态 HTML 原型，展示四类主题模式与首批验收页面矩阵。 |
| `prototype/web/theme-comfort-context.md` | 本说明文件，约束实现优先级和验收重点。 |
| `prototype/web/theme-comfort-matrix.png` | 待实现阶段或评审阶段导出，可作为视觉验收截图。 |

## 2. 主题模式

本期纳入四类主题：

| 模式 | 用途 |
|---|---|
| 系统默认 | 跟随系统或产品默认策略；仍必须可解释最终落到哪类主题。 |
| 暗色旗舰 | 当前工业石材品牌暗色，用于品牌展示、高端氛围和用户主动选择暗色。 |
| 舒适暗色 | 降低纯黑压迫、弱化刺眼对比，优先服务管理端长时间操作。 |
| 浅色 | 强光环境和偏好浅色用户使用，需要补齐完整 token 与组件状态验收。 |

## 3. 首批验收页面矩阵

| 场景 | 代表页面 / 组件 | 必须覆盖 |
|---|---|---|
| 登录页 | Web 管理端登录页 | 背景、材质拼贴、表单、错误、按钮、语言切换。 |
| 列表页 | 瓷砖 SKU 管理页 | 指标卡、筛选、表格、sticky 操作列、分页、toast。 |
| 表单页 | 瓷砖 SKU 编辑表单 | 输入、选择器、帮助文案、错误、保存 CTA。 |
| 弹窗 | 瓷砖 SKU 新建 / 编辑弹窗 | 宽度、滚动、遮罩、表单、媒体上传状态、确认操作。 |
| `/design-system` | 主题验收页 | token、基础组件、管理端组件、状态样例。 |
| 店主 Web | 商品列表 / 详情 / 询价 | 除品牌展示页外支持舒适主题。 |

## 4. 实现边界

- HTML 原型用于表达结构和验收矩阵，不替代最终 React 实现。
- 实现必须使用 Design System semantic token；不得把原型色值直接复制进业务 TSX/CSS。
- 店主品牌展示页、Hero 和品牌氛围区域允许继续保持暗色旗舰风。
- 店主商品列表、筛选、详情阅读和询价路径需要支持舒适主题。
- 主题偏好采用本地持久化 + 账号级持久化二者结合，后续 Change 必须补 API / DB / Orval 设计。

## 5. Knowledge-base 约束

- 瓷砖 SKU 列表页遵守 `admin-list-page-consistency.md`。
- 瓷砖 SKU 表单页或设置页遵守 `admin-form-page-consistency.md`。
- 瓷砖 SKU 弹窗遵守 `admin-modal-width-css-cascade.md`。
- 瓷砖 SKU 媒体上传状态 UI 遵守 `admin-media-upload-chain.md`。
