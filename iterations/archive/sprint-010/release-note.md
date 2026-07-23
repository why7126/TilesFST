---
sprint_id: sprint-010
status: completed
lifecycle_stage: archive
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-22 11:17:51
---

# sprint-010 发布说明

## 发布主题

密码校验规则简化、小程序多页面微信分享、SKU 名称/编码展示去重、SKU 编辑弹窗图片移除与主图规则、类目编辑弹窗字段与校验规则收敛、小程序 SKU 详情页品牌入口、分类页长名称、usage-events 上报、媒体上传大小限制一致性、生产 Banner 保存、管理端首页数据概览真实数据接入、Web 登录页工具区对齐修复与 Web 管理端移动端基础适配。

## 关联范围

| 类型 | 编号 | 标题 | 发布影响 |
|---|---|---|---|
| REQ | REQ-0063-password-validation-policy-simplification | 密码校验规则简化 | 新设置/重置密码入口统一为 5-32 位、包含英文字符和数字 |
| REQ | REQ-0064-miniapp-wechat-share-pages | 微信小程序多页面支持微信分享 | 首页、商品详情页、商品列表页、品牌详情页支持微信朋友与朋友圈分享 |
| REQ | REQ-0027-mobile-page-adaptation | Web 管理端移动端基础适配优化 | 已实现 Web 管理端页面在手机和小屏平板下达到基础可用；已创建 `update-web-admin-mobile-adaptation` |
| REQ | REQ-0065-sku-metadata-name-sku-dedup | SKU 元数据名称与编码展示去重 | SKU 编码作为系统自动生成唯一内部识别字段，商品名称作为用户填写与公开展示字段 |
| REQ | REQ-0067-admin-category-edit-modal-validation | 管理端类目编辑弹窗字段与校验规则 | 类目编码由系统自动生成且以 `CAT-` 开头；管理端弹窗不要求用户填写编码，类目名称和同层级唯一校验更严格；类目列表名称列第二行仅展示编码 |
| REQ | REQ-0066-admin-sku-image-removal-main-image-rules | 管理端 SKU 编辑弹窗商品图片移除与主图规则 | SKU 编辑弹窗支持移除图片；设置主图后自动前置；移除当前主图后自动选择后一张或剩余第一张为主图 |
| BUG | BUG-0070-miniapp-sku-detail-duplicate-brand-button | 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复 | 删除底部重复品牌按钮，保留内容区“查看品牌主页”入口 |
| BUG | BUG-0071-login-page-theme-language-selector-misalignment | 登录页右上角主题选择模块与语言选择模块没有对齐 | 统一登录页主题选择与语言选择工具区布局，提升入口页首屏一致性 |
| BUG | BUG-0072-miniapp-usage-events-bad-request | 微信小程序 usage-events 上报接口频繁返回 400 | 收敛小程序事件字典与后端接收契约，减少合法行为事件 400 噪音 |
| BUG | BUG-0073-video-upload-23m-file-fails | 上传 23M 文件失败，图片、视频和文档均受影响 | 统一图片、视频、文档上传限制、提示和错误响应，避免合法边界文件上传失败或错误不可诊断 |
| BUG | BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 生产环境小程序商品详情页品牌卡片误跳搜索页 | 修复商品详情页品牌卡片跳转目标，进入对应品牌详情页 |
| BUG | BUG-0077-miniapp-category-secondary-name-truncated | 微信小程序分类页二级分类名称超过 4 个字被省略 | 修复分类页二级分类长名称展示，避免超过 4 个字即省略导致不可辨识 |
| BUG | BUG-0075-prod-admin-brand-banner-save-fails | 生产环境管理端品牌类型 Banner 配置无法保存 | 修复生产管理端品牌详情 Banner 新增/编辑保存，补齐 MySQL schema drift/迁移证据与错误提示 |
| BUG | BUG-0079-admin-dashboard-overview-mock-data | 管理端首页数据概览仍使用 Mock 数据 | 管理端首页数据概览接入真实数据源，不再以 Mock 数据作为生产成功态 |
| Change | update-password-validation-policy | 密码策略规范更新 | 修改 auth、admin-password-change、user-management 能力规范 |
| Change | add-miniapp-wechat-share-pages | 小程序页面分享能力新增 | 修改 miniapp-home、miniapp-sku-detail-page、miniapp-product-list-page、miniapp-brand-detail-home-page、miniapp-global-custom-navigation-bar 与 miniapp-device-evidence-template 能力规范 |
| Change | fix-miniapp-sku-detail-duplicate-brand-button | SKU 详情页品牌入口规范修复 | 修改 miniapp-sku-detail-page 能力规范 |
| Change | fix-login-page-tool-selector-alignment | 登录页工具区布局规范修复 | 修改 web-client 管理端登录页能力规范 |
| Change | fix-miniapp-usage-events-contract-drift | 小程序 usage-events 上报契约修复 | 修改 product-usage-logging 能力规范 |
| Change | fix-upload-size-limit-consistency | 公共上传大小限制一致性修复 | 修改 object-storage、system-settings、brand-certificate-management 能力规范 |
| Change | fix-miniapp-sku-detail-brand-card-route | SKU 详情页品牌卡片路由修复 | 修改 miniapp-sku-detail-page 能力规范 |
| Change | fix-miniapp-category-secondary-name-truncated | 分类页二级分类长名称展示修复 | 修改 miniapp-category-list-page 能力规范 |
| Change | fix-prod-admin-brand-banner-save | 生产管理端品牌类型 Banner 保存修复 | 修改 banner-management、database、testing 能力规范 |
| Change | refine-sku-metadata-name-code-display | SKU 名称与编码展示规范调整 | 修改 tile-sku-management、miniapp-sku-detail-page、miniapp-product-list-page、miniapp-search 能力规范 |
| Change | refine-admin-category-edit-modal-validation | 类目弹窗字段与校验规范调整 | 修改 tile-category-management、web-client 能力规范 |
| Change | add-admin-sku-image-removal-main-image-rules | SKU 图片编辑规则规范调整 | 修改 tile-sku-management 能力规范 |
| Change | fix-admin-dashboard-overview-real-data | 管理端 Dashboard 数据概览真实数据修复 | 修改 admin-dashboard 能力规范 |

