---
purpose: 生产媒体维护作业 Runbook
content: 记录媒体漂移聚合任务、缩略图重新生成任务的执行命令、处理过程、结果解读和验收口径
source: REQ-0099-global-thumbnail-size-limit / BUG-0116-prod-media-historical-object-drift 运维沉淀
update_method: 媒体维护任务、生产 Compose 入口或对象存储验收口径变化时更新
created_at: 2026-08-05 23:16:00
updated_at: 2026-08-06 09:54:23
---

# 生产媒体维护作业 Runbook

## 1. 适用范围

本文档用于生产或生产等价环境中的媒体历史维护任务，覆盖：

- BUG-0116 媒体漂移聚合任务：SKU 主图暂存路径正式化、证书图片 key 迁移、SKU / 品牌 Logo / 证书图片缩略图回填和对象 key 二次审计。
- 历史缩略图重新生成任务：让历史 SKU、品牌 Logo 与品牌证书图片 `.thumb` 读取当前 `media.thumbnail_max_size_kb` effective 策略。
- 运维 dry-run、备份确认、apply、二次审计和结果解读。

保存系统设置中的“缩略图体积目标上限 (KB)”只影响后续新生成缩略图，不会自动扫描或覆盖历史 `.thumb` 对象。历史资源要应用新策略，必须显式执行本文档中的维护任务。

## 2. 执行前检查

执行 apply 前必须完成：

- MySQL 快照或等价数据库备份。
- 对象存储 bucket / prefix 快照，至少覆盖 `images/`、`files/` 和相关 `.thumb` 对象。
- 确认生产 `.env` 指向预期数据库与对象存储。
- 先跑 dry-run，并确认输出中 `environment.database_backend`、`environment.object_storage_provider` 和 `environment.object_storage_bucket_hash` 符合预期。
- 确认 `thumbnail_max_size_kb` 为预期值；`0` 表示不限制，正整数表示尽量不超过目标 KB。

## 3. 生产命令

当前生产环境如只能通过根目录兼容 Compose 入口进入后端容器，使用以下命令。

### 3.1 媒体漂移聚合任务 dry-run

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance bug-0116-media-drift --limit 100
```

### 3.2 媒体漂移聚合任务 apply

仅在 dry-run 无阻断失败且已确认备份后执行：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance bug-0116-media-drift --limit 100 --apply --confirm-backup
```

### 3.3 缩略图重新生成任务 dry-run

只想聚焦历史 SKU、品牌 Logo 与品牌证书图片 `.thumb` 时，执行独立缩略图任务。任务名保留为 `backfill-brand-certificate-thumbnails` 是为了兼容既有生产命令；实际处理范围包含 SKU、品牌和证书图片：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-brand-certificate-thumbnails --limit 100
```

### 3.4 缩略图重新生成任务 apply

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-brand-certificate-thumbnails --limit 100 --apply --confirm-backup
```

### 3.5 deploy 包装入口

