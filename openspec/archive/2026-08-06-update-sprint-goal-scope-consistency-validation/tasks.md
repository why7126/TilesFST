## 1. 校验脚本

- [x] 1.1 在 `scripts/validate-sprint-scope.py` 中解析 `sprint.md ## 1. 目标` 的 Sprint 目标编号列表。
- [x] 1.2 校验 `sprint.yaml.requirements` 与 `sprint.yaml.bugs` 均出现在目标编号列表中。
- [x] 1.3 实现纯 Change 显式展示策略，避免已由 REQ/BUG 表达的 Change 重复强制。
- [x] 1.4 支持完整 ID 与短编号等价匹配。
- [x] 1.5 输出具体缺失项、缺失位置和格式异常提示。

## 2. 工作流规则

- [x] 2.1 更新 `.agents/skills/sprint-propose/SKILL.md`，明确追加 Scope 后必须同步目标编号列表并运行增强校验。
- [x] 2.2 更新 `.agents/skills/workflow-sync/SKILL.md`，明确目标编号列表与 Scope marker block 的维护边界。
- [x] 2.3 按需更新 `rules/iterations-lifecycle.md` 或相关规则，保持 Sprint Scope 校验门禁一致。

## 3. 测试与验证

- [x] 3.1 增加目标编号列表缺失 REQ 的失败测试，覆盖 `sprint-020` / `REQ-0100` 类场景。
- [x] 3.2 增加目标编号列表完整时通过的测试。
- [x] 3.3 增加短编号与完整 ID 等价匹配测试。
- [x] 3.4 增加 `--item` 聚焦校验仍检查目标编号列表的测试。
- [x] 3.5 运行 `python scripts/validate-openspec-language.py`、OpenSpec 校验和相关 pytest。

## 4. 文档同步

- [x] 4.1 更新 Change acceptance 或实现记录，说明 API、数据库、Web、小程序、管理端、Orval、Docker 均不受影响。
- [x] 4.2 `/opsx-apply` 完成后用 `validate-sprint-scope.py sprint-021 --item REQ-0102-sprint-goal-scope-consistency-validation` 验证当前 Sprint 范围。
- [x] 4.3 用历史 `sprint-020 --item REQ-0100-mintlify-docs-site-ia-content-experience` 验证缺失项提示。
