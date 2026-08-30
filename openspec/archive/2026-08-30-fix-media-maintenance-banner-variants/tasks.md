## 1. 后端维护任务

- [x] 1.1 在媒体维护候选来源中加入 Banner 自定义上传图，来源类型使用 `banner_image` 或等价稳定枚举。
- [x] 1.2 限定 Banner 候选范围，优先覆盖 `image_source = 'custom_upload'` 或 `images/default/banners/` 标准目录，避免重复处理 SKU/品牌引用图。
- [x] 1.3 确保 `backfill-image-variants` 能为 Banner 生成 `.thumb.webp` 与 `.display.webp`。
- [x] 1.4 确保缩略图专项任务能覆盖 Banner `.thumb.webp` 缺失候选，或将任务命名/描述调整为真实覆盖范围。
- [x] 1.5 确保 `media-drift-reconcile` 聚合任务汇总 Banner 缩略图候选，不把 Banner 缺失派生图遗漏为 0。
- [x] 1.6 保持 dry-run 不写数据库、不写对象存储、不删除对象；apply 继续要求 `--apply --confirm-backup`。
- [x] 1.7 保持输出脱敏，不输出真实 object key、bucket、endpoint、密钥、连接串、Authorization header、Cookie、`.env` 内容或本机绝对路径。
- [x] 1.8 对已迁入 `images/default/banners/{banner_id}/` 的 Banner，在 `backfill-image-variants` 中补充旧无 id URL `.thumb.webp` / `.display.webp` alias 审计和生成，避免历史 URL fallback 到原图。

## 2. 文档

- [x] 2.1 更新 `docs/standards/production-media-maintenance-runbook.md`，明确三个批量命令覆盖 Banner 自定义上传图。
- [x] 2.2 在 Runbook 中补充 Banner 生成格式：`.thumb.webp` 与 `.display.webp`，原图格式保留。
- [x] 2.3 在 Runbook 中补充历史数据删除策略：不删除原图，不删除已有合格派生图，只写入缺失或不合格派生图。
- [x] 2.4 在 Runbook 中补充 Banner dry-run 进入 apply 条件、apply 正常判断、幂等复核和 `curl -I` 验证点。

## 3. 测试

- [x] 3.1 补充 `_thumbnail_source_rows()` 测试，确认返回 `banner_image` 来源。
- [x] 3.2 补充 Banner 候选过滤测试，避免非自定义上传或非 Banner 目录对象造成重复处理。
- [x] 3.3 补充 `backfill-image-variants` 测试，确认 Banner 缺失 `thumbnail` 与 `display` 时产生正确统计。
- [x] 3.4 补充 `media-drift-reconcile` 或缩略图专项回归测试，确认聚合摘要覆盖 Banner 候选。
- [x] 3.5 补充或更新脱敏测试，确认新增 Banner 来源不会输出 raw object key 或敏感环境信息。
- [x] 3.6 补充业务 id Banner 已有 canonical WebP、旧无 id alias 缺失时的回归测试。

## 4. 验证

