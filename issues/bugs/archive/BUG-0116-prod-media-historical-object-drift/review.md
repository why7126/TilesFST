---
bug_id: BUG-0116-prod-media-historical-object-drift
title: 生产历史媒体对象与缩略图存在规范漂移评审
severity: high
review_result: approved
reviewed_at: 2026-08-04 10:46:13
reviewer:
created_at: 2026-08-04 10:46:13
updated_at: 2026-08-04 10:46:13
---

# 生产历史媒体对象与缩略图存在规范漂移评审

## 评审结论

结论：确认修复，状态为 `approved`。

本 BUG 覆盖生产历史媒体对象治理，影响 SKU 商品图片、品牌 Logo 和品牌证书图片三类对象。缺陷包已补齐 `bug.md`、`root-cause.md`、`workaround.md`、`acceptance.md` 和 `trace.md`，根因、影响范围、临时规避边界和回归验收均已明确，允许进入 `/bug-opsx` 与后续 Sprint 规划。

## 评审清单

| 项目 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 生产历史数据可通过 dry-run 审计复现；根因指向对象存储 key 规则演进后未完成统一历史数据治理。 |
| 严重等级合理 | 通过 | `high` 合理；问题影响多端媒体展示性能、对象 key 治理、发布媒体验收和生产批处理安全。 |
| 回归验收明确 | 通过 | `acceptance.md` 已按媒体 BUG 四联模板覆盖 `key`、`object`、`URL`、`render`，并拆出 SKU、品牌 Logo、证书图片三条验收线。 |
| hotfix 路径 | 不采用 | 本缺陷涉及生产数据审计、备份、dry-run、apply、幂等和二次验收，不适合绕过 OpenSpec 和 Sprint 的热修路径。 |

## 修复前置条件

- 必须先通过 `/bug-opsx BUG-0116` 创建 OpenSpec Change。
- 来源于 BUG 的 Change 在 `/opsx-apply` 前必须纳入 Sprint 正式范围。
- 生产 apply 前必须完成数据库与对象存储备份，并保留 dry-run 摘要。
- 不得在修复中泄露生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

## 后续建议

下一步执行：

```bash
/bug-opsx BUG-0116
```
