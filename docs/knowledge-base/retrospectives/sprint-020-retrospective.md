---
sprint_id: sprint-020
title: Sprint 020 迭代经验复盘
status: draft
created_at: 2026-08-06 08:30:00
updated_at: 2026-08-06 08:40:24
owner: product
related_iteration: iterations/archive/sprint-020/
source: /sprint-exps sprint-020
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 020 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-08-19 09:00:00 ~ 2026-09-02 18:00:00 |
| REQ / BUG / Change | 3 / 1 / 4 |
| Change 批次 | 不适用；少于 10 个 Change |
| tasks 完成度 | 44/44 |
| 估算 | 14 SP / 14 人天 |
| 容量 | 30 人天；占用 46.67%；fix buffer 53.33% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；4/4 Change archived |
| AI usage | Snapshot 本体为 actual / present；已补充真实 token 矩阵；标准 Fact Sheet summary 仍受 BUG-0118 影响显示 stale / estimated_fallback |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-020 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-020 --json`、`iterations/archive/sprint-020/sprint.yaml`、`iterations/archive/sprint-020/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 管理端媒体列表性能体验 | SKU/Banner 列表优先使用缩略图，保留详情/编辑/预览原图口径 |
| 全局缩略图治理 | 系统设置新增缩略图目标体积上限，默认不限制，仅影响增量生成 |
| 小程序隐私接口收敛 | 移除电话与剪贴板能力残留，支持提审时“未采集用户隐私”口径 |
| Mintlify 文档站体验 | 文档站信息架构、版本入口、任务入口与公开安全校验完成收口 |

### Change 摘要

| Change | 关联 | tasks | 归档证据 |
|--------|------|------:|----------|
| `optimize-admin-media-list-thumbnails` | REQ-0098 | 5/5 | trace.md present |
| `fix-miniapp-privacy-interface-drift` | BUG-0117 | 5/5 | trace.md present |
| `improve-mintlify-docs-site` | REQ-0100 | 10/10 | trace.md present |
| `update-global-thumbnail-size-limit` | REQ-0099 | 24/24 | trace.md present |

本 Sprint 没有 Fact Sheet warnings、没有 archived path residual、没有 needs_detail 触发项；复盘按 summary-first 完成，没有展开完整 `evidence_hints` 或逐个 raw tasks/trace。

## 2. 流程复盘

### 做得好的

1. **范围小但链路完整**：3 个 P1 REQ、1 个高优先级 BUG、4 个 Change 全部归档，44/44 tasks 完成，Sprint close readiness 与 stale scan 最终为 PASS。
2. **媒体治理连续推进**：sprint-019 的媒体 URL/render、维护作业、对象存储证据经验，被承接到缩略图展示和缩略图体积上限策略中。
3. **小程序隐私能力用 BUG 流程收敛**：电话与剪贴板能力残留没有作为零散补丁处理，而是通过 BUG → Change → Sprint → archive 闭环。
4. **文档站能力纳入同一 Sprint 收尾**：Mintlify 信息架构优化没有只停留在站点文件调整，还通过 release governance 与校验脚本进入归档证据。
5. **归档路径残留为 0**：Sprint close 前后均使用 residual gate，复盘文档只引用 `openspec/archive/...` 与 `iterations/archive/...` 路径。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Sprint close 前仍有中间态文案残留 | readiness 初次命中 acceptance-report 与 Issue trace 中的 proposed/applied/待 archive 语义 | 归档关闭前需要额外修正文档事实，增加收尾成本 |
| stale scan 对业务词仍可能误判 | `SKU pending 图片正式化` 被识别为中间态残留，需改写为“临时图片正式化” | 业务术语与流程状态词需要更清晰的文档写法或扫描例外 |
| AI usage fresh gate 标准 summary 仍误报 blocker | Fact Sheet summary 显示 `snapshot_status: stale`、`ai_usage_mode: estimated_fallback`；独立 snapshot check 显示 `present` / `actual` / fresh gate pass | 已记录 BUG-0118；本复盘按已验证 actual snapshot 补充矩阵，并保留 baseline 缺陷说明 |
| 媒体缩略图策略跨端影响多 | REQ-0098 与 REQ-0099 同时触达 backend、admin web、API、Orval、object storage | 后续类似需求需要更早拆出字段、生成策略、历史对象三类验收 |
| Sprint 目标列表缺少 REQ-0100 | `sprint.md` 目标编号列表侧重媒体与隐私，Scope 已包含 REQ-0100 | 人读目标与机器 Scope 不完全一致，后续提案应同步目标列表 |

