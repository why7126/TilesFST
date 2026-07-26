---
sprint_id: sprint-012
title: Sprint 012 迭代经验复盘
status: draft
created_at: 2026-07-26 17:42:08
updated_at: 2026-07-26 17:42:08
owner: product
related_iteration: iterations/archive/sprint-012/
source: /sprint-exps sprint-012
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 012 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-07-26 15:15:24 ~ 2026-08-08 18:00:00 |
| REQ / BUG / Change | 6 / 0 / 6 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 143/143 |
| 估算 | 26 SP / 26.0 人天 |
| 容量 | 30 人天；占用 86.67%；fix buffer 13.33% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；6/6 Change archived |
| AI usage | Fact Sheet summary 标记 `estimated_fallback/stale`，warning 1；不可作为真实 token 统计展示 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-012 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-012 --json`、`iterations/archive/sprint-012/sprint.yaml`、`iterations/archive/sprint-012/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| Request Snapshot | API 请求日志补齐 method、path、route template、query/body 摘要、资源标识、状态、错误码、耗时、操作者、客户端和环境上下文 |
| 客户端请求身份 | 统一 Web 管理端、店主 Web 和微信小程序 `client_type` 与客户端请求标识，明确后端可信 `request_id` 边界 |
| Task Trace 关联模型 | 补强 `parent_request_id`、span `request_id` 与日志详情双向定位能力 |
| Task Trace 覆盖扩展 | 将任务链路从上传扩展到保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询等首批场景 |
| 审计日志链路 | audit log 支持 `task_trace_id` 与 `task_type`，敏感审计写入点可回到任务链路 |
| 观测仪表 | 管理端日志审计升级为链路观测入口，覆盖摘要、分布、排行、追踪 ID 查询和明细下钻 |

## 2. 流程复盘

### 做得好的

1. **平台治理主线集中**：6 个 REQ 都围绕日志、请求身份、Task Trace 和观测闭环展开，没有混入无关业务功能。
2. **OpenSpec 与 Sprint 闭环完整**：Fact Sheet 显示 6/6 Change archived，143/143 tasks 完成，关联 6 个 REQ 均进入 archive 阶段。
3. **归档路径残留门禁有效**：Sprint close 后 `checked_files=86`、`residual_count=0`，复盘没有继续传播旧 Sprint change 阶段路径或 active Change 路径。
4. **容量未超载**：26/30 人天，容量占用 86.67%，虽然 fix buffer 只有 13.33%，但未触发硬阻断。
5. **横切验收意识增强**：API、DB、OpenAPI/Orval、管理端、小程序和安全脱敏都被纳入 Sprint 横切清单。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Acceptance 正文有历史 stale 文案 | Fact Sheet acceptance signals 仍能看到部分 AC 证据为“待实现与测试” | Sprint 已归档，但验收报告正文容易让读者误判完成状态 |
| AI usage freshness 口径不稳定 | `/sprint-archive` hook 可刷新 snapshot，但 Fact Sheet summary 仍返回 `estimated_fallback/stale` | 复盘不能安全展示真实 token 矩阵，成本分析只能走风险估算 |
| Scope 横切面过大 | 6 个 REQ 同时触达 API、DB、三端客户端、管理端、审计、Task Trace | apply 阶段 token 和验证成本集中，后续需要更细的分段执行 |
| fix buffer 偏低 | `fix_buffer_ratio=13.33%` | 若中途出现生产缺陷或 DB drift，Sprint 容量回旋空间不足 |

### 优化建议

