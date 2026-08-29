---
note: workflow-sync — workflow-sync 自动同步 — 16/16 Change archived；0 applied；Sprint `completed`
title: sprint-026 归档
created_at: 2026-08-25 15:21:18
updated_at: 2026-08-28 16:29:38
---

# sprint-026 归档

## 1. 目标

### Sprint 目标编号列表

- BUG-0141-ai-usage-token-count-jsonl
- BUG-0140-admin-current-user-avatar-missing-object
- BUG-0139-admin-avatar-upload-nginx-redirect-cors
- REQ-0123-upload-stage-trace-spans
- BUG-0142-admin-avatar-upload-storage-put-slow
- REQ-0124-log-audit-behavior-trace-model
- REQ-0125-miniapp-certificate-detail-home-floating-button
- BUG-0143-miniapp-telemetry-request-amplification
- BUG-0144-miniapp-usage-events-overreporting
- BUG-0145-admin-log-detail-field-overlap
- REQ-0126-product-data-collection-observability-standard
- REQ-0127-product-data-collection-observability-hard-gate
- REQ-0128-search-experience-unification
- REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
- refine-skill-final-output-contract
- fix-workflow-sync-sprint-propose-iteration

### BUG-0141-ai-usage-token-count-jsonl 要点

修复 AI usage extractor 对新版 Codex session JSONL 的解析缺陷：新版用户消息使用 `payload.type=message`、`payload.role=user`、`payload.content` 文本片段列表；提取器已能创建 command run，后续 `payload.type=token_count` 可归属到对应命令运行，并让 `sprint-025` snapshot 恢复 actual 用量模式。Change `fix-ai-usage-message-content-token-count` 已归档。

### BUG-0140-admin-current-user-avatar-missing-object 要点

修复管理后台当前登录用户头像引用缺失媒体对象的问题：历史用户头像 key 已补齐受控数据修复流程，后端头像更新链路已校验 `avatar_object_key` 对应 object 存在，个人资料页头像加载失败已 fallback 到 initials。该 BUG 属于管理端媒体一致性缺陷，Change `fix-admin-current-user-avatar-object-consistency` 已归档。

### BUG-0139-admin-avatar-upload-nginx-redirect-cors 要点

修复管理后台头像上传无尾斜杠路径被 Web Nginx 301 重定向后丢失宿主机端口的问题：补齐 `/api/v1/admin/uploads` 精确匹配，保持 Docker Web `localhost:3000` 同源上传链路，避免 CORS 预检拦截。该 BUG 属于管理端媒体上传代理缺陷，Change `fix-admin-avatar-upload-nginx-redirect-cors` 已归档。

### REQ-0123-upload-stage-trace-spans 要点

为头像上传和通用图片上传分支补齐阶段级耗时可观测能力：阶段耗时优先写入 task trace spans，而不只是日志；至少覆盖 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object`。该 REQ 对应 Change `add-upload-stage-trace-spans` 已归档。

### BUG-0142-admin-avatar-upload-storage-put-slow 要点

修复管理端头像上传 127KB WebP 文件返回 200 但等待约 31.74 秒的问题：阶段级 trace 已确认主要耗时来自 `thumbnail_generate=28464ms`，而非对象存储写入。该 BUG 已评审通过且根因 confirmed，本 Sprint 先纳入正式范围，后续通过 `/bug-opsx` 创建修复 Change 并回填本 Sprint scope。

### REQ-0124-log-audit-behavior-trace-model 要点

为日志审计补齐用户行为链路、接口请求链路和任务流程节点采集模型：界面触发入口通过 `usage_events.behavior_trace_id` 关联 `request_logs.behavior_trace_id`，再通过 `task_traces.parent_request_id` 与 `task_trace_spans` 联动；直接 API 调用保留 `behavior_trace_id` 可空，并从 `request_logs.request_id` 独立进入任务链路。该 REQ 已评审通过并已创建 `add-log-audit-behavior-trace-model` Change，后续通过 `/opsx-apply REQ-0124-log-audit-behavior-trace-model` 实现。

### REQ-0125-miniapp-certificate-detail-home-floating-button 要点

为小程序证书详情页补齐【返回首页】悬浮按钮，复用既有 `home-floating-button` 组件并保持 `offset="list"` 与品牌详情页、商品列表页等深层内容页一致。该 REQ 已评审通过，当前先纳入 Sprint 正式范围，后续通过 `/req-opsx` 创建 OpenSpec Change 并回填同一 Sprint scope。

### BUG-0143-miniapp-telemetry-request-amplification 要点

修复微信小程序启动阶段埋点请求数量异常偏高的问题：`track()` 上报 usage-events 时不应继续触发 RUM，商品卡曝光应去重、采样或批量上报，首页业务 API 的性能观测仍需保留。该 BUG 已评审通过且根因 confirmed，当前先纳入 Sprint 正式范围，后续通过 `/bug-opsx` 创建修复 Change 并回填本 Sprint scope。

### BUG-0144-miniapp-usage-events-overreporting 要点

治理小程序商品列表页与搜索页 usage-events 仍可能偏多的问题：商品列表页应收敛 `product_list_item_exposure` 与 `product_card_exposure` 双口径，搜索页输入埋点应具备防抖、合并或采样等频控策略，搜索结果与商品卡曝光应有清晰去重窗口。该 BUG 已评审通过且根因 confirmed，当前先纳入 Sprint 正式范围，后续通过 `/bug-opsx` 创建修复 Change 并回填本 Sprint scope。

### BUG-0145-admin-log-detail-field-overlap 要点

修复 Web 管理端日志详情抽屉长字段名和值重叠的问题：`parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 等排障字段必须在基础信息和 Request Snapshot 中保持可读，字段说明 tooltip 的 hover/focus 可访问性不得丢失。该 BUG 已评审通过且根因 confirmed，当前先纳入 Sprint 正式范围，后续通过 `/bug-opsx` 创建修复 Change 并回填本 Sprint scope。

