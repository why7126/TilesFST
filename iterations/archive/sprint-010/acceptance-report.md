---
note: workflow-sync — 16/16 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-010
status: completed
lifecycle_stage: archive
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-22 11:19:34
---

# sprint-010 验收报告

## 0. 最终归档结论

2026-07-22 11:17:51 执行 `/sprint-archive sprint-010` 收尾：readiness 检查通过，16/16 个 Change 已归档，298/298 个任务完成；Issue promote gate 通过后关闭 Sprint。AI usage snapshot 当前为 `estimated_fallback` 且 stale，未使用真实 token session 输入，后续可按 Fact Sheet 建议用本地 session JSONL 刷新。

## 1. 验收范围

| 类型 | 编号 | Change | 当前状态 | 验收结论 |
|---|---|---|---|---|
| REQ | REQ-0063-password-validation-policy-simplification | update-password-validation-policy | done，已归档（`update-password-validation-policy` archived 2026-07-21 23:01:00） | 待实现 |
| REQ | REQ-0064-miniapp-wechat-share-pages | add-miniapp-wechat-share-pages | done，已归档（`add-miniapp-wechat-share-pages` archived 2026-07-21 22:57:26） | 静态验收通过；真机 follow_up |
| REQ | REQ-0027-mobile-page-adaptation | update-web-admin-mobile-adaptation | done，已归档（`update-web-admin-mobile-adaptation` archived 2026-07-22 09:24:02） | 前端测试通过；待归档 |
| REQ | REQ-0065-sku-metadata-name-sku-dedup | refine-sku-metadata-name-code-display | done，已归档（`refine-sku-metadata-name-code-display` archived 2026-07-22 09:56:14） | 待实现 |
| REQ | REQ-0067-admin-category-edit-modal-validation | refine-admin-category-edit-modal-validation | done，已归档（`refine-admin-category-edit-modal-validation` archived 2026-07-22 09:55:00） | 后端/API 与前端测试通过；待归档 |
| REQ | REQ-0066-admin-sku-image-removal-main-image-rules | add-admin-sku-image-removal-main-image-rules | done，已归档（`add-admin-sku-image-removal-main-image-rules` archived 2026-07-22 09:58:04） | 测试通过；已归档 |
| BUG | BUG-0070-miniapp-sku-detail-duplicate-brand-button | fix-miniapp-sku-detail-duplicate-brand-button | done，已归档（`fix-miniapp-sku-detail-duplicate-brand-button` archived 2026-07-21 22:54:39） | 待实现 |
| BUG | BUG-0071-login-page-theme-language-selector-misalignment | fix-login-page-tool-selector-alignment | done，已归档（`fix-login-page-tool-selector-alignment` archived 2026-07-21 23:00:30） | 待实现 |
| BUG | BUG-0072-miniapp-usage-events-bad-request | fix-miniapp-usage-events-contract-drift | done，已归档（`fix-miniapp-usage-events-contract-drift` archived 2026-07-21 15:26:34） | 待实现 |
| BUG | BUG-0073-video-upload-23m-file-fails | fix-upload-size-limit-consistency | done，已归档（`fix-upload-size-limit-consistency` archived 2026-07-21 23:00:59） | 待实现 |
| BUG | BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | fix-miniapp-sku-detail-brand-card-route | done，已归档（`fix-miniapp-sku-detail-brand-card-route` archived 2026-07-22 09:01:56） | 已通过 |
| BUG | BUG-0077-miniapp-category-secondary-name-truncated | fix-miniapp-category-secondary-name-truncated | done，已归档（`fix-miniapp-category-secondary-name-truncated` archived 2026-07-21 15:28:09） | 待实现 |
| BUG | BUG-0075-prod-admin-brand-banner-save-fails | fix-prod-admin-brand-banner-save | done，已归档（`fix-prod-admin-brand-banner-save` archived 2026-07-21 23:00:44） | 自动化验收通过；生产 smoke follow-up |
| BUG | BUG-0079-admin-dashboard-overview-mock-data | fix-admin-dashboard-overview-real-data | done，已归档（`fix-admin-dashboard-overview-real-data` archived 2026-07-22 09:19:39） | 后端/API 与前端测试通过 |

