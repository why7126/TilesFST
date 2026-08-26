---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-26 20:26:00
---

# 测试规范

后端使用 pytest；前端使用 Vitest/Testing Library；接口变更必须补充集成测试。

## 契约变更与测试夹具

- API / Schema / 表单校验 / Workflow snapshot / 发布治理契约变更时，MUST 同步更新测试夹具、helper 与最小合法 payload，禁止测试继续提交已废弃或后端生成字段。
- 共享测试 helper SHOULD 使用最小合法输入；例如类目创建只提交 `name`、`sort_order` 等客户端仍可写字段，不提交由后端生成的 `code`。
- 测试读取 OpenSpec Change 文件时 MUST 兼容 active 与 archive 路径；优先复用 `tests/path_helpers.py` 的 `resolve_change_file()`，禁止只硬编码 `openspec/changes/<change-id>/...`。
- `/opsx-archive`、`/sprint-archive` 或发布准备前，SHOULD 运行相关 pytest，优先发现 archived path residual、fixture/schema drift 和测试 helper payload invalid。

## 根因证据与测试回扣

- BUG 修复、验收返修和测试失败分析 SHOULD 回扣 `rules/root-cause-evidence.md`：测试证据可作为根因 confirmed 的证据之一，但必须能定位到测试名、失败/通过摘要和对应行为。
- 当根因状态为 `unknown`、`hypothesis` 或 `probable` 时，测试计划应说明仍需补充的复现、日志、截图或回归证据。
- 触达 BUG 根因或返修证据时，优先运行聚焦校验：`python scripts/validate-root-cause-evidence.py --bug <BUG-id>` 或 `--change <change-id>`。

## 产品数据采集与链路观测测试门禁

涉及 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装的变更，MUST 读取 `docs/standards/product-data-collection-observability.md`，并补充或声明 `product_data_collection_observability`、`affected_layers`、N/A 原因与验证摘要：行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期、旧数据兼容、OpenAPI / Orval 和端侧链路 ID 透传验证。

相关 Change SHOULD 运行 `python scripts/validate-product-data-observability-gates.py --change <change-id>` 或等价聚焦校验；失败时必须先补齐声明字段、N/A 原因或验收证据。
