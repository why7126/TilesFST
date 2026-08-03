---
change_id: fix-admin-brand-list-logo-rendering
type: fix
status: applied
source_bug: BUG-0105-admin-brand-list-logo-renders-text
created_at: 2026-08-03 08:33:03
updated_at: 2026-08-03 12:49:26
---

# 任务清单

- [x] 1. 确认管理后台品牌列表 Logo 列当前字段来源和渲染路径。
- [x] 2. 修复 Logo 列渲染：已上传 Logo 显示图片或缩略图，优先使用 `thumbnail_url`。
- [x] 3. 补齐未上传 Logo、加载失败、无效 URL 的稳定占位状态。
- [x] 4. 回归品牌搜索、编辑入口、上下架、分页等品牌列表既有操作。
- [x] 5. 补充 Web 测试，覆盖已上传 Logo、未上传 Logo、加载失败 fallback 和“不显示文本 URL/key”。
- [x] 6. 若实现触及 API Schema，补充后端/API 测试并同步 OpenAPI、Orval 与 API 文档；若未触及，记录无需 Orval。
- [x] 7. 按 `issues/bugs/archive/BUG-0105-admin-brand-list-logo-renders-text/acceptance.md` AC-001 至 AC-006 回归验收。
- [x] 8. 评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，记录不适用原因。
