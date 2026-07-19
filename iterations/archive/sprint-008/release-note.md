---
title: Sprint 008 发布说明
purpose: 记录 Sprint 008 规划期发布范围
content: 纳入 XL 管理端页面分层验收模板、Agent 上下文预算治理、微信小程序首页、自定义导航栏、首页样式信息架构优化，并承接品牌证书后续运营观察点
source: /sprint-propose
update_method: Sprint 范围变化或发布计划变化时同步更新
created_at: 2026-07-16 08:59:46
updated_at: 2026-07-19 15:31:45
---

# Sprint 008 发布说明

## 发布状态

已发布。当前正式发布对象为文档/治理型能力、小程序业务能力和小程序缺陷修复：XL 管理端页面分层验收模板、规则/Skill 已读摘要复用上下文预算治理、微信小程序首页首期闭环、微信小程序首页品牌自定义导航栏、微信小程序全局自定义导航栏、微信小程序首页样式与信息架构优化、微信小程序 SKU 详情页、微信小程序分类列表页、微信小程序搜索通用组件、微信小程序商品列表页通用组件、BUG-0065 小程序首页预览运行入口修复。

发布备注：本次按用户确认强制关闭 Sprint；微信开发者工具/真机相关视口验收残留作为人工 follow-up，不阻塞发布说明归档。

## 正式范围

| 类型 | 条目 | 状态 |
|---|---|---|
| REQ | REQ-0039 XL 管理端页面分层验收模板 | 已纳入 |
| REQ | REQ-0040 规则/Skill 已读摘要复用纳入命令上下文预算治理 | 已纳入 |
| REQ | REQ-0041 微信小程序首页 | 已纳入 |
| REQ | REQ-0042 微信小程序首页品牌自定义导航栏 | 已纳入；Change `add-miniapp-custom-navigation-bar` 已创建 |
| REQ | REQ-0043 微信小程序首页样式与信息架构优化 | 已纳入 |
| REQ | REQ-0044 微信小程序新增瓷砖 SKU 详情页 | 已纳入 |
| REQ | REQ-0045 新增分类列表页 | 已纳入 |
| REQ | REQ-0046 微信小程序搜索通用组件并应用 | 已纳入 |
| REQ | REQ-0047 微信小程序商品列表页通用组件并应用 | 已纳入 |
| REQ | REQ-0048 小程序全局自定义导航栏 | 已纳入；Change `add-miniapp-global-custom-navigation-bar` 已创建 |
| Change | add-miniapp-global-custom-navigation-bar | proposed |
| BUG | BUG-0065 微信小程序首页预览效果与 REQ-0041 原型和验收差异明显 | 已纳入 |
| Change | add-xl-admin-page-acceptance-template | proposed |
| Change | update-rule-skill-summary-reuse-context-budget | proposed |
| Change | add-miniapp-home | proposed |
| Change | update-miniapp-home-style-optimization | proposed |
| Change | add-miniapp-sku-detail-page | proposed |
| Change | add-miniapp-category-list-page | proposed |
| Change | add-miniapp-search-component | proposed |
| Change | add-miniapp-product-list-component | proposed |
| Change | fix-miniapp-home-preview-runtime-entry | in_progress |

## 待评审观察点

来自 `sprint-007` 复盘行动项 `A-005`：

- 过期证书提醒
- 证书类型统计
- 批量维护

以上内容仅作为后续 `/req-capture` 输入；在形成 approved REQ 与 OpenSpec Change 前，不进入正式发布说明。

## 影响范围

