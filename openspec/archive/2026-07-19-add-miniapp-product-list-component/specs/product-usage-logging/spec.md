## ADDED Requirements

### Requirement: 小程序商品列表行为事件
系统 SHALL 记录小程序商品列表浏览、曝光、点击、筛选、排序、刷新、加载更多和失败事件，用于分析商品发现效率。

#### Scenario: 商品列表页浏览
- **WHEN** 用户进入商品列表页
- **THEN** 系统 SHALL 记录 `product_list_page_view`
- **AND** 事件 SHALL 包含 sourcePage、categoryId、brandId、keyword、sort、filterSnapshot、pageSize 和 requestId 中适用字段。

#### Scenario: 商品曝光与点击
- **WHEN** 商品卡片曝光或用户点击商品卡片
- **THEN** 系统 SHALL 记录 `product_list_item_exposure` 或 `product_list_item_click`
- **AND** 事件 SHALL 包含 skuId、sourcePage、列表上下文、位置索引和 requestId 中适用字段。

#### Scenario: 筛选和排序事件
- **WHEN** 用户打开筛选、应用筛选或切换排序
- **THEN** 系统 SHALL 记录 `product_list_filter_open`、`product_list_filter_apply` 或 `product_list_sort_change`
- **AND** 事件 SHALL 包含 filterSnapshot、sort、resultCount 和 requestId 中适用字段。

#### Scenario: 刷新与加载更多事件
- **WHEN** 用户触发下拉刷新、上拉加载更多或加载失败
- **THEN** 系统 SHALL 记录 `product_list_refresh`、`product_list_load_more` 或 `product_list_load_failed`
- **AND** 事件 SHALL 包含 page、pageSize、resultCount、errorCode 和 requestId 中适用字段。

#### Scenario: 商品列表事件敏感信息过滤
- **WHEN** 系统记录商品列表行为事件
- **THEN** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、原始 object key、内部备注或不必要个人敏感信息。
