## ADDED Requirements

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。

#### Scenario: 记录原 BUG 场景

- **WHEN** 团队使用四联模板验收媒体类 BUG
- **THEN** 验收记录 SHALL 包含 BUG 编号、标题、严重等级、影响范围、复现入口、受影响端和环境
- **AND** 验收记录 SHALL 包含修复前实际结果和修复后期望结果
- **AND** 涉及特定媒体资源时 SHALL 记录媒体类型、业务资源或等价脱敏标识。

#### Scenario: key 维度验收

- **WHEN** 团队验收媒体类 BUG 的 key 维度
- **THEN** 验收记录 SHALL 确认业务记录中的媒体 key 稳定、可追溯，并符合单 Bucket 标准前缀策略
- **AND** 验收记录 SHALL 禁止用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径作为对象存储 key
- **AND** 若修复涉及历史 key 兼容或迁移，验收记录 SHALL 包含旧 key、新 key 和兼容结果。

#### Scenario: object 维度验收

- **WHEN** 团队验收媒体类 BUG 的 object 维度
- **THEN** 验收记录 SHALL 确认对象存储中真实 object 存在，并与业务记录 key 对应
- **AND** 验收记录 SHALL 覆盖 MIME Type、文件大小、扩展名、权限边界和对象可读性
- **AND** object 验收失败时 SHALL 记录对象不存在、大小为 0、类型不匹配、权限错误或存储环境不可用等失败原因。

#### Scenario: URL 维度验收

- **WHEN** 团队验收媒体类 BUG 的 URL 维度
- **THEN** 验收记录 SHALL 区分相对 URL、公开 URL、签名 URL、代理 URL 或静态资源 URL
- **AND** 验收记录 SHALL 记录页面或接口入口、HTTP 状态、业务错误码和用户可见表现
- **AND** 客户端 SHALL 继续使用后端鉴权、代理或签名 URL 策略读取媒体，SHALL NOT 直连未授权对象存储。

#### Scenario: render 维度验收

- **WHEN** 团队验收媒体类 BUG 的 render 维度
- **THEN** 验收记录 SHALL 覆盖受影响端的媒体展示、占位、失败态和用户可见行为
- **AND** Web 管理端 SHOULD 覆盖上传后预览、列表缩略展示、详情或编辑弹窗展示
- **AND** 店主 Web SHOULD 覆盖公开页面、商品卡片、详情页或媒体预览入口
- **AND** 微信小程序 SHALL 覆盖合法域名、图片/视频组件限制、DevTools/真机/体验版 evidence 或明确的不可用原因
- **AND** 小程序端 SHALL NOT 依赖 Web 浏览器专属 API。

#### Scenario: 不适用、失败和阻塞处理

- **WHEN** 某端、某维度或某 evidence 对当前媒体 BUG 不适用
- **THEN** 验收记录 SHALL 标记 `n/a` 并说明不适用原因和影响判断
- **WHEN** 某维度验收失败
- **THEN** 验收记录 SHALL 标记 `fail`，并包含实际结果、期望结果、复现步骤、影响范围和排查线索
- **WHEN** 验收被环境、数据、域名、MinIO 或小程序体验版阻塞
- **THEN** 验收记录 SHALL 标记 `blocked`，并记录阻塞原因、缺失资源、负责人或下一步补证方式。

#### Scenario: 媒体上传链路横切验收

- **WHEN** 媒体类 BUG 涉及上传、编辑、列表回显、历史对象、缩略图、回填或审计脚本
- **THEN** 四联模板 SHALL 要求记录上传状态机 `idle -> uploading -> done/failed` 或等价状态证据
- **AND** 涉及 Web 管理端上传/编辑/列表刷新时 SHALL 记录同会话即时回显 evidence
- **AND** 涉及上传大小、Nginx 或 Docker Web 边界时 SHALL 通过 `http://localhost:3000` 或等价 Web 入口验证边界文件，或记录 `N/A` 原因
- **AND** 涉及历史对象、缩略图、回填或审计脚本时 SHALL 记录 dry-run/apply/统计摘要，且输出 SHALL NOT 泄露敏感信息。
