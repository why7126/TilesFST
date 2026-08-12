---
purpose: 规范工程日志目录说明
content: 记录 spec-study 学习报告与 spec-opt 治理迭代日志的存放位置、命名规则与边界
source: /spec-opt rename-spec-sync-to-spec-study
update_method: spec-study 或 spec-opt 日志治理规则变化时更新
created_at: 2026-08-07 09:56:44
updated_at: 2026-08-08 21:03:00
---

# 规范工程日志

`docs/spec-logs/` 用于存放规范工程日志，包括 `/spec-study` 学习其他项目 Harness 工程后生成的学习报告，以及 `/spec-opt` 对本项目规范、技能、脚本、目录边界和校验规则的迭代更新日志。

[CHANGELOG.md](CHANGELOG.md) 是规范工程变更历史总账，用于按时间倒序汇总规范、脚本、技能、命令和治理文档的更新记录。单次 `study` 报告和 `governance` 日志继续作为详细事实源，`CHANGELOG.md` 只记录摘要、影响范围、验证结果、详细日志入口和其他项目可复用的落地提示词。

## 命名规则

文件名 MUST 使用：

```text
YYYYMMDDhhmmss-study-xxx.md
YYYYMMDDhhmmss-governance-xxx.md
```

- `YYYYMMDDhhmmss`：报告生成时刻的 `Asia/Shanghai` 日期时间，精确到秒。
- `study`：`/spec-study` 跨项目学习报告。
- `governance`：`/spec-opt` 本项目规范、技能、脚本或校验规则迭代日志。
- `xxx`：小写 kebab-case 主题，例如 `pm-harness`、`design-system`、`api-governance`、`spec-logs`。

## 去重规则

- 同一次 `/spec-study` 学习应用流程只生成一份正式 `study` 报告。
- 学习阶段候选内容不得另行落盘为第二份正式 `study` 报告；可保留在最终回复、active Change 文档或同一报告的阶段章节中。
- `/spec-study` 触发的治理资产应用结果必须汇总到同一份 `study` 报告，不得再额外生成内容重复的 `governance` 日志。
- 若同一学习对象、学习主题和用户确认批次已存在本流程报告，后续应用结果、验证结果或修正 MUST 更新同一文件。
- `/spec-opt` 每次独立治理变更 MAY 生成一份 `governance` 日志；同一治理变更的补充修正 SHOULD 更新同一日志。
- `/spec-opt` 完成治理资产更新后 MUST 维护 [CHANGELOG.md](CHANGELOG.md)；若同一治理变更已有总账条目，后续验证结果或修正 SHOULD 更新同一条记录，不得重复新增同义条目。
- `CHANGELOG.md` 的每条记录 MUST 包含“跨项目落地提示词”，用于说明其他项目要落地同类规范时可直接使用的 Prompt；提示词必须脱敏、项目无关、可复制。

## 边界

- 本目录只承载 `/spec-study` 学习报告和 `/spec-opt` 治理迭代日志。
- `CHANGELOG.md` 只承载治理资产变更历史摘要，不替代单次日志、OpenSpec Change、Sprint 或 Issue 事实源。
- 不存放需求、BUG、Sprint 四件套或 OpenSpec Change 事实源。
- 不存放学习对象源码、密钥、真实客户数据、用户隐私数据、本机绝对路径、运行时数据库、依赖目录或构建产物。
- 不得记录可识别个人或客户主体的信息，包括但不限于姓名、手机号、邮箱、地址、证件号、账号 ID、访问令牌、订单原文、聊天原文、工单原文、截图中的个人信息和未脱敏日志。
- 如确需说明隐私相关风险或本地路径，MUST 使用脱敏占位符、仓库相对路径或聚合描述，例如 `<user-email>`、`<customer-id>`、`<local-project>/rules/global.md`、`rules/global.md`、`某类用户标识`，不得写入原始值或本机绝对路径。
