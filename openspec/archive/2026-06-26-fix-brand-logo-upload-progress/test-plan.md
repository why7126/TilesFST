## Test Plan

## 1. Automated Tests

| 类型 | 命令 | 验证点 |
|---|---|---|
| Web Vitest | `cd src/web && npx vitest run src/features/admin/components/BrandFormModal.test.tsx` | 上传中状态、进度反馈、成功预览、失败重试、同文件重选 |
| Web Vitest 回归 | `cd src/web && npx vitest run src/pages/admin/BrandManagementPage.test.tsx` | 品牌列表、弹窗入口、既有状态提示与 Logo 展示不回退 |
| Web build | `cd src/web && npm run build` | TypeScript 与生产构建不回退 |
| Backend pytest | `pytest src/backend/tests/test_admin_brands.py` | 如上传接口或媒体链路有变更，则验证上传 MIME、URL 可访问与权限边界 |
| Orval | `./scripts/generate-openapi-client.sh` | 仅当 API schema 或响应字段变化时执行 |

## 2. Manual Checks

| 检查 | 步骤 | 期望 |
|---|---|---|
| 上传进度 | 编辑品牌 → 更换 Logo → 选择图片 | Logo 控件附近展示进度反馈 |
| 成功预览 | 等待上传完成 | 弹窗 Logo 预览更新为新图片 |
| 保存回显 | 保存品牌并重新打开编辑弹窗 | 回显最新 Logo |
| 失败重试 | 模拟上传失败或选择非法文件 | 显示错误，允许重新选择 |
| 同文件重选 | 失败后再次选择同一文件 | 可重试或明确提示 |

## 3. Regression Scope

- 品牌查询、重置、分页、每页显示切换。
- 品牌新增、编辑、启用、停用、删除。
- `BUG-0003` 已修复的 Logo 可访问 URL、列表/弹窗回显与 toast 非位移不得回退。
- admin / employee / store_owner 权限边界不得回退。

## 4. Not Required

- 不需要数据库迁移测试：本 change 不新增字段。
- 不需要小程序专项测试：本 change 不直接修改小程序。
- 默认不需要 Orval：除非实现阶段改变上传 API schema。
