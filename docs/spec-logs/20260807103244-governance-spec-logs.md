---
purpose: spec-logs 治理迭代日志
content: 记录 docs/spec-logs 同时承载 spec-study 学习报告与 spec-opt 治理迭代日志的规则变更
source: /spec-opt add-spec-logs-governance-log-convention
created_at: 2026-08-07 10:32:44
updated_at: 2026-08-07 10:50:46
---

# spec-logs 治理迭代日志

## 迭代目标

将本项目规范、技能、脚本的迭代更新日志也统一沉淀到 `docs/spec-logs/`，并通过文件名与 `/spec-study` 学习报告区分。

## 变更摘要

- `/spec-study` 学习报告使用 `YYYYMMDDhhmmss-study-xxx.md`。
- `/spec-opt` 治理迭代日志使用 `YYYYMMDDhhmmss-governance-xxx.md`。
- `docs/spec-logs/README.md` 明确两类日志的用途、命名和边界。
- `docs/spec-logs/` 明确禁止写入用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、学习对象源码和截图中的个人信息。
- `/spec-study` 与 `/spec-opt` 日志生成规则补充脱敏占位符和聚合描述要求。
- `rules/directory-structure.md`、`docs/README.md`、`AGENTS.md` 和 `rules/agent-context-budget.md` 同步目录归属和命令要求。

## 影响范围

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要验证。
- 测试：业务测试不适用，执行治理校验。

## 更新文件

- `.agents/skills/spec-opt/SKILL.md`
- `.agents/skills/spec-study/SKILL.md`
- `docs/spec-logs/README.md`
- `docs/spec-logs/20260807103244-governance-spec-logs.md`
- `docs/README.md`
- `rules/directory-structure.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `openspec/changes/add-spec-logs-governance-log-convention/`

## 隐私检查结果

- 已检查本日志内容，不包含本机用户路径、真实姓名、手机号、邮箱、地址、证件号、账号 ID、访问令牌、密钥、订单原文、聊天原文、工单原文、截图个人信息、未脱敏日志、真实客户数据或学习对象源码。
- 涉及隐私边界的内容仅保留为规则级聚合描述，未记录任何原始用户或客户数据。

## 验证结果

- OpenSpec、目录结构、OpenSpec 文档语言、Agent 上下文预算、Sprint scope、Workflow Sync 与 AI Usage hook 均已通过。

## 后续建议

- 后续 `/spec-opt` 归档前确认对应 `YYYYMMDDhhmmss-governance-xxx.md` 已生成或更新。
- 后续 `/spec-study` 应用阶段确认对应 `YYYYMMDDhhmmss-study-xxx.md` 已生成。
