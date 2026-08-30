---
purpose: 批量图片处理 Runbook
content: 记录图片转换、thumbnail/display 派生生成、缩略图重建、对象 key 迁移、生产执行、安全门禁和验收证据模板
source: REQ-0122-batch-image-processing-runbook / add-batch-image-processing-runbook
update_method: 媒体批处理脚本、生产维护入口、对象 key 迁移策略或版本 usage-docs 投影变化时更新
created_at: 2026-08-25 10:02:47
updated_at: 2026-08-29 22:18:26
---

# 批量图片处理 Runbook

## 1. 归属与投影

本文档是批量图片处理的长期事实源，归属 `docs/standards/batch-image-processing-runbook.md`。版本发布需要交付使用说明时，必须把本文档的关键执行步骤、安全门禁和验收模板投影到对应 `releases/vX.Y.Z/usage-docs/`，并在 manifest 或等价索引中记录来源、目标路径、适用版本和更新时间。

当前版本投影模板位于 `releases/templates/usage-docs/operations/batch-image-processing-runbook.mdx`。已发布且明确跳过 usage docs 的版本不得反向补写内容快照；后续具体版本生成 usage docs 时，应从模板或本文档投影到该版本目录。

## 2. 适用范围

本 Runbook 覆盖以下批量图片处理场景：

- 图片转换和派生生成：历史图片 `thumbnail` / `display` 补生成或重生成，`display` 读取详情展示图体积目标，`thumbnail` 读取缩略图体积目标。
- 缩略图专项重建：针对 SKU 商品图、品牌 Logo、品牌证书图片等同目录 `.thumb` 对象进行 dry-run、apply 和二次审计。
- 对象 key 迁移：SKU pending 主图正式化、所有媒体迁入业务对象 id 目录、图片类证书从 `files/` 迁移到 `images/`，以及对象 key 二次审计。
- 生产执行：通过生产 Compose 维护入口执行 dry-run、备份确认、显式 apply、分批处理和收尾验收。

非目标：

- 不在本文档中执行生产任务。
- 不把未实现或未验证脚本写成可直接生产 apply 的事实。
- 不改变 API、数据库、Web、管理端或小程序运行时契约。

## 3. 脚本清单

