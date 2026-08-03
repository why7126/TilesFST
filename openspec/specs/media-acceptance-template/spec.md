# media-acceptance-template Specification

## Purpose
定义媒体五联验收模板，统一后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布检查对 key、object、URL、thumbnail benefit 与 miniapp render 的证据记录、失败处理、横切上传 gate 和引用方式。

## Requirements
### Requirement: 媒体五联验收模板

系统 MUST 提供一套可复用的媒体五联验收模板，用于后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布前检查统一记录 `key`、`object`、`URL`、`thumbnail benefit` 与 `miniapp render` 五个维度的状态、证据、N/A 理由、blocked 原因和失败处理线索。模板 MUST 不记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。

#### Scenario: 模板包含五联维度

- **WHEN** 团队为媒体相关需求、缺陷、变更、Sprint 或 Release 引用媒体五联验收模板
- **THEN** 模板 MUST 包含 `key`、`object`、`URL`、`thumbnail benefit`、`miniapp render` 五个维度
- **AND** 每个维度 MUST 支持 `pass`、`fail`、`n/a`、`blocked` 或等价状态
- **AND** `n/a` 与 `blocked` MUST 记录原因，不得留空
- **AND** 每个媒体样例 MUST 可独立记录和追踪。

#### Scenario: key 维度覆盖对象标识和命名规则

- **WHEN** 模板使用者检查 `key` 维度
- **THEN** 记录 MUST 包含媒体类型、业务资源、`object_key` 或等价脱敏对象标识
- **AND** MUST 确认 key 符合 MinIO 单桶 + 前缀策略
- **AND** MUST 确认 key 不使用用户原始文件名
- **AND** 历史对象或迁移对象 MUST 记录旧 key、新 key 或兼容读取状态。

#### Scenario: object 维度覆盖对象存储事实

- **WHEN** 模板使用者检查 `object` 维度
- **THEN** 记录 MUST 确认对象存储中真实 object 存在并能与业务记录中的 key 对应
- **AND** MUST 覆盖 MIME Type、文件大小、扩展名、安全校验和权限边界
- **AND** 对象不存在、大小为 0、类型不匹配或权限错误 MUST 记录失败表现和排查线索
- **AND** 记录 MUST NOT 暴露对象存储凭证或内部绝对路径。

#### Scenario: URL 维度覆盖受控访问结果

- **WHEN** 模板使用者检查 `URL` 维度
- **THEN** 记录 MUST 区分相对 URL、公开 URL、签名 URL、代理 URL 或等价受控访问方式
- **AND** MUST 记录访问结果、HTTP 状态、错误码、用户可见表现和入口页面或接口
- **AND** MUST 确认前端、小程序或管理端未直连未授权对象存储
- **AND** 403、404、签名过期、域名配置错误或代理错误 MUST 可被记录为失败原因。

#### Scenario: thumbnail benefit 维度覆盖真实收益

- **WHEN** 模板使用者检查 `thumbnail benefit` 维度
- **THEN** 记录 MUST 说明缩略图、封面图或轻量媒体在该场景中的实际收益
- **AND** 收益 SHOULD 覆盖列表首屏加载、卡片渲染速度、弱网体验、带宽节省、后台预览效率或视频封面识别等类型
- **AND** 若场景没有缩略图或封面图，MUST 标记 `n/a` 并说明原因
- **AND** MUST NOT 仅以“缩略图已生成”作为唯一通过标准。

#### Scenario: miniapp render 维度覆盖小程序端渲染

- **WHEN** 模板使用者检查 `miniapp render` 维度
- **THEN** 记录 MUST 覆盖微信小程序真机或等价预览环境的媒体渲染结果
- **AND** 图片类媒体 SHOULD 记录加载、占位、预览或失败态
- **AND** 视频类媒体 SHOULD 记录播放入口、封面、全屏或失败提示
- **AND** MUST 记录域名、组件或平台限制导致的 blocked 或 fail
- **AND** 若本次媒体能力不涉及小程序，MUST 标记 `n/a` 并说明影响判断。

### Requirement: 媒体五联验收失败记录

系统 MUST 要求媒体五联验收模板中的失败项可转化为后续 BUG 记录，至少包含失败现象、影响范围、复现入口、期望结果、实际结果、相关 key 或 URL、端和环境。

#### Scenario: fail 状态可转 BUG

- **WHEN** 任一五联维度状态为 `fail`
- **THEN** 记录 MUST 包含足以支撑 `/bug-capture` 的失败现象、影响范围、复现入口、期望结果和实际结果
- **AND** SHOULD 记录相关媒体类型、业务资源、key、URL、小程序页面或组件
- **AND** SHOULD 记录截图、日志或命令摘要位置。

#### Scenario: blocked 状态可重试

- **WHEN** 任一五联维度状态为 `blocked`
- **THEN** 记录 MUST 包含阻塞原因、责任环境、重试条件和当前影响判断
- **AND** blocked 项不得被视为通过
- **AND** 后续补齐环境或资源后 MUST 重新记录结果。

### Requirement: 媒体上传横切 gate

媒体五联验收模板 MUST 保留媒体上传横切 gate，并要求后续包含真实上传或回显的媒体变更检查上传状态机、同会话即时回显、Docker Web 入口和失败信息位置。与当前媒体变更无关的 gate MUST 标记 `n/a` 并说明原因，不得删除整节。

#### Scenario: 上传状态机和即时回显 gate

- **WHEN** 后续媒体变更包含上传控件、上传流程或上传后回显
- **THEN** 验收记录 MUST 检查上传状态机是否覆盖 `idle → uploading → done/failed`
- **AND** MUST 检查同一会话上传成功后是否即时回显缩略图、文件卡片或媒体 URL
- **AND** 失败信息 MUST 出现在上传控件、字段组或媒体样例记录中，不得只依赖全局 toast。

#### Scenario: Docker Web 边界文件 gate

- **WHEN** 后续媒体变更包含真实上传链路
- **THEN** 验收记录 MUST 经 Docker Web `http://localhost:3000` 或等价用户入口执行边界文件验收
- **AND** MUST NOT 只调用后端 `:8000` 作为唯一上传验收
- **AND** 若该变更不涉及真实上传，记录 MUST 标记 `n/a` 并说明原因。

### Requirement: 模板沉淀位置与引用方式

系统 MUST 将媒体五联验收模板沉淀到长期治理文档或等价模板位置，并保证后续媒体相关需求、BUG、OpenSpec Change、Sprint 验收和发布检查可以稳定引用。

#### Scenario: 长期模板文档存在

- **WHEN** 本 Change 实现完成
- **THEN** 仓库 MUST 存在长期模板文档或等价模板
- **AND** 文档 SHOULD 位于 `docs/standards/`、`rules/media.md`、对象存储相关文档或经 design/trace 明确说明的替代位置
- **AND** 模板 MUST 包含五联样例表、状态说明、N/A/blocked 填写规则和失败转 BUG 信息要求。

#### Scenario: 后续媒体变更引用模板

- **WHEN** 后续 REQ、BUG、OpenSpec Change、Sprint 或 Release 涉及图片、视频、Logo、证书图片、SKU 媒体、缩略图、封面图或小程序媒体渲染
- **THEN** 相关验收材料 SHOULD 引用媒体五联验收模板
- **AND** 使用者 MUST 按媒体样例逐项记录五联维度、状态、证据和风险。