## 2. 功能验收要点

- [ ] 密码长度少于 5 位失败。
- [ ] 密码长度等于 5 位且包含英文和数字成功。
- [ ] 密码长度等于 32 位且包含英文和数字成功。
- [ ] 密码长度超过 32 位失败。
- [ ] 缺少英文字符失败。
- [ ] 缺少数字失败。
- [ ] 修改本人密码、创建用户、重置密码策略一致。
- [ ] 旧提示“至少 8 位”、大小写、特殊字符不再显示。
- [ ] 小程序首页支持分享给微信朋友，分享卡片标题/路径可打开首页。
- [ ] 小程序首页支持分享到微信朋友圈，朋友圈打开后不空白。
- [ ] 小程序商品详情页支持分享给微信朋友和朋友圈，分享路径保留 SKU 标识，图片缺失时可使用兜底图。
- [ ] 小程序商品列表页支持分享给微信朋友和朋友圈，分享路径保留关键词、分类、品牌或专区等必要筛选参数。
- [ ] 小程序品牌详情页支持分享给微信朋友和朋友圈，分享路径保留品牌标识。
- [ ] 分享直达后的返回按钮、首页兜底和内容 offset 可用；分享埋点失败不阻断用户分享。
- [ ] `/admin/login` 在 `375x812` 与 `390x844` 下隐藏左侧品牌区，登录表单居中，账号、密码、记住登录状态、登录按钮可见且可操作。
- [ ] `/admin/dashboard` 在移动视口下指标卡、快捷操作、最近更新表格不重叠，页面级无不可控横向溢出。
- [ ] `/admin/tile-skus` 在移动视口下筛选区、宽表格、分页、SKU 弹窗和媒体字段可访问。
- [ ] `/admin/brands` 在移动视口下筛选区、Logo 列、表格、分页、品牌弹窗和状态确认可访问。
- [ ] `/admin/users` 在移动视口下筛选区、用户表格、分页、用户弹窗和重置密码确认可访问。
- [ ] `/admin/logs` 在移动视口下多条件筛选、日志表格、分页和日志详情抽屉可关闭、可滚动。
- [ ] `/admin/settings/basic` 在移动视口下设置导航、表单字段、保存/重置操作和确认弹窗可访问。
- [ ] `/admin/forbidden` 在移动视口下文案和返回/跳转入口不溢出。
- [ ] `AdminLayout` 在 `≤1023px` 下保持单列 Shell，Sidebar 不遮挡主内容，导航项可完整访问或可滚动访问。
- [ ] `.main-content` 与 `.content-inner` 不产生页面级不可控横向滚动；宽表格横向滚动限制在表格容器内。
- [ ] 新增/编辑弹窗、确认弹窗、重置密码弹窗和系统设置确认弹窗在 `375px` 宽度下头部、关闭按钮、内容区和底部操作可访问。
- [ ] 管理端 SKU 新增/编辑表单以“商品名称”作为用户填写字段，SKU 编码不要求手工填写。
- [ ] 草稿或正式 SKU 创建时系统自动生成唯一稳定的 SKU 编码，编辑商品名称不得改变既有 SKU 编码。
- [ ] 管理端 SKU 列表、详情、搜索结果、确认文案和错误提示以商品名称为主；如展示 SKU 编码，必须明确标注为内部/系统识别信息且不替代商品名称。
- [ ] 小程序/店主端商品卡片、SKU 详情、推荐、收藏、搜索结果、列表筛选结果和分享标题仅展示商品名称，不展示 SKU 编码。
- [ ] 小程序/店主端搜索可兼容 SKU 编码命中既有数据，但公开结果不展示 SKU 编码。
- [ ] 管理端 SKU 编辑弹窗中每张商品图片均提供明确移除入口。
- [ ] 移除非主图图片后，当前主图保持不变且仍位于图片列表第一位。
- [ ] 将任一非主图设为主图后，该图片自动移动到第一位，且列表中只有一张图片标记为主图。
- [ ] 移除当前主图后，如原主图后一张图片仍存在，则自动设为新主图并移动到第一位；否则选择剩余第一张图片为主图。
- [ ] 移除全部图片后，图片列表为空，保存草稿或允许缺图状态时不产生幽灵主图；正式发布缺图规则沿用既有 SKU 校验。
- [ ] 保存后 SKU 图片 payload 顺序、主图标记与再次打开编辑弹窗的回填一致。
- [ ] 移除图片只删除 SKU 图片关联，不物理删除 MinIO 对象或绕过 `/media/{object_key}` 受控读取。
- [ ] 管理端类目新增弹窗不展示「类目编码」输入项，也不要求用户填写编码。
- [ ] 管理端类目编辑弹窗不展示可编辑的「类目编码」输入项，不允许通过弹窗修改既有编码。
- [ ] 类目新增弹窗的上级类目、类目名称、排序权重均展示一致必填标识。
- [ ] 类目名称 trim 后非空，最多 10 个用户可见字符，且仅允许中文、英文、数字。
- [ ] 同一上级类目下类目名称唯一；编辑自身不误判重复，改名为同层级其他类目名称会被拒绝。
- [ ] `POST /api/v1/admin/tile-categories` 创建请求不再要求前端提交 `code`，后端返回的 `code` 以 `CAT-` 开头。
- [ ] 类目创建/更新错误响应继续遵守统一 envelope，名称重复、非法名称和非法排序权重错误可诊断。
- [ ] OpenAPI 导出和 Orval 生成物与类目创建请求契约保持一致，前端创建 payload 不包含用户填写的 `code`。
- [ ] 管理端类目列表名称列第一行只展示类目名称。
- [ ] 管理端类目列表名称列第二行只展示类目编码。
- [ ] 管理端类目列表名称列不展示层级路径，例如 `父级类目 / 二级类目`。
- [ ] SKU 商品详情页内容区保留“查看品牌主页”入口。
- [ ] 点击内容区“查看品牌主页”进入当前 SKU 关联品牌主页。
- [ ] SKU 商品详情页底部操作区不再显示品牌按钮。
- [ ] 删除底部品牌按钮后，底部操作区无空白占位、错位、异常间距或残留点击热区。
- [ ] 小程序收藏页、品牌详情页、SKU 详情页品牌入口、商品卡片和品牌卡片等合法 usage-events 上报返回成功，不再大量出现 400。
- [ ] 小程序 usage-events 上报字段与后端 `POST /api/v1/usage-events` Schema / 事件字典一致。
- [ ] 非法 usage-events 仍返回可诊断的 400 错误，不影响合法事件写入。
- [ ] usage-events 上报失败不阻断页面浏览、跳转、收藏或分享等用户操作。
- [ ] 明确图片、视频、文档三类上传业务允许大小上限，前端提示、后端校验、系统设置和部署代理配置保持一致。
- [ ] 约 23M 图片在允许配置下上传成功；若产品确认图片上限仍低于 23M，则返回明确限制提示。
- [ ] 约 23M 视频在允许 MIME Type 且走视频上传入口时上传成功，并可通过 `/media/{object_key}` 受控读取。
- [ ] 约 23M PDF / 文档在允许配置下上传成功；若不允许，则返回清晰错误提示。
- [ ] 超过各类型上限的文件返回统一结构错误响应，不出现无提示失败、上传卡住、500 或内部路径泄露。
- [ ] 不支持的 MIME Type 或扩展名被拒绝，且放宽大小限制不绕过类型校验。
- [ ] 上传成功对象使用标准对象前缀和安全对象 Key，继续通过后端 `/media/{object_key}` 受控读取，不前端直连对象存储写入。
- [ ] SKU 详情接口返回的 `data.brand.brand_entry_path` 指向 `/pages/brand-detail/index?brandId=<brand_id>`。
- [ ] 点击 SKU 商品详情页品牌卡片进入当前 SKU 关联品牌详情页，不再进入搜索页。
- [ ] 品牌详情页收到正确 `brandId` 并加载对应品牌信息。
- [ ] 微信小程序分类页中，4 字以内二级分类名称正常显示，布局不得回退。
- [ ] 微信小程序分类页中，5-8 字二级分类名称可完整识别或以业务可接受方式清晰展示。
- [ ] 微信小程序分类页中，超过 8 字二级分类名称不遮挡相邻分类、商品列表、导航栏或其他操作区。
- [ ] 点击长名称二级分类后进入对应分类商品列表，分类 ID、选中态和商品列表筛选结果正确。
- [ ] 生产根路径 `https://tilesfst.wjoyhappy.site/` 不返回 Nginx 502。
- [ ] 生产 `https://tilesfst.wjoyhappy.site/api/v1/health` 返回 200 与健康响应。
- [ ] 实际反馈 SKU 的 `/api/v1/miniapp/skus/<SKU ID>` 返回 200，视频项 `media[].url` 不为空。
- [ ] 实际视频 `/media/{object_key}` 返回 200，`Content-Type` 为小程序可播放视频类型，且不是 Nginx 502 HTML 页面。
- [ ] 微信真机打开实际反馈页面后视频可加载并播放，不再显示「视频暂时无法播放」。
- [ ] Web 管理端登录页同时展示主题选择模块与语言选择模块。
- [ ] 登录页主题选择模块与语言选择模块在桌面视口下保持统一工具区对齐，不重叠、不裁切、不异常换行。
- [ ] 登录页主题选择模块与语言选择模块在窄屏视口下保持可见且不遮挡标题、表单字段或安全提示。
- [ ] 修复后主题切换、语言按钮 `aria-label="切换语言"`、登录表单提交和登录后跳转不回退。
- [ ] 生产或类生产 MySQL `banners` 表包含 `brand_id`，旧表缺列时有幂等迁移或 drift 修复路径。
- [ ] 管理端可成功新建 `jump_type=BRAND_DETAIL` Banner，并持久化 `brand_id`、`image_source`、`image_object_key`、展示位置、排序和有效期。
- [ ] 管理端可成功编辑既有品牌详情 Banner。
- [ ] `brand_logo` 与 `custom_upload` 两种图片来源均按规则保存。
- [ ] 品牌不存在、品牌未启用、品牌无 Logo、Logo key 不匹配、标题重复等失败场景返回明确错误，不暴露原始 SQL、DSN、MinIO 凭据或内部堆栈。
- [ ] 保存成功后，管理端列表、详情和小程序对应轮播查询读取到同一配置。
- [ ] 非品牌跳转类型 Banner 保存、上线、下线和删除逻辑不回归。
- [ ] 管理端首页数据概览 SKU 总数、品牌数量、Banner 数量、用户数量来自真实后端数据源，不再依赖生产页面 Mock 常量。
- [ ] 管理端首页概览指标与对应业务表、后端查询或管理端列表页统计口径一致。
- [ ] 测试数据新增、更新或删除后，刷新 Dashboard 可展示更新后的真实统计结果。
- [ ] Dashboard 概览请求中展示 loading 或骨架态。
- [ ] Dashboard 概览真实统计为 0 时展示 0 或明确空状态，不以 Mock 数据填充。
- [ ] Dashboard 概览接口失败、鉴权失败或网络异常时展示错误状态或重试入口，不展示 Mock 数据作为成功结果。
- [ ] Dashboard 概览错误信息不泄露数据库 DSN、SQL、MinIO 凭据、内部堆栈或密钥。

