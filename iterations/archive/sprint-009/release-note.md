---
sprint_id: sprint-009
status: completed
lifecycle_stage: archive
created_at: 2026-07-19 12:50:12
updated_at: 2026-07-20 23:23:22
---

# sprint-009 发布说明

## 发布主题

微信小程序商品浏览、品牌展示、品牌列表页、证书列表页、添加到我的小程序引导语、管理后台 Banner 投放范围配置优化、分类导航、商品列表双列卡片、SKU 详情页视频播放修复、用户收藏列表、顶部导航、自定义导航 best-practice、设备验收证据、首页推荐入口、首页设备验收残留、搜索体验优化与管理端品牌证书组件复用。

## 计划范围

| 类型 | 编号 | 标题 | 发布说明 |
|---|---|---|---|
| REQ | REQ-0049-miniapp-product-card-component | 微信小程序商品卡片组件 | 统一小程序各类商品列表中的商品卡片展示、图片占位、点击跳转和异常状态 |
| REQ | REQ-0050-miniapp-brand-header-page-title-rules | 小程序 brand-header 页面标题规则 | 统一首页双行品牌文案与非首页单行标题规则，优化返回、状态栏和微信原生胶囊避让体验 |
| REQ | REQ-0051-category-list-product-list-entry-by-level | 分类列表页支持一二级分类商品列表入口 | 支持从一级分类查看下属二级分类商品聚合结果，并保留二级分类精确商品列表入口 |
| REQ | REQ-0052-miniapp-device-evidence-template | 小程序 DevTools/真机验收 evidence 模板 | 建立小程序 DevTools/真机验收 evidence 模板，区分自动化、设备验收和人工 follow-up 证据 |
| REQ | REQ-0053-miniapp-custom-navigation-best-practice | 小程序自定义导航 best-practice 沉淀 | 沉淀小程序自定义导航 best-practice，统一状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵 |
| REQ | REQ-0054-brand-card-common-component | 生成品牌卡片通用组件 | 沉淀微信小程序品牌卡片组件，统一品牌 Logo、品牌名称、入口提示、Logo fallback 和点击跳转体验 |
| REQ | REQ-0055-brand-certificate-common-component | 生成品牌证书通用组件 | 沉淀管理端品牌证书缩略图、状态 Badge、预览入口和文件卡片，提升品牌证书页面组件复用与验收一致性 |
| REQ | REQ-0056-product-list-card-only-layout | 商品列表页改为双列商品卡片展示 | 收敛微信小程序商品列表页展示策略，移除搜索、筛选和排序控件，采用一行 2 个商品卡片直接浏览 |
| REQ | REQ-0057-certificate-list-page | 新增证书列表页 | 新增微信小程序公开证书列表页，支持证书卡片、搜索筛选、分页加载、图片/PDF 预览、安全过滤和小程序导航设备验收 |
| REQ | REQ-0059-favorite-list-page | 新增收藏列表页 | 新增用户侧收藏列表页，集中展示已收藏对象，支持详情跳转、取消收藏、空状态、未登录状态和状态同步 |
| REQ | REQ-0060-brand-list-page | 新增品牌列表页 | 新增微信小程序品牌列表页，提供品牌轮播、一行 2 个品牌卡片、品牌跳转、公开品牌过滤和小程序导航设备验收 |
| REQ | REQ-0061-miniapp-share-add-guide | 小程序添加到我的小程序引导语 | 新增右上角原生入口附近的添加到我的小程序轻量引导，支持手工关闭、胶囊避让和设备 evidence 验收 |
| REQ | REQ-0062-admin-banner-placement-scope | 管理后台 Banner 投放范围配置优化 | 收敛 Banner 管理投放范围为小程序首页轮播和品牌列表页轮播，并清理旧 Web/专题/历史位置 Banner 业务数据 |
| BUG | BUG-0066-search-component-prototype-deviation | 搜索组件整体交互与原型差异较大 | 修复小程序搜索页与 REQ-0046 原型在搜索首页、联想、结果、筛选和无结果状态上的体验偏差 |
| BUG | BUG-0067-home-recommendation-list-entry-routing | 首页推荐模块查看更多和榜单入口误跳搜索页 | 修复首页新品榜、热销榜和推荐模块「查看更多」误入搜索页的问题，进入对应商品列表页 |
| BUG | BUG-0068-miniapp-home-device-acceptance-followup | Sprint 008 小程序首页 DevTools 与真机验收残留未闭环 | 补齐小程序首页 DevTools / 真机、320-430 pt、胶囊避让和内容不遮挡 evidence，避免把自动化侧证误写为真机通过 |
| BUG | BUG-0069-miniapp-sku-detail-carousel-video-not-playable | SKU 商品详情页轮播图视频不能显示和播放 | 修复 SKU 商品详情页轮播图视频 URL 生成字段错误，确保视频项能显示和播放，并保持图片轮播兼容 |

