---
sprint_id: sprint-011
title: Sprint 011 迭代经验复盘
status: draft
created_at: 2026-07-26 15:49:00
updated_at: 2026-07-26 15:49:00
owner: product
related_iteration: iterations/archive/sprint-011/
source: /sprint-exps sprint-011
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 011 迭代经验复盘

## 1. 迭代概况

| 指标 | 值 |
|------|-----|
| Sprint 状态 | completed / archive |
| 计划周期 | 2026-07-23 09:17:23 ~ 2026-07-25 18:00:00 |
| REQ / BUG / Change | 3 / 5 / 8 |
| Change 批次 | 不适用；未达到 10 个 Change 批次阈值 |
| tasks 完成度 | 157/157 |
| 估算 | 24 SP / 24.0 人天 |
| 容量 | 30 人天；占用 80.0%；fix buffer 20.0% |
| 归档路径残留 | 0；`check-archived-path-residuals.py` PASS |
| readiness | PASS；8/8 Change archived |
| AI usage | Snapshot `present/actual`，REQ/BUG/Change 覆盖 pass，warning 0 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-011 --summary`、`scripts/check-archived-path-residuals.py --sprint sprint-011 --json`、`iterations/archive/sprint-011/sprint.yaml`、`iterations/archive/sprint-011/acceptance-report.md`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 生产上传链路 | 修复视频上传 99% 后 504、补 Web Nginx 上传专用 location、上传超时配置和对象存储闭环验证 |
| 小程序视频体验 | 补视频 Range/206、封面兜底、全屏入口、全屏上下文保持、长按/保存/转发平台降级说明 |
| 生产 DB / Banner | 修复生产 MySQL `banners` schema drift，恢复品牌类型 Banner 创建保存 |
| 管理端上传状态 | 区分客户端上传与服务端保存阶段，降低 99% 误判和重复提交风险 |
| 可观测与审计 | 建立 Task Trace MVP，串联上传节点、审计日志查询和详情时间线 |
| 日志审计体验 | 操作者筛选从 User ID 输入改为用户名称/账号搜索下拉，保留 `actor_user_id` 精确过滤 |

## 2. 流程复盘

### 做得好的

1. **范围控制比 sprint-010 更稳**：8 个 Change、24/30 人天，容量占用 80%，没有在收尾阶段继续追加超容量范围。
2. **生产缺陷与体验增强放在同一条媒体主线上**：上传 99%、视频慢启动、全屏重载和保存/转发体验互相补足，减少了分散修补。
3. **归档门禁有效拦住证据缺口**：`fix-miniapp-sku-video-slow-start` 缺 `trace.md` 被 readiness 识别，已补 `## 归档验证摘要` 兜底。
4. **路径残留门禁干净**：Sprint 迁入 archive 后 residual_count 为 0，复盘不传播旧 change 阶段路径或 active Change 路径。
5. **已有最佳实践被复用**：media-upload、admin-list、admin-form、miniapp-custom-navigation 都继续作为横切验收依据。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| 归档证据结构不一致 | Fact Sheet warning：`fix-miniapp-sku-video-slow-start` 缺 `trace.md` | archive readiness 被阻断，需要人工补 fallback summary |
| 验收证据仍混有真机/生产 follow-up | 小程序真机、生产 Nginx/backend 日志、生产候选数据仍需上线 sign-off | Sprint 可归档，但 release sign-off 仍需补证 |
| 观测范围容易向 dashboard 膨胀 | acceptance 中 AC-050~AC-053 已标记转入后续 dashboard Change | REQ-0069 MVP 边界需要继续守住，避免可观测性一次做成平台级工程 |
| Token 主要消耗集中在 apply/propose | Opsx-Apply 42496044 tokens，Sprint-Propose 34475330 tokens | 规划与实现阶段仍需要更强的摘要复用和分段处理 |
| active/archived 路径兼容仍是持续风险 | 本 Sprint 依赖 readiness、residual gate、测试 helper 兼容 archive path | 后续测试和文档链接必须继续通过 resolver，不硬编码 active path |

### 优化建议

