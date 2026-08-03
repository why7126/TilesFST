## 1. 文档与最佳实践

- [x] 1.1 更新 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，将管理端筛选下拉统一 gate 明确为 apply 前必读项。
- [x] 1.2 在最佳实践中补充 apply checklist：共享组件复用、页面级弹层样式禁止、状态覆盖、窄屏和弹层不裁切、筛选语义不变。

## 2. Apply Gate

- [x] 2.1 更新 `.agents/skills/opsx-apply/SKILL.md` 的 Cross-cutting Apply Gate，新增 `admin-filter-dropdown` 标签触发条件和引用文档。
- [x] 2.2 在 `/opsx-apply` checklist 输出中增加 best-practice read、shared component reuse、overlay clipping、query semantics 和 regression test plan 结果。
- [x] 2.3 明确未命中管理端筛选下拉的 Change 可标记 `n/a`，避免阻断后端、数据库、发布或非筛选 UI 变更。

## 3. 测试与验证

- [x] 3.1 补充或更新测试，验证 `opsx-apply` skill 或相关治理文档包含 `admin-filter-dropdown` gate 与必需检查项。
- [x] 3.2 补充或更新前端共享组件/代表页面测试，确保普通下拉、可搜索下拉、空态、加载态、禁用态、已选中态、清空/重置和 DOM 类名契约被覆盖。
- [x] 3.3 如实现触及页面 CSS 或弹层定位，补充桌面和窄屏视觉 smoke 或 Playwright 检查说明。

## 4. 收尾校验

- [x] 4.1 运行 `openspec validate standardize-admin-filter-dropdown-gate --strict`。
- [x] 4.2 运行相关 Vitest 或治理 pytest，确认 gate 文档和管理端筛选下拉测试通过。
- [x] 4.3 复核不影响 API、数据库、Orval、小程序、媒体上传和 Docker Compose，并在完成输出中说明。

## 归档验证摘要

- 验证命令与结果：`openspec validate standardize-admin-filter-dropdown-gate --strict` 通过；`pnpm --dir src/web test src/shared/ui/admin-filter-select.test.tsx src/shared/ui/searchable-select.test.tsx` 通过；`uv run pytest tests/test_opsx_apply_admin_filter_gate.py` 通过；`python scripts/validate-agent-context-budget.py` 通过。
- 验收结论：管理端筛选下拉统一 gate 已进入最佳实践与 `/opsx-apply` checklist，OpenSpec delta spec、技能文档、最佳实践文档和测试均已补齐。
- 关联 Issue 或 Sprint 状态：本 Change 为纯技术治理 Change，无 `source_requirement`、`source_bug` 或 Sprint scope；Workflow Sync 在 propose/apply 阶段均报告 Sprint skipped/no-sprint。
- 归档路径与时间：预期归档到 `openspec/archive/2026-08-01-standardize-admin-filter-dropdown-gate/`，归档命令执行时间为 2026-08-01 00:00:00 Asia/Shanghai。
