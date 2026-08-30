## MODIFIED Requirements

### Requirement: 存量图片必须支持批量生成多规格资源

系统 MUST 支持对存量图片批量生成 `thumbnail` 与 `display`。批量生成 MUST 覆盖 SKU 图片、品牌 Logo、品牌证书图片、图片类证书文件，以及 Banner 自定义上传图。批量生成 MUST 采用 dry-run / apply 两阶段，MUST 默认只读，apply MUST 显式触发，并 MUST 提供幂等性、失败统计、重试建议、二次审计和脱敏输出。针对 JPEG、PNG、WebP 原图，批量生成的 `thumbnail` 与 `display` MUST 使用 WebP 派生格式；SVG、PDF、GIF、HEIC、TIFF、BMP 或不支持对象 MUST 记录跳过、拒绝或 fallback 分类。批量生成 MUST 保留原图格式、MIME 和访问语义，MUST NOT 将原图转码替换为 WebP。

#### Scenario: 存量图片 WebP dry-run 不写入

- **WHEN** 运维执行存量图片 WebP 多规格生成 dry-run
- **THEN** 输出 MUST 包含待处理数量、已存在 WebP 派生数量、缺失规格、跳过原因、失败分类、预计写入对象和风险摘要
- **AND** 当 Banner 自定义上传图缺少 `.thumb.webp` 或 `.display.webp` 时，输出 MUST 包含 Banner 候选来源
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST NOT 包含真实密钥、数据库连接串、Authorization header、Cookie、真实 `.env`、本机绝对路径、未脱敏 object key 全量值或真实客户数据。

#### Scenario: 存量图片 WebP apply 显式受控

- **GIVEN** dry-run 已完成且备份或风险确认已记录
- **WHEN** 运维显式执行 WebP 派生 apply
- **THEN** 系统 MUST 为支持格式生成缺失或不合格的 WebP `thumbnail` 与 WebP `display`
- **AND** Banner 自定义上传图的派生图 MUST 写入原图同目录，使用 `.thumb.webp` 与 `.display.webp` 后缀
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等
- **AND** apply 后 MUST 支持二次审计验证 key、object、URL、render 和规格收益。
