---
purpose: 生产媒体维护作业 Runbook
content: 记录媒体漂移聚合任务、缩略图与 WebP 派生图重新生成任务的执行命令、处理过程、结果解读和验收口径
source: REQ-0099-global-thumbnail-size-limit / BUG-0116-prod-media-historical-object-drift 运维沉淀
update_method: 媒体维护任务、生产 Compose 入口或对象存储验收口径变化时更新
created_at: 2026-08-05 23:16:00
updated_at: 2026-08-30 08:10:01
---

# 生产媒体维护作业 Runbook

## 1. 适用范围

本文档用于生产或生产等价环境中的媒体历史维护任务，覆盖：

- 媒体漂移聚合任务：SKU 主图暂存路径正式化、所有媒体业务对象 id 目录迁移、证书图片 key 迁移、SKU / Banner 自定义上传图 / 品牌 Logo / 证书图片缩略图回填和对象 key 二次审计；能力来源包含 BUG-0116、BUG-0146 运维沉淀与 REQ-0131。
- 历史缩略图和详情展示图重新生成任务：让历史 SKU、Banner 自定义上传图、品牌 Logo 与品牌证书图片 `.thumb` 读取当前 `media.thumbnail_max_size_kb` effective 策略，`.display` 读取当前 `media.display_max_size_kb` effective 策略。
- 运维 dry-run、备份确认、apply、二次审计和结果解读。

保存系统设置中的“缩略图体积目标上限 (KB)”和“详情展示图体积目标上限 (KB)”只影响后续新生成派生图，不会自动扫描或覆盖历史 `.thumb` / `.display` 对象。历史资源要应用新策略，必须显式执行本文档中的维护任务。

## 2. 执行前检查

执行 apply 前必须完成：

- MySQL 快照或等价数据库备份。
- 对象存储 bucket / prefix 快照，至少覆盖 `images/`、`files/`、`images/default/banners/` 和相关 `.thumb` / `.display` 对象。
- 确认生产 `.env` 指向预期数据库与对象存储。
- 先跑 dry-run，并确认输出中 `environment.database_backend`、`environment.object_storage_provider` 和 `environment.object_storage_bucket_hash` 符合预期。
- 确认 `thumbnail_max_size_kb` 和 `display_max_size_kb` 为预期值；`0` 表示不限制，正整数表示尽量不超过目标 KB，`display_max_size_kb` 默认值为 `768`。

## 3. 生产命令

每个维护任务都支持两种生产运行方式：

- 根目录兼容 `docker-compose` 入口：复用当前生产 Compose 文件，进入 `tilesfst-backend` 容器执行维护模块。
- `./deploy/scripts/` 包装入口：优先用于已迁移到 `deploy/` 部署矩阵的环境；生产 `prod mysql-tencent-cos` 会使用 `deploy/prod/compose.tencent-cos.yml` 的 `tilesfst-maintenance` 服务运行同一个后端维护模块。

两种入口的任务参数、JSON 输出和结果判断口径一致。缺少 `--apply --confirm-backup` 时均为 dry-run，不写 MySQL 或对象存储。命令示例默认把 stdout 重定向到当前执行目录的时间戳 JSON 文件，便于保存、比对和归档；Docker 或脚本的 stderr 提示仍会显示在终端。生产 JSON 虽然只包含脱敏 key hash 和统计摘要，提交或外发前仍需按安全规则复核。

### 3.0 进度输出

`backfill-image-variants`、`backfill-brand-certificate-thumbnails` 和 `media-drift-reconcile` 支持可选 `--progress` 参数。未传入该参数时，命令仍只在 stdout 输出最终 JSON，既有 `jq`、重定向和审计归档脚本不需要调整。

启用 `--progress` 后，过程进度写入 stderr，最终 JSON 仍写入 stdout。生产执行时可以将 stdout 保存为审计 JSON，同时把 stderr 作为运行日志保存：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-image-variants --progress \
  > backfill-image-variants-apply-$(date +%Y%m%d%H%M%S).json \
  2> backfill-image-variants-progress-$(date +%Y%m%d%H%M%S).log
```

进度行示例：

```text
progress task=backfill-image-variants stage=image_variant_backfill status=running completed=1 total=720 progress_percent=0.14 success=0 failed=0 skipped=0
```

字段口径：

| 字段 | 说明 |
|---|---|
| `task` | 当前维护任务名。 |
| `stage` | 当前阶段；`media-drift-reconcile` 会展示 5 个子任务阶段。 |
| `completed` / `total` | 已完成 item 数和当前任务或阶段总量。 |
| `progress_percent` | `completed / total` 的百分比，保留两位小数。 |
| `success` / `failed` / `skipped` | 当前已知成功、失败、跳过计数；dry-run 候选 item 完成扫描后会进入 `completed`，是否需要写入仍以最终 JSON 的 `estimated_writes` 和 `retry_candidates` 为准。 |

`backfill-image-variants` 的进度总量按去重原图 item 计算，`estimated_writes` 按预计写入派生对象数计算。同一原图可能同时需要 `.thumb.webp` 和 `.display.webp`，因此 `estimated_writes` 可能大于进度总量。

`media-drift-reconcile` 的进度总量按 5 个聚合阶段计算：`sku_pending_formalization`、`business_id_media_key_migration`、`certificate_image_key_migration`、`brand_logo_and_certificate_thumbnail_backfill` 和 `object_key_audit`。阶段内部完整明细仍以最终 JSON 的 `tasks.*` 为准。

聚合任务进入子任务后，会继续输出当前子任务的 item 级心跳。此时同一个 `stage` 的 `total` 会切换为该子任务 item 总数，`completed` 表示该子任务已处理 item 数。长耗时对象迁移阶段会在慢操作前输出枚举化状态：

| 状态 | 含义 |
|---|---|
| `item_started` | 开始处理当前 item。 |
| `checking_source` | 正在检查源对象是否存在。 |
| `checking_target` | 正在检查目标对象是否存在。 |
| `copying_object` | apply 模式下正在复制原对象或派生对象。 |
| `updating_db` | apply 模式下正在更新数据库引用。 |

如果日志长时间停在 `checking_source` 或 `checking_target`，优先排查对象存储网络、权限、限流和 bucket/prefix 可访问性；如果长时间停在 `copying_object`，优先排查对象体积、COS 上传耗时和连接稳定性；如果停在 `updating_db`，优先排查数据库锁、连接池和事务提交耗时。

进度输出只包含任务名、阶段名、计数、百分比和枚举状态，不输出真实 object key、原始文件名、客户信息、数据库连接串、对象存储 endpoint、access key、secret key、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。需要审计失败对象时，继续使用最终 JSON 中的脱敏 hash、标准前缀和失败原因枚举。

本进度能力不新增 API、数据库 Schema、Web、管理端、小程序、Orval、对象 key 策略、派生图生成策略或生产备份确认门禁。

### 3.1 媒体漂移聚合任务

命令用途：面向生产数据库中已公开或已绑定的头像、SKU 主图/视频、Banner 自定义上传图、品牌 Logo、品牌证书图片和证书文件引用，处理 SKU 主图仍停留在 `images/default/tiles/pending/`、媒体对象缺少业务 id 目录、图片类证书仍落在 `files/default/brand-certificates/`、`.thumb` 缩略图缺失或复制原图、Banner 缺少 `.thumb.webp` / `.display.webp` 导致 `/media` fallback 到原图、对象 key 仍不符合标准前缀策略等历史媒体漂移问题。

#### 3.1.1 dry-run

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance media-drift-reconcile --limit 100 --progress \
  > media-drift-reconcile-dry-run-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100 --progress \
  > media-drift-reconcile-dry-run-$(date +%Y%m%d%H%M%S).json
```

