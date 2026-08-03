---
sprint_id: sprint-018
title: Sprint 018 迭代经验复盘
status: draft
created_at: 2026-08-03 20:54:07
updated_at: 2026-08-03 20:54:07
owner: product
related_iteration: iterations/archive/sprint-018/
source: /sprint-exps sprint-018
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 018 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-08-03 08:40:00 ~ 2026-08-17 18:00:00 |
| REQ / BUG / Change | 2 / 8 / 10 |
| Change 批次 | 2 批；每批 5 个 Change |
| tasks 完成度 | 132/132 |
| 估算 | 25 SP / 25 人天 |
| 容量 | 30 人天；占用 83.33%；fix buffer 16.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；10/10 Change archived |
| AI usage | Fresh gate blocker；Fact Sheet 暂不允许输出真实 token 成本矩阵 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-018 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-018 --json`、`iterations/archive/sprint-018/sprint.yaml`、`iterations/archive/sprint-018/acceptance-report.md`、`data/ai-usage/sprints/sprint-018.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| Mintlify 多版本文档站治理 | 建立 `mintlify/` 源目录、release usage docs 投影、`latest` 指针、共享截图资产和可选 docs-site profile |
| 部署环境矩阵治理 | 标准化 `deploy/`、local/prod env 示例、Compose 脚本入口、部署文档和发布镜像输入追踪 |
| 管理后台展示修复 | 品牌 Logo、证书字段、SKU 表头、品牌编辑 Logo 成功态、类目中文括号等展示/校验问题收口 |
| 小程序展示修复 | 返回首页按钮重复点击、卡片和 Banner 缩略图策略、品牌/商品/证书列表轻量 URL 使用 |
| Sprint 关闭治理 | readiness、stale scan、residual、Workflow Sync、AI usage hook 全部闭环 |

### Change 批次摘要

| 批次 | Change 数 | tasks | warnings | blockers | recommended next read |
|------|----------:|------:|---------:|---------:|-----------------------|
| batch-001 | 5 | 84/84 | 1 | 0 | batch_evidence_hints |
| batch-002 | 5 | 48/48 | 1 | 0 | batch_evidence_hints |

两批 warning 均为 archived Change 缺 `trace.md`，分别是 `fix-miniapp-home-navigation-repeat-click` 与 `fix-admin-brand-edit-logo-uploaded-text`。Sprint readiness 通过 fallback summary，因此不阻断关闭，但复盘行动项应推动归档证据标准化。

## 2. 流程复盘

### 做得好的

1. **大 Sprint 仍完成了完整归档闭环**：10 个 Change 全部 archived，132/132 tasks 完成，Sprint close stale scan 与 archived path residual gate 均为 PASS。
2. **治理需求与缺陷修复同 Sprint 收口**：REQ-0093/REQ-0094 建立部署与文档站基础设施，同时 8 个 BUG 修复集中清理管理端和小程序展示体验。
3. **`sprint-archive` 及时暴露事实漂移**：关闭前发现已 archived Issue/Change 文档里残留 `proposed`、`in_sprint`、`待 archive` 等中间态文案，修复后 stale scan 清零。
4. **多 Change 批次机制有价值**：Fact Sheet 的 `change_batches` 让复盘能在 10 个 Change 场景下先看聚合计数和 warning，而不是展开所有 tasks/trace。
5. **归档路径残留控制有效**：迁移到 `iterations/archive/sprint-018/` 后，136 个 scoped 文件残留为 0，未传播旧 `iterations/change/` 或 active Change 路径。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| archived Change 仍有 2 个缺 `trace.md` | Fact Sheet warnings: `change-trace-missing` x2 | readiness 可依赖 fallback summary 通过，但后续追溯成本高于标准 trace |
| Sprint acceptance 报告仍保留部分未勾验收补充项 | Fact Sheet acceptance signals 包含若干 `- [ ]` 人工验收补充 | Sprint 最终结论已 passed，但人读时可能误解为整体验收未完成 |
| BUG-0110 需要终端外手工验证 | sprint-archive 已将微信开发者工具/体验版网络面板验证记录为风险限制 | 代码与接口测试可闭环，但真实端上网络请求仍需发布/体验版阶段复核 |
| AI usage fresh gate 与 snapshot 状态不一致 | snapshot 文件已刷新，但 Fact Sheet fresh gate 仍报 stale / estimated_fallback blocker | 复盘不能输出真实 token 成本矩阵，说明 fresh gate 判定或刷新触发需要改进 |
| Sprint 容量接近上限 | 25/30 人天，fix buffer 16.67% | 治理需求加多个 UI BUG 容易压缩验收和返修缓冲 |

