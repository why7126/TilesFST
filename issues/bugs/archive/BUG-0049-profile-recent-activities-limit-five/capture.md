---
bug_id: BUG-0049-profile-recent-activities-limit-five
status: rejected
created_at: 2026-06-28 18:48:41
updated_at: 2026-06-28 19:11:39
severity_hint: medium
environment: local|docker
related_requirement: REQ-0014-profile-page
related_bug:
captured_via: capture
classification_rationale: 初判为规范未达标；explore 后确认为产品策略调整（20→5），改走 REQ-0014 修订而非 BUG 链
rejection_rationale: 非缺陷；已转 REQ-0014 v1.1 修订并由 fix-profile-activities-display-limit 交付归档
superseded_by: REQ-0014-profile-page v1.1
related_change: fix-profile-activities-display-limit
---

# 现象（已作废 — 初 capture 方向错误）

初 capture 误以为「仅显示 5 条」为实现缺陷。`/bug-explore` 澄清：用户期望 **最多展示 5 条**（20 条过多），属需求修订。

# 处置

- **status**: `rejected` → 已归档至 `issues/bugs/archive/`
- **闭环**: REQ-0014 v1.1 + `fix-profile-activities-display-limit`（archived 2026-06-28）

# 附件

- screenshots/
- logs/
