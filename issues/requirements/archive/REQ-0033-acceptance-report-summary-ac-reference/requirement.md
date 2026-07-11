---
requirement_id: REQ-0033-acceptance-report-summary-ac-reference
title: acceptance-report 拆分最终验收摘要与原始 AC 引用
terminal: multi
version: v1
status: archived
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-07-11 15:59:15
updated_at: 2026-07-11 20:13:04
---

# REQ-0033 acceptance-report 拆分最终验收摘要与原始 AC 引用

## 1. 需求背景

当前 Sprint `acceptance-report.md` 同时承载最终验收结论、归档门禁结果、REQ/BUG 原始 AC 勾选清单和人工 sign-off 参考。随着 Sprint 范围扩大，报告中可能出现“最终归档检查已通过”与大量历史原始 AC `- [ ]` 并存的情况。

这种结构会造成双重事实源：归档判断实际依赖 `/sprint-archive` readiness gate、Change archive 状态和 tasks 完成情况，但读者看到原始 AC 未勾选时，容易误判 Sprint 尚未完成，进而干扰归档、复盘和发布判断。

本需求用于调整 Sprint 验收报告的信息架构，将最终验收摘要与原始 AC 引用明确拆分，使归档判断有清晰事实源，同时保留原始 AC 的追溯价值。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 产品 / 需求负责人 | 快速判断 Sprint 是否已通过最终验收与归档门禁，不被历史 AC 勾选状态误导。 |
| QA / 验收人员 | 能区分“最终验收结论”和“原始 AC 追溯”，把人工 sign-off 项作为复核参考。 |
| 开发负责人 | 在 Sprint archive 时有稳定的验收报告结构，减少归档前后的状态争议。 |
| AI / Workflow Sync | 能按固定章节刷新派生状态，不覆盖人工最终结论或混淆原始 AC。 |
| 后续复盘读者 | 能追溯原始 AC 来源，又能明确 Sprint 关闭依据。 |

## 3. 需求目标

- `acceptance-report.md` 必须明确拆分“最终验收摘要”和“原始 AC 引用”。
- 最终验收摘要必须作为 Sprint 归档判断的主要阅读入口。
- 原始 AC 引用必须保留追溯性质，不直接覆盖最终归档结论。
- Workflow Sync 对 `acceptance-report.md` 的刷新必须服务于最终摘要和状态行，不制造新的双事实源。
- 历史未勾选 AC 不得导致已通过归档门禁的 Sprint 被误判为未完成。

## 4. 范围

### 4.1 包含

| 范围 | 说明 |
|---|---|
| Sprint 验收报告模板 | 后续 `iterations/change/<sprint>/acceptance-report.md` 应采用拆分结构。 |
| 最终验收摘要 | 汇总 Sprint archive readiness、Change archive 数、tasks 完成数、Sprint 状态、验收结论与人工 sign-off 状态。 |
| 原始 AC 引用 | 保留 REQ/BUG `acceptance.md` 来源、状态和必要摘录，但明确为追溯资料。 |
| Workflow Sync | 调整或约束 `acceptance-report.md` 的自动刷新口径，避免覆盖人工结论或强化混淆。 |
| Sprint archive 流程 | 归档关闭时更新最终摘要，而不是依赖逐条原始 AC 勾选作为唯一判断。 |
| 文档治理 | 明确最终摘要、原始 AC、人工 sign-off 的职责边界。 |

### 4.2 不包含

| 不包含 | 说明 |
|---|---|
| 批量重写历史 Sprint 报告 | 历史报告可作为参考，除非后续明确安排迁移或修复。 |
| 改写 REQ/BUG `acceptance.md` | 原始 AC 的编写、编号和勾选规则仍由 req/bug complete 阶段负责。 |
| 放宽归档门禁 | `/sprint-archive` 仍必须依赖 readiness gate、Change archive 和 tasks 完成情况。 |
| 新增业务功能 | 本需求不新增 Web 管理端、店主端、小程序或后端业务能力。 |
| 直接修改源码 | 本 PRD 不直接实现脚本或模板变更；后续必须评审后进入 OpenSpec Change。 |

