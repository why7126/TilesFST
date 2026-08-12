---
title: sprint-022 复盘
purpose: 复盘 sprint-022 的流程、需求、开发质量、可复用抽象与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-022
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-12 00:25:00
updated_at: 2026-08-12 00:25:00
---

# sprint-022 复盘

## 概况

sprint-022 已完成归档，目录为 `iterations/archive/sprint-022/`。本 Sprint 覆盖 7 个 REQ、4 个 BUG、18 个 OpenSpec Change，229/229 个任务完成，验收状态为 passed。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 治理流程 | `/spec-study`、spec-logs、capture/explore/modify 路由、git-check、引导式反馈 | 纯治理 Change 适合小颗粒串行归档，但必须避免旧路径和中间态残留 |
| 小程序媒体性能 | BUG-0125、BUG-0126 | 缩略图 URL 语义、对象审计、Network/render evidence 必须同时闭环 |
| 商品与前台展示 | REQ-0103、REQ-0104、REQ-0106 | 排序/置顶/隐藏标题属于多端展示契约，后端字段、前台解释性和榜单边界要一起验收 |
| 管理端体验与性能 | REQ-0107、REQ-0108、REQ-0109、BUG-0127、BUG-0128、REQ-0110 | 管理端列表、弹窗、表格、冻结列、分页和用户菜单模式有明显复用空间 |

批次事实来自 `generate-sprint-fact-sheet.py --summary`：

