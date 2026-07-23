---
bug_id: BUG-0072-miniapp-usage-events-bad-request
title: 微信小程序 usage-events 上报接口频繁返回 400
status: done
severity: high
created_at: 2026-07-21 14:41:14
updated_at: 2026-07-22 08:47:45
related_requirement: REQ-0024-product-usage-logging
related_change: fix-miniapp-usage-events-contract-drift
---

# 回归验收

## AC-001 小程序当前埋点事件必须通过后端契约校验

- [ ] 梳理 `src/miniapp/**` 当前所有 `track()` 事件，包括动态事件名分支。
- [ ] 每个合法小程序事件在后端事件字典中存在定义。
- [ ] 每个定义包含明确的 `category`、`required`、`forbidden`。
- [ ] 后端测试覆盖小程序当前全部合法事件，合法 payload 返回 200。

## AC-002 收藏页埋点不再返回 400

- [ ] 进入收藏页触发 `favorite_list_page_view`，`POST /api/v1/usage-events` 返回成功。
- [ ] 收藏页读取失败触发 `favorite_list_load_failed`，后端返回成功或按明确字段原因拒绝。
- [ ] 空态引导触发 `favorite_list_empty_action_click`，后端返回成功。
- [ ] 点击收藏项触发 `favorite_list_item_click`，后端返回成功。
- [ ] 取消收藏触发 `favorite_list_remove`，后端返回成功。

## AC-003 品牌详情页埋点不再返回未知事件

- [ ] `brand_detail_view` 返回成功。
- [ ] `brand_detail_tab_click` 返回成功。
- [ ] `brand_products_load` 返回成功。
- [ ] `brand_products_load_more` 返回成功。
- [ ] `brand_products_load_failed` 返回成功或按明确字段原因拒绝。
- [ ] `brand_certificates_load` 返回成功。
- [ ] `brand_certificates_load_failed` 返回成功或按明确字段原因拒绝。
- [ ] `brand_certificate_click` 返回成功。

## AC-004 商品 / 品牌卡片组件埋点不再返回未知事件

- [ ] `product_card_exposure` 返回成功。
- [ ] `product_card_click` 返回成功。
- [ ] `product_card_unavailable_click` 返回成功。
- [ ] `product_card_image_failed` 返回成功或按明确字段原因拒绝。
- [ ] `brand_card_click` 返回成功。
- [ ] `brand_card_unavailable_click` 返回成功。
- [ ] `brand_card_image_failed` 返回成功或按明确字段原因拒绝。

## AC-005 已注册事件的必填字段保持一致

- [ ] `product_list_page_view` 的小程序 payload 包含 `pageSize`、`requestId`、`sort` 等后端必填字段。
- [ ] `sku_detail_view` 的小程序 payload 包含 `sku_id`、`page_path`、`client_type`。
- [ ] `sku_load_error` 的小程序 payload 包含 `sku_id`、`page_path`、`client_type`、`error_code`、`stage`。
- [ ] 字段命名在小程序端和后端字典中保持一致，不混用 `skuId` / `sku_id`、`requestId` / `request_id` 等未经约定的字段。

## AC-006 安全校验不得放宽

- [ ] 未知事件仍返回 400，不允许静默写入。
- [ ] 包含 `authorization`、`cookie`、`raw_payload`、`raw_object_key`、`object_key`、`phone` 等禁止字段的事件仍返回 400。
- [ ] 修复不得记录 Authorization header、Cookie、`.env` 内容、本机路径、对象存储内部 key、后台备注或原始敏感 payload。

## AC-007 统计写入完整性

- [ ] 合法小程序事件成功写入 `usage_events`。
- [ ] 写入记录包含正确的 `client_type=wechat_miniapp`。
- [ ] 写入记录的 `event_category`、`page_path`、`summary` 可用于日志审计页查询和排查。
- [ ] 对热销、访问、收藏、品牌入口等依赖行为事件的统计，不再因 400 缺失关键事件。

## AC-008 回归测试与防漂移

- [ ] 增加后端 pytest，覆盖本缺陷涉及的全部小程序事件。
- [ ] 增加一个事件字典一致性测试或脚本，发现小程序新增 `track()` 字面量事件未注册时失败。
- [ ] 对动态事件名调用点建立明确测试样例，避免只覆盖字面量事件。
- [ ] 回归测试必须包含“未知事件仍拒绝”和“禁止字段仍拒绝”的负向用例。

## AC-009 小程序调试体验

- [ ] 在微信开发者工具 macOS / mp 2.01.2510290 / lib 3.16.2 环境下复测。
- [ ] 关键页面操作后，Console / Network 不再大量出现 `POST /api/v1/usage-events 400`。
- [ ] 埋点失败仍不得阻断页面浏览、跳转、收藏、分享或证书预览等主流程。
