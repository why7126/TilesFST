---
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
title: 版本部署升级与回滚治理能力 - 验收标准
acceptance_status: pending
created_at: 2026-08-21 18:34:27
updated_at: 2026-08-21 22:13:10
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：系统能够校验目标版本的 `release.json.version`、`PRODUCT_VERSION`、image manifest `image_tag`、Git tag / commit 和部署 env `TILESFST_IMAGE_TAG` 的一致性，缺失或漂移时按规则输出 blocker 或 warning。
- [ ] AC-002：系统能够为每条部署或升级路径输出支持级别，支持级别至少包含 `fresh-install-supported`、`adjacent-upgrade-supported`、`cross-version-upgrade-supported`、`cross-version-upgrade-requires-manual-review` 和 `unsupported`。
- [ ] AC-003：缺少跨版本演练、中间版本 release 事实源或关键证据时，系统不得将跨版本升级标记为 `cross-version-upgrade-supported`。
- [ ] AC-004：系统能够生成 `from_version -> to_version` 升级路径对象，包含来源版本、目标版本、支持级别、来源事实可信度、影响摘要、升级前检查、升级步骤、回滚步骤、blocker、warning 和证据摘要。
- [ ] AC-005：升级路径对象不得包含真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。
- [ ] AC-006：系统能够生成目标版本首次部署计划，覆盖目标 release、image manifest、生产 env 检查、MySQL 空库初始化、对象存储配置、Docker Compose config、首次管理员初始化和部署后 smoke。
- [ ] AC-007：首次部署计划通过后，系统能够以证据驱动方式将该路径标记为 `fresh-install-supported`。
- [ ] AC-008：系统能够生成上一发布版本到目标版本的相邻升级计划，覆盖目标镜像校验、env diff、DB 影响判断、备份确认、`TILESFST_IMAGE_TAG` 更新、服务重启策略和升级后 smoke。
- [ ] AC-009：相邻升级回滚计划必须覆盖旧镜像 tag 或旧离线包、旧 env 摘要、DB 备份恢复条件、对象存储写入影响和回滚后 smoke。
- [ ] AC-010：系统能够生成指定旧版本到目标版本的跨版本升级计划，并聚合中间版本的 DB、env、Docker、API、对象存储和生产维护任务影响。
- [ ] AC-011：跨版本升级计划必须明确必须 dry-run 的维护任务、必须人工确认或演练的步骤、是否需要先升中间版本，以及支持级别降级原因。
- [ ] AC-012：跨版本回滚计划必须明确全量备份要求、旧镜像和旧 env 恢复方式、DB 回滚边界、对象存储写入不可逆风险和回滚后 smoke。
- [ ] AC-013：env diff 能力必须覆盖 `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`、`deploy/**/*.env.example` 和 `scripts/build-images.env.example`。
- [ ] AC-014：env diff 输出必须包含 added、removed、changed_default、required_in_production、unsafe_example_value、manual_review 等分类；只输出变量名、分类、说明和修复建议，不输出真实生产 env 值。
- [ ] AC-015：数据库升级验证必须记录 SQLite schema、MySQL schema、migration、`schema_migrations` 或等价版本记录、目标 MySQL drift/smoke、DB 备份和关键业务读写 smoke。
- [ ] AC-016：当升级影响数据库时，升级计划必须要求 MySQL drift 或目标 MySQL smoke、备份和回滚证据；不得仅凭本地 SQLite 测试通过宣称生产 DB 升级安全。
- [ ] AC-017：回滚证据必须结构化记录 previous_image、target_image、env_snapshot、database_backup、object_storage_backup 或只读确认、rollback_steps 和 post_rollback_smoke。
- [ ] AC-018：缺少必要回滚证据时，升级计划必须标记为 blocked 或 requires manual review。
- [ ] AC-019：upgrade 相关命令不得自动执行生产升级，不得自动修改真实 env，不得自动执行写入型 DB 或对象存储维护任务。
- [ ] AC-020：upgrade 相关命令必须接入 Workflow Sync / AI Usage 输出契约，并在需要用户确认时输出结构化选项、推荐项、阻塞项和下一步。

## 非功能 AC

- [ ] AC-NF-001：升级计划、回滚证据、命令输出和发布记录不得泄露密钥、真实 `.env`、数据库连接串、对象存储凭据、Authorization header、Cookie 或真实客户数据。
- [ ] AC-NF-002：升级支持级别必须由证据驱动，缺少证据时降级为 requires manual review 或 unsupported。
- [ ] AC-NF-003：升级计划必须复用现有 release、image、deploy、DB 和 maintenance 脚本，不创建互相竞争的平行发布事实源。
- [ ] AC-NF-004：跨版本分析必须遵守上下文预算治理，先定位版本和影响摘要，不默认全量展开历史归档、OpenAPI 生成物、大日志或镜像 manifest 全文。
- [ ] AC-NF-005：命令输出必须面向发布、实施、运维和评审读者，优先展示来源版本、目标版本、支持级别、blocker、warning、升级前检查、升级步骤、回滚步骤和证据缺口。

## 横切 AC（knowledge-base）

本 REQ 为发布治理 / 部署升级 / 回滚治理能力，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: add-version-deployment-upgrade-rollback-governance
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: opsx.modify
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```