### 优化建议

1. **将 archived Change 证据标准升级为必选 trace 或结构化 fallback**：fallback 可继续保留，但缺 trace 应在 opsx-archive 阶段自动写入最小 trace 或更强提示。
2. **Sprint acceptance 人工补充项需要关闭语义**：如果某条为终端外验证或发布期验证，应标记 `waived`、`external` 或 `release-gate`，避免保留普通未勾项。
3. **小程序端上验证要前置到 release checklist**：无法在终端完成的 DevTools/体验版网络面板验证，应进入 release-prepare 或 miniapp-prepare 清单。
4. **Fact Sheet AI usage fresh gate 需要自检**：当 snapshot `estimated: false` 且矩阵存在但 fresh gate 仍 blocker，应输出更具体原因或提供自动修复命令。
5. **10+ Change Sprint 默认 batch-first**：sprint-exps、sprint-archive、sprint-apply 都应先消费批次摘要，再按 warning/blocker 精读。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 暂不展示 | Fact Sheet fresh gate 为 blocker，按技能要求不得输出真实成本矩阵 |
| AI usage mode | estimated_fallback | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | stale | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | blocker | blocker: `snapshot-status-stale`、`usage-mode-estimated_fallback` |
| Snapshot 文件状态 | 已存在，且本次尝试刷新后仍被 Fact Sheet 判 stale | `data/ai-usage/sprints/sprint-018.json` 可读；fresh gate 判定仍未通过 |
| 覆盖状态 | requirements / bugs / changes 均 pass | Fact Sheet coverage status |
| 矩阵可用性 | usage_matrices present，但不可作为真实成本矩阵输出 | Fresh gate 未通过时不能用具体数值量化成本 |
| 主要输入消耗风险 | Sprint 四件套、10 个 OpenSpec Change、archive lookup、规则/技能重复读取 | Fact Sheet `token_risks` |
| 主要输出消耗风险 | Workflow Sync、readiness、测试/校验摘要、长 JSON summary | 本次 summary 输出因矩阵较长被截断 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、分段读取、已读规则摘要复用、未展开完整 evidence_hints | 符合 `rules/agent-context-budget.md` |
| recommended_action | 刷新 sprint snapshot 后重新检查 fresh gate | `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-018 --json` |

### 矩阵输出状态

本次不输出 `total_tokens`、`input_tokens`、`output_tokens`、`model_call_count` 四张真实成本矩阵。原因是 Fact Sheet fresh gate 仍为 blocker。虽然 snapshot 文件存在且包含 usage matrices，但技能要求只有 `fresh_gate.status: pass`、`snapshot_status: present`、`ai_usage_mode: actual` 且矩阵存在时，才能按真实统计输出。

