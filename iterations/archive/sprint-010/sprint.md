---
note: workflow-sync — workflow-sync 自动同步 — 16/16 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-010
status: completed
lifecycle_stage: archive
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-22 11:32:00
---

# sprint-010 迭代规划

## 1. Sprint 目标

本 Sprint 聚焦低风险规则修复、入口页体验收敛、小程序分享链路补齐、媒体上传链路一致性修复、SKU 名称/编码展示去重、类目编辑弹窗字段与校验规则收敛、SKU 编辑弹窗图片移除与主图兜底、生产主题偏好反馈修复、生产 Banner 保存链路恢复、管理端首页数据概览真实数据接入、管理端 Banner 图片完整预览修复与 Web 管理端移动端基础适配，将 `REQ-0063-password-validation-policy-simplification`、`REQ-0064-miniapp-wechat-share-pages`、`REQ-0027-mobile-page-adaptation`、`REQ-0065-sku-metadata-name-sku-dedup`、`REQ-0067-admin-category-edit-modal-validation`、`REQ-0066-admin-sku-image-removal-main-image-rules`、`BUG-0070-miniapp-sku-detail-duplicate-brand-button`、`BUG-0071-login-page-theme-language-selector-misalignment`、`BUG-0072-miniapp-usage-events-bad-request`、`BUG-0073-video-upload-23m-file-fails`、`BUG-0074-prod-theme-preference-sync-toast-persistent`、`BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search`、`BUG-0077-miniapp-category-secondary-name-truncated`、`BUG-0075-prod-admin-brand-banner-save-fails`、`BUG-0079-admin-dashboard-overview-mock-data`、`BUG-0080-admin-banner-image-preview-cropped` 纳入正式迭代范围。目标是在不改变既有认证安全边界、登录接口契约、小程序导航边界、对象存储安全边界、SKU 唯一编码系统识别边界、SKU 图片对象存储物理删除边界、类目编码内部识别边界、Banner 投放范围、Banner API/数据库契约和管理端权限边界的前提下，同步完成密码策略简化、小程序 SKU 详情页底部重复品牌按钮移除、商品详情页品牌卡片跳转品牌详情页修复、SKU 编码由系统自动生成且小程序/店主端隐藏展示、SKU 编辑弹窗商品图片可移除、设主图自动前置与移除主图后自动兜底、类目编码由系统自动生成且管理端弹窗隐藏填写入口、分类页二级分类长名称展示修复、微信小程序 usage-events 上报契约漂移修复、图片/视频/文档上传大小限制一致性修复、生产主题偏好同步失败提示常驻修复、生产管理端品牌类型 Banner 保存失败修复、管理端首页数据概览真实数据接入、管理端 Banner 列表和弹窗图片完整预览修复、Web 管理端登录页右上角工具区对齐修复、首页/商品详情页/商品列表页/品牌详情页微信分享能力，以及当前已实现 Web 管理端页面在手机和小屏平板下的基础可用性。

正式目标：

