---
note: workflow-sync — 18/18 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-009
status: completed
lifecycle_stage: archive
created_at: 2026-07-19 12:50:12
updated_at: 2026-07-20 23:30:55
---

# sprint-009 验收报告

## 验收范围

| 类型 | 编号 | 标题 | 当前状态 | 验收结论 |
|---|---|---|---|---|
| REQ | REQ-0049-miniapp-product-card-component | 微信小程序商品卡片组件 | done，已归档（`update-miniapp-product-card-component` archived 2026-07-19 18:09:44） | 待 OpenSpec Change、实现与验收 |
| REQ | REQ-0050-miniapp-brand-header-page-title-rules | 小程序 brand-header 页面标题规则 | done，已归档（`update-miniapp-brand-header-title-rules` archived 2026-07-19 20:47:02） | 待 OpenSpec Change、实现与验收 |
| REQ | REQ-0051-category-list-product-list-entry-by-level | 分类列表页支持一二级分类商品列表入口 | done，已归档（`update-miniapp-category-product-list-entry` archived 2026-07-19 18:14:48） | 待 OpenSpec Change、实现与验收 |
| REQ | REQ-0052-miniapp-device-evidence-template | 小程序 DevTools/真机验收 evidence 模板 | done，已归档（`add-miniapp-device-evidence-template` archived 2026-07-19 18:11:18） | 待 OpenSpec Change、实现与验收 |
| REQ | REQ-0053-miniapp-custom-navigation-best-practice | 小程序自定义导航 best-practice 沉淀 | done，已归档（`add-miniapp-custom-navigation-best-practice` archived 2026-07-19 20:59:58） | 已创建 OpenSpec Change，待实现与验收 |
| REQ | REQ-0054-brand-card-common-component | 生成品牌卡片通用组件 | done，已归档（`add-miniapp-brand-card-component` archived 2026-07-19 21:11:26） | 待 OpenSpec Change、实现与验收 |
| REQ | REQ-0055-brand-certificate-common-component | 生成品牌证书通用组件 | done，已归档（`update-brand-certificate-common-component` archived 2026-07-19 18:14:29） | 已创建 OpenSpec Change，待实现与验收 |
| REQ | REQ-0056-product-list-card-only-layout | 商品列表页改为双列商品卡片展示 | done，已归档（`update-miniapp-product-list-card-only-layout` archived 2026-07-20 14:56:25） | 已完成小程序列表页双列卡片实现、静态测试、后端分类聚合回归与真机验收 |
| REQ | REQ-0057-certificate-list-page | 新增证书列表页 | done，已归档（`add-miniapp-certificate-list-page` archived 2026-07-20 10:22:00） | 待实现与验收 |
| REQ | REQ-0059-favorite-list-page | 新增收藏列表页 | done，已归档（`add-favorite-list-page` archived 2026-07-20 18:06:16） | 待实现与验收 |
| REQ | REQ-0060-brand-list-page | 新增品牌列表页 | done，已归档（`add-brand-list-page` archived 2026-07-20 23:23:22） | 已完成品牌入口、品牌列表页、品牌轮播、双列品牌卡片、公开品牌过滤、静态测试与 `implementation/device-evidence.md` 静态视口 evidence；真机/DevTools 截图为 follow_up |
| REQ | REQ-0061-miniapp-share-add-guide | 小程序添加到我的小程序引导语 | done，已归档（`add-miniapp-share-add-guide` archived 2026-07-20 23:23:22） | 已完成首页轻量引导、两行文案、右上角三点提示符、关闭状态、静态测试、用户确认真机验收与 320/375/430 pt 静态视口 evidence；未声称 DevTools 截图通过 |
| REQ | REQ-0062-admin-banner-placement-scope | 管理后台 Banner 投放范围配置优化 | done，已归档（`update-admin-banner-placement-scope` archived 2026-07-20 22:51:30） | 待实现与验收；需覆盖展示端/位置收敛、旧数据删除、品牌列表页轮播分流、API/DB/Orval 与管理端横切 AC |
| BUG | BUG-0066-search-component-prototype-deviation | 搜索组件整体交互与原型差异较大 | done，已归档（`fix-miniapp-search-prototype-alignment` archived 2026-07-19 18:14:29） | 待 OpenSpec Change、修复与回归验收 |
| BUG | BUG-0067-home-recommendation-list-entry-routing | 首页推荐模块查看更多和榜单入口误跳搜索页 | done，已归档（`fix-miniapp-home-recommendation-routing` archived 2026-07-19 18:26:06） | 待 OpenSpec Change、修复与回归验收 |
| BUG | BUG-0068-miniapp-home-device-acceptance-followup | Sprint 008 小程序首页 DevTools 与真机验收残留未闭环 | done，已归档（`fix-miniapp-home-device-acceptance` archived 2026-07-19 21:13:20） | 待 OpenSpec Change、修复与回归验收 |
| BUG | BUG-0069-miniapp-sku-detail-carousel-video-not-playable | SKU 商品详情页轮播图视频不能显示和播放 | done，已归档（`fix-miniapp-sku-detail-video-url` archived 2026-07-20 08:57:35） | 已创建 OpenSpec Change，待修复与回归验收 |

