---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
title: Sprint 008 小程序首页 DevTools 与真机验收残留未闭环
severity: high
status: done
owner:
discovered_at: 2026-07-19 17:34:02
environment: 微信开发者工具 / 真机
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
related_change:
source_sprint: sprint-008
created_at: 2026-07-19 17:34:02
updated_at: 2026-07-19 21:39:11
---

# BUG-0068 Sprint 008 小程序首页 DevTools 与真机验收残留未闭环

## 现象

Sprint 008 强制关闭时已明确保留小程序首页设备验收风险：`fix-miniapp-home-preview-runtime-entry` 仍缺微信开发者工具真实首页预览确认，`add-miniapp-global-custom-navigation-bar` 仍缺 320/375/430 pt 与 320-430 pt 逻辑宽度下的胶囊避让、状态栏避让和内容不遮挡验收。

当前自动化与静态测试只能证明首页运行脚本、自定义导航声明、禁止伪系统胶囊、基础点击尺寸和安全区样式存在，不能替代微信开发者工具或真机上的真实视觉 evidence。因此 Sprint 008 已归档，但首页真实预览和设备适配验收尚未形成闭环。

## 复现步骤

1. 使用微信开发者工具打开 `src/miniapp/`。
2. 进入首页 `pages/index/index`，确认预览加载真实小程序运行脚本，而非原型、截图或静态测试结果。
3. 在 320、375、390、430 pt 以及 320-430 pt 逻辑宽度范围检查首页首屏。
4. 检查首页品牌导航、搜索入口、Banner、快捷入口、新品推荐、热销推荐、瀑布流和底部 TabBar。
5. 检查微信原生分享 / 关闭胶囊、状态栏、自定义 fixed header 与底部安全区，确认页面内容和点击目标没有被遮挡。
6. 在真机或等效微信开发者工具预览环境记录截图、设备型号、逻辑宽度、预览时间和验收结论。

## 期望 vs 实际

期望：

- 首页在微信开发者工具和真机预览中能真实展示品牌导航、搜索、Banner、快捷入口、推荐模块和底部 TabBar。
- 320-430 pt 范围内无横向滚动、关键文本不可读、卡片挤压、点击区域不足或首屏大面积空白。
- 自定义导航栏避让微信原生胶囊和状态栏，不手绘模拟分享、关闭或胶囊控件。
- fixed header、底部 TabBar 和安全区不遮挡首页关键内容与主要点击目标。
- 验收材料明确区分自动化侧证、微信开发者工具截图、真机截图和人工结论。

实际：

- Sprint 008 已归档，自动化与静态检查通过，但真实 DevTools / 真机预览 evidence 尚未补齐。
- 尚不能确认 320-430 pt 下首页首屏是否持续满足胶囊避让、内容不遮挡和无横向滚动要求。
- 尚不能把 Sprint 008 小程序首页设备验收表述为已完成。

## 影响范围

| 范围 | 影响 |
|---|---|
| 微信小程序首页 | 首页首屏真实预览和终端客户第一屏体验仍缺设备验收闭环 |
| 自定义导航栏 | 原生胶囊、状态栏和 fixed header 避让仍需真实环境确认 |
| Sprint 008 验收 | 已归档但保留人工 follow-up，发布或验收表述不得声称真机通过 |
| API / 数据库 / Orval | 暂无直接影响；当前缺口聚焦小程序 UI 验收 evidence |
| Web / 管理端 | 暂无影响 |

## 严重等级说明

严重等级为 `high`。

理由：该缺陷阻断 Sprint 008 小程序首页真实设备验收闭环，直接影响 `REQ-0041-miniapp-home` 的首页首屏、320-430 pt 适配、胶囊避让和内容不遮挡结论。虽然当前没有证据表明生产数据、鉴权或接口安全受影响，但如果真实设备上存在遮挡或重叠，将直接影响终端客户进入小程序后的核心体验，因此需要优先进入 `/bug-complete` 与后续评审流程。

## 已知侧证

- `tests/test_miniapp_static.py` 已覆盖首页运行入口、自定义导航、禁止伪胶囊、基本点击尺寸和安全区样式。
- 最近一次 `/bug-explore` 期间运行 `uv run pytest tests/test_miniapp_static.py`，结果为 16 passed。
- 上述侧证仅说明代码形态未明显回退，不等同于微信开发者工具或真机视觉验收完成。
