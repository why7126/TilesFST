---
change_id: add-miniapp-custom-navigation-bar
created_at: 2026-07-19 10:08:02
updated_at: 2026-07-19 10:54:32
---

# 实现验收记录

## Native Controls

- 首页 `brand-header` 仅渲染品牌 Logo、门店名称、副文案和无文案右侧避让占位；未在 WXML / WXSS 中自绘分享、关闭或胶囊控件。
- 分享使用页面已有 `onShareAppMessage()` 标准能力；关闭能力保持微信小程序原生行为。
- 首页 `pages/index/index.json` 启用 `navigationStyle: custom`；未在 `app.json` 全局启用，避免扩展为全小程序统一 custom navigation 壳层。
- Logo / 门店名称 / 副文案与右侧原生分享、关闭胶囊避让保留在同一个 `brand-header` 顶部模块中。
- `brand-header` 使用 `position: fixed` 固定在页面顶部，页面加载时通过 `wx.getSystemInfoSync()` 与 `wx.getMenuButtonBoundingClientRect()` 计算真实状态栏与胶囊位置，避免与手机顶部时间 / 网络状态栏重叠。
- CSS 提供 `106px` 兜底高度和 `44px` 顶部避让；运行时 `navBarStyle` / `pageTopStyle` 会按机型覆盖固定导航高度与页面内容让位。
- 导航内容在可视导航区内通过 `align-items: center` 垂直居中。
- 左侧 Logo + 产品名文案组和右侧原生分享 / 关闭胶囊避让区统一使用 88rpx 内容高度，分别通过 `align-items: center`、`justify-content: center` 和 `align-self: center` 保持中心线一致。
- 页面内容以 `padding-top: calc(env(safe-area-inset-top) + 124rpx)` 让位，避免搜索框和 Banner 被遮挡。
- 右侧避让以 `native-action-reserve` 保留 184rpx 空间。

## 320-430 pt Layout

- 320 pt 视口近似为 640rpx 内容宽度：页面左右 padding 合计 64rpx，右侧避让 184rpx，Logo 与间距 96rpx 后，品牌文案仍保留约 296rpx 可读宽度。
- 430 pt 视口近似为 860rpx 内容宽度：同样避让原生区域后，品牌文案保留约 516rpx 可读宽度。
- 门店名称和副文案使用单行省略，避免横向滚动和与右侧原生按钮区域重叠。

## API / DB / Orval

- 本次仅修改小程序首页 WXML / WXSS 与静态测试，未新增或修改后端 API、数据库字段、OpenAPI 或 Orval 生成物。
