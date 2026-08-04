---
requirement_id: REQ-0097-prod-compose-media-maintenance-job
title: 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行 - 验收标准
acceptance_status: passed
created_at: 2026-08-04 10:37:36
updated_at: 2026-08-04 23:12:32
---

# 验收标准

## 功能 AC

- [x] AC-001 生产维护任务主入口明确以 `deploy/prod/compose.tencent-cos.yml` 为当前推荐生产 Compose，根目录生产 Compose 仅作为兼容入口说明。
- [x] AC-002 维护任务可通过 Docker Compose 一次性容器执行，且不要求将生产 `.env`、数据库连接串或对象存储密钥下载到开发机。
- [x] AC-003 维护任务镜像策略明确：专用 `tilesfst-maintenance` 服务/镜像优先；若复用 `tilesfst-backend`，必须证明不改变在线服务启动命令、端口和健康检查语义。
- [x] AC-004 维护脚本支持外部 MySQL，不得在生产 `APP_ENV=production` 下回退 SQLite。
- [x] AC-005 维护脚本支持腾讯云 COS / S3 兼容对象存储 provider，并通过后端配置或对象存储适配层访问对象。
- [x] AC-006 所有写数据库或对象存储的任务必须支持 dry-run / apply 两阶段，且 dry-run 不写数据库、不写对象存储、不删除对象。
- [x] AC-007 apply 必须要求显式参数触发，并在文档或命令输出中提示 MySQL 快照和对象存储 bucket / prefix 快照前置条件。
- [x] AC-008 维护任务支持 limit、batch size、范围过滤或等价分批控制方式，避免一次性处理不可控数据集。
- [x] AC-009 维护任务重复执行时能识别 already_done、skipped 或等价状态，不重复破坏数据库引用或生成冲突对象。
- [x] AC-010 dry-run / apply / 二次审计输出必须包含成功、失败、跳过、重试候选和失败原因统计。
- [x] AC-011 日志和报告不得输出真实密钥、数据库连接串、Authorization header、Cookie、生产 `.env` 原文、本机绝对路径或真实客户敏感数据。
- [x] AC-012 维护任务执行后必须输出媒体四联或五联验收摘要，覆盖 key、object、URL、thumbnail benefit、render 或明确 N/A / blocked 原因。
- [x] AC-013 Object Key 迁移、缩略图回填、SKU 暂存主图正式化和二次审计至少有接入规则或明确排期，不得以一次性手工脚本替代治理入口。
- [x] AC-014 回滚说明以恢复 MySQL 快照和对象存储快照为主；未验证反向脚本不得被描述为默认可靠回滚。
- [x] AC-015 真实生产执行证据应保存在受控运维证据位置或后续指定事实源中，仓库内不得提交真实备份、真实对象导出或生产 `.env`。

## 文档与治理 AC

- [x] AC-DOC-001 后续 OpenSpec Change 必须同步 Dockerfile、Compose、deploy env 示例、部署文档、媒体文档、对象存储文档和测试计划中受影响部分。
- [x] AC-DOC-002 若新增环境变量，必须同步 `.env.example`、`deploy/**/*.env.example` 或对应 env 示例，并为每个变量补充用途、安全边界和候选值说明。
- [x] AC-DOC-003 若新增维护镜像或 Compose service，必须纳入发布镜像准备和 image manifest 输入追踪。
- [x] AC-DOC-004 若涉及 API、DB schema 或 Orval 生成类型变化，必须在后续 Change 中明确同步项；本需求默认不直接新增对外 API。

## 横切 AC（knowledge-base）

本 REQ 为生产运维 / 后端维护任务，不新增管理端列表、表单、弹窗或媒体上传 UI，因此知识库 UI 横切标签为 N/A。以下复盘经验已转化为功能 AC：

| 来源 | 转化到 |
|---|---|
| `docs/knowledge-base/retrospectives/sprint-016-retrospective.md` 媒体五联、dry-run/apply、对象存储安全输出 | AC-006、AC-010、AC-012 |
| `docs/knowledge-base/retrospectives/sprint-017-retrospective.md` 跨端媒体证据拆分、存量补齐脱敏输出 | AC-010、AC-011、AC-012 |
| `docs/knowledge-base/retrospectives/sprint-018-retrospective.md` deploy 矩阵、Compose profile、env 示例不得泄密、发布验收补充项语义 | AC-001、AC-002、AC-DOC-002、AC-DOC-003 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: add-prod-media-maintenance-jobs
source_sprint: null
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

