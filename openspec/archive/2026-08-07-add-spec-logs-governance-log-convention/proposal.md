## 背景

`docs/spec-logs/` 已用于 `/spec-study` 学习报告，但本项目自身规范、技能、脚本的迭代更新也需要沉淀过程日志。两类日志应共用同一目录，便于检索，同时通过文件名区分来源类型。

## 变更内容

- 将 `docs/spec-logs/` 定义为规范工程日志目录，承载 `/spec-study` 学习报告和 `/spec-opt` 治理迭代日志。
- 约定学习报告命名为 `YYYYMMDDhhmmss-study-xxx.md`。
- 约定治理迭代日志命名为 `YYYYMMDDhhmmss-governance-xxx.md`。
- 更新 `/spec-opt`：规范、技能、脚本迭代完成后必须写入治理迭代日志。
- 更新 `/spec-study`：学习报告命名增加 `study-` 类型前缀。
- 增加隐私边界：`docs/spec-logs/` 下文档不得包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志或学习对象源码。
- 为本次规则变更生成治理迭代日志。

## 能力

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：补充 `/spec-opt` 治理迭代日志与 `/spec-study` 学习报告在 `docs/spec-logs/` 下的命名区分、隐私禁写和脱敏规则。

## 影响

- 影响 `.agents/skills/spec-opt/SKILL.md`、`.agents/skills/spec-study/SKILL.md`、`docs/spec-logs/README.md`、`docs/spec-logs/20260807103244-governance-spec-logs.md`、`docs/README.md`、`rules/directory-structure.md`、`rules/agent-context-budget.md` 与本 Change 文档。
- 不影响后端 API、数据库、Web、小程序、管理端业务实现。
- 不需要 Orval。
- 不需要 Docker Compose 验证。
