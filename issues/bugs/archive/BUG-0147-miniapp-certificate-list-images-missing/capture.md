---
bug_id: BUG-0147-miniapp-certificate-list-images-missing
status: done
created_at: 2026-08-30 10:23:23
updated_at: 2026-08-30 11:49:41
severity_hint: high
environment: prod
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0135-miniapp-certificate-card-file-url-fallback
lifecycle_stage: plan
---

# 现象

生产环境微信小程序证书列表页的证书卡片图片区域未显示实际证书图片，所有图片区域降级为“证书”文字占位。页面仍能展示证书名称、品牌名称和证书类型，说明列表数据加载成功，但卡片封面图片字段不可用。

# 复现步骤

1. 打开生产环境微信小程序。
2. 进入底部 Tab「证书」，打开证书列表页。
3. 观察证书卡片顶部媒体区域。
4. 只读请求生产接口：
   `GET /api/v1/miniapp/certificates?page=1&pageSize=12`
5. 对比接口返回的证书图片字段与小程序列表页渲染条件。

# 期望 vs 实际

- 期望：图片类证书在证书列表页展示可公开访问的轻量缩略图；缺少缩略图时应有明确的后端数据或媒体维护证据，避免图片证书全部退回文字占位。
- 实际：生产接口返回的 6 条证书均为 `file_kind: "image"`，但 `file_url` 与 `thumbnail_url` 均为 `null`，小程序卡片没有可用 `thumbnail_url`，因此全部显示“证书”占位。

# 影响范围

- 生产环境微信小程序证书列表页。
- 后端公开接口 `GET /api/v1/miniapp/certificates`。
- 证书媒体字段聚合、历史证书图片 key 迁移、缩略图回填链路。
- 用户浏览证书入口的视觉可信度和点击转化；详情页是否受影响需在后续根因探索中补证。

# 初步线索

- 小程序证书列表页仅在 `file_kind == 'image'`、`thumbnail_url` 非空且图片未加载失败时渲染 `<image>`；否则展示“证书”占位。
- 后端列表接口为了公开安全会隐藏 `file_url`，但缩略图字段依赖服务层从 `record.file_url` 推导。
- 生产接口当前返回 `file_url: null`、`thumbnail_url: null`，说明公开聚合层没有拿到可推导的媒体 URL。
- 后端已有证书图片 key 迁移和证书缩略图回填脚本，后续应排查生产数据是否仍存在旧 `files/default/brand-certificates/` 路径、空 `file_url`、缺主图记录或缺派生缩略图对象。

# 建议验收或复现要点

- [ ] 生产接口 `GET /api/v1/miniapp/certificates?page=1&pageSize=12` 中图片类证书返回非空 `thumbnail_url`。
- [ ] 小程序证书列表页图片类证书卡片展示实际证书缩略图，不再全部显示“证书”占位。
- [ ] 修复后仍不在列表接口暴露原始对象 key、后台备注、Authorization header、Cookie 或 `.env` 内容。
- [ ] 若涉及历史媒体数据，dry-run 能报告需迁移或回填的证书图片数量，apply 后对象存储存在对应 `.thumb.webp`。
- [ ] 补充后端接口测试覆盖 `file_url` 为空或历史 key 场景下的 `thumbnail_url` 行为。
- [ ] 补充小程序静态或交互测试，覆盖证书列表卡片图片字段正常、图片失败降级两种状态。

# 来源

- 来源命令：`/bug-capture`
- 来源描述：小程序证书列表页图片不显示；生产接口返回 image 类型证书但 `file_url` 和 `thumbnail_url` 均为空，导致列表卡片全部显示“证书”占位。
- 只读生产接口证据：`GET /api/v1/miniapp/certificates?page=1&pageSize=12` 返回 6 条证书，均为 `file_kind: "image"` 且 `file_url: null`、`thumbnail_url: null`。
- 截图证据：用户提供的小程序证书列表页截图，卡片媒体区均显示“证书”占位。

# 拆分说明

本次不拆分。现象集中在同一页面、同一公开证书列表接口与同一证书媒体字段链路，一次后端数据聚合/媒体维护修复可闭环。

# 附件

- 会话截图：Image #1，小程序证书列表页多张证书卡片图片区域显示“证书”占位。
