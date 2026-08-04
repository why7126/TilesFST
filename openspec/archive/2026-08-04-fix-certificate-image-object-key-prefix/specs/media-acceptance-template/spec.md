## ADDED Requirements

### Requirement: 媒体类 BUG 必须使用四联验收模板

媒体类 BUG 修复、返修、回归测试、Sprint 验收或发布前检查 SHALL 使用媒体类 BUG 四联验收模板。模板 SHALL 覆盖原 BUG 场景、`key`、`object`、`URL`、`render` 四个维度，并 SHALL 为每个维度记录 `pass`、`fail`、`n/a` 或 `blocked` 状态、证据和失败/阻塞处理。模板 SHALL 遵守对象存储单桶策略、对象 Key 标准前缀、后端受控媒体读取、上传安全和小程序平台限制。模板 SHALL NOT 记录真实客户数据、真实密钥、Authorization header、Cookie、`.env` 内容、本机绝对路径或未脱敏 MinIO 凭证。涉及品牌证书时，模板 SHALL 明确区分图片类证书和 PDF/文档类证书：图片类证书 key 使用 `images/`，PDF/文档类证书 key 使用 `files/`。

#### Scenario: key 维度验收

- **WHEN** 团队验收媒体类 BUG 的 key 维度
- **THEN** 验收记录 SHALL 确认业务记录中的媒体 key 稳定、可追溯，并符合单 Bucket 标准前缀策略
- **AND** 验收记录 SHALL 禁止用户原始文件名、本机绝对路径、临时路径或未脱敏内部路径作为对象存储 key
- **AND** 若修复涉及品牌证书，验收记录 SHALL 区分图片类证书 `images/` key 与 PDF/文档类证书 `files/` key
- **AND** 若修复涉及历史 key 兼容或迁移，验收记录 SHALL 包含旧 key、新 key 和兼容结果。

#### Scenario: 媒体上传链路横切验收

- **WHEN** 媒体类 BUG 涉及上传、编辑、列表回显、历史对象、缩略图、回填或审计脚本
- **THEN** 四联模板 SHALL 要求记录上传状态机 `idle -> uploading -> done/failed` 或等价状态证据
- **AND** 涉及 Web 管理端上传/编辑/列表刷新时 SHALL 记录同会话即时回显 evidence
- **AND** 涉及品牌证书图片时 SHALL 记录图片原图和缩略图 key 均归入 `images/` 或等价标准图片前缀
- **AND** 涉及品牌证书 PDF 或文档附件时 SHALL 记录文件 key 归入 `files/`
- **AND** 涉及上传大小、Nginx 或 Docker Web 边界时 SHALL 通过 `http://localhost:3000` 或等价 Web 入口验证边界文件，或记录 `N/A` 原因
- **AND** 涉及历史对象、缩略图、回填或审计脚本时 SHALL 记录 dry-run/apply/统计摘要，且输出 SHALL NOT 泄露敏感信息。
