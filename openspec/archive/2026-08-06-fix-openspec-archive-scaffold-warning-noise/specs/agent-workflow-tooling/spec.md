# agent-workflow-tooling 规格变更

## ADDED Requirements

### Requirement: OpenSpec 归档输出区分兼容 warning 与真实风险
系统 MUST 在 `/opsx-archive` 与底层归档封装流程中区分已知 OpenSpec CLI 兼容 warning 与真实归档风险。对于项目中文语言规范已覆盖且不影响归档结果的英文脚手架标题提示，系统 MUST 在安全条件满足时吸收该提示，避免成功路径反复输出固定非阻塞说明；对于真实错误、未知 stderr、目录结构错误或中文语言校验失败，系统 MUST 保留阻断或可见 warning。

#### Scenario: 已知英文脚手架 warning 被安全吸收
- **WHEN** `/opsx-archive <change-id>` 或底层归档脚本执行成功
- **AND** OpenSpec CLI stderr 仅包含 `proposal.md` 缺少英文 `## Why` / `## What Changes` 的已知兼容 warning
- **AND** `python scripts/validate-openspec-language.py` 通过
- **THEN** 最终归档说明 MUST NOT 重复展示该固定非阻塞 warning
- **AND** 系统 MUST NOT 要求为消除该 warning 在 Change 文档中回填英文脚手架标题
- **AND** 归档成功结论 MUST 继续清晰表达 Change 已归档

#### Scenario: 未知 stderr 仍然可见
- **WHEN** OpenSpec CLI stderr 包含已知兼容 warning 之外的 warning 或 error
- **THEN** 归档最终输出 MUST 保留未知 stderr 的可见诊断信息
- **AND** 系统 MUST NOT 将未知 stderr 当作已知兼容 warning 静默吸收

#### Scenario: 语言校验失败仍然阻断
- **WHEN** `python scripts/validate-openspec-language.py` 失败
- **THEN** 归档流程 MUST 按项目语言规范门禁失败处理
- **AND** 最终输出 MUST 包含语言校验失败信息
- **AND** 系统 MUST NOT 因 OpenSpec CLI 兼容 warning 可吸收而覆盖语言校验失败结果

#### Scenario: OpenSpec CLI 失败仍然阻断
- **WHEN** OpenSpec CLI 返回非零退出码
- **THEN** 归档流程 MUST 失败
- **AND** 最终输出 MUST 保留必要错误信息
- **AND** 系统 MUST NOT 将 CLI 失败路径降级为成功 warning