dry-run 结果正常的判断：

- 输出 `mode: dry_run`、`dry_run: true`。
- `environment.database_backend`、`environment.object_storage_provider`、`environment.object_storage_bucket_hash` 与预期生产环境一致。
- `summary.failed = 0`，且不存在 `summary.status = blocked` 或 `failure_category = object_storage_unreachable`。
- `pending_main_images`、`business_id_media_candidates`、`certificate_file_image_candidates`、`thumbnail_candidates` 或 `retry_candidates` 大于 0 表示发现可处理候选，可以在备份后分批 apply；不代表已经修复。Banner 候选会出现在 `tasks.business_id_media_key_migration.items[].source_type = banner_image` 或 `tasks.brand_logo_and_certificate_thumbnail_backfill.items[].source_type = banner_image`。
- `non_standard_keys_after_audit = 0` 表示本次二次审计未发现残留不规范 key；大于 0 时先看 `tasks.object_key_audit`。
- `acceptance_summary.key.status = pass`、`acceptance_summary.object.status = pass` 只证明 key / object 维度通过；`URL: n/a` 和 `render: blocked` 仍要求 apply 后补端侧 URL 与展示证据。

是否进入 apply 的判断：

- 可以进入 apply：`environment.*` 符合预期、`summary.failed = 0`、未出现 `summary.status = blocked` / `failure_category = object_storage_unreachable`，且 `pending_main_images`、`business_id_media_candidates`、`certificate_file_image_candidates`、`thumbnail_candidates`、`retry_candidates` 任一项大于 0；如果本次目标是修复 Banner，需确认明细中存在 `source_type = banner_image` 或 Banner 前缀候选；同时已完成 MySQL 和对象存储 bucket / prefix 备份。
- 不需要进入 apply：上述候选项全部为 0，且 `non_standard_keys_after_audit = 0`，表示本批没有可处理历史漂移。
- 不得进入 apply：`summary.failed > 0`、对象存储不可达、生产环境指纹不符、`non_standard_keys_after_audit > 0` 且无法解释，或备份未完成。

生成格式与删除策略：

- dry-run 只输出候选、目标 key hash、标准前缀、统计摘要和失败原因，不生成新对象、不更新数据库、不删除历史对象。
- 输出中的 `target`、`target_thumbnail` 或候选统计只是 apply 计划；不能据此清理 COS 或修改数据库。

#### 3.1.2 apply

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance media-drift-reconcile --limit 100 --apply --confirm-backup --progress \
  > media-drift-reconcile-apply-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100 --apply --confirm-backup --progress \
  > media-drift-reconcile-apply-$(date +%Y%m%d%H%M%S).json
```

apply 结果正常的判断：

- 输出 `mode: apply`、`dry_run: false`，且 `environment.*` 仍指向预期生产环境。
- `summary.failed = 0`，且不存在 `summary.status = blocked` 或 `failure_category = object_storage_unreachable`。
- 各子任务 `summary.success` 表示本批实际写入数量；`summary.skipped`、`already_conformant` 或 `document_skipped` 表示按规则跳过。
- 若 `summary.retry_candidates` 在 apply 输出中仍大于 0，只表示本批进入处理的候选计数；最终是否清零必须以 apply 后重新 dry-run 为准。
- apply 后重新跑 3.1.1 dry-run，若 `pending_main_images = 0`、`business_id_media_candidates = 0`、`certificate_file_image_candidates = 0`、`thumbnail_candidates = 0`、`retry_candidates = 0`、`non_standard_keys_after_audit = 0`，且目标 Banner 不再出现在 `source_type = banner_image` 缺失派生图候选中，表示维护侧闭环。
- `acceptance_summary.render.status = blocked` 是预期提示；维护侧闭环后仍需补管理端、店主 Web 或小程序渲染证据。

生成格式与删除策略：

- SKU pending 主图正式化会把原图复制到 `images/default/tiles/{tile_id}/{filename}`，并把数据库 `tile_images.object_key` / `url` 更新到正式 key；原图格式和扩展名保持不变。
- 业务 id 目录迁移会把头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件复制到 `{prefix}/default/{business_media_type}/{business_object_id}/{filename}`，并更新业务表引用。若目标对象已存在，任务可只更新数据库引用以保持幂等。已短暂生成的 `users/{id}/avatars`、`brands/{id}/logos`、`banners/{id}/images`、`tiles/{id}/images` 等过渡目录只作为兼容来源，不作为最终目标。
- SKU 正式化会同时写入目标同目录 `.thumb.webp` / `.display.webp` 派生对象；如果源派生对象已存在则复制到目标同目录，否则从原图生成 WebP 派生对象。
- 图片类证书 key 迁移会把 `files/default/brand-certificates/...` 下的图片复制到 `images/default/brand-certificates/...`，并更新证书表 `file_key`；PDF 和非支持图片类型继续保留在 `files/`。
- 缩略图回填会为 SKU、Banner 自定义上传图、品牌 Logo 和品牌证书图片写入或覆盖同目录 `.thumb.webp`，Content-Type 为 `image/webp`；聚合任务中的缩略图子任务不单独生成 `.display.webp`，Banner 详情展示图补齐建议优先使用 3.3 的 `backfill-image-variants`。
- 本任务不删除旧对象：pending 源对象、历史缺少业务 id 目录的源对象、旧 `files/` 图片对象、旧 `.thumb` / `.display` 派生对象默认保留。删除只能在备份和验收完成后，通过单独受控清理脚本或人工对象存储清理流程执行，且必须以当前数据库引用和对象存储快照为依据。

### 3.2 缩略图专项重建任务

命令用途：面向 SKU 图片、Banner 自定义上传图、品牌 Logo 和品牌证书图片的同目录 `.thumb` 缩略图，单独审计或重生成缺失、与原图同 size、与原图 bytes 完全一致，或在配置了 `thumbnail_max_size_kb` 时超过目标体积的历史缩略图。本任务适合只补 Banner `.thumb.webp` 的场景；不处理 `.display.webp`、SKU pending 主图正式化、证书 `files/` 到 `images/` 迁移，也不做对象 key 聚合审计。

#### 3.2.1 dry-run

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-brand-certificate-thumbnails --limit 100 --progress \
  > backfill-brand-certificate-thumbnails-dry-run-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100 --progress \
  > backfill-brand-certificate-thumbnails-dry-run-$(date +%Y%m%d%H%M%S).json
```

