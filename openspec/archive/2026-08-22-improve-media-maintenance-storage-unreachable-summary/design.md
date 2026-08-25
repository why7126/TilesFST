## 背景

REQ-0117 来源于媒体维护 dry-run 体验优化：生产维护作业在对象存储不可达时应尽早告诉运维“环境不可用”，而不是继续逐条扫描并输出误导性的缺失对象摘要。现有 `prod-media-maintenance-jobs` 已定义 dry-run/apply、安全执行、脱敏输出、备份和二次审计，本 Change 只扩展 dry-run 的失败分类与聚合摘要。

当前相关约束：

- dry-run MUST NOT 写数据库或对象存储。
- apply 仍必须显式触发，并遵守备份、幂等和二次审计要求。
- 输出必须脱敏，不能暴露真实对象存储凭据、完整对象 key、连接串或本机路径。
- 生产对象存储可能是 MinIO、腾讯云 COS、火山云 TOS 或其他 S3 兼容服务。

## 目标与非目标

**目标：**

- 统一识别对象存储不可达、权限异常、bucket 不存在、region/endpoint 配置错误和网络超时等阻断类错误。
- 在 dry-run 发现阻断类错误时快速返回 blocked 摘要，并阻止“可进入 apply”的结论。
- 保留对象真实不存在的 missing 类统计，避免把 `NoSuchKey` / `NoSuchObject` 误判为环境不可达。
- 为对象相关子任务输出可追溯的 `affected_tasks`、失败分类和建议动作。
- 通过测试证明 blocked 摘要准确且无敏感信息泄露。

**非目标：**

- 不自动创建、修复、迁移或授权对象存储 bucket。
- 不新增后台 UI、管理端 API 或小程序行为。
- 不改变 REQ-0097 已定义的 dry-run/apply、备份、回滚和二次审计主流程。
- 不引入新的对象存储 SDK 或外部依赖。

## 技术决策

### 1. 在维护作业层统一归类对象存储异常

实现阶段应在生产媒体维护作业的对象访问封装处增加统一分类 helper，将底层 SDK / 适配层异常归一为：

- `object_storage_unreachable`：endpoint 不可达、网络超时、认证失败、权限不足、bucket 不存在、region 错误、存储服务不可用或 `STORAGE_UNAVAILABLE` 等环境阻断。
- `object_missing`：`MEDIA_NOT_FOUND`、`NoSuchKey`、`NoSuchObject` 或等价单对象不存在。
- `object_check_failed`：无法明确归类但不应泄露底层细节的检查失败。

这样可以让 SKU pending 主图正式化、证书图片 key 迁移、缩略图回填、object audit 等子任务复用同一语义。

### 2. dry-run 首次确认不可达后短路对象相关扫描

当 dry-run 的对象访问遇到 `object_storage_unreachable`，维护作业应立即停止后续对象相关扫描，返回 blocked 摘要。数据库候选范围统计可以保留已完成结果，但输出必须清楚标识对象维度未验证。

选择短路而不是继续遍历，是为了避免在生产维护窗口内制造大量重复失败日志，也避免把环境问题误写成数据问题。

### 3. 聚合摘要使用顶层 blocked 与 affected_tasks

输出结构应包含顶层状态和受影响任务，例如：

```json
{
  "status": "blocked",
  "failure_category": "object_storage_unreachable",
  "affected_tasks": ["object_key_audit", "thumbnail_backfill"],
  "recommended_action": "检查 endpoint、region、bucket、权限、网络与 env 注入"
}
```

具体字段名可沿用现有维护作业摘要结构，但语义必须可被测试和验收读取。

### 4. 脱敏摘要只暴露诊断所需元信息

blocked 摘要可输出 provider、bucket hash、auto create bucket 策略、region 是否配置、path-style/virtual-host 风格和错误分类。真实 bucket 名、object key、endpoint 私有域名、access key、secret key、连接串、Authorization header、Cookie、`.env` 原文、完整 SDK 堆栈和本机绝对路径都必须被过滤或替换。

## 风险与取舍

- [Risk] 底层 SDK 异常类型在不同 provider 上差异较大 -> Mitigation：分类 helper 以项目适配层统一异常、SDK error code 和 message pattern 的最小集合实现，并用测试覆盖典型 COS/MinIO/S3 兼容错误。
- [Risk] 过早短路会减少单次 dry-run 中可见的数据问题 -> Mitigation：对象存储不可达时对象维度本身没有可信证据，摘要必须提示修复环境后重新 dry-run。
- [Risk] 脱敏过度导致排查信息不足 -> Mitigation：保留 provider、bucket hash、auto create bucket 策略和建议动作，不输出敏感原文。

## 迁移计划

该变更不涉及数据库迁移或 API 契约迁移。实现后发布到生产维护镜像或 backend 镜像即可生效。若出现误分类，可回滚代码版本；已生成的 dry-run 摘要不写入业务数据。

## 开放问题

- 无阻塞问题。实现阶段可根据现有维护命令摘要结构决定字段命名，但必须保留 `blocked`、`object_storage_unreachable` 和 `affected_tasks` 等等价语义。
