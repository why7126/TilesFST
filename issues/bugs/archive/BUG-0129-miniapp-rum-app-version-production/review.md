---
bug_id: BUG-0129-miniapp-rum-app-version-production
review_status: approved
created_at: 2026-08-12 14:21:57
updated_at: 2026-08-12 14:21:57
reviewed_at: 2026-08-12 14:21:57
reviewer: user
decision: approve
---

# 评审结论

BUG-0129 确认为需要修复，评审通过。

# 评审清单

- [x] 可复现或根因充分：小程序 RUM 与管理后台性能观测口径不一致已有代码证据，覆盖版本号、request_id、指标标签、空态和聚合分组展示。
- [x] 严重等级合理：`medium`，不阻断主流程，但影响性能观测可信度与排障效率。
- [x] 回归验收明确：`acceptance.md` 已覆盖小程序上报、管理端展示、完整分组键、空态样式、安全隐私与 Web RUM 回归。
- [x] 是否需 hotfix 路径：暂不需要 hotfix，可进入常规 Sprint 修复。

# 批准范围

批准同一修复范围内处理以下问题：

1. 小程序 `app_version` 不再显示 `production`，与 Web 管理后台使用统一产品版本号口径。
2. 小程序 RUM 样本补齐可追踪的 `request_id`。
3. 小程序指标名在管理后台展示为中文可读名称。
4. 性能观测列表空态样式对齐管理端表格体验。
5. 聚合列表展示完整分组键，补充网络和设备维度，避免隐藏分组维度造成疑似重复项。

# 后续建议

先纳入 Sprint，再创建 BUG 修复 Change。
