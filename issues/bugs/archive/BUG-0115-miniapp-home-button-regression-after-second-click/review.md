---
bug_id: BUG-0115-miniapp-home-button-regression-after-second-click
review_status: approved
reviewed_at: 2026-08-04 09:01:04
reviewed_by: AI
created_at: 2026-08-04 09:01:04
updated_at: 2026-08-04 09:01:04
---

# 评审结论

确认修复，状态批准为 `approved`。

## 评审清单

- [x] 可复现或根因充分：用户反馈与历史 BUG-0109 现象一致，缺陷包已明确同页重复进入、跨页重复进入和第二次点击失效路径。
- [x] 严重等级合理：返回首页按钮覆盖多个小程序核心页面，二次点击失效会阻断深层页面回首页的主要导航路径，`high` 合理。
- [x] 回归验收明确：acceptance.md 已覆盖同页重复点击、跨页面状态隔离、TabBar/非 TabBar 页面、成功/失败/兜底路径释放和真实状态流测试。
- [x] 是否需 hotfix 路径：建议优先纳入最近 Sprint；若体验版或正式版正在对外验收且可稳定复现，可按高优先级 hotfix 处理。

## 评审说明

该问题属于已交付微信小程序全局返回首页能力的回归缺陷。历史修复 `fix-miniapp-home-navigation-repeat-click` 已归档，但当前反馈再次出现“每个页面点击一次后，再一次点击就失效”的同类现象，说明需要重新进入修复流程，并补强真实连续点击状态流测试。

## 后续动作

- 可执行 `/bug-opsx BUG-0115-miniapp-home-button-regression-after-second-click` 创建修复 Change。
- 可通过 `/sprint-propose` 纳入 Sprint 正式范围。
