# batch-image-processing-runbook Specification

## Purpose

定义批量图片处理 Runbook 的长期事实源、版本使用文档投影、生产执行安全门禁和验收证据模板要求。

## Requirements
### Requirement: 批量图片处理 Runbook 必须双投影

系统 MUST 提供批量图片处理 Runbook。Runbook MUST 以 `docs/` 下长期文档作为事实源，并 MUST 投影到 `releases/vX.Y.Z/usage-docs/` 或等价版本使用文档快照。双投影 MUST 保留相同的核心执行步骤、安全门禁、验收证据模板和适用版本说明。

#### Scenario: 长期事实源与版本快照同时存在

- **WHEN** 团队发布包含批量图片处理 Runbook 的版本
- **THEN** `docs/` 下 MUST 存在长期 Runbook 事实源
- **AND** 目标 `releases/vX.Y.Z/usage-docs/` MUST 存在该 Runbook 的版本快照或索引投影
- **AND** 投影记录 MUST 标明源路径、快照路径、适用版本和更新时间。

#### Scenario: 双投影关键章节一致

- **WHEN** 团队校验批量图片处理 Runbook
- **THEN** 长期事实源与版本快照 MUST 同时覆盖图片转换脚本、`thumb` / `display` 派生生成、缩略图专项重建、对象 key 迁移、生产执行步骤、安全门禁和验收证据模板
- **AND** 任一投影缺失关键章节时 MUST 阻断验收通过。

### Requirement: Runbook 必须明确图片处理脚本清单

Runbook MUST 提供图片处理脚本清单，覆盖图片转换脚本、`thumbnail` / `display` 派生生成、缩略图专项重建、对象 key 迁移和二次审计入口。每个脚本或入口 MUST 标注状态、用途、执行环境、参数、dry-run 支持、apply 支持、输入输出、幂等性和脱敏要求。未实现或未验证的脚本 MUST 标注为待实现或预留，MUST NOT 提供生产 apply 命令。

#### Scenario: 脚本状态可区分

- **WHEN** 运维阅读 Runbook 脚本清单
- **THEN** 每个脚本或入口 MUST 明确标注现有可用、需修改、需新增、仅预留或不适用
- **AND** 未实现脚本 MUST NOT 被描述为可直接执行
- **AND** 生产 apply 示例 MUST 只出现在已验证支持 apply 的入口中。

#### Scenario: 生产推荐命令使用语义化任务名

- **WHEN** Runbook、部署文档或 usage docs 模板提供可复制的生产媒体维护聚合命令
- **THEN** 推荐命令 MUST 使用 `media-drift-reconcile` 或等价语义化任务名
- **AND** 历史 BUG 编号任务名 MUST 仅作为兼容别名或历史来源说明
- **AND** 推荐生产命令 MUST NOT 要求执行者复制带具体 BUG 编号的任务名。

#### Scenario: 派生图生成入口说明完整

- **WHEN** Runbook 描述 `thumbnail` 与 `display` 派生生成
- **THEN** 文档 MUST 说明输入图片范围、目标规格、输出 key 规则、MIME、质量或体积目标、失败分类、重试建议和二次审计方式
- **AND** 文档 MUST 明确 `display` 与 `thumbnail` 分别读取对应配置或规格约束
- **AND** 文档 MUST 说明无法生成派生图时的跳过、失败或后续补齐策略。

### Requirement: Runbook 必须覆盖缩略图专项重建

Runbook MUST 提供缩略图专项重建流程，覆盖候选识别、dry-run 摘要、备份确认、apply 显式触发、幂等复跑、失败分类、对象存储不可达阻断和二次审计。缩略图专项重建 MUST NOT 默认把原图 fallback 写作性能通过证据。

#### Scenario: 缩略图重建 dry-run 不写入

- **WHEN** 运维按 Runbook 执行缩略图专项重建 dry-run
- **THEN** dry-run MUST 输出待重建数量、已存在数量、跳过原因、失败分类、预计写入对象和风险摘要
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST 脱敏。

