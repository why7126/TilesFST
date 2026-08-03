## ADDED Requirements

### Requirement: Sprint close stale scan 回归测试
测试治理 SHALL 要求 Sprint close stale scan、Workflow Sync 四件套刷新和旧归档路径残留检查具备聚焦自动化回归覆盖。

#### Scenario: stale 中间态文案触发测试失败
- **WHEN** pytest 使用 fixture 构造一个目标 Sprint 四件套，其中已创建或已归档 Change 仍显示待 `/req-opsx`、待 `/bug-opsx` 或待 `/opsx-apply`
- **THEN** stale scan 测试 MUST 断言命令返回非零退出码
- **AND** 断言报告包含命中文件、关联对象、真实状态和建议修复动作

#### Scenario: legacy archive path 真实残留触发测试失败
- **WHEN** pytest 使用 fixture 构造 Sprint 四件套或新生成报告引用 `openspec/changes/archive/` 作为 canonical archive path
- **THEN** stale scan 或 residual 测试 MUST 断言该引用被标记为 blocker
- **AND** 断言建议改用 `openspec/archive/`

#### Scenario: 允许的 legacy 例外不触发失败
- **WHEN** pytest fixture、兼容读取 helper 或迁移脚本中包含 `openspec/changes/archive/` legacy 字符串
- **THEN** 测试 MUST 断言 stale scan 将其归类为允许例外或忽略
- **AND** 该例外 MUST NOT 造成 Sprint close gate 失败

#### Scenario: Workflow Sync 刷新后 stale scan 通过
- **WHEN** Workflow Sync 根据 `sprint.yaml`、Issue trace 和 Change 状态刷新 `sprint.md` Scope 派生块
- **THEN** 测试 MUST 断言刷新后的四件套不再保留由机器事实可确定的过期规划文案
- **AND** 再次运行 stale scan MUST 返回 0

#### Scenario: 测试保持路径解析兼容
- **WHEN** 测试需要读取 Change tasks、trace 或归档证据
- **THEN** 测试 MUST 继续兼容 active path、canonical archive path 和 legacy archive fallback
- **AND** 新断言 MUST 区分“兼容读取 legacy”与“生成 canonical legacy 路径”两种语义
