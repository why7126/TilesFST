---
sprint_id: sprint-009
title: Sprint 009 迭代经验复盘
status: draft
created_at: 2026-07-20 23:33:49
updated_at: 2026-07-20 23:33:49
owner: product
related_iteration: iterations/archive/sprint-009/
source: /sprint-exps sprint-009
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 009 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-07-31 09:00:00 ~ 2026-08-14 18:00:00 |
| REQ / BUG / Change | 14 / 4 / 18 |
| Change 批次 | 4 批；5、5、5、3 个 Change |
| tasks 完成度 | 351/351 |
| 估算 | 36 SP / 36.0 人天 |
| 容量 | 30 人天；占用 120%；fix buffer -20% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；18/18 Change archived，trace present |
| AI usage | Fact Sheet summary 标记 `estimated_fallback/stale`，snapshot 文件 `estimated=false` 且存在 totals；本复盘按“不稳定统计”处理 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-009 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-009 --json`、`iterations/archive/sprint-009/sprint.yaml`、`iterations/archive/sprint-009/acceptance-report.md`、`data/ai-usage/sprints/sprint-009.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 小程序商品浏览 | 商品卡片、商品列表双列布局、分类入口、搜索原型对齐、首页推荐入口修复、SKU 视频 URL 修复 |
| 小程序品牌链路 | 品牌卡片、品牌列表页、品牌详情页、品牌轮播、品牌入口与品牌相关跳转 |
| 小程序证书与收藏 | 证书列表页、收藏列表页、品牌详情证书 Tab 和用户侧回访能力 |
| 小程序导航与设备证据 | brand-header 标题规则、自定义导航 best-practice、设备 evidence 模板、首页设备验收残留闭环、添加到我的小程序引导 |
| 管理端与媒体治理 | 品牌证书通用组件、Banner 投放范围收敛、media-upload/admin-list/admin-modal 横切验收继续复用 |

## 2. 流程复盘

### 做得好的

1. **Sprint 008 经验被快速承接**：小程序运行事实源漂移、设备验收、固定导航遮挡、路径残留检查都进入了 Sprint 009 的 Scope 与横切清单。
2. **Change 全量归档闭环**：18 个 Change 全部 archived，最终 readiness 为 PASS，351 个 task 全部完成。
3. **路径残留门禁有效**：归档关闭后检查 262 个文件，residual_count 为 0，避免新复盘继续传播旧 active 路径。
4. **小程序页面链路形成品牌/证书/收藏闭环**：品牌列表、品牌详情、证书列表、收藏列表与 SKU 详情、商品列表相互承接，用户浏览路径更完整。
5. **设备 evidence 边界比上一轮更清楚**：对 DevTools 不可运行的情况，最终使用静态视口 evidence 和 follow_up，不再把静态测试写成真机或 DevTools 截图通过。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Sprint 范围过大 | 18 个 Change、351 tasks、36.0/30.0 人天 | apply/archive/exps 都容易接近上下文和质量边界 |
| 容量到 120% 边界 | capacity_usage 1.2，fix buffer -20% | 后期靠补证据和强制关闭推进，验收余量很薄 |
| 设备验收仍依赖人工工具 | 品牌列表与添加引导语需要 320/375/430 pt evidence，当前环境无微信开发者工具截图能力 | 容易在 archive readiness 上卡住，或迫使 evidence 改为静态替代 |
| 文档状态与事实一度不一致 | 部分 acceptance 表述仍显示“待实现与验收”，但 Change 已 archived | Workflow Sync 能更新派生状态，但正文验收结论仍需要人为补齐语义 |
| AI usage 统计视图不一致 | Fact Sheet summary 标记 `estimated_fallback/stale`，snapshot 文件又显示 `estimated=false` | 复盘无法把 token totals 无条件作为真实统计，需要修复生成脚本口径 |

### 优化建议

