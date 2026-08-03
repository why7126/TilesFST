---
sprint_id: sprint-014
title: Sprint 014 发布说明
status: published
lifecycle_stage: archive
created_at: 2026-07-29 15:51:41
updated_at: 2026-07-31 08:14:33
owner: product
---

# Sprint 014 发布说明

## 发布范围

| 类型 | ID | 标题 | 状态 |
|---|---|---|---|
| REQ | REQ-0081-release-image-build-governance | 发布镜像准备与构建治理 | done |
| Change | update-release-image-build-governance | 发布镜像准备与构建治理 | archived |
| REQ | REQ-0082-admin-category-name-special-characters | 管理后台瓷砖类目名称允许特殊字符 | done |
| Change | update-admin-category-name-special-characters | 管理后台瓷砖类目名称允许特殊字符 | archived |
| REQ | REQ-0083-miniapp-brand-list-category-summary | 小程序品牌列表页按品牌单行展示类目汇总 | done |
| Change | update-miniapp-brand-list-category-summary | 小程序品牌列表页按品牌单行展示类目汇总 | archived |
| REQ | REQ-0084-web-modal-disable-outside-close | Web 端所有弹窗禁用点击空白区域自动关闭 | done |
| Change | update-web-modal-disable-outside-close | Web 端所有弹窗禁用点击空白区域自动关闭 | archived |
| REQ | REQ-0085-miniapp-global-home-floating-button | 小程序非首页页面新增返回首页全局悬浮按钮 | done |
| Change | add-miniapp-global-home-floating-button | 小程序非首页页面新增返回首页全局悬浮按钮 | archived |
| BUG | BUG-0090-admin-sku-list-publish-sort-order | 管理端 SKU 列表默认排序未按发布状态使用业务时间 | done |
| Change | fix-admin-sku-list-publish-sort-order | 管理端 SKU 列表默认排序修复 | archived |
| BUG | BUG-0091-miniapp-product-list-sort-consistency | 小程序搜索商品结果页与分类商品列表页排序需与品牌详情页一致 | done |
| Change | fix-miniapp-product-list-sort-consistency | 小程序商品列表排序一致性修复 | archived |
| BUG | BUG-0092-miniapp-card-images-slow-load | 小程序体验版商品卡片图片加载很慢 | done |
| Change | fix-miniapp-card-image-loading | 小程序商品卡片图片加载性能修复 | archived |
| BUG | BUG-0093-miniapp-category-secondary-grid-name-full-display | 小程序分类页二级类目卡片 3 列布局导致名称未完整显示 | done |
| Change | fix-miniapp-category-secondary-grid-name-display | 小程序分类页二级类目名称完整展示修复 | archived |

## 用户可见变化

- 发布流程将明确判断当前版本是否需要镜像准备或镜像构建。
- 发布时若涉及 Dockerfile、Compose、构建脚本、环境变量、数据库 schema 或 migration 变化，将需要镜像构建计划或 manifest 证据。
- `/image-prepare` 与 `/image-build` 将分离：前者负责准备和校验输入，后者负责真实构建与产物清单。
- 管理后台瓷砖类目名称将在最多 15 个字符内支持中文、英文、数字和常见特殊字符，便于运营维护带连接符、斜杠、括号等业务表达的类目名称。
- 管理后台类目树默认只显示一级类目，支持通过 `+/-` 展开或收起子级类目，减少多级类目同时展示时的信息拥挤。
- 小程序品牌列表页顶部轮播保持不变，下半部品牌列表将调整为每行一个品牌，并展示品牌 Logo、品牌名称、商品数量和该品牌所有上架商品对应的末级类目名称；无商品品牌仅在左侧展示空态值、右侧留空；点击品牌 Logo / 名称进入品牌详情页，点击右侧类目进入该品牌该类目下的商品列表页。
- Web 管理端和展示端标准弹窗点击空白区域或遮罩时不再自动关闭，减少表单编辑、确认操作、详情预览和上传过程中的误触中断。
- 小程序非首页页面将提供统一的返回首页悬浮按钮，用户在搜索、分类列表、分类商品列表、品牌列表、品牌详情、证书列表、收藏列表和商品详情等页面可一键回到首页；首页本身不展示该按钮。
- 管理端 SKU 列表默认排序将按发布时间或创建时间保持稳定，减少刚发布或新建未发布商品位置不符合运营预期的问题。
- 小程序搜索商品结果页与分类商品列表页排序将与品牌详情页商品 Tab 保持一致，减少不同入口看到的商品顺序差异。
- 小程序商品卡片图片加载将优化为缩略图优先、非首屏按需加载，并补充缺图/对象不存在时的稳定占位降级。
- 小程序分类页二级类目卡片将调整为每行 2 个，并完整展示所有二级类目名称，避免规格和工艺描述被省略。

