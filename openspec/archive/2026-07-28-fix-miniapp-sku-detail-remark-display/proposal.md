## Why

`BUG-0086-miniapp-sku-detail-remark-not-shown` 已确认：微信小程序商品详情页未展示商品/SKU 已维护的备注说明信息，导致用户无法看到完整的商品补充说明。

正式能力 `miniapp-sku-detail-page` 已要求 SKU 详情页展示“备注说明”，因此该问题属于既有能力实现偏差。需要通过 fix Change 明确详情接口、端侧字段映射、页面展示和回归测试的修复范围，避免只在页面临时补 UI 而遗漏接口契约或空态边界。

## What Changes

- 修复小程序 SKU 详情页备注说明展示链路，确保非空备注说明可见。
- 校验 SKU 详情接口响应、端侧数据适配和页面模板使用一致字段。
- 备注说明为空时按既有空态规则隐藏、占位或安全展示，不出现 `null`、`undefined`、字段名泄露或异常空白卡片。
- 补充小程序字段映射/页面渲染测试和包含备注说明的回归样例。
- 如修复发现详情接口缺少字段，同步 API / OpenAPI / Orval / docs / 后端契约测试。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-sku-detail-page`: SKU 详情页必须端到端展示非空备注说明，并覆盖空态和回归测试。

## Impact

- 影响范围：微信小程序商品详情页、SKU 详情数据映射链路；可能涉及 miniapp SKU 详情接口响应字段。
- API：可能影响。如果后端详情接口已经返回备注说明，则不需要改 API；若未返回，必须同步 API / OpenAPI / Orval / docs / tests。
- 数据库：预计不影响；若现有商品/SKU 表已有备注说明字段，仅读取展示。
- Web/管理端：预计不影响，除非需确认管理端维护的备注字段来源。
- 小程序：影响 `src/miniapp/pages/tile-detail/` 及相关服务/模型/测试。
- Docker Compose：不影响。

## Rollback Plan

- 若修复导致详情页加载或布局异常，可回滚小程序端备注说明展示节点和字段映射改动。
- 若新增或调整接口字段导致契约异常，可回滚接口字段暴露改动并同步回滚 OpenAPI / Orval 生成物。
- 回滚后保留 `BUG-0086` 追溯记录，重新评估字段来源和空态策略。
