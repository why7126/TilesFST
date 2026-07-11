---
sprint_id: sprint-005
title: Sprint 005 迭代经验复盘
status: draft
created_at: 2026-07-11 10:26:11
updated_at: 2026-07-11 10:26:11
owner: product
related_iteration: iterations/archive/sprint-005/
related_requirements:
  - REQ-0028-admin-list-page-contract
  - REQ-0029-admin-list-foundation-components
  - REQ-0030-api-docs-swagger-policy-checklist
  - REQ-0031-api-validation-envelope-governance
related_bugs:
  - BUG-0056-sprint-archive-incomplete-tasks-gate
  - BUG-0057-api-governance-tags-known-debt
  - BUG-0058-workflow-sync-check-time-drift-idempotency
  - BUG-0059-user-password-copy-not-working
  - BUG-0060-audit-log-request-id-copy-error
  - BUG-0061-change-password-policy-error-message-unclear
related_changes:
  - add-admin-list-page-contract
  - add-admin-list-foundation-components
  - fix-sprint-archive-incomplete-tasks-gate
  - update-api-docs-swagger-policy-checklist
  - fix-api-governance-route-tags-known-debt
  - fix-workflow-sync-check-time-drift-idempotency
  - fix-user-password-copy-not-working
  - fix-audit-log-request-id-copy-error
  - fix-change-password-policy-error-message
  - update-api-validation-envelope-governance
source: /sprint-exps sprint-005
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 005 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-07-04 22:30:20 ~ 2026-07-18 22:30:20 |
| 实际归档 | 2026-07-11 10:12:30（`/sprint-archive sprint-005`） |
| REQ | 4（全部 done / archive） |
| BUG | 6（全部 done / archive） |
| Change | 10（2 add-* + 2 update-* + 6 fix-*） |
| Change archived | 10/10；readiness gate PASS |
| 估算 | 40 SP / 29.0 人天 |
| fix-* 占比 | 6/10 = 60% |
| tasks 完成度 | 157/157 |
| 主要质量簇 | 管理端列表模板/组件、API governance、workflow tooling、Clipboard fallback、密码策略提示、validation envelope |
| 主要风险 | 容量超限、fix buffer 仅 15.0%、issue 子文档状态与 trace 派生状态不一致 |

### 交付主线

| 阶段 | 事件 |
|------|------|
| 2026-07-04 ~ 2026-07-05 | Sprint 从 REQ-0030 API docs checklist 起步，并承接 BUG-0057 / BUG-0058 两条治理债 |
| 2026-07-06 ~ 2026-07-07 | 追加一次性密码复制、修改密码策略提示两个管理端交互修复 |
| 2026-07-09 | 追加并闭环 `/sprint-archive` readiness gate、日志审计 `request_id` 复制兜底 |
| 2026-07-10 | 追加并完成 AdminListPage 契约与 MetricCard / pagination-window 基础组件 |
| 2026-07-11 | 追加并完成 API validation envelope 治理，随后归档 Sprint |

证据：`iterations/archive/sprint-005/sprint.yaml`、`sprint.md` Scope 表、`acceptance-report.md` 最终归档检查、OpenSpec archive `tasks.md`。

## 2. 流程复盘

### 做得好的