| Batch | Change 数 | Tasks | Blockers | Warnings | Next Read |
|-------|----------:|------:|---------:|---------:|-----------|
| batch-001 | 5 | 30/30 | 0 | 0 | none |
| batch-002 | 5 | 77/77 | 0 | 0 | none |
| batch-003 | 5 | 64/64 | 0 | 0 | none |
| batch-004 | 3 | 58/58 | 0 | 0 | none |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-022 --json` 报告 `residual_count=0`。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| Sprint 收尾 | `/sprint-archive` 后 readiness、stale scan、residual gate 全部通过 | 先用 Fact Sheet 和 gate 聚合事实，再修正旧路径和中间态文案 |
| 大 Sprint 控制 | 18 个 Change 被拆成 4 个 batch，summary 中每批均有 tasks/trace 计数 | 10+ Change Sprint 默认按 batch 报告，不展开所有 tasks |
| Issue 闭环 | 7 个 REQ、4 个 BUG 的验收结果全部 passed | `acceptance_status` 与 trace 的 done/archived 语义必须同步 |
| 治理演进 | spec-study、spec-logs、git-check、引导式反馈契约被纳入治理资产 | 治理 Change 不触碰业务 `src/` 时仍要走 Sprint Inclusion Gate |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| 旧路径残留 | Sprint 归档后部分 archived Change 文档仍引用 `iterations/change/sprint-022/` 或 active Change 路径 | 归档移动目录后，历史证据文档未统一改 canonical archive path | `/sprint-archive` 后必须跑 residual gate，并只写新归档路径 |
| 中间态文案 | 已 archived 的 Issue/Change 仍残留 “待 archive / proposed / in_sprint” | Workflow Sync 只能刷新派生块，人写说明区需要补写闭环事实 | 收尾前跑 stale scan，把人写说明区改为“后续已归档” |
| AI usage 新鲜度 | 首次 summary 显示 snapshot stale / estimated_fallback | Sprint 文档关闭时间晚于快照生成时间 | 复盘前先刷新 snapshot，再重新读 summary |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-022.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Freshness baseline | 2026-08-11T16:20:00Z | 来源：`sprint.md:updated_at` |
| Generated at | 2026-08-12T00:20:41.865701Z | `data/ai-usage/sprints/sprint-022.json` |
| command_run_count | 125 | snapshot totals |
| model_call_count | 1,738 | snapshot totals |
| tool_call_count | 2,916 | snapshot totals |
| input_tokens | 227,647,189 | snapshot totals |
| cached_input_tokens | 217,337,472 | snapshot totals |
| output_tokens | 816,663 | snapshot totals |
| reasoning_output_tokens | 47,029 | snapshot totals |
| total_tokens | 228,886,612 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 13 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3604645 | 2916171 | 0 | 0 | 2871992 | 3964067 | 8013791 | 5534030 | 5483927 | 6400357 | 19028234 | 9248395 | 0 | 0 | 62102323 | 53709489 | 21355136 | 21447948 | 0 | 0 | 3206107 |
| sprint-022 | 0 | 3604645 | 2916171 | 0 | 0 | 2871992 | 3964067 | 8013791 | 5534030 | 5483927 | 6400357 | 19028234 | 9248395 | 0 | 0 | 62102323 | 53709489 | 21355136 | 21447948 | 0 | 0 | 3206107 |
| REQ-0103-product-recall-list-pin-priority | 0 | 0 | 393713 | 0 | 0 | 508472 | 0 | 1365639 | 0 | 934825 | 0 | 1646330 | 0 | 0 | 0 | 1473132 | 9382282 | 1034169 | 4508232 | 0 | 0 | 0 |
| REQ-0104-miniapp-recall-pinned-product-badge | 0 | 0 | 271708 | 0 | 0 | 422057 | 0 | 947029 | 0 | 961427 | 0 | 3604670 | 0 | 0 | 0 | 2625759 | 0 | 1252415 | 2706711 | 0 | 0 | 0 |
| REQ-0106-admin-banner-title-hidden | 0 | 0 | 467767 | 0 | 0 | 354607 | 0 | 886339 | 0 | 625996 | 0 | 2190758 | 0 | 0 | 0 | 2412243 | 0 | 1448861 | 1637332 | 0 | 0 | 0 |
| REQ-0107-real-user-page-load-rum | 0 | 0 | 621971 | 0 | 0 | 429325 | 0 | 1130994 | 0 | 603156 | 0 | 2195046 | 0 | 0 | 0 | 5970149 | 28861794 | 1383347 | 1692402 | 0 | 0 | 0 |
| REQ-0108-admin-banner-list-display-optimization | 0 | 0 | 511339 | 0 | 0 | 380811 | 0 | 1010880 | 0 | 617743 | 0 | 1829839 | 0 | 0 | 0 | 7434480 | 1327702 | 1839151 | 1513621 | 0 | 0 | 0 |
| REQ-0109-admin-theme-user-menu-modes | 0 | 0 | 452995 | 0 | 0 | 441221 | 0 | 803312 | 0 | 934547 | 0 | 4007456 | 0 | 0 | 0 | 3599582 | 883066 | 1448861 | 1780033 | 0 | 0 | 0 |
| REQ-0110-admin-user-contact-info-management | 0 | 0 | 196678 | 0 | 0 | 335499 | 0 | 1869598 | 0 | 806233 | 0 | 3554135 | 0 | 0 | 0 | 3479915 | 10585007 | 1900345 | 0 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 706897 | 0 | 0 | 0 | 0 | 976621 | 0 | 1695766 | 0 | 1485270 | 0 | 2474029 | 0 | 0 | 1756573 | 0 | 0 | 3683172 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 964154 | 0 | 0 | 0 | 0 | 593767 | 0 | 1261372 | 0 | 1542604 | 0 | 1217051 | 0 | 0 | 4776970 | 0 | 787135 | 908763 | 0 | 0 | 0 |
| BUG-0127-admin-log-audit-slow-load | 0 | 1491603 | 0 | 0 | 0 | 0 | 1272230 | 0 | 1160774 | 0 | 2307945 | 0 | 1561950 | 0 | 0 | 3403015 | 5593603 | 1092196 | 943761 | 0 | 0 | 0 |
| BUG-0128-admin-user-menu-email-subtitle | 0 | 441991 | 0 | 0 | 0 | 0 | 1121449 | 0 | 1416118 | 0 | 1064538 | 0 | 3995365 | 0 | 0 | 2252254 | 0 | 721812 | 2073921 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3593607 | 2898223 | 0 | 0 | 2843946 | 3952212 | 7956651 | 5515739 | 5469488 | 6391136 | 18934537 | 9212718 | 0 | 0 | 61588598 | 53470403 | 21270498 | 21358516 | 0 | 0 | 3190917 |
| sprint-022 | 0 | 3593607 | 2898223 | 0 | 0 | 2843946 | 3952212 | 7956651 | 5515739 | 5469488 | 6391136 | 18934537 | 9212718 | 0 | 0 | 61588598 | 53470403 | 21270498 | 21358516 | 0 | 0 | 3190917 |
| REQ-0103-product-recall-list-pin-priority | 0 | 0 | 390770 | 0 | 0 | 503823 | 0 | 1356664 | 0 | 933257 | 0 | 1607675 | 0 | 0 | 0 | 1436001 | 9366130 | 1030329 | 4502310 | 0 | 0 | 0 |
| REQ-0104-miniapp-recall-pinned-product-badge | 0 | 0 | 269032 | 0 | 0 | 417536 | 0 | 941854 | 0 | 958999 | 0 | 3596902 | 0 | 0 | 0 | 2588676 | 0 | 1249630 | 2703063 | 0 | 0 | 0 |
| REQ-0106-admin-banner-title-hidden | 0 | 0 | 465943 | 0 | 0 | 350835 | 0 | 880768 | 0 | 623943 | 0 | 2180823 | 0 | 0 | 0 | 2380944 | 0 | 1446227 | 1634134 | 0 | 0 | 0 |
| REQ-0107-real-user-page-load-rum | 0 | 0 | 617211 | 0 | 0 | 424620 | 0 | 1117969 | 0 | 601183 | 0 | 2185853 | 0 | 0 | 0 | 5918144 | 28678991 | 1381717 | 1689560 | 0 | 0 | 0 |
| REQ-0108-admin-banner-list-display-optimization | 0 | 0 | 509702 | 0 | 0 | 377494 | 0 | 1006210 | 0 | 616229 | 0 | 1821850 | 0 | 0 | 0 | 7421986 | 1319900 | 1836023 | 1511031 | 0 | 0 | 0 |
| REQ-0109-admin-theme-user-menu-modes | 0 | 0 | 450453 | 0 | 0 | 436980 | 0 | 797625 | 0 | 931267 | 0 | 3996948 | 0 | 0 | 0 | 3555474 | 877462 | 1446227 | 1776425 | 0 | 0 | 0 |
| REQ-0110-admin-user-contact-info-management | 0 | 0 | 195112 | 0 | 0 | 332658 | 0 | 1855561 | 0 | 804610 | 0 | 3544486 | 0 | 0 | 0 | 3440769 | 10565601 | 1898208 | 0 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 704650 | 0 | 0 | 0 | 0 | 974113 | 0 | 1690924 | 0 | 1483039 | 0 | 2468368 | 0 | 0 | 1722120 | 0 | 0 | 3675529 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 961851 | 0 | 0 | 0 | 0 | 591862 | 0 | 1256888 | 0 | 1540547 | 0 | 1205429 | 0 | 0 | 4760574 | 0 | 758882 | 880889 | 0 | 0 | 0 |
| BUG-0127-admin-log-audit-slow-load | 0 | 1487869 | 0 | 0 | 0 | 0 | 1269646 | 0 | 1156201 | 0 | 2305189 | 0 | 1552149 | 0 | 0 | 3387293 | 5582886 | 1066331 | 915690 | 0 | 0 | 0 |
| BUG-0128-admin-user-menu-email-subtitle | 0 | 439237 | 0 | 0 | 0 | 0 | 1116591 | 0 | 1411726 | 0 | 1062361 | 0 | 3986772 | 0 | 0 | 2215270 | 0 | 719768 | 2069885 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 11038 | 17948 | 0 | 0 | 28046 | 11855 | 57140 | 18291 | 14439 | 9221 | 68158 | 35677 | 0 | 0 | 292279 | 159057 | 36041 | 42283 | 0 | 0 | 15190 |
| sprint-022 | 0 | 11038 | 17948 | 0 | 0 | 28046 | 11855 | 57140 | 18291 | 14439 | 9221 | 68158 | 35677 | 0 | 0 | 292279 | 159057 | 36041 | 42283 | 0 | 0 | 15190 |
| REQ-0103-product-recall-list-pin-priority | 0 | 0 | 2943 | 0 | 0 | 4649 | 0 | 8975 | 0 | 1568 | 0 | 13116 | 0 | 0 | 0 | 11498 | 16152 | 3840 | 5922 | 0 | 0 | 0 |
| REQ-0104-miniapp-recall-pinned-product-badge | 0 | 0 | 2676 | 0 | 0 | 4521 | 0 | 5175 | 0 | 2428 | 0 | 7768 | 0 | 0 | 0 | 12157 | 0 | 2785 | 3648 | 0 | 0 | 0 |
| REQ-0106-admin-banner-title-hidden | 0 | 0 | 1824 | 0 | 0 | 3772 | 0 | 5571 | 0 | 2053 | 0 | 9935 | 0 | 0 | 0 | 7937 | 0 | 2634 | 3198 | 0 | 0 | 0 |
| REQ-0107-real-user-page-load-rum | 0 | 0 | 4760 | 0 | 0 | 4705 | 0 | 13025 | 0 | 1973 | 0 | 9193 | 0 | 0 | 0 | 27340 | 102774 | 1630 | 2842 | 0 | 0 | 0 |
| REQ-0108-admin-banner-list-display-optimization | 0 | 0 | 1637 | 0 | 0 | 3317 | 0 | 4670 | 0 | 1514 | 0 | 7989 | 0 | 0 | 0 | 12494 | 7802 | 3128 | 2590 | 0 | 0 | 0 |
| REQ-0109-admin-theme-user-menu-modes | 0 | 0 | 2542 | 0 | 0 | 4241 | 0 | 5687 | 0 | 3280 | 0 | 10508 | 0 | 0 | 0 | 19342 | 5604 | 2634 | 3608 | 0 | 0 | 0 |
| REQ-0110-admin-user-contact-info-management | 0 | 0 | 1566 | 0 | 0 | 2841 | 0 | 14037 | 0 | 1623 | 0 | 9649 | 0 | 0 | 0 | 14241 | 19406 | 2137 | 0 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 2247 | 0 | 0 | 0 | 0 | 2508 | 0 | 4842 | 0 | 2231 | 0 | 5661 | 0 | 0 | 9498 | 0 | 0 | 7643 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 2303 | 0 | 0 | 0 | 0 | 1905 | 0 | 4484 | 0 | 2057 | 0 | 11622 | 0 | 0 | 16396 | 0 | 3473 | 4729 | 0 | 0 | 0 |
| BUG-0127-admin-log-audit-slow-load | 0 | 3734 | 0 | 0 | 0 | 0 | 2584 | 0 | 4573 | 0 | 2756 | 0 | 9801 | 0 | 0 | 15722 | 10717 | 2048 | 4067 | 0 | 0 | 0 |
| BUG-0128-admin-user-menu-email-subtitle | 0 | 2754 | 0 | 0 | 0 | 0 | 4858 | 0 | 4392 | 0 | 2177 | 0 | 8593 | 0 | 0 | 12414 | 0 | 2044 | 4036 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 28 | 52 | 0 | 0 | 34 | 28 | 69 | 33 | 41 | 34 | 112 | 63 | 0 | 0 | 532 | 385 | 156 | 138 | 0 | 0 | 33 |
| sprint-022 | 0 | 28 | 52 | 0 | 0 | 34 | 28 | 69 | 33 | 41 | 34 | 112 | 63 | 0 | 0 | 532 | 385 | 156 | 138 | 0 | 0 | 33 |
| REQ-0103-product-recall-list-pin-priority | 0 | 0 | 9 | 0 | 0 | 5 | 0 | 10 | 0 | 6 | 0 | 20 | 0 | 0 | 0 | 19 | 52 | 13 | 21 | 0 | 0 | 0 |
| REQ-0104-miniapp-recall-pinned-product-badge | 0 | 0 | 7 | 0 | 0 | 5 | 0 | 8 | 0 | 7 | 0 | 18 | 0 | 0 | 0 | 32 | 0 | 8 | 16 | 0 | 0 | 0 |
| REQ-0106-admin-banner-title-hidden | 0 | 0 | 6 | 0 | 0 | 4 | 0 | 8 | 0 | 5 | 0 | 12 | 0 | 0 | 0 | 15 | 0 | 11 | 11 | 0 | 0 | 0 |
| REQ-0107-real-user-page-load-rum | 0 | 0 | 11 | 0 | 0 | 6 | 0 | 11 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 48 | 226 | 9 | 12 | 0 | 0 | 0 |
| REQ-0108-admin-banner-list-display-optimization | 0 | 0 | 6 | 0 | 0 | 4 | 0 | 9 | 0 | 5 | 0 | 11 | 0 | 0 | 0 | 34 | 18 | 11 | 11 | 0 | 0 | 0 |
| REQ-0109-admin-theme-user-menu-modes | 0 | 0 | 8 | 0 | 0 | 6 | 0 | 8 | 0 | 8 | 0 | 21 | 0 | 0 | 0 | 34 | 8 | 11 | 12 | 0 | 0 | 0 |
| REQ-0110-admin-user-contact-info-management | 0 | 0 | 5 | 0 | 0 | 4 | 0 | 15 | 0 | 5 | 0 | 17 | 0 | 0 | 0 | 35 | 69 | 10 | 0 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 6 | 0 | 0 | 0 | 0 | 7 | 0 | 11 | 0 | 9 | 0 | 11 | 0 | 0 | 26 | 0 | 0 | 19 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 6 | 0 | 0 | 0 | 0 | 3 | 0 | 6 | 0 | 7 | 0 | 16 | 0 | 0 | 28 | 0 | 11 | 14 | 0 | 0 | 0 |
| BUG-0127-admin-log-audit-slow-load | 0 | 10 | 0 | 0 | 0 | 0 | 7 | 0 | 6 | 0 | 11 | 0 | 17 | 0 | 0 | 22 | 28 | 9 | 10 | 0 | 0 | 0 |
| BUG-0128-admin-user-menu-email-subtitle | 0 | 6 | 0 | 0 | 0 | 0 | 11 | 0 | 10 | 0 | 7 | 0 | 19 | 0 | 0 | 32 | 0 | 9 | 12 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec apply / modify | high | `Opsx-Apply` 62,102,323 total tokens，`Opsx-Modify` 53,709,489 total tokens | 大 Change 分段执行；先读 summary 与 diff stat；UI 返修用聚焦文件和截图证据，不回读全量 Change |
| OpenSpec archive | high | `Opsx-Archive` 21,355,136 total tokens | 归档前用 readiness、language、directory gate 聚合；成功路径只输出摘要 |
| Sprint propose | medium | `Sprint-Propose` 21,447,948 total tokens | 多范围项追加时串行脚本写 `sprint.yaml`，避免重复读取四件套全文 |
| REQ/BUG opsx | medium | `REQ-Opsx` 19,028,234、`BUG-Opsx` 9,248,395 total tokens | 复用已读规则摘要；只读当前 Issue trace 与必要 acceptance/root-cause |
| 大 Sprint 归档查证 | medium | 18 Change、229/229 tasks；Fact Sheet 标记 OpenSpec changes 风险 high | 10+ Change 默认使用 batch summary，只有 blocker/warning 才读原文 |

已采用的节省策略：

| 策略 | 结果 |
|------|------|
| Fact Sheet summary 优先 | 未展开 18 个 archived Change 的 raw tasks/trace |
| residual/stale gate 聚合 | 通过脚本定位旧路径和旧状态文案，避免全仓搜索 |
| 分段读取 | 只在修复 stale/residual 时读取命中行附近片段 |
| 矩阵专用渲染 | 使用 `--ai-usage-markdown` 写入表格，避免手工读取原始矩阵 JSON |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| 小程序媒体性能 | BUG-0125 与 BUG-0126 都证明“有缩略图对象”不等于“页面真的用缩略图” | 媒体验收必须同时覆盖 key、object、URL、render 四联 |
| 管理端列表一致性 | Banner、日志审计、用户管理都触发列展示、换行、冻结列、分页等细节返修 | 新管理端列表需求应默认引用 `admin-list-page-consistency.md` |
| RUM 观测 | REQ-0107 多次围绕弹窗/页面、筛选、样本明细和分页调整 | 复杂观测页应在 PRD 阶段明确主列表、样本页、敏感字段、分页方式 |
| 主题入口 | 主题偏好从多模式收敛到用户菜单入口 | 偏好类能力要把历史值兼容、API 枚举、UI 入口和测试一起设计 |
| 用户联系信息 | 用户管理与个人资料页存在身份展示和联系信息边界 | 身份字段、联系字段、登录标识应建统一 display helper，避免伪邮箱回归 |

## 开发质量复盘

| 维度 | 做得好的点 | 待改进点 |
|------|------------|----------|
| API/DB/Orval | REQ-0107、REQ-0110、REQ-0108 等涉及接口的 Change 均同步 OpenAPI/Orval 与测试 | 大量生成物改动应继续用 diff stat 和 focused schema 复核 |
| 小程序 | 静态测试覆盖了商品卡片、详情页、品牌链路 URL/render 绑定 | 真机/DevTools evidence 仍容易在文档中先写 pending，收尾要强制回填 |
| Web 管理端 | 多数 UI 返修有聚焦测试和 1440px smoke 证据 | Playwright 环境缺包时要明确替代证据，不能把“未截图”写成已截图 |
| Workflow | archive readiness、stale scan、residual gate 有效阻断错误闭环 | 人写说明区仍需被脚本扫描，避免派生块正确但正文过时 |

## 可复用抽象

| 抽象 | 来源 | 建议 |
|------|------|------|
| AdminListPage 列契约 | REQ-0108、BUG-0127、REQ-0110 | 沉淀“列 nowrap / 有效期换行 / 冻结操作列 / 分页”组件契约 |
| AdminUserIdentityDisplay | BUG-0128、REQ-0110 | 用户菜单、个人资料、用户管理列表统一使用 display helper |
| MiniappMediaUrlContract | BUG-0125、BUG-0126 | 将 `url`、`preview_url`、`cover_url`、`.thumb`、fallback 规则写成共享测试 helper |
| PerformanceTableShell | REQ-0107、BUG-0127 | 性能观测页、样本页、日志审计页共享分页、筛选、复制和样本入口模式 |
| Governance Archive Gates | sprint-022 archive | stale scan、residual gate、AI usage fresh gate 作为复盘前置检查 |

## 行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 将小程序媒体四联验收沉淀为独立最佳实践，覆盖 key/object/URL/render、DevTools evidence、历史缩略图审计 | `/req-capture` | open |
| T-002 | P1 | 为管理端列表页建立更强的列显示契约，包括 nowrap、有效期例外、冻结操作列、后端分页 | `/req-capture` | open |
| T-003 | P2 | 为用户身份与联系信息展示沉淀 display helper 规范，避免伪邮箱、登录名、联系邮箱混用 | `/req-capture` | open |
| T-004 | P2 | 为 RUM/日志类观测页沉淀“主列表 + 样本页 + 后端分页 + 复制 request_id”模式 | `/req-capture` | open |
| T-005 | P1 | 将 `/sprint-exps` 前置检查标准化：先刷新 AI usage snapshot，再运行 summary/residual gate，不读取 raw evidence hints | `/opsx-propose` | open |

## Follow-up Capture 建议

未自动创建 Issue。建议后续按团队优先级选择 capture：

1. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：沉淀小程序媒体四联验收最佳实践
   背景：BUG-0125、BUG-0126 均暴露媒体性能验收不能只看对象存在。
   影响范围：docs/knowledge-base、miniapp、backend media、测试 helper。
   建议验收要点：覆盖 key/object/URL/render 四联、DevTools/真机 Network evidence、历史对象审计与回填策略。
   来源 Change/Sprint/命令：sprint-022 `/sprint-exps`

2. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：建立管理端列表页列展示与分页一致性契约
   背景：Banner、日志审计、用户管理在列展示、换行、分页和操作列上反复返修。
   影响范围：Web 管理端、设计系统、前端测试、docs/knowledge-base。
   建议验收要点：nowrap 规则、有效期例外、冻结操作列、分页样式、后端真实分页。
   来源 Change/Sprint/命令：sprint-022 `/sprint-exps`

3. 建议命令：`/opsx-propose`
   类型倾向：治理 Change
   标题：强化 sprint-exps AI usage fresh gate 与矩阵写入流程
   背景：首次复盘 summary 因 snapshot stale 阻断真实矩阵展示，需要先刷新再复核。
   影响范围：`.agents/skills/sprint-exps/SKILL.md`、`scripts/generate-sprint-fact-sheet.py`、AI usage 文档。
   建议验收要点：复盘前自动提示刷新、刷新后重新 summary、无 fresh gate pass 不输出真实矩阵。
   来源 Change/Sprint/命令：sprint-022 `/sprint-exps`
