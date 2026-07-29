---
change_id: add-miniapp-certificate-detail-page
purpose: 小程序证书详情页实现与设备证据记录
created_at: 2026-07-29 08:49:47
updated_at: 2026-07-29 08:49:47
---

# Evidence

## Static / Automated

| target | page_path | source | status | conclusion |
|---|---|---|---|---|
| add-miniapp-certificate-detail-page | pages/certificate-detail/index?certificateId=20 | pytest | passed | 静态测试覆盖路由注册、详情接口调用、列表/品牌入口跳转、分享、品牌入口、媒体预览、禁止范围外能力。 |
| add-miniapp-certificate-detail-page | /api/v1/miniapp/certificates/20 | pytest | passed | 后端测试覆盖详情成功、隐藏/软删除/停用品牌过滤、旧单文件兼容、多图主图排序和安全字段过滤。 |
| add-miniapp-certificate-detail-page | src/web/openapi.json / generated.ts | generate-openapi-client.sh | passed | OpenAPI 与 Orval generated 已同步新增公开证书详情接口与 schema。 |

## Device Matrix

| target | page_path | entry | viewport | source | status | artifact_ref | conclusion | remaining_risk |
|---|---|---|---|---|---|---|---|---|
| add-miniapp-certificate-detail-page | pages/certificate-detail/index?certificateId=20 | list_to_detail | 320pt | devtools | blocked | manual-summary | 当前执行环境未提供微信 DevTools 可视化会话，无法生成截图；静态布局已覆盖无横向滚动、底部安全区和自定义导航接入。 | 需后续在微信 DevTools 320pt 补正常、加载、错误、无图/PDF、分享直达截图。 |
| add-miniapp-certificate-detail-page | pages/certificate-detail/index?certificateId=20 | list_to_detail | 375pt | devtools | blocked | manual-summary | 当前执行环境未提供微信 DevTools 可视化会话，无法生成截图；静态布局已覆盖无横向滚动、底部安全区和自定义导航接入。 | 需后续在微信 DevTools 375pt 补正常、加载、错误、无图/PDF、分享直达截图。 |
| add-miniapp-certificate-detail-page | pages/certificate-detail/index?certificateId=20 | share_direct | 430pt | devtools | blocked | manual-summary | 当前执行环境未提供微信 DevTools 可视化会话，无法生成截图；分享路径和返回兜底已由静态契约覆盖。 | 需后续在微信 DevTools 430pt 补正常、加载、错误、无图/PDF、分享直达截图。 |
| add-miniapp-certificate-detail-page | pages/certificate-detail/index?certificateId=20 | share_direct | device | real_device | follow_up | manual-summary | 当前执行环境无真机连接，未报告真机通过。 | 需发布体验版或连接真机后补状态栏、胶囊 reserve、返回兜底和内容 offset 证据。 |

## Miniapp Custom Navigation

```yaml
target: add-miniapp-certificate-detail-page
page_path: pages/certificate-detail/index?certificateId=20
entry: list_to_detail | brand_detail | share_direct
source: static_test
status: passed
conclusion:
  status_bar: static_pass
  capsule_reserve: static_pass
  back_fallback: static_pass
  content_offset: static_pass
remaining_risk: DevTools and real-device screenshots are blocked/follow_up in this execution environment.
```
