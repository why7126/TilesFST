---
title: 管理端表单页一致性最佳实践
purpose: 预防 Profile/Settings 等表单页重复 CTA、原生 confirm、inline tip 布局抖动类 BUG
content: 提炼自 Sprint 003 BUG-0023、0026、0043、0046、0047 及 Sprint 002 BUG-0015
source: /sprint-exps sprint-003
update_method: 新表单页或 Settings Tab 时更新
owner: 前端负责人
status: draft
created_at: 2026-06-28 19:42:56
updated_at: 2026-06-28 19:42:56
note: 个案见 issues/bugs/；本文写模式与预防
---

# 管理端表单页一致性最佳实践

## 背景

Sprint 003 中个人资料（REQ-0014）与系统设置（REQ-0017）分别出现：

- 页头 + 表单底 **双「保存」**（`BUG-0023`、`BUG-0043`）
- **`window.confirm`** 用于恢复默认 / dirty Tab 切换（`BUG-0046`；改密取消 `BUG-0026`）
- **inline save-tip** 导致主内容 layout shift（`BUG-0047`，与 Sprint 002 `BUG-0015` 同类）

根因：`add-*` acceptance 允许双 CTA 或仅要求「二次确认」而未限定 DS 呈现形式；各页独立 port CSS。

## 必须对齐的基准

**交互基准**：管理端列表页成功反馈（`AdminLayout` fixed toast）+ 类目/品牌页 **DS confirm modal**（`modal-backdrop` + `role="dialog"`）

| 区域 | 要求 |
|------|------|
| 保存 CTA | 全页 **仅一处** accessible name 为「保存设置/保存修改」的 button，位于 **表单 footer**（`settings-panel-footer` / 表单 `actions`） |
| 页头 hero | MUST NOT 重复渲染保存按钮；可保留标题、眉标、summary |
| 危险/不可逆操作 | 「恢复默认」、放弃 dirty 切换 Tab **MUST** DS confirm modal；**禁止** `window.confirm` / `window.alert` |
| 成功/失败反馈 | **fixed toast**（`.admin-toast-region`）；**禁止** summary 与主表单之间的文档流条件块 |
| dirty 提示 | 「有未保存修改」可为静态文案；不得用会推挤 layout 的块级 success banner |

## 实现优先级

```text
1. AdminFormPage / SystemSettingsPage Shell 模板（hero + nav + panel + footer）
2. 复用 AdminLayout toast 与共享 ConfirmModal
3. 单页 Tab 仅填字段与 PATCH 逻辑
```

## 验收 gate（新增表单/设置页 MUST）

- [ ] 全页仅 1 个「保存*」button（vitest 计数）
- [ ] 恢复默认 / dirty 切换为 DS modal（无原生对话框）
- [ ] 保存成功 toast 不引起 `settings-layout` / 表单区垂直位移
- [ ] 1440×1024 与 prototype HTML 并排（PNG 可选）

## 关联 BUG（个案）

- `issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/`
- `issues/bugs/archive/BUG-0026-change-password-cancel-confirm-redundant/`
- `issues/bugs/archive/BUG-0043-system-settings-duplicate-save-buttons/`
- `issues/bugs/archive/BUG-0046-system-settings-reset-confirm-ui-inconsistency/`
- `issues/bugs/archive/BUG-0047-system-settings-save-tip-layout-shift/`

## 参考

- `rules/ui-design.md` 管理端表单章节
- `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` §4
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`（toast 模式）
