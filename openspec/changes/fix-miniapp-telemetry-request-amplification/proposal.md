## 背景

BUG-0143 发现微信小程序冷启动进入首页时产生约 28 条 `/api/v1/performance-events` 请求和 25 条 `/api/v1/usage-events` 请求。根因已确认为小程序 `track()` 复用统一 `request()` 上报 usage events，而统一请求层会对每个 API 请求自动生成 RUM `api_duration` 或 `api_failed_duration`，导致遥测请求自身被再次记录为性能事件；同时商品卡曝光在组件属性 observer 中逐条触发，首页新品、热销和瀑布流首屏卡片数量会线性放大 usage 请求。

## 变更内容

- 小程序统一请求封装需要支持区分业务请求与遥测请求，`/api/v1/usage-events` 和 `/api/v1/performance-events` 等遥测上报不得继续派生 API 性能事件。
- 小程序首页商品卡曝光需要具备同一页面、同一模块、同一 SKU 的幂等去重、队列批量或等价压力控制策略，避免请求数量与 observer 触发次数一比一增长。
- 保留首页业务 API 的 RUM 观测能力，`/api/v1/miniapp/home`、`/api/v1/miniapp/products` 和 `app_launch_ready` 不因修复退化。
- 行为事件仍需满足后端 usage event 字典与隐私校验，埋点失败不得阻断首页加载、商品展示、点击、分享或搜索。
- 本 Change 不新增管理端报表、不引入第三方埋点平台、不改变业务数据模型；若实现选择后端批量 usage API，必须同步 OpenAPI、Orval、API 文档和测试。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `real-user-performance-monitoring`：补充小程序遥测请求不触发 RUM 的边界，明确业务请求性能观测不退化。
- `product-usage-logging`：补充小程序 usage 事件上报压力控制、商品卡曝光去重或批量约束，以及事件字典和隐私边界。

## 影响

- 小程序：影响 `src/miniapp/services/api.ts`、`src/miniapp/services/performance.ts`、`src/miniapp/components/product-card/` 和首页相关埋点调用。
- 后端 API：默认可通过端侧队列合并到既有单事件接口完成；如实现新增批量 usage 接收接口，则影响 OpenAPI、Orval、API 文档和后端测试。
- 数据库：默认不涉及；如新增后端批量接口，仍复用既有 usage events 存储模型。
- Web / 管理端 / 对象存储 / Docker Compose：不涉及功能变更。

## 回滚计划

- 若小程序端遥测过滤导致业务 API RUM 缺失，回滚请求封装中的遥测跳过条件，保留商品曝光去重以减少 usage 请求。
- 若批量或队列策略导致事件丢失，可临时切回单条 usage 上报，同时保留 `/api/v1/usage-events` 不触发 RUM 的边界。
- 回滚后必须重新冷启动首页统计 usage-events 与 performance-events 请求数量，并确认主流程不被埋点错误阻断。
