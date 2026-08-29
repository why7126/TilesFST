---
title: sprint-026 复盘
purpose: 复盘 sprint-026 的流程、需求、开发质量、可复用抽象与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-026
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-28 16:29:38
updated_at: 2026-08-28 16:29:38
---

# sprint-026 复盘

## 概况

sprint-026 已完成归档，目录为 `iterations/archive/sprint-026/`。本 Sprint 覆盖 7 个 REQ、7 个 BUG、16 个 OpenSpec Change，270/270 个任务完成，验收、归档、路径残留和产品数据采集与链路观测门禁均已闭环。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 产品数据采集与链路观测 | REQ-0124、REQ-0126、REQ-0127、REQ-0123 | 行为事件、请求日志、Task Trace 和流程节点需要同时有数据模型、端侧透传、管理端查询和流程门禁，不能只靠单点实现 |
| 小程序搜索与埋点性能 | REQ-0128、BUG-0143、BUG-0144 | 搜索体验统一后，性能瓶颈会从查询转向卡片构建、事件上报频率和端侧状态切换，需要 Server-Timing、事件字典和 Network 证据一起验收 |
| 管理端媒体与可读性 | BUG-0140、BUG-0139、BUG-0142、BUG-0145 | 媒体上传、头像对象一致性和日志详情长字段都需要用端到端证据验证，而不是只看接口返回成功 |
| 治理脚本与命令契约 | BUG-0141、`refine-skill-final-output-contract`、`fix-workflow-sync-sprint-propose-iteration` | Workflow Sync、AI usage、最终输出契约和 Sprint 归档门禁需要持续脚本化，避免状态漂移在收尾阶段集中爆发 |
| 小程序局部体验 | REQ-0125、REQ-0129 | 深层页返回首页、底部操作栏和收藏状态需要统一安全区与不同 viewport 验收，避免一个页面的体验修复破坏另一个页面 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 7 |
| bugs | 7 |
| changes | 16 |
| tasks | 270/270 |
| change batches | 4 |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | pass |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-026 --json` 报告 `residual_count=0`。产品数据采集与链路观测门禁：`validate-product-data-observability-gates.py --sprint sprint-026` 通过，Sprint 范围内声明与验收证据可追溯。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| 大 Sprint 批次化 | Fact Sheet 将 16 个 Change 拆为 4 个 batch，全部 tasks 完成且每批 blockers/warnings 均为 0 | 10 个以上 Change 的 Sprint 复盘和归档默认从 batch summary 入手，只在 warning 或 missing 时回读原始任务 |
| 观测门禁落地 | REQ-0124、REQ-0126、REQ-0127 把行为链路模型、通用规范和硬门禁连成闭环 | 涉及 API、DB、请求封装、埋点或 Task Trace 的范围必须同时声明 affected layers、N/A 原因和 validation 摘要 |
| 归档收尾脚本化 | `/sprint-archive` 阶段 stale scan、residual gate、Workflow Sync 和 AI usage hook 最终均通过 | 状态漂移与旧路径残留不要靠人工猜，先跑聚合门禁，再按报告精确修复 |
| 性能返修可定位 | REQ-0128 用 Server-Timing 将搜索性能瓶颈拆到品牌识别、SKU list/count、证书查询和卡片构建 | 接口慢不应只靠总耗时讨论，服务端分段与端侧 Network 证据要一起沉淀 |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| 收尾文案漂移 | Sprint close 前 stale scan 曾发现验收报告、Sprint 文档和 Issue 子文档残留 `待 req-opsx`、`待 archive`、`pending` 等旧语义 | 多轮 apply/archive 后，部分人读文档不是 Workflow Sync 派生块，旧阶段说明没有自动刷新 | 归档前固定运行 stale scan；对非派生人写段落使用“后续已归档”或“历史过程记录”表达 |
| 旧路径残留 | 归档后 residual gate 曾发现已归档 Change 文档仍引用 `openspec/changes/<change-id>/` 或 `iterations/change/sprint-026/` | Change 内证据路径在 active 阶段写入，归档移动后没有统一替换 | `/opsx-archive` 与 `/sprint-archive` 后保留 residual gate，复盘只写 canonical archive path |
| AI usage 快照时效 | Sprint close 中途文档更新后，旧 snapshot 一度变为 stale / estimated_fallback | snapshot generated_at 早于最新 acceptance-report updated_at | post-command hook 后必须重新跑 Fact Sheet summary，以刷新后的 fresh gate 判断是否可写真实矩阵 |
| 小程序搜索返修次数多 | REQ-0128 从卡片内容、分页、分类/品牌/证书/收藏边界到性能分段多次返修 | 初始范围同时覆盖多页面、多端管理列表、埋点和性能，验收面很宽 | 后续搜索类需求先拆“入口/范围/性能/埋点”四类验收，每类单独列最小证据 |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-026.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Matrix write gate | pass | fresh gate pass、actual/present 且矩阵存在 |
| Freshness baseline | 2026-08-28T08:21:48Z | 来源：`acceptance-report.md:updated_at` |
| Generated at | 2026-08-28T08:21:55.773905Z | `data/ai-usage/sprints/sprint-026.json` |
| command_run_count | 129 | snapshot totals |
| model_call_count | 1,163 | snapshot totals |
| tool_call_count | 2,096 | snapshot totals |
| input_tokens | 164,700,317 | snapshot totals |
| cached_input_tokens | 159,290,240 | snapshot totals |
| output_tokens | 564,947 | snapshot totals |
| reasoning_output_tokens | 60,503 | snapshot totals |
| total_tokens | 165,622,295 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 16 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。`-` 表示该 workflow 阶段在当前 snapshot 中未采集或未归因，不等价于真实 `0`；只有已观测 workflow 列中的数字 `0` 才表示真实零消耗。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 2458913 | 8176448 | 0 | - | 0 | 0 | 0 | 2111750 | 0 | 2409682 | 0 | 0 | - | - | 107899659 | 24466240 | 14282547 | 3817056 | - | - | 0 |
| sprint-026 | - | 2458913 | 8176448 | 0 | - | 0 | 0 | 0 | 2111750 | 0 | 2409682 | 0 | 0 | - | - | 107899659 | 24466240 | 14282547 | 3817056 | - | - | 0 |
| REQ-0123-upload-stage-trace-spans | - | 0 | 522280 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 13207484 | 0 | 0 | 0 | - | - | 0 |
| REQ-0124-log-audit-behavior-trace-model | - | 0 | 1365275 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | 0 | 0 | - | - | 0 |
| REQ-0125-miniapp-certificate-detail-home-floating-button | - | 0 | 737030 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3091508 | 741833 | 0 | 0 | - | - | 0 |
| REQ-0126-product-data-collection-observability-standard | - | 0 | 3700940 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14535685 | 1345220 | 0 | 0 | - | - | 0 |
| REQ-0127-product-data-collection-observability-hard-gate | - | 0 | 379385 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 6715294 | 0 | 0 | 0 | - | - | 0 |
| REQ-0128-search-experience-unification | - | 0 | 815570 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 8896070 | 17656004 | 1693130 | 3817056 | - | - | 0 |
| REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | - | 0 | 655968 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3619291 | 0 | 0 | 0 | - | - | 0 |
| BUG-0141-ai-usage-token-count-jsonl | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14869124 | 4723183 | 0 | 0 | - | - | 0 |
| BUG-0140-admin-current-user-avatar-missing-object | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 2409682 | 0 | 0 | - | - | 4344716 | 0 | 1129697 | 0 | - | - | 0 |
| BUG-0139-admin-avatar-upload-nginx-redirect-cors | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 4558908 | 0 | 1553726 | 0 | - | - | 0 |
| BUG-0142-admin-avatar-upload-storage-put-slow | - | 420116 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 5186571 | 0 | 0 | 0 | - | - | 0 |
| BUG-0143-miniapp-telemetry-request-amplification | - | 805138 | 0 | 0 | - | 0 | 0 | 0 | 2111750 | 0 | 0 | 0 | 0 | - | - | 10653444 | 0 | 7361592 | 0 | - | - | 0 |
| BUG-0144-miniapp-usage-events-overreporting | - | 554109 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 8322935 | 0 | 0 | 0 | - | - | 0 |
| BUG-0145-admin-log-detail-field-overlap | - | 679550 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7787193 | 0 | 0 | 0 | - | - | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 2445571 | 8109161 | 0 | - | 0 | 0 | 0 | 2105697 | 0 | 2405177 | 0 | 0 | - | - | 107373403 | 24310953 | 14148245 | 3802110 | - | - | 0 |
| sprint-026 | - | 2445571 | 8109161 | 0 | - | 0 | 0 | 0 | 2105697 | 0 | 2405177 | 0 | 0 | - | - | 107373403 | 24310953 | 14148245 | 3802110 | - | - | 0 |
| REQ-0123-upload-stage-trace-spans | - | 0 | 518550 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 13137327 | 0 | 0 | 0 | - | - | 0 |
| REQ-0124-log-audit-behavior-trace-model | - | 0 | 1361394 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | 0 | 0 | - | - | 0 |
| REQ-0125-miniapp-certificate-detail-home-floating-button | - | 0 | 733411 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3056055 | 699166 | 0 | 0 | - | - | 0 |
| REQ-0126-product-data-collection-observability-standard | - | 0 | 3655671 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14457765 | 1333300 | 0 | 0 | - | - | 0 |
| REQ-0127-product-data-collection-observability-hard-gate | - | 0 | 375448 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 6686475 | 0 | 0 | 0 | - | - | 0 |
| REQ-0128-search-experience-unification | - | 0 | 812493 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 8828688 | 17566878 | 1691077 | 3802110 | - | - | 0 |
| REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | - | 0 | 652194 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3583948 | 0 | 0 | 0 | - | - | 0 |
| BUG-0141-ai-usage-token-count-jsonl | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14830859 | 4711609 | 0 | 0 | - | - | 0 |
| BUG-0140-admin-current-user-avatar-missing-object | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 2405177 | 0 | 0 | - | - | 4329037 | 0 | 1124967 | 0 | - | - | 0 |
| BUG-0139-admin-avatar-upload-nginx-redirect-cors | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 4544650 | 0 | 1515107 | 0 | - | - | 0 |
| BUG-0142-admin-avatar-upload-storage-put-slow | - | 416712 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 5172462 | 0 | 0 | 0 | - | - | 0 |
| BUG-0143-miniapp-telemetry-request-amplification | - | 801995 | 0 | 0 | - | 0 | 0 | 0 | 2105697 | 0 | 0 | 0 | 0 | - | - | 10623282 | 0 | 7311812 | 0 | - | - | 0 |
| BUG-0144-miniapp-usage-events-overreporting | - | 550492 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 8271669 | 0 | 0 | 0 | - | - | 0 |
| BUG-0145-admin-log-detail-field-overlap | - | 676372 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7736219 | 0 | 0 | 0 | - | - | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 13342 | 40654 | 0 | - | 0 | 0 | 0 | 6053 | 0 | 4505 | 0 | 0 | - | - | 363524 | 83011 | 38912 | 14946 | - | - | 0 |
| sprint-026 | - | 13342 | 40654 | 0 | - | 0 | 0 | 0 | 6053 | 0 | 4505 | 0 | 0 | - | - | 363524 | 83011 | 38912 | 14946 | - | - | 0 |
| REQ-0123-upload-stage-trace-spans | - | 0 | 3730 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 44164 | 0 | 0 | 0 | - | - | 0 |
| REQ-0124-log-audit-behavior-trace-model | - | 0 | 3881 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | 0 | 0 | - | - | 0 |
| REQ-0125-miniapp-certificate-detail-home-floating-button | - | 0 | 3619 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 10824 | 6441 | 0 | 0 | - | - | 0 |
| REQ-0126-product-data-collection-observability-standard | - | 0 | 18636 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 49373 | 11920 | 0 | 0 | - | - | 0 |
| REQ-0127-product-data-collection-observability-hard-gate | - | 0 | 3937 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 28819 | 0 | 0 | 0 | - | - | 0 |
| REQ-0128-search-experience-unification | - | 0 | 3077 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 39141 | 53076 | 2053 | 14946 | - | - | 0 |
| REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | - | 0 | 3774 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 9350 | 0 | 0 | 0 | - | - | 0 |
| BUG-0141-ai-usage-token-count-jsonl | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 38265 | 11574 | 0 | 0 | - | - | 0 |
| BUG-0140-admin-current-user-avatar-missing-object | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 4505 | 0 | 0 | - | - | 15679 | 0 | 4730 | 0 | - | - | 0 |
| BUG-0139-admin-avatar-upload-nginx-redirect-cors | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14258 | 0 | 6701 | 0 | - | - | 0 |
| BUG-0142-admin-avatar-upload-storage-put-slow | - | 3404 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 14109 | 0 | 0 | 0 | - | - | 0 |
| BUG-0143-miniapp-telemetry-request-amplification | - | 3143 | 0 | 0 | - | 0 | 0 | 0 | 6053 | 0 | 0 | 0 | 0 | - | - | 30162 | 0 | 17207 | 0 | - | - | 0 |
| BUG-0144-miniapp-usage-events-overreporting | - | 3617 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 25273 | 0 | 0 | 0 | - | - | 0 |
| BUG-0145-admin-log-detail-field-overlap | - | 3178 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 22202 | 0 | 0 | 0 | - | - | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 32 | 68 | 0 | - | 0 | 0 | 0 | 13 | 0 | 14 | 0 | 0 | - | - | 718 | 171 | 124 | 23 | - | - | 0 |
| sprint-026 | - | 32 | 68 | 0 | - | 0 | 0 | 0 | 13 | 0 | 14 | 0 | 0 | - | - | 718 | 171 | 124 | 23 | - | - | 0 |
| REQ-0123-upload-stage-trace-spans | - | 0 | 9 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 82 | 0 | 0 | 0 | - | - | 0 |
| REQ-0124-log-audit-behavior-trace-model | - | 0 | 7 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 0 | 0 | 0 | - | - | 0 |
| REQ-0125-miniapp-certificate-detail-home-floating-button | - | 0 | 8 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 29 | 11 | 0 | 0 | - | - | 0 |
| REQ-0126-product-data-collection-observability-standard | - | 0 | 25 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 100 | 17 | 0 | 0 | - | - | 0 |
| REQ-0127-product-data-collection-observability-hard-gate | - | 0 | 7 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 38 | 0 | 0 | 0 | - | - | 0 |
| REQ-0128-search-experience-unification | - | 0 | 5 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 60 | 115 | 11 | 23 | - | - | 0 |
| REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | - | 0 | 7 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 22 | 0 | 0 | 0 | - | - | 0 |
| BUG-0141-ai-usage-token-count-jsonl | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 94 | 28 | 0 | 0 | - | - | 0 |
| BUG-0140-admin-current-user-avatar-missing-object | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 14 | 0 | 0 | - | - | 24 | 0 | 17 | 0 | - | - | 0 |
| BUG-0139-admin-avatar-upload-nginx-redirect-cors | - | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 32 | 0 | 20 | 0 | - | - | 0 |
| BUG-0142-admin-avatar-upload-storage-put-slow | - | 8 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 30 | 0 | 0 | 0 | - | - | 0 |
| BUG-0143-miniapp-telemetry-request-amplification | - | 7 | 0 | 0 | - | 0 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | - | - | 61 | 0 | 48 | 0 | - | - | 0 |
| BUG-0144-miniapp-usage-events-overreporting | - | 10 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 54 | 0 | 0 | 0 | - | - | 0 |
| BUG-0145-admin-log-detail-field-overlap | - | 7 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 47 | 0 | 0 | 0 | - | - | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec Apply | high | `Opsx-Apply` total_tokens 107,899,659，占 Sprint 总量最大；REQ-0126、REQ-0123、BUG-0141、BUG-0143 等单项 apply 消耗高 | 大范围实现先用 Fact Sheet、`rg --files`、focused diff 和分批测试，避免每轮重读规则、四件套和归档历史 |
| Opsx-Modify | high | `Opsx-Modify` total_tokens 24,466,240，REQ-0128 占 17,656,004 | 对复杂 UI/性能返修先输出最小失败证据、服务端分段耗时和单点 diff，减少多轮宽泛探索 |
| Opsx-Archive | high | `Opsx-Archive` total_tokens 14,282,547，BUG-0143 archive 占 7,361,592 | 归档前先跑 language、directory、observability、archive evidence，失败只回读报告点名文件 |
| REQ Capture | medium | `REQ-Capture` total_tokens 8,176,448，REQ-0126 占 3,700,940 | 捕获阶段保持轻量，不把规范正文或长验收模板提前写入 capture |
| Sprint 四件套 | high | Fact Sheet 标记 `sprint.md` 超过 200 行 | 复盘、归档、发布默认读取 summary 和聚合计数，必要时再分段读四件套 |
| OpenSpec changes | high | 16 个 Change、270/270 tasks | 对 10+ Change Sprint 使用 batch summary；只在 blockers/warnings 时读具体 tasks/trace |
| Archive lookup | medium | 归档路径由 `sprint.yaml` changes[] 解析 | 禁止 broad-scan `openspec/archive/**`；使用 residual gate 和 fact sheet canonical path |

### Token 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为复杂小程序搜索/性能需求建立“入口、范围、性能、埋点”四段验收模板，减少返修时反复重读整条 Change | `/req-capture` | open |
| T-002 | P1 | 将 Sprint close stale scan 的常见旧语义修复经验沉淀为治理脚本建议，减少人工改验收报告和 trace 的次数 | `/opsx-propose` | open |
| T-003 | P2 | 对搜索性能类 Change 默认要求 `Server-Timing` 或等价分段耗时证据，避免只凭总 TTFB 判断瓶颈 | `/req-capture` | open |
| T-004 | P2 | 对媒体上传类 BUG 沿用 key/object/URL/render/耗时五联验收，并把 Docker Web 入口证据作为高风险上传缺陷的推荐项 | `/req-capture` | open |
| T-005 | P2 | 复盘命令继续优先使用 Fact Sheet summary、batch summary、diff stat 和成功日志摘要，避免复制完整 trace、tasks、OpenAPI/Orval 生成物 | 下一 Sprint 执行约束 | open |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| 观测模型 | REQ-0124 将 `usage_events -> request_logs -> task_traces -> task_trace_spans` 四层模型落到 DB、API、Web 透传和日志审计 | 链路观测需求必须同时定义界面触发和直接 API 两类入口，否则直接 API 会被误要求伪造行为事件 |
| 通用规范 | REQ-0126、REQ-0127 将项目内实践上升为通用规范和硬门禁 | 规范类需求要给出 N/A 规则、触发层级和校验脚本，避免后续 Change 只口头声明不适用 |
| 搜索体验 | REQ-0128 横跨小程序首页、搜索页、品牌/证书/收藏列表、管理端列表和行为事件 | 体验统一不等于所有页面跳同一个搜索入口；列表内搜索、全局搜索和详情推荐要先划清边界 |
| 小程序局部 UI | REQ-0125、REQ-0129 都涉及深层页返回首页和安全区避让 | 小程序深层页 UI 变更应固定覆盖 320/375/430pt，并明确与底部 actionbar 的 offset 关系 |
| 缺陷驱动需求 | BUG-0143、BUG-0144 暴露埋点治理和请求性能是同一类问题的两个面 | 埋点修复不能只减少请求数量，还要保证事件字典、必填字段和业务 API 性能观测不退化 |

## 开发质量复盘

| 维度 | 做得好的点 | 待改进点 |
|------|------------|----------|
| 后端与数据库 | 日志审计链路模型同步了 SQLite/MySQL schema、API 文档、Orval 和聚焦测试 | 性能类接口后续应更早加入分段耗时，减少靠截图反复定位 |
| 小程序 | 搜索入口、列表搜索、收藏页、证书页、商品详情和 actionbar 都补了静态/接口回归 | 初始设计要更早定义“本页过滤”与“全局搜索”的差异，降低返修轮次 |
| 管理端 | 日志详情长字段布局用字段说明 tooltip 与响应式列宽一起验收 | 长字段、ID、URL、object key 等排障信息应进入通用详情行组件规范 |
| 媒体上传 | 头像 key/object/URL/render 与 WebP 缩略图耗时都进入验收 | 媒体四联可以扩展为带耗时维度的五联，适配上传性能问题 |
| 治理脚本 | Workflow Sync、最终输出契约和 observability hard gate 都落到脚本/规则/技能 | 归档前非派生人写段落仍需要 stale scan 兜底，后续可考虑自动修复建议模式 |

## 可复用抽象

| 抽象 | 来源 | 建议 |
|------|------|------|
| ProductObservabilityGate | REQ-0124 / REQ-0126 / REQ-0127 | 对 API、DB、请求封装、行为事件、Task Trace 变更统一要求适用层级、N/A 原因和验证摘要 |
| SearchExperienceBoundaryMatrix | REQ-0128 | 用页面入口、搜索范围、结果承接、埋点事件和 API 查询参数定义搜索能力边界 |
| SearchPerformanceTimingEvidence | REQ-0128 | 将 `Server-Timing`、Network TTFB、查询分段和卡片构建耗时作为性能返修证据模板 |
| MediaUploadEvidenceFiveTuple | BUG-0140 / BUG-0139 / BUG-0142 / REQ-0123 | 在 key、object、URL、render 基础上补耗时/trace span，适配上传性能与可观测性缺陷 |
| LogDetailFieldLayoutPattern | BUG-0145 | 为长字段名和值提供可复用详情行布局、tooltip 可访问性和窄宽度换行策略 |
| SprintArchiveStaleResidualGate | sprint-026 archive | 将 stale scan、residual gate、Workflow Sync 和 AI usage fresh gate 作为 Sprint close 固定顺序 |

## 行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| A-001 | P1 | 为搜索体验类需求沉淀边界矩阵模板，覆盖全局搜索、本页过滤、分页策略、性能证据和埋点字段 | `/req-capture` | open |
| A-002 | P1 | 为 Sprint 归档 stale scan 常见旧状态文案增加自动修复建议或 reconcile 扩展 | `/opsx-propose` | open |
| A-003 | P2 | 将媒体上传四联验收扩展为五联实践，增加阶段耗时或 trace span 维度 | `/req-capture` | open |
| A-004 | P2 | 为日志审计详情长字段展示沉淀管理端详情行布局最佳实践 | `/req-capture` | open |
| A-005 | P2 | 下一轮包含 10+ Change 的 Sprint 继续使用 Fact Sheet batch summary 作为复盘与归档输入，不默认读取全部 Change 原文 | 下一 Sprint 执行约束 | open |

## Follow-up Capture 建议

以下为可独立 capture 的建议，未自动创建 Issue：

- 建议命令：`/req-capture`
  类型倾向：需求
  标题：搜索体验边界矩阵模板
  背景：sprint-026 的 REQ-0128 多次返修说明全局搜索、本页过滤、分页追加、性能分段和埋点字段需要在需求阶段拆清。
  影响范围：小程序搜索页、列表页、管理端列表、API 查询参数、usage events。
  建议验收要点：模板能覆盖入口类型、搜索范围、结果承接、分页策略、性能证据、事件字段、N/A 声明。
  来源：sprint-026 / `/sprint-exps sprint-026`

- 建议命令：`/opsx-propose`
  类型倾向：治理改进
  标题：Sprint 归档 stale scan 自动修复建议
  背景：sprint-026 close 前 stale scan 曾发现已归档对象的人读文档残留中间态文案，需要按报告人工修正。
  影响范围：`scripts/check-sprint-close-stale-scan.py`、Workflow Sync reconcile、Sprint archive 输出。
  建议验收要点：扫描报告能给出安全替换建议；不会改 workflow-sync marker 派生块；修复后 readiness、stale scan、residual gate 通过。
  来源：sprint-026 / `/sprint-exps sprint-026`

- 建议命令：`/req-capture`
  类型倾向：需求
  标题：媒体上传五联验收实践
  背景：BUG-0140、BUG-0139、BUG-0142 与 REQ-0123 说明媒体上传缺陷需要同时验证 key、object、URL、render 和阶段耗时。
  影响范围：管理端头像上传、通用图片上传、对象存储、Task Trace spans、媒体类 BUG 验收模板。
  建议验收要点：模板覆盖五联证据、Docker Web 入口证据、失败态、脱敏对象 key 和 trace span 关联。
  来源：sprint-026 / `/sprint-exps sprint-026`

## 复盘结论

sprint-026 的主线是把“产品行为数据与链路观测”从单项功能推进为项目级治理能力，同时处理搜索、媒体上传和日志审计三个高频质量面。最值得保留的经验是：大 Sprint 必须依赖 Fact Sheet、batch summary 和门禁脚本收束上下文；涉及观测、搜索和媒体的需求必须用端到端证据闭环，而不是只看字段存在或接口 200。
