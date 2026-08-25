## 背景

`REQ-0119-admin-display-image-size-limit-setting` 已确认：管理端「系统设置 - 媒体与存储」已有缩略图体积目标上限配置，但 display 图体积目标仍由后端常量固定为 768KB，管理员无法独立调整详情展示图的清晰度与流量平衡。

该配置应作为 `REQ-0115-media-multi-variant-images` 的后续治理补齐项落地，默认值沿用 768KB，并保持与 `media.thumbnail_max_size_kb` 完全独立。

## 变更内容

- 在系统设置 media 分组新增 display 图体积目标上限配置，默认 effective 值为 `768` KB。
- 管理端 `/admin/settings/media` 新增「详情展示图体积目标上限 (KB)」字段，复用既有 settings shell、footer 保存 CTA、DS modal 和 fixed toast。
- 系统设置 GET / PATCH / reset、Pydantic Schema、OpenAPI / Orval 和管理端类型消费同步新增字段。
- `.display` 派生图生成、SKU pending 图片正式化和存量图片多规格维护任务读取同一 effective 配置。
- 保存系统设置不自动扫描、读取、覆盖或重建历史 `.display` 对象；历史对象策略调整仍走受控维护任务。
- 保持 `.display` key、URL、bucket、前缀、受控 `/media/...` 读取和图片格式策略稳定。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `system-settings`：media 分组新增 display 图体积目标字段、API 契约、管理端 UI 与 reset 默认值。
- `media-multi-variant-images`：display 派生图生成和维护任务重生成必须读取系统设置 effective 配置。
- `object-storage`：派生 display 对象仍保持同目录 key / URL / 受控读取规则，并补齐配置变更后的媒体四联验收要求。
- `prod-media-maintenance-jobs`：历史图片多规格维护任务重生成 display 图时读取同一配置，且保持 dry-run / apply 边界。

## 影响范围

- 后端：系统设置 media schema/service、图片派生生成配置读取、上传与 SKU pending 图片正式化链路、维护任务配置读取。
- Web 管理端：系统设置媒体页字段展示、编辑、保存、恢复默认、dirty 切换确认、fixed toast 与 UI 验收。
- API：`GET /api/v1/admin/system-settings/media`、`PATCH /api/v1/admin/system-settings/media`、`POST /api/v1/admin/system-settings/media/reset` 响应与 payload 字段。
- OpenAPI / Orval：系统设置 schema 与前端生成类型需要同步。
- 对象存储：只影响 `.display` 派生对象内容和目标体积，不改变 key、URL、bucket、前缀或权限边界。
- 数据库：若系统设置使用 KV 表存储，不新增业务表；如存在 seed/defaults 需要同步默认值。
- 测试与验收：后端 API、图片派生、维护任务、管理端 UI、媒体四联 evidence、OpenSpec 和语言校验。
