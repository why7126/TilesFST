---
bug_id: BUG-0146-batch-media-maintenance-banner-variants
review_result: approved
reviewed_at: 2026-08-29 19:13:50
created_at: 2026-08-29 19:13:50
updated_at: 2026-08-29 19:13:50
reviewer: workflow
---

# Review

## 评审结论

批准修复。

BUG-0146 已具备可复核的生产现象、代码定位和 confirmed 根因。生产 Banner `.thumb.webp` URL 返回 200 但带 `x-media-fallback: 1`，且响应 `Content-Type` 为 PNG，说明派生图缺失被原图 fallback 掩盖；后端批量媒体维护候选来源未包含 `banners.image_object_key`，可以解释现有维护命令无法补齐历史 Banner 派生图。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| `root_cause_status: confirmed` 且证据链可定位 | pass | `root-cause.md` 已记录生产响应头、维护任务候选来源、上传链路和媒体代理 fallback 的证据链 |
| 严重等级合理 | pass | 生产首页/列表高曝光 Banner 可能加载原始大图，影响首屏性能、弱网体验和对象存储流量 |
| 回归验收明确 | pass | `acceptance.md` 覆盖 dry-run、apply、幂等、URL、object 和端侧 render evidence |
| 是否需 hotfix 路径 | conditional | 若生产 Banner 数量较多、原图体积普遍较大或首页加载压力明显，建议走 hotfix；否则可纳入下一 Sprint 常规修复 |

## 修复范围建议

- 在批量媒体维护候选来源中纳入 `banners.image_object_key`。
- 优先覆盖 Banner 自定义上传图，即 `image_source = 'custom_upload'` 或 `image_object_key` 位于 `images/default/banners/` 的记录。
- 确保 `backfill-image-variants` 能生成 `.thumb.webp` 与 `.display.webp`。
- 确保缩略图专项任务和 `media-drift-reconcile` 聚合任务能覆盖 Banner `.thumb.webp` 缺失候选。
- 同步更新生产媒体维护 runbook 和维护任务相关测试。

## 验收关注点

- dry-run 输出中应出现 `source_type: banner_image`。
- apply 后 COS 中 Banner 原图旁应存在 `.thumb.webp` 与 `.display.webp`。
- apply 后同一 Banner 派生图 URL 应返回 `Content-Type: image/webp`，不再出现 `x-media-fallback: 1`。
- 幂等 dry-run 不应再次报告同一 Banner 派生图缺失。
- Web 管理端或小程序首页/品牌列表需补充 Network/render evidence。

## 后续建议

先纳入 Sprint，再创建 BUG 修复 Change。若选择 hotfix，可在 Sprint scope 中标注生产媒体性能修复优先级，并将生产 dry-run/apply 输出 JSON 作为验收证据。
