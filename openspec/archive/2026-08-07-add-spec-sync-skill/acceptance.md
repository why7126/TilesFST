---
created_at: 2026-08-07 09:06:21
updated_at: 2026-08-07 09:20:34
change_id: add-spec-sync-skill
acceptance_status: passed
---

# 验收记录

## 验收要点

- [x] `/spec-sync` 技能说明覆盖本地项目与 GitHub URL 两类学习对象。
- [x] `/spec-sync` 技能说明覆盖自动学习与指定学习内容两类模式。
- [x] 学习阶段必须先输出候选学习内容并等待用户确认。
- [x] 学习对象必须全程只读，绝不允许改动学习对象代码、文档、配置或仓库状态。
- [x] 应用阶段禁止修改 `src/`。
- [x] 应用完成后必须输出学习报告。
- [x] 当前 Sprint 使用规范编号 `sprint-022`，自动编号规则已同步到 Sprint 规范和技能。

## 验证结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate add-spec-sync-skill`：通过。