### 优化建议

1. **Sprint close 前先跑 stale scan dry pass**：在 `/sprint-archive` 正式关闭前，将 `check-sprint-close-stale-scan.py` 作为固定预检，先处理 acceptance-report 与 Issue 子文档。
2. **业务状态词改写约定**：需求正文中避免把“pending / applied / proposed”等流程词用于业务对象；确需表达时用“临时”“暂存”“待正式化对象”等中文业务词。
3. **媒体类需求拆三段验收**：列表展示字段、缩略图生成策略、历史对象维护入口分别给证据，避免同一 Change 承载过多验证语义。
4. **AI usage 快照刷新前置**：`/sprint-exps` 前先确认 Fact Sheet fresh gate，通过后再输出矩阵；未通过时只记录 blocker，不做成本量化。
5. **目标列表由 Workflow Sync 或脚本校验覆盖**：Scope 已包含但目标编号列表遗漏的情况，应由 validate-sprint-scope 或复盘检查提示。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-020.json`；独立 snapshot check 为 `present` / `actual` / fresh gate pass |
| AI usage mode | actual | `python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-020 ... --json` |
| Snapshot status | present | 同上 |
| Fresh gate | pass | 同上；coverage、totals、usage_matrices 均可用 |
| Fact Sheet summary 已知误报 | BUG-0118 | 标准 summary 仍把未来 `sprint.yaml:start_date` 选为 freshness baseline，显示 stale / estimated_fallback |
| Freshness baseline | 2026-08-19T01:00:00Z | 标准 summary 当前错误来源：`sprint.yaml:start_date` |
| Generated at | 2026-08-06T00:34:43.070618Z | `data/ai-usage/sprints/sprint-020.json` |
| Command runs | 43 | snapshot totals |
| Model calls | 648 | snapshot totals |
| Tool calls | 1,128 | snapshot totals |
| Input tokens | 87,436,749 | snapshot totals |
| Cached input tokens | 83,776,000 | snapshot totals |
| Output tokens | 297,169 | snapshot totals |
| Reasoning output tokens | 21,412 | snapshot totals |
| Total tokens | 87,828,958 | snapshot totals |
| Retry count | 0 | snapshot totals |
| 矩阵规模 | 6 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/sprint-020.json`。由于 BUG-0118，标准 `--ai-usage-markdown` 的 Fact Sheet header 仍会显示 blocker；本节仅在独立 snapshot check 确认 actual/present 后补入矩阵。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 765158 | 1989720 | 0 | 0 | 1455322 | 478721 | 3564868 | 771582 | 2704142 | 1924244 | 7415203 | 3493610 | 0 | 0 | 28786098 | 11777772 | 9304061 | 8794121 | 0 | 0 | 1524322 |
| sprint-020 | 0 | 765158 | 1989720 | 0 | 0 | 1455322 | 478721 | 3564868 | 771582 | 2704142 | 1924244 | 7415203 | 3493610 | 0 | 0 | 28786098 | 11777772 | 9304061 | 8794121 | 0 | 0 | 1524322 |
| REQ-0098-admin-media-list-thumbnails | 0 | 0 | 553155 | 0 | 0 | 366544 | 0 | 1170080 | 0 | 1075702 | 0 | 2104536 | 0 | 0 | 0 | 6443238 | 0 | 2388979 | 3603081 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 653932 | 0 | 0 | 366763 | 0 | 836100 | 0 | 692000 | 0 | 2768190 | 0 | 0 | 0 | 1744744 | 10927082 | 3336188 | 1625227 | 0 | 0 | 0 |
| REQ-0099-global-thumbnail-size-limit | 0 | 0 | 782633 | 0 | 0 | 722015 | 0 | 1558688 | 0 | 936440 | 0 | 2542477 | 0 | 0 | 0 | 12408934 | 850690 | 1849256 | 763817 | 0 | 0 | 0 |
| BUG-0117-miniapp-privacy-clipboard-phone-drift | 0 | 765158 | 0 | 0 | 0 | 0 | 478721 | 0 | 771582 | 0 | 1924244 | 0 | 3493610 | 0 | 0 | 8189182 | 0 | 1729638 | 2801996 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 762102 | 1981663 | 0 | 0 | 1441190 | 476625 | 3542116 | 768305 | 2697091 | 1920696 | 7387032 | 3485195 | 0 | 0 | 28617814 | 11741999 | 9291459 | 8749631 | 0 | 0 | 1516320 |
| sprint-020 | 0 | 762102 | 1981663 | 0 | 0 | 1441190 | 476625 | 3542116 | 768305 | 2697091 | 1920696 | 7387032 | 3485195 | 0 | 0 | 28617814 | 11741999 | 9291459 | 8749631 | 0 | 0 | 1516320 |
| REQ-0098-admin-media-list-thumbnails | 0 | 0 | 550231 | 0 | 0 | 362308 | 0 | 1163165 | 0 | 1072982 | 0 | 2096237 | 0 | 0 | 0 | 6397196 | 0 | 2386379 | 3596817 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 651373 | 0 | 0 | 361964 | 0 | 828566 | 0 | 689814 | 0 | 2758679 | 0 | 0 | 0 | 1703260 | 10895048 | 3333482 | 1622784 | 0 | 0 | 0 |
| REQ-0099-global-thumbnail-size-limit | 0 | 0 | 780059 | 0 | 0 | 716918 | 0 | 1550385 | 0 | 934295 | 0 | 2532116 | 0 | 0 | 0 | 12368088 | 846951 | 1847125 | 734836 | 0 | 0 | 0 |
| BUG-0117-miniapp-privacy-clipboard-phone-drift | 0 | 762102 | 0 | 0 | 0 | 0 | 476625 | 0 | 768305 | 0 | 1920696 | 0 | 3485195 | 0 | 0 | 8149270 | 0 | 1724473 | 2795194 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 3056 | 8057 | 0 | 0 | 14132 | 2096 | 22752 | 3277 | 7051 | 3548 | 28171 | 8415 | 0 | 0 | 96503 | 35773 | 12602 | 21231 | 0 | 0 | 8002 |
| sprint-020 | 0 | 3056 | 8057 | 0 | 0 | 14132 | 2096 | 22752 | 3277 | 7051 | 3548 | 28171 | 8415 | 0 | 0 | 96503 | 35773 | 12602 | 21231 | 0 | 0 | 8002 |
| REQ-0098-admin-media-list-thumbnails | 0 | 0 | 2924 | 0 | 0 | 4236 | 0 | 6915 | 0 | 2720 | 0 | 8299 | 0 | 0 | 0 | 22016 | 0 | 2600 | 6264 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 2559 | 0 | 0 | 4799 | 0 | 7534 | 0 | 2186 | 0 | 9511 | 0 | 0 | 0 | 17805 | 32034 | 2706 | 2443 | 0 | 0 | 0 |
| REQ-0099-global-thumbnail-size-limit | 0 | 0 | 2574 | 0 | 0 | 5097 | 0 | 8303 | 0 | 2145 | 0 | 10361 | 0 | 0 | 0 | 40846 | 3739 | 2131 | 5722 | 0 | 0 | 0 |
| BUG-0117-miniapp-privacy-clipboard-phone-drift | 0 | 3056 | 0 | 0 | 0 | 0 | 2096 | 0 | 3277 | 0 | 3548 | 0 | 8415 | 0 | 0 | 15836 | 0 | 5165 | 6802 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 7 | 20 | 0 | 0 | 13 | 4 | 26 | 6 | 18 | 14 | 40 | 19 | 0 | 0 | 224 | 80 | 63 | 56 | 0 | 0 | 21 |
| sprint-020 | 0 | 7 | 20 | 0 | 0 | 13 | 4 | 26 | 6 | 18 | 14 | 40 | 19 | 0 | 0 | 224 | 80 | 63 | 56 | 0 | 0 | 21 |
| REQ-0098-admin-media-list-thumbnails | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 10 | 0 | 8 | 0 | 13 | 0 | 0 | 0 | 68 | 0 | 14 | 18 | 0 | 0 | 0 |
| REQ-0100-mintlify-docs-site-ia-content-experience | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 7 | 0 | 5 | 0 | 15 | 0 | 0 | 0 | 26 | 67 | 15 | 7 | 0 | 0 | 0 |
| REQ-0099-global-thumbnail-size-limit | 0 | 0 | 6 | 0 | 0 | 5 | 0 | 9 | 0 | 5 | 0 | 12 | 0 | 0 | 0 | 90 | 13 | 13 | 13 | 0 | 0 | 0 |
| BUG-0117-miniapp-privacy-clipboard-phone-drift | 0 | 7 | 0 | 0 | 0 | 0 | 4 | 0 | 6 | 0 | 14 | 0 | 19 | 0 | 0 | 40 | 0 | 21 | 18 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint four-piece | medium | Fact Sheet token_risks：0 个四件套文件超过 200 行，但仍建议 summary-first | 复盘和归档均先读 Fact Sheet summary，只在 warning 时分段读取 |
| OpenSpec changes | medium | 4 个 Change，44/44 tasks | 少量 Change 可引用聚合 tasks；不默认展开所有 archived tasks/trace |
| Archive lookup | medium | archive paths 可由 sprint.yaml change ids 解析；residual_count 0 | 禁止宽泛扫描 `openspec/archive/**`，用 residual gate 定位 |
| Workflow Sync 输出 | medium | sprint.archive 同步检查 28 个子文档 | 成功路径只记录 summary，不输出 detail |
| OpenAPI / Orval 生成物 | medium | REQ-0098、REQ-0099 涉及 API/Orval | 复盘仅引用同步事实，不读取 generated diff 全文 |
| stale scan 诊断 | low | 初次归档命中过中间态文案 | 只按 blocker 文件行修复，不全文展开 Issue 包 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认读取全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 输出截断 | 符合 | 成功路径仅使用 summary 与聚合计数；未输出完整 evidence hints |
| 生成物控制 | 符合 | 没有展开 OpenAPI、Orval generated 或测试日志全文 |
| 已读摘要复用 | 符合 | 复用本会话已读 AGENTS、文档治理、目录、迭代生命周期、workflow-sync、opsx-archive 摘要；本次只补读 sprint-exps 与上下文预算 |
| 需要修正 | open | AI usage fresh gate 与 Sprint 计划日期的关系仍会阻塞本次真实矩阵输出 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-020-001 | P1 | 修复或明确 sprint-exps fresh gate 对未来计划 start_date 的判定，避免归档后真实 hook 已刷新但 summary 仍 stale | `/bug-capture` | open |
| T-020-002 | P1 | 为媒体类需求沉淀“列表展示字段 / 生成策略 / 历史维护”三段验收模板 | `/req-capture` | open |
| T-020-003 | P2 | stale scan 增加业务词例外或文档写法提示，避免 `pending` 业务语义误判 | `/bug-capture` | open |
| T-020-004 | P2 | Sprint Scope 与目标编号列表一致性校验纳入 sprint-propose / workflow-sync 检查 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0098 聚焦列表优先缩略图 | 用户体验目标清晰，且明确详情/编辑/预览继续原图，降低了行为歧义 | 后续所有图片密集列表需求都应写清“列表资源”和“详情资源”分工 |
| REQ-0099 引入全局体积上限 | 默认不限制、只影响增量、历史对象显式重生成，降低破坏性 | 系统设置类媒体策略应默认无行为变化，启用后再生效 |
| REQ-0100 覆盖文档站 IA | 文档站不是纯文档编辑，已经进入 release governance 与校验脚本边界 | Mintlify 类变更应继续纳入发布治理，不作为零散站点修补 |
| BUG-0117 处理隐私声明漂移 | 小程序能力声明与真实接口能力必须一致 | 发布前 miniapp-prepare 应保留隐私接口静态扫描与提审口径复核 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | REQ-0098、REQ-0099 涉及 API 字段和设置 Schema，同步 OpenAPI/Orval 是必要门禁 | API 变更继续同步 `docs/03-api-index.md`、OpenAPI、Orval 与前后端测试 |
| DB | 本 Sprint 不改数据库结构 | 后续若缩略图策略持久化扩展到新表或迁移，必须同步 DB 文档和 migration 测试 |
| Web 管理端 | 图片 fallback、表格布局、toast/confirm 仍是高频横切风险 | 继续复用 admin-list 与 admin-form best practices |
| 小程序 | 隐私接口能力比 UI 展示更容易影响提审 | 对 `wx.makePhoneCall`、`wx.setClipboardData` 等接口保留静态扫描 |
| 文档站 | Mintlify IA 调整需要 broken links、公开安全和版本入口校验 | 文档站变更必须更新 site manifest / README / release 投影 |
| 归档 | readiness + stale scan + residual gate 可以捕捉文档事实漂移 | close 前先预检，再关 Sprint，可降低最后返工 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| List image fallback adapter | REQ-0098 | 将列表缩略图、原图 fallback、占位图、render evidence 做成管理端列表组件约定 |
| Thumbnail policy service | REQ-0099 | 后端媒体缩略图生成统一读取全局策略，避免 SKU/品牌/证书/Banner 各写一套 |
| Miniapp privacy interface scan | BUG-0117 | 小程序发布前固定扫描隐私敏感 API，并映射到提审声明 |
| Docs site IA validation | REQ-0100 | Mintlify 站点导航、版本、任务入口、公开安全形成独立校验门禁 |
| Sprint close stale preflight | sprint-020 archive | 在 close 前固定检查 Issue 子文档中间态与旧路径残留 |

