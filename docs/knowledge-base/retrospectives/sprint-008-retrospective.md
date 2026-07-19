---
sprint_id: sprint-008
title: Sprint 008 迭代经验复盘
status: draft
created_at: 2026-07-19 15:38:56
updated_at: 2026-07-19 15:38:56
owner: product
related_iteration: iterations/archive/sprint-008/
related_requirements:
  - REQ-0039-xl-admin-page-layered-acceptance-template
  - REQ-0040-rule-skill-read-summary-reuse-context-budget
  - REQ-0041-miniapp-home
  - REQ-0042-custom-navigation-bar
  - REQ-0043-miniapp-home-style-optimization
  - REQ-0044-miniapp-sku-detail-page
  - REQ-0045-category-list-page
  - REQ-0046-search-component-application
  - REQ-0047-product-list-common-component-application
  - REQ-0048-miniapp-global-custom-navigation-bar
related_bugs:
  - BUG-0065-miniapp-home-preview-deviation
related_changes:
  - add-xl-admin-page-acceptance-template
  - update-rule-skill-summary-reuse-context-budget
  - add-miniapp-home
  - update-miniapp-home-style-optimization
  - fix-miniapp-home-preview-runtime-entry
  - add-miniapp-custom-navigation-bar
  - add-miniapp-sku-detail-page
  - add-miniapp-category-list-page
  - add-miniapp-search-component
  - add-miniapp-product-list-component
  - add-miniapp-global-custom-navigation-bar
source: /sprint-exps sprint-008
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 008 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-07-16 08:59:46 ~ 2026-07-19 15:31:45 |
| 当前状态 | completed / archive |
| REQ | 10（全部 archive） |
| BUG | 1（archive） |
| Change | 11（8 add-* + 2 update-* + 1 fix-*） |
| Change archived | 11/11；readiness 为 force-proceed |
| 估算 | 36 SP / 36.0 人天 |
| 容量 | 30 人天；占用 120%；fix buffer -20% |
| tasks 完成度 | 241/245 |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| AI usage snapshot | actual / present；coverage pass；warning_count 0 |
| 主要质量簇 | 小程序首页闭环、全局导航、SKU/分类/搜索/商品列表组件、Agent 上下文预算治理、XL 验收模板 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-008 --json`、`scripts/check-archived-path-residuals.py --sprint sprint-008 --json`、`iterations/archive/sprint-008/sprint.yaml`、`iterations/archive/sprint-008/acceptance-report.md`、`data/ai-usage/sprints/sprint-008.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 治理沉淀 | `REQ-0039` 沉淀 XL 管理端页面分层验收模板；`REQ-0040` 将规则/Skill 已读摘要复用纳入上下文预算治理 |
| 小程序首页 | `REQ-0041` 完成首页首期闭环，`REQ-0043` 继续优化深色视觉、信息架构、推荐与瀑布流 |
| 小程序导航 | `REQ-0042` 完成首页品牌自定义导航栏，`REQ-0048` 扩展为全局自定义导航 |
| 小程序商品链路 | `REQ-0044`、`REQ-0045`、`REQ-0046`、`REQ-0047` 完成 SKU 详情、分类、搜索、商品列表页面与组件链路 |
| 缺陷修复 | `BUG-0065` 修复小程序首页运行入口脱节，补充 `.ts` / `.js` 同步与空模板回归测试 |

## 2. 流程复盘

### 做得好的

