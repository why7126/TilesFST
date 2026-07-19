---
requirement_id: REQ-0050-miniapp-brand-header-page-title-rules
title: 小程序 brand-header 页面标题规则验收标准
status: pending_review
created_at: 2026-07-19 14:26:30
updated_at: 2026-07-19 14:26:30
---

# REQ-0050 小程序 brand-header 页面标题规则验收标准

## 1. 首页 brand-header AC

- [ ] AC-HOME-001 首页 `brand-header` 第一行显示 `菲尚特瓷砖馆`。
- [ ] AC-HOME-002 首页 `brand-header` 第二行显示 `质感空间，由砖而生`。
- [ ] AC-HOME-003 首页不显示非首页返回按钮。
- [ ] AC-HOME-004 首页右侧避让微信原生分享 / 关闭胶囊。
- [ ] AC-HOME-005 首页搜索框、Banner、快捷入口和首屏内容不被 fixed header 遮挡。
- [ ] AC-HOME-006 首页加载态、错误态和数据正常态下双行文案高度稳定，不闪烁、不挤压首屏内容。

## 2. 非首页单行标题 AC

- [ ] AC-TITLE-001 search 页面 `brand-header` 只显示一行标题 `搜索`。
- [ ] AC-TITLE-002 category 页面 `brand-header` 只显示一行标题 `全部分类` 或等价分类页标题。
- [ ] AC-TITLE-003 product-list 页面 `brand-header` 只显示一行列表标题，不展示分类名 / 关键词第二行。
- [ ] AC-TITLE-004 tile-detail 页面 `brand-header` 只显示一行标题 `商品详情`，不展示 SKU 编号第二行。
- [ ] AC-TITLE-005 favorites 页面 `brand-header` 只显示一行标题 `收藏`。
- [ ] AC-TITLE-006 certificates 页面 `brand-header` 只显示一行标题 `证书`。
- [ ] AC-TITLE-007 store-info 页面 `brand-header` 只显示一行标题 `门店信息`。
- [ ] AC-TITLE-008 非首页不得渲染 `subtitle`、品牌副文案、SKU 编号副标题或其他第二行辅助文案。
- [ ] AC-TITLE-009 非首页标题过长时单行截断，不换行、不横向滚动、不挤压右侧胶囊避让区。

## 3. 返回按钮 AC

- [ ] AC-BACK-001 非首页左侧显示返回按钮，首页不显示返回按钮。
- [ ] AC-BACK-002 有上一页页面栈时，点击返回按钮回到上一页。
- [ ] AC-BACK-003 无上一页页面栈时，点击返回按钮兜底回首页。
- [ ] AC-BACK-004 从分享卡片直达 tile-detail 时，返回按钮不报错，且可兜底回首页。
- [ ] AC-BACK-005 加载态、空态、错误态下返回按钮仍可点击。
- [ ] AC-BACK-006 返回按钮点击热区不小于 44x44 pt，且不与页面标题重叠。

## 4. 微信原生胶囊与分享 AC

- [ ] AC-WX-001 所有覆盖页面导航栏右侧均避让微信原生分享 / 关闭胶囊。
- [ ] AC-WX-002 返回按钮、首页双行文案、非首页标题均不得进入微信原生胶囊区域。
- [ ] AC-WX-003 WXML / WXSS 中不得新增自绘分享按钮、关闭按钮或胶囊控件。
- [ ] AC-WX-004 支持分享的页面继续保留微信小程序原生分享能力。
- [ ] AC-WX-005 tile-detail 分享标题、路径和 SKU 参数不因导航栏标题改为 `商品详情` 而丢失。
- [ ] AC-WX-006 非分享页面不得出现不可点击的伪分享按钮或伪关闭按钮。

## 5. 状态栏与内容避让 AC

- [ ] AC-LAYOUT-001 导航栏高度计算包含状态栏高度、导航内容高度和微信菜单按钮 / 胶囊避让信息。
- [ ] AC-LAYOUT-002 页面主体内容从导航栏下方开始，不被 fixed header 遮挡。
- [ ] AC-LAYOUT-003 搜索框、分类列表、商品列表、详情媒体区、收藏占位、证书占位和门店信息内容均不被导航栏遮挡。
- [ ] AC-LAYOUT-004 加载态、空态、错误态和骨架屏同样避让导航栏高度。
- [ ] AC-LAYOUT-005 320、375、430 pt 宽度下，返回按钮、标题和右侧胶囊避让区无重叠。
- [ ] AC-LAYOUT-006 页面不产生横向滚动，标题截断不会导致布局抖动。

## 6. 范围与数据 AC

- [ ] AC-SCOPE-001 本需求不新增业务页面。
- [ ] AC-SCOPE-002 本需求不调整底部 TabBar。
- [ ] AC-SCOPE-003 本需求不新增后台文案配置能力。
- [ ] AC-SCOPE-004 本需求默认不新增 API。
- [ ] AC-SCOPE-005 本需求默认不修改数据库表或字段。
- [ ] AC-SCOPE-006 本需求不创建 OpenSpec Change；后续开发前必须完成 `/req-review` 与 `/req-opsx`。
- [ ] AC-SCOPE-007 若后续实现阶段发现 API / DB / Orval 发生变化，必须同步 OpenAPI、Orval、docs、schema 和测试。

## 7. 测试与验证 AC

- [ ] AC-TEST-001 后续实现阶段必须在微信开发者工具或真机验证首页双行文案。
- [ ] AC-TEST-002 后续实现阶段必须逐页验证 search、category、product-list、tile-detail、favorites、certificates、store-info 的非首页单行标题。
- [ ] AC-TEST-003 后续实现阶段必须验证返回按钮在有页面栈和无页面栈两种情况下的行为。
- [ ] AC-TEST-004 后续实现阶段必须验证微信右侧原生胶囊可见、可用，且未被自定义导航遮挡。
- [ ] AC-TEST-005 后续实现阶段必须验证 tile-detail 分享路径仍包含当前 SKU 参数。
- [ ] AC-TEST-006 后续实现阶段必须记录或截图 320、375、430 pt 宽度下导航栏无重叠、内容不遮挡。
- [ ] AC-TEST-007 若 `find`、`profile` 后续接入 `custom-navigation`，必须验证其遵守非首页单行标题规则，或在后续需求中明确豁免。

## 横切 AC（knowledge-base）

本 REQ 为小程序导航 UI，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签，因此无 `AC-XCUT-*` 管理端横切验收项。

参考复盘：`docs/knowledge-base/retrospectives/sprint-007-retrospective.md` 中关于分层验收、成功路径 compact 输出和范围控制的经验，已转化到本文件的页面覆盖、范围与数据、测试与验证 AC。