1. **将 archived Change 缺 trace 检查前移**：在 `/opsx-archive` 成功后立即要求 `trace.md` 或完整 fallback summary，避免等到 `/sprint-archive` 才阻断。
2. **把 release sign-off 与 Sprint archive 分层**：Sprint 可基于自动化和生产等价验证关闭；真机/生产证据用 release checklist 明确追踪。
3. **可观测能力分层交付**：Task Trace MVP、日志详情、dashboard/聚合分析分不同 Change，不把 AC-050~AC-053 混入已完成范围。
4. **继续脚本化 stale acceptance 检查**：已归档 Scope 若验收正文仍写“待实现/尚未实现/planned”，应在 archive 前自动提示。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-011.json`，由脱敏 command-runs 聚合 |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| generated_at | 2026-07-26T07:46:21.727949Z | Fact Sheet summary |
| command run 数 | 71 | Sprint snapshot totals |
| 模型调用次数 | 1144 | Sprint snapshot totals |
| 工具调用次数 | 2148 | Sprint snapshot totals |
| input tokens | 145439323 | Sprint snapshot totals |
| cached input tokens | 139136512 | Sprint snapshot totals |
| output tokens | 657746 | Sprint snapshot totals |
| reasoning output tokens | 61295 | Sprint snapshot totals |
| total tokens | 146353701 | Sprint snapshot totals |
| retry count | 0 | Sprint snapshot totals |
| 主要输入消耗 | Opsx-Apply、Sprint-Propose、BUG-Opsx、Opsx-Archive | 矩阵列显示 apply/propose/archive 阶段占比最高 |
| 主要输出消耗 | Sprint-Propose、Opsx-Apply、BUG/REQ Opsx | 多轮计划、实现摘要和归档报告输出较多 |
| 重复/浪费来源 | 规则/Skill 重读、Sprint 四件套、Change archive 查找、测试与 Workflow Sync 输出 | Fact Sheet token_risks 指向四件套、8 个 Change、archive lookup |
| 已采用节省策略 | Fact Sheet summary、residual JSON、矩阵脚本化、只回读 warning 相关片段 | 符合 `rules/agent-context-budget.md` 的先定位再读取 |

> 矩阵口径：`Total` 与 `sprint-011` 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图。同一 command run 关联多个 REQ/BUG 时会计入多个对象行，因此对象行不应直接相加后与 `Total` 比较。

### 总 Token 消耗数 `total_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 4035697 | 1149211 | 0 | 0 | 971025 | 5275005 | 3990872 | 3324792 | 4019106 | 6959152 | 8676926 | 14756431 | 0 | 0 | 42496044 | 14053748 | 34475330 | 0 | 0 | 2170362 |
| sprint-011 | 0 | 4035697 | 1149211 | 0 | 0 | 971025 | 5275005 | 3990872 | 3324792 | 4019106 | 6959152 | 8676926 | 14756431 | 0 | 0 | 42496044 | 14053748 | 34475330 | 0 | 0 | 2170362 |
| REQ-0068-miniapp-sku-video-fullscreen-actions | 0 | 0 | 495086 | 0 | 0 | 541420 | 0 | 902402 | 0 | 1379756 | 0 | 2862644 | 0 | 0 | 0 | 3461604 | 1416805 | 2612566 | 0 | 0 | 0 |
| REQ-0069-upload-observability-trace-logs | 0 | 0 | 439756 | 0 | 0 | 429605 | 0 | 2318895 | 0 | 891493 | 0 | 2796521 | 0 | 0 | 0 | 16954248 | 1423840 | 1379811 | 0 | 0 | 0 |
| REQ-0070-audit-log-operator-name-filter | 0 | 0 | 214369 | 0 | 0 | 0 | 0 | 1249740 | 0 | 1747857 | 0 | 3017761 | 0 | 0 | 0 | 8061864 | 1939634 | 2019406 | 0 | 0 | 0 |
| BUG-0081-prod-cos-video-upload-fails | 0 | 1417586 | 0 | 0 | 0 | 0 | 498423 | 0 | 558945 | 0 | 1403881 | 0 | 2397007 | 0 | 0 | 3168046 | 2588417 | 1780777 | 0 | 0 | 0 |
| BUG-0082-prod-miniapp-sku-video-slow-start | 0 | 679029 | 0 | 0 | 0 | 0 | 1929881 | 0 | 836837 | 0 | 1202955 | 0 | 3843463 | 0 | 0 | 2392985 | 2418128 | 1406994 | 0 | 0 | 0 |
| BUG-0083-prod-admin-brand-banner-save-500 | 0 | 706021 | 0 | 0 | 0 | 0 | 552062 | 0 | 609273 | 0 | 1671161 | 0 | 4141930 | 0 | 0 | 2705129 | 3133391 | 1415612 | 0 | 0 | 0 |
| BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | 0 | 831844 | 0 | 0 | 0 | 0 | 1541956 | 0 | 841856 | 0 | 1336759 | 0 | 2326386 | 0 | 0 | 2382436 | 1093477 | 1043070 | 0 | 0 | 0 |
| BUG-0085-admin-video-upload-stuck-at-99 | 0 | 401217 | 0 | 0 | 0 | 0 | 752683 | 0 | 477881 | 0 | 1344396 | 0 | 2047645 | 0 | 0 | 3369732 | 2401620 | 2601570 | 0 | 0 | 0 |

