## ADDED Requirements

### Requirement: 管理端主要列表搜索一致性 gate
系统 MUST 为管理端主要列表提供统一搜索与筛选验收 gate，使品牌、类目、SKU、规格、Banner、证书、用户、日志等列表在关键词入口、筛选区、重置、分页、空态、权限和横切 UI 上保持一致。

#### Scenario: 搜索区和筛选区一致
- **WHEN** 后续 Change 新增或修改管理端主要列表的搜索、筛选或重置能力
- **THEN** 页面 MUST 优先复用 `AdminListPage`、共享筛选卡片、共享搜索输入或等价 shared wrapper
- **AND** 关键词、筛选项、重置按钮、表格和分页顺序 MUST 与现有管理端列表基准一致
- **AND** 若页面不接入共享模板，design MUST 记录等价封装理由和差异边界。

#### Scenario: 查询语义和分页一致
- **WHEN** 用户输入关键词、调整筛选项或点击重置
- **THEN** 页面 MUST 将页码回到第一页
- **AND** 响应 MUST 展示后端真实 total
- **AND** 页面 MUST NOT 使用全量拉取后前端切片的伪分页作为验收结果
- **AND** 空态 MUST 区分暂无数据和当前条件无结果。

#### Scenario: 横切 UI 不回归
- **WHEN** 管理端列表搜索改造完成
- **THEN** 页面 MUST 保持 `page-summary` + `page-right` 分页 DOM、fixed toast、DS confirm、表头 nowrap、长文本截断、sticky 操作列、横向滚动和窄屏可达性
- **AND** Web 管理端 MUST 使用 Design System semantic token
- **AND** 页面 MUST NOT 新增裸 Hex、`window.confirm` 或文档流 notice 推挤布局。

#### Scenario: 权限边界一致
- **WHEN** 管理端用户执行搜索或筛选
- **THEN** 后端 MUST 只返回该用户有权查看的数据
- **AND** 前端 MUST NOT 通过隐藏列、前端过滤或本地缓存暴露未授权数据
- **AND** 非授权用户仍按对应业务 spec 返回 401 或 403。
