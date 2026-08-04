---
sprint_id: sprint-019
title: Sprint 019 迭代经验复盘
status: draft
created_at: 2026-08-04 23:15:03
updated_at: 2026-08-04 23:58:00
owner: product
related_iteration: iterations/archive/sprint-019/
source: /sprint-exps sprint-019
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 019 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-08-04 00:00:00 ~ 2026-08-18 18:00:00 |
| REQ / BUG / Change | 3 / 6 / 11 |
| Change 批次 | 3 批；5 + 5 + 1 个 Change |
| tasks 完成度 | 117/117 |
| 估算 | 24 SP / 24 人天 |
| 容量 | 30 人天；占用 80%；fix buffer 20% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；11/11 Change archived |
| AI usage | Fresh gate pass；已输出真实 token 成本矩阵 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-019 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-019 --json`、`iterations/archive/sprint-019/sprint.yaml`、`iterations/archive/sprint-019/acceptance-report.md`、`data/ai-usage/sprints/sprint-019.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 工作流证据治理 | archived Change 缺 `trace.md` 时支持最小 trace 或结构化 fallback；Sprint close readiness 更稳 |
| Fact Sheet summary 治理 | 10+ Change Sprint 使用 compact batch summary，降低复盘和归档读取成本 |
| 媒体对象治理 | 证书图片 key 前缀、历史对象漂移、缩略图和生产维护作业入口完成收口 |
| 小程序发布与 UI 修复 | Network 面板发布清单、品牌类目两列对齐、返回首页按钮二次点击回归修复 |
| 管理端展示治理 | 管理端列表字段 display adapter 检查表沉淀 |

### Change 批次摘要

| 批次 | Change 数 | tasks | warnings | blockers | recommended next read |
|------|----------:|------:|---------:|---------:|-----------------------|
| batch-001 | 5 | 53/53 | 0 | 0 | none |
| batch-002 | 5 | 57/57 | 0 | 0 | none |
| batch-003 | 1 | 7/7 | 0 | 0 | none |

本 Sprint 没有 Fact Sheet warnings、没有 archived path residual、没有 needs_detail 触发项，因此复盘按 summary-first 完成，没有展开完整 `evidence_hints` 或逐个 raw tasks/trace。

## 2. 流程复盘

### 做得好的

1. **sprint-018 行动项被快速产品化**：`auto-archive-trace-fallback`、`add-compact-fact-sheet-summary-for-large-sprints`、小程序 Network checklist 都来自上一轮复盘，说明复盘行动项能进入下一 Sprint 并闭环。
2. **大型 Sprint 的 batch-first 机制有效**：11 个 Change、117 个 tasks 没有靠人工逐项翻 trace，而是通过 Fact Sheet batch 摘要完成归档和复盘判断。
3. **媒体治理从单点 BUG 升级为生产维护能力**：证书图片 key 前缀修复、生产媒体维护作业、历史对象漂移修复形成了一条更完整的审计/迁移/复核链。
4. **Sprint archive gate 能捕捉文档事实漂移**：关闭前 stale scan 和 residual gate 清理了归档 Issue 子文档中间态文案与旧路径，最终 residual_count 为 0。
5. **AI usage hook 已能写入 sprint.exps command run**：archive 后 hook 可刷新 sprint snapshot，说明使用数据采集链路已基本可用。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| AI usage freshness baseline 误用未来计划 end_date | 修复前 Fact Sheet 将 `2026-08-18 18:00:00` 作为 `min_generated_at`；修复后跳过未来计划 end_date | 已通过 Change `fix-sprint-exps-ai-usage-matrix-freshness` 修复 |
| 缺少 sprint-015 风格的 AI usage Markdown 渲染命令 | summary 默认只提供 compact 矩阵摘要，fields 模式输出 JSON，技能执行时仍需临场把 JSON 转表 | 已新增 `--ai-usage-markdown`，直接输出 `Token Usage Fact Sheet` 与四张矩阵 |
| Sprint close stale scan 对业务词 `pending` 过敏 | 归档时历史媒体“pending 目录”类业务描述触发 stale blocker | 文档需改写为“暂存目录”，说明扫描规则需要区分状态词和业务路径语义 |
| 媒体验收仍依赖多类证据拼合 | key/object/URL/render、dry-run/apply、二次审计分散在不同文档和脚本 | 后续生产媒体类 BUG 仍可能出现证据散落与返修成本 |
| 容量虽然低于上限，但跨域多 | 3 REQ、6 BUG、11 Change，涉及 workflow、media、miniapp、admin、release | 多域同 Sprint 容易让验收标准和文档同步变复杂 |

