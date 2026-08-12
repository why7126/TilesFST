---
created_at: 2026-08-07 09:06:21
updated_at: 2026-08-12 00:20:00
sprint_id: sprint-022
---

# 发布说明

## 变更摘要

- 关闭 sprint-022：18 个 OpenSpec Change 已全部归档，覆盖治理流程优化、商品召回置顶、小程序置顶标识、Banner 展示优化、RUM 性能观测、媒体性能修复、管理端主题入口、日志审计性能和用户联系信息维护。
- 小程序商品详情、品牌链路媒体加载修复已完成缩略图 URL 语义、懒加载、缓存与验收 evidence 回填。
- 管理后台 Banner、主题用户菜单、日志审计、身份展示和用户联系信息维护相关能力已完成 API/OpenAPI/Orval、文档与测试同步（按各 Change 适用范围）。

## 影响范围

- 项目治理工作流、Agent 技能入口与 spec-logs 治理日志。
- 后端 FastAPI、SQLite/MySQL 文档、OpenAPI/Orval 生成物和相关 pytest。
- Web 管理端 Banner、主题偏好、性能观测、日志审计、用户管理与身份展示。
- 微信小程序商品列表、商品详情、品牌列表、品牌详情和品牌分类商品列表媒体展示。

## 发布风险

- Sprint 内 Change 均已归档；发布前仍应按版本发布流程复核环境变量、Docker/镜像证据和产品使用文档是否需要生成。
- AI usage 快照当前为 `estimated_fallback` 且 stale；如需真实成本复盘，需提供本地 session JSONL 后刷新。
