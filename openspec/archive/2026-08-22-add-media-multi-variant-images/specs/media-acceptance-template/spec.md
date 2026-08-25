## MODIFIED Requirements

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

### Requirement: 媒体上传横切 gate

媒体五联验收模板 MUST 保留媒体上传横切 gate，并要求后续包含真实上传、派生生成或回显的媒体变更检查上传状态机、同会话即时回显、Docker Web 入口、失败信息位置和对象存储标准前缀。与当前媒体变更无关的 gate MUST 标记 `n/a` 并说明原因，不得删除整节。

#### Scenario: 多规格生成状态机和即时回显 gate

- **WHEN** 后续媒体变更包含上传控件、派生生成流程或上传后回显
- **THEN** 验收记录 MUST 检查上传或生成状态机是否覆盖 `idle -> uploading -> done / failed` 或等价状态
- **AND** MUST 检查同一会话上传成功后是否即时回显 `thumbnail`、`display`、文件卡片或媒体 URL
- **AND** 失败信息 MUST 出现在上传控件、字段组或媒体样例记录中，不得只依赖全局 toast。
