## Test Plan

## 1. Automated Tests

| 类型 | 命令 | 验证点 |
|---|---|---|
| Backend pytest | `cd src/backend && uv run pytest tests/ -k "brand or upload or media"` | Logo 上传、媒体 URL 可访问、非法 MIME、object_key 安全 |
| Web Vitest | `cd src/web && npx vitest run src/pages/admin src/features/admin` | 品牌列表 Logo 渲染、品牌弹窗 Logo 回显、提示布局不推挤主体 |
| Web build | `cd src/web && npm run build` | TypeScript 与生产构建不回退 |
| Orval | `./scripts/generate-openapi-client.sh` | 仅当 API schema 或响应字段变化时执行 |

## 2. Manual Checks

| 检查 | 步骤 | 期望 |
|---|---|---|
| Logo 上传与展示 | 新增品牌上传 Logo，保存后返回列表 | 品牌列展示 Logo 图片 |
| 编辑回显 | 打开已上传 Logo 的品牌编辑弹窗 | 弹窗展示当前 Logo，支持更换并即时预览 |
| Tips 稳定性 | 在品牌列表执行启用、停用、删除、保存 | 提示出现/消失不改变页面主体纵向位置 |
| 权限 | 使用 admin/employee/store_owner 分别访问上传与品牌维护 | admin/employee 可维护，store_owner 被拒绝 |

## 3. Regression Scope

- 品牌查询、重置、分页、每页显示切换。
- 品牌新增、编辑、启用、停用、删除。
- BUG-0002 已修复的分页与 Logo 控件 UI 一致性不得回退。
- SKU 图片/视频上传不应因通用媒体访问策略受影响。

## 4. Not Required

- 不需要数据库迁移测试：本 change 不新增字段。
- 不需要小程序专项测试：本 change 不直接修改小程序，但媒体 URL 策略应保持后续可复用。
