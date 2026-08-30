---
title: sprint-028 复盘
purpose: 复盘 sprint-028 的流程、媒体缺陷修复、发布治理、环境证据门禁与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-028
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-30 14:50:52
updated_at: 2026-08-30 14:50:52
---

# sprint-028 复盘

## 概况

sprint-028 已完成归档，目录为 `iterations/archive/sprint-028/`。本 Sprint 覆盖 0 个 REQ、1 个 BUG、5 个 OpenSpec Change，43/43 个任务完成；归档路径残留、陈旧引用扫描、环境分层证据门禁、目录结构校验、Workflow Sync 和产品数据采集与链路观测门禁均已通过。验收结论为 passed。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| AI Usage 治理 | `standardize-ai-usage-session-discovery` | 本地存在 Codex session 时应优先自动发现，失败再要求显式 `--session-jsonl` |
| 小程序证书媒体缺陷 | BUG-0147 / `fix-miniapp-certificate-media-urls` | 图片类证书验收必须同时看 API 字段、对象 key、公开 URL 和端侧 render |
| 发布决策面板 | `add-release-status-decision-panel` | 发布命令输出应把缺失决策、证据缺口、生产后置项和环境不可用分开 |
| 环境分层证据 | `standardize-environment-tiered-evidence-gates`、`enforce-environment-tiered-evidence-gates` | 开发归档、体验版验收、生产发布必须使用不同证据边界，不能互相冒充 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 0 |
| bugs | 1 |
| changes | 5 |
| tasks | 43/43 |
| estimated story points | 7 |
| estimated person days | 7 |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | blocker |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-028 --json` 报告 `residual_count=0`。产品数据采集与链路观测门禁：`validate-product-data-observability-gates.py --sprint sprint-028` 已通过，适用层级覆盖 `backend_api`、`wechat_miniapp_request_flow`、`request_logs`、`maintenance_jobs`，Task Trace 按实际维护任务使用情况判断。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| Sprint 收口清晰 | 5 个 Change 均已先归档，再关闭 Sprint | `/sprint-archive` 只消费 `sprint.yaml` 与 Fact Sheet summary，避免重复展开所有 archive 内容 |
| 媒体缺陷证据具体 | BUG-0147 没有停留在 HTTP 200，而是要求 key/object/URL/render 四联证据 | 图片、视频、证书等媒体缺陷沿用 `miniapp-media-four-part-acceptance-practice` |
| 发布状态分类更可执行 | release status 输出开始区分 decision、prepare、publish、production_only_pending 等 blocker 类型 | 发布前状态面板应给出“当前阶段 + 阻塞分类 + 下一命令”，减少靠口头判断推进 |
| 环境门禁脚本化 | 环境分层证据从规则文字进入 `validate-environment-tiered-evidence.py` 与归档/发布校验 | 生产证据不可得时记录为后置项，不阻塞开发归档；生产发布时重新判定 |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| AI Usage 覆盖归因不完整 | Fact Sheet summary 显示 `changes-coverage-missing`，缺少 `standardize-environment-tiered-evidence-gates` 覆盖 | 历史 command-run 与 Sprint snapshot 聚合口径未能把该治理 Change 归因进去 | 后续治理 Change 归档时确认 command-run 落在 `data/ai-usage/command-runs/opsxs/<change-id>/` 或等价可聚合路径 |
| Sprint 文档容易遗留 active path | `/sprint-archive` 前曾发现 `openspec/changes/...` 旧路径引用 | 归档 Change 后，人读文档关联区不一定由 Workflow Sync 完全覆盖 | 关闭前固定跑 residual gate，并只写 `openspec/archive/YYYY-MM-DD-<change-id>/` |
| 发布/环境规则容易散落 | sprint-028 同时修改 Skill、rules、scripts、release status 口径 | 门禁类规则跨多个命令族，若只改一处会产生状态解释漂移 | 治理 Change 必须包含入口文件、技能、脚本、测试和复盘说明的同步矩阵 |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 无法安全作为完整真实矩阵使用 | 来源：`data/ai-usage/sprints/sprint-028.json` 存在，但 Fact Sheet fresh gate 未通过 |
| AI usage mode | estimated_fallback | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | blocker | blocker: `changes-coverage-missing`、`usage-mode-estimated_fallback` |
| Matrix write gate | blocker | `usage_matrices_summary.available=false`，不得输出真实 token 成本矩阵 |
| Freshness baseline | 2026-08-30T06:46:49Z | 来源：`sprint.md:updated_at` |
| Generated at | 2026-08-30T06:47:54Z | snapshot 已刷新，但覆盖仍不足 |
| 覆盖缺口 | `standardize-environment-tiered-evidence-gates` | Sprint scope 期望 5 个 Change，snapshot 聚合只识别 4 个 |
| 主要输入消耗风险 | 中 | Sprint 四件套虽均小于 200 行，但 OpenSpec archive 有 5 个 Change、43 个 tasks，默认应走 summary |
| 主要输出消耗风险 | 中 | Workflow Sync、Fact Sheet JSON 与测试日志容易输出过长，成功路径应只保留摘要 |
| 已采用节省策略 | 已采用 | 使用 Fact Sheet summary、归档残留 JSON、聚合计数和短片段，未展开全部 trace/tasks |

本次不写 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张真实矩阵。原因是 fresh gate 和 matrix write gate 均为 blocker；现有 snapshot 可用于提示风险和定位覆盖缺口，不能用于真实 token 成本量化。推荐动作：确认自动发现的 `AI_USAGE_SESSIONS_DIR` 或 `~/.codex/sessions` 中是否包含 `standardize-environment-tiered-evidence-gates` 可归因 token_count 事件，必要时使用显式 `--session-jsonl` 做历史回溯。

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec archive 回读 | medium | 5 个 Change、43/43 tasks；Fact Sheet 标记 archive lookup 为 medium | 复盘默认只看 Fact Sheet summary，只有 warnings 或用户要求时读 evidence hints |
| Workflow / 发布治理规则扩散 | medium | 本 Sprint 同时触达 release status、sprint archive、environment evidence、AI Usage | 治理 Change 用同步矩阵和脚本校验减少多轮人工比对 |
| AI Usage 归因缺口 | medium | `changes-coverage-missing` 导致矩阵不可写 | 将 usage hook 归档路径和 Change ID 聚合纳入下一轮治理检查 |
| 媒体四联证据 | low | BUG-0147 需要 API 字段、对象 key、URL、render 多证据 | 保留固定证据模板，避免每次重新解释验收口径 |

### Token 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-028-01 | P1 | 修正 AI Usage Sprint snapshot 对已归档治理 Change 的覆盖聚合，避免 fresh gate 在 snapshot 已刷新后仍报 `changes-coverage-missing` | `/bug-capture` | open |
| T-028-02 | P2 | 为 `/sprint-exps` 输出增加“矩阵不可写但 snapshot 存在”的固定说明，避免误读 `estimated_fallback` | `/opsx-propose` | open |
| T-028-03 | P2 | 继续执行 Fact Sheet summary 优先、warnings 后再回读 evidence hints 的复盘策略 | 下一 Sprint 执行约束 | done |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| BUG 进入 Sprint 的时机 | BUG-0147 作为高优先级生产小程序问题进入 Sprint，范围聚焦到证书列表图片 URL/缩略图 | 生产缺陷进入 Sprint 时，优先保留单一用户可见失败面，再把治理补强作为独立 Change |
| 媒体字段契约 | 图片类证书不能只依赖端侧 fallback，后端 API 应返回可渲染 `file_url` 或 `thumbnail_url` | 媒体字段要以端侧实际渲染为验收出口，API、对象存储和小程序展示一起闭环 |
| 发布状态决策 | release status 不应只告诉“失败”，还应告诉失败属于输入缺失、证据缺失还是生产后置 | 发布面板是操作导航，不是日志转述；分类越稳，用户越容易做下一步决策 |
| 环境分层证据 | 开发、体验版、生产证据的边界被写入规则并脚本化 | 开发归档可以通过开发证据闭环，生产发布必须单独确认生产门禁 |

## 开发质量复盘

| 维度 | 观察 | 后续要求 |
|------|------|----------|
| 自动化覆盖 | Sprint close readiness、环境分层证据、产品观测门禁、目录结构和 Workflow Sync 均通过 | 归档类命令继续把脚本结果作为事实源，避免靠人读状态判断 |
| 媒体回归 | BUG-0147 继承 sprint-027 媒体四联验收经验 | 后续媒体缺陷必须记录对象 key、公开 URL、响应头和端侧 render |
| 文档同步 | `sprint.md` 已补 `reason`，关联 Change 路径已切换到 archive | 复盘和发布文档不得传播 active Change 旧路径 |
| 治理脚本 | 环境 evidence gate 接入归档与发布链路 | 治理脚本需要同时验证正向 pass 和典型错误分类，防止口径漂移 |

## 行动项

| ID | 优先级 | 类型 | 描述 | 建议命令 | 状态 |
|----|--------|------|------|----------|------|
| A-028-01 | P1 | BUG | AI Usage Sprint snapshot 已刷新但缺少 `standardize-environment-tiered-evidence-gates` 覆盖，导致复盘矩阵不可写 | `/bug-capture` | open |
| A-028-02 | P2 | REQ | 为媒体类 BUG 建立统一证据包生成/校验入口，减少每次手工组织 key/object/URL/render 证据 | `/req-capture` | open |
| A-028-03 | P2 | 规范 | 发布状态决策面板与环境分层证据门禁可在后续 release/sprint 命令中继续观察是否需要精简输出 | 下一 Sprint 观察 | open |

## 可复用实践

- 媒体缺陷验收使用 key、object、URL、render 四联证据，不把 HTTP 200 当作充分条件。
- 发布与归档命令输出要区分开发证据、体验版证据和生产发布证据，生产后置项不得伪装成开发通过。
- Sprint 关闭后复盘只引用 `iterations/archive/<sprint-id>/` 与 `openspec/archive/YYYY-MM-DD-<change-id>/`。
- AI Usage fresh gate 未通过时，复盘应记录 blocker 与 recommended_action，不写真实成本矩阵。

## 回链

- Sprint 归档：`iterations/archive/sprint-028/`
- 验收报告：`iterations/archive/sprint-028/acceptance-report.md`
- 关联 BUG：`issues/bugs/archive/BUG-0147-miniapp-certificate-list-images-missing/`
- 关联 Change：`openspec/archive/2026-08-30-standardize-ai-usage-session-discovery/`、`openspec/archive/2026-08-30-fix-miniapp-certificate-media-urls/`、`openspec/archive/2026-08-30-add-release-status-decision-panel/`、`openspec/archive/2026-08-30-standardize-environment-tiered-evidence-gates/`、`openspec/archive/2026-08-30-enforce-environment-tiered-evidence-gates/`
- AI Usage snapshot：`data/ai-usage/sprints/sprint-028.json`
