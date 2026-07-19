## 1. 规范与技能

- [x] 1.1 更新 `rules/issues-lifecycle.md`，区分单 Issue 归档与 Sprint 整体归档门禁。
- [x] 1.2 更新 `.agents/skills/workflow-sync/SKILL.md`，说明 reconcile 不因所属 Sprint 未 completed 阻断。
- [x] 1.3 更新 `.agents/skills/opsx-archive/SKILL.md`，说明 `/opsx-archive <change-id>` 后 issue promote 可在 Sprint 未完成时执行。

## 2. 脚本与测试

- [x] 2.1 修改 `scripts/workflow_sync/issue_status_residuals.py`，移除单 Issue reconcile 对 Sprint completed 的依赖。
- [x] 2.2 补充 `tests/test_issue_status_residuals.py`，覆盖 closed issue + archived change + incomplete sprint 仍可 reconcile。
- [x] 2.3 保留未闭环 issue / 未 archived change 的 blocker 测试。

## 3. 验证与当前阻塞修复

- [x] 3.1 运行 focused tests。
- [x] 3.2 运行 OpenSpec 校验。
- [x] 3.3 对 `REQ-0039-xl-admin-page-layered-acceptance-template` 重跑 residual reconcile 与 promote，确认 Sprint 未 completed 时可归档单 Issue。
- [x] 3.4 记录不影响 API、DB、Orval、Docker Compose、Web、小程序运行时代码。
