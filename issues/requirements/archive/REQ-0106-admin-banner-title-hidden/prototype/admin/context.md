---
requirement_id: REQ-0106-admin-banner-title-hidden
surface: web-admin
status: pending_review
created_at: 2026-08-10 22:40:54
updated_at: 2026-08-10 22:40:54
---

# Admin Prototype Context

## 页面

- 路由：`/admin/banners`
- 组件：Banner 管理列表、新增/编辑 Banner 弹窗。

## 交互策略

- 弹窗移除“Banner 标题”字段。
- 原首行标题字段移除后，展示端/展示位置/图片区域自然上移，保持现有表单网格间距。
- 保存按钮仍为“保存 Banner”。
- 错误区域不得出现标题必填、标题重复等运营可见提示。
- 列表第一列以 Banner 缩略图为主，辅以展示位置、跳转类型或目标信息；标题如保留仅作为内部识别名。

## 待后续实现确认

- 内部标题由前端生成还是后端生成。
- 列表第一列最终识别组合：缩略图 + 展示位置、缩略图 + 跳转目标，或缩略图 + 内部识别名。
- 是否调整关键词搜索 placeholder。

## PNG

待实现阶段或设计阶段导出。