## 6. 行动项

| ID | 优先级 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议下一命令 | 状态 |
|----|--------|----------|------|------|----------|--------------|------|
| A-020-001 | P1 | BUG | sprint-exps AI usage fresh gate 对未来计划 start_date 判定导致真实矩阵阻塞 | sprint-020 归档后 hook 可刷新 snapshot，但 Fact Sheet summary 仍因 start_date baseline 判 stale | sprint-exps、Fact Sheet、AI usage snapshot | `/bug-capture` | open |
| A-020-002 | P1 | REQ | 媒体类需求三段验收模板 | 缩略图展示、生成策略、历史维护常被混在同一验收链路 | REQ/BUG 文档、media upload、object storage、admin web | `/req-capture` | open |
| A-020-003 | P2 | BUG | stale scan 对业务词 pending 误判为流程中间态 | REQ-0099 中 “SKU pending 图片正式化” 触发 close blocker | sprint archive readiness、Issue 文档 | `/bug-capture` | open |
| A-020-004 | P2 | REQ | Sprint 目标编号列表与 Scope 一致性校验 | sprint-020 Scope 含 REQ-0100，但目标编号列表未列出 | sprint-propose、workflow-sync、validate-sprint-scope | `/req-capture` | open |

未自动创建 Issue。以上行动项可作为后续 `/capture`、`/req-capture` 或 `/bug-capture` 输入。

