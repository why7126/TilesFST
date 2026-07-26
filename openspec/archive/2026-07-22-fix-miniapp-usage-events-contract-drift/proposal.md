## Why

`BUG-0072-miniapp-usage-events-bad-request` 已评审通过。微信小程序运行时频繁请求 `POST /api/v1/usage-events` 并返回 400。探索与缺陷完善阶段已确认：小程序当前存在多个合法业务埋点事件，但后端 `EVENT_DEFINITIONS` 未覆盖这些事件名，导致后端按事件字典白名单返回 `40001 未知埋点事件`；部分已注册事件也存在必填字段命名或字段缺失风险。

现行 `product-usage-logging` 规格已经要求 usage event 必须按人工定义事件字典采集，并要求未知事件和禁止属性被拒绝；同时收藏页、品牌详情页和品牌卡片规格已经声明对应小程序行为应记录埋点。缺口在于产品使用日志能力没有明确要求后端事件字典持续覆盖这些后续小程序页面和组件新增事件，也缺少防止小程序 `track()` 事件与后端字典漂移的测试门禁。

## What Changes

- 修改 `product-usage-logging` 能力：明确小程序 usage event 字典必须覆盖当前小程序合法事件，包括收藏页、品牌详情页、商品卡片和品牌卡片组件事件。
- 要求后端为这些事件定义明确的 `category`、`required` 和 `forbidden` 属性，并保持统一响应结构。
- 要求小程序 payload 与后端 required 字段保持一致，必要时统一字段命名。
- 要求增加回归测试和防漂移测试，覆盖小程序当前全部 `track()` 字面量事件和动态事件名样例。
- 明确未知事件、禁止属性和敏感信息拒绝边界不得放宽。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `product-usage-logging`: 修正微信小程序 usage event 字典覆盖、字段契约和防漂移测试要求。

## Impact

- **api:** 影响 `POST /api/v1/usage-events` 的事件字典覆盖范围；不新增接口路径，不改变统一响应结构。若实现变更 OpenAPI Schema 或错误响应细节，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。
- **backend:** 预计补齐 `src/backend/app/services/log_service.py` 中小程序事件定义，并补充 pytest 覆盖合法事件成功、未知事件拒绝、禁止字段拒绝。
- **miniapp:** 预计梳理 `src/miniapp/**` 中 `track()` 调用，统一 payload 字段名和必填字段；埋点失败仍不得阻断页面浏览、跳转、收藏、分享或证书预览。
- **database:** 不涉及表结构或迁移；继续写入既有 `usage_events` 表。
- **web/admin:** 不涉及页面功能；管理端日志审计可查询更完整的小程序 usage event。
- **tests:** 必须补充后端事件字典测试和小程序事件防漂移测试；必要时补充小程序静态校验或构建检查。

## Rollback Plan

如修复导致合法小程序事件被错误接受敏感字段、日志审计数据污染或高频事件写入异常，可回滚本 Change 的后端事件字典和小程序 payload 调整，同时保留未知事件与禁止字段拒绝逻辑。回滚后 `BUG-0072` 仍保持未修复，不得以关闭未知事件校验作为长期规避方案。
