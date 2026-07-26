---
change_id: fix-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式对齐 - 设计
created_at: 2026-07-01 20:33:50
updated_at: 2026-07-02 08:58:31
source_bug: BUG-0052-api-docs-metric-cards-inconsistent
status: applied
---

# Design

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | `/admin/api-docs` 标题下方接口摘要指标卡与 `/admin/tile-skus` 同类指标卡视觉不一致 |
| 稳定复现 | 管理员进入 `/admin/api-docs`，查看摘要卡；再进入 `/admin/tile-skus`，对照 SKU 统计卡 |
| 实际结构 | API docs 摘要卡使用 `p.metric-label` + `strong` + `span` |
| 期望结构 | 使用 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc` |
| 影响范围 | Web 管理端 `/admin/api-docs` UI 一致性与 Design System 验收 |
| 严重等级 | medium |

## Root Cause

管理端通用 metric card 样式由 `admin-home.css` 提供，关键选择器为：

```text
.metric-label
.metric-value
.metric-desc
```

`/admin/tile-skus` 页面使用了上述结构，因此数字强调色、字号、间距和说明文字弱化层级完整生效。`/admin/api-docs` 页面只复用了外层 `summary-grid` / `metric-card`，内部没有 `.metric-value` / `.metric-desc`，导致样式命中不完整。

## Repair Strategy

1. 将 `/admin/api-docs` 四个摘要卡从 `div.metric-card` 调整为与 SKU 页一致的结构：

   ```text
   article.metric-card
     div.metric-label
     div.metric-value
     div.metric-desc
   ```

2. 保留现有数据字段：
   - `total_routes`
   - `protected_routes`
   - `orval_mapped_routes`
   - `non_api_v1_routes`

3. 保留现有文案含义，但允许把英文标签调整为更符合管理端 metric baseline 的中文标签或继续保持当前 label，只要视觉层级一致。
4. 不修改 `api-docs.css` 中 route table、filter、Swagger panel 样式；如需微调，仅限接口文档页特有布局，不重写通用 metric 视觉规则。
5. 不修改 backend aggregation endpoint、OpenAPI、Orval、Swagger 策略或权限守卫。

## Frontend Design

涉及文件预计为：

- `src/web/src/pages/admin/ApiDocsPage.tsx`
- `src/web/src/pages/admin/ApiDocsPage.test.tsx`

实现要求：

- MUST 使用既有 `summary-grid`、`metric-card`、`metric-label`、`metric-value`、`metric-desc`。
- MUST NOT 在 TSX/CSS 中新增裸 Hex。
- MUST NOT 引入新的页面级 card 嵌套或营销式组件。
- SHOULD 保持 `/admin/api-docs` 摘要区与 `/admin/tile-skus` 摘要区 DOM 语义接近。

## Test Design

前端测试需覆盖：

- `ApiDocsPage` 渲染四个摘要指标卡。
- 每个摘要卡或至少全部摘要区包含 `.metric-value` 与 `.metric-desc`。
- 既有 Orval 方法名展示、「未生成」状态、筛选、生产 Swagger 只读入口测试继续通过。

不需要新增后端测试；本 change 不改 API。

## Risk

| 风险 | 缓解 |
|---|---|
| 为追求视觉接近而新增局部硬编码样式 | 使用既有 metric class 和 semantic token，禁止裸 Hex |
| 改 DOM 影响测试查询 | 更新测试断言以可访问文本和 class 结构为准 |
| 与 BUG-0053 分页修复并行冲突 | 本 change 仅触碰 summary 区；BUG-0053 应聚焦 table header/pagination |
| 与 BUG-0051 Swagger 代理修复交叉 | 不修改 Swagger link、proxy 或环境策略 |
