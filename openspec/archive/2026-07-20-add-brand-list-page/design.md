## Context

`REQ-0060-brand-list-page` 已评审通过，定位为微信小程序访客端品牌列表页。当前小程序已经具备首页轮播、分类、搜索、商品列表、商品详情和品牌卡片组件，但首页品牌入口仍是占位或找砖降级语义，缺少真实品牌频道。

现有相关能力：

- `miniapp-home`：首页已有 Banner 轮播、快捷入口、TabBar 和深色视觉基准。
- `miniapp-brand-card-component`：已有单品牌卡片组件，提供 Logo 降级、整卡点击、跳转 fallback 和埋点上下文。
- `brand-management`：已有品牌主数据能力，可作为品牌列表公开数据来源。
- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`：要求新增小程序页面考虑状态栏、胶囊 reserve、返回兜底、页面 offset 和设备 evidence。

原型优先级和冲突处理：

```text
prototype/miniapp/prototype.html
  > prototype/miniapp/context.md
  > acceptance.md
  > rules/ui-design.md
  > openspec/specs
```

本需求没有 PNG Golden Reference；`prototype/miniapp/prototype.png` 后续可从 HTML 导出，不阻塞实现。用户原始描述中的 `siderbar` 在小程序语境下不直接等同 Web 侧边栏，设计按实际小程序入口形态落地：优先确认 TabBar 或首页快捷入口中的“品牌”入口。

## Goals / Non-Goals

**Goals:**

- 新增微信小程序品牌列表页，承接“品牌”入口。
- 顶部品牌轮播对齐首页轮播交互和视觉。
- 主体品牌列表使用一行 2 个品牌卡片。
- 复用现有品牌主数据和品牌卡片能力，不新增重复品牌表。
- 入口文案从“找砖”或建设中品牌馆语义调整为“品牌”，点击进入品牌列表页。
- 记录小程序导航、设备视口、TabBar 遮挡和真机/DevTools evidence 验收。

**Non-Goals:**

- 不实现管理端品牌维护、品牌排序后台或品牌轮播配置后台。
- 不完整实现品牌详情页/主页；该能力由 `REQ-0058-brand-detail-home-page` 承接。
- 不实现品牌收藏、预约、询价、下单或用户收藏统计。
- 不新增 Web 展示端品牌列表页。
- 不新增重复品牌数据源或重复 Banner 数据源。

## Decisions

### D1. 品牌列表页作为小程序新页面落地

新增页面建议路径为 `pages/brands/index`，具体路径在实现阶段按现有小程序路由规范确认。品牌入口不再降级到搜索页或占位提示，而是进入该页面。

备选方案：

- 继续使用首页品牌馆占位提示：实现成本低，但无法满足 REQ-0060 的品牌列表页目标。
- 把品牌列表塞入首页模块：会加重首页职责，也难以承接品牌详情页/品牌商品列表闭环。

### D2. 品牌轮播优先复用首页 Banner 体验

品牌页顶部轮播沿用首页轮播的自动播放、循环、指示点和品牌金激活态。数据来源优先复用 Banner 管理能力；如果实现需要品牌页专属轮播位，必须在任务中明确配置来源、字段兼容和后台边界。

备选方案：

- 新增独立品牌轮播表：扩展性强，但本需求范围内会引入重复数据源和管理端改造，暂不采用。
- 静态品牌头图：实现简单，但不能满足“品牌轮播（与首页轮播一致）”的明确要求。

### D3. 品牌卡片复用逻辑，扩展双列列表态

`miniapp-brand-card-component` 已定义单品牌展示、Logo 降级、整卡点击和埋点上下文。本 Change 应复用这些逻辑，同时为品牌列表提供双列卡片样式或列表态 variant。组件内部仍不得直接请求品牌列表、品牌详情、SKU 列表或搜索接口；页面容器负责数据加载和列表状态机。

备选方案：

- 完全新写品牌卡片：容易造成 Logo 降级、跳转 fallback 和埋点差异。
- 直接复用现有横向卡片样式：不能满足一行 2 个卡片的视觉要求。

### D4. 品牌点击目标与 REQ-0058 对齐

品牌卡片点击优先进入品牌详情页/主页。若 `REQ-0058` 尚未交付，实现阶段可以降级到品牌商品列表，并携带品牌筛选参数；不可访问品牌必须阻止无效跳转并给出轻量提示。

### D5. 设备与导航验收纳入实现任务

品牌列表页涉及顶部导航、轮播首屏和底部 TabBar，必须按小程序自定义导航 best-practice 验收 320/375/430 pt 视口、胶囊 reserve、返回兜底、页面 offset 和真机/DevTools evidence。DevTools 通过不得冒充真机通过。

## Risks / Trade-offs

- [Risk] 品牌页轮播配置来源不明确，可能导致实现阶段新增重复数据源。  
  Mitigation: 任务中先确认复用 Banner 能力或以字段兼容方式新增品牌页位置，不引入重复品牌/Banner 表。

- [Risk] `REQ-0058` 未交付时，品牌卡片目标页不可用。  
  Mitigation: 允许临时降级到品牌商品列表或不可用提示，并在后续 Sprint 中与 `REQ-0058` 串联。

- [Risk] 现有品牌卡片组件偏横向卡片，双列列表态直接复用可能挤压文字。  
  Mitigation: 扩展列表态样式，覆盖 320/375/430 pt 截图验收。

- [Risk] 小程序 `.ts` 与 `.js` 运行事实源可能漂移。  
  Mitigation: 新页面和组件更新时补充静态测试，确认微信开发者工具实际加载脚本不是空模板。

## Migration Plan

1. 新增品牌列表页路由和入口映射。
2. 接入品牌轮播数据和品牌列表数据，优先复用现有接口；必要时新增小程序聚合接口并同步 API/Orval/docs/tests。
3. 扩展品牌卡片双列列表态，保留 Logo 降级、不可用提示、防重复点击和埋点上下文。
4. 将首页/TabBar/快捷入口文案调整为“品牌”，点击进入品牌列表页。
5. 补充小程序静态测试和设备 evidence。

Rollback 策略：如品牌列表页无法按期上线，入口可临时恢复到原安全降级提示，但不得保留指向无效路由；Change 不能标记完成。

## Implementation Notes

- 品牌页轮播已选择复用现有 `MINIAPP_HOME_CAROUSEL` Banner 数据源，不新增品牌页专属轮播表或后台配置枚举。
- 品牌列表页使用 `GET /api/v1/miniapp/brands` 聚合接口，返回 `status=ENABLED` 的品牌；公开 SKU 数仅作为 `product_count` 辅助信息，不作为列表展示门槛。Logo 与轮播图统一返回 `/media/...` 安全 URL。
- OpenAPI JSON 与 API 文档已同步；Orval 本地生成命令在当前环境持续无输出卡住，生成客户端待后续环境恢复后补跑。
- DevTools 320/375/430 pt 与真机 evidence 当前环境不可执行，验收 evidence 待后续补录。

## Open Questions

- [Resolved] 品牌页轮播复用现有 `MINIAPP_HOME_CAROUSEL`，不新增专属轮播表。
- [Resolved] 品牌卡片默认跳转品牌筛选商品列表；不可用品牌显示轻提示。
- [Resolved] “品牌”入口同步 TabBar 与首页快捷入口。
- [Pending Evidence] DevTools 320/375/430 pt 与真机 evidence 待补录。
