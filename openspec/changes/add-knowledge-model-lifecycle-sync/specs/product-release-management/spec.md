---
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
created_at: 2026-09-10 19:19:40
updated_at: 2026-09-10 19:19:40
---

## ADDED Requirements

### Requirement: 版本知识快照准备与确认

系统 MUST 在release-prepare构建完整小规模Git知识快照，锁定来源与模型依赖；release-publish仅核验并关联候选，不重新抽取，发布后的内容不可覆写。

#### Scenario: 生命周期门禁
- **WHEN** 候选范围和摘要均与已确认发布范围一致
- **THEN** 系统 MUST 记录快照关联；仅以发布确认表示生效，不依据文件或tag存在推断
