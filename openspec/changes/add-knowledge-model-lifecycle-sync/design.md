---
source_requirement: REQ-0138-knowledge-model-lifecycle-sync
iteration: sprint-030
created_at: 2026-09-10 19:19:40
updated_at: 2026-09-10 22:51:56
---

# 技术设计

## 目标与边界

来源为REQ-0138的13条FR和31条AC。实现元本体→领域模型→映射→生成事实，不执行真实业务动作。无业务API/DB/UI变化；原型冲突处理N/A，模型的Page不是产品UI交付。完整知识快照提交Git已由用户选定。

## 决策与替代方案

| 决策 | 采用 | 替代与理由 |
|---|---|---|
| 执行位置 | scripts/knowledge_model/模块、scripts/sync-knowledge-model.py与validate-knowledge-model.py薄入口 | 不部署服务，减少首版运行依赖 |
| 模型 | ontology/meta-ontology.yaml、product-development-ontology.yaml与domain-models/tilesfst/M系列；schema独立 | 不将Schema当本体；不引入OWL/RDF工具链 |
| 抽取 | 显式仓库相对映射、确定性解析、审核候选 | 不用名称启发式自动批准强规则 |
| 提交 | 不可变generation目录加原子current指针 | 多文件逐个覆盖不能保证读者一致 |
| 并发 | 单仓库写锁、输入摘要重验 | 不采用最后写入覆盖 |
| 快照 | 完整小规模Git快照，依赖摘要锁定 | 不采用仅manifest外部存储 |

## 目录与写入契约

registry登记版本、模块、维护者、coverage、阈值和入口。ontology、domain-models、schema、mappings、overrides为受控维护区；generated、snapshots仅工具生成；unresolved为工具记录、人工通过受控操作处置。注册未覆盖维度及理由，不能以空文件计为完成。

运行锁和运行回执放data/knowledge-model/，不得提交。原子提交的临时目录在目标目录同一文件系统内创建。generated/generations/<content-id>/保存实体（含规则）、关系、Change分片与manifest，generated/current.yaml原子指向通过校验的generation；所有消费者先固定current值再读取。generation内容不含易变运行时间；运行时间放回执，重复输入不会制造无意义diff。旧generation只在确认无读者且不被快照引用后清理，至少保留最近2份；运行记录默认30天。unresolved仅存脱敏结构化摘要。发布快照永久保留，不受运行清理影响。

首版单快照最多100个文件、10MiB UTF-8内容，单文件最多2MiB；registry可配置，但配置变更需评审，超限拒绝快照而非截断。测试覆盖等于及超过阈值。YAML使用安全加载，拒绝重复键；路径拒绝越界、绝对路径及逃逸符号链接，不执行模型表达式或工具名称。

## 语义与版本

类型ID按命名空间唯一；元类型、领域模型元素、生成事实分层。Relation显式起终点、基数、版本及必要属性。继承允许经声明的兼容类型；类型/引用/模板参数/事件载荷均验证。强规则采用白名单声明式条件（相等、集合、存在、合取），未知操作符拒绝；不尝试任意自然语言推理。冲突仅在同版本、同条件范围内已确认规则可证明相反时阻断，否则记录未知。

schema_version、meta_ontology_version、domain_model_version、product_version和snapshot_id独立；兼容矩阵显式登记。快照锁定本体、模型、映射、提取器和来源摘要。领域模型中的权限与接口示例经正式规格/OpenAPI核对，业务补偿仅语义，不与同步恢复状态混用。

## 来源固定与归档顺序

以Change ID为单位，源清单包含Change文件、正式spec、实际修改文件、OpenAPI、测试证据和Issue关联；有反向引用的对象一起失效重建。来源采用已提交的Git对象与内容摘要，文件定位以该Commit为准；归档前后路径允许迁移映射，不改稳定语义ID。只消费试点明确列出的版本，不用整份当前工作区代表Change。

归档前预检映射和覆盖→原有OpenSpec归档→Workflow Sync→必要Issue迁移→固定归档资料与输入提交→临时构建→校验→锁内输入复核→写generation→原子切换current→独立回执→trace摘要。