1. **归档前增加 acceptance stale phrase gate**：已 completed/archived 的 Sprint 若仍保留“待实现/待测试/planned”等正文，应输出 warning 或阻断。
2. **修正 AI usage summary freshness 口径**：当 post-command hook 已刷新 snapshot 时，Fact Sheet summary 应能稳定报告 `present/actual`。
3. **平台治理拆分为可验证薄片**：Request Snapshot、客户端身份、Task Trace 模型、Task Trace 覆盖、审计联动、dashboard 聚合各自保留独立验收矩阵。
4. **容量规划保留更高 fix buffer**：涉及 API/DB/日志/前端/小程序的治理 Sprint，建议保留至少 20% fix buffer。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 无 | Fact Sheet summary 标记 snapshot `stale`，`ai_usage_mode=estimated_fallback` |
| AI usage mode | estimated_fallback | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | stale | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| warning_count | 1 | Fact Sheet: `ai_usage_snapshot.warning_count` |
| reason | snapshot-stale | summary 推荐刷新 `data/ai-usage/sprints/sprint-012.json` |
| impact | 不能把矩阵或 totals 当真实统计展示 | 遵循 `/sprint-exps` 规则：非 actual 不展示真实 token 矩阵 |
| recommended_action | `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-012` | 需要本地 session JSONL 才能重新校准 |
| 主要输入消耗 | 估算集中在 OpenSpec apply/archive、Sprint propose、规则/Skill、Sprint 四件套与 Change trace/tasks | Fact Sheet token_risks：6 Change、143/143 tasks、四件套读取、archive lookup |
| 主要输出消耗 | 估算集中在测试摘要、Workflow Sync、归档报告和大 diff 摘要 | 本复盘只引用聚合计数，不复制日志全文 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、已读规则摘要复用、按需片段读取 | 符合 `rules/agent-context-budget.md` |

### 矩阵状态

本次不输出 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张矩阵。原因是 Fact Sheet summary 对 `sprint-012` 的 `ai_usage_snapshot` 判定为 `estimated_fallback/stale`；即使底层文件中存在聚合字段，也不能在复盘中作为真实统计展示。刷新 snapshot 后可重新运行 `/sprint-exps sprint-012` 或补充本章节。

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec changes | high | Fact Sheet token_risks：6 个 Change，143/143 tasks | 复盘只引用 Change 计数与任务聚合；apply 时按 Change 分段处理 |
| Sprint 四件套 | medium | 四件套合计 469 行，`sprint.md` 163 行 | 复盘默认使用 Fact Sheet summary；只在写回链时读尾部片段 |
| Archive lookup | medium | archive path 由 `sprint.yaml` change ids 解析 | 使用 resolver 和 residual gate，避免宽泛扫描 `openspec/archive/**` |
| Acceptance 长清单 | medium | acceptance-report 137 行，仍含部分 stale AC 文案 | 增加 stale phrase gate，输出命中行摘要而不是全文 |
| AI usage freshness | medium | summary 报 `snapshot-stale` | 将 hook refresh 与 Fact Sheet freshness 口径对齐 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次先运行 `--summary`，未默认展开全部 Sprint 四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 `sprint-exps` skill、Fact Sheet summary、README/样式片段和 Sprint 尾部回链位置 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 需要修正 | 是 | AI usage summary 对 actual/fallback 的判定仍不稳定，导致 token 章节降级 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 修复 `generate-sprint-fact-sheet.py --summary` 对 `/sprint-archive` hook 刷新后 snapshot 的 freshness 判定，避免 actual 被降级为 stale fallback | `/bug-capture` | open |
| T-002 | P1 | 为 completed/archived Sprint 增加 acceptance stale phrase gate，扫描“待实现/待测试/planned”等残留并输出行号摘要 | `/opsx-propose` | open |
| T-003 | P2 | 平台治理 Sprint 默认要求 fix buffer >= 20%，低于阈值时在 `/sprint-propose` 风险中标红 | `/opsx-propose` | open |
| T-004 | P2 | 为日志/Task Trace 类 Change 提供统一验收模板：API、DB、OpenAPI/Orval、管理端、小程序、安全脱敏、性能边界 | `/req-capture` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| 6 个 REQ 构成完整观测链路 | 从请求输入、客户端身份、任务链路、审计联动到 dashboard，需求设计有清晰递进 | 后续继续用“事实采集 → 关联模型 → 可视化入口”的三段式拆分平台治理需求 |
| Request Snapshot 与客户端身份强耦合 | `request_id`、`client_request_id`、`client_type` 边界决定日志可信度 | API 字段命名和 UI 文案必须持续区分可信服务端 ID 与可伪造客户端标识 |
| Task Trace 覆盖容易扩大 | 首批候选包含保存 SKU、批量、导入导出、媒体、异步、复杂查询 | 每类任务必须写清“纳入原因/未纳入原因”，防止一次性覆盖所有历史接口 |
| Dashboard 是展示层不是事实源 | 观测仪表依赖请求日志、行为事件、审计日志和 Task Trace 的统一口径 | dashboard Change 不应反向修改底层事实口径，除非另立 API/DB Change |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| 日志安全 | Snapshot 和 metadata 一旦落库，后端脱敏是最终边界 | 新增日志字段必须覆盖 Authorization、Cookie、Token、Secret、DSN、内部路径、原始文件名 |
| API / Orval | 日志详情响应和筛选字段变化会直接影响管理端 | API 变更必须同步 OpenAPI、Orval、docs 和前端测试 |
| SQLite / MySQL | 日志、审计、Task Trace 字段在 JSON 与索引列之间有生产差异 | DB 变更必须同步 schema drift、MySQL migration 和查询策略说明 |
| 管理端观测 UI | 长 ID、复制、fixed toast、移动端表格都容易回归 | 继续复用 admin-list 最佳实践和 `LogAuditPage.test.tsx` |
| 小程序请求封装 | fallback base URL 重试会影响客户端请求标识复用策略 | 小程序静态测试要覆盖 `client_type` 和 client request id 生成位置 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Request Snapshot builder | REQ-0071、REQ-0072 | 沉淀字段白名单、敏感字段黑名单、route template 降级、body schema 摘要为后端统一 helper |
| Client request identity helper | Web 管理端、店主 Web、小程序 | 三端用同名语义注入 `client_type` 和客户端请求标识，避免各端自行拼 header |
| Task Trace helper | REQ-0073、REQ-0074、REQ-0075 | 统一创建 trace、写 span、关联 request/audit log、失败兜底和 metadata 脱敏 |
| LogAudit detail sections | REQ-0071、REQ-0075、REQ-0076 | 管理端日志详情按 Snapshot、请求身份、Task Trace、审计上下文分组展示 |
| Observability query model | REQ-0076 | 聚合摘要、分布、排行、明细入口统一从同一筛选条件派生 |

