## 1. 对象存储失败分类

- [x] 1.1 梳理现有生产媒体维护作业的对象访问入口和异常处理路径。
- [x] 1.2 新增或复用统一 helper，将 `STORAGE_UNAVAILABLE`、endpoint/region/bucket/权限/网络错误归类为 `object_storage_unreachable`。
- [x] 1.3 保留 `MEDIA_NOT_FOUND`、`NoSuchKey`、`NoSuchObject` 等对象不存在分支为 missing 类统计。

## 2. dry-run 快速阻断摘要

- [x] 2.1 在对象存储不可达时短路后续对象相关扫描，并返回顶层 `blocked` 摘要。
- [x] 2.2 在聚合维护任务中传播对象维度 blocked，输出 `affected_tasks` 或等价字段。
- [x] 2.3 输出 provider、bucket hash、auto create bucket 策略、失败分类和建议动作。
- [x] 2.4 确保 blocked 摘要不建议进入备份确认或 apply。

## 3. 安全输出与文档

- [x] 3.1 增加脱敏过滤或断言，禁止输出真实 bucket、密钥、连接串、raw object key、生产私有 URL、完整 SDK 堆栈和本机绝对路径。
- [x] 3.2 更新生产媒体维护 runbook，说明对象存储不可达时的检查顺序和重新 dry-run 要求。

## 4. 测试与验证

- [x] 4.1 补充后端测试覆盖对象存储不可达时的 blocked 摘要和 affected tasks。
- [x] 4.2 补充测试覆盖对象真实不存在时仍归入 missing 统计。
- [x] 4.3 补充测试覆盖聚合任务顶层阻断语义和敏感信息输出保护。
- [x] 4.4 运行聚焦 pytest、`python scripts/validate-openspec-language.py` 和 `openspec validate improve-media-maintenance-storage-unreachable-summary --strict`。
