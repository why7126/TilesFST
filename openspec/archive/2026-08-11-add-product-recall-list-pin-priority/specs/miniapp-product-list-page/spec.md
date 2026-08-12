## ADDED Requirements

### Requirement: 商品列表召回置顶排序

小程序普通商品列表公开查询 MUST 支持少量召回 SKU 置顶排序。普通商品列表包括分类商品、品牌商品、普通关键词商品和非榜单推荐入口；首页无筛选全部产品瀑布流 MUST 保持既有首页排序，不应用本能力。后端 MUST 先应用公开条件和当前请求筛选，再计算召回置顶资格，并在分页前对完整结果集排序。每次请求默认最多 4 个生效召回 SKU 进入置顶区；超过上限时按 `recall_pin_sort_order` 升序、既有排序兜底和 SKU ID 升序裁定。小程序端 MUST 按接口返回顺序展示，不得做跨页本地重排，也不得展示召回置顶 UI 标识。

#### Scenario: 普通商品列表置顶排序

- **GIVEN** 当前普通商品列表存在多个可公开 SKU
- **AND** 其中部分 SKU 的 `recall_pin_sort_order` 小于 `9999` 且当前时间处于有效期内
- **WHEN** 小程序请求 `/api/v1/miniapp/products`
- **THEN** 生效召回 SKU MUST 排在非召回 SKU 之前
- **AND** 生效召回 SKU MUST 按 `recall_pin_sort_order` 升序排列
- **AND** 非召回 SKU MUST 保持该入口既有排序规则。

#### Scenario: 筛选条件先于置顶资格

- **GIVEN** 某 SKU 配置了生效召回置顶
- **WHEN** 该 SKU 不满足当前关键词、品牌、类目、规格、价格区间或公开展示条件
- **THEN** 系统 MUST 排除该 SKU
- **AND** MUST NOT 将其强行插入列表顶部。

#### Scenario: 置顶上限裁定

- **GIVEN** 当前请求内有 5 个或更多生效召回候选 SKU
- **WHEN** 后端计算商品列表排序
- **THEN** 仅排序值最靠前的 4 个 SKU MUST 进入置顶区
- **AND** 其余召回候选 MUST 按普通商品排序参与结果。

#### Scenario: 分页前排序稳定

- **WHEN** 用户刷新商品列表或加载更多
- **THEN** 后端 MUST 在分页前完成召回置顶排序
- **AND** 多页合并后 MUST NOT 出现重复、漏项或已加载商品顺序跳动。

#### Scenario: 榜单和价格排序不受影响

- **WHEN** 商品列表请求为 `section=new`、`section=hot`、价格升序或价格降序
- **THEN** 后端 MUST 跳过召回置顶排序
- **AND** 结果 MUST 保持新品榜、热销榜或价格排序原有语义。

#### Scenario: 小程序无置顶标识

- **WHEN** 小程序展示参与召回置顶的 SKU
- **THEN** 商品卡片 MUST NOT 展示“置顶”“推荐”“召回”等新增角标、标签或说明文案
- **AND** 页面 MUST NOT 新增排序说明、筛选控件或列表控件。
