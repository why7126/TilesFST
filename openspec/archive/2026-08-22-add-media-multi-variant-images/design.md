## 设计目标

本 Change 将媒体图片从单一原图 URL 使用模式升级为 `thumbnail / display / original` 三规格模型，使列表、详情展示和高清预览各自使用合适资源。设计必须同时覆盖增量上传、存量补生成、对象存储直出、小程序端实际请求和验收证据，避免只生成对象但端上仍加载原图。

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: possible
  storage: true
  api: true
capabilities:
  new:
    - media-multi-variant-images
  modified:
    - object-storage
    - miniapp-sku-detail-page
    - tile-sku-management
    - prod-media-maintenance-jobs
    - media-acceptance-template
```

## 核心设计

### 三规格资源模型

| 规格 | 语义 | 典型使用 |
|---|---|---|
| `thumbnail` | 低体积、快速可见 | 商品列表、卡片、轻量预览 |
| `display` | 清晰展示、控制下载成本 | 商品详情普通展示、图册浏览 |
| `original` | 上传原图或等价高清资源 | 高清预览、下载、纹理细节查看 |

三规格必须可追溯到同一媒体记录或业务对象。实现可以选择数据库显式字段、对象 key 约定派生或媒体服务适配层，但必须在 apply 阶段固定一种事实源，并同步 API / DB / docs / tests。

### 生成策略

- 新上传图片保留 `original`，并生成 `thumbnail` 与 `display`。
- 生成失败不得暴露内部路径或存储细节；是否阻断原图上传必须在实现设计中明确。
- `display` 规格必须在 apply 阶段明确目标宽高、质量、格式和体积上限。
- 透明 PNG、非透明 PNG、JPG、WebP 的保留或转换策略必须在 apply 阶段定稿。
- 生成逻辑必须遵守上传安全、MIME 白名单、对象 key 安全和 MinIO 单桶前缀策略。

### URL 与接口契约

商品、SKU 或媒体相关 API 应返回 `thumbnail_url`、`display_url`、`original_url`，或通过统一媒体服务返回等价语义字段。字段必须说明 URL 类型、缓存、签名、权限、过期和 fallback 策略。API 变化必须同步 OpenAPI、Orval、接口文档和测试；若最终不新增字段而采用媒体服务统一适配，必须在实现和文档中写明兼容原因。

### 对象存储直出

对象存储直出纳入本期，但不得让前端直连未授权对象存储。后端必须通过媒体服务或对象存储适配层生成受控 URL，明确以下边界：

- 签名 URL、公开 URL、后端 `/media` 代理 URL 的选择条件。
- URL 过期、缓存头、权限范围和失败 fallback。
- 原图默认公开风险，尤其是 `original` 不得默认无限公开。
- 后续 CDN URL 替换时保持字段语义稳定。

### 存量图片批量生成

存量图片批量生成纳入本期，必须提供 dry-run / apply 两阶段：

- dry-run 输出待处理数量、缺失规格、跳过原因、失败分类、预计写入对象和风险摘要。
- apply 必须显式触发，要求备份或风险确认，输出成功、失败、跳过、重试建议和幂等摘要。
- 输出必须脱敏，不包含真实密钥、真实 `.env`、Authorization header、Cookie、本机绝对路径、真实客户数据或完整 object key。
- 二次审计必须验证 key、object、URL、render 和规格收益。

## UI Contract

本 REQ 存在 `prototype/web/context.md`，但没有完整页面 HTML 或 PNG，当前事实源优先级为：

```text
prototype/web/context.md > acceptance.md > requirement.md > rules/ui-design.md > openspec/specs
```

页面与入口：

- 本 Change 不默认新增独立管理端页面。
- 若实现涉及管理端上传控件或生成状态展示，应在 SKU 新增/编辑、媒体上传或维护入口中承载。
- 若实现涉及小程序展示，应覆盖商品列表、SKU 详情展示、图片预览和加载失败态。

信息架构：

- 上传入口展示上传状态、派生生成状态、失败摘要和同会话回显。
- 存量批量生成入口若出现 UI，必须包含范围、dry-run 结果、风险确认、apply 结果和失败统计。
- 小程序展示不增加解释型页面文案，只通过图片组件绑定、fallback 和预览行为体现。

视觉 token 与交互：

- Web 管理端必须使用 Design System semantic token，不得新增裸 Hex。
- 上传控件必须覆盖 `idle -> uploading -> done / failed`。
- 失败态必须靠近上传控件、字段组或媒体对象，不能只依赖全局 toast。
- 小程序列表、详情、预览必须具备稳定 fallback，避免空白、无限 loading 或重复请求。

Mock/API 边界：

- apply 前不得把 Mock URL 写作真实 API 完成。
- 如果某端暂只做静态绑定测试，验收必须标记端上 Network evidence 待补或 blocked。
- 真实 API 字段、权限和错误态必须在 OpenAPI / Orval / docs / tests 中同步。

权限规则：

- 管理端上传和批量生成入口必须鉴权。
- 店主端和小程序只能读取允许公开或受控签名的媒体 URL。
- 前端不得使用未授权 object key 拼接对象存储地址。

一致性参照：

- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`
- `docs/standards/prototype-ui-acceptance.md`

## 冲突处理报告

| 事实源 | 结论 |
|---|---|
| `prototype/web/context.md` | 明确当前不绘制完整页面，后续如涉及 UI 必须补 UI Contract 与截图证据。 |
| `acceptance.md` | 要求功能 AC、媒体四联、小程序 Network evidence 和横切 AC。 |
| `rules/ui-design.md` | Web 管理端必须复用 DS token 与上传 best practice。 |
| 既有 `miniapp-sku-detail-page` spec | 详情页已有高清展示与预览语义，本 Change 将 `display_url` 与 `original_url` 固化为通用能力。 |

无 HTML / PNG 视觉冲突；本 Change 的 UI 风险属于后续 apply 阶段需要补证的交互与截图证据。

## 验收策略

- API / Orval / docs / tests：新增或变更字段必须同步。
- DB：若新增字段或迁移，必须同步 SQLite/MySQL schema、迁移文档和测试；若不改表，必须说明派生规则。
- 对象存储：验证三规格对象存在、MIME、size、key/prefix、直出 URL 和 fallback。
- 小程序：验证列表、详情、预览三类 URL 实际请求，记录 DevTools、体验版或真机 Network evidence。
- 存量批量生成：验证 dry-run、apply、幂等、失败统计、二次审计和脱敏输出。
