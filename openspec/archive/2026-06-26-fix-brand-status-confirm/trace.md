# fix-brand-status-confirm — Trace

## 关联

| 字段 | 值 |
|---|---|
| requirement_id | REQ-0008-brand-status-confirm |
| parent_requirement | REQ-0005-brand-management |
| parent_changes | add-brand-management |
| reference_change | fix-tile-category-management-refine（启停确认模式） |
| type | fix |
| iteration | sprint-002 |

## 视觉 Diff Checklist（1280×1024）

对照 `issues/requirements/archive/REQ-0008-brand-status-confirm/prototype/web/brand-status-confirm-context.md`。

| # | 项 | Pass |
|---|-----|------|
| 1 | 点击停用 → 确认弹窗 → 非直接 API | [x] |
| 2 | 点击启用 → 确认弹窗 → 非直接 API | [x] |
| 3 | 停用标题「停用品牌」+ 正文含前台不可见说明 | [x] |
| 4 | 启用标题「启用品牌」+ 正文仅确认意图 | [x] |
| 5 | 底部「取消」+「确认停用/确认启用」 | [x] |
| 6 | 启停确认 modal 结构同删除确认 | [x] |
| 7 | 取消/遮罩/× 不改变状态 | [x] |
| 8 | 删除仍独立确认弹窗 | [x] |

## 验证命令

```bash
cd src/web && npx vitest run src/pages/admin/BrandManagementPage.test.tsx
cd src/web && npm run build
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/admin/brands
```

## 验证结果（2026-06-26）

| 命令 | 结果 |
|---|---|
| vitest BrandManagementPage | 5/5 passed |
| npm run build | success |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 21:15:13 | `/req-opsx` | 创建 change；proposal/design/specs/tasks/trace |
| 2026-06-26 21:19:00 | `/opsx-apply` | 启停确认弹窗 + vitest 5/5 + build 通过 |
| 2026-06-26 21:24:30 | `/opsx-archive` | 归档；web-client spec +1 ADDED |
