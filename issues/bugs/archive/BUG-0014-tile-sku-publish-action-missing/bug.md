---
bug_id: BUG-0014-tile-sku-publish-action-missing
title: SKU 列表已下架行缺少「上架」操作入口
severity: high
status: draft
owner: product
discovered_at: 2026-06-27 12:03:34
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: add-tile-sku-management
suggested_fix_change: fix-tile-sku-publish-action-missing
---

# 缺陷说明

瓷砖 SKU 列表页（`/admin/tile-skus`）中，状态为 **已下架**（`DISABLED`）的行操作列未展示「上架」或「恢复」按钮，运营无法从列表直接恢复上架。后端 `POST /api/v1/admin/tile-skus/{id}/publish` 已实现且可用；缺陷限定于前端操作列条件渲染逻辑。

与 BUG-0001（类目停用行缺少「启用」）同类，但机制不同：本缺陷对 `DISABLED` 状态显式渲染 `null`，而非与删除条件错误绑定。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（local 或 Docker 均可）。
2. 进入「瓷砖 SKU」列表页（`/admin/tile-skus`）。
3. 找一条 **已上架** SKU，点击「下架」，确认状态变为 **已下架**；或筛选「已下架」找到既有行。
4. 观察该行「操作」列。
5. （对照）同页找 **草稿** 或 **待完善** 行，确认是否展示「上架」；进入「瓷砖类目」列表，确认 **已停用** 行展示「启用」。

# 期望结果

- **已下架** SKU 行 MUST 展示「上架」或「恢复」操作，使运营可从列表调用 publish 恢复上架。
- 操作列结构：**编辑**、**上架/恢复**、**删除**（删除仍按 `canDeleteTileSku` 独立控制）。
- 与 `REQ-0006-tile-sku-management` AC-018、AC-037、FR-007 及 `business-flow.md` §6 上下架/恢复流程一致。
- 行为对齐类目管理页（BUG-0001 已修复）：非上架状态行始终有恢复入口，删除按钮独立判断。

# 实际结果

- **已下架** 行仅展示：**编辑**、**删除**（删除可点，因非 `PUBLISHED`）。
- **不展示**：**上架** / **恢复**。
- **草稿 / 待完善** 行正常展示「上架」；**已上架** 行正常展示「下架」。

根因代码（`TileSkuManagementPage.tsx` 操作列）：

```tsx
{item.status === 'PUBLISHED' ? (下架) : item.status !== 'DISABLED' ? (上架) : null}
```

当 `status === 'DISABLED'` 时错误渲染为 `null`。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖 SKU 列表 | 已下架 SKU 无法从 UI 恢复上架 |
| 角色 | `admin`、`employee`（同页写操作） |
| 后端 / API | 无变更需求；`publish_sku` 不限制来源 status |
| 数据库 | 无数据损坏 |
| 店主端 / 小程序 / 目录 | 间接影响：下架 SKU 无法通过管理端 UI 重新曝光 |
| 关联需求 | REQ-0006-tile-sku-management（`add-tile-sku-management` 实现范围） |
| 关联缺陷 | BUG-0001（同类对称问题，已修复，可作参考） |

# 严重等级说明

严重程度为 **high**。

理由：

- **阻断核心运营流程**：SKU 下架后无法通过列表恢复上架，须直接调 API 或无法操作。
- 与 REQ-0006 明确要求的上架/恢复能力不符，属功能缺失而非纯视觉问题。
- 后端能力已就绪，修复成本低（前端条件渲染 + 单测），但业务影响面大。
- 非生产 hotfix 场景（本地/Docker 开发环境），应走常规 `fix-*` OpenSpec change。

# 修复建议（供 bug-complete / bug-opsx）

1. `TileSkuManagementPage.tsx`：非 `PUBLISHED` 行（含 `DISABLED`）展示 publish 操作；`DISABLED` 文案优先「恢复」，其余非上架态可用「上架」（与 AC-037 一致）。
2. 补充 vitest：mock `DISABLED` 行应存在「恢复」或「上架」文案；`PUBLISHED` 行仍为「下架」。
3. 可选：后端集成测试补充 `DISABLED → publish → PUBLISHED` 路径（非必须，API 逻辑已覆盖）。
4. OpenSpec：`fix-tile-sku-publish-action-missing`，父 change 为 `add-tile-sku-management`。

# 临时绕过

通过 Swagger 或 curl 调用 `POST /api/v1/admin/tile-skus/{id}/publish`（须满足主图与必填项校验）。