### REQ-0126-product-data-collection-observability-standard 要点

建立通用产品数据采集与链路观测规范，把 REQ-0124 的项目内行为链路模型沉淀为跨产品标准：覆盖小程序、店主端、App、Web 管理端和后端 API，明确 `usage_events -> request_logs -> task_traces -> task_trace_spans` 四层链路、直接 API 调用入口、Task Trace 分级覆盖、默认保留周期、敏感字段脱敏和新产品接入 checklist。该 REQ 已评审通过，当前先纳入 Sprint 正式范围，后续通过 `/req-opsx` 创建 OpenSpec Change 并回填同一 Sprint scope。

### REQ-0127-product-data-collection-observability-hard-gate 要点

将 `docs/standards/product-data-collection-observability.md` 从参考规范提升为流程硬门禁，接入 `AGENTS.md`、相关 `rules/`、req / opsx / sprint 技能检查清单和实现级校验脚本。该 REQ 已评审通过，当前先纳入 Sprint 正式范围，后续通过 `/req-opsx` 创建 OpenSpec Change 并回填同一 Sprint scope；在 Change 设计中必须保留 `product_data_collection_observability` 适用性声明、affected layers、N/A 规则和校验脚本策略。

### REQ-0128-search-experience-unification 要点

统一搜索体验：强化小程序首页搜索入口，复用或增强 `search-entry` 入口契约，以 `/pages/search/index` 继续承接搜索首页、联想和结果页；同时补齐分类、品牌、证书、商品、收藏等小程序主要列表搜索路径，并统一管理端品牌、类目、SKU、规格、Banner、证书、用户、日志等主要列表关键词搜索、筛选、重置、分页和空态体验。该 REQ 已评审通过，当前先纳入 Sprint 正式范围，后续通过 `/req-opsx` 创建 OpenSpec Change 并回填同一 Sprint scope；在 Change 设计中必须保留搜索行为事件、请求链路、关键词脱敏、API / Orval 影响和 Task Trace N/A 声明。

### REQ-0129-miniapp-sku-detail-actionbar-compact-favorite 要点

优化小程序商品详情页底部操作栏：收藏按钮去掉可见第二行“收藏 / 已收藏”文字，仅保留心形状态表达；在保持收藏交互、toast 反馈和分享主按钮优先级不变的前提下压缩 actionbar 高度，并同步调整返回首页悬浮按钮 offset。该 REQ 已评审通过，当前先纳入 Sprint 正式范围，后续通过 `/req-opsx` 创建 OpenSpec Change 并回填同一 Sprint scope；Change 验收必须覆盖 320/375/430pt 视觉证据、安全区、不遮挡和 product_data_collection_observability N/A 复核。

### fix-workflow-sync-sprint-propose-iteration 要点

修复 Workflow Sync 在 `sprint.propose` 后未自动回填已纳入 REQ/BUG `trace.md` `iteration` 的治理一致性问题。该 Change 只调整治理脚本、规则说明和聚焦测试，不修改业务 `src/`、API、DB、Web、小程序或管理端。

### refine-skill-final-output-contract 要点

