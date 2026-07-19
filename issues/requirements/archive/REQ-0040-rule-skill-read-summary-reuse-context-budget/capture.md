---
req_id: REQ-0040-rule-skill-read-summary-reuse-context-budget
status: done
created_at: 2026-07-16 08:58:55
updated_at: 2026-07-18 09:18:43
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement:
---

# 规则/Skill 已读摘要复用纳入命令上下文预算治理

将规则文件与 Skill 文件的已读摘要复用机制纳入命令上下文预算治理，减少同一会话内连续执行工作流命令时对相同规则与 Skill 的重复全量读取。

# 原始描述

将规则/Skill 已读摘要复用机制纳入命令上下文预算治理，减少连续命令重复读取。

# 待澄清

- [ ] 已读摘要的事实源应存放在会话内存、命令输出摘要、临时文件，还是长期文档/trace 中。
- [ ] 摘要复用的失效条件：文件内容变更、命令类型切换、跨会话、或用户显式要求重新读取。
- [ ] 哪些文件允许摘要承接：仅 `rules/` 与 `.agents/skills/`，还是也包含 OpenSpec Change、Sprint、issues 片段。
- [ ] 是否需要为各命令 Skill 增加统一的“已读摘要复用”执行模板与校验脚本。

# 探索结论

（/req-explore 后人工确认写入）
