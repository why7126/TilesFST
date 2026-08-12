## ADDED Requirements

### Requirement: 性能上报与聚合 API 治理
API 治理 SHALL 记录真实用户性能上报和聚合查询接口的请求、响应、错误码、OpenAPI、Orval、权限和隐私边界。

#### Scenario: 性能上报接口契约
- **WHEN** 后端新增性能事件上报接口
- **THEN** OpenAPI SHALL 描述请求体字段、枚举值、长度限制、数值范围、批量上报限制和错误响应
- **AND** API 文档 SHALL 说明公开端、小程序和管理端上报权限边界
- **AND** Orval SHALL 生成或更新 Web client types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: 性能聚合查询接口契约
- **WHEN** 后端新增管理端性能聚合查询接口
- **THEN** OpenAPI SHALL 描述筛选参数、聚合响应、样本不足标识、分位指标口径和权限错误
- **AND** API 文档 SHALL 说明 P50、P75、P95、P99 或等价分位的计算口径
- **AND** 聚合响应 SHALL 描述 `page`、`page_size`、`total` 和 `total_pages` 后端分页字段
- **AND** 查询接口 SHALL 仅允许管理端授权角色访问。

#### Scenario: 敏感字段错误码
- **WHEN** 性能上报 payload 包含禁止字段或字段校验失败
- **THEN** API SHALL 返回统一错误响应和文档化错误码
- **AND** 错误响应 SHALL NOT 回显 Authorization、Cookie、Token、签名 URL、真实客户数据或原始 payload。
