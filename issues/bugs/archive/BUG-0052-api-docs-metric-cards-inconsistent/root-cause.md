---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式与瓷砖 SKU 页不一致 - 根因分析
severity: medium
status: approved
owner: product
created_at: 2026-07-01 13:54:17
updated_at: 2026-07-01 14:01:11
related_requirement: REQ-0022-admin-api-docs-menu
---

# 根因分析

## 直接原因

接口文档页 `/admin/api-docs` 的摘要指标卡虽然复用了 `summary-grid` 与 `metric-card` 容器类名，但卡片内部 DOM 使用了：

```text
p.metric-label
strong
span
```

瓷砖 SKU 页 `/admin/tile-skus` 的同类指标卡使用的是管理端基准结构：

```text
article.metric-card
  div.metric-label
  div.metric-value
  div.metric-desc
```

管理端通用指标卡样式在 `admin-home.css` 中主要绑定 `.metric-label`、`.metric-value`、`.metric-desc`。接口文档页缺少 `.metric-value` 与 `.metric-desc`，导致数字强调色、字号、上间距和说明文字弱化层级不能完整命中。

## 根本原因

REQ-0022 实现接口文档页时，页面局部完成了“看起来像指标卡”的容器复用，但没有把 SKU 页同类指标卡作为结构级复用基线。

| 层级 | 现状 | 结果 |
|---|---|---|
| DOM 结构 | `/admin/api-docs` 使用 `strong` / `span` 表达数值和说明 | 通用 metric 样式无法完整命中 |
| 样式复用 | 仅复用 `summary-grid` / `metric-card` 容器 | 边框与背景接近，但文字层级不一致 |
| 验收粒度 | REQ-0022 验收了 summary 指标存在 | 未覆盖与 SKU 页同类卡片 DOM/class 对齐 |
| 组件抽象 | 管理端指标卡没有独立共享组件 | 页面可各自拼 DOM，容易漂移 |

该问题属于 UI 结构复用不足，不是数据接口、权限、数据库或路由问题。

## 触发条件

满足以下条件即可触发：

1. 使用管理员身份进入 Web 管理端。
2. 打开 `/admin/api-docs`。
3. 页面渲染接口摘要指标卡。
4. 与 `/admin/tile-skus` 标题下方 SKU 统计指标卡对照。

该缺陷不依赖后端接口返回的具体统计值；只要接口文档页渲染 summary 区域，即可观察到样式不一致。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是，接口文档页 JSX 结构未使用管理端 metric 基准 class |
| design | 是，页面局部实现未结构级对齐既有 SKU 页同类组件 |
| ui | 是，影响管理端视觉一致性与 Design System 验收 |
| api | 否，不涉及 API 请求、响应或错误码 |
| db | 否，不涉及数据库结构或查询 |
| security | 否，不涉及鉴权、敏感信息或上传安全 |
| deployment | 否，不涉及 Docker、Nginx 或端口配置 |

## 关联实现点

- 接口文档页：`src/web/src/pages/admin/ApiDocsPage.tsx`
- SKU 页基准：`src/web/src/pages/admin/TileSkuManagementPage.tsx`
- 管理端指标卡样式：`src/web/src/features/admin/styles/admin-home.css`
- 接口文档页局部样式：`src/web/src/features/admin/styles/api-docs.css`

## 修复方向建议

后续修复 Change 中建议优先采用最小 UI 对齐方案：

1. 将 `/admin/api-docs` 摘要卡片 DOM 调整为 SKU 页同类结构：`article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`。
2. 保留现有 `summary-grid`、`metric-card` 和 semantic token 样式来源，不新增裸 Hex。
3. 增加前端测试，断言接口文档页 summary 卡包含 `.metric-value` 与 `.metric-desc`，防止再次用裸 `strong` / `span` 漂移。
4. 若后续多页面复用继续增加，可考虑在单独 OpenSpec Change 中抽象管理端 `MetricCard` 共享组件；本 BUG 修复不必扩大范围。