## 7. Follow-up Capture 文案

### Follow-up 1

- 建议命令：`/bug-capture`
- 类型倾向：BUG
- 标题：sprint-exps AI usage fresh gate 对未来计划 start_date 判定导致真实矩阵阻塞
- 背景：sprint-020 已归档，post-command hook 曾刷新 AI usage snapshot，但 Fact Sheet summary 仍显示 `snapshot_status: stale` 与 `ai_usage_mode: estimated_fallback`，导致复盘不能输出真实成本矩阵。
- 影响范围：`scripts/generate-sprint-fact-sheet.py`、`scripts/extract-ai-usage.py`、`data/ai-usage/sprints/<sprint-id>.json`、`/sprint-exps`。
- 建议验收或复现要点：归档 Sprint 后运行 usage hook，再运行 Fact Sheet summary；fresh gate 应能解释或正确通过，不得在 actual snapshot 已刷新后仍无依据阻塞矩阵输出。
- 来源 Change/Sprint/命令：Sprint `sprint-020`，命令 `/sprint-exps sprint-020`。

### Follow-up 2

- 建议命令：`/req-capture`
- 类型倾向：REQ
- 标题：媒体类需求三段验收模板
- 背景：sprint-020 同时覆盖列表缩略图展示、缩略图生成策略和历史对象维护入口，验收证据容易分散。
- 影响范围：需求模板、BUG 验收、media upload、object storage、admin web 列表。
- 建议验收或复现要点：模板应强制拆分“列表展示字段”“生成策略”“历史对象维护/重生成”三段证据，并明确 API/Orval/DB/对象存储影响。
- 来源 Change/Sprint/命令：Sprint `sprint-020`，命令 `/sprint-exps sprint-020`。

