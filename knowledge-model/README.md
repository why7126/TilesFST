---
created_at: 2026-09-10 20:38:13
updated_at: 2026-09-10 20:38:13
---

# 产品知识模型

本目录把现有 Issue、OpenSpec、代码、API 和验收资料投影为带来源的知识。原资料仍是事实源，不复制需求正文或建立第二套文档库。

| 区域 | 用途与写入权限 |
|---|---|
| registry.yaml、ontology/ | 人工评审维护版本、范围、元本体与研发本体 |
| domain-models/tilesfst/ | 人工维护领域对象、行为、规则、场景、主体；未覆盖维度明确原因 |
| schema/ | 人工维护 YAML 结构契约，不替代本体语义 |
| mappings/、overrides/ | 人工评审的显式抽取与覆盖；覆盖绑定来源摘要 |
| generated/ | 工具独占写入；禁止手工编辑，通过同步重建 |
| unresolved/ | 人工维护异常的风险、来源、处置状态；高风险未处置阻断 Sprint |
| snapshots/ | prepare 生成、publish 关联；完整小快照纳入 Git，发布后冻结 |
| validation/ | 人工维护能力问题和正反例；工具执行，不调用业务 API |

工具与恢复说明见 [生命周期操作规范](../docs/standards/knowledge-model-lifecycle.md)。当前仅覆盖 `add-knowledge-model-lifecycle-sync`；其他 Change 返回有原因的 out_of_scope。M6/M7/ME/M9 尚未覆盖，不按空文件计数。

元本体定义可用的概念及引用类型；领域文件定义 SKU 发布与删除约束的语义；generated 是带 Git 来源的具体事实。示例仅引用已有正式规格、Python 符号和 OpenAPI 操作，不执行发布动作。
