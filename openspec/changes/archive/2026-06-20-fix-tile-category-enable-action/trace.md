# fix-tile-category-enable-action — Trace

## 关联

| 字段 | 值 |
|---|---|
| bug_id | BUG-0001-tile-category-enable-missing |
| iteration | sprint-002 |
| related_requirement | REQ-0005-tile-category-management |
| parent_change | add-tile-category-management |
| type | fix |

## 修复 Checklist

| # | 项 | Pass |
|---|-----|------|
| 1 | 停用+SKU=0：编辑、启用、删除（可点） | [x] |
| 2 | 停用+SKU>0：编辑、启用；删除置灰 | [x] |
| 3 | 启用：编辑、停用；无删除 | [x] |
| 4 | 点击启用后 Toast + 列表/树刷新 | [x] vitest enableCategory mock |
| 5 | vitest AC-009/AC-010 | [x] |
| 6 | 弹窗/树/筛选无回归 | [x] 未改其他逻辑 |

## 验证命令

```bash
cd src/web && npx vitest run src/pages/admin/TileCategoryManagementPage.test.tsx  # pass 3/3
cd src/web && npm run build  # pass
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/admin/tile-categories  # 200
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-20 | `/opsx-apply` | 修复操作列；新增 vitest；build 通过 |
| 2026-06-20 | `/opsx-archive` | 归档（--skip-specs；父 add 未 archive） |