- `REQ-0063-password-validation-policy-simplification`：统一修改本人密码、创建用户初始密码、管理员重置密码等入口的新密码策略，清理旧的 8 位、大小写和特殊字符提示，确保前后端规则一致。
- `REQ-0064-miniapp-wechat-share-pages`：小程序首页、商品详情页、商品列表页、品牌详情页支持分享给微信朋友和朋友圈，分享直达后保留必要参数，埋点失败不阻断分享。
- `REQ-0027-mobile-page-adaptation`：Web 管理端已实现页面完成移动端基础适配，确保 AdminLayout、筛选区、表格、分页、弹窗、抽屉、登录页和无权限页在 `375x812`、`390x844`、`768x1024` 与桌面回归视口下无明显溢出、重叠或不可操作；`update-web-admin-mobile-adaptation` 已 apply，待 archive。
- `REQ-0065-sku-metadata-name-sku-dedup`：SKU 编码保留为系统自动生成的唯一内部识别字段，商品名称作为用户填写与公开展示字段；管理端不要求手填编码，小程序/店主端隐藏编码。
- `REQ-0067-admin-category-edit-modal-validation`：管理端类目新增 / 编辑弹窗不展示可填写的类目编码，类目编码由后端生成 `CAT-` 前缀唯一值；上级类目、类目名称、排序权重必填，类目名称最多 10 个字符且仅允许中文、英文、数字，同一上级下名称唯一；类目列表名称列第一行展示类目名称，第二行仅展示类目编码，不展示层级路径。
- `REQ-0066-admin-sku-image-removal-main-image-rules`：管理端 SKU 编辑弹窗支持移除任意商品图片；设置主图后自动移动到第一位；移除当前主图时按后一张图片优先、否则剩余第一张图片自动兜底为主图；默认不改变上传接口、对象存储物理删除、API / DB / Orval。
- `BUG-0070-miniapp-sku-detail-duplicate-brand-button`：删除小程序 SKU 商品详情页底部重复品牌按钮，保留内容区“查看品牌主页”入口，回归底部操作区布局稳定性。
- `BUG-0071-login-page-theme-language-selector-misalignment`：统一 Web 管理端登录页主题选择模块与语言选择模块的工具区布局，回归桌面/窄屏对齐、主题切换、语言按钮可访问性和登录流程。
- `BUG-0072-miniapp-usage-events-bad-request`：收敛微信小程序 usage-events 上报事件字典与后端 `POST /api/v1/usage-events` 契约，关键页面访问和交互事件不再因未知事件或缺失字段大量返回 400。
- `BUG-0073-video-upload-23m-file-fails`：统一图片、视频、文档上传大小限制、系统设置、前端提示、后端校验和部署代理配置，约 23M 合法文件符合产品规则时可上传或被清晰拒绝。
- `BUG-0074-prod-theme-preference-sync-toast-persistent`：修复生产 Web 管理端主题偏好同步失败提示常驻问题，确保失败提示自动消失或可关闭，本机主题保持生效，并补账号偏好同步生产链路证据。
- `BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search`：修复生产小程序 SKU 商品详情页品牌卡片误跳搜索页，确保 SKU 详情接口返回品牌详情页路径，并回归品牌入口链路。
- `BUG-0077-miniapp-category-secondary-name-truncated`：修复微信小程序分类页二级分类名称超过 4 个字被省略为 `...` 的展示问题，确保长名称可辨识、布局稳定且分类点击入口正确。
- `BUG-0075-prod-admin-brand-banner-save-fails`：修复生产环境 Web 管理端品牌类型 Banner 无法保存问题，补齐 MySQL 既有表迁移或 drift 检查、品牌详情 Banner 保存回归、明确错误提示和小程序展示读取证据。
- `BUG-0079-admin-dashboard-overview-mock-data`：修复管理端首页数据概览仍使用 Mock 数据问题，移除生产页面 Mock 成功态，接入真实后端数据源或受鉴权保护的 Dashboard 概览 API，补 loading、empty、error、权限边界和指标口径回归。
- `BUG-0080-admin-banner-image-preview-cropped`：修复管理端 Banner 列表缩略图与新建/编辑弹窗图片预览显示不全问题，确保横幅图、方图、竖图和超宽图完整可识别，且不改变 Banner API、数据库、对象存储或展示端投放策略。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0063-password-validation-policy-simplification | 密码校验规则简化 | done | 1.0 人天 | archived `update-password-validation-policy`（2026-07-21 23:01:00） |
| REQ | REQ-0064-miniapp-wechat-share-pages | 微信小程序多页面支持微信分享 | done | 3.0 人天 | archived `add-miniapp-wechat-share-pages`（2026-07-21 22:57:26） |
| REQ | REQ-0027-mobile-page-adaptation | Web 管理端移动端基础适配优化 | done | 5.0 人天 | archived `update-web-admin-mobile-adaptation`（2026-07-22 09:24:02） |
| REQ | REQ-0065-sku-metadata-name-sku-dedup | 瓷砖 SKU 元数据名称与编码展示去重 | done | 3.0 人天 | archived `refine-sku-metadata-name-code-display`（2026-07-22 09:56:14） |
| REQ | REQ-0067-admin-category-edit-modal-validation | 管理端类目编辑弹窗字段与校验规则 | done | 3.0 人天 | archived `refine-admin-category-edit-modal-validation`（2026-07-22 09:55:00） |
| REQ | REQ-0066-admin-sku-image-removal-main-image-rules | 管理端 SKU 编辑弹窗商品图片移除与主图规则 | done | 1.0 人天 | archived `add-admin-sku-image-removal-main-image-rules`（2026-07-22 09:58:04） |
| BUG | BUG-0070-miniapp-sku-detail-duplicate-brand-button | 小程序商品详情页底部品牌按钮与内容区查看品牌主页重复 | done | 1.0 人天 | archived `fix-miniapp-sku-detail-duplicate-brand-button`（2026-07-21 22:54:39） |
| BUG | BUG-0071-login-page-theme-language-selector-misalignment | 登录页右上角主题选择模块与语言选择模块没有对齐 | done | 1.0 人天 | archived `fix-login-page-tool-selector-alignment`（2026-07-21 23:00:30） |
| BUG | BUG-0072-miniapp-usage-events-bad-request | 微信小程序 usage-events 上报接口频繁返回 400 | done | 1.0 人天 | archived `fix-miniapp-usage-events-contract-drift`（2026-07-21 15:26:34） |
| BUG | BUG-0073-video-upload-23m-file-fails | 上传 23M 文件失败，图片、视频和文档均受影响 | done | 3.0 人天 | archived `fix-upload-size-limit-consistency`（2026-07-21 23:00:59） |
| BUG | BUG-0074-prod-theme-preference-sync-toast-persistent | 生产环境主题偏好同步失败提示持续不消失 | done | 1.0 人天 | archived `fix-theme-preference-sync-toast-persistent`（2026-07-22 08:57:20） |
| BUG | BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 生产环境小程序商品详情页品牌卡片误跳搜索页 | done | 1.0 人天 | archived `fix-miniapp-sku-detail-brand-card-route`（2026-07-22 09:01:56） |
| BUG | BUG-0077-miniapp-category-secondary-name-truncated | 微信小程序分类页二级分类名称超过 4 个字被省略 | done | 1.0 人天 | archived `fix-miniapp-category-secondary-name-truncated`（2026-07-21 15:28:09） |
| BUG | BUG-0075-prod-admin-brand-banner-save-fails | 生产环境管理端品牌类型 Banner 配置无法保存 | done | 3.0 人天 | archived `fix-prod-admin-brand-banner-save`（2026-07-21 23:00:44） |
| BUG | BUG-0079-admin-dashboard-overview-mock-data | 管理端首页数据概览仍使用 Mock 数据 | done | 3.0 人天 | archived `fix-admin-dashboard-overview-real-data`（2026-07-22 09:19:39） |
| BUG | BUG-0080-admin-banner-image-preview-cropped | 管理端 Banner 列表和弹窗中 Banner 图片显示不全 | done | 1.0 人天 | archived `fix-admin-banner-image-preview-cropped`（2026-07-22 09:31:04） |

BUG：`BUG-0070`、`BUG-0071`、`BUG-0072`、`BUG-0073`、`BUG-0074`、`BUG-0078`、`BUG-0077`、`BUG-0075`、`BUG-0079`、`BUG-0080` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 16 个范围项关联 Change；16 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 开发人数 | 2 |
| 测试人数 | 1 |
| Sprint 容量 | 30 人天 |
| 已纳入估算 | 32.0 人天 |
| 容量占用 | 106.67% |
| fix 缓冲 | -2.0 人天 |
| fix 缓冲比例 | -6.67% |

容量门禁：Risk。当前纳入一个 M 级 add 型 Change、五个 update 型 Change、十个 fix 型 Change，容量占用 106.67%，低于 120% 硬阻断阈值，可继续规划。风险：已超过 30 人天容量，fix 缓冲为 -2.0 人天 / -6.67%，低于建议 30%；本 Sprint 后续不得净新增范围，新增生产问题必须通过替换低优先级项或拆分 Sprint 处理。

## 4. 里程碑

