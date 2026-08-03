## ADDED Requirements

### Requirement: Sprint close stale scan 工具输出
系统 SHALL 提供命令式 stale scan 能力，基于目标 Sprint 四件套、`sprint.yaml` 范围和关联 Change 状态输出稳定、可执行的检查报告。

#### Scenario: 扫描指定 Sprint
- **WHEN** 用户或 `/sprint-archive` 调用 stale scan 并指定 `sprint-xxx`
- **THEN** 系统 MUST 只读取该 Sprint 的四件套和由 `sprint.yaml` 指向的关联 Issue、Change 状态证据
- **AND** 系统 MUST NOT 默认扫描全部 `iterations/**`、`openspec/archive/**` 或历史归档目录

#### Scenario: 报告包含可执行修复建议
- **WHEN** stale scan 发现 blocker
- **THEN** 报告 MUST 包含建议命令或修复路径，例如重新运行 Workflow Sync、运行目录结构校验、执行归档路径 residual 修复或手工更新非派生人工说明
- **AND** 报告 MUST 明确禁止手工编辑 `sprint.md` workflow-sync marker 派生块

#### Scenario: 自动刷新后保持幂等
- **WHEN** Workflow Sync 或 Sprint close 流程刷新四件套派生块
- **THEN** 系统 MUST 清除由机器事实可确定的过期规划文案
- **AND** 再次运行 stale scan MUST 不因同一派生命中重复失败

#### Scenario: 无法解析 Sprint 时失败
- **WHEN** stale scan 通过 `--sprint auto` 或等价方式无法解析唯一目标 Sprint
- **THEN** 系统 MUST 返回非零退出码
- **AND** 报告 MUST 要求显式传入目标 `sprint-xxx`

### Requirement: Sprint close stale scan 例外边界
系统 SHALL 明确定义 legacy 字符串和中间态文案的允许例外，避免自动化误伤迁移、兼容读取和回归测试。

#### Scenario: 测试与迁移文件中的 legacy 字符串不阻断
- **WHEN** stale scan 命中测试 fixture、迁移脚本、兼容读取逻辑或 residual scanner 自身的 `openspec/changes/archive/` 字符串
- **THEN** 系统 MUST 将命中标记为允许例外
- **AND** 系统 MUST NOT 因该例外阻断目标 Sprint close

#### Scenario: 新生成 Sprint 事实不得使用 legacy 路径
- **WHEN** Workflow Sync、Sprint close、Fact Sheet、release note 或 acceptance report 生成新的归档路径事实
- **THEN** 系统 MUST 使用 `openspec/archive/`
- **AND** 系统 MUST NOT 将 `openspec/changes/archive/` 作为 canonical archive path 写入新事实
