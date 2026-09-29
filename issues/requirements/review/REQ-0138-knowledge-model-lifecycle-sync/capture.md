---
req_id: REQ-0138-knowledge-model-lifecycle-sync
status: captured
created_at: 2026-09-10 17:22:01
updated_at: 2026-09-10 17:50:22
recorded_by: product
source: 用户需求与方案讨论
priority_hint: P1
parent_requirement: null
---

# 一句话

建立 knowledge-model 基础结构与生命周期同步机制：支持 Change 归档增量更新、Sprint 一致性校验、发布快照及失败恢复。

# 原始描述

在 TilesFST 现有 Issue、OpenSpec、Sprint、Release 和 Workflow Sync 体系基础上，建立运行同步机制所必需的最小知识模型基础。当 OpenSpec Change 归档成功后，根据 Change、关联 REQ/BUG、正式规格、代码、API 和测试增量更新知识模型；Sprint 归档时执行跨 Change 一致性校验；产品版本正式发布时绑定产品版本、Git Commit 并生成知识快照。同步失败不得污染现有知识模型，支持安全重试和问题追踪。

基础结构与同步机制共同构成一个最小生命周期交付闭环，沿用同一需求，不拆分为独立需求。知识模型只保存结构化事实、关系、规则候选和来源，不替代已有事实源。

## 1. 最小知识模型基础

首版目标结构：

```text
knowledge-model/
├── README.md
├── registry.yaml
├── ontology/
│   ├── meta-ontology.yaml
│   └── product-development-ontology.yaml
├── domain-models/
│   └── tilesfst/
│       ├── m1-object-model.yaml
│       ├── m2-behavior-model.yaml
│       ├── m3-rule-model.yaml
│       ├── m4-scenario-model.yaml
│       ├── m5-actor-model.yaml
│       ├── m6-compensation-model.yaml
│       ├── m7-quality-model.yaml
│       ├── me-event-model.yaml
│       └── m9-ui-model.yaml
├── schema/
│   └── knowledge-model.schema.yaml
├── mappings/
├── generated/
├── overrides/
├── unresolved/
├── snapshots/
└── validation/
```

建立最小注册表、元本体、产品研发本体及领域模型、独立格式约束、模型状态和生成区，明确各目录的自动写入与人工维护边界，禁止人工修改 generated/。同步更新 rules/directory-structure.md、目录校验及必要入口，在 docs/README.md 或对应说明入口建立导航，并在 project.yaml 登记 knowledge-model 能力。实际目录和治理资产在后续 OpenSpec 实现阶段建立。

## 2. Change 归档增量更新

正式触发点为 OpenSpec Change 归档成功，不使用普通文件移动或每次 PR 作为正式同步事件。以 Change 为增量单位，覆盖 REQ/BUG 来源和直接 Change；多 Change Issue 的交付闭环分别按既有规则汇总。

输入包括 Change ID、关联 REQ/BUG、proposal/design/tasks/trace、合并后的正式规格、实际修改文件以及测试和验收结果。固定来源清单和内容摘要，避免混入其他未归档改动，并检查必要反向引用。

输出包括新增或修改的实体与关系、规则候选、来源文件与 Git Commit、无法确定的异常项和差异摘要。同步不自动理解所有自然语言规则，模型结论不替代后端鉴权。

## 3. Sprint 归档一致性校验

检查 Sprint 内所有 Change 的同步完成情况、同一实体类型冲突、权限与状态规则冲突、无来源规则、已删除代码或 API 的残留引用、未处理的高风险异常。

结构性错误和已确认的高风险冲突阻断 Sprint 归档；低风险语义缺失生成警告并进入待处理项。区分抽取未知与事实错误，不将模型校验通过视为业务验收、真机或线上验证通过。

## 4. 发布快照

产品版本正式发布时形成对应版本的知识快照，目标结构：

```text
knowledge-model/snapshots/vX.Y.Z/
├── manifest.yaml
├── entities.yaml
├── relations.yaml
└── rules.yaml
```

manifest 至少记录 product_version、knowledge_model_version、git_commit、generated_at、included_sprints、included_changes，并能追溯 Release。正式快照以确认的发布范围为准，不能将发布计划、已实现能力或 Git tag 存在等同于已发布或已部署。

首版小规模完整快照提交 Git，限制试点范围与体积，支持离线追溯和重建验证。发布准备时构建候选、发布确认时绑定生效的具体职责，需与现有发布规范协调确定。

## 5. 失败恢复与记录

