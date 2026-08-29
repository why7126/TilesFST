## MODIFIED Requirements

### Requirement: 任务链路追踪

系统 SHALL 为可观测任务记录可关联的 Task Trace，包含任务类型、阶段 spans、状态、开始时间、结束时间或耗时、请求关联标识、失败摘要，并支持按任务或请求上下文查询。

#### Scenario: 上传阶段耗时写入 Task Trace spans

- **GIVEN** 管理端头像上传或通用图片上传请求已通过鉴权并进入后端上传处理
- **WHEN** 系统执行文件读取、对象存储写入或图片派生阶段
- **THEN** 系统 SHALL 将阶段耗时写入 Task Trace spans
- **AND** 每个 span SHALL 包含稳定阶段名、状态、开始时间、结束时间或耗时
- **AND** 失败 span SHALL 包含脱敏错误摘要
- **AND** 系统 SHALL NOT 仅依赖普通日志作为阶段耗时事实源

#### Scenario: 上传失败保留已完成阶段 spans

- **GIVEN** 上传请求已经完成一个或多个阶段
- **WHEN** 后续阶段发生对象存储写入失败、派生图生成失败或业务降级
- **THEN** 系统 SHALL 保留失败前已经完成的 spans
- **AND** 系统 SHALL 为失败阶段记录 `failed` 或等价失败状态
- **AND** 系统 SHALL 记录后续未执行阶段的 `skipped` 状态或提供可解释的缺省语义
- **AND** 错误摘要 SHALL NOT 包含密钥、Authorization header、Cookie、本机绝对路径或完整堆栈
