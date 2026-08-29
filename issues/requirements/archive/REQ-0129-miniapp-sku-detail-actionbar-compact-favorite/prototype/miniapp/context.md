---
requirement_id: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
status: pending_review
created_at: 2026-08-28 13:37:34
updated_at: 2026-08-28 13:37:34
---

# 小程序原型策略

## 目标

为商品详情页底部操作栏提供紧凑化视觉参考：收藏按钮去掉第二行文字，保留心形状态；“分享给客户”保持主按钮；返回首页悬浮按钮根据新 actionbar 高度下移或重新避让。

## 原型文件

| 文件 | 说明 |
|---|---|
| `prototype/miniapp/actionbar-compact.html` | 静态 HTML 原型，用于表达底部操作栏紧凑布局、收藏图标状态和首页悬浮按钮相对位置。 |
| `prototype/miniapp/context.md` | 原型目标、关键状态和验收说明。 |

## 状态覆盖

| 状态 | 原型表达 |
|---|---|
| 未收藏 | 空心心形，次级颜色，按钮无可见文字。 |
| 已收藏 | 实心心形，品牌强调色，按钮无可见文字。 |
| 请求中 | 保持按钮区域稳定，不能把底部栏撑高。 |
| 分享主操作 | 金色主按钮，占据主要宽度和视觉权重。 |
| 首页悬浮按钮 | 位于底部栏上方，距离随 actionbar 高度收敛，不压住推荐卡片。 |

## 验收提示

- 原型只表达布局策略，不代表最终像素值。
- 实现阶段需以小程序 WXML/WXSS 为事实源，补充 DevTools 320 pt、375 pt、430 pt 视觉证据。
- 真机不可用时，验收记录需标记 follow_up 或 blocked，不写成真机已通过。
- 本需求不改变 API、DB、请求封装和行为事件。
