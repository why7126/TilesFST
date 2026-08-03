---
sprint_id: sprint-015
title: Sprint 015 迭代经验复盘
status: draft
created_at: 2026-07-31 23:10:44
updated_at: 2026-07-31 23:15:45
owner: product
related_iteration: iterations/archive/sprint-015/
source: /sprint-exps sprint-015
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 015 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 实际周期 | 2026-07-31 15:17:00 ~ 2026-07-31 23:07:14 |
| REQ / BUG / Change | 1 / 5 / 6 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 109/109 |
| 估算 | 13.5 SP / 13.5 人天 |
| 容量 | 30 人天；占用 45.00%；fix buffer 55.00% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；6/6 Change archived |
| AI usage | `present/actual`；69 command runs，980 model calls，1,720 tool calls，123,474,476 total tokens |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-015 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-015 --json`、`iterations/archive/sprint-015/sprint.yaml`、`iterations/archive/sprint-015/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 管理端 SKU 类目筛选 | SKU 页类目筛选改为级联选择，父类目包含所有子孙类目 SKU |
| 管理端素材列 | SKU 素材列只保留图片/视频数量，不展示主图状态标签和素材完整度筛选 |
| 管理端类目树 | 类目树节点计数改为直接子类目数量，“全部类目”显示顶层类目数量 |
| 管理端筛选下拉 | 品牌、类目、规格、证书、Banner、用户、设置、日志、接口文档、主题等页面筛选下拉统一 |
| 小程序品牌列表 | 新版品牌 Hero、品牌矩阵、品牌卡片与类目胶囊独立点击，减少说明性冗余文案 |
| 小程序商品卡片图片 | 公开列表 `cover_image` 可访问回退、同路径缩略图生成、历史回填与媒体审计 |

## 2. 流程复盘

### 做得好的

1. **Scope 控制更健康**：本 Sprint 6 个 Change、13.5 人天，占用 45%，保留 55% fix buffer，比 sprint-014 的高占用更适合作为修复型 Sprint。
2. **归档闭环完整**：6/6 Change 都已归档且有 `trace.md`，readiness PASS，归档路径残留为 0，没有继续传播旧 active Change 路径。
3. **横向 UI 问题集中处理**：BUG-0098 将多个管理端页面的筛选下拉统一到共享控件/样式基线，避免一页一套局部 CSS 继续分化。
4. **媒体链路修复覆盖到数据侧**：BUG-0094 没有停留在小程序渲染层，而是覆盖 `cover_image` 可访问性、同路径缩略图、历史回填和审计脚本。
5. **复盘读取边界更克制**：本次复盘先使用 Fact Sheet summary 与 residual JSON，没有默认展开全部 Issue trace、Change tasks 或 OpenAPI/Orval 生成物。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| 验收报告中仍保留 follow_up | acceptance signals 显示小程序 DevTools / 真机验收与对象存储历史回填保留 follow_up/运营执行项 | 不阻断 archive，但发布前仍需要 release checklist 明确补证或确认不可用 |
| 归档前非 marker 文案出现中间态 | `/sprint-archive` 时曾修正 release-note / acceptance 中 `proposed`、`applied`、`待实现与验收` 等文案 | Workflow Sync 对非 marker 自然语言仍需 close-time stale scan |
| 管理端筛选 UI 一致性是复发类问题 | BUG-0098 横跨多个管理端页面，说明页面级下拉样式长期分化 | 新列表页或筛选区改造需要把统一筛选控件作为 apply 前置 gate |
| 小程序图片性能与可访问性容易互相拉扯 | BUG-0094 承接 BUG-0092 图片性能优化后的无图回归 | 媒体优化必须同时验证性能、URL 可访问性、缩略图存在性和 fallback |
| AI usage snapshot 需要后置刷新 | 初次 Fact Sheet summary 曾显示 `estimated_fallback/stale`；`sprint.exps` hook 后刷新为 actual | `/sprint-exps` 文档生成前最好先确认 snapshot freshness，避免复盘中途返工 |

### 优化建议

