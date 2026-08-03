---
sprint_id: sprint-014
title: Sprint 014 迭代经验复盘
status: draft
created_at: 2026-07-31 08:18:50
updated_at: 2026-07-31 08:18:50
owner: product
related_iteration: iterations/archive/sprint-014/
source: /sprint-exps sprint-014
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 014 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 实际周期 | 2026-07-29 15:51:41 ~ 2026-07-31 08:14:33 |
| REQ / BUG / Change | 5 / 4 / 9 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 183/183 |
| 估算 | 28 SP / 28.0 人天 |
| 容量 | 30 人天；占用 93.33%；fix buffer 6.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；9/9 Change archived |
| AI usage | `present/actual`；77 command runs，1,152 model calls，2,301 tool calls，153,830,437 total tokens |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-014 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-014 --json`、`iterations/archive/sprint-014/sprint.yaml`、`iterations/archive/sprint-014/acceptance-report.md`、`data/ai-usage/sprints/sprint-014.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 发布镜像治理 | `/image-prepare`、`/image-build`、release image gates、plan/manifest 校验、敏感信息扫描和发布文档同步 |
| 类目命名 | 管理端类目名称支持 15 个可见字符与常见特殊字符，后端校验、OpenAPI/Orval、管理端和多端展示回归同步 |
| Web 弹窗策略 | 标准 Dialog / Modal 点击外部空白区域不关闭，明确关闭入口与表单/确认/详情状态保持 |
| 小程序品牌列表 | 品牌列表下半部改为单行品牌信息，展示商品数量和末级类目集合，并拆分品牌/类目点击区域 |
| 小程序全局回首页 | 非首页主要页面统一回首页悬浮按钮，覆盖 TabBar、页面栈、防重复点击和底部避让 |
| 小程序图片加载 | 商品卡片图片缩略图优先、按需加载、缓存/观测/缺图占位和对象引用审计 |
| 小程序分类页 | 二级类目两列展示，长名称完整显示，skeleton 和点击路由保持一致 |
| 排序一致性 | 管理端 SKU 列表发布/创建时间排序，小程序搜索/分类商品列表与品牌详情商品 Tab 排序一致 |

## 2. 流程复盘

### 做得好的

1. **归档闭环完整**：9 个 Change 全部归档且带 `trace.md`，readiness 返回 PASS，归档路径残留为 0，没有继续传播旧 change 阶段路径或 active Change 路径。
2. **横切门禁更成熟**：发布镜像治理、API/Orval、DB/docs、MinIO、安全扫描、目录结构、AI usage hook 都进入可验证命令链。
3. **多端体验修复集中闭环**：Web 弹窗、小程序品牌列表、商品图片、分类页、商品排序和管理端 SKU 排序都以明确 Change 落地，避免把问题散落成口头待办。
4. **自动化证据足够支撑归档**：Fact Sheet 显示 183/183 tasks 完成，acceptance 为 final，Workflow Sync 与 residual gate 成功。
5. **AI usage 已刷新到 actual**：归档后 hook 将 `data/ai-usage/sprints/sprint-014.json` 更新为 `actual/present`，复盘可直接使用真实矩阵。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Scope 过满，fix buffer 偏低 | `sprint.yaml` 显示 28.0/30 人天，占用 93.33%，fix buffer 6.67% | 后续再纳入 P0/P1 缺陷时几乎没有缓冲，Sprint-Propose 和验收同步成本升高 |
| 多次追加范围导致 Sprint-Propose 成本高 | AI usage 中 `Sprint-Propose` 为 34,609,416 total tokens，213 model calls | 反复刷新四件套、release-note、acceptance 和 workflow-sync 派生块，消耗显著 |
| 小程序人工 evidence 仍保留 follow_up | acceptance 中 REQ-0083、REQ-0085、BUG-0092、BUG-0093 均有 DevTools / 真机 / 体验版 evidence follow_up | 允许 archive，但发布前仍需补录或明确不可用原因，不能写作真机通过 |
| 验收文案存在短暂中间态残留 | `/sprint-archive` 后 release-note 与 acceptance 曾保留 `proposed/applied/in_sprint` 和“待实现与验收”文案，后续已修正 | 说明 Workflow Sync 对部分非 marker 文案仍需人工或脚本复核 |
| usage coverage 有历史归因噪声 | `data/ai-usage/sprints/sprint-014.json` coverage 中出现非本 Sprint 范围的 `BUG-0085-admin-video-upload-stuck-at-99` | 不影响 scope 统计，但复盘矩阵解释时不能把该归因行当作 Sprint 014 交付范围 |

