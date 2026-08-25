## MODIFIED Requirements

### Requirement: 证书详情分享

小程序证书详情页 SHALL 支持微信原生分享或等价分享能力，并保证分享路径可直达同一张证书详情。图片证书分享图 SHALL 优先使用 `display_url` 或等价展示图，缺失时使用 `thumbnail_url` 或安全占位；PDF/文档证书 SHALL 使用稳定占位或品牌兜底图，不得伪造图片展示图。

#### Scenario: 分享证书详情

- **WHEN** 用户通过微信原生分享能力分享证书详情页
- **THEN** 小程序 SHALL 提供微信原生分享数据或等价分享能力
- **AND** 分享标题 SHALL 包含证书名称和品牌名称
- **AND** 分享路径 SHALL 携带 `certificateId` 和来源参数
- **AND** 图片证书分享图 SHALL 优先使用证书主图 `display_url`、`thumbnail_url` 或稳定占位
- **AND** PDF 或文档证书分享图 SHALL 使用稳定占位或品牌兜底图
- **AND** 页面 SHALL NOT 提供底部固定“分享证书”按钮
- **AND** 分享内容 SHALL NOT 包含内部备注、后台状态、不可公开字段、原始 object key 或未授权素材地址。

#### Scenario: 证书分享图四联证据

- **WHEN** 团队验收证书详情分享图
- **THEN** 验收 SHALL 记录图片证书 `display_url`、`thumbnail_url` 或占位图的 key、object、URL 和 render 四联证据
- **AND** 小程序 DevTools、真机或体验版 evidence SHALL 覆盖 AppData 分享图字段、页面渲染、URL 类型、HTTP 状态或 N/A 原因
- **AND** 证书详情分享图 SHALL NOT 退回原图作为默认普通展示通过证据。