优化命令技能最终输出契约，统一 `下一步` 与 `待用户决策/处理` 的真实结果表达，移除占位模板、通用示例和重复确认诱因，并扩展上下文预算校验脚本覆盖契约卫生风险。该 Change 已归档。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0123-upload-stage-trace-spans | 上传链路阶段级耗时写入 trace spans | done | 3 人天 | archived `add-upload-stage-trace-spans`（2026-08-25 19:16:00） |
| REQ | REQ-0124-log-audit-behavior-trace-model | 日志审计补齐行为链路与任务链路采集模型 | done | 5 人天 | archived `add-log-audit-behavior-trace-model`（2026-08-27 23:10:25） |
| REQ | REQ-0125-miniapp-certificate-detail-home-floating-button | 小程序证书详情页新增返回首页悬浮按钮 | done | 0.5 人天 | archived `update-miniapp-certificate-detail-home-floating-button`（2026-08-26 08:32:09） |
| REQ | REQ-0126-product-data-collection-observability-standard | 建立通用产品数据采集与链路观测规范 | done | 1 人天 | archived `add-product-data-collection-observability-standard`（2026-08-26 19:36:50） |
| REQ | REQ-0127-product-data-collection-observability-hard-gate | 产品数据采集与链路观测规范硬门禁 | done | 1 人天 | archived `add-product-data-collection-observability-hard-gate`（2026-08-27 23:14:21） |
| REQ | REQ-0128-search-experience-unification | 搜索体验统一优化 | done | 5 人天 | archived `update-search-experience-unification`（2026-08-28 13:02:11） |
| REQ | REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | 小程序商品详情页底部收藏按钮与操作栏紧凑化 | done | 0.5 人天 | archived `update-miniapp-sku-detail-actionbar-compact-favorite`（2026-08-28 14:27:38） |
| BUG | BUG-0141-ai-usage-token-count-jsonl | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | done | 1 人天 | archived `fix-ai-usage-message-content-token-count`（2026-08-25 15:13:14） |
| BUG | BUG-0140-admin-current-user-avatar-missing-object | 当前登录用户头像引用缺失媒体对象 | done | 1 人天 | archived `fix-admin-current-user-avatar-object-consistency`（2026-08-25 15:44:17） |
| BUG | BUG-0139-admin-avatar-upload-nginx-redirect-cors | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 | done | 1 人天 | archived `fix-admin-avatar-upload-nginx-redirect-cors`（2026-08-25 15:35:15） |
| BUG | BUG-0142-admin-avatar-upload-storage-put-slow | 管理端头像上传小文件对象存储写入耗时 30 秒以上 | done | 1 人天 | archived `fix-admin-avatar-webp-thumbnail-timeout`（2026-08-25 22:35:18） |
| BUG | BUG-0143-miniapp-telemetry-request-amplification | 微信小程序启动阶段埋点请求数量异常偏高 | done | 1 人天 | archived `fix-miniapp-telemetry-request-amplification`（2026-08-27 23:19:01） |
| BUG | BUG-0144-miniapp-usage-events-overreporting | 小程序商品列表页与搜索页 usage-events 仍可能偏多 | done | 1 人天 | archived `fix-miniapp-usage-events-overreporting`（2026-08-27 23:13:09） |
| BUG | BUG-0145-admin-log-detail-field-overlap | 管理端日志详情长字段名和值重叠 | done | 1 人天 | archived `fix-admin-log-detail-field-overlap`（2026-08-27 00:49:46） |
| Change | refine-skill-final-output-contract | refine skill final output contract | archived | 1 人天 | archived `refine-skill-final-output-contract`（2026-08-27 23:20:11） |
| Change | fix-workflow-sync-sprint-propose-iteration | fix workflow sync sprint propose iteration | archived | 1 人天 | archived `fix-workflow-sync-sprint-propose-iteration`（2026-08-27 23:15:02） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0123 | 上传链路阶段级耗时写入 trace spans | P1 | done | archived `add-upload-stage-trace-spans`（2026-08-25 19:16:00） |
| REQ-0124 | 日志审计补齐行为链路与任务链路采集模型 | P1 | done | archived `add-log-audit-behavior-trace-model`（2026-08-27 23:10:25） |
| REQ-0125 | 小程序证书详情页新增返回首页悬浮按钮 | P2 | done | archived `update-miniapp-certificate-detail-home-floating-button`（2026-08-26 08:32:09） |
| REQ-0126 | 建立通用产品数据采集与链路观测规范 | P1 | done | archived `add-product-data-collection-observability-standard`（2026-08-26 19:36:50） |
| REQ-0127 | 产品数据采集与链路观测规范硬门禁 | P1 | done | archived `add-product-data-collection-observability-hard-gate`（2026-08-27 23:14:21） |
| REQ-0128 | 搜索体验统一优化 | P1 | done | archived `update-search-experience-unification`（2026-08-28 13:02:11） |
| REQ-0129 | 小程序商品详情页底部收藏按钮与操作栏紧凑化 | P2 | done | archived `update-miniapp-sku-detail-actionbar-compact-favorite`（2026-08-28 14:27:38） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0141 | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | medium | done | archived `fix-ai-usage-message-content-token-count`（2026-08-25 15:13:14） |
| BUG-0140 | 当前登录用户头像引用缺失媒体对象 | high | done | archived `fix-admin-current-user-avatar-object-consistency`（2026-08-25 15:44:17） |
| BUG-0139 | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 | high | done | archived `fix-admin-avatar-upload-nginx-redirect-cors`（2026-08-25 15:35:15） |
| BUG-0142 | 管理端头像上传小文件对象存储写入耗时 30 秒以上 | high | done | archived `fix-admin-avatar-webp-thumbnail-timeout`（2026-08-25 22:35:18） |
| BUG-0143 | 微信小程序启动阶段埋点请求数量异常偏高 | medium | done | archived `fix-miniapp-telemetry-request-amplification`（2026-08-27 23:19:01） |
| BUG-0144 | 小程序商品列表页与搜索页 usage-events 仍可能偏多 | medium | done | archived `fix-miniapp-usage-events-overreporting`（2026-08-27 23:13:09） |
| BUG-0145 | 管理端日志详情长字段名和值重叠 | medium | done | archived `fix-admin-log-detail-field-overlap`（2026-08-27 00:49:46） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `fix-ai-usage-message-content-token-count` | BUG-0141-ai-usage-token-count-jsonl | archived | archived `fix-ai-usage-message-content-token-count`（2026-08-25 15:13:14） |
| `fix-admin-current-user-avatar-object-consistency` | BUG-0140-admin-current-user-avatar-missing-object | archived | archived `fix-admin-current-user-avatar-object-consistency`（2026-08-25 15:44:17） |
| `fix-admin-avatar-upload-nginx-redirect-cors` | BUG-0139-admin-avatar-upload-nginx-redirect-cors | archived | archived `fix-admin-avatar-upload-nginx-redirect-cors`（2026-08-25 15:35:15） |
| `add-upload-stage-trace-spans` | REQ-0123-upload-stage-trace-spans | archived | archived `add-upload-stage-trace-spans`（2026-08-25 19:16:00） |
| `fix-admin-avatar-webp-thumbnail-timeout` | BUG-0142-admin-avatar-upload-storage-put-slow | archived | archived `fix-admin-avatar-webp-thumbnail-timeout`（2026-08-25 22:35:18） |
| `add-log-audit-behavior-trace-model` | REQ-0124-log-audit-behavior-trace-model | archived | archived `add-log-audit-behavior-trace-model`（2026-08-27 23:10:25） |
| `update-miniapp-certificate-detail-home-floating-button` | REQ-0125-miniapp-certificate-detail-home-floating-button | archived | archived `update-miniapp-certificate-detail-home-floating-button`（2026-08-26 08:32:09） |
| `fix-miniapp-telemetry-request-amplification` | BUG-0143-miniapp-telemetry-request-amplification | archived | archived `fix-miniapp-telemetry-request-amplification`（2026-08-27 23:19:01） |
| `fix-miniapp-usage-events-overreporting` | BUG-0144-miniapp-usage-events-overreporting | archived | archived `fix-miniapp-usage-events-overreporting`（2026-08-27 23:13:09） |
| `add-product-data-collection-observability-standard` | REQ-0126-product-data-collection-observability-standard | archived | archived `add-product-data-collection-observability-standard`（2026-08-26 19:36:50） |
| `add-product-data-collection-observability-hard-gate` | REQ-0127-product-data-collection-observability-hard-gate | archived | archived `add-product-data-collection-observability-hard-gate`（2026-08-27 23:14:21） |
| `refine-skill-final-output-contract` | — | archived | archived `refine-skill-final-output-contract`（2026-08-27 23:20:11） |
| `fix-workflow-sync-sprint-propose-iteration` | — | archived | archived `fix-workflow-sync-sprint-propose-iteration`（2026-08-27 23:15:02） |
| `update-search-experience-unification` | REQ-0128-search-experience-unification | archived | archived `update-search-experience-unification`（2026-08-28 13:02:11） |
| `fix-admin-log-detail-field-overlap` | BUG-0145-admin-log-detail-field-overlap | archived | archived `fix-admin-log-detail-field-overlap`（2026-08-27 00:49:46） |
| `update-miniapp-sku-detail-actionbar-compact-favorite` | REQ-0129-miniapp-sku-detail-actionbar-compact-favorite | archived | archived `update-miniapp-sku-detail-actionbar-compact-favorite`（2026-08-28 14:27:38） |
<!-- workflow-sync:scope-changes:end -->