### 优化建议

1. **Sprint 规划冻结线前置**：当 capacity usage 超过 85% 或 fix buffer 低于 15% 时，新增范围默认要求移出低优先级项或拆 Sprint。
2. **发布说明/验收表增加 close-time stale scan**：`/sprint-archive` 后自动搜索 `proposed|applied|in_sprint|待实现与验收`，避免归档文档保留中间态。
3. **小程序 evidence 独立成发布 checklist**：DevTools/真机/体验版 Network evidence 可不阻塞 archive，但必须在 release-prepare 前集中复核。
4. **把 high-token 命令增量化**：Sprint-Propose、Opsx-Apply、Opsx-Archive 对应 summary/diff/stat 优先，减少全量四件套、trace、archive 和测试日志重复展开。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-014.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| generated_at | 2026-07-31T00:15:51.966132Z | snapshot 生成时间 |
| command_run_count | 77 | snapshot totals |
| model_call_count | 1,152 | snapshot totals |
| tool_call_count | 2,301 | snapshot totals |
| input_tokens | 152,913,613 | snapshot totals |
| cached_input_tokens | 144,462,336 | snapshot totals |
| output_tokens | 661,249 | snapshot totals |
| reasoning_output_tokens | 59,184 | snapshot totals |
| total_tokens | 153,830,437 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 主要输入消耗 | Opsx-Apply、Sprint-Propose、Opsx-Archive、Opsx-Modify、REQ-Opsx | 横切发布治理、Web/小程序/UI、API/DB/docs/tests 同步与多次 Scope 回填 |
| 主要输出消耗 | Opsx-Apply、Sprint-Propose、Opsx-Modify、Opsx-Archive | 实现说明、验收返修、同步报告、归档摘要和测试摘要 |
| 重复/浪费来源 | 多次 Sprint-Propose 扩围、XL/L Change 横切实现、归档文案状态复核、设备 evidence follow_up 反复说明 | Fact Sheet token_risks：9 Change、183/183 tasks、`sprint.md` 超 200 行 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、已读规则摘要复用、路径残留 gate、矩阵从 JSON 生成 | 符合 `rules/agent-context-budget.md` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。Snapshot coverage 还包含历史归因行 `BUG-0085-admin-video-upload-stuck-at-99`，本复盘矩阵只展示 Sprint 014 正式 scope 的 5 REQ / 4 BUG。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 2477801 | 1259819 | 0 | 0 | 2257962 | 2008486 | 3219148 | 2276932 | 3143184 | 4393546 | 9394996 | 5947517 | 0 | 0 | 40062851 | 18763564 | 23170403 | 34609416 | 0 | 0 | 844812 |
| sprint-014 | 0 | 2477801 | 1259819 | 0 | 0 | 2257962 | 2008486 | 3219148 | 2276932 | 3143184 | 4393546 | 9394996 | 5947517 | 0 | 0 | 40062851 | 18763564 | 23170403 | 34609416 | 0 | 0 | 844812 |
| REQ-0081-release-image-build-governance | 0 | 0 | 563204 | 0 | 0 | 635587 | 0 | 622135 | 0 | 890465 | 0 | 2343817 | 0 | 0 | 0 | 6667262 | 0 | 4919702 | 720129 | 0 | 0 | 0 |
| REQ-0082-admin-category-name-special-characters | 0 | 0 | 293995 | 0 | 0 | 251445 | 0 | 539751 | 0 | 551749 | 0 | 1507869 | 0 | 0 | 0 | 3322447 | 1812684 | 4822101 | 1653872 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 402620 | 0 | 0 | 340102 | 0 | 891934 | 0 | 619078 | 0 | 3392947 | 0 | 0 | 0 | 5517990 | 11150273 | 1213262 | 2800545 | 0 | 0 | 0 |
| REQ-0084-web-modal-disable-outside-close | 0 | 0 | 0 | 0 | 0 | 696018 | 0 | 566209 | 0 | 516077 | 0 | 0 | 0 | 0 | 0 | 1840559 | 0 | 1776250 | 6514295 | 0 | 0 | 0 |
| REQ-0085-miniapp-global-home-floating-button | 0 | 0 | 0 | 0 | 0 | 334810 | 0 | 599119 | 0 | 565815 | 0 | 2150363 | 0 | 0 | 0 | 2730667 | 4459866 | 817114 | 6488520 | 0 | 0 | 0 |
| BUG-0090-admin-sku-list-publish-sort-order | 0 | 0 | 0 | 0 | 0 | 0 | 1165868 | 0 | 689456 | 0 | 1235079 | 0 | 1868535 | 0 | 0 | 3522100 | 0 | 2084345 | 6150503 | 0 | 0 | 0 |
| BUG-0092-miniapp-card-images-slow-load | 0 | 867639 | 0 | 0 | 0 | 0 | 561793 | 0 | 792660 | 0 | 1499260 | 0 | 985935 | 0 | 0 | 7480805 | 0 | 930731 | 2732539 | 0 | 0 | 0 |
| BUG-0093-miniapp-category-secondary-grid-name-full-display | 0 | 579579 | 0 | 0 | 0 | 0 | 280825 | 0 | 345403 | 0 | 931380 | 0 | 1612076 | 0 | 0 | 3447979 | 1340741 | 1493867 | 1964858 | 0 | 0 | 0 |
| BUG-0091-miniapp-product-list-sort-consistency | 0 | 1030583 | 0 | 0 | 0 | 0 | 794615 | 0 | 449413 | 0 | 727827 | 0 | 1480971 | 0 | 0 | 5533042 | 0 | 5113031 | 7613422 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 2454896 | 1250109 | 0 | 0 | 2232243 | 1995848 | 3176176 | 2260483 | 3131139 | 4380297 | 9352489 | 5892631 | 0 | 0 | 39827811 | 18650582 | 23085236 | 34384308 | 0 | 0 | 839365 |
| sprint-014 | 0 | 2454896 | 1250109 | 0 | 0 | 2232243 | 1995848 | 3176176 | 2260483 | 3131139 | 4380297 | 9352489 | 5892631 | 0 | 0 | 39827811 | 18650582 | 23085236 | 34384308 | 0 | 0 | 839365 |
| REQ-0081-release-image-build-governance | 0 | 0 | 560781 | 0 | 0 | 629956 | 0 | 616773 | 0 | 888371 | 0 | 2331384 | 0 | 0 | 0 | 6637072 | 0 | 4913639 | 690752 | 0 | 0 | 0 |
| REQ-0082-admin-category-name-special-characters | 0 | 0 | 290509 | 0 | 0 | 247251 | 0 | 532250 | 0 | 549525 | 0 | 1499186 | 0 | 0 | 0 | 3287304 | 1805199 | 4814272 | 1645353 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 398819 | 0 | 0 | 335683 | 0 | 881027 | 0 | 616493 | 0 | 3381745 | 0 | 0 | 0 | 5466305 | 11084446 | 1210530 | 2791216 | 0 | 0 | 0 |
| REQ-0084-web-modal-disable-outside-close | 0 | 0 | 0 | 0 | 0 | 689372 | 0 | 557175 | 0 | 513501 | 0 | 0 | 0 | 0 | 0 | 1808686 | 0 | 1772750 | 6484669 | 0 | 0 | 0 |
| REQ-0085-miniapp-global-home-floating-button | 0 | 0 | 0 | 0 | 0 | 329981 | 0 | 588951 | 0 | 563249 | 0 | 2140174 | 0 | 0 | 0 | 2715593 | 4446076 | 793062 | 6434735 | 0 | 0 | 0 |
| BUG-0090-admin-sku-list-publish-sort-order | 0 | 0 | 0 | 0 | 0 | 0 | 1157310 | 0 | 684818 | 0 | 1231556 | 0 | 1859447 | 0 | 0 | 3503289 | 0 | 2080987 | 6112563 | 0 | 0 | 0 |
| BUG-0092-miniapp-card-images-slow-load | 0 | 864432 | 0 | 0 | 0 | 0 | 559725 | 0 | 788567 | 0 | 1496011 | 0 | 954970 | 0 | 0 | 7458094 | 0 | 905989 | 2712713 | 0 | 0 | 0 |
| BUG-0093-miniapp-category-secondary-grid-name-full-display | 0 | 573227 | 0 | 0 | 0 | 0 | 278813 | 0 | 342209 | 0 | 927956 | 0 | 1604901 | 0 | 0 | 3439985 | 1314861 | 1488282 | 1956805 | 0 | 0 | 0 |
| BUG-0091-miniapp-product-list-sort-consistency | 0 | 1017237 | 0 | 0 | 0 | 0 | 789315 | 0 | 444889 | 0 | 724774 | 0 | 1473313 | 0 | 0 | 5511483 | 0 | 5105725 | 7572764 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 22905 | 9710 | 0 | 0 | 25719 | 12638 | 42972 | 16449 | 12045 | 13249 | 42507 | 33304 | 0 | 0 | 171016 | 68139 | 43488 | 141661 | 0 | 0 | 5447 |
| sprint-014 | 0 | 22905 | 9710 | 0 | 0 | 25719 | 12638 | 42972 | 16449 | 12045 | 13249 | 42507 | 33304 | 0 | 0 | 171016 | 68139 | 43488 | 141661 | 0 | 0 | 5447 |
| REQ-0081-release-image-build-governance | 0 | 0 | 2423 | 0 | 0 | 5631 | 0 | 5362 | 0 | 2094 | 0 | 12433 | 0 | 0 | 0 | 30190 | 0 | 6063 | 8384 | 0 | 0 | 0 |
| REQ-0082-admin-category-name-special-characters | 0 | 0 | 3486 | 0 | 0 | 4194 | 0 | 7501 | 0 | 2224 | 0 | 8683 | 0 | 0 | 0 | 13456 | 7485 | 7829 | 8519 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 3801 | 0 | 0 | 4419 | 0 | 10907 | 0 | 2585 | 0 | 11202 | 0 | 0 | 0 | 30840 | 43368 | 2732 | 9329 | 0 | 0 | 0 |
| REQ-0084-web-modal-disable-outside-close | 0 | 0 | 0 | 0 | 0 | 6646 | 0 | 9034 | 0 | 2576 | 0 | 0 | 0 | 0 | 0 | 10381 | 0 | 3500 | 29626 | 0 | 0 | 0 |
| REQ-0085-miniapp-global-home-floating-button | 0 | 0 | 0 | 0 | 0 | 4829 | 0 | 10168 | 0 | 2566 | 0 | 10189 | 0 | 0 | 0 | 15074 | 13790 | 3141 | 33131 | 0 | 0 | 0 |
| BUG-0090-admin-sku-list-publish-sort-order | 0 | 0 | 0 | 0 | 0 | 0 | 8558 | 0 | 4638 | 0 | 3523 | 0 | 9088 | 0 | 0 | 18811 | 0 | 3358 | 17334 | 0 | 0 | 0 |
| BUG-0092-miniapp-card-images-slow-load | 0 | 3207 | 0 | 0 | 0 | 0 | 2068 | 0 | 4093 | 0 | 3249 | 0 | 9383 | 0 | 0 | 22711 | 0 | 3974 | 19826 | 0 | 0 | 0 |
| BUG-0093-miniapp-category-secondary-grid-name-full-display | 0 | 6352 | 0 | 0 | 0 | 0 | 2012 | 0 | 3194 | 0 | 3424 | 0 | 7175 | 0 | 0 | 7994 | 3496 | 5585 | 8053 | 0 | 0 | 0 |
| BUG-0091-miniapp-product-list-sort-consistency | 0 | 13346 | 0 | 0 | 0 | 0 | 5300 | 0 | 4524 | 0 | 3053 | 0 | 7658 | 0 | 0 | 21559 | 0 | 7306 | 19464 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 35 | 21 | 0 | 0 | 36 | 34 | 33 | 23 | 25 | 36 | 57 | 51 | 0 | 0 | 307 | 111 | 158 | 213 | 0 | 0 | 12 |
| sprint-014 | 0 | 35 | 21 | 0 | 0 | 36 | 34 | 33 | 23 | 25 | 36 | 57 | 51 | 0 | 0 | 307 | 111 | 158 | 213 | 0 | 0 | 12 |
| REQ-0081-release-image-build-governance | 0 | 0 | 5 | 0 | 0 | 5 | 0 | 4 | 0 | 5 | 0 | 11 | 0 | 0 | 0 | 46 | 0 | 23 | 10 | 0 | 0 | 0 |
| REQ-0082-admin-category-name-special-characters | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 6 | 0 | 5 | 0 | 11 | 0 | 0 | 0 | 33 | 11 | 21 | 9 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 9 | 0 | 0 | 5 | 0 | 9 | 0 | 5 | 0 | 21 | 0 | 0 | 0 | 53 | 67 | 10 | 14 | 0 | 0 | 0 |
| REQ-0084-web-modal-disable-outside-close | 0 | 0 | 0 | 0 | 0 | 14 | 0 | 7 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 19 | 0 | 14 | 38 | 0 | 0 | 0 |
| REQ-0085-miniapp-global-home-floating-button | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 7 | 0 | 5 | 0 | 14 | 0 | 0 | 0 | 21 | 22 | 14 | 49 | 0 | 0 | 0 |
| BUG-0090-admin-sku-list-publish-sort-order | 0 | 0 | 0 | 0 | 0 | 0 | 27 | 0 | 8 | 0 | 11 | 0 | 13 | 0 | 0 | 30 | 0 | 12 | 32 | 0 | 0 | 0 |
| BUG-0092-miniapp-card-images-slow-load | 0 | 5 | 0 | 0 | 0 | 0 | 3 | 0 | 4 | 0 | 7 | 0 | 12 | 0 | 0 | 40 | 0 | 16 | 27 | 0 | 0 | 0 |
| BUG-0093-miniapp-category-secondary-grid-name-full-display | 0 | 12 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 9 | 0 | 13 | 0 | 0 | 16 | 11 | 22 | 12 | 0 | 0 | 0 |
| BUG-0091-miniapp-product-list-sort-consistency | 0 | 18 | 0 | 0 | 0 | 0 | 18 | 0 | 7 | 0 | 9 | 0 | 13 | 0 | 0 | 49 | 0 | 26 | 37 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Opsx-Apply | high | 40,062,851 total tokens，307 model calls | 对 XL/L Change 先用 Fact Sheet、diff stat 和 focused tests 定位，再按 API/DB、Web、miniapp、docs/tests 分段 apply |
| Sprint-Propose | high | 34,609,416 total tokens，213 model calls | 多次追加 Scope 后只刷新增量范围和状态摘要，不重复读完整四件套 |
| Opsx-Archive | high | 23,170,403 total tokens，158 model calls | archive 前使用 status/tasks/spec heading 摘要，归档后用 residual gate 和 Fact Sheet 代替 archive 全量读取 |
| Opsx-Modify | high | 18,763,564 total tokens，111 model calls | 验收返修前先拆分反馈为最小补丁，复用上次 diff 和 focused test，不重新展开全量 Change |
| Sprint 四件套 | medium | `sprint.md` 405 行，Fact Sheet token_risks 标记 high | 复盘优先 summary；只在回链、stale 文案和 closure note 时读局部片段 |
| OpenSpec archive lookup | medium | 9 Change，183/183 tasks | 使用 resolver、Fact Sheet 和 residual gate，避免宽泛扫描 `openspec/archive/**` |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次先运行 `--summary`，没有默认展开全部 Sprint 四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 `sprint-exps` skill、Fact Sheet summary、README、上期复盘样式和必要索引片段 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 需要修正 | 是 | Sprint-Propose、Opsx-Apply、Opsx-Archive 总成本偏高，说明多次扩围和横切实现仍需要更强的增量化 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-014-001 | P1 | 为 `/sprint-propose` 增加容量冻结线：capacity usage > 85% 或 fix buffer < 15% 时，新增范围需要移出项、拆 Sprint 或明确风险批准 | `/opsx-propose` | open |
| T-014-002 | P1 | 为 `/sprint-archive` 增加 close-time stale scan，自动检查 release-note / acceptance 中的 `proposed`、`applied`、`in_sprint`、`待实现与验收` | `/opsx-propose` | open |
| T-014-003 | P1 | 将小程序 DevTools / 真机 / 体验版 Network evidence 抽成 release-prepare 前置 checklist，避免 archive 后遗漏发布证据 | `/req-capture` | open |
| T-014-004 | P2 | 对 XL/L Change 的 `/opsx-apply` 增加分段执行建议：API/DB、Web、miniapp、docs/tests 分块验收 | `/opsx-propose` | open |
| T-014-005 | P2 | 对 `data/ai-usage` coverage 中非本 Sprint 范围的历史归因行增加 summary warning 或过滤视图 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| 本 Sprint 从发布治理扩展到 UI、小程序和排序修复 | Scope 价值高但较满，容量风险比 sprint-013 明显增大 | 下一 Sprint 在 85% capacity usage 后冻结新增范围，除 P0 外不再扩围 |
| 发布镜像治理属于命令/发布链路能力 | 需要脚本、技能、release template、docs、tests 多点同步 | 治理类 REQ 继续用“命令输入/输出/门禁/证据/安全字段”作为验收骨架 |
| 小程序品牌列表和商品排序相互影响 | 品牌维度、类目维度和商品公开口径必须统一 | 小程序列表类需求在 propose 阶段就写清公开口径、点击区域、排序字段和空态 |
| Web 弹窗策略是横切交互规范 | 一处共享默认能减少误触，但历史自定义弹窗容易漏 | 共享 Dialog / Modal 需要明确默认行为和例外登记 |
| 设备 evidence 被反复标记 follow_up | 静态/API 自动化无法替代 DevTools/真机体验证据 | 发布流程中建立单独 evidence checklist，不把 follow_up 藏在 Change 验收里 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | 类目特殊字符和品牌列表聚合需要 OpenAPI/Orval 同步 | API 字段或 schema 变化继续强制跑 Orval 和 API 标准校验 |
| DB / 排序 | SKU 发布时间、创建时间、空值兜底和稳定分页必须由后端保证 | 排序修复不得只做当前页前端排序；必须覆盖分页稳定性测试 |
| Web UI | 弹窗外部点击策略、类目树展开和 SKU 列表排序都属于横切 UI 回归 | admin-list/admin-modal best-practice 要作为 apply 前置检查 |
| 小程序 UI | 品牌单行列表、全局回首页、分类页两列、商品图片加载都需要 320/375/430 pt 视口意识 | 小程序静态测试继续覆盖布局关键类名、路由参数、TabBar/安全区避让和 fallback |
| 媒体 / MinIO | 图片慢加载问题需要缩略图、缓存、对象存在性和失败占位一起处理 | 媒体类 BUG 必须补对象审计脚本或等价诊断路径 |
| 归档质量 | 本期 9/9 Change 都有 trace，residual 0 | 归档后继续跑 readiness、residual、directory structure、workflow sync 和 AI usage hook |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Release image evidence model | REQ-0081 | 将 image_required、plan、manifest、input_hashes、blockers、安全扫描沉淀为发布治理通用证据模型 |
| Category visible-character validator | REQ-0082 | 后端校验、前端字段错误、OpenAPI 描述、测试样例共用同一合法/非法样例表 |
| Dialog outside-close policy | REQ-0084 | 共享 Dialog / Modal 默认禁用外部点击关闭，例外通过组件级配置和测试说明登记 |
| Miniapp brand row model | REQ-0083 | 品牌 Logo/名称/商品数/末级类目集合/点击区域可作为品牌列表行组件契约 |
| Miniapp floating home button | REQ-0085 | 页面覆盖清单、例外原因、TabBar/reLaunch 策略、防重复点击和底部避让可继续复用 |
| Public product sorting contract | BUG-0091、BUG-0090 | 排序能力统一描述事实字段、空值兜底、稳定 secondary sort、分页不重排和不影响分支 |
| Media image audit | BUG-0092 | 对公开 SKU 主图/缩略图/对象存在性/失败率做只读审计，作为媒体性能 BUG 的诊断模板 |