1. **把 close-time stale scan 固化到归档**：归档前后检查 release-note / acceptance / sprint.md 中的 `proposed`、`applied`、`in_sprint`、`待实现与验收`。
2. **管理端筛选区统一 gate**：新增或修改管理端筛选页面时，必须复用统一筛选下拉，并覆盖触发框、弹层宽度、选中态、重置态、窄屏和裁切。
3. **媒体类 BUG 使用四联验收**：接口 URL 可访问、对象存储存在性、前端/小程序渲染、性能懒加载必须一起验收。
4. **小程序设备 evidence 前移到 release-prepare**：DevTools、真机、体验版 Network evidence 可以不阻断 archive，但必须在发布准备阶段集中确认。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-015.json` |
| AI usage mode | actual | `sprint.exps` post-command hook 刷新后为真实快照 |
| Snapshot status | present | `data/ai-usage/sprints/sprint-015.json` generated_at: 2026-07-31T15:15:45.170854Z |
| command_run_count | 69 | snapshot totals |
| model_call_count | 980 | snapshot totals |
| tool_call_count | 1,720 | snapshot totals |
| input_tokens | 122,791,697 | snapshot totals |
| cached_input_tokens | 117,667,328 | snapshot totals |
| output_tokens | 494,100 | snapshot totals |
| reasoning_output_tokens | 48,529 | snapshot totals |
| total_tokens | 123,474,476 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 主要输入消耗 | Opsx-Modify、Opsx-Apply、Sprint-Propose、Opsx-Archive、BUG-Opsx | 多页面 UI 横向统一、媒体链路跨后端/小程序/对象存储、归档同步和 Sprint 范围刷新 |
| 主要输出消耗 | Opsx-Modify、Opsx-Apply、Sprint-Propose、BUG-Opsx、BUG-Complete | 实现说明、验收返修、归档摘要、Workflow Sync 与测试摘要 |
| 重复/浪费来源 | 多页面筛选 UI 横向统一、媒体链路四段验证、归档前中间态文案修正、AI usage snapshot 中途刷新 | 6 个 Change 中包含管理端横切和媒体横切修复 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、已读规则摘要复用、分段读取、未展开完整 evidence_hints | 符合 `rules/agent-context-budget.md` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。Snapshot totals 包含 `sprint.exps` post-command hook 记录；下方矩阵按技能固定列展示，不单列 `sprint.exps`。Snapshot attribution 中出现 `REQ-0006`、`REQ-0083` 两个历史关联行，保留为归因视图，不代表 Sprint 015 正式 scope 新增范围。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 2079134 | 327668 | 0 | 0 | 420064 | 2658591 | 861505 | 6426607 | 655332 | 6071722 | 2067769 | 10064827 | 0 | 0 | 22841087 | 39910869 | 11492771 | 14425242 | 0 | 0 | 1101445 |
| sprint-015 | 0 | 2079134 | 327668 | 0 | 0 | 420064 | 2658591 | 861505 | 6426607 | 655332 | 6071722 | 2067769 | 10064827 | 0 | 0 | 22841087 | 39910869 | 11492771 | 14425242 | 0 | 0 | 1101445 |
| REQ-0086-miniapp-brand-list-ui-interaction-optimization | 0 | 0 | 327668 | 0 | 0 | 420064 | 0 | 861505 | 0 | 655332 | 0 | 2067769 | 0 | 0 | 0 | 2617866 | 6388842 | 1510808 | 1583787 | 0 | 0 | 0 |
| REQ-0006-tile-sku-management | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1281061 | 0 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 420064 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0096-admin-sku-category-filter-only-top-level | 0 | 506429 | 0 | 0 | 0 | 0 | 854373 | 0 | 1697640 | 0 | 1729925 | 0 | 2757647 | 0 | 0 | 4003018 | 11394453 | 1281061 | 3596065 | 0 | 0 | 0 |
| BUG-0097-admin-sku-material-main-image-tag-redundant | 0 | 362263 | 0 | 0 | 0 | 0 | 729906 | 0 | 348702 | 0 | 749335 | 0 | 1256432 | 0 | 0 | 3612702 | 4907746 | 1001404 | 2472263 | 0 | 0 | 0 |
| BUG-0095-admin-category-tree-count-shows-product-count | 0 | 483753 | 0 | 0 | 0 | 0 | 279042 | 0 | 583033 | 0 | 919547 | 0 | 3068417 | 0 | 0 | 0 | 3952448 | 1628695 | 2222169 | 0 | 0 | 0 |
| BUG-0094-miniapp-list-images-not-loading-after-speed-fix | 0 | 257692 | 0 | 0 | 0 | 0 | 515918 | 0 | 3298416 | 0 | 1786822 | 0 | 975339 | 0 | 0 | 9983476 | 0 | 2671773 | 2401809 | 0 | 0 | 0 |
| BUG-0098-admin-filter-dropdown-ui-consistency | 0 | 468997 | 0 | 0 | 0 | 0 | 279352 | 0 | 498816 | 0 | 886093 | 0 | 2006992 | 0 | 0 | 2624025 | 13267380 | 3399030 | 2149149 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 2061558 | 324203 | 0 | 0 | 414606 | 2642696 | 853302 | 6389215 | 652647 | 6054693 | 2057627 | 9994239 | 0 | 0 | 22661525 | 39732965 | 11444862 | 14365473 | 0 | 0 | 1094286 |
| sprint-015 | 0 | 2061558 | 324203 | 0 | 0 | 414606 | 2642696 | 853302 | 6389215 | 652647 | 6054693 | 2057627 | 9994239 | 0 | 0 | 22661525 | 39732965 | 11444862 | 14365473 | 0 | 0 | 1094286 |
| REQ-0086-miniapp-brand-list-ui-interaction-optimization | 0 | 0 | 324203 | 0 | 0 | 414606 | 0 | 853302 | 0 | 652647 | 0 | 2057627 | 0 | 0 | 0 | 2578290 | 6374455 | 1508719 | 1576256 | 0 | 0 | 0 |
| REQ-0006-tile-sku-management | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1254236 | 0 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 414606 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0096-admin-sku-category-filter-only-top-level | 0 | 502386 | 0 | 0 | 0 | 0 | 850328 | 0 | 1688388 | 0 | 1725869 | 0 | 2747527 | 0 | 0 | 3953973 | 11367231 | 1254236 | 3587442 | 0 | 0 | 0 |
| BUG-0097-admin-sku-material-main-image-tag-redundant | 0 | 359797 | 0 | 0 | 0 | 0 | 725137 | 0 | 345064 | 0 | 745996 | 0 | 1248881 | 0 | 0 | 3603059 | 4859476 | 998900 | 2463929 | 0 | 0 | 0 |
| BUG-0095-admin-category-tree-count-shows-product-count | 0 | 479873 | 0 | 0 | 0 | 0 | 276684 | 0 | 578806 | 0 | 916347 | 0 | 3057347 | 0 | 0 | 0 | 3931919 | 1626180 | 2214833 | 0 | 0 | 0 |
| BUG-0094-miniapp-list-images-not-loading-after-speed-fix | 0 | 254365 | 0 | 0 | 0 | 0 | 513506 | 0 | 3281920 | 0 | 1783688 | 0 | 942120 | 0 | 0 | 9938464 | 0 | 2664134 | 2383543 | 0 | 0 | 0 |
| BUG-0098-admin-filter-dropdown-ui-consistency | 0 | 465137 | 0 | 0 | 0 | 0 | 277041 | 0 | 495037 | 0 | 882793 | 0 | 1998364 | 0 | 0 | 2587739 | 13199884 | 3392693 | 2139470 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 17576 | 3465 | 0 | 0 | 5458 | 15895 | 8203 | 37392 | 2685 | 17029 | 10142 | 47145 | 0 | 0 | 83577 | 133982 | 22580 | 59769 | 0 | 0 | 7159 |
| sprint-015 | 0 | 17576 | 3465 | 0 | 0 | 5458 | 15895 | 8203 | 37392 | 2685 | 17029 | 10142 | 47145 | 0 | 0 | 83577 | 133982 | 22580 | 59769 | 0 | 0 | 7159 |
| REQ-0086-miniapp-brand-list-ui-interaction-optimization | 0 | 0 | 3465 | 0 | 0 | 5458 | 0 | 8203 | 0 | 2685 | 0 | 10142 | 0 | 0 | 0 | 15703 | 14387 | 2089 | 7531 | 0 | 0 | 0 |
| REQ-0006-tile-sku-management | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1496 | 0 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 5458 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0096-admin-sku-category-filter-only-top-level | 0 | 4043 | 0 | 0 | 0 | 0 | 4045 | 0 | 9252 | 0 | 4056 | 0 | 10120 | 0 | 0 | 22195 | 27222 | 1496 | 8623 | 0 | 0 | 0 |
| BUG-0097-admin-sku-material-main-image-tag-redundant | 0 | 2466 | 0 | 0 | 0 | 0 | 4769 | 0 | 3638 | 0 | 3339 | 0 | 7551 | 0 | 0 | 9643 | 26256 | 2504 | 8334 | 0 | 0 | 0 |
| BUG-0095-admin-category-tree-count-shows-product-count | 0 | 3880 | 0 | 0 | 0 | 0 | 2358 | 0 | 4227 | 0 | 3200 | 0 | 11070 | 0 | 0 | 0 | 20529 | 2515 | 7336 | 0 | 0 | 0 |
| BUG-0094-miniapp-list-images-not-loading-after-speed-fix | 0 | 3327 | 0 | 0 | 0 | 0 | 2412 | 0 | 16496 | 0 | 3134 | 0 | 9776 | 0 | 0 | 20880 | 0 | 7639 | 18266 | 0 | 0 | 0 |
| BUG-0098-admin-filter-dropdown-ui-consistency | 0 | 3860 | 0 | 0 | 0 | 0 | 2311 | 0 | 3779 | 0 | 3300 | 0 | 8628 | 0 | 0 | 15156 | 45588 | 6337 | 9679 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | 0 | 41 | 8 | 0 | 0 | 6 | 37 | 8 | 51 | 5 | 46 | 13 | 81 | 0 | 0 | 174 | 295 | 89 | 86 | 0 | 0 | 16 |
| sprint-015 | 0 | 41 | 8 | 0 | 0 | 6 | 37 | 8 | 51 | 5 | 46 | 13 | 81 | 0 | 0 | 174 | 295 | 89 | 86 | 0 | 0 | 16 |
| REQ-0086-miniapp-brand-list-ui-interaction-optimization | 0 | 0 | 8 | 0 | 0 | 6 | 0 | 8 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 29 | 46 | 9 | 8 | 0 | 0 | 0 |
| REQ-0006-tile-sku-management | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 |
| REQ-0083-miniapp-brand-list-category-summary | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BUG-0096-admin-sku-category-filter-only-top-level | 0 | 10 | 0 | 0 | 0 | 0 | 10 | 0 | 14 | 0 | 11 | 0 | 15 | 0 | 0 | 41 | 61 | 9 | 16 | 0 | 0 | 0 |
| BUG-0097-admin-sku-material-main-image-tag-redundant | 0 | 5 | 0 | 0 | 0 | 0 | 15 | 0 | 5 | 0 | 9 | 0 | 12 | 0 | 0 | 20 | 44 | 10 | 17 | 0 | 0 | 0 |
| BUG-0095-admin-category-tree-count-shows-product-count | 0 | 10 | 0 | 0 | 0 | 0 | 4 | 0 | 7 | 0 | 9 | 0 | 23 | 0 | 0 | 0 | 35 | 11 | 13 | 0 | 0 | 0 |
| BUG-0094-miniapp-list-images-not-loading-after-speed-fix | 0 | 6 | 0 | 0 | 0 | 0 | 4 | 0 | 19 | 0 | 8 | 0 | 16 | 0 | 0 | 52 | 0 | 27 | 21 | 0 | 0 | 0 |
| BUG-0098-admin-filter-dropdown-ui-consistency | 0 | 10 | 0 | 0 | 0 | 0 | 4 | 0 | 6 | 0 | 9 | 0 | 15 | 0 | 0 | 32 | 109 | 23 | 11 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| 管理端筛选下拉横切统一 | high | BUG-0098 覆盖品牌、类目、规格、证书、Banner、用户、设置、日志、接口文档、主题等页面 | 以共享筛选控件和页面 smoke 清单替代逐页重新分析，输出只保留失败页面摘要 |
| 小程序商品卡片媒体链路 | high | BUG-0094 覆盖后端 `cover_image`、对象存储缩略图、历史回填、小程序商品卡片 | 建立媒体类 BUG 标准证据模板，按 API、storage、miniapp、audit 四段读取 |
| Sprint 四件套 | medium | Fact Sheet token_risks 标记 `sprint.md` 超 200 行 | 复盘和归档优先用 Fact Sheet summary，仅对 stale 文案和回链做局部读取 |
| OpenSpec archive lookup | medium | 6 Change，109/109 tasks，archive paths 需 resolver 解析 | 使用 readiness、Fact Sheet 和 residual gate，避免宽泛扫描 `openspec/archive/**` |
| AI usage snapshot 中途刷新 | medium | 初次 summary stale，hook 后 actual | 在 `/sprint-archive` 后立刻检查 summary；若仍 stale，先刷新再进入 `/sprint-exps` 正文生成 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，没有默认展开全部四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 Sprint Fact Sheet、residual JSON、上期复盘样式、知识库索引和必要最佳实践片段 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 需要修正 | 是 | `/sprint-exps` 前应确保 AI usage snapshot 为 actual/present，否则只能输出估算分析 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-015-001 | P1 | 为 `/sprint-archive` 或 `/sprint-exps` 增加 AI usage snapshot fresh gate：summary 若 stale，先刷新后再生成复盘正文 | `/opsx-propose` | open |
| T-015-002 | P1 | 管理端筛选下拉统一纳入 `admin-list-page-consistency` apply 前置检查，新增页面不得保留页面级下拉样式分化 | `/opsx-propose` | open |
| T-015-003 | P1 | 媒体类 BUG 建立“URL 可访问 / 对象存在 / 小程序渲染 / 性能懒加载”四联验收模板 | `/req-capture` | open |
| T-015-004 | P2 | `/sprint-archive` 后自动扫描 release-note / acceptance / sprint.md 中的中间态文案并生成修正建议 | `/opsx-propose` | open |
| T-015-005 | P2 | 小程序 DevTools / 真机 / 体验版 evidence 独立进入 release-prepare checklist，避免 archive 后被遗忘 | `/req-capture` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| 本 Sprint 以修复型范围为主 | 5 个 BUG + 1 个体验优化，范围清晰且容量健康 | 后续修复型 Sprint 继续保持 50% 以上 fix buffer，承接突发问题 |
| REQ-0086 与 BUG-0094 都涉及小程序列表体验 | 品牌入口、类目入口、商品卡片图片、TabBar/安全区需要统一视口和设备证据 | 小程序列表类需求在 proposal 阶段就写清点击区域、媒体字段、空态、设备 evidence |
| BUG-0098 暴露管理端筛选区设计债 | 横跨多页面的视觉一致性不适合靠单页 CSS 修补 | 统一筛选控件应成为 Design System / shared admin UI 的稳定能力 |
| BUG-0096 与 BUG-0095 都依赖类目树语义 | 类目筛选子树、直接子类目数量、顶层数量必须区分清楚 | 类目相关需求要显式写明“商品数量”和“子类目数量”的字段语义 |
| BUG-0094 是性能优化后的回归 | 优化不能只看加载速度，还要验证真实图片展示与 fallback | 媒体性能需求必须同时设计可访问性验收 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / Orval | SKU 类目筛选、类目树计数、品牌列表类目 ID、公开列表 `cover_image` 都有潜在接口语义 | 任何参数语义或响应字段变化必须同步 OpenAPI、Orval、docs 和测试 |
| Web UI | 管理端筛选下拉统一覆盖多页面，局部样式容易遗漏 | 优先使用 shared admin filter select，页面只配置字段，不重写弹层样式 |
| 小程序 UI | 品牌卡片上行和类目胶囊点击边界需要阻止误触 | 关键点击区域必须有静态测试或 DevTools evidence |
| 媒体 / MinIO | 缩略图路径策略必须与公开 URL 访问策略一致 | 回填脚本必须 dry-run、可重入、输出统计摘要且不泄露本机路径或密钥 |
| 归档质量 | readiness PASS、residual 0、6/6 trace present | 继续保持 archive 后 residual gate 和 Workflow Sync 必跑 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Admin filter select | BUG-0098 | 固化为管理端筛选区唯一入口，统一触发框、弹层、选项、重置、空态、加载态和窄屏行为 |
| Category tree semantics | BUG-0096 / BUG-0095 | 建立“筛选子树”和“直接子类目数量”的字段说明与测试 fixture，避免商品数量误绑 |
| Miniapp product media evidence | BUG-0094 | 沉淀商品卡片媒体链路验收模板：公开 API、对象存储、缩略图、fallback、lazy-load |
| Miniapp brand card interaction | REQ-0086 | 品牌卡片结构复用上行品牌入口 + 下行类目胶囊入口，点击边界作为组件契约 |

## 6. 行动项

| ID | 优先级 | 类型 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------|------------|------|
| T-015-001 | P1 | workflow | AI usage snapshot fresh gate，避免复盘只能输出 estimated_fallback | `/opsx-propose` | open |
| T-015-002 | P1 | best-practice | 管理端筛选下拉统一 gate 进入最佳实践与 apply checklist | `/opsx-propose` | open |
| T-015-003 | P1 | requirement | 媒体类 BUG 四联验收模板 | `/req-capture` | open |
| T-015-004 | P2 | workflow | close-time stale scan 自动检查归档文档中间态文案 | `/opsx-propose` | open |
| T-015-005 | P2 | release | 小程序设备 evidence 进入 release-prepare checklist | `/req-capture` | open |

## 7. 回链

- Sprint：`iterations/archive/sprint-015/`
- 归档 Change：`openspec/archive/2026-07-31-fix-admin-sku-category-cascade-filter/`、`openspec/archive/2026-07-31-fix-admin-sku-material-main-image-tag/`、`openspec/archive/2026-07-31-fix-admin-category-tree-count/`、`openspec/archive/2026-07-31-update-miniapp-brand-list-ui-interaction-optimization/`、`openspec/archive/2026-07-31-fix-miniapp-product-card-thumbnails/`、`openspec/archive/2026-07-31-fix-admin-filter-dropdown-ui-consistency/`
- 相关最佳实践：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md`、`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
