---
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
title: 管理后台证书列表证书字段额外显示图片或文件名称评审记录
review_result: approved
reviewed_at: 2026-08-03 08:26:56
reviewer: AI
created_at: 2026-08-03 08:26:56
updated_at: 2026-08-03 08:26:56
---

# 评审记录

## 评审结论

确认修复，状态为 `approved`。

## 评审清单

- [x] 可复现或根因充分：已记录管理后台证书列表字段额外显示图片名称、文件名称、对象 key 或原始 URL 的复现路径，根因聚焦在列表展示边界与上传/编辑场景信息混用。
- [x] 严重等级合理：`low`，问题影响列表可读性和上传实现细节暴露，不阻断核心证书维护流程。
- [x] 回归验收明确：`acceptance.md` 已覆盖只展示证书主图和证书名称、不展示文件名/对象 key/URL、无主图占位、列表操作保持正常，以及关联 `BUG-0089` 不回归。
- [x] 是否需 hotfix 路径：不需要。该问题为管理后台展示噪音，适合进入常规 BUG 修复流程。

## 后续动作

- 可执行 `/bug-opsx BUG-0107` 创建修复 Change。
- 可在评审通过后纳入 Sprint 规划。