若生产环境已使用 `deploy/` 入口，优先使用包装脚本：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos bug-0116-media-drift --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos bug-0116-media-drift --limit 100 --apply --confirm-backup
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100 --apply --confirm-backup
```

## 4. 聚合任务处理过程

`bug-0116-media-drift` 是聚合入口，单次执行会运行 4 个子任务：

| 子任务 | 作用 | 是否写入 |
|---|---|---|
| `sku_pending_formalization` | 将公开 SKU 主图从暂存目录正式化到 SKU 目录，并同步缩略图 | apply 时写对象存储和数据库 |
| `certificate_image_key_migration` | 将图片类证书从 `files/` 前缀迁移到 `images/` 前缀 | apply 时写对象存储和数据库 |
| `brand_logo_and_certificate_thumbnail_backfill` | 审计或重生成 SKU、品牌 Logo 与品牌证书图片同目录 `.thumb` | apply 时写对象存储 |
| `object_key_audit` | 二次审计品牌 Logo / 证书对象 key 是否仍不规范 | 始终只读 |

`--limit 100` 是分别传给每个子任务的限制，不是聚合任务全局最多处理 100 条。因此聚合输出中的总样本数可能超过 100。

## 5. 顶层结果解读

输出是 JSON，先看顶层字段。顶层字段在聚合任务和独立缩略图任务中都存在；聚合任务的各子任务结果位于 `tasks.*`，独立任务的同类结果直接位于顶层。

### 5.1 通用顶层字段

| 字段 | 结果解读 |
|---|---|
| `task` | 当前输出所属任务名。`bug-0116-media-drift` 表示聚合任务；`backfill-brand-certificate-thumbnails` 表示独立缩略图任务。 |
| `mode` | 执行模式。`dry_run` 只审计和预估，不写数据库或对象存储；`apply` 才会执行写入。 |
| `dry_run` | 布尔值形式的写入开关。`true` 与 `mode: dry_run` 一致，表示本次结果只能作为计划和风险判断，不能当作已经修复完成。 |
| `limit` | 本次单任务或每个聚合子任务的处理上限。聚合任务里不是全局上限，因此多个子任务样本相加可能超过该值。 |
| `summary` | 当前任务的汇总结论。聚合任务顶层 `summary` 是四个子任务的归纳；独立缩略图任务顶层 `summary` 是缩略图审计结论。 |
| `tasks` | 仅聚合任务存在，记录四个子任务的完整输出。排障时应先看顶层 `summary`，再进入对应 `tasks.*.summary` 和 `tasks.*.items`。 |
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
| `acceptance_summary.task` | `bug-0116-media-drift` / `backfill-brand-certificate-thumbnails` | 标识这份验收摘要对应的任务，归档证据时要和 JSON 文件名、执行命令对应。 |
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
| `summary.task_count` | 4 | 聚合任务已运行 4 个子任务：SKU 主图正式化、证书图片 key 迁移、缩略图回填、对象 key 审计。 |
| `summary.failed` | 0 | 聚合层未发现失败项；可进入备份确认和分批 apply 判断。 |
| `summary.retry_candidates` | 55 | 当前聚合 dry-run 发现 55 个需要重生成或重试的缩略图候选。 |
| `summary.pending_main_images` | 0 | 没有公开 SKU 主图仍停留在暂存目录，本批无需主图正式化。 |
| `summary.certificate_file_image_candidates` | 0 | 没有图片类证书仍需要从 `files/` 迁移到 `images/`。 |
| `summary.thumbnail_candidates` | 55 | 本批真正待处理的是 55 个缩略图候选，主要来自 copied-original 缩略图。 |
| `summary.non_standard_keys_after_audit` | 0 | 二次审计未发现遗留不规范 key；key 漂移侧当前通过。 |

推荐判断：

```text
failed = 0 且 retry_candidates > 0
→ dry-run 已找到可处理对象，可在备份后分批 apply。

failed > 0
→ 不要 apply，先看 tasks.*.summary.failure_reasons 与 items。

