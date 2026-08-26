## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、详情展示图、媒体观测、对象存储直出和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图、图片类品牌证书缩略图、用户头像和图片 `display` 派生图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异、规格目录或等价稳定规则区分 `thumbnail`、`display` 与 `original`。业务记录保存非空媒体 object key 前 SHOULD 校验对象存在；用户头像等当前身份展示关键媒体写入非空 key 前 MUST 校验对象存在且可受控读取。

系统 SHALL 生成真实轻量缩略图与详情展示图：对于尺寸大于目标尺寸的支持图片，派生图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于对应规格约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。无法达到目标体积时 SHALL NOT 默认阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。

对象存储直出 SHALL 作为受控媒体读取形态之一，仅能由后端媒体服务或对象存储适配层生成。系统 SHALL 明确签名 URL、公开 URL、后端 `/media` 代理 URL 的选择条件、过期策略、缓存策略和 fallback。客户端 SHALL NOT 直连未授权对象存储，响应 SHALL NOT 暴露对象存储密钥、bucket 权限细节或内部 endpoint 白名单。

#### Scenario: 用户头像 key 写入前对象可读

- **GIVEN** 用户资料写入链路接收非空头像 `avatar_object_key`
- **WHEN** 该 key 对应对象不存在、权限异常或无法通过后端对象存储适配层读取
- **THEN** 系统 SHALL 拒绝写入该 key
- **AND** 系统 SHALL 返回统一错误响应
- **AND** 错误响应 SHALL NOT 暴露对象存储 endpoint、bucket、access key、secret key 或底层 SDK 堆栈

#### Scenario: 用户头像受控媒体 URL 可读

- **GIVEN** 用户头像 `avatar_object_key` 已成功保存
- **WHEN** 客户端访问 `/media/{avatar_object_key}` 或等价受控 URL
- **THEN** 后端 SHALL 返回可读图片响应
- **AND** 响应 Content-Type SHALL 与对象内容匹配
- **AND** 客户端 SHALL NOT 直连未授权对象存储

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。涉及历史用户头像 key 数据修复时，模板 SHALL 记录 dry-run、apply 和二次幂等复查摘要。

#### Scenario: 用户头像历史对象修复四联验收

- **WHEN** 团队验收用户头像对象缺失类 BUG
- **THEN** key 维度 SHALL 记录头像 key 前缀、业务字段清理或保留原因
- **AND** object 维度 SHALL 记录对象存在性、MIME、大小或缺失原因
- **AND** URL 维度 SHALL 记录 `/media/{object_key}` 或等价受控 URL 的 HTTP 状态与业务错误码
- **AND** render 维度 SHALL 覆盖个人资料页、侧边栏或用户列表中的头像 fallback 表现
