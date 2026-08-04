# media-acceptance-template Specification

## Purpose
定义媒体五联验收模板，统一后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布检查对 key、object、URL、thumbnail benefit 与 miniapp render 的证据记录、失败处理、横切上传 gate 和引用方式。
## Requirements
### Requirement: 媒体五联验收模板

系统 MUST 提供一套可复用的媒体五联验收模板，用于后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布前检查统一记录 `key`、`object`、`URL`、`thumbnail benefit` 与 `miniapp render` 五个维度的状态、证据、N/A 理由、blocked 原因和失败处理线索。模板 MUST 不记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。生产媒体维护作业执行后 MUST 输出可映射到五联维度的验收摘要；不涉及小程序或端侧渲染时 MUST 标记 `n/a` 或 `blocked` 并说明原因。

#### Scenario: 模板包含五联维度

- **WHEN** 团队为媒体相关需求、缺陷、变更、Sprint 或 Release 引用媒体五联验收模板
- **THEN** 模板 MUST 包含 `key`、`object`、`URL`、`thumbnail benefit`、`miniapp render` 五个维度
- **AND** 每个维度 MUST 支持 `pass`、`fail`、`n/a`、`blocked` 或等价状态
- **AND** `n/a` 与 `blocked` MUST 记录原因，不得留空
- **AND** 每个媒体样例 MUST 可独立记录和追踪。

#### Scenario: 生产维护作业输出五联摘要

- **WHEN** 生产媒体维护作业完成 dry-run、apply 或二次审计
- **THEN** 输出 SHOULD 包含 key、object、URL、thumbnail benefit、miniapp render 的状态摘要
- **AND** 不涉及缩略图收益时 MUST 将 `thumbnail benefit` 标记为 `n/a` 并说明原因
- **AND** 不涉及小程序端渲染时 MUST 将 `miniapp render` 标记为 `n/a` 或 `blocked` 并说明影响判断
- **AND** 任一 `fail` 项 MUST 包含足以支撑后续 `/bug-capture` 的失败现象、影响范围、期望结果和实际结果。

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

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。涉及品牌证书时，模板 SHALL 明确区分图片类证书和 PDF/文档类证书：图片类证书 key 使用 `images/`，PDF/文档类证书 key 使用 `files/`。针对 `BUG-0116-prod-media-historical-object-drift`，验收记录 SHALL 覆盖 SKU 商品图片、品牌 Logo 和品牌证书图片三类历史媒体对象，并 SHALL 记录 dry-run、apply、二次审计、幂等和 fail / blocked 摘要。

#### Scenario: BUG-0116 四联验收覆盖三类对象

- **GIVEN** BUG-0116 修复已执行 dry-run 或 apply
- **WHEN** 团队回填媒体 BUG 四联验收
- **THEN** `key` 维度 SHALL 分别记录 SKU 主图、品牌 Logo 和证书图片的脱敏 key、前缀策略、旧 key / 新 key 或不迁移原因
- **AND** `object` 维度 SHALL 记录原图 object、同目录 `.thumb` object、MIME、size、扩展名、权限、同 size / 同 bytes 检查和 dry-run/apply/幂等摘要
- **AND** `URL` 维度 SHALL 记录 `/media/{object_key}` 或等价后端受控 URL 的 HTTP 状态、业务错误码和用户可见表现
- **AND** `render` 维度 SHALL 记录 Web 管理端、店主 Web、小程序受影响页面的展示、预览、占位或失败态 evidence
- **AND** 任一维度为 `fail` 或 `blocked` 时 SHALL 记录实际结果、期望结果、影响范围、排查线索和重试条件。

#### Scenario: BUG-0116 生产执行证据边界

- **GIVEN** BUG-0116 修复需要在生产或生产等价环境执行维护任务
- **WHEN** 团队记录验收证据
- **THEN** 证据 SHALL 包含备份确认摘要、dry-run 摘要、apply 摘要、二次审计摘要和幂等复跑摘要
- **AND** 若真实生产 apply 尚未执行，验收 SHALL 标记 `blocked` 或 external evidence 待补充
- **AND** 证据 SHALL NOT 包含生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径、真实客户数据或不可公开运维地址。

