## Why

[BUG-0042-system-settings-page-title-v2-suffix](issues/bugs/archive/BUG-0042-system-settings-page-title-v2-suffix/) 已评审通过：系统设置页眉标硬编码 `SYSTEM / SYSTEM SETTINGS / V2`，用户期望去除 `/ V2`（产品版本已由侧栏 `ProductVersionBadge` 展示）。

## What Changes

- `SystemSettingsPage.tsx` 眉标改为 `SYSTEM / SYSTEM SETTINGS`。
- 同步 5 份 `system-settings-*.html` prototype eyebrow（避免 port 回退）。
- MODIFIED `system-settings` spec 页头眉标要求。
- Vitest 断言眉标文案。

## Capabilities

### Modified Capabilities

- `system-settings`：MODIFIED「管理端系统设置页面与分组导航」— 眉标无版本后缀。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `SystemSettingsPage.tsx`；prototype HTML |
| 后端 / API / Orval | 无 |

## Rollback Plan

1. 回滚眉标文案至 fix 前。
2. `pnpm vitest run SystemSettingsPage`。
