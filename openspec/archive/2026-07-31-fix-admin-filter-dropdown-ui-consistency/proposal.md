## Why

BUG-0098 已评审通过：管理端多个页面已经提供筛选条件下拉框，但不同页面之间的下拉框位置、展开交互和 UI 样式未与瓷砖类目页保持一致。该问题影响瓷砖品牌页、瓷砖类目页、瓷砖规格页、品牌证书页、Banner 管理页、用户管理页、系统设置页、日志审计页、接口文档页和界面主题页等后台高频筛选体验。

当前缺陷属于管理端既有筛选能力的一致性偏差，不需要新增业务接口或数据模型，但需要通过 OpenSpec Change 明确统一的 Design System 与管理端列表筛选下拉约束，避免继续出现逐页实现和局部样式分化。

## What Changes

- 以瓷砖类目页筛选下拉为交互和视觉基准，统一管理端筛选条件下拉框的位置、尺寸、触发方式、弹层对齐、宽度策略和状态表现。
- 在 Design System 中补充管理端筛选下拉一致性要求，覆盖 Select / Dropdown / Popover 等轻量浮层在筛选区内的使用边界。
- 要求受影响页面复用统一筛选控件、统一筛选栏模板或等价 shared/admin UI 封装，避免页面级裸样式和不一致的局部实现。
- 明确筛选字段、查询参数、接口请求和查询结果语义不变；本 Change 不新增、不删除、不重命名 API 字段。
- 增加回归测试和视觉 smoke 任务，覆盖桌面与窄屏视口、下拉弹层裁切、状态样式、重置行为和 Design System token 约束。

## Rollback Plan

- 若统一筛选控件或样式引入严重页面阻塞，可先回退对应 Web 前端组件与样式变更，保留原有页面筛选能力。
- 回退不得修改后端 API、数据库、OpenAPI / Orval 输出或筛选参数语义。
- 回退后保留 BUG-0098 与本 Change 记录，重新评估受影响页面矩阵并拆分后续修复任务。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `design-system`: 补充管理端筛选下拉框统一交互、样式、弹层、状态和测试治理要求。

## Impact

- Web: 影响管理端筛选栏与筛选下拉组件实现，预计涉及品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档、界面主题等页面。
- Admin: 影响管理端高频筛选体验一致性。
- Miniapp: 不影响。
- Backend / API / Database / Storage: 不影响；不得新增或修改接口、错误码、Pydantic Schema、OpenAPI、Orval、数据库迁移、MinIO 或对象存储策略。
- Tests: 需要补充前端组件测试或页面 smoke，覆盖统一下拉交互、视觉状态、重置行为、弹层不裁切和 Design System token 约束。
