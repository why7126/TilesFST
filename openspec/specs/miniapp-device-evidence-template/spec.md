# miniapp-device-evidence-template Specification

## Purpose
定义微信小程序 DevTools 预览、真机验收、自动化证据、N/A、blocked 与 follow-up 的统一 evidence 模板，确保后续小程序需求、BUG、OpenSpec Change、Sprint 验收报告和 release note 能区分真实设备验收、开发者工具预览和静态测试边界。
## Requirements
### Requirement: 小程序设备验收 evidence 模板

系统 MUST 提供一套可复用的 `miniapp_device_evidence` 模板，用于微信小程序相关需求、BUG、OpenSpec Change、Sprint 验收报告和 release note 统一记录 DevTools 预览、真机验收、自动化证据、N/A、blocked 和 follow-up 结论。

#### Scenario: 模板基础结构完整

- **WHEN** 团队创建或引用小程序设备验收 evidence 模板
- **THEN** 模板 MUST 包含 `template_ref`、`target`、`pages`、`evidence_items` 和 `summary` 字段或等价表格列
- **AND** `target` MUST 支持记录 REQ、BUG 或 OpenSpec Change ID
- **AND** `pages` MUST 支持记录页面路径、页面标题、关键 query 参数和验收场景
- **AND** `summary` MUST 支持记录最终结论、阻塞项、剩余风险和后续承接方式。

#### Scenario: evidence 状态可复用

- **WHEN** 模板记录任一 evidence item
- **THEN** evidence 状态 MUST 为 `required`、`passed`、`failed`、`blocked`、`not_applicable` 或 `follow_up` 之一
- **AND** `passed` MUST 有可复核证据，例如截图、录屏、命令摘要、人工验收摘要或 artifact 引用
- **AND** `failed` MUST 记录失败表现、影响页面和后续处理建议
- **AND** `blocked`、`not_applicable` 和 `follow_up` MUST 记录原因
- **AND** `follow_up` MUST 记录剩余风险、责任人或后续承接方式。

### Requirement: DevTools 与真机 evidence 字段

系统 MUST 在小程序设备验收 evidence 模板中分别定义 DevTools 预览和真机验收字段，使两类人工设备证据可以被独立记录和复核。

#### Scenario: DevTools evidence 字段完整

- **WHEN** 团队记录 DevTools 预览 evidence
- **THEN** evidence MUST 记录微信开发者工具版本或可识别版本摘要
- **AND** MUST 记录小程序基础库版本
- **AND** MUST 记录模拟器设备或 viewport 宽度，例如 320、375、430 pt
- **AND** MUST 记录页面路径、关键 query 参数和验收场景
- **AND** MUST 记录截图、录屏、报告相对路径，或无法保存文件时的人工摘要
- **AND** 结论 MUST 明确 DevTools 预览不等同于真机验收，除非另有真机 evidence。

#### Scenario: 真机 evidence 字段完整

- **WHEN** 团队记录真机验收 evidence
- **THEN** evidence MUST 记录设备型号、系统类型与版本、微信版本和小程序基础库版本
- **AND** MUST 记录页面路径、关键 query 参数和用户状态
- **AND** MUST 记录视口宽度、安全区、状态栏和微信原生胶囊避让结论
- **AND** MUST 记录执行人、执行时间、截图或录屏引用、验收结论和剩余风险。

#### Scenario: 高风险小程序交互需要真机结论或例外状态

- **WHEN** Change 涉及自定义导航栏、fixed header、触控区域、分享、返回、关闭、图片预览或页面滚动
- **THEN** evidence SHOULD 至少保留一条真机验收记录
- **AND** 若无法执行真机验收，MUST 标记 `blocked` 或 `follow_up`
- **AND** 不得在缺少真机 evidence 时写作“真机通过”。

### Requirement: 自动化与人工设备证据边界

系统 MUST 明确静态测试、脚本/单元测试、DevTools 预览和真机验收的证据边界，防止验收报告、Change trace 或 release note 混淆结论。

#### Scenario: 自动化证据不得替代设备验收

- **WHEN** 静态测试、脚本测试或单元测试通过
- **THEN** evidence MAY 记录命令摘要和覆盖边界
- **AND** 静态测试通过 MUST NOT 被表述为 DevTools 实际渲染通过
- **AND** 脚本或单元测试通过 MUST NOT 被表述为真机安全区、微信原生能力或真实触控通过。

#### Scenario: DevTools 不等同真机

- **WHEN** DevTools 预览通过但缺少真机验收记录
- **THEN** Sprint 验收报告、release note 和 Change trace MUST 避免写成“真机通过”或“设备验收已完成”
- **AND** summary MUST 将真机结论标记为 `required`、`blocked`、`not_applicable` 或 `follow_up` 并说明原因。

