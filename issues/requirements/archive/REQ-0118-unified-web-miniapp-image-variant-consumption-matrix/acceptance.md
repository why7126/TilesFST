---
requirement_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
acceptance_status: passed
created_at: 2026-08-22 21:04:14
updated_at: 2026-08-25 14:51:36
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 输出统一消费矩阵，字段固定为：页面、位置、图对象、是否缩略图、是否 display 图、是否原图、优化方案。
- [ ] AC-002 矩阵覆盖微信小程序首页、商品列表、搜索、商品详情、品牌列表、品牌详情、证书列表、证书详情、收藏等页面。
- [ ] AC-003 矩阵覆盖 Web 管理端 SKU、Banner、品牌、品牌证书、用户头像等真实媒体展示位置。
- [ ] AC-004 店主 Web 展示端只按“预留规范”列入矩阵，不得写成当前真实页面已满足。
- [ ] AC-005 矩阵明确 `thumbnail` 用于列表、卡片、推荐位、小 Logo、证书缩略卡和视频封面。
- [ ] AC-006 矩阵明确 `display` 用于详情普通展示、图册浏览、表单大预览和证书详情普通展示。
- [ ] AC-007 矩阵明确 `original` 仅用于高清预览、下载、审核保真或原文件查看。
- [ ] AC-008 非原图目标场景不得 fallback 到 `original`；当前存在原图 fallback 的位置必须在优化方案中标记移除或补齐目标规格。
- [ ] AC-009 同一页面位置若同时包含普通展示和点击预览，必须拆成不同矩阵行，不得一行同时标记 display 和 original。
- [ ] AC-010 优化方案列必须逐行填写；无需优化写 `-`，需优化写明补字段、换规格、移除原图 fallback、补占位或拆分预览场景。
- [ ] AC-011 矩阵必须说明后续规范落点，且避免与父需求三规格全局语义形成重复事实源冲突。
- [ ] AC-012 本需求不得直接修改 `src/`、不得创建 OpenSpec Change、不得新增 API 字段、不得修改数据库结构。

## 目标消费矩阵

