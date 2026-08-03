---
review_id: REV-REQ-0094-001
requirement_id: REQ-0094-mintlify-versioned-docs-directory
date: 2026-08-03
reviewed_at: 2026-08-03 18:38:56
participants:
  - product
  - ai
result: approved
created_at: 2026-08-03 18:38:56
updated_at: 2026-08-03 18:38:56
---

# REQ-0094 评审记录

## 评审结论

评审通过。

本需求范围清晰：以方案 B 为主线，新增 `mintlify/` 文档站源目录，保留 `releases/vX.Y.Z/usage-docs/` 作为发布事实源和版本快照，并通过站点投影、多版本导航、共享截图资产、`latest` 指针和 Docker Compose 可选文档站服务形成完整治理闭环。

本需求不涉及业务 UI 原型，不新增后端 API 或数据库表；后续实现前必须通过 OpenSpec Change 更新目录边界、发布文档治理、Docker Compose、端口环境变量和校验脚本。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖目录、manifest、站点同步、共享截图、Compose profile、端口和发布门禁。
- [x] 优先级与依赖合理，作为 REQ-0088 的增强需求成立。
- [x] UI 类原型不适用，本需求为文档站 / 发布 / 部署治理。
- [x] 与现有 REQ 不重复：REQ-0088 已完成 release usage docs 快照治理，REQ-0094 扩展站点源目录与部署承载。

## 条件通过项

- [ ] 后续 `/req-opsx` 必须明确 `mintlify/` 一级目录边界，并更新 `AGENTS.md`、`rules/directory-structure.md` 和目录校验脚本。
- [ ] 后续实现 Docker Compose 文档站服务时，必须使用 `docs-site` 或等价 profile，不得让默认部署无条件启动 Mintlify 服务。
- [ ] 新增端口和环境变量必须同步 `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md`。
- [ ] 若发布范围包含 Compose / Dockerfile / 文档站服务部署变更，必须执行 Docker Compose 验证，并按发布规范判断是否需要 `/image-prepare` 与 `/image-build`。

## 下一步

```text
/req-opsx REQ-0094-mintlify-versioned-docs-directory
/sprint-propose（评审通过后可纳入 Sprint）
```
