---
change_id: update-miniapp-sku-detail-actionbar-compact-favorite
source_requirement: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
source_sprint: sprint-026
status: applied
created_at: 2026-08-28 14:18:04
updated_at: 2026-08-28 14:27:38
---

# Change 追踪

## 基本信息

```yaml
change_id: update-miniapp-sku-detail-actionbar-compact-favorite
source_requirement: REQ-0129-miniapp-sku-detail-actionbar-compact-favorite
source_sprint: sprint-026
change_type: fix
status: applied
affected_capabilities:
  - miniapp-sku-detail-page
affected_layers:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
product_data_collection_observability:
  status: not_applicable
  affected_layers: []
  reason: 仅调整微信小程序商品详情页底部操作栏静态 UI、收藏按钮可见文案和返回首页悬浮按钮 actionbar offset；不新增或修改 API、DB、请求日志、行为事件、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。
  validation: 已通过实现 diff 确认未修改收藏 API、SKU 详情 API、分享 open-type、请求封装、track 事件名、数据模型、OpenAPI 或 Orval；已通过 `uv run pytest tests/test_miniapp_static.py` 静态回归确认 UI 合同。
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| Readiness | ready |
| 评审状态 | `in_sprint`，已完成 `/req-review` 且纳入 `sprint-026` |
| 六件套 | `requirement.md`、`user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md`、`prototype/miniapp/*` 已具备 |
| Change 类型 | `fix`，修改既有 `miniapp-sku-detail-page` 规格 |
| 实现边界 | 仅小程序 UI 与样式；不写 `src/` 于本命令，后续由 `/opsx-apply` 实现 |

## Conflict Report

| 来源 | 结论 |
|---|---|
| `prototype/miniapp/actionbar-compact.html` | 表达底部 actionbar 紧凑布局、收藏图标状态和返回首页悬浮按钮相对位置。 |
| `prototype/miniapp/context.md` | 明确原型只表达布局策略，不代表最终像素值。 |
| `acceptance.md` | AC-001 至 AC-020 已覆盖功能、视觉、小程序证据和观测 N/A。 |
| `openspec/specs/miniapp-sku-detail-page/spec.md` | 已有收藏分享、视觉可用性和移动视口要求，本 Change 追加紧凑 actionbar 场景。 |

冲突处理：无硬冲突。若原型像素与小程序触控热区、安全区或既有样式约束冲突，优先保留触控热区、安全区避让和深色视觉一致性。

## 小程序 UI 证据清单

- [x] 320 pt 视口：静态等价摘要通过。actionbar 使用 `grid-template-columns: 112rpx minmax(0, 1fr)`，收藏按钮无可见第二行文字，按钮保留 `88rpx` 高度和动态 `aria-label`，返回首页悬浮按钮 actionbar offset 为 `154rpx + safe-area`。
- [x] 375 pt 视口：静态等价摘要通过。底栏 `min-height: 108rpx`、上下 padding 收敛到 `10rpx`，分享按钮仍为 `88rpx` 高度并保留 `open-type="share"`。
- [x] 430 pt 视口：静态等价摘要通过。页面底部留白从 `150rpx` 收敛到 `126rpx`，悬浮按钮 actionbar offset 下调后不再沿用旧 `190rpx` 高度假设。
- [x] 收藏请求中 / 失败回滚：静态测试确认 `toggleFavorite`、`previous = product.favorite`、失败回滚和 toast 路径未改；`loading="{{favoriteBusy}}"` 保留在同一 `88rpx` 按钮容器内。
- [x] Diff 复核：未修改 API、DB、Orval、请求封装、track 事件名或数据模型。

## 实现证据

| 类型 | 结论 |
|---|---|
| 聚焦测试 | `uv run pytest tests/test_miniapp_static.py::test_miniapp_home_floating_button_covers_non_home_pages_and_navigation_fallback tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states`：2 passed |
| 小程序静态回归 | `uv run pytest tests/test_miniapp_static.py`：38 passed |
| 关键样式证据 | `.actions min-height: 108rpx`、`.actions padding: 10rpx 24rpx calc(10rpx + env(safe-area-inset-bottom))`、`.action-btn height/min-height: 88rpx`、`.home-floating-area.offset-actionbar bottom: calc(154rpx + env(safe-area-inset-bottom))` |
| 视觉证据说明 | 当前环境未直接启动微信开发者工具或真机截图；已记录 320/375/430 pt 静态等价摘要。体验版或真机阶段如需截图，可在 `/opsx-archive` 前补充外部验收截图路径或人工确认。 |
| 观测边界 | 不涉及 API、DB、Orval、请求封装、行为事件、请求日志或 Task Trace。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-28 14:27:38 | `/opsx-apply` | 完成小程序商品详情页紧凑 actionbar、收藏按钮去文字、返回首页悬浮按钮 offset 调整和静态测试。 |
| 2026-08-28 14:18:04 | `/req-opsx` | 从 REQ-0129 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 与 trace。 |
