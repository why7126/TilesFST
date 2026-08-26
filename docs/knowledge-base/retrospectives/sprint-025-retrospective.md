---
title: sprint-025 复盘
purpose: 复盘 sprint-025 的流程、需求、开发质量、可复用抽象与模型 Token 使用
content: Sprint 经验复盘
source: /sprint-exps sprint-025
update_method: Sprint 归档后由 AI 生成，后续由团队 Review
status: draft
created_at: 2026-08-25 15:48:21
updated_at: 2026-08-25 18:18:35
---

# sprint-025 复盘

## 概况

sprint-025 已完成归档，目录为 `iterations/archive/sprint-025/`。本 Sprint 覆盖 9 个 REQ、7 个 BUG、18 个 OpenSpec Change，306/306 个任务完成，验收与归档状态闭环。

范围聚类：

| 类别 | 覆盖项 | 经验信号 |
|------|--------|----------|
| 发布与升级治理 | REQ-0114 | 版本部署、升级、回滚不能只靠代码幂等，需要 release 事实源、env diff、DB drift/smoke 与回滚证据共同定义支持级别 |
| 媒体多规格与 WebP | REQ-0115、REQ-0119、REQ-0120、REQ-0122 | 图片 `thumbnail/display/original` 要同时覆盖生成、配置、历史补生成、Runbook 和版本使用文档投影，避免能力散落 |
| 小程序轻量图消费 | BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0137、REQ-0118、REQ-0121 | 小程序媒体性能验收必须证明 key、object、URL、render/Network 四联，不再把字段存在当成端上已消费 |
| Workflow Sync 治理 | REQ-0116、BUG-0136、BUG-0138、两个治理 Change | 状态回填、YAML frontmatter、根因 confirmed gate 和 Sprint 默认选择规则都需要脚本化校验，减少人工收尾漂移 |

Fact Sheet summary：

| 指标 | 值 |
|------|----:|
| requirements | 9 |
| bugs | 7 |
| changes | 18 |
| tasks | 306/306 |
| warnings | 0 |
| archived path residuals | 0 |
| AI usage fresh gate | pass |

归档路径残留检查：`check-archived-path-residuals.py --sprint sprint-025 --json` 报告 `residual_count=0`。

## 流程复盘

做得好的地方：

| 维度 | 观察 | 可复用做法 |
|------|------|------------|
| 大 Sprint 分批 | Fact Sheet 将 18 个 Change 拆为 4 个 batch，且每批 warnings/blockers 均为 0 | 大于 10 个 Change 的 Sprint 默认用 batch summary 判断任务完成与证据风险，不展开全部归档文档 |
| 媒体验收 | REQ-0120 与 BUG-0137 补齐小程序 WebP、display/thumb 请求和 render evidence | 媒体类验收以端上实际请求为准，接口字段、对象存在和截图要互相印证 |
| 治理脚本闭环 | Workflow Sync、OpenSpec、stale scan、residual gate 与 AI usage fresh gate 全部通过 | Sprint 收尾优先跑聚合脚本，再定位少量异常，避免人工扫全仓 |
| Snapshot 修复 | AI usage snapshot 从缺失恢复为 `actual/present`，fresh gate 与 matrix write gate 均 pass | session JSONL 归因需要显式支持 manual-map/turn-hash 兜底，避免长会话命令无法归属到 Sprint |

卡点：

