---
bug_id: BUG-0042-system-settings-page-title-v2-suffix
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 页头眉标硬编码含 `/ V2`

`SystemSettingsPage.tsx` L798 将眉标写死为：

```tsx
<p className="eyebrow">SYSTEM / SYSTEM SETTINGS / V2</p>
```

所有 5 个 Tab 共用同一页头组件，故任意分组均展示多余版本后缀。

### 1.2 CSS Port 自 prototype HTML 原样带入

`issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-*.html` 中 eyebrow 亦为 `SYSTEM / SYSTEM SETTINGS / V2`；`add-system-settings` 实现时按 HTML Golden Reference 1:1 port，未与用户期望及 AC-006 文案 reconcile。

## 2. 根本原因

### 2.1 版本信息展示职责未分离

产品版本已由侧栏 `ProductVersionBadge`（`ProductVersionBadge` + `PRODUCT_VERSION`）承担；页内眉标重复 `/ V2` 造成信息冗余，且与 REQ AC-006（`SYSTEM / SETTINGS`）及用户反馈（`SYSTEM / SYSTEM SETTINGS` 无后缀）不一致。

### 2.2 原型与验收标准文案分歧未在交付前消化

AC-006 要求 `SYSTEM / SETTINGS`；prototype 含 `/ V2`；用户明确要求 `SYSTEM / SYSTEM SETTINGS`。三者在 `add-system-settings` 归档前未统一，实现选择了 prototype 字面量。

## 3. 触发条件

1. 以 `admin` 登录 Web 管理端。
2. 访问 `/admin/settings` 或任意 `/admin/settings/{tab}`。
3. 页头加载完成即可见多余 `/ V2`；与是否 dirty、保存无关。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否回归 | 否 |
| 主要修复面 | `SystemSettingsPage.tsx`；可选 prototype HTML delta |
| 建议 Change | `fix-system-settings-page-title-v2-suffix` |

## 5. 后续修复建议

1. 将 L798 改为 `SYSTEM / SYSTEM SETTINGS`。
2. 同步更新 5 份 `system-settings-*.html` prototype eyebrow（避免后续 port 回退）。
3. 在 fix change delta spec **MODIFIED AC-006**：眉标为 `SYSTEM / SYSTEM SETTINGS`，MUST NOT 含版本后缀。
