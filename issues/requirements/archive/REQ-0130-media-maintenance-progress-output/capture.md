---
req_id: REQ-0130-media-maintenance-progress-output
status: done
created_at: 2026-08-29 18:02:43
updated_at: 2026-08-29 23:04:06
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0097-prod-compose-media-maintenance-job
captured_via: capture
classification_rationale: 用户提出生产媒体维护命令在执行过程中展示总量、完成数和百分比进度，属于已交付维护任务的可观测与运维体验增强，不是现有行为偏差。
---

# 一句话

媒体维护任务应支持可选进度输出，在长时间 backfill / reconcile 执行过程中展示总量、已完成数量和进度百分比，并保持最终 JSON 输出可被脚本稳定解析。

# 原始描述

标题：媒体维护任务进度输出

背景：生产执行 `backfill-image-variants`、`backfill-brand-certificate-thumbnails`、`media-drift-reconcile` 等维护任务时，批量处理图片派生图可能耗时较长。当前命令只在结束后输出 JSON，执行过程中无法直观看到总量、已完成数量和进度百分比。

影响范围：后端媒体维护 CLI、生产 Docker Compose 运维命令、媒体维护 Runbook、测试用例。

建议验收或复现要点：维护命令应提供可选进度输出能力，展示需要完成多少个、已完成多少个和进度百分比；默认 JSON 输出不破坏现有 `jq` / 自动化解析；生产执行时不泄露真实 object key、`.env`、密钥或连接串。

# 分类分析

| 条目 | 类型倾向 | 原因 | 建议命令 |
|---|---|---|---|
| 媒体维护任务进度输出 | REQ | 新增 CLI 运维体验与任务可观测能力；现有命令无进度输出并非故障 | `/req-generate REQ-0130-media-maintenance-progress-output` |

# 背景与关联

- 关联需求：`REQ-0097-prod-compose-media-maintenance-job`、`REQ-0122-batch-image-processing-runbook`
- 涉及端与模块：后端媒体维护 CLI、Docker Compose 生产运维、Runbook、pytest
- 业务价值：降低生产批量媒体维护时的不确定感，便于判断任务是否正常推进、是否卡住以及大致剩余处理量
- 预期后续：在 OpenSpec Change 中设计 `--progress` 或等价参数，明确 stdout / stderr 边界、聚合任务阶段进度和日志脱敏策略

# 待澄清

- [ ] 进度输出优先采用纯文本行、JSON Lines，还是两者都支持
- [ ] 进度输出是否仅在 `--apply` 开启，还是 dry-run 也支持
- [ ] 聚合任务 `media-drift-reconcile` 是否需要展示 4 个子任务阶段级进度

# 建议验收要点

- [ ] 默认不加进度参数时，命令行为保持不变，最终 stdout 仍只输出完整 JSON。
- [ ] 加进度参数后，执行过程中展示 `task`、`total`、`completed`、`success`、`failed`、`skipped`、`progress_percent` 等关键信息。
- [ ] 进度输出不得污染最终 JSON 的 stdout；推荐写入 stderr，确保 `jq` 和生产脚本可继续解析 stdout。
- [ ] `backfill-image-variants`、`backfill-brand-certificate-thumbnails` 和 `media-drift-reconcile` 的长耗时路径都有覆盖。
- [ ] 输出内容只包含统计、阶段名和脱敏信息，不包含真实 object key、`.env`、密钥、连接串、Authorization header 或 Cookie。
- [ ] 测试覆盖默认 JSON 兼容、开启进度后的 stderr 输出、异常失败计数和聚合任务阶段进度。

# 产品数据采集与链路观测适用性

```yaml
product_data_collection_observability:
  applicable: false
  affected_layers: []
  reason: 本需求仅记录媒体维护 CLI 的本地进度输出能力，不新增 API、DB、请求日志、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装；后续若实现改为写入任务追踪表或日志审计表，需在 Change 阶段重新评估。
  validation: capture 阶段仅完成适用性声明；后续 OpenSpec 设计与实现阶段复核。
```

# 探索结论

（/req-explore 后人工确认写入）
