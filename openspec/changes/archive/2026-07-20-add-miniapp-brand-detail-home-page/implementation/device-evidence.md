---
created_at: 2026-07-20 09:12:18
updated_at: 2026-07-20 22:37:56
target: add-miniapp-brand-detail-home-page
status: passed
---

# 品牌主页/详情页设备验收记录

## 当前结论

本次 `/opsx-apply` 已完成后端接口、小程序页面、静态测试与 OpenSpec 校验；用户已在 `/opsx-archive add-miniapp-brand-detail-home-page` 过程中确认真机验收完成。当前记录以用户验收确认为归档证据，不附加本地自动截图。

## Evidence Matrix

| 页面 | 视口 / 设备 | 来源 | 状态 | 说明 |
|---|---|---|---|---|
| `pages/brand-list/index` | 真机 | real_device | passed | 用户确认品牌轮播、双列品牌卡片、自定义导航与底部 TabBar 已完成验收 |
| `pages/brand-detail/index` 商品 Tab | 真机 | real_device | passed | 用户确认品牌信息区、Tab、商品双列卡片和自定义导航已完成验收 |
| `pages/brand-detail/index` 证书 Tab | 真机 | real_device | passed | 用户确认证书卡片、Tab、自定义导航和底部区域已完成验收 |
| 品牌入口页与品牌主页 | 真机 | real_device | passed | 用户在当前归档命令中确认真机验收完成 |

## 已完成的非设备校验

- `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`
- `openspec validate add-miniapp-brand-detail-home-page --strict`
- OpenAPI 导出与 Orval 生成
