## ADDED Requirements

### Requirement: SKU 召回置顶运营配置

管理端 SKU 维护能力 MUST 支持运营配置召回置顶排序信息。系统 MUST 在 SKU 新建、编辑和详情回显中维护 `recall_pin_sort_order`、`recall_pin_starts_at`、`recall_pin_ends_at` 或等价字段。`recall_pin_sort_order` MUST 只允许正整数，默认值 MUST 为 `9999`；数值低于 `9999` 且处于有效期内时才表示该 SKU 可参与小程序普通商品列表和搜索 SKU 结果的召回置顶排序。管理端 SKU 列表 MUST 展示排序字段，但默认排序 MUST NOT 因该字段改变。

#### Scenario: 新建 SKU 默认召回排序值

- **WHEN** 管理端新建 SKU 且运营未填写召回排序值
- **THEN** 系统 MUST 将 `recall_pin_sort_order` 持久化为 `9999`
- **AND** 该 SKU MUST 按普通商品参与公开列表排序。

#### Scenario: 召回排序值正整数校验

- **WHEN** 管理端保存 SKU 时提交空值、非数字、零、负数或小数作为召回排序值
- **THEN** 系统 MUST 拒绝非法值或按空值规则归一化为 `9999`
- **AND** 非空非法值 MUST 在排序输入框下方给出红色字段级校验提示“排序值必须为正整数”
- **AND** MUST NOT 将该错误展示到弹窗顶部全局错误区
- **AND** 系统 MUST NOT 保存非正整数排序值。

#### Scenario: SKU 弹窗排序字段位置和帮助说明

- **WHEN** 管理端打开 SKU 新建或编辑弹窗
- **THEN** 召回排序字段 MUST 以“排序”作为标签
- **AND** MUST 放在“参考价格”字段之后
- **AND** MUST 标记为必填
- **AND** 标签旁 MUST 提供问号帮助图标，鼠标 hover 时说明默认值、正整数约束和数值越低越靠前。

#### Scenario: 召回置顶有效期校验

- **WHEN** 管理端保存 SKU 时提交生效开始时间晚于生效结束时间
- **THEN** 系统 MUST 拒绝保存
- **AND** 管理端 MUST 展示可理解的字段级校验提示。

#### Scenario: 召回配置保存回显

- **WHEN** 运营保存召回排序值和有效期后再次打开 SKU 详情或编辑弹窗
- **THEN** 系统 MUST 回显已保存的排序值、生效开始时间和生效结束时间
- **AND** 保存成功或失败反馈 MUST 使用既有 fixed toast，不得造成 SKU 列表或弹窗布局位移。

#### Scenario: 管理端列表排序不变

- **WHEN** 管理端请求 SKU 列表
- **THEN** 管理端 SKU 列表 MUST 在状态字段前展示“排序”字段
- **AND** 管理端 SKU 列表 MUST 继续遵循既有管理端排序规则
- **AND** MUST NOT 因 `recall_pin_sort_order` 较低而将 SKU 在管理端列表置顶
- **AND** 状态字段中的“已上架”“已下架”短标签 MUST 单行显示。
