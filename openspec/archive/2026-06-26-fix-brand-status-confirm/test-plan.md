# fix-brand-status-confirm — Test Plan

## 范围

| 层级 | 文件 | 覆盖 |
|---|---|---|
| 单元/组件 | `src/web/src/pages/admin/BrandManagementPage.test.tsx` | 启停确认弹窗、API 调用时机、取消路径 |
| 构建 | `src/web` | `npm run build` |
| 手工 | `/admin/brands` | 启停确认文案、Toast、列表刷新 |

## 用例映射

| AC | 测试 |
|---|---|
| AC-001 ~ AC-002 | 点击启停先出弹窗，确认前 API 未调用 |
| AC-003 ~ AC-005 | 弹窗标题/正文/按钮 DOM 断言 |
| AC-006 | 取消/关闭后 API 未调用 |
| AC-007 | 确认后 mock enable/disable 被调用 |
| AC-009 | 删除确认仍独立（可选同文件断言） |
| AC-018 ~ AC-021 | vitest + build |

## 命令

```bash
cd src/web && npx vitest run src/pages/admin/BrandManagementPage.test.tsx
cd src/web && npm run build
```

## 非范围

- 后端 pytest（无 API 变更）
- E2E Playwright（本期 vitest 足够）
