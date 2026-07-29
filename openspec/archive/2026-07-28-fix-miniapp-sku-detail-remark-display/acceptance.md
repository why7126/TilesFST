---
change_id: fix-miniapp-sku-detail-remark-display
status: in_progress
created_at: 2026-07-28 22:44:51
updated_at: 2026-07-29 00:09:26
---

# Acceptance

## AC-001 备注说明非空时展示

给定某个 SKU 已维护公开备注说明，  
当用户打开微信小程序 SKU 详情页，  
则页面必须展示该备注说明，且内容与接口返回值一致。

## AC-002 空备注说明安全处理

给定某个 SKU 备注说明为空，  
当用户打开微信小程序 SKU 详情页，  
则页面不得展示 `null`、`undefined`、接口字段名、异常空白卡片或布局错位。

## AC-003 公开字段边界

给定 SKU 同时存在公开备注和后台内部备注或其他内部字段，  
当小程序请求详情数据并渲染页面，  
则页面只能展示允许公开的备注说明，不得暴露内部备注、库存管理、原始 object key、Authorization header、Cookie 或敏感配置。

## AC-004 非回归

修复后 SKU 详情页的媒体浏览、品牌入口、收藏、分享、异常状态和安全媒体 URL 能力不得回归。

## 验收进展

- 已通过 `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` 覆盖 AC-001、AC-002、AC-003 与主要详情页非回归场景。
- 待补充微信开发者工具或真机预览证据后，关闭手工验收项。