| 页面 | 位置 | 图对象 | 是否缩略图 | 是否 display 图 | 是否原图 | 优化方案 |
|---|---|---|---|---|---|---|
| 小程序首页 | Banner | 商品 / Banner | 是 | 否 | 否 | 若当前链路存在原图 fallback，改为安全占位或补齐缩略图。 |
| 小程序首页 | 新品 / 热销 / 全部商品卡片 | 商品 | 是 | 否 | 否 | - |
| 小程序首页 | 品牌入口或配置 Logo | 品牌 / 配置 | 是 | 否 | 否 | 本地静态配置图不纳入三规格；业务品牌图使用缩略图。 |
| 小程序商品列表页 | 商品卡片主图 | 商品 | 是 | 否 | 否 | - |
| 小程序搜索页 | 商品搜索结果卡片 | 商品 | 是 | 否 | 否 | - |
| 小程序商品详情页 | Banner 普通展示 | 商品 | 否 | 是 | 否 | 缺 display 时不得回退原图；补齐 display 或使用安全占位。 |
| 小程序商品详情页 | 图片预览 | 商品 | 否 | 否 | 是 | - |
| 小程序商品详情页 | 品牌区域 | 品牌 | 是 | 否 | 否 | 若详情接口只提供品牌原图，补充品牌缩略图字段或改用安全占位。 |
| 小程序商品详情页 | 同系统推荐 | 商品 | 是 | 否 | 否 | - |
| 小程序商品详情页 | 同品牌推荐 | 商品 | 是 | 否 | 否 | - |
| 小程序商品详情页 | 视频封面 | 视频封面 / 商品 | 是 | 否 | 否 | 缺视频封面缩略图时使用商品缩略图或安全占位，不回退视频原文件。 |
| 小程序品牌列表页 | Banner | Banner / 品牌 | 是 | 否 | 否 | 若当前链路存在原图 fallback，移除原图 fallback。 |
| 小程序品牌列表页 | 品牌 Logo | 品牌 | 是 | 否 | 否 | - |
| 小程序品牌详情页 | 品牌 Logo | 品牌 | 是 | 否 | 否 | 若实际展示尺寸升级为头图，再拆分 display 行。 |
| 小程序品牌详情页 | 品牌商品 | 商品 | 是 | 否 | 否 | - |
| 小程序品牌详情页 | 品牌证书 | 证书 | 是 | 否 | 否 | - |
| 小程序证书列表页 | 证书缩略图 | 证书 | 是 | 否 | 否 | - |
| 小程序证书详情页 | 证书普通展示 | 证书 | 否 | 是 | 否 | 补齐或改用 display；不得用 thumbnail 或 original 充当普通展示通过项。 |
| 小程序证书详情页 | 图片预览 / 文件查看 | 证书 | 否 | 否 | 是 | PDF 或原文件查看使用 original；图片预览使用 original。 |
| 小程序收藏页 | 收藏商品卡片 | 商品 | 是 | 否 | 否 | 收藏快照字段若只保存原图，后续修正为保存或派生缩略图。 |
| 小程序分类页 / 门店信息页 / 发现页 | 无业务媒体或静态图 | - | 否 | 否 | 否 | 不涉及业务图片；如后续接入业务图，按矩阵补行。 |
| Web 管理端 SKU 管理 | SKU 列表主图 | 商品 | 是 | 否 | 否 | 移除原图 fallback；缺缩略图时显示安全占位或标记需补齐派生图。 |
| Web 管理端 SKU 管理 | SKU 表单图片网格 / 大预览 | 商品 | 否 | 是 | 否 | 移除原图 fallback；缺 display 时使用安全占位并提示补齐。 |
| Web 管理端 SKU 管理 | SKU 图片高清预览 / 原图查看 | 商品 | 否 | 否 | 是 | - |
| Web 管理端 Banner 管理 | Banner 列表图 | Banner | 是 | 否 | 否 | 移除原图 fallback；补齐缩略图或安全占位。 |
| Web 管理端 Banner 管理 | Banner 表单选择 / 回显预览 | Banner / 商品 / 品牌 | 否 | 是 | 否 | 按来源对象选择 display；品牌小 Logo 场景可拆分为 thumbnail；不得使用原图回显。 |
| Web 管理端 Banner 管理 | Banner 原图审核或放大查看 | Banner | 否 | 否 | 是 | 若当前无独立入口，可不纳入实现；矩阵保留语义。 |
| Web 管理端品牌管理 | 品牌列表 Logo | 品牌 | 是 | 否 | 否 | 移除原图 fallback；缺缩略图时使用品牌占位。 |
| Web 管理端品牌管理 | 品牌表单 Logo 回显 | 品牌 | 是 | 否 | 否 | 编辑态不得直接使用原图；如展示区域放大，再拆为 display。 |
| Web 管理端品牌证书管理 | 证书列表缩略图 | 证书 | 是 | 否 | 否 | 移除原文件 fallback；缺缩略图时使用文件类型占位。 |
| Web 管理端品牌证书管理 | 证书表单附件 / 图片预览 | 证书 | 否 | 是 | 否 | 图片普通预览补 display；PDF 用文件卡片，不用原图充当 display。 |
| Web 管理端品牌证书管理 | 证书下载 / 原文件查看 | 证书 | 否 | 否 | 是 | - |
| Web 管理端用户 / 个人资料 | 头像列表 / 菜单 | 头像 | 是 | 否 | 否 | 若仅有 `avatar_url`，补头像缩略图或明确例外审批；不得默认原图。 |
| Web 管理端用户 / 个人资料 | 头像表单回显 | 头像 | 是 | 否 | 否 | 若头像裁剪或大预览场景存在，再拆分 display 或 original。 |
| 店主 Web 预留 | 商品列表 / 商品卡片 / 推荐商品 | 商品 | 是 | 否 | 否 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 商品详情普通展示 / 图册浏览 | 商品 | 否 | 是 | 否 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 点击放大 / 高清预览 / 下载 | 商品 / 证书 | 否 | 否 | 是 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 品牌列表 Logo / 品牌卡片 | 品牌 | 是 | 否 | 否 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 品牌详情 Logo 或头图普通展示 | 品牌 | 否 | 是 | 否 | 预留规范；若只是小尺寸 Logo，应拆分为 thumbnail。 |
| 店主 Web 预留 | 证书列表 | 证书 | 是 | 否 | 否 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 证书详情普通展示 | 证书 | 否 | 是 | 否 | 预留规范，非当前实现验收。 |
| 店主 Web 预留 | 证书下载或原文件查看 | 证书 | 否 | 否 | 是 | 预留规范，非当前实现验收。 |

