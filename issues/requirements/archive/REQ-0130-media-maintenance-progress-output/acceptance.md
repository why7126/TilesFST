---
requirement_id: REQ-0130-media-maintenance-progress-output
acceptance_status: passed
lifecycle_stage: review
created_at: 2026-08-29 18:08:25
updated_at: 2026-08-30 08:45:27
---

# 验收标准

## 功能 AC

- [x] AC-001 媒体维护 CLI 提供可选进度输出开关，推荐参数为 `--progress` 或等价命名。
- [x] AC-002 默认不启用进度输出时，stdout 仍只输出现有最终 JSON，现有 `jq` 和生产脚本解析不受影响。
- [x] AC-003 启用进度输出后，进度信息输出到 stderr 或等价隔离通道，最终 JSON 继续输出到 stdout。
- [x] AC-004 进度信息包含任务名、阶段、总量、已完成数量、成功数量、失败数量、跳过数量和进度百分比。
- [x] AC-005 `backfill-brand-certificate-thumbnails` 支持 dry-run 扫描和 apply 重生成过程中的进度输出。
- [x] AC-006 `backfill-image-variants` 支持 `.thumb.webp` / `.display.webp` 派生图扫描与写入进度，并说明一个源图多个派生写入的计数口径。
- [x] AC-007 `media-drift-reconcile` 支持 SKU pending 主图正式化、业务对象 ID 目录迁移、证书图片 key 迁移、缩略图回填和对象 key 审计阶段的进度展示。
- [x] AC-007A `media-drift-reconcile` 进入长耗时子任务后继续输出 item 级心跳，至少能判断当前子任务总量、已完成数量和进度百分比。
- [x] AC-007B `business_id_media_key_migration` 等对象迁移阶段在对象存储或数据库慢操作前输出枚举化状态，例如 `checking_source`、`checking_target`、`copying_object`、`updating_db`。
- [x] AC-008 apply 模式下，失败数量随处理过程更新；最终失败原因仍以 JSON 中 `failure_reasons` 和脱敏 item 为准。
- [x] AC-009 当任务无法预先计算准确总量时，进度输出明确总量口径或使用阶段级进度，不展示误导性百分比。
- [x] AC-010 生产媒体维护 Runbook 更新进度参数用法、stdout / stderr 边界、示例输出、日志采集和审计注意事项。
- [x] AC-011 CLI help 文案说明进度参数不会改变最终 JSON stdout。

## 安全与脱敏 AC

- [x] AC-SEC-001 进度输出不得包含真实 object key、原始文件名、客户信息、数据库连接串、对象存储 endpoint、access key、secret key、Authorization header、Cookie、真实 `.env` 内容或本机绝对路径。
- [x] AC-SEC-002 失败对象定位继续使用最终 JSON 的脱敏 hash、标准前缀和失败原因枚举，进度行不新增敏感定位信息。
- [x] AC-SEC-003 对象存储不可达或权限异常时，进度输出不得泄露底层凭据、私有 endpoint 或未脱敏异常堆栈。
- [x] AC-SEC-004 item 级心跳和 I/O 状态只输出枚举状态、计数和百分比，不输出真实 object key、文件名、数据库值或异常详情。

## 测试 AC

- [x] AC-TEST-001 补充测试验证默认命令 stdout JSON 兼容。
- [x] AC-TEST-002 补充测试验证启用进度后 stderr 有进度输出，stdout 仍可被 JSON 解析。
- [x] AC-TEST-003 补充测试验证 `completed`、`success`、`failed`、`skipped` 和 `progress_percent` 计算正确。
- [x] AC-TEST-004 补充测试验证 `media-drift-reconcile` 的阶段级进度输出。
- [x] AC-TEST-004A 补充测试验证 `business_id_media_key_migration` 的 item 级心跳和 I/O 状态输出。
- [x] AC-TEST-005 补充测试验证进度输出不包含真实 object key、`.env`、密钥、连接串或 Authorization/Cookie。

## 文档与影响 AC

- [x] AC-DOC-001 后续 OpenSpec Change、Runbook 和测试计划说明本需求不新增 Web、管理端或小程序 UI。
- [x] AC-DOC-002 后续实现说明不改变 API、数据库 Schema、Orval、对象 key 策略、派生图生成策略或生产备份确认门禁。
- [x] AC-DOC-003 后续实现若改为持久化任务进度、写入 Task Trace 或日志审计表，必须重新评估产品数据采集与链路观测门禁。
- [x] AC-DOC-004 验收记录包含 dry-run、apply 或测试中的进度输出样例，但样例必须脱敏。

## 横切 AC（knowledge-base）

本需求为后端 CLI 运维体验增强，不涉及管理端列表页、管理端表单页、管理端弹窗或媒体上传入口，未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签。知识库横切 AC：N/A。

## 产品数据采集与链路观测 AC

- [x] AC-OBS-001 需求、Change 和验收材料均声明本需求不新增 API、DB、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。
- [x] AC-OBS-002 若后续方案改变为持久化进度或写入任务链路观测数据，必须将 `product_data_collection_observability` 改为适用并补齐 affected layers、脱敏、保留周期和验证项。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-29 23:01:04
accepted_by: codex
source_change: add-media-maintenance-progress-output
source_sprint: sprint-027
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

