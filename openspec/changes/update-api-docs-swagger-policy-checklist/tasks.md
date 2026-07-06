# Tasks

- [ ] 同步 `admin-api-docs`、`web-client`、`deployment`、`testing` delta specs，固化 Swagger Web 代理与生产 `Try It Out` checklist。
- [ ] 更新或确认 `docs/03-api-index.md` 是否需要补充接口文档页同源 Swagger 入口、生产只读策略与 Web 代理说明。
- [ ] 更新或确认 `docs/standards/api-governance.md` 是否需要补充 API docs refine / Swagger / Orval checklist。
- [ ] 在实现 trace 或验收记录中记录 Vite dev proxy、Docker Nginx、生产等价代理策略；无法自动化时标注人工 smoke。
- [ ] 确认本 Change 未新增 API contract、未修改数据库、未引入 Orval 生成需求。
- [ ] 运行 `openspec validate update-api-docs-swagger-policy-checklist --strict`。
- [ ] 运行 `python scripts/validate-directory-structure.py`。
- [ ] 更新 REQ-0030 trace、Sprint 005 范围与验收记录，闭环 Sprint 004 A-006。
