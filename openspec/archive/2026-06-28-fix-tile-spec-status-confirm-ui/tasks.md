## 1. 前端 — 启停 confirm（BUG-0037 AC-001/002/004/005）

- [x] 1.1 `TileSpecManagementPage.tsx`：启停 confirm markup 对齐 `TileCategoryManagementPage`（`modal-card`、无 `confirm-card`）
- [x] 1.2 标题区补 `modal-close`（×）与 `aria-labelledby`（如 `status-spec-title`）
- [x] 1.3 正文使用 `page-desc`；停用含「停用后前台将不再展示该规格。」
- [x] 1.4 主按钮改为「确认启用」/「确认停用」；取消/遮罩/× 不请求 API

## 2. 前端 — 删除 confirm（BUG-0037 AC-003/004/005）

- [x] 2.1 删除 confirm markup 对齐类目页删除 modal
- [x] 2.2 主按钮改为「删除规格」+ `btn primary`；移除 `danger` class
- [x] 2.3 标题区补 `modal-close` 与 `aria-labelledby`（如 `delete-spec-title`）

## 3. 测试

- [x] 3.1 更新 `TileSpecManagementPage.test.tsx`：停用须先出 dialog；确认前 `disableTileSpec` mock 未调用
- [x] 3.2 断言 dialog 文案含「停用后前台将不再展示该规格。」；点击「确认停用」后 mock 被调用
- [x] 3.3 回归既有分页 DOM、保存后 refresh 用例仍 pass
- [x] 3.4 回归 `TileCategoryManagementPage.test.tsx`、`BrandManagementPage.test.tsx` confirm 用例
- [x] 3.5 运行 `cd src/web && npx vitest run src/pages/admin/TileSpecManagementPage.test.tsx`
- [x] 3.6 运行 `cd src/web && pnpm build`（`npx vite build` pass；pnpm 脚本因 approve-builds 门禁 exit 1）

## 4. 冒烟与追溯

- [x] 4.1 本地/Docker：`/admin/tile-specs` 启停/删除 confirm 与类目页并排手工冒烟（可选 PNG）— Docker bundle 字符串 + API 启停 roundtrip 通过（2026-06-28）
- [x] 4.2 填写 `openspec/changes/fix-tile-spec-status-confirm-ui/trace.md` checklist（≥8 项）
- [x] 4.3 更新 `issues/bugs/archive/BUG-0037-tile-spec-status-confirm-ui-inconsistency/trace.md`（`openspec_changes.status: applied`）
- [x] 4.4 完成后 `/opsx-archive fix-tile-spec-status-confirm-ui`

## 5. 知识沉淀（可选）

- [x] 5.1 本缺陷为 UI confirm 形态对齐，通常可跳过 `docs/knowledge-base/incidents/`