1. **Sprint 004 行动项被有效承接**：A-001 到 A-007 均在 Sprint 005 中转化为 REQ/BUG/Change，且全部归档。
2. **归档门禁从经验变成脚本**：BUG-0056 新增 readiness gate 后，Sprint 005 归档前能明确检查 10 个 Change 的 `tasks.md` 完成度。
3. **治理债集中闭环**：API tags、workflow-sync 时间漂移、API docs checklist、validation envelope 都从“反复噪声”转为可校验能力。
4. **管理端横切抽象向前推进**：AdminListPage 契约、MetricCard / MetricCardGrid、pagination-window 从页面修补提升为共享模板和基础组件。
5. **关键交互补齐失败路径**：一次性密码复制与日志 `request_id` 复制都覆盖 Clipboard API 不可用、reject、手动复制兜底。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Scope 继续膨胀 | Sprint 从 REQ-0030 起步，最终扩展到 4 REQ + 6 BUG，估算 40 SP / 29 人天 | 超过 2 人两周约 20 人天基线，计划容量失真 |
| fix 占比偏高 | 6/10 Change 为 fix-* | Sprint 仍在偿还上一轮横切债，新增主能力空间被压缩 |
| issue 子文档状态残留 | 部分 archive 下 `acceptance.md` / `root-cause.md` / `requirement.md` 仍显示 draft、pending_review、in_sprint | trace 与 workflow-sync 表已 done，但人工阅读子文档会产生状态歧义 |
| acceptance-report 正文和派生事实不完全一致 | 顶部结论为归档通过，但部分 AC 仍保留未勾选历史文本 | 审计时需要区分“原验收清单”和“最终归档事实” |
| Change trace 不完全统一 | `fix-api-governance-route-tags-known-debt` 归档目录缺少 `trace.md`，仅保留 proposal/design/tasks | 复盘和审计需要从 issue trace 或 tasks 侧补证据 |
| 归档早于计划结束日期 | 实际归档 2026-07-11，计划结束 2026-07-18 | 说明 Sprint 实际是治理冲刺闭环，而非完整两周节奏 |

### 优化建议

1. **Sprint freeze 规则升级**：进入 apply 后，非 P0/P1 或不影响归档的条目只进入下一 Sprint；超过 120% 容量时必须拆 Sprint。
2. **archive 后文档状态一致性检查**：增加脚本检查 archive 目录下 issue 子文档是否仍有 `draft`、`pending_review`、`in_sprint` 等遗留状态。
3. **acceptance-report 分层**：将“原始 AC 清单”和“最终归档门禁结论”分区展示，避免未勾选历史 AC 与已归档事实混在一起。
4. **Change trace 完整性门禁**：归档前检查 active / archived Change 是否保留 `trace.md` 或等价归档记录。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 无 | 当前仓库未暴露 Sprint 005 全部 AI 会话 input/output/cached token 元数据；本节不编造具体 token 数字 |
| 主要输入消耗 | 高 | Sprint 四件套、10 个 issue 包、10 个 OpenSpec archive、docs/API/OpenAPI/Orval 相关 diff、workflow-sync 输出 |
| 主要输出消耗 | 中高 | 多次 Workflow Sync Report、readiness report、OpenSpec validate、pytest/Vitest/build/Orval 输出、较大 `git diff` |
| 重复/浪费来源 | 中 | 早期流程容易重复全量读取 rules、Sprint 文档、archive Change、生成物 diff；Sprint 005 后半段已通过预算规则收敛 |
| 已采用节省策略 | 有 | `rules/agent-context-budget.md`、`sed -n` 分段、`rg` 定位、readiness 摘要、`git diff --stat` / focused diff、generated 文件不全文展开 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint 四件套与 acceptance-report 长正文 | high | `acceptance-report.md` 保留大量原始 AC 和横切 AC | 复盘读取优先 `sprint.yaml`、Scope 表、最终归档检查；AC 明细按条目聚合读取 |
| 10 个 OpenSpec archive | high | Sprint 005 包含 10 个 Change，且 tasks 总数 157 | 按 change 分批处理；先读 `tasks.md` checkbox、trace 验证摘要和 delta headings |
| OpenAPI / Orval 生成物 | high | BUG-0057、BUG-0061、REQ-0031 均涉及 OpenAPI / Orval | 默认只看 `git diff --stat`、目标 schema 片段和生成命令摘要，不展开 generated 全文 |
| Workflow Sync 输出 | medium | sprint.archive 与 opsx.archive 会输出多条 issue/registry skipped/updated 行 | 成功时只保留 report 摘要；失败时再定位具体 marker |
| 测试日志 | medium | pytest、Vitest、build、validate-api-standard 在多个 Change 中重复出现 | 成功只记录命令 + passed 数；失败只截取失败用例和关键堆栈 |
| archive 目录宽泛搜索 | medium | 复盘天然需要读取已归档 Change | 从 `sprint.yaml` 的 Change 列表构造精确路径，避免 `rg` 全扫 `openspec/changes/archive/**` |
| 规则与 Skill 重复读取 | low to medium | source-command 类任务都需要读 AGENTS/rules/skill | 同一会话复用已读规则摘要；仅当文件有改动或任务类型新增时重读 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| 先定位再读取 | 符合 | 使用 `find` / `rg` 先定位 issue、Change、knowledge-base 文件 |
| 分段读取 | 符合 | 对长文档使用 `sed -n` 读取关键片段 |
| 不全文展开 generated | 符合 | 未读取 `src/web/src/shared/api/generated.ts` 全文 |
| archive 读取 | 有必要但需收敛 | `/sprint-exps` 必须读 Sprint 内 archived Change；后续可用脚本生成摘要 |
| 大输出处理 | 需继续优化 | `git diff` 和 acceptance-report 仍容易产生长输出，应优先 stat/heading 摘要 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为 `/sprint-exps` 增加 Sprint facts 摘要脚本，自动汇总 Change tasks、trace 验证、issue 状态残留 | `/opsx-propose improve-sprint-exps-fact-sheet` | open |
| T-002 | P1 | 为 archive issue 子文档状态残留增加检查，减少复盘时人工检索和状态歧义 | `/bug-capture` | open |
| T-003 | P2 | 为 Workflow Sync 成功报告增加 `--summary` 模式，仅输出 updated/skipped 计数和关键文件 | `/req-capture` | open |
| T-004 | P2 | 为 OpenAPI/Orval 变更复核沉淀 diff 摘要命令，默认输出 schema/operation 级摘要 | `/req-capture` | open |

