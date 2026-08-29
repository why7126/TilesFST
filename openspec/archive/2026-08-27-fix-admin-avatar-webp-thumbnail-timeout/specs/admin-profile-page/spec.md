## MODIFIED Requirements

### Requirement: 个人资料头像 self-upload

已认证 `admin` 或 `employee` MUST 可通过授权上传接口上传本人头像（JPG/PNG/WebP，≤2MB），写入 MinIO 或 S3 兼容对象存储，并更新 `avatar_object_key`。上传失败 MUST 保留旧头像并展示错误。上传成功后用于 profile 更新的 `object_key` MUST 能通过后端受控 `/media/{object_key}` 或等价 URL 读取。头像上传链路 MUST 避免 WebP thumbnail 生成长尾阻塞接口到 30 秒级，并 MUST 通过阶段级 Task Trace spans 保留慢点归属。

#### Scenario: 运营人员上传头像

- **WHEN** `employee` 在个人资料页选择合法头像文件
- **THEN** 系统 MUST 允许 upload 并成功 PATCH profile
- **AND** MUST 写入 `avatar_update` audit

#### Scenario: 上传头像后对象与 URL 可读

- **GIVEN** 用户通过个人资料页上传合法头像且上传接口返回 `object_key`
- **WHEN** 用户使用该 `object_key` 保存个人资料
- **THEN** profile 更新 MUST 成功
- **AND** `/media/{object_key}` 或等价受控 URL MUST 返回可读图片
- **AND** `GET /api/v1/profile/me` 返回的 `avatar_url` MUST 与受控媒体读取策略一致

#### Scenario: WebP 头像 thumbnail 生成不造成 30 秒级等待

- **GIVEN** 已认证 `admin` 或 `employee` 上传 127KB 级合法 WebP 头像
- **WHEN** 后端同步处理原图写入和适用的 thumbnail / display 派生图
- **THEN** 上传接口 MUST NOT 因 `thumbnail_generate` 阶段阻塞到 30 秒级等待
- **AND** Task Trace MUST 记录 `thumbnail_generate` 阶段耗时与状态
- **AND** `original_put_object`、`thumbnail_put_object` 或等价对象写入阶段 MUST 与派生图生成阶段分开记录
- **AND** 验收 MUST 使用同一样本或等价 WebP 样本记录接口总耗时、阶段耗时和 request/task trace id 摘要

#### Scenario: 头像派生图生成失败或降级可解释

- **GIVEN** 头像 thumbnail 或 display 生成失败、超时保护触发或按策略跳过
- **WHEN** 上传接口返回成功或失败
- **THEN** 系统 MUST 保留已完成阶段 spans
- **AND** 失败或跳过阶段 MUST 有脱敏错误摘要、状态或稳定跳过依据
- **AND** 上传响应 MUST NOT 返回不存在或不可读的 thumbnail / display key
- **AND** 上传失败时 MUST 保留旧头像并向管理端展示可理解失败态
