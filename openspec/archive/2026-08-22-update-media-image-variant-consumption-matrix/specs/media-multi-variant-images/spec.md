## MODIFIED Requirements

### Requirement: 媒体图片必须支持多规格展示图

系统 MUST 支持 `thumbnail`、`display`、`original` 三类媒体图片规格。`thumbnail` MUST 用于列表、卡片和轻量预览；`display` MUST 用于详情普通展示和图册浏览；`original` MUST 保留上传原图或等价高清资源，用于高清预览、下载或需要保真的场景。三类规格 MUST 可追溯到同一媒体记录或业务对象，并 MUST 明确 key、MIME、尺寸、质量、体积上限、生成状态和失败原因的记录方式。

系统 MUST 沉淀 Web 与微信小程序统一的图片三规格消费矩阵。矩阵字段 MUST 至少包括：页面、位置、图对象、是否缩略图、是否 display 图、是否原图、优化方案。矩阵 MUST 覆盖微信小程序真实页面、Web 管理端真实媒体展示位置，并为店主 Web 展示端提供明确的预留规范。矩阵中的每个页面位置 MUST 只表达一个主消费规格；普通展示、高清预览、下载或原文件查看使用不同规格时，MUST 拆成独立行。

非原图目标场景 MUST NOT fallback 到 `original`。当列表、卡片、推荐位、小 Logo 等 `thumbnail` 目标场景，或详情普通展示、图册浏览、表单大预览等 `display` 目标场景缺少目标规格时，系统 MUST 使用安全占位、补齐派生图或在矩阵优化方案中标记后续修正；验收 MUST NOT 将原图 fallback 写作缩略图或展示图性能通过。

#### Scenario: 新上传图片生成三规格资源

- **WHEN** 管理端用户上传合法图片
- **THEN** 系统 MUST 保留 `original`
- **AND** 系统 MUST 生成或调度生成 `thumbnail` 与 `display`
- **AND** 三规格资源 MUST 能追溯到同一媒体记录或业务对象
- **AND** 生成失败 MUST 有可观测记录和明确降级策略
- **AND** 错误响应或日志摘要 MUST NOT 暴露对象存储密钥、Authorization header、Cookie、真实 `.env`、本机绝对路径或真实客户数据。

#### Scenario: 派生规格缺失时可安全回退

- **GIVEN** 目标规格 URL 缺失、生成失败或对象不可读
- **WHEN** 客户端请求列表、详情或预览媒体
- **THEN** 系统 MUST 按明确 fallback 顺序返回可用 URL 或安全占位
- **AND** fallback 事件 MUST 可观测
- **AND** 验收记录 MUST NOT 将 fallback 原图视为轻量规格性能通过。

#### Scenario: 统一消费矩阵覆盖小程序页面

- **WHEN** 团队维护图片三规格消费矩阵
- **THEN** 矩阵 MUST 覆盖微信小程序首页、商品列表页、搜索页、商品详情页、品牌列表页、品牌详情页、证书列表页、证书详情页和收藏页
- **AND** 首页 Banner、商品卡片、搜索结果、推荐商品、品牌 Logo、证书缩略图和收藏商品卡片 MUST 以 `thumbnail` 为目标规格
- **AND** 商品详情 Banner 普通展示和证书详情普通展示 MUST 以 `display` 为目标规格
- **AND** 商品图片预览、证书图片预览、下载或原文件查看 MUST 以 `original` 为目标规格
- **AND** 不使用业务媒体的页面 MAY 标注“不涉及业务图片”。

#### Scenario: 统一消费矩阵覆盖 Web 管理端真实媒体位置

- **WHEN** 团队维护图片三规格消费矩阵
- **THEN** 矩阵 MUST 覆盖 Web 管理端 SKU 管理、Banner 管理、品牌管理、品牌证书管理、用户或个人资料中的真实媒体展示位置
- **AND** SKU 列表主图、Banner 列表图、品牌列表 Logo、证书列表缩略图、头像列表或菜单 MUST 以 `thumbnail` 为目标规格
- **AND** SKU 表单图片网格或大预览、Banner 表单选择或回显预览、证书表单图片普通预览 MUST 以 `display` 为目标规格
- **AND** SKU 图片高清预览、Banner 原图审核或放大查看、证书下载或原文件查看 MUST 以 `original` 为目标规格
- **AND** 当前只存在原图 fallback 或单一 URL 字段的位置 MUST 在优化方案中标记为移除原图 fallback、补齐目标规格字段或使用安全占位。

#### Scenario: 店主 Web 展示端按预留规范处理

- **GIVEN** 店主 Web 展示端真实业务页面尚未作为本 Change 验收对象
- **WHEN** 团队维护图片三规格消费矩阵
- **THEN** 店主 Web 条目 MUST 标注为预留规范
- **AND** 商品列表、商品卡片、推荐商品、品牌列表 Logo、品牌卡片和证书列表 SHOULD 以 `thumbnail` 为目标规格
- **AND** 商品详情普通展示、图册浏览、品牌详情头图普通展示和证书详情普通展示 SHOULD 以 `display` 为目标规格
- **AND** 点击放大、高清预览、下载和原文件查看 SHOULD 以 `original` 为目标规格
- **AND** 预留规范 MUST NOT 被写作当前实现已满足或当前页面已验收。

#### Scenario: 矩阵优化方案记录已知偏离点

- **WHEN** 当前实现与目标消费规格不一致
- **THEN** 矩阵 MUST 在优化方案列记录偏离处理建议
- **AND** 优化方案 SHOULD 区分补齐目标规格字段、改用目标规格、移除原图 fallback、使用安全占位、拆分普通展示与预览场景
- **AND** 本规范 Change MUST NOT 直接修复 Web、小程序、后端、API、数据库或对象存储实现偏离
- **AND** 需要实现修正时 MUST 通过后续独立 REQ、BUG 或 OpenSpec Change 处理。