## 用户可见变化

- 管理端密码规则提示将从旧规则调整为：密码需为 5-32 位，并同时包含英文字符和数字。
- 修改密码、创建用户初始密码、管理员重置密码的基础策略保持一致。
- 小程序首页、商品详情页、商品列表页、品牌详情页可分享给微信朋友和微信朋友圈；分享打开后保留必要页面参数。
- Web 管理端登录页、Dashboard、SKU、品牌、用户、日志、系统设置等已实现页面在手机和小屏平板下不出现明显横向溢出、控件重叠、弹窗不可关闭或分页/筛选不可操作。
- 管理端 SKU 新增/编辑时用户填写“商品名称”，SKU 编码由系统自动生成并作为内部识别字段。
- 管理端 SKU 编辑弹窗中的商品图片可移除；设置主图后该图默认移动到第一位；移除当前主图后系统自动选择后一张图片或剩余第一张图片作为主图。
- 管理端类目新增/编辑弹窗不再显示可填写的类目编码；新增类目时系统生成 `CAT-` 前缀唯一编码。
- 管理端类目名称最多 10 个字符，仅允许中文、英文、数字；同一上级类目下不允许重名。
- 管理端类目列表名称列第一行只显示类目名称，第二行只显示类目编码，不再展示层级路径。
- 小程序/店主端商品卡片、详情、推荐、收藏、搜索结果和分享标题只展示商品名称，暂不展示 SKU 编码。
- 小程序 SKU 商品详情页底部操作区不再显示重复品牌按钮，用户通过内容区“查看品牌主页”进入品牌主页。
- 小程序收藏页、品牌详情页、商品/品牌卡片等关键行为的 usage-events 合法上报不再频繁返回 400。
- 管理端图片、视频、文档上传限制和提示更一致；约 23M 文件按产品规则可成功上传或获得明确限制提示。
- 小程序 SKU 商品详情页品牌卡片进入对应品牌详情页，不再误跳搜索页。
- 小程序分类页二级分类长名称可辨识，不再超过 4 个字即省略为不可判断含义的 `...`。
- 生产 Web 管理端可保存品牌类型 Banner；若品牌、Logo 或数据库状态不合法，返回可理解错误而不是静默失败或原始 SQL 异常。
- Web 管理端首页数据概览展示真实 SKU、品牌、Banner、用户统计，不再用 Mock 值误导管理员。
- Web 管理端登录页右上角主题选择与语言选择保持统一对齐，桌面和窄屏视口不遮挡登录内容。

## 技术发布注意

