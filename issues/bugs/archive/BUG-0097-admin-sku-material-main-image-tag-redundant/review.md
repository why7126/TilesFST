---
bug_id: BUG-0097-admin-sku-material-main-image-tag-redundant
title: 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签
status: done
severity: low
review_result: approved
reviewed_at: 2026-07-31 15:06:59
reviewer:
hotfix_required: false
created_at: 2026-07-31 15:06:59
updated_at: 2026-07-31 20:54:53
---

# Review

## 评审结论

确认修复，状态为 `approved`。该 BUG 可进入 `/bug-opsx` 创建修复 Change，也可纳入 Sprint 正式范围。

## 评审清单

- [x] 可复现或根因充分：素材列渲染逻辑会基于 `has_main_image` 展示「主图已设 / 缺主图」标签；在有图片即有主图兜底的业务规则下，正向「主图已设」标签为冗余展示。
- [x] 严重等级合理：严重等级为 `low`，不阻断 SKU 数据维护或前台展示，主要影响管理端列表扫描体验。
- [x] 回归验收明确：acceptance.md 已覆盖正向标签移除、素材数量保留、素材不完整识别、列表布局和 SKU 维护操作不受影响。
- [x] 是否需 hotfix 路径：不需要 hotfix，可随常规 BUG 修复流程进入 OpenSpec Change 与 Sprint。

## 评审说明

该问题属于管理后台 Web 展示冗余，不涉及 API 契约、数据库结构、权限边界或上传存储策略变化。修复时应重点确保移除「主图已设」后，图片/视频数量仍保留可用判断能力；验收返修要求页面同步删除素材完整度条件筛选。

## 后续动作

下一步执行 `/bug-opsx BUG-0097`，创建对应修复 Change。
