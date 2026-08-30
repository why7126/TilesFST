---
note: workflow-sync — 3/3 Change 已 archive；0 applied；待人工 sign-off
title: sprint-027 验收报告
created_at: 2026-08-29 18:13:44
updated_at: 2026-08-30 08:45:27
---

# sprint-027 验收报告

## 验收范围

| 类型 | 编号 | 标题 | 状态 | 说明 |
|---|---|---|---|---|
| REQ | REQ-0130-media-maintenance-progress-output | 媒体维护任务进度输出 | done，已归档（`add-media-maintenance-progress-output` archived 2026-08-29 21:46:01） | Change 已归档，验收证据已随归档记录闭环 |
| REQ | REQ-0131-media-object-key-business-id-layout | 统一媒体对象 Key 按业务对象 id 分目录 | done，已归档（`update-media-object-key-business-id-layout` archived 2026-08-29 23:14:05） | 自动化验收通过；生产 apply 仍需发布前备份确认 |
| BUG | BUG-0146-batch-media-maintenance-banner-variants | 批量媒体维护命令未覆盖 Banner 自定义上传图 | done，已归档（`fix-media-maintenance-banner-variants` archived 2026-08-30 08:22:53） | 本地 alias apply 与本地 no-fallback 截图通过；生产公网历史 URL 仍 fallback，需用生产 MySQL/env 重新执行并补证 |

## 验收重点

- 默认命令 stdout JSON 兼容。
- 开启进度后进度输出进入 stderr 或等价隔离通道。
- `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`media-drift-reconcile` 均有进度覆盖。
- 进度字段包含任务、阶段、总量、完成、成功、失败、跳过和百分比。
- 输出脱敏，不泄露真实 object key、`.env`、密钥、连接串、Authorization header 或 Cookie。
- Runbook、CLI help 和测试同步。
- Banner 自定义上传图进入批量媒体维护候选，生成 `.thumb.webp` 与 `.display.webp`。
- Banner 派生图 URL 返回 `Content-Type: image/webp`，不再出现 `x-media-fallback: 1`。
- 小程序首页/品牌列表或 Web 管理端 Banner 预览补充 Network/render evidence。
- 对象 key 最终目录矩阵采用扁平业务媒体类型目录：`user-avatars`、`brand-logos`、`banners`、`tiles`、`brand-certificates`；`avartars` 等错误拼写必须进入审计失败分类。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  status: partial
  affected_layers:
    - backend
    - storage
  reason: 本 Sprint 纳入后端媒体维护 CLI 运维增强和 Banner 历史派生图补齐修复；当前规划不新增业务 API、DB schema、请求日志、行为事件、Web/小程序请求封装或 App 请求封装。若后续 Change 改为持久化进度、写 Task Trace 或新增接口字段，需重新评估。
  validation: REQ-0131 已通过产品数据采集与链路观测门禁；BUG-0146 已补充本地等价环境 dry-run、幂等、URL、miniapp API、生产 apply JSON、生产管理端截图、本地 alias apply 和本地 no-fallback 截图证据；本次已确认生产历史无 id URL 需要兼容并补充 alias 生成逻辑，但生产公网复核仍为 PNG fallback，待使用生产 MySQL/env 重新执行维护任务后复核 no-fallback 与生产公开 API 字段一致性。
```

## 验收结果回填

```yaml
acceptance_status: partial
accepted_at: 2026-08-30 08:42:16
accepted_by: workflow-sync
evidence:
  - "REQ-0131: OpenSpec strict、语言校验、产品数据采集与链路观测门禁通过。"
  - "REQ-0131: 后端对象 key/维护任务/部署脚本聚焦测试 47 passed；Pillow 图片上传与媒体测试 97 passed。"
  - "REQ-0131: 管理端媒体相关 Vitest 9 files / 94 tests passed；小程序媒体相关 pytest 61 passed。"
  - "REQ-0131: Docker Compose 当前 backend/web/docs-site 均运行中，Web 暴露 http://localhost:3000，Backend 暴露 http://localhost:8000。"
  - "BUG-0146: logs/media-drift-reconcile-local-dry-run.json 显示本地等价环境聚合 dry-run 成功，task_count=5，failed=0，聚合子任务扫描到 banner_image。"
  - "BUG-0146: logs/backfill-image-variants-local-dry-run.json 显示 banner_items=6、banner_needs=0、failed=0、estimated_writes=0。"
  - "BUG-0146: logs/backfill-image-variants-production-apply-20260830073333.json 显示生产 apply 扫描 total=691、success=1、failed=2、skipped=689；其中 banner_items=6、banner_failed=0，Banner 均已存在 thumb/display 并跳过。"
  - "BUG-0146: logs/banner-thumb-local-curl.headers 与 logs/banner-display-local-curl.headers 显示本地 Banner thumb/display URL 均为 200、Content-Type=image/webp、x-media-fallback=0。"
  - "BUG-0146: logs/miniapp-home-local-response.json 与 logs/miniapp-brands-local-response.json 显示本地公开接口返回 Banner display.webp URL；对应 display URL 的 curl headers 也为 image/webp 且 x-media-fallback=0。"
  - "BUG-0146: screenshots/banner-management-production-network-20260829.png 为用户补充的生产管理端 Banner 列表和 Network 截图，可作为 render evidence 入口。"
  - "BUG-0146: screenshots/miniapp-home-production-network-render-20260830.png 为用户补充的生产小程序首页 DevTools 截图，页面渲染成功，Network 中多条 .thumb.webp / .display.webp 请求为 200/webp。"
  - "BUG-0146: logs/miniapp-home-production-response-20260830.json 与 logs/miniapp-brands-production-response-20260830.json 为生产公开接口响应证据。"
  - "BUG-0146: logs/backfill-image-variants-local-alias-apply-20260830081739.json 为本地 development/sqlite/tencent-cos alias apply 证据，显示写入 12 个 Banner 旧无 id alias；该文件不是生产 MySQL apply 证据。"
  - "BUG-0146: screenshots/miniapp-home-local-banner-no-fallback-20260830.png 显示本地后端 127.0.0.1:8000 返回 Content-Type=image/webp、x-media-fallback=0。"
failed_items:
  - "BUG-0146: 生产历史无 id Banner .thumb.webp / .display.webp URL 在 2026-08-30 08:23 复核仍返回 Content-Type=image/png、x-media-fallback=1；本地 alias apply 已通过，但生产公网仍未闭环。"
  - "BUG-0146: 生产公开 API curl 返回自定义 Banner URL 字段为空；本地 no-fallback 截图不能替代生产公网/API 一致性证据。"
  - "BUG-0146: 生产 apply 整批任务仍有非 Banner sku_image 失败，summary.failed=2、retry_candidates=2、failure_reasons.OSError=2，需作为维护残留另行跟进。"
notes: Sprint 范围内 3 个 Change 已全部归档，Sprint 按 partial 验收关闭；BUG-0146 已按用户确认直接归档，本地 alias apply 与 no-fallback 已通过，生产 no-fallback 和公开 API 字段一致性后置到发布/运维窗口补证。
```
