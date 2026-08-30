# media-acceptance-template Specification

## Purpose
定义媒体五联验收模板，统一后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布检查对 key、object、URL、thumbnail benefit 与 miniapp render 的证据记录、失败处理、横切上传 gate 和引用方式。
## Requirements
### Requirement: 媒体五联验收模板

系统 MUST 提供一套可复用的媒体五联验收模板，用于后续媒体相关 REQ、BUG、OpenSpec Change、Sprint 验收和发布前检查统一记录 `key`、`object`、`URL`、`thumbnail/display benefit` 与 `miniapp render` 五个维度的状态、证据、N/A 理由、blocked 原因和失败处理线索。涉及多规格图片时，模板 MUST 区分 `thumbnail`、`display`、`original`，并记录三类资源的对象存在性、URL 语义、体积/像素收益和端上实际使用情况。

#### Scenario: 多规格图片验收覆盖

- **WHEN** 团队为媒体多规格图片能力记录验收
- **THEN** 验收记录 MUST 分别覆盖 `thumbnail`、`display`、`original`
- **AND** key 维度 MUST 记录脱敏 key hash、标准前缀、资源类型和规格类型
- **AND** object 维度 MUST 记录存在性、MIME、size、像素或体积收益
- **AND** URL 维度 MUST 记录 URL 类型、HTTP 状态、业务状态、缓存或签名边界
- **AND** render 维度 MUST 记录列表、详情、预览的实际展示、fallback 或失败态。

#### Scenario: 小程序 Network evidence 覆盖

- **WHEN** 多规格图片影响微信小程序展示
- **THEN** 验收记录 MUST 分别记录列表 `thumbnail_url`、详情 `display_url`、预览 `original_url` 的页面路径、URL 类型、HTTP 状态、资源大小和耗时
- **AND** DevTools Network 不得自动等同于体验版或真机通过
- **AND** 缺少体验版或真机 evidence 时 MUST 标记 `blocked` 或 `follow_up`。

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

媒体五联验收模板 MUST 保留媒体上传横切 gate，并要求后续包含真实上传、派生生成或回显的媒体变更检查上传状态机、同会话即时回显、Docker Web 入口、失败信息位置和对象存储标准前缀。与当前媒体变更无关的 gate MUST 标记 `n/a` 并说明原因，不得删除整节。

#### Scenario: 多规格生成状态机和即时回显 gate

- **WHEN** 后续媒体变更包含上传控件、派生生成流程或上传后回显
- **THEN** 验收记录 MUST 检查上传或生成状态机是否覆盖 `idle -> uploading -> done / failed` 或等价状态
- **AND** MUST 检查同一会话上传成功后是否即时回显 `thumbnail`、`display`、文件卡片或媒体 URL
- **AND** 失败信息 MUST 出现在上传控件、字段组或媒体样例记录中，不得只依赖全局 toast。

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

### Requirement: 小程序媒体四联最佳实践

系统 SHALL 为小程序媒体性能相关需求、BUG、OpenSpec Change、Sprint 验收和发布检查提供小程序媒体四联最佳实践引用。该实践 SHALL 覆盖 `key`、`object`、`URL`、`render` 四个维度，并 SHALL 明确对象存在、`.thumb` URL 存在、接口测试通过或只读审计摘要均不能单独证明小程序媒体性能验收通过。该实践 SHALL 不替代媒体五联验收模板或媒体类 BUG 四联验收模板，而是补充小程序媒体场景的 Network evidence、真实轻量资源命中、高清展示图语义和端侧 render 证据要求。

#### Scenario: 详情页高清展示与列表缩略图区分

- **WHEN** 团队验收小程序商品详情页媒体清晰度修复
- **THEN** 验收记录 SHALL 区分详情页展示 URL、图片预览 URL、商品列表卡片 URL、推荐位 URL 和 Banner URL
- **AND** 详情页展示 URL SHALL 使用原图或详情级高清展示图
- **AND** 图片预览 URL SHALL 使用原图或等价高清 URL
- **AND** 商品列表、商品卡片、推荐位和 Banner URL SHALL 继续使用 `.thumb` 或等价轻量图片
- **AND** render evidence SHALL 覆盖清晰度、轮播高度和首屏商品信息露出。

### Requirement: 媒体验收环境分层

媒体五联和媒体类 BUG 四联验收 SHALL 区分开发证据、体验版证据和生产证据，生产环境不可用时不得阻塞开发归档，但必须作为发布阶段或发布后待办记录。

#### Scenario: 开发阶段媒体 render 证据
- **WHEN** 媒体 BUG 或 Change 在开发阶段验证列表图、详情图、证书图、Logo、缩略图或受控 `/media` URL
- **THEN** 验收记录 MAY 使用开发 API smoke、对象存储审计摘要、DevTools 截图或 DevTools Network evidence
- **AND** 该结论 SHALL 标记为开发阶段通过或开发证据充分
- **AND** SHALL NOT 写作生产对象、生产域名、体验版或真机 Network 已通过。

#### Scenario: 生产媒体证据后置
- **WHEN** 生产对象、生产接口、生产 no-fallback、生产缩略图回填或生产真实用户路径只有发布或生产维护后才能验证
- **THEN** 开发阶段验收 SHALL 将该缺口记录为 `production_only_pending` 或发布阶段待办
- **AND** SHALL 记录重试条件、责任环境和后续承接命令
- **AND** SHALL NOT 将该缺口作为开发归档 blocker，除非 Change 目标明确是生产维护执行。

#### Scenario: 生产维护或生产发布强门禁
- **WHEN** Change 目标明确为生产维护执行，或发布对象声明 `release_target.environment=production`
- **THEN** 生产对象、生产 URL、生产 no-fallback 媒体、备份、dry-run/apply 和二次审计证据 SHALL 按范围参与强门禁
- **AND** 缺失时 SHALL 标记为 `blocked`、`environment_unavailable` 或 `publish_evidence_missing`。

