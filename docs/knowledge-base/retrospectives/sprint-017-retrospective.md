---
sprint_id: sprint-017
title: Sprint 017 迭代经验复盘
status: draft
created_at: 2026-08-02 19:39:19
updated_at: 2026-08-02 19:39:19
owner: product
related_iteration: iterations/archive/sprint-017/
source: /sprint-exps sprint-017
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 017 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 实际周期 | 2026-08-01 10:35:08 ~ 2026-08-02 19:31:01 |
| REQ / BUG / Change | 5 / 1 / 6 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 109/109 |
| 估算 | 17.5 SP / 17.5 人天 |
| 容量 | 30 人天；占用 58.33%；fix buffer 41.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；6/6 Change archived |
| AI usage | `actual/present/pass`；可使用真实 token 矩阵 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-017 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-017 --json`、`iterations/archive/sprint-017/sprint.yaml`、`iterations/archive/sprint-017/acceptance-report.md`、`data/ai-usage/sprints/sprint-017.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 版本化产品使用文档 | 建立 `releases/<version>/usage-docs/`、manifest、按需生成/跳过决策、旧版本维护和公开安全校验 |
| 媒体验收治理 | 沉淀媒体五联验收模板和媒体类 BUG 四联验收模板，覆盖 key、object、URL、render、性能/降级和 N/A/blocked 口径 |
| Workflow 子文档同步 | 补齐 REQ/BUG 子文档状态同步、验收结果回填、drift check、Sprint close stale scan 和归档门禁 |
| 小程序展示修复 | 清理品牌列表页轮播图 `BRAND GALLERY` 与说明性文案，保持轮播能力不回归 |
| 品牌/证书缩略图 | 将真实缩略图生成与优先读取扩展到品牌图片和图片类品牌证书，覆盖后端、管理端、小程序、店主 Web 和存量补齐 |

## 2. 流程复盘

### 做得好的

1. **Sprint 收口非常完整**：6 个 Change 全部 archived，5 个 REQ 与 1 个 BUG 全部进入 archive/done，readiness、promote、residual、stale scan、Workflow Sync 和 AI usage hook 均闭环。
2. **治理型需求互相支撑**：REQ-0088 的 usage docs 治理、REQ-0089 的子文档同步、REQ-0090/0091 的媒体验收模板共同降低了 release、media、archive 三条链路的重复返工。
3. **媒体能力没有只修表层展示**：REQ-0092 覆盖真实缩略图生成、后端受控读取、管理端回显、小程序/店主端展示、存量 dry-run/apply 和媒体五联 evidence。
4. **关闭前门禁捕获了真实文档债**：`/sprint-archive` 前 stale scan 抓到 Sprint 四件套与已归档 Issue 子文档中的中间态残留，修复后 close scan 从 BLOCKED 转为 PASS。
5. **复盘读取边界符合预算规则**：本次复盘优先使用 Fact Sheet summary、residual JSON 和 AI usage snapshot，没有默认展开所有 Issue trace、Change tasks 或生成物 diff。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Sprint close 前仍有自然语言中间态残留 | readiness 初次报告曾命中 acceptance-report、release-note、Issue 子文档中的未闭环语义 | 机器状态已 done/archive，但人工阅读会误判为未实现、未验证或未归档 |
| 单个 archived Change 缺 `trace.md` | Fact Sheet warning：`fix-miniapp-brand-list-carousel-text` `change-trace-missing`，readiness 依赖 fallback summary pass | fallback 可接受，但证据入口不如 trace 稳定，后续检索成本更高 |
| REQ-0092 范围跨端且密度高 | Backend、Web/Admin、小程序、店主 Web、Storage、存量补齐、API/DB/Orval/Docker 条件影响 | 单 Change 跨面过宽时，验收证据容易分散，必须靠五联模板约束 |
| Token 消耗集中在 apply/archive/propose | AI usage 显示 `Opsx-Apply`、`Opsx-Archive`、`REQ-Opsx`、`Sprint-Propose` 为主要 token 消耗事件 | 说明高风险阶段仍需要更强的摘要复用、批次化读取和脚本化校验 |
| release 文档是否生成需要显式确认 | REQ-0088 明确 usage docs 不是每个版本都必须生成 | 发布命令若默认生成文档，会造成版本噪音和维护负担 |

### 优化建议

