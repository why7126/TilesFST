## Test Plan

## 1. Automated Tests

| 类型 | 命令 | 验证点 |
|---|---|---|
| Web unit/component | `cd src/web && npx vitest run src/pages/admin src/features/admin` | 品牌页分页、品牌弹窗 Logo 上传入口、既有管理端测试 |
| Web build | `cd src/web && npm run build` | TypeScript 与生产构建不回退 |

## 2. Manual Visual Checks

| 检查 | 步骤 | 期望 |
|---|---|---|
| 分页一致性 | 打开 `/admin/brands` 与 `/admin/users` 并排对比 | 品牌页分页与用户页分页布局和视觉一致 |
| Logo 控件一致性 | 打开新增品牌弹窗与新增用户弹窗并排对比 | Logo 选择控件与头像上传控件视觉层级一致 |
| 功能冒烟 | 创建/编辑品牌并选择 Logo | 上传与保存流程可用 |

## 3. Not Required

- 不运行 Orval：API 未变更。
- 不运行后端 pytest：后端未变更。
- 不运行 Docker Compose：部署文件未变更；若验收需要可启动 Web 进行人工视觉检查。