| 领域 | 当前结论 |
|---|---|
| API | 可能新增或调整小程序首页聚合、usage event、热销统计相关契约 |
| 数据库 | 若现有 usage events 不足以支撑热销统计，可能新增或扩展统计事件/聚合字段 |
| Web | 不影响 |
| 小程序 | 新增原生微信小程序首页、搜索、商品详情、门店信息、分享和咨询首期闭环；新增 SKU 详情页展示、媒体浏览、收藏、分享、品牌/推荐跳转和异常状态 |
| 小程序导航 | 纳入首页品牌自定义导航栏，明确 brand-header 品牌展示、右侧原生分享/关闭按钮、门店信息排除和搜索框下置；OpenSpec Change `add-miniapp-custom-navigation-bar` 已创建 |
| 小程序全局导航 | 纳入全局自定义导航栏，明确首页保留 brand-header、非首页左侧返回、右侧微信原生胶囊避让、状态栏避让和 fixed header 内容不遮挡；OpenSpec Change `add-miniapp-global-custom-navigation-bar` 已创建 |
| 小程序分类 | 新增 TabBar「分类」频道，覆盖一级/二级分类双栏浏览、分类树缓存、二级分类跳转、骨架/空/错误状态和分类埋点 |
| 小程序搜索 | 新增搜索通用组件、搜索首页、实时联想、搜索结果、筛选抽屉、无结果状态和搜索埋点；不包含管理端搜索配置中心 |
| 小程序商品列表 | 新增商品列表页通用组件、商品卡片、分类/搜索/品牌/推荐入口复用、筛选排序、分页加载、状态治理和商品列表埋点；OpenSpec Change `add-miniapp-product-list-component` 已创建 |
| 小程序体验优化 | 优化首页深色视觉、品牌 Header、四入口导航、新品/热销推荐、全部产品瀑布流、TabBar 目标文案和埋点预留 |
| 小程序修复 | 修复首页预览运行入口脱节，补充 `.ts`/`.js` 同步与空模板回归测试 |
| 管理端 | 影响后续管理端页面验收模板，不改运行时代码 |
| Orval | 若新增或调整小程序 API contract，则需要同步 |
| Docker Compose | 不需要 |

## 发布摘要

- 沉淀 XL 管理端页面分层验收模板，覆盖 DB/API/上传/Orval/Web/Docker/横切 UI gate。
- 将规则/Skill 已读摘要复用机制纳入 Agent 上下文预算治理。
- 增强命令 Skill 与预算校验，减少连续命令重复读取。
- 新增微信小程序首页首期闭环，覆盖首页聚合、搜索、商品详情、门店信息、分享、咨询和热销行为统计。
- 纳入微信小程序首页品牌自定义导航栏，下一步创建 OpenSpec Change，后续覆盖品牌 Header、右侧原生分享/关闭、门店信息排除、搜索框下置和真机避让验收。
- 纳入微信小程序首页样式与信息架构优化，已创建 OpenSpec Change，后续实施深色视觉、瀑布流和 TabBar 安全降级验收。
- 纳入微信小程序 SKU 详情页，已创建 OpenSpec Change，后续覆盖 SKU 信息、图片/视频混合轮播、图片预览、收藏、分享、品牌入口、同系列/同品牌推荐和异常状态。
- 纳入微信小程序分类列表页，已创建 OpenSpec Change，后续覆盖分类 Tab、一级/二级分类、分类树接口、缓存版本号、跳转防抖、图片占位、异常状态和埋点。
- 纳入微信小程序搜索通用组件并应用，已创建 OpenSpec Change，后续覆盖搜索入口组件、搜索首页、联想、结果、筛选、无结果、埋点和小程序原型验收。
- 纳入微信小程序商品列表页通用组件并应用，已创建 OpenSpec Change，后续覆盖商品列表容器、商品卡片、筛选排序、分页加载、状态治理、埋点和小程序原型验收。
- 纳入微信小程序全局自定义导航栏，已创建 OpenSpec Change，后续覆盖首页 brand-header 保留、非首页返回、原生胶囊避让、状态栏避让和 fixed header 内容避让。
- 修复 BUG-0065，确保微信开发者工具首页预览加载真实首页业务逻辑，避免空模板 `.js` 覆盖 `.ts` 实现。
