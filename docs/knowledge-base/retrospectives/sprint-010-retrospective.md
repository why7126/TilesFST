---
sprint_id: sprint-010
title: Sprint 010 迭代经验复盘
status: draft
created_at: 2026-07-22 11:32:00
updated_at: 2026-07-22 20:25:00
owner: product
related_iteration: iterations/archive/sprint-010/
source: /sprint-exps sprint-010
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 010 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-08-17 09:00:00 ~ 2026-08-28 18:00:00 |
| REQ / BUG / Change | 6 / 10 / 16 |
| Change 批次 | 4 批；5、5、5、1 个 Change |
| tasks 完成度 | 298/298 |
| 估算 | 32 SP / 32.0 人天 |
| 容量 | 30 人天；占用 106.67%；fix buffer -6.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；16/16 Change archived，trace present |
| AI usage | Snapshot 已重建并包含矩阵；`check-snapshot` 为 `present/actual`，Fact Sheet 因 Sprint 日期口径仍有 `snapshot-stale` warning |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-010 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-010 --json`、`iterations/archive/sprint-010/sprint.yaml`、`iterations/archive/sprint-010/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 管理端规则与表单 | 密码策略简化、SKU 名称/编码语义、类目弹窗字段校验、SKU 图片移除与主图规则 |
| 小程序体验 | 多页面微信分享、SKU 详情品牌入口、分类长名称、usage-events 契约、重复品牌按钮修复 |
| 媒体与生产缺陷 | 上传大小限制一致性、生产 Banner 保存、主题偏好 Toast、品牌卡片路由 |
| 管理端体验治理 | 登录页工具区对齐、Dashboard 真实数据、Banner 图片完整预览、移动端基础适配 |

## 2. 流程复盘

### 做得好的

1. **归档闭环完整**：16 个 Change 全部进入 `openspec/changes/archive/`，298 个 task 全部完成，readiness 最终 PASS。
2. **大 Sprint 使用批次摘要控制上下文**：Fact Sheet 将 16 个 Change 分成 4 批，所有 batch blocker/warning 均为 0，复盘无需展开原始 tasks/trace。
3. **路径残留门禁有效**：归档关闭前后 residual check 都为 0，复盘不传播旧 `iterations/change/sprint-010/` 或 active Change 路径。
4. **Sprint 009 的经验被继续承接**：media-upload、admin-list、admin-modal、miniapp-custom-navigation 等 best-practice 被纳入横切验收。
5. **生产类问题拆分更清楚**：BUG-0076 因生产条件不足被移出 sprint-010，避免用 force-proceed 把未具备验收条件的项混进已完成范围。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| 范围仍偏大 | 16 个 Change、298 tasks、32.0/30.0 人天 | apply/archive/exps 都需要依赖 Fact Sheet 控制上下文，人工复核压力高 |
| fix 比例偏高 | 10 个 BUG，覆盖小程序、管理端、上传、生产 DB/API | 说明上游验收矩阵和发布前 smoke 仍需前置 |
| acceptance 正文仍有滞后语义 | Fact Sheet acceptance signals 中仍出现“待实现”“待归档”等旧结论 | Scope 已 done，但验收正文可能误导发布判断 |
| AI usage freshness 口径不稳定 | `check-snapshot` 为 `present/actual`，但 Fact Sheet summary 因 Sprint `end_date` 晚于归档时间标记 `snapshot-stale` | 复盘可使用矩阵统计，但工具链 freshness gate 仍需修正 |
| 多端 evidence 仍依赖人工确认 | 小程序分享、生产 smoke、真机 evidence 多处仍需要 release 前确认 | 发布准备阶段可能继续补证据，容易挤压发布节奏 |

### 优化建议

