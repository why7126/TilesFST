---
change_id: update-miniapp-price-red-display
requirement_id: REQ-0133-miniapp-price-red-display
created_at: 2026-09-05 23:04:16
updated_at: 2026-09-06 14:19:32
---

# 价格展示实施验证

## 实现与范围

采用独立价格 token `miniappPriceTokens.amount`，最终实现值为 `#F87171`；占位与卡片辅助标签为 `#AFA58E`。生成入口为 `src/web/scripts/sync-design-tokens.ts`，输出 `src/miniapp/styles/price.generated.wxss`。三个使用方局部导入并设置 `price-theme`，避免自定义组件样式隔离导致变量丢失。详情门店说明继续使用既有辅助色。

`src/miniapp/utils/price.ts` 与 `.js` 统一有效、无价和不可查看状态；正数格式保留原字符串，不计算报价。卡片、详情主价格、两个推荐区和收藏均接入。收藏展示字段 `priceView` 在写入既有快照前移除，不增加持久化字段。组件每次收到商品数据都会重新归一化，避免有效→无价→有效残留颜色。

原有 BUG-0148 grid 图片 `aspectFit` 与比例适配保留。共享工作区内另有公开分享等变更，不属于本需求实施差异。本需求不修改 API、DB、Web 商城价格、管理端、Orval、部署输入、请求封装、事件或日志；Docker Compose 与产品数据采集层级为 N/A。

## 页面与状态覆盖

| 入口 | 实施检查与证据 |
|---|---|
| 首页新品／热门 | WXML 引用 compact；共享组件三个密度的源码适配渲染与状态测试 |
| 首页全部产品 | WXML 引用 grid；组件渲染与微信商品列表相同组件 |
| 商品列表／品牌详情 | 两者引用 grid；[微信商品列表截图](wechat-product-list.png)验证有效、无价 |
| 搜索最佳匹配／综合 SKU／SKU Tab | 三处均引用 list；组件渲染与状态切换测试 |
| 商品详情主价格 | [微信详情截图](wechat-detail.png)验证长金额；加载和错误分支保留，正常数据经 normalizeSkuDetail |
| 同系列／同品牌推荐 | 两个模板接入相同状态类，归一化测试分别验证；微信截图展示同系列有效及无价，未单独截图同品牌 |
| 收藏 | [微信收藏截图](wechat-favorites.png)验证有效、无价及失效；归一化和持久化边界测试 |

源码复用检查不等同于每个路由的端到端操作通过。页面合成数据只通过 DevTools setData 写入内存，详情与收藏直接使用展示状态；数据归一化由独立可执行测试验证。没有写入后台或变更真实收藏。完成后已返回首页。

## 原型与实际样式

局部 HTML 已导出 REQ `prototype/miniapp/price-states.png`（1440×1000），实施前完成开发侧 Skeleton 视觉自检，并补充移动预览。它只约束颜色和状态，既有页面结构是布局事实源；这不是用户验收签字。

[320px](price-card-320.png)、[375px](price-card-375.png)、[430px](price-card-430.png) 为 Chromium 对实际共享组件 WXML/WXSS 的合成数据适配渲染，包含 list、compact、grid 和长金额；取证结果见 [浏览器样式](browser-styles.json)。适配移除了图片并将 rpx 换算为 px，不证明微信完整页面布局。检查未发现价格文本新增横向溢出。

微信截图为 DevTools 模拟器，CSS 视口宽 430，输出图片 612×1324；使用项目实际 WXML/WXSS。不是手机、体验版或线上证据。[微信样式](wechat-styles.json)由运行时 `wx.createSelectorQuery().fields(computedStyle)` 取得：

| 节点 | color | 字号 | opacity | 实际背景 |
|---|---|---|---|---|
| 详情 `.price` | rgb(248,113,113) | 21px | 1 | rgb(33,30,22) |
| 推荐 `.recommend-price` 有效／无价 | rgb(248,113,113)／rgb(175,165,142) | 12px | 1 | rgb(33,30,22) |
| 门店 `.price-note` | rgb(141,131,111) | 12px | 1 | rgb(33,30,22) |
| 收藏 `.favorite-price` 有效／无价 | rgb(248,113,113)／rgb(175,165,142) | 16px | 1 | rgb(33,30,22) |
| 失效收藏价格 | rgb(175,165,142) | 16px | 自身1，父卡片0.62 | 原卡片背景叠加页面 |

金额在实际卡片背景上的 WCAG 对比度为 **6.02:1**，满足 4.5:1；不把父卡片淡化后的失效文字列为有效金额。有效金额、占位、辅助文字与局部原型语义一致，品牌金仍用于品牌和操作。最终颜色为开发侧核对结果，业务验收 pending。

## 测试与同步

- 新增 `tests/test_miniapp_price.py`：13 种输入、TS/JS 行为一致性、卡片有效→无价→有效／失效、详情推荐、收藏不可查看优先及展示字段不持久化；2 项测试通过。
- 初次 `python -m pytest tests/test_miniapp_price.py tests/test_miniapp_static.py -q` 为40通过。共享工作区后续修改商品列表分享参数后，末次为39通过、1失败：`test_miniapp_product_list_page_carries_category_navigation` 仍断言旧 `sort=default` 字面量，当前商品列表已使用 `sort=${encodeURIComponent(this.data.sort)}`。本需求未修改商品列表逻辑，不调整另一项工作的断言。
- `node --import tsx ./scripts/sync-design-tokens.ts`（src/web）成功；它与 pnpm sync:tokens 使用同一生成文件入口，绕过沙箱下 tsx CLI 的 IPC EPERM。Web 原有 tokens.generated.css 无差异。
- `pnpm build` 成功，保留既有大 chunk 提示。全量 tsc 初次被 TypeScript 6 的 baseUrl 弃用检查拦截，补充忽略该弃用后仍有9处既有错误，位于管理端上传接口、BrandCertificateComponents.test.tsx 和 auth-store；不能宣称全量类型检查通过。
- `/design-system` 已展示三个小程序 token 的正确名称和值；[1440 预览](design-system-1440.png)同时记录本地 Web 全局工具样式未正常呈现的情况，不能用该截图证明 Web 完整视觉回归通过。本次未改 globals.css、Tailwind 配置或商城样式。
- OpenSpec 当前 Change strict、目录结构、Agent 上下文预算已通过；中文及产品数据采集门禁随最终文档再次执行。

## 待验收边界

REQ 正式验收保留 pending：尚未执行手机／体验版验证、每条路由端到端验证或用户视觉确认。归档前需要核对验收结论。共享工作区静态测试失败与 Web 预览全局样式问题已记录，未扩展本需求去修改其他功能。

## 执行链路复盘

REQ approved → sprint-029 → update Change → 实施与开发验证；业务验收待确认。有效金额误用品牌金及占位混色由统一状态和独立 token 解决。证据显示实际模拟器变量可解析；共享工作区并行修改会影响末次回归，建议在稳定快照复测全套。未自动创建 follow-up Issue／Change。

## 2026-09-06 归档复核

用户在已披露验证边界后执行 `/opsx-archive REQ-0133`，按该范围进行归档。当前工作区复测 `python -m pytest tests/test_miniapp_price.py tests/test_miniapp_static.py -q` 为 **40 passed**，此前商品列表字面量断言失败已消除。最终价格token、状态helper、实际截图、computed style及文档一致；保留真机、体验版、逐路由端到端和Web完整视觉／类型检查未覆盖说明，不将其改写为通过。API、DB、Orval、环境、部署及发布文档无需变更；小程序README与UI规范已同步。无明显规范优化点，未自动创建follow-up。
