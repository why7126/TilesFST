---
created_at: 2026-09-08 16:48:51
updated_at: 2026-09-08 16:48:51
---

## ADDED Requirements

### Requirement: Apply 当前 Change 持续执行

两个 apply 入口 MUST 持续完成当前 Change 中依赖满足且已获授权的任务，修复范围内可恢复错误，保留必要确认及归档发布边界。

#### Scenario: 任务分组完成或测试失败
- **WHEN** 已完成一组任务或出现范围内可修复错误
- **THEN** Agent MUST 继续后续任务或修复复测，不因阶段汇报而等待继续指令

#### Scenario: 局部阻塞与人工确认
- **WHEN** 某任务缺少必要授权、资源或关键决策
- **THEN** Agent MUST 记录阻塞证据和恢复条件，暂停相关依赖并继续其他可执行任务；用户明确停止时停止全部工作

#### Scenario: 部分完成与恢复
- **WHEN** 仍有未完成任务或必需验证未通过
- **THEN** Agent MUST 保留真实未完成状态，不声称 applied 或可归档，恢复时承接已完成工作和已确认决策

#### Scenario: 完成收尾
- **WHEN** 所有适用任务与必需验证已完成
- **THEN** Agent MUST 同步真实状态并报告结果，不自动执行归档、发布或其他 Change