1. **下一轮 12+ Change 强制输出“可移出项”**：容量超过 100% 时，`sprint-propose` 应同步列出替换/移出候选，避免后期只靠归档门禁兜底。
2. **验收正文 stale phrase 脚本化**：扫描 acceptance-report 中已 archived 行仍写“待实现/待归档/待验收”的情况。
3. **生产 smoke 在 apply 中段落盘**：涉及生产 DB、上传、主题偏好、Banner 保存和真实数据的 Change，不等 archive 才补证据。
4. **把 Dashboard/列表/弹窗/上传横切测试继续组件化**：减少每个 fix Change 重写类似验收和断言。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-010.json`，由脱敏 command-runs 聚合；当前 snapshot 纳入 Sprint scope 的 REQ/BUG/Change 记录 |
| 聚合口径 | Sprint scope | 命中 `sprint_id=sprint-010`，或命中 `iterations/archive/sprint-010/sprint.yaml` 中的 REQ/BUG/Change，均纳入 Sprint snapshot |
| command run 数 | 118 | Sprint snapshot totals |
| 模型调用次数 | 1484 | Sprint snapshot totals |
| 工具调用次数 | 3110 | Sprint snapshot totals |
| input tokens | 185240677 | Sprint snapshot totals |
| cached input tokens | 175099008 | Sprint snapshot totals |
| output tokens | 831062 | Sprint snapshot totals |
| reasoning output tokens | 69842 | Sprint snapshot totals |
| total tokens | 186259048 | Sprint snapshot totals |
| retry count | 0 | Sprint snapshot totals |
| 非零命令列 | 15 类 | `bug.capture`、`bug.generate`、`bug.complete`、`bug.review`、`bug.opsx`、`req.capture`、`req.generate`、`req.complete`、`req.review`、`req.opsx`、`opsx.apply`、`opsx.archive`、`sprint.propose`、`sprint.archive`、`sprint.exps` |
| 仍为 0 的列 | Explore/Propose/Apply 部分 | 当前 `sprint-010` 归属数据中未发现 `req.explore`、`bug.explore`、`opsx.explore`、`opsx.propose`、`sprint.explore`、`sprint.apply` 等 workflow_event |
| 已采用节省策略 | 有 | 先 `--summary`，按 `needs_detail=false` 不读取 evidence hints；大 Sprint 使用 batch summary；残留检查脚本化 |

> 矩阵口径：`Total` 与 `sprint-010` 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图。同一 command run 关联多个 REQ/BUG 时会计入多个对象行，因此对象行不应直接相加后与 `Total` 比较。Token Usage Fact Sheet 的 totals 包含 `sprint.exps` 记录；矩阵列严格按规范命令列表展示，不包含 `Sprint-Exps` 列，因此矩阵列合计会小于 totals。

### 总 Token 消耗数 `total_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 3639468 | 1744845 | 0 | 0 | 1439986 | 5262610 | 3950549 | 5418167 | 4929887 | 9385883 | 12242484 | 20775055 | 0 | 0 | 57330804 | 23291085 | 33177918 | 0 | 0 | 1565523 |
| sprint-010 | 0 | 3639468 | 1744845 | 0 | 0 | 1439986 | 5262610 | 3950549 | 5418167 | 4929887 | 9385883 | 12242484 | 20775055 | 0 | 0 | 57330804 | 23291085 | 33177918 | 0 | 0 | 1565523 |
| REQ-0063-password-validation-policy-simplification | 0 | 0 | 308423 | 0 | 0 | 308818 | 0 | 766665 | 0 | 642056 | 0 | 1885638 | 0 | 0 | 0 | 0 | 1416726 | 2256802 | 0 | 0 | 0 |
| REQ-0064-miniapp-wechat-share-pages | 0 | 0 | 271908 | 0 | 0 | 322830 | 0 | 650692 | 0 | 1257733 | 0 | 3046099 | 0 | 0 | 0 | 3822028 | 2217204 | 1331651 | 0 | 0 | 0 |
| REQ-0027-mobile-page-adaptation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5999580 | 597537 | 1175829 | 0 | 0 | 0 |
| REQ-0065-sku-metadata-name-sku-dedup | 0 | 0 | 287702 | 0 | 0 | 288814 | 0 | 1420823 | 0 | 1359036 | 0 | 2920739 | 0 | 0 | 0 | 10137244 | 884017 | 1304469 | 0 | 0 | 0 |
| REQ-0067-admin-category-edit-modal-validation | 0 | 0 | 488156 | 0 | 0 | 519524 | 0 | 1112369 | 0 | 1671062 | 0 | 2059343 | 0 | 0 | 0 | 8254699 | 783133 | 1427845 | 0 | 0 | 0 |
| REQ-0066-admin-sku-image-removal-main-image-rules | 0 | 0 | 388656 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2330665 | 0 | 0 | 0 | 4948934 | 2710551 | 1366203 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1137683 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 272977 | 0 | 0 | 0 | 0 | 592840 | 0 | 398568 | 0 | 773625 | 0 | 1544718 | 0 | 0 | 0 | 1137683 | 1749163 | 0 | 0 | 0 |
| BUG-0071-login-page-theme-language-selector-misalignment | 0 | 314532 | 0 | 0 | 0 | 0 | 853816 | 0 | 375288 | 0 | 861236 | 0 | 2192441 | 0 | 0 | 5365830 | 2799874 | 0 | 0 | 0 | 0 |
| BUG-0072-miniapp-usage-events-bad-request | 0 | 399196 | 0 | 0 | 0 | 0 | 818304 | 0 | 577727 | 0 | 1445093 | 0 | 2314999 | 0 | 0 | 0 | 2796190 | 0 | 0 | 0 | 0 |
| BUG-0073-video-upload-23m-file-fails | 0 | 303143 | 0 | 0 | 0 | 0 | 73731 | 0 | 0 | 0 | 1124847 | 0 | 0 | 0 | 0 | 5680992 | 1047630 | 3296213 | 0 | 0 | 0 |
| BUG-0074-prod-theme-preference-sync-toast-persistent | 0 | 366953 | 0 | 0 | 0 | 0 | 415499 | 0 | 603422 | 0 | 1262441 | 0 | 3685567 | 0 | 0 | 1713110 | 1366250 | 1652034 | 0 | 0 | 0 |
| BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 0 | 400133 | 0 | 0 | 0 | 0 | 785891 | 0 | 768267 | 0 | 1297906 | 0 | 3689970 | 0 | 0 | 0 | 1365468 | 2081993 | 0 | 0 | 0 |
| BUG-0077-miniapp-category-secondary-name-truncated | 0 | 367442 | 0 | 0 | 0 | 0 | 745646 | 0 | 693258 | 0 | 1266498 | 0 | 1561153 | 0 | 0 | 565116 | 1051153 | 5772499 | 0 | 0 | 0 |
| BUG-0075-prod-admin-brand-banner-save-fails | 0 | 418860 | 0 | 0 | 0 | 0 | 785891 | 0 | 1216685 | 0 | 0 | 0 | 1527407 | 0 | 0 | 5667054 | 3499913 | 1636933 | 0 | 0 | 0 |
| BUG-0079-admin-dashboard-overview-mock-data | 0 | 262740 | 0 | 0 | 0 | 0 | 211664 | 0 | 250214 | 0 | 753295 | 0 | 1433365 | 0 | 0 | 5100382 | 0 | 887123 | 0 | 0 | 0 |
| BUG-0080-admin-banner-image-preview-cropped | 0 | 533492 | 0 | 0 | 0 | 0 | 1093167 | 0 | 534738 | 0 | 600942 | 0 | 2825435 | 0 | 0 | 1738837 | 665386 | 3624877 | 0 | 0 | 0 |
| BUG-0076-prod-miniapp-video-temporarily-unplayable | 0 | 0 | 0 | 0 | 0 | 0 | 73731 | 0 | 693258 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3614284 | 0 | 0 | 0 |

