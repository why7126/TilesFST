## 背景

`/capture`、`/explore` 与 `/opsx-modify` 已分别具备类型分类、只读分流和验收返修边界，但对“需求开发中、需求已归档但 Sprint 未归档、Sprint 已归档”三类阶段的推荐路径没有集中表述。AI 在验收反馈、归档后偏差和新增诉求之间切换时，容易只凭单条命令规则推导，输出不够稳定。

## 变更内容

- 在 `/capture` 中补充需求相关偏差的阶段分流表，明确何时不自动 capture、何时记录 BUG、何时记录 REQ。
- 在 `/explore` 中补充只读阶段分流判断，作为讨论和后续命令建议依据。
- 在 `/opsx-modify` 中补充验收返修阶段边界，明确 Change 已归档或范围越界时应停止并转入 capture 链路。
- 写入治理迭代日志，并维护 `docs/spec-logs/CHANGELOG.md`。

## 能力范围

### 新增能力

- 无业务能力新增。

### 修改能力

- `agent-workflow-tooling`：补充 capture / explore / opsx-modify 对需求相关偏差的阶段分流规则。

## 影响

- 影响 `.agents/skills/capture`、`.agents/skills/explore`、`.agents/skills/opsx-modify` 的治理命令规则。
- 不修改 `src/` 业务代码。
- 不影响 API、数据库、Web、小程序、管理端、Orval 或 Docker Compose。
