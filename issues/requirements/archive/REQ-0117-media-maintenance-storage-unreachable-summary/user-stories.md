---
requirement_id: REQ-0117-media-maintenance-storage-unreachable-summary
title: 媒体维护 dry-run 增加对象存储不可达快速摘要 - 用户故事
created_at: 2026-08-22 17:14:59
updated_at: 2026-08-22 17:14:59
---

# 用户故事

## US-001 运维快速识别对象存储不可达

作为实施 / 运维人员，我希望媒体维护 dry-run 在 COS、MinIO 或 S3 兼容对象存储不可达时快速返回阻断摘要，以便先修复 endpoint、网络、bucket 或权限问题，而不是逐条排查误导性的对象缺失。

验收要点：

- dry-run 能把对象存储不可达归类为 `object_storage_unreachable` 或等价枚举。
- 输出包含 provider、bucket hash、auto create bucket 策略和建议动作。
- 输出不包含真实 bucket 名、access key、secret key、连接串、raw object key 或本机绝对路径。

## US-002 发布负责人阻止错误 apply 判断

作为发布负责人，我希望聚合媒体维护任务在对象存储不可达时在顶层 summary 标记 blocked，以便阻止“失败为 0、可以 apply”的错误判断。

验收要点：

- 聚合任务在顶层 summary 或 acceptance summary 中表达对象维度 blocked。
- 受影响子任务可从 `affected_tasks` 或等价字段追溯。
- 对象存储不可达时不得建议进入备份确认和 apply。

## US-003 后端开发统一失败分类

作为后端开发，我希望维护任务能复用统一的对象存储不可达识别和短路机制，以便避免不同任务各自把 `STORAGE_UNAVAILABLE` 误处理为对象缺失。

验收要点：

- 对象不存在和对象存储不可达分支清晰区分。
- `MEDIA_NOT_FOUND` 或 NoSuchKey / NoSuchObject 仍归入对象缺失统计。
- `STORAGE_UNAVAILABLE` 或等价异常归入对象存储不可达统计，并触发快速摘要或短路。

## US-004 测试验证安全输出

作为测试 / 验收人员，我希望有聚焦测试覆盖对象存储不可达、对象不存在和敏感信息输出保护，以便确保 dry-run 结果既准确又安全。

验收要点：

- 测试覆盖对象存储不可达时的 blocked 摘要。
- 测试覆盖对象真实不存在时仍保留 missing 类统计。
- 测试覆盖聚合任务顶层阻断语义和敏感输出保护。

## US-005 产品负责人理解运维收益

作为产品 / 业务负责人，我希望需求能说明快速失败摘要的价值和边界，以便评审时判断是否纳入 Sprint。

验收要点：

- 文档说明本需求不会自动修复对象存储，也不会执行生产写入。
- 文档说明对象存储修复后仍需重新 dry-run，再判断是否进入 apply。
- 文档说明本需求继承 REQ-0097 的 dry-run、apply、快照、二次审计和脱敏输出边界。