## 验收 Gate

- [ ] `REQ-0049` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [ ] `REQ-0050` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [ ] `REQ-0051` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [ ] `REQ-0052` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [x] `REQ-0053` 已通过 `/req-opsx` 创建 OpenSpec Change `add-miniapp-custom-navigation-best-practice`。
- [ ] `REQ-0054` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [ ] `REQ-0055` 已通过 `/req-opsx` 创建 OpenSpec Change。
- [x] `REQ-0056` 已通过 `/req-opsx` 创建 OpenSpec Change `update-miniapp-product-list-card-only-layout`。
- [x] `REQ-0057` 已通过 `/req-opsx` 创建 OpenSpec Change `add-miniapp-certificate-list-page`。
- [x] `REQ-0059` 已通过 `/req-opsx` 创建 OpenSpec Change `add-favorite-list-page`。
- [x] `REQ-0060` 已通过 `/req-opsx` 创建 OpenSpec Change `add-brand-list-page`。
- [x] `REQ-0061` 已通过 `/req-opsx` 创建 OpenSpec Change `add-miniapp-share-add-guide`。
- [x] `REQ-0062` 已通过 `/req-opsx` 创建 OpenSpec Change `update-admin-banner-placement-scope`。
- [ ] `BUG-0066` 已通过 `/bug-opsx` 创建修复 OpenSpec Change。
- [ ] `BUG-0067` 已通过 `/bug-opsx` 创建修复 OpenSpec Change。
- [ ] `BUG-0068` 已通过 `/bug-opsx` 创建修复 OpenSpec Change。
- [x] `BUG-0069` 已通过 `/bug-opsx` 创建修复 OpenSpec Change `fix-miniapp-sku-detail-video-url`。
- [x] 生成的 Change 已回填到 `iterations/archive/sprint-009/sprint.yaml` 的 `changes[]`。
- [ ] 商品卡片组件实现完成，并对照 `acceptance.md` 的 AC-001 至 AC-016 验收。
- [ ] brand-header 页面标题规则实现完成，并对照 REQ-0050 `acceptance.md` 的 AC-HOME、AC-TITLE、AC-BACK、AC-WX、AC-LAYOUT 与 AC-TEST 验收。
- [ ] 分类列表页一二级分类商品列表入口实现完成，并对照 REQ-0051 `acceptance.md` 的 AC-001 至 AC-029 验收。
- [ ] 小程序设备 evidence 模板实现完成，并对照 REQ-0052 `acceptance.md` 的 AC-STRUCT、AC-STATE、AC-DEVTOOLS、AC-DEVICE、AC-BOUNDARY、AC-SAFE 与 AC-REF 验收。
- [ ] 小程序自定义导航 best-practice 实现完成，并对照 REQ-0053 `acceptance.md` 的 AC-STRUCT、AC-SAFEAREA、AC-CAPSULE、AC-BACK、AC-OFFSET、AC-CHECK、AC-MATRIX、AC-SCOPE 与 AC-REF 验收。
- [ ] 品牌卡片组件实现完成，并对照 REQ-0054 `acceptance.md` 的 AC-001 至 AC-022 验收。
- [ ] 品牌证书通用组件实现完成，并对照 REQ-0055 `acceptance.md` 的 AC-001 至 AC-030、AC-UI-001 至 AC-UI-007、AC-API-001 至 AC-API-004 与 AC-XCUT-001 至 AC-XCUT-010 验收。
- [x] 商品列表页双列卡片展示实现完成，并对照 REQ-0056 `acceptance.md` 的 AC-001 至 AC-017 与 AC-UI-001 至 AC-UI-012 验收；用户已确认完成真机验收。
- [ ] 证书列表页实现完成，并对照 REQ-0057 `acceptance.md` 的 AC-001 至 AC-025 与 AC-XCUT-N/A 验收；需补公开证书 API、证书卡片、搜索筛选、图片/PDF 预览、安全过滤、埋点、自定义导航与 320/375/430 pt evidence。
- [ ] 收藏列表页实现完成，并对照 REQ-0059 `acceptance.md` 的 AC-001 至 AC-022 与 AC-UI-001 至 AC-UI-009 验收；若覆盖小程序，需补自定义导航与 320/375/430 pt evidence。
- [x] 品牌列表页实现完成，并对照 REQ-0060 `acceptance.md` 的 AC-001 至 AC-DOC-004 验收；品牌轮播、双列品牌卡片、TabBar、状态栏、胶囊 reserve 与 320/375/430 pt 静态视口 evidence 已记录在 `openspec/changes/archive/2026-07-20-add-brand-list-page/implementation/device-evidence.md`。
- [x] 添加到我的小程序引导语实现完成，并对照 REQ-0061 `acceptance.md` 的 AC-001 至 AC-SCOPE-005 验收；首页轻量引导、两行文案、右上角小/大/小三点提示符、胶囊 bottom/right 定位、right 52px fallback、手工关闭、当前会话不重复展示、API / DB / Orval N/A、静态测试、用户确认真机验收与 320/375/430 pt 静态视口 evidence 已完成。
- [ ] 管理后台 Banner 投放范围配置优化实现完成，并对照 REQ-0062 `acceptance.md` 的 AC-001 至 AC-XCUT-010 验收；需确认展示端仅小程序、展示位置仅首页轮播/品牌列表页轮播、旧 Web/专题/历史位置 Banner 业务记录删除、品牌列表页轮播不复用首页轮播、OpenAPI/Orval/DB 文档与测试同步。
- [ ] 搜索组件原型偏差已修复，并对照 BUG-0066 `acceptance.md` 的 AC-BUG-001 至 AC-BUG-014 验收。
- [ ] 首页推荐入口路由已修复，并对照 BUG-0067 `acceptance.md` 的 AC-BUG-001 至 AC-BUG-008 验收。
- [ ] Sprint 008 小程序首页 DevTools / 真机验收残留已闭环，并对照 BUG-0068 `acceptance.md` 的 AC-001 至 AC-008 验收。
- [ ] SKU 商品详情页轮播视频 URL 已修复，并对照 BUG-0069 `acceptance.md` 的视频展示、视频播放、图片兼容和小程序 evidence 验收。
- [ ] 小程序原型与实现差异已记录或修正。
- [ ] Workflow Sync 与 AI usage hook 成功路径保持 compact summary。

