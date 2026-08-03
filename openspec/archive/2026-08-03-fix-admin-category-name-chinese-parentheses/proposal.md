---
change_id: fix-admin-category-name-chinese-parentheses
type: fix
source_bug: BUG-0103-admin-category-name-chinese-parentheses
related_requirement: REQ-0005-tile-category-management
status: proposed
created_at: 2026-08-03 08:32:46
updated_at: 2026-08-03 08:32:46
---

# 修复管理后台类目名称不支持中文括号

## Why

BUG-0103 记录了管理后台瓷砖类目名称支持英文括号但不支持中文括号 `（`、`）` 的问题。该问题会影响中文业务命名的完整表达，例如 `墙砖（哑光）` 不能正常新增或编辑保存。

现有 `tile-category-management` spec 已要求类目名称允许中文、英文、数字和常见可见特殊字符，但未显式覆盖中文全角括号，导致前端或后端实现可能只覆盖英文半角括号。

## What Changes

- 明确类目名称合法字符集 MUST 包含中文全角括号 `（`、`）`。
- 修复管理后台类目新增和编辑时对中文括号的误拦截。
- 保持既有名称长度、非空、同层级唯一、控制字符拦截和错误提示要求不变。
- 补充前后端回归测试，覆盖中文括号、英文括号和非法输入不放宽。

## Impact

- Backend: 可能涉及类目名称 Schema、服务层校验或错误处理。
- Web Admin: 可能涉及 `CategoryFormModal` 或类目表单校验。
- API: 输入兼容性扩展，不新增接口；若后端校验逻辑变化，应保留统一响应结构和稳定错误码。
- Database: 不涉及表结构变更。
- Miniapp: 不直接涉及；仅需确认展示端不会因包含中文括号的类目名称异常展示。
- Orval: 不需要，除非实现阶段意外修改 OpenAPI schema。

## Rollback Plan

如修复引入误放宽或展示异常，可回滚类目名称字符集校验改动，并保留现有英文括号行为。回滚后需重新执行中文括号、英文括号、空名称、超长名称、重复名称和控制字符测试，确认系统回到修复前行为且未破坏既有类目保存链路。