归档刚完成而输入尚未提交时，记录source_revision_pending并保留正式模型，提供单Change恢复入口；不自行提交用户工作区。归档完成状态与知识同步待恢复分别报告。准备真实演练时在正常授权的提交节点固定输入，不能为消除等待而伪填HEAD。

幂等键由Change、输入摘要、本体/领域/映射/提取版本构成。generation提交标识用于恢复：切换前失败保持既有current；切换后回执失败仅补记录；重复归档命令识别已归档路径并进入同步恢复入口。冻结后回执只进入独立记录；原trace中的稳定运行标识可关联后续结果。

## 生命周期集成

通用Workflow Sync的check/dry-run不得触发写入；集成在归档编排收尾调用同步入口。opsx-archive与基础archive技能统一引用同一实现，sprint-archive批处理复用且去重。Sprint readiness对每个Change报告synced/stale/failed/out_of_scope；范围外有原因，范围内强错误阻断。

prepare按release真实范围构建候选快照，清单不推断整个Sprint均已发布；publish仅比较范围与摘要并在release.json关联快照。快照中的发布状态不自行宣称生效，查询发布事实以publish_confirmation为准。release确认失败不损坏候选，后续重试复用。发布字段和schema接入需更新发布validator，知识产物不应无理由计入业务镜像输入。

## 试点、迁移与风险

采用本Change自举验证研发追踪闭环，领域层用SKU上架既有规格/接口作只读来源。必须在实现阶段固定源清单和提交；该业务资料只是试点的模型输入，不能宣称本Change实现SKU业务。多Change及冲突、并发、补偿场景在临时仓库测试。真实Sprint归档和发布需既有审批边界；apply阶段完成预演证据，真实生命周期证据由后续命令补充，绝不伪造完成事件。

默认覆盖仅本Change；既有Change显式范围外，后续通过受控配置扩展，不全仓回填。关闭该覆盖可停止新生成，旧快照仍可读；失败回滚只恢复模型指针，不撤销OpenSpec或业务发布。

主要风险为零Sprint缓冲、归档与Git提交时序、跨技能同步漂移。沿用13人天估算，若扩大范围重估；先验证恢复状态和输入固定，再推进独立本体任务。

## 治理与测试同步矩阵

| 范围 | 更新目标与验证 |
|---|---|
| 顶层边界 | AGENTS.md、rules/directory-structure.md、目录validator、project.yaml、docs/README.md |
| 详细规范 | docs/standards/knowledge-model-lifecycle.md、docs/spec-logs变更摘要与治理日志 |
| 归档/Sprint | 对应技能、Workflow Sync集成边界、readiness脚本及隔离测试 |
| 发布 | prepare/publish技能、release validator和快照测试 |
| 模型工具 | scripts/knowledge_model、薄入口、tests/test_knowledge_model_* |

knowledge_base_refs为docs/knowledge-base/README.md和retrospectives/sprint-028-retrospective.md。承接归档路径残留、同步矩阵、证据边界；UI横切N/A。

## 产品数据采集与链路观测

依据docs/standards/product-data-collection-observability.md：

```yaml
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 本地研发工具只读消费仓库资料，不新增业务API、数据库表、请求日志、行为事件、Task Trace或端请求封装。
  validation: AC-OBS-001/002验证边界、脱敏及保留；无OpenAPI/Orval、SQLite/MySQL迁移或Compose需求，业务实现测试未运行。
```

## 实现细化

trace 使用 knowledge-trace-v1 规范化来源：仅排除工具维护的回执区与 updated_at，其他内容核对固定 Commit。快照 manifest 内嵌依赖文本及摘要，并记录首轮 prepare 的 Git 基线；已发布快照按冻结依赖验证。未发布候选输入漂移时拒绝覆盖，维护者核对后清除候选再 prepare。进程锁与原子指针保障进程失败恢复，不声明断电事务保证。源码样例属于本 Change 的证据输入，不生成本 Change 修改 SKU 业务的虚假关系。