| 里程碑 | 目标日期 | 说明 |
|---|---|---|
| Sprint 规划完成 | 2026-07-20 22:30:24 | 纳入 `REQ-0063` 与 `update-password-validation-policy` |
| 实现与自测 | 2026-08-22 18:00:00 | 完成后端密码策略、API、管理端提示、小程序分享矩阵、Web 登录页布局和测试 |
| Web 管理端移动端适配 smoke | 2026-08-25 18:00:00 | 完成 `/admin/login`、Dashboard、SKU、品牌、用户、日志、系统设置等页面在 375/390/768/1440 视口下的基础可用性 smoke |
| 分享 evidence 收口 | 2026-08-26 18:00:00 | 完成小程序首页、商品详情页、商品列表页、品牌详情页分享直达和 320/375/430 evidence |
| 生产 DB / Banner smoke 收口 | 2026-08-27 18:00:00 | 完成 BUG-0075 MySQL drift/迁移证据、品牌详情 Banner 保存与展示读取 smoke |
| 管理端 Dashboard 真实数据验收 | 2026-08-27 18:00:00 | 完成 BUG-0079 Dashboard 概览真实数据、空态、错误态、权限和 API/Orval 判定证据 |
| 验收收口 | 2026-08-28 18:00:00 | 完成 acceptance、Workflow Sync 和归档前检查 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 旧密码提示散落在前端组件或测试中 | 用户看到 8 位、大小写、特殊字符等旧文案 | 实现阶段搜索旧提示并补前端测试 |
| 后端入口规则漂移 | 修改密码、创建用户、重置密码规则不一致 | 优先修改统一校验/生成函数，并补多入口测试 |
| 安全策略被误删 | 弱密码表、限流、token_version 或受保护账号逻辑回退 | tasks 明确保留既有安全边界，测试覆盖不回退 |
| API 错误结构变化影响前端 | 前端无法展示具体失败项 | 如 schema 变化，同步 OpenAPI、Orval 与 API 文档 |
| SKU 名称/编码语义跨端漂移 | 管理端、API、小程序搜索/详情/分享可能继续混用 SKU 编码和商品名称，或把系统编码暴露给店主端 | 实现阶段固定 `sku_code` 为系统自动生成唯一识别字段，商品名称作为用户填写和公开展示字段；补后端自动编码、管理端文案、小程序隐藏编码、搜索兼容与分享标题回归测试 |
| 小程序底部操作栏布局回归 | 删除品牌按钮后出现空白、错位或残留点击热区 | 补小程序静态测试，验收截图覆盖内容区入口和底部操作区 |
| 小程序 SKU 详情品牌入口误跳回归 | 修复品牌卡片路径时可能影响品牌列表页、搜索 fallback 或品牌详情页参数 | 后端测试断言 SKU 详情 `brand_entry_path` 指向品牌详情页，并回归品牌列表页入口和搜索 fallback 边界 |
| 小程序分类页长名称布局回归 | 修复二级分类长名称省略时可能影响三列宫格、点击热区或窄屏布局 | 覆盖 4 字以内、5-8 字、超过 8 字分类名称，并回归二级分类点击商品列表入口 |
| 小程序 usage-events 契约继续漂移 | 新增页面或组件事件名未登记，或必要字段未补齐，继续产生 400 噪音 | 建立小程序事件字典与后端事件定义对照测试，覆盖收藏页、品牌详情页、商品/品牌卡片关键事件 |
| 媒体上传限制继续不一致 | 图片、视频、文档上限来源不同，或前端提示、后端校验、Nginx/代理配置不一致 | 统一 effective 上传限制，补 23M 边界测试、超限错误测试和 Docker/Web 入口验证；保留 MinIO/S3 适配层 |
| Web 登录页工具区布局回归 | 主题选择与语言选择对齐修复可能遮挡标题、表单或安全提示 | 补 Web 登录页桌面/窄屏布局证据，并回归主题切换、语言按钮可访问性和登录流程 |
| 管理端移动端适配范围横跨页面多 | 同时触及 AdminLayout、列表页、表单页、弹窗、抽屉和上传控件，可能引发桌面回归或页面级横向滚动 | 先执行 `/req-opsx REQ-0027-mobile-page-adaptation` 固化 design/tasks，再按页面矩阵做 375/390/768/1440 smoke；优先复用 DS token、AdminLayout、列表/表单/弹窗既有模式 |
| 生产主题偏好同步失败提示常驻 | 修复 Toast 生命周期可能影响其他管理端提示，单纯前端修复也可能掩盖生产 API/DB 漂移 | 补主题同步失败自动消失/可关闭测试，收集 `PATCH /api/v1/auth/me/theme` Network/日志证据，明确是否需要 OpenAPI/Orval 或 DB 迁移 |
| 生产小程序视频播放 502 链路未完全恢复 | 只修复单个页面或播放器可能掩盖生产域名、API、`/media/` upstream 仍不可用 | 先做生产入口、`/api/v1/health`、实际 SKU 接口和实际 `/media/{object_key}` smoke，再做微信真机播放 evidence |
| 生产品牌类型 Banner 保存失败 | MySQL 既有 `banners` 表可能缺少 `brand_id`，或品牌 Logo/状态数据触发业务校验，若只修本地新库会漏掉生产路径 | 优先补生产/类生产 MySQL schema drift 或迁移证据，覆盖 `POST/PUT /api/v1/admin/banners` 品牌详情保存、`brand_logo`/`custom_upload` 和错误 envelope |
| 管理端首页概览真实数据接入 | 现有规格与实现曾允许 Mock 数据，若只替换前端常量可能导致统计口径、权限、空态和错误态不完整 | 优先确认是否复用或新增 Dashboard 概览 API，固定 SKU/品牌/Banner/用户统计口径；补真实数据、空数据、接口失败、未授权和前端渲染测试，若 API 变化同步 OpenAPI/Orval/docs |
| 管理端 Banner 图片完整预览 | 列表缩略图和弹窗预览可能复用裁切型容器，修复时若只改单处可能导致另一处仍裁切，或引发表格行高/弹窗滚动回归 | BUG-0080 实现阶段同时覆盖列表与弹窗、自定义上传图/品牌 Logo/SKU 主图、多比例图片和 DS token 背景/边框；确认不改变 Banner API、数据库、对象存储或展示端投放策略 |
| SKU 图片移除与主图状态回归 | 图片数组重排、主图唯一性、移除当前主图兜底和保存 payload 顺序可能与后端 normalize 不一致 | REQ-0066 实现阶段补 TileSkuFormModal 组件测试和必要后端回归；移除只改变 SKU 图片关联，不物理删除 MinIO 对象 |
| 微信朋友圈分享参数受限 | 朋友圈入口可能无法承载复杂查询或图片兜底差异 | 分享路径只保留必要业务参数，复杂上下文降级到可打开的列表/详情页 |
| 小程序运行入口漂移 | `.ts` 源文件与实际运行 `.js` 入口未同步导致验收误判 | 实现阶段同时检查源文件与运行入口，静态测试不得替代 DevTools/真机 evidence |

