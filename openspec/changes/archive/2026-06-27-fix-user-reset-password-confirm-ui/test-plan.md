# fix-user-reset-password-confirm-ui — Test Plan

## 单元 / 组件（Vitest）

| 用例 | 文件 | 断言 |
|---|---|---|
| 重置先 dialog 后 API | `UserManagementPage.test.tsx` | 点击「重置密码」→ `getByRole('dialog')`；确认前 `resetUserPassword` 未调用 |
| 禁止 window.confirm | 同上 | `vi.spyOn(window, 'confirm')` 未调用 |
| 取消重置 | 同上 | 取消后 dialog 关闭；API 未调用 |
| 确认重置 | 同上 | 确认后 `resetUserPassword` 被调用 |
| 冻结/删除回归 | 同上 | 既有 confirm 用例全 pass |
| 品牌/类目回归 | `BrandManagementPage.test.tsx`、`TileCategoryManagementPage.test.tsx` | 启停用例全 pass |

## 构建

```bash
cd src/web && npm run build
```

## 手工冒烟

1. `admin` 登录 → `/admin/users` → 「重置密码」→ 出现 DS modal（非浏览器 alert）。
2. 取消 → 无 API 调用。
3. 确认重置 → Toast + 结果弹窗展示密码。
4. 同页冻结/删除 confirm 仍正常。
5. `/admin/brands`、`/admin/tile-categories` 启停 confirm 仍正常。

## 不在 scope

- `ResetPasswordDialog` 内容与复制逻辑变更
- API / pytest（无后端变更）
