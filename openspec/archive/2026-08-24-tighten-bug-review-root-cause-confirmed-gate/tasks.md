## 1. 规则与命令

- [x] 1.1 更新 `rules/root-cause-evidence.md`，声明 `/bug-review` approve 前必须满足 confirmed 根因门禁。
- [x] 1.2 更新 `rules/bug-management.md`，将非 confirmed、缺文档、缺状态写为 BUG approve blocker。
- [x] 1.3 更新 `.agents/skills/bug-review/SKILL.md`，在评审写入和目录迁移前运行 confirmed 校验。
- [x] 1.4 更新入口摘要，确保 AGENTS、docs 索引和上下文预算规则保留该门禁。

## 2. 脚本与测试

- [x] 2.1 为 `scripts/validate-root-cause-evidence.py` 增加 `--require-confirmed` 模式。
- [x] 2.2 补充聚焦测试，覆盖非 confirmed 阻断、缺文档阻断、confirmed 通过和默认模式兼容。
- [x] 2.3 运行脚本级验证与聚焦 pytest。

## 3. OpenSpec、Sprint 与日志

- [x] 3.1 补齐本 Change 的 proposal、design、tasks、delta spec、trace、acceptance 和 test-plan。
- [x] 3.2 将纯治理 Change 纳入 `sprint-025` 正式 `changes[]` scope，并运行 Workflow Sync。
- [x] 3.3 写入治理迭代日志并更新 `docs/spec-logs/CHANGELOG.md`。
- [x] 3.4 运行上下文预算、OpenSpec 语言、目录结构、目标 Change 和文档卫生校验。
