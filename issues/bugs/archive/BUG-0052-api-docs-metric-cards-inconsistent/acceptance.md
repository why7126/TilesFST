---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
title: 接口文档页指标卡样式与瓷砖 SKU 页不一致 - 验收标准
severity: medium
status: approved
owner: product
created_at: 2026-07-01 13:54:17
updated_at: 2026-07-01 14:01:11
related_requirement: REQ-0022-admin-api-docs-menu
---

# 验收标准

## AC-001 指标卡 DOM 结构对齐

- [ ] 打开 `/admin/api-docs`。
- [ ] 标题下方四个摘要指标卡使用管理端基准结构。
- [ ] 每个卡片包含 `.metric-label`、`.metric-value`、`.metric-desc`。
- [ ] 摘要卡不再使用裸 `strong` / `span` 作为数值和说明的唯一样式承载。

## AC-002 视觉层级与 SKU 页一致

- [ ] 打开 `/admin/tile-skus`，记录标题下方 SKU 统计指标卡视觉基线。
- [ ] 打开 `/admin/api-docs`，对照接口摘要指标卡。
- [ ] 两个页面指标卡在边框、背景、圆角、内边距、数字强调色、数字字号、说明文字弱化层级上保持一致。
- [ ] 页面仍符合暗色旗舰风管理端视觉规范。

## AC-003 semantic token 与样式边界

- [ ] 修复不得在 TSX/CSS 中新增裸 Hex。
- [ ] 修复应复用已有 `summary-grid`、`metric-card`、`metric-label`、`metric-value`、`metric-desc` 语义类。
- [ ] 如需新增局部 class，仅用于接口文档页特有布局，不重写通用 metric 视觉规则。

## AC-004 接口文档页功能不回归

- [ ] `/admin/api-docs` 仍展示接口总数、受保护接口数、Orval 映射数、非 `/api/v1` 路由数。
- [ ] 接口搜索、Method 筛选、Tag 筛选、Auth 筛选仍可用。
- [ ] OpenAPI JSON 入口仍可打开。
- [ ] Swagger UI / Swagger 只读入口仍按当前环境策略展示。
- [ ] Orval 方法名和「未生成」状态展示不受影响。

## AC-005 权限边界不回归

- [ ] admin 仍可访问 `/admin/api-docs`。
- [ ] employee 仍不能在侧栏看到「接口文档」入口。
- [ ] employee 直链 `/admin/api-docs` 仍进入无权限页或等价拦截。
- [ ] 店主 Web 与微信小程序不出现接口文档入口。

## AC-006 前端测试覆盖

- [ ] `ApiDocsPage` 测试覆盖摘要指标卡渲染。
- [ ] 测试断言摘要指标卡存在 `.metric-value` 与 `.metric-desc`。
- [ ] 既有接口筛选、Orval 展示、生产 Swagger 只读测试继续通过。

## AC-007 影响范围确认

- [ ] 修复不修改后端 API 请求/响应结构。
- [ ] 修复不修改数据库。
- [ ] 修复不修改 MinIO、上传或媒体直出链路。
- [ ] 修复不要求重新生成 Orval。
- [ ] 修复不要求 Docker Compose 配置变更。
