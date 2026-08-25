---
requirement_id: REQ-0122-batch-image-processing-runbook
acceptance_status: passed
lifecycle_stage: archive
created_at: 2026-08-25 09:26:23
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 功能 AC

- [x] AC-001 Runbook 明确长期技术文档归属 `docs/`，并明确版本发布需要时投影到 `releases/vX.Y.Z/usage-docs/`，两者通过 manifest 或等价索引保持可追溯。
- [x] AC-002 Runbook 明确图片转换脚本的输入范围、支持格式、输出格式、目标尺寸或体积策略、执行模式、日志位置和失败处理。
- [x] AC-003 Runbook 明确 `thumbnail / display / original` 三类资源的生成关系、对象 key 规则、MIME/格式策略、尺寸或体积目标、失败降级和字段回填边界。
- [x] AC-004 Runbook 提供缩略图专项重建步骤，覆盖品牌 Logo、证书图片、SKU 商品图、Banner 或其他适用媒体类型，并支持范围过滤和幂等重跑说明。
- [x] AC-005 Runbook 覆盖对象 key 迁移流程，包括迁移前盘点、映射规则、目标 key 冲突检查、dry-run、apply、数据库引用回填、兼容读取、回滚和二次审计。
- [x] AC-006 Runbook 明确生产执行步骤，包含环境确认、备份、dry-run、人工复核、apply、分批执行、中止条件、验收和收尾记录。
- [x] AC-007 Runbook 建立安全门禁清单，禁止泄露真实 `.env`、密钥、数据库连接串、Authorization header、Cookie、本机绝对路径、生产私有域名和真实客户数据。
- [x] AC-008 Runbook 的写入型命令必须要求 dry-run 通过、备份完成和人工确认；删除对象或清理历史对象必须作为高风险动作单独确认。
- [x] AC-009 Runbook 提供验收证据模板，覆盖执行摘要、对象存储抽样、数据库或接口校验、端侧展示验证、thumbnail/display 收益、安全复核和回滚判断。
- [x] AC-010 Runbook 对 API、数据库、Orval、Docker Compose、对象存储、Web、小程序和管理端给出影响矩阵；不涉及项必须写“不涉及”。
- [x] AC-011 Runbook 明确现有脚本、后续改造脚本和后续新增脚本；未交付能力必须标注后续治理范围，不得写作生产可直接执行事实。
- [x] AC-012 Runbook 验收模板允许记录 blocked 补证项；缺少生产截图、日志、对象抽样或端侧证据时不得伪造通过。

## 媒体批处理证据 AC

- [x] AC-MEDIA-001 对象 key 证据必须说明源 key、目标 key、标准前缀、分类边界和脱敏规则，图片证书与 PDF/文档证书归属不得混淆。
- [x] AC-MEDIA-002 对象存储证据必须说明对象存在性、MIME、大小、权限、派生关系、缺失对象和失败对象清单。
- [x] AC-MEDIA-003 URL 证据必须说明后端受控 `/media/{object_key}`、签名 URL、对象存储直出或 CDN URL 的选择条件、过期策略、缓存和 fallback。
- [x] AC-MEDIA-004 `thumbnail/display` 收益证据必须说明缩略图或展示图真实生成，体积、尺寸、加载或展示收益可解释；名义存在但无收益不得写作通过。
- [x] AC-MEDIA-005 render 证据必须覆盖受影响的管理端、店主 Web 或小程序场景；无法补齐 DevTools、真机、体验版或截图时必须标记 blocked。
- [x] AC-MEDIA-006 dry-run/apply 证据必须说明影响数量、成功、失败、跳过、重试候选、失败原因统计和幂等重跑结果。

## 文档投影 AC

- [x] AC-DOC-001 长期 Runbook 只沉淀当前事实和安全边界，不写入会话推理、临时草稿、未脱敏日志或生产执行原始敏感材料。
- [x] AC-DOC-002 版本使用文档快照继承或投影长期 Runbook 时，manifest 记录来源、版本、生成时间、覆盖页面和维护边界。
- [x] AC-DOC-003 旧版本 Runbook 快照默认冻结；内容性更正必须记录更正原因、操作者或确认来源、时间、文件范围和变更说明。
- [x] AC-DOC-004 `mintlify/` 若投影发布 Runbook，只能承载公开站点源文件和公开截图资产，不替代 release 快照事实源。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002 媒体上传链路复发类缺陷

- [x] AC-XCUT-001 Runbook 涉及上传或派生图链路时，必须要求验证上传状态机 `idle -> uploading -> done/failed`；若本次仅处理历史对象而无上传入口，标注 `N/A — 仅历史对象批处理，不改变上传入口`。
- [x] AC-XCUT-002 Runbook 涉及上传后回显时，必须要求同会话即时回显证据；若本次不触发新上传，标注 `N/A — 无新上传回显场景`。
- [x] AC-XCUT-003 Runbook 涉及上传大小、Nginx 或 Docker Web 边界时，必须要求从 `http://localhost:3000` 或生产等价 Web 入口验证，不能只打后端 `:8000`。
- [x] AC-XCUT-004 Runbook 涉及媒体对象读取时，必须要求 `object_key` 与 `/media/` 代理一致性证据，覆盖脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现。
- [x] AC-XCUT-005 Runbook 必须确认新上传不会写入 `data/uploads/`，历史对象迁移或兼容读取不得把 legacy 路径作为新上传通过证据。
- [x] AC-XCUT-006 Runbook 涉及小程序媒体卡片或详情展示时，必须要求 DevTools、真机或体验版 evidence；缺证时必须标记 blocked 或进入 Release 前补证清单。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 12:03:49
accepted_by: workflow-sync
source_change: add-batch-image-processing-runbook
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 实现证据

| 维度 | 状态 | 证据 |
|---|---|---|
| docs | pass | `docs/standards/batch-image-processing-runbook.md` 为长期事实源，已加入 `docs/README.md` standards 索引。 |
| usage-docs | pass | `releases/templates/usage-docs/operations/batch-image-processing-runbook.mdx` 为版本投影模板，`releases/templates/usage-docs/manifest.json` 记录源路径、模板路径、目标投影路径和维护边界。 |
| script-inventory | pass | Runbook 脚本清单覆盖 `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`formalize-pending-tile-images`、`migrate-certificate-image-keys`、生产推荐聚合入口 `media-drift-reconcile`、历史兼容别名 `bug-0116-media-drift`、`object-key-audit`、兼容包装脚本和独立图片格式转换脚本的后续治理状态。 |
| safety-gate | pass | Runbook 覆盖 dry-run、MySQL 快照、bucket / prefix 快照、显式 `--apply --confirm-backup`、blocked 中止条件和敏感输出禁止清单。 |
| acceptance-template | pass | Runbook 覆盖 dry-run、apply、key、object、URL、render、benefit、idempotency、rollback、缩略图专项和对象 key 迁移专项模板。 |
| production-run | n/a | 本 Change 未执行真实生产图片处理任务，未写数据库或对象存储。 |

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-25 10:09:46 | `openspec validate add-batch-image-processing-runbook --strict` | pass |
| 2026-08-25 10:09:46 | `python scripts/validate-openspec-language.py` | pass |
| 2026-08-25 10:09:46 | `python scripts/validate-directory-structure.py` | pass |
| 2026-08-25 10:09:46 | `python scripts/validate-doc-prose-hygiene.py docs/standards/batch-image-processing-runbook.md releases/templates/usage-docs/operations/batch-image-processing-runbook.mdx` | pass：findings=0 |
