---
created_at: 2026-07-19 18:26:06
updated_at: 2026-07-19 19:29:18
---

# Tasks

- [x] 1. 修复首页快捷入口路由
  - [x] 1.1 将「新品榜」入口跳转调整为 `/pages/product-list/index?section=new`。
  - [x] 1.2 将「热销榜」入口跳转调整为 `/pages/product-list/index?section=hot`。

- [x] 2. 修复首页推荐模块查看更多路由
  - [x] 2.1 将「新品推荐」查看更多调整为商品列表页 `section=new`。
  - [x] 2.2 将「热销推荐」查看更多调整为商品列表页 `section=hot`。

- [x] 3. 同步小程序运行脚本
  - [x] 3.1 同步 `src/miniapp/pages/index/index.ts` 与 `src/miniapp/pages/index/index.js` 的路由逻辑。
  - [x] 3.2 确认搜索框、搜索关键词入口和 Banner `jump_type=search` 仍进入搜索页。

- [x] 4. 补充回归测试
  - [x] 4.1 更新 `tests/test_miniapp_static.py`，断言首页推荐和榜单入口使用 `/pages/product-list/index?section=`。
  - [x] 4.2 断言首页推荐和榜单入口不再使用 `/pages/search/index?section=`。
  - [x] 4.3 运行相关小程序静态测试。

- [x] 5. 验收与知识沉淀
  - [x] 5.1 在微信开发者工具人工验证 4 个入口进入商品列表页。
  - [x] 5.2 如修复过程暴露可复用事故经验，补充 `docs/knowledge-base/incidents/`。
