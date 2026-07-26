## ADDED Requirements

### Requirement: SKU 弹窗表单字段规则修复

Web 客户端 MUST 修复 `/admin/tile-skus` 新增/编辑 SKU 弹窗（`TileSkuFormModal`）的表单字段规则，对齐 UAT 产品决策（[BUG-0012](issues/bugs/archive/BUG-0012-tile-sku-modal-form-field-rules/)）：**表面工艺非必填**、**参考价格（元）必填且新建默认 0**。修复 MUST 同步前后端校验，且 MUST NOT 回退 BUG-0011 弹窗滚动布局或 BUG-0009 列表 UI。

#### Scenario: 表面工艺非必填

- **WHEN** 用户打开新增或编辑 SKU 弹窗
- **THEN** 「表面工艺」Label MUST NOT 显示必填星号
- **AND** 留空表面工艺、填齐其它必填项后点击「创建 SKU」或「保存」 MUST 成功提交

#### Scenario: 参考价格必填且新建默认零

- **WHEN** 用户打开「新增 SKU」弹窗
- **THEN** 「参考价格（元）」输入框 MUST 默认值为 `0`
- **AND** Label MUST 显示必填星号
- **AND** Label 文案 MUST 仍为「参考价格（元）」

#### Scenario: 参考价格空值被拦截

- **WHEN** 用户清空参考价格并尝试创建或保存
- **THEN** 前端 MUST 展示校验错误且不关闭弹窗
- **AND** MUST NOT 向 API 发送 `reference_price: null`

#### Scenario: 参考价格零元列表展示

- **WHEN** SKU 保存后 `reference_price` 为 `0`
- **THEN** 列表「参考价格」列 MUST 显示 `¥ 0.00`
- **AND** MUST NOT 显示「—」

#### Scenario: 弹窗布局与滚动不回退

- **WHEN** 修复完成后在矮视口打开 SKU 弹窗
- **THEN** 880px 宽度、主体可滚动、头尾固定 MUST 仍满足 BUG-0011 验收

#### Scenario: Orval 类型同步

- **WHEN** 后端 OpenAPI 更新 reference_price 必填语义
- **THEN** 团队 MUST 运行 `./scripts/generate-openapi-client.sh` 并提交生成客户端
