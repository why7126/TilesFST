---
title: 需求追踪
purpose: REQ-0005-tile-category-management 分析与追溯（含 /requirement-to-change 产出）
content: 关联文档、影响分析、建议 Change、测试映射
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态或迭代变更时同步更新
owner: product
status: in_sprint
note: add-tile-category-management 已 archive（2026-06-20）；web-client spec 已含 BUG-0001 fix 场景
readiness: ready
---

# 需求追踪

## 1. Requirement Readiness Report

| 检查项 | 结果 |
|---|---|
| `requirement.md` | ✓ v2 本次增强 |
| `user-stories.md` | ✓ 本次补齐 |
| `business-flow.md` | ✓ 本次补齐 |
| `acceptance.md` | ✓ 本次补齐 AC-001 ~ AC-043 |
| `trace.md` | ✓ 本文件 |
| `test-plan.md` | ✓ 本次补齐 |
| `prototype/web/tile-category-management.html` | ✓ V2 |
| `prototype/web/tile-category-management-add.html` | ✓ V2 |
| `prototype/web/prototype-context-list.md` | ✓ |
| `prototype/web/prototype-context-add.md` | ✓ |
| `prototype/web/*.png` | ✗ 待导出 Golden Reference |
| 状态 / 优先级 / 负责人 / 来源 | ✓（见 §2） |

**结论：Partially Ready** — 文档与 HTML 原型齐全，可进入 `/requirement-to-opsx`；视觉验收前建议补齐 list/add PNG。

> **编号说明**：本项目 `REQ-0005-*` 含多个子需求（`user-management`、`brand-management`、`tile-category-management` 等），以完整目录名区分。

---

## 2. 基本信息

```yaml
requirement_id: REQ-0005-tile-category-management
requirement_name: tile-category-management
requirement_type: 管理端 / 主数据
priority: P0
status: in_sprint
owner: product
source: admin-home V5 + tile-category-management HTML V2 原型
target_users:
  - 后台运营
  - 后台管理员
target_clients:
  web_admin: 本期实现
  web_catalog: 下游消费（停用类目隐藏）
  wechat_miniapp: 不涉及
iteration: sprint-002
change_type: Feature
suggested_change_id: add-tile-category-management
openspec_changes:
  - change_id: add-tile-category-management
    type: add
    status: archived
    iteration: sprint-002
    requirement_id: REQ-0005-tile-category-management
    strategy: css-port
related_requirements:
  - REQ-0004-admin-home
  - REQ-0005-user-management
  - REQ-0005-brand-management
related_changes:
  - add-admin-home
  - add-user-management
```

---

## 3. Requirement Analysis

### 业务目标

建立最多三级的瓷砖类目主数据管理能力，支撑 SKU 归属、前台目录与筛选导航；在 admin-home 框架下提供类目树 + 列表联动的一致运营体验。

### 用户

- **后台运营**：维护类目树、排序、启停、编码与描述。
- **后台管理员**：同运营，并受 RBAC 与深度/删除规则约束。

### 核心能力

| ID | 能力 |
|---|---|
| FR-001 | 四指标卡（总数/启用/绑定SKU/最大层级） |
| FR-002 | 类目检索（名称编码、状态、层级） |
| FR-003 | 类目树与列表联动 |
| FR-004 | 新增/编辑弹窗（560px 单列字段） |
| FR-005 | 启用 / 停用 |
| FR-006 | 条件删除（SKU=0 且停用） |
| FR-007 | 分页与每页 10/20/50 |
| FR-008 | 调整排序入口（工具栏） |
| FR-009 | 三级深度校验 |
| FR-010 | 权限点 category:* |

### 非功能需求

| 维度 | 要求 |
|---|---|
| 安全 | 管理端 JWT；删除与写操作服务端二次校验 |
| 性能 | 树 + 列表分页；sku_count 可冗余或子查询 |
| 兼容 | CSS Port + semantic token；与用户/品牌管理一致 |
| 可维护性 | 扩展 tile_categories 表 + admin API + Orval |

---

## 4. Impact Analysis

```yaml
impact:
  backend: true       # tile-categories CRUD、tree、enable/disable、delete
  web: true           # TileCategoryManagementPage、CategoryFormModal、树组件
  miniapp: false
  admin: true
  database: true      # tile_categories 表扩展、迁移
  storage: false      # 本期无图片上传
  api: true           # GET tree/list、POST/PUT/DELETE、enable/disable
  algorithm: false
  test: true          # pytest + vitest
  docs: true          # docs/03-api-index.md、docs/04-database-design.md
  design_system: true # 管理端树+列表+弹窗；/design-system 可选预览
```