## 6. Follow-up 建议

以下事项未自动创建 Issue。

| 建议命令 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议验收要点 | 来源 |
|----------|----------|------|------|----------|--------------|------|
| `/opsx-propose` | 技术治理 | Sprint archive stale 文案扫描 | sprint-014 close 后曾出现 release-note/acceptance 中间态文案残留 | Sprint 四件套、Workflow Sync、归档脚本 | archive 后自动报告 `proposed/applied/in_sprint/待实现与验收` 命中；不改 marker 块；残留为 0 才允许 close success | sprint-014 / `/sprint-exps sprint-014` |
| `/req-capture` | 需求 | 小程序发布 evidence checklist | 多个小程序 Change 仍保留 DevTools/真机/体验版 evidence follow_up | release-prepare、小程序验收、发布说明 | 发布前列出 320/375/430 pt、真机、Network、TabBar/安全区、截图/不可用原因；不可将静态测试写作真机通过 | sprint-014 / `/sprint-exps sprint-014` |
| `/opsx-propose` | 技术治理 | AI usage scope attribution filter | sprint-014 usage coverage 出现非本 Sprint 范围 BUG-0085 归因行 | `scripts/extract-ai-usage.py`、Fact Sheet summary、复盘矩阵 | summary 区分正式 scope 与额外归因；矩阵可选择 scope-only 或 all-attribution；不得误报交付范围 | sprint-014 / `/sprint-exps sprint-014` |
| `/opsx-propose` | 流程治理 | Sprint 容量冻结线 | sprint-014 capacity usage 93.33%，fix buffer 6.67% | `/sprint-propose`、`sprint.yaml`、容量门禁 | 超过阈值时新增范围提示拆分/移出项；风险写入 sprint.md；Workflow Sync 后保留明确冻结说明 | sprint-014 / `/sprint-exps sprint-014` |