- [x] 4.1 运行 `uv run pytest src/backend/tests/test_media_maintenance.py tests/test_deploy_media_maintenance_script.py -q`。
- [x] 4.2 运行 OpenSpec 严格校验和语言校验。
- [x] 4.3 记录生产或等价环境 `backfill-image-variants` dry-run JSON 摘要，确认包含 Banner 候选。
- [x] 4.4 记录 apply JSON 摘要，确认生产 Banner 派生图已存在或写入成功，且 Banner 维度失败数为 0；整批任务仍有非 Banner 失败需另行跟进。
- [x] 4.5 记录 apply 后幂等 dry-run 摘要，确认同一 Banner 不再作为缺失派生图候选。
- [x] 4.6 记录 `curl -I` 摘要，确认 Banner `.thumb.webp` / `.display.webp` 返回 `Content-Type: image/webp` 且不再出现 `x-media-fallback: 1`；开发环境已验证通过，生产公网因当前无生产执行条件后置到发布/运维窗口补证。
- [x] 4.7 回填 BUG acceptance，补充 Web 管理端或小程序 Banner Network/render evidence。
- [x] 4.8 若生产影响具备事故沉淀价值，归档前补充 `docs/knowledge-base/incidents/` 经验记录；否则在归档说明中标记 N/A。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-29 21:13:47 | 本地 `media-drift-reconcile` 在 `business_id_media_key_migration` 阶段查询 `tile_videos.mime_type`，但 SQLite/MySQL schema 均无该列，导致 dry-run 失败。 | 将 `tile_videos` 候选查询中的 `mime_type` 改为 `NULL AS mime_type`，保持视频对象按 object key 迁移，不新增数据库字段；同步测试夹具为真实 schema，并更新 5 阶段聚合测试预期。 | `uv run pytest src/backend/tests/test_media_maintenance.py tests/test_deploy_media_maintenance_script.py -q` 通过，30 passed。 |
| 2026-08-29 23:23:55 | 回填本地 dry-run、curl、miniapp API 证据；用户补充生产管理端 Banner Network 截图。 | 将 BUG acceptance 更新为 partial：本地等价环境已证明 Banner 候选扫描、幂等 dry-run 和本地 URL no-fallback；生产 apply JSON 与生产端 render/no-fallback 仍未闭环。 | `logs/backfill-image-variants-local-dry-run.json` 显示 `banner_items=6`、`banner_needs=0`；本地 curl headers 为 `Content-Type: image/webp`、`x-media-fallback: 0`；生产截图已归档到 `screenshots/banner-management-production-network-20260829.png`。4.4 与 4.7 保持未完成。 |
| 2026-08-30 07:39:12 | 用户补充生产 `backfill-image-variants` apply JSON。 | 归档生产 apply JSON 到 BUG logs，并回填验收：生产 apply 扫描 6 条 `banner_image`，均显示 thumb/display 已存在并跳过，Banner 维度失败数为 0；整批任务有非 Banner `sku_image` 失败，不能宣称全任务正常。 | `logs/backfill-image-variants-production-apply-20260830073333.json` 显示 `total=691`、`success=1`、`failed=2`、`skipped=689`、`banner_items=6`、`banner_failed=0`。4.7 仍保持未完成。 |
| 2026-08-30 07:46:42 | 用户补充生产小程序 DevTools 截图。 | 归档小程序首页截图并回填 4.7；同时复核生产历史无 id Banner URL，发现 `.thumb.webp` / `.display.webp` 仍 fallback 到 PNG 原图，故 4.6 退回未完成。 | `screenshots/miniapp-home-production-network-render-20260830.png` 显示小程序页面有 `.thumb.webp` / `.display.webp` 200/webp 请求；`logs/production-banner-thumb-673dd7ed-legacy-path-curl.headers` 与 `logs/production-banner-display-673dd7ed-legacy-path-curl.headers` 显示历史无 id 路径仍 `Content-Type: image/png`、`x-media-fallback: 1`。 |
| 2026-08-30 08:10:01 | 生产历史无 id Banner URL 仍 fallback，需确认是否兼容旧路径或修正生产接口 URL 字段为空。 | 在 `backfill-image-variants` 中对已迁入 `images/default/banners/{banner_id}/` 的 Banner 增加旧无 id `.thumb.webp` / `.display.webp` alias 审计与 apply 生成；优先复制 canonical WebP，缺失时从原图生成，不改写 `banners.image_object_key`，不删除历史对象。 | `uv run pytest src/backend/tests/test_media_maintenance.py tests/test_deploy_media_maintenance_script.py -q` 通过，33 passed；生产 4.6 仍需部署后重新执行 dry-run/apply 与 `curl -I` 补证。 |
| 2026-08-30 08:22:53 | 用户补充 `backfill-image-variants-apply-20260830081739.json` 与小程序 DevTools 截图。 | 归档为本地 alias apply / 本地 no-fallback 证据；解析确认该 JSON 为 `development` + `sqlite` 环境，不能作为生产 MySQL 证据；同步保存生产公网 curl 复核结果。 | 本地 alias apply 写入 12 个 Banner 旧无 id alias，截图中 `127.0.0.1:8000` 返回 `Content-Type: image/webp`、`x-media-fallback: 0`；生产公网历史无 id thumb/display URL 在 2026-08-30 08:23 仍返回 `Content-Type: image/png`、`x-media-fallback: 1`。 |

## 归档前剩余阻塞

- 生产后置验证：生产历史无 id Banner `.thumb.webp` / `.display.webp` URL 当前仍 fallback 到 PNG 原图，`x-media-fallback=1`；开发环境 alias apply 已证明逻辑可执行。因当前无法在真正生产环境执行，生产 MySQL/env apply 与公网 no-fallback curl 作为发布/运维窗口验证项处理，不阻塞本 Change 归档。
- 证据冲突：生产公开小程序 API curl 返回自定义 Banner URL 字段为空，但用户补充的小程序 DevTools 截图显示页面实际加载 `.webp` 图片；需确认是否存在缓存、环境差异或接口字段兼容问题。
- 生产维护残留：`backfill-image-variants-production-apply-20260830073333.json` 中整批任务仍有非 Banner `sku_image` 失败，`summary.failed=2`、`retry_candidates=2`、`failure_reasons.OSError=2`，需作为独立维护残留跟进。
- 4.8：本次暂不新增事故沉淀文档；原因是该 BUG 当前仍处于验收中，生产闭环完成后若仍有复用价值，再通过知识沉淀流程补充。