1. **Sprint 007 行动项承接快**：`REQ-0039`、`REQ-0040` 直接来自上一轮复盘行动项，说明复盘已经能进入正式 Issue/Change 闭环。
2. **小程序能力从单页扩展到链路**：首页、导航、SKU 详情、分类、搜索、商品列表在同一 Sprint 中形成闭环，后续端到端验收更容易围绕真实路径组织。
3. **归档路径残留门禁有效**：归档关闭时先发现 Sprint 旧阶段路径与 active Change 路径残留，修复后 residual_count 为 0。
4. **AI usage 从 stale fallback 刷新为 actual**：Sprint close 后置 hook 成功刷新 `data/ai-usage/sprints/sprint-008.json`，复盘可使用真实统计。
5. **强制关闭保留事实边界**：本次按用户确认强制关闭，但验收报告保留了微信开发者工具/真机验收残留，没有把自动化检查冒充设备验收。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Sprint 容量明显超载 | 36.0 / 30.0 人天，容量占用 120%，fix buffer -20% | 范围冻结后仍缺少真实缓冲，任何设备验收问题都会挤压关闭质量 |
| 强制关闭带着未完成任务 | `fix-miniapp-home-preview-runtime-entry` 18/20；`add-miniapp-global-custom-navigation-bar` 15/17 | 设备/视口验收风险被转为人工 follow-up，后续必须显式追踪 |
| 小程序视觉验收依赖外部工具 | 微信开发者工具/真机、320/375/430 pt 截图验收无法由当前自动化完全替代 | 需要把“自动化覆盖”和“设备验收”拆成不同任务状态 |
| Change 数量和 tasks 数量偏高 | 11 个 Change，245 个 tasks，Fact Sheet 标记 OpenSpec changes 为 high token risk | apply/archive/exps 命令容易消耗大量上下文，需要更强摘要入口 |
| 文档派生状态容易与强制关闭语义冲突 | Workflow Sync 会刷新部分 note 与派生表格 | 强制关闭说明必须写入正文和门禁记录，避免只依赖 frontmatter note |

### 优化建议

