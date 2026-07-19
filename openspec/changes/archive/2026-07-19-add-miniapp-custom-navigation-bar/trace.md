---
change_id: add-miniapp-custom-navigation-bar
change_type: update
status: proposed
created_at: 2026-07-19 09:49:14
updated_at: 2026-07-19 09:49:14
source_requirement: REQ-0042-custom-navigation-bar
iteration: sprint-008
capabilities:
  new: []
  modified:
    - miniapp-home
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
---

# Change Trace

## 来源

- REQ: `issues/requirements/archive/REQ-0042-custom-navigation-bar/`
- Sprint: `iterations/archive/sprint-008/`
- Parent: `REQ-0041-miniapp-home`
- Baseline: `REQ-0043-miniapp-home-style-optimization`

## 决策

- 自定义导航栏取当前首页搜索框上方 `brand-header` 的品牌展示部分。
- 包含 `store-logo`、`store-name`、`store-subtitle` 和右侧微信小程序原生分享 / 关闭能力。
- 排除 `store-link`、"门店信息"入口、多门店切换暗示和默认 `openStoreInfo` 跳转。
- 搜索框保持在自定义导航栏下方。
- 默认不改 API / DB / Orval / Docker。

## UI / Prototype Checklist

- [ ] 以 REQ-0043 prototype 和深色首页为视觉基准。
- [ ] 不手绘模拟微信系统状态栏、分享按钮、关闭按钮或胶囊控件。
- [ ] 320-430 pt 宽度下品牌内容不与右侧原生按钮区域重叠。
- [ ] 门店信息入口不属于自定义导航栏。
- [ ] 搜索框不并入自定义导航栏。

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-07-19 09:49:14 | /req-opsx | 从 REQ-0042 创建 OpenSpec Change，修改 `miniapp-home` 规格 |