1. **把 close stale scan 前移到常规事件**：`opsx.archive` 和 `sprint.archive` 都应在写状态后立即检查中间态残留，减少最后关闭时集中返工。
2. **归档 Change trace/fallback 标准化**：单 Change archive 后若缺 `trace.md`，必须自动确认 fallback summary 覆盖命令、结果、验收、Issue/Sprint 状态、archive 路径和时间。
3. **跨端媒体能力拆分验收包**：后端对象/缩略图、管理端上传/列表、小程序展示、店主端展示、存量补齐分别给出 evidence 摘要，最后由媒体五联汇总。
4. **高 token 阶段强制 summary-first**：`opsx.apply`、`opsx.archive`、`sprint.propose` 默认先使用脚本摘要、diff stat 和 scoped evidence hints，再按 blocker 回读。
5. **发布文档 gate 保持“确认优先”**：`release-prepare` 必须先记录 generate / skip 决策，未确认时不得生成空 usage docs 目录。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-017.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Command run 数 | 53 | `ai_usage_snapshot.totals.command_run_count` |
| 模型调用数 | 749 | `ai_usage_snapshot.totals.model_call_count` |
| 工具调用数 | 1523 | `ai_usage_snapshot.totals.tool_call_count` |
| retry 数 | 0 | `ai_usage_snapshot.totals.retry_count` |
| input tokens | 100763730 | `ai_usage_snapshot.totals.input_tokens` |
| cached input tokens | 95984512 | `ai_usage_snapshot.totals.cached_input_tokens` |
| output tokens | 452003 | `ai_usage_snapshot.totals.output_tokens` |
| reasoning output tokens | 41561 | `ai_usage_snapshot.totals.reasoning_output_tokens` |
| total tokens | 101391477 | `ai_usage_snapshot.totals.total_tokens` |
| 主要输入消耗 | `Opsx-Apply`、`Opsx-Archive`、`REQ-Opsx`、`Sprint-Propose` | 四类事件合计占主要输入消耗 |
| 主要输出消耗 | `Opsx-Apply`、`Sprint-Propose`、`REQ-Opsx`、`REQ-Complete` | 输出主要来自实现/规划/规格与验收说明 |
| 重复/浪费来源 | close 前中间态残留修复、跨端媒体证据拼接、归档路径和 Issue 子文档扫描 | Fact Sheet warning 与 sprint archive 过程暴露 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、分段读取、已读规则摘要复用、未展开完整 evidence_hints | 符合 `rules/agent-context-budget.md` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 187256 | 2856726 | 0 | 0 | 2403431 | 659420 | 4196615 | 850601 | 5174200 | 1082104 | 16370849 | 1234958 | 0 | 0 | 28928512 | 3396569 | 16672359 | 14843823 | 0 | 0 | 2534054 |
| sprint-017 | 0 | 187256 | 2856726 | 0 | 0 | 2403431 | 659420 | 4196615 | 850601 | 5174200 | 1082104 | 16370849 | 1234958 | 0 | 0 | 28928512 | 3396569 | 16672359 | 14843823 | 0 | 0 | 2534054 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 661403 | 0 | 0 | 596464 | 0 | 1203042 | 0 | 953739 | 0 | 3445350 | 0 | 0 | 0 | 4866732 | 1904039 | 4656729 | 632384 | 0 | 0 | 0 |
| REQ-0090-media-five-point-acceptance-template | 0 | 0 | 311701 | 0 | 0 | 271845 | 0 | 378468 | 0 | 586176 | 0 | 2002843 | 0 | 0 | 0 | 1634447 | 1492530 | 3220629 | 2487916 | 0 | 0 | 0 |
| REQ-0091-media-bug-four-point-acceptance-template | 0 | 0 | 233454 | 0 | 0 | 237245 | 0 | 437088 | 0 | 952099 | 0 | 3065875 | 0 | 0 | 0 | 1328682 | 0 | 1583145 | 3010940 | 0 | 0 | 0 |
| REQ-0089-workflow-subdocument-status-sync | 0 | 0 | 517824 | 0 | 0 | 491894 | 0 | 606254 | 0 | 862089 | 0 | 2896494 | 0 | 0 | 0 | 7486453 | 0 | 2858719 | 2837075 | 0 | 0 | 0 |
| REQ-0092-brand-certificate-image-thumbnails | 0 | 0 | 1132344 | 0 | 0 | 805983 | 0 | 1571763 | 0 | 1820097 | 0 | 4960287 | 0 | 0 | 0 | 10481864 | 0 | 3108818 | 3380456 | 0 | 0 | 0 |
| BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | 0 | 187256 | 0 | 0 | 0 | 0 | 659420 | 0 | 850601 | 0 | 1082104 | 0 | 1234958 | 0 | 0 | 3130334 | 0 | 1244319 | 2495052 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 184558 | 2838822 | 0 | 0 | 2375540 | 655533 | 4159441 | 845145 | 5160500 | 1078350 | 16303516 | 1228983 | 0 | 0 | 28737509 | 3382804 | 16572618 | 14719920 | 0 | 0 | 2520491 |
| sprint-017 | 0 | 184558 | 2838822 | 0 | 0 | 2375540 | 655533 | 4159441 | 845145 | 5160500 | 1078350 | 16303516 | 1228983 | 0 | 0 | 28737509 | 3382804 | 16572618 | 14719920 | 0 | 0 | 2520491 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 658162 | 0 | 0 | 590274 | 0 | 1195689 | 0 | 951725 | 0 | 3432537 | 0 | 0 | 0 | 4837703 | 1896592 | 4623483 | 602969 | 0 | 0 | 0 |
| REQ-0090-media-five-point-acceptance-template | 0 | 0 | 308762 | 0 | 0 | 267130 | 0 | 372372 | 0 | 583726 | 0 | 1993574 | 0 | 0 | 0 | 1599202 | 1486212 | 3213728 | 2479439 | 0 | 0 | 0 |
| REQ-0091-media-bug-four-point-acceptance-template | 0 | 0 | 230631 | 0 | 0 | 232277 | 0 | 430012 | 0 | 948795 | 0 | 3053421 | 0 | 0 | 0 | 1292964 | 0 | 1578156 | 2998290 | 0 | 0 | 0 |
| REQ-0089-workflow-subdocument-status-sync | 0 | 0 | 514917 | 0 | 0 | 486578 | 0 | 601460 | 0 | 860028 | 0 | 2885717 | 0 | 0 | 0 | 7460085 | 0 | 2835187 | 2783635 | 0 | 0 | 0 |
| REQ-0092-brand-certificate-image-thumbnails | 0 | 0 | 1126350 | 0 | 0 | 799281 | 0 | 1559908 | 0 | 1816226 | 0 | 4938267 | 0 | 0 | 0 | 10424901 | 0 | 3105572 | 3369774 | 0 | 0 | 0 |
| BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | 0 | 184558 | 0 | 0 | 0 | 0 | 655533 | 0 | 845145 | 0 | 1078350 | 0 | 1228983 | 0 | 0 | 3122654 | 0 | 1216492 | 2485813 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 2698 | 17904 | 0 | 0 | 27891 | 3887 | 37174 | 5456 | 13700 | 3754 | 67333 | 5975 | 0 | 0 | 125145 | 13765 | 33143 | 80615 | 0 | 0 | 13563 |
| sprint-017 | 0 | 2698 | 17904 | 0 | 0 | 27891 | 3887 | 37174 | 5456 | 13700 | 3754 | 67333 | 5975 | 0 | 0 | 125145 | 13765 | 33143 | 80615 | 0 | 0 | 13563 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 3241 | 0 | 0 | 6190 | 0 | 7353 | 0 | 2014 | 0 | 12813 | 0 | 0 | 0 | 29029 | 7447 | 9647 | 7897 | 0 | 0 | 0 |
| REQ-0090-media-five-point-acceptance-template | 0 | 0 | 2939 | 0 | 0 | 4715 | 0 | 6096 | 0 | 2450 | 0 | 9269 | 0 | 0 | 0 | 12967 | 6318 | 6901 | 8477 | 0 | 0 | 0 |
| REQ-0091-media-bug-four-point-acceptance-template | 0 | 0 | 2823 | 0 | 0 | 4968 | 0 | 7076 | 0 | 3304 | 0 | 12454 | 0 | 0 | 0 | 14317 | 0 | 4989 | 12650 | 0 | 0 | 0 |
| REQ-0089-workflow-subdocument-status-sync | 0 | 0 | 2907 | 0 | 0 | 5316 | 0 | 4794 | 0 | 2061 | 0 | 10777 | 0 | 0 | 0 | 26368 | 0 | 2391 | 31670 | 0 | 0 | 0 |
| REQ-0092-brand-certificate-image-thumbnails | 0 | 0 | 5994 | 0 | 0 | 6702 | 0 | 11855 | 0 | 3871 | 0 | 22020 | 0 | 0 | 0 | 34784 | 0 | 3246 | 10682 | 0 | 0 | 0 |
| BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | 0 | 2698 | 0 | 0 | 0 | 0 | 3887 | 0 | 5456 | 0 | 3754 | 0 | 5975 | 0 | 0 | 7680 | 0 | 5969 | 9239 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 5 | 33 | 0 | 0 | 32 | 11 | 35 | 11 | 36 | 12 | 86 | 11 | 0 | 0 | 199 | 26 | 119 | 104 | 0 | 0 | 29 |
| sprint-017 | 0 | 5 | 33 | 0 | 0 | 32 | 11 | 35 | 11 | 36 | 12 | 86 | 11 | 0 | 0 | 199 | 26 | 119 | 104 | 0 | 0 | 29 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 7 | 0 | 0 | 5 | 0 | 8 | 0 | 5 | 0 | 16 | 0 | 0 | 0 | 35 | 10 | 27 | 11 | 0 | 0 | 0 |
| REQ-0090-media-five-point-acceptance-template | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 4 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 17 | 16 | 25 | 12 | 0 | 0 | 0 |
| REQ-0091-media-bug-four-point-acceptance-template | 0 | 0 | 6 | 0 | 0 | 4 | 0 | 5 | 0 | 8 | 0 | 19 | 0 | 0 | 0 | 18 | 0 | 18 | 14 | 0 | 0 | 0 |
| REQ-0089-workflow-subdocument-status-sync | 0 | 0 | 5 | 0 | 0 | 4 | 0 | 4 | 0 | 5 | 0 | 14 | 0 | 0 | 0 | 39 | 0 | 13 | 33 | 0 | 0 | 0 |
| REQ-0092-brand-certificate-image-thumbnails | 0 | 0 | 8 | 0 | 0 | 15 | 0 | 14 | 0 | 13 | 0 | 24 | 0 | 0 | 0 | 75 | 0 | 14 | 19 | 0 | 0 | 0 |
| BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | 0 | 5 | 0 | 0 | 0 | 0 | 11 | 0 | 11 | 0 | 12 | 0 | 11 | 0 | 0 | 15 | 0 | 22 | 15 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| `Opsx-Apply` | high | 28,928,512 total tokens；199 model calls | apply 阶段按 Change 分段处理，先读 tasks/status/delta headings，再按失败或缺证据回读实现细节 |
| `Opsx-Archive` | high | 16,672,359 total tokens；119 model calls | 归档证据、目录结构、Workflow Sync、Issue promote 输出默认摘要化，失败时只展开 blocker |
| `REQ-Opsx` | high | 16,370,849 total tokens；86 model calls | proposal/design/tasks 用模板化脚本和已有摘要，避免重复全量读取 rules/Skill |
| `Sprint-Propose` | high | 14,843,823 total tokens；104 model calls | 多次纳入同一 Sprint 时先用 `sprint.yaml` 与 scope summary，减少重复展开四件套 |
| Sprint four-piece | high | Fact Sheet token_risks：`sprint.md` 超 200 行 | 复盘、archive、apply 优先使用 Fact Sheet summary；只在 warnings/needs_detail 时读片段 |
| OpenSpec changes | medium | Fact Sheet token_risks：6 Change，109/109 tasks | 10 个以下可逐项摘要；10 个以上必须用 change_batches |
| Archive lookup | medium | residual_count 0；archive paths 由 sprint.yaml change ids 解析 | 禁止宽泛扫描 `openspec/archive/**`；用 residual gate 和 fact sheet 定位 |
| 媒体跨端证据 | high | REQ-0092 覆盖 Backend、Web/Admin、小程序、店主 Web、Storage | 将 evidence 分为对象、URL、缩略收益、端上渲染、存量补齐五类，复用媒体五联模板 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认展开全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 Fact Sheet、residual JSON、知识库索引、上期复盘样式和 Sprint 回链片段 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 已读摘要复用 | 符合 | `document-governance`、`directory-structure`、`iterations-lifecycle`、`agent-context-budget` 等规则沿用本会话已读摘要 |
| 需要修正 | 是 | 高风险命令仍有超高 input tokens，后续应把 summary-first、失败日志摘要和批次化读取变成脚本默认行为 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-017-001 | P1 | 将 archived Change trace/fallback 完整性检查前移并模板化，避免缺 trace 的 Change 依赖人工记忆补证 | `/opsx-propose` | open |
| T-017-002 | P1 | 为媒体五联验收增加 evidence 采集清单：object key、object exists、URL、thumbnail benefit、render | `/req-capture` | open |
| T-017-003 | P1 | 为 `opsx.apply` 和 `opsx.archive` 增加摘要优先模式，失败时只展开 blocker 文件片段 | `/opsx-propose` | open |
| T-017-004 | P2 | 将 Sprint close stale scan 的命中词从硬编码词扩展为“阶段语义 + 当前生命周期”判定，降低模板示例误报 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0088 重新定义 usage docs 为按需生成 | 发布文档不是版本发布的默认副产物，而是需要用户确认的公开内容 | release 系列命令必须先记录 generate/skip 决策，再生成或校验文档 |
| REQ-0090 与 REQ-0091 分别治理通用媒体能力和媒体类 BUG | 五联与四联边界清晰，能减少“修了对象但端上仍不可用”的验收漏洞 | 后续媒体 Change 在 proposal 阶段就应标明适用五联或四联 |
| REQ-0089 把子文档同步变成一等能力 | `trace.md`、主文档、acceptance、review 的状态语义更一致 | workflow sync 应继续承担派生块和子文档状态职责，避免人工改 marker |
| REQ-0092 跨端但验收口径明确 | 品牌/证书缩略图涉及多端、多文件、多存量策略，媒体五联成为必要约束 | 下一次类似能力可考虑拆成后端缩略图、管理端展示、端上消费三个 Change |
| BUG-0102 体量小但用户可见 | 小程序展示文案属于低复杂度高感知缺陷 | UI 文案类 BUG 应保持 Change 小、验收聚焦、影响范围清楚 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | Sprint 中多数治理能力不触发 API；REQ-0092 若新增字段则必须同步 OpenAPI/Orval | 后续涉及响应字段、上传字段或媒体 URL 字段时，必须同步 API docs、Orval 和 tests |
| DB | 使用缩略图字段或持久化对象 metadata 时会触发 DB 文档和 migration 风险 | 继续要求 DB 结构变更同步 schema、数据库文档和测试 |
| Object Storage / MinIO | 品牌/证书图片必须继续走后端受控 `/media/{object_key}` 或等价链路 | 前端和小程序不得直连未授权对象存储；存量补齐输出必须脱敏 |
| 小程序 | BUG-0102 验收强调不把 Web 静态测试等同真机通过 | release-prepare 仍需明确 DevTools、真机或体验版 evidence 的边界 |
| Sprint archive | stale scan 能有效阻断 closed 状态与文案事实冲突 | 模板示例中的中间态词也可能误报，规则需要更懂文档角色 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Usage docs release gate | REQ-0088 | 封装 generate/skip/pending_confirmation 三态，供 release-prepare、release-publish 和 usage-docs validate 共用 |
| Media five-point evidence block | REQ-0090 / REQ-0092 | 形成标准 evidence 表，可嵌入 Change tasks、Issue acceptance、Sprint acceptance-report |
| Media bug four-point evidence block | REQ-0091 / BUG-0102 后续媒体类 BUG | 区分原 BUG 场景、key/object/URL/render 与失败/阻塞记录 |
| Issue subdocument status reconciler | REQ-0089 | 常规 workflow event 写当前状态，archive promote 前只做补救性 reconcile |
| Sprint close stale semantic scanner | REQ-0089 / sprint archive | 从单纯关键词升级为“文件角色 + 当前生命周期 + target 状态”的判定器 |
| Brand/certificate thumbnail adapter | REQ-0092 | 复用 SKU 图片缩略图经验，形成品牌、证书、SKU 可共享的媒体派生策略 |