| 入口 | 状态 | 用途 | dry-run | apply | 生产入口 | 备注 |
|---|---|---|---|---|---|---|
| `python -m app.modules.media.maintenance backfill-image-variants` | 现有可用 | 审计或生成历史图片 `thumbnail` 与 `display` 派生对象 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... backfill-image-variants` | `display_max_size_kb` 默认 `768`，`thumbnail_max_size_kb` 读取 effective 配置。 |
| `python -m app.modules.media.maintenance backfill-brand-certificate-thumbnails` | 现有可用 | 审计或重建 SKU、品牌 Logo、品牌证书图片缩略图 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... backfill-brand-certificate-thumbnails` | 历史命令名保留；实际覆盖 SKU、品牌和证书图片。 |
| `python -m app.modules.media.maintenance formalize-pending-tile-images` | 现有可用 | 将公开 SKU 主图从 pending key 正式化到 SKU 目录 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... formalize-pending-tile-images` | 写对象存储和数据库引用。 |
| `python -m app.modules.media.maintenance migrate-business-id-media-keys` | 现有可用 | 将头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件迁入业务对象 id 目录 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... migrate-business-id-media-keys` | 只复制目标对象并更新引用；不默认删除旧对象。 |
| `python -m app.modules.media.maintenance migrate-certificate-image-keys` | 现有可用 | 将历史图片类证书从 `files/` 前缀迁移到 `images/` 前缀 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... migrate-certificate-image-keys` | PDF/文档证书继续保留 `files/` 前缀。 |
| `python -m app.modules.media.maintenance media-drift-reconcile` | 现有可用 | 聚合执行 SKU pending、业务 id 目录迁移、证书图片 key 迁移、缩略图回填和对象 key 审计 | 支持，默认 | 支持，需 `--apply --confirm-backup` | `deploy/scripts/media-maintenance.sh ... media-drift-reconcile` | 生产推荐聚合入口。 |
| `python -m app.modules.media.maintenance bug-0116-media-drift` | 历史兼容别名 | 等价调用 `media-drift-reconcile` | 支持，默认 | 支持，需 `--apply --confirm-backup` | 不作为推荐生产命令 | 仅用于兼容历史脚本、日志或旧文档引用。 |
| `python -m app.modules.media.maintenance object-key-audit` | 现有可用 | 只读审计非标准媒体对象 key 前缀 | 支持，只读 | 不支持 | `deploy/scripts/media-maintenance.sh ... object-key-audit` | 若传 `--apply` 应被阻断。 |
| `scripts/backfill-brand-certificate-thumbnails.py` | 兼容包装 | 调用后端缩略图重建入口 | 支持 | 使用 `--execute --confirm-backup` | 不推荐生产优先使用 | 生产优先使用 `deploy/scripts/media-maintenance.sh`。 |
| `scripts/migrate-pending-tile-images.py` | 兼容包装 | 调用 SKU pending 主图正式化入口 | 支持 | 使用 `--apply --confirm-backup` | 不推荐生产优先使用 | 输出中包含 target key 时，归档前必须脱敏。 |
| `scripts/migrate_object_keys.py` | 本地/历史迁移脚本 | 迁移 legacy object key 到语义布局 | 支持 `--dry-run` | 支持 `--apply` | 不作为默认生产入口 | 仅 SQLite 路径默认；生产执行需先评估 DB 后端和对象存储配置。 |
| 独立图片格式转换脚本 | 待实现 | 将原始图片批量转换为指定编码格式 | 不适用 | 不适用 | 不可生产执行 | 当前仓库未发现独立通用转换脚本；不得写生产 apply 命令。 |

## 4. 进度输出

`backfill-image-variants`、`backfill-brand-certificate-thumbnails` 和 `media-drift-reconcile` 支持可选 `--progress` 参数。启用后过程进度写入 stderr，最终 JSON 仍写入 stdout；未启用时继续只输出最终 JSON，兼容既有 `jq`、重定向和审计归档脚本。

生产执行建议同时保存 JSON 和进度日志：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100 --progress \
  > media-drift-reconcile-dry-run-$(date +%Y%m%d%H%M%S).json \
  2> media-drift-reconcile-progress-$(date +%Y%m%d%H%M%S).log
```

`media-drift-reconcile` 的进度总量按 5 个聚合阶段计算：`sku_pending_formalization`、`business_id_media_key_migration`、`certificate_image_key_migration`、`brand_logo_and_certificate_thumbnail_backfill` 和 `object_key_audit`。进度行只包含任务名、阶段、计数、百分比和枚举状态，不输出真实 object key、数据库连接串、对象存储 endpoint、密钥、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。

## 5. `thumbnail` / `display` 派生生成

执行目的：为历史图片生成或重生成轻量展示资源。列表、卡片、小 Logo 和推荐位优先消费 `thumbnail`；详情普通展示、Banner、图册普通浏览和受控分享图优先消费 `display`；高清预览、下载或保真查看才使用 `original`。

候选识别：

- 原图存在且属于支持图片 MIME。
- 缺少同目录 `thumbnail` 或 `display`。
- 既有派生对象与原图 bytes 相同、体积相同或超过对应目标。
- 对象存储不可达时整体标记 blocked，不进入 apply。

dry-run：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-image-variants --limit 100
```

apply：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-image-variants --limit 100 --apply --confirm-backup
```

执行要求：

- dry-run 只输出待处理数量、预计写入对象、跳过原因、失败分类和风险摘要，不写数据库或对象存储。
- apply 前必须确认 MySQL 快照和对象存储 bucket / prefix 快照。
- apply 必须可幂等复跑，已符合策略的派生对象应跳过。
- 输出只允许记录脱敏 key hash、标准前缀、provider、bucket hash、数量和失败分类。

## 6. 缩略图专项重建

执行目的：只聚焦历史 `.thumb` 对象，适用于品牌 Logo、证书图片、SKU 商品图、Banner 或其他进入缩略图矩阵的媒体类型。不得把原图 fallback 当作缩略图性能通过证据。