BUG：BUG-0141 已纳入正式范围且 Change 已 apply，待 archive；BUG-0140 已纳入正式范围且 Change 已 apply，下一步执行 `/opsx-archive BUG-0140-admin-current-user-avatar-missing-object`。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 25 SP / 25 人天 |
| 容量占用 | 83.33% |
| fix 缓冲 | 5 人天 / 16.67% |

容量门禁通过。`project.yaml` 未提供显式 Sprint 容量，沿用最近已归档 Sprint 的确认容量基线：2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 1 个 P1 媒体上传可观测性 REQ、1 个 P1 日志审计链路观测 REQ、1 个 P1 通用数据采集与链路观测规范 REQ、1 个 P1 采集规范硬门禁治理 REQ、1 个 P1 搜索体验统一 REQ、2 个 P2 小程序体验一致性 REQ、1 个 medium 治理脚本 BUG、1 个 P1 Workflow Sync 治理一致性 Change、2 个 medium 小程序埋点请求治理 BUG、1 个 medium 管理端日志详情 UI BUG 与 3 个 high 管理端媒体 BUG，合计估算 25 人天，占用 83.33%。fix 缓冲为 5 人天 / 16.67%，低于 30% 建议线，后续如继续追加范围应优先拆分或移出低优先级项。

## 4. 里程碑

