---
bug_id: BUG-0110-miniapp-card-banner-thumbnail-usage
review_status: approved
reviewed_at: 2026-08-03 08:27:19
reviewer: AI
created_at: 2026-08-03 08:27:19
updated_at: 2026-08-03 08:27:19
severity: high
hotfix_required: false
related_requirement: null
related_bug: BUG-0100-thumbnail-size-equals-original
---

# 缺陷评审

## 评审结论

批准修复。该缺陷影响小程序商品卡片、品牌卡片、证书卡片和 Banner 等多个高频媒体展示场景，若存在原图直载，会造成移动端加载性能回退，并与既有缩略图治理目标不一致。

## 评审清单

- [x] 可复现或根因充分：已明确需核查各小程序展示组件是否统一优先读取缩略图 URL，并保留降级策略。
- [x] 严重等级合理：`high` 合理，问题影响多个高频展示场景和加载性能；暂未确认功能不可用或数据损坏，不升级为 `critical`。
- [x] 回归验收明确：`acceptance.md` 已覆盖商品卡片、品牌卡片、证书卡片、Banner、缩略图缺失降级和详情/预览不回归。
- [x] 是否需 hotfix 路径：暂不需要 hotfix；建议进入常规 BUG 修复流程并优先排入后续 Sprint。

## 后续处理

- 可执行 `/bug-opsx BUG-0110` 创建修复 Change。
- 进入 Sprint 前需确保该 BUG 保持 `approved` 状态，并在 Sprint 规划中纳入正式范围。