#### Scenario: 缩略图重建二次审计

- **GIVEN** 缩略图专项重建 apply 已完成
- **WHEN** 运维执行二次审计
- **THEN** 审计 MUST 覆盖 key、object、URL、render 和 benefit
- **AND** benefit MUST 对比缩略图与原图的 bytes、像素或等价性能收益
- **AND** 原图 fallback MUST NOT 被记录为缩略图性能通过。

### Requirement: Runbook 必须覆盖对象 key 迁移

Runbook MUST 提供对象 key 迁移流程，覆盖迁移候选识别、旧 key 与新 key 映射、dry-run、apply、数据库引用更新、对象复制或移动策略、幂等复跑、失败清单、二次审计和回滚说明。对象 key 迁移的默认回滚 MUST 以 MySQL 快照和对象存储 bucket / prefix 快照恢复为主；未验证反向脚本 MUST NOT 被描述为默认可靠回滚。

#### Scenario: 对象 key 迁移前置门禁

- **WHEN** 运维准备执行对象 key 迁移 apply
- **THEN** Runbook MUST 要求已完成 dry-run 并记录摘要
- **AND** Runbook MUST 要求已确认 MySQL 快照
- **AND** Runbook MUST 要求已确认对象存储 bucket 或 prefix 快照
- **AND** Runbook MUST 要求执行窗口、影响范围和回滚负责人已记录。

#### Scenario: 对象 key 迁移验收

- **GIVEN** 对象 key 迁移 apply 已完成
- **WHEN** 团队验收迁移结果
- **THEN** 验收 MUST 记录旧 key、新 key、数据库引用、对象存在性、受控 URL、端侧 render 和失败项处理
- **AND** 重复执行 MUST 幂等跳过已迁移或不适用记录
- **AND** 验收证据 MUST 脱敏 object key 或使用可复核摘要。

### Requirement: Runbook 必须定义生产执行安全门禁

Runbook MUST 定义批量图片处理生产执行安全门禁。任何写数据库或对象存储的任务 MUST 默认先 dry-run，apply MUST 显式触发，并 MUST 在执行前确认数据库快照、对象存储 bucket / prefix 快照、执行窗口、回滚路径和脱敏日志策略。Runbook MUST NOT 要求将生产 `.env`、数据库连接串或对象存储密钥下载到开发机。

#### Scenario: 生产执行不泄露敏感信息

- **WHEN** Runbook 提供生产执行命令、日志示例或验收证据模板
- **THEN** 内容 MUST NOT 包含真实 `.env`、数据库连接串、对象存储 access key、secret key、Authorization header、Cookie、本机绝对路径、真实客户数据、生产私有 URL 或未脱敏 object key 全量值
- **AND** 命令示例 MUST 使用变量名、占位符或脱敏摘要。

#### Scenario: apply 必须显式确认

- **WHEN** 批量图片处理任务可能写数据库或对象存储
- **THEN** Runbook MUST 要求默认执行 dry-run
- **AND** apply MUST 使用显式参数或等价确认
- **AND** 未完成备份确认、对象存储可达性检查或风险摘要确认时 MUST 阻断 apply。

### Requirement: Runbook 必须提供验收证据模板

Runbook MUST 提供批量图片处理验收证据模板。模板 MUST 覆盖 dry-run、apply、二次审计、key、object、URL、render、benefit、失败分类、阻断原因、重试建议和人工补证步骤。模板 MUST 支持缩略图专项重建、`display` 派生生成和对象 key 迁移分别记录专项证据。

#### Scenario: 验收证据可支持发布交付

- **WHEN** 团队完成批量图片处理 Runbook 实现验收
- **THEN** 验收记录 MUST 包含长期 Runbook 路径、版本快照路径、脚本清单、dry-run 示例、apply 门禁、二次审计模板和脱敏检查结论
- **AND** 若未执行真实生产任务，验收 MUST 明确标注未执行生产任务及原因
- **AND** 记录 MUST 能支持发布前检查和后续 `/bug-capture` 或 `/req-capture` 追踪。
