## 任务清单

- [x] 1. 后端性能事件模型与接口
  - [x] 1.1 新增性能事件 Pydantic Schema，校验 `client_type`、`page_key`、`metric_name`、`duration_ms`、`sample_rate`、`occurred_at` 等字段
  - [x] 1.2 新增性能事件上报接口，支持单条或批量上报，并确保非法 payload 返回统一错误响应
  - [x] 1.3 实现敏感字段拒绝或移除策略，覆盖 Authorization、Cookie、Token、签名 URL、手机号、openid、完整请求体和完整响应体
  - [x] 1.4 确保公开端与小程序匿名上报不获得管理端权限，管理端聚合查询保持鉴权
- [x] 2. 数据库存储与聚合
  - [x] 2.1 新增 SQLite 性能事件表、索引和迁移
  - [x] 2.2 新增 MySQL baseline/migration，保持字段类型、索引和字符集兼容
  - [x] 2.3 实现按时间、端类型、页面、版本、网络和设备类别聚合样本量、平均值、最大值、P50/P75/P95/P99 或等价分位
  - [x] 2.4 明确数据保留周期、清理策略或后续治理入口
- [x] 3. Web RUM 采集与管理端观测
  - [x] 3.1 在 Web 管理端和店主展示端受控入口采集页面加载、首屏可用、完整加载、关键接口和关键资源耗时
  - [x] 3.2 实现采样、批量或节流上报，并保证上报失败不阻断主业务
  - [x] 3.3 管理端性能观测入口或查询预留支持筛选、摘要、慢页面排行、趋势、版本对比、空态、错误态和样本不足态
  - [x] 3.4 Web UI 使用 Design System semantic token 和既有管理端组件，不新增裸 Hex
- [x] 4. 微信小程序 RUM 采集
  - [x] 4.1 在 App/page 生命周期或统一工具中记录页面进入、`onLoad`、`onShow`、`onReady`、首个关键接口完成和首屏渲染就绪
  - [x] 4.2 实现小程序端采样、批量或节流上报，并确保失败不影响列表、详情、搜索、首页和品牌页面主流程
  - [x] 4.3 补充小程序真实环境或体验版 Network evidence 记录入口，无法自动化时标记人工验证来源
- [x] 5. API、文档与生成物同步
  - [x] 5.1 更新 OpenAPI schema、请求/响应示例和错误码说明
  - [x] 5.2 运行 Orval 生成 Web API client，确认 generated 文件不手工编辑
  - [x] 5.3 更新 `docs/03-api-index.md`、`docs/04-database-design.md` 和必要部署/环境说明
