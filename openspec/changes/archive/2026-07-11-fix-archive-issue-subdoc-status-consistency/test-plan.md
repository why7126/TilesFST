# Test Plan

## Automated

- `pytest tests/test_promote_issues_for_archive.py`
  - 覆盖 BUG 子文档 frontmatter residual 阻断。
  - 覆盖 REQ 子文档 fenced YAML block residual 阻断。
  - 覆盖无 residual 时 promote 成功。
  - 覆盖阻断报告包含路径与状态值。

- `python scripts/sync-workflow-status.py --sprint auto --check`
  - 验证 workflow-sync 派生文档没有漂移。

- `openspec validate fix-archive-issue-subdoc-status-consistency --strict`
  - 验证 OpenSpec Change 结构与 delta spec。

## Manual

- 对一个真实待归档 issue 包手工保留 `status: pending_review`，确认归档流程阻断。
- 修正该状态后再次执行 promote，确认允许迁入 `archive/`。

## Not Required

- 不需要 Docker Compose 验证。
- 不需要 Orval 生成。
- 不需要 Web / 小程序 UI 回归。
