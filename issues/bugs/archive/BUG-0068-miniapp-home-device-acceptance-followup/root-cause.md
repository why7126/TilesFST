---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
status: done
created_at: 2026-07-19 17:36:58
updated_at: 2026-07-19 21:39:11
root_cause_type: process/acceptance-evidence/miniapp-device
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **process / acceptance-evidence / miniapp-device** |
| 引入阶段 | Sprint 008 强制关闭与归档阶段 |
| 责任模块 | 微信小程序首页、全局自定义导航栏、Sprint 验收 evidence |
| 关联后端 | 默认无；当前问题不是接口契约或数据聚合缺陷 |
| 关联测试 | `tests/test_miniapp_static.py` 可提供自动化侧证，但不能证明 DevTools / 真机视觉验收已完成 |

## 2. 直接原因

Sprint 008 关闭时已接受两个小程序人工验收残留：

- `fix-miniapp-home-preview-runtime-entry`：首页运行入口修复后，仍缺微信开发者工具真实首页预览与 320-430 pt 视口布局验收。
- `add-miniapp-global-custom-navigation-bar`：全局自定义导航接入后，仍缺 320/375/430 pt 下的原生胶囊避让、状态栏避让和 fixed header 内容不遮挡验收。

这些残留在 Sprint 验收报告中被标注为人工 follow-up 风险，但在 `BUG-0068` 创建前没有独立 Issue 承接，导致后续无法按 BUG 生命周期推进复验、评审和修复。

## 3. 根本原因

### 3.1 设备验收 evidence 未独立建模

Sprint 008 同时包含自动化测试、静态检查、OpenSpec 归档和人工设备验收。归档时自动化侧证已通过，但 DevTools / 真机 evidence 没有被建模为独立交付物，导致“可归档的代码事实”和“尚未完成的设备验收事实”混在同一验收结论里。

### 3.2 强制关闭后的 follow-up 需要独立 Issue 生命周期

Sprint 强制关闭允许非阻断部分先闭环，但遗留风险必须能继续被追踪。`BUG-0068` 的缺失使首页真实预览、320-430 pt、胶囊避让和内容不遮挡这些验收点无法进入 `/bug-complete`、`/bug-review` 和后续 fix Change。

### 3.3 自动化侧证边界表达不足

现有静态测试可证明以下代码形态：

- 首页运行脚本包含 `loadHome()` 与首页交互逻辑。
- 首页声明自定义导航组件。
- 自定义导航调用微信系统信息和菜单按钮信息。
- WXML / WXSS 中未新增手绘分享、关闭或胶囊控件。
- 主要点击目标和安全区样式存在。

但这些测试不能证明真实设备上的菜单按钮坐标、状态栏高度、可视区域、底部安全区和截图效果。缺少明确 evidence 模板时，容易把自动化通过误写成真机通过。

## 4. 触发条件

满足以下条件即可触发该验收缺口：

1. Sprint 已归档或准备发布。
2. 小程序首页和全局自定义导航存在 DevTools / 真机人工验收项。
3. 只有静态测试、代码检查或自动化结果，没有微信开发者工具 / 真机截图与设备信息。
4. 验收结论需要声明首页预览、320-430 pt 适配、原生胶囊避让或内容不遮挡已通过。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| 首页运行脚本一定已坏 | 暂不成立；上一轮 `/bug-explore` 中 `tests/test_miniapp_static.py` 16 passed |
| 后端首页聚合接口不可用 | 暂无证据；当前缺口聚焦设备验收 evidence |
| 数据库结构缺失 | 暂无证据；不涉及 SQLite / MySQL schema |
| Orval 或 Web 生成物异常 | 不涉及；小程序端不依赖 Orval 生成物 |
| Docker Compose 配置错误 | 暂无证据；本 BUG 默认不要求 Docker Compose 变更 |

## 6. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | process / acceptance-evidence / miniapp-device |
| 是否代码缺陷 | 未确认；需设备 evidence 判定 |
| 是否接口缺陷 | 默认否 |
| 是否数据库缺陷 | 否 |
| 是否测试缺口 | 是；缺少 DevTools / 真机 evidence gate |
| 主要修复面 | 小程序设备验收 evidence、截图记录、验收模板和必要时的 UI 避让修复 |

## 7. 修复建议（供后续 bug-opsx）

1. 建立 `BUG-0068` 的设备验收 evidence 模板，记录设备型号、微信开发者工具版本、逻辑宽度、截图、结论和剩余风险。
2. 对首页 `pages/index/index` 至少覆盖 320、375、390、430 pt 视口。
3. 对首页品牌导航、微信原生胶囊、状态栏、搜索、Banner、快捷入口、推荐模块和底部 TabBar 逐项截图确认。
4. 若截图发现遮挡、重叠、横向滚动或内容不可读，再在对应 fix Change 中修改小程序 UI。
5. 默认不修改 API、数据库、Orval、Web 或 Docker Compose；如设备验收暴露接口或环境问题，需另行说明范围变化。
