---
sprint_id: sprint-021
title: Sprint 021 迭代经验复盘
status: draft
created_at: 2026-08-06 17:28:00
updated_at: 2026-08-06 17:28:00
owner: product
related_iteration: iterations/archive/sprint-021/
source: /sprint-exps sprint-021
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 021 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-09-03 09:00:00 ~ 2026-09-17 18:00:00 |
| REQ / BUG / Change | 1 / 7 / 10 |
| Change 批次 | 2 批；每批 5 个 Change |
| tasks 完成度 | 107/107 |
| 估算 | 10 SP / 10 人天 |
| 容量 | 30 人天；占用 33.33%；fix buffer 66.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；10/10 Change archived |
| stale scan | PASS；60 个文件，0 blocker，0 warning |
| AI usage | actual / present；fresh gate pass；矩阵 11 行 x 22 列 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-021 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-021 --json`、`iterations/archive/sprint-021/sprint.yaml`、`iterations/archive/sprint-021/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| AI usage freshness | 修复未来计划 `start_date` / `end_date` 被误当成 snapshot 新鲜度下限的问题 |
| OpenSpec archive 输出治理 | 吸收已知英文 scaffold warning、proposal warning stdout 与多行 warning 块 |
| docs-site 部署稳定性 | 移除 Mintlify cache volume 引发的 EBUSY 风险并同步部署文档 |
| Sprint close 治理 | 子文档 residual cleanup、business word stale scan、路径 residual gate 全部收口 |
| Sprint inclusion 与下一步参数 | 所有 Change apply 前必须纳入 Sprint；REQ/BUG 来源下一步命令保持原始 Issue ID |
| Scope 一致性 | Sprint 目标编号列表与 Scope 主表一致性进入校验链路 |

### Change 批次摘要

| Batch | Change 数 | Tasks | Blockers | Warnings | Next read |
|------|----------:|------:|---------:|---------:|-----------|
| batch-001 | 5 | 49/49 | 0 | 0 | none |
| batch-002 | 5 | 58/58 | 0 | 0 | none |

本 Sprint 没有 Fact Sheet warnings、没有 archived path residual、没有 needs_detail 触发项；复盘按 summary-first 完成，没有展开完整 `evidence_hints` 或逐个 raw tasks/trace。

## 2. 流程复盘

### 做得好的

1. **归档治理形成闭环**：10 个 Change 全部归档，107/107 tasks 完成，archive evidence 均为 `trace.md present`。
2. **Sprint close gate 有效前移问题**：readiness 初次发现 Issue 子文档中间态文案残留，修正后 stale scan 从 28 blockers 收敛到 0。
3. **大 Sprint 复盘采用批次摘要**：10 个 Change 触发 `change_batches`，复盘只使用批次数、tasks 聚合和 warning/blocker 数，避免逐个展开归档 Change。
4. **AI usage 快照真实可用**：post-command hook 刷新后，Fact Sheet fresh gate 为 pass，未来计划时间进入 skipped，不再误伤真实矩阵。
5. **路径残留为 0**：Sprint 迁移到 `iterations/archive/sprint-021/` 后，118 个文件 residual scan 通过，没有传播旧 active path。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| 归档后 Issue 历史记录仍容易携带中间态字面量 | stale scan 初次命中 28 个 blocker，集中在 trace、acceptance、root-cause 等子文档 | close 前需要额外清理文案，增加 Sprint 收尾成本 |
| stale scan 规则自身文档容易被递归误伤 | BUG-0121 文档为了说明阻断词而保留触发词，最终也被 close gate 命中 | 规则类 BUG 文档需要使用描述性语言或明确豁免语义 |
| Sprint 状态迁移后仍需二次同步 | `sprint.archive` Workflow Sync 成功后更新 2 处派生状态 | 四件套手工闭环后仍要以 Workflow Sync 兜底 |
| AI usage 成本非常高 | total_tokens 100,894,311；input_tokens 100,514,622；model_call_count 808 | 归档型治理 Sprint 如果反复读取规则、Change 和 Issue，会快速放大成本 |
| 多个治理 Change 串联产生范围漂移风险 | 本 Sprint 同时修改技能、规则、脚本、OpenSpec spec 和归档流程 | 需要用 scope / residual / stale / context-budget 多门禁组合防回退 |

