---
requirement_id: REQ-0138-knowledge-model-lifecycle-sync
title: 建立 knowledge-model 基础结构与生命周期同步机制
status: in_sprint
created_at: 2026-09-10 17:36:18
updated_at: 2026-09-10 23:00:04
owner: product
related_change: add-knowledge-model-lifecycle-sync
---

# 需求说明

## 背景与目标用户

现有 Issue、OpenSpec、源码、测试和发布资料分别保存交付事实，缺少统一语义约束与可追溯投影。目标用户为研发人员、流程维护者、评审者及执行生命周期命令的 Agent。本需求建立本体驱动的最小知识底座，按既有生命周期生成可验证知识，不建设问答产品。

## 范围

首版包含元本体、产品研发本体及最小领域模型、结构 Schema、映射与抽取、Change 增量同步、Sprint 一致性校验、完整小规模 Git 快照、恢复及同步记录。选择一个真实、范围较小的 Change 验证全链路，其余 Change 必须明确是否在覆盖范围。

不包含图数据库、图谱可视化、Agent 问答或动作执行、全量历史回填、全部模块覆盖、自然语言规则的全自动理解、跨产品本体平台和销售实施材料生成。定义领域概念不代表导入真实客户或商品实例。

## 功能要求

### FR-001 目录与治理登记

目标目录为：

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

ontology 定义建模语言与产品研发通用语义；domain-models/tilesfst 定义具体领域对象、行为、规则及应用绑定；schema 校验文件结构；generated 保存按已审核模型和映射生成的产品事实；validation 检查跨层引用、本体一致性与业务预期。registry 登记模型版本、文件入口、依赖、覆盖范围与维护责任。更新 project.yaml、AGENTS.md 必要摘要、目录规范及校验、文档索引与治理同步矩阵。实际目录及脚本在 OpenSpec 实现阶段建立。

### FR-002 产品研发本体

product-development-ontology.yaml 定义 Product、ProductModule、ProductCapability、Requirement、Bug、Change、Page、UIComponent、API、BusinessObject、DataField、BusinessRule、UserRole、TestCase、Sprint、Release、Evidence，并补齐关系使用的 UserAction、Permission 和来源 Artifact 类型。

关系至少覆盖 Product contains ProductModule、ProductModule provides ProductCapability、Page presents ProductCapability、Page contains UIComponent、UIComponent triggers UserAction、UserAction calls API、API reads/writes BusinessObject、Requirement changes ProductCapability、TestCase validates BusinessRule、Sprint includes Change、Release includes Sprint。API 读写使用两种明确关系。Release 对实际发布 Change 另存明确成员关系，不能仅由所属 Sprint 推断全部发布。

每种类型、关系有稳定 ID、中文含义与所属命名空间；关系定义合法起终点、基数及必要属性约束。类型与实例分离，页面展示类型与展示具体记录的关系不能混用。未注册概念或关系不允许成为正式知识。

### FR-003 TilesFST 领域模型

定义 TileSKU、Brand、TileCategory、TileSpec、BrandCertificate、TileImage、TileVideo、Banner、AdminUser、Employee。业务对象映射到 BusinessObject；AdminUser 表示账户类型，Employee 表示角色语义，并通过账户角色关系连接 UserRole，不能把账户和角色当成同类实例。

覆盖 SKU 所属品牌、类目、规格、图片及视频，品牌证书和类目父子关系。基数、可空性、类目层级和状态条件须从正式规格核对；不能依据名称猜测强规则。历史兼容记录与当前新建约束需区分适用条件和版本。

### FR-004 行为语义与权限边界

meta-ontology.yaml 定义 AgentAction、Tool、InputParameter、Precondition、Postcondition、RequiredPermission、FailureCondition、ConfirmationPolicy；明确与 UserAction、Permission 的映射或继承关系。动作描述目标类型、参数、所需权限、前置条件、调用映射、成功后置条件及失败条件。

以 PublishTileSKU 为语义样例，关联 TileSKU、所需管理权限、资料和主图校验、上架接口及 PUBLISHED 后置状态。ManageTileSKU 和 publishAdminTileSku 是用户提供的概念示例，必须核对实际权限及 OpenAPI 标识后才建立真实映射，不据此新增接口或权限。后置条件只在成功证据成立时成立。首版不执行动作，模型许可不替代后端校验。

### FR-005 来源映射与知识生成

