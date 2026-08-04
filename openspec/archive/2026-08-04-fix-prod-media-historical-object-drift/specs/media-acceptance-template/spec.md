## MODIFIED Requirements

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
