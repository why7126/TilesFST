## Context

- **BUG**: `BUG-0027-tile-spec-list-ui-inconsistency`、`BUG-0028-tile-spec-modal-form-layout`、`BUG-0029-tile-spec-list-not-refresh-after-create`
- **Severity**: medium（0027/0028）、high（0029）
- **Root cause type**: design / frontend-ui（0027/0028）、code / frontend-logic（0029）
- **Related REQ**: `REQ-0009-tile-spec-management`
- **Parent Change**: `add-tile-spec-management`
- **Target files**: `TileSpecManagementPage.tsx`、`TileSpecFormModal.tsx`、`tile-spec-management.css`

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/review/BUG-0027-.../acceptance.md
2. issues/bugs/review/BUG-0028-.../acceptance.md
3. issues/bugs/review/BUG-0029-.../acceptance.md
4. issues/requirements/review/REQ-0009-.../prototype/web/tile-size-management.html
5. issues/requirements/review/REQ-0009-.../prototype/web/tile-size-management-modal.html
6. openspec/changes/add-tile-spec-management/specs/web-client/spec.md（基线 requirement）
7. rules/ui-design.md
8. UserManagementPage / BrandManagementPage（分页黄金参考）
```

## Bug Analysis Report

### BUG-0027 — 列表分页与字号

- 分页使用 `pagination-bar` / `page-indicator`，无 CSS 定义，与用户管理页 `.pagination` 结构不一致。
- `.size-name` 13px + `--admin-text`，同表 td 12px + `--admin-muted`，主列视觉权重过高。

### BUG-0028 — 弹窗布局

- JSX 顺序：宽/长 → 厚度/排序 → 尺寸名称 → 备注；规范：宽/长 → 尺寸名称 → 厚度/排序 → 备注。
- `.form-full` 已跨列，但缺 `.textarea { width: 100%; height; resize: none }` port。
- **非缺陷**：只读 preview 显示 `600×1200mm` 符合 AC-021，MUST NOT 去掉 `mm`。

### BUG-0029 — 保存后不刷新

- `onSuccess={setNotice}` 仅 Toast；启停/删除路径已调用 `loadSpecs()`。
- 与 `BrandManagementPage` / `TileSkuManagementPage` 模式不一致。

## Root Cause（摘要）

| ID | BUG | 结论 |
|---|---|---|
| RC-001 | 0027 | 分页 invent 非标准 DOM，未参照 BUG-0002/0009 已验收模式 |
| RC-002 | 0027 | `.size-name` 从原型 port 时放大字号，未对齐管理端列表 rhythm |
| RC-003 | 0028 | 弹窗 JSX 字段顺序未对照 AC-019 / modal HTML |
| RC-004 | 0028 | CSS port 遗漏 textarea 宽度/高度规则 |
| RC-005 | 0029 | `onSuccess` 复制不完整，遗漏 `loadSpecs()` |
| RC-006 | 0029 | 缺少「保存后 UI 同步」前端测试 gate |

## Goals / Non-Goals

**Goals:**

- 分页 DOM/视觉与用户管理页一致（0027 AC-001～002）。
- 尺寸名称列字号与同表协调（0027 AC-003）。
- 弹窗字段顺序与备注整行（0028 AC-001～003）。
- 保存后列表 + summary 自动刷新（0029 AC-001～004）。
- Vitest 覆盖关键路径；change trace 记录并排验收。

**Non-Goals:**

- 修改 `buildDisplayName()` 或去掉 `mm` 后缀。
- 后端 API / migration / sku_count 逻辑变更。
- AC-021 宽长冲突 inline 提示（0028 AC-010 可选，本 change SHOULD 延后 unless 容量允许）。

## Decisions

### D1：合并三 BUG 为单一 fix change

- **决策**：`fix-tile-spec-admin-ui` 一次 touch 列表页 + 弹窗 + CSS。
- **理由**：共享文件、同 Sprint、减少重复 PR；各 BUG acceptance 仍可独立勾选。

### D2：分页对齐 UserManagementPage

- **决策**：复制 `page-summary` + `page-buttons` + `page-size-wrap` 结构；删除 `pagination-bar`。
- **理由**：与 BUG-0009 修复模式一致；REQ-0009 AC-042 要求复用品牌/用户管理分页模式。

### D3：`.size-name` 调整为 12px 或与 `.user-main` 同等层级

- **决策**：优先 12px + `--admin-text`（或 13px 仅当与 user-main 并排验收通过）。
- **理由**：用户反馈与同表数值列对比明显偏大；BUG-0027 acceptance 要求 rhythm 协调。

### D4：弹窗字段重排 + textarea port

- **决策**：移动尺寸名称 block；在 `.tile-spec-form-grid` 作用域补 `.input,.textarea{width:100%}` 与 textarea 固定高度、`resize:none`。
- **理由**：对齐 prototype modal HTML 与 `brand-management.css` `.brand-textarea` 模式。

### D5：onSuccess 双回调

```tsx
onSuccess={(message) => {
  setNotice(message);
  void loadSpecs();
}}
```

- **理由**：与 Brand/TileSku 一致；保持当前页码（loadSpecs 默认不传 overridePage）。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| `add-tile-spec-management` 未 archive，web-client delta 合并顺序 | fix change 依赖同一 requirement 标题；archive 时先 add 后 fix |
| 0028 AC-010 冲突提示未做 | tasks 明确 optional；不阻塞 0027/0029 |
| 筛选下新建 ENABLED 规格不可见 | 0029 AC-006 已定义预期行为 |

## Migration Plan

- 无数据迁移；前端 deploy 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（三 BUG approved，acceptance 已明确）。
