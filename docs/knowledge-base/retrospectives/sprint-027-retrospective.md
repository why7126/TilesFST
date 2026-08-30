---
title: sprint-027 复盘
purpose: 复盘 sprint-027 的流程、需求、开发质量、媒体治理经验与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-027
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-30 09:11:14
updated_at: 2026-08-30 09:11:14
---

# sprint-027 复盘

## 概况

sprint-027 已完成归档，目录为 `iterations/archive/sprint-027/`。本 Sprint 覆盖 2 个 REQ、1 个 BUG、3 个 OpenSpec Change，68/68 个任务完成；归档路径残留、陈旧引用扫描、Workflow Sync 和产品数据采集与链路观测门禁均已通过。验收结论为 partial：Sprint 范围内实现与归档闭环，BUG-0146 的生产 no-fallback 与公开 API 字段一致性补证后置到发布/运维窗口。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 媒体维护运维体验 | REQ-0130 | 进度输出必须与 stdout 最终 JSON 隔离，生产命令默认仍保持可被脚本消费 |
| 媒体对象 Key 治理 | REQ-0131 | 业务对象 id 分目录会穿透上传、派生图、迁移、回滚、Runbook 和端侧读取，必须用 dry-run/apply/audit 证据守住批量改写边界 |
| Banner 历史派生图补齐 | BUG-0146 | `/media` fallback 的 HTTP 200 会掩盖派生图缺失，验收必须看 `Content-Type`、`x-media-fallback` 和公开 API 字段 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 2 |
| bugs | 1 |
| changes | 3 |
| tasks | 68/68 |
| estimated story points | 5 |
| estimated person days | 5 |
| capacity usage | 16.67% |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | pass |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-027 --json` 报告 `residual_count=0`。产品数据采集与链路观测门禁：`validate-product-data-observability-gates.py --sprint sprint-027` 已通过，REQ-0131 的 request_logs、task_traces、task_trace_spans、backend_api、web_admin_request_flow、wechat_miniapp_request_flow、maintenance_jobs 适用层级可追溯。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| Sprint 范围聚焦 | 3 个 Change 均围绕媒体维护和对象存储 Key 治理，任务规模可控 | 小 Sprint 可直接按 `sprint.yaml` changes[] 和 Fact Sheet summary 复盘，不需要展开归档全文 |
| 运维命令兼容性 | REQ-0130 明确进度输出走 stderr 或等价隔离通道，保留 stdout JSON 契约 | 生产 CLI 增强默认先声明 stdout/stderr 边界，再补进度字段和脱敏要求 |
| 批量媒体治理证据 | REQ-0131 覆盖 key 矩阵、迁移 dry-run/apply/audit/rollback、旧 key 兼容和 Runbook | 涉及对象存储改写时，把“旧引用可读、新 key 可追溯、派生图同目录、可回滚”作为最小验收集合 |
| 收尾门禁有效 | stale scan、residual gate、Workflow Sync 和 AI Usage fresh gate 均在归档后通过 | 复盘只消费通过门禁后的事实源，避免把 active 阶段旧路径和旧状态带入知识库 |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| 生产补证未完全闭环 | BUG-0146 生产历史无 id Banner URL 在 2026-08-30 08:23 仍返回 `image/png` 与 `x-media-fallback=1` | 本地 alias apply 已证明逻辑可行，但生产公网复核需要使用生产 MySQL/env 重新执行维护任务 | 把生产 no-fallback 与公开 API 字段一致性列为发布/运维窗口独立 BUG 或发布前 gate |
| fallback 掩盖真实缺陷 | `/media` 返回 HTTP 200 时仍可能是原图 fallback，不代表 `.thumb.webp` / `.display.webp` 已存在 | 验收早期容易只看 URL 可访问，而没有看响应头和内容类型 | 媒体派生图验收必须固定记录 `Content-Type`、`Content-Length`、`x-media-fallback` 和端侧 render |
| 非 Banner 残留失败 | 生产 apply JSON 仍有非 Banner `sku_image` 失败：`summary.failed=2`、`retry_candidates=2`、`OSError=2` | BUG-0146 主线聚焦 Banner，但批量维护命令暴露了同任务下的其他对象存储异常 | 批量维护 apply 后将非主线失败单独 capture，避免挤在已归档 Sprint 的验收尾部 |
| AI Usage 发现口径曾不稳定 | 归档链路依赖本地 session JSON 时，若默认发现目录不明确会影响成本分析 | 旧口径未把 `~/.codex/sessions` 固化为默认 session discovery 规范 | sprint-028 已通过 `standardize-ai-usage-session-discovery` 归档修正，后续复盘沿用 actual snapshot + fresh gate |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-027.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Matrix write gate | pass | 必须 fresh gate pass、actual/present 且矩阵存在才可输出真实矩阵 |
| Freshness baseline | 2026-08-30T00:45:27Z | 来源：`acceptance-report.md:updated_at`；跳过 sprint.yaml:end_date=2026-09-12 18:13:44（future-planned-time） |
| Generated at | 2026-08-30T01:13:42.755054Z | `data/ai-usage/sprints/sprint-027.json` |
| command_run_count | 35 | snapshot totals |
| model_call_count | 343 | snapshot totals |
| tool_call_count | 600 | snapshot totals |
| input_tokens | 48,883,352 | snapshot totals |
| cached_input_tokens | 47,481,984 | snapshot totals |
| output_tokens | 167,464 | snapshot totals |
| reasoning_output_tokens | 19,423 | snapshot totals |
| total_tokens | 49,146,205 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 5 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。`-` 表示该 workflow 阶段在当前 snapshot 中未采集或未归因，不等价于真实 `0`；只有已观测 workflow 列中的数字 `0` 才表示真实零消耗。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 380985 | 1580613 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7767612 | 39416995 | 0 | 0 | - | - | 0 |
| sprint-027 | - | 380985 | 1580613 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7767612 | 39416995 | 0 | 0 | - | - | 0 |
| REQ-0130-media-maintenance-progress-output | - | 0 | 640241 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 4608384 | 4428897 | 0 | 0 | - | - | 0 |
| REQ-0131-media-object-key-business-id-layout | - | 0 | 940372 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 25295172 | 0 | 0 | - | - | 0 |
| BUG-0146-batch-media-maintenance-banner-variants | - | 380985 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3159228 | 9692926 | 0 | 0 | - | - | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 377307 | 1573735 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7706222 | 39226088 | 0 | 0 | - | - | 0 |
| sprint-027 | - | 377307 | 1573735 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 7706222 | 39226088 | 0 | 0 | - | - | 0 |
| REQ-0130-media-maintenance-progress-output | - | 0 | 636669 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 4590928 | 4415267 | 0 | 0 | - | - | 0 |
| REQ-0131-media-object-key-business-id-layout | - | 0 | 937066 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 25192583 | 0 | 0 | - | - | 0 |
| BUG-0146-batch-media-maintenance-banner-variants | - | 377307 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 3115294 | 9618238 | 0 | 0 | - | - | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 3678 | 6878 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 32603 | 124305 | 0 | 0 | - | - | 0 |
| sprint-027 | - | 3678 | 6878 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 32603 | 124305 | 0 | 0 | - | - | 0 |
| REQ-0130-media-maintenance-progress-output | - | 0 | 3572 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 17456 | 13630 | 0 | 0 | - | - | 0 |
| REQ-0131-media-object-key-business-id-layout | - | 0 | 3306 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 71158 | 0 | 0 | - | - | 0 |
| BUG-0146-batch-media-maintenance-banner-variants | - | 3678 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 15147 | 39517 | 0 | 0 | - | - | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 7 | 12 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 65 | 259 | 0 | 0 | - | - | 0 |
| sprint-027 | - | 7 | 12 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 65 | 259 | 0 | 0 | - | - | 0 |
| REQ-0130-media-maintenance-progress-output | - | 0 | 6 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 34 | 20 | 0 | 0 | - | - | 0 |
| REQ-0131-media-object-key-business-id-layout | - | 0 | 6 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 0 | 164 | 0 | 0 | - | - | 0 |
| BUG-0146-batch-media-maintenance-banner-variants | - | 7 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - | 31 | 75 | 0 | 0 | - | - | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Opsx-Modify | high | `Opsx-Modify` total_tokens 39,416,995，占 Sprint 总量最大；REQ-0131 单项 25,295,172，BUG-0146 单项 9,692,926 | 媒体治理返修先用 no-fallback 响应头、dry-run/apply JSON 和对象 key diff 定位，不重复读取完整归档材料 |
| Opsx-Apply | high | `Opsx-Apply` total_tokens 7,767,612；REQ-0130 与 BUG-0146 均有 apply 消耗 | 小 Sprint 实现阶段仍应从变更任务、相关脚本和最小测试入手，避免把 Runbook、规则和 trace 每轮全量展开 |
| REQ Capture | medium | `REQ-Capture` total_tokens 1,580,613；两个 REQ 都在捕获阶段形成了较完整范围 | 媒体治理 REQ 捕获时只写目标、边界和验收问题，详细矩阵留到 Change proposal 或 design |
| BUG Capture | low | `BUG-Capture` total_tokens 380,985 | 生产缺陷捕获保持轻量，但必须包含复现 URL、响应头和环境口径 |
| Archive lookup | medium | 归档路径由 `sprint.yaml` changes[] 解析，residual_count=0 | 复盘、发布、回溯统一引用 `openspec/archive/YYYY-MM-DD-<change-id>/`，不 broad-scan 历史目录 |

### Token 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-027-01 | P1 | 为媒体派生图缺陷建立固定证据包：源 URL、派生 URL、`Content-Type`、`x-media-fallback`、公开 API 字段、端侧 render 截图 | `/req-capture` | open |
| T-027-02 | P1 | 对批量媒体维护的生产 apply 失败项单独 capture，避免后续复盘反复从归档材料中拆主线与旁支 | `/bug-capture` | open |
| T-027-03 | P2 | `sprint-exps` 继续只在 AI Usage fresh gate pass 时写真实矩阵；fail 时输出 recommended_action 并停止矩阵落盘 | 下一 Sprint 执行约束 | done |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| CLI 输出契约 | REQ-0130 的核心不是“显示进度”，而是“显示进度同时不破坏生产 JSON 消费链路” | 运维 CLI 新增人类可读输出时，默认把机器可读 stdout 视为 API 契约 |
| Key 目录治理 | REQ-0131 将用户头像、品牌 Logo、Banner、SKU 图片/视频、证书图片/文件统一到业务对象 id 目录 | 对象 Key 规范不是纯存储规范，必须同步 DB 引用、端侧禁止拼 URL、旧 key 兼容和迁移 rollback |
| Banner 历史数据 | BUG-0146 暴露历史无 id key 与新目录策略之间的 alias/派生图补齐问题 | 新 key 规范落地后，历史数据兼容要作为独立验收项，不能只验证新上传路径 |
| 生产与本地证据边界 | 本地 alias apply 和 no-fallback 已通过，但生产公网仍未闭环 | 本地等价证据可证明实现逻辑，不可替代生产窗口的最终发布证据 |

## 开发质量复盘

| 维度 | 观察 | 后续要求 |
|------|------|----------|
| 自动化覆盖 | REQ-0131 覆盖后端 key/maintenance/deploy、Pillow 媒体、小程序媒体和管理端媒体 Vitest | 媒体治理 Change 继续保留跨层测试，尤其是派生图、迁移和端侧读取边界 |
| 运维证据 | BUG-0146 保留 local dry-run、backfill dry-run、production apply JSON、local alias apply、local no-fallback 等证据 | 生产补证必须补同一 URL 维度的 no-fallback 与公开 API 字段一致性 |
| 文档同步 | Runbook、对象存储策略、Sprint 验收报告和归档 trace 均已同步 | 若后续执行旧对象清理或生产重跑，需要新增发布/运维记录，不回改已归档 Sprint 事实 |
| 门禁脚本 | stale scan、residual gate、observability gate 和 AI Usage hook 让收尾状态更可验证 | 文档治理类变更应继续优先落脚本，而不是靠复盘文字提醒 |

## 行动项

| ID | 优先级 | 类型 | 描述 | 建议命令 | 状态 |
|----|--------|------|------|----------|------|
| A-027-01 | P1 | BUG | 补生产 Banner 历史无 id 派生图 no-fallback 与公开 API 字段一致性证据 | `/bug-capture` | open |
| A-027-02 | P1 | BUG | 追踪生产 apply 中非 Banner `sku_image` 的 `OSError` 失败与 `retry_candidates=2` | `/bug-capture` | open |
| A-027-03 | P2 | REQ | 建立媒体派生图 no-fallback/API 字段一致性 smoke，作为发布前可复用检查 | `/req-capture` | open |
| A-027-04 | P2 | 规范 | 固化 `~/.codex/sessions` 为 AI Usage 默认 session discovery，避免复盘成本分析缺口 | `standardize-ai-usage-session-discovery` | done，已在 sprint-028 归档 |

## 可复用实践

- 媒体维护命令输出分层：stdout 保持最终 JSON，stderr 或隔离通道输出进度，生产日志默认脱敏。
- 媒体派生图验收固定检查响应头，不把 HTTP 200 当作派生图已生成的充分条件。
- 批量对象存储迁移先 dry-run，再 apply/audit，rollback 和旧 key 读取兼容必须同时保留。
- Sprint 复盘默认从 Fact Sheet summary 与 AI Usage markdown 获取聚合事实；只有 warnings、missing 或用户指定细节时才回读归档原文。

## 回链

- Sprint 归档：`iterations/archive/sprint-027/`
- 验收报告：`iterations/archive/sprint-027/acceptance-report.md`
- 关联 REQ：`issues/requirements/archive/REQ-0130-media-maintenance-progress-output/`、`issues/requirements/archive/REQ-0131-media-object-key-business-id-layout/`
- 关联 BUG：`issues/bugs/archive/BUG-0146-batch-media-maintenance-banner-variants/`
- AI Usage snapshot：`data/ai-usage/sprints/sprint-027.json`
