## 背景

当前 SKU 图片和视频已经具备 `pending` 到 `tiles/{tile_id}` 的正式化目录治理，但品牌 Logo、Banner、品牌证书、头像等媒体仍主要按资源类型目录加 UUID 存储。不同媒体类型的 Key 归属规则不一致，会让存量迁移、派生图回填、对象审计和旧媒体兼容判断变得模糊。

REQ-0131 要求统一所有媒体对象 Key 按业务对象 id 分目录，并把旧媒体读取兼容、受控迁移、文档规范和观测验收纳入同一交付边界。

## 变更内容

- 统一新增媒体对象 Key 目录矩阵：头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片和品牌证书文件均按业务对象 id 归属。
- 为业务对象创建前上传建立统一 `pending` 暂存与保存后 formalize 规则。
- 保留旧数据库媒体引用的受控读取兼容，避免历史 URL 因新目录策略中断。
- 增加存量媒体迁移要求：dry-run、apply、二次审计、幂等、备份确认和回滚边界。
- 要求图片原图、`.thumb.webp`、`.display.webp` 保持同一业务对象目录或等价可追溯目录。
- 同步对象存储、媒体上传、批处理 Runbook、生产媒体维护作业、发布验收和产品数据采集与链路观测声明。
- 不在本 Change 中直接删除旧对象；旧对象清理必须作为单独高风险动作确认。

## 能力影响

### 新增能力

- 无。该变更是在既有对象存储、媒体上传、业务管理和生产维护能力上统一规则。

### 修改能力

- `object-storage`：统一媒体对象 Key 按业务对象 id 分目录、pending/formalize、旧 key 兼容和迁移边界。
- `brand-management`：品牌 Logo 上传与保存后回显需归属 `brand-logos/{brand_id}/`。
- `banner-management`：Banner 自定义图片需归属 `banners/{banner_id}/`。
- `brand-certificate-management`：证书图片与文件需归属 `brand-certificates/{certificate_id}/`。
- `tile-sku-management`：SKU 图片与视频继续使用 `tiles/{tile_id}/`，并对 pending/formalize、派生图和旧 key 兼容补齐统一验收。
- `user-management`：用户头像需归属 `user-avatars/{user_id}/`，并保持旧头像引用兼容。
- `prod-media-maintenance-jobs`：存量媒体迁移需具备 dry-run/apply/audit/rollback、脱敏输出和失败分类。
- `batch-image-processing-runbook`：批处理 Runbook 需补齐业务 id 目录迁移、派生图同步和旧对象清理边界。

## 影响范围

- 后端：上传 Key 生成、保存后 formalize、媒体服务、对象存储适配层、迁移/审计维护任务、错误处理和脱敏输出。
- API：上传响应、保存接口和媒体读取 URL 语义可能需要补充说明；若响应字段变化，必须同步 OpenAPI、Orval、API 文档和测试。
- 数据库：优先复用既有媒体引用字段；若新增媒体别名表、迁移状态表或索引，必须同步 SQLite/MySQL schema、迁移和数据库文档。
- 对象存储：新增正式业务对象 id 目录和 pending 目录；保留旧 key 读取兼容；旧对象不默认删除。
- Web 管理端：既有上传入口、同会话回显、保存后回显和字段级错误需要回归验证。
- 店主端与小程序：媒体展示应继续消费后端 URL，不自行拼接新目录；需补 render/Network evidence。
- 文档：更新 `rules/object-storage.md`、`rules/media.md`、`docs/07-object-storage-strategy.md`、批处理 Runbook 和发布验收材料。
- Docker Compose：若上传边界、Nginx 或维护任务执行方式变化，需通过 Docker Web 或生产 Compose 入口验证；若不变化需记录 N/A 原因。

## Requirement Readiness Report

REQ-0131 readiness：partially ready，可创建 Change。

- 已具备：`requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md`、`prototype/web/context.md` 和 `review.md`。
- 状态门禁：REQ 已评审并纳入 `sprint-027`，当前状态为 `in_sprint`。
- 非阻塞项：命中的 `media-upload` best-practice 为 draft，且本需求默认不新增 UI 原型 PNG；后续实现阶段需用既有上传入口补验收证据。
