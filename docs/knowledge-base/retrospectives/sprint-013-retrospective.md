---
sprint_id: sprint-013
title: Sprint 013 迭代经验复盘
status: draft
created_at: 2026-07-29 09:31:30
updated_at: 2026-07-29 09:31:30
owner: product
related_iteration: iterations/archive/sprint-013/
source: /sprint-exps sprint-013
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 013 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 实际周期 | 2026-07-28 00:24:49 ~ 2026-07-29 09:24:09 |
| REQ / BUG / Change | 4 / 4 / 8 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 144/144 |
| 估算 | 20.5 SP / 20.5 人天 |
| 容量 | 30 人天；占用 68.33%；fix buffer 31.67% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；8/8 Change archived |
| AI usage | `present/actual`；57 command runs，814 model calls，1,656 tool calls，109,197,684 total tokens |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-013 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-013 --json`、`iterations/archive/sprint-013/sprint.yaml`、`iterations/archive/sprint-013/acceptance-report.md`、`data/ai-usage/sprints/sprint-013.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 类目名称长度 | 类目名称输入上限调整为 15 个用户可见字符，并完成 API、管理端和展示端回归 |
| 商品详情备注 | 小程序 SKU 详情页展示公开备注说明，空值不暴露异常占位 |
| 品牌证书多图 | 管理端品牌证书支持多图上传、唯一主图、旧单文件兼容和主图缩略图 |
| 小程序证书详情 | 新增证书详情页、公开详情 API、列表/品牌入口、分享与媒体预览链路 |
| 品牌商品排序 | 品牌详情页商品 Tab 按发布时间升序、ID 升序稳定返回 |
| SKU 发布时间列 | 管理端 SKU 列表新增发布时间列，区分首次发布与更新时间 |
| SKU 编辑成功态 | 管理端 SKU 编辑保存成功后直接关闭弹窗 |
| 证书图片噪音 | 移除品牌证书新增/编辑弹窗图片说明下方的冗余文件名文本 |

## 2. 流程复盘

### 做得好的

1. **Scope 薄片化但覆盖完整**：4 个 REQ 与 4 个 BUG 都有明确 Change，既覆盖体验增强，也收纳了中途发现的高价值修复。
2. **归档闭环更干净**：Sprint archive 后 residual gate 返回 0，复盘没有继续传播旧 Sprint change 阶段路径或 active Change 路径。
3. **容量保留健康**：20.5/30 人天，fix buffer 31.67%，允许 BUG-0089 追加后仍不过载。
4. **媒体与小程序边界被纳入验收**：证书多图、MinIO 单桶策略、Docker Web 上传边界、小程序证书详情 DevTools/真机 evidence 均进入 Sprint 文档。
5. **AI usage 已能真实统计**：`data/ai-usage/sprints/sprint-013.json` 为 `actual`，不再像 sprint-012 一样降级到 fallback。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| archived Change 缺 `trace.md` | Fact Sheet warning：`fix-miniapp-brand-detail-product-sort-order` 缺 `trace.md`，靠 `tasks.md` 的 `## 归档验证摘要` 兜底通过 | Sprint archive 能通过，但证据链不如带 trace 的 Change 稳定 |
| Sprint 规划过程反复扩围 | `sprint.yaml` 显示 4 REQ + 4 BUG 分多次纳入，`Sprint-Propose` token 达 21,221,138 | Scope 回填、同步和验收文案修正成本明显上升 |
| 管理端 UI 问题重复出现 | 本期包含 SKU 列、SKU 编辑弹窗、证书图片文本噪音，均属于 admin-list/admin-form/admin-modal 模式 | 需要继续把列表列变更、弹窗成功态、上传控件文案纳入共享验收模板 |
| 小程序设备 evidence 仍有 blocked/follow_up | acceptance 记录小程序证书详情 DevTools/真机 evidence 未报告真机通过 | 发布说明可保留边界，但下一 Sprint 需要尽早安排真机或 DevTools 可用性 |

### 优化建议

