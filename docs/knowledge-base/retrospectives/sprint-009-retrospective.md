---
sprint_id: sprint-009
title: Sprint 009 迭代经验复盘
status: draft
created_at: 2026-07-20 23:33:49
updated_at: 2026-07-22 12:13:05
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
| AI usage | actual / present；coverage pass；warning_count 0；已按 Sprint scope 重新聚合 |

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
| AI usage 统计视图曾不一致 | 旧复盘口径曾把 summary 判断为 stale，但本次按 Sprint scope 重新聚合后为 actual / present | 说明统计问题来自聚合口径，不是 `data/ai-usage` 缺数据；后续需保持脚本测试覆盖 |

### 优化建议

1. **20+ 页面/组件级 Sprint 拆成两个迭代**：品牌/证书/收藏链路与后台 Banner/证书组件最好分开，避免管理端和小程序验收互相挤压。
2. **设备 evidence 任务前置到 apply 阶段中段**：不要等 archive readiness 才补 320/375/430 pt evidence；没有 DevTools 时应提前生成 `blocked/follow_up/static_review` 记录。
3. **验收报告正文纳入 Workflow Sync 或专门校验**：Scope 表可自动同步，但 acceptance-report 的“待实现”句子需要规则或脚本扫描。
4. **AI usage summary 口径统一**：`generate-sprint-fact-sheet.py --summary` 应把 `estimated=false`、actual hook、warning 字段一致化。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-009.json`，由修复后的 Sprint scope 聚合生成 |
| AI usage mode | actual | snapshot 字段 `ai_usage_mode` |
| Snapshot status | present | snapshot 字段 `snapshot_status` |
| Command run 数 | 142 | snapshot totals |
| Model call 数 | 2,335 | snapshot totals |
| Tool call 数 | 4,827 | snapshot totals |
| Input tokens | 291,188,975 | snapshot totals |
| Cached input tokens | 277,085,952 | snapshot totals |
| Output tokens | 1,174,812 | snapshot totals |
| Reasoning output tokens | 111,807 | snapshot totals |
| Total tokens | 292,638,940 | snapshot totals |
| Retry count | 0 | snapshot totals |
| 非零命令列 | `BUG-Capture`、`REQ-Capture`、`REQ-Generate`、`BUG-Generate`、`REQ-Complete`、`BUG-Complete`、`REQ-Review`、`BUG-Review`、`REQ-Opsx`、`BUG-Opsx`、`Opsx-Apply`、`Opsx-Archive`、`Sprint-Propose`、`Sprint-Archive` | 按固定矩阵列统计；`sprint.exps` 等额外事件不进入矩阵列 |
| 仍为 0 的列 | `Capture`、`BUG-Explore`、`REQ-Explore`、`Opsx-Explore`、`Opsx-Propose`、`Sprint-Explore`、`Sprint-Apply` | 当前 Sprint scope 未匹配到这些固定命令列 |
| 矩阵外事件 | `release.prepare`、`release.propose`、`release.publish`、`req.archive`、`sprint.exps` | 已计入 totals，但不属于当前规范要求的横向列 |

说明：下列表格按 Sprint scope 聚合，除显式 `sprint_id` 外，也会纳入与本 Sprint 的 REQ、BUG、Change 关联的命令记录；同一需求或 BUG 的短 ID 与完整目录名会在 Sprint 内合并，避免重复行。

### 总Token消耗数【total_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 1,925,855 | 6,534,827 | 0 | 0 | 4,986,390 | 4,906,185 | 10,226,714 | 2,022,158 | 15,284,864 | 5,577,010 | 50,561,892 | 6,876,399 | 0 | 0 | 110,150,589 | 16,640,282 | 50,266,085 | 0 | 0 | 164,312 |
| sprint-009 | 0 | 1,925,855 | 6,534,827 | 0 | 0 | 4,986,390 | 4,906,185 | 10,226,714 | 2,022,158 | 15,284,864 | 5,577,010 | 50,561,892 | 6,876,399 | 0 | 0 | 110,150,589 | 16,640,282 | 50,266,085 | 0 | 0 | 164,312 |
| REQ-0049-miniapp-product-card-component | 0 | 0 | 388,782 | 0 | 0 | 410,526 | 0 | 787,055 | 0 | 1,335,655 | 0 | 4,609,431 | 0 | 0 | 0 | 0 | 2,410,605 | 1,031,362 | 0 | 0 | 0 |
| REQ-0050-miniapp-brand-header-page-title-rules | 0 | 0 | 211,946 | 0 | 0 | 304,642 | 0 | 743,677 | 0 | 1,438,226 | 0 | 0 | 0 | 0 | 0 | 15,621,481 | 711,312 | 1,728,129 | 0 | 0 | 0 |
| REQ-0051-category-list-product-list-entry-by-level | 0 | 0 | 242,215 | 0 | 0 | 209,453 | 0 | 444,662 | 0 | 1,218,099 | 0 | 0 | 0 | 0 | 0 | 6,927,202 | 1,670,788 | 1,528,201 | 0 | 0 | 0 |
| REQ-0052-miniapp-device-evidence-template | 0 | 0 | 285,487 | 0 | 0 | 273,629 | 0 | 1,086,464 | 0 | 1,454,401 | 0 | 3,829,910 | 0 | 0 | 0 | 2,592,843 | 3,325,812 | 2,080,998 | 0 | 0 | 0 |
| REQ-0053-miniapp-custom-navigation-best-practice | 0 | 0 | 416,648 | 0 | 0 | 339,689 | 0 | 808,989 | 0 | 1,254,498 | 0 | 5,320,425 | 0 | 0 | 0 | 1,773,819 | 0 | 1,331,661 | 0 | 0 | 0 |
| REQ-0054-brand-card-common-component | 0 | 0 | 186,417 | 0 | 0 | 336,277 | 0 | 661,549 | 0 | 1,327,739 | 0 | 6,322,275 | 0 | 0 | 0 | 2,166,634 | 821,499 | 1,656,846 | 0 | 0 | 0 |
| REQ-0055-brand-certificate-common-component | 0 | 0 | 573,065 | 0 | 0 | 365,487 | 0 | 991,405 | 0 | 1,357,884 | 0 | 3,063,175 | 0 | 0 | 0 | 10,728,997 | 659,490 | 4,272,757 | 0 | 0 | 0 |
| REQ-0056-product-list-card-only-layout | 0 | 0 | 384,995 | 0 | 0 | 353,697 | 0 | 933,050 | 0 | 1,175,326 | 0 | 5,044,248 | 0 | 0 | 0 | 2,944,766 | 927,149 | 1,931,688 | 0 | 0 | 0 |
| REQ-0057-certificate-list-page | 0 | 0 | 520,911 | 0 | 0 | 453,637 | 0 | 585,530 | 0 | 1,232,146 | 0 | 5,314,620 | 0 | 0 | 0 | 9,460,120 | 636,546 | 10,762,195 | 0 | 0 | 0 |
| REQ-0058-brand-detail-home-page | 0 | 0 | 951,655 | 0 | 0 | 418,965 | 0 | 679,166 | 0 | 685,920 | 0 | 2,897,739 | 0 | 0 | 0 | 11,517,219 | 590,103 | 3,314,043 | 0 | 0 | 0 |
| REQ-0059-favorite-list-page | 0 | 0 | 0 | 0 | 0 | 354,340 | 0 | 933,050 | 0 | 604,108 | 0 | 2,406,074 | 0 | 0 | 0 | 5,246,261 | 803,423 | 2,477,021 | 0 | 0 | 0 |
| REQ-0060-brand-list-page | 0 | 0 | 1,265,880 | 0 | 0 | 396,759 | 0 | 1,023,323 | 0 | 740,078 | 0 | 8,614,511 | 0 | 0 | 0 | 11,249,571 | 466,007 | 3,216,398 | 0 | 0 | 0 |
| REQ-0061-miniapp-share-add-guide | 0 | 0 | 407,908 | 0 | 0 | 292,344 | 0 | 603,797 | 0 | 618,299 | 0 | 4,551,645 | 0 | 0 | 0 | 4,954,197 | 205,393 | 4,559,814 | 0 | 0 | 0 |
| REQ-0062-admin-banner-placement-scope | 0 | 0 | 698,918 | 0 | 0 | 476,945 | 0 | 878,047 | 0 | 842,485 | 0 | 2,598,109 | 0 | 0 | 0 | 9,281,135 | 852,424 | 793,046 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,837,499 | 1,243,383 | 0 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7,247,066 | 0 | 0 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 440,939 | 0 | 0 | 0 | 0 | 1,346,225 | 0 | 670,870 | 0 | 1,332,113 | 0 | 2,345,518 | 0 | 0 | 7,247,066 | 0 | 2,645,678 | 0 | 0 | 0 |
| BUG-0067-home-recommendation-list-entry-routing | 0 | 443,929 | 0 | 0 | 0 | 0 | 1,029,622 | 0 | 763,290 | 0 | 1,257,051 | 0 | 2,345,518 | 0 | 0 | 3,601,779 | 254,541 | 2,013,736 | 0 | 0 | 0 |
| BUG-0068-miniapp-home-device-acceptance-followup | 0 | 513,165 | 0 | 0 | 0 | 0 | 947,956 | 0 | 0 | 0 | 1,329,151 | 599,161 | 0 | 0 | 0 | 6,927,202 | 3,207,200 | 1,403,366 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 527,822 | 0 | 0 | 0 | 0 | 1,582,382 | 0 | 587,998 | 0 | 1,658,695 | 0 | 4,530,881 | 0 | 0 | 4,837,499 | 1,243,383 | 3,519,146 | 0 | 0 | 0 |

### 总输入Token消耗数【input_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 1,908,803 | 6,478,818 | 0 | 0 | 4,926,359 | 4,887,328 | 10,108,197 | 2,008,993 | 15,243,761 | 5,562,514 | 50,395,348 | 6,851,240 | 0 | 0 | 109,666,698 | 16,578,266 | 49,947,833 | 0 | 0 | 163,021 |
| sprint-009 | 0 | 1,908,803 | 6,478,818 | 0 | 0 | 4,926,359 | 4,887,328 | 10,108,197 | 2,008,993 | 15,243,761 | 5,562,514 | 50,395,348 | 6,851,240 | 0 | 0 | 109,666,698 | 16,578,266 | 49,947,833 | 0 | 0 | 163,021 |
| REQ-0049-miniapp-product-card-component | 0 | 0 | 384,945 | 0 | 0 | 406,180 | 0 | 778,650 | 0 | 1,332,055 | 0 | 4,586,440 | 0 | 0 | 0 | 0 | 2,403,167 | 1,025,535 | 0 | 0 | 0 |
| REQ-0050-miniapp-brand-header-page-title-rules | 0 | 0 | 209,415 | 0 | 0 | 300,002 | 0 | 734,125 | 0 | 1,434,355 | 0 | 0 | 0 | 0 | 0 | 15,576,222 | 709,291 | 1,719,861 | 0 | 0 | 0 |
| REQ-0051-category-list-product-list-entry-by-level | 0 | 0 | 239,348 | 0 | 0 | 206,420 | 0 | 436,269 | 0 | 1,215,215 | 0 | 0 | 0 | 0 | 0 | 6,881,118 | 1,667,269 | 1,519,590 | 0 | 0 | 0 |
| REQ-0052-miniapp-device-evidence-template | 0 | 0 | 283,239 | 0 | 0 | 268,758 | 0 | 1,074,661 | 0 | 1,451,282 | 0 | 3,812,858 | 0 | 0 | 0 | 2,582,272 | 3,316,716 | 2,072,978 | 0 | 0 | 0 |
| REQ-0053-miniapp-custom-navigation-best-practice | 0 | 0 | 412,767 | 0 | 0 | 334,199 | 0 | 799,992 | 0 | 1,251,285 | 0 | 5,308,405 | 0 | 0 | 0 | 1,745,403 | 0 | 1,323,627 | 0 | 0 | 0 |
| REQ-0054-brand-card-common-component | 0 | 0 | 183,679 | 0 | 0 | 332,610 | 0 | 653,623 | 0 | 1,324,312 | 0 | 6,289,218 | 0 | 0 | 0 | 2,153,597 | 820,166 | 1,647,509 | 0 | 0 | 0 |
| REQ-0055-brand-certificate-common-component | 0 | 0 | 568,176 | 0 | 0 | 361,615 | 0 | 981,031 | 0 | 1,354,585 | 0 | 3,047,393 | 0 | 0 | 0 | 10,707,534 | 657,784 | 4,253,844 | 0 | 0 | 0 |
| REQ-0056-product-list-card-only-layout | 0 | 0 | 381,015 | 0 | 0 | 350,000 | 0 | 925,013 | 0 | 1,172,689 | 0 | 5,031,754 | 0 | 0 | 0 | 2,906,261 | 925,155 | 1,923,739 | 0 | 0 | 0 |
| REQ-0057-certificate-list-page | 0 | 0 | 517,496 | 0 | 0 | 449,384 | 0 | 577,243 | 0 | 1,228,886 | 0 | 5,301,256 | 0 | 0 | 0 | 9,415,567 | 633,952 | 10,744,271 | 0 | 0 | 0 |
| REQ-0058-brand-detail-home-page | 0 | 0 | 945,225 | 0 | 0 | 414,721 | 0 | 668,980 | 0 | 683,540 | 0 | 2,886,975 | 0 | 0 | 0 | 11,479,611 | 588,461 | 3,278,873 | 0 | 0 | 0 |
| REQ-0059-favorite-list-page | 0 | 0 | 0 | 0 | 0 | 350,574 | 0 | 925,013 | 0 | 601,708 | 0 | 2,396,254 | 0 | 0 | 0 | 5,196,132 | 801,148 | 2,467,507 | 0 | 0 | 0 |
| REQ-0060-brand-list-page | 0 | 0 | 1,255,638 | 0 | 0 | 391,837 | 0 | 1,012,881 | 0 | 737,907 | 0 | 8,600,752 | 0 | 0 | 0 | 11,215,141 | 465,136 | 3,177,899 | 0 | 0 | 0 |
| REQ-0061-miniapp-share-add-guide | 0 | 0 | 404,067 | 0 | 0 | 288,194 | 0 | 595,752 | 0 | 615,913 | 0 | 4,541,256 | 0 | 0 | 0 | 4,935,085 | 204,992 | 4,515,665 | 0 | 0 | 0 |
| REQ-0062-admin-banner-placement-scope | 0 | 0 | 693,808 | 0 | 0 | 471,865 | 0 | 869,977 | 0 | 840,029 | 0 | 2,584,259 | 0 | 0 | 0 | 9,231,415 | 828,359 | 761,362 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4,823,469 | 1,238,215 | 0 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7,225,187 | 0 | 0 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 437,126 | 0 | 0 | 0 | 0 | 1,340,647 | 0 | 666,245 | 0 | 1,328,885 | 0 | 2,332,391 | 0 | 0 | 7,225,187 | 0 | 2,634,170 | 0 | 0 | 0 |
| BUG-0067-home-recommendation-list-entry-routing | 0 | 440,140 | 0 | 0 | 0 | 0 | 1,025,011 | 0 | 759,292 | 0 | 1,253,565 | 0 | 2,332,391 | 0 | 0 | 3,592,684 | 253,606 | 2,005,367 | 0 | 0 | 0 |
| BUG-0068-miniapp-home-device-acceptance-followup | 0 | 508,489 | 0 | 0 | 0 | 0 | 944,199 | 0 | 0 | 0 | 1,325,376 | 594,968 | 0 | 0 | 0 | 6,881,118 | 3,204,618 | 1,393,862 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 523,048 | 0 | 0 | 0 | 0 | 1,577,471 | 0 | 583,456 | 0 | 1,654,688 | 0 | 4,518,849 | 0 | 0 | 4,823,469 | 1,238,215 | 3,482,174 | 0 | 0 | 0 |

### 总输出Token消耗数【output_tokens】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 17,052 | 56,009 | 0 | 0 | 60,031 | 18,857 | 118,517 | 13,165 | 41,103 | 14,496 | 166,544 | 25,159 | 0 | 0 | 355,811 | 40,921 | 212,293 | 0 | 0 | 1,291 |
| sprint-009 | 0 | 17,052 | 56,009 | 0 | 0 | 60,031 | 18,857 | 118,517 | 13,165 | 41,103 | 14,496 | 166,544 | 25,159 | 0 | 0 | 355,811 | 40,921 | 212,293 | 0 | 0 | 1,291 |
| REQ-0049-miniapp-product-card-component | 0 | 0 | 3,837 | 0 | 0 | 4,346 | 0 | 8,405 | 0 | 3,600 | 0 | 22,991 | 0 | 0 | 0 | 0 | 7,438 | 5,827 | 0 | 0 | 0 |
| REQ-0050-miniapp-brand-header-page-title-rules | 0 | 0 | 2,531 | 0 | 0 | 4,640 | 0 | 9,552 | 0 | 3,871 | 0 | 0 | 0 | 0 | 0 | 24,805 | 2,021 | 8,268 | 0 | 0 | 0 |
| REQ-0051-category-list-product-list-entry-by-level | 0 | 0 | 2,867 | 0 | 0 | 3,033 | 0 | 8,393 | 0 | 2,884 | 0 | 0 | 0 | 0 | 0 | 24,285 | 3,519 | 8,611 | 0 | 0 | 0 |
| REQ-0052-miniapp-device-evidence-template | 0 | 0 | 2,248 | 0 | 0 | 4,871 | 0 | 11,803 | 0 | 3,119 | 0 | 17,052 | 0 | 0 | 0 | 10,571 | 9,096 | 8,020 | 0 | 0 | 0 |
| REQ-0053-miniapp-custom-navigation-best-practice | 0 | 0 | 3,881 | 0 | 0 | 5,490 | 0 | 8,997 | 0 | 3,213 | 0 | 12,020 | 0 | 0 | 0 | 7,906 | 0 | 8,034 | 0 | 0 | 0 |
| REQ-0054-brand-card-common-component | 0 | 0 | 2,738 | 0 | 0 | 3,667 | 0 | 7,926 | 0 | 3,427 | 0 | 33,057 | 0 | 0 | 0 | 13,037 | 1,333 | 9,337 | 0 | 0 | 0 |
| REQ-0055-brand-certificate-common-component | 0 | 0 | 4,889 | 0 | 0 | 3,872 | 0 | 10,374 | 0 | 3,299 | 0 | 15,782 | 0 | 0 | 0 | 21,463 | 1,706 | 18,913 | 0 | 0 | 0 |
| REQ-0056-product-list-card-only-layout | 0 | 0 | 3,980 | 0 | 0 | 3,697 | 0 | 8,037 | 0 | 2,637 | 0 | 12,494 | 0 | 0 | 0 | 16,552 | 1,994 | 7,949 | 0 | 0 | 0 |
| REQ-0057-certificate-list-page | 0 | 0 | 3,415 | 0 | 0 | 4,253 | 0 | 8,287 | 0 | 3,260 | 0 | 13,364 | 0 | 0 | 0 | 44,553 | 2,594 | 17,924 | 0 | 0 | 0 |
| REQ-0058-brand-detail-home-page | 0 | 0 | 6,430 | 0 | 0 | 4,244 | 0 | 10,186 | 0 | 2,380 | 0 | 10,764 | 0 | 0 | 0 | 37,608 | 1,642 | 14,285 | 0 | 0 | 0 |
| REQ-0059-favorite-list-page | 0 | 0 | 0 | 0 | 0 | 3,766 | 0 | 8,037 | 0 | 2,400 | 0 | 9,820 | 0 | 0 | 0 | 29,443 | 2,275 | 9,514 | 0 | 0 | 0 |
| REQ-0060-brand-list-page | 0 | 0 | 10,242 | 0 | 0 | 4,922 | 0 | 10,442 | 0 | 2,171 | 0 | 13,759 | 0 | 0 | 0 | 34,430 | 871 | 17,142 | 0 | 0 | 0 |
| REQ-0061-miniapp-share-add-guide | 0 | 0 | 3,841 | 0 | 0 | 4,150 | 0 | 8,045 | 0 | 2,386 | 0 | 10,389 | 0 | 0 | 0 | 19,112 | 401 | 22,549 | 0 | 0 | 0 |
| REQ-0062-admin-banner-placement-scope | 0 | 0 | 5,110 | 0 | 0 | 5,080 | 0 | 8,070 | 0 | 2,456 | 0 | 13,850 | 0 | 0 | 0 | 27,042 | 2,970 | 10,703 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14,030 | 5,168 | 0 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 21,879 | 0 | 0 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 3,813 | 0 | 0 | 0 | 0 | 5,578 | 0 | 4,625 | 0 | 3,228 | 0 | 13,127 | 0 | 0 | 21,879 | 0 | 11,508 | 0 | 0 | 0 |
| BUG-0067-home-recommendation-list-entry-routing | 0 | 3,789 | 0 | 0 | 0 | 0 | 4,611 | 0 | 3,998 | 0 | 3,486 | 0 | 13,127 | 0 | 0 | 9,095 | 935 | 8,369 | 0 | 0 | 0 |
| BUG-0068-miniapp-home-device-acceptance-followup | 0 | 4,676 | 0 | 0 | 0 | 0 | 3,757 | 0 | 0 | 0 | 3,775 | 4,193 | 0 | 0 | 0 | 24,285 | 2,582 | 9,504 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 4,774 | 0 | 0 | 0 | 0 | 4,911 | 0 | 4,542 | 0 | 4,007 | 0 | 12,032 | 0 | 0 | 14,030 | 5,168 | 15,836 | 0 | 0 | 0 |

### 模型调用次数【model_call_count】

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 43 | 147 | 0 | 0 | 59 | 40 | 89 | 15 | 114 | 37 | 380 | 62 | 0 | 0 | 802 | 138 | 344 | 0 | 0 | 2 |
| sprint-009 | 0 | 43 | 147 | 0 | 0 | 59 | 40 | 89 | 15 | 114 | 37 | 380 | 62 | 0 | 0 | 802 | 138 | 344 | 0 | 0 | 2 |
| REQ-0049-miniapp-product-card-component | 0 | 0 | 9 | 0 | 0 | 6 | 0 | 8 | 0 | 11 | 0 | 61 | 0 | 0 | 0 | 0 | 24 | 7 | 0 | 0 | 0 |
| REQ-0050-miniapp-brand-header-page-title-rules | 0 | 0 | 6 | 0 | 0 | 4 | 0 | 7 | 0 | 11 | 0 | 0 | 0 | 0 | 0 | 89 | 9 | 11 | 0 | 0 | 0 |
| REQ-0051-category-list-product-list-entry-by-level | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 5 | 0 | 11 | 0 | 0 | 0 | 0 | 0 | 65 | 13 | 11 | 0 | 0 | 0 |
| REQ-0052-miniapp-device-evidence-template | 0 | 0 | 4 | 0 | 0 | 3 | 0 | 9 | 0 | 10 | 0 | 44 | 0 | 0 | 0 | 18 | 27 | 12 | 0 | 0 | 0 |
| REQ-0053-miniapp-custom-navigation-best-practice | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 7 | 0 | 9 | 0 | 26 | 0 | 0 | 0 | 13 | 0 | 8 | 0 | 0 | 0 |
| REQ-0054-brand-card-common-component | 0 | 0 | 5 | 0 | 0 | 4 | 0 | 6 | 0 | 10 | 0 | 77 | 0 | 0 | 0 | 12 | 4 | 10 | 0 | 0 | 0 |
| REQ-0055-brand-certificate-common-component | 0 | 0 | 12 | 0 | 0 | 4 | 0 | 8 | 0 | 9 | 0 | 41 | 0 | 0 | 0 | 60 | 3 | 21 | 0 | 0 | 0 |
| REQ-0056-product-list-card-only-layout | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 8 | 0 | 9 | 0 | 25 | 0 | 0 | 0 | 39 | 7 | 12 | 0 | 0 | 0 |
| REQ-0057-certificate-list-page | 0 | 0 | 13 | 0 | 0 | 5 | 0 | 5 | 0 | 9 | 0 | 32 | 0 | 0 | 0 | 69 | 9 | 50 | 0 | 0 | 0 |
| REQ-0058-brand-detail-home-page | 0 | 0 | 21 | 0 | 0 | 5 | 0 | 6 | 0 | 5 | 0 | 17 | 0 | 0 | 0 | 76 | 4 | 39 | 0 | 0 | 0 |
| REQ-0059-favorite-list-page | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 8 | 0 | 5 | 0 | 17 | 0 | 0 | 0 | 66 | 5 | 13 | 0 | 0 | 0 |
| REQ-0060-brand-list-page | 0 | 0 | 25 | 0 | 0 | 4 | 0 | 8 | 0 | 5 | 0 | 48 | 0 | 0 | 0 | 75 | 2 | 36 | 0 | 0 | 0 |
| REQ-0061-miniapp-share-add-guide | 0 | 0 | 11 | 0 | 0 | 4 | 0 | 6 | 0 | 5 | 0 | 28 | 0 | 0 | 0 | 39 | 1 | 39 | 0 | 0 | 0 |
| REQ-0062-admin-banner-placement-scope | 0 | 0 | 14 | 0 | 0 | 4 | 0 | 6 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 58 | 12 | 9 | 0 | 0 | 0 |
| REQ-0044-miniapp-sku-detail-page | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 38 | 19 | 0 | 0 | 0 | 0 |
| REQ-0046-search-component-application | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 52 | 0 | 0 | 0 | 0 | 0 |
| BUG-0066-search-component-prototype-deviation | 0 | 10 | 0 | 0 | 0 | 0 | 11 | 0 | 5 | 0 | 9 | 0 | 38 | 0 | 0 | 52 | 0 | 15 | 0 | 0 | 0 |
| BUG-0067-home-recommendation-list-entry-routing | 0 | 10 | 0 | 0 | 0 | 0 | 9 | 0 | 6 | 0 | 9 | 0 | 38 | 0 | 0 | 33 | 2 | 12 | 0 | 0 | 0 |
| BUG-0068-miniapp-home-device-acceptance-followup | 0 | 10 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 9 | 12 | 0 | 0 | 0 | 65 | 14 | 8 | 0 | 0 | 0 |
| BUG-0069-miniapp-sku-detail-carousel-video-not-playable | 0 | 13 | 0 | 0 | 0 | 0 | 12 | 0 | 4 | 0 | 10 | 0 | 24 | 0 | 0 | 38 | 19 | 31 | 0 | 0 | 0 |

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
