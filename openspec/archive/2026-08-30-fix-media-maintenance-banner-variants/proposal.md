## 背景

BUG-0146 记录了生产环境批量媒体维护命令未覆盖 Banner 自定义上传图的问题。生产样本中 `/media/images/default/banners/<uuid>.thumb.webp` 返回 200，但响应头为 `Content-Type: image/png`、`Content-Length: 6191144`、`x-media-fallback: 1`，说明缺失的 WebP 缩略图被 `/media` fallback 到原图掩盖。

现有 Banner 上传接口已按同目录策略请求生成 `thumbnail` 与 `display` 派生图，但历史批量维护任务的候选来源未包含 `banners.image_object_key`。因此历史 Banner 缺少 `.thumb.webp` / `.display.webp` 时，`backfill-image-variants`、缩略图专项任务和 `media-drift-reconcile` 都无法发现并补齐。

## 变更内容

- 将 Banner 自定义上传图纳入批量媒体维护候选来源，来源类型使用 `banner_image` 或等价稳定枚举。
- 让 `backfill-image-variants` 对 Banner 原图生成同目录 WebP `.thumb.webp` 与 `.display.webp`。
- 让缩略图专项任务和 `media-drift-reconcile` 聚合任务覆盖 Banner `.thumb.webp` 缺失候选。
- 保持 dry-run 默认只读，apply 继续要求 `--apply --confirm-backup`，重复执行保持幂等。
- 输出继续脱敏，不暴露真实 bucket、密钥、连接串、完整 object key、生产私有 URL、Authorization header、Cookie 或 `.env` 内容。
- 更新生产媒体维护 Runbook，明确 Banner 覆盖范围、生成格式、历史原图保留策略、dry-run 进入 apply 条件和 JSON 输出解析。
- 补充聚焦测试，覆盖候选来源、dry-run/apply 行为、聚合任务统计和脱敏输出。

## 能力影响

### 修改能力

- `prod-media-maintenance-jobs`：生产媒体维护任务必须覆盖 Banner 自定义上传图。
- `media-multi-variant-images`：存量图片多规格生成必须包含 Banner 自定义上传图。
- `banner-management`：Banner 自定义上传图必须可被历史派生图维护任务补齐。

## 影响范围

- 后端：涉及 `app.modules.media.maintenance` 候选来源与维护任务统计。
- 对象存储：新增历史 Banner 派生对象写入路径，格式为 WebP；不改写原图对象格式和访问语义。
- 文档：涉及生产媒体维护 Runbook。
- 测试：涉及媒体维护任务单元测试和部署脚本/Runbook 相关测试。
- API：不新增或修改 HTTP API。
- 数据库：不新增表、字段或迁移；只读取现有 `banners.image_object_key`。
- Web / 管理端 / 小程序：不改 UI；apply 后需补端侧 render evidence。
- Orval：不涉及，无 OpenAPI 变更。
- Docker Compose：不改变 Compose 配置；继续通过现有生产 `docker-compose exec` 或 `deploy/scripts/media-maintenance.sh` 入口执行。

## 回滚计划

- 代码回滚：回退本 Change 对维护任务候选来源、测试和 Runbook 的修改。
- 数据回滚：本 Change 生成的 `.thumb.webp` / `.display.webp` 是派生对象，不删除或改写原图；若必须回退对象存储状态，以 apply 前对象存储 bucket / prefix 快照恢复为准。
- 数据库回滚：不涉及 DB schema；维护任务不应改写 `banners.image_object_key`。
- 运行回滚：若 apply 过程中发现异常，停止后保留 JSON 输出和失败分类，修复后重新 dry-run；重复执行应保持幂等。

## 产品数据采集与链路观测

`product_data_collection_observability` 判定为部分适用。

```yaml
product_data_collection_observability:
  status: partial
  affected_layers:
    - backend
    - storage
  reason: 本变更涉及后端维护命令读取现有 Banner 业务记录并写入对象存储派生图，但不新增业务 API、DB schema、请求日志、行为事件、Task Trace 或端侧请求封装。
  validation: 通过维护任务 dry-run/apply/幂等 JSON 摘要、脱敏输出检查、对象存储派生图检查和端侧 render evidence 验证。
```

适用层级：`backend`、`storage`。本变更涉及后端维护命令和对象存储历史派生对象写入，但不新增业务 API、DB schema、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。

若实现阶段引入持久化任务进度、Task Trace 写入、HTTP 任务接口或端侧字段变更，必须重新补齐 affected layers、脱敏边界、保留周期和验证项。
