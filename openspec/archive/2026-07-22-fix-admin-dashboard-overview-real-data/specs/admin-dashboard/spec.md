---
created_at: 2026-07-22 08:35:05
updated_at: 2026-07-22 08:35:05
---

# admin-dashboard Specification Delta

## MODIFIED Requirements

### Requirement: 管理端 Dashboard 数据概览

`/admin/dashboard` MUST 展示「数据概览」区块，包含 4 个指标卡：SKU 总数、品牌数量、Banner 数量、用户数量。桌面端 MUST 为四列网格；关键数值 MUST 使用品牌金强调。指标数值 MUST 来自真实后端接口或真实业务聚合结果，MUST NOT 在生产页面成功态中使用 Mock 常量、演示数组或固定 fallback 值。统计口径 MUST 与对应后端查询、业务表或管理端列表页总数保持一致。请求中、空数据、错误和无权限场景 MUST 有明确 UI 状态；接口失败时 MUST NOT 展示 Mock 数据作为成功结果。若新增或修改接口，接口 MUST 使用 `/api/v1` 前缀、统一响应 envelope、管理端鉴权，并同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: 指标卡展示

- **WHEN** 用户访问 `/admin/dashboard`
- **THEN** MUST 展示 4 个指标卡，分别对应 SKU 总数、品牌数量、Banner 数量、用户数量
- **AND** 每个指标卡 MUST 包含标签、数值与辅助说明
- **AND** 指标数值 MUST 来自真实数据源，不得来自生产页面 Mock 常量。

#### Scenario: 指标卡桌面网格

- **WHEN** 视口宽度 >= 1024px
- **THEN** 指标卡 MUST 以四列网格排列
- **AND** 关键数值 MUST 保持品牌金强调样式。

#### Scenario: 真实数据统计口径

- **WHEN** 后端返回 Dashboard 数据概览结果
- **THEN** SKU 总数 MUST 与 SKU 管理列表或后端 SKU 查询总量一致
- **AND** 品牌数量 MUST 与品牌管理列表或后端品牌查询总量一致
- **AND** Banner 数量 MUST 与 Banner 管理列表或后端 Banner 查询总量一致
- **AND** 用户数量 MUST 与用户管理列表或后端用户查询总量一致，并遵守当前账号权限边界。

#### Scenario: 数据变更后刷新

- **WHEN** 测试数据新增、更新或删除影响某个概览指标
- **AND** 用户刷新 Dashboard 或重新触发数据请求
- **THEN** 对应指标 MUST 展示更新后的真实统计结果
- **AND** MUST NOT 保持固定演示值。

#### Scenario: 加载与空状态

- **WHEN** Dashboard 概览接口请求中
- **THEN** 页面 MUST 展示 loading、骨架或等价等待状态
- **WHEN** 真实统计结果为 0
- **THEN** 页面 MUST 展示 0 或明确空状态
- **AND** MUST NOT 使用 Mock 数据填充。

#### Scenario: 错误状态不使用 Mock 兜底

- **WHEN** Dashboard 概览接口返回错误、鉴权失败或网络异常
- **THEN** 页面 MUST 展示错误状态或重试入口
- **AND** MUST NOT 展示 Mock 数据作为成功结果
- **AND** 错误信息 MUST NOT 泄露数据库 DSN、SQL、MinIO 凭据、内部堆栈或密钥。

#### Scenario: API 契约同步

- **WHEN** 修复新增或修改 Dashboard 概览 API
- **THEN** API 路径 MUST 使用 `/api/v1` 前缀
- **AND** 响应 MUST 使用统一 envelope
- **AND** OpenAPI、Orval、`docs/03-api-index.md` 和相关后端/前端测试 MUST 同步更新。
