---
created_at: 2026-08-30 12:45:20
updated_at: 2026-08-30 12:55:22
status: applied
sprint: sprint-028
---

# Trace

```yaml
change_id: enforce-environment-tiered-evidence-gates
source_command: /spec-opt
source_type: governance
status: applied
sprint: sprint-028
product_data_collection_observability:
  applicability: not_applicable
  affected_layers: []
  reason: "纯治理脚本、规则和测试变更；不修改运行时代码、API、DB、日志或端侧请求封装。"
  validation: "环境分层证据脚本、聚焦 pytest、OpenSpec 语言、目录结构和 Sprint scope 校验通过。"
implementation:
  scripts:
    - scripts/environment_tiered_evidence.py
    - scripts/validate-environment-tiered-evidence.py
    - scripts/validate-archive-evidence.py
    - scripts/validate-sprint-archive-readiness.py
    - scripts/validate-release.py
  command_skills:
    - .agents/skills/opsx-archive/SKILL.md
    - .agents/skills/sprint-archive/SKILL.md
    - .agents/skills/release-status/SKILL.md
    - .agents/skills/release-publish/SKILL.md
validation:
  - command: python scripts/validate-environment-tiered-evidence.py --change enforce-environment-tiered-evidence-gates
    result: pass
  - command: python scripts/validate-environment-tiered-evidence.py --sprint sprint-028
    result: pass
  - command: uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_sprint_archive_readiness.py::test_environment_evidence_blocker_blocks_sprint_archive_readiness tests/test_release_validation.py::test_release_status_reclassifies_production_only_pending_for_production_target tests/test_release_validation.py::test_release_status_keeps_production_followups_non_blocking_for_development
    result: pass
    summary: "8 passed"
  - command: uv run pytest tests/test_environment_tiered_evidence_validation.py tests/test_sprint_archive_readiness.py tests/test_release_validation.py
    result: failed_unrelated
    summary: "47 passed, 3 failed；失败来自既有 usage-docs screenshot fixture 规则漂移，不属于本次环境分层 evidence 门禁。"
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-30 12:45:20 | /spec-opt | 创建环境证据强脚本门禁治理 Change。 |
| 2026-08-30 12:55:22 | /spec-opt | 完成脚本、归档/发布 validator 接入、规则/Skill 同步和聚焦测试。 |
