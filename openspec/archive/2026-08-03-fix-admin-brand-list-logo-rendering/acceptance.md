---
change_id: fix-admin-brand-list-logo-rendering
type: fix
status: applied
source_bug: BUG-0105-admin-brand-list-logo-renders-text
acceptance_status: passed
created_at: 2026-08-03 08:33:03
updated_at: 2026-08-03 12:49:26
---

# 验收记录

本 Change 继承 `BUG-0105-admin-brand-list-logo-renders-text` 的验收标准。

| AC | 验收点 | 状态 |
|---|---|---|
| AC-001 | 已上传 Logo 的品牌在列表第一列显示图片或缩略图，不显示 URL/key/文件名文本 | passed |
| AC-002 | 未上传 Logo 的品牌显示合理占位 | passed |
| AC-003 | 图片加载失败时显示稳定 fallback，不暴露内部路径或异常 | passed |
| AC-004 | Logo 列布局稳定，不挤压其他列或造成表格跳动 | passed |
| AC-005 | 品牌搜索、编辑、上下架等既有操作不回归 | passed |
| AC-006 | API 字段契约已验证；如变更则同步 OpenAPI/Orval/docs/tests | passed |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: "2026-08-03 12:49:26"
accepted_by: codex
evidence:
  - command: "pnpm --dir src/web exec vitest run src/pages/admin/BrandManagementPage.test.tsx"
    result: "1 file / 9 tests passed"
  - files:
      - src/web/src/features/admin/lib/brand-display.ts
      - src/web/src/pages/admin/BrandManagementPage.tsx
      - src/web/src/pages/admin/BrandManagementPage.test.tsx
    result: "Logo 列按 thumbnail_url/logo_url 渲染图片，未上传和加载失败使用占位，不展示 URL/key 文本。"
failed_items: []
source_event: opsx.archive
notes: "本修复仅调整 Web 管理后台品牌列表展示逻辑，不修改 API Schema、数据库、对象存储策略、Orval 或 Docker Compose；长期 docs 不需要更新。"
```
