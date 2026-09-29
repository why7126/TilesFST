---
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
created_at: 2026-09-10 19:19:40
updated_at: 2026-09-10 19:19:40
---

## ADDED Requirements

### Requirement: 本体知识目录与归档同步

系统 MUST 登记knowledge-model目录及维护边界，在归档成功、Workflow Sync和必要Issue迁移后调用知识同步；check/dry-run不得生成知识；冻结后恢复不得改写交付事实。

#### Scenario: 生命周期门禁
- **WHEN** 归档已成功但模型同步失败
- **THEN** 系统 MUST 分别记录归档完成和同步待恢复，允许单Change重试且不重复归档
