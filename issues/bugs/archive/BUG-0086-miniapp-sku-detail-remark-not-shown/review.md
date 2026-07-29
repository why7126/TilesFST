---
bug_id: BUG-0086-miniapp-sku-detail-remark-not-shown
status: done
created_at: 2026-07-28 22:36:32
updated_at: 2026-07-29 07:55:06
reviewed_at: 2026-07-28 22:36:32
review_result: approved
reviewer:
---

# BUG Review

## 评审结论

确认修复，状态批准为 `approved`。

该缺陷描述清晰：微信小程序商品详情页未展示商品/SKU 已维护的备注说明信息，造成商品补充说明缺失，影响商品资料完整浏览体验。

## 评审清单

- [x] 可复现或根因充分
- [x] 严重等级合理
- [x] 回归验收明确
- [x] 已判断是否需要 hotfix 路径

## 严重等级确认

严重等级维持 `medium`。

理由：

- 商品详情页整体访问不被阻断。
- 备注说明属于商品资料补充信息，缺失会影响客户或店主理解商品细节。
- 问题范围集中在小程序商品详情页字段展示链路，适合通过常规 fix Change 修复并回归。

## Hotfix 判断

暂不按 hotfix 处理。

理由：

- 当前缺陷不影响商品详情页主路径访问、图片/视频浏览、收藏或分享等关键操作。
- 后续可通过 `/bug-opsx` 创建 OpenSpec fix Change，并在 Sprint 中安排字段映射、页面展示和真机验收。

## 后续动作

- 可执行 `/bug-opsx BUG-0086-miniapp-sku-detail-remark-not-shown` 创建 OpenSpec fix Change。
- 修复时应确认商品/SKU 详情接口、端侧字段映射和页面模板展示链路一致。
- 修复验收必须覆盖非空备注说明展示、空备注说明空态、页面主要信息不回归。
