## MODIFIED Requirements

### Requirement: SKU 收藏与分享

SKU 详情页 SHALL 支持 SKU 粒度收藏、取消收藏和微信原生分享。公开分享文案 SHALL 使用品牌名称与商品名称，不展示 SKU 编码。SKU 详情页底部收藏按钮 SHALL 保持次级操作层级，在紧凑 actionbar 中通过心形图标状态、颜色和反馈表达收藏状态，不再展示“收藏 / 已收藏”可见第二行文字。

#### Scenario: 收藏和取消收藏成功

- **WHEN** 用户点击收藏或取消收藏当前 SKU 且请求成功
- **THEN** 页面 SHALL 更新按钮状态
- **AND** 页面 SHALL 展示成功 Toast
- **AND** 收藏页或等价收藏数据 SHALL 与当前 SKU 收藏事实保持一致。

#### Scenario: 收藏失败回滚

- **WHEN** 收藏或取消收藏请求失败、超时或授权失败
- **THEN** 页面 SHALL 回滚到请求前状态
- **AND** 页面 SHALL 展示可理解失败提示
- **AND** 失败 SHALL NOT 阻断用户继续浏览详情。

#### Scenario: 收藏接口幂等

- **WHEN** 客户端重复提交收藏或取消收藏请求
- **THEN** 后端 SHALL 返回与目标状态一致的结果
- **AND** 不得产生重复收藏记录或错误取消状态。

#### Scenario: 分享 SKU

- **WHEN** 用户点击 SKU 详情页分享入口
- **THEN** 小程序 SHALL 调起微信原生分享或等价分享能力
- **AND** 分享标题 SHALL 包含商品名称和品牌名称
- **AND** 分享卡片 SHALL 包含主图、商品名称、品牌和参考价格
- **AND** 分享路径 SHALL 携带 `skuId` 和来源参数
- **AND** 分享标题、摘要和卡片展示 SHALL NOT 拼接 SKU 编码。

#### Scenario: 商品详情页紧凑收藏按钮

- **WHEN** 用户查看 SKU 详情页底部固定操作栏
- **THEN** 收藏按钮 SHALL NOT 展示“收藏 / 已收藏”可见第二行文字
- **AND** 收藏按钮 SHALL 通过心形图标形态、颜色或等价视觉状态区分未收藏和已收藏
- **AND** 收藏按钮 SHALL 保留不小于 44x44 pt 或小程序等效有效触控区域
- **AND** 收藏请求中、成功、取消成功和失败回滚 SHALL NOT 导致底部操作栏高度跳变
- **AND** “分享给客户”按钮 SHALL 继续保持主视觉权重、稳定点击热区和微信 `open-type="share"` 能力。

### Requirement: SKU 详情页视觉与可用性

SKU 详情页 SHALL 延续微信小程序首页 v6 深色企业轻奢风，并在主流小程序视口内保持可用。顶部媒体区 SHALL 比旧固定 `680rpx` 更适合瓷砖详情展示，同时 SHALL 保持首屏商品名称或关键商品信息可见。底部 actionbar SHALL 在安全区适配和触控热区约束下保持紧凑，并与返回首页悬浮按钮 offset 协同，避免遮挡底部主操作或页面内容。

#### Scenario: 深色视觉和大媒体区

- **WHEN** 用户查看 SKU 详情页
- **THEN** 页面 SHALL 使用与小程序首页 v6 一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 顶部媒体区 SHALL 采用大图布局
- **AND** 媒体区高度 SHALL 基于视口宽度、安全区和上限约束计算，避免固定 `680rpx` 无法适配主流设备
- **AND** 首屏 SHALL 露出商品名称或关键商品信息
- **AND** 页面 SHALL NOT 使用电商红主按钮、纯白大背景或购物导向视觉。

#### Scenario: 移动视口可用

- **WHEN** 团队在 320 到 430px 逻辑宽度和常见底部安全区验收页面
- **THEN** 页面 SHALL 无横向滚动、内容重叠、按钮遮挡或关键文字截断
- **AND** 主要点击目标 SHALL 不小于 44x44px 或小程序等效尺寸
- **AND** 顶部媒体区变高后 SHALL NOT 将商品名称或关键商品信息完全挤出首屏。

#### Scenario: 底部 actionbar 与返回首页悬浮按钮协同

- **WHEN** SKU 详情页底部 actionbar 压缩后展示
- **THEN** 页面底部内容留白 SHALL 与新的 actionbar 高度匹配，避免固定栏遮挡内容或留下明显过大空白
- **AND** 返回首页悬浮按钮在 actionbar 场景下 SHALL 避开压缩后的底部栏和系统安全区
- **AND** 返回首页悬浮按钮 SHALL NOT 遮挡收藏按钮、分享按钮、推荐商品卡片或关键商品信息
- **AND** 小程序视觉验收 SHALL 覆盖 320 pt、375 pt、430 pt 视口的底部操作栏、收藏图标状态、分享按钮和返回首页悬浮按钮位置。