### 总输入 Token 消耗数 `input_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 3600578 | 1727471 | 0 | 0 | 1424926 | 5237291 | 3915277 | 5379194 | 4916389 | 9355677 | 12168050 | 20675047 | 0 | 0 | 57068598 | 23220182 | 32900362 | 0 | 0 | 1559265 |
| sprint-010 | 0 | 3600578 | 1727471 | 0 | 0 | 1424926 | 5237291 | 3915277 | 5379194 | 4916389 | 9355677 | 12168050 | 20675047 | 0 | 0 | 57068598 | 23220182 | 32900362 | 0 | 0 | 1559265 |
| REQ-0063-password-validation-policy-simplification | 0 | 0 | 304811 | 0 | 0 | 305325 | 0 | 759362 | 0 | 639911 | 0 | 1874886 | 0 | 0 | 0 | 0 | 1414465 | 2250494 | 0 | 0 | 0 |
| REQ-0064-miniapp-wechat-share-pages | 0 | 0 | 269359 | 0 | 0 | 318482 | 0 | 642336 | 0 | 1254386 | 0 | 3035509 | 0 | 0 | 0 | 3799637 | 2214303 | 1295655 | 0 | 0 | 0 |
| REQ-0027-mobile-page-adaptation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5967154 | 594810 | 1164300 | 0 | 0 | 0 |
| REQ-0065-sku-metadata-name-sku-dedup | 0 | 0 | 284344 | 0 | 0 | 285368 | 0 | 1410779 | 0 | 1355846 | 0 | 2907705 | 0 | 0 | 0 | 10110538 | 861816 | 1273472 | 0 | 0 | 0 |
| REQ-0067-admin-category-edit-modal-validation | 0 | 0 | 484093 | 0 | 0 | 515751 | 0 | 1102800 | 0 | 1666246 | 0 | 2027910 | 0 | 0 | 0 | 8230246 | 781116 | 1414360 | 0 | 0 | 0 |
| REQ-0066-admin-sku-image-removal-main-image-rules | 0 | 0 | 384864 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2322040 | 0 | 0 | 0 | 4932754 | 2699314 | 1335077 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1135602 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 269744 | 0 | 0 | 0 | 0 | 590028 | 0 | 394782 | 0 | 770431 | 0 | 1537722 | 0 | 0 | 0 | 1135602 | 1737281 | 0 | 0 | 0 |
| BUG-0071-login-page-theme-language-selector-misalignment | 0 | 311263 | 0 | 0 | 0 | 0 | 850051 | 0 | 371926 | 0 | 858039 | 0 | 2183052 | 0 | 0 | 5332225 | 2793783 | 0 | 0 | 0 | 0 |
| BUG-0072-miniapp-usage-events-bad-request | 0 | 395113 | 0 | 0 | 0 | 0 | 814540 | 0 | 572746 | 0 | 1441802 | 0 | 2306447 | 0 | 0 | 0 | 2792065 | 0 | 0 | 0 | 0 |
| BUG-0073-video-upload-23m-file-fails | 0 | 299330 | 0 | 0 | 0 | 0 | 73226 | 0 | 0 | 0 | 1121487 | 0 | 0 | 0 | 0 | 5663138 | 1038687 | 3278189 | 0 | 0 | 0 |
| BUG-0074-prod-theme-preference-sync-toast-persistent | 0 | 362958 | 0 | 0 | 0 | 0 | 412973 | 0 | 598616 | 0 | 1259027 | 0 | 3674377 | 0 | 0 | 1701666 | 1363835 | 1623796 | 0 | 0 | 0 |
| BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 0 | 396415 | 0 | 0 | 0 | 0 | 783240 | 0 | 763853 | 0 | 1294632 | 0 | 3681263 | 0 | 0 | 0 | 1362636 | 2074558 | 0 | 0 | 0 |
| BUG-0077-miniapp-category-secondary-name-truncated | 0 | 362952 | 0 | 0 | 0 | 0 | 741796 | 0 | 688372 | 0 | 1262178 | 0 | 1554009 | 0 | 0 | 562871 | 1048414 | 5748585 | 0 | 0 | 0 |
| BUG-0075-prod-admin-brand-banner-save-fails | 0 | 414816 | 0 | 0 | 0 | 0 | 783240 | 0 | 1211560 | 0 | 0 | 0 | 1495225 | 0 | 0 | 5644154 | 3494959 | 1618205 | 0 | 0 | 0 |
| BUG-0079-admin-dashboard-overview-mock-data | 0 | 259569 | 0 | 0 | 0 | 0 | 209750 | 0 | 247147 | 0 | 749964 | 0 | 1425412 | 0 | 0 | 5057115 | 0 | 878662 | 0 | 0 | 0 |
| BUG-0080-admin-banner-image-preview-cropped | 0 | 528418 | 0 | 0 | 0 | 0 | 1088601 | 0 | 530192 | 0 | 598117 | 0 | 2817540 | 0 | 0 | 1714221 | 663064 | 3612478 | 0 | 0 | 0 |
| BUG-0076-prod-miniapp-video-temporarily-unplayable | 0 | 0 | 0 | 0 | 0 | 0 | 73226 | 0 | 688372 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3595250 | 0 | 0 | 0 |

