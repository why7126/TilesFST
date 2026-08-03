---
sprint_id: sprint-016
title: Sprint 016 迭代经验复盘
status: draft
created_at: 2026-08-01 09:37:42
updated_at: 2026-08-01 09:37:42
owner: product
related_iteration: iterations/archive/sprint-016/
source: /sprint-exps sprint-016
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 016 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 实际周期 | 2026-08-01 07:31:37 ~ 2026-08-15 18:00:00 |
| REQ / BUG / Change | 1 / 2 / 3 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 68/68 |
| 估算 | 13 SP / 13 人天 |
| 容量 | 30 人天；占用 43.33%；fix buffer 56.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；3/3 Change archived |
| AI usage | `estimated_fallback/stale`；不得按真实 token 统计展示，需刷新 snapshot |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-016 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-016 --json`、`iterations/archive/sprint-016/sprint.yaml`、`iterations/archive/sprint-016/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 管理端 SKU 列表排序 | 未上架 SKU 优先，未上架按创建时间倒序，已上架按发布时间倒序；下架后保留最近发布时间展示 |
| 公开 SKU 主图对象路径 | 修复公开主图长期停留在 `images/default/tiles/pending/...` 的问题，绑定 SKU 后归入商品目录 |
| SKU 缩略图真实生成 | `.thumb.*` 不再复制原图 bytes，支持真实缩小、历史审计与幂等再生成 |
| 媒体链路治理 | 主图路径、缩略图尺寸、对象存储、后端媒体 URL、小程序卡片渲染与审计脚本形成闭环 |

## 2. 流程复盘

### 做得好的

1. **范围小而聚焦**：3 个 Change 共同围绕 SKU 列表运营效率与媒体链路质量，容量占用 43.33%，保留了较健康的 fix buffer。
2. **媒体修复没有停在 UI 层**：BUG-0099 和 BUG-0100 同时覆盖对象 key、缩略图真实生成、历史脚本、后端受控读取和小程序渲染，避免只修表象。
3. **归档闭环补强有效**：`fix-media-thumbnail-generation` 初始缺少 archive trace，归档前补齐后 readiness 从 BLOCKED 转为 PASS，说明 gate 对历史证据缺口有实际拦截价值。
4. **路径残留检查起到了保护作用**：Sprint 文档中 active Change 路径被替换为 `openspec/archive/...`，最终 residual_count 为 0，避免复盘继续传播旧路径。
5. **复盘读取边界克制**：本次复盘优先使用 Fact Sheet summary 与 residual JSON，没有展开全部 Issue trace、Change tasks 或生成物 diff。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Sprint 关闭前四件套存在中间态文案 | `acceptance-report.md` 与 `release-note.md` 曾保留“待验收 / planned”等旧文案 | 容易让 completed/archive 的机器状态与人工阅读结论冲突 |
| 已归档 Change 缺 trace 会阻断 Sprint close | `fix-media-thumbnail-generation` archive 目录初次 readiness 报告缺 `trace.md` | 需要 `/opsx-archive` 后置 gate 确认每个归档 Change 都有 trace 或完整 fallback |
| 媒体链路存在连续缺陷 | BUG-0099 修路径，BUG-0100 修缩略图真实降尺寸 | 说明“对象存在”不足以证明媒体能力生效，验收要覆盖路径、尺寸、体积、渲染和历史数据 |
| Token snapshot 状态不够清晰 | Fact Sheet summary 显示 `estimated_fallback/stale`，即使 hook 曾返回 ok，也不能作为真实统计展示 | 复盘无法输出真实 token 矩阵，降低模型成本分析可信度 |
| Docker/依赖验证成本偏高 | 缩略图真实生成涉及 Pillow、Docker build 与容器导入验证 | 媒体能力引入依赖时，应提前准备聚焦构建验证命令和日志截断策略 |

### 优化建议

