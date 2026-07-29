## MODIFIED Requirements

### Requirement: SKU 详情信息展示

SKU 详情页 SHALL 完整展示用户选砖所需的品牌、商品名称、价格、参数、类目和备注信息。SKU 编码 SHALL 作为系统内部识别字段，不在小程序/店主端详情页标题、参数区或推荐卡中展示。备注说明 SHALL 使用 SKU 详情接口返回的公开备注字段端到端展示，非空时可见，空值时按安全空态处理。

#### Scenario: 展示 SKU 核心字段

- **WHEN** SKU 详情加载成功
- **THEN** 页面 SHALL 展示品牌名称、商品名称、参考价格、计价单位、规格、表面工艺、主色系、完整类目路径和备注说明
- **AND** 备注说明非空时 SHALL 在详情信息区或等价公开信息区展示，内容 SHALL 与 SKU 详情接口返回的公开备注说明字段一致
- **AND** 品牌信息 SHALL 位于商品名称上方并提供品牌入口
- **AND** 页面 SHALL NOT 展示 SKU 编码、`sku_code` 字段名或“SKU 编码：xxx”参数行。

#### Scenario: 空字段安全展示

- **WHEN** 表面工艺、主色系、备注或可选媒体字段为空
- **THEN** 页面 SHALL 按字段规则展示 “—”、隐藏对应模块或展示安全占位
- **AND** 备注说明为空时 SHALL NOT 展示 `null`、`undefined`、接口字段名、异常空白卡片或布局错位
- **AND** 页面 SHALL NOT 展示 `null`、`undefined`、接口字段名或空白异常卡片
- **AND** 商品名称缺失 SHALL 作为异常数据处理，不得用 SKU 编码作为正常公开兜底。

#### Scenario: 备注说明公开字段边界

- **WHEN** SKU 详情接口和小程序页面处理备注说明
- **THEN** 小程序 SHALL 只展示允许公开的商品/SKU 备注说明字段
- **AND** 响应和页面 SHALL NOT 暴露后台内部备注、库存管理、内部审核信息、原始 object key、Authorization header、Cookie 或敏感配置
- **AND** 小程序端字段映射 SHALL 与接口返回字段保持一致，避免接口已返回但页面未绑定展示。

### Requirement: SKU 详情页接口与测试同步

SKU 详情页涉及的 API、数据库、OpenAPI、Orval、文档和测试 SHALL 保持同步。

#### Scenario: 测试覆盖

- **WHEN** SKU 详情页实现完成或生产视频播放缺陷修复完成
- **THEN** 后端测试 SHALL 覆盖公开字段过滤、详情成功、不可公开状态、收藏幂等、推荐排除和安全媒体 URL
- **AND** 小程序或静态测试 SHALL 覆盖页面入口、媒体状态、收藏分享交互、异常状态和范围外能力未出现
- **AND** 小程序测试 SHALL 覆盖备注说明非空展示和空备注说明安全空态
- **AND** 若 SKU 详情接口为修复备注说明新增或调整字段，后端测试、OpenAPI、Orval 和 API 文档 SHALL 同步更新
- **AND** 后端测试 SHALL 覆盖 `tile_videos.object_key` 与 `tile_videos.file_name` 语义不同的场景，确保视频 `media[].url` 使用对象 key 生成安全媒体 URL
- **AND** 后端测试 SHALL 覆盖视频 `/media/{object_key}` Range/206 响应
- **AND** 小程序测试 SHALL 覆盖视频封面或兜底 poster 展示
- **AND** 生产修复验收 SHALL 附实际 SKU 接口、实际 `/media/{object_key}` 与微信真机播放证据。
