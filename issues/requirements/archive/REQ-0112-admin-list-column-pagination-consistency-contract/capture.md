---
req_id: REQ-0112-admin-list-column-pagination-consistency-contract
status: archived
created_at: 2026-08-12 14:22:52
updated_at: 2026-08-12 21:38:05
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 建立管理端列表页列展示与分页一致性契约

# 原始描述

类型倾向：REQ

标题：建立管理端列表页列展示与分页一致性契约

背景：Banner、日志审计、用户管理在列展示、换行、分页和操作列上反复返修。

影响范围：Web 管理端、设计系统、前端测试、docs/knowledge-base。

建议验收要点：nowrap 规则、有效期例外、冻结操作列、分页样式、后端真实分页。

# 待澄清

- [ ] 需要纳入一致性契约的首批管理端列表页范围。
- [ ] 有效期字段允许换行或多行展示的例外规则细节。
- [ ] 冻结操作列在不同视口宽度和横向滚动下的具体交互验收方式。
- [ ] 后端真实分页需要覆盖的接口清单与分页参数/响应契约。

# 探索结论

（/req-explore 后人工确认写入）
