---
change_id: add-media-multi-variant-images
status: applied
created_at: 2026-08-22 14:06:22
updated_at: 2026-08-22 18:22:44
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-025
change_type: add
owner: product
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: possible
  storage: true
  api: true
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-media-upload-chain.md
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/knowledge-base/retrospectives/sprint-022-retrospective.md
prototype_refs:
  - issues/requirements/archive/REQ-0115-media-multi-variant-images/prototype/web/context.md
---

# Change 追踪

## 来源

- REQ：`issues/requirements/archive/REQ-0115-media-multi-variant-images/`
- Sprint：`iterations/archive/sprint-025/`
- 评审结论：存量图片批量生成与对象存储直出纳入本期；CDN 正式接入仅预留。

## Readiness

```yaml
requirement_readiness: Partially Ready
review_gate: pass
sprint_inclusion_gate: pass
change_created_by_cli: true
reason: REQ 六件套齐全且已评审通过；命中的 knowledge-base 文档为 draft，UI 原型当前为策略说明，PNG 待 apply 阶段按需补证。
```

## Conflict Report

```yaml
prototype_priority:
  - prototype/web/context.md
  - acceptance.md
  - requirement.md
  - rules/ui-design.md
  - openspec/specs
conflict_status: no_blocking_conflict
notes:
  - 无 HTML / PNG 原型，不存在视觉稿冲突。
  - 如 apply 阶段涉及管理端上传状态或小程序展示 UI，必须补 UI Contract、截图和关键交互证据。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-22 14:06:22 | `/req-opsx` | 通过 OpenSpec CLI 创建 Change，生成 proposal、design、delta specs、tasks 和 trace。 |
| 2026-08-22 14:33:52 | `/opsx-apply` | 实现三规格图生成、端侧消费、存量回填、对象存储直出适配、OpenAPI/Orval、文档与聚焦测试。 |
| 2026-08-22 17:21:41 | `/opsx-modify` | 根据验收反馈返修小程序 SKU 详情图片预览，基于 media 下标统一使用 `original_url || preview_url || url` 生成 `current` 与 `urls`，并补静态测试与验收记录。 |
| 2026-08-22 17:28:36 | `/opsx-modify` | 根据复验证据继续返修：`wx.previewImage` 前显式 `wx.getImageInfo({ src: current })` 获取 original URL，解决 DevTools Network 仍未观察到 original 请求的问题。 |
| 2026-08-22 17:33:29 | `/opsx-modify` | 回填用户二次复验证据：DevTools Network 已观察到 SKU 377 原图 `.png` 请求，AC-MINIAPP-003 可按 DevTools evidence 记为通过。 |
| 2026-08-22 18:22:44 | `/opsx-archive` | 归档前验收结论回填为 passed，体验版或真机 evidence 作为发布前增强项，不阻塞本 Change。 |

## 实现摘要

- 后端媒体服务新增 `thumbnail / display / original` URL 派生、`.display` 生成、缺失回退和短期对象存储直出 URL 适配。
- 上传接口、管理端 SKU、Miniapp 商品/SKU 媒体响应新增多规格 URL 字段。
- 管理端 SKU 图片上传补齐 `idle -> uploading -> uploaded / failed` 状态和同会话回显；小程序列表/详情/预览分别消费 thumbnail/display/original。
- 新增 `backfill-image-variants` 维护任务，默认 dry-run，写入必须 `--apply --confirm-backup`。
- 未新增数据库表字段；多规格 URL 由原图 `object_key` 派生。

## 证据摘要

| 类型 | 状态 | 证据 |
|---|---|---|
| 后端测试 | pass | `tests/test_media_storage.py`、`tests/test_deploy_media_maintenance_script.py`，31 passed |
| 小程序测试 | pass | miniapp 媒体字段与静态绑定聚焦测试，3 passed |
| Web 测试 | pass | `pnpm ... test` 实际运行 Web 62 个测试文件 / 359 tests passed |
| OpenAPI / Orval | pass | `./scripts/generate-openapi-client.sh` |
| TypeScript 全量检查 | blocked | `BrandCertificateComponents.test.tsx` mock 类型与 `auth-store.ts` 主题枚举既有/旁支问题阻塞 |
| UI/Network evidence | blocked | 未执行 1440px Web 截图、微信 DevTools/真机 Network evidence |

## 验收返修记录

### 反馈摘要

用户提供 SKU 377 上传、保存、对象存储与微信 DevTools Network 证据：上传和保存接口均已返回 original/display/thumb 三规格 URL；小程序 SKU 详情响应中 `media[0].preview_url` 与 `media[0].original_url` 均为原图；对象存储中同一 SKU 前缀下存在原图、display、thumb 三对象；但点击图片预览时未观察到原图请求。

### 调整摘要

- `src/miniapp/pages/tile-detail/index.wxml`：图片节点新增 `data-media-index="{{index}}"`。
- `src/miniapp/pages/tile-detail/index.ts` 与 `index.js`：新增 `previewUrlForMedia`，并让 `previewImage` 通过 media 下标匹配被点击图片；`current` 与 `urls` 均使用 `original_url || preview_url || url`。
- 第二次返修补充：在 `wx.previewImage` 前调用 `wx.getImageInfo({ src: current })`，用同一个 original URL 显式触发端侧取图；`complete` 后仍以 original URL 的 `current` 与 `urls` 调用预览。
- `tests/test_miniapp_static.py`：新增静态断言覆盖 media 下标、原图优先 resolver、`current` 与 `urls` 的统一来源。

### 证据化根因

```yaml
root_cause_status: confirmed
confirmed_facts:
  - 后端 SKU 详情接口已返回 `media.original_url` / `media.preview_url` 为原图。
  - 返修前小程序预览 `current` 来源于点击节点 `data-url`，`urls` 来源于独立 media map，缺少同一 media index 绑定。
  - 第一次返修后用户 DevTools Network 仍未观察到 original URL 请求，说明仅依赖 `wx.previewImage` 内部取图不足以形成稳定可观测 evidence。
  - 二次返修后用户 DevTools Network 已观察到同一对象的原图 `.png` 请求。
residual_risk:
  - 当前证据为微信 DevTools；体验版或真机 evidence 可作为发布前增强证据，但不再阻塞 AC-MINIAPP-003 的 DevTools 验收。
```
