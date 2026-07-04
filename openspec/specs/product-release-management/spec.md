# 产品版本发布管理规范

## Purpose
定义产品版本发布对象、公开 Mintlify 发布公告、发布前门禁，以及受治理的 `releases/` 目录，用于将一个或多个 Sprint 的交付内容整理为一个对外产品版本。
## Requirements
### Requirement: 产品版本发布对象
系统 SHALL 支持产品版本发布对象，用于表示一次对外产品版本发布，并可将该发布关联到一个或多个 Sprint。

#### Scenario: 一个产品版本关联多个 Sprint
- **WHEN** 为某个版本创建产品发布对象
- **THEN** 发布对象 SHALL 支持关联一个或多个 Sprint ID。
- **AND** 发布对象 SHALL 区分产品发布范围与 Sprint 级 `release-note.md` 范围。

#### Scenario: 发布范围可追溯
- **WHEN** 从关联 Sprint 准备发布范围
- **THEN** 发布对象 SHALL 追踪相关 REQ、BUG 和 OpenSpec Change。
- **AND** 每个正式发布项 SHALL 可追溯到来源 issue 或 change 文档。

#### Scenario: 未完成工作不得进入正式发布范围
- **WHEN** REQ、BUG、Sprint 或 OpenSpec Change 未评审、未纳入交付范围，或未按要求归档
- **THEN** 发布流程 SHALL 将其排除在正式发布范围之外。
- **AND** 流程 MAY 仅以“已知问题”或“后续计划”列出，并使用明确的非发布措辞。

### Requirement: 公开 Mintlify 发布公告
产品版本发布管理能力 SHALL 生成或维护面向公开展示的 Mintlify 静态文档发布公告源文件。

#### Scenario: 公告为静态公开文档
- **WHEN** 准备发布公告
- **THEN** 公告 SHALL 以适合 Mintlify 的静态文档源文件编写。
- **AND** 公告展示 SHALL NOT 依赖后端运行时 API 或数据库查询。

#### Scenario: 公告构建或预览校验
- **WHEN** 发布准备流程运行校验
- **THEN** 流程 SHALL 执行 Mintlify build、preview 或已文档化的等价校验步骤。
- **AND** 校验失败 SHALL 阻断发布确认。

#### Scenario: 公告源文件可评审
- **WHEN** 创建发布公告源文件
- **THEN** 文件 SHALL 适合 Git Review。
- **AND** 当 metadata 记录发布时间时，SHALL 使用项目标准时间字段 `YYYY-MM-DD HH:mm:ss`。

### Requirement: 发布公告内容结构
每份产品发布公告 SHALL 包含客户、店主、实施、运维和项目团队所需的最小公开发布内容。

#### Scenario: 必填公告章节
- **WHEN** 生成产品发布公告
- **THEN** 公告 SHALL 包含版本号、发布时间、关联 Sprint 列表、新增功能、修复 BUG、发布说明、已知问题、升级步骤、回滚说明和影响范围。

#### Scenario: 影响范围分类
- **WHEN** 记录影响范围
- **THEN** 文档 SHALL 区分 Web 管理端、店主 Web、小程序、后端、数据库、对象存储和 Docker 影响。

#### Scenario: 公开安全边界
- **WHEN** 评审公告内容
- **THEN** 公告 SHALL NOT 暴露密钥、真实客户数据、私有数据库连接串、MinIO 凭据、非公开域名或敏感运维细节。

### Requirement: 发布前校验门禁
发布流程 SHALL 在必填发布就绪检查通过前阻断发布确认；若某项不适用，必须明确标记不适用并说明理由。

#### Scenario: 必填发布检查
- **WHEN** 发布准备流程运行
- **THEN** 流程 SHALL 检查 OpenSpec 归档状态、测试、Orval 同步、Docker Compose 同步、数据库迁移同步、`.env.example` 同步、`PRODUCT_VERSION` 一致性，以及 Mintlify build 或 preview 校验。

#### Scenario: API 变更门禁
- **WHEN** 发布范围包含 API 变更
- **THEN** 发布门禁 SHALL 要求提供 OpenAPI 与 Orval 同步证据。

#### Scenario: 数据库变更门禁
- **WHEN** 发布范围包含数据库变更
- **THEN** 发布门禁 SHALL 要求提供迁移、数据库文档和回滚说明证据。

#### Scenario: 门禁失败阻断发布
- **WHEN** 任一必填发布门禁失败
- **THEN** 发布确认 SHALL 停止。
- **AND** 流程 SHALL 报告失败门禁和建议修复方式。

### Requirement: releases 目录治理
项目 SHALL 在目录规则更新后，使用受治理的顶层 `releases/` 目录存放产品版本发布对象和公开发布公告源文件。

#### Scenario: 使用前更新目录规则
- **WHEN** 实现创建顶层 `releases/` 目录
- **THEN** `rules/directory-structure.md` SHALL 已定义该目录职责、边界、命名规则和生命周期。
- **AND** AGENTS 指南 SHALL 在描述允许的顶层目录时提及该目录。

#### Scenario: 目录关系已文档化
- **WHEN** 引入 `releases/`
- **THEN** 文档 SHALL 说明它与 `iterations/`、`issues/`、`openspec/changes/`、已归档 specs 和 Mintlify 文档源的关系。

#### Scenario: 目录边界
- **WHEN** 发布产物存放在 `releases/` 下
- **THEN** 这些产物 SHALL 表示产品发布材料和公开公告源文件。
- **AND** 它们 SHALL NOT 替代 Sprint 四件套、issue 文档、OpenSpec changes 或运行时部署数据。

### Requirement: 发布命令族
项目 SHALL 定义用于提议、准备和确认产品发布的 release 命令族。

#### Scenario: 命令事实源
- **WHEN** 新增或修改 release 命令
- **THEN** `.cursor/commands/` SHALL 作为事实源。
- **AND** SHALL 运行 `python scripts/sync-agent-commands.py` 或已文档化的等价同步流程。

#### Scenario: release propose 命令
- **WHEN** 使用 release proposal 命令
- **THEN** 它 SHALL 为某个产品版本和选定 Sprint 范围创建或更新产品发布计划。

#### Scenario: release prepare 命令
- **WHEN** 使用 release preparation 命令
- **THEN** 它 SHALL 运行发布门禁，并生成或更新 Mintlify 公告源文件。

#### Scenario: release publish 命令
- **WHEN** 使用 release publish 或确认命令
- **THEN** 它 SHALL 记录发布确认凭据，且不引入 draft、pending、published、retracted 状态机。

### Requirement: 不新增应用内公告入口
产品版本发布管理能力 SHALL NOT 在管理端菜单、登录页、店主 Web 或小程序内新增发布公告入口。

#### Scenario: 不新增管理端菜单入口
- **WHEN** 实现产品版本发布管理
- **THEN** Web 管理端 sidebar 或菜单 SHALL NOT 新增发布公告入口。

#### Scenario: 不新增店主端或小程序入口
- **WHEN** 产品发布公告发布
- **THEN** 店主 Web 和小程序 SHALL NOT 作为本能力的一部分新增发布公告入口。

#### Scenario: 不新增后端公告服务
- **WHEN** 实现发布公告
- **THEN** 实现 SHALL NOT 新增后端公告 API 或数据库表，除非后续 OpenSpec Change 明确要求。
