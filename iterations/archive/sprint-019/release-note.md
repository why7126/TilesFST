---
sprint_id: sprint-019
title: Sprint 019 发布说明
status: published
created_at: 2026-08-04 00:00:00
updated_at: 2026-08-04 23:08:58
owner: product
---

# Sprint 019 发布说明

## 1. 发布摘要

本 Sprint 已交付 11 个归档 Change，覆盖归档证据 trace/fallback、Fact Sheet compact summary、管理端列表字段 adapter 检查表、小程序 Network 面板发布清单、生产媒体维护作业入口、证书图片对象 key 前缀修复、usage docs 前置版本 SemVer 排序修复、Fact Sheet AI usage fresh gate snapshot 修复、小程序品牌列表对齐与返回首页按钮回归修复，以及生产历史媒体对象漂移修复。

## 2. 正式范围

| 类型 | 编号 | 说明 |
|---|---|---|
| Change | `auto-archive-trace-fallback` | archived Change 缺 trace 时自动生成最小归档 trace 或结构化 fallback 摘要 |
| Change | `add-compact-fact-sheet-summary-for-large-sprints` | 大型 Sprint Fact Sheet summary 默认输出 compact AI usage 摘要，完整矩阵按需读取 |
| BUG | `BUG-0112-certificate-image-object-key-prefix` | 修复证书图片对象 key 未归入 `images/` 前缀 |
| Change | `fix-certificate-image-object-key-prefix` | 收敛证书图片/PDF key 分流、缩略图、历史迁移、规范、Skill 与测试 |
| Change | `fix-usage-docs-previous-version-semver-sort` | 修复 usage docs 前置版本 SemVer 排序 |
| Change | `fix-fact-sheet-ai-usage-fresh-gate-snapshot` | 修复 AI usage fresh gate snapshot 状态判断 |
| Change | `standardize-admin-list-field-display-adapters` | 建立管理端列表字段展示 adapter 检查表 |
| Change | `update-miniapp-network-panel-release-checklist` | 小程序 Network 面板验证纳入发布准备清单 |
| Change | `fix-miniapp-brand-list-category-column-alignment` | 修复小程序品牌类目两列对齐 |
| Change | `fix-miniapp-home-button-repeat-click-regression` | 修复返回首页按钮二次点击失效 |
| Change | `add-prod-media-maintenance-jobs` | 增加生产媒体维护作业入口 |
| Change | `fix-prod-media-historical-object-drift` | 修复生产历史媒体对象与缩略图规范漂移 |

## 3. 影响说明

- API：BUG-0112 若实现调整上传响应字段或 Schema，必须同步 OpenAPI / Orval；若仅修正 `object_key` 值形态则不新增接口。
- 数据库：不改表结构；可能通过迁移脚本更新历史证书图片 key 引用。
- Web：需验收管理端证书上传、编辑、列表/弹窗回显。
- 微信小程序：需按影响范围验收证书图片展示或明确 N/A。
- 管理端：影响品牌证书图片上传、缩略图和回显。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：需要补充归档证据校验与 workflow 相关 pytest。
- 测试：需要补充 Fact Sheet summary compact 与 fields 完整矩阵读取 pytest。
- 测试：需要补充证书图片/PDF key 分流、缩略图、历史迁移 dry-run/apply 幂等和媒体四联验收。

## 4. 发布风险

| 风险 | 缓解 |
|---|---|
| fallback 误放宽归档 blocker | 测试覆盖 incomplete tasks、缺失 tasks、legacy archive path 和 Issue 未闭环仍阻断 |
| 自动 trace 语义不清 | 自动生成 trace 明确标记来源与证据字段，不写无法确认的验收结论 |
| compact summary 影响矩阵落表 | 保留 `usage_matrices_summary` 和 fields 完整矩阵读取路径 |
| 证书图片 key 迁移不完整 | 历史迁移先 dry-run，apply 后复核对象存在、数据库引用和受控 URL |
