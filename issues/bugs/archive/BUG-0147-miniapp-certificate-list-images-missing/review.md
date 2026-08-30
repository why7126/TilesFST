---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
review_result: approved
reviewed_at: 2026-08-30 10:31:55
created_at: 2026-08-30 10:31:55
updated_at: 2026-08-30 10:31:55
reviewer: AI
---

# 评审结论

评审通过，确认需要修复。

# 评审依据

| 检查项 | 结论 | 说明 |
|---|---|---|
| 根因状态 | 通过 | `root_cause_status: confirmed`，且根因证据链包含用户截图、生产接口只读请求和相关代码定位。 |
| 严重等级 | 通过 | `high` 合理；生产小程序底部一级入口的图片类证书全部显示占位，影响证书可信展示。 |
| 回归验收 | 通过 | `acceptance.md` 已覆盖接口字段、公开安全、品牌证书 key 前缀、对象存储、URL 和小程序 render evidence。 |
| Hotfix 路径 | 建议优先排入最近 Sprint | 问题发生在生产展示链路，但未阻断页面访问；建议按高优先级进入 Sprint 后创建修复 Change。 |

# 修复范围建议

- 后端公开证书列表 API：保证图片类证书返回可访问 `thumbnail_url`。
- 证书媒体 key / URL 一致性：图片证书使用 `images/default/brand-certificates/`，PDF / 文档证书使用 `files/default/brand-certificates/`。
- 历史媒体数据：补充迁移、缩略图回填 dry-run / apply / 幂等证据。
- 小程序回归：证书列表页真实缩略图展示和失败降级。

# 评审结果

状态：`approved`

推荐后续路径：先纳入 Sprint，再创建 OpenSpec 修复 Change。
