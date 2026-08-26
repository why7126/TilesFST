---
req_id: REQ-0123-upload-stage-trace-spans
status: captured
created_at: 2026-08-25 18:37:29
updated_at: 2026-08-25 18:37:29
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0115-media-multi-variant-images
captured_via: capture
classification_rationale: 已有头像上传与通用图片上传链路需要新增阶段级耗时可观测能力，属于增强性需求而非已交付行为偏差。
---

# 一句话

头像上传和通用图片上传分支应接入阶段级耗时，并优先写入 task trace spans，至少覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。

# 原始描述

给头像上传和通用图片上传分支接入阶段级耗时，最好写入 task trace spans，而不只是日志；至少要能看到 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。

# 背景与关联

- 关联需求：`REQ-0115-media-multi-variant-images`
- 关联问题背景：`BUG-0142-admin-avatar-upload-storage-put-slow`
- 涉及端与模块：后端 media upload、头像上传、通用图片上传、对象存储适配层、图片衍生规格生成链路
- 业务价值：在上传耗时异常时可以按阶段定位瓶颈，区分文件读取、原图入库、缩略图生成与入库、展示图生成与入库等阶段，减少只能依赖日志猜测的排查成本
- 预期后续：在 OpenSpec Change 中明确 trace span 数据结构、采集边界、失败阶段记录方式、测试证据和兼容性策略

# 影响范围

- 后端：影响头像上传与通用图片上传服务链路，需要在关键阶段记录耗时。
- API：可能影响上传响应或异步任务查询返回的 trace 信息，需在后续 PRD/Change 阶段明确是否新增或扩展字段。
- 数据库：若 task trace spans 持久化依赖现有表或新增结构，需在后续阶段确认。
- 对象存储：需覆盖原图、缩略图、展示图 `put_object` 阶段耗时，不改变对象 key 策略。
- Web/小程序：本条 capture 不直接改变展示端行为；若 trace 对管理端可见，后续需说明入口。
- Orval：若 API 响应契约变化，后续实现阶段需要同步生成。

# 建议验收要点

- [ ] 头像上传和通用图片上传都能产生阶段级耗时记录。
- [ ] trace spans 至少包含 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。
- [ ] 每个 span 至少能表达阶段名称、开始/结束或耗时、成功/失败状态，以及失败错误摘要。
- [ ] 阶段耗时优先写入 task trace spans；日志只作为辅助证据，不作为唯一事实源。
- [ ] 任一阶段失败时，已完成阶段的 span 不丢失，失败阶段可定位。
- [ ] 单元或集成测试覆盖头像上传与通用图片上传两条分支的 span 生成。

# 待澄清

- [ ] trace spans 是否复用现有 task trace 存储结构，还是需要新增字段或表。
- [ ] 管理端是否需要在本期展示阶段耗时，还是仅后端任务 trace 可查询。
- [ ] 同步上传接口是否需要在响应中返回 trace id 或 span 摘要。

# 探索结论

（/req-explore 后人工确认写入）