1. **20+ 页面/组件级 Sprint 拆成两个迭代**：品牌/证书/收藏链路与后台 Banner/证书组件最好分开，避免管理端和小程序验收互相挤压。
2. **设备 evidence 任务前置到 apply 阶段中段**：不要等 archive readiness 才补 320/375/430 pt evidence；没有 DevTools 时应提前生成 `blocked/follow_up/static_review` 记录。
3. **验收报告正文纳入 Workflow Sync 或专门校验**：Scope 表可自动同步，但 acceptance-report 的“待实现”句子需要规则或脚本扫描。
4. **AI usage summary 口径统一**：`generate-sprint-fact-sheet.py --summary` 应把 `estimated=false`、actual hook、warning 字段一致化。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 不稳定 | `data/ai-usage/sprints/sprint-009.json` 有 totals 且 `estimated=false`；但 Fact Sheet summary 标记 `estimated_fallback/stale` |
| AI usage mode | estimated_fallback（按 Fact Sheet summary） | 复盘遵守 summary 门禁，不把 totals 无条件声明为真实统计 |
| Snapshot status | stale（按 Fact Sheet summary） | summary recommended_action 要求用 session JSONL 刷新 |
| Snapshot file totals | 有 | 文件中存在 input、cached input、output、reasoning、total、command/model/tool call 等 totals |
| 主要输入消耗 | high | 14 REQ、4 BUG、18 Change、351 tasks、四件套中 `sprint.md` 372 行 |
| 主要输出消耗 | high | readiness、Fact Sheet、Workflow Sync、路径残留、测试日志、归档报告、复盘报告 |
| 重复/浪费来源 | medium | 多次运行 archive/readiness/fact-sheet；全量目标测试输出出现 51 passed / 1 failed 的长日志 |
| 已采用节省策略 | 有 | 先 summary、按 warning 决定是否回读、残留检查脚本化、focused tests、成功路径只输出摘要 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Sprint 四件套 | high | Fact Sheet token_risks：`sprint.md` >= 200 行 | 复盘继续只读 summary；正文只在需要回链时读尾部片段 |
| OpenSpec changes | high | 18 个 Change，351/351 tasks | 10+ Change 强制使用 batch summary；禁止逐个读 tasks/trace |
| Archive lookup | medium | Fact Sheet token_risks 标记 archive lookup 风险 | 只通过 `sprint.yaml` change ids 解析 archive path，禁止宽泛扫 archive |
| 设备 evidence 补录 | medium | 品牌列表和添加引导语在 archive readiness 前仍有 7 个未完成 evidence task | apply 阶段要求 evidence 文件先落盘；archive 只校验，不补写大段说明 |
| 测试日志 | medium | 全量目标测试 52 项输出较长，且有一个无关失败 | 成功路径跑 focused tests；全量失败只摘失败用例、不要复制完整日志 |
| AI usage 生成口径 | medium | summary 与 snapshot 文件字段不一致 | 增加 `test_generate_sprint_fact_sheet` 覆盖 `estimated=false` 与 actual mode 判定 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，未默认读完整 evidence hints |
| 大 Sprint 批次化 | 符合 | 18 Change 使用 4 个 batch 摘要，未逐个展开原始 tasks |
| 路径残留检查 | 符合 | 使用 `check-archived-path-residuals.py --json`，未传播旧 active 路径 |
| 测试输出控制 | 部分符合 | focused tests 输出紧凑；全量测试失败输出仍偏长，后续应先按失败摘要处理 |
| 规则摘要复用 | 符合 | 同会话已读规则/Skill 未重复全量展开，复盘只补读 sprint-exps 技能和索引 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 修复 Fact Sheet AI usage summary 与 snapshot 文件实际字段不一致的问题 | `/bug-capture` | open |
| T-002 | P1 | 为小程序设备 evidence 增加标准状态枚举：`devtools_pass`、`static_pass_devtools_unavailable`、`real_device_follow_up` | `/req-capture` | open |
| T-003 | P2 | 对 10+ Change Sprint 的 archive/exps 默认只输出 batch summary，失败时再读具体 evidence hints | `/opsx-propose` | open |
| T-004 | P2 | 全量 pytest 失败时只输出失败用例摘要与重试命令，避免长日志进入复盘上下文 | `/opsx-propose` | open |

## 3. 需求与设计

| 条目 | 经验 |
|------|------|
| REQ-0052 / REQ-0053 | 将设备 evidence 模板和自定义导航 best-practice 单独成 Change，使后续页面能复用验收语言 |
| REQ-0054 / REQ-0060 / REQ-0058 | 品牌卡片、品牌列表、品牌详情页拆分合理，避免单个品牌能力过大 |
| REQ-0056 / REQ-0051 | 商品列表页展示策略和分类入口参数拆分，降低分类页与列表页职责混淆 |
| REQ-0062 | Banner 投放范围收敛到小程序首页轮播与品牌列表页轮播，减少运营位历史包袱 |
| BUG-0067 / BUG-0069 | 首页推荐入口和 SKU 视频 URL 都是边界明确的行为性缺陷，适合独立 fix Change |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| 首期范围过密 | 同时做品牌、证书、收藏、Banner、搜索、分类、导航和设备治理 | 下一 Sprint 按“端侧体验”和“管理端治理”拆分 |
| 手工设备 evidence 被动补录 | Archive readiness 前仍有 evidence task 未完成 | apply 中段加入 evidence 文件检查；缺 DevTools 时立即标 static/follow_up |
| 验收语义过度依赖正文人工维护 | acceptance-report 曾出现已归档但仍写“待实现” | 增加验收报告 stale phrase 检查 |
| API/Orval 影响判定滞后 | `add-brand-list-page` 1.4 在归档后才补证据引用 | tasks 中的 “If API changes” 应要求写明确结论：changed / not_applicable |

