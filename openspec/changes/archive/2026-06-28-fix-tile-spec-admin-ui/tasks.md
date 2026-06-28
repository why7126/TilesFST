## 1. 准备与定位

- [x] 1.1 阅读 BUG-0027、BUG-0028、BUG-0029 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `TileSpecManagementPage.tsx`、`TileSpecFormModal.tsx`、`UserManagementPage.tsx`、`BrandManagementPage.tsx`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO、Docker compose 变更

## 2. 前端修复（BUG-0027 — 列表分页与字号）

- [x] 2.1 将 `TileSpecManagementPage.tsx` 分页 DOM 替换为 `pagination` + `page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- [x] 2.2 删除 `pagination-bar`、`pagination-left`、`pagination-right`、`page-indicator`
- [x] 2.3 每页条数选项改为「20 条 / 50 条 / 100 条」，含「每页显示」标签与 `aria-label`
- [x] 2.4 调整 `tile-spec-management.css` 中 `.size-name` 字号/字色，与同表列 rhythm 协调
- [x] 2.5 加载态分页 summary 可显示「…」（对齐用户管理页 optional 模式）

## 3. 前端修复（BUG-0028 — 弹窗布局）

- [x] 3.1 重排 `TileSpecFormModal.tsx`：宽/长 → 只读尺寸名称（form-full）→ 厚度/排序 → 备注（form-full）
- [x] 3.2 在 `.tile-spec-form-grid` 作用域 port `.input`、`.textarea` → `width: 100%`
- [x] 3.3 备注 `textarea`：固定高度（对齐 prototype ~112px）、`resize: none`、semantic token 边框/背景
- [x] 3.4 **不要**修改 `buildDisplayName()` 或去掉 `mm` 后缀
- [x] 3.5 （可选）AC-021 宽长冲突 inline 提示 — 若本 sprint 不做，在 trace 标注延后

## 4. 前端修复（BUG-0029 — 保存后刷新）

- [x] 4.1 将 `TileSpecFormModal` 的 `onSuccess` 改为 `(message) => { setNotice(message); void loadSpecs(); }`
- [x] 4.2 验证新增后列表 + summary 即时更新；编辑后行内数据同步
- [x] 4.3 验证启停/删除 refresh 无回归；筛选场景符合 AC-006

## 5. 测试

- [x] 5.1 SHOULD：`TileSpecManagementPage.test.tsx` — 分页含 `.pagination`/`.page-buttons`，不含 `pagination-bar`
- [x] 5.2 SHOULD：`TileSpecFormModal.test.tsx` — 字段 DOM 顺序；备注 textarea 在 `.form-full` 内
- [x] 5.3 SHOULD：mock `fetchTileSpecs`，保存 success 后断言 `loadSpecs` / fetch 再次调用
- [x] 5.4 运行 `cd src/web && pnpm vitest run`（相关用例）与 `pnpm build`

## 6. 验收与追溯

- [x] 6.1 并排 BUG-0027：规格列表 vs 用户管理分页（1440×1024）
- [x] 6.2 并排 BUG-0028：弹窗 vs `tile-size-management-modal.html`
- [x] 6.3 手工 BUG-0029：新增/编辑保存无需 F5
- [x] 6.4 勾选 BUG-0027 acceptance AC-001～AC-009
- [x] 6.5 勾选 BUG-0028 acceptance AC-001～AC-009（AC-010 若延后单独注明）
- [x] 6.6 勾选 BUG-0029 acceptance AC-001～AC-008
- [x] 6.7 填写本 change `trace.md`；更新 `add-tile-spec-management/trace.md` checklist 第 2、7 项
- [x] 6.8 更新 BUG-0027/0028/0029 `trace.md` 中 `openspec_changes`（apply 后 → applied）
- [x] 6.9 评估 `docs/knowledge-base/incidents/`（UI 一致性缺陷，通常不需要）

## 7. 归档准备

- [x] 7.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-tile-spec-admin-ui`
- [x] 7.2 归档前确认 `add-tile-spec-management` 已 archive 或 delta 合并顺序无冲突
