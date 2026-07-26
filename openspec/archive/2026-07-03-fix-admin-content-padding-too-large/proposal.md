---
change_id: fix-admin-content-padding-too-large
title: 管理端全局内容区域间距与宽度收敛修复
created_at: 2026-07-03 18:41:48
updated_at: 2026-07-03 18:41:48
source_bug: BUG-0054-admin-content-padding-too-large
status: proposed
---

## Why

BUG-0054 已评审通过。管理端全局右侧主内容区域仍保留早期宽松布局：`.main-content` 使用 `48px 56px 72px`，`.content-inner` 使用 `max-width: 1080px`，部分页面继续使用 1080/1120px 页面级宽度上限。用户反馈该问题不只影响日志审计页，而是全局管理端内容区留白偏大、有效展示面积偏小。

关联 BUG：`issues/bugs/archive/BUG-0054-admin-content-padding-too-large/`

## What Changes

- 将管理端 desktop 主内容 padding 从旧值收敛到 `24px 24px 48px` 量级。
- 将 tablet / mobile 主内容 padding 联动收敛到更紧凑的响应式值。
- 移除全局 `.content-inner` 的 `1080px` 硬上限，改为 `100%` 或 `min(1440px, 100%)` 的统一策略。
- 清理 SKU、系统设置等页面与全局内容宽度策略冲突的页面级 max-width。
- 更新已有 OpenSpec 中写死的 1080/1120px 管理端内容宽度要求，避免归档后正式 specs 继续保留冲突条款。
- 增加前端测试或静态断言，覆盖 Shell padding、content-inner max-width 与 divergent override。
- 完成多视口、多页面视觉回归：日志审计、SKU、用户、Dashboard、系统设置。

不修改后端 API、数据库、Orval、MinIO、Docker Compose、店主端或小程序。

## Capabilities

### Modified Capabilities

- `admin-dashboard`: 管理端全局 Shell 内容区 padding 与 content-inner 宽度策略。
- `web-client`: 复用 AdminLayout 的管理端业务页面不再要求 1080/1120px 主内容宽度。
- `user-management`: 用户管理页跟随全局 AdminLayout 内容宽度策略。
- `system-settings`: 系统设置页移除独立 1080px 内容容器锁定。
- `testing`: 增加针对 BUG-0054 的前端布局回归覆盖。

## Rollback Plan

1. 回滚 `admin-home.css` 中 `.main-content` padding 和 `.content-inner` max-width 调整。
2. 回滚 SKU、系统设置等页面级 max-width 清理。
3. 回滚新增或更新的前端测试断言。
4. 不涉及数据库迁移、后端接口、Orval 生成物、MinIO 或 Docker 配置回滚。
5. 若回滚导致 BUG-0054 复现，必须在 BUG trace 中记录原因并重新评审修复路径。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 不涉及 |
| API | 不新增或修改请求、响应、错误码 |
| 数据库 | 不涉及 |
| Web 管理端 | 全局 AdminLayout 主内容区域、日志审计、SKU、用户、Dashboard、系统设置等页面视觉密度 |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | 不需要执行 |
| Docker Compose | 不涉及 |
| 测试 | 更新 `AdminLayout` / 管理端布局相关 Vitest 或静态断言 |
| 文档 | OpenSpec trace、BUG trace 与父需求关联索引同步 |