- [x] 6. 测试与验收
  - [x] 6.1 补充后端 pytest，覆盖上报、聚合、权限、敏感字段和数据库兼容
  - [x] 6.2 补充 Web Vitest/Testing Library 或等价测试，覆盖采集、降级和管理端页面关键状态
  - [x] 6.3 补充小程序静态测试或等价验证，覆盖埋点调用、隐私字段和上报失败降级
  - [x] 6.4 运行 OpenSpec、语言、目录结构、API/DB/前后端相关测试，并在 trace 记录结果

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-11 08:45:36 | 性能观测页标题与其他管理页不一致；重置按钮长度/布局不一致；安全边界长文案不应常驻展示；需要解释页面指标如何解读。 | 页面 H1 统一为“性能观测”并使用 `page-title`；重置按钮移入 `log-audit-filter-actions`；安全边界与“页面如何解读”改为 hover/focus tooltip。 | `PerformanceRumPage.test.tsx`、`AdminLayout.test.tsx` 聚焦测试通过；1440px Playwright smoke 记录 title、button、tooltip computed style 与截图。 |
| 2026-08-11 08:54:34 | 重置按钮不需要图标。 | 移除性能观测页重置按钮内的 `RotateCcw` 图标，仅保留文字按钮。 | `PerformanceRumPage.test.tsx` 覆盖重置按钮不包含 `svg`；重新记录 1440px Playwright smoke。 |
| 2026-08-11 09:18:36 | 性能观测页当前列表是聚合数据，需要明确每次加载明细在哪里查看。 | 新增管理端性能样本明细接口与页面内“查看样本”面板，样本只展示受控字段；明确 RUM 单次明细不放到日志审计。 | 后端样本接口测试、`PerformanceRumPage.test.tsx` 样本明细测试、OpenAPI/Orval、1440px Playwright smoke、OpenSpec 校验。 |
| 2026-08-11 09:22:36 | 样本明细放在聚合表下方不合理，确认承载方式改为弹窗。 | 移除页面下方常驻样本明细区；点击“查看样本”打开独立弹窗，弹窗内展示加载、空态、错误态和安全样本表。 | `PerformanceRumPage.test.tsx`、`pnpm --dir src/web build`、1440px Playwright smoke、OpenSpec 校验。 |
| 2026-08-11 09:43:36 | 弹窗样式不可读，确认改为 760-880px 宽的居中紧凑样本列表。 | 弹窗宽度调整为 840px 居中；提升弹窗遮罩层级高于筛选区；移除宽表格，改为摘要标签与样本卡片字段列表；使用稳定背景层级提高可读性。 | `PerformanceRumPage.test.tsx`、`pnpm --dir src/web build`、1440px Playwright smoke、OpenSpec 校验。 |
| 2026-08-11 10:05:36 | 性能观测页表格与样本弹窗继续返修：页面列拆出版本号、操作列右侧冻结并改名、聚合列表新增后端真实分页、弹窗样式对齐其他管理页、Web RUM 版本号取左上角版本号并补 `request_id` 上报。 | Summary API 增加 `page/page_size/total/total_pages` 并按 P95 聚合维度分页；页面列拆为“页面/版本号”，右侧冻结列改为“操作”；新增管理端分页控件；样本弹窗字段使用“版本号”；Web RUM 使用产品版本常量并生成 `rum-*` request_id。 | `UV_CACHE_DIR=.uv-cache uv run pytest src/backend/tests/test_performance_events.py`、`pnpm --dir src/web test src/pages/admin/PerformanceRumPage.test.tsx src/features/performance/rum.test.ts`、`./scripts/generate-openapi-client.sh`、`pnpm --dir src/web build` 通过；当前环境未安装 Playwright 包，自动 1440px 截图未生成。 |
| 2026-08-11 10:29:36 | 性能观测筛选模块缺少筛选项 Label，需与其他管理页样式一致；删除“数据边界”和“页面如何解读”两块信息。 | 为时间范围、端类型、指标三个筛选项补充 `field-label`；保留既有 `log-audit-filter-grid` 和重置按钮布局；移除筛选区帮助块、`FieldHelp` 与 `Info` 图标依赖。 | `pnpm --dir src/web test src/pages/admin/PerformanceRumPage.test.tsx` 通过；测试覆盖筛选 Label 存在且两块帮助信息不展示。 |
| 2026-08-11 13:53:36 | 查看样本使用弹窗不合适，确认直接废除弹窗，改为独立页面。 | 聚合页“查看样本”改为跳转 `/admin/performance/samples`；新增性能样本独立页，使用管理端列表样式展示筛选上下文和样本列表；移除样本弹窗状态、加载逻辑和弹窗专用样式。 | `pnpm --dir src/web test src/pages/admin/PerformanceRumPage.test.tsx src/pages/admin/PerformanceSamplesPage.test.tsx`、`pnpm --dir src/web build` 通过。 |
| 2026-08-11 18:56:35 | 管理后台性能观测页分页样式与其他页面不一致；性能样本页缺少分页且列表样式不一致；移除样本页说明文案；`request_id` 支持复制并复用日志审计复制样式。 | 聚合页分页控件 DOM、类名、文案和选项对齐日志审计页；样本接口和样本页新增 `page/page_size/total/total_pages` 后端真实分页；样本页移除说明文案；`request_id` 使用 `request-id-cell` 与 `request-copy-action` 复制按钮。 | `UV_CACHE_DIR=.uv-cache uv run pytest src/backend/tests/test_performance_events.py`、`pnpm --dir src/web test src/pages/admin/PerformanceRumPage.test.tsx src/pages/admin/PerformanceSamplesPage.test.tsx`、`./scripts/generate-openapi-client.sh`、`pnpm --dir src/web build` 通过。 |
| 2026-08-11 22:11:27 | 网络显示为未知，需要确认是否无法获取；确认小程序 RUM 补充 `wx.getNetworkType` 网络类型采集，Web 端保留不支持时展示未知并补充说明。 | 小程序 RUM 上报统一通过 `wx.getNetworkType` 获取并缓存网络类型，页面生命周期与 API 耗时埋点不再硬编码 `unknown`；Web 性能观测页补充浏览器不支持网络类型时显示未知的说明。 | `UV_CACHE_DIR=.uv-cache uv run pytest tests/test_miniapp_static.py -k performance_rum`、`pnpm --dir src/web test src/pages/admin/PerformanceRumPage.test.tsx`、`pnpm --dir src/web build` 通过。 |
