---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-30 12:55:22
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

## 环境分层验收与生产证据后置

测试证据必须说明目标环境和证明边界。开发阶段可使用 pytest、Vitest、静态校验、开发 API smoke、Docker 本地验证、微信 DevTools 截图或 DevTools Network 摘要支撑 `dev_acceptance`；这些证据不得表述为体验版、真机或生产发布已经通过。

生产环境、生产数据库、生产对象存储、生产公开 API、生产 no-fallback 媒体、生产 smoke、生产真实用户路径、体验版入口或真机设备只有发布后才能获得时，开发阶段验收应记录为 `production_only_pending`、`environment_unavailable`、`follow_up` 或 `not_applicable_for_development`，并明确 `blocking_scope`。除非 Change 目标本身就是生产维护执行或生产发布确认，这类证据缺口不得阻塞 `opsx.archive` 或开发阶段 Sprint 归档。

环境相关 evidence SHOULD 包含或等价记录：

| 字段 | 含义 |
|---|---|
| `target_environment` | `development`、`trial`、`production` 或 `not_applicable` |
| `phase` | `dev_acceptance`、`trial_acceptance`、`release_prepare`、`production_publish` 或 `post_release` |
| `blocking_scope` | 当前缺口阻塞的命令或阶段，例如 `opsx.archive`、`sprint.archive`、`release-publish:production` |
| `classification` | `prepare_evidence_missing`、`production_only_pending`、`environment_unavailable`、`blocked`、`not_applicable` 或 `follow_up` |
| `evidence_ref` | 脱敏命令摘要、截图、报告、artifact 或人工摘要 |

环境分层 evidence 在归档和发布链路中是脚本门禁：

```bash
python scripts/validate-environment-tiered-evidence.py --change <change-id>
python scripts/validate-environment-tiered-evidence.py --sprint <sprint-id>
python scripts/validate-environment-tiered-evidence.py --release-dir releases/<version> --target production
```

该门禁必须阻断：开发证据冒充体验版、真机或生产通过；体验版 / 真机 Network 标记 `passed` 却缺少可定位 evidence；生产发布目标仍遗留 `production_only_pending` 而未重新判定。