## 5. 功能要求

### FR-001 报告结构拆分

`acceptance-report.md` MUST 至少包含以下职责清晰的章节：

| 章节 | 职责 |
|---|---|
| 最终验收摘要 | 展示 Sprint 是否满足关闭和归档判断。 |
| 最终归档检查 | 展示 readiness gate、Change archive、tasks 完成数、Sprint 状态等机器可验证结果。 |
| 原始 AC 引用 | 引用 REQ/BUG `acceptance.md`，用于追溯和人工复核。 |
| 人工 sign-off 记录 | 记录人工验收人、验收时间、遗留复核项或说明。 |

章节命名可在 OpenSpec 阶段微调，但 MUST 保持“最终判断”和“原始引用”两个层级分离。

### FR-002 最终验收摘要事实源

最终验收摘要 MUST 以 Sprint 归档事实为主要依据，包括：

- `validate-sprint-archive-readiness.py` 或等价 readiness gate 结果；
- Sprint 关联 Change 的 archived / applied / proposed 汇总；
- `tasks.md` 完成计数；
- `sprint.yaml` 的 `status` 与 `lifecycle_stage`；
- 人工 sign-off 状态和最终结论。

最终验收摘要 SHOULD 使用表格或固定字段，避免读者需要从原始 AC 勾选列表推断归档状态。

### FR-003 原始 AC 引用定位

原始 AC 引用 MUST 明确标注其用途为“来源追溯 / 人工复核参考”，不得与最终归档结论混为同一判断层级。

原始 AC 引用 SHOULD 保留以下信息：

- REQ/BUG 编号与标题；
- 来源 `acceptance.md` 路径；
- 当前 issue 状态与关联 Change 状态；
- 必要的 AC 摘录、范围摘要或链接；
- 若存在未勾选项，说明其是否为历史未 sign-off、人工待复核、已由最终摘要覆盖，或仍是阻断项。

### FR-004 未勾选项语义

原始 AC 中的 `- [ ]` MUST 有明确语义，至少区分：

| 类型 | 说明 |
|---|---|
| 待人工 sign-off | 实现和归档门禁已通过，但人工细项尚未逐条确认。 |
| 阻断归档 | 仍影响 readiness gate 或 Sprint close，必须阻断归档。 |
| 历史追溯 | 历史模板遗留或未迁移勾选状态，不作为当前归档判断。 |

报告中不得只保留裸 `- [ ]` 清单而无语义说明。

### FR-005 Workflow Sync 刷新口径

Workflow Sync 对 `acceptance-report.md` 的自动刷新 SHOULD 遵循以下约束：

- 可以刷新 workflow 派生 note、issue 状态行和 Change 状态摘要；
- 不得覆盖人工填写的最终验收结论、验收人或 sign-off 说明；
- 不得把原始 AC 未勾选项自动解释为 Sprint 未完成；
- 若正文无实质变化，不应仅因派生时间漂移刷新 `updated_at`；
- 状态刷新应优先落入最终摘要或明确的派生状态区。

### FR-006 Sprint archive 关闭口径

`/sprint-archive` 关闭 Sprint 时，MUST 优先维护最终验收摘要和最终归档检查：

- readiness gate PASS；
- Change 全部 archived；
- tasks 全部完成；
- Sprint 状态为 `completed` 且目录进入 `iterations/archive/`；
- 若仍需人工 QA 复核，应记录为 sign-off open item，而不是回退 Sprint 关闭状态。

### FR-007 兼容历史报告

本需求 SHOULD 优先影响后续新 Sprint 或后续被主动更新的验收报告。历史 `acceptance-report.md` 若存在大量未勾选 AC，可通过后续专项修复或人工 QA review 处理，不要求本需求默认批量迁移。

### FR-008 文档和模板一致性