### 总输出 Token 消耗数 `output_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 38890 | 17374 | 0 | 0 | 15060 | 25319 | 35272 | 38973 | 13498 | 30206 | 53072 | 79181 | 0 | 0 | 220525 | 51041 | 193979 | 0 | 0 | 6258 |
| sprint-010 | 0 | 38890 | 17374 | 0 | 0 | 15060 | 25319 | 35272 | 38973 | 13498 | 30206 | 53072 | 79181 | 0 | 0 | 220525 | 51041 | 193979 | 0 | 0 | 6258 |
| REQ-0063-password-validation-policy-simplification | 0 | 0 | 3612 | 0 | 0 | 3493 | 0 | 7303 | 0 | 2145 | 0 | 10752 | 0 | 0 | 0 | 0 | 2261 | 6308 | 0 | 0 | 0 |
| REQ-0064-miniapp-wechat-share-pages | 0 | 0 | 2549 | 0 | 0 | 4348 | 0 | 8356 | 0 | 3347 | 0 | 10590 | 0 | 0 | 0 | 22391 | 2901 | 14642 | 0 | 0 | 0 |
| REQ-0027-mobile-page-adaptation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 32426 | 2727 | 11529 | 0 | 0 | 0 |
| REQ-0065-sku-metadata-name-sku-dedup | 0 | 0 | 3358 | 0 | 0 | 3446 | 0 | 10044 | 0 | 3190 | 0 | 13034 | 0 | 0 | 0 | 26706 | 2339 | 10034 | 0 | 0 | 0 |
| REQ-0067-admin-category-edit-modal-validation | 0 | 0 | 4063 | 0 | 0 | 3773 | 0 | 9569 | 0 | 4816 | 0 | 10071 | 0 | 0 | 0 | 24453 | 2017 | 13485 | 0 | 0 | 0 |
| REQ-0066-admin-sku-image-removal-main-image-rules | 0 | 0 | 3792 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8625 | 0 | 0 | 0 | 16180 | 11237 | 10057 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2081 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 3233 | 0 | 0 | 0 | 0 | 2812 | 0 | 3786 | 0 | 3194 | 0 | 6996 | 0 | 0 | 0 | 2081 | 11882 | 0 | 0 | 0 |
| BUG-0071-login-page-theme-language-selector-misalignment | 0 | 3269 | 0 | 0 | 0 | 0 | 3765 | 0 | 3362 | 0 | 3197 | 0 | 9389 | 0 | 0 | 33605 | 6091 | 0 | 0 | 0 | 0 |
| BUG-0072-miniapp-usage-events-bad-request | 0 | 4083 | 0 | 0 | 0 | 0 | 3764 | 0 | 4981 | 0 | 3291 | 0 | 8552 | 0 | 0 | 0 | 4125 | 0 | 0 | 0 | 0 |
| BUG-0073-video-upload-23m-file-fails | 0 | 3813 | 0 | 0 | 0 | 0 | 505 | 0 | 0 | 0 | 3360 | 0 | 0 | 0 | 0 | 17854 | 8943 | 18024 | 0 | 0 | 0 |
| BUG-0074-prod-theme-preference-sync-toast-persistent | 0 | 3995 | 0 | 0 | 0 | 0 | 2526 | 0 | 4806 | 0 | 3414 | 0 | 11190 | 0 | 0 | 11444 | 2415 | 8047 | 0 | 0 | 0 |
| BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 0 | 3718 | 0 | 0 | 0 | 0 | 2651 | 0 | 4414 | 0 | 3274 | 0 | 8707 | 0 | 0 | 0 | 2832 | 7435 | 0 | 0 | 0 |
| BUG-0077-miniapp-category-secondary-name-truncated | 0 | 4490 | 0 | 0 | 0 | 0 | 3850 | 0 | 4886 | 0 | 4320 | 0 | 7144 | 0 | 0 | 2245 | 2739 | 23914 | 0 | 0 | 0 |
| BUG-0075-prod-admin-brand-banner-save-fails | 0 | 4044 | 0 | 0 | 0 | 0 | 2651 | 0 | 5125 | 0 | 0 | 0 | 11355 | 0 | 0 | 22900 | 4954 | 18728 | 0 | 0 | 0 |
| BUG-0079-admin-dashboard-overview-mock-data | 0 | 3171 | 0 | 0 | 0 | 0 | 1914 | 0 | 3067 | 0 | 3331 | 0 | 7953 | 0 | 0 | 21300 | 0 | 8461 | 0 | 0 | 0 |
| BUG-0080-admin-banner-image-preview-cropped | 0 | 5074 | 0 | 0 | 0 | 0 | 4566 | 0 | 4546 | 0 | 2825 | 0 | 7895 | 0 | 0 | 4902 | 2322 | 12399 | 0 | 0 | 0 |
| BUG-0076-prod-miniapp-video-temporarily-unplayable | 0 | 0 | 0 | 0 | 0 | 0 | 505 | 0 | 4886 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19034 | 0 | 0 | 0 |