## 风险与备注

- 当前 sprint-009 已纳入 REQ-0049、REQ-0050、REQ-0051、REQ-0052、REQ-0053、REQ-0054、REQ-0055、REQ-0056、REQ-0057、REQ-0059、REQ-0060、REQ-0061、REQ-0062、BUG-0066、BUG-0067、BUG-0068 与 BUG-0069；REQ-0062 纳入后总估算 36.0/30.0 人天，容量占用 120.00%，等于硬阻断阈值但未超过，后续必须冻结新增范围。REQ-0056 已完成商品列表页搜索/筛选/排序移除、双列 `product-card` grid 复用、入口上下文与分页状态保留，并补充修正一级分类商品列表接口语义：`categoryLevel=primary` 同时返回一级分类直挂 SKU 与启用二级子分类 SKU。相关后端回归 `test_miniapp_product_list_primary_category_aggregates_self_and_enabled_children` 与商品列表筛选回归已通过；用户已确认完成真机验收。REQ-0061 已完成两行引导文案、小/大/小三点提示符、贴近分享按钮的定位微调和用户确认真机验收，仍待 DevTools 320/375/430 pt evidence；REQ-0057、REQ-0060 与 REQ-0062 当前仍需继续实现或验收；BUG-0069 已完成代码修复与目标自动化测试，仍待 OpenSpec CLI strict 校验恢复后完成 1.3 并进入 applied。

## 归档结论

- 归档时间：2026-07-20 23:23:22
- Readiness：PASS，18/18 Change archived，351/351 tasks complete。
- Sprint 结论：completed / archive。
- AI usage：`ai_usage_mode: estimated_fallback`，原因是当前未提供本地 session JSONL 且 snapshot stale；影响为无法声明使用真实 token 快照，建议后续运行 `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-009 --json` 刷新。
