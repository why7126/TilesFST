---
change_id: fix-admin-category-name-chinese-parentheses
source_bug: BUG-0103-admin-category-name-chinese-parentheses
created_at: 2026-08-03 08:32:46
updated_at: 2026-08-03 08:32:46
---

# Test Plan

## 后端

- 运行或补充 `src/backend/tests/test_admin_tile_categories.py`。
- 覆盖创建类目名称 `墙砖（哑光）` 成功。
- 覆盖更新类目名称 `地砖（防滑）` 成功。
- 覆盖英文括号名称仍成功。
- 覆盖空名称、16 个以上用户可见字符、换行、制表符和不可见控制字符仍失败。
- 覆盖同层级重复名称仍返回稳定业务错误。

## Web 管理端

- 运行或补充 `src/web/src/features/admin/components/CategoryFormModal.test.tsx`。
- 覆盖中文括号输入不触发字段级错误且允许提交。
- 覆盖英文括号输入不回退。
- 覆盖非法字符和超长名称仍展示字段级错误并阻止提交。

## 手工回归

- 管理后台新增 `墙砖（哑光）`。
- 编辑已有类目为 `地砖（防滑）`。
- 检查类目树、列表、详情或选择器展示。
- 检查刷新页面后名称仍完整保留。

## 生成物

- 默认不需要 Orval。
- 若实现阶段修改 OpenAPI schema 或错误码契约，必须运行 `./scripts/generate-openapi-client.sh` 并同步 API 文档。
