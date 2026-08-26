## MODIFIED Requirements

### Requirement: 个人资料头像更新

系统 SHALL 支持已认证管理员或员工更新自己的头像，并为头像上传链路记录阶段级 Task Trace spans。

#### Scenario: 头像上传分支记录基础阶段

- **GIVEN** 已认证管理员或员工在个人资料页上传头像
- **WHEN** 后端读取文件并通过对象存储适配层保存头像原图
- **THEN** 系统 SHALL 在同一次 Task Trace 中记录 `file_read`
- **AND** 系统 SHALL 记录 `original_put_object`
- **AND** 每个 span SHALL 包含状态与耗时
- **AND** 系统 SHALL NOT 绕过后端鉴权或让前端直连对象存储

#### Scenario: 头像派生图阶段记录或说明跳过

- **GIVEN** 头像上传链路生成 thumbnail 或 display 派生图
- **WHEN** 派生图生成和写入完成、失败或跳过
- **THEN** 系统 SHALL 记录 `thumbnail_generate`、`thumbnail_put_object`、`display_generate`、`display_put_object` 中适用阶段的 spans
- **AND** 不适用阶段 SHALL 记录 `skipped` 或在实现记录中明确稳定跳过依据
- **AND** 失败阶段 SHALL 保留脱敏错误摘要
