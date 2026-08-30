---
created_at: 2026-08-30 12:26:56
updated_at: 2026-08-30 12:26:56
---

# 设计

## 设计目标

建立一套统一的环境分层 evidence 语义，让开发验收、体验版验证、生产发布验证和发布后跟进各自有清晰的阻塞范围。规范应帮助 AI 和人工评审准确表达“当前阶段已验证什么、不能验证什么、后续由哪个阶段承接”，避免开发阶段被生产环境不可用卡死，也避免用开发证据冒充生产验证。

## 分层模型

每条环境相关 evidence SHOULD 具备以下字段或等价表格列：

| 字段 | 含义 |
|---|---|
| `target_environment` | `development`、`trial`、`production` 或 `not_applicable` |
| `phase` | `dev_acceptance`、`trial_acceptance`、`release_prepare`、`production_publish` 或 `post_release` |
| `blocking_scope` | 当前证据缺口阻塞的命令或阶段，例如 `opsx.archive`、`sprint.archive`、`release-publish:production` |
| `classification` | `prepare_evidence_missing`、`production_only_pending`、`environment_unavailable`、`blocked`、`not_applicable` 或 `follow_up` |
| `evidence_ref` | 命令摘要、截图、报告、artifact 或人工摘要，必须脱敏且可复核 |

## 阶段门禁

开发验收阶段允许使用本地测试、开发 API smoke、微信 DevTools 截图、DevTools Network 摘要、静态校验、Docker 本地或等价开发环境证据。若生产环境、体验版入口、真机设备或生产对象不可用，应记录为后置证据，不阻塞 `opsx.archive`，除非该 Change 的目标明确是生产执行或生产发布。

体验版验证阶段用于验证小程序体验版入口、合法域名、真机或等价手机入口的关键页面和媒体资源。缺少体验版证据不得写作体验版通过；若当前命令只处于开发归档，可记录为 `production_only_pending`、`follow_up` 或发布检查项。

生产发布阶段必须重新读取发布对象目标环境。`release_target.environment=production` 时，生产 env、备份、公开 API、生产 no-fallback 媒体、生产 smoke、回滚准备等证据按发布范围参与强门禁；`development` 时仅作为后续生产发布待办。

## 文档归属

- `rules/testing.md` 记录通用测试与环境证据边界。
- `rules/release.md` 作为生产发布门禁事实源，保留已有 release target 语义并补充跨阶段引用。
- `rules/media.md` 记录媒体证据与生产对象验证后置口径。
- `docs/standards/miniapp-device-evidence-template.md` 和 `docs/standards/media-bug-four-point-acceptance-template.md` 记录字段模板与示例。
- `.agents/skills/*/SKILL.md` 只保留命令执行摘要和阻塞分类，不复制完整规范正文。

## 产品数据采集与链路观测

本变更只修改治理资产，不新增或修改 API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装运行时代码。

```yaml
product_data_collection_observability:
  applicability: not_applicable
  affected_layers: []
  reason: "纯治理文档与命令说明变更；不改变运行时代码、接口、数据库、日志采集或端侧请求封装。"
  validation: "运行 OpenSpec、目录、上下文预算和文档表达卫生校验。"
```

## 风险与取舍

- 已采纳：用字段化 evidence 表达阻塞范围，避免只靠自然语言解释阶段差异。
- 未采纳：不新增强制生产自动化脚本；生产环境仍依赖发布命令族和人工确认。
- 替代方案：仅修改 `rules/release.md`，但不能覆盖 BUG、Change、小程序和媒体模板中的实际误判场景。
