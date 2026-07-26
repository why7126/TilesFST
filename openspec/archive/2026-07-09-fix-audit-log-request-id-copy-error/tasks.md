# Tasks

- [x] 确认日志审计页当前 `request_id` 复制函数与 `AdminToast` 使用方式，避免改动列表、筛选、分页和详情抽屉主流程。
- [x] 修复复制函数，检查 `navigator.clipboard?.writeText` 可用性，并在成功路径写入完整 `request_id`。
- [x] 为 Clipboard API 不存在或 `writeText` 失败路径提供手动复制兜底或等价明确提示。
- [x] 保持成功、失败和兜底反馈使用 fixed toast 或等价固定层，不造成页面布局位移。
- [x] 确保成功复制才上报 `copy_request_id`；失败或兜底路径不得误报成功复制。
- [x] 补充 `LogAuditPage.test.tsx` 回归测试：成功复制、Clipboard API 不存在、`writeText` reject、空 `request_id` 防御。
- [x] 运行 `pnpm --dir src/web test src/pages/admin/LogAuditPage.test.tsx`。
- [x] 运行 `openspec validate fix-audit-log-request-id-copy-error --strict`。
- [x] 更新 BUG-0060 trace 与验收记录；如修复经验可复用，评估是否沉淀到 `docs/knowledge-base/incidents/`。