1. **把 archive trace 完整性前移**：`/opsx-archive` 成功后立即检查 archived Change 是否有 `trace.md`，没有则必须写入完整 `## 归档验证摘要`。
2. **为 Sprint close 增加中间态文案扫描**：关闭前扫描 `planned`、`pending`、`待验收`、`待实现`、active `openspec/changes/...` 等残留。
3. **媒体类验收升级为“五联”**：对象 key 归位、对象存在、URL 可访问、缩略图真实降尺寸/降体积、小程序渲染均需覆盖。
4. **Token snapshot 要求可判定 freshness**：`/sprint-exps` 前若 summary 为 stale 或 estimated fallback，先刷新或明确保留 fallback，不混用矩阵数字。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 无 | Fact Sheet summary 显示 snapshot 非真实可用状态 |
| AI usage mode | estimated_fallback | `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | stale | `ai_usage_snapshot.snapshot_status` |
| usage_matrices | 不采用 | 虽然 summary 暴露矩阵字段，但 mode/status 不满足 `actual/present`，不得按真实统计展示 |
| 主要输入消耗 | 估算：OpenSpec/Issue/Sprint 流程文档、媒体链路跨端证据、Docker/依赖验证 | 基于 token_risks 与 3 Change / 68 tasks 规模判断 |
| 主要输出消耗 | 估算：归档报告、Workflow Sync 摘要、测试/构建摘要、复盘与行动项 | 未使用具体 token 数字 |
| 重复/浪费来源 | 归档前中间态文案修正、缺 trace 后补证、媒体链路多段验证 | Fact Sheet warnings 为 0，但 Sprint close 过程暴露过这些卡点 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、已读规则摘要复用、分段读取、未展开完整 evidence_hints | 符合 `rules/agent-context-budget.md` |
| recommended_action | `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-016 --json` | 刷新后再重跑 Fact Sheet |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。当前 snapshot 为 `estimated_fallback/stale`，以下四张矩阵不填入具体数值，避免把估算数据误读为真实统计。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|---------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-----------:|-----------:|---------:|---------:|-------------:|-------------:|-----------:|-------------:|---------------:|---------------:|-------------:|---------------:|
| Total | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |
| sprint-016 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|---------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-----------:|-----------:|---------:|---------:|-------------:|-------------:|-----------:|-------------:|---------------:|---------------:|-------------:|---------------:|
| Total | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |
| sprint-016 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|---------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-----------:|-----------:|---------:|---------:|-------------:|-------------:|-----------:|-------------:|---------------:|---------------:|-------------:|---------------:|
| Total | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |
| sprint-016 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|---------:|------------:|------------:|------------:|------------:|-------------:|-------------:|-------------:|-------------:|-----------:|-----------:|---------:|---------:|-------------:|-------------:|-----------:|-------------:|---------------:|---------------:|-------------:|---------------:|
| Total | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |
| sprint-016 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 | 未采用 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec changes | medium | Fact Sheet token_risks：3 Change，68/68 tasks | 复盘继续优先使用 summary；只有 warnings/needs_detail 时回读 tasks/trace 片段 |
| Archive lookup | medium | Archive path 由 sprint.yaml change ids 解析；residual_count 0 | 使用 readiness、Fact Sheet 与 residual gate，避免宽泛扫描 `openspec/archive/**` |
| 媒体链路验证 | high | BUG-0099/BUG-0100 覆盖对象存储、后端媒体、历史脚本、小程序 | 建立媒体五联验收模板，减少每次重新推导验证面 |
| Docker/依赖日志 | medium | BUG-0100 涉及后端 Docker build 与 Pillow 导入验证 | 构建输出默认截断，只保留命令、结论、失败关键段 |
| close-time 文案修正 | medium | Sprint close 前修正 acceptance/release-note/sprint.md 中间态文案 | 沉淀 close stale scan 脚本或 Workflow Sync 检查项 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认展开全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 Fact Sheet、residual JSON、知识库索引、上期复盘样式和 Sprint 回链片段 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 需要修正 | 是 | AI usage snapshot stale 时应先刷新，否则复盘只能展示 fallback 分析 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-016-001 | P1 | 为 `/opsx-archive` 增加归档 Change `trace.md` / fallback 完整性检查，避免 Sprint close 才发现证据缺口 | `/opsx-propose` | open |
| T-016-002 | P1 | 媒体类 BUG 建立五联验收模板：对象 key、对象存在、URL 可访问、真实缩略收益、小程序渲染 | `/req-capture` | open |
| T-016-003 | P1 | `/sprint-exps` 前刷新或校验 AI usage snapshot，若不是 `actual/present` 则只输出 fallback 并提示补证 | `/opsx-propose` | open |
| T-016-004 | P2 | Sprint close 增加自然语言中间态 stale scan，覆盖 `planned`、`待验收`、active Change path 等残留 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| REQ-0087 与 BUG-0099/0100 都与运营素材效率相关 | SKU 排序和主图/缩略图质量共同影响运营发现、发布和公开展示效率 | 运营效率类 Sprint 可按“列表决策效率 + 媒体可用性”组合规划，但每条验收要能独立闭环 |
| BUG-0099 与 BUG-0100 是同一媒体链路的连续缺陷 | 先修对象 key 归位，再修缩略图真实降尺寸，说明链路验收曾只覆盖存在性 | 媒体验收应默认覆盖对象路径、内容派生、体积收益和端上渲染 |
| 管理端排序契约容易跨 API/Web/文档 | 默认排序影响后端查询、管理端展示、测试 fixture 与 API 说明 | 排序类需求在 proposal 阶段写清分组优先级、空值处理、是否新增前端控件和 Orval 是否需要同步 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | 本 Sprint 最终未新增接口字段、错误码或 DB 字段，但排序契约和媒体字段语义有文档风险 | 若后续显式化排序参数或图片响应字段，必须同步 OpenAPI、Orval、API index 和测试 |
| Object Storage / MinIO | 单 Bucket + 同目录 `.thumb` 策略适合保持公开 URL 与对象生命周期一致 | 禁止前端直连对象存储；历史迁移/审计脚本必须 dry-run、apply、幂等和安全输出 |
| Media processing | 缩略图真实生成引入图片处理依赖和 Docker 验证成本 | 媒体依赖变更要同步部署/镜像文档，并保留容器内导入验证摘要 |
| Sprint archive | readiness、promote、residual、Workflow Sync 组合能发现证据缺口和路径残留 | 关闭前必须跑完整门禁，且非 marker 文案也要人工/脚本扫描 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| SKU list ordering fixture | REQ-0087 | 建立混合上架状态、空发布时间、同组多记录的排序 fixture，后续列表排序需求直接复用 |
| Media lifecycle validator | BUG-0099 / BUG-0100 | 将 pending key、同目录 `.thumb`、对象存在、URL 可访问、缩略图尺寸/体积收益组合成一套审计输出 |
| Archive evidence gate | sprint-016 close | 在 `/opsx-archive` 后立即校验 archived Change trace/fallback，减少 `/sprint-archive` 返工 |
| Close stale scan | sprint-016 close | 对 Sprint 四件套自然语言执行中间态词扫描，结果只输出命中文件、行号和建议替换 |

## 6. 行动项

| ID | 优先级 | 类型 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------|------------|------|
| T-016-001 | P1 | workflow | archived Change trace/fallback 完整性检查前移到 `/opsx-archive` | `/opsx-propose` | open |
| T-016-002 | P1 | requirement | 媒体五联验收模板，覆盖 key、object、URL、thumbnail benefit、miniapp render | `/req-capture` | open |
| T-016-003 | P1 | workflow | AI usage snapshot fresh gate，避免 `/sprint-exps` 输出 fallback 而无法量化成本 | `/opsx-propose` | open |
| T-016-004 | P2 | workflow | Sprint close stale scan 自动检查四件套中间态文案和旧路径 | `/opsx-propose` | open |

未自动创建 Issue；以上行动项仅作为后续 capture/propose 的标准输入。

## 7. 回链

- Sprint：`iterations/archive/sprint-016/`
- 归档 Change：`openspec/archive/2026-08-01-update-admin-sku-list-sort-optimization/`、`openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/`、`openspec/archive/2026-08-01-fix-media-thumbnail-generation/`
- 相关知识：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md`、`docs/knowledge-base/incidents/media-thumbnail-copy-regression.md`
