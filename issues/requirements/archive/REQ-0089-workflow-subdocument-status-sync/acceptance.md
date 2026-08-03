---
requirement_id: REQ-0089-workflow-subdocument-status-sync
title: REQ/BUG 子文档状态同步与验收结果回填机制 - 验收标准
acceptance_status: passed
created_at: 2026-08-01 09:52:35
updated_at: 2026-08-02 19:32:35
---

# 验收标准

## AC-001 文档角色边界明确

- [ ] 必须在规则或设计中明确 `trace.md`、`requirement.md`、`bug.md`、`acceptance.md`、`review.md` 等文档的状态字段职责。
- [ ] 若子文档字段不表示当前主状态，必须改名、移除或写明语义，避免与 `trace.md status` 混淆。
- [ ] `trace.md` 必须继续作为机器状态事实源。

## AC-002 常规状态变化会同步人类入口文档

- [ ] `req.generate` 后 `requirement.md` 与 `trace.md` 均可表达 `draft`。
- [ ] `bug.generate` 后 `bug.md` 与 `trace.md` 均可表达 `draft`。
- [ ] `req.review` / `bug.review` 后主文档与 `review.md` 不得保留冲突状态。
- [ ] `opsx.apply` 后主文档和验收入口能表达实现完成后的验收入口语义。
- [ ] `opsx.archive` / `sprint.archive` 后主文档和验收入口能表达闭环语义。

## AC-003 验收结果可回填

- [ ] `acceptance.md` 或等价验收结果文档必须支持记录 `acceptance_status`、`accepted_at`、`accepted_by`、`source_change`、`source_sprint`、`evidence`、`failed_items`。
- [ ] 已归档 Issue 必须存在验收通过、失败、部分通过或豁免结论。
- [ ] 未完成验收时必须记录下一步，不能只残留旧状态。

## AC-004 Drift check 覆盖子文档

- [ ] 校验能发现 `trace.md` frontmatter 与 fenced yaml 状态不一致。
- [ ] 校验能发现 registry 与 `trace.md` 状态不一致。
- [ ] 校验能发现 `plan/review/archive` 目录阶段与 `lifecycle_stage` 不一致。
- [ ] 校验能发现 `requirement.md` / `bug.md` / `acceptance.md` 中未解释的状态漂移。
- [ ] 校验失败报告必须包含文件路径、字段来源、旧值、期望值和建议命令。

## AC-005 历史漂移治理受控

- [ ] 历史 archive 扫描必须支持 dry-run。
- [ ] dry-run 必须按可安全同步、需人工判断、缺证据、缺验收结果等类别输出。
- [ ] apply 只能处理 dry-run 中明确可安全同步的项。
- [ ] apply 后必须刷新 `updated_at` 并可复跑 check 验证。
- [ ] 批量修复不得绕过 review、acceptance、OpenSpec archive 或 Sprint archive。

## AC-006 Workflow Sync 摘要包含子文档信息

- [ ] 相关事件的 Workflow Sync 摘要应包含子文档检查数量和更新数量。
- [ ] 如存在 drift warning，摘要应给出数量和下一步建议。
- [ ] 成功路径不得输出大量子文档正文。

## AC-007 归档门禁前移

- [ ] `/opsx-archive` 后必须能检查 archived Change trace 或 fallback 证据完整性。
- [ ] `/sprint-archive` 前必须能扫描 Issue 包和 Sprint 四件套中的中间态文案残留。
- [ ] 发现早期规划、验收未闭环、实现未完成或 active Change 路径等残留时，必须修复或记录豁免原因。

## AC-008 安全与上下文预算

- [ ] 历史扫描默认限制在 `issues/requirements` 和 `issues/bugs`，并按阶段与文件类型控制范围。
- [ ] 大量漂移只输出计数、分类和样例，不默认展开全部文件。
- [ ] 不得写入或输出 prompt、session、工具输出正文、密钥、`.env`、Authorization header、Cookie 或真实客户数据。
- [ ] 成功路径只输出摘要；失败路径只输出必要文件路径与字段。

## Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 写入 AC 数 |
|---|---|---:|
| N/A | 纯流程治理需求，不涉及管理端列表/表单/弹窗/媒体上传 UI best-practice | 0 |

## 知识库引用

- `docs/knowledge-base/README.md`
- `docs/knowledge-base/retrospectives/sprint-016-retrospective.md`

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: improve-workflow-subdocument-status-sync
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

