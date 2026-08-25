---
req_id: REQ-0117-media-maintenance-storage-unreachable-summary
status: done
created_at: 2026-08-22 16:57:17
updated_at: 2026-08-22 19:38:59
recorded_by: product
source: 用户反馈
priority_hint: P2
parent_requirement: REQ-0097-prod-compose-media-maintenance-job
---

# 一句话

媒体维护 dry-run 在对象存储不可达时，应更快返回脱敏失败摘要，避免把基础设施不可达误判为大量对象缺失。

# 原始描述

为后续给媒体维护 dry-run 增加更快的对象存储不可达失败摘要。

# 背景与关联

- 来源命令：`/explore`
- 类型倾向：运维体验与证据质量增强
- 关联需求：`REQ-0097-prod-compose-media-maintenance-job`
- 涉及模块：后端媒体维护任务、对象存储适配层、生产媒体维护 runbook、维护任务测试
- 现状依据：当前维护任务已有 dry-run、脱敏输出和 `failure_reasons`，但 `_object_exists()` 会把所有 `AppError` 压成 `False`；对象存储适配器会把非对象不存在异常统一映射为 `STORAGE_UNAVAILABLE`，因此对象存储不可达时容易呈现为多条对象缺失或逐条失败。
- 业务价值：让生产或生产等价环境的媒体维护 dry-run 更快识别 COS/MinIO 不可达、权限或 endpoint 配置问题，减少误判、等待时间和人工排障成本。

# 待澄清

- [ ] 快速摘要应覆盖所有媒体维护任务，还是先覆盖 `bug-0116-media-drift`、`backfill-brand-certificate-thumbnails` 与 `backfill-image-variants`。
- [ ] 不可达探测应作为任务启动前的统一健康检查，还是在首次 `STORAGE_UNAVAILABLE` 后短路并汇总。
- [ ] dry-run 返回不可达时是否使用 `status: blocked`，以及是否仍保留部分数据库扫描摘要。
- [ ] 失败摘要需包含哪些脱敏字段：provider、bucket hash、auto_create_bucket、task、affected_tasks、failure_reason、recommended_action。

# 建议验收要点

- [ ] 当对象存储不可达、权限异常或 endpoint 配置错误时，媒体维护 dry-run 应快速返回脱敏 JSON 摘要，不逐条输出大量误导性的对象缺失明细。
- [ ] 摘要必须使用枚举化失败原因，例如 `object_storage_unreachable` 或等价分类，并保留 `object_storage_provider`、`object_storage_bucket_hash`、`auto_create_bucket` 等安全环境信息。
- [ ] 不得输出 access key、secret key、数据库连接串、Authorization header、Cookie、真实 `.env` 内容、本机绝对路径或未脱敏 object key。
- [ ] 现有对象真实不存在的场景仍应保持为对象缺失类统计，不能被误归类为对象存储不可达。
- [ ] 聚合任务应在顶层 `summary` 或 `acceptance_summary.object` 中表达阻断状态，便于运维先处理对象存储连接问题再考虑 apply。
- [ ] 补充聚焦测试覆盖对象存储不可达、对象不存在、聚合任务短路摘要和敏感信息输出保护。

# 探索结论

`/explore` 判断该建议有用，属于 P2 偏上的运维增强需求。当前实现中 `src/backend/app/modules/media/storage.py` 会把对象存储连接、权限或 SDK 异常映射为 `STORAGE_UNAVAILABLE`，但 `src/backend/app/modules/media/maintenance.py` 的对象存在性判断会把所有 `AppError` 简化为 `False`。若生产对象存储不可达，dry-run 可能呈现为多条 `missing_original`、`missing_thumbnail` 或 `object_exists=false`，排障信号不够清晰。建议后续通过统一健康探测或首次不可达短路，输出安全、快速、可读的失败摘要。
