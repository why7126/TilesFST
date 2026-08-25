---
change_id: add-webp-derived-image-variants
source_requirement: REQ-0120-webp-derived-image-variants
status: applied
lifecycle_stage: change
created_at: 2026-08-22 22:09:00
updated_at: 2026-08-25 14:18:06
---

# Change 追踪

## 基本信息

```yaml
change_id: add-webp-derived-image-variants
source_requirement: REQ-0120-webp-derived-image-variants
source_sprint: sprint-025
status: applied
change_type: update
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: false
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - media-multi-variant-images
    - object-storage
    - prod-media-maintenance-jobs
readiness: ready
prototype_gate:
  has_prototype_context: true
  has_html: false
  has_png: false
  ui_contract_required: true
  conflict_result: 无 HTML/PNG 冲突；context 仅约束既有入口的端侧消费与验收策略。
tasks_total: 31
tasks_completed: 31
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| 评审状态 | pass：REQ 状态为 `in_sprint`，已完成 `/req-review` 并纳入 `sprint-025`。 |
| 文档齐备 | pass：`requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md`、`prototype/web/context.md` 齐备。 |
| Readiness | ready：原 REQ 标记 `Partially Ready` 仅因不新增独立 UI 原型，OpenSpec 已通过 UI Contract 消化。 |
| Sprint Inclusion | pass：REQ 已在 `iterations/archive/sprint-025/sprint.yaml` 正式范围内。 |

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: false
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - media-multi-variant-images
    - object-storage
    - prod-media-maintenance-jobs
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-25 14:18:06 | `/opsx-modify` | 补充用户提供的 Docker Web `localhost:3000` SKU 图片上传与 `display.webp` 展示截图证据：上传接口返回 `200 OK` / `code: 0`，原图保留 PNG，派生 URL 为 `.thumb.webp` / `.display.webp`，SKU 编辑弹窗即时回显，`display.webp` GET 返回 `200`。 |
| 2026-08-25 12:03:34 | evidence-update | 补充用户提供的小程序微信开发者工具截图证据：品牌页渲染可见，`.display.webp` 请求返回 `200 OK`，`content-length: 13126`；未写入本机临时截图路径。 |
| 2026-08-22 22:25:05 | `/opsx-apply` | 实现 JPEG/PNG/WebP 上传统一生成 WebP `thumbnail` / `display` 派生图；原图格式与 MIME 保持不变；PDF 无派生 URL；历史 `.thumb.jpg` / `.display.jpg` 与新 `.thumb.webp` / `.display.webp` 缺失均保留受控 fallback。 |
| 2026-08-22 22:09:00 | `/req-opsx` | 基于 REQ-0120 创建 OpenSpec Change，生成 proposal、design、delta specs、tasks 与 trace。 |

## 实现证据

| 维度 | 状态 | 证据 |
|---|---|---|
| backend | pass | `src/backend/app/modules/media/storage.py` 固定派生图输出 WebP，key 使用 `.thumb.webp` / `.display.webp`，写入 `image/webp`，派生失败不阻断原图上传。 |
| upload API | pass | `src/backend/app/api/v1/uploads.py` 在无派生 key 时返回 `thumbnail_url/display_url = null`，PDF 证书文件不再返回图片派生 URL。 |
| object storage | pass | 同目录派生 key 可由原图 key 推导；历史 `.thumb.jpg` / `.display.jpg` fallback 保留，新 `.thumb.webp` 缺失时可尝试回退常见原图扩展。 |
| maintenance | pass | `src/backend/app/modules/media/maintenance.py` 对 WebP 派生图执行 dry-run/apply/幂等检查，并把非 `image/webp` 派生对象视为待重建。 |
| web/admin/miniapp | pass | 端侧字段结构未变，既有 `thumbnail_url`、`display_url`、`original_url` 消费逻辑继续复用；本次未改 Web UI 样式。 |
| database | n/a | 未新增字段或迁移，派生 key 继续由原图 key 推导。 |
| OpenAPI/Orval | n/a | 响应字段未增删改名，Schema 未变化；无需重新生成 Orval。 |

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-22 22:24:00 | `uv run python -m pytest ../../tests/test_media_storage.py tests/test_media_thumbnail_generation.py tests/test_media_maintenance.py ../../tests/test_migrate_pending_tile_images.py ../../tests/test_audit_miniapp_card_images.py tests/test_admin_banners.py tests/test_admin_brands.py tests/test_admin_tile_skus.py ../../tests/integration/api/test_admin_brand_certificates.py` | pass：136 passed，4 warnings。 |

## 媒体验收摘要

| 维度 | 状态 | 证据 |
|---|---|---|
| key | pass | 自动化测试覆盖 `.thumb.webp` / `.display.webp` key 推导、直出 URL 推导和历史 fallback。 |
| object | pass | 自动化测试覆盖 JPEG/PNG/WebP 输入生成 WebP 内容，派生对象 Content-Type 为 `image/webp`。 |
| URL | pass | 自动化测试覆盖 `/media` 受控 URL、direct URL、PDF 无派生 URL、缺失派生回退原图。 |
| render | pass | 小程序微信开发者工具截图已补：品牌页可见卡片渲染，`.display.webp` 返回 `200 OK`；Docker Web `http://localhost:3000` SKU 编辑弹窗截图已补，上传后商品图片即时回显并请求 `.display.webp`。 |
| benefit | pass | 自动化测试覆盖缩略图/展示图小于原图；Docker Web SKU 样本原图约 `1189508` bytes，`display.webp` 传输约 `26.96 kB`。 |

