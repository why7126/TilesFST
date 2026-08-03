---
bug_id: BUG-0109-miniapp-home-button-one-time-failure
review_result: approved
reviewed_at: 2026-08-03 08:26:07
reviewer:
created_at: 2026-08-03 08:26:07
updated_at: 2026-08-03 08:26:07
---

# 评审结论

确认修复。

# 评审清单

- [x] 可复现或根因充分：缺陷现象明确，复现路径覆盖同页重复进入、跨页进入和返回首页按钮重复点击。
- [x] 严重等级合理：`high` 合理。问题阻断小程序全局返回首页导航路径，影响商品详情、品牌详情、证书详情、搜索结果等关键浏览流程。
- [x] 回归验收明确：`acceptance.md` 已覆盖重复点击、多页面一致性、状态恢复、快速重复点击和体验版回归范围。
- [x] 是否需 hotfix 路径：暂不按 hotfix 处理；建议优先纳入最近 Sprint 修复。如体验版演示或客户验收受阻，可提升为 hotfix。

# 决策

- 状态：`approved`
- 后续允许：`/bug-opsx BUG-0109`
- Sprint 建议：作为高优先级小程序导航缺陷，进入下一次 Sprint 规划时优先排期。
