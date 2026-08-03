---
change_id: fix-admin-brand-list-logo-rendering
type: fix
status: applied
source_bug: BUG-0105-admin-brand-list-logo-renders-text
created_at: 2026-08-03 08:33:03
updated_at: 2026-08-03 12:49:26
---

# 测试计划

## Web 端

- 品牌列表存在 `thumbnail_url` 时，Logo 列渲染图片。
- 品牌列表仅存在 `logo_url` 时，Logo 列回退渲染图片。
- 品牌未上传 Logo 时，Logo 列渲染设计系统占位。
- 图片加载失败时，Logo 列渲染 fallback，不显示对象 key、文件名、URL 文本或调试文案。
- Logo 图片加载、失败和占位状态不改变表格列宽和行高。
- 品牌搜索、编辑入口、上下架、分页等操作保持可用。

## API 契约

- 默认仅验证现有 `GET /api/v1/admin/brands` 返回字段是否满足前端渲染。
- 若修改品牌列表响应 Schema，必须补充后端测试，并同步 OpenAPI、Orval 和 API 文档。

## 回归

- 运行品牌管理页相关前端测试。
- 如触及后端，运行品牌管理 API 相关 pytest。
- 记录是否需要 Docker Compose 验证；默认不需要。
