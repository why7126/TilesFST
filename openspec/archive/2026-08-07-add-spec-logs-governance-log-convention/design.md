## 设计

`docs/spec-logs/` 作为规范工程日志目录，按文件名区分日志来源：

| 类型 | 命名 | 生成命令 |
|---|---|---|
| 跨项目学习报告 | `YYYYMMDDhhmmss-study-xxx.md` | `/spec-study` |
| 本项目治理迭代日志 | `YYYYMMDDhhmmss-governance-xxx.md` | `/spec-opt` |

## 日志边界

- `study` 日志记录学习对象、学习模式、候选内容、采纳内容、未采纳内容和学习对象只读保护结果。
- `governance` 日志记录本项目规范、技能、脚本、目录边界或校验规则的迭代目标、变更摘要、影响范围、更新文件和验证结果。
- 两类日志都不得存放需求、BUG、Sprint 四件套、OpenSpec Change 事实源、源码副本、密钥、访问令牌、真实客户数据、用户隐私数据、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息、运行时数据库、依赖目录或构建产物。
- 如需说明隐私相关风险，必须使用脱敏占位符或聚合描述，不得写入原始值。

## 执行要求

- `/spec-study` 应用完成后写 `YYYYMMDDhhmmss-study-xxx.md`。
- `/spec-opt` 治理变更完成后写 `YYYYMMDDhhmmss-governance-xxx.md`。
- 日志 Markdown 必须含 `created_at` 与 `updated_at`。
- 日志属于长期 docs，目录边界由 `rules/directory-structure.md` 和 `docs/spec-logs/README.md` 管理。