dry-run 结果正常的判断：

- 输出 `mode: dry_run`、`dry_run: true`。
- `environment.*` 与预期生产环境一致，`summary.failed = 0`，`summary.failure_reasons = {}`。
- `summary.total` 表示本批纳入审计的去重原图数量。
- `summary.retry_candidates` / `summary.estimated_writes` 表示预计会重生成的 `.thumb` 数量；大于 0 时可在备份后 apply。Banner 候选会出现在 `items[].source_type = banner_image`，`object_key_prefix` 通常为 `images/default/banners`。
- `summary.missing_thumbnail`、`summary.same_size`、`summary.same_bytes`、`summary.exceeds_target_size` 用于解释候选来源。
- `acceptance_summary.render.status = n/a` 是预期结果；该任务不承担端侧页面展示验收。

是否进入 apply 的判断：

- 可以进入 apply：`environment.*` 符合预期、`summary.failed = 0`、`summary.failure_reasons = {}`，且 `summary.retry_candidates > 0` 或 `summary.estimated_writes > 0`；如果本次目标是 Banner，需确认 `items[].source_type = banner_image` 存在并对应 `images/default/banners` 前缀；同时已完成对象存储相关 prefix 备份。
- 不需要进入 apply：`summary.retry_candidates = 0`、`summary.estimated_writes = 0`、`summary.failed = 0`，表示本批 `.thumb` 缩略图无需重建。
- 不得进入 apply：存在失败原因、对象存储不可达、生产环境指纹不符、`thumbnail_max_size_kb` 与预期配置不一致，或备份未完成。

生成格式与删除策略：

- dry-run 只审计现有原图和同目录 `.thumb.webp`，输出预计写入数量和候选原因，不生成新缩略图、不覆盖现有缩略图、不删除历史对象。
- `estimated_writes` 只代表 apply 可能写入的 `.thumb.webp` 数量；不是删除清单。

#### 3.2.2 apply

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-brand-certificate-thumbnails --limit 100 --apply --confirm-backup --progress \
  > backfill-brand-certificate-thumbnails-apply-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100 --apply --confirm-backup --progress \
  > backfill-brand-certificate-thumbnails-apply-$(date +%Y%m%d%H%M%S).json
```

apply 结果正常的判断：

- 输出 `mode: apply`、`dry_run: false`，且 `environment.*` 与预期生产环境一致。
- `summary.failed = 0`，`summary.failure_reasons = {}`。
- `summary.success` 表示本批成功重生成并写入 `.thumb` 的数量。
- `summary.already_conformant` / `skipped` 表示无需覆盖的对象数量。
- `summary.not_within_target` 大于 0 时，需要结合图片复杂度和 `thumbnail_max_size_kb` 目标值判断是否接受。
- apply 后重新跑 3.2.1 dry-run，若 `retry_candidates = 0`、`estimated_writes = 0`、`failed = 0`，表示缩略图存储维护侧闭环。
- 如果影响小程序卡片、证书卡片、品牌 Logo 或管理端列表，仍需补端侧 render 证据。

生成格式与删除策略：

- apply 从 SKU、Banner 自定义上传图、品牌 Logo 或证书图片原图生成同目录 `.thumb.webp`，默认最大尺寸为缩略图规格，Content-Type 为 `image/webp`，并读取当前 `media.thumbnail_max_size_kb` effective 策略。
- 目标 `.thumb.webp` 已存在但被判定缺失收益、同 size、同 bytes 或超过目标时，会被新的 WebP 缩略图覆盖；已符合策略的对象跳过。
- 原图不会被转换或删除；历史 `.thumb.jpg`、`.thumb.png` 或其他旧派生对象不会被本任务删除。后续如需清理旧派生对象，必须另走受控清理流程，并先确认没有数据库、Web、小程序或缓存链路仍引用旧 key。

### 3.3 缩略图与详情展示图 WebP 派生任务

命令用途：面向历史 SKU 图片、Banner 自定义上传图、品牌 Logo 和品牌证书图片，批量审计或生成同目录 `.thumb.webp` 与 `.display.webp` 派生对象。该任务适合在调整“缩略图体积目标上限 (KB)”或“详情展示图体积目标上限 (KB)”后，让历史图片重新应用当前策略，也适合修复 Banner 只有原图、缺少 `.thumb.webp` / `.display.webp` 时的访问 fallback。它不会把原图整体替换为 WebP，也不会更新业务原图 key；原图继续保留上传时的格式，WebP 仅作为列表、卡片和详情普通展示的派生资源。

#### 3.3.1 dry-run

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-image-variants --limit 100 --progress \
  > backfill-image-variants-dry-run-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-image-variants --limit 100 --progress \
  > backfill-image-variants-dry-run-$(date +%Y%m%d%H%M%S).json
```

dry-run 结果正常的判断：