## 4. 开发与质量

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| 小程序运行事实源漂移 | BUG-0067、多个小程序页面 | 微信开发者工具实际加载 `.js`，而源码维护 `.ts` | 继续保留 runtime entry 静态测试，新页面默认加入 `.js` 非空与 `.ts` 对齐检查 |
| 自定义导航和胶囊遮挡 | REQ-0050、REQ-0053、REQ-0060、REQ-0061 | fixed header、状态栏、胶囊 reserve 和首屏内容耦合 | 使用统一 `custom-navigation`，并把 320/375/430 pt evidence 标准化 |
| 页面职责边界重叠 | 分类、搜索、商品列表、品牌列表 | 多入口都可能承接筛选、排序、列表容器和埋点 | 需求设计阶段写清“入口页 / 列表容器 / 搜索页 / 详情页”职责 |
| 管理端横切 AC 复用 | REQ-0055、REQ-0062 | admin-list/admin-modal/media-upload 反复出现 | 继续引用 best-practice，不在每个 Change 重写完整规则 |
| Archive 后补证据 | REQ-0060、REQ-0061 | 验收工具不可用导致 task 卡在最后 | 强制要求证据文件在 apply 阶段存在，archive 不负责补业务证据 |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 小程序静态测试 | 覆盖路由、TabBar、运行入口、品牌列表、添加引导语、自定义导航、搜索、分类、商品列表、证书和收藏 |
| 后端 miniapp API | 覆盖公开品牌列表、品牌轮播、证书列表、SKU 视频 URL、公开字段过滤与 usage event 字典 |
| 管理端回归 | Banner 与品牌证书涉及 admin-list/admin-modal/media-upload，已有专项测试与 best-practice 承接 |
| 设备验收 | 仍无法由当前环境自动运行 DevTools/真机，需继续人工或工具化补强 |
| 归档质量 | readiness PASS、Workflow Sync Errors 0、promote issues 无待迁移、residual_count 0 |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| 小程序设备 evidence 模板 | REQ-0052 已沉淀模板，Sprint 009 实际用于品牌列表和添加引导语补证据 | 将状态枚举和必填字段做成校验脚本 |
| 小程序自定义导航 | REQ-0053 与多页面接入形成统一导航模式 | 建立页面级 matrix：home/subpage/tabbar/detail/share-entry |
| 品牌组件链路 | brand-card、brand-list、brand-detail 能组合复用 | 后续品牌商品列表和品牌证书展示继续复用卡片与埋点上下文 |
| 公开 API 安全过滤 | miniapp brands/certificates/products/skus 均强调不暴露 raw object key、内部备注和敏感字段 | 抽出公开响应字段过滤测试 helper |
| Sprint Fact Sheet | 支持 scope、batch、warnings、token_risks、residuals | 修复 AI usage mode 判断，并扩大 summary/fields 测试覆盖 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P1 | 修复 `generate-sprint-fact-sheet.py --summary` 对 AI usage actual/estimated 的判定口径，避免复盘误报 | `/bug-capture` | 工具链 | open |
| A-002 | P1 | 建立小程序设备 evidence 状态枚举和校验脚本，覆盖 DevTools 不可用、静态替代、真机 follow_up 等状态 | `/req-capture` | 小程序 + 测试 | open |
| A-003 | P1 | 下一 Sprint 容量超过 100% 时必须列出可移出项；达到 120% 不允许净新增范围，只允许替换 | `/sprint-propose` | 产品 | open |
| A-004 | P2 | 为验收报告增加 stale phrase 检查，识别已 archived 但正文仍写“待实现/待验收”的行 | `/opsx-propose` | 工具链 | open |
| A-005 | P2 | 将公开 API 字段过滤沉淀成共享测试 helper，减少品牌/证书/SKU/商品重复断言 | `/req-capture` | 后端 | open |
| A-006 | P2 | 对 full pytest 失败输出做摘要策略：先 focused tests，再只记录失败用例与关键断言 | `/opsx-propose` | 测试治理 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `docs/knowledge-base/retrospectives/sprint-009-retrospective.md` | 新建 | 本文档 |
| `docs/knowledge-base/README.md` | 更新 | 增加 sprint-009 复盘索引 |
| `iterations/archive/sprint-009/sprint.md` | 更新 | 增加复盘回链 |

