---
change_id: update-admin-category-name-special-characters
status: archived
type: update
created_at: 2026-07-30 22:21:01
updated_at: 2026-07-31 00:05:01
source_requirement: REQ-0082-admin-category-name-special-characters
source_requirement_path: issues/requirements/archive/REQ-0082-admin-category-name-special-characters/
iteration: sprint-014
---

# Change Trace

## 来源

| 类型 | ID | 路径 |
|---|---|---|
| REQ | REQ-0082-admin-category-name-special-characters | `issues/requirements/archive/REQ-0082-admin-category-name-special-characters/` |

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: true
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - tile-category-management
change_type: update
expected_openspec_change: update-admin-category-name-special-characters
```

## Readiness Report

| 项 | 结论 |
|---|---|
| REQ 状态 | approved |
| 文档完整度 | Ready |
| requirement.md | 已存在 |
| user-stories.md | 已存在 |
| business-flow.md | 已存在 |
| acceptance.md | 已存在，含 7 条 AC-XCUT |
| prototype/web | 已存在 HTML + context，PNG 待导出但非阻塞 |

## Conflict Report

| 优先级 | 来源 | 结论 |
|---|---|---|
| 1 | HTML | `prototype/web/admin-category-name-special-characters.html` 定义特殊字符合法样例、控制字符错误态与列表/树展示样例 |
| 2 | PNG | 未导出，后续实现可补截图 |
| 3 | context | `prototype-context.md` 要求复用现有类目管理页、类目新增 / 编辑弹窗、列表和类目树 |
| 4 | acceptance | 功能 AC 与横切 AC 已转入 tasks 和 design |
| 5 | ui-design | 使用 semantic token 与管理端 modal/list best-practice |
| 6 | specs | 现有“类目名称输入长度上限”需通过 MODIFIED delta 将字符集放宽写入正式规则 |

## UI / PNG Checklist

- [x] 实现后补充或记录 1440px 管理端弹窗 computed width 证据：`CategoryFormModal.test.tsx` 继续校验 `.category-modal` 专属类、无 `.modal-card` 双挂载；CSS contract 保持 `width: 560px`。
- [x] 实现后补充或记录 720px 以下矮视口弹窗滚动证据：`CategoryFormModal.test.tsx` 继续校验 `.modal-body` `overflow-y: auto` 与固定 footer contract。
- [x] 实现后补充或记录管理端类目列表 / 类目树特殊字符名称展示证据：`TileCategoryManagementPage.test.tsx` 使用 `岩板-启用`、`仿古砖/停用` 样例覆盖列表与确认弹窗；`CategoryFormModal.test.tsx` 覆盖类目树父级选项与弹窗保存。
- [x] 实现后补充或记录小程序与 Web 展示端特殊字符名称布局回归证据：`tests/test_miniapp_static.py` 分类页与商品列表入口静态回归通过；`TileSkuFormModal.test.tsx` 使用 `墙砖-600×600` 覆盖 SKU 类目选择器样例。

## Validation Evidence

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-30 23:10:34 | `./scripts/generate-openapi-client.sh` | OpenAPI 导出与 Orval 生成成功 |
| 2026-07-30 23:10:34 | `uv run pytest src/backend/tests/test_admin_tile_categories.py` | 16 passed |
| 2026-07-30 23:10:34 | `pnpm --dir src/web test -- CategoryFormModal` | 56 files / 300 tests passed |
| 2026-07-30 23:10:34 | `pnpm --dir src/web test -- TileCategoryManagementPage TileSkuFormModal tile-categories-api` | 56 files / 300 tests passed |
| 2026-07-30 23:10:34 | `uv run pytest tests/test_miniapp_static.py` | 30 passed |
| 2026-07-30 23:10:34 | `openspec validate update-admin-category-name-special-characters --strict` | valid |
| 2026-07-30 23:10:34 | `python scripts/sync-workflow-status.py --event opsx.apply --change update-admin-category-name-special-characters --sprint auto` | updated 3, errors 0 |
| 2026-07-30 23:19:57 | `pnpm --dir src/web test -- CategoryTree CategoryFormModal TileCategoryManagementPage` | 57 files / 302 tests passed |

## 验收返修

| 时间 | 反馈 | 处理 |
|---|---|---|
| 2026-07-30 23:19:57 | 类目树前面的勾选框改成 `+/-`，支持类目展开和收起，默认只显示一级类目，其他级别类目默认收起。 | 已将管理端类目树改为默认折叠的递归树；有子级节点前置 `+/-` 展开按钮，展开 / 收起与类目筛选点击分离。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:05:01 | `/opsx-archive` | 归档 Change，delta spec 已合并到 `openspec/specs/tile-category-management/spec.md`，关联 REQ 已迁入 archive |
| 2026-07-30 23:19:57 | `/opsx-modify` | 验收返修类目树展开/收起交互，默认仅显示一级类目，补充组件测试与验证证据 |
| 2026-07-30 23:10:34 | `/opsx-apply` | 完成后端校验、管理端表单、OpenAPI / Orval、API/DB/错误码文档与测试回归，Change 状态更新为 applied |
| 2026-07-30 22:55:04 | `/sprint-propose` | 纳入 `sprint-014` 正式范围，关联 REQ 可进入 apply 门禁 |
| 2026-07-30 22:21:01 | `/req-opsx` | 基于 REQ-0082 创建 OpenSpec Change proposal/design/spec/tasks/trace |