## 6. 知识库承接

| 来源 | 承接项 | 本 Sprint 处理 |
|---|---|---|
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 容量超过 100% 时冻结范围更早执行 | sprint-010 当前纳入 19.0 人天，避免复现 sprint-008 / sprint-009 容量边界问题 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 复盘继续只消费 Fact Sheet / 摘要 | 本 Sprint 范围小，仍要求 apply/archive 输出保持 compact summary |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序页面链路和设备 evidence 容易在后期补录 | BUG-0070 实现阶段提前补小程序静态测试和必要截图，不等 archive readiness 再补 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序页面链路和设备 evidence 容易在后期补录 | BUG-0078 实现阶段同步补 API 响应证据与小程序品牌详情页跳转 evidence |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序页面链路和设备 evidence 容易在后期补录 | BUG-0077 实现阶段提前补分类页长名称 DevTools/真机或静态替代 evidence |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序页面链路、埋点与设备 evidence 容易在后期补录 | BUG-0072 实现阶段同步补 usage-events 请求/响应证据、事件字典防漂移测试和必要小程序 Network evidence |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 验收语义容易滞后于事实状态 | BUG-0071 实现阶段同步更新 acceptance-report 与 trace，避免工具区对齐已修复但验收正文仍显示待实现 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 验收语义容易滞后于事实状态 | BUG-0074 实现阶段同步更新 acceptance-report、生产 API smoke 与 trace，避免 Toast 已修复但账号偏好同步证据缺失 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 管理端与媒体治理需继续复用 media-upload/admin-list/admin-modal 横切验收 | BUG-0073 实现阶段沿用媒体上传五层验收，提前补 Docker/Web 入口、对象存储和前端状态证据 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序页面链路、媒体 URL 与设备 evidence 容易在后期补录 | BUG-0076 实现阶段提前补生产入口 curl、实际 `/media/` 响应头和微信真机播放 evidence |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 管理端与生产数据库类证据需前置，不等 archive readiness 补录 | BUG-0075 实现阶段提前补 MySQL drift/迁移、备份/回滚边界、Banner 保存 API 与小程序展示读取证据 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 验收语义和真实数据证据不能后补 | BUG-0079 实现阶段同步补 Dashboard 真实数据、空态、错误态、权限和 API/Orval 判定证据，避免首页已接入但验收仍停留在 Mock/待实现表述 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | Sprint 范围过大和验收证据后补会压缩质量余量 | BUG-0080 纳入后容量为 103.33%，实现阶段必须前置列表/弹窗截图或组件测试证据，不得再净新增范围 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 小程序运行入口 `.js` / `.ts` 与设备 evidence 容易漂移 | REQ-0064 实现阶段必须同步运行入口、分享路径和 DevTools 320/375/430 evidence |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | Sprint 范围过大和验收证据后补会压缩质量余量 | REQ-0027 实现阶段需前置移动端 smoke 矩阵与截图 evidence，不等 archive readiness 再补 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 管理端列表、弹窗和小程序 evidence 需随跨端语义变更前置 | REQ-0065 实现阶段同步补管理端 SKU 表单/列表证据、小程序卡片/详情/搜索/分享隐藏编码 evidence 和 API/Orval 判定 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 管理端弹窗与验收证据需随字段语义变更前置 | REQ-0067 实现阶段同步补类目弹窗字段截图或组件证据、后端编码生成与同层级重名测试、OpenAPI/Orval 判定，避免弹窗已改但 API 契约或错误码滞后 |
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 管理端弹窗、媒体引用和状态机证据需前置 | REQ-0066 实现阶段同步补 SKU 编辑弹窗图片移除、设主图前置、移除主图兜底和 API/DB/Orval 判定证据 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 前端、后端 API、媒体读取、Nginx、环境文档五层必须同时验收 | BUG-0073 验收覆盖 23M 图片/视频/文档边界、超限错误非 413、`/media/{object_key}` 读取和 `.env.example` / 文档同步 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 管理端媒体引用必须通过后端授权上传与 `/media/{object_key}` 受控读取 | BUG-0075 覆盖品牌 Logo 引用与 Banner 自定义上传 object key，不允许前端直连对象存储写入 |
| `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 分享直达、原生胶囊避让、返回兜底和内容 offset 必须成组验收 | REQ-0064 分享直达验收覆盖四个页面，不新增自绘分享 UI，不遮挡原生胶囊 |
| `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 字段级错误和 fixed toast 避免 layout shift | 密码字段错误必须在字段附近展示，成功反馈使用 fixed toast |
| `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 表单保存反馈和字段错误不得造成 layout shift，失败需可理解 | BUG-0075 若调整管理端 Banner 表单错误展示，必须保持单一保存 CTA、fixed toast 与字段级错误稳定 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端弹窗宽度与 CSS cascade 防回归 | 修改密码弹窗保持 520px computed width，避免 `modal-card` 与专属类并存 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 列表页分页、指标卡、fixed toast、DS confirm modal 需要统一 | REQ-0027 覆盖品牌、Banner、类目、规格、SKU、用户、日志、API 文档等列表页移动端降级与无页面级横向溢出 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 列表页缩略图修复不得破坏表格行高、分页、筛选与操作列一致性 | BUG-0080 覆盖 Banner 列表图片完整预览，固定容器尺寸并保持列表扫描效率 |
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 列表页主识别字段、分页、筛选和 fixed toast 需一致 | REQ-0065 管理端 SKU 列表以商品名称为主展示，SKU 编码如保留仅作内部弱化信息，分页、筛选、批量/确认反馈不回归 |
| `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 表单页单一保存 CTA、fixed toast 与 DS modal 防 layout shift | REQ-0027 覆盖个人资料、系统设置与修改密码等移动端单列可用性 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 宽弹窗与窄弹窗需验收 computed width 与矮视口滚动 | REQ-0027 覆盖 SKU、Banner、用户、品牌、系统设置确认等弹窗移动端可关闭、可滚动、footer 可达 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | Banner 弹窗图片预览修复不得引入 modal-card 层叠、computed width 或矮视口滚动回归 | BUG-0080 覆盖 Banner 新建/编辑弹窗预览完整显示、footer 可达与上传控件不遮挡 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端 SKU 弹窗不得因字段调整引入 CSS cascade 回归 | REQ-0065 SKU 新增/编辑弹窗不要求手填 SKU 编码，商品名称字段可填写且错误提示稳定；弹窗类名、computed width 和矮视口滚动不回归 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | SKU 图片编辑区不得引入弹窗层叠和矮视口滚动回归 | REQ-0066 SKU 编辑弹窗继续使用专属 `sku-modal-card` 策略，图片移除按钮、主图标记和底部操作在 1440px 与矮视口下可达 |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端类目弹窗不得因移除编码字段和新增必填标识引入 CSS cascade 回归 | REQ-0067 CategoryFormModal 不同时挂载 `modal-card` 与专属类，1440px computed width、矮视口滚动、字段级错误和 footer 可达性需验收；类目列表名称列需回归第一行名称、第二行仅编码、不展示层级路径 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 上传控件状态机和即时回显不得因移动端适配被隐藏 | REQ-0027 覆盖品牌 Logo、Banner 图片、SKU 图片/视频、用户头像移动端上传控件回归；默认不修改上传 API 或对象存储策略 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 媒体上传即时回显和 `/media/{object_key}` 读取需与预览一致 | BUG-0080 验收自定义上传图、品牌 Logo、SKU 主图等图片来源的预览一致性，但默认不改上传 API、对象存储或 Nginx |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 媒体引用变更不得误删对象或破坏上传状态机 | REQ-0066 图片移除仅删除 SKU 图片关联；主图切换与图片移除后即时回显一致，默认不触发 Docker 边界上传验收 |

