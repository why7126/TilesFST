## MODIFIED Requirements

### Requirement: 小程序媒体四联最佳实践

系统 SHALL 为小程序媒体性能相关需求、BUG、OpenSpec Change、Sprint 验收和发布检查提供小程序媒体四联最佳实践引用。该实践 SHALL 覆盖 `key`、`object`、`URL`、`render` 四个维度，并 SHALL 明确对象存在、`.thumb` URL 存在、接口测试通过或只读审计摘要均不能单独证明小程序媒体性能验收通过。该实践 SHALL 不替代媒体五联验收模板或媒体类 BUG 四联验收模板，而是补充小程序媒体场景的 Network evidence、真实轻量资源命中、高清展示图语义和端侧 render 证据要求。

#### Scenario: 详情页高清展示与列表缩略图区分

- **WHEN** 团队验收小程序商品详情页媒体清晰度修复
- **THEN** 验收记录 SHALL 区分详情页展示 URL、图片预览 URL、商品列表卡片 URL、推荐位 URL 和 Banner URL
- **AND** 详情页展示 URL SHALL 使用原图或详情级高清展示图
- **AND** 图片预览 URL SHALL 使用原图或等价高清 URL
- **AND** 商品列表、商品卡片、推荐位和 Banner URL SHALL 继续使用 `.thumb` 或等价轻量图片
- **AND** render evidence SHALL 覆盖清晰度、轮播高度和首屏商品信息露出。