---

## 5. 功能映射与代码基线

| 功能 | PRD | 现状 |
|---|---|---|
| 类目列表页 | §4 ~ §9 | 无页面；`admin-nav` 中「瓷砖类目」无 `path` |
| 类目 API | §13 | 后端无 tile-category admin 模块 |
| tile_categories 表 | §13 | schema 仅 id+name 桩 |
| 类目树 | §8 | 无实现 |

| 模块 | 路径 | 动作 |
|---|---|---|
| 导航 | `src/web/src/features/admin/data/admin-nav.ts` | 为 category 增加 `path: '/admin/tile-categories'` |
| 路由 | `src/web/src/app/App.tsx` | 注册 TileCategoryManagementPage |
| 页面 | `src/web/src/pages/admin/TileCategoryManagementPage.tsx` | **新建** |
| 弹窗 | `src/web/src/features/admin/components/CategoryFormModal.tsx` | **新建** |
| 树 | `src/web/src/features/admin/components/CategoryTree.tsx` | **新建**（或内联） |
| API | `src/backend/app/api/v1/admin_tile_categories.py` | **新建** |
| 模型 | `src/backend/app/models/tile_category.py` | **扩展** |
| 迁移 | `src/backend/app/db/schema.sql` + migrations | **扩展** |

---

## 6. 关联文档

| 文档 | 路径 | 状态 |
|---|---|---|
| PRD | `requirement.md` | ✓ |
| 用户故事 | `user-stories.md` | ✓ |
| 业务流程 | `business-flow.md` | ✓ |
| 验收标准 | `acceptance.md` | ✓ |
| 测试计划 | `test-plan.md` | ✓ |
| 列表原型 HTML | `prototype/web/tile-category-management.html` | ✓ |
| 列表原型说明 | `prototype/web/prototype-context-list.md` | ✓ |
| 弹窗原型 HTML | `prototype/web/tile-category-management-add.html` | ✓ |
| 弹窗原型说明 | `prototype/web/prototype-context-add.md` | ✓ |
| 列表 PNG | `prototype/web/tile-category-management.png` | 待补齐 |
| 弹窗 PNG | `prototype/web/tile-category-management-add.png` | 待补齐 |

---

## 7. 视觉验收 Trace Checklist

- [ ] Sidebar 激活「瓷砖类目」
- [ ] 无导出、无批量
- [ ] 4 指标卡
- [ ] 检索：名称/编码 + 状态 + 层级
- [ ] 左侧类目树 280px + 右侧列表联动
- [ ] 工具栏仅「调整排序」
- [ ] 删除仅 SKU=0 且停用行展示
- [ ] 弹窗 560px、单列六字段
- [ ] 分页含 10/20/50
- [ ] HTML 原型并排验收；PNG 补齐后 Golden Reference 验收

---

## 8. 工作量与 Sprint 建议

| 项 | 预估 |
|---|---|
| Story Points | 13 ~ 21 SP（含树+表联动，高于品牌管理） |
| 人天 | 7 ~ 10 人天 |
| 建议 Sprint | `sprint-002`（已纳入） |

**风险**

- 现有 `tile_categories` 仅为桩表，迁移需兼容未来 `tiles.category_id`。
- 类目树 SKU 汇总口径（节点自身 vs 含子级）须在 OpenSpec design 定稿。
- 「调整排序」交互未在 HTML 展开，本期可能仅占位。
- PNG 缺失影响视觉验收，可先用 HTML 并排。

---

## 9. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-15 | 需求入库 | requirement v2 + HTML 原型 V2 |
| 2026-06-16 | `/requirement-to-change` | 补齐 user-stories / business-flow / acceptance / trace / test-plan；增强 requirement 元数据 |
| 2026-06-16 | `/requirement-to-opsx` | 创建 `add-tile-category-management` OpenSpec（proposal/design/specs/tasks/trace） |
| 2026-06-16 | 纳入 sprint-002 | 更新 `sprint.yaml` / `sprint.md` / release-note / acceptance-report |
| 2026-06-20 | `/opsx-apply` | 34/37 任务完成；BUG-0001 fix 已合入代码 |
| 2026-06-20 | `/opsx-archive` | 归档至 `2026-06-20-add-tile-category-management`；specs 已 sync（含 fix 启停场景） |

---

## 10. 后续动作

1. 导出 `tile-category-management.png`、`tile-category-management-add.png` 至 `prototype/web/`（可选 PNG sign-off）。
2. ~~`/opsx-archive add-tile-category-management`~~ ✓ 已归档
