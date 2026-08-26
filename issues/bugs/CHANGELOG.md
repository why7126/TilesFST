---
purpose: 缺陷当前态看板索引
content: 每个 BUG 一行的当前状态、阶段、Sprint、Change、下一步和事实源路径摘要
source: /spec-study apply ProjectMoonBox 治理学习改写
update_method: BUG capture、生成、补齐、评审、纳入 Sprint、创建 Change、apply、archive 或状态同步后按需更新对应行
created_at: 2026-08-10 23:28:57
updated_at: 2026-08-26 09:52:55
---

# 缺陷当前态看板索引

本文件只作为目录级当前态索引，不替代 `_registry.yaml`、单条 `trace.md`、Sprint 四件套或 OpenSpec Change 事实源。

| BUG | 标题 | 状态 | 阶段 | Sprint | Change | 最近更新时间 | 下一步 | 事实源 |
|---|---|---|---|---|---|---|---|---|
| BUG-0144-miniapp-usage-events-overreporting | 小程序商品列表页与搜索页 usage-events 仍可能偏多 | in_sprint | review | sprint-026 | fix-miniapp-usage-events-overreporting | 2026-08-26 09:52:55 | `/opsx-archive BUG-0144-miniapp-usage-events-overreporting` | `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/trace.md` |
| BUG-0143-miniapp-telemetry-request-amplification | 微信小程序启动阶段埋点请求数量异常偏高 | in_sprint | review | sprint-026 | fix-miniapp-telemetry-request-amplification | 2026-08-26 08:10:19 | `/opsx-archive BUG-0143-miniapp-telemetry-request-amplification` | `issues/bugs/review/BUG-0143-miniapp-telemetry-request-amplification/trace.md` |
| BUG-0141-ai-usage-token-count-jsonl | AI usage extractor 未识别新版 token_count JSONL 导致 Sprint snapshot 缺失 | in_sprint | review | sprint-026 | fix-ai-usage-message-content-token-count | 2026-08-25 18:22:19 | `/opsx-archive BUG-0141-ai-usage-token-count-jsonl` | `issues/bugs/review/BUG-0141-ai-usage-token-count-jsonl/trace.md` |
| BUG-0140-admin-current-user-avatar-missing-object | 当前登录用户头像引用缺失媒体对象 | done | archive | sprint-026 | fix-admin-current-user-avatar-object-consistency | 2026-08-25 17:41:57 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0140-admin-current-user-avatar-missing-object/trace.md` |
| BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | Workflow Sync 写入 REQ trace frontmatter 时可能生成非法 YAML 结构 | done | archive | sprint-025 | fix-workflow-sync-trace-frontmatter-invalid-yaml | 2026-08-25 10:22:24 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml/trace.md` |
| BUG-0137-miniapp-lightweight-image-variant-consumption | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 | done | review | sprint-025 | fix-miniapp-lightweight-image-variant-consumption | 2026-08-25 09:43:38 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0137-miniapp-lightweight-image-variant-consumption/trace.md` |
| BUG-0136-workflow-sync-bug-generate-captured-draft | Workflow Sync 对 bug.generate 未主动从 captured 推进 draft | done | archive | sprint-025 | fix-workflow-sync-bug-generate-status-transition | 2026-08-22 21:56:07 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0136-workflow-sync-bug-generate-captured-draft/trace.md` |
| BUG-0135-miniapp-certificate-card-file-url-fallback | 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件 | done | review | sprint-025 | fix-miniapp-certificate-card-file-url-fallback | 2026-08-22 21:59:26 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0135-miniapp-certificate-card-file-url-fallback/trace.md` |
| BUG-0134-miniapp-certificate-detail-display-url | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 | done | review | sprint-025 | fix-miniapp-certificate-detail-display-url | 2026-08-24 17:15:07 | 暂无可推进下一步 | `issues/bugs/archive/BUG-0134-miniapp-certificate-detail-display-url/trace.md` |
| BUG-0131-miniapp-sku-detail-carousel-original-image-height | 小程序商品详情页轮播图清晰度不足且高度偏小 | in_sprint | review | sprint-024 | fix-miniapp-sku-detail-carousel-original-image-height | 2026-08-21 13:54:57 | `/opsx-archive BUG-0131-miniapp-sku-detail-carousel-original-image-height` | `issues/bugs/archive/BUG-0131-miniapp-sku-detail-carousel-original-image-height/trace.md` |
| BUG-0130-miniapp-home-no-jump-banner-internal-title | 小程序首页无跳转轮播图显示内部标题 | in_sprint | review | sprint-024 | fix-miniapp-home-no-jump-banner-internal-title | 2026-08-21 08:45:32 | `/opsx-apply BUG-0130-miniapp-home-no-jump-banner-internal-title` | `issues/bugs/archive/BUG-0130-miniapp-home-no-jump-banner-internal-title/trace.md` |
| BUG-0128-admin-user-menu-email-subtitle | 管理后台身份展示不应显示伪邮箱 | in_sprint | review | sprint-022 | fix-admin-identity-fake-email-display | 2026-08-11 22:12:00 | `/opsx-apply BUG-0128-admin-user-menu-email-subtitle` | `issues/bugs/archive/BUG-0128-admin-user-menu-email-subtitle/trace.md` |
| 待同步 | 待同步 | 待同步 | 待同步 | 待同步 | 待同步 | 2026-08-10 23:28:57 | 后续命令按需更新对应行 | `_registry.yaml` |