dry-run：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100
```

apply：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100 --apply --confirm-backup
```

验收重点：

- key：原图和 `.thumb` 位于同一业务目录或等价可追溯目录。
- object：原图和缩略图对象均存在，MIME、bytes 和尺寸可解释。
- URL：端侧使用后端受控 `/media/{object_key}`、受控签名 URL 或安全占位。
- render：管理端、店主 Web 或小程序按影响范围补截图、DevTools、真机或体验版 evidence；无法补齐时标记 blocked。
- benefit：缩略图相对原图具备 bytes、像素、加载耗时或等价收益；无收益时不得通过。

## 7. 对象 key 迁移

执行目的：修复历史对象 key 与标准前缀不一致的问题，确保图片资源使用 `images/`，文件资源使用 `files/`，SKU 公开主图不继续停留在 pending 目录，且头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件进入业务对象 id 目录。用户头像的业务对象 id 是 `users.id`，在 SQLite/MySQL 中为字符串/UUID 形态；迁移验收应按字符串 ID 段理解，不得按整数 ID 口径判断。

生产优先入口：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100 --progress
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos media-drift-reconcile --limit 100 --apply --confirm-backup --progress
```

专项入口：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos formalize-pending-tile-images --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos migrate-business-id-media-keys --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos migrate-certificate-image-keys --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos object-key-audit --limit 100
```

对象 key 迁移 apply 前必须记录：

- dry-run 摘要、候选数量、跳过数量、失败数量和 retry candidates。
- 旧 key 与新 key 的脱敏映射，至少包含 hash、标准前缀、业务资源类型和业务对象 id；用户头像目标前缀应体现 `images/default/user-avatars/{user_id}/`，并审计 `avartars` 等错误拼写。
- 聚合任务顶层 `business_id_media_candidates` 和 `tasks.business_id_media_key_migration.summary`，用于判断业务对象 id 目录迁移候选、失败分类、目标冲突和对象缺失。
- MySQL 快照位置或备份编号。
- 对象存储 bucket / prefix 快照位置或备份编号。
- 执行窗口、影响范围、回滚负责人和中止条件。

默认回滚：

- 恢复 MySQL 快照。
- 恢复对象存储 bucket / prefix 快照。
- 重新执行只读审计确认数据库引用和对象 key 前缀一致。

默认迁移不删除旧对象。旧对象清理必须在 key、object、URL、render 和幂等复跑验收完成后，另行通过受控清理脚本或人工清理流程执行。

未验证的反向脚本不得写作默认可靠回滚。若后续新增反向脚本，必须先有 OpenSpec Change、测试、dry-run/apply 证据和脱敏验收记录。

## 8. 生产执行步骤

