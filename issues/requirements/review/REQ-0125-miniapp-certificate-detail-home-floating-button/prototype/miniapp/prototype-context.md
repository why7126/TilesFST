---
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
title: 小程序证书详情页返回首页悬浮按钮原型上下文
status: pending_review
owner: product
source: acceptance.md
created_at: 2026-08-25 22:39:27
updated_at: 2026-08-26 08:32:09
---

# 原型上下文

## 1. 目标

本 prototype context 用于约束证书详情页局部新增的【返回首页】悬浮按钮。该需求不重做证书详情页整体原型，只要求在既有证书详情页面结构中复用 `home-floating-button`，并保持 `offset="list"` 与其他深层内容页一致。

## 2. 页面落点

```text
CertificateDetailPage
├── custom-navigation(title)
├── CertificateMediaHero
├── CertificateSummary
├── BrandEntry / brand-card
├── CertificateInfoPanel
├── ErrorOrEmptyState
└── home-floating-button(offset="list")
```

## 3. 状态覆盖

| 状态 | 说明 | 验收重点 |
|---|---|---|
| normal | 证书详情加载成功 | 按钮可见、可点击，返回首页成功。 |
| loading | 证书数据加载中 | 按钮不遮挡骨架屏和导航栏。 |
| error | 网络失败或接口失败 | 按钮作为恢复路径保留，不遮挡重试按钮。 |
| hidden | 证书不可查看或不存在 | 按钮可回首页，错误提示可读。 |
| share-direct | 分享直达无页面栈 | 左上返回兜底与悬浮返回首页均可到首页。 |
| repeated-tap | 快速重复点击 | 导航锁可恢复，不出现重复跳转。 |

## 4. 视觉约束

- 复用 `home-floating-button` 的图标、文案、尺寸、圆角、阴影和按压态。
- 默认使用 `offset="list"`，不新增证书详情页专属 offset。
- 按钮位于页面右下侧既有组件位置，不遮挡证书主图、品牌入口或错误态按钮；证书信息字段被按钮局部覆盖可接受。
- 在 320 / 375 / 430 pt 逻辑宽度下确认按钮与底部安全区、滚动内容和品牌卡片不冲突。

## 5. 验收证据

- DevTools 320 / 375 / 430 pt 截图或等价截图摘要。
- 分享直达页面栈兜底操作记录。
- 快速重复点击导航锁恢复摘要。
- 小程序静态检查结果，覆盖组件声明、WXML 引用和 `.ts` / `.js` 同步。
