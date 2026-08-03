## Context

REQ-0089 指出当前工作流事实源存在分层不清的问题：`trace.md` 是机器状态事实源，但 `requirement.md`、`bug.md`、`acceptance.md`、`review.md`、BUG 分析文档等也含 `status` 或验收相关字段。常规命令大多只维护 `trace.md` 和派生块，子文档状态主要在 archive promote 被 residual gate 拦截后才补救。

Sprint 016 复盘暴露了同类问题：Sprint close 前四件套曾残留“待验收 / planned”等中间态文案，且归档 Change 缺 trace 会阻断 close。这说明状态漂移应在工作流过程中前移检查，而不是留到最终收尾。

## Goals / Non-Goals

**Goals:**

- 建立 Issue 子文档状态字段角色边界，减少 `status` 语义混淆。
- 将常规状态传播纳入 Workflow Sync 或共享脚本。
- 为验收结果回填提供稳定、可测试的结构。
- 扩展 drift check，能发现子文档、目录阶段、registry 和验收结论不一致。
- 为历史 archive 漂移提供受控 dry-run / apply 治理路径。

**Non-Goals:**

- 不直接批量修复历史 archive 文档。
- 不新增业务 API、数据库模型、Web 页面或小程序页面。
- 不改变 OpenSpec 的 Change 创建、apply、archive 基本流程。
- 不持久化 Codex prompt、session、工具输出正文或敏感信息。

## Decisions

### D1. `trace.md` 继续作为机器事实源，子文档状态作为派生读物

`trace.md` 继续维护 canonical `status`、`lifecycle_stage`、`iteration` 和 `openspec_changes`。主文档和验收文档可以保留状态字段，但其语义必须明确：要么同步当前主状态，要么改为 `document_status`、`review_result`、`acceptance_status` 等不混淆字段。

替代方案是移除所有子文档状态字段。该方案更干净，但历史文档多、迁移风险高；本 Change 先要求角色边界和同步/检查能力。

### D2. 常规同步与闭环 reconcile 分离

常规同步负责在 `req.review`、`bug.review`、`req.opsx`、`bug.opsx`、`opsx.apply`、`opsx.archive`、`sprint.archive` 等事件后同步可安全派生的子文档状态与验收入口。闭环 reconcile 继续用于 archive promote 阻塞后的残留修复，只能在 Issue 主状态和关联交付对象已闭环时写入。

这样可以避免把 reconcile 误用成绕过 review/acceptance 的万能修复。

### D3. 验收结果回填优先扩展 `acceptance.md`

`acceptance.md` 先同时承载验收标准和验收结果，新增标准化结果块或 frontmatter/yaml 字段，例如 `acceptance_status`、`accepted_at`、`source_change`、`source_sprint`、`evidence`、`failed_items`。未来如果文档膨胀，再独立拆 `acceptance-result.md`。

### D4. 历史治理必须 dry-run 优先

历史 archive 漂移不可直接批量修改。扫描必须先分类：可安全同步、需人工判断、缺证据、缺验收结果、不建议自动修复。只有 dry-run 中明确安全的项可以 apply，并刷新 `updated_at`。

### D5. 输出保持摘要化

成功路径只报告检查数量、更新数量、漂移 warning 数量和建议动作；失败路径输出文件路径、字段来源、旧值、目标值和建议命令。不得默认展开大量 Issue 文档正文。

## Risks / Trade-offs

- 子文档历史格式不统一 → 先做扫描分类和 safe-to-sync 判定，无法判断的文档留给人工确认。
- `status` 字段语义混淆 → 在规则和 Skill 中明确字段角色，并在 check 中报告冲突。
- Workflow Sync 输出格式变化影响测试 → 同步更新 workflow snapshot 和 pytest。
- 归档门禁变严导致短期阻塞增多 → 提供 dry-run、分类报告和豁免记录，减少无头绪返工。

## Migration Plan

1. 实现常规子文档状态同步 planner 和 patcher。
2. 扩展验收结果块生成/检查。
3. 扩展 `--check` 或新增 drift scan/check 命令。
4. 将 promote residual gate 改为复用新的扫描分类能力。
5. 更新 req/bug/opsx/sprint skills 与 rules。
6. 增加 focused pytest，覆盖 REQ、BUG、archive、dry-run/apply、summary 输出和敏感信息边界。

## Open Questions

- 历史文档中 `capture.md status: captured` 是否应视作可接受历史状态，还是 archive 阶段统一要求非阻塞字段重命名。
- 验收结果块最终放 frontmatter、fenced yaml 还是 Markdown 表格，需在实现时根据现有 parser 稳定性选择。