1. **归档前强制补齐 archived Change trace 或 fallback 摘要**：现有 readiness 已能检查 fallback，建议 `/opsx-archive` 阶段直接生成，避免 Sprint archive 时补证据。
2. **追加 Scope 时立即刷新发布说明和验收清单**：多次 `/sprint-propose` 后，应自动把新增 BUG 和 Change 写入 release-note 的发布范围。
3. **把管理端列表/弹窗/上传控件验收模板前置到 propose/apply**：重复 UI 问题不需要每次重新设计 AC，直接引用 best-practice 并补场景差异。
4. **小程序 evidence 作为独立发布边界管理**：DevTools/真机不可用时允许 archive，但必须在 release-note 保留 blocked/follow_up，并在下一 Sprint 规划时显式评估是否转 BUG 或验证任务。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-013.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| command_run_count | 57 | snapshot totals |
| model_call_count | 814 | snapshot totals |
| tool_call_count | 1,656 | snapshot totals |
| input_tokens | 108,576,285 | snapshot totals |
| cached_input_tokens | 103,624,960 | snapshot totals |
| output_tokens | 454,209 | snapshot totals |
| reasoning_output_tokens | 39,614 | snapshot totals |
| total_tokens | 109,197,684 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 主要输入消耗 | Opsx-Apply、Sprint-Propose、Opsx-Archive、BUG-Opsx、REQ-Opsx | 横切 API/DB/Web/小程序/文档同步与多次 Scope 回填 |
| 主要输出消耗 | Opsx-Apply、Sprint-Propose、REQ-Opsx、Opsx-Archive | 主要来自实现说明、同步报告、测试/验收摘要和归档输出 |
| 重复/浪费来源 | 多次 Sprint-Propose 扩围、归档证据缺 trace 后补、宽范围横切验收 | Fact Sheet token_risks：8 Change、144/144 tasks、四件套中 `sprint.md` 超 200 行 |
| 已采用节省策略 | Fact Sheet summary、residual JSON、已读规则摘要复用、路径残留 gate、矩阵从 JSON 生成 | 符合 `rules/agent-context-budget.md` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 1361538 | 1521049 | 0 | 0 | 1318074 | 868281 | 2889044 | 2801896 | 2918308 | 2669992 | 9261879 | 10750062 | 0 | 0 | 34991593 | 14743597 | 21221138 | 0 | 0 | 1881233 |
| sprint-013 | 0 | 1361538 | 1521049 | 0 | 0 | 1318074 | 868281 | 2889044 | 2801896 | 2918308 | 2669992 | 9261879 | 10750062 | 0 | 0 | 34991593 | 14743597 | 21221138 | 0 | 0 | 1881233 |
| REQ-0077-category-name-max-length-15 | 0 | 0 | 418794 | 0 | 0 | 350214 | 0 | 719249 | 0 | 1066125 | 0 | 2034394 | 0 | 0 | 0 | 2574520 | 1892471 | 1443506 | 0 | 0 | 0 |
| REQ-0078-certificate-multiple-images-main-image | 0 | 0 | 504114 | 0 | 0 | 402577 | 0 | 734590 | 0 | 639260 | 0 | 2493803 | 0 | 0 | 0 | 8888116 | 1506608 | 4514524 | 0 | 0 | 0 |
| REQ-0079-admin-sku-list-published-at | 0 | 0 | 139424 | 0 | 0 | 200667 | 0 | 467948 | 0 | 502221 | 0 | 1681938 | 0 | 0 | 0 | 3145102 | 1506608 | 3996015 | 0 | 0 | 0 |
| REQ-0080-miniapp-certificate-detail-page | 0 | 0 | 458717 | 0 | 0 | 364616 | 0 | 967257 | 0 | 710702 | 0 | 3051744 | 0 | 0 | 0 | 8664460 | 2480991 | 4956987 | 0 | 0 | 0 |
| BUG-0086-miniapp-sku-detail-remark-not-shown | 0 | 389097 | 0 | 0 | 0 | 0 | 575708 | 0 | 1765792 | 0 | 453550 | 0 | 1421257 | 0 | 0 | 4706171 | 1297210 | 2451399 | 0 | 0 | 0 |
| BUG-0087-miniapp-brand-detail-product-tab-sort-order | 0 | 733735 | 0 | 0 | 0 | 0 | 575708 | 0 | 2478298 | 0 | 1766188 | 0 | 5126042 | 0 | 0 | 2385795 | 5847286 | 1380051 | 0 | 0 | 0 |
| BUG-0088-admin-sku-edit-save-extra-step | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3145102 | 1102532 | 0 | 0 | 0 | 0 |
| BUG-0089-admin-certificate-edit-image-filename-noise | 0 | 238706 | 0 | 0 | 0 | 0 | 292573 | 0 | 323598 | 0 | 450254 | 0 | 4202763 | 0 | 0 | 4627429 | 616499 | 2478656 | 0 | 0 | 0 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 1352217 | 1507187 | 0 | 0 | 1301435 | 863354 | 2848237 | 2791654 | 2906490 | 2661366 | 9214211 | 10723509 | 0 | 0 | 34803269 | 14674085 | 21061207 | 0 | 0 | 1868064 |
| sprint-013 | 0 | 1352217 | 1507187 | 0 | 0 | 1301435 | 863354 | 2848237 | 2791654 | 2906490 | 2661366 | 9214211 | 10723509 | 0 | 0 | 34803269 | 14674085 | 21061207 | 0 | 0 | 1868064 |
| REQ-0077-category-name-max-length-15 | 0 | 0 | 415472 | 0 | 0 | 346280 | 0 | 708645 | 0 | 1061336 | 0 | 2025226 | 0 | 0 | 0 | 2538895 | 1889213 | 1437278 | 0 | 0 | 0 |
| REQ-0078-certificate-multiple-images-main-image | 0 | 0 | 500058 | 0 | 0 | 398310 | 0 | 722275 | 0 | 636932 | 0 | 2479641 | 0 | 0 | 0 | 8855188 | 1502144 | 4473232 | 0 | 0 | 0 |
| REQ-0079-admin-sku-list-published-at | 0 | 0 | 137188 | 0 | 0 | 196435 | 0 | 459810 | 0 | 499838 | 0 | 1668728 | 0 | 0 | 0 | 3109770 | 1502144 | 3978279 | 0 | 0 | 0 |
| REQ-0080-miniapp-certificate-detail-page | 0 | 0 | 454469 | 0 | 0 | 360410 | 0 | 957507 | 0 | 708384 | 0 | 3040616 | 0 | 0 | 0 | 8627024 | 2478044 | 4924600 | 0 | 0 | 0 |
| BUG-0086-miniapp-sku-detail-remark-not-shown | 0 | 385551 | 0 | 0 | 0 | 0 | 572412 | 0 | 1762050 | 0 | 451045 | 0 | 1414689 | 0 | 0 | 4676785 | 1293717 | 2442089 | 0 | 0 | 0 |
| BUG-0087-miniapp-brand-detail-product-tab-sort-order | 0 | 730474 | 0 | 0 | 0 | 0 | 572412 | 0 | 2470309 | 0 | 1761880 | 0 | 5114554 | 0 | 0 | 2376855 | 5840639 | 1337174 | 0 | 0 | 0 |
| BUG-0088-admin-sku-edit-save-extra-step | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3109770 | 1077843 | 0 | 0 | 0 | 0 |
| BUG-0089-admin-certificate-edit-image-filename-noise | 0 | 236192 | 0 | 0 | 0 | 0 | 290942 | 0 | 321345 | 0 | 448441 | 0 | 4194266 | 0 | 0 | 4618752 | 592485 | 2468555 | 0 | 0 | 0 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 9321 | 13862 | 0 | 0 | 16639 | 4927 | 40807 | 10242 | 11818 | 8626 | 47668 | 26553 | 0 | 0 | 126391 | 26986 | 97200 | 0 | 0 | 13169 |
| sprint-013 | 0 | 9321 | 13862 | 0 | 0 | 16639 | 4927 | 40807 | 10242 | 11818 | 8626 | 47668 | 26553 | 0 | 0 | 126391 | 26986 | 97200 | 0 | 0 | 13169 |
| REQ-0077-category-name-max-length-15 | 0 | 0 | 3322 | 0 | 0 | 3934 | 0 | 10604 | 0 | 4789 | 0 | 9168 | 0 | 0 | 0 | 14971 | 3258 | 6228 | 0 | 0 | 0 |
| REQ-0078-certificate-multiple-images-main-image | 0 | 0 | 4056 | 0 | 0 | 4267 | 0 | 12315 | 0 | 2328 | 0 | 14162 | 0 | 0 | 0 | 32928 | 4464 | 20458 | 0 | 0 | 0 |
| REQ-0079-admin-sku-list-published-at | 0 | 0 | 2236 | 0 | 0 | 4232 | 0 | 8138 | 0 | 2383 | 0 | 13210 | 0 | 0 | 0 | 14448 | 4464 | 17736 | 0 | 0 | 0 |
| REQ-0080-miniapp-certificate-detail-page | 0 | 0 | 4248 | 0 | 0 | 4206 | 0 | 9750 | 0 | 2318 | 0 | 11128 | 0 | 0 | 0 | 37436 | 2947 | 11519 | 0 | 0 | 0 |
| BUG-0086-miniapp-sku-detail-remark-not-shown | 0 | 3546 | 0 | 0 | 0 | 0 | 3296 | 0 | 3742 | 0 | 2505 | 0 | 6568 | 0 | 0 | 8991 | 3493 | 9310 | 0 | 0 | 0 |
| BUG-0087-miniapp-brand-detail-product-tab-sort-order | 0 | 3261 | 0 | 0 | 0 | 0 | 3296 | 0 | 7989 | 0 | 4308 | 0 | 11488 | 0 | 0 | 8940 | 6647 | 21848 | 0 | 0 | 0 |
| BUG-0088-admin-sku-edit-save-extra-step | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14448 | 3634 | 0 | 0 | 0 | 0 |
| BUG-0089-admin-certificate-edit-image-filename-noise | 0 | 2514 | 0 | 0 | 0 | 0 | 1631 | 0 | 2253 | 0 | 1813 | 0 | 8497 | 0 | 0 | 8677 | 2543 | 10101 | 0 | 0 | 0 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|------|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
| Total | 0 | 21 | 33 | 0 | 0 | 18 | 13 | 28 | 19 | 23 | 19 | 57 | 58 | 0 | 0 | 239 | 120 | 140 | 0 | 0 | 26 |
| sprint-013 | 0 | 21 | 33 | 0 | 0 | 18 | 13 | 28 | 19 | 23 | 19 | 57 | 58 | 0 | 0 | 239 | 120 | 140 | 0 | 0 | 26 |
| REQ-0077-category-name-max-length-15 | 0 | 0 | 9 | 0 | 0 | 5 | 0 | 7 | 0 | 8 | 0 | 12 | 0 | 0 | 0 | 25 | 13 | 7 | 0 | 0 | 0 |
| REQ-0078-certificate-multiple-images-main-image | 0 | 0 | 10 | 0 | 0 | 5 | 0 | 7 | 0 | 5 | 0 | 15 | 0 | 0 | 0 | 66 | 18 | 31 | 0 | 0 | 0 |
| REQ-0079-admin-sku-list-published-at | 0 | 0 | 4 | 0 | 0 | 4 | 0 | 6 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 31 | 18 | 22 | 0 | 0 | 0 |
| REQ-0080-miniapp-certificate-detail-page | 0 | 0 | 10 | 0 | 0 | 4 | 0 | 8 | 0 | 5 | 0 | 17 | 0 | 0 | 0 | 51 | 14 | 26 | 0 | 0 | 0 |
| BUG-0086-miniapp-sku-detail-remark-not-shown | 0 | 9 | 0 | 0 | 0 | 0 | 9 | 0 | 11 | 0 | 5 | 0 | 12 | 0 | 0 | 25 | 17 | 15 | 0 | 0 | 0 |
| BUG-0087-miniapp-brand-detail-product-tab-sort-order | 0 | 5 | 0 | 0 | 0 | 0 | 9 | 0 | 15 | 0 | 9 | 0 | 23 | 0 | 0 | 20 | 27 | 21 | 0 | 0 | 0 |
| BUG-0088-admin-sku-edit-save-extra-step | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 17 | 0 | 0 | 0 | 0 |
| BUG-0089-admin-certificate-edit-image-filename-noise | 0 | 7 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 5 | 0 | 23 | 0 | 0 | 21 | 14 | 18 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Opsx-Apply | high | 34,991,593 total tokens，239 model calls | 对 XL/L Change 先用 Fact Sheet 和 diff stat 定位，再按 API/DB/Web/miniapp 分段 apply |
| Sprint-Propose | high | 21,221,138 total tokens，140 model calls | 多次追加 Scope 后使用增量同步报告，不重复读完整四件套 |
| Opsx-Archive | high | 14,743,597 total tokens，120 model calls | `/opsx-archive` 阶段自动写归档验证摘要，减少 Sprint archive 后补证据 |
| BUG-Opsx / REQ-Opsx | high | 合计 20,011,941 total tokens | opsx 生成阶段复用模板化 task/test sections，避免为常见 UI/上传问题重复展开规则 |
| Sprint 四件套 | medium | `sprint.md` 324 行，Fact Sheet token_risks 标记 high | 复盘优先 summary；只在回链和 stale 检查时读尾部片段 |
| OpenSpec archive lookup | medium | 8 Change，144/144 tasks | 使用 resolver 和 residual gate，避免宽泛扫描 `openspec/archive/**` |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次先运行 `--summary`，未默认展开全部 Sprint 四件套、Issue trace、Change tasks |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 读取边界 | 符合 | 只读 `sprint-exps` skill、Fact Sheet summary、README、上期复盘样式和必要路径片段 |
| 输出截断 | 符合 | 未复制测试日志、OpenAPI/Orval 生成物、完整 evidence_hints 或完整 tasks |
| 需要修正 | 是 | Sprint-Propose 与 Opsx-Apply 总成本偏高，说明多次扩围和横切实现仍需要更强的增量化 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-013-001 | P1 | 为 `/opsx-archive` 自动写入 `## 归档验证摘要`，尤其是 trace 缺失时，避免 Sprint close 阶段补证据 | `/opsx-propose` | open |
| T-013-002 | P1 | 为 `/sprint-propose` 增加增量 release-note/scope 同步检查，追加 BUG 或 REQ 后自动刷新发布范围 | `/opsx-propose` | open |
| T-013-003 | P2 | 对 XL/L Change 的 `/opsx-apply` 增加分段执行建议：API/DB、Web、miniapp、docs/tests 分块验收 | `/opsx-propose` | open |
| T-013-004 | P2 | 将 admin-list/admin-form/admin-modal/media-upload 常见 AC 收敛为可引用模板，减少每次 UI BUG 重写验收 | `/req-capture` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| 多图证书与证书详情形成上下游闭环 | REQ-0078 负责管理端维护能力，REQ-0080 承接小程序公开详情 | 后续媒体类需求继续按“管理端维护 → 公开端消费 → evidence”拆薄片 |
| 类目长度与 SKU 时间列是字段级薄片 | 范围清楚，不扩大为类目体系或发布流程改造 | 字段级需求继续明确“不包含筛选、排序、导出、历史清洗”等边界 |
| BUG-0087 排序修复依赖事实字段定义 | 发布时间必须用 `tiles.published_at`，空值才用 `created_at` 兜底 | 涉及排序的 BUG 必须先写清事实字段、空值策略和不影响的排序分支 |
| 设备 evidence 有发布边界 | 小程序证书详情能通过静态/API 自动化，但真机 evidence 仍保留 follow_up | 小程序交付应把 DevTools/真机环境可用性作为 Sprint 早期风险 |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| API / DB / Orval | 证书多图和证书详情横跨 Schema、Repository、Service、OpenAPI/Orval 与文档 | API 或 DB 变更必须继续用 OpenAPI/Orval/docs/tests 同步 gate |
| MinIO / 上传 | 多图证书和文件名噪音修复都依赖上传状态机稳定 | 上传控件必须覆盖 idle/uploading/done/failed、主图、删除、继续添加和失败提示 |
| 管理端列表 | SKU 发布时间列与列表横切一致性强相关 | admin-list 变更继续回归分页 DOM、fixed toast、宽表布局和无 `window.confirm` |
| 管理端弹窗 | SKU 编辑成功态、证书图片文本噪音、弹窗宽度属于重复模式 | admin-form/admin-modal 最佳实践需要作为 apply 前置检查 |
| 小程序页面 | 证书详情与品牌详情商品 Tab 都要求接口顺序和页面展示一致 | 小程序静态测试要覆盖路由、入口、分享、返回兜底和禁止端侧跨页重排 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Certificate media model | REQ-0078、REQ-0080 | 继续沉淀证书图片数组、主图唯一性、旧单文件兼容、安全 URL 的统一模型 |
| Admin upload control AC | REQ-0078、BUG-0089 | 将图片卡片、主图标记、删除、继续添加、失败态、隐藏无价值文件名文本作为共享 AC |
| Published time display helper | REQ-0079、BUG-0087 | 时间字段显示和排序都必须区分 published/updated/created，前端展示 helper 与后端排序契约应一致 |
| Miniapp detail page shell | REQ-0080、已有商品详情页 | 大媒体区、信息分区、品牌入口、分享、错误态可继续复用，但避免带入交易/收藏模块 |
| Archive evidence fallback | BUG-0087 | trace 缺失时的 `## 归档验证摘要` 可脚本化，字段固定为 validation、acceptance、issue_or_sprint_status、archive_evidence |

