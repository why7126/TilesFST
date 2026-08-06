---
req_id: REQ-0102-sprint-goal-scope-consistency-validation
status: archived
created_at: 2026-08-06 11:14:12
updated_at: 2026-08-06 13:08:31
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement:
---

# Sprint 目标编号列表与 Scope 一致性校验

# 原始描述

背景：sprint-020 Scope 包含 REQ-0100，但 sprint.md 目标编号列表未列出，可能影响人读理解。

影响范围：/sprint-propose、Workflow Sync、validate-sprint-scope.py、Sprint 四件套。

建议验收或复现要点：新增或同步 Sprint Scope 后，目标编号列表与 Scope 主表应一致；校验失败应提示具体缺失项。

# 待澄清

- [ ] 是否仅校验需求编号，还是 BUG / Change 编号列表也需要纳入一致性检查。
- [ ] `/sprint-propose` 与 Workflow Sync 谁作为目标编号列表的事实写入方。

# 探索结论

（/req-explore 后人工确认写入）