## 7. 横切预防清单

| 标签 | 适用性 | 验收 gate |
|---|---|---|
| admin-list | applicable | REQ-0027 与 REQ-0065 覆盖管理端 SKU 等列表页；分页、筛选、fixed toast、DS confirm modal 和主展示字段不回归 |
| admin-form | applicable | 字段级密码错误显示在字段附近；保存/成功反馈不得造成布局位移；如触及表单页，保存 CTA 保持单一 |
| admin-modal | applicable | 修改密码弹窗保持 520px computed width；TSX 不得同时挂载 `modal-card` 与专属类；REQ-0066 SKU 编辑弹窗图片移除和主图操作保持 computed width、矮视口滚动、footer 可达性不回归 |
| admin-category-modal | applicable | REQ-0067 覆盖类目新增 / 编辑弹窗：无可填写编码输入，上级类目、类目名称、排序权重必填标识一致；类目名称字段级校验、同层级重名错误映射、computed width 和矮视口滚动不回归；类目列表名称列第一行名称、第二行仅编码、不展示层级路径 |
| media-upload | applicable | BUG-0073 覆盖前端上传状态、后端 MIME/大小校验、MinIO/S3 写入、`/media/{object_key}` 读取、Nginx/代理大小限制、`.env.example` 与文档同步；REQ-0066 覆盖 SKU 图片移除、主图切换即时回显和不物理删除对象；超限应返回业务 400，不能依赖 413 |
| admin-banner-preview | applicable | BUG-0080 覆盖 Banner 列表缩略图和弹窗预览完整显示；横幅图、方图、竖图、超宽图不裁切关键信息；不改变 API/DB/对象存储/展示端投放策略 |
| miniapp-detail | applicable | SKU 详情页底部操作栏删除品牌按钮后无空白、错位或残留点击热区；内容区品牌入口仍可跳转；SKU 详情品牌卡片不得误跳搜索页 |
| miniapp-category | applicable | 分类页二级分类长名称可辨识；4 字以内、5-8 字、超过 8 字名称均需回归；点击长名称二级分类进入正确商品列表 |
| miniapp-usage-events | applicable | 小程序收藏页、品牌详情页、商品/品牌卡片和关键页面访问事件与后端事件定义一致；合法上报不再返回 400；非法事件错误可诊断 |
| miniapp-share | applicable | 首页、商品详情页、商品列表页、品牌详情页均覆盖微信朋友/朋友圈分享；分享路径保留必要参数；分享直达不空白，返回兜底可用 |
| miniapp-navigation | applicable | 不自绘微信系统胶囊；分享直达后的自定义导航栏 offset、返回按钮和首页兜底符合既有 best-practice |
| login-ui | applicable | 登录页主题选择与语言选择共享工具区布局或等价对齐规则；桌面/窄屏无重叠、裁切、遮挡表单 |
| theme-preference | applicable | 主题偏好同步失败提示自动消失或可关闭；本机主题保持生效；`PATCH /api/v1/auth/me/theme` 生产链路可诊断 |
| prod-media-smoke | applicable | BUG-0076 覆盖生产根路径、`/api/v1/health`、实际 SKU 接口、实际 `/media/{object_key}` 视频 URL、微信真机播放；若仅生产配置恢复，验收记录明确不需要 Orval |
| admin-banner | applicable | 品牌详情 Banner 新增/编辑保存成功；`brand_id`、图片来源、展示位置和有效期回显一致；失败场景错误 envelope 可理解且不泄密 |
| mysql-drift | applicable | 生产/类生产 MySQL `banners.brand_id` 缺失可被幂等迁移或 drift check 阻断；SQLite 默认 pytest 不依赖本机 MySQL |
| web-admin-mobile | applicable | REQ-0027 覆盖 `375x812`、`390x844`、`768x1024`、`1440x1024`；页面级无不可控横向溢出，筛选/分页不重叠，弹窗/抽屉可关闭，登录页和无权限页不回归 |
| sku-name-code | applicable | SKU 编码作为系统自动生成唯一内部识别字段；商品名称作为用户填写和公开展示字段；小程序/店主端商品卡片、详情、搜索结果、推荐/收藏和分享标题不得展示 SKU 编码 |
| admin-dashboard-data | applicable | Dashboard 数据概览必须使用真实后端数据源；loading、empty、error、权限边界和 API/Orval 判定必须作为验收 gate |
| open-change-gate | applicable | REQ-0065 已关联 `refine-sku-metadata-name-code-display`；REQ-0067 已关联 `refine-admin-category-edit-modal-validation`；REQ-0066 已关联 `add-admin-sku-image-removal-main-image-rules`；REQ-0027 已关联 `update-web-admin-mobile-adaptation` 并由 Workflow Sync 回填 Change，且已通过 `/opsx-apply` |

