---
title: 临时规避
purpose: BUG-0001 修复前的 workaround
bug_id: BUG-0001-tile-category-enable-missing
status: draft
---

# 临时规避

## 1. 运营侧（无 UI）

若类目为 **停用 + SKU=0** 且必须重新启用，在修复发布前可通过 API 直接启用：

```http
POST /api/v1/admin/tile-categories/{id}/enable
Authorization: Bearer <admin_token>
```

成功返回 200 后刷新列表页，状态应变为「启用」。

## 2. 数据侧替代（不推荐）

- **不要**为「启用」目的先删除再新建同名类目：编码唯一约束可能导致冲突，且丢失原 id 关联。
- **不要**通过 SQL 直接改 `status`：绕过业务校验，且与审计/后续前台消费不一致。

## 3. 可删除行的特殊路径

对 SKU=0 的停用行，若业务上接受 **删除后重建**：

1. 点击「删除」移除类目；
2. 通过「新增类目」重新创建。

此路径 **不能**保留原 id，仅适用于无下游引用、可丢弃历史 id 的场景。

## 4. 规避有效期

- **有效期**：自 2026-06-20 起至 `fix-tile-category-enable-action` 发布并验收通过。
- **修复后**：上述 API workaround 仅作应急保留，正常流程应使用列表「启用」按钮。
