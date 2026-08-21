---
title: sprint-023 复盘
purpose: 复盘 sprint-023 的流程、需求、开发质量、可复用抽象与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-023
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-12 22:10:00
updated_at: 2026-08-12 22:10:00
---

# sprint-023 复盘

## 概况

sprint-023 已完成归档，目录为 `iterations/archive/sprint-023/`。本 Sprint 覆盖 3 个 REQ、1 个 BUG、6 个 OpenSpec Change，65/65 个任务完成，验收状态为 passed。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 发布与复盘治理 | `optimize-release-workflow-ux`、`strengthen-sprint-exps-ai-usage-fresh-gate` | 发布/复盘命令适合小颗粒治理 Change，但 AI usage fresh gate 必须在真实矩阵输出前强制通过 |
| 小程序媒体验收 | REQ-0111 | 媒体验收从 BUG 个案上升为 key/object/URL/render 四联证据链和 helper 资产 |
| 管理端列表契约 | REQ-0112 | 列 nowrap、有效期例外、冻结操作列、真实分页和 DOM 结构应成为横切契约 |
| 性能观测一致性 | BUG-0129、REQ-0113 | 小程序 RUM、Web RUM、筛选候选值、聚合列表和样本页字段顺序要一起验收 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 3 |
| bugs | 1 |
| changes | 6 |
| tasks | 65/65 |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | pass |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-023 --json` 报告 `residual_count=0`。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| Sprint 收尾 | `/sprint-archive` 后 readiness、stale scan、residual gate 全部通过 | 先用 Fact Sheet 和 gate 聚合事实，再修正人写说明区旧状态 |
| 小 Sprint 控制 | 6 个 Change 未触发 batch 模式，65/65 tasks 聚合足以支撑复盘 | 小规模 Sprint 默认不用展开所有 archived tasks/trace |
| Issue 闭环 | 3 个 REQ 与 1 个 BUG 的 acceptance result 均为 passed | `acceptance_status`、trace 状态和 Sprint Scope 说明要同步为完成态 |
| 治理资产演进 | 发布流程 UX 与 sprint-exps AI usage fresh gate 均以 Change 形式归档 | 命令体验优化也应遵守 Sprint Inclusion Gate 和归档证据 |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| 中间态文案残留 | Sprint close 前发现 `pending`、`in_sprint`、`applied`、`待 archive` 等旧语义 | Workflow Sync 派生块已正确，但人写说明区仍保留过程记录 | close 前必须跑 stale scan，并把过程记录改为“随后已归档闭环” |
| 验收报告覆盖不足 | release-note / acceptance-report 早期只列部分范围项 | 纯治理项和后追加 REQ 容易在收尾文档中遗漏 | Sprint close 时对照 `sprint.yaml` 的 changes/requirements/bugs 补齐四件套 |
| Token 矩阵新鲜度 | 复盘必须等待 `sprint.archive` hook 后的最新 snapshot | Sprint 文档更新时间会晚于早期 usage snapshot | `/sprint-exps` 先读 summary；若 fresh gate 不过，先刷新并重新 summary |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-023.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Matrix write gate | pass | 必须 fresh gate pass、actual/present 且矩阵存在才可输出真实矩阵 |
| Freshness baseline | 2026-08-12T14:03:11Z | 来源：`sprint.md:updated_at` |
| Generated at | 2026-08-12T14:03:21.025162Z | `data/ai-usage/sprints/sprint-023.json` |
| command_run_count | 41 | snapshot totals |
| model_call_count | 533 | snapshot totals |
| tool_call_count | 981 | snapshot totals |
| input_tokens | 69,565,381 | snapshot totals |
| cached_input_tokens | 65,683,456 | snapshot totals |
| output_tokens | 243,411 | snapshot totals |
| reasoning_output_tokens | 12,538 | snapshot totals |
| total_tokens | 69,943,775 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 8 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 542546 | 644188 | 0 | 0 | 885533 | 1428886 | 2832543 | 1249228 | 2663623 | 758880 | 8130638 | 1017772 | 0 | 0 | 19088747 | 8740179 | 7594532 | 13331584 | 0 | 0 | 1034896 |
| sprint-023 | 0 | 542546 | 644188 | 0 | 0 | 885533 | 1428886 | 2832543 | 1249228 | 2663623 | 758880 | 8130638 | 1017772 | 0 | 0 | 19088747 | 8740179 | 7594532 | 13331584 | 0 | 0 | 1034896 |
| REQ-0111-miniapp-media-four-part-acceptance-practice | 0 | 0 | 178396 | 0 | 0 | 335820 | 0 | 860922 | 0 | 617954 | 0 | 2611425 | 0 | 0 | 0 | 2830537 | 0 | 1015798 | 3437984 | 0 | 0 | 0 |
| REQ-0112-admin-list-column-pagination-consistency-contract | 0 | 0 | 146184 | 0 | 0 | 183416 | 0 | 831056 | 0 | 1014154 | 0 | 3291869 | 0 | 0 | 0 | 4204238 | 0 | 561793 | 3319989 | 0 | 0 | 0 |
| REQ-0113-admin-performance-observability-filter-options | 0 | 0 | 319608 | 0 | 0 | 366297 | 0 | 1140565 | 0 | 1031515 | 0 | 2227344 | 0 | 0 | 0 | 3216255 | 4001426 | 2002411 | 2843656 | 0 | 0 | 0 |
| BUG-0129-miniapp-rum-app-version-production | 0 | 542546 | 0 | 0 | 0 | 0 | 1428886 | 0 | 1249228 | 0 | 758880 | 0 | 1017772 | 0 | 0 | 3515339 | 4738753 | 923597 | 3729955 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 0 | 178396 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 0 | 178396 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 539921 | 637980 | 0 | 0 | 871449 | 1424256 | 2814241 | 1244737 | 2654608 | 757257 | 8105282 | 983763 | 0 | 0 | 18933045 | 8680267 | 7582183 | 13307319 | 0 | 0 | 1029073 |
| sprint-023 | 0 | 539921 | 637980 | 0 | 0 | 871449 | 1424256 | 2814241 | 1244737 | 2654608 | 757257 | 8105282 | 983763 | 0 | 0 | 18933045 | 8680267 | 7582183 | 13307319 | 0 | 0 | 1029073 |
| REQ-0111-miniapp-media-four-part-acceptance-practice | 0 | 0 | 176758 | 0 | 0 | 330808 | 0 | 855022 | 0 | 615888 | 0 | 2603434 | 0 | 0 | 0 | 2788350 | 0 | 1013687 | 3430625 | 0 | 0 | 0 |
| REQ-0112-admin-list-column-pagination-consistency-contract | 0 | 0 | 144593 | 0 | 0 | 178856 | 0 | 825349 | 0 | 1010986 | 0 | 3281128 | 0 | 0 | 0 | 4170711 | 0 | 559225 | 3312931 | 0 | 0 | 0 |
| REQ-0113-admin-performance-observability-filter-options | 0 | 0 | 316629 | 0 | 0 | 361785 | 0 | 1133870 | 0 | 1027734 | 0 | 2220720 | 0 | 0 | 0 | 3173929 | 3991994 | 1999595 | 2839341 | 0 | 0 | 0 |
| BUG-0129-miniapp-rum-app-version-production | 0 | 539921 | 0 | 0 | 0 | 0 | 1424256 | 0 | 1244737 | 0 | 757257 | 0 | 983763 | 0 | 0 | 3502494 | 4688273 | 922074 | 3724422 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 0 | 176758 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 0 | 176758 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 2625 | 6208 | 0 | 0 | 14084 | 4630 | 18302 | 4491 | 9015 | 1623 | 25356 | 7290 | 0 | 0 | 80481 | 26869 | 12349 | 24265 | 0 | 0 | 5823 |
| sprint-023 | 0 | 2625 | 6208 | 0 | 0 | 14084 | 4630 | 18302 | 4491 | 9015 | 1623 | 25356 | 7290 | 0 | 0 | 80481 | 26869 | 12349 | 24265 | 0 | 0 | 5823 |
| REQ-0111-miniapp-media-four-part-acceptance-practice | 0 | 0 | 1638 | 0 | 0 | 5012 | 0 | 5900 | 0 | 2066 | 0 | 7991 | 0 | 0 | 0 | 16856 | 0 | 2111 | 7359 | 0 | 0 | 0 |
| REQ-0112-admin-list-column-pagination-consistency-contract | 0 | 0 | 1591 | 0 | 0 | 4560 | 0 | 5707 | 0 | 3168 | 0 | 10741 | 0 | 0 | 0 | 9473 | 0 | 2568 | 7058 | 0 | 0 | 0 |
| REQ-0113-admin-performance-observability-filter-options | 0 | 0 | 2979 | 0 | 0 | 4512 | 0 | 6695 | 0 | 3781 | 0 | 6624 | 0 | 0 | 0 | 16490 | 9432 | 2816 | 4315 | 0 | 0 | 0 |
| BUG-0129-miniapp-rum-app-version-production | 0 | 2625 | 0 | 0 | 0 | 0 | 4630 | 0 | 4491 | 0 | 1623 | 0 | 7290 | 0 | 0 | 12845 | 17437 | 1523 | 5533 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 0 | 1638 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 0 | 1638 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 6 | 17 | 0 | 0 | 11 | 9 | 27 | 7 | 22 | 4 | 44 | 15 | 0 | 0 | 160 | 59 | 57 | 80 | 0 | 0 | 15 |
| sprint-023 | 0 | 6 | 17 | 0 | 0 | 11 | 9 | 27 | 7 | 22 | 4 | 44 | 15 | 0 | 0 | 160 | 59 | 57 | 80 | 0 | 0 | 15 |
| REQ-0111-miniapp-media-four-part-acceptance-practice | 0 | 0 | 5 | 0 | 0 | 4 | 0 | 8 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 34 | 0 | 9 | 21 | 0 | 0 | 0 |
| REQ-0112-admin-list-column-pagination-consistency-contract | 0 | 0 | 4 | 0 | 0 | 3 | 0 | 10 | 0 | 10 | 0 | 20 | 0 | 0 | 0 | 20 | 0 | 10 | 26 | 0 | 0 | 0 |
| REQ-0113-admin-performance-observability-filter-options | 0 | 0 | 8 | 0 | 0 | 4 | 0 | 9 | 0 | 7 | 0 | 11 | 0 | 0 | 0 | 31 | 27 | 11 | 16 | 0 | 0 | 0 |
| BUG-0129-miniapp-rum-app-version-production | 0 | 6 | 0 | 0 | 0 | 0 | 9 | 0 | 7 | 0 | 4 | 0 | 15 | 0 | 0 | 30 | 32 | 8 | 17 | 0 | 0 | 0 |
| BUG-0125-miniapp-sku-detail-media-original-load | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0126-miniapp-brand-media-slow-load | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec apply | high | `Opsx-Apply` 19,088,747 total tokens，160 次模型调用 | 大 Change 分段执行；优先 diff stat、测试摘要和目标文件片段 |
| Sprint propose | high | `Sprint-Propose` 13,331,584 total tokens，80 次模型调用 | 多范围项追加时复用已读 Issue 摘要，串行写 `sprint.yaml` 后只跑 scope 校验 |
| OpenSpec archive | medium | `Opsx-Archive` 7,594,532 total tokens，57 次模型调用 | 归档前用 readiness/language/directory gate 聚合，成功路径只输出摘要 |
| OpenSpec modify | medium | `Opsx-Modify` 8,740,179 total tokens，59 次模型调用 | 验收返修只读失败证据和相关文件，不回读完整 Change |
| 归档查证 | medium | 6 Change、65/65 tasks；Fact Sheet 标记 OpenSpec changes 风险 medium | 默认使用 summary；只有 warning/blocker 时读取 evidence hints |

已采用的节省策略：

| 策略 | 结果 |
|------|------|
| Fact Sheet summary 优先 | 未展开 6 个 archived Change 的 raw tasks/trace |
| residual/stale gate 聚合 | 通过脚本确认 70 个范围文件无旧路径残留 |
| 分段读取 | 只在修复 stale 文案和索引时读取命中片段 |
| 矩阵专用渲染 | 使用 `--ai-usage-markdown` 写入表格，避免手工读取原始矩阵 JSON |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| 小程序媒体四联验收 | REQ-0111 将 BUG-0125/0126 的经验转为最佳实践和 helper | 媒体验收不能只看对象或 URL，要覆盖 key、object、URL、render 四个事实 |
| 管理端列表契约 | REQ-0112 将多页面列表体验问题收敛为横切契约 | 新列表页应默认声明 nowrap、例外字段、冻结操作列、分页 DOM 与真实分页边界 |
| 性能观测筛选 | REQ-0113 把候选值接口、筛选顺序、聚合列表和样本页上下文纳入同一 Change | 观测页需求要同时覆盖 API、Orval、筛选区、列表字段和失败态 |
| RUM 口径修复 | BUG-0129 说明小程序和 Web 的版本号、request_id、指标标签必须统一口径 | 性能事件类 BUG 要明确隐私边界、fallback 行为和 Web 回归 |
| 命令治理 | 发布与复盘命令都补了更强 gate | 治理命令改变行为时也应进 Sprint，避免脱离 OpenSpec 追踪 |

## 开发质量复盘

| 维度 | 做得好的点 | 待改进点 |
|------|------------|----------|
| API/Orval | REQ-0113 覆盖候选值接口、OpenAPI/Orval 和管理端筛选 | 生成物复核仍应坚持 focused schema，不展开完整 generated diff |
| 小程序 | BUG-0129 与 REQ-0111 同时覆盖 RUM 和媒体 evidence helper | 后续真机/体验版证据要在 acceptance 中更早回填，减少 close 前补文案 |
| Web 管理端 | 性能观测聚合、样本页、admin-list 契约一起纳入验收 | 性能观测筛选失败态与空态应作为共用测试模式沉淀 |
| Workflow | `/sprint-archive` 的 stale scan 成功发现残留中间态 | 人写说明区的状态词仍要谨慎，避免与机器状态冲突 |

## 可复用抽象

| 抽象 | 来源 | 建议 |
|------|------|------|
| MiniappMediaFourPartEvidence | REQ-0111 | 将 key/object/URL/render、Network evidence 和审计 helper 作为媒体类验收默认模板 |
| AdminListPageContract | REQ-0112 | 管理端列表页默认复用列宽、nowrap、冻结列、分页 DOM 与真实分页契约 |
| PerformanceFilterOptions API | REQ-0113 | 观测类页面候选值接口统一返回可筛选维度，并与样本页上下文保持一致 |
| RumVersionRequestIdContract | BUG-0129 | 小程序/Web RUM 统一版本号、request_id、指标标签和隐私字段边界 |
| SprintExpsUsageGate | strengthen-sprint-exps-ai-usage-fresh-gate | 复盘文档只在 fresh gate + matrix write gate 通过后写真实 token 矩阵 |

## 行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 将性能观测筛选失败态、空态和样本页上下文沉淀为观测页横切测试模式 | `/req-capture` | open |
| T-002 | P1 | 为后续管理端列表改造建立“契约引用检查”，需求进入 Sprint 前确认是否引用 admin-list 最佳实践 | `/opsx-propose` | open |
| T-003 | P2 | 为小程序媒体四联验收补一条 release/miniapp-prepare 前置检查，避免体验版才发现 URL/render 漂移 | `/req-capture` | open |
| T-004 | P2 | 将 `/sprint-archive` stale scan 命中的人写说明区状态词整理为脚本提示样例，降低手工修文成本 | `/opsx-propose` | open |
| T-005 | P2 | 对高 token 的 `opsx.apply` 和 `sprint.propose` 增加 summary-first 操作清单，避免重复读取 Issue/Change 全文 | `/opsx-propose` | open |

## Follow-up Capture 建议

未自动创建 Issue。建议后续按团队优先级选择 capture：

1. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：沉淀性能观测页筛选失败态与样本页上下文测试模式
   背景：BUG-0129 与 REQ-0113 都涉及性能观测聚合、筛选、样本页上下文和空态/失败态。
   影响范围：Web 管理端性能观测页、测试 helper、docs/knowledge-base。
   建议验收要点：筛选候选值失败时不误展示为空数据；样本页上下文字段与聚合分组键一致；Web/小程序 RUM 回归通过。
   来源 Change/Sprint/命令：sprint-023 / `/sprint-exps sprint-023`

2. 建议命令：`/opsx-propose`
   类型倾向：治理 Change
   标题：强化 sprint close stale scan 的人写说明区提示
   背景：sprint-023 close 前 stale scan 命中旧中间态文案，修复后归档通过。
   影响范围：`scripts/check-sprint-close-stale-scan.py`、`scripts/validate-sprint-archive-readiness.py`、相关技能说明。
   建议验收要点：报告展示命中词、生命周期事实、建议替换语义；不要求手工编辑 workflow-sync marker blocks。
   来源 Change/Sprint/命令：sprint-023 / `/sprint-archive sprint-023` / `/sprint-exps sprint-023`