## 当前状态

- Sprint 状态：completed
- OpenSpec Change：`REQ-0049` 已创建 `update-miniapp-product-card-component`；`REQ-0053` 已创建 `add-miniapp-custom-navigation-best-practice`；`REQ-0055` 已创建 `update-brand-certificate-common-component`；`REQ-0056` 已创建 `update-miniapp-product-list-card-only-layout`；`REQ-0057` 已创建 `add-miniapp-certificate-list-page`；`REQ-0059` 已创建 `add-favorite-list-page`；`REQ-0060` 已创建 `add-brand-list-page`；`REQ-0061` 已创建 `add-miniapp-share-add-guide`；`REQ-0062` 已创建 `update-admin-banner-placement-scope`；`BUG-0069` 已创建 `fix-miniapp-sku-detail-video-url`；`REQ-0050`、`REQ-0051`、`REQ-0052`、`REQ-0054`、`BUG-0066`、`BUG-0067` 与 `BUG-0068` 仍待 `/req-opsx` 或 `/bug-opsx` 创建
- 发布结论：已完成 Sprint 归档范围内 18 个 OpenSpec Change 的归档闭环；小程序 DevTools 截图类 evidence 使用静态视口 evidence 与 follow_up 边界记录，未冒充真机或 DevTools 截图通过。

## 不包含

- 商品列表容器、筛选、排序、分页状态机
- 除 BUG-0069 视频 URL 修复外的 SKU 详情页新增能力
- Web 端商品卡片
- 商品后台管理和交易能力
- 三级及以上分类模型、后台分类管理或分类页直接展示商品卡片
- 后台搜索配置中心、热门词维护、同义词维护或自然语言搜索
- brand-header 后台文案配置、底部 TabBar 改造或小程序整体视觉重设计
- 小程序自定义导航组件源码重构、自动化截图工具链或历史设备 evidence 全量回填
- 商品列表页 UI 重构、后端 section 语义调整或推荐算法调整
- 搜索页自身搜索、筛选和结果页能力调整
- 收藏分组、分享收藏夹、购物车、询价单、在线下单、推荐算法或管理端收藏运营
- 品牌主页完整信息架构、品牌商品列表容器、Web 端品牌卡片、管理端品牌操作、品牌 API/DB/Logo 上传链路；`REQ-0060` 仅覆盖小程序品牌列表页入口、轮播和双列品牌卡片列表
- 管理端品牌证书维护、店主 Web 证书展示、证书审批、OCR 或真伪校验；`REQ-0057` 仅覆盖小程序公开证书列表与受控预览
- 小程序添加引导语后台配置、服务端频率控制、运营弹窗或埋点接口；`REQ-0061` 默认只覆盖本地轻量引导和关闭状态
- Web 展示端 Banner、专题页 Banner、其他历史运营位保留或迁移；`REQ-0062` 明确删除不符合小程序首页轮播/品牌列表页轮播范围的旧 Banner 业务记录，但不物理删除 MinIO 对象
- 自动化截图工具链、真机云测能力或历史设备 evidence 全量回填
- 非 BUG-0068 范围内的历史小程序页面真机 evidence 全量补录