| 阶段 | 目标 |
|---|---|
| OpenSpec | 基于 REQ-0123 创建 `add-*` Change，基于 REQ-0124 创建日志审计链路采集 Change，基于 REQ-0125 创建小程序证书详情页返回首页悬浮按钮 Change，基于 REQ-0126 创建通用产品数据采集与链路观测规范 Change，基于 REQ-0127 创建采集规范硬门禁治理 Change，基于 REQ-0128 创建搜索体验统一优化 Change，基于 BUG-0142、BUG-0143、BUG-0144 与 BUG-0145 创建 `fix-*` Change，回填同一 Sprint scope；BUG-0141 已完成 apply，等待 archive；BUG-0140 与 BUG-0139 已 archived。 |
| 实现 | REQ-0123 覆盖头像上传与通用图片上传 task trace spans；REQ-0124 覆盖 usage_events、request_logs、task_traces、task_trace_spans 链路字段、前端请求透传、直接 API 兼容和日志审计查询；REQ-0125 覆盖证书详情页 `home-floating-button offset="list"` 接入、分享直达和错误态返回首页；REQ-0126 覆盖通用采集规范正文、接入 checklist、保留周期、脱敏边界和后续引用门禁；REQ-0127 覆盖 AGENTS、rules、req/opsx/sprint 技能检查清单和实现级门禁校验脚本；REQ-0128 覆盖小程序搜索入口、搜索页承接、多列表搜索路径、管理端主要列表搜索一致性、搜索行为事件和请求链路观测；BUG-0142 收敛 WebP 头像缩略图生成长尾；BUG-0143 收敛小程序启动阶段 usage/performance 埋点请求放大；BUG-0144 收敛商品列表页与搜索页 usage-events 双口径、高频输入和曝光去重缺口；BUG-0145 收敛管理端日志详情长字段名和值重叠；BUG-0140 覆盖历史头像 key 数据修复、后端头像 key 存在性校验、个人资料页图片失败 fallback；BUG-0139 覆盖 Nginx 无尾斜杠上传代理修复；BUG-0141 完成 AI usage extractor 修复收尾。 |
| 验证 | REQ-0123 验证六阶段 spans、失败保留、脱敏与媒体五联证据；REQ-0124 验证界面行为一对多请求、直接 API 无行为链路、任务请求 parent_request_id、三类链路 ID 查询、敏感字段脱敏、DB/API/Orval 同步与 admin-list 横切 AC；REQ-0125 验证组件声明、WXML 挂载、`.ts`/`.js` 同步、`offset="list"`、分享直达返回兜底、重复点击导航锁和 320/375/430pt 不遮挡；REQ-0126 验证规范覆盖端、四层模型、Task Trace 分级覆盖、默认保留周期、禁止采集字段、新产品接入清单和后续引用方式；REQ-0127 验证采集规范门禁引用、适用性声明、N/A 原因、触发范围识别、校验脚本摘要和事实唯一归属；REQ-0128 验证小程序入口不遮挡、全局搜索与列表内搜索边界、管理端真实分页与重置、关键词脱敏、行为事件、请求链路透传、API/Orval/DB 影响声明和 Task Trace N/A；BUG-0142 验证 127KB WebP 头像上传端到端耗时收敛、`thumbnail_generate` 阶段耗时收敛与媒体四联验收；BUG-0143 验证 usage-events 不触发 RUM、商品卡曝光请求数量可控且首页业务 API 性能观测不退化；BUG-0144 验证商品列表页曝光口径唯一或边界清晰、搜索输入频控、搜索结果与商品卡曝光去重、事件字典兼容和 Network 数量对比；BUG-0145 验证日志详情基础信息与 Request Snapshot 中长字段名和值不重叠、tooltip 可访问性保留、桌面和窄宽度截图通过；BUG-0140 与 BUG-0139 按媒体四联验收 key/object/URL/render；BUG-0139 额外验证 Docker Web `localhost:3000` 不再 301 丢端口；BUG-0141 保持新版 JSONL fixture 与 snapshot actual 恢复验证。 |
| 归档 | 完成 `/opsx-archive BUG-0141-ai-usage-token-count-jsonl`、REQ-0123、REQ-0124、REQ-0125、REQ-0126、REQ-0127、REQ-0128、BUG-0142、BUG-0143、BUG-0144 与 BUG-0145 对应 Change apply/archive 后，回填验收与 Sprint 收尾。 |

## 5. 风险

