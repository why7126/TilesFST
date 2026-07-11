---
sprint_id: sprint-006
title: Sprint 006 迭代经验复盘
status: draft
created_at: 2026-07-11 20:17:47
updated_at: 2026-07-11 20:17:47
owner: product
related_iteration: iterations/archive/sprint-006/
related_requirements:
  - REQ-0020-theme-comfort-refine
  - REQ-0032-clipboard-copy-helper-best-practice
  - REQ-0033-acceptance-report-summary-ac-reference
  - REQ-0034-ai-token-usage-observability
related_bugs:
  - BUG-0062-archive-issue-subdoc-status-consistency
  - BUG-0063-archived-change-trace-fallback-summary
  - BUG-0064-theme-selector-sidebar-placement
related_changes:
  - update-theme-comfort-refine
  - add-clipboard-copy-helper-best-practice
  - update-acceptance-report-summary-ac-reference
  - add-ai-token-usage-observability
  - fix-archive-issue-subdoc-status-consistency
  - fix-archive-trace-fallback-summary-gate
  - fix-theme-selector-sidebar-placement
source: /sprint-exps sprint-006
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 006 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-07-11 17:50:09 ~ 2026-07-25 17:50:09 |
| 当前状态 | completed / archive |
| REQ | 4（全部 archive） |
| BUG | 3（全部 archive） |
| Change | 7（1 add-* + 2 update-* + 4 fix-*） |
| Change archived | 7/7；readiness gate PASS |
| 估算 | 39 SP / 26.0 人天 |
| 容量 | 30 人天；占用 87%；fix buffer 27% |
| tasks 完成度 | 108/108 |
| 主要质量簇 | 多主题舒适度、Clipboard helper、Sprint 验收报告治理、AI Token 使用量观测、归档门禁、主题选择器位置 |
| 主要风险 | fix buffer 低于 30%、归档门禁变严格后暴露子文档状态残留、AI usage 精确计量尚未落盘 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-006`、`iterations/archive/sprint-006/sprint.yaml`、`acceptance-report.md` 最终验收摘要、OpenSpec archive `tasks.md` 计数。

### 交付主线

| 主线 | 交付 |
|------|------|
| Web 体验 | `REQ-0020` 完成多主题与账号级偏好，`BUG-0064` 将主题选择器移入侧边栏用户头像上方 |
| 横切交互 | `REQ-0032` 沉淀 Clipboard copy helper 与代表场景测试 |
| 工作流治理 | `REQ-0033` 拆分 acceptance-report 最终摘要与原始 AC 引用；`BUG-0062`、`BUG-0063` 加固归档门禁 |
| 复盘观测 | `REQ-0034` 建立 AI usage fact source、解析、脱敏、聚合与 `/sprint-exps` 接入 |

## 2. 流程复盘

### 做得好的

1. **Sprint 005 行动项被直接产品化**：Clipboard fallback、acceptance-report 分层、归档 residual status gate、archived Change trace fallback、AI usage fact sheet 都进入 Sprint 006 并完成归档。
2. **归档门禁能发现真实问题**：Sprint archive 过程中，Issue 子文档 residual status gate 阻断了多个 REQ/BUG 包移动；修复后 residual status 为 0。
3. **Fact Sheet 先行降低复盘读取成本**：本次 `/sprint-exps` 先使用自动 Fact Sheet，warnings 为空、needs_detail 为 false，因此没有展开全部 trace/tasks。
4. **范围较 Sprint 005 收敛**：7 个 Change、108 tasks，相比 Sprint 005 的 10 个 Change、157 tasks，治理密度仍高但可控。
5. **最终 specs 可校验**：Sprint archive 后 `openspec validate --specs --strict` 24 项通过。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| fix buffer 仍偏低 | `sprint.yaml` 记录 fix buffer 7.0 人天 / 27% | 新增 P0/P1 时仍可能挤压主能力交付 |
| Issue 子文档状态不是天然闭环 | 归档门禁曾阻断子文档状态残留 | 若没有 gate，archive 后审计会看到 trace done 但子文档仍 pending/approved 的矛盾 |
| 精确 Token 统计缺失 | Fact Sheet 显示 `data/ai-usage/sprints/sprint-006.json` 不存在 | 复盘只能估算 token 风险，无法量化命令级高消耗 |
| planning 到 completed 的状态跨度过大 | Sprint archive 前四件套仍有 `planning` 残留，需要 archive 时修正 | 中间 apply 状态如果不及时同步，读者会误判 Sprint 阶段 |
| 治理 Change 与业务 Change 同 Sprint 交错 | 主题偏好涉及 API/DB/Orval/Web，归档门禁又同步变严格 | 任一端验证失败都会放大 Sprint close 成本 |

### 优化建议

1. **把 Issue 子文档状态修复前移**：在 `/opsx-archive` 的 promote 阶段通过脚本自动列出、必要时提供明确修复命令，而不是 Sprint close 后集中暴露。
2. **新增 Sprint apply 状态同步检查**：当所有 Change 已 applied 时，四件套 `status` 应先从 `planning` 或 `in_progress` 对齐到交付中状态。
3. **把 AI usage snapshot 生成纳入 Sprint close**：`REQ-0034` 已提供能力，后续 Sprint 应在 `/sprint-exps` 前生成 `data/ai-usage/sprints/<sprint>.json`。
4. **保持 archive 查询精确路径**：继续从 `sprint.yaml` Change 列表解析 archive 目录，避免全扫 `openspec/changes/archive/**`。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 无 | Fact Sheet 显示 `data/ai-usage/sprints/sprint-006.json` 不存在；本节不编造具体 token 数字 |
| 主要输入消耗 | 中 | Sprint 四件套 4 个文件、7 个 Change、108 tasks、7 个 Issue trace/status 证据 |
| 主要输出消耗 | 中 | Workflow Sync Report、readiness report、OpenSpec archive/validate 输出、git status 摘要 |
| 重复/浪费来源 | 中 | archive 阶段多次读取规则/技能和多次输出 Workflow Sync 全量 updated/skipped 行 |
| 已采用节省策略 | 有 | 先运行 Fact Sheet、warnings 为空不展开 trace/tasks、使用 `rg`/`find` 定位、成功日志只保留摘要 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec Change 队列 | medium | 7 个 Change、108/108 tasks | 按 Sprint 队列逐个 archive；复盘只引用 Fact Sheet 计数和 archive path |
| Workflow Sync 输出 | medium | 每次 opsx.archive / sprint.archive 都输出 updated/skipped 文件列表 | 成功路径引入 summary 模式；失败时再展开具体文件 |
| Issue residual status gate | medium | promote gate 阻断多个 Issue 子文档状态 | 将 residual 扫描结果聚合为 issue 级计数，必要时再显示文件明细 |
| Sprint 四件套 | medium | `sprint.md` 175 行，其他文件较短 | `/sprint-exps` 默认读 Fact Sheet；仅在 warnings/needs_detail 时分段读取原文 |
| Archive lookup | medium | Fact Sheet 标记 archive lookup 风险 | 从 `sprint.yaml` 精确解析 Change archive path，禁止宽泛扫 archive 历史 |
| 规则与 Skill 读取 | low to medium | source-command 系列任务都需要读 AGENTS/rules/skill | 同一会话复用规则摘要；只在文件变更或任务类型切换时补读 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | `/sprint-exps` 先运行文本与 JSON Fact Sheet，再决定无需展开原始 trace/tasks |
| 分段读取 | 符合 | 只读取 Sprint 005 样例、知识库索引和 sprint-006 回链片段 |
| archive 读取 | 符合但需谨慎 | 本次只使用 Fact Sheet 暴露的 archive path 和计数，没有全量读取 archive Change |
| 大输出处理 | 基本符合 | 校验通过时仅保留摘要；Workflow Sync 原始输出仍偏长，后续应摘要化 |
| 精确 token 计量 | 待改进 | `REQ-0034` 能力已归档，但本 Sprint 未生成 snapshot 文件 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 在 `/sprint-archive` 或 `/sprint-exps` 前自动生成 `data/ai-usage/sprints/<sprint>.json`，让复盘使用真实统计 | `/req-capture` | open |
| T-002 | P1 | 为 Workflow Sync 成功路径增加 summary 输出，默认展示 updated/skipped 计数和关键对象 | `/opsx-propose` | open |
| T-003 | P2 | 为 promote residual status gate 增加 issue 级摘要和可选明细模式，减少长表输出 | `/opsx-propose` | open |
| T-004 | P2 | 将同一会话已读规则摘要写入命令运行上下文，避免复盘/归档连续命令重复读取 | `/req-capture` | open |

## 3. 需求与设计

### 正向经验

| 条目 | 经验 |
|------|------|
| REQ-0020 | 多主题能力一次性覆盖 API、DB、Orval、Web 与 Design System，避免只做前端局部皮肤 |
| REQ-0032 | Clipboard helper 明确“helper 负责结果归一化，调用方负责 UI/埋点”，抽象边界清晰 |
| REQ-0033 | acceptance-report 分层后，最终验收事实和原始 AC 引用不再互相干扰 |
| REQ-0034 | AI usage 需求把脱敏、归因、聚合和复盘接入一起设计，避免后续只做日志堆积 |
| BUG-0062 / BUG-0063 | 归档门禁从经验建议变成脚本阻断，且报告可操作 |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| Token snapshot 未成为默认产物 | Fact Sheet 只能 estimated fallback | 下一 Sprint 将 usage extraction 纳入 close checklist |
| Sprint 状态流转仍依赖人工收尾 | archive 时才修正 planning/completed | Workflow Sync 可在 apply/archive 阶段更主动维护 Sprint 状态 |
| 子文档状态闭环需要手动修正 | promote gate 报告阻断后需批量改状态 | 提供脚本化 reconcile 或由 workflow-sync 维护子文档 frontmatter |

## 4. 开发与质量

### 重复 BUG / 模式

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| UI 控件位置与布局口径漂移 | BUG-0064、REQ-0020 | 主题能力与 Sidebar 信息架构耦合，控件位置需要明确归属 | 新增主题/偏好控件时先确认导航层级和用户头像区域契约 |
| 复制交互失败路径重复 | REQ-0032 承接 Sprint 005 BUG | Clipboard API 不可用、reject、空值、fallback 过去由页面各自处理 | 新复制入口必须复用 `copyTextToClipboard` 或同等 helper |
| 归档文档状态残留 | BUG-0062 | trace/status 与子文档 frontmatter/fenced YAML 不是同一事实源 | promote 前 residual gate 必须保持阻断 |
| archived Change 证据不完整 | BUG-0063 | 历史归档可能缺 trace | archived Change 必须有 `trace.md`，或 proposal/design/tasks 中有完整归档验证摘要 |
| AI 会话成本不可追溯 | REQ-0034 | 原始 session 数据敏感，过去没有脱敏事实源 | 仅提交聚合后的 safe snapshot，不提交 prompt、绝对路径、工具输出正文 |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 后端 / DB / API | `REQ-0020` 覆盖主题偏好持久化、current-user contract、OpenAPI / Orval 同步 |
| 前端 | `REQ-0020`、`REQ-0032`、`BUG-0064` 覆盖主题、复制 helper、Sidebar 位置和代表组件 |
| 工具链 | `REQ-0033`、`BUG-0062`、`BUG-0063`、`REQ-0034` 覆盖 workflow sync、readiness、promote gate、fact sheet 与 usage parser |
| 归档校验 | Sprint readiness 7/7 PASS；OpenSpec specs strict 24/24 PASS |
| 缺口 | Token usage snapshot 未在本 Sprint 复盘前生成，导致模型成本仍无法精确量化 |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| 多主题基础设施 | 主题 token、偏好持久化、首屏应用、Design System 预览 | 后续新页面默认加入主题验收矩阵，不再按页面补救 |
| Clipboard helper | `copyTextToClipboard` 及代表调用方迁移 | 新复制入口先写 helper 单测，再接业务文案与埋点 |
| Acceptance report 分层 | 最终摘要、归档检查、原始 AC 引用分区 | 后续 Sprint 归档报告只审最终摘要，AC 明细作为追溯材料 |
| Issue residual status scanner | promote gate 可阻断 archive 包残留状态 | 发展为 reconcile 工具或 workflow-sync 子命令 |
| AI usage fact source | parser、redaction、aggregation、Fact Sheet 接入 | 将 snapshot 生成纳入 `/sprint-exps` 前置步骤 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P1 | 将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程，避免继续 estimated fallback | `/req-capture` | 工具链 | open |
| A-002 | P1 | 为 Issue 子文档 residual status 增加自动 reconcile 或明确修复命令，减少手工批量改状态 | `/opsx-propose` | 工具链 | open |
| A-003 | P2 | Workflow Sync 增加 summary 输出模式，成功路径减少长 skipped 列表 | `/opsx-propose` | 工具链 | open |
| A-004 | P2 | 下一轮主题相关页面新增时，复用 `REQ-0020` 主题验收矩阵并补充截图/DOM 检查 | `/sprint-propose` | 前端 | open |
| A-005 | P2 | 为 Clipboard helper 建立 best-practice 文档，沉淀调用方文案、fallback 和敏感值边界 | `/req-capture` | 前端 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-006-retrospective.md` | 新建 | 本文档 |
| `best-practices/admin-list-page-consistency.md` | 沿用 | 继续作为管理端列表、toast、分页横切验收来源 |
| `best-practices/admin-modal-width-css-cascade.md` | 沿用 | 继续约束重置密码等弹窗宽度与滚动 |
| `best-practices/admin-form-page-consistency.md` | 沿用 | 继续约束设置/表单类页面固定错误区和 CTA |
| `best-practices/admin-media-upload-chain.md` | 沿用 | 本 Sprint 未触碰上传链路，保持 N/A 口径 |
| `best-practices/clipboard-fallback.md` | 建议后续新建 | REQ-0032 已提供 helper，可沉淀为长期最佳实践 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-07-11 20:17:47 | 初稿（`/sprint-exps sprint-006`） |