## 8. 依赖 ASCII 树

```text
sprint-010
├── REQ-0063 密码校验规则简化
    ├── parent: REQ-0015 管理端修改密码
    ├── change: update-password-validation-policy
    ├── specs: auth / admin-password-change / user-management
    ├── backend: 统一密码校验与随机密码生成
    ├── web-admin: 修改密码弹窗与用户管理密码提示
    └── next: /opsx-apply update-password-validation-policy
└── REQ-0064 小程序多页面微信分享
    ├── parents: REQ-0041 / REQ-0044 / REQ-0047 / REQ-0058
    ├── change: add-miniapp-wechat-share-pages
    ├── specs: miniapp-home / miniapp-sku-detail-page / miniapp-product-list-page / miniapp-brand-detail-home-page / miniapp-global-custom-navigation-bar / miniapp-device-evidence-template
    ├── miniapp: 首页、商品详情页、商品列表页、品牌详情页微信朋友与朋友圈分享
    └── next: /opsx-apply add-miniapp-wechat-share-pages
└── REQ-0027 Web 管理端移动端基础适配
    ├── parent: REQ-0004 管理端首页
    ├── change: update-web-admin-mobile-adaptation
    ├── specs: web-client / admin-dashboard
    ├── web-admin: AdminLayout、Dashboard、列表页、表单页、弹窗、抽屉、登录页、无权限页移动端基础可用
    └── next: /opsx-archive update-web-admin-mobile-adaptation
└── REQ-0065 SKU 元数据名称与编码展示去重
    ├── change: refine-sku-metadata-name-code-display
    ├── specs: tile-sku-management / miniapp-sku-detail-page / miniapp-product-list-page / miniapp-search
    ├── backend: 自动生成唯一 SKU 编码并保留系统识别稳定性
    ├── web-admin: 商品名称作为用户填写字段，SKU 编码不要求手填或仅作内部弱化信息
    ├── miniapp: 商品卡片、详情、推荐、收藏、搜索结果与分享标题仅展示商品名称
    └── next: /opsx-apply refine-sku-metadata-name-code-display
└── REQ-0067 管理端类目编辑弹窗字段与校验规则
    ├── parent: REQ-0005 管理端瓷砖类目管理
    ├── change: refine-admin-category-edit-modal-validation
    ├── specs: tile-category-management / web-client
    ├── backend: 类目编码创建时生成 CAT- 前缀唯一值，类目名称格式与同层级唯一兜底校验
    ├── web-admin: CategoryFormModal 隐藏编码输入，上级类目、类目名称、排序权重必填，字段级错误稳定展示；列表名称列第二行仅展示类目编码
    ├── api: POST /api/v1/admin/tile-categories 不再要求 code；实现阶段同步 OpenAPI / Orval
    └── next: /opsx-archive refine-admin-category-edit-modal-validation
└── REQ-0066 管理端 SKU 编辑弹窗图片移除与主图规则
    ├── parent: REQ-0006 管理端瓷砖 SKU 管理
    ├── change: add-admin-sku-image-removal-main-image-rules
    ├── specs: tile-sku-management
    ├── web-admin: TileSkuFormModal 支持图片移除、设主图前置、移除当前主图后后一张或剩余第一张兜底
    ├── storage: 仅变更 SKU 图片关联，不物理删除 MinIO 对象
    └── next: /opsx-apply add-admin-sku-image-removal-main-image-rules
└── BUG-0070 小程序 SKU 详情页重复品牌按钮
    ├── parent: REQ-0044 小程序 SKU 详情页
    ├── change: fix-miniapp-sku-detail-duplicate-brand-button
    ├── specs: miniapp-sku-detail-page
    ├── miniapp: 删除底部品牌按钮，保留内容区品牌入口
    └── status: archived（2026-07-22）
└── BUG-0071 Web 登录页工具区未对齐
    ├── change: fix-login-page-tool-selector-alignment
    ├── specs: web-client
    ├── web-admin: 统一主题选择与语言选择工具区布局
    └── status: archived（2026-07-22）
└── BUG-0072 微信小程序 usage-events 400
    ├── parent: REQ-0024 产品使用行为埋点与接口请求日志详情
    ├── change: fix-miniapp-usage-events-contract-drift
    ├── specs: product-usage-logging
    ├── api: 收敛 POST /api/v1/usage-events 事件字典与请求字段契约
    ├── miniapp: 修复收藏页、品牌详情页、商品/品牌卡片等上报事件
    └── next: /opsx-apply fix-miniapp-usage-events-contract-drift
└── BUG-0073 上传 23M 文件失败
    ├── change: fix-upload-size-limit-consistency
    ├── specs: object-storage / system-settings / brand-certificate-management
    ├── backend: 统一图片、视频、文档 effective 上传大小限制与错误响应
    ├── web-admin: 上传入口提示、系统设置 media Tab 和失败状态
    ├── storage: 保留单 Bucket、标准前缀和受控读取
    └── next: /opsx-apply fix-upload-size-limit-consistency
└── BUG-0074 生产主题偏好同步失败提示常驻
    ├── change: fix-theme-preference-sync-toast-persistent
    ├── specs: web-client / auth
    ├── web-admin: 主题同步失败 Toast 自动消失或可关闭，本机主题保持生效
    ├── api: 回归 PATCH /api/v1/auth/me/theme 生产链路、统一响应 envelope 和账号偏好持久化
    └── next: /opsx-apply fix-theme-preference-sync-toast-persistent
└── BUG-0078 生产小程序 SKU 详情页品牌卡片误跳搜索页
    ├── parent: REQ-0044 小程序 SKU 详情页
    ├── change: fix-miniapp-sku-detail-brand-card-route
    ├── specs: miniapp-sku-detail-page
    ├── api: 修正 SKU 详情 brand_entry_path 指向品牌详情页
    └── next: /opsx-apply fix-miniapp-sku-detail-brand-card-route
└── BUG-0077 小程序分类页二级分类长名称省略
    ├── parent: REQ-0045 分类列表页
    ├── change: fix-miniapp-category-secondary-name-truncated
    ├── specs: miniapp-category-list-page
    ├── miniapp: 优化二级分类长名称展示，保持三列宫格与分类跳转
    └── next: /opsx-apply fix-miniapp-category-secondary-name-truncated
└── BUG-0075 生产管理端品牌类型 Banner 无法保存
    ├── parent: REQ-0062 管理后台 Banner 投放范围配置优化
    ├── change: fix-prod-admin-brand-banner-save
    ├── specs: banner-management / database / testing
    ├── database: 补齐 MySQL banners.brand_id 既有表迁移或 drift check
    ├── api: 回归 POST/PUT /api/v1/admin/banners 品牌详情保存与错误 envelope
    ├── web-admin: 品牌详情 Banner 保存、回显和失败提示
    ├── miniapp: 已上线品牌详情 Banner 按 position 分流读取
    └── next: /opsx-apply fix-prod-admin-brand-banner-save
└── BUG-0079 管理端首页数据概览仍使用 Mock 数据
    ├── change: fix-admin-dashboard-overview-real-data
    ├── specs: admin-dashboard
    ├── web-admin: Dashboard 数据概览移除生产 Mock 成功态，接入真实数据源
    ├── api: 复用或新增受鉴权保护的 Dashboard 概览接口；若 API 变化同步 OpenAPI/Orval/docs/tests
    └── next: /opsx-apply fix-admin-dashboard-overview-real-data
└── BUG-0080 管理端 Banner 图片预览显示不全
    ├── parent: REQ-0016 Banner 管理
    ├── change: fix-admin-banner-image-preview-cropped
    ├── specs: banner-management
    ├── web-admin: Banner 列表缩略图与新建/编辑弹窗图片预览完整显示
    ├── tests: 前端组件测试或截图/人工验收覆盖多比例图片与多图片来源
    └── status: archived（2026-07-22）
```

