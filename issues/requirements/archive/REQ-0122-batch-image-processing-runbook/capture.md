---
req_id: REQ-0122-batch-image-processing-runbook
status: done
lifecycle_stage: archive
created_at: 2026-08-25 09:17:47
updated_at: 2026-08-25 12:05:38
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0115-media-multi-variant-images
captured_via: capture
classification_rationale: 用户描述为新增批量图片处理 Runbook，覆盖生产操作步骤、安全门禁与验收证据，属于尚未交付的运维文档和流程能力，不是现有能力偏差。
---

# 一句话

新增批量图片处理 Runbook，覆盖图片转换脚本、thumb/display 派生生成、缩略图专项重建、对象 key 迁移、生产执行步骤、安全门禁和验收证据。

# 原始描述

新增批量图片处理 Runbook，覆盖图片转换脚本、thumb/display 派生生成、缩略图专项重建、对象 key 迁移、生产执行步骤、安全门禁和验收证据。

# 背景与关联

- 父需求：`REQ-0115-media-multi-variant-images`
- 关联能力：媒体图片多规格展示图、对象存储 key 规范、生产媒体维护任务
- 涉及端与模块：docs/runbook、media maintenance、object storage、deploy/prod、release/upgrade 验收证据
- 业务价值：把批量图片处理和生产维护操作沉淀为可审计、可复跑、可验收的 Runbook，降低生产对象迁移、派生图重建和缩略图修复过程中的误操作风险。

# 影响范围

- 图片转换脚本：明确输入范围、输出格式、幂等策略、失败重试和日志位置。
- thumb/display 派生生成：说明派生规则、目标尺寸或体积策略、对象 key 命名与回填字段。
- 缩略图专项重建：提供按媒体类型、对象前缀或记录范围重建缩略图的操作步骤。
- 对象 key 迁移：覆盖迁移前盘点、dry-run、映射校验、回滚策略和兼容读取边界。
- 生产执行步骤：覆盖环境准备、备份、执行窗口、命令顺序、监控和回滚。
- 安全门禁：覆盖鉴权、最小权限、真实密钥保护、对象存储访问边界和危险命令禁止项。
- 验收证据：覆盖执行摘要、样例对象、接口或 DB 校验、对象存储抽样、前端/小程序展示检查和失败清单。

# 建议验收要点

- [ ] Runbook 明确批量图片转换、thumb/display 派生生成、缩略图专项重建和对象 key 迁移的适用场景与禁止场景。
- [ ] Runbook 包含生产执行前置检查、dry-run、备份、执行、监控、回滚和收尾验收步骤。
- [ ] Runbook 的命令示例不得包含真实 `.env`、密钥、生产私有域名、Authorization header、Cookie、本机绝对路径或真实客户数据。
- [ ] Runbook 验收证据模板覆盖对象存储抽样、数据库/接口字段校验、前端或小程序展示验证、失败对象清单和人工确认结论。
- [ ] Runbook 说明 API、数据库、Orval、Docker Compose、对象存储、Web、小程序和管理端影响；不涉及项需明确写“不涉及”。

# 待澄清

- [ ] Runbook 应归入长期技术文档 `docs/`、发布快照 `releases/vX.Y.Z/usage-docs/`，还是两者都需要投影。
- [ ] 批量处理脚本是否仅记录现有脚本用法，还是需要新增或改造脚本能力。
- [ ] 对象 key 迁移是否要求支持生产可回滚执行，还是仅提供人工操作指南和验收模板。

# 探索结论

（/req-explore 后人工确认写入）