#### Scenario: N/A 必须可复核

- **WHEN** Change 不影响小程序页面渲染、导航、安全区、触控或真实运行入口
- **THEN** 模板 MAY 将 DevTools 或真机 evidence 标记为 `not_applicable`
- **AND** N/A reason MUST 说明不适用事实，例如仅新增模板文档、不改小程序运行时代码、不改 UI 交互或不改真实页面入口。

### Requirement: evidence 安全与引用方式

系统 MUST 约束小程序设备验收 evidence 的存储路径、敏感信息边界和后续引用方式，使证据可复核且不泄露敏感数据。

#### Scenario: 证据路径与敏感信息安全

- **WHEN** 模板记录截图、录屏、报告、命令摘要或人工记录
- **THEN** 路径 MUST 使用仓库相对路径或稳定 artifact 引用
- **AND** evidence MUST NOT 记录本机绝对路径、token、Cookie、Authorization header、`.env` 内容、真实密钥、数据库 DSN、MinIO 凭据、真实客户数据、未脱敏手机号、地址或个人隐私
- **AND** evidence MUST NOT 复制大段日志、完整构建输出或无法复核的口头描述
- **AND** 若截图包含敏感信息，MUST 先脱敏或记录不可公开原因。

#### Scenario: 标准文档沉淀

- **WHEN** 本能力实现完成
- **THEN** 仓库 MUST 存在小程序设备验收 evidence 长期标准文档
- **AND** 文档 SHOULD 位于 `docs/standards/miniapp-device-evidence-template.md`
- **AND** 若不位于该路径，Change trace 或 design MUST 说明替代位置和引用方式。

#### Scenario: 后续流程引用模板

- **WHEN** 后续小程序 REQ、OpenSpec Change、Sprint 验收报告或 release note 需要记录设备验收结论
- **THEN** 相关材料 SHOULD 引用小程序设备验收 evidence 模板
- **AND** OpenSpec `tasks.md` SHOULD 将 DevTools 或真机 evidence 作为人工验收任务
- **AND** Sprint `acceptance-report.md` SHOULD 汇总设备验收通过、阻塞、N/A 或 follow-up 结论
- **AND** release note SHOULD 只记录用户可理解的设备验收结论和剩余风险，不复制完整 evidence。

### Requirement: 小程序分享设备 evidence
小程序分享能力验收 SHALL 记录 DevTools、真机、静态测试、blocked 或 follow-up 结论，明确分享、返回、原生胶囊和运行入口同步的证据边界。

#### Scenario: 分享矩阵 evidence
- **WHEN** 团队验收首页、商品详情页、商品列表页和品牌详情页的微信分享
- **THEN** evidence SHALL 覆盖微信朋友分享和朋友圈分享
- **AND** evidence SHALL 记录页面路径、关键 query 参数、分享渠道、视口或设备来源和结论
- **AND** evidence SHALL 覆盖 DevTools 320、375、430 pt 或等价静态视口检查。

#### Scenario: 真机不可用时标记剩余风险
- **WHEN** 分享、返回、原生胶囊或页面滚动涉及真机体验但无法执行真机验收
- **THEN** evidence SHALL 标记 `blocked` 或 `follow_up`
- **AND** 验收报告、Change trace 或 release note SHALL NOT 写作真机通过
- **AND** remaining risk SHALL 说明缺少真机结论的影响和后续承接方式。

#### Scenario: 运行入口同步 evidence
- **WHEN** 小程序页面同时存在维护源码 `.ts` 与实际运行 `.js`
- **THEN** 静态测试或等价验收 SHALL 确认四个目标页面的运行 `.js` 包含对应分享配置
- **AND** `.ts` 包含 `onShareAppMessage` 或 `onShareTimeline` 但 `.js` 缺失对应逻辑时 SHALL 视为验收失败
- **AND** 静态测试通过 SHALL NOT 被表述为 DevTools 渲染通过或真机通过。

### Requirement: 小程序 Network evidence
系统 SHALL 在小程序 evidence 模板中支持 Network evidence，用于记录 DevTools 网络面板和体验版网络链路验证，且 SHALL 与静态测试、生产接口 smoke、DevTools 预览和真机 evidence 区分。

#### Scenario: Network evidence 来源可区分
- **WHEN** 团队记录小程序 Network evidence
- **THEN** evidence source SHALL 支持 `network_devtools` 与 `network_trial`
- **AND** `network_devtools` SHALL 表示微信开发者工具网络面板验证
- **AND** `network_trial` SHALL 表示体验版或等价手机体验入口网络链路验证
- **AND** 两者 SHALL NOT 被静态测试或生产接口 smoke 自动标记为 `passed`。

