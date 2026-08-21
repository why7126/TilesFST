# real-user-performance-monitoring 规格变更

## MODIFIED Requirements

### Requirement: 性能聚合查询
系统 SHALL 支持按端类型、页面、版本、网络、设备和时间范围聚合真实用户性能数据，并 SHALL 为管理端筛选提供受控候选值。

#### Scenario: 聚合基础指标
- **WHEN** 管理端或授权研发查询性能聚合数据
- **THEN** 系统 SHALL 返回样本量、平均耗时、最大耗时、P50、P75、P95、P99 或等价分位指标
- **AND** 聚合结果 SHALL 支持按端类型、页面 key、版本、网络类型、设备类别和时间范围过滤
- **AND** 聚合结果 SHALL 返回 `total`、`page`、`page_size` 和 `total_pages`，支持管理端后端真实分页。

#### Scenario: 慢页面与样本不足
- **WHEN** 聚合结果用于展示慢页面排行、慢指标排行或版本对比
- **THEN** 系统 SHALL 标识样本量
- **AND** 对低于统计阈值的结果 SHALL 标记样本不足
- **AND** 样本不足项 SHALL NOT 被当作可靠趋势结论。

#### Scenario: 管理端访问控制
- **WHEN** 用户访问性能聚合查询、性能候选值查询或管理端性能观测入口
- **THEN** 系统 SHALL 校验管理端权限
- **AND** 未授权用户 SHALL NOT 读取性能事件明细、聚合数据、筛选候选值或内部排障信息。

#### Scenario: 管理端样本明细查询
- **WHEN** 管理员从性能观测页聚合行查看最近样本
- **THEN** 系统 SHALL 仅返回 `page_key`、指标名、耗时、版本、网络、设备、`request_id` 和事件/接收时间等受控字段
- **AND** 系统 SHALL NOT 返回完整 URL、Header、Cookie、签名 URL、raw payload、Authorization、Token 或用户隐私字段
- **AND** 管理端 SHALL 使用独立性能样本页承载样本明细，而非弹窗承载
- **AND** 样本明细 SHALL 支持后端真实分页，并返回 `total`、`page`、`page_size` 和 `total_pages`
- **AND** 管理端样本页 SHALL 复用日志审计页复制样式支持复制 `request_id`
- **AND** 样本明细 SHALL 归属于性能观测能力，而非日志审计查询。

#### Scenario: 管理端筛选候选值查询
- **WHEN** 系统管理员按时间范围请求性能观测筛选候选值
- **THEN** 系统 SHALL 返回端类型、版本号、页面、设备、网络和指标 6 大维度候选值
- **AND** 端类型和指标 SHALL 由后端固定枚举返回 `value` 与 `label`
- **AND** 版本号、页面、设备和网络 SHALL 基于 `performance_events` 在 `start_time`、`end_time` 范围内的非空值返回
- **AND** 候选值 SHALL 仅受时间范围影响，不因端类型、版本号、页面、设备、网络或指标等其他筛选项级联收敛
- **AND** 动态候选值为空时 SHALL 返回空数组，而不是错误。

#### Scenario: 管理端筛选和字段顺序
- **WHEN** 系统管理员访问管理端性能观测页
- **THEN** 筛选区 SHALL 按时间范围 > 端类型 > 版本号 > 页面 > 网络 > 指标的顺序展示
- **AND** 端类型、版本号、页面、网络和指标 SHALL 使用可选择控件，不使用纯文本输入
- **AND** 聚合列表 SHALL 按页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 样本 > P50 > P75 > P95 > P99 > 状态 > 操作的顺序展示
- **AND** 样本页上下文 SHALL 按页面 > 版本号 > 端类型 > 设备 > 网络 > 指标的顺序展示
- **AND** 样本列表 SHALL 按页面 > 版本号 > 端类型 > 设备 > 网络 > 指标 > 耗时 > 事件时间 > 接收时间 > request_id 的顺序展示。
