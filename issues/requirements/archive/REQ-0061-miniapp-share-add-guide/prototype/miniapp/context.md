---
requirement_id: REQ-0061-miniapp-share-add-guide
title: 小程序添加到我的小程序引导语原型上下文
status: pending_review
created_at: 2026-07-19 23:50:36
updated_at: 2026-07-19 23:50:36
---

# 原型上下文

## 目标

表达用户进入微信小程序首页后，右上角微信原生胶囊附近出现一条轻量引导语，提示用户通过系统入口添加到“我的小程序”，并可手工关闭。

## 页面状态

| 状态 | 说明 |
|---|---|
| 默认展示 | 未关闭时，首页首屏右上方展示气泡提示。 |
| 手工关闭 | 点击气泡内关闭按钮后，气泡立即消失。 |
| 安全降级 | 胶囊位置信息不可用或页面异常状态时，可不展示气泡。 |

## 布局要点

- 气泡靠近右上角微信原生胶囊左下方。
- 气泡不得覆盖原生胶囊，不手绘系统按钮。
- 气泡宽度控制在小屏可读范围内，文案保持短句。
- 关闭按钮位于气泡右侧或右上角，点击热区清晰。
- 首页品牌导航、搜索入口、Banner 和商品模块不被遮挡。

## 待导出

- PNG Golden Reference：待后续设计或实现阶段从 `prototype.html` 导出。
- 真机截图 evidence：待 OpenSpec / 实现阶段按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 补充。
