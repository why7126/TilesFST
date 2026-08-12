## ADDED Requirements

### Requirement: 推送前 Git 安全检测

系统 SHALL 提供 `/git-check` 治理命令，用于在提交或推送前检测 staged、modified tracked 和 untracked 文件中的真实环境文件、运行时数据、大文件、密钥、Token、连接串、本机绝对路径和不应进入 Git 的本地数据。

#### Scenario: 默认安全扫描

- **GIVEN** 用户运行 `/git-check`
- **WHEN** 当前 staged 或 tracked 文件包含真实 `.env`、数据库文件、运行时数据、密钥、Token、连接串或本机绝对路径
- **THEN** 命令 SHALL 输出脱敏 error 并返回非 0
- **AND** 命令不得删除文件、修改 `.gitignore` 或自动 unstage

#### Scenario: 安全通过

- **GIVEN** 用户运行 `/git-check`
- **WHEN** 扫描范围没有阻断项
- **THEN** 命令 SHALL 返回 0
- **AND** 输出扫描摘要、warning 摘要和后续建议

### Requirement: 跨项目学习应用命令

系统 SHALL 通过 `/spec-study` 支持跨项目 Harness / OpenSpec / Agent 治理学习，并在用户确认后按本项目 OpenSpec 与 Sprint 门禁应用治理资产。

#### Scenario: 日志优先学习

- **GIVEN** 用户运行 `/spec-study <学习对象>`
- **WHEN** 学习对象存在 `docs/spec-logs/CHANGELOG.md`
- **THEN** 命令 SHALL 先读取该总账作为治理演进入口地图
- **AND** 再按主题读取相关 `study` 或 `governance` 单次日志
- **AND** 再横向校验 `AGENTS.md`、`rules/`、`docs/`、Agent 目录、`scripts/`、部署与环境示例等真实治理资产
- **AND** 若日志与真实资产存在漂移，候选清单 SHALL 标注漂移风险并以当前真实资产为最终依据

#### Scenario: 学习对象只读保护

- **GIVEN** 用户运行 `/spec-study` 或 `/spec-study apply`
- **WHEN** 学习对象为本地路径
- **THEN** 命令 SHALL 只读访问学习对象
- **AND** 不得在学习对象内写入、安装、生成、格式化、迁移、清理、提交、切换分支或修改 Git 状态

### Requirement: 命令引导式反馈

系统 SHALL 在命令需要用户选择、确认、补充信息或处理阻塞时提供结构化反馈，并避免用大段开放式追问替代关键决策。

#### Scenario: 使用原生交互卡片或降级文本

- **GIVEN** 命令需要用户做出 1 到 3 个关键决策
- **WHEN** 当前客户端或工具层支持原生交互卡片
- **THEN** 命令 SHOULD 使用原生交互卡片展示结构化选项、推荐项和可补充说明入口
- **AND** 当原生交互卡片不可用时，命令 SHALL 降级为文本结构化选项并说明降级原因
