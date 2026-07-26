---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
review_result: approved
reviewed_at: 2026-07-23 11:36:25
created_at: 2026-07-23 11:36:25
updated_at: 2026-07-23 22:59:48
reviewer: AI
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
related_change: fix-admin-banner-create-schema-drift
---

# Review - BUG-0083 生产环境创建品牌类型 Banner 保存接口返回 500

## 评审结论

确认修复，状态评审通过。

该问题发生在生产环境管理端，用户明确观测到 `POST https://tilesfst.wjoyhappy.site/api/v1/admin/banners` 返回 `500 Internal Server Error`。缺陷与已归档的 `BUG-0075-prod-admin-brand-banner-save-fails` 属于同一能力域，且表现为历史修复后仍无法保存品牌类型 Banner，具备回归或残留缺陷特征。

当前缺陷包已补齐 `bug.md`、`root-cause.md`、`workaround.md`、`acceptance.md` 与 `trace.md`。虽然仍需生产日志最终确认具体 SQL 异常，但现有证据足以支持进入修复流程：当前创建 SQL 会写入完整 Banner 字段，而历史 MySQL 兼容迁移只聚焦 `brand_id`，生产旧表如果缺失 `image_source`、`sku_gallery_asset_id`、`topic_id`、`valid_from`、`valid_to`、`remark` 等字段，仍会触发 500。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 已有生产接口 500 证据；结合历史 BUG-0075 与当前创建 SQL，DB drift / 部署迁移缺口判断充分 |
| 严重等级合理 | 通过 | 生产运营无法创建品牌类型 Banner，影响品牌导流与线上内容配置，`high` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖生产 MySQL drift、幂等迁移、品牌 Banner 新增/编辑、错误场景不裸 500 和生产 smoke |
| 是否需要 hotfix | 倾向需要 | 生产功能已阻断，且是历史修复残留/回归；建议按高优先级修复，必要时走 hotfix |

## 处理建议

1. 先执行 `/bug-opsx BUG-0083-prod-admin-brand-banner-save-500` 创建修复 Change。
2. 修复设计优先覆盖生产 MySQL `banners` 表完整 schema drift，而不是只补单个字段。
3. 实现阶段补充 MySQL 兼容迁移测试，覆盖旧表缺失多个 Banner 字段时的幂等补齐。
4. 修复验收必须提供生产或等价目标 MySQL drift 检查结果，以及 `POST /api/v1/admin/banners` 创建品牌类型 Banner 成功证据。
5. 在执行 `/opsx-apply` 前，将该 BUG 与修复 Change 纳入 Sprint 正式范围。

## 后续命令

```bash
/bug-opsx BUG-0083-prod-admin-brand-banner-save-500
```