### 模型调用次数 `model_call_count`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 81 | 40 | 0 | 0 | 15 | 61 | 31 | 46 | 32 | 78 | 68 | 143 | 0 | 0 | 451 | 169 | 232 | 0 | 0 | 21 |
| sprint-010 | 0 | 81 | 40 | 0 | 0 | 15 | 61 | 31 | 46 | 32 | 78 | 68 | 143 | 0 | 0 | 451 | 169 | 232 | 0 | 0 | 21 |
| REQ-0063-password-validation-policy-simplification | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 7 | 0 | 5 | 0 | 12 | 0 | 0 | 0 | 0 | 9 | 10 | 0 | 0 | 0 |
| REQ-0064-miniapp-wechat-share-pages | 0 | 0 | 7 | 0 | 0 | 4 | 0 | 6 | 0 | 9 | 0 | 16 | 0 | 0 | 0 | 34 | 11 | 17 | 0 | 0 | 0 |
| REQ-0027-mobile-page-adaptation | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 40 | 12 | 16 | 0 | 0 | 0 |
| REQ-0065-sku-metadata-name-sku-dedup | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 11 | 0 | 9 | 0 | 16 | 0 | 0 | 0 | 73 | 10 | 14 | 0 | 0 | 0 |
| REQ-0067-admin-category-edit-modal-validation | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 7 | 0 | 9 | 0 | 12 | 0 | 0 | 0 | 48 | 9 | 18 | 0 | 0 | 0 |
| REQ-0066-admin-sku-image-removal-main-image-rules | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 0 | 0 | 0 | 33 | 16 | 15 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 |
| BUG-0070-miniapp-sku-detail-duplicate-brand-button | 0 | 7 | 0 | 0 | 0 | 0 | 9 | 0 | 5 | 0 | 8 | 0 | 13 | 0 | 0 | 0 | 8 | 11 | 0 | 0 | 0 |
| BUG-0071-login-page-theme-language-selector-misalignment | 0 | 8 | 0 | 0 | 0 | 0 | 11 | 0 | 4 | 0 | 8 | 0 | 15 | 0 | 0 | 63 | 18 | 0 | 0 | 0 | 0 |
| BUG-0072-miniapp-usage-events-bad-request | 0 | 9 | 0 | 0 | 0 | 0 | 8 | 0 | 4 | 0 | 9 | 0 | 12 | 0 | 0 | 0 | 18 | 0 | 0 | 0 | 0 |
| BUG-0073-video-upload-23m-file-fails | 0 | 7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 49 | 8 | 15 | 0 | 0 | 0 |
| BUG-0074-prod-theme-preference-sync-toast-persistent | 0 | 8 | 0 | 0 | 0 | 0 | 4 | 0 | 5 | 0 | 9 | 0 | 20 | 0 | 0 | 24 | 10 | 9 | 0 | 0 | 0 |
| BUG-0078-prod-miniapp-sku-detail-brand-card-routes-search | 0 | 8 | 0 | 0 | 0 | 0 | 7 | 0 | 6 | 0 | 9 | 0 | 21 | 0 | 0 | 0 | 10 | 10 | 0 | 0 | 0 |
| BUG-0077-miniapp-category-secondary-name-truncated | 0 | 8 | 0 | 0 | 0 | 0 | 9 | 0 | 7 | 0 | 11 | 0 | 11 | 0 | 0 | 5 | 9 | 27 | 0 | 0 | 0 |
| BUG-0075-prod-admin-brand-banner-save-fails | 0 | 9 | 0 | 0 | 0 | 0 | 7 | 0 | 6 | 0 | 0 | 0 | 18 | 0 | 0 | 50 | 19 | 15 | 0 | 0 | 0 |
| BUG-0079-admin-dashboard-overview-mock-data | 0 | 7 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 10 | 0 | 14 | 0 | 0 | 39 | 0 | 6 | 0 | 0 | 0 |
| BUG-0080-admin-banner-image-preview-cropped | 0 | 10 | 0 | 0 | 0 | 0 | 12 | 0 | 5 | 0 | 5 | 0 | 19 | 0 | 0 | 12 | 10 | 18 | 0 | 0 | 0 |
| BUG-0076-prod-miniapp-video-temporarily-unplayable | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 0 | 0 | 0 |
### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Opsx-Apply | high | `total_tokens=57330804`、`model_call_count=451`，占 Sprint token 最大块 | 对 10+ Change 继续按 batch apply/archive；失败日志只保留关键段 |
| Sprint-Propose | high | `total_tokens=33177918`、`model_call_count=232`，规划阶段反复纳入 REQ/BUG/Change 造成高输入 | Sprint 范围变更时优先 diff scope，不重复全文读取 Issue 包 |
| Opsx-Archive | high | `total_tokens=23291085`、`model_call_count=169`，归档、Workflow Sync、残留检查集中发生 | 归档前置 readiness 摘要；避免展开 archive tasks/trace 全文 |
| BUG-Opsx | high | `total_tokens=20775055`、`model_call_count=143`，10 个 BUG 中多项进入 opsx | 复用 BUG→Change 模板，减少重复读取规则和 Issue 包 |
| REQ-Opsx | medium/high | `total_tokens=12242484`、`model_call_count=68` | 对相似 REQ 使用既有 proposal/design 模板和摘要复用 |
| Sprint 四件套 | high | Fact Sheet token_risks：2 个文件 >= 200 行 | 复盘默认只读 summary；只在写回链时读尾部片段 |
| acceptance 语义滞后 | medium | acceptance signals 暴露“待实现/待归档”旧语句 | 增加 stale phrase 检查，避免人工全文扫验收报告 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，未默认读取 Sprint 四件套全文 |
| 大 Sprint 批次化 | 符合 | 16 Change 使用 4 个 batch 摘要，batch warning/blocker 均为 0 |
| evidence hints 控制 | 符合 | `needs_detail=false`，未读取完整 evidence hints |
| 路径残留检查 | 符合 | 使用 `check-archived-path-residuals.py --json`，residual_count 0 |
| AI usage 矩阵 | 已修正 | 修复前只纳入 `sprint_id` 命中的 47 条记录；修复后按 Sprint scope 纳入 118 条记录，前置 REQ/BUG 命令列已恢复数值 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 修正 Fact Sheet freshness gate 对已归档但 `end_date` 晚于归档时间的 Sprint 判定，避免真实 snapshot 被标记 stale | `/bug-capture` | open |
| T-002 | P1 | 为 acceptance-report 增加 stale phrase 检查，识别已归档但正文仍写“待实现/待归档”的行 | `/opsx-propose` | open |
| T-003 | P2 | 对 10+ Change Sprint 的 exps/archive 输出固定 batch summary 模板，减少手工转述 | `/opsx-propose` | open |
| T-004 | P2 | 生产 smoke 与真机 evidence 在 apply 中段生成 evidence stub，archive 阶段只校验状态 | `/req-capture` | open |

