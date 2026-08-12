## MODIFIED Requirements

### Requirement: 规范优化命令 spec-opt

`/spec-opt` MUST 作为项目治理规范优化入口，用于新增或修改 `.agents/skills/` 命令、`rules/` 文档、`docs/` 文档规范、`scripts/` 治理脚本、`AGENTS.md` 入口和 active OpenSpec Change 文档。`/spec-opt` MUST 只修改治理资产，不得修改业务 `src/` 运行时代码。`/spec-opt` 完成本项目规范、技能或脚本迭代后，MUST 在 `docs/spec-logs/` 写入治理迭代日志。

#### Scenario: 新增或修改命令技能

- **WHEN** 用户要求新增或修改项目级命令技能
- **THEN** `/spec-opt` MUST 更新对应 `.agents/skills/<command>/SKILL.md`
- **AND** `/spec-opt` MUST 同步 `AGENTS.md` 命令入口或速查
- **AND** `/spec-opt` MUST 同步 `rules/agent-context-budget.md`
- **AND** `/spec-opt` MUST 更新相关 active OpenSpec Change 文档

#### Scenario: 新增或修改文档规范

- **WHEN** 用户要求新增或调整 `rules/`、`docs/` 或长期治理文档
- **THEN** `/spec-opt` MUST 更新对应规则或文档索引
- **AND** `/spec-opt` MUST 按文档治理规则更新 Markdown frontmatter `updated_at`
- **AND** `/spec-opt` MUST 更新相关 active OpenSpec Change 文档

#### Scenario: 新增或修改治理脚本

- **WHEN** 用户要求新增或调整 `scripts/` 下治理脚本、校验脚本或脚本说明
- **THEN** `/spec-opt` MUST 更新脚本、相关规则和相关 Skill 引用
- **AND** `/spec-opt` MUST 运行脚本级最小验证或对应测试

#### Scenario: 禁止业务实现

- **WHEN** 用户请求同时包含治理优化和业务实现
- **THEN** `/spec-opt` MUST 停止业务实现部分
- **AND** `/spec-opt` MUST 引导用户改用 `/capture`、`/req-*`、`/bug-*`、`/opsx-propose` 或对应业务流程

#### Scenario: 输出治理迭代日志

- **WHEN** `/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代
- **THEN** `/spec-opt` MUST 在 `docs/spec-logs/` 写入治理迭代日志
- **AND** 日志文件名 MUST 使用 `YYYYMMDDhhmmss-governance-xxx.md`
- **AND** `YYYYMMDDhhmmss` MUST 使用日志生成时刻的 `Asia/Shanghai` 日期时间，精确到秒
- **AND** `xxx` MUST 使用小写 kebab-case 表达治理主题
- **AND** 日志 MUST 包含迭代目标、变更摘要、影响范围、更新文件、验证结果和后续建议
- **AND** 日志 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
- **AND** 如需说明隐私相关风险，日志 MUST 使用脱敏占位符或聚合描述

### Requirement: Harness 学习同步技能

系统 MUST 提供 `/spec-study` 技能，用于学习其他项目的 Harness 工程，并在用户确认后将可复用的治理经验应用到本项目。

#### Scenario: 默认自动学习

- **WHEN** 用户执行 `/spec-study <学习对象>` 且未指定学习模式
- **THEN** 系统 MUST 默认使用自动学习模式
- **AND** 系统 MUST 综合分析项目入口、全局规范、Agent 能力目录、脚本、部署与环境示例
- **AND** 系统 MUST 输出候选学习内容，等待用户确认后才能应用

#### Scenario: 指定学习内容

- **WHEN** 用户执行 `/spec-study <学习对象> <指定学习内容>`
- **THEN** 系统 MUST 以指定主题为主线学习
- **AND** 系统 MUST 仍横向检查 `AGENTS.md`、`project.yaml`、`DOCUMENT_METADATA_INDEX.md`、`rules/`、`docs/`、Agent 目录、`scripts/`、部署与环境模块中的相关内容
- **AND** 系统 MUST NOT 只读取单一目录后得出迁移结论

#### Scenario: 支持本地项目和 GitHub URL

- **WHEN** 学习对象是本地项目路径
- **THEN** 系统 MUST 以只读方式扫描该路径的治理资产
- **AND** 系统 MUST 遵守上下文预算，先列清单、摘要，再按需读取片段
- **AND** 系统 MUST NOT 修改学习对象中的代码、文档、配置、依赖锁文件、Git 状态、缓存、生成物或运行时数据

- **WHEN** 学习对象是 GitHub 项目 URL
- **THEN** 系统 MUST 先说明需要获取远端只读快照
- **AND** 如需网络访问或 clone，系统 MUST 按当前权限策略请求批准
- **AND** 系统 MUST NOT 对学习对象执行 push、commit、checkout 覆盖、reset、clean 或任何写入远端/快照的操作

#### Scenario: 学习对象只读保护

- **WHEN** 系统学习任何本地项目、临时克隆目录或远端快照
- **THEN** 系统 MUST 把学习对象作为外部只读输入
- **AND** 系统 MUST NOT 在学习对象路径下运行安装依赖、格式化、迁移、生成、测试修复、提交、分支、清理或重置命令
- **AND** 学习报告 MUST 说明学习对象只读保护结果

#### Scenario: 应用前用户确认

- **WHEN** 系统完成学习阶段
- **THEN** 系统 MUST 告知用户学习到了哪些内容建议应用到本项目
- **AND** 系统 MUST 列出每项内容的理由、风险、拟更新目标文件和是否需要 OpenSpec/Sprint 承载
- **AND** 系统 MUST 等待用户确认学习内容，不得默认直接应用

#### Scenario: 确认后应用到本项目治理资产

- **WHEN** 用户确认应用某些学习内容
- **THEN** 系统 MUST 通过当前项目的 OpenSpec Change 和 Sprint Inclusion Gate 承载变更
- **AND** 系统 MAY 更新 `.agents/skills/`、`AGENTS.md`、`rules/`、`docs/`、`scripts/`、部署治理文件和 active Change 文档
- **AND** 系统 MUST NOT 修改 `src/` 目录下任何业务运行时代码

#### Scenario: 输出学习报告

- **WHEN** 系统完成应用阶段
- **THEN** 系统 MUST 输出学习报告
- **AND** 学习报告 MUST 写入 `docs/spec-logs/YYYYMMDDhhmmss-study-xxx.md`
- **AND** `YYYYMMDDhhmmss` MUST 使用报告生成时刻的 `Asia/Shanghai` 日期时间，精确到秒
- **AND** `xxx` MUST 使用小写 kebab-case 表达学习对象或主题
- **AND** 学习报告 MUST 包含学习对象、学习模式、采纳内容、未采纳内容、更新文件、验证结果和后续建议
- **AND** 学习报告 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
- **AND** 如需说明隐私相关风险，学习报告 MUST 使用脱敏占位符或聚合描述
- **AND** 最终回复 MUST 摘要说明学习到什么、具体应用了哪些内容、分别更新了哪些文档
