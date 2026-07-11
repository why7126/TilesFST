# Acceptance

## 验收门禁

- [ ] 待归档 BUG 包内 `bug.md` frontmatter 存在 `status: draft` 时，promote 阻断并返回非零退出码。
- [ ] 待归档 REQ 包内 fenced YAML block 存在 `status: in_sprint` 时，promote 阻断并返回非零退出码。
- [ ] 阻断报告包含 issue id、文件路径、状态来源、状态值和处理建议。
- [ ] 子文档状态均为闭环状态或无状态字段时，promote 允许执行。
- [ ] `trace.md` / registry / workflow-sync 既有状态同步行为不回归。

## 非目标验收

- [ ] 未修改业务 API 或 OpenAPI / Orval 生成物。
- [ ] 未修改数据库 schema。
- [ ] 未批量改写历史 archive issue 包。