## 影响矩阵

| 影响项 | 本需求是否涉及 | 证据要求 |
|---|---|---|
| API | 否 | 本需求只沉淀规范矩阵；若后续修正偏离点需要字段，必须另行在 Change 中记录接口、响应字段、错误码和兼容性。 |
| Orval | 否 | 本需求不改 API schema；后续 API 字段变更时必须同步 OpenAPI 与 Orval。 |
| DB | 否 | 本需求不改表、不改业务记录、不新增迁移。 |
| 对象存储 | 否 | 本需求不写入对象、不改 key/prefix；后续派生图补齐需记录 object、URL 和权限边界。 |
| Web 管理端 | 是 | 只梳理真实媒体消费位置和优化方案，不修改 UI 或前端代码。 |
| 店主 Web | 是 | 仅预留规范，不做当前页面验收。 |
| 微信小程序 | 是 | 梳理真实页面消费位置和优化方案，不修改小程序代码。 |
| 媒体验收模板 | 是 | 后续应引用该矩阵，禁止把原图 fallback 作为缩略图或 display 性能通过证据。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 21:35:35
accepted_by: workflow-sync
source_change: update-media-image-variant-consumption-matrix
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表复发类缺陷

- [ ] AC-XCUT-001 若后续 Change 修改 Web 管理端列表页，分页 DOM 必须继续使用用户管理基准的 `page-summary` + `page-right`，并验证真实后端 total；N/A — 本需求只沉淀矩阵，不修改列表实现。
- [ ] AC-XCUT-002 若后续 Change 修改 Web 管理端列表页，操作成功/失败 toast 不得引起 hero、表格或列表纵向位移；N/A — 本需求不新增 Web 操作。
- [ ] AC-XCUT-003 若后续 Change 涉及状态变更类操作，必须使用 DS confirm，且不得使用 `window.confirm`；N/A — 本需求不新增状态变更操作。
- [ ] AC-XCUT-004 若后续 Change 修改列表列展示，表头和普通字段默认 nowrap，长文本不得撑宽整表或挤压操作列；N/A — 本需求不改列表列宽。

> 来源：`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防 Sprint 003 管理端弹窗宽度层叠复发类缺陷

- [ ] AC-XCUT-005 若后续 Change 修改 Banner、SKU、品牌或证书表单弹窗，TSX 不得同时挂载 `modal-card` 与业务专属 modal class；N/A — 本需求不修改弹窗代码。
- [ ] AC-XCUT-006 若后续 Change 修改管理端弹窗，必须在 1440 视口验证 Computed width 符合目标宽度；N/A — 本需求不修改弹窗样式。
- [ ] AC-XCUT-007 若后续 Change 修改管理端弹窗，矮视口下 body scroll 不得回归；N/A — 本需求不修改弹窗样式。

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002 媒体上传与对象存储链路复发类缺陷

- [ ] AC-XCUT-008 若后续 Change 涉及图片、视频、头像或 Logo 上传，必须验收上传状态机 `idle -> uploading -> done/failed`，失败信息应落在上传控件或对象附近；N/A — 本需求不新增上传控件。
- [ ] AC-XCUT-009 若后续 Change 涉及媒体上传或回显，必须验证同会话即时回显，记录缩略图、展示图、文件卡片或媒体 URL 入口；N/A — 本需求不新增上传控件。
- [ ] AC-XCUT-010 若后续 Change 涉及上传大小、Nginx 或 Docker Web 边界，必须经 `http://localhost:3000` 验证，不得只调用后端 `:8000`；N/A — 本需求不改上传边界。
- [ ] AC-XCUT-011 若后续 Change 涉及媒体对象读写，必须记录脱敏 `object_key`、对象存在性、`/media/{object_key}` 访问状态、业务错误码和用户可见表现；N/A — 本需求不读写对象存储。
- [ ] AC-XCUT-012 若后续 Change 涉及新增上传，新增对象不得写入 `data/uploads/`，历史 key 兼容或迁移必须记录标准前缀和对象结果；N/A — 本需求不新增上传。

