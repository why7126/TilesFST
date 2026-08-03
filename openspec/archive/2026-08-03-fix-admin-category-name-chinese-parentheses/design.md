---
change_id: fix-admin-category-name-chinese-parentheses
type: fix
source_bug: BUG-0103-admin-category-name-chinese-parentheses
created_at: 2026-08-03 08:32:46
updated_at: 2026-08-03 08:32:46
---

# 设计说明

## Bug Analysis Report

- 现象：管理后台瓷砖类目名称支持英文括号，但包含中文全角括号 `（`、`）` 时无法通过校验或无法正常保存。
- 复现：在类目新增或编辑弹窗输入 `墙砖（哑光）` 后保存。
- 影响：管理后台类目新增、编辑、类目名称校验、保存与展示。
- 严重等级：medium。问题不阻断全部类目维护，但影响中文业务命名录入。
- 关联需求：REQ-0005-tile-category-management。
- 关联能力：`tile-category-management` 中的类目名称输入规则。

## Root Cause

类目名称校验链路对可见特殊字符的契约不够明确。现有 spec 要求支持常见可见特殊字符，但未明确中文全角括号，导致前端表单、后端 Schema 或服务层校验可能只允许英文半角括号。

## Fix Strategy

实现阶段应优先定位类目名称统一校验入口，避免前后端各自扩散规则。修复范围应满足：

1. 前端类目新增与编辑表单允许中文全角括号。
2. 后端类目创建与更新接口允许中文全角括号。
3. 长度统计仍按用户可见字符，中文括号计入字符数。
4. 空名称、超过 15 个用户可见字符、同层级重复名称、换行、制表符和不可见控制字符仍被拒绝。
5. 类目树、列表、详情和选择器完整展示包含中文括号的名称。

## Testing Strategy

- 后端测试覆盖 `POST /api/v1/admin/tile-categories` 和 `PUT /api/v1/admin/tile-categories/{id}` 的中文括号成功路径。
- 后端测试覆盖英文括号不回退、16 字符拒绝、空白和控制字符拒绝。
- Web 测试覆盖 `CategoryFormModal` 对中文括号不显示字段级错误且允许提交。
- Web 测试覆盖非法字符和超长名称仍阻止提交。
- 如 OpenAPI schema 未变化，不需要运行 Orval；如 schema 或错误码契约变化，必须运行 `./scripts/generate-openapi-client.sh` 并同步相关文档。

## Risk

- 若直接放宽为任意字符，可能引入控制字符、换行或展示异常。
- 若只修前端或只修后端，会造成前后端校验不一致。
- 若长度统计基于 UTF-16 code unit 而非用户可见字符，中文括号相关边界可能出现误判。