后续 OpenSpec 阶段 SHOULD 同步检查以下位置是否需要更新：

- `/sprint-propose` 生成验收报告的模板或技能说明；
- `/sprint-archive` 对 `acceptance-report.md` 的关闭说明；
- Workflow Sync `patch_acceptance_report` 的刷新逻辑；
- Sprint 复盘或 fact sheet 对验收报告信号的提取逻辑；
- `rules/document-governance.md` 与 `rules/iterations-lifecycle.md` 中的验收报告职责描述。

## 6. UI 约束

本需求不涉及 Web、管理端、小程序或店主端可见 UI。若后续实现为文档模板或自动化脚本变更，文档输出应保持 Markdown 可读性：

- 标题层级清晰，避免把最终结论埋在长 AC 清单之后。
- 最终摘要使用短表格或固定字段，便于 AI、QA 和人工 reviewer 扫描。
- 原始 AC 引用应避免复制过长全文；可优先使用路径、状态摘要和必要摘录。
- Markdown 不使用 HTML 折叠作为唯一承载方式，避免脚本解析困难。

## 7. 关联需求与文档

| 类型 | 关联项 | 说明 |
|---|---|---|
| 相关流程 | `/sprint-propose` | 生成 Sprint 四件套与初始 `acceptance-report.md`。 |
| 相关流程 | `/sprint-archive` | 更新最终验收结论并关闭 Sprint。 |
| 相关脚本 | `scripts/workflow_sync/patch.py` | 当前包含 `patch_acceptance_report`，会刷新验收报告状态行与 note。 |
| 相关脚本 | `scripts/validate-sprint-archive-readiness.py` | Sprint 关闭前 readiness gate 的主要事实源。 |
| 相关脚本 | `scripts/generate-sprint-fact-sheet.py` | 会提取验收报告中的“最终/归档/通过/阻断/未完成”等信号。 |
| 相关规则 | `rules/document-governance.md` | 规定 Sprint 四件套与 Workflow Sync 文档治理。 |
| 相关规则 | `rules/iterations-lifecycle.md` | 规定 Sprint change/archive 阶段。 |
| 参考样例 | `iterations/archive/sprint-005/acceptance-report.md` | 展示最终归档检查通过但原始 AC 未勾选项大量并存的问题。 |

## 8. 风险与约束

| 风险 | 说明 | 缓解 |
|---|---|---|
| 双事实源继续存在 | 最终摘要和原始 AC 如果没有职责说明，仍会被读者混用。 | 强制章节职责说明，并明确未勾选项语义。 |
| 自动化覆盖人工结论 | Workflow Sync 若直接替换结论，可能擦掉人工 sign-off。 | 自动刷新限制在派生状态区，人工结论独立维护。 |
| 历史报告迁移成本高 | 归档 Sprint 报告多且格式不一。 | 默认不批量迁移，仅影响后续模板和主动更新文件。 |
| 归档门禁被误解为放宽 | 拆分 AC 可能被理解为不再需要验收。 | 明确 readiness gate、tasks、Change archive 仍是硬门禁。 |
| Fact Sheet 信号误判 | 现有信号提取可能从原始 AC 或遗留文案中读到“未完成”。 | 后续实现时同步调整信号优先级，优先读取最终摘要。 |

## 9. 状态块

```yaml
status: archived
readiness: Ready
next_step: /opsx-apply update-acceptance-report-summary-ac-reference
expected_openspec_change: update-acceptance-report-summary-ac-reference
needs_prototype: false
needs_api_change: false
needs_database_change: false
needs_orval: false
needs_docker_validation: false
```

## 10. 待完善项

- `/req-complete` 阶段补充 user stories、business flow 和 acceptance。
- 评审阶段确认是否只影响后续 Sprint，还是需要对 Sprint 005 等历史报告做专项修复。
- OpenSpec 阶段确认最终模板章节名、Workflow Sync 修改边界和 fact sheet 信号提取策略。
