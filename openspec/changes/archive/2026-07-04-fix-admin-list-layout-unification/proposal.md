---
change_id: fix-admin-list-layout-unification
title: 管理端多列表页布局与筛选分页交互统一修复
created_at: 2026-07-03 18:51:13
updated_at: 2026-07-03 18:51:13
source_bug: BUG-0055-admin-list-layout-unification
status: proposed
---

## Why

BUG-0055 已评审通过。Web 管理端多个列表型页面在模块顺序、筛选/搜索交互、表格末列固定浮动和分页页码呈现上不统一，影响管理员跨页面操作的一致性和宽表格场景下操作列可达性。

关联 BUG：`issues/bugs/archive/BUG-0055-admin-list-layout-unification/`

## What Changes

- 统一瓷砖 SKU、瓷砖品牌、瓷砖类目、瓷砖规格、Banner 管理、用户管理、日志审计、接口文档页面的模块顺序：标题模块 → 指标卡模块 → 筛选/搜索模块 → 列表模块。
- 统一筛选/搜索模块交互与视觉，以瓷砖 SKU 页为基线，但移除所有页面的【查询】/【搜索】显式提交按钮。
- 统一重置按钮尺寸、对齐、圆角、字号和图标策略。
- 统一表格最后一列固定浮动，以接口文档页 sticky action column 为基线。
- 统一分页控件，最多展示 5 个可点击页码；总页数为 1 时仍保持统一结构和禁用态。
- 增加前端回归测试，覆盖模块顺序、无查询按钮、固定操作列、最多 5 个页码、筛选/每页条数变更回到第 1 页。

不修改后端 API、数据库、MinIO、媒体上传、Docker Compose、店主端或微信小程序。默认不执行 Orval；若实现阶段选择修改接口分页契约，必须重新评估 API 与 Orval 门禁。

## Capabilities

### Added Capabilities

- `web-client`: 管理端列表页横切一致性要求。
- `testing`: 管理端列表页一致性回归测试要求。

## Rollback Plan

1. 回滚本 Change 对各管理端列表页模块顺序、筛选区、分页组件和 sticky action column 的前端修改。
2. 回滚或保留新增测试时需同步确认测试目标；若回滚产品行为，应同步回滚对应测试断言。
3. 不涉及数据库迁移、后端接口、Orval 生成物、MinIO、Docker 配置或环境变量回滚。
4. 若回滚后 BUG-0055 复现，必须在 BUG trace 中记录回滚原因，并重新评审修复路径。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 不涉及 |
| API | 不新增或修改请求、响应、错误码 |
| 数据库 | 不涉及 |
| Web 管理端 | 多个列表页布局、筛选交互、表格操作列和分页体验 |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | 默认不需要执行 |
| Docker Compose | 不涉及 |
| 测试 | 更新或新增 Vitest / Testing Library 测试 |
| 文档 | OpenSpec trace、BUG trace 同步 |