### 优化建议

1. **把 AI usage fresh gate 从“可读”变成“可解释、可渲染”**：Fact Sheet 已暴露 `freshness_baseline`，并提供 `--ai-usage-markdown` 直接生成 sprint-015 风格表格，避免复盘阶段手工转换 JSON。
2. **stale scan 增加业务路径例外或字段语义判断**：媒体路径里的暂存语义不应与 Issue 生命周期状态同等处理，可按 fenced YAML 状态字段、表格状态列和普通正文分级。
3. **生产媒体维护作业沉淀为标准 runbook**：把 dry-run、快照、apply、二次审计、失败回滚、脱敏输出形成固定执行清单。
4. **继续推动 Sprint batch-first 输出**：sprint-archive、sprint-exps 成功路径只输出批次数、tasks 聚合、warning/blocker 数和 next read。
5. **复盘行动项先沉淀 capture 文案**：未授权自动 capture 时只输出标准 follow-up 文案，避免复盘命令悄悄改变 Issue 池。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-019.json`，Fact Sheet fresh gate 已通过 |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Freshness baseline | 2026-08-04T15:12:32Z | 来源：`sprint.md:updated_at`；未来计划 `end_date` 已跳过 |
| Generated at | 2026-08-04T15:32:41.758867Z | `data/ai-usage/sprints/sprint-019.json` |
| Command runs | 83 | 唯一 command run 汇总 |
| Model calls | 1038 | 模型调用总数 |
| Tool calls | 1868 | 工具调用总数 |
| Input tokens | 136124637 | 真实统计 |
| Cached input tokens | 130799360 | 真实统计 |
| Output tokens | 488276 | 真实统计 |
| Reasoning output tokens | 35146 | 真实统计 |
| Total tokens | 136700603 | 真实统计 |
| 矩阵规模 | 13 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

### 矩阵口径

`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/sprint-019.json` 经 `python scripts/generate-sprint-fact-sheet.py --sprint sprint-019 --ai-usage-markdown` 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3356965 | 774536 | 0 | 0 | 1183361 | 3856529 | 2946204 | 3480360 | 3081840 | 4463116 | 4463892 | 12570501 | 0 | 1649754 | 31258402 | 2907622 | 29072486 | 26199857 | 0 | 0 | 2562651 |
| sprint-019 | 0 | 3356965 | 774536 | 0 | 0 | 1183361 | 3856529 | 2946204 | 3480360 | 3081840 | 4463116 | 4463892 | 12570501 | 0 | 1649754 | 31258402 | 2907622 | 29072486 | 26199857 | 0 | 0 | 2562651 |
| REQ-0095-admin-list-field-display-adapter-checklist | 0 | 0 | 207162 | 0 | 0 | 357098 | 0 | 1046008 | 0 | 614015 | 0 | 2070081 | 0 | 0 | 0 | 1917683 | 0 | 710814 | 3213917 | 0 | 0 | 0 |
| REQ-0096-miniapp-network-panel-release-checklist | 0 | 0 | 567374 | 0 | 0 | 464596 | 0 | 992821 | 0 | 1445671 | 0 | 0 | 0 | 0 | 0 | 2566221 | 0 | 1806606 | 1344883 | 0 | 0 | 0 |
| REQ-0097-prod-compose-media-maintenance-job | 0 | 0 | 0 | 0 | 0 | 361667 | 0 | 907375 | 0 | 1022154 | 0 | 2393811 | 0 | 0 | 0 | 3233334 | 1670202 | 1553282 | 1900562 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4551689 | 0 | 4462252 | 0 | 0 | 0 | 0 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0112-certificate-image-object-key-prefix | 0 | 892315 | 0 | 0 | 0 | 0 | 854642 | 0 | 753300 | 0 | 590164 | 0 | 2015701 | 0 | 0 | 4677214 | 0 | 2715866 | 6322497 | 0 | 0 | 0 |
| BUG-0111-usage-docs-previous-version-semver-sort | 0 | 1865735 | 0 | 0 | 0 | 0 | 695700 | 0 | 477150 | 0 | 411655 | 0 | 1694079 | 0 | 0 | 362034 | 0 | 1684420 | 4119756 | 0 | 0 | 0 |
| BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | 0 | 257586 | 0 | 0 | 0 | 0 | 141630 | 0 | 389199 | 0 | 521740 | 0 | 2431191 | 0 | 0 | 362034 | 0 | 4651294 | 2820902 | 0 | 0 | 0 |
| BUG-0114-miniapp-brand-list-category-column-alignment | 0 | 341329 | 0 | 0 | 0 | 0 | 260879 | 0 | 567795 | 0 | 722410 | 0 | 1519574 | 0 | 0 | 4551689 | 0 | 4462252 | 1940604 | 0 | 0 | 0 |
| BUG-0115-miniapp-home-button-regression-after-second-click | 0 | 0 | 0 | 0 | 0 | 0 | 690323 | 0 | 710619 | 0 | 396897 | 0 | 1406657 | 0 | 0 | 3345812 | 0 | 4961000 | 1703751 | 0 | 0 | 0 |
| BUG-0116-prod-media-historical-object-drift | 0 | 0 | 0 | 0 | 0 | 0 | 1213355 | 0 | 582297 | 0 | 1820250 | 0 | 3503299 | 0 | 0 | 2576468 | 1237420 | 2168118 | 616546 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3340980 | 766658 | 0 | 0 | 1168679 | 3839050 | 2926981 | 3457932 | 3073397 | 4450925 | 4443275 | 12523681 | 0 | 1638062 | 31092064 | 2897121 | 29035434 | 26066242 | 0 | 0 | 2553209 |
| sprint-019 | 0 | 3340980 | 766658 | 0 | 0 | 1168679 | 3839050 | 2926981 | 3457932 | 3073397 | 4450925 | 4443275 | 12523681 | 0 | 1638062 | 31092064 | 2897121 | 29035434 | 26066242 | 0 | 0 | 2553209 |
| REQ-0095-admin-list-field-display-adapter-checklist | 0 | 0 | 204961 | 0 | 0 | 352187 | 0 | 1038639 | 0 | 611478 | 0 | 2063089 | 0 | 0 | 0 | 1888334 | 0 | 708751 | 3207870 | 0 | 0 | 0 |
| REQ-0096-miniapp-network-panel-release-checklist | 0 | 0 | 561697 | 0 | 0 | 459259 | 0 | 986590 | 0 | 1442293 | 0 | 0 | 0 | 0 | 0 | 2550758 | 0 | 1803918 | 1316323 | 0 | 0 | 0 |
| REQ-0097-prod-compose-media-maintenance-job | 0 | 0 | 0 | 0 | 0 | 357233 | 0 | 901752 | 0 | 1019626 | 0 | 2380186 | 0 | 0 | 0 | 3187354 | 1665246 | 1551624 | 1897059 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4542841 | 0 | 4456973 | 0 | 0 | 0 | 0 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0112-certificate-image-object-key-prefix | 0 | 887083 | 0 | 0 | 0 | 0 | 851330 | 0 | 749573 | 0 | 588284 | 0 | 2007314 | 0 | 0 | 4663406 | 0 | 2712883 | 6303404 | 0 | 0 | 0 |
| BUG-0111-usage-docs-previous-version-semver-sort | 0 | 1860669 | 0 | 0 | 0 | 0 | 692519 | 0 | 474301 | 0 | 410157 | 0 | 1687820 | 0 | 0 | 361088 | 0 | 1680944 | 4103146 | 0 | 0 | 0 |
| BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | 0 | 254863 | 0 | 0 | 0 | 0 | 140108 | 0 | 385855 | 0 | 519232 | 0 | 2423033 | 0 | 0 | 361088 | 0 | 4646823 | 2805401 | 0 | 0 | 0 |
| BUG-0114-miniapp-brand-list-category-column-alignment | 0 | 338365 | 0 | 0 | 0 | 0 | 259062 | 0 | 564873 | 0 | 720745 | 0 | 1512542 | 0 | 0 | 4542841 | 0 | 4456973 | 1937017 | 0 | 0 | 0 |
| BUG-0115-miniapp-home-button-regression-after-second-click | 0 | 0 | 0 | 0 | 0 | 0 | 686715 | 0 | 706640 | 0 | 395333 | 0 | 1400427 | 0 | 0 | 3336778 | 0 | 4955451 | 1700205 | 0 | 0 | 0 |
| BUG-0116-prod-media-historical-object-drift | 0 | 0 | 0 | 0 | 0 | 0 | 1209316 | 0 | 576690 | 0 | 1817174 | 0 | 3492545 | 0 | 0 | 2561371 | 1231875 | 2166211 | 593542 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 15985 | 7878 | 0 | 0 | 14682 | 17479 | 19223 | 22428 | 8443 | 12191 | 20617 | 46820 | 0 | 11692 | 122209 | 10501 | 37052 | 90054 | 0 | 0 | 9442 |
| sprint-019 | 0 | 15985 | 7878 | 0 | 0 | 14682 | 17479 | 19223 | 22428 | 8443 | 12191 | 20617 | 46820 | 0 | 11692 | 122209 | 10501 | 37052 | 90054 | 0 | 0 | 9442 |
| REQ-0095-admin-list-field-display-adapter-checklist | 0 | 0 | 2201 | 0 | 0 | 4911 | 0 | 7369 | 0 | 2537 | 0 | 6992 | 0 | 0 | 0 | 7622 | 0 | 2063 | 6047 | 0 | 0 | 0 |
| REQ-0096-miniapp-network-panel-release-checklist | 0 | 0 | 5677 | 0 | 0 | 5337 | 0 | 6231 | 0 | 3378 | 0 | 0 | 0 | 0 | 0 | 15463 | 0 | 2688 | 6359 | 0 | 0 | 0 |
| REQ-0097-prod-compose-media-maintenance-job | 0 | 0 | 0 | 0 | 0 | 4434 | 0 | 5623 | 0 | 2528 | 0 | 13625 | 0 | 0 | 0 | 23578 | 4956 | 1658 | 3503 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8848 | 0 | 5279 | 0 | 0 | 0 | 0 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0112-certificate-image-object-key-prefix | 0 | 5232 | 0 | 0 | 0 | 0 | 3312 | 0 | 3727 | 0 | 1880 | 0 | 8387 | 0 | 0 | 13808 | 0 | 2983 | 19093 | 0 | 0 | 0 |
| BUG-0111-usage-docs-previous-version-semver-sort | 0 | 5066 | 0 | 0 | 0 | 0 | 3181 | 0 | 2849 | 0 | 1498 | 0 | 6259 | 0 | 0 | 946 | 0 | 3476 | 16610 | 0 | 0 | 0 |
| BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | 0 | 2723 | 0 | 0 | 0 | 0 | 1522 | 0 | 3344 | 0 | 2508 | 0 | 8158 | 0 | 0 | 946 | 0 | 4471 | 15501 | 0 | 0 | 0 |
| BUG-0114-miniapp-brand-list-category-column-alignment | 0 | 2964 | 0 | 0 | 0 | 0 | 1817 | 0 | 2922 | 0 | 1665 | 0 | 7032 | 0 | 0 | 8848 | 0 | 5279 | 3587 | 0 | 0 | 0 |
| BUG-0115-miniapp-home-button-regression-after-second-click | 0 | 0 | 0 | 0 | 0 | 0 | 3608 | 0 | 3979 | 0 | 1564 | 0 | 6230 | 0 | 0 | 9034 | 0 | 5549 | 3546 | 0 | 0 | 0 |
| BUG-0116-prod-media-historical-object-drift | 0 | 0 | 0 | 0 | 0 | 0 | 4039 | 0 | 5607 | 0 | 3076 | 0 | 10754 | 0 | 0 | 15097 | 5545 | 1907 | 1644 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 41 | 17 | 0 | 0 | 13 | 42 | 25 | 37 | 22 | 39 | 29 | 84 | 0 | 30 | 236 | 22 | 171 | 170 | 0 | 0 | 26 |
| sprint-019 | 0 | 41 | 17 | 0 | 0 | 13 | 42 | 25 | 37 | 22 | 39 | 29 | 84 | 0 | 30 | 236 | 22 | 171 | 170 | 0 | 0 | 26 |
| REQ-0095-admin-list-field-display-adapter-checklist | 0 | 0 | 6 | 0 | 0 | 5 | 0 | 10 | 0 | 5 | 0 | 14 | 0 | 0 | 0 | 12 | 0 | 11 | 17 | 0 | 0 | 0 |
| REQ-0096-miniapp-network-panel-release-checklist | 0 | 0 | 11 | 0 | 0 | 4 | 0 | 7 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 25 | 0 | 13 | 10 | 0 | 0 | 0 |
| REQ-0097-prod-compose-media-maintenance-job | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 8 | 0 | 8 | 0 | 15 | 0 | 0 | 0 | 32 | 14 | 10 | 10 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 21 | 0 | 0 | 0 | 0 |
| REQ-0088-versioned-product-usage-docs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0112-certificate-image-object-key-prefix | 0 | 14 | 0 | 0 | 0 | 0 | 9 | 0 | 7 | 0 | 5 | 0 | 13 | 0 | 0 | 38 | 0 | 15 | 30 | 0 | 0 | 0 |
| BUG-0111-usage-docs-previous-version-semver-sort | 0 | 12 | 0 | 0 | 0 | 0 | 8 | 0 | 5 | 0 | 4 | 0 | 14 | 0 | 0 | 2 | 0 | 17 | 25 | 0 | 0 | 0 |
| BUG-0113-fact-sheet-ai-usage-fresh-gate-snapshot | 0 | 7 | 0 | 0 | 0 | 0 | 3 | 0 | 7 | 0 | 8 | 0 | 16 | 0 | 0 | 2 | 0 | 20 | 25 | 0 | 0 | 0 |
| BUG-0114-miniapp-brand-list-category-column-alignment | 0 | 8 | 0 | 0 | 0 | 0 | 3 | 0 | 6 | 0 | 7 | 0 | 12 | 0 | 0 | 24 | 0 | 21 | 12 | 0 | 0 | 0 |
| BUG-0115-miniapp-home-button-regression-after-second-click | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 8 | 0 | 4 | 0 | 12 | 0 | 0 | 20 | 0 | 26 | 12 | 0 | 0 | 0 |
| BUG-0116-prod-media-historical-object-drift | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 4 | 0 | 11 | 0 | 17 | 0 | 0 | 25 | 8 | 11 | 7 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint four-piece | high | Fact Sheet token_risks：`sprint.md` 超 200 行 | 复盘、archive、apply 优先使用 Fact Sheet summary；只在 warnings/needs_detail 时读片段 |
| OpenSpec changes | high | Fact Sheet token_risks：11 Change，117/117 tasks | 10+ Change 必须使用 `change_batches`，避免默认读取每个 raw tasks/trace |
| Archive lookup | medium | residual_count 0；archive paths 可由 sprint.yaml change ids 解析 | 禁止宽泛扫描 `openspec/archive/**`；用 residual gate 和 fact sheet 定位 |
| Stale scan 诊断 | medium | archive close 曾命中多个 Issue 子文档中间态词 | 输出 blocker 文件行即可，修复时按文件聚类，不展开整包 |
| AI usage freshness baseline | medium | 根因是未来计划 `end_date` 被误用为 `min_generated_at` | 使用四件套 `updated_at`、非未来 `end_date` 与 `start_date` 计算 baseline，并在 summary 暴露来源 |
| 媒体验收证据 | high | BUG-0112、BUG-0116 需要 key/object/URL/render 与 dry-run/apply | 沉淀媒体维护 runbook，减少每次重新构造证据链 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认展开全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 批次化读取 | 符合 | Sprint 有 11 个 Change，优先使用 `change_batches` 摘要 |
| 输出截断 | 符合 | summary 默认不输出完整矩阵；仅 fresh gate pass 后通过 fields 按需读取矩阵 |
| 已读摘要复用 | 符合 | 复用本会话已读工作流与归档规则摘要，仅补读 sprint-exps 与上下文预算 |
| 需要修正 | 已处理 | 修复 Fact Sheet freshness baseline，避免未来计划 end_date 造成 stale 误判 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-019-001 | P1 | 修复 Fact Sheet AI usage fresh gate 与 post-command hook actual 状态不一致的诊断链 | `fix-sprint-exps-ai-usage-matrix-freshness` | done |
| T-019-002 | P1 | stale scan 区分 Issue 生命周期中间态与媒体业务路径里的暂存语义 | `/bug-capture` | open |
| T-019-003 | P1 | 生产媒体维护作业沉淀标准 runbook，覆盖 dry-run、快照、apply、二次审计和脱敏输出 | `/req-capture` | open |
| T-019-004 | P2 | sprint-exps fresh gate pass 后自动调用 `--ai-usage-markdown` 输出复盘表格 | `fix-sprint-exps-ai-usage-matrix-freshness` | done |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0095 聚焦管理端列表 adapter 检查表 | 多个管理端列表问题不一定要改运行时代码，先统一展示口径很有价值 | 下一步把 adapter checklist 接入 Design System 或页面评审 checklist |
| REQ-0096 将 Network 面板验证纳入发布准备 | 端上网络证据无法完全自动化，适合放到发布清单而不是 Sprint 代码门禁 | miniapp-prepare/release-prepare 输出应包含人工验证状态和证据入口 |
| REQ-0097 与 BUG-0116 形成依赖链 | 先建立生产维护入口，再修历史媒体漂移，顺序合理 | 后续生产维护类需求应在 proposal 中明确依赖 BUG 和 runbook |
| BUG-0112 与 BUG-0116 都是媒体历史治理 | 单次上传修复不足以证明历史对象一致 | 媒体类缺陷默认要求当前路径、历史迁移、缩略图和 render 证据 |
| 小程序两个 BUG 都是体验一致性问题 | 对齐和重复点击是低代码量但高可见度问题 | 小程序 UI/导航应保留静态测试 + 体验版 checklist 的双层验收 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | 本 Sprint 默认不新增接口；媒体对象 key 值语义改变不等于 Schema 改变 | 若后续调整上传响应字段或 Schema，必须同步 OpenAPI / Orval / API 文档和 tests |
| DB | 未引入 schema 变更；生产维护作业处理历史数据和对象引用 | 维护作业必须保留 dry-run、幂等、快照和二次审计证据 |
| Web 管理端 | adapter checklist 比零散修样式更可复用 | 管理端列表/弹窗新增字段前先过 image/name/fallback adapter 检查 |
| 小程序 | 端上行为需要真实环境确认 | DevTools/体验版 Network evidence 不得写作自动通过，必须标记人工来源 |
| Workflow | archive/readiness/stale/residual gate 对 11 Change Sprint 仍有效 | 成功路径应继续 batch-first；失败路径按 blocker 文件行定位 |
| 文档治理 | Sprint close 前后路径残留清零 | 复盘文档只引用 archive path，不传播 active Change path |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Archive evidence fallback | `auto-archive-trace-fallback` | 将 trace-present、auto-generated-minimal-trace、fallback-summary-pass 做成所有 archive/readiness 调用方共用判断 |
| Large sprint compact summary | `add-compact-fact-sheet-summary-for-large-sprints` | Fact Sheet summary 默认输出批次、warning 和 token risks；矩阵按 fresh gate 和 `--ai-usage-markdown` 渲染 |
| Admin display adapter checklist | REQ-0095 | 管理端列表字段统一 image/name/status/fallback 映射和验收表 |
| Miniapp release network checklist | REQ-0096 | DevTools/体验版 Network evidence 标准化为发布前人工 gate |
| Production media maintenance runbook | REQ-0097 / BUG-0116 | 统一 dry-run、apply、snapshot、object audit、URL/render evidence 与脱敏日志要求 |

## 6. 行动项

| ID | 优先级 | 类型 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------|------------|------|
| T-019-001 | P1 | bug | Fact Sheet AI usage fresh gate 与 post-command hook actual 状态不一致，需要定位 snapshot freshness/mode 映射 | `fix-sprint-exps-ai-usage-matrix-freshness` | done |
| T-019-002 | P1 | bug | Sprint close stale scan 将媒体业务路径暂存语义误判为 Issue 中间态，需要增加语义区分 | `/bug-capture` | open |
| T-019-003 | P1 | requirement | 生产媒体维护作业沉淀 runbook，统一 dry-run、快照、apply、二次审计、脱敏输出和失败处理 | `/req-capture` | open |
| T-019-004 | P2 | workflow | sprint-exps 增加 focused AI usage fresh gate 字段读取，避免 fresh gate blocker 时误用 totals | `fix-sprint-exps-ai-usage-matrix-freshness` | done |
| T-019-005 | P2 | design-system | 管理端列表字段 adapter checklist 纳入页面评审和 Design System 示例页 | `/req-capture` | open |

## 7. 未自动创建 Issue 的 follow-up 文案

本次 `/sprint-exps sprint-019` 未获得自动 capture 授权，因此未自动创建 Issue。`T-019-001` 与 `T-019-004` 已由 `fix-sprint-exps-ai-usage-matrix-freshness` 处理；以下事项仍可独立用于后续 capture：

1. 建议命令：`/bug-capture`
   类型倾向：BUG
   标题：Sprint close stale scan 误判媒体暂存路径语义
   背景：生产历史媒体对象漂移文档中描述 SKU 图片暂存路径时，英文中间态词会被 stale scan 当作 Issue 生命周期残留。
   影响范围：`scripts/sprint_close_stale_scan.py`、媒体类 BUG 文档、Sprint close readiness。
   建议复现要点：在已 archived Issue 的正文或路径示例中保留媒体暂存目录语义，运行 `python scripts/check-sprint-close-stale-scan.py --sprint sprint-019`，确认是否误报。
   来源 Change/Sprint/命令：sprint-019 / `/sprint-exps sprint-019`。

2. 建议命令：`/req-capture`
   类型倾向：需求
   标题：生产媒体维护作业标准 runbook
   背景：REQ-0097 与 BUG-0116 已建立维护入口和历史漂移修复，但 dry-run、快照、apply、二次审计、脱敏输出仍需要统一操作说明。
   影响范围：`deploy/`、`docs/standards/`、媒体维护脚本、发布/生产运维流程。
   建议验收要点：runbook 覆盖执行前快照、dry-run、apply、失败处理、二次审计、证据归档和敏感信息脱敏。
   来源 Change/Sprint/命令：sprint-019 / `/sprint-exps sprint-019`。