1. 确认执行范围：任务名、limit、业务资源类型、目标环境、执行窗口。
2. 确认环境：生产 Compose、env 文件路径、数据库后端、对象存储 provider、bucket hash、`OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
3. 备份：完成 MySQL 快照和对象存储 bucket / prefix 快照。
4. dry-run：执行默认只读命令，保存脱敏 JSON 摘要。
5. 人工复核：确认 `failed=0`、对象存储未 blocked、预计写入量可接受、跳过原因可解释。
6. apply：显式追加 `--apply --confirm-backup`，按小批量 limit 分批执行。
7. 幂等复跑：使用相同或扩大 limit 再跑 dry-run，确认候选数量下降或为 0。
8. 二次审计：执行 `object-key-audit`、URL 抽样、端侧 render 抽样和收益对比。
9. 收尾：记录验收模板、失败清单、blocked 补证项、回滚判断和后续 Issue 建议。

## 9. 安全门禁

禁止写入长期文档、版本快照、日志归档或验收记录的内容：

- 真实 `.env` 内容、数据库连接串、对象存储 access key、secret key。
- Authorization header、Cookie、会话 token。
- 本机绝对路径、生产私有域名、真实客户数据。
- 未脱敏 object key 全量值、完整 SDK 堆栈或云厂商原始错误详情。

写入型任务阻断条件：

- 未完成 dry-run。
- 未确认 MySQL 快照或对象存储 bucket / prefix 快照。
- 对象存储不可达、bucket/region/权限不匹配或 summary 标记 blocked。
- dry-run 输出失败分类未解释。
- apply 未显式传入 `--apply --confirm-backup`。
- 删除对象或清理历史对象未单独确认。

## 10. 影响矩阵

| 维度 | 影响 | 说明 |
|---|---|---|
| API | 不涉及 | 本 Runbook 不新增或修改接口字段；若脚本实现改变响应 Schema，必须另行同步 OpenAPI 与 Orval。 |
| 数据库 | 不涉及结构 | 对象 key 迁移会写业务引用，但不新增表、字段或索引；生产执行前必须备份。 |
| Orval | 不涉及 | 无 API Schema 变化。 |
| Docker Compose | 关联执行 | 使用既有 `deploy/scripts/media-maintenance.sh` 和生产 Compose 维护 service；Runbook 不定义新的 Compose 行为。 |
| 对象存储 | 关联执行 | 写入或迁移对象必须走后端适配层和单桶标准前缀。 |
| Web 管理端 | 关联验收 | 上传状态机、同会话回显、列表/详情展示按影响范围记录 evidence。 |
| 店主 Web | 关联验收 | 公开商品、品牌、Banner、证书展示按影响范围抽样。 |
| 微信小程序 | 关联验收 | 需 DevTools、真机或体验版 evidence；缺证时标记 blocked。 |
| 管理端 | 关联验收 | 不新增管理端页面；只记录已有入口展示和上传链路验收。 |

## 11. 验收证据模板

### 11.1 dry-run 摘要

| 字段 | 填写要求 |
|---|---|
| task | 任务名，例如 `backfill-image-variants`。 |
| mode | 必须为 `dry_run` 或等价只读标识。 |
| environment | 记录 app env、database backend、object storage provider、bucket hash、auto create bucket 策略。 |
| total | 候选扫描数量。 |
| estimated_writes | 预计写入对象数量。 |
| skipped | 跳过数量和原因。 |
| failed | 失败数量和分类。 |
| retry_candidates | 可重试候选数量。 |
| business_id_media_candidates | `media-drift-reconcile` 中业务对象 id 目录迁移候选数量；大于 0 表示需在备份后评估 apply，不代表已经修复。 |
| blocked | 若对象存储不可达或环境异常，记录阻断原因和建议动作。 |

### 11.2 apply 与二次审计

| 维度 | 状态 | 证据 |
|---|---|---|
| key | pass/fail/blocked/n/a | 脱敏旧 key、新 key、标准前缀、业务资源类型和兼容结果。 |
| object | pass/fail/blocked/n/a | 对象存在性、MIME、bytes、权限、派生关系和失败对象清单。 |
| URL | pass/fail/blocked/n/a | `/media/{object_key}`、签名 URL、直出 URL 或 CDN URL 类型、HTTP 状态、缓存和 fallback。 |
| render | pass/fail/blocked/n/a | 管理端、店主 Web、小程序截图或 Network evidence；缺证写 blocked。 |
| benefit | pass/fail/blocked/n/a | `thumbnail` / `display` 相对原图的 bytes、像素、加载耗时或等价收益。 |
| idempotency | pass/fail/blocked/n/a | 同参数复跑是否跳过已处理对象，候选数量是否下降或归零。 |
| rollback | pass/fail/blocked/n/a | 快照恢复路径、是否需要回滚、回滚负责人和判断时间。 |

### 11.3 专项证据

缩略图专项重建：

```text
任务：
范围：
dry-run 摘要：
apply 摘要：
缩略图收益：
端侧 render：
blocked 补证项：
```

对象 key 迁移：

```text
任务：
旧 key 摘要：
新 key 摘要：
数据库引用：
对象存在性：
受控 URL：
端侧 render：
幂等复跑：
回滚判断：
失败清单：
```

## 12. 文档校验命令

- `openspec validate add-batch-image-processing-runbook --strict`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `python scripts/validate-doc-prose-hygiene.py docs/standards/batch-image-processing-runbook.md releases/templates/usage-docs/operations/batch-image-processing-runbook.mdx`
