## MODIFIED Requirements

### Requirement: 原图、缩略图与展示图三规格图片资源

系统 SHALL 为通用图片上传生成并保存原图、缩略图和展示图资源，并在可观测性事实源中记录关键阶段耗时。

#### Scenario: 通用图片上传成功路径记录六个基础阶段

- **GIVEN** 管理端用户通过通用图片上传入口上传可处理图片
- **WHEN** 后端完成原图保存、thumbnail 派生与 display 派生
- **THEN** 系统 SHALL 在同一次 Task Trace 中记录 `file_read`
- **AND** 系统 SHALL 记录 `original_put_object`
- **AND** 系统 SHALL 记录 `thumbnail_generate`
- **AND** 系统 SHALL 记录 `thumbnail_put_object`
- **AND** 系统 SHALL 记录 `display_generate`
- **AND** 系统 SHALL 记录 `display_put_object`
- **AND** 每个 span SHALL 包含非负 `duration_ms` 或等价耗时字段

#### Scenario: 不适用或失败的派生阶段可追踪

- **GIVEN** 通用图片上传遇到不适用派生图的格式、派生图生成失败或派生对象写入失败
- **WHEN** 系统按既有媒体策略跳过、降级或返回错误
- **THEN** 系统 SHALL 在 Task Trace 中记录对应阶段的 `skipped` 或 `failed` 状态
- **AND** 系统 SHALL 保留已完成阶段 spans
- **AND** 系统 SHALL NOT 静默缺失关键阶段解释
