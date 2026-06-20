# add-tile-sku-management — Trace

## 变更摘要

- **REQ**: `REQ-0006-tile-sku-management`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `tile-sku-management-list.html` + `tile-sku-create-modal.html` v4）
- **Depends**: `add-admin-home`；`add-brand-management`；`add-tile-category-management`
- **Iteration**: `sprint-002`
- **Status**: applied（待 archive）

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0006-tile-sku-management/requirement.md` |
| 验收 | `issues/requirements/REQ-0006-tile-sku-management/acceptance.md` |
| 列表 HTML | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-management-list.html` |
| 列表 PNG | `issues/requirements/REQ-0006-tile-sku-management/prototype/images/tile-sku-management-list.png`（**可选**） |
| 弹窗 HTML | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html` |
| 弹窗 PNG | `issues/requirements/REQ-0006-tile-sku-management/prototype/images/tile-sku-create-modal.png`（**可选**） |
| Design | `openspec/changes/add-tile-sku-management/design.md` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 内容区 1120px vs admin 1080px | 以 SKU HTML 为准；`:has(.sku-page-hero) .content-inner { max-width: 1120px }` |
| 弹窗无状态、默认草稿 | HTML 与 PRD 一致 |
| 保存草稿 vs 创建SKU | design D8：校验级别不同，均默认 DRAFT |
| PNG 缺失 | HTML 为 gate；PNG 可选，不阻塞 |
| sku_code vs model | 新增 sku_code，迁移 model |

## 视觉 Diff Checklist（1440×1024）

验收方式：2026-06-20 代码/CSS Port 结构对照 HTML v4 + Docker 路由冒烟（Web 200、API 401 未认证）。

### 列表页（tile-sku-management-list.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Shell 264px + 1fr | pass | 复用 `AdminLayout` + `admin-home.css` |
| 2 | Sidebar「瓷砖SKU」active | pass | `admin-nav.ts` path `/admin/tile-skus` |
| 3 | eyebrow OPERATIONS / SKU + 标题「瓷砖SKU」 | pass | `TileSkuManagementPage` page-hero |
| 4 | 主按钮「＋ 新增SKU」品牌金 | pass | `btn primary` |
| 5 | 4 指标卡（总数/已上架/待完善/草稿） | pass | summary API 驱动 |
| 6 | 筛选：关键词+品牌+类目+状态+素材完整度+查询/重置 | pass | 五维 + 查询按钮（非自动防抖） |
| 7 | 表格列：SKU信息/品牌类目/规格工艺/参考价格/素材/状态/时间/操作 | pass | 8 列对齐 |
| 8 | SKU信息含 44×44 主图缩略图+名称+编码 | pass | `.sku-thumb` 44px |
| 9 | 参考价格 `¥ xx.xx` 品牌金 | pass | `formatReferencePrice` |
| 10 | 素材 badge：主图已设/缺主图 + N图/M视频 | pass | `mini-badge` |
| 11 | 状态徽章四态 | pass | PUBLISHED/DRAFT/NEEDS_COMPLETION/DISABLED |
| 12 | 分页左「共 N 条」+ 右页码与每页条数 | partial | 左合计+右 pageSize 10/20/50/100；页码简化为 prev/active/next（功能等价） |
| 13 | 主内容 max-width 1120px | pass | `tile-sku-management.css` override |
| 14 | 默认排序更新时间倒序 | pass | API `ORDER BY updated_at DESC` |

### 弹窗（tile-sku-create-modal.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 15 | 遮罩暗色半透明 | pass | `modal-backdrop` |
| 16 | 弹窗宽 880px | pass | `.sku-modal-card { width: 880px }` |
| 17 | 标题含「创建后默认草稿」 | pass | `.default-note` |
| 18 | 无状态字段 | pass | status 仅列表 publish/unpublish |
| 19 | 字段顺序与 HTML 一致 | partial | 表面工艺为 input 非 select（业务可接受） |
| 20 | 参考价格（元）Label | pass | |
| 21 | 多图网格+主图标签+设为主图 | pass | upload-grid + main-flag |
| 22 | 多视频卡片+继续添加 | pass | video-list + 上传按钮 |
| 23 | 底栏：取消/保存草稿/创建SKU | pass | create 模式三按钮 |
| 24 | 头尾固定、body 可滚动 | pass | flex column + modal-body overflow |

## Docker 冒烟（7.2）

| 检查 | 结果 |
|---|---|
| `./scripts/docker-up.sh` | pass |
| `GET http://localhost:3000/admin/tile-skus` | 200 |
| `GET http://localhost:8000/api/v1/admin/tile-skus`（无 token） | 401（路由已挂载） |

## 验证命令

```bash
cd src/backend && uv run pytest tests/ -k tile_sku
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/generate-openapi-client.sh
./scripts/docker-up.sh
```

## 错误码（实现参考）

| 码 | 场景 |
|---|---|
| 30031 | SKU 编码重复 |
| 30032 | 非法删除（已上架） |
| 30033 | 上架条件不满足 |
