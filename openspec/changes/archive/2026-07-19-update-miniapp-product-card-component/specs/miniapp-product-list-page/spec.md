## MODIFIED Requirements

### Requirement: 商品卡片
商品列表页 SHALL 使用统一商品卡片组件展示用户选砖所需的公开 SKU 信息，并支持进入 SKU 详情页；商品卡片组件 SHALL 只负责单个 SKU 的展示、触控、跳转和卡片级异常，列表容器 SHALL 负责查询、筛选、排序、分页、加载态和空状态。

#### Scenario: 商品卡片字段
- **WHEN** 商品列表接口返回 SKU 数据
- **THEN** 商品卡片 SHALL 展示主图、SKU 名称、品牌、规格和参考价格
- **AND** 商品卡片 MAY 展示分类名称、适用空间、主色系、材质、工艺、风格或运营标签等辅助信息
- **AND** 辅助标签 SHALL 最多展示 3 个，选择优先级 SHALL 为规格、材质、工艺、风格
- **AND** SKU 名称 SHALL 最多展示两行，超出 SHALL 省略
- **AND** 辅助信息 SHALL NOT 挤压 SKU 名称、主图、品牌、规格或参考价格。

#### Scenario: 字段缺失兜底
- **WHEN** SKU 名称、品牌、规格或参考价格缺失
- **THEN** 商品卡片 SHALL 展示统一兜底文案
- **AND** 商品卡片 SHALL NOT 展示空字符串、`null`、`undefined`、接口字段名或错误金额
- **AND** 参考价格缺失、非正或为旧无价文案时 SHALL 展示“暂无”。

#### Scenario: 图片稳定展示
- **WHEN** 商品主图加载中或加载完成
- **THEN** 商品图片区域 SHALL 使用稳定比例容器
- **AND** 加载前后 SHALL NOT 导致列表明显跳动
- **AND** 商品卡片在 320px 小屏宽度下 SHALL 保持文字可读。

#### Scenario: 图片加载失败
- **WHEN** 商品主图缺失或加载失败
- **THEN** 商品卡片 SHALL 展示统一深色占位图或占位背景
- **AND** 页面 SHALL NOT 展示破图图标
- **AND** 其他商品信息 SHALL 保持可浏览
- **AND** 单张卡片图片失败 SHALL NOT 影响同一列表中其他商品卡片渲染。

#### Scenario: 商品卡片进入详情
- **WHEN** 用户点击商品卡片任意主要区域
- **THEN** 小程序 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 小程序 SHOULD 携带 `sourcePage`、`sourceModule`、`categoryId`、`brandId`、`keyword`、`listContext`、`index` 或 `requestId` 中可用的来源上下文
- **AND** 点击期间 SHALL 提供小程序触控反馈
- **AND** 连续点击 SHALL NOT 重复打开多个详情页
- **AND** 页面 SHALL 保留返回能力。

#### Scenario: 商品不可查看
- **WHEN** SKU 缺少 `skuId`、已下架或不可公开查看
- **THEN** 商品卡片 SHALL 阻止详情跳转
- **AND** 商品卡片 SHALL 展示“暂不可查看”或等价不可用状态
- **AND** 用户点击不可用卡片时 SHALL 获得可理解提示或等价反馈。

#### Scenario: 商品卡片埋点
- **WHEN** 商品卡片曝光、点击、图片失败或不可用点击发生
- **THEN** 小程序 SHOULD 记录 `product_card_exposure`、`product_card_click`、`product_card_image_failed` 或 `product_card_unavailable_click` 等事件
- **AND** 事件参数 SHOULD 包含 `skuId`、`skuCode`、`sourcePage`、`sourceModule`、`listContext`、`index`、`categoryId`、`brandId`、`keyword` 和 `requestId` 中可用字段。

#### Scenario: 卡片不提供交易操作
- **WHEN** 团队验收商品列表卡片
- **THEN** 商品卡片 SHALL NOT 展示收藏、分享、加入询价、购物车、立即购买、在线下单或联系商家快捷按钮。