## 3. 需求与设计

| 条目 | 经验 |
|------|------|
| REQ-0063 | 密码策略简化适合以统一校验函数为核心，避免修改密码、创建用户、重置密码三处漂移 |
| REQ-0064 | 小程序分享必须同时考虑页面路径、参数保留、朋友圈能力、运行入口同步和埋点失败不阻断 |
| REQ-0027 | 管理端移动端适配是横切治理，不适合和过多生产 BUG 一起扩张；但 smoke 矩阵可复用 |
| REQ-0065 | SKU 编码和商品名称的语义分离需要跨后端、管理端、小程序、店主端统一描述 |
| REQ-0067 | 类目编码自动生成与前端隐藏输入必须同步 OpenAPI/Orval/错误码和前后端测试 |
| REQ-0066 | 图片移除和主图兜底是前端状态机问题，适合用组件测试锁定 |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| 生产 smoke 标准还不够前置 | BUG-0074、BUG-0075、BUG-0079 仍依赖归档/发布前确认 | 在 Change tasks 里固定 smoke evidence 文件和 N/A 结论 |
| 验收正文与状态表不同步 | Scope done，但 acceptance 结论仍有旧词 | 建立 acceptance stale phrase gate |
| 小程序真机能力不可自动化 | 分享与部分页面 evidence 仍需人工 | 形成 `static_pass_devtools_unavailable` 和 `real_device_follow_up` 状态 |
| 多个管理端 UI fix 重复出现 | 登录、Banner、Dashboard、移动端、弹窗 | 继续沉淀 Admin UI smoke matrix 和组件级截图/测试策略 |

