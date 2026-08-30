## 1. 后端 CLI

- [x] 1.1 为媒体维护 CLI 增加可选 `--progress` 参数，默认关闭。
- [x] 1.2 实现可复用进度输出机制，支持任务名、阶段、总量、已完成、成功、失败、跳过和百分比。
- [x] 1.3 确保最终 JSON 继续输出到 stdout，进度输出写入 stderr 或等价隔离通道。
- [x] 1.4 为 `backfill-brand-certificate-thumbnails` 接入 dry-run 和 apply 进度。
- [x] 1.5 为 `backfill-image-variants` 接入 dry-run 和 apply 进度，并明确 item 进度与 `estimated_writes` 的计数口径。
- [x] 1.6 为 `media-drift-reconcile` 接入阶段级进度，覆盖 SKU pending 主图正式化、证书图片 key 迁移、缩略图回填和对象 key 审计。
- [x] 1.7 更新 CLI help 文案，说明进度参数不会改变最终 JSON stdout。

## 2. 文档

- [x] 2.1 更新生产媒体维护 Runbook 或批量图片处理 Runbook，说明 `--progress` 用法。
- [x] 2.2 在 Runbook 中补充 stdout / stderr 边界、示例输出、日志采集方式和审计归档注意事项。
- [x] 2.3 在文档中声明本变更不涉及 API、DB、Web、管理端、小程序、Orval、对象 key 策略或生产备份确认门禁。

## 3. 测试

- [x] 3.1 补充测试验证默认不启用进度时 stdout JSON 结构保持兼容。
- [x] 3.2 补充测试验证启用进度后 stderr 有进度输出，stdout 仍可被 JSON 解析。
- [x] 3.3 补充测试验证 `completed`、`success`、`failed`、`skipped` 和 `progress_percent` 计算正确。
- [x] 3.4 补充测试验证 `media-drift-reconcile` 输出阶段级进度。
- [x] 3.5 补充测试验证进度输出不包含真实 object key、`.env`、密钥、连接串、Authorization header 或 Cookie。

## 4. 验证

- [x] 4.1 运行相关后端测试。
- [x] 4.2 运行 OpenSpec 严格校验。
- [x] 4.3 记录 dry-run 或测试环境命令输出证据，确保样例已脱敏。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-29 21:46:01 | `media-drift-reconcile --progress` 进入 `business_id_media_key_migration` 后长时间没有新输出，无法判断完成数量或卡在对象存储/数据库。 | 聚合任务向子任务透传进度上下文；子任务内部输出 item 级心跳；`business_id_media_key_migration` 在 `checking_source`、`checking_target`、`copying_object`、`updating_db` 前输出脱敏状态。 | `uv run pytest tests/test_deploy_media_maintenance_script.py` 12 passed；OpenSpec、语言、目录与观测门禁通过。 |
