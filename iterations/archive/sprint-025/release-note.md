---
title: sprint-025 发布说明
created_at: 2026-08-21 18:43:30
updated_at: 2026-08-25 14:45:16
publish_status: published
---

# sprint-025 发布说明

## 发布范围

| 类型 | 编号 | 标题 | 状态 | 说明 |
|---|---|---|---|---|
| REQ | REQ-0114-version-deployment-upgrade-rollback-governance | 版本部署升级与回滚治理能力 | done | Change 已归档，发布治理、升级计划与回滚证据规则已闭环 |
| REQ | REQ-0115-media-multi-variant-images | 媒体图片多规格展示图能力 | done | Change 已归档，previewImage 返修与小程序 Network 验收已闭环 |
| REQ | REQ-0119-admin-display-image-size-limit-setting | 管理端媒体与存储新增 display 图体积目标上限配置 | done | Change 已归档，系统设置 API、管理端 UI 与 display 派生图证据已闭环 |

## 预期发布影响

- 发布治理：新增版本部署升级与回滚计划能力。
- 部署治理：补齐首次部署、相邻升级、跨版本升级和回滚证据要求。
- 环境治理：补齐 env diff、生产必填项和示例值安全检查。
- 数据库治理：补齐 MySQL drift/smoke、备份和回滚证据门禁。
- 镜像治理：复用同一目标版本镜像，不按部署场景拆分镜像。
- 媒体治理：新增图片 `thumbnail / display / original` 多规格生成和选择策略。
- 对象存储：对象存储直出纳入本期，需明确签名、缓存、权限和 fallback。
- 小程序体验：列表、详情、预览分别使用不同规格 URL，并补 Network evidence。
- 小程序预览：SKU 详情图片预览按 media 下标使用 `original_url || preview_url || url`，确保点击预览优先请求原图。
- 小程序详情：SKU 详情接口只返回可用的 `display_url` / `thumbnail_url`，派生展示图缺失时端侧使用本地占位图，不回退原图冷加载。
- 小程序首页：Banner 和商品卡缺图时使用视图占位或现有空态，不请求不存在的本地占位图资源。
- 管理端设置：媒体与存储设置需新增 display 图体积目标上限，默认 768KB，并与缩略图体积目标独立。

## 非发布范围

- 不建设可视化升级平台。
- 不自动执行生产升级。
- 不自动修改真实生产 env。
- 不自动执行写入型 DB 或对象存储维护任务。
- 不做视频转码或多清晰度视频。
- 不把生产 CDN 正式接入作为本期必达项。

## 发布门禁结果

- 18/18 OpenSpec Change 已归档并通过验收。
- Workflow Sync、readiness、stale scan 与 issue promote gate 无 blocker。
- 相关脚本、规范、技能、长期文档、OpenAPI / Orval 与测试证据已同步。
- 发布治理、媒体链路、小程序 Network/render、display 图配置与批处理 Runbook 证据已闭环。
- AI usage snapshot 缺失，本次关闭按 estimated_fallback 警告记录；真实 token 成本需后续使用本地 session JSONL 刷新。
