---
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: approved
review_result: approved
reviewed_at: 2026-07-19 15:47:09
created_at: 2026-07-19 15:47:09
updated_at: 2026-07-19 15:47:09
reviewer: product
severity: medium
related_requirement: REQ-0047-product-list-common-component-application
related_change:
source_change: add-miniapp-product-list-component
---

# Review - BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页

## 评审结论

通过，确认需要修复。

BUG-0067 描述的是微信小程序首页新品/热销推荐入口仍跳转搜索页，而非进入商品列表页的问题。当前缺陷具备明确复现路径、影响范围、根因分析和回归验收标准，满足进入后续 `/bug-opsx` 的条件。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 首页 `openQuickEntry` 与 `openSection` 明确将 `section` 跳转到 `/pages/search/index`；运行态 `.js` 同样存在该逻辑 |
| 严重等级合理 | 通过 | 标记为 `medium` 合理；影响首页核心推荐入口，但不涉及数据损坏、安全、权限或主流程完全不可用 |
| 回归验收明确 | 通过 | `acceptance.md` 已列出 AC-BUG-001 至 AC-BUG-008，覆盖 4 个入口、搜索场景不回归、TS/JS 同步和静态测试 |
| 是否需 hotfix 路径 | 不需要 | 暂无线上阻断、安全风险或数据风险；按常规 `fix-*` Change 修复即可 |

## 审核意见

- 本 BUG 应作为 `add-miniapp-product-list-component` 的入口应用偏差处理，后续修复 Change 应使用新的 `fix-*`。
- 修复重点应聚焦微信小程序首页的新品榜、热销榜和推荐模块「查看更多」路由，不扩大到商品列表页 UI、后端 section 语义或推荐算法调整。
- 修复时必须同步 `src/miniapp/pages/index/index.ts` 与微信开发者工具实际加载的 `src/miniapp/pages/index/index.js`。
- 建议在 `tests/test_miniapp_static.py` 增加静态断言，防止 `/pages/search/index?section=` 再次作为首页新品/热销入口目标。

## 后续动作

```text
/bug-opsx BUG-0067-home-recommendation-list-entry-routing
```
