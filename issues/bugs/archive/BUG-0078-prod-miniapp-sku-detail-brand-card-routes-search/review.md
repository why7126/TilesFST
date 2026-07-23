---
bug_id: BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search
status: done
created_at: 2026-07-21 14:56:26
updated_at: 2026-07-22 09:00:40
reviewed_at: 2026-07-21 14:56:26
review_result: approved
reviewer: AI
severity: medium
related_requirement: REQ-0044-miniapp-sku-detail-page
related_change:
---

# Review - BUG-0078 生产环境小程序商品详情页品牌卡片误跳搜索页

## 评审结论

批准修复。

该缺陷为生产环境微信小程序 SKU 商品详情页品牌入口跳转目标错误。根因已定位到 SKU 详情聚合接口返回的 `brand.brand_entry_path` 指向搜索页，而不是品牌详情页；复现条件明确，影响范围清晰，验收标准可回归。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | SKU 详情接口返回搜索页路径，前端 `brand-card` 按 `entryPath` 跳转，链路清晰 |
| 严重等级合理 | 通过 | 生产核心详情页入口错误，影响品牌浏览链路；不阻断商品主体浏览，暂定 `medium` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖 API 返回路径、品牌详情页跳转、小程序回归和非目标边界 |
| 是否需 hotfix 路径 | 不需要 | 暂无崩溃、白屏、数据风险或权限风险；建议纳入常规 BUG 修复流程 |

## 修复门禁

- 状态批准后允许执行 `/bug-opsx BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search`。
- 状态批准后允许纳入 Sprint 规划。
- 来源于该 BUG 的 OpenSpec Change 在 `/opsx-apply` 前仍必须先纳入正式 Sprint 范围。

## 评审备注

修复建议保持最小范围：优先调整 SKU 详情接口返回的 `brand.brand_entry_path` 为 `/pages/brand-detail/index?brandId=<brand_id>`，并补充后端回归测试。若字段结构不变，仅字段值修正，预计不需要 OpenAPI / Orval；实际执行时仍需按 API 变更规则复核。