## 4. 开发与质量

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| 管理端 UI 细节反复修复 | BUG-0071、BUG-0080、REQ-0027 | 登录工具区、图片预览、移动端布局缺统一 smoke | 建立页面级视觉/响应式 smoke 清单 |
| 小程序路径和运行入口漂移 | REQ-0064、BUG-0078、BUG-0077 | `.ts` 源和 `.js` 运行入口、页面路径参数容易不一致 | 继续保留 runtime entry 静态测试和页面路径断言 |
| 上传链路多层配置漂移 | BUG-0073 | 前端提示、后端校验、系统设置、Nginx/代理和对象存储限制分散 | 复用 `admin-media-upload-chain`，把有效限制来源写进测试 |
| 生产 DB/API drift | BUG-0075、BUG-0079 | 本地 SQLite 通过不代表生产 MySQL/真实数据链路通过 | MySQL drift check 与真实数据 smoke 纳入发布前门禁 |
| 语义字段跨端漂移 | REQ-0065、REQ-0067 | 后端内部字段和公开展示字段职责不清 | 需求设计阶段明确“内部识别字段 / 用户填写字段 / 公开展示字段” |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 后端/API | 覆盖密码、上传、Banner、Dashboard、类目、SKU、MySQL drift 等路径 |
| Web 管理端 | 覆盖登录页、Dashboard、Banner、类目、SKU、移动端适配和弹窗状态机 |
| 小程序 | 覆盖分享入口、品牌路径、分类长名称、usage-events、运行入口和展示隐藏编码 |
| 归档质量 | readiness PASS、Workflow Sync Errors 0、residual_count 0 |
| 发布前证据 | 生产 smoke、真机 evidence 仍需在 release 阶段明确确认 |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| Admin UI smoke matrix | sprint-010 覆盖登录、Dashboard、SKU、品牌、用户、日志、系统设置等页面 | 抽成 `admin-mobile-smoke` 或 Playwright/组件测试 helper |
| Upload effective limit | BUG-0073 统一图片、视频、文档大小限制 | 继续把前端提示、后端设置和 Nginx 说明绑定校验 |
| Public display semantics | REQ-0065 将 SKU 编码隐藏为内部识别字段 | 为公开 API/小程序展示建立字段过滤 helper |
| Category/SKU modal state | REQ-0066/0067 都是弹窗状态与字段校验 | 形成通用 modal field validation/state-machine 测试模板 |
| Sprint Fact Sheet | summary 已支持 batch、token_risks、residuals、AI usage 矩阵 | 修复归档 Sprint freshness gate，并加入 acceptance stale signals |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P1 | 修复归档 Sprint 在 `end_date` 晚于归档时间时的 AI usage freshness gate 判定 | `/bug-capture` | 工具链 | open |
| A-002 | P1 | 增加 acceptance-report stale phrase gate，阻断已归档项仍写“待实现/待归档” | `/opsx-propose` | 工具链 | open |
| A-003 | P1 | 下一 Sprint 若容量超过 100%，必须在 `sprint.yaml` 或 `sprint.md` 列出可移出项和替换规则 | `/sprint-propose` | 产品 | open |
| A-004 | P2 | 将生产 smoke evidence stub 前置到 apply 中段，覆盖 DB drift、真实数据、上传和主题偏好 | `/req-capture` | 测试治理 | open |
| A-005 | P2 | 为管理端移动端/弹窗/列表建立共享 smoke matrix，减少 UI fix 重复验收成本 | `/req-capture` | Web 管理端 | open |
| A-006 | P2 | 为小程序页面路径、分享路径和 `.ts`/`.js` 运行入口同步建立统一 helper | `/opsx-propose` | 小程序 | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `docs/knowledge-base/retrospectives/sprint-010-retrospective.md` | 新建 | 本文档 |
| `docs/knowledge-base/README.md` | 更新 | 增加 sprint-010 复盘索引 |
| `iterations/archive/sprint-010/sprint.md` | 更新 | 增加复盘回链 |
