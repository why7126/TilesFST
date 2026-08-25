## ADDED Requirements

### Requirement: 证书详情页品牌入口复用品牌卡片

小程序证书详情页 SHALL 使用既有品牌卡片组件展示所属品牌入口。证书详情页 SHALL 将证书详情响应中的品牌数据、来源上下文和证书上下文传入品牌卡片组件；品牌卡片组件 SHALL 继续负责 Logo 展示、名称展示、入口提示、不可用态、点击跳转和埋点触发。

#### Scenario: 证书详情页传入品牌卡片数据

- **WHEN** 小程序证书详情页渲染所属品牌入口
- **THEN** 页面 SHALL 使用品牌卡片组件
- **AND** 页面 SHALL 向组件传入 `brandId`、`brandName`、`brand_logo_thumbnail_url`、品牌入口参数和来源上下文
- **AND** 页面 SHALL NOT 保留页面私有品牌入口 DOM、模板结构或独立点击逻辑。

#### Scenario: 证书详情页品牌入口点击跳转

- **WHEN** 用户点击证书详情页可用品牌卡片
- **THEN** 小程序 SHALL 跳转到对应品牌详情页或既定品牌入口
- **AND** 跳转上下文 SHALL 包含可用的品牌标识和 `sourcePage=certificate_detail` 或等价来源参数
- **AND** 埋点失败 SHALL NOT 阻断品牌跳转。

#### Scenario: 证书详情页品牌入口不可用

- **WHEN** 证书详情页品牌数据缺失、品牌不可公开或品牌入口参数不可用
- **THEN** 品牌卡片 SHALL 使用统一不可用态或页面 SHALL 不展示品牌入口
- **AND** 小程序 SHALL 阻止无效跳转
- **AND** 证书详情页主体信息 SHALL 继续可浏览。

#### Scenario: 证书详情页品牌卡片移动端验收

- **WHEN** 团队验收证书详情页品牌入口
- **THEN** 验收 SHALL 覆盖 320 pt、375 pt 和 430 pt 逻辑宽度
- **AND** 正常态、缩略图缺失态、图片失败态、长品牌名态和不可用态 SHALL 确认无重叠、无遮挡、无横向溢出
- **AND** 证据 SHALL 说明证书详情页与其他品牌卡片调用方的一致性结论。