## 技术同步范围

- 新增或更新 image prepare / image build 技能入口。
- 扩展 `release.json` 模板和发布校验，增加 image gates、plan/manifest 引用和 blocker。
- 生成 `image-build-plan.json` 与 `image-manifest.json` 的校验脚本或等价能力。
- 更新生产镜像构建文档与发布规则。
- 补充 release validator、image plan、image manifest、敏感信息扫描和 hash 漂移测试。
- 更新类目创建 / 更新 API 校验、OpenAPI / Orval、管理端类目新增 / 编辑弹窗、类目列表 / 树 / 选择器展示回归。
- 补充后端 pytest、前端 Vitest / Testing Library、小程序和 Web 展示端分类入口回归证据。
- 确认或扩展小程序公开品牌列表接口，覆盖品牌公开商品数量与末级类目集合；如接口契约变更，同步 OpenAPI、Orval 或小程序 API 类型、接口文档和测试。
- 更新小程序品牌列表页布局、空态/错误态、品牌行点击、埋点和 DevTools 320/375/430 pt evidence。
- 更新 Web 标准 Dialog / Modal 外部点击关闭策略、共享弹窗默认配置、历史自定义弹窗盘点和前端交互测试；不涉及 API、数据库、Orval、小程序或 Docker。
- 更新小程序全局导航辅助能力、页面覆盖/例外清单、首页兜底跳转、防重复点击、底部安全区/TabBar/固定操作区避让和 DevTools 320/375/430 pt evidence。
- 更新管理端 SKU 列表默认排序或前端展示回归；如实现阶段触及 API 排序契约或数据库索引，需同步 OpenAPI、Orval、docs、DB 文档和测试。
- 更新小程序搜索结果页、分类商品列表页和品牌详情商品 Tab 的排序一致性回归；如实现阶段触及 API 排序字段，需同步契约和测试。
- 更新小程序首页、商品列表、搜索结果和品牌详情商品 Tab 的商品卡片图片加载策略，补充 `/media/{object_key}` 图片缓存、慢请求/失败观测、缩略图回填或对象一致性校验。
- 更新小程序分类页二级类目卡片布局、skeleton 布局和长名称展示回归证据；保持二级类目跳转参数不变。

## 不包含

- 不自动推送镜像到远程镜像仓库。
- 不直接实现 CI/CD 自动发布流水线。
- 不改变类目层级、编码自动生成、排序、启停、删除、历史数据清洗或媒体/存储能力。
- 不新增 Web 弹窗视觉体系，不默认改变 Popover、Dropdown、Tooltip、Select 下拉层或日期选择器等轻量浮层行为。
- 不改变品牌列表页顶部轮播图视觉、数据来源、跳转或兜底规则。
- 不改造品牌详情页、管理端品牌维护、类目管理规则、品牌搜索/筛选或 Web 展示端品牌列表。
- 不改变首页/TabBar 结构，不新增后端 API、数据库字段、管理端配置、Web 展示端能力或埋点报表。
- 不引入小程序直连未授权对象存储，不改变详情页高清图或视频 Range 能力。
- 除 BUG-0091 明确调整搜索商品结果页与分类商品列表页默认排序外，不改变分类树接口响应结构、数据库类目表结构、品牌页、首页“全部产品”排序或首页商品卡片布局。
- 不把真实 `.env`、数据库连接串、密钥、Authorization header、Cookie 或真实客户数据写入发布证据。

## 发布状态

当前为 published；Sprint 014 已于 2026-07-31 08:14:33 完成归档关闭。范围内 9 个 Change 均已归档，关联 REQ / BUG 已进入 archive 阶段；小程序 DevTools / 真机截图与体验版 Network evidence 仍按验收报告中的 follow_up 记录在发布前补录或标明不可用原因。