pending_main_images = 0 且 certificate_file_image_candidates = 0 且 thumbnail_candidates = 0 且 non_standard_keys_after_audit = 0
→ 本批次没有发现需要处理的历史漂移。
```

本次 `bug-0116-media-drift` 的结论是：无失败、无 SKU 主图暂存漂移、无证书图片 key 迁移候选、对象 key 审计通过，但仍有 55 个缩略图候选需要在备份后 apply。

## 6. 缩略图任务结果解读

缩略图子任务为 `tasks.brand_logo_and_certificate_thumbnail_backfill`，独立任务输出时位于顶层 `summary`。该任务虽然沿用历史命令名 `backfill-brand-certificate-thumbnails`，但处理范围包含 SKU、品牌和证书图片。

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
| `thumbnail_max_size_kb` | 0 | 0 | 当前生效策略是不限制目标 KB；本次候选来自 copied-original，而不是超过 KB 上限。 |

### 6.2 items 每字段结果解读

| 字段 | 结果解读 |
|---|---|
| `items[].source_type` | 来源类型。`sku_image` 为 SKU 主图，`brand_logo` 为品牌 Logo，`certificate_file` 为证书文件引用，`certificate_image` 为图片类证书引用。 |
| `items[].source_id` | 来源表记录 ID，用于在受控生产环境中定位业务记录。文档或日志归档时不应补充真实对象 key。 |
| `items[].object_key_hash` | 原图对象 key 的脱敏 hash，用于排障对照；不是可直接访问的对象 key。 |
| `items[].object_key_prefix` | 原图对象 key 的目录前缀。本次样本包含 `images/default/tiles/...`、`images/default/brands/logos`、证书相关前缀等。 |
| `items[].thumbnail.object_key_hash` | `.thumb` 对象 key 的脱敏 hash，用于确认审计的是哪个缩略图对象。 |
| `items[].thumbnail.object_key_prefix` | `.thumb` 对象 key 的目录前缀。正常情况下应与原图处于同一业务目录策略下。 |
| `items[].thumbnail_exists` | `.thumb` 是否存在。本次为候选的重点不是缺失，而是存在但与原图相同。 |
| `items[].needs_regeneration` | 是否需要重生成。`true` 表示 apply 会尝试写入新 `.thumb`；`false` 表示跳过。 |
| `items[].status` | 明细状态。`dry_run` 表示计划写入但本次未写；`skipped` 表示本条已符合策略或无需处理。 |
| `items[].reason` | 进入当前状态的原因。`thumbnail_copied_original` 表示缩略图是原图复制；`null` 通常表示跳过项没有异常原因。 |
| `items[].thumbnail_max_size_kb` | 该条审计使用的缩略图 KB 目标。本次为 `0`，表示不限制体积上限。 |

当 `thumbnail_max_size_kb` 为正整数时，以下情况都会进入 `retry_candidates`：

- `.thumb` 缺失。
- `.thumb` 与原图同 size。
- `.thumb` 与原图 bytes 一致。
- `.thumb` 已存在但超过当前体积目标上限。

如果 `thumbnail_max_size_kb` 不是预期值，先停止执行，检查管理后台系统设置、数据库连接和运行容器是否指向同一环境。

本次两份数据的缩略图结论是：`thumbnail_max_size_kb = 0`，所以并非按 KB 上限筛选；候选全部来自 `.thumb` 与原图同 size / 同 bytes。独立任务仍有 79 个待重生成候选，聚合任务当前批次有 55 个待重生成候选。

## 7. 聚合任务 tasks 字段解读

### 7.1 tasks 对象

| 字段 | 结果解读 |
|---|---|
| `tasks.sku_pending_formalization` | SKU 主图暂存目录正式化子任务。本次 `total = 0`，说明没有待正式化主图。 |
| `tasks.certificate_image_key_migration` | 证书图片 key 迁移子任务。本次有 4 条证书记录，但全部是非支持图片类型，跳过迁移。 |
| `tasks.brand_logo_and_certificate_thumbnail_backfill` | SKU / 品牌 Logo / 证书图片缩略图回填子任务。本次聚合批次发现 55 个 copied-original 缩略图候选。 |
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

### 7.3 certificate_image_key_migration 字段

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

### 7.4 object_key_audit 字段

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
| `certificate_image_key_migration` | `missing_original` | `files/` 源对象不存在，先核对证书记录 |
| `certificate_image_key_migration` | `target_exists` | `images/` 目标已存在，确认是否可幂等跳过 |
| `brand_logo_and_certificate_thumbnail_backfill` | `failure_reasons` | 查看是否为对象缺失、读取失败、MIME 不支持或图片解码失败 |
| `object_key_audit` | `missing_objects` | 数据库仍引用不存在对象，需要单独人工核对 |
| `object_key_audit` | `non_standard` | key 仍不符合当前前缀策略，继续分批 apply 或人工处理 |

`items` 中对象 key 会脱敏，仅输出 `object_key_hash` 和 `object_key_prefix`。不要为了排障改维护任务输出真实 key；需要定位时应在受控生产 shell 或数据库中按 hash 对照。

## 9. 执行顺序建议

```text
1. 后台确认 thumbnail_max_size_kb。
2. 跑 bug-0116-media-drift dry-run。
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
- apply 后 `non_standard_keys_after_audit` 或 `missing_objects` 异常增加。
- 对象存储写入、图片解码或数据库更新出现持续失败。

缩略图体积策略的快速回滚方式是将系统设置 `thumbnail_max_size_kb` 恢复为 `0`。已经重生成的历史 `.thumb` 如需恢复，只能依赖对象存储快照回滚或再次执行维护任务生成当前策略下的缩略图。