### 优化建议

1. **将 stale scan 文案修复脚本化**：对已归档 Issue 的历史变更记录，将“进入/推进到中间状态”转换为“阶段资料完成/后续已闭环”。
2. **规则类 BUG 文档使用描述性词汇**：描述阻断词时尽量不用会触发 gate 的原始字面量，必要时用“评审阶段”“提案阶段”“归档未闭环”等业务化表达。
3. **Sprint archive 后立即跑 Fact Sheet summary**：确认 `path`、`status`、`lifecycle_stage`、fresh gate 和 residual count 都已更新。
4. **将 10+ Change 的复盘固定为 batch-first**：只在 batch warning、missing trace、inconsistent 或用户指定 focus 时读取原始证据。
5. **高成本治理 Sprint 拆分 apply/archive 批次**：优先按依赖分组，减少每次上下文同时携带 10 个 Change 的概率。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-021.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Freshness baseline | 2026-08-06T09:17:37Z | 来源：`sprint.md:updated_at`；未来计划 start/end 均进入 skipped |
| Generated at | 2026-08-06T09:17:44.185917Z | `data/ai-usage/sprints/sprint-021.json` |
| command_run_count | 76 | snapshot totals |
| model_call_count | 808 | snapshot totals |
| tool_call_count | 1,509 | snapshot totals |
| input_tokens | 100,514,622 | snapshot totals |
| cached_input_tokens | 97,104,512 | snapshot totals |
| output_tokens | 309,077 | snapshot totals |
| reasoning_output_tokens | 24,024 | snapshot totals |
| total_tokens | 100,894,311 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 11 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/sprint-021.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3533175 | 371111 | 0 | 0 | 277964 | 3341983 | 1129624 | 3516585 | 535576 | 4537180 | 4223262 | 11687713 | 0 | 4073316 | 26127367 | 0 | 19705414 | 15014259 | 0 | 0 | 2819782 |
| sprint-021 | 0 | 3533175 | 371111 | 0 | 0 | 277964 | 3341983 | 1129624 | 3516585 | 535576 | 4537180 | 4223262 | 11687713 | 0 | 4073316 | 26127367 | 0 | 19705414 | 15014259 | 0 | 0 | 2819782 |
| REQ-0102-sprint-goal-scope-consistency-validation | 0 | 0 | 371111 | 0 | 0 | 277964 | 0 | 1129624 | 0 | 535576 | 0 | 4223262 | 86558 | 0 | 0 | 5449637 | 0 | 2104866 | 4203763 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 371111 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | 0 | 1000642 | 0 | 0 | 0 | 0 | 648253 | 0 | 567268 | 0 | 762495 | 0 | 2212813 | 0 | 0 | 2564242 | 0 | 3170654 | 1735835 | 0 | 0 | 0 |
| BUG-0119-openspec-archive-scaffold-warning-noise | 0 | 656695 | 0 | 0 | 0 | 0 | 1007071 | 0 | 398042 | 0 | 992731 | 0 | 1715186 | 0 | 0 | 2215655 | 0 | 2984474 | 1728465 | 0 | 0 | 0 |
| BUG-0120-docs-site-mintlify-cache-ebusy | 0 | 653719 | 0 | 0 | 0 | 0 | 454063 | 0 | 733550 | 0 | 918627 | 0 | 1786009 | 0 | 0 | 3119210 | 0 | 740887 | 2480210 | 0 | 0 | 0 |
| BUG-0122-archive-sync-issue-subdoc-residual-cleanup | 0 | 428036 | 0 | 0 | 0 | 0 | 188340 | 0 | 381486 | 0 | 628266 | 0 | 1781627 | 0 | 4073316 | 2758656 | 0 | 2845561 | 1039985 | 0 | 0 | 0 |
| BUG-0121-stale-scan-pending-business-word | 0 | 746978 | 0 | 0 | 0 | 0 | 706495 | 0 | 960733 | 0 | 827674 | 0 | 3011489 | 0 | 0 | 3922771 | 0 | 3064821 | 2303309 | 0 | 0 | 0 |
| BUG-0123-openspec-archive-proposal-warning-stdout | 0 | 276395 | 0 | 0 | 0 | 0 | 312314 | 0 | 439291 | 0 | 363512 | 0 | 1531054 | 0 | 0 | 2375614 | 0 | 2447469 | 1460124 | 0 | 0 | 0 |
| BUG-0124-openspec-archive-multiline-proposal-warning-stdout | 0 | 47105 | 0 | 0 | 0 | 0 | 25447 | 0 | 36215 | 0 | 89978 | 0 | 168883 | 0 | 0 | 2194479 | 0 | 857057 | 130556 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3516236 | 368400 | 0 | 0 | 273638 | 3323919 | 1124495 | 3495377 | 533755 | 4522377 | 4214423 | 11644307 | 0 | 4053469 | 26064829 | 0 | 19604267 | 14970523 | 0 | 0 | 2804607 |
| sprint-021 | 0 | 3516236 | 368400 | 0 | 0 | 273638 | 3323919 | 1124495 | 3495377 | 533755 | 4522377 | 4214423 | 11644307 | 0 | 4053469 | 26064829 | 0 | 19604267 | 14970523 | 0 | 0 | 2804607 |
| REQ-0102-sprint-goal-scope-consistency-validation | 0 | 0 | 368400 | 0 | 0 | 273638 | 0 | 1124495 | 0 | 533755 | 0 | 4214423 | 86482 | 0 | 0 | 5439100 | 0 | 2103343 | 4190582 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 368400 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | 0 | 998168 | 0 | 0 | 0 | 0 | 644004 | 0 | 562875 | 0 | 759808 | 0 | 2203853 | 0 | 0 | 2558058 | 0 | 3167062 | 1728630 | 0 | 0 | 0 |
| BUG-0119-openspec-archive-scaffold-warning-noise | 0 | 651518 | 0 | 0 | 0 | 0 | 1001494 | 0 | 394058 | 0 | 989275 | 0 | 1708226 | 0 | 0 | 2210077 | 0 | 2979724 | 1724589 | 0 | 0 | 0 |
| BUG-0120-docs-site-mintlify-cache-ebusy | 0 | 651190 | 0 | 0 | 0 | 0 | 452403 | 0 | 730583 | 0 | 916905 | 0 | 1779257 | 0 | 0 | 3112484 | 0 | 715441 | 2475066 | 0 | 0 | 0 |
| BUG-0122-archive-sync-issue-subdoc-residual-cleanup | 0 | 425326 | 0 | 0 | 0 | 0 | 187035 | 0 | 378662 | 0 | 625456 | 0 | 1774934 | 0 | 4053469 | 2752149 | 0 | 2842470 | 1035997 | 0 | 0 | 0 |
| BUG-0121-stale-scan-pending-business-word | 0 | 743190 | 0 | 0 | 0 | 0 | 703381 | 0 | 956392 | 0 | 825058 | 0 | 3003008 | 0 | 0 | 3915252 | 0 | 3037353 | 2297413 | 0 | 0 | 0 |
| BUG-0123-openspec-archive-proposal-warning-stdout | 0 | 273642 | 0 | 0 | 0 | 0 | 310262 | 0 | 436658 | 0 | 362065 | 0 | 1525191 | 0 | 0 | 2369937 | 0 | 2439676 | 1455744 | 0 | 0 | 0 |
| BUG-0124-openspec-archive-multiline-proposal-warning-stdout | 0 | 46844 | 0 | 0 | 0 | 0 | 25340 | 0 | 36149 | 0 | 89833 | 0 | 168730 | 0 | 0 | 2189611 | 0 | 851259 | 130415 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 16939 | 2711 | 0 | 0 | 4326 | 18064 | 5129 | 21208 | 1821 | 14803 | 8839 | 43406 | 0 | 19847 | 62538 | 0 | 30535 | 43736 | 0 | 0 | 15175 |
| sprint-021 | 0 | 16939 | 2711 | 0 | 0 | 4326 | 18064 | 5129 | 21208 | 1821 | 14803 | 8839 | 43406 | 0 | 19847 | 62538 | 0 | 30535 | 43736 | 0 | 0 | 15175 |
| REQ-0102-sprint-goal-scope-consistency-validation | 0 | 0 | 2711 | 0 | 0 | 4326 | 0 | 5129 | 0 | 1821 | 0 | 8839 | 76 | 0 | 0 | 10537 | 0 | 1523 | 13181 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 2711 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | 0 | 2474 | 0 | 0 | 0 | 0 | 4249 | 0 | 4393 | 0 | 2687 | 0 | 8960 | 0 | 0 | 6184 | 0 | 3592 | 7205 | 0 | 0 | 0 |
| BUG-0119-openspec-archive-scaffold-warning-noise | 0 | 5177 | 0 | 0 | 0 | 0 | 5577 | 0 | 3984 | 0 | 3456 | 0 | 6960 | 0 | 0 | 5578 | 0 | 4750 | 3876 | 0 | 0 | 0 |
| BUG-0120-docs-site-mintlify-cache-ebusy | 0 | 2529 | 0 | 0 | 0 | 0 | 1660 | 0 | 2967 | 0 | 1722 | 0 | 6752 | 0 | 0 | 6726 | 0 | 2016 | 5144 | 0 | 0 | 0 |
| BUG-0122-archive-sync-issue-subdoc-residual-cleanup | 0 | 2710 | 0 | 0 | 0 | 0 | 1305 | 0 | 2824 | 0 | 2810 | 0 | 6693 | 0 | 19847 | 6507 | 0 | 3091 | 3988 | 0 | 0 | 0 |
| BUG-0121-stale-scan-pending-business-word | 0 | 3788 | 0 | 0 | 0 | 0 | 3114 | 0 | 4341 | 0 | 2616 | 0 | 8481 | 0 | 0 | 7519 | 0 | 4274 | 5896 | 0 | 0 | 0 |
| BUG-0123-openspec-archive-proposal-warning-stdout | 0 | 2753 | 0 | 0 | 0 | 0 | 2052 | 0 | 2633 | 0 | 1447 | 0 | 5863 | 0 | 0 | 5677 | 0 | 7793 | 4380 | 0 | 0 | 0 |
| BUG-0124-openspec-archive-multiline-proposal-warning-stdout | 0 | 261 | 0 | 0 | 0 | 0 | 107 | 0 | 66 | 0 | 145 | 0 | 153 | 0 | 0 | 4868 | 0 | 5798 | 141 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 55 | 10 | 0 | 0 | 4 | 54 | 12 | 43 | 5 | 52 | 23 | 91 | 0 | 31 | 154 | 0 | 133 | 111 | 0 | 0 | 30 |
| sprint-021 | 0 | 55 | 10 | 0 | 0 | 4 | 54 | 12 | 43 | 5 | 52 | 23 | 91 | 0 | 31 | 154 | 0 | 133 | 111 | 0 | 0 | 30 |
| REQ-0102-sprint-goal-scope-consistency-validation | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 12 | 0 | 5 | 0 | 23 | 1 | 0 | 0 | 25 | 0 | 9 | 28 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0118-fact-sheet-ai-usage-future-start-date-freshness | 0 | 6 | 0 | 0 | 0 | 0 | 13 | 0 | 8 | 0 | 9 | 0 | 20 | 0 | 0 | 14 | 0 | 15 | 12 | 0 | 0 | 0 |
| BUG-0119-openspec-archive-scaffold-warning-noise | 0 | 15 | 0 | 0 | 0 | 0 | 19 | 0 | 6 | 0 | 13 | 0 | 16 | 0 | 0 | 14 | 0 | 15 | 13 | 0 | 0 | 0 |
| BUG-0120-docs-site-mintlify-cache-ebusy | 0 | 7 | 0 | 0 | 0 | 0 | 4 | 0 | 6 | 0 | 7 | 0 | 12 | 0 | 0 | 14 | 0 | 11 | 13 | 0 | 0 | 0 |
| BUG-0122-archive-sync-issue-subdoc-residual-cleanup | 0 | 11 | 0 | 0 | 0 | 0 | 4 | 0 | 7 | 0 | 10 | 0 | 17 | 0 | 31 | 19 | 0 | 17 | 13 | 0 | 0 | 0 |
| BUG-0121-stale-scan-pending-business-word | 0 | 14 | 0 | 0 | 0 | 0 | 8 | 0 | 9 | 0 | 7 | 0 | 17 | 0 | 0 | 18 | 0 | 19 | 16 | 0 | 0 | 0 |
| BUG-0123-openspec-archive-proposal-warning-stdout | 0 | 7 | 0 | 0 | 0 | 0 | 5 | 0 | 6 | 0 | 5 | 0 | 13 | 0 | 0 | 15 | 0 | 27 | 15 | 0 | 0 | 0 |
| BUG-0124-openspec-archive-multiline-proposal-warning-stdout | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 2 | 0 | 0 | 12 | 0 | 18 | 2 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint four-piece | high | Fact Sheet token_risks：`sprint.md` 超过 200 行 | 复盘和归档均先读 Fact Sheet summary，只在 warning 时分段读取 |
| OpenSpec changes | high | 10 个 Change，107/107 tasks | 10+ Change 固定使用 `change_batches`，不默认展开每个 archived tasks/trace |
| Archive lookup | medium | archive paths 可由 sprint.yaml change ids 解析；residual_count 0 | 禁止宽泛扫描 `openspec/archive/**`，用 residual gate 定位 |
| Workflow Sync 输出 | medium | `sprint.archive` 检查 56 个子文档，更新 9 个验收结果 | 成功路径只记录 summary，不输出 detail |
| Stale scan 诊断 | medium | 初次 close 命中 28 个中间态文案 blocker | 只按 blocker 文件行修复，不全文展开 Issue 包 |
| AI usage markdown | medium | 4 张 11x22 矩阵必须写入复盘 | 矩阵由脚本渲染，避免读取原始 rows JSON |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认读取全部四件套、Issue trace、Change tasks |
| 10+ Change batch-first | 符合 | 使用 `change_batches` 聚合信息，未逐个读 raw tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 输出截断 | 符合 | 成功路径使用 summary 与聚合计数；未输出完整 evidence hints |
| 生成物控制 | 符合 | 没有展开 OpenAPI、Orval generated 或测试日志全文 |
| 已读摘要复用 | 符合 | 复用本会话已读 AGENTS、文档治理、目录、迭代生命周期、workflow-sync、sprint-archive 摘要 |
| 需要修正 | open | 归档文档中出现中间态字面量时，仍需要人工或脚本化改写才能通过 stale scan |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-021-001 | P1 | 为 Sprint close stale scan 增加“规则文档示例语义”安全表达或结构化豁免策略，避免规则类 BUG 文档递归误伤 | `/bug-capture` | open |
| T-021-002 | P1 | 沉淀归档后 Issue 历史记录文案 reconcile 脚本，将中间态历史表述转成闭环语义 | `/opsx-propose` | open |
| T-021-003 | P2 | 10+ Change Sprint 的 apply/archive 过程按 batch 输出固定摘要，减少重复读取 Change 证据 | `/req-capture` | open |
| T-021-004 | P2 | 将 AI usage markdown 矩阵写入复盘时自动保留高消耗来源模板，避免人工复制旧 Sprint 内容 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0102 聚焦 Sprint 目标与 Scope 一致性 | 来源于 sprint-020 目标列表遗漏，问题边界清晰，验收可脚本化 | 目标编号列表应纳入 `/sprint-propose` 与 Workflow Sync 后置校验 |
| BUG-0118 直接修复 AI usage freshness 误判 | 未来计划时间应作为 skipped，而不是 baseline candidate | 所有 Fact Sheet freshness 逻辑都应区分事实更新时间与计划时间 |
| BUG-0119/0123/0124 连续收敛 OpenSpec archive warning | 说明 wrapper 成功路径输出兼容噪音比预期复杂 | 对 CLI stdout/stderr 建立 known warning fixture，覆盖单行与多行块 |
| BUG-0120 表明 docs-site runtime cache 也属于部署治理 | 文档站启动失败不是文档问题，而是 Compose/runtime 边界问题 | docs-site 变更继续纳入部署与目录结构测试 |
| BUG-0121/0122 强化 Sprint close 子文档事实源 | close gate 不只看 Change tasks，也要看 Issue 子文档和验收语义 | 归档同步应在 close 前提供 dry-run reconcile 摘要 |
| 直接治理 Change 占 2 个 | `require-all-changes-sprint-before-apply` 与 `standardize-next-step-issue-ids` 没有单独 Issue 来源 | 非 REQ/BUG Change 也必须在 Sprint scope 中有估算和纳入理由 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | 本 Sprint 不改业务 API；治理脚本与文档为主 | 后续 API 变更仍必须同步 OpenAPI、Orval、docs 与 tests |
| DB | 本 Sprint 不改数据库结构 | 治理类脚本不得引入运行时 DB 依赖 |
| Web / 小程序 / 管理端 | 不涉及运行时 UI 代码 | 后续 UI 需求仍遵守 Design System semantic token |
| Docker / 部署 | BUG-0120 涉及 docs-site Compose 与 Dockerfile | 文档站容器行为必须纳入 deployment docs 与目录结构校验 |
| OpenSpec | 10 个 Change 全部归档，spec 合并完成 | archive wrapper 成功路径应吸收已知 CLI warning，同时保留未知异常 |
| 测试 | 重点集中在脚本级回归测试和门禁测试 | 对 stale scan、archive stdout、scope validation 继续保留成对正负用例 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Sprint Fact Sheet fresh baseline classifier | BUG-0118 | 将计划时间、事实更新时间、snapshot generated_at 三类时间源显式分类 |
| Archive stdout warning filter | BUG-0119/0123/0124 | 建立 known-warning block parser，单行/多行 fixture 全覆盖 |
| Issue subdocument residual reconciler | BUG-0122 | 归档前对 capture/review/root-cause/acceptance 的安全状态残留做 focused dry-run |
| Stale scan context classifier | BUG-0121 | 区分结构化状态、流程说明、普通业务正文和规则示例 |
| Sprint scope goal validator | REQ-0102 | 同步校验 `sprint.yaml`、`sprint.md` 目标列表、Scope 主表和 marker 派生块 |
| Next-step parameter normalizer | standardize-next-step-issue-ids | REQ/BUG 来源链路保留原始 Issue ID，非 Issue Change 才使用 change id |

