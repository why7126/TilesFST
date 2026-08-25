## 背景

生产媒体维护 dry-run 目前会访问对象存储来判断原图、缩略图或迁移目标对象状态。若 COS、MinIO 或 S3 兼容对象存储因 endpoint、bucket、region、权限或网络问题不可达，dry-run 容易把统一不可达误读成大量对象缺失，导致运维误以为可以继续排查单个 object，甚至误判可进入 apply。

REQ-0117 已评审并纳入 `sprint-025`。本 Change 用更快的阻断摘要把对象存储环境问题前置暴露，减少生产维护窗口内的无效扫描和错误决策。

## 变更内容

- 媒体维护 dry-run 在对象存储不可达时 MUST 快速返回 `object_storage_unreachable` 或等价失败分类。
- dry-run 输出 MUST 在顶层 summary 或 acceptance summary 标记 `blocked`，并列出受影响对象相关子任务。
- 对象存储不可达 MUST 与对象真实不存在区分：`MEDIA_NOT_FOUND`、`NoSuchKey`、`NoSuchObject` 等仍归入 missing 类统计。
- 阻断摘要 MUST 输出 provider、bucket 脱敏标识、auto create bucket 策略、失败分类和建议动作。
- 阻断摘要与日志 MUST NOT 暴露真实 bucket 名、access key、secret key、连接串、raw object key、本机绝对路径、Authorization header、Cookie 或完整 SDK 堆栈。
- 本 Change 不自动修复对象存储、不新增生产写入能力、不改变 dry-run/apply 两阶段边界。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `prod-media-maintenance-jobs`：补充媒体维护 dry-run 对象存储不可达快速摘要、顶层 blocked 语义、affected tasks 和脱敏输出要求。

## 影响

- 后端：影响生产媒体维护命令、对象存储适配层异常分类和 dry-run 聚合摘要。
- 对象存储：只读检查路径需要区分不可达与对象缺失。
- API：不新增或变更对外 HTTP API，不需要 OpenAPI / Orval。
- 数据库：不新增表字段或迁移。
- Web / 小程序 / 管理端 UI：不涉及。
- 测试与文档：需要补充媒体维护 dry-run 聚焦测试、脱敏输出断言和生产媒体维护 runbook 说明。
