## Context

REQ-0059 `favorite-list-page` 已完成 capture、generate、complete 和 review，当前状态为 `approved`，物理阶段为 `issues/requirements/review/`。需求文档位于 `issues/requirements/archive/REQ-0059-favorite-list-page/`。

现有能力包含小程序首页、分类、搜索、商品列表和 SKU 详情页，收藏列表应作为“回访已保存对象”的用户侧页面，与商品列表的“发现与筛选商品”职责区分。当前端范围仍为 `multi`，但需求倾向至少覆盖微信小程序；实现阶段应在 Sprint 范围确认 Web 展示端是否同做。

## Goals / Non-Goals

**Goals:**

- 提供用户侧收藏列表页，集中展示已收藏内容。
- 首期优先支持 SKU / 商品收藏，后续可扩展品牌、分类等对象。
- 支持收藏项进入详情、取消收藏、空状态、未登录状态、异常状态、刷新和增量加载。
- 保证收藏列表与详情页收藏状态一致。
- 小程序实现时遵守自定义导航与设备 evidence best practice。
- 埋点覆盖列表浏览、收藏项点击、取消收藏、空状态行动和加载失败。

**Non-Goals:**

- 不提供 Web 管理端收藏运营、批量导出或人工维护。
- 不实现购物车、询价单、在线下单、客服会话或报价流程。
- 不实现收藏分组、分享收藏夹、多人协作或项目清单。
- 不把浏览历史、足迹或推荐结果混入收藏列表。
- 不新增媒体上传或对象存储能力。

## Decisions

### D1. 首期收藏对象优先 SKU / 商品

实现阶段 SHOULD 优先支持 SKU / 商品收藏。若必须同时支持品牌、分类等多对象收藏，数据模型和列表项必须显式包含 `objectType`、`objectId`、展示摘要和目标跳转路径，避免出现可见但不可打开的收藏项。

### D2. 收藏列表是回访页，不是商品发现页

收藏列表 SHOULD 优先展示用户已保存对象，支持进入详情和取消收藏。v1 不提供复杂筛选、批量管理、收藏分组或推荐流。空状态可以引导用户去首页、分类或搜索继续浏览。

### D3. 登录态与访客态必须先定策略

如果收藏绑定用户账号或 OpenID，未登录状态 MUST 展示登录引导或受控访客提示，不得误展示为空收藏。如果允许访客本地收藏，实现阶段必须说明本地存储、迁移登录账号和清理策略。

### D4. 详情页与列表状态一致

详情页新增/取消收藏后，再进入收藏列表时必须反映最新状态。收藏列表取消收藏后，返回详情页时应同步最新收藏状态或触发详情刷新。实现可使用服务端事实源、本地缓存失效或事件通知机制，但不得长期展示冲突状态。

### D5. 原型冲突决议

原型位于 `issues/requirements/archive/REQ-0059-favorite-list-page/prototype/web/`，优先级为 HTML > context.md > acceptance.md > `rules/ui-design.md` > OpenSpec specs。

- HTML 原型采用移动端优先表达，可映射到微信小程序或 Web 展示端移动视图。
- PNG Golden Reference 尚未导出，不阻塞 Change 创建；实现阶段可补设计截图或以 HTML/context 为验收基准。
- 若小程序页面已存在 `pages/favorites/index.*` 占位，必须以本 Change 的 spec 和原型作为目标状态，而不是保留空白占位。

### D6. 小程序导航与设备验收

若实现覆盖微信小程序，design 和 tasks MUST 引用 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`，覆盖状态栏、胶囊 reserve、返回兜底、页面 offset、320/375/430 pt DevTools evidence；没有真机时不得写作真机通过。

## Risks / Trade-offs

- [Risk] 端范围未最终确认，可能导致 Web 与小程序拆分实现成本上升 → Mitigation: Sprint 规划前确认首期端范围；如两端同做，分解任务和验收矩阵。
- [Risk] 收藏对象范围过宽导致数据模型复杂 → Mitigation: 首期优先 SKU / 商品，多对象收藏必须显式设计 `objectType`。
- [Risk] 未登录态与空收藏混淆 → Mitigation: 单独设计未登录、无收藏、网络异常和对象失效状态。
- [Risk] 列表与详情收藏状态不一致 → Mitigation: 增加状态同步任务和测试。
- [Risk] 小程序顶部导航/胶囊遮挡 → Mitigation: 按小程序导航 best practice 补 evidence。

## Migration Plan

1. 明确首期端范围、收藏对象范围和登录态策略。
2. 如需 API/DB，补充用户收藏查询、取消收藏、状态同步接口与数据模型。
3. 实现收藏列表页路由、入口、列表项、空/错/未登录状态和取消收藏交互。
4. 接入详情页收藏状态同步。
5. 补充测试与设备/视口 evidence。
6. 运行 Workflow Sync，确保 REQ、Change 与 Sprint 状态一致。

Rollback 策略：如收藏列表无法在当前 Sprint 完整上线，可先保留入口隐藏或灰度；不得暴露无法加载、无法取消或状态不同步的半成品页面。
