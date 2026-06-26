## Why

BUG-0002-brand-ui-inconsistency 已评审通过，确认瓷砖品牌管理页存在两处 Web 管理端 UI 一致性缺陷：

1. `/admin/brands` 品牌列表底部分页 UI 与 `/admin/users` 用户管理页分页 UI 不一致。
2. 新增/编辑品牌弹窗中的「品牌Logo」选择文件控件与管理端整体表单和上传控件风格不一致。

当前 `add-brand-management` 尚未归档，且原 add change 的视觉验收已记录为通过；根据项目规则，验收后发现的视觉/策略不达标 MUST 使用新的 `fix-*` change 修复，禁止在原 change 上无 spec 地硬改代码。

## What Changes

- 对齐品牌列表分页与用户管理页分页结构和视觉：
  - 统一总数摘要、翻页按钮、每页显示控件的布局。
  - 移除或重新设计割裂的 `page-left` / `brand-pagination-right` 表达。
  - 若保留跳页能力，作为统一分页组件/布局的可选扩展呈现。
- 对齐品牌 Logo 选择文件控件与管理端弹窗表单风格：
  - 参考用户管理弹窗头像上传控件的行内上传模式。
  - 保留 Logo 预览、选择/更换文件、帮助文案与错误反馈。
  - 不暴露浏览器默认 file input 皮相。
- 补充品牌管理页回归测试或验收记录，覆盖分页与 Logo 上传入口。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | 修改 `/admin/brands` 分页与 `BrandFormModal` Logo 选择文件控件 |
| Design System | 强化管理端分页与图片上传控件一致性 |
| API | 不变 |
| 数据库 | 不变 |
| MinIO / 媒体上传 | 上传能力不变，仅调整前端控件呈现 |
| Orval | 不需要 |
| Docker | 可选通过 Web 构建或本地页面验收确认 |

## Rollback Plan

若修复引起品牌管理页功能异常，可回滚本 change 的 Web UI 代码改动：

1. 恢复 `BrandManagementPage.tsx` 分页 DOM 与相关 CSS 到修复前状态。
2. 恢复 `BrandFormModal.tsx` Logo 上传控件与 `brand-management.css` 到修复前状态。
3. 保留 BUG 与 OpenSpec 记录，重新评估替代修复方案。

回滚不涉及 API、数据库迁移、Orval 或对象存储数据回滚。
