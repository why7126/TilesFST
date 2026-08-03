---
change_id: fix-admin-certificate-list-main-image-name-only
source_bug: BUG-0107-admin-certificate-list-main-image-name-only
created_at: 2026-08-03 08:33:06
updated_at: 2026-08-03 08:33:06
---

# Tasks

- [x] 1. 定位管理后台品牌证书列表证书字段渲染逻辑，确认是否复用上传组件或文件名展示 helper。
- [x] 2. 调整证书字段 UI，使列表仅展示证书主图或占位，以及证书名称。
- [x] 3. 移除列表证书字段中的图片名称、文件名称、对象 key、原始 URL 和上传组件内部文案展示。
- [x] 4. 保持无主图占位、证书名称、筛选、分页、排序和编辑入口不回归。
- [x] 5. 补充或更新 Web 管理端回归测试，覆盖 AC-0107-001 到 AC-0107-005。
- [x] 6. 运行相关前端测试，至少覆盖品牌证书管理页或组件测试。
- [x] 7. 评估修复后是否有复用价值；如形成管理端媒体列表展示经验，更新 `docs/knowledge-base/incidents/` 或说明不适用。

## 知识库决策

本修复复用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 的既有模式：管理端媒体列表只展示业务图片/占位和业务名称，不暴露文件名、对象 key、原始 URL 或上传内部文案。当前未发现新的事故模式，暂不新增 `docs/knowledge-base/incidents/`。
