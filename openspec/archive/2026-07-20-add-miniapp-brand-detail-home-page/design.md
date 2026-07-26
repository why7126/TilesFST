## Context

`REQ-0058-brand-detail-home-page` 已评审通过，目标是在微信小程序中提供品牌入口页和单品牌主页/详情页。现有能力可提供若干复用边界：

- `miniapp-home` 已定义首页 Banner、品牌馆入口、首页视觉和小程序运行入口质量门禁。
- `miniapp-product-list-page` 已定义商品列表容器、公开 SKU 查询、双列商品卡片、分页和状态机。
- `miniapp-brand-card-component` 已定义单品牌卡片组件、Logo 降级、点击跳转和埋点。
- `brand-certificate-management` 已定义品牌证书主数据、展示控制、文件预览和前台可展示边界。

本 Change 不直接实现源码，但设计阶段需要明确页面、API、复用策略、验收和风险，避免后续 `/opsx-apply` 时把品牌页做成孤立页面。

## Goals / Non-Goals

**Goals:**

- 新增小程序品牌入口页，顶部轮播与首页轮播一致，下方品牌卡片一行 2 个。
- 新增品牌主页/详情页，上半部分展示品牌图片和基础信息，下半部分通过商品/证书 Tab 展示当前品牌关联内容。
- 复用既有商品卡片、品牌卡片、证书展示和自定义导航经验。
- 明确 API 和数据过滤边界，避免暴露管理端字段、未授权素材或内部 object key。
- 将小程序 320/375/430 pt、真机/DevTools evidence、`.ts`/`.js` 运行入口同步纳入任务。

**Non-Goals:**

- 不重做 Web 管理端品牌主数据管理。
- 不建设店主 Web 品牌主页。
- 不实现品牌主页装修、复杂楼层配置、自定义 Tab、品牌视频、门店地图、客服、询价、购物车或在线下单。
- 不新增收藏、分享海报、SEO 或小程序码。

## Decisions

### D1 采用新增 capability

选择新增 `miniapp-brand-detail-home-page` capability，而不是修改 `miniapp-home` 或 `brand-management`。

原因：品牌主页是独立小程序前台浏览能力，既不是首页本身，也不是管理端品牌主数据维护。它依赖现有能力，但有自己的页面结构、路由、Tab、状态机和验收闭环。

备选方案：修改 `miniapp-home` 的“品牌馆入口”要求。该方案会把入口降级策略和完整品牌页能力混在一起，不利于独立规划和验收。

### D2 品牌轮播优先复用首页 Banner/Swiper

品牌入口页轮播应复用首页轮播的 `swiper` 视觉、图片比例、指示器、自动轮播和降级策略。数据来源优先复用现有 Banner 管理能力；若无法表达品牌页轮播位置，再在实现阶段扩展 Banner 展示端或展示位置，并同步 API、OpenAPI、Orval、docs 和 tests。

备选方案：为品牌页单独创建一套轮播数据模型。该方案会增加后台配置和数据治理成本，首期不采用。

### D3 商品 Tab 复用商品列表能力

商品 Tab 仅按 `brandId` 展示当前品牌下公开 SKU，展示策略对齐 `REQ-0056-product-list-card-only-layout` 和 `miniapp-product-list-page` 的双列商品卡片、分页、刷新、加载更多、空态和错误态。

备选方案：在品牌主页内重新实现一套商品卡片和分页状态。该方案容易造成字段兜底、埋点和小屏布局不一致，不采用。

### D4 证书 Tab 复用品牌证书公开展示边界

证书 Tab 只展示当前品牌关联且允许前台展示的证书。证书文件使用受控 URL 或等价读取引用，不暴露原始 object key，不展示后台内部字段。

备选方案：直接复用管理端证书列表字段。该方案可能暴露审计、备注、内部状态或对象存储细节，不采用。

### D5 小程序导航与运行入口作为验收门禁

品牌入口页和品牌主页需要遵守 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`。新增页面必须覆盖 DevTools 320/375/430 pt evidence，真机不可用时标记 blocked 或 follow_up；若页面存在 `.ts` 与 `.js`，必须保证微信开发者工具实际加载脚本包含业务逻辑。

备选方案：只做静态单元测试。该方案无法覆盖胶囊避让、内容 offset 和小程序运行入口漂移，不能单独作为完成证据。

## Conflict Resolution

本 REQ 存在 `prototype/miniapp/prototype.html` 和 `prototype/miniapp/context.md`，优先级为 HTML、context、acceptance、`rules/ui-design.md`、既有 specs。

- HTML 原型展示入口页和详情页两个手机视图，表达信息架构，不作为像素级最终视觉稿。
- `context.md` 明确入口页、详情页、轮播、双列卡片、Tab 与导航风险；实现应优先满足这些结构。
- `acceptance.md` 的 AC-036 至 AC-039 明确设备与运行入口要求，优先于一般 UI 建议。
- 既有 `miniapp-home` 中“品牌馆完整能力不进入本期”的限制只约束该历史首页 Change，不阻止本 Change 建设品牌页；本 Change 完成后首页品牌馆入口可在后续实现中指向品牌入口页。

## Risks / Trade-offs

- [Risk] 现有 Banner 管理无法区分品牌页轮播位置 → [Mitigation] 实现阶段先确认现有枚举；若需扩展，作为 API/Orval/docs/tests 同步任务处理。
- [Risk] 现有公开品牌详情接口字段不足 → [Mitigation] 首选复用品牌主数据公开字段；不足时新增公开 schema，严格过滤管理端字段。
- [Risk] 品牌详情中商品 Tab 和独立商品列表页产生卡片差异 → [Mitigation] 复用 `product-card` 或统一展示 adapter，并添加静态/组件测试。
- [Risk] 证书文件 URL 暴露对象存储内部 key → [Mitigation] 后端只返回受控 `file_url` 或签名/代理 URL，前端不拼接 object key。
- [Risk] 小程序新增页面 `.ts` / `.js` 漂移 → [Mitigation] 添加运行入口静态测试，或执行项目认可的同步构建步骤。
- [Risk] 真机验收暂不可用 → [Mitigation] DevTools evidence 与真机 evidence 分开记录，真机不可用必须标记 blocked 或 follow_up。

## Migration Plan

1. 确认现有品牌、Banner、商品列表和证书公开查询能力。
2. 增加或扩展后端小程序公开接口，保证字段过滤和分页状态。
3. 同步 OpenAPI、Orval、接口文档和后端测试。
4. 增加小程序品牌入口页、品牌主页/详情页、路由和服务调用。
5. 接入品牌轮播、品牌卡片、商品 Tab、证书 Tab、加载/空态/错误态和埋点。
6. 补充小程序静态测试、接口测试和设备 evidence。
7. 若发布后发现品牌页接口异常，可通过隐藏入口或降级到可返回提示回滚前台入口。

## Open Questions

- 品牌轮播是否完全复用现有 Banner 管理枚举，还是新增品牌页展示位置？
- 品牌主页的证书点击首期是图片预览、证书详情页，还是仅展开查看？
- 品牌入口页是否作为 TabBar 页面、首页快捷入口页面，还是普通二级页面？
