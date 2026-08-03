---
change_id: fix-admin-category-name-chinese-parentheses
type: fix
source_bug: BUG-0103-admin-category-name-chinese-parentheses
created_at: 2026-08-03 08:32:46
updated_at: 2026-08-03 08:32:46
---

# Tasks

- [x] 1. 定位管理后台类目名称前端表单校验与后端校验入口。
- [x] 2. 补齐类目名称合法字符规则，允许中文全角括号 `（`、`）`。
- [x] 3. 确认修复不放宽空名称、超长名称、同层级重复名称、换行、制表符和不可见控制字符限制。
- [x] 4. 补充或更新后端类目创建与更新接口测试，覆盖中文括号成功、英文括号不回退和非法输入拒绝。
- [x] 5. 补充或更新 Web 管理端类目表单测试，覆盖中文括号可提交和非法输入仍拦截。
- [x] 6. 验证类目树、列表、详情或选择器展示包含中文括号的名称不乱码、不截断、不撑破布局。
- [x] 7. 复核是否影响 OpenAPI / Orval；若无接口契约变化，记录不需要生成。
- [x] 8. 修复完成后评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无通用事故价值，记录不适用。

## Apply Notes

- 后端校验入口：`src/backend/app/services/tile_category_admin_service.py` `VALID_CATEGORY_NAME_RE`。
- Web 校验入口：`src/web/src/features/admin/components/CategoryFormModal.tsx` `CATEGORY_NAME_PATTERN`。
- 本次仅扩展名称合法字符集，允许中文全角括号 `（`、`）`；空名称、超长名称、同层级重复名称、换行、制表符、不可见控制字符与 `<` 等非法字符约束保持不变。
- 已补充后端创建/编辑中文括号测试与 Web 新增/编辑中文括号测试。
- 未修改 API Schema、响应字段或错误码，不需要运行 Orval。
- 该问题属于局部输入校验遗漏，无生产事故复用价值，暂不沉淀 `docs/knowledge-base/incidents/`。
