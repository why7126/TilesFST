---
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
created_at: 2026-09-10 19:17:59
updated_at: 2026-09-10 19:17:59
---

## 背景与动机

项目资料缺少本体约束、跨文件语义引用和生命周期投影。建立最小本体驱动知识底座，使归档增量、Sprint一致性和发布快照具有可追溯且可恢复的实现边界。

## 变更内容

- 建立knowledge-model顶层目录、元本体、产品研发本体、TilesFST领域模型、格式Schema与映射。
- 归档成功后增量同步；Sprint检查范围及语义；prepare构建完整Git快照、publish确认关联。
- 增加来源版本、跨层引用、幂等、并发、原子提交和回执恢复验证。
- 保持单真实Change试点；不建设图数据库、问答、动作执行或业务应用生成器。

## 能力

### 新增能力

- `knowledge-model`：本体与领域建模、抽取、语义验证和恢复。

### 现有能力扩展

- `agent-workflow-tooling`：知识模型目录边界、归档触发与回执。
- `sprint-planning-governance`：知识同步覆盖与一致性关闭门禁。
- `product-release-management`：完整知识快照构建、确认与版本锁定。

## 影响

涉及knowledge-model、scripts、tests、project.yaml、AGENTS.md、目录规则、相关技能和文档索引。无业务src、HTTP契约、DB结构、媒体或端侧行为变化；不需Orval、Docker Compose。沿用sprint-030中13人天，不重复计量；总容量100%，修复缓冲为0。
