---
change_id: add-brand-certificate-image-thumbnails
status: archived
type: add
source_requirement: REQ-0092-brand-certificate-image-thumbnails
created_at: 2026-08-02 18:07:10
updated_at: 2026-08-02 19:21:07
owner: product
iteration: sprint-017
---

# Change Trace

## 来源

- REQ: `issues/requirements/archive/REQ-0092-brand-certificate-image-thumbnails/`
- Source BUG: `BUG-0101-thumbnail-optimization-size-regression`
- 相关需求：`REQ-0005-brand-management`、`REQ-0038-brand-certificate-management`

## Requirement Readiness Report

| 项 | 结论 | 说明 |
|---|---|---|
| review gate | Pass | REQ `status: approved`，允许 `/req-opsx`。 |
| readiness | Ready | requirement、user-stories、business-flow、acceptance、trace、review、prototype/web 齐全。 |
| knowledge-base gate | Pass | 已转化 admin-list、admin-modal、media-upload 横切 AC。 |
| prototype | Ready | HTML + context 已有；PNG Golden Reference 后续设计阶段导出。 |

## Impact

```yaml
backend: true
web: true
miniapp: true
admin: true
database: false
storage: true
api: conditional
capabilities:
  new: []
  modified:
    - object-storage
    - brand-management
    - brand-certificate-management
    - miniapp-brand-list-page
    - miniapp-brand-detail-home-page
    - miniapp-certificate-list-page
    - web-client
```

## Conflict Report

| 来源 | 优先级 | 结论 |
|---|---:|---|
| `prototype/web/thumbnail-usage.html` | 1 | 仅作为状态说明，不作为生产 CSS Port 来源。 |
| PNG Golden Reference | 2 | 当前缺失；后续设计阶段可导出，不阻断 proposal。 |
| `prototype/web/context.md` | 3 | 明确不定义真实接口字段名、不替代 OpenSpec design。 |
| `acceptance.md` | 4 | 功能 AC 与横切 AC 作为实现验收事实源。 |
| `rules/ui-design.md` | 5 | 生产 UI 必须复用 semantic token 与 DS/shared 组件。 |
| existing specs | 6 | 通过 delta spec 修改既有能力。 |

## PNG Checklist

- [ ] 管理端品牌列表 Logo 缩略图、占位、失败态。
- [ ] 管理端品牌编辑弹窗上传中、done、failed、原图预览入口。
- [ ] 管理端品牌证书列表/卡片图片缩略图、PDF 占位、失败态。
- [ ] 小程序品牌列表、品牌主页、证书列表常见视口 evidence。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-02 19:21:07 | `/opsx-archive REQ-0092` | Change 归档到 `openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/`，REQ-0092 验收通过并迁入 archive。 |
| 2026-08-02 18:37:08 | `/opsx-apply REQ-0092` | 实现品牌 Logo 与图片类品牌证书同目录 `.thumb` 缩略图生成、API 字段、Web/小程序消费、backfill dry-run/apply 与验证。 |
| 2026-08-02 18:16:03 | `/sprint-propose sprint-017` | Change 纳入 sprint-017 正式范围，等待 `/opsx-apply`。 |
| 2026-08-02 18:07:10 | `/req-opsx` | 从 REQ-0092 创建 OpenSpec Change，生成 proposal/design/specs/tasks/trace 初稿。 |

## Implementation Evidence

| 项 | 结论 | 证据 |
|---|---|---|
| API 字段 | 新增可选字段 | `UploadResult.thumbnail_key/thumbnail_url`、`BrandAdminItem.logo_thumbnail_url`、品牌证书与小程序证书响应 `thumbnail_url`；已重新生成 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。 |
| DB | 无需变更 | 缩略图 key 由原 `logo_object_key` / `file_key` 同目录 `.thumb` 规则确定，不新增 SQLite/MySQL 字段、迁移或 schema。 |
| 依赖 / Docker 镜像 | 无需变更 | 复用既有 Pillow 与 `generate_image_thumbnail`，未新增 Python/Node 依赖或 Dockerfile 层。 |
| Backfill | 已提供 | `scripts/backfill-brand-certificate-thumbnails.py --execute` 支持 dry-run/apply，输出 total、success、failed、skipped、retry_candidates、failure_reasons 与逐项状态。 |
| 媒体五联验收 | 通过 | key：同目录 `.thumb`；object：真实缩略图字节不等于原图；URL：`/media/<thumb-key>`；benefit：列表/卡片优先小图；render evidence：Web Vitest、miniapp static、Docker Web 上传 smoke。 |
| 已知非阻断项 | 既有日期敏感测试 | `tests/test_miniapp_home.py::test_miniapp_product_list_brand_default_sort_uses_published_at_and_id` 在 2026-08-02 只返回仍属新品的 `FST-001`，旧期望仍断言 3 个 SKU；与 REQ-0092 缩略图链路无关。 |

## Validation Evidence

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-02 18:31:34 | `pnpm --dir src/web test -- --run BrandCertificateComponents BrandFormModal` | 59 files / 324 tests passed。 |
| 2026-08-02 18:34:00 | `uv --project src/backend run python -m pytest ...` | 本次相关后端 focused：61 passed。 |
| 2026-08-02 18:35:00 | `uv --project src/backend run python -m pytest tests/test_backfill_brand_certificate_thumbnails.py` | 1 passed，覆盖 dry-run/apply/repeat 幂等。 |
| 2026-08-02 18:31:00 | `uv run pytest tests/test_miniapp_static.py` | 31 passed。 |
| 2026-08-02 18:36:00 | `openspec validate add-brand-certificate-image-thumbnails --strict` | passed。 |
| 2026-08-02 18:37:08 | `curl -I http://localhost:3000` | Docker Web 返回 200。 |
| 2026-08-02 18:37:20 | Docker Web 上传 smoke | 小文件品牌 Logo 上传成功，`/media/...` 读取 200。 |
| 2026-08-02 18:37:40 | Docker Web 26MB PDF 上传 | 返回 `400 / code=50005`，不是 Nginx 413。 |