### 总输入 Token 消耗数 `input_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 4008124 | 1138042 | 0 | 0 | 960008 | 5257473 | 3955895 | 3302148 | 4008889 | 6942837 | 8641393 | 14711580 | 0 | 0 | 42254766 | 14025141 | 34073310 | 0 | 0 | 2159717 |
| sprint-011 | 0 | 4008124 | 1138042 | 0 | 0 | 960008 | 5257473 | 3955895 | 3302148 | 4008889 | 6942837 | 8641393 | 14711580 | 0 | 0 | 42254766 | 14025141 | 34073310 | 0 | 0 | 2159717 |
| REQ-0068-miniapp-sku-video-fullscreen-actions | 0 | 0 | 491744 | 0 | 0 | 535910 | 0 | 895818 | 0 | 1376786 | 0 | 2853674 | 0 | 0 | 0 | 3441018 | 1414208 | 2577586 | 0 | 0 | 0 |
| REQ-0069-upload-observability-trace-logs | 0 | 0 | 435094 | 0 | 0 | 424098 | 0 | 2300988 | 0 | 888557 | 0 | 2782542 | 0 | 0 | 0 | 16865227 | 1420877 | 1344860 | 0 | 0 | 0 |
| REQ-0070-audit-log-operator-name-filter | 0 | 0 | 211204 | 0 | 0 | 0 | 0 | 1234275 | 0 | 1743546 | 0 | 3005177 | 0 | 0 | 0 | 8039578 | 1937082 | 1978868 | 0 | 0 | 0 |
| BUG-0081-prod-cos-video-upload-fails | 0 | 1406210 | 0 | 0 | 0 | 0 | 495152 | 0 | 553718 | 0 | 1400421 | 0 | 2387972 | 0 | 0 | 3123964 | 2577780 | 1775232 | 0 | 0 | 0 |
| BUG-0082-prod-miniapp-sku-video-slow-start | 0 | 675909 | 0 | 0 | 0 | 0 | 1925763 | 0 | 833773 | 0 | 1200412 | 0 | 3834511 | 0 | 0 | 2378777 | 2408905 | 1381334 | 0 | 0 | 0 |
| BUG-0083-prod-admin-brand-banner-save-500 | 0 | 701016 | 0 | 0 | 0 | 0 | 548808 | 0 | 604086 | 0 | 1667388 | 0 | 4131339 | 0 | 0 | 2686753 | 3123806 | 1384937 | 0 | 0 | 0 |
| BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | 0 | 828677 | 0 | 0 | 0 | 0 | 1538425 | 0 | 837285 | 0 | 1333297 | 0 | 2318453 | 0 | 0 | 2368745 | 1091494 | 1013181 | 0 | 0 | 0 |
| BUG-0085-admin-video-upload-stuck-at-99 | 0 | 396312 | 0 | 0 | 0 | 0 | 749325 | 0 | 473286 | 0 | 1341319 | 0 | 2039305 | 0 | 0 | 3350704 | 2398057 | 2566101 | 0 | 0 | 0 |

