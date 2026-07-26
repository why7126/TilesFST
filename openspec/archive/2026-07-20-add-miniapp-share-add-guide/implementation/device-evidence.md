---
change_id: add-miniapp-share-add-guide
source_requirement: REQ-0061-miniapp-share-add-guide
status: archived
created_at: 2026-07-20 09:44:43
updated_at: 2026-07-20 23:23:22
---

# 小程序添加引导语实现与设备 Evidence

## 实现摘要

- 首页 `pages/index/index` 接入“添加到我的小程序”轻量引导语，基于原生胶囊 `bottom + 8px` 固定展示在右上角按钮下方，不跟随页面内容流下移。
- 引导语右侧位置通过 `wx.getMenuButtonBoundingClientRect()` 与 `windowWidth - menuButton.right + 44` 计算，失败时使用集中 fallback `top: 112px; right: 52px`，让气泡凸起更贴近分享按钮中部。
- 引导语文案调整为“点击右上角 [小/大/小三点提示符] 添加到我的小程序，方便下次找回”；三点仅为文案提示符，不模拟系统胶囊或可点击系统按钮。
- 引导语文案固定为两行展示：第一行“点击右上角 + 小/大/小三点提示符”，第二行“添加到我的小程序，方便下次找回”，避免窄屏挤成三行。
- 关闭策略为“每次新启动可展示；用户关闭后当前会话不再展示”。`App.onLaunch` 清理会话关闭标记，首页关闭入口写入 `miniapp_share_add_guide_session_closed_v1`；读写失败仅记录 warning，不阻断主功能。
- 本 Change 未新增 API、数据库、Orval、Web 展示端或管理端能力。

## 静态测试 Evidence

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
source: static_test
status: passed
artifact_ref: tests/test_miniapp_static.py::test_miniapp_home_share_add_guide_uses_native_menu_reserve_and_session_dismissal
conclusion:
  pseudo_system_controls: pass
  native_menu_reserve: pass
  close_to_native_menu: pass
  two_line_copy_layout: pass
  session_dismissal: pass
  runtime_js_ts_alignment: pass
remaining_risk: DevTools 320/375/430 pt 布局仍需在微信开发者工具中复核；真机验收已由用户确认完成。
```

## 静态视口补充 Evidence

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
source: static_layout_review
status: passed
artifact_ref: tests/test_miniapp_static.py::test_miniapp_home_share_add_guide_uses_native_menu_reserve_and_session_dismissal
conclusion:
  fixed_position: pass
  native_menu_bottom_right_calculation: pass
  max_width_320_to_430: pass
  two_line_copy_layout: pass
  close_hit_area: pass
  no_pseudo_system_controls: pass
remaining_risk: 本补充为仓库可复核静态 evidence；当前执行环境仍未提供微信开发者工具截图能力，不得写作 DevTools 截图通过。
```

## DevTools Evidence

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
entry: home_launch
viewport: 320pt
source: devtools
status: recorded_static_pass_devtools_unavailable
artifact_ref: manual-summary
conclusion:
  status_bar: static_pass
  capsule_reserve: static_pass
  content_offset: static_pass
remaining_risk: 当前执行环境未提供微信开发者工具预览能力；已用静态视口 evidence 记录 320 pt 布局约束，后续可人工补截图。
```

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
entry: home_launch
viewport: 375pt
source: devtools
status: recorded_static_pass_devtools_unavailable
artifact_ref: manual-summary
conclusion:
  status_bar: static_pass
  capsule_reserve: static_pass
  content_offset: static_pass
remaining_risk: 当前执行环境未提供微信开发者工具预览能力；已用静态视口 evidence 记录 375 pt 布局约束，后续可人工补截图。
```

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
entry: home_launch
viewport: 430pt
source: devtools
status: recorded_static_pass_devtools_unavailable
artifact_ref: manual-summary
conclusion:
  status_bar: static_pass
  capsule_reserve: static_pass
  content_offset: static_pass
remaining_risk: 当前执行环境未提供微信开发者工具预览能力；已用静态视口 evidence 记录 430 pt 布局约束，后续可人工补截图。
```

## 真机 Evidence

```yaml
target: add-miniapp-share-add-guide
page_path: pages/index/index
entry: home_launch
viewport: device
source: real_device
status: passed
artifact_ref: manual-summary
conclusion:
  status_bar: pass
  capsule_reserve: pass
  content_offset: pass
  close_behavior: pass
remaining_risk: 用户于 2026-07-20 18:28:41 确认已完成真机验收；当前记录未包含设备型号、系统类型和微信版本，后续 Sprint 收口可补充完整设备元数据。
```

## API / DB / Orval

```yaml
api: not_applicable
database: not_applicable
orval: not_applicable
web_admin: not_applicable
web_catalog: not_applicable
docker_compose: not_applicable
reason: 本 Change 仅新增小程序本地 UI 与当前会话关闭状态，不接入服务端能力。
```