- 输出 `mode: dry_run`、`dry_run: true`。
- `environment.*` 与预期生产环境一致，`summary.failed = 0`，`summary.failure_reasons = {}`。
- `summary.total` 表示本批纳入审计的去重原图数量。
- `summary.thumbnail_missing` / `summary.display_missing` 表示缺少对应 `.thumb.webp` 或 `.display.webp`。
- `summary.thumbnail_no_benefit` / `summary.display_no_benefit` 表示既有派生对象与原图同 size 或同 bytes，未体现轻量化收益。
- `summary.estimated_writes` 表示预计写入的派生对象数量；同一原图可能同时写 `.thumb.webp` 与 `.display.webp`。
- `summary.retry_candidates` 表示仍需处理的原图候选数量；候选数量不等于写入对象数。Banner 候选会出现在 `items[].source_type = banner_image`，并分别标记 `needs.thumbnail` 与 `needs.display`。
- `summary.banner_legacy_alias_missing` 表示已进入 `images/default/banners/{banner_id}/` 目录的 Banner，旧无 id 路径 `images/default/banners/<filename>.thumb.webp` 或 `.display.webp` 仍缺失或不合格的原图数量。该值大于 0 时，历史 URL 仍可能 fallback 到原图。
- `summary.banner_legacy_alias_writes` 表示预计写入的 Banner 旧无 id 兼容派生对象数量；同一 Banner 最多包含 `thumb` 与 `display` 两个 alias。

是否进入 apply 的判断：

- 可以进入 apply：`environment.*` 符合预期、`summary.failed = 0`、`summary.failure_reasons = {}`，且 `summary.retry_candidates > 0` 或 `summary.estimated_writes > 0`；如果本次目标是 Banner，需确认 `items[].source_type = banner_image` 且 `needs.thumbnail = true`、`needs.display = true`、`needs.banner_legacy_thumbnail = true` 或 `needs.banner_legacy_display = true`；同时已完成对象存储相关 prefix 备份。
- 不需要进入 apply：`summary.retry_candidates = 0`、`summary.estimated_writes = 0`、`summary.failed = 0`，表示本批 `.thumb.webp` / `.display.webp` 派生对象无需重建。
- 不得进入 apply：存在失败原因、对象存储不可达、生产环境指纹不符、`thumbnail_max_size_kb` 或 `display_max_size_kb` 与预期配置不一致，或备份未完成。

生成格式与删除策略：

- dry-run 只审计 `.thumb.webp` 和 `.display.webp` 是否缺失或需要重建；对已迁入 `images/default/banners/{banner_id}/` 的 Banner，同时审计旧无 id 路径兼容 alias 是否缺失或不合格。dry-run 不生成派生图、不覆盖对象、不删除历史数据。
- `estimated_writes` 是预计写入的派生对象数量；同一原图最多可能对应两个预计写入对象，不是删除数量。

#### 3.3.2 apply

docker-compose 运行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-image-variants --limit 100 --apply --confirm-backup --progress \
  > backfill-image-variants-apply-$(date +%Y%m%d%H%M%S).json
```

deploy 脚本运行：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-image-variants --limit 100 --apply --confirm-backup --progress \
  > backfill-image-variants-apply-$(date +%Y%m%d%H%M%S).json
```

apply 结果正常的判断：

- 输出 `mode: apply`、`dry_run: false`，且 `environment.*` 与预期生产环境一致。
- `summary.failed = 0`，`summary.failure_reasons = {}`。
- `summary.success` 表示成功生成并写入的 `.thumb.webp` / `.display.webp` 派生对象数量。
- `summary.skipped` 表示无需覆盖的原图数量。
- `summary.banner_legacy_alias_writes` 表示本次纳入处理的 Banner 旧无 id 兼容派生对象数量；apply 正常后，旧无 id URL 的 `curl -I` 应直接返回 WebP，而不是 fallback 到原图。
- `summary.not_within_target` 大于 0 时，需要评估 `thumbnail_max_size_kb` 或 `display_max_size_kb` 是否过低。
- apply 后重新跑 3.3.1 dry-run，若 `retry_candidates = 0`、`estimated_writes = 0`、`failed = 0`、`banner_legacy_alias_missing = 0`，且目标 Banner 不再显示 `needs.thumbnail = true`、`needs.display = true`、`needs.banner_legacy_thumbnail = true` 或 `needs.banner_legacy_display = true`，表示 WebP 派生对象维护侧闭环。
- 该任务不能替代端侧验收；影响 Banner、列表、卡片、详情图或证书图展示时，需要抽样验证 `/media/{object_key}` URL 和 Web / 小程序 / 管理端渲染。Banner `.thumb.webp` / `.display.webp` 的 `curl -I` 正常应返回 `Content-Type: image/webp`，且不应出现 `x-media-fallback: 1`。

生成格式与删除策略：

- apply 为每个候选原图生成或重生成同目录 `.thumb.webp` 与 `.display.webp`，Content-Type 均为 `image/webp`；已迁入业务 id 目录的 Banner 示例形态为 `images/default/banners/{banner_id}/<uuid>.thumb.webp` 与 `images/default/banners/{banner_id}/<uuid>.display.webp`。
- 对已经迁入 `images/default/banners/{banner_id}/<filename>` 的 Banner，apply 还会维护历史无 id URL 兼容 alias：`images/default/banners/<filename>.thumb.webp` 与 `images/default/banners/<filename>.display.webp`。若 canonical WebP 已存在，优先复制 canonical 派生对象；否则从 Banner 原图生成。
- `.thumb.webp` 使用缩略图规格并读取 `media.thumbnail_max_size_kb` effective 策略；`.display.webp` 使用详情展示图规格，最大宽高为 1600x1600，读取 `media.display_max_size_kb` effective 策略，默认目标为 768KB。
- 已存在但不合格的 `.thumb.webp` / `.display.webp` 或 Banner 旧无 id alias 会被覆盖；已符合策略的派生对象跳过。
- 原图不会被转换、覆盖或删除；历史 `.thumb.jpg`、`.display.jpg`、`.thumb.png`、`.display.png` 等兼容派生对象不会被本任务删除。清理旧格式派生对象必须在端侧验收和引用确认后另行执行。

## 4. 聚合任务处理过程

`media-drift-reconcile` 是生产推荐聚合入口，单次执行会运行 5 个子任务。`bug-0116-media-drift` 仅作为历史兼容别名保留，用于兼容旧脚本、日志或已归档证据：

