---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
title: 小程序证书列表页图片不显示
severity: high
status: done
owner:
discovered_at: 2026-08-30 10:23:23
environment: prod
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0135-miniapp-certificate-card-file-url-fallback
related_change: fix-miniapp-certificate-media-urls
created_at: 2026-08-30 10:26:49
updated_at: 2026-08-30 14:38:12
lifecycle_stage: review
---

# 现象

生产环境微信小程序进入「证书」Tab 后，证书列表页可正常显示证书名称、品牌名称和证书类型，但所有证书卡片顶部媒体区域均未展示实际图片，而是降级为“证书”文字占位。

# 复现步骤

1. 打开生产环境微信小程序。
2. 点击底部 Tab「证书」，进入证书列表页。
3. 观察首屏证书卡片顶部媒体区域。
4. 请求生产公开接口 `GET /api/v1/miniapp/certificates?page=1&pageSize=12`。
5. 检查接口返回的 `items[]` 中图片字段。

# 期望结果

图片类证书在证书列表卡片中展示可公开访问的轻量缩略图。列表接口应为 `file_kind: "image"` 的证书返回非空 `thumbnail_url`，同时不暴露原始对象 key、后台备注、鉴权头、Cookie 或环境变量内容。

# 实际结果

生产接口返回的 6 条证书均为 `file_kind: "image"`，但 `file_url` 与 `thumbnail_url` 均为 `null`。小程序列表页渲染图片需要 `file_kind == "image"` 且 `thumbnail_url` 非空，因此所有证书卡片都进入“证书”文字占位状态。

# 影响范围

- 生产环境微信小程序证书列表页。
- 后端公开接口 `GET /api/v1/miniapp/certificates`。
- 证书媒体字段聚合、历史证书图片 key 迁移、缩略图回填链路。
- 用户浏览证书入口的视觉可信度和点击转化。

证书详情页是否同样受影响待后续 `/bug-complete` 阶段补充复现或接口证据。

# 严重等级说明

严重等级为 `high`。证书列表页是小程序底部一级入口，图片证书全部退回占位会显著影响证书可信展示；同时问题发生在生产环境，并且与公开 API、媒体派生图和历史数据修复链路相关，具备跨层修复风险。

# 初步证据

- 小程序列表页图片渲染条件要求 `file_kind == "image"`、`thumbnail_url` 非空且未触发图片失败降级。
- 后端公开列表为了安全隐藏 `file_url`，但缩略图字段依赖服务层从证书媒体 URL 推导。
- 生产接口证据显示图片类证书的 `file_url` 与 `thumbnail_url` 均为空，能够解释当前截图中的全部占位现象。

# 初步修复方向

- 排查公开证书聚合查询对 `brand_certificates` 与 `brand_certificate_images` 的主图选择、`file_key` 路径识别和 `file_url` 生成逻辑。
- 排查生产历史证书图片是否仍存在旧路径、空 `file_url`、缺主图记录或缺 `.thumb.webp` 派生对象。
- 修复后补充接口测试，覆盖图片类证书返回非空 `thumbnail_url` 和公开安全字段过滤。
- 如涉及历史媒体数据，先执行 dry-run 统计候选，再执行受控迁移或缩略图回填。

# 关联 OpenSpec Change

- `fix-miniapp-certificate-media-urls`：type `fix`，status `archived`。
openspec_changes:
  - change_id: fix-miniapp-certificate-media-urls
    type: update
    status: archived