矩阵口径保留：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint four-piece | high | Fact Sheet token_risks：`sprint.md` 超 200 行 | 复盘、archive、apply 优先使用 Fact Sheet summary；只在 warnings/needs_detail 时读片段 |
| OpenSpec changes | high | Fact Sheet token_risks：10 Change，132/132 tasks | 10+ Change 必须使用 `change_batches`，避免默认读取每个 raw tasks/trace |
| Archive lookup | medium | residual_count 0；archive paths 可由 sprint.yaml change ids 解析 | 禁止宽泛扫描 `openspec/archive/**`；用 residual gate 和 fact sheet 定位 |
| AI usage summary 输出 | medium | `--summary` 输出包含完整 usage matrices，命令输出被截断 | 增加 `--summary-compact` 或 `--fields ai_usage_snapshot.fresh_gate,totals` |
| Workflow Sync / readiness 输出 | medium | Sprint archive 过程中多次运行 readiness、stale scan、sync | 成功路径只保留计数摘要；失败时按 blocker 定位文件片段 |
| UI / 小程序返修链 | high | BUG-0110 多轮验收返修覆盖 Banner、品牌列表、证书列表、分类商品列表 | 将媒体展示类 BUG 固定四联 evidence，减少每轮重新解释上下文 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认展开全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 批次化读取 | 符合 | Sprint 有 10 个 Change，优先使用 `change_batches` 摘要 |
| 输出截断 | 部分符合 | 未复制测试日志/完整 evidence_hints，但 Fact Sheet summary 自身输出过长，建议脚本瘦身 |
| 已读摘要复用 | 符合 | 复用本会话已读 `document-governance`、`directory-structure`、`iterations-lifecycle`、`agent-context-budget` 等规则摘要 |
| 需要修正 | 是 | AI usage fresh gate blocker 与 snapshot 文件状态不一致，需要专门治理 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-018-001 | P1 | 修复或增强 Fact Sheet AI usage fresh gate：snapshot 已刷新但仍 stale 时输出具体原因和自动重检建议 | `/bug-capture` | open |
| T-018-002 | P1 | 为 10+ Change Sprint 增加 compact summary，只输出批次、warning、fresh gate 和 token_risks，不默认展开 usage matrices | `/opsx-propose` | open |
| T-018-003 | P1 | 将小程序 DevTools/体验版网络面板验证纳入 release/miniapp 准备清单，避免 sprint archive 中保留普通未勾项 | `/req-capture` | open |
| T-018-004 | P2 | opsx-archive 对缺 `trace.md` 的 Change 自动生成最小归档 trace 或结构化 fallback 摘要 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0094 同时触及 release、Mintlify、截图资产、Compose profile | 文档站治理不是单纯目录新增，而是 release usage docs 事实源与公开站点投影的边界治理 | 后续文档站功能继续从 release manifest 出发，避免 `mintlify/` 反向成为事实源 |
| REQ-0093 与 REQ-0094 都改部署边界 | 两个治理需求有共享规则和 docs 触点，容易互相覆盖 | 后续类似治理需求在 proposal 阶段显式列出共享文件和写入顺序 |
| 8 个 BUG 多为展示一致性和媒体 URL 使用 | 管理端和小程序都暴露“字段存在但展示策略不一致”的问题 | 建立 UI 展示字段映射检查表：列表字段、详情字段、缩略图字段、fallback 字段分层 |
| BUG-0110 出现多轮返修 | 仅看 URL 字段不足以证明性能优化，必须确认对象存在、端上实际请求和降级策略 | 媒体类 BUG 默认使用 key/object/URL/render/performance 四联或五联验收 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | 多数 UI BUG 不需要 API 变更；BUG-0110 涉及列表 payload 瘦身和字段复用，需要明确 Orval N/A 理由 | 只要调整公开响应字段或 Schema，就同步 OpenAPI、Orval、API 文档和 tests；未调整也要记录 N/A |
| DB | 本 Sprint 主要是文档/部署治理和展示修复，未引入 DB schema 变更 | DB 变更继续走 schema、docs、tests 同步门禁 |
| Web 管理端 | 品牌、证书、SKU、类目修复都体现列表/弹窗展示一致性问题 | 继续复用 admin list/form best practices，避免单页局部样式漂移 |
| 小程序 | 返回首页、缩略图、Banner 和列表展示都需要端上行为验证 | 静态测试和 pytest 只能覆盖契约，体验版/DevTools 验证要进入发布清单 |
| Docker / 部署 | REQ-0093/0094 增加 deploy 与 docs-site profile 治理 | Docker Compose 默认业务服务不应依赖 docs-site；env 示例不得包含真实密钥 |
| Sprint archive | stale scan 与 residual gate 对关闭质量很有效 | 未勾人工验收项和缺 trace warning 应在 archive 前更早暴露 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Versioned docs projection | REQ-0094 | 将 release usage docs 到 `mintlify/docs/vX.Y.Z/` 的投影、hash、latest 指针和 manifest 校验脚本化 |
| Deploy environment matrix | REQ-0093 | 固化 local/prod env 示例、Compose profile、up/down/validate 脚本和发布镜像输入追踪 |
| Admin display cell adapters | BUG-0105 / BUG-0107 / BUG-0104 | 为管理端列表列渲染建立 image/name/status/fallback 的统一 adapter 或组件约束 |
| Miniapp media URL selector | BUG-0110 | 形成商品、品牌、证书、Banner 共用的缩略图优先和原图详情分层策略 |
| Sprint exps compact summary | 本次复盘 | `generate-sprint-fact-sheet.py --summary` 增加 compact 模式，避免 token 矩阵在 fresh gate blocker 时仍输出大量 JSON |

