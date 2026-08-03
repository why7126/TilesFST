---
requirement_id: REQ-0083-miniapp-brand-list-category-summary
status: done
created_at: 2026-07-30 22:36:58
updated_at: 2026-07-31 08:07:46
owner: product
source: requirement.md
---

# 验收清单

## 功能 AC

- [ ] AC-001 品牌列表页上半部轮播图保持现有布局、图片比例、指示器、自动播放和点击行为不变。
- [ ] AC-002 本次调整仅作用于轮播图下方品牌列表区域，不引入品牌轮播数据源或配置方式变化。
- [ ] AC-003 下半部品牌列表每行只展示一个品牌，不再以一行 2 个品牌卡片作为本需求目标形态。
- [ ] AC-004 每个品牌行分为左侧品牌信息区和右侧类目汇总区。
- [ ] AC-005 左侧品牌信息区展示品牌 Logo、品牌名称和商品数量。
- [ ] AC-006 右侧类目汇总区展示该品牌所有上架/公开商品对应类目的最后一层级类目名称。
- [ ] AC-007 同一品牌下重复末级类目名称只展示一次。
- [ ] AC-008 商品只绑定一级或二级类目时，展示该商品实际绑定路径中的最后一层名称。
- [ ] AC-009 点击品牌 Logo 或品牌名称进入品牌详情页/主页。
- [ ] AC-010 点击品牌右侧任一类目进入该品牌该类目下的商品列表页，并携带品牌 ID、类目 ID、类目名称和来源参数。
- [ ] AC-011 已下架、未公开或缺少有效跳转目标的品牌不得打开无效页面。
- [ ] AC-012 品牌列表加载、空状态、错误态、重试和分页/加载更多能力不因本次布局调整退化。

## 数据与接口 AC

- [ ] AC-DATA-001 品牌列表仅展示小程序公开可见、启用状态的品牌。
- [ ] AC-DATA-002 商品数量统计口径为该品牌下小程序公开可见商品数量；已下架、禁用或不公开商品不计入。
- [ ] AC-DATA-003 商品数量与末级类目集合使用同一公开商品集合口径。
- [ ] AC-DATA-004 品牌无公开商品时，商品数量展示 0 或等价空态值，右侧类目区不展示误导性类目。
- [ ] AC-DATA-005 品牌有公开商品时必须按商品关联类目展示末级类目；品牌无公开商品时仅左侧商品数量展示空态值，右侧类目区留空，不重复展示“暂无商品”。
- [ ] AC-DATA-006 品牌列表数据包含品牌 ID、品牌 Logo URL、品牌名称、商品数量、末级类目 ID 与名称集合，或在 OpenSpec design 中说明替代字段来源。
- [ ] AC-DATA-007 若现有接口缺少商品数量或末级类目集合，后续 Change 必须同步 API Schema、OpenAPI、Orval 或小程序 API 类型、接口文档和测试。
- [ ] AC-DATA-008 API 响应不得暴露管理端内部备注、未公开品牌、未公开商品、未授权素材或对象存储内部 key。

## UI / 体验 AC

- [ ] AC-UI-001 页面视觉沿用小程序现有暗色旗舰风和品牌金强调。
- [ ] AC-UI-002 品牌行左右分区清晰，左侧品牌信息优先保持可读，右侧类目汇总不得覆盖左侧内容。
- [ ] AC-UI-003 品牌 Logo 区域尺寸稳定，图片加载前后不造成列表布局跳动。
- [ ] AC-UI-004 品牌 Logo 加载失败时展示品牌名称首字、品牌占位或统一占位图，不展示破图。
- [ ] AC-UI-005 品牌名称较长时限制行数或截断，不挤压商品数量和右侧类目汇总区。
- [ ] AC-UI-006 类目名称较长或数量较多时全部折行展示，不使用“等 N 类”折叠，不产生横向滚动。
- [ ] AC-UI-007 品牌行点击区域不小于 44x44 pt，并保留小程序原生按压反馈。
- [ ] AC-UI-008 在 320、375、430 pt 宽度下，品牌行无文字重叠、Logo 拉伸、内容溢出容器或底部 TabBar 遮挡。
- [ ] AC-UI-009 加载态、空态、错误态和网络失败提示在小屏下不遮挡导航、轮播或主要内容。

## 小程序导航与设备验收 AC

> 来源：`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`

- [ ] AC-MINIAPP-001 品牌列表页按当前页面形态确认导航策略，标题、返回按钮和右侧原生胶囊 reserve 不重叠。
- [ ] AC-MINIAPP-002 页面主体使用统一导航 offset 或 spacer，首屏轮播、品牌行、加载态、空态和错误态不被 fixed 或 sticky 导航遮挡。
- [ ] AC-MINIAPP-003 返回按钮如出现，需支持页面栈返回；分享或外部直达无页面栈时有首页兜底。
- [ ] AC-MINIAPP-004 DevTools 至少覆盖 320、375、430 pt 视口，记录首屏内容、胶囊避让、品牌单行列表和 TabBar 遮挡结论。
- [ ] AC-MINIAPP-005 真机验收不可用时必须标记 blocked 或 follow_up，不得把 DevTools 截图写作真机通过。

## 埋点 AC

- [ ] AC-TRACK-001 如现有品牌列表页已有曝光埋点，本次调整后继续记录品牌列表页曝光事件。
- [ ] AC-TRACK-002 品牌 Logo / 名称点击继续记录品牌 ID、位置索引和来源入口。
- [ ] AC-TRACK-003 品牌右侧类目点击记录品牌 ID、类目 ID、类目名称、位置索引和来源入口。
- [ ] AC-TRACK-004 类目展示、商品数量和品牌点击埋点不得记录手机号、地址、微信号、授权凭据等敏感信息。
- [ ] AC-TRACK-005 埋点失败不得阻断品牌列表展示、点击跳转或重试。

## 文档与原型 AC

- [ ] AC-DOC-001 `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 已补齐并保持 `pending_review` 状态。
- [ ] AC-DOC-002 `prototype/miniapp/context.md` 与 `prototype/miniapp/prototype.html` 可作为后续设计与实现验收参考。
- [ ] AC-DOC-003 `prototype/miniapp/prototype.png` 可在后续从 HTML 导出；缺 PNG 不阻塞评审。
- [ ] AC-DOC-004 后续 `/req-opsx` 的 design.md 必须引用 `trace.md` 中的 `knowledge_base_refs`。

## 横切 AC（knowledge-base）

本 REQ 为微信小程序品牌列表页展示优化，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签；无需要转化为 `AC-XCUT-*` 的管理端横切 AC。

小程序导航与设备验收要求已参考 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 转化到上方“小程序导航与设备验收 AC”。