## 7. 行动项

| ID | 优先级 | 事项 | Owner | 建议下一步 | 状态 |
|----|--------|------|-------|------------|------|
| A-014-001 | P1 | 将 `/sprint-archive` stale 文案扫描脚本化 | workflow | `/opsx-propose` | open |
| A-014-002 | P1 | 建立小程序发布前 evidence checklist | product/qa | `/req-capture` | open |
| A-014-003 | P1 | 为高容量 Sprint 增加冻结线和扩围规则 | product | `/opsx-propose` | open |
| A-014-004 | P2 | 为 AI usage 矩阵提供 scope-only/all-attribution 两种视图 | workflow | `/opsx-propose` | open |
| A-014-005 | P2 | 将发布镜像治理经验纳入 release/image 命令模板复核清单 | release | `/sprint-propose` | open |

## 8. 本次复盘读取边界

| 项 | 结果 |
|----|------|
| Fact Sheet summary | 已使用，作为主要事实源 |
| 完整 evidence_hints | 未读取；Fact Sheet `warnings=0`、`needs_detail=false` |
| Sprint 四件套 | 仅使用 summary 和必要回链片段 |
| Issue trace / Change tasks | 未默认展开；以 Fact Sheet 聚合计数和 acceptance signals 为准 |
| OpenAPI / Orval / 测试日志 | 未读取全文 |
| 残留路径 | `check-archived-path-residuals.py --json` 显示 residual_count 0 |
