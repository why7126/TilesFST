# fix-admin-list-status-action-confirm — Test Plan

## 单元 / 组件（Vitest）

| 用例 | 文件 | 断言 |
|---|---|---|
| 冻结先 dialog 后 API | `UserManagementPage.test.tsx` | 点击「冻结」→ `getByRole('dialog')`；确认前 `updateUserStatus` 未调用 |
| 取消冻结 | 同上 | 取消后 dialog 关闭；API 未调用 |
| 确认冻结 | 同上 | 确认后 `updateUserStatus(id, 'disabled')` |
| 删除 modal 非 confirm | 同上 | 无 `window.confirm`；删除走 modal |
| 下架先 dialog | `TileSkuManagementPage.test.tsx` | 确认前 `unpublishTileSku` 未调用 |
| 恢复/上架先 dialog | 同上 | 确认前 `publishTileSku` 未调用 |
| 品牌启停回归 | `BrandManagementPage.test.tsx` | 既有用例全 pass |
| 类目启停回归 | `TileCategoryManagementPage.test.tsx` | 既有用例全 pass |

## 构建

```bash
cd src/web && npm run build
```

## 手工冒烟

1. `admin` 登录 → `/admin/users` → 冻结 → 取消 → 再确认冻结 → 解冻 confirm。
2. 从未登录用户 → 删除 confirm modal（非浏览器 alert）。
3. `/admin/tile-skus` → 下架 / 恢复 confirm。
4. `/admin/brands`、`/admin/tile-categories` 启停/删除 confirm 仍正常。

## 不在 scope

- 重置密码 confirm UI（BUG-0017）
- API / pytest（无后端变更）
