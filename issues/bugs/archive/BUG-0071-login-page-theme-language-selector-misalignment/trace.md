---
bug_id: BUG-0071-login-page-theme-language-selector-misalignment
status: done
lifecycle_stage: archive
severity: medium
created_at: 2026-07-21 08:35:25
updated_at: 2026-07-22 08:36:29
lifecycle:
  captured: 2026-07-21 08:35:25
  generated: 2026-07-21 09:17:10
  completed: 2026-07-21 09:47:39
  reviewed: 2026-07-21 10:11:02
  approved: 2026-07-21 10:11:02
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-login-page-tool-selector-alignment
source_command: /capture
captured_via: capture
classification_rationale: 已有登录页 UI 能力下，主题选择模块与语言选择模块出现视觉对齐偏差，属于现有实现与预期布局不一致。
openspec_changes:
  - change_id: fix-login-page-tool-selector-alignment
    type: fix
    status: archived
related_bugs: []
---

```yaml
bug_id: BUG-0071-login-page-theme-language-selector-misalignment
status: done
severity: medium
lifecycle_stage: review
created_at: 2026-07-21 08:35:25
updated_at: 2026-07-21 23:02:30
lifecycle:
  captured: 2026-07-21 08:35:25
  generated: 2026-07-21 09:17:10
  completed: 2026-07-21 09:47:39
  reviewed: 2026-07-21 10:11:02
  approved: 2026-07-21 10:11:02
iteration: sprint-010
related_requirement: null
related_bug: null
related_change: fix-login-page-tool-selector-alignment
source_command: /capture
captured_via: capture
classification_rationale: 已有登录页 UI 能力下，主题选择模块与语言选择模块出现视觉对齐偏差，属于现有实现与预期布局不一致。
openspec_changes:
  - change_id: fix-login-page-tool-selector-alignment
    type: fix
    status: archived
related_bugs: []
scope:
  terminal: web
  page: login
  component: top_right_tools
  issue_type: visual_alignment
readiness:
  capture: done
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: opsx-apply
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| 用户反馈 | `/capture` | 登录页右上角主题选择模块与语言选择模块没有对齐 |

## 建议验收要点

| 验收点 | 说明 |
|---|---|
| 视觉对齐 | 登录页右上角主题选择模块与语言选择模块在同一行内保持一致的垂直对齐 |
| 尺寸一致 | 两个模块的高度、交互热区和视觉重心一致，不出现上下错位 |
| 间距稳定 | 两个模块之间的水平间距符合登录页工具区布局，不因语言或主题文案变化产生错位 |
| 响应式 | 常用桌面视口与窄屏视口下右上角工具区均无重叠、换行异常或裁切 |

## 验收证据

| 类型 | 证据 |
|---|---|
| 实现 | `LoginPage.tsx` 统一 `.login-tools` 容器承载主题选择模块与语言选择模块；`LoginFormPanel.tsx` 移除独立语言按钮定位；`login-page.css` 统一控件高度、垂直居中、右侧边界和窄屏纵向布局。 |
| 测试 | `pnpm --dir src/web exec vitest run src/features/auth/components/LoginPage.test.tsx src/features/auth/components/LoginFormPanel.test.tsx src/features/auth/components/LoginForm.test.tsx src/features/theme/ThemeContext.test.tsx`，4 files / 18 tests passed。 |
| 视觉 | Playwright CLI 生成 `/private/tmp/login-tools-desktop.png` 与 `/private/tmp/login-tools-mobile.png`；桌面和窄屏均未出现重叠、裁切或遮挡登录标题、表单字段、安全提示。 |
| 非影响 | 未修改登录接口、认证流程、用户模型、数据库结构、OpenAPI 或 Orval 生成物。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 08:35:53 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-login-page-tool-selector-alignment） |
| 2026-07-22 08:35:35 | /opsx-archive | Change `fix-login-page-tool-selector-alignment` 已归档，状态同步完成。 |
| 2026-07-21 23:02:30 | /opsx-apply | Change `fix-login-page-tool-selector-alignment` apply 完成，待 archive。 |
| 2026-07-21 23:00:30 | /opsx-apply | 完成登录页工具区对齐修复与回归验收；等待 Workflow Sync 标记 Change applied |
| 2026-07-21 14:57:57 | /sprint-propose | 纳入 sprint-010 正式范围，状态更新为 in_sprint |
| 2026-07-21 14:41:52 | /bug-opsx | 创建修复 Change `fix-login-page-tool-selector-alignment`，状态 proposed |
| 2026-07-21 10:11:38 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-21 10:11:02 | /bug-review --approve | 评审通过，状态更新为 approved，准备由 plan 迁入 review 阶段 |
| 2026-07-21 09:47:39 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-21 09:17:10 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-21 08:35:25 | /capture | 记录登录页右上角主题选择模块与语言选择模块未对齐缺陷 |

- 2026-07-22 08:35:35 workflow-sync：状态同步为 done（Change archived）
