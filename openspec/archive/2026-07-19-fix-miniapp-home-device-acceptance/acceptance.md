---
change_id: fix-miniapp-home-device-acceptance
source_bug: BUG-0068-miniapp-home-device-acceptance-followup
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
---

# Acceptance

## AC-001 evidence 来源区分

验收材料 MUST 明确区分自动化测试结果、微信开发者工具截图、真机截图和人工结论；不得将静态测试通过表述为 DevTools 或真机通过。

## AC-002 首页真实预览

微信开发者工具打开 `src/miniapp/` 并进入 `pages/index/index` 后，首页 MUST 展示品牌导航、搜索入口、Banner 或品牌化降级、快捷入口、推荐模块或空状态、全部产品区域和底部 TabBar。

## AC-003 320-430 pt 覆盖

首页在 320、375、390、430 pt 及 320-430 pt 常见宽度下 MUST 无横向滚动、关键文本不可读、卡片不可接受挤压或关键模块重叠。

## AC-004 微信原生胶囊避让

首页自定义导航内容 MUST NOT 进入微信原生分享 / 关闭胶囊区域；WXML / WXSS MUST NOT 新增手绘分享、关闭或胶囊控件。

## AC-005 fixed header 与底部 TabBar 不遮挡

fixed header MUST 通过 spacer、offset 或等价方式为内容让位；底部 TabBar 与安全区 MUST 不遮挡商品卡片、加载状态、空状态或主要点击目标。

## AC-006 降级状态可验收

Banner 为空、商品为空、图片加载失败或首页请求失败时，页面 MUST 显示品牌化降级、空状态或错误提示，并继续满足 320-430 pt、胶囊避让和内容不遮挡要求。

## AC-007 自动化侧证保留但不越界

`tests/test_miniapp_static.py` 通过可作为运行入口、自定义导航声明、禁止伪胶囊和基础点击尺寸侧证，但验收结论 MUST 注明它不替代 DevTools / 真机截图。

## AC-008 技术范围不扩大

默认 MUST 聚焦小程序首页、导航栏和验收 evidence；不得修改后端 API、SQLite/MySQL schema、Pydantic Schema、Orval 生成物、Web 管理端或 Docker Compose。若设备验收发现接口、数据或环境问题，MUST 另行说明并单独承接。