- 临时生成和校验通过后才能替换正式模型；同步失败保持正式模型不变。
- 相同 Change 和输入重复同步不产生重复实体，成功步骤可安全重试，支持重新执行单个 Change 同步。
- 区分归档失败与归档成功但同步待恢复，不能通过重试重复执行已完成的归档副作用。
- 同步结果写入 Change trace.md，并能查看失败原因、差异摘要与待处理项。
- 明确 trace 回填时机和冻结后的恢复记录归属，后续重建不得反向修改已冻结交付语义。
- 人工覆盖项与来源版本关联；来源变化能识别失效覆盖或待复核内容。

## 首版明确不包含

- 图数据库和知识图谱可视化页面。
- Agent 问答接入或 Agent 动作执行。
- 一次性回填全部历史需求、BUG 或覆盖全部 TilesFST 模块。
- 自动理解所有自然语言业务规则。
- 跨产品通用本体平台。
- 销售、实施材料生成。

首版仅用一个范围较小的真实 Change 验证生命周期闭环，不要求额外交付前版建议中的通用只读问答能力，也不将 SKU 全域建模作为首版前提。

## 建议首版验收闭环

选择一个真实、范围较小且遵守现有评审和 Sprint 流程的 Change：创建与实现、完成测试 → 归档成功 → 自动生成知识增量 → 重复同步 → Sprint 一致性校验 → 测试发布流程 → 形成版本快照。测试版本与证据场景需在设计时明确，不以测试夹具或本地模拟冒充正式发布。

核心验收要点：

- Change 归档后自动完成增量同步，每条生成知识都有来源文件和 Git Commit。
- 相同输入重复执行结果幂等，不重复实体或关系。
- 构造规则冲突时 Sprint 归档被阻断；低风险缺失仅警告。
- 注入同步异常后正式知识模型不变；修复后能够安全重试。
- 已完成归档但同步失败的状态清晰可查，支持单 Change 恢复。
- 发布快照可追溯到 Release、Sprint 和 Change，历史快照不受后续更新污染。
- 验证生成区禁止人工修改，以及同步记录与冻结文档边界。

## 影响范围

拟涉及 knowledge-model、project.yaml、目录规范与校验、文档入口、scripts、tests、生命周期技能、Workflow Sync 和发布集成。首版只读消费 API 与代码等资料，不改变业务 API、SQLite/MySQL 表结构、Web、店主端、小程序或管理端行为；不需要 Orval 生成或 Docker Compose 验证。后续若范围改变需重新评估。

# 待澄清

- [ ] 本体、格式约束与映射的详细设计及试点选择由 requirement.md 和验收标准承接。
- [ ] 确定自动写入与人工维护权限、覆盖项复核、未决项与同步记录的路径及保留策略。
- [ ] 确定归档前候选预检、归档成功后同步、trace 回填及冻结后恢复的挂接顺序。
- [ ] 确定来源 Commit 绑定、原子替换、并发控制、幂等键及故障恢复状态。
- [ ] 确定候选快照构建与发布生效步骤、快照 Git 提交策略和测试发布证据场景。
- [ ] 明确结构性错误、高风险冲突、低风险警告的判定及审核责任。

# 探索结论

最小模型基础纳入本需求交付范围，以一个真实 Change 验证生命周期同步闭环。当前仅完成需求记录修订，后续先分析、生成和评审需求，再纳入 Sprint、创建 OpenSpec Change 并开发。

# 来源依据

- 用户提出的最小知识模型基础、生命周期同步、首版排除项和验收闭环。
- rules/issues-lifecycle.md：多 Change 闭环与归档同步顺序。
- rules/iterations-lifecycle.md：Sprint 归档与交付事实冻结。
- rules/document-governance.md：事实唯一归属。
- rules/release.md：发布准备与确认职责。
- .agents/skills/workflow-sync/SKILL.md：事件及状态同步边界。

## 本体范围修订

ontology/ 定义语义，schema/knowledge-model.schema.yaml 仅校验结构，validation/ 验证本体与业务预期。完整范围以 requirement.md 为准；用户选择首版完整小规模快照提交 Git。

## 领域模型分层修订

采纳元本体、产品研发本体、domain-models/tilesfst 和生成事实的分层。行为语义由元本体定义、具体行为由 m2 描述；领域对象由 m1 描述。格式 Schema 保留，M 系列只在试点内实例化必要语义，不扩展为应用生成平台。具体要求见 requirement.md 的 FR-011～FR-013。
