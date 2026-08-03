## 1. Scope and Baseline

- [x] 1.1 盘点 BUG-0098 覆盖页面的筛选下拉实现：品牌、类目、规格、品牌证书、Banner、用户、系统设置、日志审计、接口文档、界面主题。
- [x] 1.2 记录瓷砖类目页筛选下拉的基准：控件尺寸、位置、弹层对齐、选项状态、重置表现和窄屏行为。
- [x] 1.3 确认本修复不新增、不删除、不改名任何筛选 API 字段或查询语义。

## 2. Implementation

- [x] 2.1 收敛或新增统一管理端筛选下拉组件 / 筛选栏模板 / shared admin UI 封装。
- [x] 2.2 将受影响页面筛选条件下拉统一到基准交互和样式。
- [x] 2.3 使用 Design System semantic token、CSS variables、`cn()` 和既有 admin classes，移除或避免页面级裸 Hex 与一次性样式分化。
- [x] 2.4 处理下拉弹层挂载、z-index、overflow 和窄屏换行，确保不被表格、页面容器、滚动区或弹窗裁切。

## 3. Tests

- [x] 3.1 补充或更新前端组件测试，覆盖下拉 normal / hover / selected / disabled / empty / loading 状态。
- [x] 3.2 补充或更新页面测试，覆盖筛选选择、清空、重置、查询参数不变和分页重置行为。
- [x] 3.3 运行 Design System 校验，确认未新增裸 Hex、任意 Tailwind color 或未授权原生控件。
- [x] 3.4 进行桌面与窄屏视觉 smoke，确认下拉弹层不裁切、不遮挡、不引起布局抖动。

## 4. Documentation and Trace

- [x] 4.1 在实现记录中说明不影响 API、数据库、Orval、小程序、Docker 和对象存储。
- [x] 4.2 根据实现结果更新必要的 Web / Design System 文档或明确不适用原因。
- [x] 4.3 复核 BUG-0098 acceptance.md 的 AC-001 至 AC-007。
- [x] 4.4 若修复经验具备复用价值，评估是否沉淀到 `docs/knowledge-base/incidents/`；不适用时在验收记录说明。

## 验收返修记录

- [x] 2026-07-31 `/opsx-modify`：验收反馈要求“应用到瓷砖品牌页”。已新增共享 `AdminFilterSelect` 并将 `/admin/brands` 状态筛选从原生 `<select>` 调整为统一 `admin-filter-dropdown` 交互，保留原 `status` 查询参数与重置语义，并补充共享组件与品牌页页面测试。
- [x] 2026-07-31 `/opsx-modify`：验收反馈要求“应用到瓷砖类目页”。已将 `/admin/tile-categories` 状态与层级筛选从原生 `<select>` 调整为共享 `AdminFilterSelect`，保留原 `status`、`level` 查询参数与重置语义，并补充类目页页面测试。
- [x] 2026-07-31 `/opsx-modify`：验收反馈要求“应用到瓷砖规格页、品牌证书页、Banner 管理页”。已将 `/admin/tile-specs` 状态筛选、`/admin/brand-certificates` 所属品牌 / 证书类型 / 有效状态 / 展示状态筛选、`/admin/banners` 展示端 / 状态 / 时间状态筛选调整为共享 `AdminFilterSelect`，保留原查询参数与重置语义，并补充三页页面测试。
- [x] 2026-07-31 `/opsx-modify`：验收反馈要求“应用到用户管理页、系统设置页、日志审计页、接口文档页、界面主题”。已将 `/admin/users` 角色 / 状态 / 登录情况筛选、`/admin/logs` 日志类型 / 时间范围 / 状态结果筛选、`/admin/api-docs` METHOD / TAG / AUTH 筛选、`/admin/settings` 基础与媒体配置下拉、界面主题切换器调整为共享 `AdminFilterSelect` 交互，保留原筛选参数、配置保存类型和主题偏好语义，并补充相关页面与主题测试。
