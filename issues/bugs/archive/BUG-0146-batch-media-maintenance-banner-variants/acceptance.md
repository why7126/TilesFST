---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
acceptance_status: passed
created_at: 2026-08-29 19:10:08
updated_at: 2026-08-30 08:45:27
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
practice_ref: docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | `backfill-image-variants` dry-run 能识别历史 Banner 自定义上传图候选，并输出 `source_type: banner_image` | pass（本地等价环境 6 条 `banner_image`） |
| AC-002 | `backfill-image-variants` apply 能为 Banner 原图生成同目录 `.thumb.webp` 与 `.display.webp` | partial（生产 apply 扫描 6 条 `banner_image`，均已存在派生图并跳过；整批任务仍有非 Banner 失败） |
| AC-003 | 缩略图专项任务或 `media-drift-reconcile` 聚合任务能覆盖 Banner `.thumb.webp` 缺失候选 | pass（聚合任务子任务扫描到 `banner_image`） |
| AC-004 | apply 后幂等 dry-run 不再重复报告同一 Banner 派生图缺失 | pass（本地等价环境 `estimated_writes=0`、`banner_needs=0`） |
| AC-005 | Banner `.thumb.webp` / `.display.webp` 的 `/media` URL 返回 `Content-Type: image/webp`，不再出现 `x-media-fallback: 1` | passed（开发环境 alias apply 和本地 URL no-fallback 通过；生产公网验证后置到发布/运维窗口） |
| AC-006 | 小程序首页和品牌列表 Banner 有 Network/render evidence，确认普通展示不再加载原始大图 | passed（已补小程序 DevTools 截图，显示本地后端 `127.0.0.1:8000` 多条 `.thumb.webp` / `.display.webp` 请求为 200/webp） |
| AC-007 | 生产媒体维护 runbook 已更新 Banner 覆盖范围、生成格式、删除策略、dry-run 进入 apply 条件和 JSON 输出解析 | pass |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`  
小程序实践引用：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0146-batch-media-maintenance-banner-variants |
| 标题 | 批量媒体维护命令未覆盖 Banner 自定义上传图 |
| 严重等级 | high |
| 影响范围 | 小程序 / Web 管理端 / 后端维护命令 / 对象存储 / 媒体 URL |
| 复现入口 | 生产 Banner `.thumb.webp` / `.display.webp` URL、批量媒体维护 dry-run 输出 |
| 受影响端 | miniapp / admin / backend / storage |
| 环境 | prod / docker |
| 媒体类型 | image / banner / thumbnail / display |
| 业务资源 | 脱敏 Banner 自定义上传图，原图位于 `images/default/banners/` |
| 修复前实际结果 | Banner 派生图缺失时 `/media/...thumb.webp` fallback 到 PNG 原图，批量维护任务未报告 Banner 候选 |
| 修复后期望结果 | 批量维护命令补齐 Banner `.thumb.webp` 与 `.display.webp`，受控 URL 直接命中 WebP 派生对象 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | `logs/backfill-image-variants-local-dry-run.json` 显示本地等价环境包含 6 条 `source_type: banner_image`；`logs/media-drift-reconcile-local-dry-run.json` 的聚合子任务也扫描到 Banner 记录 | 若生产 dry-run 无 `source_type: banner_image` 或 key 前缀异常，回到维护任务候选 SQL 和 Banner 数据过滤条件排查 |
| object | partial | `logs/backfill-image-variants-local-dry-run.json` 显示本地等价环境 Banner 样本 `thumbnail_exists=true`、`display_exists=true`、`needs.thumbnail=false`、`needs.display=false`；`logs/backfill-image-variants-production-apply-20260830073333.json` 显示生产 apply 扫描 6 条 `banner_image`，全部 `skipped`，且 `thumbnail_exists=true`、`display_exists=true`、Banner 失败数为 0 | 整批生产 apply 仍有非 Banner `sku_image` 失败，需作为维护任务残留问题另行处理；若后续 Banner object 缺失、MIME 不符、0 字节或体积无收益，回到派生图生成和对象写入逻辑排查 |
| URL | passed | 本地等价环境 `logs/banner-thumb-local-curl.headers`、`logs/banner-display-local-curl.headers`、`logs/miniapp-home-banner-display-local-curl.headers`、`logs/miniapp-brand-banner-display-local-curl.headers` 均为 200、`Content-Type: image/webp`、`x-media-fallback: 0`；`logs/backfill-image-variants-local-alias-apply-20260830081739.json` 显示本地 alias apply 写入 12 个 Banner 旧无 id alias；生产公网历史无 id 路径复核仍为 PNG fallback，因当前无法在真正生产环境执行，转为发布/运维窗口后置验证 | 发布/运维窗口使用生产 MySQL/env 重新执行 `backfill-image-variants` dry-run/apply，确认 `environment.app_env`、`database_backend` 与生产一致，再对历史无 id URL 执行 `curl -I` |
| render | passed | `screenshots/miniapp-home-production-network-render-20260830.png` 显示小程序首页渲染成功，Network 中多条 `.thumb.webp` / `.display.webp` 请求为 200/webp；`screenshots/miniapp-home-local-banner-no-fallback-20260830.png` 显示本地后端 `127.0.0.1:8000` 返回 `Content-Type: image/webp`、`x-media-fallback: 0`；`screenshots/banner-management-production-network-20260829.png` 显示生产管理端 Banner 列表有渲染入口 | 生产公网/API 一致性作为发布/运维窗口后置验证，不阻塞本 Change 归档 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦历史批量维护命令漏扫 Banner，不直接修改上传入口；上传链路已有 `thumbnail_key` / `display_key` 参数证据 |
| 同会话即时回显 | n/a | 本 BUG 不直接修改 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | passed | 已补业务 id Banner 旧无 id alias 维护逻辑；本地 alias apply 和本地 URL no-fallback 通过，生产公网后置验证 |
| 历史对象与审计 | passed | 已记录本地等价环境 Banner 候选 dry-run、幂等 dry-run、URL headers、本地 alias apply 和生产前序 apply JSON；非 Banner 残留作为独立维护项，不阻塞 Banner 覆盖缺陷归档 |
| 小程序 evidence | passed | 已记录本地公开接口返回 Banner `.display.webp` URL，并验证对应 URL 返回 WebP 且无 fallback；已补小程序 DevTools 截图，显示本地后端 `.thumb.webp` / `.display.webp` 为 200/webp |

## 建议验证命令

修复实现后，建议按以下顺序验证：

```bash
uv run pytest src/backend/tests/test_media_maintenance.py tests/test_deploy_media_maintenance_script.py -q
```

生产 dry-run 示例：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-image-variants --limit 100 \
  > backfill-image-variants-dry-run-$(date +%Y%m%d%H%M%S).json
```

生产 apply 示例：

```bash
docker-compose --project-name tilesfst \
  --env-file .env \
  -f docker-compose.prod.external.yml \
  exec -T tilesfst-backend \
  uv run --no-sync python -m app.modules.media.maintenance backfill-image-variants --limit 100 --apply --confirm-backup \
  > backfill-image-variants-apply-$(date +%Y%m%d%H%M%S).json
```

URL 验证示例：

```bash
curl -I 'https://tilesfst.wjoyhappy.site/media/images/default/banners/<uuid>.thumb.webp'
curl -I 'https://tilesfst.wjoyhappy.site/media/images/default/banners/<uuid>.display.webp'
```

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-30 08:36:05
accepted_by: workflow-sync
source_change: fix-media-maintenance-banner-variants
source_sprint: sprint-027
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

