## ADDED Requirements

### Requirement: SKU 列表分页与表格结构 UI 一致性修复

Web 客户端 MUST 修复 `/admin/tile-skus` 瓷砖 SKU 列表页的分页与表格卡片结构 UI 一致性缺陷：列表底部分页 MUST 与用户管理页分页保持相同的 DOM 结构与视觉语言；表格卡片内 MUST NOT 出现与页面级标题重复的二级标题行（如「SKU 列表」）。修复 MUST NOT 修改 SKU API、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。

#### Scenario: SKU 列表分页对齐用户管理页

- **WHEN** 已登录 `admin` 或 `employee` 分别访问「瓷砖 SKU」与「用户管理」列表页
- **THEN** 两个页面底部分页区域 MUST 使用相同 DOM 结构：`page-summary` + `page-right` + `page-buttons` + `page-size-wrap`
- **AND** 布局、按钮尺寸、边框、圆角、字号、激活态和每页显示控件 MUST 视觉一致

#### Scenario: SKU 分页 MUST NOT 使用废弃 brand 局部结构

- **WHEN** 用户查看 SKU 列表底部分页
- **THEN** MUST NOT 出现 `page-left` 或 `brand-pagination-right` 类名/结构
- **AND** 总数摘要 MUST 独立于翻页按钮组（`page-summary`）

#### Scenario: 表格卡片内无重复标题行

- **WHEN** 用户访问 SKU 列表页
- **THEN** `table-card` 内 MUST NOT 渲染 `table-head`、`table-title`「SKU 列表」或等价卡片内二级标题
- **AND** 表格 MUST 直接以 `<table>` 表头开始（与用户管理页一致）

#### Scenario: SKU 列表分页功能不回退

- **WHEN** 用户在 SKU 列表页切换页码或修改每页条数（10 / 20 / 50 / 100）
- **THEN** 列表 MUST 正确刷新，`total` 与当前筛选结果一致
- **AND** 切换每页条数后 page=1，筛选条件 MUST 保留

#### Scenario: SKU 列表 CRUD 与筛选保持可用

- **WHEN** 用户执行查询、重置、新增 SKU、编辑、上下架或删除
- **THEN** 原有功能 MUST 继续可用
- **AND** MUST NOT 变更 API 请求参数或响应结构
