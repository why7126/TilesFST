---
sprint_id: sprint-008
title: Sprint 008 迭代经验复盘
status: draft
created_at: 2026-07-19 15:38:56
updated_at: 2026-07-22 12:13:05
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
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-008.json`，由修复后的 Sprint scope 聚合生成 |
| AI usage mode | actual | snapshot 字段 `ai_usage_mode` |
| Snapshot status | present | snapshot 字段 `snapshot_status` |
| Command run 数 | 95 | snapshot totals |
| Model call 数 | 1,466 | snapshot totals |
| Tool call 数 | 2,955 | snapshot totals |
| Input tokens | 178,529,286 | snapshot totals |
| Cached input tokens | 170,055,424 | snapshot totals |
| Output tokens | 876,075 | snapshot totals |
| Reasoning output tokens | 78,177 | snapshot totals |
| Total tokens | 179,489,249 | snapshot totals |
| Retry count | 0 | snapshot totals |
| 非零命令列 | `BUG-Capture`、`REQ-Capture`、`REQ-Generate`、`BUG-Generate`、`REQ-Complete`、`BUG-Complete`、`REQ-Review`、`BUG-Review`、`REQ-Opsx`、`BUG-Opsx`、`Opsx-Apply`、`Opsx-Archive`、`Sprint-Propose`、`Sprint-Archive` | 按固定矩阵列统计；`sprint.exps` 等额外事件不进入矩阵列 |
| 仍为 0 的列 | `Capture`、`BUG-Explore`、`REQ-Explore`、`Opsx-Explore`、`Opsx-Propose`、`Sprint-Explore`、`Sprint-Apply` | 当前 Sprint scope 未匹配到这些固定命令列 |
| 矩阵外事件 | `req.archive`、`sprint.exps` | 已计入 totals，但不属于当前规范要求的横向列 |

说明：下列表格按 Sprint scope 聚合，除显式 `sprint_id` 外，也会纳入与本 Sprint 的 REQ、BUG、Change 关联的命令记录；同一需求或 BUG 的短 ID 与完整目录名会在 Sprint 内合并，避免重复行。

### 总Token消耗数【total_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 12,396,465 | 3,925,748 | 0 | 0 | 3,538,171 | 1,095,621 | 10,461,701 | 446,019 | 11,341,526 | 643,655 | 31,061,146 | 1,840,212 | 0 | 0 | 59,426,957 | 20,207,655 | 18,603,550 | 0 | 0 | 282,333 |
| sprint-008 | 0 | 12,396,465 | 3,925,748 | 0 | 0 | 3,538,171 | 1,095,621 | 10,461,701 | 446,019 | 11,341,526 | 643,655 | 31,061,146 | 1,840,212 | 0 | 0 | 59,426,957 | 20,207,655 | 18,603,550 | 0 | 0 | 282,333 |
| REQ-0039-xl-admin-page-layered-acceptance-template | 0 | 0 | 285,124 | 0 | 0 | 514,956 | 0 | 695,215 | 0 | 1,516,697 | 0 | 2,093,741 | 0 | 0 | 0 | 1,519,560 | 1,026,379 | 1,860,219 | 0 | 0 | 0 |
| REQ-0040-rule-skill-read-summary-reuse-context-budget | 0 | 0 | 639,196 | 0 | 0 | 357,060 | 0 | 521,730 | 0 | 1,070,010 | 0 | 2,204,579 | 0 | 0 | 0 | 1,752,758 | 1,753,216 | 2,517,586 | 0 | 0 | 0 |
| REQ-0041-miniapp-home | 0 | 9,997,076 | 0 | 0 | 0 | 351,401 | 0 | 855,429 | 0 | 868,366 | 0 | 3,539,876 | 0 | 0 | 0 | 0 | 1,147,749 | 960,117 | 0 | 0 | 0 |
| REQ-0042-custom-navigation-bar | 0 | 0 | 438,399 | 0 | 0 | 310,193 | 0 | 2,712,649 | 0 | 989,878 | 0 | 4,938,385 | 0 | 0 | 0 | 2,226,233 | 2,069,542 | 2,987,300 | 0 | 0 | 0 |
| REQ-0043-miniapp-home-style-optimization | 0 | 0 | 680,003 | 0 | 0 | 1,114,832 | 0 | 2,292,558 | 0 | 663,866 | 0 | 1,926,444 | 0 | 0 | 0 | 5,031,583 | 1,599,002 | 1,378,852 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 310,992 | 0 | 0 | 0 | 0 | 581,941 | 0 | 988,333 | 0 | 2,975,633 | 0 | 0 | 0 | 14,022,243 | 5,988,517 | 1,088,464 | 0 | 0 | 0 |
| REQ-0045-category-list-page | 0 | 0 | 350,128 | 0 | 0 | 0 | 0 | 441,268 | 0 | 846,026 | 0 | 3,302,192 | 0 | 0 | 0 | 4,885,774 | 2,843,937 | 850,971 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 343,352 | 0 | 0 | 430,199 | 0 | 385,416 | 0 | 2,160,139 | 0 | 3,226,011 | 0 | 0 | 0 | 16,027,666 | 0 | 1,540,101 | 0 | 0 | 0 |
| REQ-0047-product-list-common-component-application | 0 | 0 | 299,410 | 0 | 0 | 200,341 | 0 | 1,439,859 | 0 | 1,196,929 | 0 | 4,515,420 | 0 | 0 | 0 | 6,452,010 | 2,862,703 | 2,132,852 | 0 | 0 | 0 |
| REQ-0048-miniapp-global-custom-navigation-bar | 0 | 0 | 579,144 | 0 | 0 | 259,189 | 0 | 535,636 | 0 | 1,041,282 | 0 | 2,338,865 | 0 | 0 | 0 | 4,185,881 | 916,610 | 860,225 | 0 | 0 | 0 |
| BUG-0065-miniapp-home-preview-deviation | 0 | 12,396,465 | 0 | 0 | 0 | 0 | 1,095,621 | 0 | 446,019 | 0 | 643,655 | 0 | 1,840,212 | 0 | 0 | 3,323,249 | 459,530 | 1,716,759 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7,247,066 | 0 | 0 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,837,499 | 1,243,383 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,137,683 | 0 | 0 | 0 | 0 |

### 总输入Token消耗数【input_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 12,355,886 | 3,893,637 | 0 | 0 | 3,499,426 | 1,091,618 | 10,375,130 | 440,018 | 11,270,208 | 641,030 | 30,922,092 | 1,833,078 | 0 | 0 | 59,131,731 | 20,144,127 | 18,474,052 | 0 | 0 | 279,103 |
| sprint-008 | 0 | 12,355,886 | 3,893,637 | 0 | 0 | 3,499,426 | 1,091,618 | 10,375,130 | 440,018 | 11,270,208 | 641,030 | 30,922,092 | 1,833,078 | 0 | 0 | 59,131,731 | 20,144,127 | 18,474,052 | 0 | 0 | 279,103 |
| REQ-0039-xl-admin-page-layered-acceptance-template | 0 | 0 | 282,246 | 0 | 0 | 509,256 | 0 | 685,576 | 0 | 1,506,282 | 0 | 2,085,806 | 0 | 0 | 0 | 1,507,759 | 1,022,663 | 1,853,634 | 0 | 0 | 0 |
| REQ-0040-rule-skill-read-summary-reuse-context-budget | 0 | 0 | 633,617 | 0 | 0 | 353,022 | 0 | 516,796 | 0 | 1,066,753 | 0 | 2,195,434 | 0 | 0 | 0 | 1,742,683 | 1,748,608 | 2,504,961 | 0 | 0 | 0 |
| REQ-0041-miniapp-home | 0 | 9,960,768 | 0 | 0 | 0 | 345,095 | 0 | 846,664 | 0 | 866,068 | 0 | 3,529,640 | 0 | 0 | 0 | 0 | 1,122,270 | 952,610 | 0 | 0 | 0 |
| REQ-0042-custom-navigation-bar | 0 | 0 | 434,527 | 0 | 0 | 305,932 | 0 | 2,694,727 | 0 | 963,392 | 0 | 4,924,260 | 0 | 0 | 0 | 2,213,943 | 2,066,135 | 2,973,658 | 0 | 0 | 0 |
| REQ-0043-miniapp-home-style-optimization | 0 | 0 | 677,015 | 0 | 0 | 1,109,222 | 0 | 2,285,735 | 0 | 659,265 | 0 | 1,909,840 | 0 | 0 | 0 | 4,985,036 | 1,596,012 | 1,368,887 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 307,390 | 0 | 0 | 0 | 0 | 574,908 | 0 | 985,064 | 0 | 2,959,991 | 0 | 0 | 0 | 13,972,523 | 5,977,421 | 1,079,920 | 0 | 0 | 0 |
| REQ-0045-category-list-page | 0 | 0 | 346,430 | 0 | 0 | 0 | 0 | 435,139 | 0 | 842,341 | 0 | 3,287,373 | 0 | 0 | 0 | 4,859,830 | 2,837,092 | 842,433 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 340,811 | 0 | 0 | 425,532 | 0 | 379,469 | 0 | 2,149,804 | 0 | 3,206,706 | 0 | 0 | 0 | 15,963,372 | 0 | 1,522,993 | 0 | 0 | 0 |
| REQ-0047-product-list-common-component-application | 0 | 0 | 296,372 | 0 | 0 | 196,415 | 0 | 1,428,575 | 0 | 1,193,192 | 0 | 4,496,959 | 0 | 0 | 0 | 6,418,664 | 2,859,330 | 2,121,256 | 0 | 0 | 0 |
| REQ-0048-miniapp-global-custom-navigation-bar | 0 | 0 | 575,229 | 0 | 0 | 254,952 | 0 | 527,541 | 0 | 1,038,047 | 0 | 2,326,083 | 0 | 0 | 0 | 4,164,410 | 914,596 | 850,156 | 0 | 0 | 0 |
| BUG-0065-miniapp-home-preview-deviation | 0 | 12,355,886 | 0 | 0 | 0 | 0 | 1,091,618 | 0 | 440,018 | 0 | 641,030 | 0 | 1,833,078 | 0 | 0 | 3,303,511 | 458,378 | 1,705,860 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7,225,187 | 0 | 0 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,823,469 | 1,238,215 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1,135,602 | 0 | 0 | 0 | 0 |

### 总输出Token消耗数【output_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 40,579 | 32,111 | 0 | 0 | 38,745 | 4,003 | 86,571 | 6,001 | 50,529 | 2,625 | 139,054 | 7,134 | 0 | 0 | 274,437 | 41,430 | 129,498 | 0 | 0 | 3,230 |
| sprint-008 | 0 | 40,579 | 32,111 | 0 | 0 | 38,745 | 4,003 | 86,571 | 6,001 | 50,529 | 2,625 | 139,054 | 7,134 | 0 | 0 | 274,437 | 41,430 | 129,498 | 0 | 0 | 3,230 |
| REQ-0039-xl-admin-page-layered-acceptance-template | 0 | 0 | 2,878 | 0 | 0 | 5,700 | 0 | 9,639 | 0 | 10,415 | 0 | 7,935 | 0 | 0 | 0 | 11,801 | 3,716 | 6,585 | 0 | 0 | 0 |
| REQ-0040-rule-skill-read-summary-reuse-context-budget | 0 | 0 | 5,579 | 0 | 0 | 4,038 | 0 | 4,934 | 0 | 3,257 | 0 | 9,145 | 0 | 0 | 0 | 10,075 | 4,608 | 12,625 | 0 | 0 | 0 |
| REQ-0041-miniapp-home | 0 | 36,308 | 0 | 0 | 0 | 6,306 | 0 | 8,765 | 0 | 2,298 | 0 | 10,236 | 0 | 0 | 0 | 0 | 3,381 | 7,507 | 0 | 0 | 0 |
| REQ-0042-custom-navigation-bar | 0 | 0 | 3,872 | 0 | 0 | 4,261 | 0 | 17,922 | 0 | 5,697 | 0 | 14,125 | 0 | 0 | 0 | 12,290 | 3,407 | 13,642 | 0 | 0 | 0 |
| REQ-0043-miniapp-home-style-optimization | 0 | 0 | 2,988 | 0 | 0 | 5,610 | 0 | 6,823 | 0 | 4,601 | 0 | 16,604 | 0 | 0 | 0 | 25,758 | 2,990 | 9,965 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 3,602 | 0 | 0 | 0 | 0 | 7,033 | 0 | 3,269 | 0 | 15,642 | 0 | 0 | 0 | 49,720 | 11,096 | 8,544 | 0 | 0 | 0 |
| REQ-0045-category-list-page | 0 | 0 | 3,698 | 0 | 0 | 0 | 0 | 6,129 | 0 | 3,685 | 0 | 14,819 | 0 | 0 | 0 | 25,944 | 6,845 | 8,538 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 2,541 | 0 | 0 | 4,667 | 0 | 5,947 | 0 | 10,335 | 0 | 19,305 | 0 | 0 | 0 | 64,294 | 0 | 17,108 | 0 | 0 | 0 |
| REQ-0047-product-list-common-component-application | 0 | 0 | 3,038 | 0 | 0 | 3,926 | 0 | 11,284 | 0 | 3,737 | 0 | 18,461 | 0 | 0 | 0 | 33,346 | 3,373 | 11,596 | 0 | 0 | 0 |
| REQ-0048-miniapp-global-custom-navigation-bar | 0 | 0 | 3,915 | 0 | 0 | 4,237 | 0 | 8,095 | 0 | 3,235 | 0 | 12,782 | 0 | 0 | 0 | 21,471 | 2,014 | 10,069 | 0 | 0 | 0 |
| BUG-0065-miniapp-home-preview-deviation | 0 | 40,579 | 0 | 0 | 0 | 0 | 4,003 | 0 | 6,001 | 0 | 2,625 | 0 | 7,134 | 0 | 0 | 19,738 | 1,152 | 10,899 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 21,879 | 0 | 0 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,030 | 5,168 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2,081 | 0 | 0 | 0 | 0 |

### 模型调用次数【model_call_count】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 68 | 85 | 0 | 0 | 40 | 12 | 87 | 4 | 126 | 5 | 182 | 12 | 0 | 0 | 520 | 139 | 143 | 0 | 0 | 6 |
| sprint-008 | 0 | 68 | 85 | 0 | 0 | 40 | 12 | 87 | 4 | 126 | 5 | 182 | 12 | 0 | 0 | 520 | 139 | 143 | 0 | 0 | 6 |
| REQ-0039-xl-admin-page-layered-acceptance-template | 0 | 0 | 7 | 0 | 0 | 6 | 0 | 6 | 0 | 20 | 0 | 12 | 0 | 0 | 0 | 25 | 11 | 9 | 0 | 0 | 0 |
| REQ-0040-rule-skill-read-summary-reuse-context-budget | 0 | 0 | 14 | 0 | 0 | 4 | 0 | 5 | 0 | 9 | 0 | 15 | 0 | 0 | 0 | 25 | 15 | 14 | 0 | 0 | 0 |
| REQ-0041-miniapp-home | 0 | 57 | 0 | 0 | 0 | 4 | 0 | 7 | 0 | 5 | 0 | 17 | 0 | 0 | 0 | 0 | 13 | 11 | 0 | 0 | 0 |
| REQ-0042-custom-navigation-bar | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 17 | 0 | 20 | 0 | 31 | 0 | 0 | 0 | 26 | 12 | 25 | 0 | 0 | 0 |
| REQ-0043-miniapp-home-style-optimization | 0 | 0 | 5 | 0 | 0 | 6 | 0 | 10 | 0 | 13 | 0 | 14 | 0 | 0 | 0 | 27 | 11 | 14 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 7 | 0 | 10 | 0 | 18 | 0 | 0 | 0 | 112 | 44 | 9 | 0 | 0 | 0 |
| REQ-0045-category-list-page | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 6 | 0 | 9 | 0 | 20 | 0 | 0 | 0 | 44 | 13 | 7 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 9 | 0 | 0 | 8 | 0 | 5 | 0 | 19 | 0 | 18 | 0 | 0 | 0 | 129 | 0 | 12 | 0 | 0 | 0 |
| REQ-0047-product-list-common-component-application | 0 | 0 | 9 | 0 | 0 | 4 | 0 | 18 | 0 | 12 | 0 | 24 | 0 | 0 | 0 | 53 | 14 | 16 | 0 | 0 | 0 |
| REQ-0048-miniapp-global-custom-navigation-bar | 0 | 0 | 14 | 0 | 0 | 4 | 0 | 6 | 0 | 9 | 0 | 13 | 0 | 0 | 0 | 41 | 6 | 6 | 0 | 0 | 0 |
| BUG-0065-miniapp-home-preview-deviation | 0 | 68 | 0 | 0 | 0 | 0 | 12 | 0 | 4 | 0 | 5 | 0 | 12 | 0 | 0 | 38 | 3 | 9 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 52 | 0 | 0 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 38 | 19 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |

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
