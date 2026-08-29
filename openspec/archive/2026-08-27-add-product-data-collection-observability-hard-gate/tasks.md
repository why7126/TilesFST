## 1. 入口与规则门禁

- [x] 1.1 更新 `AGENTS.md` 任务读取路由和完成检查清单，将 `docs/standards/product-data-collection-observability.md` 接入 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装和 App 请求封装触发范围。
- [x] 1.2 更新 API、数据库、测试、文档治理、需求管理、迭代生命周期或 OpenSpec 相关 rules，声明采集规范必读、必声明、必验收和 N/A 原因要求。
- [x] 1.3 确认入口和规则只引用规范路径与门禁摘要，不复制完整采集规范正文。

## 2. 技能检查清单

- [x] 2.1 更新 req 相关技能，在需求生成、完善、评审和转 OpenSpec 前检查 `product_data_collection_observability` 声明、适用层级、N/A 原因和验收项。
- [x] 2.2 更新 opsx 相关技能，在 propose、apply、modify 和 archive 阶段检查采集规范读取、声明、实现前验证和归档验收结果。
- [x] 2.3 更新 sprint 相关技能，在 propose、apply 和 archive 阶段摘要提示采集规范门禁状态，并避免复制完整规范正文。

## 3. 实现级校验脚本与测试

- [x] 3.1 新增或增强 `scripts/validate-product-data-observability-gates.py`，检查 `AGENTS.md`、相关 rules、req / opsx / sprint 技能是否引用采集规范门禁。
- [x] 3.2 为脚本增加 Change、REQ、Sprint 或当前 diff 聚焦参数，默认不扫描全部历史 archive。
- [x] 3.3 实现路径级和语义级触发识别，覆盖 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装和 App 请求封装。
- [x] 3.4 校验命中目标是否存在 `product_data_collection_observability` 或等价固定声明，并检查 `affected_layers`、`reason`、`validation` 和 N/A 原因质量。
- [x] 3.5 补充自动化测试，覆盖入口缺失、声明缺失、N/A 原因过短、聚焦扫描和成功摘要。

## 4. 验证与追踪

- [x] 4.1 运行 `python scripts/validate-product-data-observability-gates.py --change add-product-data-collection-observability-hard-gate` 或等价聚焦校验，并记录摘要。
- [x] 4.2 运行 `python scripts/validate-openspec-language.py` 和 `openspec validate add-product-data-collection-observability-hard-gate --strict`。
- [x] 4.3 运行 Workflow Sync，确认 `REQ-0127-product-data-collection-observability-hard-gate`、`add-product-data-collection-observability-hard-gate` 和 `sprint-026` 范围状态一致。
- [x] 4.4 更新 Change `acceptance.md` 与 `trace.md`，记录采集规范门禁声明、校验结果、API/DB/Orval/Web/小程序/App 影响和 N/A 边界。
