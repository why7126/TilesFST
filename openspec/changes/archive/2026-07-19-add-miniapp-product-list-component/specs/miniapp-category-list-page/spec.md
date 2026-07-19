## ADDED Requirements

### Requirement: 分类商品列表承接
分类页 SHALL 将二级分类商品浏览交由小程序商品列表页承接，分类页自身不实现商品列表、筛选或排序。

#### Scenario: 二级分类进入商品列表页
- **WHEN** 用户点击二级分类卡片
- **THEN** 小程序 SHALL 跳转到 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}` 或等价商品列表页
- **AND** 商品列表页 SHALL 负责加载该分类下公开 SKU、筛选、排序、分页和状态展示。

#### Scenario: 分类页不重复商品列表能力
- **WHEN** 团队验收分类页与商品列表页边界
- **THEN** 分类页 SHALL NOT 实现商品卡片、价格、商品分页、商品筛选、商品排序或商品列表埋点
- **AND** 分类页 SHALL 只负责分类结构展示、分类切换和二级分类跳转。