## 6. 行动项

| ID | 优先级 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议下一步 | 状态 |
|----|--------|----------|------|------|----------|--------------|------|
| A-021-001 | P1 | BUG | stale scan 对规则类示例文档递归误伤 | BUG-0121 作为 stale scan 修复本身，归档后仍因示例字面量被 close gate 命中 | Sprint archive readiness、Issue 文档 | `/bug-capture` | open |
| A-021-002 | P1 | REQ | 归档后 Issue 历史记录文案自动 reconcile | 多个 Issue trace 保留“进入中间态”的历史措辞，当前状态已闭环但 close gate 仍阻断 | Workflow Sync、promote、stale scan | `/req-capture` | open |
| A-021-003 | P2 | REQ | 10+ Change Sprint 批次化 apply/archive 经验沉淀 | sprint-021 10 个 Change 复盘依赖 batch summary 才能控制上下文成本 | sprint-apply、sprint-archive、sprint-exps | `/req-capture` | open |
| A-021-004 | P2 | BUG | AI usage markdown 高消耗来源段落存在旧 Sprint 内容污染风险 | 本次需人工核对脚本渲染输出，避免复用旧 Sprint 高消耗来源说明 | Fact Sheet、sprint-exps | `/bug-capture` | open |

未自动创建 Issue。以上行动项可作为后续 `/capture`、`/req-capture` 或 `/bug-capture` 输入。
