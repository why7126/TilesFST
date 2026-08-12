## 设计

### 治理落地原则

本变更只改治理资产，不修改 `src/` 业务代码。来自 ProjectMoonBox 的内容采用“规则意图迁移 + 本项目语境改写”，不复制学习对象的长脚本、长规范或业务实现。

### 日志优先学习

`/spec-study` 的 Phase 1 新增优先级：

1. 若学习对象存在 `docs/spec-logs/CHANGELOG.md`，先把它作为治理演进地图。
2. 按候选主题读取相关 `study` / `governance` 单次日志。
3. 再横向校验 `AGENTS.md`、`rules/`、`docs/`、`.agents/skills/`、`scripts/`、`deploy/` 等真实资产。
4. 若日志与真实资产漂移，以当前真实资产和正式规格为准，并在候选清单标注风险。

### Git 安全检测

新增 `.agents/skills/git-check/SKILL.md` 和 `scripts/git-check.py`。

默认扫描 staged、modified tracked 和 untracked 文件，不读取 ignore 且未 staged/untracked 的真实 `.env` 内容。`--all` 可用于深度扫描全仓当前文件。检测项包括：

- 真实环境文件与部署 env。
- 运行时数据、数据库文件、构建产物和大文件。
- 密钥、Token、Authorization、Cookie、数据库连接串、对象存储凭据。
- 本机绝对路径。

输出必须脱敏，error 返回非 0，warning 不阻断但要求人工复核。

### 原型驱动 UI 验收

新增 `docs/standards/prototype-ui-acceptance.md`，并在 `rules/ui-design.md`、`AGENTS.md`、`req-opsx`、`opsx-apply`、`opsx-modify`、`opsx-archive` 中引用。

带 `prototype/` 的 UI Change 需要：

- `design.md` 写入 UI Contract。
- 先完成 Skeleton 首轮确认。
- 记录 1440px 桌面截图或等价视觉证据。
- 对高风险视觉差异记录 computed style 或测试断言。
- 明确 Mock/API 边界和最终一致性检查。

### Issue 当前态看板

新增 `issues/requirements/CHANGELOG.md` 与 `issues/bugs/CHANGELOG.md`，只作为目录级当前态索引，每个 Issue 一行展示状态、阶段、Sprint、Change、下一步和事实源路径。

机器事实源仍为 `_registry.yaml`、单条 `trace.md`、Sprint 四件套和 OpenSpec Change。当前态看板不得替代 Workflow Sync，也不得写入隐私、密钥或未脱敏日志。

### 引导式反馈

在 `rules/agent-context-budget.md` 定义命令引导式反馈契约：需要用户选择、确认、补充或处理阻塞时，优先使用原生交互卡片；当前工具不支持时降级为文本结构化选项。每轮只聚焦 1-3 个关键决策，并提供推荐项与可补充说明。

## 风险与取舍

- 不自动把 Issue 当前态看板接入 Workflow Sync 写入逻辑，避免扩大脚本状态机风险；先由命令技能维护，后续可单独治理自动化。
- `/git-check` 采用保守文本扫描，可能产生 warning，需要人工判断；它不删除文件、不修改 `.gitignore`、不 unstage。
- UI 验收门禁先落文档与技能规则，不引入 Playwright 强制脚本，避免一次性拉高所有 UI Change 成本。