## 小程序媒体四联

| 维度 | 状态 | 证据 |
|---|---|---|
| key | pass | 后端响应与 helper 继续提供 `thumbnail_url`、`display_url`、`original_url`；派生 key 为 `.webp`。 |
| object | pass | 单元/集成测试覆盖对象存在、MIME 与 bytes。 |
| URL | pass | 自动化测试覆盖受控 URL 与 fallback；微信开发者工具截图显示本地后端 `/media/...display.webp` 请求返回 `200 OK`。 |
| render | pass | 用户提供微信开发者工具截图：品牌页/品牌 Tab 可见品牌卡片渲染，Network 面板过滤 `.webp` 后存在多条 `.thumb.webp` / `.display.webp` 请求。 |

Network evidence:

- source: 用户提供微信开发者工具截图，2026-08-25 12:02
- page_path: 品牌页 / 品牌 Tab
- media_kind: brand logo thumbnail/display
- media_url_type: `/media/images/default/brands/logos/<object-key-hash>.display.webp` and `.thumb.webp`
- request_domain: `127.0.0.1:8000`
- http_status: `200 OK`
- business_status: pass
- resource_bytes: `content-length: 13126` for selected `display.webp`
- duration_ms: n/a
- render_result: pass
- blocker_or_follow_up: 小程序截图证据已补；Docker Web `http://localhost:3000` 上传边界证据已由 SKU 图片上传与 `display.webp` 展示截图补齐。

## Docker Web 上传边界证据

- source: 用户提供 Docker Web Network 与 SKU 编辑弹窗截图，2026-08-25
- page_path: 管理端 SKU 编辑弹窗 / 商品图片
- upload_request: `POST http://localhost:3000/api/v1/admin/uploads/tile-images`
- upload_status: `200 OK`
- business_status: `code=0`, `message=success`
- original: `/media/images/default/tiles/pending/<object-key-hash>.png`, `mime_type=image/png`, `size=1189508`
- derived_urls: `/media/images/default/tiles/pending/<object-key-hash>.thumb.webp`, `/media/images/default/tiles/pending/<object-key-hash>.display.webp`
- render_request: `GET http://localhost:3000/media/images/default/tiles/pending/<object-key-hash>.display.webp`
- render_status: `200`
- resource_bytes: `display.webp` Network transfer about `26.96 kB`
- render_result: pass：SKU 编辑弹窗商品图片即时回显，未通过后端 `:8000` 直连作为唯一证据。

## 规范沉淀

本次已更新 `rules/media.md`、`rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`data/README.md`。暂不新增独立 best-practice 文档；当前规则已能承载 WebP 派生 key/MIME 一致性要求。