### 总输出 Token 消耗数 `output_tokens`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 27573 | 11169 | 0 | 0 | 11017 | 17532 | 34977 | 22644 | 10217 | 16315 | 35533 | 44851 | 0 | 0 | 194764 | 28607 | 191902 | 0 | 0 | 10645 |
| sprint-011 | 0 | 27573 | 11169 | 0 | 0 | 11017 | 17532 | 34977 | 22644 | 10217 | 16315 | 35533 | 44851 | 0 | 0 | 194764 | 28607 | 191902 | 0 | 0 | 10645 |
| REQ-0068-miniapp-sku-video-fullscreen-actions | 0 | 0 | 3342 | 0 | 0 | 5510 | 0 | 6584 | 0 | 2970 | 0 | 8970 | 0 | 0 | 0 | 20586 | 2597 | 14154 | 0 | 0 | 0 |
| REQ-0069-upload-observability-trace-logs | 0 | 0 | 4662 | 0 | 0 | 5507 | 0 | 17907 | 0 | 2936 | 0 | 13979 | 0 | 0 | 0 | 65698 | 2963 | 13828 | 0 | 0 | 0 |
| REQ-0070-audit-log-operator-name-filter | 0 | 0 | 3165 | 0 | 0 | 0 | 0 | 15465 | 0 | 4311 | 0 | 12584 | 0 | 0 | 0 | 22286 | 2552 | 19087 | 0 | 0 | 0 |
| BUG-0081-prod-cos-video-upload-fails | 0 | 11376 | 0 | 0 | 0 | 0 | 3271 | 0 | 5227 | 0 | 3460 | 0 | 9035 | 0 | 0 | 20891 | 10637 | 5545 | 0 | 0 | 0 |
| BUG-0082-prod-miniapp-sku-video-slow-start | 0 | 3120 | 0 | 0 | 0 | 0 | 4118 | 0 | 3064 | 0 | 2543 | 0 | 8952 | 0 | 0 | 14208 | 9223 | 5779 | 0 | 0 | 0 |
| BUG-0083-prod-admin-brand-banner-save-500 | 0 | 5005 | 0 | 0 | 0 | 0 | 3254 | 0 | 5187 | 0 | 3773 | 0 | 10591 | 0 | 0 | 18376 | 9585 | 9456 | 0 | 0 | 0 |
| BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | 0 | 3167 | 0 | 0 | 0 | 0 | 3531 | 0 | 4571 | 0 | 3462 | 0 | 7933 | 0 | 0 | 13691 | 1983 | 8432 | 0 | 0 | 0 |
| BUG-0085-admin-video-upload-stuck-at-99 | 0 | 4905 | 0 | 0 | 0 | 0 | 3358 | 0 | 4595 | 0 | 3077 | 0 | 8340 | 0 | 0 | 19028 | 3563 | 13386 | 0 | 0 | 0 |