| 子任务 | 作用 | 是否写入 |
|---|---|---|
| `sku_pending_formalization` | 将公开 SKU 主图从暂存目录正式化到 SKU 目录，并同步缩略图 | apply 时写对象存储和数据库 |
| `business_id_media_key_migration` | 将头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件迁入业务对象 id 目录；用户头像使用字符串/UUID 用户 id 目录 | apply 时写对象存储和数据库 |
| `certificate_image_key_migration` | 将图片类证书从 `files/` 前缀迁移到 `images/` 前缀 | apply 时写对象存储和数据库 |
| `brand_logo_and_certificate_thumbnail_backfill` | 审计或重生成 SKU、Banner 自定义上传图、品牌 Logo 与品牌证书图片同目录 `.thumb` | apply 时写对象存储 |
| `object_key_audit` | 二次审计头像、品牌 Logo、Banner、SKU 图片/视频和证书对象 key 是否仍不规范 | 始终只读 |

`--limit 100` 是分别传给每个子任务的限制，不是聚合任务全局最多处理 100 条。因此聚合输出中的总样本数可能超过 100。

## 5. 顶层结果解读

输出是 JSON，先看顶层字段。顶层字段在聚合任务和独立缩略图任务中都存在；聚合任务的各子任务结果位于 `tasks.*`，独立任务的同类结果直接位于顶层。

### 5.1 通用顶层字段

| 字段 | 结果解读 |
|---|---|
| `task` | 当前输出所属任务名。`media-drift-reconcile` 表示生产推荐聚合任务；`bug-0116-media-drift` 仅表示历史兼容别名；`backfill-brand-certificate-thumbnails` 表示独立缩略图任务；`backfill-image-variants` 表示缩略图与详情展示图双派生任务。 |
| `mode` | 执行模式。`dry_run` 只审计和预估，不写数据库或对象存储；`apply` 才会执行写入。 |
| `dry_run` | 布尔值形式的写入开关。`true` 与 `mode: dry_run` 一致，表示本次结果只能作为计划和风险判断，不能当作已经修复完成。 |
| `limit` | 本次单任务或每个聚合子任务的处理上限。聚合任务里不是全局上限，因此多个子任务样本相加可能超过该值。 |
| `summary` | 当前任务的汇总结论。聚合任务顶层 `summary` 是 5 个子任务的归纳；独立缩略图任务顶层 `summary` 是缩略图审计结论。 |
| `tasks` | 仅聚合任务存在，记录 5 个子任务的完整输出。排障时应先看顶层 `summary`，再进入对应 `tasks.*.summary` 和 `tasks.*.items`。 |
| `items` | 单任务的明细列表。聚合任务顶层没有 `items`，需要到 `tasks.*.items` 查看；明细 key 只输出 hash 和 prefix，不输出真实完整 key。 |
| `environment` | 执行环境快照，用于确认是否跑在预期生产数据库和对象存储上。环境不符合预期时，不能继续 apply。 |
| `acceptance_summary` | 验收摘要，按 key、object、URL、thumbnail benefit、render 分项说明本次维护输出能证明什么、不能证明什么。 |

### 5.2 environment 字段

| 字段 | 本次两份数据的值 | 结果解读 |
|---|---|---|
| `environment.app_env` | `production` | 两份结果都来自生产环境配置，不能按本地或 demo 结果处理。 |
| `environment.database_backend` | `mysql` | 连接的是生产 MySQL 后端；apply 前必须确认 MySQL 已备份。 |
| `environment.object_storage_provider` | `tencent-cos` | 媒体对象落在腾讯云 COS；apply 前必须确认 COS bucket / prefix 快照已完成。 |
| `environment.object_storage_bucket_hash` | `29590d9aae43` | 两份结果指向同一脱敏 bucket hash，可用于确认没有跨 bucket 误跑；该字段不是完整 bucket 名。 |
| `environment.auto_create_bucket` | `false` | 生产不会自动创建 bucket；如果 bucket 或权限异常，任务应失败而不是创建新 bucket。 |

### 5.3 acceptance_summary 字段

| 字段 | 本次两份数据的值 | 结果解读 |
|---|---|---|
| `acceptance_summary.task` | `media-drift-reconcile` / `backfill-brand-certificate-thumbnails` | 标识这份验收摘要对应的任务，归档证据时要和 JSON 文件名、执行命令对应；历史证据中可能出现兼容别名 `bug-0116-media-drift`。 |
| `acceptance_summary.key.status` | `pass` | 抽样对象 key 前缀符合任务预期，没有发现 key 格式阻断。 |
| `acceptance_summary.key.samples` | 聚合任务 `243`，独立缩略图任务 `299` | 表示参与 key 验收的样本数。聚合任务样本来自多个子任务，独立任务样本来自缩略图审计集合。 |
| `acceptance_summary.object.status` | `pass` | 抽样对象存在性检查通过，没有发现对象缺失阻断。 |
| `acceptance_summary.object.samples` | 聚合任务 `243`，独立缩略图任务 `299` | 表示参与对象存在性验收的样本数。 |
| `acceptance_summary.URL.status` | `n/a` | 维护任务不请求 HTTP 媒体 URL，因此不能用该字段证明前端 URL 可访问。 |
| `acceptance_summary.URL.reason` | `maintenance audit does not call HTTP media URLs` | URL 验收缺口原因是任务设计只访问存储和数据库，不走 Web HTTP 链路。 |
| `acceptance_summary.thumbnail_benefit.status` | `pass` | 缩略图收益检查通过；本次发现的 copied-original 缩略图会进入候选，已符合策略的会跳过。 |
| `acceptance_summary.thumbnail_benefit.reason` | `null` | `pass` 时没有额外阻断原因；若为非 pass，需要先解释原因再 apply。 |
| `acceptance_summary.render.status` | 聚合任务 `blocked`，独立缩略图任务 `n/a` | 聚合任务仍需要 Web 或小程序展示证据；独立缩略图任务是存储审计，不负责页面渲染验收。 |
| `acceptance_summary.render.reason` | 聚合任务 `requires Web or miniapp evidence after apply`；独立缩略图任务 `task is storage/database audit only` | 表示维护 JSON 不能替代页面抽样，apply 后仍要补管理端、小程序或店主端展示截图/访问证据。 |

### 5.4 聚合任务顶层 summary 字段

