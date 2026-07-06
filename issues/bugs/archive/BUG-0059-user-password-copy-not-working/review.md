---
bug_id: BUG-0059-user-password-copy-not-working
title: 管理端一次性密码弹窗复制密码未生效评审记录
status: approved
review_decision: approved
severity: high
owner: product
reviewed_at: 2026-07-06 15:17:18
created_at: 2026-07-06 15:17:18
updated_at: 2026-07-06 15:17:18
related_requirement: REQ-0005-user-management
related_change: null
next_step: /bug-opsx BUG-0059-user-password-copy-not-working
---

# 缺陷评审记录

## 评审结论

结论：批准修复（`approved`）。

`BUG-0059-user-password-copy-not-working` 为 `REQ-0005-user-management` 已归档能力的行为偏差。一次性密码弹窗中的「复制密码」属于创建用户与重置密码后的关键交付动作，当前复制失败会直接影响管理员安全交付初始密码或重置后的随机密码。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 两个入口共享 `ResetPasswordDialog`，复制逻辑仅调用 Clipboard API，失败路径静默吞掉，根因充分。 |
| 严重等级合理 | 通过 | 一次性密码关闭后不可再次查看，复制失败影响用户账号交付闭环，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖创建用户、重置密码、剪贴板失败兜底、测试覆盖和非目标范围。 |
| 是否需 hotfix 路径 | 不需要 | 当前有手动选中复制的临时规避方式，建议进入常规 `fix-*` Change；若演示或生产交付紧急可提高排期。 |

## 评审依据

- `bug.md` 已记录现象、复现步骤、期望/实际和影响范围。
- `root-cause.md` 已说明前端复制交互对 Clipboard API 失败路径处理不足。
- `workaround.md` 已给出关闭弹窗前手动选中复制的临时规避方案。
- `acceptance.md` 已定义修复后的回归验收标准。
- `trace.md` readiness 为 Ready，具备进入修复 Change 的条件。

## 决策

- 状态变更为 `approved`。
- 允许执行 `/bug-opsx BUG-0059-user-password-copy-not-working` 创建 `fix-*` OpenSpec Change。
- 允许后续纳入 Sprint 正式规划。
- 修复范围应优先限定在 Web 管理端一次性密码结果弹窗与对应测试。

## 风险与约束

- 修复不得新增再次查询一次性明文密码的接口。
- 修复不得将一次性明文密码写入数据库、日志、审计记录或长期文档。
- 修复不得绕过系统管理员权限边界。
- 修复应补充 `ResetPasswordDialog` 复制成功与失败路径测试。
