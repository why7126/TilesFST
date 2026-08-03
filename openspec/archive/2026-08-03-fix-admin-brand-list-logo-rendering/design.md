---
change_id: fix-admin-brand-list-logo-rendering
type: fix
status: applied
source_bug: BUG-0105-admin-brand-list-logo-renders-text
created_at: 2026-08-03 08:33:03
updated_at: 2026-08-03 12:49:26
---

# 设计说明

## 缺陷分析报告

### 现象

管理后台品牌列表第一列品牌 Logo 未渲染为图片，而是显示为文字内容。

### 复现路径

1. 登录管理后台。
2. 进入品牌列表页面。
3. 查看第一列品牌 Logo。
4. 观察已上传 Logo 的品牌是否显示图片。

### 影响

- 管理后台品牌列表无法直观看到品牌 Logo。
- 品牌维护人员无法通过列表高效核对 Logo 上传结果。
- 图片 URL、对象 key、文件名或字段文本可能以普通文字方式暴露在 UI 中。

### 严重等级

`medium`。问题影响管理后台核心列表展示质量，但不阻断品牌搜索、编辑、上下架等主流程。

## 根因分析

根因分类：`code / ui / media-rendering`。

直接原因是品牌列表 Logo 字段被当作普通文本渲染，没有使用图片或缩略图组件，也没有覆盖未上传、加载失败和无效 URL 的展示状态。

根本原因是品牌列表展示契约没有把“Logo 列必须按媒体资源渲染”作为明确回归门槛，导致字段映射或列配置沿用文本渲染路径。

## 修复方案

1. 检查管理后台品牌列表列配置，确认 Logo 列使用图片渲染组件。
2. 优先使用 `thumbnail_url`；若不可用则使用 `logo_url` 或等价受控预览 URL。
3. 未上传 Logo 时显示设计系统内稳定占位。
4. 图片加载失败时显示 fallback，占位不得暴露对象 key、存储路径、文件名或调试文案。
5. 保持品牌名称、搜索、编辑、上下架、分页等既有交互不变。
6. 实现时确认是否需要 API 字段变更：
   - 若后端已返回可展示字段，仅做 Web 展示修复和前端测试。
   - 若后端字段缺失或命名不一致，则同步 API Schema、OpenAPI、Orval、API 文档和后端测试。

## 数据与 API

- 默认不新增 SQLite/MySQL 表或字段。
- 默认不调整对象存储 key 策略。
- 默认不新增 API 端点。
- 若 `GET /api/v1/admin/brands` 已提供 `logo_url`、`thumbnail_url` 或等价预览 URL，则无需 Orval。
- 若实现确认响应 Schema 缺少必要字段，则该 Change 的实现任务必须同步 Orval 和 API 文档。

## 测试

- Web 单元/组件测试：已上传 Logo 显示图片；未上传显示占位；加载失败显示 fallback。
- Web 回归测试：品牌搜索、编辑入口、上下架或列表操作不回归。
- API 契约测试：仅当后端字段契约变化时补充。
- 静态检查：确保 Logo 列不直接渲染对象 key、文件名、URL 字符串或调试文案。

## 风险

| 风险 | 缓解 |
|---|---|
| 字段映射错误导致图片仍不显示 | 测试覆盖 `thumbnail_url`、`logo_url` 和缺失字段 |
| 图片加载失败导致布局跳动 | 固定 Logo 单元尺寸与 fallback 状态 |
| API 契约被误改 | 默认不改 API；若修改则同步 Orval/docs/tests |
| 安全信息泄露 | fallback 不展示对象 key、内部路径或错误堆栈 |
