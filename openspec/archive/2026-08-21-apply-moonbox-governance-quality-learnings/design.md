## 设计说明

本次学习应用采用“规则入口 + 命令技能短引用 + 轻量脚本校验 + 学习报告”的组合，不复制 MoonBox 长文档或脚本全文。正式行为要求写入 `agent-workflow-tooling` delta spec；执行细节分散到本项目已有规则和命令入口。

## 采纳策略

### 证据化根因分析治理

- 新增 `rules/root-cause-evidence.md`，定义 `unknown`、`hypothesis`、`probable`、`confirmed` 四类根因状态。
- `confirmed` 必须绑定日志、测试、截图、代码定位、配置差异、复现记录或用户补证等证据；证据不足时只能输出人工补证步骤。
- `/explore`、`/bug-complete`、BUG 管理规则、测试规则与 Workflow Sync 规则引用该门禁。
- `scripts/validate-root-cause-evidence.py` 先提供轻量扫描：聚焦 BUG 或 active Change，发现 confirmed 无证据、缺少根因状态时报告 warning / blocker。

### 命令执行复盘 Hook

- 在 `workflow-sync` 中央技能定义 workflow 命令最终输出的复盘字段：链路状态、问题证据、规范优化建议、follow-up 自动创建状态。
- 该复盘只允许基于脚本、校验、文件、截图、日志、用户补证或 Workflow Sync/AI Usage 结果，不凭空猜测。
- 可优化点默认只输出建议命令或 capture 文案，除非用户明确授权，不自动创建后续 Issue / Change。

### UI 返修截图逐项对照

- 在 `opsx-modify` 和 `docs/standards/prototype-ui-acceptance.md` 中补充：若验收反馈包含附件截图、标注图、原型截图或实际截图，返修前必须形成对照表。
- 对照表至少包含截图编号、页面/状态、期望表现、实际表现、偏差项、检查方式、处置结论和证据入口。
- 证据不足时先补证，不直接返修；返修后旧截图视为 stale，需要重新取证。

### Workflow Sync next 推导复核

- 在 `workflow-sync` 规则中明确 `req.opsx` / `bug.opsx` 同轮回填 Change 后，必须刷新当前态看板 next。
- 增加检查要求：若 `issues/*/CHANGELOG.md` 仍提示 `/req-opsx` 或 `/bug-opsx`，应视为派生态漂移并修复后再完成命令。

### 治理脚本门禁矩阵

- 新增 `docs/standards/command-execution-order.md`，按命令阶段列出最小相关校验。
- 保持矩阵为指导性门禁，不替代各命令 Skill 中的 MUST 校验。

## 风险与边界

- 本次不修改业务 `src/`，不修改 API/DB/Orval/Docker。
- 根因证据脚本先做轻量结构校验，不尝试自动判断业务根因真假。
- 本次不把 MoonBox 的轻量 Mintlify 模式迁回本项目。
- 当前工作区已有大量无关未提交变更，本次只聚焦新增和触达的治理资产。