### Follow-up 3

- 建议命令：`/bug-capture`
- 类型倾向：BUG
- 标题：stale scan 对业务词 pending 误判为流程中间态
- 背景：归档时需求正文中的 “SKU pending 图片正式化” 被识别为 Issue 中间态残留。
- 影响范围：`scripts/check-sprint-close-stale-scan.py`、Sprint archive readiness、Issue 文档写作规范。
- 建议验收或复现要点：普通正文中的业务词应按上下文判断；状态字段、状态表格和流程说明仍应被严格扫描。
- 来源 Change/Sprint/命令：Sprint `sprint-020`，命令 `/sprint-exps sprint-020`。

### Follow-up 4

- 建议命令：`/req-capture`
- 类型倾向：REQ
- 标题：Sprint 目标编号列表与 Scope 一致性校验
- 背景：sprint-020 Scope 包含 REQ-0100，但 `sprint.md` 目标编号列表未列出，可能影响人读理解。
- 影响范围：`/sprint-propose`、Workflow Sync、`validate-sprint-scope.py`、Sprint 四件套。
- 建议验收或复现要点：新增或同步 Sprint Scope 后，目标编号列表与 Scope 主表应一致；校验失败应提示具体缺失项。
- 来源 Change/Sprint/命令：Sprint `sprint-020`，命令 `/sprint-exps sprint-020`。