| 字段 | 本次值 | 结果解读 |
|---|---:|---|
| `summary.task_count` | 5 | 聚合任务已运行 5 个子任务：SKU 主图正式化、业务对象 id 目录迁移、证书图片 key 迁移、缩略图回填、对象 key 审计。 |
| `summary.failed` | 0 | 聚合层未发现失败项；可进入备份确认和分批 apply 判断。 |
| `summary.retry_candidates` | 55 | 当前聚合 dry-run 发现 55 个需要重生成或重试的缩略图候选。 |
| `summary.pending_main_images` | 0 | 没有公开 SKU 主图仍停留在暂存目录，本批无需主图正式化。 |
| `summary.business_id_media_candidates` | 0 | 没有头像、品牌 Logo、Banner、SKU 图片/视频或证书媒体仍需要迁入业务对象 id 目录；若大于 0，需查看 `tasks.business_id_media_key_migration`。 |
| `summary.certificate_file_image_candidates` | 0 | 没有图片类证书仍需要从 `files/` 迁移到 `images/`。 |
| `summary.thumbnail_candidates` | 55 | 本批真正待处理的是 55 个缩略图候选，主要来自 copied-original 缩略图。 |
| `summary.non_standard_keys_after_audit` | 0 | 二次审计未发现遗留不规范 key；key 漂移侧当前通过。 |

推荐判断：

```text
failed = 0 且 retry_candidates > 0
→ dry-run 已找到可处理对象，可在备份后分批 apply。

failed > 0
→ 不要 apply，先看 tasks.*.summary.failure_reasons 与 items。

summary.status = blocked 且 failure_category = object_storage_unreachable
→ 不要进入备份确认或 apply；先修复对象存储环境，再重新 dry-run。

pending_main_images = 0 且 business_id_media_candidates = 0 且 certificate_file_image_candidates = 0 且 thumbnail_candidates = 0 且 non_standard_keys_after_audit = 0
→ 本批次没有发现需要处理的历史漂移。
```

示例 `media-drift-reconcile` 的结论是：无失败、无 SKU 主图暂存漂移、无业务对象 id 目录迁移候选、无证书图片 key 迁移候选、对象 key 审计通过，但仍有 55 个缩略图候选需要在备份后 apply。

### 5.5 对象存储不可达 blocked 摘要

当 dry-run 输出 `failure_category: object_storage_unreachable` 时，表示维护任务无法可靠验证对象维度。该状态与单个对象不存在不同，不应解释为 `missing_original`、`missing_thumbnail` 或普通 `object_exists=false`。

blocked 摘要通常包含：

| 字段 | 结果解读 |
|---|---|
| `summary.status` | `blocked` 表示对象维度被环境阻断。 |
| `summary.failure_category` | `object_storage_unreachable` 表示 endpoint、region、bucket、权限、凭据、网络或对象存储服务状态不可用。 |
| `summary.affected_tasks` | 受影响对象相关子任务；聚合任务会把后续对象相关子任务标记为 blocked 或 skipped。 |
| `summary.can_apply` | `false` 时不得进入 apply 判断。 |
| `summary.recommended_action` | 按 endpoint、region、bucket、权限、网络和 env 注入顺序排查，修复后重新 dry-run。 |
| `acceptance_summary.object.status` | `blocked` 表示对象存在性无法验收。 |
| `acceptance_summary.thumbnail_benefit.status` | 对需要读取原图或缩略图的任务，blocked 表示缩略图收益无法验收。 |

排查顺序：

1. 确认生产 env 指向预期 `OBJECT_STORAGE_PROVIDER`、endpoint、region 和 bucket。
2. 确认对象存储 bucket / prefix 快照存在，且凭据具备最小读写权限。
3. 确认后端容器网络能访问对象存储 endpoint。
4. 确认 access key / secret key 或云厂商临时凭据仍有效。
5. 修复后重新执行 dry-run，再判断是否进入备份确认和 apply。

blocked 摘要只允许输出 provider、bucket hash、auto create bucket 策略、失败分类和建议动作；不得输出真实 bucket 名、raw object key、密钥、连接串、生产 `.env`、私有 URL、完整 SDK 堆栈或本机绝对路径。

## 6. 缩略图任务结果解读

缩略图子任务为 `tasks.brand_logo_and_certificate_thumbnail_backfill`，独立任务输出时位于顶层 `summary`。该任务虽然沿用历史命令名 `backfill-brand-certificate-thumbnails`，但处理范围包含 SKU、Banner 自定义上传图、品牌和证书图片。

### 6.1 summary 每字段结果解读

| 字段 | 独立缩略图任务本次值 | 聚合内缩略图子任务本次值 | 结果解读 |
|---|---:|---:|---|
| `total` | 299 | 199 | 本次纳入缩略图审计的去重原图数量。独立任务覆盖范围更大，因此样本数高于聚合内子任务。 |
| `success` | 0 | 0 | dry-run 不实际写入，所以成功写入数为 0；apply 后才应出现写入成功数。 |
| `failed` | 0 | 0 | 未发现读取、解码、生成或写入层面的失败；这是继续 apply 的必要条件。 |
| `skipped` | 220 | 144 | 已符合当前策略或无需处理的对象数量。 |
| `missing_thumbnail` | 0 | 0 | 未发现同目录 `.thumb` 缺失；本次候选不是因为缩略图不存在。 |
| `same_size` | 79 | 55 | 这些 `.thumb` 与原图体积相同，疑似历史复制原图，需要重生成。 |
| `same_bytes` | 79 | 55 | 这些 `.thumb` 与原图 bytes 完全一致，是 copied-original 的明确证据。 |
| `exceeds_target_size` | 0 | 0 | 未发现超过当前 `thumbnail_max_size_kb` 目标的既有缩略图。 |
| `already_conformant` | 220 | 144 | 已通过审计的对象数量，apply 不应重复覆盖。 |
| `estimated_writes` | 79 | 55 | dry-run 预估 apply 会写入的 `.thumb` 数；应作为本批 COS 写入量预估。 |
| `not_within_target` | 0 | 0 | dry-run 未出现“生成后仍不达标”的记录；apply 后如果大于 0，需要按图片复杂度或目标过低解释。 |
| `retry_candidates` | 79 | 55 | 当前仍需处理的缩略图候选数。独立任务还有 79 个，聚合任务当前批次有 55 个。 |
| `failure_reasons` | `{}` | `{}` | 没有失败原因聚合；如果非空，应按原因分组处理后再继续。 |
| `thumbnail_max_size_kb` | 0 | 0 | 当前生效缩略图策略是不限制目标 KB；本次候选来自 copied-original，而不是超过 KB 上限。 |
| `display_max_size_kb` | 768 | 768 | 当前生效详情展示图策略为 768KB；`backfill-image-variants`、聚合任务中的多规格回填和 pending 正式化会按该值生成 `.display`。 |