输入为 Change ID、关联 Issue、proposal/design/tasks/trace、合并后的正式规格、实际修改文件、OpenAPI、测试和验收证据。依据映射与本体输出实体、关系、规则候选、来源指针、差异摘要及未决项。

每条生成知识包含来源文件、可解析定位、输入 Git Commit、来源内容摘要、本体及映射版本。来源提交表示被消费的版本，不使用包含生成文件的提交自引用。不能把未提交工作区内容冒充该 Commit；无法固定来源时记录待恢复原因。多个前提的推导保存各自证据。人工覆盖仅修正已审核投影，不替代业务权威来源，源内容变化触发复核。

### FR-006 Change 归档集成

正式写入由归档成功触发，普通文件移动和 PR 不触发正式同步。归档前可预检输入和映射；保留既有归档、Workflow Sync 与 Issue 迁移顺序，之后构建候选、验证、切换模型和写回执。以 Change 为单位支持直接 Change 和多 Change Issue，不能以 Issue 提前闭环。

同步结果区分 synced、stale、failed、out_of_scope，范围外须有原因；范围内断裂引用、来源不可信或本体约束失败不得发布候选。反向引用纳入必要增量范围，删除和重命名不遗留失效关系。

### FR-007 Sprint 一致性门禁

Sprint 归档前检查每个 Change 的适用性及同步状态；覆盖范围内失败或过期、本体类型/关系/基数错误、已确认的同版本同条件权限或状态冲突、无来源强规则、失效代码/API 引用及高风险未决项阻断归档。低风险语义缺失仅警告。未知不等于错误，未覆盖不等于通过。模型验证结果不替代业务验收证据。

### FR-008 完整版本快照

首版将小规模完整快照提交 Git。snapshots/vX.Y.Z/ 保存 manifest.yaml、entities.yaml、relations.yaml、rules.yaml；manifest 记录产品版本、模型版本、输入 git_commit、生成时间、包含 Sprint 与 Change、来源 Release、各内容摘要和可定位的本体/映射版本。

release-prepare 构建并校验候选；release-publish 确认范围和摘要后关联已验证快照，不在确认阶段重新抽取。快照内容发布后不可覆写；正式发布状态以 release.json 确认为准。变化不反向改写既有版本知识。稳定排序与内容摘要支持重建检查；限制快照文件数量和总字节数，阈值由实现设计给出并覆盖边界测试。

### FR-009 失败恢复与写入规则

本体、Schema、映射、覆盖项由人工或明确授权的维护流程修改；generated 与 snapshots 由工具生成；unresolved 由工具记录、人工处置。禁止直接手改 generated，通过受控生成和摘要校验检测漂移。

临时构建通过全部校验后再切换正式模型，失败保持旧内容不变。并发采用互斥及输入摘要复核防止覆盖；相同 Change、输入摘要、本体/映射/提取版本重复运行不生成重复实体。允许单 Change 重试。区分归档已完成、模型已提交、回执待补等阶段；回执失败不重复已成功的模型提交，更不自动撤销 OpenSpec 归档。

Change trace 在归档收尾写同步摘要，独立记录包含运行标识、阶段、来源、差异计数、失败类别和恢复入口。Sprint 冻结后的恢复记录写入独立记录区，不反向改写冻结文档；记录区位置与保留阈值由设计确定。只保存脱敏结构化摘要，不保存原始日志、密钥或客户记录。

### FR-010 验证闭环

使用一个真实的小范围 Change 完成实现和测试、归档、自动增量、重复同步、Sprint 门禁、版本快照的闭环。冲突、故障、并发和未覆盖场景用隔离夹具验证。真实发布确认与本地模拟分别记录，未获取发布确认时不得声称真实发布验证完成。可用本需求的实现 Change 自举，但必须证明归档时工具已可用且输入已固定，避免循环依赖。

### FR-011 元本体与领域模型分层

meta-ontology.yaml 明确定义 AggregateObject、Entity、Attribute、Behavior、Rule、Scenario、Actor、Role、Permission、Event、Compensation、QualityConstraint、UIPage、UIComponent 及类型间合法关系。每个 model_type、ownerEntity、refEntity、行为规则绑定及模板引用均须有显式语义定义，不能只以字符串或文件名推断。与产品研发本体的 BusinessObject、BusinessRule、Page、UserRole 等采用明确映射，避免重复命名产生两个权威定义。

