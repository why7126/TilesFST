---
requirement_id: REQ-0086-miniapp-brand-list-ui-interaction-optimization
status: done
created_at: 2026-07-31 15:13:01
updated_at: 2026-07-31 21:40:29
owner: product
source: requirement.md
---

# 验收清单

## 功能 AC

- [ ] AC-001 品牌列表页标题展示为“品牌”，页面可从现有品牌入口正常进入。
- [ ] AC-002 顶部自定义导航保留返回入口、页面标题和右侧微信原生胶囊 reserve，不出现重叠。
- [ ] AC-003 页面展示品牌氛围 Hero 区，包含英文弱标签、主标题和辅助文案，视觉与附件设计稿一致或经产品确认等价。
- [ ] AC-004 品牌列表区域标题展示为“品牌矩阵”，不展示“按类目快速识别”辅助提示。
- [ ] AC-005 品牌矩阵每张卡片只展示一个品牌。
- [ ] AC-006 品牌卡片上行展示品牌 Logo 或首字母占位、品牌名称、商品数量和进入指示。
- [ ] AC-007 点击品牌卡片上行进入对应品牌详情页，沿用现有品牌详情路由能力。
- [ ] AC-008 品牌卡片下行不展示“全部类目 · 点击查看该品牌下的类目商品”等说明文案。
- [ ] AC-009 品牌卡片下行展示该品牌公开商品对应的末级类目胶囊标签。
- [ ] AC-010 点击任一类目标签进入该品牌下对应类目的商品列表页，并携带 `brandId` 与 `categoryId`。
- [ ] AC-011 点击类目标签不得触发品牌详情页跳转。
- [ ] AC-012 品牌列表加载、空态、错误态、重试和下拉刷新能力不因 UI 优化退化。

## 数据与接口 AC

- [ ] AC-DATA-001 品牌列表仅展示小程序公开可见、启用状态的品牌。
- [ ] AC-DATA-002 商品数量统计口径为该品牌下小程序公开可见商品数量。
- [ ] AC-DATA-003 商品数量与末级类目集合使用同一公开商品集合口径。
- [ ] AC-DATA-004 同一品牌下重复末级类目只展示一次。
- [ ] AC-DATA-005 类目集合中的每一项包含可用于跳转的类目 ID 和展示名称；若现有接口缺失，后续 Change 必须扩展接口。
- [ ] AC-DATA-006 品牌无公开商品时展示 0 款商品或确认后的空态值，不展示误导性类目。
- [ ] AC-DATA-007 API 响应不得暴露管理端内部备注、未公开品牌、未公开商品、未授权素材或对象存储内部 key。
- [ ] AC-DATA-008 如接口字段发生变化，必须同步 API Schema、OpenAPI、Orval、小程序调用类型、接口文档和测试。

## UI / 体验 AC

- [ ] AC-UI-001 页面视觉以附件原型和截图为主要参考，延续暗色旗舰风和品牌金强调。
- [ ] AC-UI-002 页面主体、Hero、品牌矩阵、卡片、类目标签和底部 TabBar 的层级清晰，不出现内容粘连。
- [ ] AC-UI-003 Hero 区高度、圆角、边框、主标题、弱标签和辅助文案在 390pt 视口下与附件设计稿整体一致或经产品确认等价。
- [ ] AC-UI-004 品牌卡片使用上下分区：上行为品牌入口，下行为类目标签区，并通过分隔线或间距区分。
- [ ] AC-UI-005 品牌 Logo 加载失败时展示品牌首字母、缩写或统一占位，不展示破图。
- [ ] AC-UI-006 品牌名称较长时限制行数或截断，商品数量和进入指示仍可见。
- [ ] AC-UI-007 类目标签完整展示并自动换行，不使用“等 N 类”折叠，不产生横向滚动；类目标签字号比品牌名称小 2rpx。
- [ ] AC-UI-008 品牌入口和类目标签均有小程序端可感知的按压反馈。
- [ ] AC-UI-009 底部 TabBar 中“品牌”项呈现选中态，滚动内容不被底部 TabBar 或安全区遮挡。
- [ ] AC-UI-010 在 320、375、390、430 pt 宽度下，页面无文字重叠、Logo 拉伸、内容横向溢出或主要入口不可点。

## 小程序导航与设备验收 AC

> 来源：`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`

- [ ] AC-MINIAPP-001 品牌列表页按 TabBar 页面形态确认导航策略，标题、返回按钮和右侧原生胶囊 reserve 不重叠。
- [ ] AC-MINIAPP-002 页面主体使用统一导航 offset 或 spacer，Hero、品牌矩阵、加载态、空态和错误态不被 fixed 或 sticky 导航遮挡。
- [ ] AC-MINIAPP-003 返回按钮如出现，需支持页面栈返回；外部或分享直达无页面栈时有首页兜底。
- [ ] AC-MINIAPP-004 DevTools 至少覆盖 320、375、390、430 pt 视口，记录首屏内容、胶囊避让、品牌卡片和 TabBar 遮挡结论。
- [ ] AC-MINIAPP-005 真机验收不可用时必须标记 `blocked` 或 `follow_up`，不得把 DevTools 截图写作真机通过。

## 埋点 AC

- [ ] AC-TRACK-001 如现有品牌列表页已有曝光埋点，本次调整后继续记录品牌列表页曝光事件。
- [ ] AC-TRACK-002 品牌入口点击继续记录品牌 ID、位置索引和来源入口。
- [ ] AC-TRACK-003 类目标签点击记录品牌 ID、类目 ID、类目名称、位置索引和来源入口。
- [ ] AC-TRACK-004 埋点不得记录手机号、地址、微信号、授权凭据等敏感信息。
- [ ] AC-TRACK-005 埋点失败不得阻断品牌列表展示、点击跳转或重试。

## 文档与原型 AC

- [ ] AC-DOC-001 `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 已补齐并保持 `pending_review` 状态。
- [ ] AC-DOC-002 `prototype/miniapp/context.md` 与 `prototype/miniapp/prototype.html` 可作为后续设计与实现验收参考。
- [ ] AC-DOC-003 `prototype/miniapp/prototype.png` 可在后续从 HTML 或设计稿导出；缺 PNG 不阻塞评审。
- [ ] AC-DOC-004 后续 `/req-opsx` 的 design.md 必须引用 `trace.md` 中的 `knowledge_base_refs`。

## 横切 AC（knowledge-base）

本 REQ 为微信小程序品牌列表页 UI 与交互体验优化，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签；无需要转化为 `AC-XCUT-*` 的管理端横切 AC。

小程序导航与设备验收要求已参考 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 转化到上方“小程序导航与设备验收 AC”。Sprint 014 复盘中关于“小程序列表类需求在 propose 阶段写清公开口径、点击区域、排序字段和空态”的经验，已转化到功能、数据与 UI 验收项。
