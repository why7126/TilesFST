# add-tile-category-management — Trace

## 变更摘要

- **REQ**: `REQ-0005-tile-category-management`
- **Iteration**: `sprint-002`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `tile-category-management.html` + `tile-category-management-add.html`）
- **Depends**: `add-admin-home`（AdminLayout）；参考 `add-user-management` / `add-brand-management`
- **Status**: proposed

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0005-tile-category-management/requirement.md` |
| 验收 | `issues/requirements/REQ-0005-tile-category-management/acceptance.md` |
| 列表 HTML | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.html` |
| 列表 PNG | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management.png`（待补齐） |
| 弹窗 HTML | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management-add.html` |
| 弹窗 PNG | `issues/requirements/REQ-0005-tile-category-management/prototype/web/tile-category-management-add.png`（待补齐） |
| Design | `openspec/changes/add-tile-category-management/design.md` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 无导出 | HTML 与 PRD 一致 |
| 工具栏仅调整排序 | 一致；reorder 本期占位 |
| 删除仅停用+SKU=0 | 一致 |
| 弹窗 560px 单列 + Switch 状态 | 以 HTML 为准 |
| 树 SKU 汇总 | 含子级汇总 |
| PNG 缺失 | 先 HTML 并排 |

## 视觉 Diff Checklist（1280×1024）

### 列表页（tile-category-management.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Shell 264px + 1fr | | |
| 2 | Sidebar「瓷砖类目」active | | |
| 3 | eyebrow CATEGORY MANAGEMENT + 标题 | | |
| 4 | 主按钮「＋ 新增类目」品牌金 | | |
| 5 | 无导出、无批量 | | |
| 6 | 4 指标卡（总数/启用/绑定SKU/最大层级3） | | |
| 7 | 检索：名称编码+状态+层级+查询+重置 | | |
| 8 | work-grid：树 280px + 表格 | | |
| 9 | 树节点 level-2/3 缩进与 tree-count | | |
| 10 | 工具栏仅「调整排序」 | | |
| 11 | 表格列：名称/层级/排序/SKU/状态/时间/操作 | | |
| 12 | 名称副行 path 展示 | | |
| 13 | 删除仅停用且 SKU=0 行 | | |
| 14 | 分页 10/20/50 | | |
| 15 | 主内容 max-width 1080px | | |

### 弹窗（tile-category-management-add.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 16 | 遮罩暗色半透明 + blur | | |
| 17 | 弹窗宽 560px 居中 | | |
| 18 | 六字段单列：上级/名称/编码/排序/描述/状态 | | |
| 19 | 上级类目 help 文案 | | |
| 20 | Switch「新增后立即启用」 | | |
| 21 | 取消 + 保存类目按钮 | | |
| 22 | 头尾固定布局 | | |

## 验证命令

```bash
cd src/backend && uv run pytest tests/ -k tile_categor
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/generate-openapi-client.sh
./scripts/docker-up.sh
```

## 错误码（实现参考）

| 码 | 场景 |
|---|---|
| `CATEGORY_CODE_DUPLICATED` | 编码重复 |
| `CATEGORY_DELETE_FORBIDDEN` | 非法删除 |
| `CATEGORY_MAX_DEPTH_EXCEEDED` | 超过三级 |
| `CATEGORY_INVALID_SORT_ORDER` | 排序非正整数 |
| `CATEGORY_NOT_FOUND` | id 不存在 |