### 模型调用次数 `model_call_count`

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Total | 0 | 56 | 22 | 0 | 0 | 10 | 40 | 30 | 23 | 25 | 44 | 45 | 77 | 0 | 0 | 354 | 102 | 291 | 0 | 0 | 25 |
| sprint-011 | 0 | 56 | 22 | 0 | 0 | 10 | 40 | 30 | 23 | 25 | 44 | 45 | 77 | 0 | 0 | 354 | 102 | 291 | 0 | 0 | 25 |
| REQ-0068-miniapp-sku-video-fullscreen-actions | 0 | 0 | 7 | 0 | 0 | 6 | 0 | 7 | 0 | 9 | 0 | 16 | 0 | 0 | 0 | 36 | 10 | 15 | 0 | 0 | 0 |
| REQ-0069-upload-observability-trace-logs | 0 | 0 | 9 | 0 | 0 | 4 | 0 | 17 | 0 | 5 | 0 | 13 | 0 | 0 | 0 | 122 | 12 | 21 | 0 | 0 | 0 |
| REQ-0070-audit-log-operator-name-filter | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 11 | 0 | 11 | 0 | 16 | 0 | 0 | 0 | 44 | 11 | 26 | 0 | 0 | 0 |
| BUG-0081-prod-cos-video-upload-fails | 0 | 20 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 9 | 0 | 13 | 0 | 0 | 40 | 28 | 8 | 0 | 0 | 0 |
| BUG-0082-prod-miniapp-sku-video-slow-start | 0 | 7 | 0 | 0 | 0 | 0 | 15 | 0 | 6 | 0 | 8 | 0 | 20 | 0 | 0 | 26 | 25 | 7 | 0 | 0 | 0 |
| BUG-0083-prod-admin-brand-banner-save-500 | 0 | 14 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 10 | 0 | 21 | 0 | 0 | 27 | 26 | 13 | 0 | 0 | 0 |
| BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | 0 | 6 | 0 | 0 | 0 | 0 | 10 | 0 | 5 | 0 | 7 | 0 | 11 | 0 | 0 | 24 | 8 | 16 | 0 | 0 | 0 |
| BUG-0085-admin-video-upload-stuck-at-99 | 0 | 9 | 0 | 0 | 0 | 0 | 7 | 0 | 4 | 0 | 10 | 0 | 12 | 0 | 0 | 35 | 14 | 20 | 0 | 0 | 0 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| Opsx-Apply | high | `total_tokens=42496044`、`model_call_count=354` | 按 Change 分段处理，失败日志只保留关键段，复用已读规则摘要 |
| Sprint-Propose | high | `total_tokens=34475330`、`model_call_count=291` | 范围变更时优先 diff `sprint.yaml` scope，不重复展开 Issue 包 |
| BUG-Opsx | high | `total_tokens=14756431`、`model_call_count=77` | 固化 BUG→Change 模板，减少重复读取 capture/bug/root-cause 全文 |
| Opsx-Archive | high | `total_tokens=14053748`、`model_call_count=102` | 归档优先使用 readiness summary、Workflow Sync summary 和 residual JSON |
| Sprint 四件套 | high | Fact Sheet token_risks：`sprint.md` 超 200 行 | 复盘默认使用 Fact Sheet summary；只在写回链和处理 warning 时读片段 |
| OpenSpec changes | high | Fact Sheet token_risks：8 Change，157/157 tasks | 不默认读取每个 `tasks.md`；只按 warning 回读 `fix-miniapp-sku-video-slow-start` fallback |
| Archive lookup | medium | Fact Sheet token_risks：archive path 由 sprint.yaml 解析 | 使用脚本 resolver，避免宽泛扫描 `openspec/changes/archive/**` |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 本次复盘先运行 `--summary`，未默认展开全部四件套、Issue trace、Change tasks |
| warning 定向回读 | 符合 | 仅针对缺 trace 的历史 Change 回读已有证据并补 fallback |
| residual gate | 符合 | `check-archived-path-residuals.py --json` 返回 residual_count 0 |
| 输出截断 | 符合 | 复盘使用聚合计数、矩阵和短证据，不复制测试日志或 OpenAPI/Orval 生成物 |
| 可继续改进 | 需要 | Sprint-Propose 和 Opsx-Apply 输入消耗仍高，后续应加强 scope diff、Change 分段和失败摘要模板 |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为 `/opsx-archive` 增加归档后 trace/fallback 自检，缺失时立即补证据而不是延后到 Sprint 关闭 | `/opsx-propose` | open |
| T-002 | P1 | 为 `acceptance-report.md` 增加 stale phrase gate，扫描 completed/archived 范围中仍出现“待实现/尚未实现/planned”的行 | `/opsx-propose` | open |
| T-003 | P1 | 将生产/真机 evidence 从 Sprint archive 中剥离成 release sign-off checklist，避免归档与上线确认混淆 | `/req-capture` | open |
| T-004 | P2 | 将 Task Trace dashboard、聚合排行和安全脱敏验证作为后续独立 Change，避免 REQ-0069 MVP 膨胀 | `/sprint-propose` | open |
| T-005 | P2 | 针对 Sprint-Propose 高 token 消耗，优先读取 `sprint.yaml` diff 与 registry 摘要，减少重复展开 Issue 包 | `/opsx-propose` | open |

## 3. 需求与设计复盘

