---
bug_id: BUG-0067-home-recommendation-list-entry-routing
status: done
created_at: 2026-07-19 15:43:52
updated_at: 2026-07-19 19:31:31
classification: code/test
related_requirement: REQ-0047-product-list-common-component-application
source_change: add-miniapp-product-list-component
---

# Root Cause - BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页

## 直接原因

微信小程序首页的新品/热销入口仍使用搜索页旧路由：

- `src/miniapp/pages/index/index.ts` 中 `openQuickEntry` 对 `entry.section` 执行 `/pages/search/index?section=...`。
- `src/miniapp/pages/index/index.ts` 中 `openSection` 对推荐模块「查看更多」执行 `/pages/search/index?section=...`。
- 微信开发者工具实际加载的 `src/miniapp/pages/index/index.js` 中存在相同逻辑。

商品列表页已经支持 `section=new|hot`，但首页推荐入口没有迁移到 `/pages/product-list/index?section=...`，因此用户从新品榜、热销榜或推荐模块查看更多进入时被带到搜索页。

## 根本原因

根本原因是商品列表页新增后，首页推荐入口的路由契约没有同步调整，且静态测试没有覆盖“入口必须进入商品列表页”这一行为。

当前项目已有以下能力：

- `src/miniapp/pages/product-list/index.ts` 会读取 `section`，并将 `new` / `hot` 映射为「新品榜」/「热销榜」标题。
- `/api/v1/miniapp/products` 支持 `section: new|hot`。
- `MiniappHomeService.search_products` 将 `section=new` 映射为新品过滤，将 `section=hot` 映射为热销优先排序。
- `src/miniapp/README.md` 明确商品列表页用于承接分类、搜索、品牌、新品榜和热销榜等入口。

但首页实现仍保留旧的搜索页承接方式，导致 REQ-0047 的商品列表入口应用未覆盖首页推荐与榜单入口。

## 触发条件

满足以下任一操作即可触发：

1. 在微信小程序首页点击「新品榜」。
2. 在微信小程序首页点击「热销榜」。
3. 在微信小程序首页点击「新品推荐」模块的「查看更多」。
4. 在微信小程序首页点击「热销推荐」模块的「查看更多」。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是。首页 `openQuickEntry` 与 `openSection` 路由目标错误 |
| test | 是。缺少首页推荐入口必须跳转商品列表页的静态回归断言 |
| design | 否。当前证据显示是已定义入口策略未接入，不是新设计缺失 |
| api | 否。后端商品列表接口已支持 `section=new|hot` |
| db | 否。当前问题不涉及数据库结构或数据写入 |
| security | 否。当前问题不涉及权限绕过或敏感信息泄露 |

## 影响判断

该问题影响微信小程序首页推荐入口的用户路径与商品列表页应用闭环。数据接口和商品详情主流程未发现不可用，但推荐模块无法正确承接到新品/热销商品列表，会削弱首页推荐转化与 REQ-0047 的入口覆盖可信度。
