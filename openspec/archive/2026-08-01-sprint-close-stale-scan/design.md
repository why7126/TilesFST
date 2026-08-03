## Context

当前 Sprint 生命周期已经有容量门禁、Workflow Sync 派生块、目录结构校验和 archived path residual 测试，但这些约束分散在不同脚本与规则中。Sprint close 时，四件套仍可能保留早期规划文本：Issue 已创建 Change 后还显示“待 `/req-opsx` / `/bug-opsx`”，Change 已 apply 或 archived 后还显示“待 `/opsx-apply`”，或报告中继续把 `openspec/changes/archive/` 当作归档事实路径。此类残留通常不会破坏业务代码，却会误导归档判断、复盘输入和后续自动化。

本变更面向 Sprint close / archive 的治理自动化，不改变瓷砖业务功能。实现时应复用现有 Workflow Sync、目录校验、archived path residual scanner 和 pytest fixture 能力，避免新增一套不可追踪的并行事实源。

## Goals / Non-Goals

**Goals:**

- 在 Sprint close 或 `/sprint-archive` 相关路径中提供自动 stale scan，覆盖四件套状态文案与旧归档路径残留。
- stale scan 输出机器可读或稳定文本报告，包含命中文件、片段、原因、严重级别和建议修复动作。
- 将真实阻断项与允许例外分开：测试 fixture、迁移兼容读取、legacy 字符串常量可被白名单解释；真实 Sprint 四件套和新生成报告不得保留旧路径或过期中间态。
- 通过 Workflow Sync 刷新派生块，减少人工手改 `sprint.md` Scope marker 的需求。
- 补充聚焦 pytest，确保门禁可重复运行、幂等、失败信息可执行。

**Non-Goals:**

- 不自动 archive 未完成 Change，不替代人工 sign-off，也不改变 Sprint scope、Issue review 或 OpenSpec apply/archive 的前置门禁。
- 不修复所有历史归档 Sprint 文档中的旧文案；历史归档内容可作为兼容输入或回归 fixture，除非用户单独要求迁移。
- 不修改业务 API、数据库、Web UI、小程序或 MinIO 上传策略。
- 不引入外部依赖或持久化新的敏感数据。

## Decisions

1. **将 stale scan 作为 Sprint close 门禁，而不是普通全文 lint。**
   - 原因：问题只在 Sprint close 语境中具备阻断意义；历史归档和测试 fixture 中存在 legacy 字符串是合理的。
   - 替代方案：全仓库禁止相关字符串。该方案会误伤迁移脚本、兼容测试和历史证据。

2. **复用现有 scanner/validator 思路，必要时新增 `scripts/validate-sprint-close-stale-scan.py`。**
   - 原因：现有 `validate-directory-structure.py` 关注真实目录，`archived_path_residuals.py` 关注路径残留，Workflow Sync 已能刷新派生块；新增薄封装可组合这些检查并补充 Sprint 文案规则。
   - 替代方案：把所有逻辑塞进 `/sprint-archive` 脚本。该方案降低复用性，也不利于单独测试和 dry-run。

3. **检查输入以 `sprint.yaml` 定位四件套，不默认扫描全部 `iterations/archive/**`。**
   - 原因：遵守上下文预算与目录边界，避免历史 Sprint 大范围噪音；目标 Sprint 可从命令参数或 Workflow Sync `--sprint auto` 解析。
   - 替代方案：每次 close 扫描全量迭代目录。该方案代价高且容易把历史事实当作当前阻断。

4. **报告区分 `blocker`、`warning` 和 `allowed_legacy`。**
   - 原因：真实四件套 stale 文案应阻断；测试 fixture 或兼容 fallback 只需可见；部分人工验收未完成文字可能需要 warning 而不是自动失败。
   - 替代方案：所有命中一律失败。该方案会使人工 sign-off 和历史追溯文本难以表达。

5. **修复优先通过 Workflow Sync 或专用 reconcile 命令完成，禁止手工编辑派生 marker 块。**
   - 原因：`sprint.md` Scope 派生块已有 Workflow Sync 管辖边界；手工改派生块会导致下次同步回退。
   - 替代方案：stale scan 自动直接改全部文档。该方案可能覆盖人工验收结论，不符合现有治理规则。

## Risks / Trade-offs

- [Risk] 规则过严误判历史追溯文本或人工验收备注。→ Mitigation: 以目标 Sprint 四件套和机器派生区为主，支持 allowed legacy 分类，并为人工区域提供 warning 级别。
- [Risk] 规则过松导致 stale 文案继续通过。→ Mitigation: 对已能从 `sprint.yaml` 和 Change 状态确定的矛盾文案使用 blocker，并用 pytest fixture 固化典型案例。
- [Risk] Workflow Sync 不能覆盖所有残留来源。→ Mitigation: 报告提供明确文件路径和建议命令；无法自动修复的人工区域不静默通过。
- [Risk] `--sprint auto` 解析不到 Sprint。→ Mitigation: CLI 返回非零并提示显式传入 `sprint-xxx`，不得 fallback 到全量扫描。
