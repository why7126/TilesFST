# fix-admin-list-status-action-confirm — Acceptance

来源：`issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/acceptance.md`

## 用户管理 confirm

- [ ] AC-001 冻结须先 confirm modal，确认后 API + Toast
- [ ] AC-002 解冻须先 confirm modal
- [ ] AC-003 取消/遮罩/× 不调用 API
- [ ] AC-004 删除使用 DS modal，禁止 `window.confirm`

## SKU 上下架 confirm

- [ ] AC-005 下架须先 confirm modal
- [ ] AC-006 上架/恢复须先 confirm modal
- [ ] AC-007 取消不调用 publish/unpublish API

## 视觉与回归

- [ ] AC-008 modal 对齐 Golden Reference（类目/品牌）
- [ ] AC-009 品牌/类目/SKU 删除 MUST NOT 回归
- [ ] AC-010 重置密码 confirm 不在 scope（BUG-0017）

## 自动化与范围

- [ ] AC-011 Vitest 确认门禁（用户 + SKU）
- [ ] AC-012 纯前端，无 Orval
- [ ] AC-013 权限边界不回归
- [ ] AC-014 Docker/本地冒烟
- [ ] AC-015 OpenSpec archive 与 trace 更新
