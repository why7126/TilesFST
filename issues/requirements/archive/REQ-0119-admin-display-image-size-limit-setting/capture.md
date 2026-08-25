---
req_id: REQ-0119-admin-display-image-size-limit-setting
status: done
created_at: 2026-08-22 21:12:30
updated_at: 2026-08-22 22:20:00
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0115-media-multi-variant-images
---

# 一句话

管理端「系统设置 - 媒体与存储」新增 display 图体积目标上限配置，默认值沿用 768KB，使详情展示图的清晰度与流量策略可运营配置。

# 原始描述

管理端媒体与存储新增 display 图体积目标上限配置。

补充决策：

- 正式新增该配置项。
- 默认值沿用 768KB。

# 背景与关联

- 关联需求：`REQ-0115-media-multi-variant-images`
- 现有配置：`media.thumbnail_max_size_kb` 已支持缩略图体积目标上限，`0` 表示不限制。
- 当前缺口：`.display` 图已作为详情普通展示规格存在，但体积目标仍由代码常量固定为 768KB，管理端无法配置。
- 涉及端与模块：Web 管理端系统设置、后端系统设置 API、媒体上传与图片派生规格生成、历史图片多规格维护任务、OpenAPI / Orval、媒体与对象存储文档。
- 业务价值：让运营或部署方可以独立调整详情展示图的流量与清晰度平衡，避免缩略图配置与详情图配置混用。

# 待澄清

- [ ] display 图体积目标上限是否允许 `0` 表示不限制，还是必须保持 768KB 以上的正数默认策略。
- [ ] 配置范围是否采用 `1-2048KB`、`0-2048KB` 或其他上限。
- [ ] 历史 `.display` 对象是否仅通过维护任务重生成，保存系统设置是否继续不触发历史对象扫描。
- [ ] UI 文案是否使用“display 图”还是面向用户改写为“详情展示图”。

# 建议验收要点

- [ ] 管理端 `/admin/settings/media` 展示「display 图体积目标上限 (KB)」或等价字段，默认 effective 值为 768。
- [ ] 后端 `GET /api/v1/admin/system-settings/media` 返回该字段，`PATCH` 可更新并写入设置事实源，`reset` 恢复默认 768。
- [ ] 后续新上传或新生成的 `.display` 图读取该 effective 值，并尽量不超过目标上限；`.thumb` 仍读取独立的 `media.thumbnail_max_size_kb`。
- [ ] 保存系统设置不自动扫描或重建历史 `.display` 对象；历史对象需通过受控维护任务重生成。
- [ ] 文档、OpenAPI / Orval、相关测试与媒体多规格验收口径同步更新。

# 探索结论

（/req-explore 后人工确认写入）
