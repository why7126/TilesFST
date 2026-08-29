---
req_id: REQ-0127-product-data-collection-observability-hard-gate
status: done
created_at: 2026-08-26 19:48:35
updated_at: 2026-08-27 23:13:16
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0126-product-data-collection-observability-standard
---

# 一句话

建立产品数据采集与链路观测规范硬门禁，将 `docs/standards/product-data-collection-observability.md` 接入项目入口、规则、技能检查清单和实现级校验脚本，使相关变更在需求、OpenSpec、Sprint、实现和验收阶段必须读取、声明并通过校验。

# 原始描述

用户要求建立产品数据采集与链路观测规范硬门禁：

- 把 `docs/standards/product-data-collection-observability.md` 接入 `AGENTS.md`。
- 把该规范接入相关 `rules/`。
- 把该规范接入 req、opsx、sprint 技能检查清单。
- 补齐实现级校验脚本。
- 使采集规范在 API、DB、日志审计、行为埋点、Task Trace、前端/小程序/App 请求封装相关变更中成为必读、必声明、必验收的流程门禁。

# 背景与关联

- 父需求：`REQ-0126-product-data-collection-observability-standard`
- 关联文档：`docs/standards/product-data-collection-observability.md`
- 关联能力：产品数据采集、请求日志、行为埋点、Task Trace、日志审计、API/DB/前端/小程序/App 请求封装治理
- 业务价值：把已沉淀的产品数据采集规范从“参考文档”提升为可执行流程门禁，避免 API、DB、端请求封装和链路观测相关变更遗漏采集声明、验收标准或校验证据。

# 影响范围

- 入口与规则：`AGENTS.md`、API/DB/日志审计/Task Trace/前端/小程序/App 请求封装相关 `rules/`。
- 命令技能：`req-*`、`opsx-*`、`sprint-*` 中涉及检查清单、必读规则、下一步门禁或验收输出的技能。
- 校验脚本：新增或增强实现级校验，覆盖相关文档引用、声明字段、验收项和变更范围扫描。
- 研发流程：需求生成、需求完善、OpenSpec propose/apply/archive、Sprint propose/apply/archive 相关门禁。

# 建议验收要点

- [ ] `AGENTS.md` 明确在 API、DB、日志审计、行为埋点、Task Trace、前端/小程序/App 请求封装相关任务中追加读取产品数据采集与链路观测规范。
- [ ] 相关 `rules/` 明确该规范的必读、必声明、必验收触发条件，并避免重复粘贴完整规范正文。
- [ ] req、opsx、sprint 技能检查清单纳入采集规范门禁，能引导需求、Change 与 Sprint 在涉及范围内声明适用性、影响范围和验收结果。
- [ ] 实现级校验脚本能检查入口、规则、技能和变更材料是否引用或声明采集规范门禁。
- [ ] 校验覆盖 API、DB、日志审计、行为埋点、Task Trace、前端请求封装、小程序请求封装和 App 请求封装相关关键词或路径。
- [ ] 门禁允许明确声明“不适用”，但必须记录原因；不得默默跳过。
- [ ] 变更不直接修改业务 `src/` 实现，除非后续 OpenSpec Change 明确进入实现阶段并纳入 Sprint。
- [ ] 文档更新遵守事实唯一归属和表达卫生，不把完整规范正文复制到多个入口文件。

# 待澄清

- [ ] 实现级校验脚本应作为新增独立脚本，还是并入现有目录结构、OpenSpec、上下文预算或 workflow 校验脚本。
- [ ] 门禁触发范围是否只扫描 active Change 和本次变更文件，还是也覆盖历史归档材料。
- [ ] App 请求封装在当前仓库中是否仅作为治理规范项保留，还是已有具体目录需要纳入路径级校验。
- [ ] 对“不适用”声明是否需要固定字段名和模板，例如 `product_data_collection_observability: not_applicable` 与原因。

# 探索结论

（/req-explore 后人工确认写入）
