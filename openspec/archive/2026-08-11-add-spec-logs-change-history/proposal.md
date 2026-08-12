## 背景

`docs/spec-logs/` 已用于存放 `/spec-opt` 治理迭代日志和 `/spec-study` 学习报告，但缺少一个持续维护的变更历史总账。随着规范、脚本、技能和命令频繁迭代，仅依赖分散的时间戳日志不利于快速了解治理资产的演进脉络。

## 变更内容

- 在 `docs/spec-logs/` 新增长期维护的 `CHANGELOG.md`，记录规范、脚本、技能和命令等治理资产的变更历史索引。
- 明确 `CHANGELOG.md` 与单次 `YYYYMMDDhhmmss-governance-*.md` 日志的职责边界。
- 同步 `docs/spec-logs/README.md`、`docs/README.md` 和文档治理规则，要求 `/spec-opt` 在治理迭代完成后维护变更历史。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：补充 `/spec-opt` 治理迭代日志与变更历史总账的输出要求。

## 影响

- 影响文档治理、规范工程日志目录说明、`/spec-opt` 输出规范和 OpenSpec 变更事实源。
- 不修改 `src/` 业务代码。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。
