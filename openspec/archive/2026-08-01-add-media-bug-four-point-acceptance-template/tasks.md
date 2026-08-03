## 1. 文档落点

- [x] 1.1 确认媒体类 BUG 四联验收模板最终落点，优先评估 `rules/media.md`、`rules/object-storage.md`、`docs/standards`、`docs/knowledge-base` 和 BUG acceptance 模板职责。
- [x] 1.2 在选定落点新增四联验收模板，覆盖原 BUG 场景、`key`、`object`、`URL`、`render`、状态、证据和失败/阻塞处理。
- [x] 1.3 将 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 的上传状态机、同会话即时回显、Docker Web `:3000` 边界文件和媒体代理一致性转化为模板检查项。
- [x] 1.4 引用 Sprint 015/016 复盘中的媒体链路经验，明确小程序 evidence、历史对象、缩略图、回填和审计脚本的补证要求。

## 2. 工作流集成

- [x] 2.1 明确哪些媒体类 BUG 必须触发四联验收，哪些非媒体 BUG 可标记为 N/A。
- [x] 2.2 明确四联验收如何嵌入 BUG `acceptance.md`、Sprint `acceptance-report.md` 或 Release 检查清单，且不得手工编辑 Workflow Sync 管辖的 Scope marker 块。
- [x] 2.3 如更新 `.agents/skills/bug-*` 或模板说明，确保新增规则不会自动创建 follow-up Issue，不泄露 session 或本机路径。
- [x] 2.4 与 `REQ-0090-media-five-point-acceptance-template` 保持互相引用，说明通用五联和 BUG 四联的适用差异。

## 3. 验证

- [x] 3.1 运行 `openspec validate add-media-bug-four-point-acceptance-template --strict`。
- [x] 3.2 如仅修改 Markdown/rules/skills，运行对应文档或目录结构校验；若无自动校验，记录人工复核项。
- [x] 3.3 如新增脚本、自动化检查、API、DB、Web UI 或小程序能力，补充对应 pytest/Vitest/静态校验、OpenAPI/Orval、数据库文档或 Docker Compose 验证。
- [x] 3.4 在 trace 或实施记录中明确 API、数据库、Web、小程序、管理端、Orval、Docker Compose 和测试是否适用。

## 4. 归档准备

- [x] 4.1 同步受影响 docs/rules 的 `updated_at`，保持 `YYYY-MM-DD HH:mm:ss`。
- [x] 4.2 在归档前确认 `REQ-0091` trace 中 `openspec_changes` 状态已由 Workflow Sync 刷新。
- [x] 4.3 归档前复核不存在 `openspec/changes/archive/` 真实目录或新生成 canonical 引用。
