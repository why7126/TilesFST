## Context

- **BUG**: `BUG-0011-tile-sku-modal-content-overflow`
- **Severity**: high
- **Root cause type**: code / frontend-ui
- **Related REQ**: `REQ-0006-tile-sku-management`
- **Parent change**: `add-tile-sku-management`（in-progress，34/35 tasks）
- **Target**: `TileSkuFormModal` + `tile-sku-management.css`

## Bug Analysis Report

### 现象

SKU 新增/编辑弹窗内容高度超出可视区域，底部表单项被裁切，弹窗内无垂直滚动条，用户无法完成完整表单填写。

### 复现路径

1. admin 登录，访问 `/admin/tile-skus`。
2. 打开「新增SKU」或「编辑」弹窗。
3. 视口高度 ≤900px（或 1080p 非全屏）。
4. 观察无法滚动至 SKU 图片/视频/备注区域；footer 可能不可达。

### 影响

- **阻塞** SKU 创建/编辑在常规办公视口下的可用性。
- 不影响 API、DB、权限、MinIO。
- 阻塞 REQ-0006 弹窗 AC 验收。

## Root Cause

### RC-001：flex 弹窗缺少可滚动 body

`.sku-modal-card` 设置 `max-height: calc(100vh - 64px)`、`overflow: hidden`、flex column，但 `.modal-body` 未设置 `flex: 1; min-height: 0; overflow-y: auto`，内容被父级裁切。

### RC-002：长表单高度超过常见视口

双列 grid + 图片 5 列 grid + 视频列表 + 备注 textarea 总高度天然超过矮视口剩余空间。

## Design Decisions

### D1：固定头尾 + 可滚动 body

```text
.sku-modal-card (flex column, max-height, overflow hidden)
├── .modal-head      (flex-shrink: 0)
├── .modal-body      (flex: 1; min-height: 0; overflow-y: auto)
└── .modal-footer    (flex-shrink: 0)
```

MUST NOT 让整个卡片随内容无限增高突破 `max-height`。

### D2：不扩大行为面

本 change 不修改：

- SKU API、校验规则、save_mode 逻辑。
- 字段顺序、Label、按钮文案。
- 数据库、Orval、MinIO。

### D3：验收视口矩阵

人工验收 MUST 覆盖：

| 视口 | 用途 |
|------|------|
| 1440×900 | 笔记本 |
| 1280×720 | 矮视口 |
| 1920×1080 非全屏 | 窗口高约 900px |

## Test Strategy

- Vitest + RTL：`TileSkuFormModal` 打开时 `.modal-body`（或 scroll wrapper）具备可滚动布局 class/style。
- 人工：矮视口滚动至底部，确认图片/视频/备注与 footer 可交互。
- 构建：`cd src/web && npx vitest run …`；`npm run build`。

## Risks

| 风险 | 缓解 |
|---|---|
| 双 scroll（body + 页面） | 滚动仅发生在 modal-body；遮罩不滚动 |
| footer 被挤出视口 | flex-shrink: 0 on head/footer |
| 回归 add-tile-sku-management | 不改变表单字段与 API 调用 |
