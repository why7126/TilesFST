## 1. 实现

- [x] 1.1 定位管理后台品牌编辑弹窗 Logo 上传/预览区域的成功态文案来源。
- [x] 1.2 移除已有 Logo 回显和上传成功后稳定状态中的 `已上传Logo` 冗余文案。
- [x] 1.3 保留 Logo 预览、替换、删除或重新上传交互。
- [x] 1.4 保留上传中、上传失败、格式不支持等必要状态反馈。

## 2. 验证

- [x] 2.1 回归验证已有 Logo 的品牌编辑弹窗不再显示 `已上传Logo`。
- [x] 2.2 回归验证已有 Logo 图片仍正常预览且布局不跳动。
- [x] 2.3 回归验证替换、删除或重新上传 Logo 交互保持正常。
- [x] 2.4 回归验证上传失败、格式不支持等错误提示仍可见。
- [x] 2.5 运行或补充相关前端测试。
- [x] 2.6 运行 `openspec validate fix-admin-brand-edit-logo-uploaded-text --strict`。

## 3. 文档

- [x] 3.1 确认本修复不需要更新 API、数据库、Orval、MinIO 或 Docker 文档。
- [x] 3.2 如修复发现可复用的上传状态展示经验，评估是否沉淀到 `docs/knowledge-base/incidents/`。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-03 09:11:20 | 品牌 Logo 区域不显示 `品牌Logo` 这 4 个字的文案 | 将字段可见标签收敛为 `Logo`，移除 Logo 区域旁的中性 `品牌 Logo` 文案；同步更新 BUG acceptance 与 brand-management delta spec | `pnpm --dir src/web test src/features/admin/components/BrandFormModal.test.tsx` 通过；`openspec validate fix-admin-brand-edit-logo-uploaded-text --strict` 通过 |
| 2026-08-03 11:29:03 | 品牌 Logo 图片顶部与格式提示文字顶部对齐，避免图片顶部超出文字顶部 | 将 `.brand-logo-preview` 增加 2px 顶部偏移，保持 `.brand-logo-meta` 顶部对齐；补充 CSS 规则回归测试并同步 BUG acceptance 与 brand-management delta spec | `pnpm --dir src/web test src/features/admin/components/BrandFormModal.test.tsx` 通过；`openspec validate fix-admin-brand-edit-logo-uploaded-text --strict` 通过 |
| 2026-08-03 11:30:07 | 截图验收确认 2px 偏移仍未实现顶部视觉对齐 | 将 `.brand-logo-preview` 顶部偏移调整为 14px，使 Logo 图片顶部贴近格式提示文字实际字面顶部；同步 CSS 回归测试 | `pnpm --dir src/web test src/features/admin/components/BrandFormModal.test.tsx` 通过；`openspec validate fix-admin-brand-edit-logo-uploaded-text --strict` 通过 |
| 2026-08-03 11:59:17 | 截图验收确认 14px 偏移过冲，文字顶部超过图片顶部 | 将 `.brand-logo-preview` 顶部偏移回调为 8px，在 2px 与 14px 之间校准视觉顶部对齐；同步 CSS 回归测试 | `pnpm --dir src/web test src/features/admin/components/BrandFormModal.test.tsx` 通过；`openspec validate fix-admin-brand-edit-logo-uploaded-text --strict` 通过 |

## 归档验证摘要

- 归档时间：2026-08-03 12:50:06
- 归档对象：`fix-admin-brand-edit-logo-uploaded-text`
- 来源缺陷：`BUG-0106-admin-brand-edit-logo-uploaded-text`
- Sprint：`sprint-018`
- 规格同步：`brand-management` / `MODIFIED` / `品牌 Logo 上传`
- 实现摘要：移除品牌编辑弹窗 Logo 区域冗余成功态文案；保留 Logo 预览、替换、上传中、上传失败和格式提示；将 Logo 预览图与格式提示文字做顶部视觉对齐。
- 验证证据：
  - `pnpm --dir src/web test src/features/admin/components/BrandFormModal.test.tsx` 通过，5 tests passed
  - `openspec validate fix-admin-brand-edit-logo-uploaded-text --strict` 通过
  - `git diff --check` 通过
- 文档同步：BUG acceptance 与 active Change delta spec 已同步；本修复不涉及 API、数据库、Orval、MinIO、Docker 或长期部署文档更新。
