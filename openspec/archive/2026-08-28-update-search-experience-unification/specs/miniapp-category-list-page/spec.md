## MODIFIED Requirements

### Requirement: 微信小程序分类列表页入口
系统 SHALL 提供微信小程序 `pages/category/index` 分类列表页，作为底部 TabBar「分类」一级频道，用于展示一级与二级瓷砖分类结构。分类页 SHALL 保持左右双栏分类浏览主体验，并 SHALL NOT 展示全局搜索入口、搜索框或等价搜索路径。用户可从分类页进入对应商品列表后，在商品列表上下文继续搜索或调整关键词。

#### Scenario: 分类 Tab 进入页面
- **WHEN** 用户点击底部 TabBar「分类」
- **THEN** 小程序 SHALL 打开 `pages/category/index`
- **AND** 页面 SHALL 展示页面标题、左右双栏分类主体、一级分类商品列表入口、二级分类卡片和底部 TabBar
- **AND** 页面 SHALL NOT 展示商品卡片、价格、收藏按钮、筛选排序栏、热门分类模块、订单、库存、新增、编辑或上下架入口
- **AND** 页面 SHALL NOT 展示全局搜索入口、搜索框或等价搜索路径。

#### Scenario: 分类页进入商品列表
- **WHEN** 用户点击一级分类商品列表入口或二级分类卡片
- **THEN** 小程序 SHALL 进入商品列表页
- **AND** 跳转参数 SHALL 携带当前分类上下文
- **AND** 商品列表页 MAY 提供当前分类范围内继续搜索或返回完整搜索页调整关键词的轻量路径。
