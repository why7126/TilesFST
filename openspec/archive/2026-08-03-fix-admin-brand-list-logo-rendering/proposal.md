---
change_id: fix-admin-brand-list-logo-rendering
type: fix
status: applied
source_bug: BUG-0105-admin-brand-list-logo-renders-text
created_at: 2026-08-03 08:33:03
updated_at: 2026-08-03 12:49:26
---

# 修复管理后台品牌列表 Logo 渲染

## 背景与原因

`BUG-0105-admin-brand-list-logo-renders-text` 已评审通过。管理后台品牌列表第一列的品牌 Logo 未正常渲染为图片，而是显示为文字内容。

该问题影响品牌列表的视觉识别和 Logo 上传结果核对效率，也可能把图片 URL、对象 key、文件名或字段文本暴露到表格单元格中。当前严重等级为 `medium`，不阻断品牌数据维护，但需要进入正常 BUG 修复流程。

## 变更内容

- 修复管理后台品牌列表 Logo 列渲染方式，使已上传 Logo 的品牌显示图片或缩略图。
- 为未上传 Logo、图片加载失败或无效 URL 提供稳定占位。
- 回归品牌搜索、编辑、上下架等既有操作。
- 验证前端字段映射与后端品牌列表响应中的 `logo_url`、`thumbnail_url` 或等价预览 URL 一致。

## 范围

### 范围内

- Web 管理后台品牌列表 Logo 列展示。
- 品牌 Logo 字段映射、图片缩略图优先级和 fallback 状态。
- 与 `GET /api/v1/admin/brands` 响应字段契约相关的最小验证。
- Web 前端回归测试；如实现触及后端字段契约，则补充后端/API/Orval 测试。

### 范围外

- 新增品牌 Logo 上传能力。
- 新增数据库字段或迁移。
- 改造 MinIO 存储策略。
- 小程序品牌展示。
- 品牌编辑弹窗冗余文案问题，该事项由独立 BUG 跟踪。

## 回滚方案

1. 若仅前端渲染变更导致问题，回滚品牌列表 Logo 列组件或字段映射变更。
2. 若 API 字段契约被调整且出现兼容风险，回滚后端 Schema/API 改动并重新生成 Orval 客户端。
3. 回滚后保留现有品牌数据，不执行数据库清理。
4. 回滚验证至少覆盖品牌列表加载、搜索、编辑入口和上下架操作。

## 影响范围

- API：默认不变；实现时若发现缺少可展示 URL 字段，必须同步 OpenAPI、Orval、docs 和测试。
- DB：默认不变。
- Web：影响管理后台品牌列表。
- 小程序：不影响。
- 管理端：影响品牌列表 Logo 展示。
- Docker Compose：不需要。
