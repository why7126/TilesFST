## 任务清单

- [x] 1. 扩展 Workflow Sync linked Change 模型
  - [x] 1.1 梳理 `IssueRecord` 中 `openspec_changes`、`related_changes`、`related_change` 的读取和派生规则。
  - [x] 1.2 明确 REQ 与 BUG 当前主 linked Change 的选择策略。
  - [x] 1.3 多 active 候选无法判断时输出 blocker，不静默覆盖。

- [x] 2. 同步 REQ / BUG 主文档与 registry
  - [x] 2.1 在 `req.opsx` 中同步 `requirement.md` linked Change 可读入口。
  - [x] 2.2 在 `bug.opsx` 中同步 `bug.md` linked Change 可读入口。
  - [x] 2.3 扩展 `_registry.yaml` patch，更新 `related_change`。
  - [x] 2.4 保持重复运行幂等。

- [x] 3. 保持 Sprint scope 回填与 apply 门禁一致
  - [x] 3.1 确认已在 Sprint 的 REQ/BUG 创建 Change 后补齐 `changes[]`。
  - [x] 3.2 同步 `scope_estimates[].change`。
  - [x] 3.3 确认 `/opsx-apply --sprint auto --change <change-id> --dry-run` 可解析到 Sprint。

- [x] 4. 增加测试
  - [x] 4.1 覆盖 REQ `req.opsx` trace、`requirement.md`、registry 同步。
  - [x] 4.2 覆盖 BUG `bug.opsx` trace、`bug.md`、registry 同步。
  - [x] 4.3 覆盖 Sprint scope 回填和幂等重复运行。
  - [x] 4.4 覆盖多候选 Change blocker 或明确选择路径。

- [x] 5. 验证与文档同步
  - [x] 5.1 运行聚焦 Workflow Sync 测试。
  - [x] 5.2 运行 `python scripts/validate-openspec-language.py`。
  - [x] 5.3 运行 OpenSpec 校验。
  - [x] 5.4 如规则、技能或脚本行为说明变化，同步对应 `rules/`、`.agents/skills/` 或治理日志。
