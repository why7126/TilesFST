---
change_id: fix-miniapp-home-device-acceptance
type: fix
status: applied
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 21:13:20
source_bug: BUG-0068-miniapp-home-device-acceptance-followup
source_sprint: sprint-008
target_sprint: sprint-009
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
---

# Trace

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| BUG | `BUG-0068-miniapp-home-device-acceptance-followup` | Sprint 008 小程序首页 DevTools 与真机验收残留未闭环 |
| REQ | `REQ-0041-miniapp-home` | 微信小程序首页原始需求 |
| BUG | `BUG-0065-miniapp-home-preview-deviation` | 首页运行入口修复后仍保留设备验收 follow-up |
| Sprint | `sprint-008` | 来源 Sprint，强制关闭时保留人工验收风险 |
| Sprint | `sprint-009` | 目标 Sprint，BUG-0068 已纳入正式范围 |

## Evidence

| 类型 | 路径 / 命令 | 状态 | 说明 |
|---|---|---|---|
| 设备验收记录 | `issues/bugs/archive/BUG-0068-miniapp-home-device-acceptance-followup/logs/device-evidence.md` | passed | 自动化、源码静态侧证、DevTools 与真机/等效设备人工验证均已记录 |
| 静态测试 | `uv run pytest tests/test_miniapp_static.py` | passed | 19 passed；不替代 DevTools / 真机验收 |
| DevTools | 微信开发者工具打开 `src/miniapp/` | passed | 用户确认已人工验证；具体版本与截图路径未随本消息提供 |
| 真机 | iOS / Android 或等效微信预览设备 | passed | 用户确认已人工验证；具体设备与截图路径未随本消息提供 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 21:13:20 | /opsx-apply | 用户确认已人工验证，DevTools / 真机或等效设备验收闭环；Change 状态更新为 applied |
| 2026-07-19 19:40:29 | /opsx-apply | 建立 BUG-0068 设备验收 evidence 记录；DevTools / 真机验收因环境不可用保留 blocked/follow_up |
| 2026-07-19 18:14:29 | /bug-opsx | 创建缺陷修复 Change，状态 proposed |