### 6.2 items 每字段结果解读

| 字段 | 结果解读 |
|---|---|
| `items[].source_type` | 来源类型。`sku_image` 为 SKU 主图，`banner_image` 为 Banner 自定义上传图或 `images/default/banners/` 标准目录图，`brand_logo` 为品牌 Logo，`certificate_file` 为证书文件引用，`certificate_image` 为图片类证书引用。 |
| `items[].source_id` | 来源表记录 ID，用于在受控生产环境中定位业务记录。文档或日志归档时不应补充真实对象 key。 |
| `items[].object_key_hash` | 原图对象 key 的脱敏 hash，用于排障对照；不是可直接访问的对象 key。 |
| `items[].object_key_prefix` | 原图对象 key 的目录前缀。本次样本可能包含 `images/default/tiles/...`、`images/default/banners`、`images/default/brands/logos`、证书相关前缀等。 |
| `items[].thumbnail.object_key_hash` | `.thumb` 对象 key 的脱敏 hash，用于确认审计的是哪个缩略图对象。 |
| `items[].thumbnail.object_key_prefix` | `.thumb` 对象 key 的目录前缀。正常情况下应与原图处于同一业务目录策略下。 |
| `items[].thumbnail_exists` | `.thumb` 是否存在。本次为候选的重点不是缺失，而是存在但与原图相同。 |
| `items[].needs_regeneration` | 是否需要重生成。`true` 表示 apply 会尝试写入新 `.thumb`；`false` 表示跳过。 |
| `items[].status` | 明细状态。`dry_run` 表示计划写入但本次未写；`skipped` 表示本条已符合策略或无需处理。 |
| `items[].reason` | 进入当前状态的原因。`thumbnail_copied_original` 表示缩略图是原图复制；`null` 通常表示跳过项没有异常原因。 |
| `items[].thumbnail_max_size_kb` | 该条审计使用的缩略图 KB 目标。本次为 `0`，表示不限制体积上限。 |
| `items[].display_max_size_kb` | 该条审计或重生成使用的详情展示图 KB 目标；默认 `768`，与缩略图目标独立。 |

当 `thumbnail_max_size_kb` 为正整数时，以下情况都会进入 `retry_candidates`：

- `.thumb` 缺失。
- `.thumb` 与原图同 size。
- `.thumb` 与原图 bytes 一致。
- `.thumb` 已存在但超过当前体积目标上限。

如果 `thumbnail_max_size_kb` 或 `display_max_size_kb` 不是预期值，先停止执行，检查管理后台系统设置、数据库连接和运行容器是否指向同一环境。

本次两份数据的缩略图结论是：`thumbnail_max_size_kb = 0`，所以并非按 KB 上限筛选；候选全部来自 `.thumb` 与原图同 size / 同 bytes。独立任务仍有 79 个待重生成候选，聚合任务当前批次有 55 个待重生成候选。

## 7. 聚合任务 tasks 字段解读

### 7.1 tasks 对象

| 字段 | 结果解读 |
|---|---|
| `tasks.sku_pending_formalization` | SKU 主图暂存目录正式化子任务。本次 `total = 0`，说明没有待正式化主图。 |
| `tasks.business_id_media_key_migration` | 业务对象 id 目录迁移子任务，覆盖用户头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件；用户头像业务对象 id 按字符串/UUID 目录处理。 |
| `tasks.certificate_image_key_migration` | 证书图片 key 迁移子任务。本次有 4 条证书记录，但全部是非支持图片类型，跳过迁移。 |
| `tasks.brand_logo_and_certificate_thumbnail_backfill` | SKU / Banner 自定义上传图 / 品牌 Logo / 证书图片缩略图回填子任务。本次聚合批次发现 55 个 copied-original 缩略图候选。 |
| `tasks.object_key_audit` | 对象 key 二次审计子任务。本次 40 条样本均未发现不规范 key 或对象缺失。 |

### 7.2 sku_pending_formalization 字段

| 字段 | 本次值 | 结果解读 |
|---|---:|---|
| `summary.total` | 0 | 没有进入 SKU 主图正式化审计的记录。 |
| `summary.success` | 0 | dry-run 且无候选，因此无成功写入。 |
| `summary.failed` | 0 | 无失败。 |
| `summary.missing_original` | 0 | 未发现待正式化原图缺失。 |
| `summary.missing_thumbnail` | 0 | 未发现待正式化缩略图缺失。 |
| `summary.target_exists` | 0 | 未发现目标正式 key 已存在冲突。 |
| `summary.thumbnail_max_size_kb` | 0 | 本子任务使用的缩略图 KB 目标为不限制。 |
| `summary.failure_reasons` | `{}` | 无失败原因。 |
| `items` | `[]` | 无明细，和 `total = 0` 一致。 |

### 7.3 business_id_media_key_migration 字段

| 字段 | 本次值 | 结果解读 |
|---|---:|---|
| `summary.total` | 0 | 没有进入业务对象 id 目录迁移审计的记录。 |
| `summary.candidates` | 0 | 没有需要从历史目录迁入业务对象 id 目录的候选；若大于 0，需按资源类型复核目标前缀。 |
| `summary.success` | 0 | dry-run 不实际写入；apply 后表示成功复制对象并更新数据库引用的数量。 |
| `summary.skipped` | 0 | 已符合业务对象 id 目录或不支持迁移的对象数量。 |
| `summary.failed` | 0 | 无失败；若大于 0，先看 `failure_reasons`。 |
| `summary.missing_original` | 0 | 未发现源对象缺失。 |
| `summary.target_exists` | 0 | 未发现目标 key 已存在；目标存在时可作为幂等重跑线索。 |
| `items[].source_type` | 示例为 `user_avatar`、`brand_logo`、`banner_image` 等 | 表示迁移来源。用户头像应迁入 `images/default/user-avatars/{user_id}/`，其中 `user_id` 可为 UUID 字符串；`avartars` 等错误拼写应在对象 key 审计中暴露为失败原因。 |
| `items[].business_id` | 示例为 UUID 或数字 ID | 业务对象 id 目录段；文档归档只记录脱敏前缀或摘要，不记录完整 object key。 |
| `items[].target.object_key_prefix` | 目标标准前缀 | 用于判断目标目录是否符合 `{prefix}/default/{business_media_type}/{business_object_id}`。 |

