---
bug_id: BUG-0067-home-recommendation-list-entry-routing
title: 首页推荐模块查看更多和榜单入口误跳搜索页
severity: medium
status: approved
owner: product
discovered_at: 2026-07-19 15:26:47
environment: local|miniapp
related_requirement: REQ-0047-product-list-common-component-application
related_change:
source_change: add-miniapp-product-list-component
created_at: 2026-07-19 15:39:21
updated_at: 2026-07-19 15:47:09
---

# BUG-0067 首页推荐模块查看更多和榜单入口误跳搜索页

## 现象

微信小程序首页的推荐入口存在路由偏差：点击「新品推荐」和「热销推荐」模块的「查看更多」，以及点击快捷入口中的「新品榜」「热销榜」，当前都会进入搜索页；按产品列表页能力说明和用户反馈，这些入口应进入对应的商品列表页。

该问题与 `REQ-0047-product-list-common-component-application` 相关。该需求已交付商品列表页，用于承接分类、搜索、品牌、新品榜和热销榜等入口；当前首页仍保留搜索页旧跳转，导致新品/热销榜入口未进入商品列表承接页。

## 复现步骤

1. 打开微信小程序首页 `pages/index/index`。
2. 点击快捷入口「新品榜」。
3. 返回首页，点击快捷入口「热销榜」。
4. 返回首页，点击「新品推荐」模块右侧「查看更多」。
5. 返回首页，点击「热销推荐」模块右侧「查看更多」。
6. 观察实际进入的页面路径和页面标题。

## 期望结果

- 点击「新品榜」或「新品推荐」的「查看更多」时，应进入商品列表页，并携带 `section=new`，页面标题展示「新品榜」或等价的新品推荐商品列表标题。
- 点击「热销榜」或「热销推荐」的「查看更多」时，应进入商品列表页，并携带 `section=hot`，页面标题展示「热销榜」或等价的热销推荐商品列表标题。
- 商品列表页应通过 `/api/v1/miniapp/products` 携带 `section=new|hot` 获取公开 SKU、分页状态和筛选 facets。
- 搜索页仍只用于搜索入口、搜索关键词跳转和 Banner `jump_type=search` 等搜索场景，不应承接新品/热销榜入口。

## 实际结果

- `openQuickEntry` 对 `entry.section` 执行 `wx.navigateTo({ url: /pages/search/index?section=... })`，导致「新品榜」「热销榜」进入搜索页。
- `openSection` 对「查看更多」执行 `wx.navigateTo({ url: /pages/search/index?section=... })`，导致「新品推荐」「热销推荐」进入搜索页。
- `src/miniapp/pages/index/index.ts` 与微信开发者工具实际加载的 `src/miniapp/pages/index/index.js` 均存在相同问题。
- 商品列表页和后端接口已支持 `section=new|hot`，但首页推荐入口没有使用该能力。

## 影响范围

| 影响面 | 说明 |
|---|---|
| 微信小程序首页 | 「新品榜」「热销榜」快捷入口，以及新品/热销推荐模块「查看更多」入口跳转错误 |
| 商品列表页应用 | `pages/product-list/index.*` 已具备 `section=new|hot` 标题与请求能力，但首页入口未接入 |
| 用户浏览路径 | 用户无法从首页推荐入口直达新品/热销商品列表，只能误入搜索页，推荐流量承接被打断 |
| 静态回归覆盖 | 现有 `tests/test_miniapp_static.py` 仅确认首页入口存在和商品列表页存在，未断言首页推荐入口必须进入 product-list |

## 严重等级说明

严重等级标记为 `medium`。该问题影响首页核心推荐入口和商品列表页承接路径，属于用户可见的导航行为错误；但搜索页、商品详情、商品列表接口和数据本身未发现不可用或损坏，也不涉及权限、安全或数据泄露，因此不标记为 `high`、`critical` 或 `blocker`。

## 关联证据

| 类型 | 路径 / 位置 | 说明 |
|---|---|---|
| 首页 TS | `src/miniapp/pages/index/index.ts` | `openQuickEntry` 与 `openSection` 当前把 `section` 跳到 `/pages/search/index` |
| 首页运行 JS | `src/miniapp/pages/index/index.js` | 微信开发者工具实际加载文件，同样把 `section` 跳到 `/pages/search/index` |
| 首页模板 | `src/miniapp/pages/index/index.wxml` | 「新品榜」「热销榜」绑定 `openQuickEntry`；「查看更多」绑定 `openSection` |
| 商品列表页 | `src/miniapp/pages/product-list/index.ts` | 已读取 `section`，并将 `new` / `hot` 映射为「新品榜」/「热销榜」标题 |
| 小程序说明 | `src/miniapp/README.md` | 明确商品列表页用于承接分类、搜索、品牌、新品榜和热销榜等入口 |
| 后端接口 | `src/backend/app/api/v1/miniapp.py` | `/api/v1/miniapp/products` 支持 `section: new|hot` |
| 后端服务 | `src/backend/app/services/miniapp_home_service.py` | `section=new` 映射 `only_new`，`section=hot` 映射 `hot_first` |
| 后端 Repository | `src/backend/app/repositories/miniapp_home_repository.py` | `only_new` 添加新品过滤，`hot_first` 使用热销优先排序 |

## 后续建议

下一步执行：

```text
/bug-complete BUG-0067-home-recommendation-list-entry-routing
```

后续修复应通过 `fix-*` OpenSpec Change 处理，不应直接修改 `src/` 绕过流程。修复时建议同步修改 `src/miniapp/pages/index/index.ts` 和 `src/miniapp/pages/index/index.js`，并在 `tests/test_miniapp_static.py` 增加首页推荐入口必须进入 `/pages/product-list/index?section=` 的静态断言。
