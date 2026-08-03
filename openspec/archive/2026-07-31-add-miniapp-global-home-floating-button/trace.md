---
change_id: add-miniapp-global-home-floating-button
status: applied
source_requirement: REQ-0085-miniapp-global-home-floating-button
change_type: add
created_at: 2026-07-30 23:20:00
updated_at: 2026-07-31 00:08:26
owner: product
---

# Change Trace

## 基本信息

```yaml
change_id: add-miniapp-global-home-floating-button
status: applied
source_requirement: REQ-0085-miniapp-global-home-floating-button
requirement_path: issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/
iteration: sprint-014
change_type: add
capabilities:
  new: []
  modified:
    - miniapp-global-custom-navigation-bar
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
readiness: Ready
prototype:
  miniapp:
    html: issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/prototype/miniapp/home-floating-button.html
    context: issues/requirements/archive/REQ-0085-miniapp-global-home-floating-button/prototype/miniapp/context.md
    png: pending_export
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-013-retrospective.md
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| review.md | present / approved |
| trace.md | present / approved |
| prototype | present / miniapp HTML + context |
| readiness | Ready |

## Impact Analysis

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-global-custom-navigation-bar
```

## Conflict Report

| 来源 | 结论 |
|---|---|
| prototype/web | 不存在，Web UI Explore Gate 不适用 |
| prototype/miniapp/home-floating-button.html | 最高视觉参考，表达首页隐藏、详情页上移避让操作区、列表/错误态可回首页 |
| prototype/miniapp/context.md | 明确非目标：不作为最终 WXML/WXSS，不验证真实设备，不确认最终图标和路由 API |
| acceptance.md | 与原型一致，补充 AC-001 ~ AC-029 与小程序导航 evidence |
| openspec/specs/miniapp-global-custom-navigation-bar/spec.md | 已有顶部返回、胶囊、offset、分享直达规则；本 Change 新增独立返回首页悬浮按钮，不替代顶部返回按钮 |

## PNG Checklist

- [ ] PNG Golden Reference 待后续从 `prototype/miniapp/home-floating-button.html` 导出。
- [ ] DevTools 320/375/430 pt evidence follow_up：当前执行环境未连接微信开发者工具，已用静态测试覆盖页面接入、底部避让 class 与导航兜底，不写作 DevTools 通过。
- [ ] 真机 evidence follow_up：当前无 iOS/Android 真机 evidence，不写作真机通过。

## Apply Evidence

### 页面覆盖清单

| 页面 | 路径 | 结论 | 避让策略 |
|---|---|---|---|
| 首页 | `pages/index/index` | 隐藏；页面未声明 `home-floating-button` 组件 | TabBar 首页保留既有入口 |
| 搜索结果页 | `pages/search/index` | `searchMode == 'result'` 时展示 | `offset="list"`，避让结果列表、空态、错误态和底部安全区 |
| 分类列表页 | `pages/category/index` | 展示 | `offset="tabbar"`，上移避让自定义 TabBar、分类左右滚动区和查看全部商品入口 |
| 分类商品列表页 | `pages/product-list/index` | 展示 | `offset="list"`，避让商品列表、加载更多和底部安全区 |
| 品牌列表页 | `pages/brand-list/index` | 展示 | `offset="tabbar"`，上移避让自定义 TabBar、品牌行和加载更多 |
| 品牌详情页 | `pages/brand-detail/index` | 展示 | `offset="list"`，避让品牌信息、Tab、商品/证书列表和底部安全区 |
| 证书列表页 | `pages/certificates/index` | 展示 | `offset="tabbar"`，上移避让自定义 TabBar、证书卡片和加载更多 |
| 收藏列表页 | `pages/favorites/index` | 展示 | `offset="tabbar"`，上移避让自定义 TabBar、收藏卡片和取消收藏按钮 |
| 商品详情页 | `pages/tile-detail/index` | 展示 | 有商品数据时 `offset="actionbar"`，上移避让收藏/分享底部固定操作条；错误态使用列表偏移 |

### 例外清单

| 页面/流程 | 结论 | 理由 |
|---|---|---|
| `pages/index/index` TabBar 首页 | 隐藏 | 首页本身即为返回目标，避免重复入口 |
| 登录页/授权页 | N/A | 当前小程序无独立登录/授权页面；后续新增需重新评估 |
| 错误页 | 覆盖 | 搜索、商品列表、品牌详情、商品详情错误态保留悬浮按钮或等价可恢复入口 |
| 全屏视频页 | 豁免 | 当前商品详情全屏视频走微信原生视频能力，不在页面层叠加悬浮按钮 |
| 图片预览/原生预览 | 豁免 | `wx.previewImage` / 原生预览期间不叠加自定义悬浮按钮，避免破坏原生流程 |

### 导航策略与测试

- 首页路径：`/pages/index/index`，位于 `app.json` TabBar，返回首页优先使用 `wx.switchTab`，失败时兜底 `wx.reLaunch`。
- 新增统一组件：`src/miniapp/components/home-floating-button/`，集中管理 `show`、`offset`、`navigating` 状态锁、失败 toast 和安全区偏移。
- 接入页面 `.ts` / `.js` 一致：组件同时提供 `index.ts` 与 `index.js`，页面仅声明组件与 WXML 接入，无页面级路由分叉。
- 自动化测试：`uv run pytest tests/test_miniapp_static.py`，31 passed，覆盖首页隐藏、分类列表/品牌列表/证书列表/收藏列表等非首页 TabBar 页展示、搜索结果/商品列表/品牌详情/商品详情接入、点击回首页、导航失败、防重复点击、底部 tabbar/actionbar/list 避让与 TS/JS runtime 同步。
- Device evidence：DevTools 320/375/430 pt 与真机 evidence 当前为 follow_up，未记录本机绝对路径、token、Cookie、Authorization header、`.env`、真实密钥、数据库 DSN、MinIO 凭据或真实客户数据。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:03:10 | `/opsx-modify` | 验收返修：补齐分类列表页、品牌列表页、证书列表页、收藏列表页返回首页悬浮按钮，并使用 `offset="tabbar"` 避让自定义 TabBar。 |
| 2026-07-30 23:47:14 | `/opsx-apply` | 实现小程序返回首页悬浮按钮组件，接入搜索结果、商品列表、品牌详情、商品详情并补充静态测试与 evidence follow_up。 |
| 2026-07-30 23:26:20 | `/sprint-propose sprint-014` | 纳入 Sprint 014 正式范围，可通过 `/opsx-apply --sprint auto` 解析。 |
| 2026-07-30 23:20:00 | `/req-opsx` | 从 REQ-0085 创建 OpenSpec Change，状态为 proposed。 |
