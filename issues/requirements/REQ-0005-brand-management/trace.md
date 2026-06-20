---
title: 需求追踪
purpose: REQ-0005-brand-management 分析与追溯（含 /requirement-to-change 产出）
content: 关联文档、影响分析、建议 Change、测试映射
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态或迭代变更时同步更新
owner: product
status: proposed
note: 瓷砖品牌管理；OpenSpec add-brand-management 已创建
readiness: ready
---

# 需求追踪

## 1. Requirement Readiness Report

| 检查项 | 结果 |
|---|---|
| `requirement.md` | ✓ v7 |
| `user-stories.md` | ✓ 本次补齐 |
| `business-flow.md` | ✓ 本次补齐 |
| `acceptance.md` | ✓ 本次补齐 AC-001 ~ AC-039 |
| `trace.md` | ✓ 本文件 |
| `test-plan.md` | ✓ 本次补齐 |
| `prototype/web/brand-management.html` | ✓ V7 |
| `prototype/web/brand-management-modal.html` | ✓ V7 |
| `prototype/web/*-context.md` | ✓ |
| `prototype/web/*.png` | ✗ 待导出 Golden Reference |
| 状态 / 优先级 / 负责人 / 来源 | ✓（见 §2） |

**结论：Ready** — 可 `/opsx-apply`；PNG golden reference 待补齐后升级视觉 gate。

> **编号说明**：本项目 `REQ-0005-*` 含多个子需求（`user-management`、`brand-management`、`tile-category-management` 等），以完整目录名区分。

---

## 2. 基本信息

```yaml
requirement_id: REQ-0005-brand-management
requirement_name: brand-management
requirement_type: 管理端 / 主数据
priority: P0
status: in_sprint
owner: product
source: admin-home V5 + brand-management HTML V7 原型
target_users:
  - 后台运营
  - 后台管理员
target_clients:
  web_admin: 本期实现
  web_catalog: 下游消费（停用品牌隐藏）
  wechat_miniapp: 不涉及
iteration: sprint-002
change_type: Feature
suggested_change_id: add-brand-management
openspec_changes:
  - change_id: add-brand-management
    type: add
    status: applied
    iteration: sprint-002
    requirement_id: REQ-0005-brand-management
    strategy: css-port
related_requirements:
  - REQ-0004-admin-home
  - REQ-0005-user-management
related_changes:
  - add-admin-home
  - add-user-management
```

---

## 3. Requirement Analysis

### 业务目标

建立瓷砖品牌主数据管理能力，支撑 SKU 关联、前台展示与搜索筛选；在 admin-home 框架下提供一致的后台运营体验。

### 用户

- **后台运营**：日常维护品牌资料、排序、Logo、启停。
- **后台管理员**：同运营，并受 RBAC 约束。

### 核心能力

| ID | 能力 |
|---|---|
| FR-001 | 品牌列表、关键词与状态筛选、分页跳页 |
| FR-002 | 四指标卡（总数/启用/停用/未关联 SKU） |
| FR-003 | 新增/编辑弹窗（固定字段顺序与校验） |
| FR-004 | 启用 / 停用 |
| FR-005 | 条件删除（SKU=0 且停用） |
| FR-006 | 每页显示数 20/50/100 |
| FR-007 | Logo 上传（MinIO） |
| FR-008 | 权限点 brand:* |

### 非功能需求

| 维度 | 要求 |
|---|---|
| 安全 | 管理端 JWT；删除与写操作服务端二次校验 |
| 性能 | 列表分页；sku_count 可冗余或子查询 |
| 兼容 | CSS Port + semantic token；与用户管理分页一致 |
| 可维护性 | brands 表 + admin API + Orval 客户端 |

---

## 4. Impact Analysis

```yaml
impact:
  backend: true       # brands CRUD、enable/disable、delete 校验
  web: true           # BrandManagementPage、BrandFormModal、样式
  miniapp: false
  admin: true
  database: true      # brands 表、迁移
  storage: true       # Logo → MinIO brands/ 前缀
  api: true           # GET/POST/PUT/DELETE + enable/disable
  algorithm: false
  test: true          # pytest + vitest
  docs: true          # docs/03-api-index.md、docs/04-database-design.md
  design_system: true # 管理端列表/弹窗；/design-system 可选预览
```

---

## 5. 功能映射与代码基线

| 功能 | PRD | 现状 |
|---|---|---|
| 品牌列表页 | §3 ~ §10 | 无页面；`admin-nav` 中「瓷砖品牌」无 `path` |
| 品牌 API | §13 | 后端无 brand 模块 |
| brands 表 | §13 | schema 无 brands 表 |
| Logo 上传 | §11 | 可复用 `uploads` 模式 |

| 模块 | 路径 | 动作 |
|---|---|---|
| 导航 | `src/web/src/features/admin/data/admin-nav.ts` | 为 brand 增加 `path: '/admin/brands'` |
| 路由 | `src/web/src/app/App.tsx` | 注册 BrandManagementPage |
| 页面 | `src/web/src/pages/admin/BrandManagementPage.tsx` | **新建** |
| 弹窗 | `src/web/src/features/admin/components/BrandFormModal.tsx` | **新建** |
| API | `src/backend/app/api/v1/admin_brands.py` | **新建** |
| 模型 | `src/backend/app/models/brand.py` | **新建** |
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
| 列表原型 HTML | `prototype/web/brand-management.html` | ✓ |
| 列表原型说明 | `prototype/web/brand-management-context.md` | ✓ |
| 弹窗原型 HTML | `prototype/web/brand-management-modal.html` | ✓ |
| 弹窗原型说明 | `prototype/web/brand-management-modal-context.md` | ✓ |
| 列表 PNG | `prototype/web/brand-management.png` | 待补齐 |
| 弹窗 PNG | `prototype/web/brand-management-modal.png` | 待补齐 |

---

## 7. 视觉验收 Trace Checklist

- [ ] Sidebar 激活「瓷砖品牌」
- [ ] 无导出、无批量、无多余标题行
- [ ] 4 指标卡
- [ ] 筛选一行四控件
- [ ] 删除按钮四态矩阵与 tooltip
- [ ] 分页含每页 20/50/100
- [ ] 弹窗 720px、字段顺序、Logo/介绍通栏
- [ ] HTML 原型并排验收；PNG 补齐后 Golden Reference 验收

---

## 8. 工作量与 Sprint 建议

| 项 | 预估 |
|---|---|
| Story Points | 8 ~ 13 SP |
| 人天 | 5 ~ 8 人天 |
| 建议 Sprint | **sprint-002**（已纳入） |

**风险**

- SKU 模块未实现时 `sku_count` 需约定（默认 0 或占位字段）。
- 删除策略（物理 vs 软删除）须在 OpenSpec design 定稿。
- PNG 缺失可能影响视觉验收节奏，可先用 HTML 并排。

---

## 9. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-15 | 需求入库 | requirement + HTML 原型 V7 |
| 2026-06-16 | `/requirement-to-change` | 补齐 user-stories / business-flow / acceptance / trace / test-plan |
| 2026-06-16 | `/requirement-to-opsx` | 创建 `add-brand-management` OpenSpec |
| 2026-06-16 | 纳入 sprint-002 | 更新 `iterations/sprint-002/` 四件套与本 trace |

---

## 10. 后续动作

1. 导出 `brand-management.png`、`brand-management-modal.png` 至 `prototype/web/`。
2. **`/opsx-apply add-brand-management`** → 实现 + 测试 + Orval。
3. Sprint 002 结束前验收并 **`/opsx-archive add-brand-management`**。
