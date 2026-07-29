---
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
created_at: 2026-07-28 22:39:18
updated_at: 2026-07-29 07:54:10
reviewed_at: 2026-07-28 22:39:18
review_result: approved
reviewer: AI
severity: medium
related_requirement: REQ-0058-brand-detail-home-page
related_change:
---

# Review - BUG-0087 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序

## 评审结论

批准修复。

该缺陷属于微信小程序品牌详情页已交付能力中的排序规则偏差。根因已定位到品牌详情页商品 Tab 复用 `/api/v1/miniapp/products` 通用默认排序，而当前通用默认排序为 `updated_at DESC, id DESC`，未满足品牌过滤场景下发布时间升序、ID 升序的展示预期。影响范围、非目标和回归验收边界已经明确。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 品牌详情页请求仅携带 `brandId` 与分页参数，后端排序函数当前默认返回更新时间倒序和 ID 倒序，链路清晰 |
| 严重等级合理 | 通过 | 不阻断页面访问或商品详情跳转，但影响品牌页商品陈列顺序、分页稳定性和验收一致性，`medium` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖品牌过滤召回、发布时间升序、ID 升序、分页稳定和搜索/榜单非目标回归 |
| 是否需 hotfix 路径 | 不需要 | 暂无崩溃、白屏、数据损坏、权限或安全风险，建议纳入常规 BUG 修复流程 |

## 修复门禁

- 状态批准后允许执行 `/bug-opsx BUG-0087-miniapp-brand-detail-product-tab-sort-order`。
- 状态批准后允许纳入 Sprint 规划。
- 来源于该 BUG 的 OpenSpec Change 在 `/opsx-apply` 前仍必须先纳入正式 Sprint 范围。

## 评审备注

修复建议保持最小范围：优先在后端品牌过滤场景固化发布时间升序、ID 升序排序，并补充后端回归测试。若仅调整排序逻辑且不改变请求/响应结构，预计不需要 OpenAPI / Orval；若实际新增 `published_at` 字段、排序参数或响应字段，必须同步 DB、API、docs、Orval 和测试。
