---
requirement_id: REQ-0107-real-user-page-load-rum
acceptance_status: passed
created_at: 2026-08-10 22:56:55
updated_at: 2026-08-12 00:15:15
---

# 验收清单

## 功能 AC

- [ ] AC-001 Web 端能采集页面导航、首屏可用、完整加载、关键接口和关键资源等受控性能指标，并能区分 `web_admin` 与 `web_catalog`。
- [ ] AC-002 微信小程序能采集页面进入、生命周期节点、首个关键接口完成、首屏渲染就绪和页面可交互等指标，且不依赖 Web 浏览器专属 API。
- [ ] AC-003 性能事件模型包含 `client_type`、`page_key`、`app_version`、`network_type`、`device_class`、`metric_name`、`duration_ms`、`sample_rate`、`occurred_at` 和服务端接收时间。
- [ ] AC-004 后端性能上报接口使用 Schema 校验字段、枚举、长度和数值范围，对非法 payload 返回统一错误响应与错误码。
- [ ] AC-005 端侧上报失败、超时、被限流或采样关闭时，不影响页面加载、搜索、列表、详情、上传或管理操作主流程。
- [ ] AC-006 性能数据不包含手机号、openid、Authorization、Cookie、Token、签名 URL、完整请求体、完整响应体或真实客户数据。
- [ ] AC-007 后端可按端类型、页面、版本、时间范围、网络类型和设备类别聚合样本量、平均耗时、最大耗时、P50、P75、P95、P99。
- [ ] AC-008 聚合查询能输出慢页面排行、慢指标排行和版本对比所需数据，并对样本不足的统计项给出明确标识。
- [ ] AC-009 管理端性能观测入口若纳入首期，必须具备权限控制、筛选、摘要指标、慢页面排行、趋势或版本对比、空态和错误态。
- [ ] AC-010 管理端性能观测入口若不纳入首期，后端聚合接口和数据结构仍需能支撑后续看板，不得只写入不可查询日志。
- [ ] AC-011 SQLite demo 与生产 MySQL 均具备可运行的数据结构、索引或查询策略，避免长期事件数据无限增长拖慢业务查询。
- [ ] AC-012 API 变更同步 OpenAPI、Orval、`docs/03-api-index.md`、接口错误码说明和前后端测试。
- [ ] AC-013 数据库变更同步 SQLite schema、MySQL schema、迁移脚本、`docs/04-database-design.md` 和相关测试。
- [ ] AC-014 小程序发布前必须保留真实环境或体验版网络证据入口；无法自动化通过时标记人工验证来源。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: add-real-user-page-load-rum
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 验收返修记录

| 时间 | 反馈 | 处理 | 证据 |
|---|---|---|---|
| 2026-08-11 08:45:36 | 性能观测页标题与其他页面不一致；重置按钮长度不一致；安全边界长文案不常驻展示；页面解读需通过 tooltip 提供。 | 标题统一为“性能观测”；重置按钮复用管理端筛选 actions 容器；安全边界与页面解读说明改为 hover/focus tooltip。 | `PerformanceRumPage.test.tsx`、`AdminLayout.test.tsx` 聚焦测试通过；1440px Playwright smoke 截图和 computed style 已记录在 Change trace。 |
| 2026-08-11 08:54:34 | 重置按钮不需要图标。 | 移除性能观测页重置按钮图标，仅保留文字。 | `PerformanceRumPage.test.tsx` 补充断言重置按钮不包含 `svg`；视觉 smoke 重新取证。 |
| 2026-08-11 09:18:36 | 性能观测列表是聚合数据，需明确每次加载样本明细在哪里查看。 | 在性能观测页内新增聚合行“查看样本”和样本明细面板；新增管理端样本接口，仅返回受控字段；明确不进入日志审计查看。 | 后端样本接口、前端样本面板、OpenAPI/Orval 和 1440px Playwright smoke 证据记录在 Change trace。 |
| 2026-08-11 09:22:36 | 样本明细放在聚合表下方不合理，确认承载方式改为弹窗。 | 移除页面下方常驻样本区；点击聚合行“查看样本”打开样本明细弹窗。 | `PerformanceRumPage.test.tsx` 覆盖弹窗打开、关闭和安全字段不展示；1440px Playwright smoke 重新取证。 |
| 2026-08-11 09:43:36 | 弹窗样式不可读，确认改为紧凑样本列表。 | 弹窗改为 840px 居中紧凑列表，提升遮罩层级，移除宽表格并增强内容背景层级。 | `PerformanceRumPage.test.tsx` 覆盖紧凑样本弹窗；1440px Playwright smoke 重新取证。 |
| 2026-08-11 10:05:36 | 性能观测页页面列太宽且混有版本信息；明细列需改为右侧冻结操作列；聚合列表需后端真实分页；弹窗 UI 对齐其他管理页；弹窗“版本”改为“版本号”；Web RUM 版本号应取左上角产品版本并补齐 `request_id`。 | 页面列拆为“页面/版本号”，页面 key 收窄并省略溢出；右侧冻结列改名“操作”；summary API 增加 `page/page_size/total/total_pages` 并由页面分页控件调用；样本弹窗字段统一“版本号”；Web RUM 使用产品版本常量并生成 `rum-*` request_id。 | 后端性能事件测试、前端性能页/RUM 测试、OpenAPI/Orval 生成、Web build 通过；当前环境缺少 Playwright 包，最新 1440px 自动截图未生成。 |
| 2026-08-11 10:29:36 | 性能观测筛选模块缺少 Label，样式需保持与其他管理页一致；删除“数据边界”和“页面如何解读”两块信息。 | 为时间范围、端类型、指标补充显式 `field-label`；删除筛选区帮助块、tooltip 组件和 Info 图标依赖。 | `PerformanceRumPage.test.tsx` 聚焦测试通过，覆盖 Label 存在和两块帮助信息不展示。 |
| 2026-08-11 13:53:36 | 查看样本使用弹窗不合适，确认直接废除弹窗，改为独立页面。 | 聚合页“查看样本”改为跳转 `/admin/performance/samples`；新增性能样本独立页，使用管理端列表样式承载筛选上下文和样本列表；移除样本弹窗代码和样式。 | `PerformanceRumPage.test.tsx`、`PerformanceSamplesPage.test.tsx` 聚焦测试通过；Web build 通过。 |
| 2026-08-11 18:56:35 | 性能观测页分页样式与其他页面不一致；性能样本页缺少分页且列表样式不一致；样本页说明文案多余；`request_id` 需要支持复制。 | 聚合页分页控件对齐日志审计页；样本接口和样本页新增后端真实分页；移除样本页说明文案；`request_id` 使用日志审计同款复制按钮与复制反馈。 | 后端性能事件测试、前端性能页/样本页测试、OpenAPI/Orval 生成、Web build 通过。 |
| 2026-08-11 22:11:27 | 网络显示为未知，需要确认是否无法获取；补充小程序网络类型采集，并说明 Web 浏览器不支持时仍显示未知。 | 小程序 RUM 使用 `wx.getNetworkType` 获取并缓存网络类型，页面生命周期和 API 耗时埋点共享；Web 性能观测页补充“不支持网络类型采集时显示未知”的说明。 | 小程序 RUM 静态测试、性能观测页测试、Web build 通过。 |

## 横切 AC（knowledge-base）

无横切 AC：本需求不命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 四类 best-practices 标签。管理端性能观测入口属于指标仪表与趋势分析场景，后续若实现为 CRUD 列表、表单、弹窗或媒体上传链路，应在对应 Change design 中补读并转化相关 best-practices。
