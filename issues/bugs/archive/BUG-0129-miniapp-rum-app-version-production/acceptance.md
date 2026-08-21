---
bug_id: BUG-0129-miniapp-rum-app-version-production
acceptance_status: passed
created_at: 2026-08-12 14:19:46
updated_at: 2026-08-12 22:03:11
---

# 验收标准

## AC-001 统一小程序与 Web 产品版本号

- Given 小程序触发 RUM 上报
- When 管理后台性能观测页展示小程序聚合和样本数据
- Then `app_version` 不得显示 `production`、`development`、`dev` 等运行环境名
- And 小程序与 Web 管理后台使用统一产品版本号来源或等价同步机制

## AC-002 小程序 RUM request_id 可追踪

- Given 小程序触发启动、接口成功或接口失败性能上报
- When 后端保存性能事件
- Then 每条新小程序 RUM 样本应包含非空 `request_id`
- And 管理后台样本页应展示该 `request_id`
- And 有 `request_id` 时复制按钮可用

## AC-003 小程序指标名可读

- Given 管理后台性能观测页展示小程序 RUM 数据
- When 指标为 `app_launch_ready`、`api_duration` 或 `api_failed_duration`
- Then 聚合页、筛选下拉和样本页均显示中文可读名称
- And 未知指标仍可安全回退展示原始值

建议映射：

| 指标 | 显示名称 |
|---|---|
| `app_launch_ready` | 小程序启动就绪 |
| `api_duration` | 接口请求耗时 |
| `api_failed_duration` | 接口失败耗时 |

## AC-004 聚合列表展示完整分组键

- Given 后端按 `client_type + page_key + metric_name + app_version + network_type + device_class` 聚合
- When 管理后台性能观测页展示聚合列表
- Then 表格必须展示网络和设备维度
- And 用户能区分看似重复的页面、版本、端类型和指标记录
- And “查看样本”跳转必须带上 `network_type` 和 `device_class` 上下文
- And 样本页上下文区域必须展示网络和设备

## AC-005 空态样式符合管理端列表体验

- Given 性能观测聚合列表无匹配数据
- When 页面展示“暂无性能样本”
- Then 空态字号、颜色、居中方式和高度应符合管理端表格内空态样式
- And 不得出现过大的标题式文字或破坏表格卡片层级

## AC-006 回归 Web RUM

- Given Web 管理后台和店主 Web 继续上报 RUM
- When 查看性能观测聚合页和样本页
- Then 既有 `PRODUCT_VERSION`、Web 指标中文名、Web `request_id` 生成策略保持不变
- And 新增小程序映射不破坏 Web 筛选和样本跳转

## AC-007 安全与隐私边界

- Given 性能观测 API 返回聚合和样本数据
- Then 不得返回完整 URL、Header、Cookie、Authorization、签名 URL、raw payload、用户隐私或内部鉴权字段
- And 新增 `request_id`、网络、设备展示不得暴露敏感信息

## AC-008 测试覆盖

- 后端或前端测试覆盖小程序 RUM `request_id` 非空上报。
- 前端测试覆盖小程序指标中文映射。
- 前端测试覆盖聚合列表展示网络、设备分组维度。
- 前端测试覆盖空态样式或空态 class。
- 回归测试覆盖 Web RUM 现有行为不退化。

## AC-009 开发环境 RUM baseUrl 与 fallback

- Given 根目录 `.env` 配置了 `HOST_PORT_BACKEND`
- When 执行小程序环境生成脚本生成 dev `env.ts/env.js`
- Then 小程序 dev `apiBaseUrl` 与 `apiFallbackBaseUrls` 应按 `HOST_PORT_BACKEND` 渲染
- And 脚本不得硬编码固定 `8010` 作为开发环境 API 地址
- And 小程序 RUM 上报应复用同一 baseUrl 与 fallback 队列
- And fallback 成功后，后续性能事件应优先使用已成功的 baseUrl，避免每条都先产生一次连接失败

# 验收结果回填

| 时间 | 结论 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-12 21:36:48 | passed | `fix-miniapp-rum-performance-observability` 归档验证 | OpenSpec Change 已实现、验收返修并归档闭环 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 22:03:11
accepted_by: workflow-sync
source_change: fix-miniapp-rum-performance-observability
source_sprint: sprint-023
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

