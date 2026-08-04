---
change_id: standardize-admin-list-field-display-adapters
status: applied
created_at: 2026-08-04 08:45:39
updated_at: 2026-08-04 09:08:00
source_requirement: REQ-0095-admin-list-field-display-adapter-checklist
change_type: update
iteration: sprint-019
---

# Change Trace

## 基本信息

```yaml
change_id: standardize-admin-list-field-display-adapters
status: applied
type: update
source_requirement: REQ-0095-admin-list-field-display-adapter-checklist
requirement_path: issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/
iteration: sprint-019
capabilities:
  new: []
  modified:
    - design-system
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-018-retrospective.md
cross_cutting_tags:
  - admin-list
prototype_refs:
  - issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/prototype/web/context.md
  - issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/prototype/web/admin-list-field-adapter-checklist.html
png_checklist:
  required: false
  reason: 当前 prototype 为 HTML 策略参考；PNG Golden Reference 待后续 design 决定是否导出。
```

## Conflict Resolution

- HTML prototype 优先级最高，但本需求中的 HTML 是检查表工作台参考，不要求直接上线为生产页面。
- `acceptance.md` 的功能 AC 与横切 AC 是后续实现验收事实源。
- `rules/ui-design.md` 管理端列表约束继续生效：暗色旗舰风、semantic token、列表效率优先。
- 本 Change 更新 `design-system` spec，不拆分修改品牌、证书、SKU、Banner 多个业务 spec。

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-08-04 08:45:39 | `/req-opsx` | 从 REQ-0095 创建 OpenSpec Change，状态为 proposed |
| 2026-08-04 08:50:00 | `/sprint-propose` | 纳入 sprint-019 正式范围 |
| 2026-08-04 09:08:00 | `/opsx-apply` | 建立管理端列表字段 image/name/fallback adapter 检查表，并接入 Design System 与 docs 索引 |

## Apply 记录

### 实现摘要

- 新增 `docs/standards/admin-list-field-display-adapters.md`，定义 image/name/fallback adapter 检查项、首批品牌/证书/SKU/Banner 列表盘点、横切验收和分层验收 N/A 记录。
- 更新 `src/shared/design-system/spec.md` 与 `src/shared/design-system/README.md`，将管理端列表字段 adapter 检查表纳入 Design System 可执行说明。
- 更新 `docs/README.md`，将检查表加入 standards 索引。

### Cross-cutting Apply Gate

| 检查项 | 结果 | 说明 |
|---|---|---|
| `admin-list` acceptance | PASS | REQ-0095 已包含 AC-XCUT-ADMIN-LIST-001 至 004；实现文档显式引用对应 gate |
| `knowledge_base_refs` | PASS | 已引用并读取 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| best-practices read | PASS | 检查表纳入分页 DOM、fixed toast、DS confirm、no `window.confirm` |
| `admin-filter-dropdown` | N/A | 本 Change 不修改筛选下拉逻辑 |

Verdict: PROCEED

### 验证记录

| 命令 | 结果 | 说明 |
|---|---|---|
| `openspec validate standardize-admin-list-field-display-adapters --strict` | PASS | OpenSpec 严格校验通过 |
| `python scripts/validate-openspec-language.py` | PASS | OpenSpec 语言校验通过 |
| `python scripts/validate-design-system.py` | FAIL | 发现既有基线违规 296 项；本 Change 仅新增/更新文档与 Design System 说明，未修改 Web 运行时代码 |

### N/A 记录

- API / OpenAPI / Orval：N/A，本 Change 不新增或修改接口。
- DB / Schema / Migration：N/A，本 Change 不修改数据模型。
- Docker Compose：N/A，本 Change 不修改部署、环境变量或运行时服务。
- Web 自动化测试：N/A，本 Change 为治理文档和验收检查表，不改变页面 DOM 或交互行为。