- 原始 `~/.codex/sessions` 文件包含本机私有会话输入，修复和测试只能使用脱敏最小 fixture，不得复制入仓库。
- 如果只修 `token_count` 事件识别而不修用户消息列表文本提取，snapshot 仍会因为没有 command run 归属而失败。
- 修复后需要重新生成 `sprint-025` snapshot，否则历史复盘仍会显示 `estimated_fallback`。
- BUG-0140 若只做前端 fallback 或只清理当前数据，会掩盖对象存储与用户资料字段漂移，后端写入校验与数据修复证据必须同时完成。
- BUG-0139 若只修带尾斜杠路径或只依赖后端 CORS，会绕过 Docker Web 上传边界；必须覆盖无尾斜杠精确匹配和上传专用代理顺序。
- BUG-0142 若只关注 `storage_put_object` 总耗时命名，可能误判对象存储；实现前必须保留阶段级 trace 证据，优先收敛 `thumbnail_generate`。
- REQ-0123 若只输出日志而未写入 task trace spans，后续仍无法稳定归因上传慢阶段；实现需明确 spans 的事实源、查询入口和失败保留策略。
- REQ-0124 若将 `request_id` 混用为行为链路 ID，会导致一次用户行为触发多个请求时无法归因；实现需保持 `behavior_trace_id`、`behavior_event_id`、`request_id` 和 `task_trace_id` 语义分离。
- REQ-0124 涉及 DB、API、前端请求封装和管理端日志审计，若只改数据表不改查询/展示/测试，会形成“采集了但查不到”的半成品链路。
- REQ-0126 若只沉淀字段名而不沉淀接入 checklist、保留周期、脱敏边界和后续引用方式，会变成一次性说明文档，难以作为跨产品开发规范推进。
- REQ-0126 若把“所有点击”误解为纯 UI 噪音全量采集，可能放大 usage_events 体量并制造隐私与成本风险；规范必须坚持“可命名业务行为采集，纯 UI 噪音可排除”的口径。
- REQ-0127 若只在文档中增加引用而没有实现级校验脚本，采集规范仍会停留在人工记忆层面；后续 Change 必须同时覆盖规则、技能检查清单和脚本验证。
- REQ-0127 若把完整规范正文复制到多个入口，会造成事实源漂移；实现应只写短摘要和路径引用，详细规则继续归属 `docs/standards/product-data-collection-observability.md`。
- REQ-0125 若只在 WXML 挂载按钮而不覆盖分享直达、错误态和重复点击导航锁，可能形成“正常浏览可用但直达/异常状态不可恢复”的体验缺口。
- REQ-0125 若新增页面私有 offset 或样式，会破坏既有 `home-floating-button` 统一口径；实现必须优先复用 `offset="list"`。
- BUG-0143 若只减少 performance-events 而不处理商品卡曝光逐条上报，usage-events 仍会在首页首屏随卡片数量线性膨胀。
- BUG-0143 若直接关闭小程序 RUM，可能丢失首页业务 API 性能观测；实现必须区分遥测请求和业务请求。
- BUG-0144 若只删除某个事件名而不定义商品列表页、搜索页和商品卡组件的主口径，会造成报表口径断层；实现必须明确保留事件、去重键和窗口重置策略。
- REQ-0128 同时覆盖小程序与管理端列表，若后续 Change 不先收敛 MVP 页面清单，容易导致范围扩散；实现前必须明确本期页面清单与延期项。
- REQ-0128 若混淆全局搜索与列表内搜索，会让用户不清楚搜索范围；文案、scope 参数、空态和跳转路径必须明确表达当前搜索语义。
- REQ-0128 若新增多个查询参数但未同步 OpenAPI、Orval、API 文档和测试，会造成端侧类型漂移；Change 设计必须逐项声明复用现有 API、纯前端过滤或新增后端参数。
- REQ-0128 搜索关键词可能包含敏感输入，行为事件和请求日志必须使用脱敏摘要、截断或统计字段，不得无限制保存原文。
- 追加 REQ-0128、REQ-0129、BUG-0145 与 Workflow Sync 治理一致性 Change 后，Sprint fix 缓冲降至 16.67%，低于 30% 建议线；若再追加范围，应优先拆分到下一 Sprint 或移出低优先级项。

## 6. 知识库承接

- 最近复盘 `docs/knowledge-base/retrospectives/sprint-025-retrospective.md` 提醒媒体类验收必须证明 key、object、URL、render/Network 四联，不再把字段存在当成端上已消费。
- 媒体上传最佳实践 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 要求同时验证上传状态机、对象 key、`/media` 代理 URL 与同会话即时回显。
- REQ-0123 承接 sprint-025 媒体五联验收经验：上传可观测性验收除 key/object/URL/render 外，必须补充阶段耗时或瓶颈收益证据。
- REQ-0124 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：日志审计筛选、分页、长字段展示和 fixed toast 必须按管理端列表页一致性 gate 验收。
- REQ-0124 承接 `docs/knowledge-base/retrospectives/sprint-022-retrospective.md` 中 RUM / 日志类观测页经验：复杂观测页需要在 PRD 和 Change 阶段明确主列表、详情链路、敏感字段和后端分页方式。
- REQ-0126 承接 sprint-025 复盘中的 Workflow Sync 和 AI usage 治理经验：规范必须明确事实源分层、保留周期、脱敏边界和接入验收入口，避免观测数据只停留在实现局部。
- REQ-0127 承接 sprint-025 治理脚本闭环经验：产品数据采集与链路观测规范必须进入 AGENTS、rules、技能清单和脚本校验，不能只作为长期文档存在。
- REQ-0125 承接 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`：分享直达、返回兜底、页面 offset、导航锁恢复和 320/375/430pt 截图矩阵必须进入 Change 验收。
- REQ-0128 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：管理端主要列表搜索改造必须保持真实分页、`page-summary` + `page-right`、fixed toast、DS confirm、nowrap/sticky 操作列和筛选 query 语义。
- REQ-0128 承接 sprint-025 治理经验：搜索行为与请求日志属于观测链路，Change 阶段必须保留 product_data_collection_observability 摘要、关键词脱敏和请求链路 ID 透传验证。
- BUG-0145 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 的列展示契约：日志详情中的长字段同样必须使用截断、换行、tooltip/title 或等价可访问策略，不能撑破布局或遮挡值列。
- BUG-0145 承接 `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` 的弹窗/抽屉宽度经验：修复时必须验证运行时 computed 布局，而不只看源 CSS。
- BUG-0139 继续承接同一最佳实践中的 Docker Web `http://localhost:3000` 上传边界检查，不能只验证后端 `:8000` 直连。
- 本 Sprint 继续沿用 AI usage fresh gate 规则：snapshot 未达到 `present` / `actual` / fresh gate pass 前，不输出真实 token 成本矩阵。