## 6. Follow-up 建议

以下事项未自动创建 Issue。

| 建议命令 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议验收要点 | 来源 |
|----------|----------|------|------|----------|--------------|------|
| `/opsx-propose` | 技术治理 | opsx archive 自动生成归档验证摘要 | BUG-0087 archived Change 缺 `trace.md`，Sprint archive 阶段需要补 `tasks.md` 兜底摘要 | `.agents/skills/opsx-archive`、`scripts/validate-sprint-archive-readiness.py`、归档模板 | trace 缺失时 archive 阶段自动生成完整 fallback；readiness 不再需要人工补证据 | sprint-013 / `/sprint-exps sprint-013` |
| `/opsx-propose` | 技术治理 | sprint-propose 增量同步 release-note 发布范围 | sprint-013 多次追加 BUG/REQ 后，release-note 曾保留 in_sprint/proposed/applied 等旧状态 | `scripts/sync-workflow-status.py`、`iterations/*/release-note.md` | 追加 scope 后 release-note 中 REQ/BUG/Change 状态与 `sprint.yaml`、Scope 表一致 | sprint-013 / `/sprint-exps sprint-013` |
| `/req-capture` | 需求 | 管理端上传控件与弹窗 AC 模板化 | SKU 编辑、SKU 列、证书图片文件名噪音等 UI 问题重复依赖 admin-list/admin-form/admin-modal/media-upload 验收 | `docs/knowledge-base/best-practices/`、OpenSpec task/test 模板 | 新模板可被后续 UI REQ/BUG 引用，覆盖列表、弹窗、上传状态机和无价值文案移除 | sprint-013 / `/sprint-exps sprint-013` |
| `/bug-capture` | BUG | 小程序证书详情真机 evidence follow-up | sprint-013 证书详情 DevTools/真机 evidence 保留 blocked/follow_up，未报告真机通过 | `src/miniapp/pages/certificate-detail/`、小程序 DevTools/真机验证流程 | 真机或 DevTools 320/375/430 pt evidence 明确通过或给出可复现阻断原因 | sprint-013 / `/sprint-exps sprint-013` |

## 7. 复盘结论

Sprint 013 是一次业务体验增强与缺陷修复混合的高完成度 Sprint：8/8 Change archived，144/144 tasks 完成，容量占用健康，路径残留清零。主要经验是“薄片化范围 + 横切验收清单”可以支撑 API/DB/Web/小程序/上传链路一起交付；主要改进点在流程工具链，尤其是归档证据自动化、追加 Scope 后 release-note 同步，以及大型 apply 的分段 token 控制。

## 8. 更新文件

| 文件 | 动作 | 说明 |
|------|------|------|
| `docs/knowledge-base/retrospectives/sprint-013-retrospective.md` | 新建 | 本文档 |
| `docs/knowledge-base/README.md` | 更新 | 增加 sprint-013 复盘索引 |
| `iterations/archive/sprint-013/sprint.md` | 更新 | 增加复盘回链 |
