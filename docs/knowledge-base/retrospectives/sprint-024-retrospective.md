---
title: sprint-024 复盘
purpose: 复盘 sprint-024 的流程、需求、开发质量、可复用抽象与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-024
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-21 14:51:53
updated_at: 2026-08-21 14:51:53
---

# sprint-024 复盘

## 概况

sprint-024 已完成归档，目录为 `iterations/archive/sprint-024/`。本 Sprint 覆盖 2 个 BUG、5 个 OpenSpec Change，37/37 个任务完成，验收状态为 passed。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 治理质量学习应用 | `apply-moonbox-governance-quality-learnings`、`apply-deepseek-harness-doc-governance-learnings` | 跨项目 Harness 学习可以沉淀 root-cause evidence、文档事实唯一归属、命令复盘和防御性模板，但仍应以 Change、Sprint 和验证脚本闭环 |
| 命令体验治理 | `default-review-approve-command` | 高频正向评审命令适合默认 approve，但反向结果仍需显式 flag，避免误拒绝或误驳回 |
| 小程序公开展示缺陷 | BUG-0130 | 公开 Banner DTO 与小程序兜底展示必须净化内部标题，且无跳转点击不能暴露后台建设状态 |
| 小程序详情页媒体体验 | BUG-0131 | 商品详情页应区分详情高清展示 URL、预览 URL 与列表 `.thumb` 性能 URL，并用高度与首屏信息露出断言防止视觉回退 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 0 |
| bugs | 2 |
| changes | 5 |
| tasks | 37/37 |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | pass |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-024 --json` 报告 `residual_count=0`。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| Sprint 收尾 | `/sprint-archive` 后 Sprint 迁入 `iterations/archive/sprint-024/`，readiness、stale scan、residual gate 全部通过 | Sprint close 前先用 Fact Sheet 定位状态，再修正人写说明区旧状态，最后跑 Workflow Sync 和 AI Usage Hook |
| 归档证据 | 5 个 Change 均已 archived 且 trace.md present | Sprint 复盘默认无需展开全部 archived tasks/trace，只引用聚合计数和归档路径 |
| Issue 闭环 | BUG-0130、BUG-0131 均位于 `issues/bugs/archive/` 且 trace 状态 done | 媒体类 BUG 的验收状态要同时同步到 `acceptance.md` 与 trace 变更记录，避免 close stale scan 误判 |
| 治理命令演进 | `default-review-approve-command` 将正向 review 默认值写入规则、技能与治理日志 | 命令体验优化也要走 OpenSpec Change，不应绕过 Sprint Inclusion Gate |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| 中间态文案残留 | Sprint close 初次 readiness 命中 `待 /opsx-apply`、`pending`、`blocked`、`待实现` 等旧语义 | Workflow Sync 派生状态正确，但人写验收表和 BUG acceptance/trace 仍保留过程描述 | `/sprint-archive` 前必须跑 stale scan；历史过程记录要改为“后续已归档闭环”或转为发布前补证建议 |
| 归档路径预写 | BUG Change proposal 仍引用 `iterations/change/sprint-024/` | Change 先归档于 Sprint close 前，proposal 中的 Sprint 路径没有随 Sprint 目录迁移自动刷新 | Sprint close residual gate 后统一将 Sprint 证据链接指向 `iterations/archive/<sprint>/` |
| Git 跟踪状态 | `sprint-024` 四件套在当前工作区表现为未跟踪路径，`git mv` 无法记录重命名 | 归档前相关 Sprint 文件未进入 Git index，普通迁移只能移动工作区文件 | 关闭 Sprint 后用 `git status --short` 聚焦复核归档目录，提交前再运行 `/git-check` |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-024.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Matrix write gate | pass | 必须 fresh gate pass、actual/present 且矩阵存在才可输出真实矩阵 |
| Freshness baseline | 2026-08-21T06:44:50Z | 来源：`acceptance-report.md:updated_at`；跳过 `sprint.yaml:end_date=2026-08-21 18:00:00`（future-planned-time） |
| Generated at | 2026-08-21T06:45:11.378629Z | `data/ai-usage/sprints/sprint-024.json` |
| command_run_count | 25 | snapshot totals |
| model_call_count | 363 | snapshot totals |
| tool_call_count | 755 | snapshot totals |
| input_tokens | 46,620,888 | snapshot totals |
| cached_input_tokens | 44,548,096 | snapshot totals |
| output_tokens | 195,323 | snapshot totals |
| reasoning_output_tokens | 12,868 | snapshot totals |
| total_tokens | 46,918,937 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 4 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 1663897 | 0 | 0 | 0 | 0 | 3025253 | 0 | 2771116 | 0 | 1896679 | 0 | 5620470 | 0 | 0 | 15365393 | 4545553 | 6203431 | 3793388 | 0 | 0 | 2033757 |
| sprint-024 | 0 | 1663897 | 0 | 0 | 0 | 0 | 3025253 | 0 | 2771116 | 0 | 1896679 | 0 | 5620470 | 0 | 0 | 15365393 | 4545553 | 6203431 | 3793388 | 0 | 0 | 2033757 |
| BUG-0130-miniapp-home-no-jump-banner-internal-title | 0 | 568701 | 0 | 0 | 0 | 0 | 1003474 | 0 | 999227 | 0 | 1101935 | 0 | 3040600 | 0 | 0 | 1611738 | 4545553 | 1226239 | 2231625 | 0 | 0 | 0 |
| BUG-0131-miniapp-sku-detail-carousel-original-image-height | 0 | 1095196 | 0 | 0 | 0 | 0 | 2021779 | 0 | 1771889 | 0 | 794744 | 0 | 2579870 | 0 | 0 | 4838313 | 0 | 1109984 | 1561763 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 1657306 | 0 | 0 | 0 | 0 | 3017466 | 0 | 2759759 | 0 | 1866838 | 0 | 5600209 | 0 | 0 | 15223645 | 4529462 | 6161053 | 3781006 | 0 | 0 | 2024144 |
| sprint-024 | 0 | 1657306 | 0 | 0 | 0 | 0 | 3017466 | 0 | 2759759 | 0 | 1866838 | 0 | 5600209 | 0 | 0 | 15223645 | 4529462 | 6161053 | 3781006 | 0 | 0 | 2024144 |
| BUG-0130-miniapp-home-no-jump-banner-internal-title | 0 | 565500 | 0 | 0 | 0 | 0 | 1000166 | 0 | 994029 | 0 | 1098811 | 0 | 3031498 | 0 | 0 | 1573679 | 4529462 | 1194185 | 2226736 | 0 | 0 | 0 |
| BUG-0131-miniapp-sku-detail-carousel-original-image-height | 0 | 1091806 | 0 | 0 | 0 | 0 | 2017300 | 0 | 1765730 | 0 | 768027 | 0 | 2568711 | 0 | 0 | 4824295 | 0 | 1105919 | 1554270 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 6591 | 0 | 0 | 0 | 0 | 7787 | 0 | 11357 | 0 | 5678 | 0 | 20261 | 0 | 0 | 90625 | 16091 | 14938 | 12382 | 0 | 0 | 9613 |
| sprint-024 | 0 | 6591 | 0 | 0 | 0 | 0 | 7787 | 0 | 11357 | 0 | 5678 | 0 | 20261 | 0 | 0 | 90625 | 16091 | 14938 | 12382 | 0 | 0 | 9613 |
| BUG-0130-miniapp-home-no-jump-banner-internal-title | 0 | 3201 | 0 | 0 | 0 | 0 | 3308 | 0 | 5198 | 0 | 3124 | 0 | 9102 | 0 | 0 | 11437 | 16091 | 4614 | 4889 | 0 | 0 | 0 |
| BUG-0131-miniapp-sku-detail-carousel-original-image-height | 0 | 3390 | 0 | 0 | 0 | 0 | 4479 | 0 | 6159 | 0 | 2554 | 0 | 11159 | 0 | 0 | 14018 | 0 | 4065 | 7493 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 13 | 0 | 0 | 0 | 0 | 18 | 0 | 15 | 0 | 13 | 0 | 33 | 0 | 0 | 133 | 24 | 60 | 30 | 0 | 0 | 24 |
| sprint-024 | 0 | 13 | 0 | 0 | 0 | 0 | 18 | 0 | 15 | 0 | 13 | 0 | 33 | 0 | 0 | 133 | 24 | 60 | 30 | 0 | 0 | 24 |
| BUG-0130-miniapp-home-no-jump-banner-internal-title | 0 | 6 | 0 | 0 | 0 | 0 | 8 | 0 | 7 | 0 | 7 | 0 | 14 | 0 | 0 | 21 | 24 | 17 | 12 | 0 | 0 | 0 |
| BUG-0131-miniapp-sku-detail-carousel-original-image-height | 0 | 7 | 0 | 0 | 0 | 0 | 10 | 0 | 8 | 0 | 6 | 0 | 19 | 0 | 0 | 24 | 0 | 14 | 18 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| OpenSpec apply | high | `Opsx-Apply` 15,365,393 total tokens，133 次模型调用 | 小程序媒体 BUG apply 时优先读取目标页面、服务和测试片段；避免同时展开所有 archived Change |
| OpenSpec archive | medium | `Opsx-Archive` 6,203,431 total tokens，60 次模型调用 | 归档前使用 readiness、language、directory、evidence gate 聚合；成功路径只输出摘要 |
| BUG opsx | medium | `BUG-Opsx` 5,620,470 total tokens，33 次模型调用 | BUG trace 已有单一 linked Change 时复用摘要，不重复读取完整 bug.md/root-cause/acceptance |
| OpenSpec modify | medium | BUG-0130 验收返修产生 `Opsx-Modify` 4,545,553 total tokens | 返修只读失败截图、相关样式/交互文件和验收条目，不回读完整 Sprint 四件套 |
| Sprint propose / archive | medium | `Sprint-Propose` 3,793,388；`Sprint-Archive` 2,033,757 total tokens | Sprint 命令优先 Fact Sheet summary、stale/residual 聚合报告和 focused git status |
| 归档查证 | medium | 5 Change、37/37 tasks；Fact Sheet 标记 OpenSpec changes 风险 medium | 默认使用 summary；只有 warning/blocker 时读取 evidence hints |

已采用的节省策略：

| 策略 | 结果 |
|------|------|
| Fact Sheet summary 优先 | 未展开 5 个 archived Change 的 raw tasks/trace |
| residual/stale gate 聚合 | 通过脚本确认 51 个范围文件无旧路径残留 |
| 分段读取 | 只在修复 stale 文案、索引和回链时读取命中片段 |
| 矩阵专用渲染 | 使用 `--ai-usage-markdown` 写入表格，避免手工读取原始矩阵 JSON |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| 公开字段净化 | BUG-0130 暴露无跳转 Banner 内部标题，说明后台素材标题和公开展示标题必须明确边界 | Banner DTO、toast、分享摘要、埋点摘要均应视为公开面，不能默认复用内部标题 |
| 无跳转点击兜底 | BUG-0130 返修要求点击保持静默，不展示“内容建设中” | 无跳转内容不是待建设内容，端侧 fallback 应区分 silent、toast、navigate 三类策略 |
| 详情页媒体 URL | BUG-0131 要求详情大图使用原图或详情级高清图，列表仍保持 `.thumb` | 媒体字段需要按展示场景命名和测试：detail display、preview、list thumbnail 不能混用 |
| 首屏高度设计 | BUG-0131 同时要求轮播更适合瓷砖展示且商品信息仍露出 | 媒体高度调整必须绑定关键视口和首屏信息露出断言，不只看单一截图 |
| 治理学习应用 | 两个学习 Change 强化根因证据、文档表达卫生、命令复盘和防御性模板 | 跨项目学习适合沉淀为治理资产，但应用结果必须接受当前项目目录、语言和验证规则约束 |

## 开发质量复盘

| 维度 | 做得好的点 | 待改进点 |
|------|------------|----------|
| 小程序媒体 | BUG-0131 同时保护详情高清、预览高清和列表 `.thumb` 性能边界 | 发布前仍建议补 DevTools、真机或体验版 render evidence，减少仅靠静态断言闭环的风险 |
| 公开展示 | BUG-0130 覆盖后端 DTO 净化和小程序端防御逻辑 | 后续 Banner 类功能应在 API schema 或测试中显式标注 public/private 字段 |
| 验收返修 | BUG-0130 返修移除 Banner 渐变遮罩、图片透明化和无跳转占位提示 | UI/视觉返修应优先保留截图对照或 computed style 证据，避免只凭文字描述验收 |
| 治理脚本 | stale scan、residual gate、AI usage fresh gate 均在 Sprint close 中发挥作用 | 人写说明区仍会漂移，需把常见旧状态词转为更明确的建议替换语义 |
| Git/工作区 | Sprint 归档命令只处理 Sprint scope，仓库可能同时存在其他待提交变更 | 提交前需要 `/git-check` 或 focused status，避免把运行时数据、未跟踪大文件或无关改动混入 |

## 可复用抽象

| 抽象 | 来源 | 建议 |
|------|------|------|
| PublicBannerTextSanitizer | BUG-0130 | 后端公开 Banner DTO 明确输出展示标题；小程序端对 `internal-*` 或空标题做静默兜底 |
| MiniappBannerClickPolicy | BUG-0130 | 小程序 Banner 点击策略区分 `navigate`、`silent`、`toast`，无跳转 Banner 默认 silent |
| MiniappSkuMediaUrlContract | BUG-0131 | SKU 媒体字段区分 `detail_display_url`、`preview_url`、`thumbnail_url` 或等价语义，并覆盖列表性能回归 |
| TileDetailHeroViewportContract | BUG-0131 | 商品详情媒体高度按 320/375/430px 逻辑宽度断言，同时保证商品名称或关键价格信息首屏可见 |
| GovernanceDecisionRecord | deepseek/moonbox 学习应用 | 治理日志记录采纳原因、未采纳原因、替代方案、验证责任和触发条件 |

## 行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为公开 Banner DTO 建立 public/private 字段净化契约，覆盖标题、跳转、toast、分享和埋点摘要 | `/req-capture` | open |
| T-002 | P1 | 将 SKU 媒体 URL 语义沉淀为小程序媒体字段契约，明确详情展示、预览、列表缩略图三类 URL 的测试边界 | `/req-capture` | open |
| T-003 | P2 | 为小程序详情页 Hero 媒体高度建立视口矩阵和首屏信息露出验收模板 | `/req-capture` | open |
| T-004 | P2 | 将 Sprint close stale scan 的常见旧状态词转为更具体的建议替换语义，减少归档前人工判断成本 | `/opsx-propose` | open |
| T-005 | P2 | 对高 token 的 `opsx.apply` 增加媒体类 BUG summary-first 清单，限制默认读取范围和测试日志输出 | `/opsx-propose` | open |

## Follow-up Capture 建议

未自动创建 Issue。建议后续按团队优先级选择 capture：

1. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：建立公开 Banner DTO 字段净化契约
   背景：BUG-0130 暴露无跳转 Banner 内部标题，并在返修中要求无跳转点击保持静默。
   影响范围：后端 Banner DTO、小程序首页轮播、品牌列表页轮播、分享/埋点摘要、测试 helper。
   建议验收要点：公开 DTO 不输出内部标题；无跳转 Banner 点击 silent；toast、分享、埋点不暴露后台内部字段；后台管理端仍保留内部标题维护能力。
   来源 Change/Sprint/命令：BUG-0130 / `fix-miniapp-home-no-jump-banner-internal-title` / sprint-024 / `/sprint-exps sprint-024`

2. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：沉淀小程序 SKU 媒体 URL 语义契约
   背景：BUG-0131 修复要求详情页展示高清图、预览高清图和列表 `.thumb` 性能策略同时成立。
   影响范围：后端 SKU 详情/列表接口、小程序商品详情页、商品列表页、媒体四联验收模板。
   建议验收要点：详情大图不使用小尺寸 `.thumb`；预览保持高清；列表/卡片/推荐位/Banner 继续使用 `.thumb`；关键视口下首屏商品信息可见。
   来源 Change/Sprint/命令：BUG-0131 / `fix-miniapp-sku-detail-carousel-original-image-height` / sprint-024 / `/sprint-exps sprint-024`

3. 建议命令：`/opsx-propose`
   类型倾向：治理 Change
   标题：强化 Sprint close stale scan 建议替换语义
   背景：sprint-024 close 前 stale scan 命中 BUG acceptance 和 trace 中的中间态文案，需要人工判断替换为归档后事实。
   影响范围：`scripts/check-sprint-close-stale-scan.py`、`scripts/validate-sprint-archive-readiness.py`、`sprint-archive` 技能说明。
   建议验收要点：报告展示命中词、当前生命周期事实、建议替换语义；不要求手工编辑 workflow-sync marker blocks。
   来源 Change/Sprint/命令：sprint-024 / `/sprint-archive sprint-024` / `/sprint-exps sprint-024`
