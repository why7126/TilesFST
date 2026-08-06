---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
review_result: approved
reviewed_at: 2026-08-06 11:05:55
reviewed_by: AI
created_at: 2026-08-06 11:05:55
updated_at: 2026-08-06 11:05:55
---

# 缺陷评审

## 评审结论

确认修复。该问题属于 Docker Compose docs-site profile 的运行时配置缺陷，根因清晰，复现路径明确，修复范围集中在文档站服务缓存挂载、部署文档和测试断言。

## 评审清单

- [x] 可复现或根因充分：Mintlify CLI 重命名 `/home/node/.mintlify` 时与 Docker named volume 挂载点冲突，导致 `EBUSY`。
- [x] 严重等级合理：`medium`，不影响核心业务服务，但阻断文档站预览和发布验收链路。
- [x] 回归验收明确：acceptance.md 已覆盖移除冲突挂载、docs-site 启动、部署文档同步和目录结构测试。
- [x] hotfix 路径判断：不需要 hotfix；若当前发布必须依赖 docs-site 验收，可在 Sprint 中优先纳入。

## 后续动作

- 可执行 `/bug-opsx BUG-0120-docs-site-mintlify-cache-ebusy` 创建修复 Change。
- 若该 BUG 来源于正式修复流程，`/opsx-apply` 前必须先纳入 Sprint 正式范围。