## 6. 行动项

| ID | 优先级 | 类型 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------|------------|------|
| T-018-001 | P1 | bug | Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致，需定位 stale 判定或 mode 映射 | `/bug-capture` | open |
| T-018-002 | P1 | workflow | 为 10+ Change Sprint 增加 compact Fact Sheet summary，避免默认输出完整 usage matrices | `/opsx-propose` | open |
| T-018-003 | P1 | requirement | 将小程序 DevTools/体验版网络面板验证纳入 release/miniapp 准备清单 | `/req-capture` | open |
| T-018-004 | P2 | workflow | archived Change 缺 `trace.md` 时自动生成最小归档 trace 或结构化 fallback 摘要 | `/opsx-propose` | open |
| T-018-005 | P2 | design-system | 管理端列表字段展示建立统一 image/name/fallback adapter 检查表 | `/req-capture` | open |

## 7. 未自动创建 Issue 的 follow-up 文案

本次 `/sprint-exps sprint-018` 未获得自动 capture 授权，因此未自动创建 Issue。以下事项可独立用于后续 capture：

1. 建议命令：`/bug-capture`
   类型倾向：BUG
   标题：Fact Sheet AI usage fresh gate 与已刷新 snapshot 状态不一致
   背景：`data/ai-usage/sprints/sprint-018.json` 已刷新并存在 usage matrices，但 `generate-sprint-fact-sheet.py --summary` 仍报告 `snapshot_status: stale` 与 `ai_usage_mode: estimated_fallback`。
   影响范围：`scripts/generate-sprint-fact-sheet.py`、`scripts/extract-ai-usage.py`、Sprint 复盘 token 成本矩阵输出。
   建议复现要点：刷新 sprint-018 snapshot 后立即运行 Fact Sheet summary，观察 fresh gate 是否仍 blocker；检查 generated_at、estimated、ai_usage_mode 映射。
   来源 Change/Sprint/命令：sprint-018 / `/sprint-exps sprint-018`。

2. 建议命令：`/req-capture`
   类型倾向：需求
   标题：为 10+ Change Sprint 增加 compact Fact Sheet summary
   背景：sprint-018 summary 在 fresh gate blocker 场景仍输出大量 usage matrices，命令输出被截断。
   影响范围：`scripts/generate-sprint-fact-sheet.py`、`sprint-exps`、`sprint-archive`、Agent 上下文预算。
   建议验收要点：新增 compact 模式或字段选择，默认只输出 Sprint 概况、batch counts、warnings、fresh gate、token_risks；完整矩阵仅 fresh gate pass 且用户需要时输出。
   来源 Change/Sprint/命令：sprint-018 / `/sprint-exps sprint-018`。

3. 建议命令：`/req-capture`
   类型倾向：需求
   标题：将小程序 DevTools/体验版网络面板验证纳入发布准备清单
   背景：BUG-0110 的端上网络面板验证无法在终端环境完成，Sprint archive 只能记录风险。
   影响范围：miniapp release/prepare、BUG-0110 类媒体展示验收、release checklist。
   建议验收要点：发布前清单能标记 DevTools/体验版验证项、验证负责人、通过/失败/豁免结论和证据入口。
   来源 Change/Sprint/命令：sprint-018 / `/sprint-exps sprint-018`。
