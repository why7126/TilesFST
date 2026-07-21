---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
status: done
review_result: approved
reviewed_at: 2026-07-19 17:41:40
reviewer: AI
created_at: 2026-07-19 17:41:40
updated_at: 2026-07-19 21:39:11
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
---

# BUG-0068 评审结论

## 结论

评审通过，确认需要修复或验收闭环。

`BUG-0068` 聚焦 Sprint 008 强制关闭后遗留的小程序首页 DevTools / 真机验收 evidence 缺口。缺陷包已经补齐，根因、规避方案和回归验收标准足以支撑后续 `/bug-opsx` 创建 fix Change，或纳入 Sprint 后执行设备验收与必要的小程序 UI 修复。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | Sprint 008 验收报告已明确保留 DevTools / 真机、320-430 pt、胶囊避让和内容不遮挡人工 follow-up；根因归类为验收 evidence / 流程缺口充分 |
| 严重等级合理 | 通过 | `high` 合理；若真实设备出现遮挡或重叠，将直接影响终端客户首页首屏体验和 REQ-0041 验收结论 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖 evidence 来源区分、首页真实预览、320-430 pt、胶囊避让、fixed header / TabBar 不遮挡、降级状态和范围边界 |
| 是否需 hotfix 路径 | 不需要 | 当前没有证据表明生产已发生不可用；优先走常规 fix / 验收闭环路径，若真机发现首页首屏不可用再升级 |

## 评审意见

本 BUG 不应先假设代码必然错误。当前已知事实是自动化与静态检查只能作为代码形态侧证，不能替代微信开发者工具或真机截图。后续 fix Change 应优先补齐设备验收 evidence；只有当截图证明存在遮挡、重叠、横向滚动或内容不可读时，才扩大到小程序 UI 修复。

默认范围不包含 API、数据库、Orval、Web 管理端或 Docker Compose。若设备验收过程中发现接口、数据或环境问题，应在后续 BUG / REQ 或 OpenSpec Change 中单独说明。

## 门禁结果

| 后续动作 | 结果 | 说明 |
|---|---|---|
| `/bug-opsx BUG-0068` | 允许 | 状态评审通过，可创建 fix Change |
| `/sprint-propose` 纳入 Sprint | 允许 | 评审通过后可纳入 Sprint 正式范围 |
| `/sprint-apply` 或 `/opsx-apply` | 需后置门禁 | 必须先有 fix Change，且纳入某个 `sprint-xxx` 后才能实现 |

## 下一步

```text
/bug-opsx BUG-0068-miniapp-home-device-acceptance-followup
```