## 6. 行动项

| ID | 优先级 | 类型 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------|------------|------|
| T-017-001 | P1 | workflow | archived Change trace/fallback 完整性检查前移并模板化 | `/opsx-propose` | open |
| T-017-002 | P1 | requirement | 媒体五联 evidence 采集清单沉淀为可复用模板和脚本校验输入 | `/req-capture` | open |
| T-017-003 | P1 | workflow | 高 token 命令默认 summary-first，失败时只展开 blocker 片段 | `/opsx-propose` | open |
| T-017-004 | P2 | workflow | close stale scan 改进为语义化判断，降低模板示例误报 | `/opsx-propose` | open |
| T-017-005 | P2 | release | release-prepare 对 usage docs 生成/跳过决策输出固定摘要，防止默认创建空目录 | `/opsx-propose` | open |
| T-017-006 | P2 | miniapp | 小程序媒体/轮播验收区分 DevTools、真机、体验版 evidence，不互相替代 | `/req-capture` | open |

未自动创建 Issue；以上行动项仅作为后续 capture/propose 的标准输入。

## 7. 回链

- Sprint：`iterations/archive/sprint-017/`
- 归档 Change：`openspec/archive/2026-08-02-add-versioned-product-usage-docs/`、`openspec/archive/2026-08-01-add-media-five-point-acceptance-template/`、`openspec/archive/2026-08-01-add-media-bug-four-point-acceptance-template/`、`openspec/archive/2026-08-01-improve-workflow-subdocument-status-sync/`、`openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text/`、`openspec/archive/2026-08-02-add-brand-certificate-image-thumbnails/`
- 相关知识：`docs/knowledge-base/retrospectives/sprint-016-retrospective.md`、`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md`、`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