## 9. 发布计划

- 本 Sprint 可作为认证/用户管理规则调整随产品小版本发布。
- REQ-0064 可随小程序体验能力进入同一发布批次；发布前需确认四页面分享矩阵、分享直达参数和 DevTools/真机 evidence。
- REQ-0027 可随 Web 管理端体验优化进入同一发布批次；发布前需确认 `375x812`、`390x844`、`768x1024`、`1440x1024` 视口下 AdminLayout、登录、Dashboard、SKU、品牌、用户、日志、系统设置等页面 smoke evidence，并明确不需要 OpenAPI / Orval / DB / Docker 的结论。
- REQ-0065 可随 SKU 元数据体验优化进入同一发布批次；发布前需确认管理端商品名称/自动编码、小程序/店主端隐藏 SKU 编码、搜索兼容和分享标题 evidence，并明确 OpenAPI / Orval / DB 是否需要同步。
- BUG-0070 可随小程序体验修复进入同一发布批次；发布前需确认内容区品牌入口与底部操作栏截图 evidence。
- BUG-0072 可随小程序体验修复进入同一发布批次；发布前需确认收藏页、品牌详情页、商品/品牌卡片等 usage-events 合法上报不再 400。
- BUG-0073 可随管理端媒体上传修复进入同一发布批次；发布前需确认约 23M 图片、视频、文档按产品规则成功或被清晰拒绝，且 Docker/Web 入口不返回 Nginx 413。
- BUG-0074 可随 Web 管理端主题体验修复进入同一发布批次；发布前需确认主题同步失败提示自动消失或可关闭，且账号偏好 API 生产链路可保存并在刷新/重新登录后保持。
- BUG-0078 可随小程序体验修复进入同一发布批次；发布前需确认 SKU 详情品牌卡片进入品牌详情页，不再进入搜索页。
- BUG-0077 可随小程序体验修复进入同一发布批次；发布前需确认分类页二级分类长名称可辨识，且二级分类点击商品列表入口不回退。
- BUG-0075 可随生产管理端 Banner 保存修复进入同一发布批次；发布前需确认 MySQL `banners.brand_id` 迁移/drift 证据、品牌详情 Banner 新增/编辑保存、错误 envelope 与小程序展示读取。
- BUG-0079 可随 Web 管理端 Dashboard 真实数据修复进入同一发布批次；发布前需确认首页 SKU/品牌/Banner/用户概览指标来自真实数据源，loading/empty/error/权限边界可用，并明确是否同步 OpenAPI、Orval 和 API 文档。
- BUG-0080 可随 Web 管理端 Banner 体验修复进入同一发布批次；发布前需确认列表缩略图、弹窗预览、多比例图片、多图片来源和 DS token 视觉证据，并明确无需 API / DB / Orval / Docker 变更。
- BUG-0071 可随 Web 管理端登录页体验修复进入同一发布批次；发布前需确认桌面/窄屏登录页工具区截图 evidence。
- 发布前必须确认是否同步 OpenAPI、Orval、API 文档和错误码文档。
- BUG-0073 可能涉及系统设置字段、`.env.example`、OpenAPI/Orval 判定、MinIO/S3 上传链路和 Docker/Nginx/生产代理配置说明；实现阶段必须明确是否实际改 API schema 或 DB seed。
- BUG-0075 可能涉及 MySQL migration/schema drift 检查、数据库文档、后端 Banner 测试、错误码文档和 OpenAPI/Orval 判定；若仅补迁移与既有响应契约，需说明不需要 Orval。
- BUG-0079 可能涉及新增或复用 Dashboard 概览 API、OpenAPI/Orval、API 文档、后端统计查询和前端 Dashboard 测试；若仅复用既有列表 total 接口且 schema 不变，需说明不需要 Orval。
- BUG-0080 预计仅涉及 Web 管理端 Banner 预览 UI；若实现阶段发现 API、数据库、对象存储或展示端投放策略也需修改，必须先更新 OpenSpec 设计与任务并同步对应文档/测试。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0063-password-validation-policy-simplification/` |
| REQ | `issues/requirements/archive/REQ-0064-miniapp-wechat-share-pages/` |
| REQ | `issues/requirements/archive/REQ-0027-mobile-page-adaptation/` |
| REQ | `issues/requirements/archive/REQ-0065-sku-metadata-name-sku-dedup/` |
| BUG | `issues/bugs/archive/BUG-0070-miniapp-sku-detail-duplicate-brand-button/` |
| BUG | `issues/bugs/archive/BUG-0071-login-page-theme-language-selector-misalignment/` |
| BUG | `issues/bugs/archive/BUG-0072-miniapp-usage-events-bad-request/` |
| BUG | `issues/bugs/archive/BUG-0073-video-upload-23m-file-fails/` |
| BUG | `issues/bugs/archive/BUG-0074-prod-theme-preference-sync-toast-persistent/` |
| BUG | `issues/bugs/archive/BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search/` |
| BUG | `issues/bugs/archive/BUG-0077-miniapp-category-secondary-name-truncated/` |
| BUG | `issues/bugs/archive/BUG-0075-prod-admin-brand-banner-save-fails/` |
| BUG | `issues/bugs/archive/BUG-0079-admin-dashboard-overview-mock-data/` |
| BUG | `issues/bugs/archive/BUG-0080-admin-banner-image-preview-cropped/` |
| Change | `openspec/changes/archive/2026-07-22-update-password-validation-policy/` |
| Change | `openspec/changes/archive/2026-07-22-add-miniapp-wechat-share-pages/` |
| Change | `openspec/changes/archive/2026-07-22-fix-miniapp-sku-detail-duplicate-brand-button/` |
| Change | `openspec/changes/archive/2026-07-22-fix-login-page-tool-selector-alignment/` |
| Change | `openspec/changes/archive/2026-07-22-fix-miniapp-usage-events-contract-drift/` |
| Change | `openspec/changes/archive/2026-07-22-fix-upload-size-limit-consistency/` |
| Change | `openspec/changes/archive/2026-07-22-fix-theme-preference-sync-toast-persistent/` |
| Change | `openspec/changes/archive/2026-07-22-fix-miniapp-sku-detail-brand-card-route/` |
| Change | `openspec/changes/archive/2026-07-22-fix-miniapp-category-secondary-name-truncated/` |
| Change | `openspec/changes/archive/2026-07-22-fix-prod-admin-brand-banner-save/` |
| Change | `openspec/changes/archive/2026-07-22-refine-sku-metadata-name-code-display/` |
| Change | `openspec/changes/archive/2026-07-22-fix-admin-dashboard-overview-real-data/` |
| Change | `openspec/changes/archive/2026-07-22-fix-admin-banner-image-preview-cropped/` |
| Knowledge | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |
| Knowledge | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| Knowledge | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| Knowledge | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |
| Knowledge | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` |

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 11:32:00 | `/sprint-exps` | 生成复盘文档 `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` |
| 2026-07-22 11:17:51 | `/sprint-archive` | 关闭 sprint-010：16/16 Change archived，298/298 tasks 完成，Sprint 进入 completed/archive |
| 2026-07-22 10:40:27 | `/sprint-propose` | 将 BUG-0076 与 fix-prod-miniapp-video-upstream-502 移出 sprint-010，待生产条件具备后重新规划 |
| 2026-07-22 09:28:10 | `/sprint-propose` | 将 BUG-0080 与 fix-admin-banner-image-preview-cropped 纳入 sprint-010 |
| 2026-07-22 09:01:58 | `/sprint-propose` | 将 BUG-0079 与 fix-admin-dashboard-overview-real-data 纳入 sprint-010 |
| 2026-07-21 18:20:23 | `/sprint-propose` | 将 REQ-0065 与 refine-sku-metadata-name-code-display 纳入 sprint-010 |
| 2026-07-21 16:32:10 | `/sprint-propose` | 将 REQ-0027 纳入 sprint-010；待 `/req-opsx` 创建 `update-web-admin-mobile-adaptation` |
| 2026-07-21 15:38:16 | `/sprint-propose` | 将 BUG-0075 与 fix-prod-admin-brand-banner-save 纳入 sprint-010 |
| 2026-07-21 15:37:29 | `/sprint-propose` | 将 BUG-0076 与 fix-prod-miniapp-video-upstream-502 纳入 sprint-010 |
| 2026-07-21 15:32:13 | `/sprint-propose` | 将 BUG-0074 与 fix-theme-preference-sync-toast-persistent 纳入 sprint-010 |
| 2026-07-21 15:28:09 | `/sprint-propose` | 将 BUG-0077 与 fix-miniapp-category-secondary-name-truncated 纳入 sprint-010 |
| 2026-07-21 15:26:34 | `/sprint-propose` | 将 BUG-0072 与 fix-miniapp-usage-events-contract-drift 纳入 sprint-010 |
| 2026-07-21 15:28:53 | `/sprint-propose` | 将 BUG-0073 与 fix-upload-size-limit-consistency 纳入 sprint-010 |
| 2026-07-21 15:22:32 | `/sprint-propose` | 将 BUG-0078 与 fix-miniapp-sku-detail-brand-card-route 纳入 sprint-010 |
| 2026-07-21 14:59:21 | `/sprint-propose` | 将 REQ-0064 与 add-miniapp-wechat-share-pages 纳入 sprint-010 |
| 2026-07-21 14:57:57 | `/sprint-propose` | 将 BUG-0071 与 fix-login-page-tool-selector-alignment 纳入 sprint-010 |
| 2026-07-21 09:15:27 | `/sprint-propose` | 将 BUG-0070 与 fix-miniapp-sku-detail-duplicate-brand-button 纳入 sprint-010 |
| 2026-07-20 22:30:24 | `/sprint-propose` | 创建 sprint-010，纳入 REQ-0063 与 update-password-validation-policy |
