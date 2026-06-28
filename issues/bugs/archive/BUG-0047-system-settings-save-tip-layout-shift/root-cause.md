---
bug_id: BUG-0047-system-settings-save-tip-layout-shift
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 条件渲染 tip 插入文档流

`SystemSettingsPage.tsx` L841：

```tsx
{saveTip ? <div className="settings-save-tip">{saveTip}</div> : null}
```

tip 出现在 `summary-grid` 与 `settings-layout` 之间；无 tip 时该节点不存在，有 tip 时整块插入，推动下方内容下移。

### 1.2 CSS 占用垂直空间

`.settings-save-tip`（`system-settings.css` L501–509）含 `margin-top: 12px`、`padding: 10px 14px`，加剧位移幅度。

### 1.3 恢复默认成功亦设置 saveTip

L185 `setSaveTip('已恢复默认配置')` 触发相同 layout shift。

## 2. 根本原因

### 2.1 REQ AC-012 / OpenSpec 要求 inline save-tip

`add-system-settings` 按 spec 实现文档流内联提示，未采用列表页 `AdminToast` 或 Profile 占位模式。

### 2.2 与 BUG-0015 全站 tip 统一方向冲突

管理端列表页已改为 `AdminLayout` + fixed `admin-toast-region`；系统设置页仍用 inline 条件块，造成交互不一致。

## 3. 触发条件

1. 保存或恢复默认成功 → `saveTip` 非 null → layout shift。
2. tip 清除或切 Tab → 内容回弹。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 关联 BUG | BUG-0015、BUG-0003 |
| 建议 Change | `fix-system-settings-save-tip-layout-shift` |

## 5. 后续修复建议

**推荐方案 A**：通过 `AdminLayout` outlet context 调用 `AdminToast`（与列表页一致，零 layout shift）。

**备选方案 B**：Profile 式 `.save-tip.is-hidden` 预留占位。

fix change 需 MODIFIED AC-012 若放弃 inline tip。