- 如实现阶段修改 OpenAPI schema 或错误码示例，发布前必须同步 Orval 和 API 文档。
- REQ-0064 默认不修改 API / DB / Orval；发布前需完成四页面分享矩阵、参数保留、运行入口同步、DevTools 320/375/430 与真机或 follow-up evidence。
- REQ-0027 默认不修改 API / DB / Orval / Docker / MinIO / 小程序；已完成 `/req-opsx REQ-0027-mobile-page-adaptation` 并回填 `update-web-admin-mobile-adaptation`，实现阶段覆盖 `375x812`、`390x844`、`768x1024`、`1440x1024` 视口 smoke 与截图 evidence。若触及 API、数据库、上传链路、环境变量或 Docker 配置，必须拆分或同步相应治理文档、OpenAPI/Orval 和测试。
- REQ-0065 需保留底层 `sku_code` 唯一性和系统识别稳定性，管理端公开主字段切换为商品名称，小程序/店主端隐藏编码；若 API schema、错误码或 DB 约束变化，必须同步 OpenAPI、Orval、数据库文档和测试。默认不涉及 Docker、MinIO 或媒体上传链路。
- REQ-0067 需保留底层 `tile_categories.code` 唯一性和系统识别稳定性，创建接口不再要求前端提交 `code`，后端生成 `CAT-` 前缀编码；类目列表名称列第二行仅展示编码，不展示层级路径；必须同步 OpenAPI、Orval、错误码文档和前后端测试。默认不涉及 DB 迁移、Docker、小程序、店主端、MinIO 或媒体上传链路。
- REQ-0066 默认只调整管理端 SKU 编辑弹窗图片数组状态、主图顺序和保存 payload；不物理删除 MinIO 对象，不新增 DB 表，不影响小程序或店主端。若实现阶段修改 SKU 图片请求/响应 schema 或错误码，必须同步 OpenAPI、Orval、API 文档和测试；若未触及上传链路，Docker 边界上传验收标记为 N/A。
- BUG-0070 如仅删除小程序前端重复按钮，不需要 OpenAPI / Orval；发布前需完成小程序静态测试和必要截图 evidence。
- BUG-0072 涉及 `POST /api/v1/usage-events` 契约与小程序事件字典收敛；若仅扩充后端事件定义或修正小程序 payload 且 schema 不变，不需要 Orval；若请求/响应结构变化，必须同步 OpenAPI、Orval、API 文档与错误码示例。
- BUG-0073 可能涉及系统设置 media 分组、上传错误响应、`.env.example`、对象存储文档、Docker/Nginx/生产代理配置说明和前端上传提示；若新增或修改 API 字段、错误码或 schema，必须同步 OpenAPI、Orval、API 文档与测试。
- BUG-0078 如仅调整 SKU 详情接口既有字段取值，不需要 Orval；发布前需完成后端接口测试和小程序品牌详情页跳转 evidence。
- BUG-0077 如仅调整小程序前端展示样式，不需要 OpenAPI / Orval；发布前需完成分类页长名称截图 evidence、点击入口回归和必要静态测试。
- BUG-0076 若仅恢复生产运行时或反代配置，不需要 OpenAPI / Orval；发布前需完成生产根路径、`/api/v1/health`、实际 SKU 接口、实际 `/media/{object_key}` 视频 URL 和微信真机播放 evidence。若修改 API schema、媒体错误结构或对象存储读取行为，必须同步 OpenAPI、Orval、API 文档和测试。
- BUG-0075 涉及生产 MySQL schema drift/迁移和管理端 Banner 保存链路；发布前需完成 `banners.brand_id` 表结构证据、品牌详情 Banner 新增/编辑、`brand_logo`/`custom_upload`、小程序展示读取和错误 envelope 验证。若 API schema 或错误码变化，必须同步 OpenAPI、Orval、API 文档和错误码文档。
- BUG-0079 涉及管理端 Dashboard 数据源真实化；发布前需完成 SKU/品牌/Banner/用户统计口径、loading/empty/error、权限边界、后端/API 和前端测试证据。若新增或修改 Dashboard 概览 API，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试；若复用既有接口且 schema 不变，需明确不需要 Orval。
- BUG-0071 如仅调整 Web 登录页布局，不需要 OpenAPI / Orval；发布前需完成 Web 登录页桌面/窄屏截图 evidence。
- BUG-0075 涉及数据库兼容路径；不应改变 MinIO 单桶策略或让前端直连对象存储。

## 当前状态

已完成归档。2026-07-22 11:17:51 关闭 sprint-010，16/16 个 Change 已归档，范围内 REQ/BUG 均迁入 archive；发布前仍需按产品发布流程确认生产 smoke、真机 evidence 和实际版本公告。
