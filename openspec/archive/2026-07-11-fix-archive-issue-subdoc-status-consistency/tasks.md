# Tasks

- [x] 抽取或新增 issue 子文档状态 residual 扫描能力，覆盖 frontmatter 与 fenced YAML block。
- [x] 在 `scripts/promote-issues-for-archive.py` 的 archive promote 候选检查中加入 residual blocker。
- [x] 输出可操作阻断报告，包含 issue id、文件路径、状态来源、状态值和处理建议。
- [x] 更新 `/opsx-archive` 与 `/sprint-archive` 技能说明，明确归档前必须通过 issue 子文档状态一致性门禁。
- [x] 新增 pytest：BUG 子文档 frontmatter residual 阻断。
- [x] 新增 pytest：REQ 子文档 fenced YAML block residual 阻断。
- [x] 新增 pytest：无 residual 时 promote 成功。
- [x] 新增 pytest：阻断报告包含具体路径与状态值。
- [x] 运行相关 pytest 与 OpenSpec 校验。
- [x] 评估是否需要将经验沉淀到 `docs/knowledge-base/incidents/`。

## 实现记录

- 新增 `scripts/workflow_sync/issue_status_residuals.py` 作为共享扫描能力；当前经验以脚本测试与归档技能说明承接，暂不新增 incident 文档。
- 已运行 `uv run pytest tests/test_issue_status_residuals.py tests/test_generate_sprint_fact_sheet.py`。
- 已运行 `openspec validate fix-archive-issue-subdoc-status-consistency --strict`。
