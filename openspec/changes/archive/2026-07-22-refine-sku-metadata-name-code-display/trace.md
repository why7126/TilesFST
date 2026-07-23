---
change_id: refine-sku-metadata-name-code-display
status: proposed
created_at: 2026-07-21 18:14:27
updated_at: 2026-07-22 09:56:14
source_requirement: REQ-0065-sku-metadata-name-sku-dedup
iteration: sprint-010
change_type: update
owner: product
---

# Change Trace

## 来源

- REQ: `issues/requirements/archive/REQ-0065-sku-metadata-name-sku-dedup`
- Parent REQ: `REQ-0006-tile-sku-management`
- Review: `issues/requirements/archive/REQ-0065-sku-metadata-name-sku-dedup/review.md`
- Sprint: `iterations/change/sprint-010`

## Readiness

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| Knowledge-base gate | Pass |
| Cross-cutting tags | admin-list, admin-modal |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: possible
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - tile-sku-management
    - miniapp-sku-detail-page
    - miniapp-product-list-page
    - miniapp-search
```

## Conflict Report

| Source | Finding | Resolution |
|---|---|---|
| prototype/web/sku-metadata-name-sku-dedup.html | 管理端目标态要求“商品名称”为主展示，编码为内部弱信息 | design D1/D4 采纳；tile-sku-management delta 更新列表和弹窗 |
| prototype/web/*-context.md | SKU 编码系统生成，公开端不展示 | design D2/D4 采纳；miniapp delta 隐藏编码 |
| acceptance.md | AC-XCUT 覆盖 admin-list/admin-modal | tasks 2.5、4.5 保留验收证据 |
| openspec/specs/tile-sku-management | 旧规范要求 create 校验编码 | delta 修改为后端自动生成 |
| openspec/specs/miniapp-sku-detail-page | 旧规范要求详情展示 SKU 编码 | delta 修改为不展示编码 |
| openspec/specs/miniapp-product-list-page | 旧规范允许卡片展示并要求响应包含编码 | delta 修改为 UI 不展示，响应可兼容 |
| openspec/specs/miniapp-search | 旧规范文案强调 SKU 编码 | delta 修改为后端可匹配但公开 UI 不展示 |

## Prototype / Evidence Checklist

- [x] 管理端 1440×1024 列表检查：`TileSkuManagementPage.test.tsx` 覆盖商品名称主展示、`商品名称 / SKU 编码` 搜索 placeholder、分页 DOM `page-summary` + `page-right`、fixed toast 与 DS confirm modal；已通过 focused Vitest。
- [x] 管理端 SKU 弹窗 computed width 检查：CSS 栈保留 `.admin-shell .sku-modal-card { width: 880px; max-width: calc(100vw - 32px); }`，且 `TileSkuFormModal.test.tsx` 覆盖 `sku-modal-card` 单一专属类与 CSS scroll rule；本次尝试用 Playwright 编程读取 computed width，但 `playwright` / `@playwright/test` Node module 未暴露，已记录环境限制，归档前可补 DevTools/截图证据作为增强。
- [x] 管理端矮视口弹窗滚动检查：CSS 保留 `.admin-shell .sku-modal-card .modal-body { min-height: 0; overflow-y: auto; }` 与移动端 `max-height: calc(100vh - 24px)`；`TileSkuFormModal.test.tsx` 已覆盖 scroll rule。
- [x] 小程序商品列表/详情/搜索/分享静态或设备 evidence：`tests/test_miniapp_home.py` 覆盖详情参数、分享标题与搜索建议不展示 SKU 编码；`tests/test_miniapp_static.py -k "not wechat_share_evidence"` 覆盖 WXML 不渲染 SKU 编码相关文案。
- [ ] PNG Golden Reference：optional，可在实现阶段按需导出。

## Apply Verification

| 时间 | 类别 | 命令 / 证据 | 结果 |
|---|---|---|---|
| 2026-07-22 09:28:39 | 后端与公开接口 | `uv run pytest src/backend/tests/test_admin_tile_skus.py tests/test_miniapp_home.py -q` | 47 passed |
| 2026-07-22 09:28:39 | 管理端 Web | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx src/pages/admin/TileSkuManagementPage.test.tsx` | 2 files / 17 tests passed |
| 2026-07-22 09:56:14 | 管理端 SKU 弹窗微调 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx` | 1 file / 13 tests passed；覆盖编辑弹窗不显示 SKU 编码、参考价格位于表面工艺前、图片/视频上传说明、视频卡与继续添加视频大卡片尺寸一致 |
| 2026-07-22 09:28:39 | 小程序静态 | `uv run pytest tests/test_miniapp_static.py -q -k "not wechat_share_evidence"` | 28 passed, 1 deselected；全文件仍有无关失败：`add-miniapp-wechat-share-pages/implementation/share-evidence.md` 缺失 |
| 2026-07-22 09:28:39 | OpenAPI / Orval | 检查 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` 的 `TileSkuCreateRequest` | `sku_code` 已为可选且 required 仅含 `name`，本次无需重新生成 Orval |

## 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-22 09:56:14 | UI follow-up | SKU 编辑弹窗隐藏内部 SKU 编码；调整参考价格/表面工艺顺序；补充商品图片与视频上传类型、大小和多文件说明；视频上传改为与图片一致的添加卡交互，并恢复为原大视频卡片尺寸 |
| 2026-07-22 09:28:39 | /opsx-apply | 实现后端自动 SKU 编码、管理端商品名称主展示、小程序公开端隐藏编码；完成 focused 后端/Web/miniapp 验证，弹窗 computed width 真实浏览器证据待归档前补充 |
| 2026-07-21 18:20:23 | /sprint-propose | 纳入 sprint-010，待 `/opsx-apply refine-sku-metadata-name-code-display` |
| 2026-07-21 18:14:27 | /req-opsx | 从 REQ-0065 创建 OpenSpec Change，状态 proposed |
