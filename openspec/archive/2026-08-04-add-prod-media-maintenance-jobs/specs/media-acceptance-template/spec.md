## MODIFIED Requirements

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

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。涉及品牌证书时，模板 SHALL 明确区分图片类证书和 PDF/文档类证书：图片类证书 key 使用 `images/`，PDF/文档类证书 key 使用 `files/`。涉及生产媒体维护作业失败、返修或回归时，四联模板 SHALL 引用维护作业 dry-run/apply/二次审计摘要。

#### Scenario: 媒体上传链路横切验收

- **WHEN** 媒体类 BUG 涉及上传、编辑、列表回显、历史对象、缩略图、回填或审计脚本
- **THEN** 四联模板 SHALL 要求记录上传状态机 `idle -> uploading -> done/failed` 或等价状态证据
- **AND** 涉及 Web 管理端上传/编辑/列表刷新时 SHALL 记录同会话即时回显 evidence
- **AND** 涉及品牌证书图片时 SHALL 记录图片原图和缩略图 key 均归入 `images/` 或等价标准图片前缀
- **AND** 涉及品牌证书 PDF 或文档附件时 SHALL 记录文件 key 归入 `files/`
- **AND** 涉及上传大小、Nginx 或 Docker Web 边界时 SHALL 通过 `http://localhost:3000` 或等价 Web 入口验证边界文件，或记录 `N/A` 原因
- **AND** 涉及历史对象、缩略图、回填或审计脚本时 SHALL 记录 dry-run/apply/统计摘要，且输出 SHALL NOT 泄露敏感信息。

#### Scenario: 生产维护失败可转缺陷

- **WHEN** 生产媒体维护作业的四联摘要出现 `fail`
- **THEN** 摘要 MUST 记录失败维度、脱敏对象标识、影响范围、实际结果、期望结果和重试条件
- **AND** 摘要 SHOULD 能被直接用于后续 `/bug-capture`
- **AND** blocked 项不得被视为通过。