## 3. 需求与设计

### 正向经验

| 条目 | 经验 |
|------|------|
| REQ-0028 | 从 BUG-0055 的 8 页面不一致中抽象出 AdminListPage 契约，方向正确：先契约、验收页、代表页，再推广 |
| REQ-0029 | MetricCard / MetricCardGrid / pagination-window 将 DOM 契约变成组件和工具，降低后续页面漂移 |
| REQ-0030 | API docs checklist 把 dev、Docker、production 代理和 Try It Out 策略写成固定门禁，避免只靠页面文案 |
| REQ-0031 | validation envelope 把 Pydantic 默认 422 纳入统一错误响应，连同 Web parser、OpenAPI/Orval、上传路径一起治理 |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| Issue 子文档状态事实源分散 | trace 已 done，但 acceptance/root-cause/review 仍可能保持旧状态 | workflow-sync 或独立检查应覆盖 archive issue 包内关键子文档 |
| 验收报告正文过长 | 归档结论和原始 AC 清单混排 | 增加“最终验收摘要”并把 AC 明细折叠为引用路径 |
| 容量门禁不够硬 | 29 人天仍继续归档闭环 | `/sprint-propose` 对超容量追加项要求明确“替换/延期/拆分”选择 |

## 4. 开发与质量

### 重复 BUG / 模式

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| Clipboard API 只覆盖成功路径 | BUG-0059、BUG-0060 | 浏览器权限、非安全上下文、API 不存在时缺 fallback | 抽象共享复制 helper 或至少建立 Clipboard fallback checklist |
| API 契约元数据治理不足 | BUG-0057、REQ-0031 | 源码级校验不足以保证最终 OpenAPI 契约正确 | 所有 API governance 必须校验最终 OpenAPI，而不只校验源码启发式规则 |
| 文档时间/状态语义混用 | BUG-0058、Sprint archive | `updated_at` 曾被误用为归档事实；子文档状态未完全派生 | 明确事实时间、维护时间、派生状态三类字段边界 |
| 管理端列表 DOM 漂移 | REQ-0028、REQ-0029、BUG-0060 | 页面局部复制结构导致指标卡、分页、toast 行为不一致 | 新列表页默认复用 AdminListPage / MetricCard / pagination-window |
| 表单错误反馈泛化 | BUG-0061、REQ-0031 | 后端策略失败折叠，前端只能展示泛化 message | API error 应保留可解释失败项，Web 映射字段或固定错误区 |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 后端 | BUG-0061 覆盖密码策略多失败项；REQ-0031 覆盖 validation envelope、上传缺文件、业务 AppError 不被覆盖 |
| 前端 | BUG-0059 / BUG-0060 覆盖 Clipboard 成功、reject、API 不存在；REQ-0028 / REQ-0029 覆盖 DOM 契约 |
| 工具链 | BUG-0056 覆盖 readiness gate；BUG-0058 覆盖 workflow-sync no delta |
| 文档/治理 | REQ-0030 固化 API docs checklist；BUG-0057 增强最终 OpenAPI tags 校验 |
| 缺口 | acceptance-report 和 issue 子文档状态一致性尚缺自动测试 |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| `AdminListPage` | 已建立模板契约、设计系统样例和代表页接入 | 下一 Sprint 可按低风险页面逐页迁移，不做一次性大改 |
| `MetricCard` / `MetricCardGrid` | 已沉淀稳定 DOM class 和布局能力 | 新管理端列表页禁止局部复制 summary-grid |
| `pagination-window` | 已形成共享分页窗口工具和边界测试 | 后续删除页面局部旧实现，保留兼容期 |
| Clipboard fallback | 两个 BUG 形成相似模式 | 抽象 `copyTextWithFallback` 或沉淀 best-practice |
| validation envelope parser | 已扩展后端 handler 与 Web parser | 后续表单统一消费 `message` 与 `data.errors[]` |
| workflow fact sheet | readiness gate 已证明可行 | 为 sprint-exps / archive 增加统一事实摘要脚本 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P0 | 在归档后增加 issue 子文档状态一致性检查，发现 archive 包内残留 draft/pending_review/in_sprint | `/bug-capture` | 工具链 | open |
| A-002 | P1 | 为 Clipboard 复制交互沉淀共享 helper 或 best-practice，覆盖成功、失败、API 不存在、手动复制 | `/req-capture` | 前端 | open |
| A-003 | P1 | 将 Sprint 容量超限纳入 `/sprint-propose` 硬提示，超过 120% 必须拆分或替换范围 | `/opsx-propose` | 流程 | open |
| A-004 | P1 | 为 `/sprint-exps` 增加自动 Fact Sheet，减少人工读取四件套、trace、tasks 的 token 消耗 | `/opsx-propose improve-sprint-exps-fact-sheet` | 工具链 | open |
| A-005 | P2 | 将 acceptance-report 拆成最终验收摘要 + 原始 AC 引用，避免历史未勾选项干扰归档判断 | `/req-capture` | QA/产品 | open |
| A-006 | P2 | 检查 archived Change 是否缺失 `trace.md`，缺失时要求 proposal/design/tasks 至少有归档验证摘要 | `/bug-capture` | 工具链 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-005-retrospective.md` | 新建 | 本文档 |
| `best-practices/admin-list-page-consistency.md` | 沿用 | REQ-0028 / REQ-0029 已将经验产品化为模板和组件 |
| `best-practices/admin-modal-width-css-cascade.md` | 沿用 | BUG-0059 / BUG-0061 继续依赖弹窗布局稳定性 |
| `best-practices/admin-form-page-consistency.md` | 沿用 | REQ-0031 / BUG-0061 强化字段错误与固定错误区 |
| `best-practices/admin-media-upload-chain.md` | 沿用 | REQ-0031 将上传参数校验纳入 validation envelope |
| `best-practices/clipboard-fallback.md` | 建议后续新建 | BUG-0059 / BUG-0060 暴露重复复制兜底模式 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-07-11 10:26:11 | 初稿（`/sprint-exps sprint-005`） |
