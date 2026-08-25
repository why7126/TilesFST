## ADDED Requirements

### Requirement: 证书详情品牌入口必须消费品牌 Logo 缩略图

证书详情 API 或小程序数据适配层 MUST 为所属品牌数据提供 `brand_logo_thumbnail_url` 或等价品牌 Logo 缩略图 URL。证书详情页品牌卡片普通展示 MUST 优先消费该缩略图字段。缩略图缺失、不可读或加载失败时，系统 MUST 使用安全占位、品牌首字或统一失败态；验收 MUST NOT 将品牌 Logo 原图 fallback 写作缩略图性能通过。

#### Scenario: 证书详情 brand 数据包含品牌缩略图字段

- **WHEN** 小程序请求证书详情并响应包含所属品牌
- **THEN** 响应或页面适配后的 `brand` 数据 MUST 包含 `brand_logo_thumbnail_url` 或等价缩略图字段
- **AND** 该字段 MUST 表示适合品牌卡片小图展示的受控 URL 或安全静态资源
- **AND** 响应 MUST NOT 暴露对象存储原始 Key、本机路径、后台备注、内部审计字段或真实存储凭据。

#### Scenario: 证书详情品牌卡片不使用原图 fallback

- **WHEN** 证书详情页品牌卡片渲染品牌 Logo
- **THEN** 小程序 MUST 优先请求 `brand_logo_thumbnail_url` 或等价缩略图 URL
- **AND** 缩略图缺失、为空或加载失败时 MUST 使用安全占位或统一失败态
- **AND** 小图展示场景 MUST NOT 请求品牌 Logo 原图作为默认 fallback。

#### Scenario: 证书详情品牌 Logo 四联验收

- **WHEN** 团队验收证书详情页品牌入口
- **THEN** 验收 SHALL 记录品牌 Logo 缩略图的 key、object、URL 和 render 四联证据，无法适用的维度 SHALL 明确标注 N/A 原因
- **AND** Network evidence SHALL 记录 URL 类型、HTTP 状态、资源大小、耗时和渲染结论
- **AND** 验收记录 SHALL NOT 包含 Authorization header、Cookie、真实 `.env`、本机绝对路径或未脱敏 object key。