## 6. Follow-up 建议

以下事项未自动创建 Issue。

| 建议命令 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议验收要点 | 来源 |
|----------|----------|------|------|----------|--------------|------|
| `/bug-capture` | BUG | Sprint Fact Sheet AI usage freshness 误报 stale fallback | sprint-012 关闭 hook 已刷新 snapshot，但 summary 仍报告 `estimated_fallback/stale` | `scripts/generate-sprint-fact-sheet.py`、`scripts/ai_usage.py`、复盘 token 章节 | hook 刷新后 summary 能稳定输出 `present/actual`；缺 session 时仍保留 fallback | sprint-012 / `/sprint-exps sprint-012` |
| `/opsx-propose` | 技术治理 | Completed Sprint acceptance stale phrase gate | sprint-012 acceptance 正文仍可检出“待实现与测试”类历史文案 | `scripts/validate-sprint-archive-readiness.py`、`acceptance-report.md` 生成/同步 | completed/archive 范围出现 stale phrase 时输出行号摘要或阻断 | sprint-012 / `/sprint-exps sprint-012` |
| `/req-capture` | 需求 | 日志与 Task Trace 验收模板标准化 | 日志治理类 Change 横跨 API/DB/Orval/Web/小程序/安全，验收清单重复出现 | `docs/knowledge-base/best-practices/`、OpenSpec task/test templates | 新建模板能被后续日志/Task Trace Change 引用，覆盖安全脱敏与跨端测试 | sprint-012 / `/sprint-exps sprint-012` |

## 7. 复盘结论

Sprint 012 是一次完成度高但横切面很宽的平台观测治理 Sprint。流程上，OpenSpec archive、Sprint archive、Issue archive 和路径残留门禁都顺利闭环；质量上，日志安全、请求身份、Task Trace 和管理端观测需要继续保持模板化验收。主要遗留不是业务实现，而是工作流工具链的观测口径：AI usage freshness 与 acceptance stale 文案需要被脚本化修正，避免后续复盘在“已经归档但证据表述不一致”的地方消耗注意力。

## 8. 更新文件

| 文件 | 动作 | 说明 |
|------|------|------|
| `docs/knowledge-base/retrospectives/sprint-012-retrospective.md` | 新建 | 本文档 |
| `docs/knowledge-base/README.md` | 更新 | 增加 sprint-012 复盘索引 |
| `iterations/archive/sprint-012/sprint.md` | 更新 | 增加复盘回链 |
