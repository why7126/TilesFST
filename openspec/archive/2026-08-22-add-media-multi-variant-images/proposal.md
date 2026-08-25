## 背景

小程序商品详情页冷加载分析暴露出通用媒体能力缺口：当前列表、详情普通展示和高清预览对原图或大图 URL 的依赖较重，无法稳定按场景控制下载体积、清晰度和后端 `/media` 代理压力。`BUG-0132` 负责具体详情页偏差，本 Change 负责把背后的通用能力沉淀为可复用的媒体多规格图机制。

`REQ-0115` 已评审并纳入 `sprint-025`，评审确认存量图片批量生成与对象存储直出均纳入本期；生产 CDN 正式接入只做能力预留，不作为本期必达项。

## 变更内容

- 新增媒体图片多规格展示图能力，定义 `thumbnail`、`display`、`original` 三类资源语义、生成策略、失败降级和追踪要求。
- 扩展商品、SKU 或媒体相关 API 的多规格 URL 契约，覆盖 `thumbnail_url`、`display_url`、`original_url` 或等价统一媒体服务字段。
- 修改小程序 SKU 详情和相关列表媒体选择策略：列表使用轻量图，详情展示使用 `display`，高清预览使用 `original`，首屏外图片启用 lazy-load。
- 修改对象存储能力，明确多规格对象 key/prefix、同源追溯、对象存储直出签名/缓存/权限/fallback 边界，后续 CDN 保持可替换。
- 扩展生产媒体维护作业，支持存量图片批量生成多规格资源的 dry-run / apply、幂等、失败统计、二次审计和脱敏输出。
- 扩展媒体验收模板，要求多规格图同时覆盖 key、object、URL、render、thumbnail/display benefit 和小程序 Network evidence。
- 不实现视频转码、多清晰度视频、生产 CDN 正式接入或独立媒体处理平台。

## 能力范围

### 新增能力

- `media-multi-variant-images`：媒体图片多规格展示图能力，覆盖三规格资源模型、上传生成、接口 URL、多端选择、存量批量生成、对象存储直出和验收证据。

### 修改能力

- `object-storage`：补充多规格对象 key/prefix、受控读取与对象存储直出边界。
- `miniapp-sku-detail-page`：补充 SKU 详情页 `display` / `original` URL 使用、首屏外 lazy-load 和 Network evidence。
- `tile-sku-management`：补充管理端 SKU 图片上传、列表/详情/编辑返回多规格 URL 和回显要求。
- `prod-media-maintenance-jobs`：补充存量图片批量生成多规格资源的 dry-run / apply 作业。
- `media-acceptance-template`：补充多规格图和小程序媒体 evidence 验收维度。

## 影响

- 后端：影响 media / uploads / object storage 适配层、SKU 媒体组装、存量维护脚本或命令。
- API：可能新增或扩展商品、SKU、媒体响应字段；需要同步 OpenAPI、Orval、API 文档和测试。
- 数据库：需要评估是否新增媒体派生关系字段；若不新增表字段，必须明确可派生 URL 规则和对象追溯方式。
- 对象存储：新增或规范 `thumbnail`、`display`、`original` 派生对象 key/prefix，支持对象存储直出。
- Web 管理端：上传状态机、同会话回显、生成状态和列表/详情/预览规格选择可能受影响。
- 微信小程序：列表、详情展示、预览、lazy-load、fallback 和 Network evidence 受影响。
- 测试与文档：需要补充媒体四联/五联、小程序 Network evidence、存量批量生成 dry-run/apply、对象存储直出安全边界和发布前检查。
