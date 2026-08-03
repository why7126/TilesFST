## Context

BUG-0098 指出管理端多个页面的筛选下拉框位置和 UI 样式不统一。现有正式规格中，`design-system` 已定义管理端列表基础组件、`AdminListPage` 页面模板、语义样式和轻量浮层边界；各业务页面规格也已经定义筛选能力，但缺少跨页面筛选下拉的一致性验收基准。

本 Change 只做修复规格与实现计划，不直接写 `src/`。后续 `/opsx-apply` 阶段需要在 Web 管理端代码中定位已有筛选栏、Select / Dropdown 封装和页面级样式。

## Root Cause

- 直接原因：管理端多个页面的筛选下拉未统一采用瓷砖类目页的筛选下拉交互和样式。
- 根本原因：管理端筛选控件缺少统一复用约束或验收基准，页面实现可能分别处理 Select / Dropdown、筛选栏布局和局部样式。
- 分类：`design`
- 严重等级：`medium`

## Design Goals

- 以瓷砖类目页作为筛选下拉交互和视觉基准。
- 统一管理端筛选区内下拉框位置、尺寸、对齐、弹层、状态和重置表现。
- 保持现有筛选语义、请求参数和查询结果不变。
- 使用 Design System semantic token 和 shared/admin UI 组件，避免裸 Hex 或页面级局部样式继续分化。
- 在桌面和窄屏视口下保证下拉层不被表格、页面容器、滚动区或弹窗裁切。

## Proposed Solution

1. 盘点受影响页面筛选区：
   - `/admin/brands`
   - `/admin/tile-categories`
   - `/admin/tile-specs`
   - `/admin/brand-certificates`
   - `/admin/banners`
   - `/admin/users`
   - `/admin/settings`
   - `/admin/logs`
   - `/admin/api-docs`
   - `/design-system` 或界面主题相关入口
2. 识别瓷砖类目页当前筛选下拉的基准行为：
   - 控件高度、宽度策略、图标与文本对齐。
   - 弹层宽度、边界对齐、z-index、阴影和打开方向。
   - normal / hover / selected / disabled / empty / loading 状态。
   - 重置后的占位文案和视觉状态。
3. 将基准沉淀到统一的筛选下拉组件、筛选栏模板或等价 shared/admin UI 封装。
4. 替换或收敛受影响页面的页面级筛选下拉实现。
5. 补充测试：
   - 组件级 DOM / class / 状态测试。
   - 页面级 smoke 覆盖核心页面筛选下拉。
   - Design System 校验覆盖 semantic token 和禁止裸 Hex。

## Non-goals

- 不新增筛选字段。
- 不改变现有 API 请求路径、查询参数、响应结构或错误码。
- 不修改数据库结构、迁移、Pydantic Schema、OpenAPI / Orval 生成物。
- 不重设计管理端整体视觉风格。
- 不改变 Dialog / Modal 外部点击关闭策略；本 Change 只约束筛选区轻量下拉浮层。

## Risks and Mitigations

- 风险：统一样式后某些页面筛选栏宽度不足。
  - 缓解：用响应式约束和稳定宽度策略处理，窄屏下允许换行但不得文本溢出或遮挡操作。
- 风险：下拉弹层被表格或滚动容器裁切。
  - 缓解：复核弹层挂载位置、z-index 与 overflow 边界，增加 smoke 验收。
- 风险：误改筛选语义。
  - 缓解：测试中断言查询参数与重置行为不变，不触碰后端接口。
- 风险：页面级样式继续分化。
  - 缓解：通过 shared/admin UI 组件、semantic token 和 Design System 示例约束后续实现。

## Test Strategy

- 运行前端相关测试，优先覆盖管理端筛选下拉组件、受影响页面筛选交互和 Design System 示例。
- 对至少桌面 1440x1024 与窄屏管理端视口做视觉 smoke，确认下拉弹层不裁切、不遮挡关键操作。
- 若实现未改 API，明确记录无需 Orval；如意外触及 API，必须同步 OpenAPI / Orval / docs / tests。
