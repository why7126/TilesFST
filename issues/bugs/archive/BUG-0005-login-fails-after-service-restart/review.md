---
bug_id: BUG-0005-login-fails-after-service-restart
review_id: REV-BUG-0005-001
status: in_sprint
reviewed_at: 2026-06-26 20:57:56
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0005-login-fails-after-service-restart` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0005-login-fails-after-service-restart
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 已给出服务重启后登录失败的复现路径；`root-cause.md` 已定位到默认 admin seed 只在缺失时创建、持久化 SQLite 中已有 admin 时不会校验或恢复密码。 |
| 严重等级合理 | 通过 | 缺陷会阻断内部员工进入管理端，影响数据维护、演示和验收流程，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖首次启动、服务重启、已有 admin、显式恢复策略、Docker 环境变量说明、错误提示、安全边界和认证回归。 |
| 是否需 hotfix 路径 | 不需要 | 当前影响本地或 Docker 管理端登录恢复路径，尚未确认生产全量不可用；可通过标准 `fix-*` OpenSpec Change 修复。 |

## 3. 批准理由

1. 缺陷影响管理端登录入口，失败提示会误导用户继续检查账号密码。
2. 根因与运行时数据库、默认管理员初始化策略和环境变量说明相关，属于需要通过正式修复消化的系统行为问题。
3. 修复可能涉及启动初始化策略、测试和部署文档，必须通过 `fix-*` OpenSpec Change 管理。
4. 回归验收已明确要求不泄露账号存在性、不输出明文密码、不放宽管理端权限边界。

## 4. 后续要求

1. 创建 `fix-*` OpenSpec Change 时，必须明确默认管理员初始化与密码恢复策略。
2. 若支持显式重置默认管理员密码，必须通过受控环境变量或一次性管理流程触发，避免每次启动覆盖真实管理员密码。
3. 必须同步根目录 `.env.example`、Docker/部署文档和数据库说明，避免环境变量事实源不一致。
4. 必须补充后端回归测试，覆盖空数据库首次启动、已有 admin 重启、显式恢复触发与未触发场景。
5. 修复不得改变 `POST /api/v1/auth/login` 的统一凭证错误语义，也不得破坏 `admin`、`employee`、`store_owner` 权限边界。
