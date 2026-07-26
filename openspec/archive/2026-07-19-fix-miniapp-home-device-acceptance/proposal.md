---
change_id: fix-miniapp-home-device-acceptance
type: fix
status: proposed
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
source_bug: BUG-0068-miniapp-home-device-acceptance-followup
source_sprint: sprint-008
target_sprint: sprint-009
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
---

# Proposal: 修复小程序首页设备验收闭环缺口

## Why

`BUG-0068-miniapp-home-device-acceptance-followup` 记录了 Sprint 008 强制关闭后仍未闭环的小程序首页 DevTools 与真机验收残留。当前自动化与静态检查只能证明首页运行入口、自定义导航声明、禁止伪胶囊、点击尺寸和安全区样式存在，不能替代微信开发者工具或真机上的真实视觉 evidence。

该缺口影响 `REQ-0041-miniapp-home` 的首页真实预览、320-430 pt 适配、微信原生胶囊避让、fixed header 和底部 TabBar 不遮挡结论。若继续在验收或发布材料中误写为真机通过，会造成质量结论失真；若真实设备存在遮挡或重叠，会直接影响终端客户进入小程序后的首屏体验。

## What Changes

- 为小程序首页补齐 DevTools / 真机验收 evidence 要求，明确截图、设备、逻辑宽度、验收时间和结论的记录边界。
- 将 320、375、390、430 pt 和 320-430 pt 常见宽度纳入首页设备回归验收。
- 对首页品牌导航、搜索入口、Banner、快捷入口、新品推荐、热销推荐、全部产品、底部 TabBar、自定义导航胶囊避让和 fixed header 内容避让建立闭环验收任务。
- 若设备 evidence 暴露遮挡、重叠、横向滚动、关键模块缺失或内容不可读，在本 Change 范围内修复小程序首页 / 自定义导航相关 UI。
- 保留自动化侧证，但明确其不能替代 DevTools / 真机验收。

## Out of Scope

- 默认不修改后端 API、SQLite/MySQL schema、Pydantic Schema、Orval 生成物、Web 展示端、管理端或 Docker Compose。
- 不新增后台配置、独立导航栏 API、设备验收平台或新的业务页面。
- 不把真机无法执行时的 follow-up 自动创建为新 BUG；如发现独立接口、数据或环境缺陷，应另行 capture。

## Bug Analysis Report

| 项 | 结论 |
|---|---|
| 现象 | Sprint 008 已归档，但首页真实 DevTools / 真机预览、320-430 pt 适配和胶囊避让 evidence 尚未补齐。 |
| 根因分类 | process / acceptance-evidence / miniapp-device |
| 严重等级 | high |
| 影响范围 | 微信小程序首页、自定义导航栏、Sprint 008 验收表述、发布质量结论 |
| 关联 REQ | `REQ-0041-miniapp-home` |
| 关联 BUG | `BUG-0065-miniapp-home-preview-deviation` |
| 当前侧证 | `tests/test_miniapp_static.py` 曾通过 16 项，但仅为自动化/静态侧证。 |

## Rollback Plan

- 若仅新增 evidence 文档或验收记录，无需运行时回滚；撤回错误结论并重新标记为 `follow_up` 或 `blocked`。
- 若本 Change 修改小程序首页或自定义导航 UI 后产生回归，回滚对应 `src/miniapp/` 文件，并保留失败截图与原因。
- 回滚后重新运行小程序静态测试，并在验收材料中明确 DevTools / 真机结论未通过或待复验。

## Risks

- DevTools 与真机环境可能无法在 CI 内自动复现，需要人工 evidence 支撑。
- 设备验收可能暴露真实 UI 缺陷，使修复范围从 evidence 扩展到小程序首页或导航栏布局。
- 若缺少截图或设备元数据，验收结论仍可能不可复核。