### 7.4 certificate_image_key_migration 字段

| 字段 | 本次值 | 结果解读 |
|---|---:|---|
| `summary.total` | 4 | 审计了 4 条证书文件记录。 |
| `summary.image_candidates` | 0 | 没有可迁移的图片类证书文件。 |
| `summary.document_skipped` | 4 | 4 条都被识别为非支持图片或文档类文件，按规则跳过。 |
| `summary.success` | 0 | dry-run 且无迁移候选，因此无成功写入。 |
| `summary.failed` | 0 | 无失败。 |
| `summary.missing_original` | 0 | 未发现源对象缺失。 |
| `summary.target_exists` | 0 | 未发现目标 key 已存在冲突。 |
| `summary.failure_reasons` | `{}` | 无失败原因。 |
| `items[].table` | `brand_certificates` | 明细来自品牌证书表。 |
| `items[].source_id` | 示例为 `2` 等证书记录 ID | 用于定位证书记录。 |
| `items[].source.object_key_hash` | 示例为 `e4a52161b6c4` | 源对象 key hash，只用于脱敏对照。 |
| `items[].source.object_key_prefix` | `files/default/brand-certificates` | 源对象仍在证书文件目录，但本次判定不是可迁移图片。 |
| `items[].target` | `null` | 未生成目标图片 key，因为该条不需要迁移。 |
| `items[].status` | `skipped` | 明细被跳过，没有写入计划。 |
| `items[].reason` | `not_supported_image` | 跳过原因是文件不是当前迁移任务支持的图片类型。 |

### 7.5 object_key_audit 字段

| 字段 | 本次值 | 结果解读 |
|---|---:|---|
| `summary.total` | 40 | 二次审计了 40 个对象引用。 |
| `summary.non_standard` | 0 | 未发现不规范对象 key。 |
| `summary.missing_objects` | 0 | 未发现数据库引用但对象存储缺失。 |
| `items[].source_type` | 示例为 `brand_logo` 等 | 表示被审计对象的业务来源。 |
| `items[].source_id` | 示例为 `2` 等记录 ID | 用于定位业务记录。 |
| `items[].object_key_hash` | 脱敏 hash | 用于对象 key 对照，不暴露真实 key。 |
| `items[].object_key_prefix` | 示例为 `images/default/brands/logos` | 用于判断对象是否落在预期前缀策略下。 |
| `items[].issue` | `null` | 没有发现 key 格式问题。 |
| `items[].object_exists` | `true` | 对象存储中可找到对应对象。 |

## 8. 子任务异常解读

| 子任务 | 异常字段 | 处理建议 |
|---|---|---|
| `sku_pending_formalization` | `missing_original` | 原图对象缺失，不应盲目 apply；先核对数据库记录与对象存储 |
| `sku_pending_formalization` | `target_exists` | 目标对象已存在，需确认是否为历史重跑或 key 冲突 |
| `business_id_media_key_migration` | `missing_original` | 源对象缺失，不应盲目更新数据库引用；先核对业务记录与对象存储 |
| `business_id_media_key_migration` | `target_exists` | 目标对象已存在，通常可作为幂等重跑线索，但仍需确认源/目标对象内容和业务记录 |
| `business_id_media_key_migration` | `invalid_business_id` 或类型转换异常 | 业务对象 id 口径与 schema 不一致；用户头像 `users.id` 是字符串/UUID，不能按整数 ID 处理 |
| `certificate_image_key_migration` | `missing_original` | `files/` 源对象不存在，先核对证书记录 |
| `certificate_image_key_migration` | `target_exists` | `images/` 目标已存在，确认是否可幂等跳过 |
| `brand_logo_and_certificate_thumbnail_backfill` | `failure_reasons` | 查看是否为对象缺失、读取失败、MIME 不支持或图片解码失败 |
| `object_key_audit` | `missing_objects` | 数据库仍引用不存在对象，需要单独人工核对 |
| `object_key_audit` | `non_standard` | key 仍不符合当前前缀策略，继续分批 apply 或人工处理 |

`items` 中对象 key 会脱敏，仅输出 `object_key_hash` 和 `object_key_prefix`。不要为了排障改维护任务输出真实 key；需要定位时应在受控生产 shell 或数据库中按 hash 对照。

## 9. 执行顺序建议

```text
1. 后台确认 thumbnail_max_size_kb。
2. 跑 `media-drift-reconcile` dry-run。
3. 读取顶层 summary 和各子任务 failure_reasons。
4. failed = 0 后确认 MySQL 与对象存储备份。
5. 按 --limit 100 分批 apply。
6. 每批 apply 后再跑 dry-run。
7. 当候选数下降到 0 或只剩明确需人工处理项时，记录验收结果。
8. 对管理端、小程序或店主端抽样访问 `/media/...thumb...`，补 render 证据。
```

## 10. 验收口径

维护任务本身只能证明 storage / key / object 侧结果，不能单独证明所有展示端渲染都通过。

| 验收项 | 通过条件 |
|---|---|
| key | `non_standard_keys_after_audit` 下降或归零，遗留项有人工解释 |
| object | `missing_objects` 和子任务 `failed` 为 0，或遗留项已登记 |
| URL | 抽样 `/media/{thumbnail_key}` 可受控读取 |
| thumbnail benefit | 新 `.thumb` 不是原图复制，体积/尺寸有收益；正整数目标下超过目标的历史缩略图会进入候选 |
| render | 管理端、小程序或店主端抽样页面能显示图片；维护任务输出中的 `render: blocked` 表示仍需人工或自动化补证 |

## 11. 回滚与停止条件

出现以下情况应停止 apply：

- `failed > 0` 且原因不是已知可忽略项。
- `thumbnail_max_size_kb` 与后台配置不一致。
- `environment.database_backend` 或 `object_storage_provider` 与预期生产环境不一致。
- dry-run 输出 `summary.status=blocked` 或 `failure_category=object_storage_unreachable`。
- apply 后 `non_standard_keys_after_audit` 或 `missing_objects` 异常增加。
- 对象存储写入、图片解码或数据库更新出现持续失败。

缩略图体积策略的快速回滚方式是将系统设置 `thumbnail_max_size_kb` 恢复为 `0`。已经重生成的历史 `.thumb` 如需恢复，只能依赖对象存储快照回滚或再次执行维护任务生成当前策略下的缩略图。