#### Scenario: DevTools Network 字段完整
- **WHEN** 团队记录 `network_devtools` evidence
- **THEN** evidence SHALL 记录微信开发者工具版本或可识别版本摘要、小程序基础库版本、运行策略、`urlCheck` 状态、页面路径和关键 query
- **AND** SHALL 记录请求域名、关键 API HTTP 状态、业务响应状态、图片/视频/证书/静态资源加载结论
- **AND** 结论 SHALL 明确 DevTools Network 不等同于体验版或真机网络验收。

#### Scenario: 体验版 Network 字段完整
- **WHEN** 团队记录 `network_trial` evidence
- **THEN** evidence SHALL 记录体验版来源、最新版本确认方式、重新扫码或等价入口确认、页面路径和验证场景
- **AND** SHALL 记录体验版是否请求生产 API 域名
- **AND** SHALL 记录首页、至少一个列表页、至少一个详情或媒体资源页面的接口和资源加载结论
- **AND** 若体验版 Network 工具不可用，evidence SHALL 记录替代观察方式、阻塞原因、剩余风险和后续承接方式。

#### Scenario: Network evidence 状态与安全
- **WHEN** Network evidence 未完成、失败或不可用
- **THEN** 状态 SHALL 使用 `required`、`failed`、`blocked`、`not_applicable` 或 `follow_up` 表达
- **AND** 缺少体验版 Network evidence 时 SHALL NOT 写作 `passed`
- **AND** evidence SHALL NOT 记录 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据、未脱敏隐私或完整网络日志。

### Requirement: 小程序媒体 Network evidence

系统 SHALL 在小程序设备 evidence 模板中支持媒体资源 Network evidence，用于记录图片、视频、Logo、证书图片、缩略图、封面图和受控 `/media` URL 的真实请求链路。媒体 Network evidence SHALL 与静态测试、接口 smoke、DevTools 预览和真机 render evidence 区分。

#### Scenario: 媒体 Network 字段完整

- **WHEN** 团队记录小程序媒体资源 Network evidence
- **THEN** evidence SHALL 记录页面路径、验证场景、请求域名、HTTP 状态、业务响应状态、资源类型、资源大小或耗时摘要
- **AND** SHALL 记录媒体 URL 类型、受控 `/media` 访问方式、resolved / fallback 结论或等价观测摘要
- **AND** SHALL 记录该 evidence 来源为 `network_devtools`、`network_trial`、`real_device` 或明确的替代来源
- **AND** DevTools Network 结论 SHALL 明确不等同于体验版或真机网络验收。

#### Scenario: 缺少体验版或真机证据时不能写通过

- **WHEN** 小程序媒体性能变更影响真实用户体感但缺少体验版或真机 Network evidence
- **THEN** evidence SHALL 使用 `required`、`blocked` 或 `follow_up` 表达
- **AND** SHALL 记录阻塞原因、责任环境、重试条件和发布前承接方式
- **AND** SHALL NOT 写作体验版或真机媒体 Network 验收已通过。

#### Scenario: 媒体 Network evidence 安全

- **WHEN** 团队记录小程序媒体 Network evidence
- **THEN** evidence SHALL NOT 包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据、未脱敏 object key 全量值或完整网络日志
- **AND** 截图、录屏或报告包含敏感信息时 SHALL 先脱敏或记录不可公开原因。

### Requirement: 小程序证据来源声明

小程序设备与 Network evidence 模板 SHALL 说明证据来源、执行方式、覆盖入口和证明边界；DevTools 预览、DevTools Network、静态校验或开发 API smoke 证据不得被表述为体验版、真机、线上或发布完成通过。

#### Scenario: DevTools 支撑当前范围验收
- **WHEN** 小程序 Change 记录 DevTools 截图、DevTools 预览或 DevTools Network evidence
- **THEN** evidence SHALL 可用于支撑其实际覆盖范围内的开发验收或问题排查结论
- **AND** 记录 SHALL 包含 `evidence_source`、`verification_boundary`、`evidence_ref`、`network_summary` 或等价信息
- **AND** 结论 SHALL 明确不等同于体验版、真机、线上或发布完成通过。

#### Scenario: 小程序入口或设备当前不可验证
- **WHEN** 体验版入口、真机设备、线上域名、线上接口或真实用户路径当前不可验证
- **THEN** 记录 SHALL 说明当前已有证据来源、不可验证原因、后续承接方式或 N/A 理由
- **AND** `production_only_pending` SHALL 仅作为历史兼容字段解释，不作为新流程推荐分类
- **AND** SHALL NOT 因当前不可获得证据而扩大通过结论。

