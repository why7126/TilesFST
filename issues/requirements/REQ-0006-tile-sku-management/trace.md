---
title: 需求追踪
purpose: REQ-0006 瓷砖SKU管理分析与追溯
content: 关联文档、影响分析、建议 Change、原型映射
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态或迭代变更时同步更新
owner: product
status: in_sprint
note: /req-review approved
readiness: ready
---

# 需求追踪

## 1. Requirement Readiness Report

| 检查项 | 结果 |
|---|---|
| `requirement.md` | ✓ v4 |
| `capture.md` | ✓ /req-complete 补录 |
| `user-stories.md` | ✓ 本次补齐 US-001 ~ US-004 |
| `business-flow.md` | ✓ 本次补齐 |
| `acceptance.md` | ✓ 本次补齐 AC-001 ~ AC-056 |
| `trace.md` | ✓ 本文件 |
| `prototype/web/tile-sku-management-list.html` | ✓ v4 |
| `prototype/web/tile-sku-create-modal.html` | ✓ v4 |
| `prototype/web/*-context.md` | ✓ v4 |
| `prototype/images/*.png` | ○ 可选（Golden Reference，非必须） |
| 状态 / 优先级 / 来源 | ✓（见 §2） | — 评审已通过；v4 HTML 原型为视觉验收主依据；PNG 为可选增强，不阻塞 req-opsx / opsx-apply / archive。

原型优先级（AGENTS.md / design.md）：

```text
1. prototype/web/*.html          ← 主 gate
2. prototype/web/*-context.md
3. acceptance.md
4. rules/ui-design.md
5. prototype/images/*.png        ← 可选 Golden Reference，非必须
6. openspec/specs/
```

---

## 2. 基本信息

```yaml
requirement_id: REQ-0006-tile-sku-management
requirement_name: tile-sku-management
requirement_type: 管理端 / 主数据
priority: P0
status: in_sprint
owner: product
source: ui-design.md + admin-home 框架 + tile-sku v4 HTML 原型
version: v4
target_users:
  - 后台运营
  - 后台管理员
  - 只读账号
target_clients:
  web_admin: 本期实现
  web_catalog: 下游消费（已上架 SKU）
  wechat_miniapp: 不涉及
iteration: sprint-002
change_type: Feature
suggested_change_id: add-tile-sku-management
openspec_changes:
  - change_id: add-tile-sku-management
    type: add
    status: applied
    requirement_id: REQ-0006-tile-sku-management
    strategy: css-port
    iteration: sprint-002
related_requirements:
  - REQ-0004-admin-home
  - REQ-0005-brand-management
  - REQ-0005-tile-category-management
related_changes:
  - add-admin-home
  - add-brand-management
  - add-tile-category-management
lifecycle:
  captured: 2026-06-20
  generated: null
  completed: 2026-06-20
  reviewed: 2026-06-20
  approved: 2026-06-20
```

---

## 3. Requirement Analysis

### 业务目标

建立瓷砖 SKU 商品主数据管理能力，支撑品牌/类目关联、规格参数、参考价格、多图主图、多视频素材与上下架；在 admin-home 框架下提供一致的后台运营体验。

### 核心能力

| ID | 能力 |
|---|---|
| FR-001 | SKU 列表、多维筛选、分页 |
| FR-002 | 四指标卡（总数/已上架/待完善/草稿） |
| FR-003 | 新增/编辑弹窗（880px，无状态字段，默认草稿） |
| FR-004 | 多图上传与主图指定 |
| FR-005 | 多视频上传与管理 |
| FR-006 | 参考价格（元）录入与列表格式化 |
| FR-007 | 上下架 / 恢复 |
| FR-008 | 条件删除（非已上架且无引用） |
| FR-009 | 权限与 API 鉴权 |
| FR-010 | 素材完整度筛选与展示 |

### 与现有 schema 差距（实现参考）

当前 `tiles` 表含 name、model、category_id、color、size、description、status；`tile_images` 已含 `is_main`。

**预期扩展**（opsx design 定稿）：

- `model` → 对齐 SKU 编码（sku_code）或新增字段
- 新增 brand_id、surface_finish、color_family、reference_price
- 视频元数据表或 media 关联
- status 枚举：published / draft / needs_completion / disabled

### 非功能需求

| 维度 | 要求 |
|---|---|
| UI | CSS Port + semantic token；Sidebar 264px；列表 1120px 内容宽 |
| 媒体 | MinIO 单桶 + 前缀；见 rules/media.md |
| 安全 | 管理端 RBAC；上传走后端授权 |
| 性能 | 列表分页默认 20；骨架屏加载 |

---

## 4. 文档关联

| 文档 | 路径 | 状态 |
|---|---|---|
| 需求 PRD | `requirement.md` | ✓ v4 |
| 用户故事 | `user-stories.md` | ✓ |
| 业务流程 | `business-flow.md` | ✓ |
| 验收标准 | `acceptance.md` | ✓ |
| 列表 HTML | `prototype/web/tile-sku-management-list.html` | ✓ |
| 弹窗 HTML | `prototype/web/tile-sku-create-modal.html` | ✓ |
| 列表 context | `prototype/web/tile-sku-management-list-context.md` | ✓ |
| 弹窗 context | `prototype/web/tile-sku-create-modal-context.md` | ✓ |
| 列表 PNG | `prototype/images/tile-sku-management-list.png` | **可选** |
| 弹窗 PNG | `prototype/images/tile-sku-create-modal.png` | **可选** |

---

## 5. FR → AC 映射（摘要）

| FR | 主要 AC |
|---|---|
| FR-001 | AC-007 ~ AC-018 |
| FR-002 | AC-005 ~ AC-006 |
| FR-003 | AC-022 ~ AC-030 |
| FR-004 | AC-031 ~ AC-034 |
| FR-005 | AC-035 ~ AC-036 |
| FR-006 | AC-015、AC-026 |
| FR-007 | AC-037 |
| FR-008 | AC-038 ~ AC-039 |
| FR-009 | AC-004、AC-044 |
| FR-010 | AC-011、AC-016、AC-034 |

---

## 6. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-20 | `/req-complete` | 补齐 capture、user-stories、business-flow、acceptance、trace；status → pending_review |
| 2026-06-20 | 原型入库 | v4 列表 HTML + 新增弹窗 HTML + context（先于六件套存在） |
| 2026-06-20 | `/req-review --approve` | 评审通过；写入 review.md；status → approved |
| 2026-06-20 | `/req-opsx` | 创建 OpenSpec change `add-tile-sku-management` |
| 2026-06-20 | 纳入 sprint-002 | `/sprint-propose`；status → in_sprint |

---

## 7. 后续动作

1. ~~**`/req-review REQ-0006-tile-sku-management --approve`**~~ → 已通过（2026-06-20）
2. ~~**`/req-opsx REQ-0006-tile-sku-management`**~~ → 已创建 `add-tile-sku-management`（2026-06-20）
3. **`/opsx-apply add-tile-sku-management`**（sprint-002 队列；依赖 brand + category apply 完成）
4. 导出 `prototype/images/*.png`（**可选**；HTML 并排验收即可）
