---
created_at: 2026-07-19 18:26:06
updated_at: 2026-07-19 18:26:06
---

# Design

## Bug Analysis Report

### 现象

首页四个推荐相关入口存在路由偏差：

- 快捷入口「新品榜」进入 `/pages/search/index?section=new`。
- 快捷入口「热销榜」进入 `/pages/search/index?section=hot`。
- 「新品推荐」模块「查看更多」进入 `/pages/search/index?section=new`。
- 「热销推荐」模块「查看更多」进入 `/pages/search/index?section=hot`。

期望行为是进入商品列表页，并由商品列表页通过 `section=new|hot` 请求公开 SKU、展示标题和分页筛选状态。

### 根因分类

- `code`：首页 `openQuickEntry` 与 `openSection` 保留旧搜索页路由。
- `test`：现有小程序静态测试没有断言首页推荐入口必须进入商品列表页。

严重等级：`medium`。这是用户可见导航行为错误，影响首页推荐流量承接，但不涉及权限、安全、数据损坏或核心接口不可用。

### 关联项

- BUG：`BUG-0067-home-recommendation-list-entry-routing`
- 父需求：`REQ-0047-product-list-common-component-application`
- 来源 Change：`add-miniapp-product-list-component`
- Sprint：`sprint-009`

## 修复方案

1. 将首页 `entry.section` 类快捷入口统一导航到 `/pages/product-list/index?section=${section}`。
2. 将首页推荐模块「查看更多」统一导航到 `/pages/product-list/index?section=${section}`。
3. 保持搜索入口与搜索 Banner 的搜索页跳转不变，避免扩大行为范围。
4. 同步维护 `src/miniapp/pages/index/index.ts` 和 `src/miniapp/pages/index/index.js`，确保微信开发者工具实际加载逻辑与源码一致。
5. 在静态测试中新增断言：
   - 首页源码包含 `/pages/product-list/index?section=`。
   - 首页推荐/榜单入口不再使用 `/pages/search/index?section=`。
   - 搜索入口仍保留搜索页路由。

## 测试策略

- 静态测试：补充 `tests/test_miniapp_static.py` 对首页 section 路由目标的断言。
- 小程序人工验收：在微信开发者工具分别点击「新品榜」「热销榜」「新品推荐查看更多」「热销推荐查看更多」。
- 接口回归：复用现有 `/api/v1/miniapp/products?section=new|hot` 测试，确认公开 SKU 查询仍可用。

## 非目标

- 不新增商品列表页 UI 能力。
- 不新增或修改后端 API 契约。
- 不调整新品定义、热销排序算法或推荐算法。
- 不改动 Web 管理端、店主 Web 展示端或小程序其它 Tab 导航结构。
