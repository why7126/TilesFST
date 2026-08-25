## ADDED Requirements

### Requirement: 媒体维护 dry-run 必须快速摘要对象存储不可达

生产媒体维护作业在 dry-run 期间 MUST 区分对象真实不存在和对象存储不可达。当对象存储因 endpoint、region、bucket、权限、凭据、网络或服务状态导致不可达时，dry-run MUST 快速返回阻断摘要，MUST 将顶层状态或对象验收维度标记为 `blocked`，并 MUST NOT 输出可进入 apply 的结论。

#### Scenario: 对象存储不可达时返回 blocked 摘要

- **WHEN** 运维执行生产媒体维护 dry-run 且对象存储 endpoint、bucket、region、权限或网络不可用
- **THEN** 作业 MUST 返回 `object_storage_unreachable` 或等价失败分类
- **AND** 作业 MUST 将顶层 summary 或 acceptance summary 的对象维度标记为 `blocked`
- **AND** 作业 MUST 列出受影响对象相关子任务或等价 `affected_tasks`
- **AND** 作业 MUST 建议先检查 endpoint、region、bucket、权限、网络与 env 注入后重新 dry-run
- **AND** 作业 MUST NOT 输出可进入备份确认或 apply 的结论。

#### Scenario: 对象不存在仍归入 missing 统计

- **WHEN** dry-run 访问单个媒体对象并收到 `MEDIA_NOT_FOUND`、`NoSuchKey`、`NoSuchObject` 或等价对象不存在结果
- **THEN** 作业 MUST 将该对象归入 missing 类统计
- **AND** 作业 MUST NOT 将单个对象不存在误报为 `object_storage_unreachable`
- **AND** 作业 MUST 在对象存储整体可达时继续生成正常 dry-run 摘要。

#### Scenario: 阻断摘要必须脱敏

- **WHEN** dry-run 输出对象存储不可达摘要、日志或验收证据
- **THEN** 输出 MAY 包含 provider、bucket hash、auto create bucket 策略、失败分类和建议动作
- **AND** 输出 MUST NOT 包含真实 bucket 名、access key、secret key、连接串、raw object key、本机绝对路径、Authorization header、Cookie、`.env` 原文、生产私有 URL 或完整 SDK 堆栈。

#### Scenario: 聚合维护任务传播对象维度 blocked

- **WHEN** 聚合媒体维护任务中的任一对象相关子任务发现对象存储不可达
- **THEN** 聚合任务 MUST 在顶层 summary 传播 `blocked` 状态
- **AND** 聚合任务 MUST 标明受影响子任务和未完成对象检查范围
- **AND** 聚合任务 MUST 将后续对象相关子任务标记为 skipped、blocked 或等价不可执行状态
- **AND** 聚合任务 MUST 提示修复对象存储环境后重新 dry-run。