## 7. 横切预防清单

- [ ] AI usage fixture 必须脱敏，不含 prompt 原文、系统/开发者指令、工具输出正文、本机绝对路径、Authorization header、Cookie、`.env` 内容或密钥。
- [ ] 回归测试必须覆盖旧式 `user_message.text` 与新版 `message.payload.content[]` 两类用户消息结构。
- [ ] 修复后必须检查 `sprint-025` snapshot 不再因 `required-metrics-empty` 失败。
- [ ] BUG-0140 必须按媒体四联验收覆盖 `key`、`object`、`URL`、`render`，并记录数据修复 dry-run/apply/幂等摘要。
- [ ] 头像更新链路不得接受不存在的 `avatar_object_key`；个人资料页图片失败必须 fallback 到 initials。
- [ ] BUG-0139 必须从 Docker Web `http://localhost:3000` 入口验证 `POST /api/v1/admin/uploads` 不再返回 301，且头像上传控件可成功回显。
- [ ] Nginx 上传专用代理新增无尾斜杠精确匹配后，不得破坏品牌 Logo、Banner、瓷砖图片、瓷砖视频等带子路径上传。
- [ ] REQ-0123 必须在 task trace spans 中验证 `file_read`、`original_put_object`、`thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 六阶段；日志不能作为唯一验收事实源。
- [ ] REQ-0123 接入不得破坏上传状态机、同会话即时回显、`object_key` 与 `/media/{object_key}` 代理读取一致性。
- [ ] REQ-0124 必须验证界面触发入口 `usage_events.behavior_trace_id -> request_logs.behavior_trace_id -> task_traces.parent_request_id -> task_trace_spans` 可联动查询。
- [ ] REQ-0124 必须验证直接 API 调用入口 `request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans` 在 `behavior_trace_id` 为空时仍可排障。
- [ ] REQ-0124 日志审计列表必须保持后端真实分页、长 ID 截断、统一筛选控件、fixed toast 和敏感字段脱敏；不得用前端全量切片伪分页。
- [ ] REQ-0126 必须明确小程序、店主端、App、Web 管理端和后端 API 的统一采集范围，以及不适用项的 N/A 记录方式。
- [ ] REQ-0126 必须明确所有业务 API 请求记录 `request_logs`、直接 API 调用 `behavior_trace_id` 可空、Task Trace 分级覆盖和默认保留周期。
- [ ] REQ-0126 必须把 Authorization、Cookie、Token、密码、真实密钥、完整请求体/响应体、本机绝对路径和真实客户敏感数据列为禁止采集或展示字段。
- [x] REQ-0127 已验证 `AGENTS.md`、相关 `rules/`、req/opsx/sprint 技能检查清单和实现级校验脚本均接入 `docs/standards/product-data-collection-observability.md`。
- [x] REQ-0127 已验证触发范围内的 Change 能声明 `product_data_collection_observability` 适用性、affected layers、N/A 原因和 validation 摘要。
- [x] REQ-0127 已验证实现级校验脚本默认聚焦 active Change、目标 Sprint、REQ 或当前 diff，不默认扫描全部历史 archive。
- [ ] REQ-0125 必须复用 `home-floating-button offset="list"`，不得新增证书详情页私有按钮样式或 offset。
- [ ] REQ-0125 必须覆盖证书详情页正常态、加载失败、证书不可查看、网络失败和分享直达场景的返回首页路径。
- [ ] REQ-0125 必须按小程序自定义导航 best practice 记录 DevTools 320/375/430pt evidence；真机不可用时标记 blocked 或 follow_up。
- [ ] BUG-0143 必须验证 `track()` 上报 `/api/v1/usage-events` 时不再派生 `/api/v1/performance-events`。
- [ ] BUG-0143 必须验证普通首页业务 API 仍会产生 `api_duration`，不得为了降噪关闭业务性能观测。
- [ ] BUG-0143 必须验证商品卡曝光具备去重、采样或批量策略，重复 observer 不导致重复请求。
- [x] BUG-0144 已验证商品列表页 `product_list_item_exposure` 与 `product_card_exposure` 不再无边界双报。
- [x] BUG-0144 已验证搜索页 `search_input` 不再按每个字符变化直接产生不可控 usage-events。
- [x] BUG-0144 已验证搜索结果曝光与商品卡曝光的去重键覆盖 page/sourceModule/listContext/requestId/skuId 等关键上下文。
- [ ] BUG-0145 必须验证日志详情基础信息与 Request Snapshot 中 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 不再和值重叠。
- [ ] BUG-0145 必须验证字段说明 tooltip 的 hover/focus 可访问性保留，且桌面与窄宽度视口均有视觉证据。
- [ ] BUG-0145 产品数据采集与链路观测门禁：适用层级为 Web 管理端日志审计展示；不新增或修改 API、DB、日志采集字段、行为事件、Task Trace 或请求封装，Change 阶段需记录 N/A 原因和视觉验证摘要。

## 8. 依赖

```text
BUG-0141 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0141-ai-usage-token-count-jsonl
        └── /opsx-apply BUG-0141-ai-usage-token-count-jsonl
