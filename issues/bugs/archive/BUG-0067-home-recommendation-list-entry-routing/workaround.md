---
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: done
created_at: 2026-07-19 15:43:52
updated_at: 2026-07-19 19:31:31
related_requirement: REQ-0047-product-list-common-component-application
source_change: add-miniapp-product-list-component
---

# Workaround - BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页

## 临时规避方案

暂无可完全等价的产品侧规避方案。修复前，用户仍可通过以下方式浏览公开商品，但不能等价替代新品榜和热销榜入口：

- 从「分类」页进入某个分类的商品列表页。
- 从搜索入口输入关键词后浏览搜索结果。
- 从首页新品推荐或热销推荐中直接点击单个商品进入详情页。

## 可接受的临时使用边界

在修复前，可按以下边界临时使用：

- 内部联调可继续使用商品列表页直接路径 `/pages/product-list/index?section=new` 和 `/pages/product-list/index?section=hot` 验证后端 `section` 能力。
- 产品演示时应避开首页「新品榜」「热销榜」和推荐模块「查看更多」作为推荐列表入口，或提前说明该入口路由待修复。
- 用户若需要查看更多商品，可临时从分类页或搜索页进入商品列表和搜索结果。

## 不建议的规避方式

- 不建议把新品榜/热销榜入口解释为搜索入口；这会改变产品语义。
- 不建议修改商品列表页标题或后端 `section` 语义来适配当前错误跳转。
- 不建议绕过 OpenSpec 流程直接修改 `src/miniapp/pages/index/*`。

## 修复前风险

| 风险 | 说明 |
|---|---|
| 推荐流量承接失败 | 首页推荐入口无法进入对应商品列表，用户路径被打断 |
| 验收遗漏 | 现有静态测试只确认入口和商品列表页存在，未确认入口路由目标 |
| 重复误跳 | `.ts` 与运行态 `.js` 同时存在错误逻辑，单改其一会导致开发者工具与源码意图不一致 |

## 推荐处理

完成 BUG 评审后创建 `fix-*` Change，集中修复首页新品/热销入口路由，并补充静态测试覆盖 `index.ts` 与 `index.js` 的 product-list 跳转。