分层为“元本体定义 Behavior → 领域模型描述 TileSKU_Publish → 生成事实关联实际 API、Change 和测试”。一次真实用户上架操作属于业务运行记录，首版不采集。领域模型是元本体的应用，具体商品记录不是领域类型；验证器须区分元类型、领域模型元素和生成事实的引用层级。

### FR-012 M 系列语义覆盖与首版边界

| 文件 | 职责 | 首版约束 |
|---|---|---|
| m1-object-model | 聚合、对象、属性、引用与约束 | 覆盖已列 TilesFST 类型，只有试点关联映射要求实例化 |
| m2-behavior-model | 命令、查询、参数、前后置条件 | 定义语义，不调用真实工具 |
| m3-rule-model | 校验与计算规则 | 规则有来源与适用条件，不执行任意表达式 |
| m4-scenario-model | 主流程、异常流程及业务能力绑定 | 一个试点场景及其证据关系 |
| m5-actor-model | 主体、角色、权限、数据范围 | 账户、角色和权限明确分离 |
| m6-compensation-model | 业务重试、补偿与幂等语义 | 不建设 Saga 或业务补偿执行器；无已确认业务来源时声明范围外及理由 |
| m7-quality-model | 性能、一致性、并发与审计约束 | 仅记录有依据的约束及证据，不编造 SLA |
| me-event-model | 事件类型、载荷、生产者与订阅者 | 不建设事件总线；示例事件未经来源确认不得标为实际存在 |
| m9-ui-model | 页面、组件、模板与业务模型绑定 | 只做语义引用，不生成页面或新增 UI 功能 |

文件登记 coverage/status，允许显式未覆盖，不能通过空文件冒充完成语义建模。试点要求对象、行为、规则、主体、场景及实现证据形成一个闭环；其余维度按真实来源覆盖或声明 N/A。共用 UI 模板只在存在真实复用需求时单独定义；所有引用都必须解析到合法模板及参数契约。

业务补偿描述产品业务失败后的语义；知识同步恢复描述工具自身提取、提交、回执的恢复。两者使用独立标识和状态，业务补偿不得导致模型工具执行真实业务操作。

### FR-013 跨文件语义、版本与来源

分别登记 schema_version、meta_ontology_version、domain_model_version、product_version、snapshot_id，并记录兼容关系及内容摘要。快照锁定完整依赖集合，元本体不兼容变更要求重新验证领域模型和受影响生成事实；失败不发布新模型，不改写已发布快照。

引用验证覆盖类型、属性、关系、行为 ownerEntity、参数类型、规则、主体/权限、事件载荷、场景步骤、补偿目标、质量约束和 UI 模板绑定；不能仅检查引用 ID 存在，还需检查目标类型、跨层合法性、基数、参数及版本兼容。

每个领域模型元素具有稳定 ID、权威依据、审核状态及可解析来源；来自规范的产品规则保留原规范权威，代码/API 映射保留对应版本证据。REQ/Change/测试关联允许暂缺并声明原因，不伪造来源以补齐字段；缺强规则依据则保持候选。合同示例只作为用户提供的结构优化依据，不引入合同领域概念、原文、业务数据或未经核验的校验结论。首版不要求 OWL/RDF 工具链或应用代码生成器。

## UI 与影响约束

无产品页面或交互改动，无 UI prototype；本体中 Page/UIComponent 为语义类型，不构成 UI 开发。business-flow.md 提供本体与格式约束职责图。API/数据库均为只读事实输入，不变更 HTTP 请求响应、错误码、Pydantic Schema 或 SQLite/MySQL 结构，不需 Orval 和 Docker Compose；测试新增在后续实现阶段。

## 关联需求

REQ-0089-workflow-subdocument-status-sync 提供既有状态传播边界，REQ-0026-product-release-management 提供发布对象语义；本需求为独立交付单元，非上述需求子项。

## 状态与观测声明

需求已纳入 sprint-030，关联 Change 为 add-knowledge-model-lifecycle-sync。需求验收标准见 acceptance.md。

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 本地研发治理工具只读提取仓库资料，不新增业务 API、数据库表、请求日志、行为埋点、Task Trace 或端请求封装；同步记录为研发工具摘要。
  validation: 后续验证不输出敏感资料、保留策略有效且无业务 API/DB/端契约变化；范围扩大时重新评估。
```

观测规范依据：docs/standards/product-data-collection-observability.md。
openspec_changes:
  - change_id: add-knowledge-model-lifecycle-sync
    type: update
    status: applied