BUG-0140 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0140-admin-current-user-avatar-missing-object
        └── /opsx-apply BUG-0140-admin-current-user-avatar-missing-object（已完成；下一步 archive）
BUG-0139 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0139-admin-avatar-upload-nginx-redirect-cors
        └── /opsx-apply BUG-0139-admin-avatar-upload-nginx-redirect-cors
REQ-0123 approved
└── sprint-026 scope
    └── /req-opsx REQ-0123-upload-stage-trace-spans
        └── /opsx-apply REQ-0123-upload-stage-trace-spans
REQ-0124 in_sprint
└── sprint-026 scope
    └── add-log-audit-behavior-trace-model archived
        └── openspec/archive/2026-08-27-add-log-audit-behavior-trace-model
REQ-0125 approved
└── sprint-026 scope
    └── /req-opsx REQ-0125-miniapp-certificate-detail-home-floating-button
REQ-0127 done
└── sprint-026 scope
    └── add-product-data-collection-observability-hard-gate archived
        └── openspec/archive/2026-08-27-add-product-data-collection-observability-hard-gate
BUG-0143 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0143-miniapp-telemetry-request-amplification
        └── /opsx-apply BUG-0143-miniapp-telemetry-request-amplification
BUG-0144 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0144-miniapp-usage-events-overreporting
        └── /opsx-apply BUG-0144-miniapp-usage-events-overreporting
BUG-0145 approved
└── sprint-026 scope
    └── /bug-opsx BUG-0145-admin-log-detail-field-overlap
        └── /opsx-apply BUG-0145-admin-log-detail-field-overlap
REQ-0126 approved
└── sprint-026 scope
    └── /req-opsx REQ-0126-product-data-collection-observability-standard
        └── /opsx-apply REQ-0126-product-data-collection-observability-standard
```

## 9. 发布计划

该 Sprint 包含研发治理脚本修复、管理端媒体一致性缺陷修复、管理端头像上传代理修复、媒体上传可观测性增强、日志审计链路观测增强、通用产品数据采集与链路观测规范、小程序证书详情页导航一致性增强、小程序埋点请求治理和管理端日志详情 UI 修复。若进入产品版本发布，REQ-0123 应归类为管理后台上传链路可观测性增强，REQ-0124 应归类为管理后台日志审计与链路观测增强，REQ-0126 应归类为产品研发治理规范增强，REQ-0125 应归类为小程序证书详情页体验优化，BUG-0140 应归类为管理后台头像展示与媒体数据一致性修复，BUG-0139 应归类为管理后台头像上传链路修复，BUG-0143 与 BUG-0144 应归类为小程序性能观测与行为埋点请求治理，BUG-0145 应归类为管理后台日志详情可读性修复。

## 10. 关联文档

- `issues/bugs/archive/BUG-0141-ai-usage-token-count-jsonl/`
- `issues/bugs/archive/BUG-0140-admin-current-user-avatar-missing-object/`
- `issues/bugs/archive/BUG-0139-admin-avatar-upload-nginx-redirect-cors/`
- `issues/requirements/archive/REQ-0123-upload-stage-trace-spans/`
- `issues/requirements/archive/REQ-0124-log-audit-behavior-trace-model/`
- `issues/requirements/archive/REQ-0125-miniapp-certificate-detail-home-floating-button/`
- `issues/requirements/archive/REQ-0126-product-data-collection-observability-standard/`
- `issues/bugs/archive/BUG-0144-miniapp-usage-events-overreporting/`
- `issues/bugs/archive/BUG-0145-admin-log-detail-field-overlap/`
- `scripts/ai_usage.py`
- `tests/test_ai_usage.py`
- `data/ai-usage/sprints/sprint-025.json`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`

## 11. 复盘

- `docs/knowledge-base/retrospectives/sprint-026-retrospective.md`
