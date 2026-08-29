## ADDED Requirements

### Requirement: 收藏列表搜索路径
收藏列表页 SHALL 提供当前收藏范围搜索策略，帮助用户在已收藏对象中快速定位商品。收藏列表搜索 SHALL 保持收藏卡片布局，不跳完整搜索结果页，且 SHALL NOT 把当前收藏范围无结果误表达为全站无结果。

#### Scenario: 收藏范围搜索
- **WHEN** 收藏列表页支持在当前收藏范围内输入关键词
- **THEN** 页面 SHALL 仅过滤当前用户可见收藏对象
- **AND** 搜索空态 SHALL 明确说明当前为收藏范围无结果
- **AND** 页面 SHALL 提供清空关键词或继续调整关键词的路径
- **AND** 页面 SHALL NOT 展示显著的“去全局搜索调整”主按钮
- **AND** 未登录状态 SHALL NOT 被误展示为收藏搜索无结果。

#### Scenario: 收藏页不进入完整搜索
- **WHEN** 用户在收藏列表页提交或清空关键词
- **THEN** 小程序 SHALL 在当前收藏列表页更新结果
- **AND** 页面 SHALL 保持收藏卡片点击、取消收藏和失效对象降级行为
- **AND** 页面 SHALL NOT 因收藏搜索提交跳转 `/pages/search/index`。