| 观察 | 结论 | 建议 |
|------|------|------|
| 5 个 BUG 中 3 个集中在上传/视频链路 | 媒体链路是当前产品质量高风险区 | 发布前 smoke 应覆盖上传、媒体读取、SKU 保存、Nginx/backend 日志和小程序播放 |
| REQ-0068 与 BUG-0084 强相关 | 全屏增强和全屏重载修复应作为同一体验链路验收 | 后续小程序视频需求先画出 inline/fullscreen/preview 三态状态机 |
| REQ-0069 易膨胀为观测平台 | 本 Sprint 正确收敛为 Task Trace MVP + 审计日志查看 | dashboard、聚合、排行另立 Change |
| REQ-0070 复用现有用户列表 API | 避免新增不必要后端契约 | 类似筛选体验优先复用候选 API 和 SearchableSelect |

## 4. 开发质量复盘

| 主题 | 经验 | 后续要求 |
|------|------|----------|
| 上传链路 | 前端 99% 不等于服务端保存完成，状态必须拆分 | 上传组件统一展示客户端传输、服务端保存、完成/失败四态 |
| 媒体读取 | 视频必须支持 Range/206，同时保证非视频读取不回归 | 媒体相关 Change 必跑 `tests/test_media_storage.py` |
| 生产 DB drift | SQLite 与 MySQL 约束差异会导致生产 500 | DB 变更必须同步 schema drift 检查、幂等迁移和生产 smoke |
| 小程序平台能力 | 长按菜单、保存视频、全屏行为受微信能力限制 | 验收记录必须区分静态测试、DevTools 和真机 evidence |
| 审计与脱敏 | Task Trace metadata 一旦落库就必须默认脱敏 | 新增日志字段必须覆盖 Authorization、Cookie、Secret、DSN、内部路径 |

## 5. 可复用抽象

| 抽象方向 | 来源 | 建议 |
|----------|------|------|
| Admin 上传状态模型 | BUG-0081、BUG-0085、REQ-0069 | 提炼 `client_uploading`、`server_saving`、`saved`、`failed` 状态文案与事件埋点 |
| 媒体播放验收模板 | BUG-0082、REQ-0068、BUG-0084 | 建立小程序视频验收清单：poster、Range、inline、fullscreen、preview、真机 evidence |
| AdminList 筛选组件 | REQ-0070、REQ-0069 | 继续复用 `SearchableSelect`、fixed toast、分页 DOM 和移动端筛选布局规则 |
| Change archive evidence | BUG-0082 缺 trace | 将 `trace.md` 或 `## 归档验证摘要` 作为归档产物标准化 |

## 6. Follow-up 建议

以下事项未自动创建 Issue。

| 建议命令 | 类型倾向 | 标题 | 背景 | 影响范围 | 建议验收要点 | 来源 |
|----------|----------|------|------|----------|--------------|------|
| `/opsx-propose` | 技术治理 | 归档 Change trace/fallback 自检 | sprint-011 关闭时发现历史 Change 缺 `trace.md` | OpenSpec archive、readiness、sprint-archive | 缺 trace 时 archive 命令自动提示并生成完整 fallback 摘要 | sprint-011 / sprint-exps |
| `/opsx-propose` | 技术治理 | acceptance stale phrase gate | sprint-011 曾出现已归档范围仍保留“待实现/planned”语义 | iterations 四件套、archive readiness | completed/archived Scope 中 stale phrase 触发 warning 或阻断 | sprint-011 / sprint-exps |
| `/req-capture` | 需求 | Release sign-off checklist 分层 | 生产/真机证据不应阻断 Sprint archive，但需要发布前闭环 | release、miniapp、production smoke | release-prepare 能追踪真机、生产 Nginx/backend 日志、浏览器 Network 证据 | sprint-011 / sprint-exps |
| `/sprint-propose` | 需求/增强 | 观测 dashboard 与聚合分析 | AC-050~AC-053 已转入后续范围 | 管理端日志审计、Task Trace、后端聚合 API | SQLite/MySQL 聚合、慢任务排行、下钻、脱敏测试全部通过 | sprint-011 / sprint-exps |

## 7. 结论

Sprint 011 是一次“生产媒体链路修复 + 小程序视频体验 + 审计可观测 MVP”的集中收敛。它比上一轮更小、更聚焦，最终 8/8 Change archived、157/157 tasks 完成、路径残留 0。最值得保留的经验是：媒体链路必须按上传、读取、播放、保存、审计五层验收；最需要继续改的是：归档证据和验收 stale 语义要脚本化前置，别让最后一公里靠人工判断兜底。