| 卡点 | 表现 | 根因 | 预防 |
|------|------|------|------|
| AI usage 归因缺失 | `/sprint-archive` 初次关闭记录显示 snapshot 缺失并降级 estimated_fallback | 当前会话 command run 能解析 token，但原始记录缺少 `sprint_id`，自动 post hook 选择到非目标 turn | 为 Sprint archive/exps 保留 turn_hash 到 sprint_id 的 manual attribution，并在 hook 前做 dry-run fresh gate |
| 归档命令与 Git index | Sprint 目录迁移使用普通移动后，工作区显示旧路径删除与 archive 路径新增 | sandbox 阻止 `git mv` 写 `.git/index.lock`，且部分 Sprint 文件归档前未进入 Git index | 归档后用 focused `git status --short` 与 `/git-check` 做提交前复核，不在复盘中修正 Git 元数据 |
| 大范围媒体链路 | 媒体能力跨后端、对象存储、Web、小程序、Runbook 与 release usage-docs | 单个 Sprint 同时包含能力建设、BUG 修复和治理增强，证据矩阵很容易变宽 | 后续媒体类 Sprint 按生成、消费、维护、发布文档分层验收，每层只读对应事实源 |
| 历史对象与不可达对象 | BUG-0134 与 REQ-0117 都涉及对象缺失和对象存储不可达判别 | NoSuchResource、历史 key 漂移、基础设施不可达的处理语义不同 | 维护任务必须先 dry-run，顶层输出 blocked/summary，并脱敏展示环境与建议动作 |

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-025.json` |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Fresh gate | pass | Fact Sheet: `ai_usage_snapshot.fresh_gate.status` |
| Matrix write gate | pass | 必须 fresh gate pass、actual/present 且矩阵存在才可输出真实矩阵 |
| Freshness baseline | 2026-08-25T07:48:21Z | 来源：`sprint.md:updated_at` |
| Generated at | 2026-08-25T09:58:54.859842Z | `data/ai-usage/sprints/sprint-025.json` |
| command_run_count | 100 | snapshot totals |
| model_call_count | 104 | snapshot totals |
| tool_call_count | 90 | snapshot totals |
| input_tokens | 8,004,377 | snapshot totals |
| cached_input_tokens | 6,558,848 | snapshot totals |
| output_tokens | 34,785 | snapshot totals |
| reasoning_output_tokens | 5,565 | snapshot totals |
| total_tokens | 8,039,162 | snapshot totals |
| retry_count | 0 | snapshot totals |
| 矩阵规模 | 18 行 x 22 列 | `usage_matrices.rows` / `usage_matrices.columns` |

矩阵口径：`Total` 与 Sprint 行按唯一 command run 汇总；REQ/BUG 行是对象归因视图，同一 command run 关联多个 REQ/BUG 时可在多个对象行出现，因此对象行不应直接相加后与 `Total` 比较。`-` 表示该 workflow 阶段在当前 snapshot 中未采集或未归因，不等价于真实 `0`；只有已观测 workflow 列中的数字 `0` 才表示真实零消耗。矩阵数据来自 `data/ai-usage/sprints/<sprint-id>.json` 经 Fact Sheet 渲染输出。

### total_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 17860 | 173832 | - | - | 283896 | 507667 | - | - | - | 22945 | 91837 | - | - | 29657 | 240132 | 159914 | 310257 | 27478 | - | - | 6173687 |
| sprint-025 | - | 17860 | 173832 | - | - | 283896 | 507667 | - | - | - | 22945 | 91837 | - | - | 29657 | 240132 | 159914 | 310257 | 27478 | - | - | 6173687 |
| REQ-0114-version-deployment-upgrade-rollback-governance | - | 0 | 63900 | - | - | 59222 | 0 | - | - | - | 0 | 91837 | - | - | 0 | 71022 | 33940 | 59504 | 27478 | - | - | 6173687 |
| REQ-0115-media-multi-variant-images | - | 0 | 19103 | - | - | 200254 | 279575 | - | - | - | 0 | 91837 | - | - | 0 | 105357 | 125974 | 59504 | 27478 | - | - | 6173687 |
| REQ-0116-workflow-opsx-linked-change-backfill | - | 0 | 19103 | - | - | 93438 | 0 | - | - | - | 0 | 91837 | - | - | 0 | 122164 | 0 | 116524 | 0 | - | - | 6173687 |
| REQ-0117-media-maintenance-storage-unreachable-summary | - | 0 | 49922 | - | - | 37346 | 0 | - | - | - | 0 | 0 | - | - | 0 | 43006 | 0 | 105780 | 0 | - | - | 6173687 |
| REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | - | 0 | 0 | - | - | 37346 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6173687 |
| REQ-0119-admin-display-image-size-limit-setting | - | 0 | 57656 | - | - | 37346 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6173687 |
| REQ-0120-webp-derived-image-variants | - | 0 | 21457 | - | - | 37346 | 0 | - | - | - | 22945 | 0 | - | - | 0 | 40627 | 0 | 0 | 0 | - | - | 6173687 |
| REQ-0121-miniapp-certificate-detail-brand-card-entry | - | 0 | 0 | - | - | 58958 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6173687 |
| REQ-0122-batch-image-processing-runbook | - | 0 | 0 | - | - | 65160 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6173687 |
| BUG-0132-miniapp-sku-detail-large-image-cold-load | - | 0 | 19103 | - | - | 59222 | 67290 | - | - | - | 0 | 91837 | - | - | 0 | 71022 | 0 | 59504 | 27478 | - | - | 6173687 |
| BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | - | 0 | 0 | - | - | 37346 | 48163 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6173687 |
| BUG-0134-miniapp-certificate-detail-display-url | - | 0 | 0 | - | - | 37346 | 119526 | - | - | - | 0 | 0 | - | - | 29657 | 34335 | 47127 | 41510 | 0 | - | - | 6173687 |
| BUG-0135-miniapp-certificate-card-file-url-fallback | - | 0 | 0 | - | - | 37346 | 40621 | - | - | - | 0 | 0 | - | - | 0 | 34335 | 0 | 0 | 0 | - | - | 6173687 |
| BUG-0136-workflow-sync-bug-generate-captured-draft | - | 0 | 0 | - | - | 37346 | 40869 | - | - | - | 0 | 0 | - | - | 0 | 34335 | 0 | 0 | 0 | - | - | 6173687 |
| BUG-0137-miniapp-lightweight-image-variant-consumption | - | 0 | 0 | - | - | 37346 | 288875 | - | - | - | 0 | 0 | - | - | 29657 | 0 | 78847 | 41510 | 0 | - | - | 6173687 |
| BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | - | 17860 | 0 | - | - | 0 | 0 | - | - | - | 0 | 0 | - | - | 0 | 40627 | 0 | 46443 | 0 | - | - | 6173687 |

### input_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 17700 | 172851 | - | - | 282573 | 505481 | - | - | - | 22748 | 91670 | - | - | 29537 | 239679 | 159559 | 309538 | 27358 | - | - | 6145683 |
| sprint-025 | - | 17700 | 172851 | - | - | 282573 | 505481 | - | - | - | 22748 | 91670 | - | - | 29537 | 239679 | 159559 | 309538 | 27358 | - | - | 6145683 |
| REQ-0114-version-deployment-upgrade-rollback-governance | - | 0 | 63513 | - | - | 58803 | 0 | - | - | - | 0 | 91670 | - | - | 0 | 70942 | 33796 | 59421 | 27358 | - | - | 6145683 |
| REQ-0115-media-multi-variant-images | - | 0 | 18961 | - | - | 199413 | 278708 | - | - | - | 0 | 91670 | - | - | 0 | 105178 | 125763 | 59421 | 27358 | - | - | 6145683 |
| REQ-0116-workflow-opsx-linked-change-backfill | - | 0 | 18961 | - | - | 92895 | 0 | - | - | - | 0 | 91670 | - | - | 0 | 122004 | 0 | 116338 | 0 | - | - | 6145683 |
| REQ-0117-media-maintenance-storage-unreachable-summary | - | 0 | 49635 | - | - | 37134 | 0 | - | - | - | 0 | 0 | - | - | 0 | 42910 | 0 | 105422 | 0 | - | - | 6145683 |
| REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | - | 0 | 0 | - | - | 37134 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6145683 |
| REQ-0119-admin-display-image-size-limit-setting | - | 0 | 57396 | - | - | 37134 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6145683 |
| REQ-0120-webp-derived-image-variants | - | 0 | 21268 | - | - | 37134 | 0 | - | - | - | 22748 | 0 | - | - | 0 | 40529 | 0 | 0 | 0 | - | - | 6145683 |
| REQ-0121-miniapp-certificate-detail-brand-card-entry | - | 0 | 0 | - | - | 58526 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6145683 |
| REQ-0122-batch-image-processing-runbook | - | 0 | 0 | - | - | 64810 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6145683 |
| BUG-0132-miniapp-sku-detail-large-image-cold-load | - | 0 | 18961 | - | - | 58803 | 66728 | - | - | - | 0 | 91670 | - | - | 0 | 70942 | 0 | 59421 | 27358 | - | - | 6145683 |
| BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | - | 0 | 0 | - | - | 37134 | 47760 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 6145683 |
| BUG-0134-miniapp-certificate-detail-display-url | - | 0 | 0 | - | - | 37134 | 118454 | - | - | - | 0 | 0 | - | - | 29537 | 34236 | 46992 | 41442 | 0 | - | - | 6145683 |
| BUG-0135-miniapp-certificate-card-file-url-fallback | - | 0 | 0 | - | - | 37134 | 40218 | - | - | - | 0 | 0 | - | - | 0 | 34236 | 0 | 0 | 0 | - | - | 6145683 |
| BUG-0136-workflow-sync-bug-generate-captured-draft | - | 0 | 0 | - | - | 37134 | 40461 | - | - | - | 0 | 0 | - | - | 0 | 34236 | 0 | 0 | 0 | - | - | 6145683 |
| BUG-0137-miniapp-lightweight-image-variant-consumption | - | 0 | 0 | - | - | 37134 | 288311 | - | - | - | 0 | 0 | - | - | 29537 | 0 | 78771 | 41442 | 0 | - | - | 6145683 |
| BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | - | 17700 | 0 | - | - | 0 | 0 | - | - | - | 0 | 0 | - | - | 0 | 40529 | 0 | 46336 | 0 | - | - | 6145683 |

### output_tokens 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 160 | 981 | - | - | 1323 | 2186 | - | - | - | 197 | 167 | - | - | 120 | 453 | 355 | 719 | 120 | - | - | 28004 |
| sprint-025 | - | 160 | 981 | - | - | 1323 | 2186 | - | - | - | 197 | 167 | - | - | 120 | 453 | 355 | 719 | 120 | - | - | 28004 |
| REQ-0114-version-deployment-upgrade-rollback-governance | - | 0 | 387 | - | - | 419 | 0 | - | - | - | 0 | 167 | - | - | 0 | 80 | 144 | 83 | 120 | - | - | 28004 |
| REQ-0115-media-multi-variant-images | - | 0 | 142 | - | - | 841 | 867 | - | - | - | 0 | 167 | - | - | 0 | 179 | 211 | 83 | 120 | - | - | 28004 |
| REQ-0116-workflow-opsx-linked-change-backfill | - | 0 | 142 | - | - | 543 | 0 | - | - | - | 0 | 167 | - | - | 0 | 160 | 0 | 186 | 0 | - | - | 28004 |
| REQ-0117-media-maintenance-storage-unreachable-summary | - | 0 | 287 | - | - | 212 | 0 | - | - | - | 0 | 0 | - | - | 0 | 96 | 0 | 358 | 0 | - | - | 28004 |
| REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | - | 0 | 0 | - | - | 212 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 28004 |
| REQ-0119-admin-display-image-size-limit-setting | - | 0 | 260 | - | - | 212 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 28004 |
| REQ-0120-webp-derived-image-variants | - | 0 | 189 | - | - | 212 | 0 | - | - | - | 197 | 0 | - | - | 0 | 98 | 0 | 0 | 0 | - | - | 28004 |
| REQ-0121-miniapp-certificate-detail-brand-card-entry | - | 0 | 0 | - | - | 432 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 28004 |
| REQ-0122-batch-image-processing-runbook | - | 0 | 0 | - | - | 350 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 28004 |
| BUG-0132-miniapp-sku-detail-large-image-cold-load | - | 0 | 142 | - | - | 419 | 562 | - | - | - | 0 | 167 | - | - | 0 | 80 | 0 | 83 | 120 | - | - | 28004 |
| BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | - | 0 | 0 | - | - | 212 | 403 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 28004 |
| BUG-0134-miniapp-certificate-detail-display-url | - | 0 | 0 | - | - | 212 | 1072 | - | - | - | 0 | 0 | - | - | 120 | 99 | 135 | 68 | 0 | - | - | 28004 |
| BUG-0135-miniapp-certificate-card-file-url-fallback | - | 0 | 0 | - | - | 212 | 403 | - | - | - | 0 | 0 | - | - | 0 | 99 | 0 | 0 | 0 | - | - | 28004 |
| BUG-0136-workflow-sync-bug-generate-captured-draft | - | 0 | 0 | - | - | 212 | 408 | - | - | - | 0 | 0 | - | - | 0 | 99 | 0 | 0 | 0 | - | - | 28004 |
| BUG-0137-miniapp-lightweight-image-variant-consumption | - | 0 | 0 | - | - | 212 | 564 | - | - | - | 0 | 0 | - | - | 120 | 0 | 76 | 68 | 0 | - | - | 28004 |
| BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | - | 160 | 0 | - | - | 0 | 0 | - | - | - | 0 | 0 | - | - | 0 | 98 | 0 | 107 | 0 | - | - | 28004 |

### model_call_count 矩阵

| 对象 | Capture | BUG-Capture | REQ-Capture | BUG-Explore | REQ-Explore | REQ-Generate | BUG-Generate | REQ-Complete | BUG-Complete | REQ-Review | BUG-Review | REQ-Opsx | BUG-Opsx | Opsx-Explore | Opsx-Propose | Opsx-Apply | Opsx-Modify | Opsx-Archive | Sprint-Propose | Sprint-Explore | Sprint-Apply | Sprint-Archive |
| ------ | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: | ------: |
| Total | - | 1 | 7 | - | - | 9 | 14 | - | - | - | 1 | 2 | - | - | 1 | 5 | 3 | 6 | 1 | - | - | 54 |
| sprint-025 | - | 1 | 7 | - | - | 9 | 14 | - | - | - | 1 | 2 | - | - | 1 | 5 | 3 | 6 | 1 | - | - | 54 |
| REQ-0114-version-deployment-upgrade-rollback-governance | - | 0 | 3 | - | - | 3 | 0 | - | - | - | 0 | 2 | - | - | 0 | 1 | 1 | 1 | 1 | - | - | 54 |
| REQ-0115-media-multi-variant-images | - | 0 | 1 | - | - | 6 | 6 | - | - | - | 0 | 2 | - | - | 0 | 2 | 2 | 1 | 1 | - | - | 54 |
| REQ-0116-workflow-opsx-linked-change-backfill | - | 0 | 1 | - | - | 4 | 0 | - | - | - | 0 | 2 | - | - | 0 | 2 | 0 | 2 | 0 | - | - | 54 |
| REQ-0117-media-maintenance-storage-unreachable-summary | - | 0 | 2 | - | - | 2 | 0 | - | - | - | 0 | 0 | - | - | 0 | 1 | 0 | 2 | 0 | - | - | 54 |
| REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | - | 0 | 0 | - | - | 2 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 54 |
| REQ-0119-admin-display-image-size-limit-setting | - | 0 | 2 | - | - | 2 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 54 |
| REQ-0120-webp-derived-image-variants | - | 0 | 1 | - | - | 2 | 0 | - | - | - | 1 | 0 | - | - | 0 | 1 | 0 | 0 | 0 | - | - | 54 |
| REQ-0121-miniapp-certificate-detail-brand-card-entry | - | 0 | 0 | - | - | 3 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 54 |
| REQ-0122-batch-image-processing-runbook | - | 0 | 0 | - | - | 3 | 0 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 54 |
| BUG-0132-miniapp-sku-detail-large-image-cold-load | - | 0 | 1 | - | - | 3 | 3 | - | - | - | 0 | 2 | - | - | 0 | 1 | 0 | 1 | 1 | - | - | 54 |
| BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | - | 0 | 0 | - | - | 2 | 2 | - | - | - | 0 | 0 | - | - | 0 | 0 | 0 | 0 | 0 | - | - | 54 |
| BUG-0134-miniapp-certificate-detail-display-url | - | 0 | 0 | - | - | 2 | 5 | - | - | - | 0 | 0 | - | - | 1 | 1 | 1 | 1 | 0 | - | - | 54 |
| BUG-0135-miniapp-certificate-card-file-url-fallback | - | 0 | 0 | - | - | 2 | 2 | - | - | - | 0 | 0 | - | - | 0 | 1 | 0 | 0 | 0 | - | - | 54 |
| BUG-0136-workflow-sync-bug-generate-captured-draft | - | 0 | 0 | - | - | 2 | 2 | - | - | - | 0 | 0 | - | - | 0 | 1 | 0 | 0 | 0 | - | - | 54 |
| BUG-0137-miniapp-lightweight-image-variant-consumption | - | 0 | 0 | - | - | 2 | 5 | - | - | - | 0 | 0 | - | - | 1 | 0 | 1 | 1 | 0 | - | - | 54 |
| BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | - | 1 | 0 | - | - | 0 | 0 | - | - | - | 0 | 0 | - | - | 0 | 1 | 0 | 1 | 0 | - | - | 54 |

## 需求与设计复盘

| 主题 | 观察 | 经验 |
|------|------|------|
| 三规格图片契约 | REQ-0115、REQ-0118、REQ-0120 把生成、消费矩阵和 WebP 编码拆成独立 Change | 媒体规格要以 `thumbnail/display/original` 的使用场景建模，不以文件扩展名或单端页面兜底建模 |
| 小程序性能 | BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0137 都源于普通展示场景退回原图或无效占位 | 端侧普通展示必须有“非原图目标场景不得 fallback 到原图”的硬规则，并用 Network evidence 验收 |
| 系统设置 | REQ-0119 将 display 目标体积与 thumbnail 目标体积拆开 | 配置项要表达展示场景差异，避免为了列表性能压缩详情图清晰度 |
| Runbook 投影 | REQ-0122 同时要求 docs 长期事实源与 release usage-docs 快照 | 运维步骤必须区分长期能力说明、版本快照和生产授权门禁，不能把未实现脚本写成可执行事实 |
| 治理门禁 | BUG-0138 与 root-cause confirmed gate 说明 YAML 和证据状态也需要自动化约束 | 工作流状态不是纯文案，必须能被 parser、registry、trace 和 Sprint scope 共同校验 |

## 开发质量复盘

| 维度 | 做得好的点 | 待改进点 |
|------|------------|----------|
| 后端与对象存储 | 媒体派生、对象缺失识别、不可达摘要和 WebP MIME/key 一致性均进入验收范围 | 历史对象维护仍需持续保持 dry-run/apply/幂等证据，避免生产数据操作含混 |
| 小程序 | 首页、品牌列表、品牌主页、证书详情、商品详情多个入口统一验证轻量图消费 | 未来每个新增媒体位都应先登记消费矩阵，再实现页面字段映射 |
| 管理端 | display 图体积目标设置纳入系统设置，并与缩略图目标分离 | 媒体配置 UI 后续需要持续保持 Design System token、固定保存 CTA 和 dirty 确认模式 |
| 治理脚本 | Workflow Sync 对 bug.generate、linked Change 回填和 YAML frontmatter 的缺陷得到修复 | AI usage hook 的目标 turn 选择仍暴露可改进空间，尤其是长会话和复合命令场景 |
| 文档与发布 | 批量图片处理 Runbook 绑定 docs 与 usage-docs 投影 | release 快照应只消费当前版本事实，不反向覆盖长期技术文档或旧版本语义 |

## 可复用抽象

| 抽象 | 来源 | 建议 |
|------|------|------|
| ImageVariantConsumptionMatrix | REQ-0118 / BUG-0137 | 以页面位置、普通展示、预览/下载和 fallback 策略定义三规格消费，作为后续 Web/小程序媒体变更入口清单 |
| MediaEvidenceFiveTuple | REQ-0115 / REQ-0120 | 媒体验收记录 key、object、URL、render/Network、体积或耗时收益，避免单点证据过度推断 |
| StorageMaintenanceBlockedSummary | REQ-0117 / BUG-0134 | dry-run 顶层区分 storage unavailable、object missing、historical key drift，并输出脱敏建议动作 |
| VersionUpgradeEvidenceModel | REQ-0114 | 部署支持级别以 release facts、env diff、DB smoke/drift 和 rollback evidence 标注可信度 |
| WorkflowYamlFrontmatterWriter | BUG-0138 | trace/frontmatter 写入走结构化 YAML parser round-trip，防止嵌套状态污染顶层 Issue 状态 |
| SprintAiUsageAttributionGate | sprint-025 archive/exps | post-command hook 先校验 target turn、sprint coverage、fresh gate 和 matrix write gate，失败时给出可执行补洞动作 |

## 行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 优化 AI usage post-command hook 的目标 turn 选择与 Sprint 归因提示，减少 snapshot 缺失或误选零 token turn | `/opsx-propose` | open |
| T-002 | P1 | 将媒体五联验收模板沉淀为可复用 checklist，覆盖 key、object、URL、render/Network、收益指标 | `/req-capture` | open |
| T-003 | P2 | 为图片三规格消费矩阵增加新页面/新媒体位准入检查，防止后续新增入口绕过轻量图策略 | `/opsx-propose` | open |
| T-004 | P2 | 将对象存储不可达与对象缺失分类扩展到更多维护脚本输出，保持 blocked/summary/脱敏建议一致 | `/req-capture` | open |
| T-005 | P2 | 为大 Sprint 归档命令增加 snapshot/fresh-gate 前置 dry-run 建议，避免关闭记录先写 estimated_fallback | `/opsx-propose` | open |

## Follow-up Capture 建议

未自动创建 Issue。建议后续按团队优先级选择 capture：

1. 建议命令：`/opsx-propose`
   类型倾向：治理 Change
   标题：优化 AI usage post-command hook 的目标 turn 选择
   背景：sprint-025 归档时 token snapshot 初次缺失，后续需通过 session JSONL 与 manual attribution 刷新为 actual/present。
   影响范围：`scripts/ai_usage.py`、`scripts/extract-ai-usage.py`、`sprint-archive` / `sprint-exps` 技能说明、AI Usage 相关测试。
   建议验收要点：post hook 能优先选择当前 workflow event 的非零 token turn；缺少 sprint_id 时输出 turn_hash/manual-map 建议；dry-run 能在写入前报告 fresh gate 和 coverage 风险。
   来源 Change/Sprint/命令：sprint-025 / `/sprint-archive sprint-025` / `/sprint-exps sprint-025`

2. 建议命令：`/req-capture`
   类型倾向：REQ
   标题：沉淀媒体五联验收模板
   背景：sprint-025 多个媒体 REQ/BUG 均需要证明 key、object、URL、render/Network 与体积收益，单点证据不足以确认端上性能闭环。
   影响范围：媒体上传/派生、对象存储维护、小程序媒体位、Web 管理端回显、验收文档模板。
   建议验收要点：模板能区分 thumbnail/display/original；要求端上 Network 或 render evidence；记录对象存储状态和收益指标；适用于新上传与历史补生成。
   来源 Change/Sprint/命令：REQ-0115、REQ-0120、BUG-0137 / sprint-025 / `/sprint-exps sprint-025`

3. 建议命令：`/opsx-propose`
   类型倾向：治理 Change
   标题：为媒体消费矩阵增加准入检查
   背景：sprint-025 修复多处小程序普通展示回退原图问题，说明新增媒体位容易绕过已沉淀的三规格消费矩阵。
   影响范围：媒体消费矩阵文档、相关 lint/check 脚本、Sprint/Change 验收清单。
   建议验收要点：新增页面或媒体位必须声明 thumbnail/display/original 消费策略；非原图场景不得 fallback 到 original；检查结果能定位页面、字段和建议修复动作。
   来源 Change/Sprint/命令：REQ-0118、BUG-0137 / sprint-025 / `/sprint-exps sprint-025`