## 3. 横切验收

- [ ] 管理端字段级密码错误在字段附近展示，不只依赖全局 Toast。
- [ ] 修改密码弹窗保持 520px computed width。
- [ ] 弹窗矮视口下 body scroll 和 footer 可访问。
- [ ] 成功反馈使用 fixed toast 或既有 AdminLayout toast，不造成 layout shift。
- [ ] 小程序 SKU 详情页其他底部操作入口和基础浏览能力不受影响。
- [ ] 小程序 SKU 详情页品牌卡片路由修复不影响品牌列表页品牌卡片、首页 Banner 品牌跳转和搜索 fallback。
- [ ] 小程序分类页二级分类长名称展示修复不影响一级分类切换、二级分类选中态、商品列表加载、空态展示或网络异常降级。
- [ ] 如 BUG-0077 仅调整小程序前端展示样式，验收记录明确不需要 OpenAPI / Orval；若字段结构变化，必须同步 OpenAPI / Orval。
- [ ] 小程序 usage-events 事件字面量、动态事件样例和后端事件定义存在防漂移测试。
- [ ] 小程序分享能力不新增自绘分享 UI，不遮挡微信原生胶囊。
- [ ] 小程序分享实现同步源文件与实际运行入口，避免 `.ts` / `.js` 漂移。
- [ ] REQ-0027 已执行 `/req-opsx REQ-0027-mobile-page-adaptation` 并回填 `update-web-admin-mobile-adaptation`；实现前通过 `/opsx-apply update-web-admin-mobile-adaptation --sprint auto` 门禁。
- [ ] REQ-0027 新增或修改的 UI 样式使用 semantic token / admin token，TSX/CSS 不新增裸 Hex 或任意设计色 `rgba(...)`。
- [ ] REQ-0027 管理端列表页分页、指标卡、fixed toast、DS confirm modal 对齐 admin-list best-practice，移动端允许换行但不得改变语义结构。
- [ ] REQ-0027 管理端表单页保持单一保存 CTA、fixed toast 和 DS confirm modal，不使用 `window.confirm` / `window.alert`。
- [ ] REQ-0027 管理端弹窗不得同时挂载 `modal-card` 与专属类；宽弹窗与窄弹窗需验收 computed width 和矮视口滚动。
- [ ] REQ-0027 品牌 Logo、Banner 图片、SKU 图片/视频、用户头像等已有上传控件移动端仍保持 `idle → uploading → done / failed` 状态机和即时回显；默认不改上传 API 或对象存储策略。
- [ ] 如 REQ-0027 未修改 API 契约，验收记录明确不需要 OpenAPI / Orval；若字段结构变化，必须同步 OpenAPI / Orval。
- [ ] 如 REQ-0027 未修改 DB / Docker / 环境变量 / MinIO，验收记录明确不需要数据库迁移和 Docker Compose 验证；若触及则补对应门禁。
- [ ] REQ-0065 管理端 SKU 列表分页、筛选、fixed toast、DS confirm modal 和空态文案不因主展示字段调整回归。
- [ ] REQ-0065 管理端 SKU 弹窗不得同时挂载 `modal-card` 与专属类；商品名称字段、错误提示、computed width 和矮视口滚动需回归。
- [ ] REQ-0065 小程序商品卡片、详情、推荐/收藏、搜索结果和分享标题隐藏 SKU 编码时，不影响跳转参数、收藏状态、品牌入口和搜索筛选。
- [ ] REQ-0065 如仅调整展示字段和既有 `sku_code` 自动生成逻辑且 API schema 不变，验收记录明确不需要 Orval；若请求/响应字段、错误码或数据库约束变化，必须同步 OpenAPI、Orval、数据库文档和测试。
- [ ] REQ-0065 不改变 MinIO 单桶策略、媒体上传链路或对象 Key 安全校验。
- [ ] REQ-0066 SKU 编辑弹窗不得同时挂载 `modal-card` 与专属类；图片移除按钮、主图标签、上传控件和底部操作在 computed width、矮视口滚动下不回归。
- [ ] REQ-0066 图片移除和主图切换保持上传控件 `idle → uploading → done / failed` 状态机与即时回显不回归；未触及上传链路时 Docker 边界上传验收标记为 N/A。
- [ ] REQ-0066 如仅调整前端图片数组状态和既有保存 payload 且 API schema 不变，验收记录明确不需要 OpenAPI / Orval；若请求/响应字段、错误码或 Pydantic schema 变化，必须同步 OpenAPI、Orval、API 文档和测试。
- [ ] REQ-0066 不物理删除 MinIO 对象，不改变 MinIO 单桶策略、对象 Key 安全校验、小程序或店主端展示能力。
- [x] REQ-0067 CategoryFormModal 不得同时挂载 `modal-card` 与专属类；computed width、矮视口滚动和底部操作区可达性不回归。
- [x] REQ-0067 类目名称、同层级唯一和排序权重必须有后端兜底测试，不能只依赖前端校验。
- [x] REQ-0067 如新增或调整错误码、请求字段或 Pydantic schema，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/standards/error-codes.md` 和测试；默认不需要 DB 迁移、Docker Compose 验证、小程序或 MinIO 变更。
- [x] REQ-0067 类目列表名称列展示需保持第一行名称、第二行仅编码，不展示层级路径。
- [ ] 如 BUG-0070 未修改 API 契约，验收记录明确不需要 OpenAPI / Orval。
- [ ] 如 BUG-0078 仅修改既有 API 字段取值且 schema 不变，验收记录明确不需要 Orval；若字段结构变化，必须同步 OpenAPI / Orval。
- [ ] 如 REQ-0064 未修改 API 契约，验收记录明确不需要 OpenAPI / Orval。
- [ ] 如 BUG-0071 未修改 API 契约，验收记录明确不需要 OpenAPI / Orval。
- [ ] BUG-0073 如新增或修改系统设置字段、上传限制查询、错误码或 API schema，必须同步 OpenAPI / Orval、`.env.example`、API 文档和测试；若未改 schema，验收记录明确不需要 Orval。
- [ ] BUG-0073 Docker/Web 入口上传边界文件不返回 Nginx 413，后端业务超限返回 400。
- [ ] BUG-0073 MinIO/S3 单 Bucket、`images/`、`videos/`、`files/` 前缀和对象 Key 安全校验不回退。
- [ ] BUG-0076 如仅恢复生产部署或反代配置，验收记录明确不需要 OpenAPI / Orval；若修改 API schema、媒体错误结构或对象存储读取行为，必须同步 OpenAPI / Orval。
- [ ] BUG-0076 生产视频修复不绕过 `/media/{object_key}` 受控读取链路，不让小程序直连未授权对象存储。
- [ ] BUG-0075 MySQL schema drift/迁移验证不依赖生产真实数据；默认 SQLite pytest 仍可本地运行。
- [ ] BUG-0075 管理端 Banner 保存错误使用统一 envelope，错误提示可理解且不造成表单 layout shift。
- [ ] BUG-0075 品牌 Logo 引用与 Banner 自定义上传仍通过后端鉴权、MinIO 适配层和 `/media/{object_key}` 受控读取。
- [ ] BUG-0075 如新增或调整错误码、响应字段或 API schema，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和错误码文档；若未改 schema，验收记录明确不需要 Orval。
- [ ] BUG-0079 如新增或修改 Dashboard 概览 API，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和后端/前端测试；若复用既有接口且 schema 不变，验收记录明确不需要 Orval。
- [ ] BUG-0079 Dashboard 真实数据接口必须走管理端鉴权，员工账号不得看到越权统计。

## 4. 测试与证据

| 项 | 状态 | 证据 |
|---|---|---|
| 后端密码策略测试 | pending | 待 `/opsx-apply` |
| 修改密码 API 测试 | pending | 待 `/opsx-apply` |
| 用户创建/重置密码测试 | pending | 待 `/opsx-apply` |
| Web 管理端提示测试 | pending | 待 `/opsx-apply` |
| OpenAPI/Orval 同步 | pending | 若实现阶段触发则补充 |
| 小程序分享矩阵静态测试 | passed | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`，覆盖四页面朋友分享与朋友圈分享 |
| 小程序分享参数编码测试 | passed | `tests/test_miniapp_static.py` 覆盖商品列表白名单 query 与中文编码；`implementation/share-evidence.md` 记录路径矩阵 |
| 小程序运行入口同步检查 | passed | `tests/test_miniapp_static.py` 覆盖四页面 `.ts` 与实际运行 `.js` 分享方法一致性 |
| 小程序分享 DevTools evidence | static_review | 当前环境无微信开发者工具截图能力；`implementation/share-evidence.md` 记录 320 / 375 / 430 pt 等价静态视口 evidence，未写作 DevTools 通过 |
| 小程序分享真机 evidence | follow_up | 当前环境无法执行真机验收；`implementation/share-evidence.md` 标记 `real_device_follow_up` 与剩余风险 |
| Web 管理端移动端 OpenSpec Change | passed | 已创建 `update-web-admin-mobile-adaptation` 并回填 sprint-010 |
| Web 管理端移动端 smoke | passed | `src/web/src/pages/admin/AdminMobileAdaptation.test.ts` 覆盖路由矩阵、移动断点、表格容器滚动、分页 DOM、modal/drawer 高度与 SKU/Banner 专属宽弹窗；`pnpm --dir src/web test` 通过 |
| Web 管理端移动端截图 evidence | static_review | 当前项目未引入 Playwright 依赖；以 Vitest/jsdom + CSS/source contract smoke 作为等价 evidence，后续真机或浏览器截图可在 archive 前补充 |
| Web 管理端弹窗/抽屉可用性 evidence | passed | smoke 覆盖通用 modal、SKU/Banner 宽弹窗、日志详情抽屉移动端宽高与滚动契约 |
| SKU 编码自动生成后端测试 | pending | 待 `/opsx-apply refine-sku-metadata-name-code-display` 后补充创建草稿/正式 SKU、唯一性、编辑商品名称不改编码证据 |
| 管理端 SKU 名称/编码展示测试 | pending | 待实现后补充 SKU 表单、列表、详情、搜索、确认文案和错误提示 evidence |
| 小程序 SKU 编码隐藏静态测试 | pending | 待实现后覆盖商品卡片、详情、推荐、收藏、搜索结果、分享标题不展示 SKU 编码 |
| SKU 搜索兼容测试 | pending | 待实现后补充商品名称搜索与 SKU 编码兼容命中但结果隐藏编码证据 |
| SKU 图片移除组件测试 | passed | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx` 通过，覆盖移除非主图、移除当前主图、移除全部图片和上传后即时回显可移除 |
| SKU 主图前置与兜底测试 | passed | `TileSkuFormModal.test.tsx` 覆盖设主图自动前置、payload 主图 `sort_order=0`、移除当前主图后一张优先；`removeImageDraft` 覆盖最后位置主图剩余第一张兜底 |
| SKU 图片 payload / 回填一致性测试 | passed | `TileSkuFormModal.test.tsx` 覆盖保存 payload 顺序和 `is_main` 标记；`uv run pytest src/backend/tests/test_admin_tile_skus.py` 覆盖后端主图第一、`sort_order` 连续和 GET/PUT 回填一致 |
| SKU 图片移除对象存储边界 | passed | `uv run pytest src/backend/tests/test_admin_tile_skus.py` 覆盖 PUT images 完整事实源、缺失图片解除关联、空 images 清空关联；未触及上传链路或物理删除 MinIO 对象，Docker 边界上传验收 N/A |
| 类目编码系统生成后端测试 | passed | `uv run pytest src/backend/tests/test_admin_tile_categories.py` 覆盖创建不传 `code` 成功、生成 `CAT-` 编码、客户端提交 `code` 不被信任 |
| 类目名称格式与同层级唯一后端测试 | passed | `uv run pytest src/backend/tests/test_admin_tile_categories.py` 覆盖空名称、超长名称、非法字符、同父级重复、编辑自身不误判和编辑改名重复 |
| 管理端类目弹窗组件测试 | passed | `pnpm --dir src/web exec vitest run src/features/admin/components/CategoryFormModal.test.tsx src/features/admin/api/tile-categories-api.test.ts` 覆盖隐藏编码输入、必填标识、上级类目选项、字段级错误和 create payload 不含 `code` |
| 管理端类目列表名称列测试 | passed | `pnpm --dir src/web exec vitest run src/pages/admin/TileCategoryManagementPage.test.tsx src/features/admin/components/CategoryFormModal.test.tsx src/features/admin/api/tile-categories-api.test.ts` 覆盖名称列第一行名称、第二行仅类目编码、不展示层级路径 |
| 类目 API / Orval 同步判定 | passed | 已运行 `./scripts/generate-openapi-client.sh`；`TileCategoryCreateRequest` 不包含 `code`，API 文档与错误码登记已同步 |
| 小程序 SKU 详情静态测试 | pending | 待 `/opsx-apply fix-miniapp-sku-detail-duplicate-brand-button` |
| 小程序截图 evidence | pending | 待实现后补充内容区入口与底部操作区截图 |
| 小程序 usage event 字典测试 | pending | 待 `/opsx-apply fix-miniapp-usage-events-contract-drift` |
| 小程序 usage event 防漂移测试 | pending | 待实现后覆盖 `src/miniapp/**` 字面量 track 事件和动态事件样例 |
| 小程序 usage-events Network evidence | pending | 待实现后补充收藏页、品牌详情页、商品/品牌卡片组件关键交互不再 400 的证据 |
| 媒体上传 23M 边界后端测试 | pending | 待 `/opsx-apply fix-upload-size-limit-consistency` |
| 媒体上传前端提示测试 | pending | 待实现后覆盖图片、视频、文档限制提示和失败状态 |
| 媒体上传 Docker/Web 入口 evidence | pending | 待实现后覆盖约 23M 文件、超限文件和非 413 业务错误 |
| 对象存储受控读取 evidence | pending | 待实现后确认 `/media/{object_key}` 可读取上传对象 |
| SKU 详情品牌入口 API 测试 | passed | `uv run pytest tests/test_miniapp_home.py` 通过 29 项；SKU 详情 `data.brand.brand_entry_path` 指向 `/pages/brand-detail/index?brandId=1`，品牌列表页入口不回归 |
| SKU 详情品牌卡片跳转 evidence | passed | `uv run pytest tests/test_miniapp_static.py` 通过 27 项；SKU 详情页仍使用 `brand-card`，品牌详情页仍注册在 `app.json`；接口返回品牌详情页路径后组件优先按 `brand_entry_path` 跳转 |
| 小程序分类页长名称静态测试 | pending | 待 `/opsx-apply fix-miniapp-category-secondary-name-truncated` |
| 小程序分类页长名称 evidence | pending | 待实现后补充 4 字以内、5-8 字、超过 8 字二级分类名称截图与点击证据 |
| Web 登录页工具区测试 | passed | `pnpm --dir src/web exec vitest run src/features/auth/components/LoginPage.test.tsx src/features/auth/components/LoginFormPanel.test.tsx src/features/auth/components/LoginForm.test.tsx src/features/theme/ThemeContext.test.tsx` 通过 4 files / 18 tests |
| Web 登录页截图 evidence | passed | Playwright CLI 生成 `/private/tmp/login-tools-desktop.png` 与 `/private/tmp/login-tools-mobile.png`；桌面/窄屏工具区不重叠、不裁切、不遮挡标题、表单或安全提示 |
| 品牌详情 Banner API 回归测试 | passed | `uv run pytest tests/test_admin_banners.py` 覆盖品牌详情新增、编辑、`brand_logo`、`custom_upload`、禁用品牌、无 Logo、Logo key 不匹配、重复标题和非品牌逻辑 |
| MySQL Banner schema drift/迁移验证 | passed | `uv run pytest ../../tests/test_mysql_migrations.py ../../tests/test_mysql_schema_drift.py` 覆盖旧 `banners` 表缺 `brand_id` 的幂等补齐、索引/外键取舍和 drift 检测 |
| 生产管理端 Banner 保存 smoke | follow_up | 当前本地会话无真实生产 Network/DB 访问；已在 `implementation/db.md` 记录发布前备份、迁移、drift check、回滚和证据要求 |
| 小程序 Banner 展示读取 evidence | passed | `uv run pytest ../../tests/test_miniapp_home.py` 覆盖首页轮播与品牌列表页轮播按 `position` 分流读取，品牌跳转保留 `target_id` |
| Dashboard 概览真实数据 API 测试 | passed | `uv run pytest src/backend/tests/test_admin_dashboard.py` 通过 4 项，覆盖真实计数、空数据 0、未登录 401、employee 隐藏用户统计 |
| Dashboard 概览前端测试 | passed | `pnpm --dir src/web exec vitest run src/pages/admin/DashboardPage.test.tsx` 通过 4 项，覆盖真实数值、loading、error、无权限隐藏用户统计 |
| OpenAPI/Orval 同步判定 | passed | BUG-0079 新增 Dashboard 概览 API；已运行 `./scripts/generate-openapi-client.sh` 并更新 `src/web/openapi.json`、`src/web/src/shared/api/generated.ts`、`docs/03-api-index.md` |

## 5. 结论

当前为 Sprint 规划阶段，验收结论待实现与测试后更新。
