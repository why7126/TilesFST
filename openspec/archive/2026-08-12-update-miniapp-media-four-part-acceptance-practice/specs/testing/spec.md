## ADDED Requirements

### Requirement: 小程序媒体测试 helper

测试治理能力 SHALL 提供或要求复用小程序媒体测试 helper，用于表达图片展示 URL、preview URL、视频 URL、poster / cover、fallback、lazy-load、页面模板绑定和受控 `/media` URL 语义。该 helper SHALL 服务自动化断言和验收摘要，不得替代对象存储审计、小程序 Network evidence 或端侧 render evidence。

#### Scenario: 图片媒体 URL 语义断言

- **WHEN** 后端接口或小程序页面测试检查图片媒体
- **THEN** helper SHALL 支持断言展示 URL 优先使用缩略图
- **AND** SHALL 支持断言 preview URL 保留原图或等价高清资源
- **AND** SHALL 支持断言 fallback 和 lazy-load 绑定符合预期。

#### Scenario: 视频媒体 URL 语义断言

- **WHEN** 后端接口或小程序页面测试检查视频媒体
- **THEN** helper SHALL 支持断言视频播放 URL 不被缩略图或 poster 替换
- **AND** SHALL 支持断言视频 poster / cover URL 优先使用轻量图片
- **AND** SHALL 支持记录不涉及视频时的 `n/a` 原因。

#### Scenario: 受控媒体 URL 安全断言

- **WHEN** 测试检查媒体 URL 输出
- **THEN** helper SHALL 支持断言客户端使用后端受控 `/media/{object_key}` 或等价 URL
- **AND** SHALL 支持断言输出不直连未授权对象存储
- **AND** SHALL 支持断言测试摘要不暴露 raw object key、密钥、`.env`、Authorization header、Cookie 或本机绝对路径。
