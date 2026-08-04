## 测试目标

验证小程序返回首页悬浮按钮在同页重复进入、跨页面重复进入、快速重复点击和导航失败兜底后均可恢复可点击状态。

## 自动化测试

- 组件状态流：模拟 `handleReturnHome()` 第一次点击成功后解锁，再次调用仍触发 `wx.switchTab`。
- 页面 show 重置：模拟 `pageLifetimes.show()` 后 `navigating` 与 timer 均恢复。
- 失败兜底：模拟 `wx.switchTab` fail 后进入 `wx.reLaunch`，确认 complete 后释放锁。
- 快速重复点击：在 `navigating: true` 时重复点击不触发第二次导航，解锁后再次点击可触发。
- 静态覆盖：确认分类页、品牌列表页、搜索结果页、商品列表页、品牌详情页、证书页、收藏页和商品详情页仍接入 `home-floating-button`。

## 手工验证

- DevTools：320 pt、375 pt、430 pt 视口下验证同页重复进入和跨页重复进入。
- 体验版或真机：至少覆盖一个 TabBar 页面和一个非 TabBar 详情页。
- 若无法执行真机验证，验收材料标记 `blocked` 或 `follow_up`，不得写作真机通过。

## 不适用

- 后端 API 测试：不适用，本 Change 不改接口。
- 数据库迁移测试：不适用，本 Change 不改表结构。
- Orval 生成：不适用，本 Change 不改 OpenAPI。
- Docker Compose 验证：默认不适用，本 Change 不改部署或服务编排。
