---
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
review_result: approved
reviewed_at: 2026-08-05 09:48:53
reviewer: project-owner
created_at: 2026-08-05 09:48:53
updated_at: 2026-08-05 09:48:53
---

# Review

## 评审结论

确认修复，状态置为 `approved`。

当前产品真实面向用户不应提供电话拨打、复制门店微信号或复制证书文件链接能力，但现有小程序提交包、后端服务合约和文档测试仍残留电话与剪贴板隐私接口口径。该问题会导致微信小程序提审时“未采集用户隐私”声明与代码扫描结果不一致，影响发布合规。

## 评审清单

- [x] 可复现或根因充分：提审提示与静态代码线索均指向 `wx.makePhoneCall` / `wx.setClipboardData` 残留路径。
- [x] 严重等级合理：`high`，影响小程序提审与发布权限表现，但不是线上全站不可用或数据破坏。
- [x] 回归验收明确：acceptance 已覆盖小程序提交包、后端 home 合约、证书详情失败兜底、文档规格和提审隐私声明。
- [x] 是否需 hotfix 路径：建议优先修复并纳入近期 Sprint；若当前发布必须立即提审，应先完成该修复再提交。

## 后续动作

- 可执行 `/bug-opsx BUG-0117-miniapp-privacy-clipboard-phone-drift` 创建修复 Change。
- 进入实现前需按项目门禁纳入 Sprint。
