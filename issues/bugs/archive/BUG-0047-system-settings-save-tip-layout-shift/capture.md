---
bug_id: BUG-0047-system-settings-save-tip-layout-shift
status: captured
created_at: 2026-06-28 17:53:48
updated_at: 2026-06-28 17:53:48
severity_hint: medium
environment: local|docker
related_requirement: REQ-0017-system-settings
related_bug: BUG-0015-admin-list-status-tips-layout-shift
captured_via: capture
classification_rationale: 保存成功 inline tip 插入文档流导致下方内容位移，与管理端其它状态提示 fixed/overlay 模式不一致
---

# 现象

「系统设置」页点击「保存设置」成功后，页面中部出现 `settings-save-tip` 提示条，插入文档流导致下方 Tab 内容与底部操作区发生上下位移；与其它管理端列表页状态变更提示的交互不一致。

# 复现步骤

1. 以 `admin` 登录 Web 管理端。
2. 进入「系统设置 → 基础信息」（`/admin/settings/basic`）。
3. 修改任意字段后点击「保存设置」。
4. 观察保存成功提示出现/消失时，下方表单与 footer 是否发生 layout shift。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 保存成功提示采用与管理端其它页面一致的非推挤模式（如 fixed/overlay toast 或预留占位），不出现内容跳动。 |
| **实际** | 中部条件渲染的 `settings-save-tip` 推挤下方内容，产生明显上下波动。 |

# 初步线索

- `SystemSettingsPage.tsx` 约 841 行：`{saveTip ? <div className="settings-save-tip">{saveTip}</div> : null}`。
- 参考：`BUG-0015`、`BUG-0003` 同类 layout shift 修复（admin 列表页 status tips）。
- REQ-0017 AC-012 原描述 inline save-tip；与用户反馈及项目统一 tip 模式需 reconcile。

# 附件

- screenshots/
- logs/