1. **小程序设备验收建立独立 Gate**：将 DevTools/真机、320/375/430 pt、胶囊避让、TabBar 遮挡拆成可复用验收清单，并允许标记 `manual_pending`。
2. **容量超过 100% 时冻结范围更早执行**：达到 120% 时只允许 P0/P1 缺陷替换范围，不再叠加新小程序页面。
3. **强制关闭必须生成 follow-up Issue**：如果 Sprint archive 使用 force-proceed，必须自动或手动创建后续 REQ/BUG，承接未完成的人工验收。
4. **复盘继续只消费 Fact Sheet**：Sprint 008 四件套和 Change 数量都偏大，`sprint-exps` 应继续避免全文展开 trace/tasks。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-008.json`，由 Fact Sheet 暴露 |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Command run 数 | 33 | snapshot totals |
| Model call 数 | 679 | snapshot totals |
| Tool call 数 | 1345 | snapshot totals |
| Input tokens | 84,351,510 | snapshot totals |
| Cached input tokens | 80,639,872 | snapshot totals |
| Output tokens | 397,060 | snapshot totals |
| Reasoning output tokens | 38,757 | snapshot totals |
| Total tokens | 84,791,457 | snapshot totals |
| Retry count | 0 | snapshot totals |
| 主要输入消耗 | 高 | 10 个 REQ、1 个 BUG、11 个 Change、245 tasks、小程序多页面链路、归档与复盘命令 |
| 主要输出消耗 | 中 | Workflow Sync、readiness、Fact Sheet、路径残留检查、AI usage hook 与测试摘要 |
| 重复/浪费来源 | 中 | 连续命令中规则/Skill 读取、Sprint 四件套超过 200 行、归档路径核对、Change tasks 反复状态读取 |
| 已采用节省策略 | 有 | Fact Sheet 优先、残留检查脚本化、同会话规则摘要复用、只分段读取索引和样例复盘 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint 四件套 | high | Fact Sheet 标记 `sprint.md` >= 200 行 | 复盘与关闭默认消费 Fact Sheet；只在 warnings 指向具体文件时分段回读 |
| OpenSpec changes | high | 11 个 Change，241/245 tasks | 按 Change 分批处理；成功路径只输出计数、状态和 archive path |
| 小程序多页面链路 | high | 首页、导航、详情、分类、搜索、商品列表均纳入 Sprint | 对共享组件和页面接入建立统一静态测试，减少每页重复验收文字 |
| 设备/视口验收残留 | medium | 2 个 Change 共 4 个未完成 task | 将手工设备验收结果结构化为单独 evidence 文件，避免在 tasks、acceptance、trace 之间重复描述 |
| Archive lookup | medium | Fact Sheet 标记 archive lookup 风险 | 通过 `sprint.yaml` 精确解析归档目录；禁止宽泛扫描 `openspec/changes/archive/**` |
| 规则与 Skill 读取 | medium | Sprint close/exps 都要求读取 AGENTS、rules 与命令 Skill | 同一会话复用已读摘要；仅在文件变化、门禁失败或任务升级时补读 |
| Workflow Sync 输出 | medium | `sprint.archive` 更新 4 个文件，`--check` 跳过 26 个无差异文件 | 成功路径保持 summary；失败时再用 `--output detail` |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `generate-sprint-fact-sheet.py --json`，并基于 `warnings` 和 `token_risks` 决定是否回读 |
| 搜索排除 | 基本符合 | 未全文读取 `openspec/changes/archive/**`、generated、node_modules、dist；仅按报告修复过两处路径残留 |
| 分段读取 | 符合 | 只读取 sprint-007 复盘样例、知识库索引和 sprint-008 回链片段 |
| 大输出处理 | 需继续优化 | Fact Sheet 结构化但仍很长，后续可提供 `--summary` 或 `--fields` 输出 |
| 精确 token 计量 | 符合 | snapshot 为 actual/present，coverage pass，warning_count 0 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为 `generate-sprint-fact-sheet.py` 增加 summary/fields 模式，复盘默认不输出完整 evidence hints | `/opsx-propose` | open |
| T-002 | P1 | 为小程序 DevTools/真机验收建立可复用 evidence 模板，避免设备验收散落在 tasks 与 acceptance 中 | `/req-capture` | open |
| T-003 | P2 | 将 force-proceed 关闭自动生成 follow-up Issue 或至少输出标准 capture 文案 | `/opsx-propose` | open |
| T-004 | P2 | 对 10+ Change Sprint 增加分批 archive/exps 摘要，减少一次性读取 tasks 和 trace 的上下文峰值 | `/opsx-propose` | open |

## 3. 需求与设计

### 正向经验

| 条目 | 经验 |
|------|------|
| REQ-0039 | XL 管理端页面分层验收模板回应了上一 Sprint 对复杂后台能力的验收拆层需求 |
| REQ-0040 | 规则/Skill 摘要复用从口头约束进入正式治理，能直接降低后续命令成本 |
| REQ-0041 / REQ-0043 | 首页首期闭环和体验优化拆成主能力 + refinement，比在单个 Change 中塞视觉重构更清晰 |
| REQ-0042 / REQ-0048 | 首页导航与全局导航拆分，便于先验证品牌 Header，再推广到非首页返回与胶囊避让 |
| REQ-0044 ~ REQ-0047 | SKU、分类、搜索、商品列表围绕真实用户浏览链路组织，组件复用方向明确 |
| BUG-0065 | 运行入口脱节被独立 fix Change 承接，避免把缺陷混入首页需求主体 |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| 小程序设备验收证据不足 | 关闭时仍有 4 个手工验收 task 未完成 | 下一 Sprint 建立设备验收 evidence 文件，记录机型、视口、截图路径、结论和 reviewer |
| 页面链路过多 | 7 个小程序业务能力集中交付 | 后续 Sprint 以“入口 + 组件 + 页面接入 + 设备验收”分批规划 |
| 容量风险被接受但缺替换策略 | capacity_usage 120%，fix buffer -20% | Sprint propose 超过 100% 时必须写明可移出项和触发条件 |
| 强制关闭没有自动 follow-up Issue | 风险写入验收报告，但未进入 issues 队列 | 使用 `/bug-capture` 或 `/req-capture` 承接人工设备验收残留 |

## 4. 开发与质量

### 重复模式与预防

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| 小程序运行事实源漂移 | BUG-0065 | `.ts` 业务逻辑与微信开发者工具实际加载 `.js` 可能脱节 | 保留关键页面 `.js` 非空模板静态测试，并在新增页面时同步 runtime 策略 |
| 固定导航遮挡风险 | REQ-0042、REQ-0048 | 自定义导航、状态栏、原生胶囊和页面主体 spacing 同时参与布局 | 建立统一 `custom-navigation` offset 和 320/375/430 pt 验收矩阵 |
| 页面组件边界重叠 | REQ-0045、REQ-0046、REQ-0047 | 分类、搜索和商品列表都可能承接筛选、排序、分页、跳转 | 明确分类页只管分类结构，搜索组件只管搜索语义，商品列表组件只管列表状态机 |
| 强制关闭风险外溢 | fix 和 global navigation Change | 手工设备验收无法在当前环境完成 | 强制关闭后必须在复盘行动项中形成 follow-up，避免风险在文档中沉睡 |
| Token 成本随 Sprint 范围线性放大 | 11 Change / 245 tasks | 每个命令都可能读取任务、trace、acceptance、sync 输出 | 用 Fact Sheet 聚合、命令 summary 和按 warning 回读替代全文展开 |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 工具链 | `REQ-0040` 覆盖上下文预算规则、Skill Guardrails、校验脚本和测试 |
| 小程序静态测试 | 首页运行入口、关键页面 `.js` 非空、全局导航组件接入和禁止伪系统控件已覆盖 |
| 后端 / API / DB | 小程序首页、详情、分类、搜索等能力涉及后端契约与公开字段过滤，需继续保持 OpenAPI/Orval 同步 |
| UI / 设备验收 | 自动化无法完全替代微信开发者工具/真机，当前遗留项集中在视口和胶囊避让 |
| 归档校验 | 残留路径检查 PASS；Workflow Sync `--check` PASS；AI usage hook actual/present |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| 小程序 `custom-navigation` | 首页形态与非首页形态已统一，支持返回兜底和胶囊避让计算 | 抽象设备验收矩阵，沉淀为 miniapp navigation best-practice |
| 搜索入口与搜索结果 | `REQ-0046` 建立搜索入口、联想、结果、筛选和无结果状态 | 与商品列表组件共享筛选、排序、分页状态机 |
| 商品列表组件 | `REQ-0047` 建立商品卡片、分页加载、空/错/无更多状态 | 分类、搜索、品牌、推荐入口复用统一参数和埋点 |
| 小程序运行入口静态测试 | `BUG-0065` 形成 `.ts` / `.js` 漂移检测 | 所有新增小程序页面默认加入 runtime entry 检查 |
| Sprint Fact Sheet | 本次复盘依赖结构化 scope、warnings、token_risks、AI usage | 增加 summary 模式，减少复盘命令的结构化输出体积 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P1 | 为 Sprint 008 遗留的微信开发者工具/真机验收建立 follow-up Issue，覆盖首页预览、320-430 pt、胶囊避让和内容不遮挡 | `/bug-capture` | 测试 + 小程序 | open |
| A-002 | P1 | 为小程序自定义导航沉淀 best-practice，明确状态栏、胶囊、返回兜底、页面 offset 和截图验收矩阵 | `/req-capture` | 小程序 | open |
| A-003 | P1 | 为 force-proceed archive 建立自动 follow-up 提示或 Issue 生成机制，避免未完成 task 只停留在验收报告 | `/opsx-propose` | 工具链 | open |
| A-004 | P2 | 为 10+ Change Sprint 增加 Fact Sheet summary/fields 输出，降低 `/sprint-exps` 和 `/sprint-archive` 上下文峰值 | `/opsx-propose` | 工具链 | open |
| A-005 | P2 | 将分类、搜索、商品列表组件的边界和共享状态机整理为下一轮小程序组件治理需求 | `/sprint-propose` | 产品 + 小程序 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-008-retrospective.md` | 新建 | 本文档 |
| `incidents/miniapp-runtime-entry-drift.md` | 沿用 | BUG-0065 已沉淀运行入口漂移经验 |
| `retrospectives/sprint-007-retrospective.md` | 承接 | `REQ-0039`、`REQ-0040` 已承接上一 Sprint 行动项 |
| `best-practices/admin-list-page-consistency.md` | 沿用 | XL 管理端页面验收模板继续引用管理端横切 gate |
| `best-practices/admin-media-upload-chain.md` | 沿用 | 后续涉及媒体上传的小程序/管理端能力继续复用安全边界 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-07-19 15:38:56 | 初稿（`/sprint-exps sprint-008`） |
