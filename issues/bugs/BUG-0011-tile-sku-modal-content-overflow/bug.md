---
bug_id: BUG-0011-tile-sku-modal-content-overflow
title: SKU新增/编辑弹窗内容溢出且无垂直滚动条
severity: high
status: draft
owner: product
discovered_at: 2026-06-27 08:56:54
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 缺陷说明

瓷砖 SKU 新增/编辑弹窗（`TileSkuFormModal`）在常规视口下，表单内容（含备注、SKU 图片、SKU 视频等区块）总高度超出弹窗可视区域。弹窗卡片虽设置了 `max-height`，但内容区未启用内部滚动，底部字段被裁切且**无法通过滚动访问**，用户在未放大窗口或较小分辨率下无法完成完整表单填写与保存操作。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local 或 Docker 均可）。
2. 进入「瓷砖SKU」列表页（`/admin/tile-skus`）。
3. 点击「新增SKU」或某行「编辑」，打开 SKU 弹窗。
4. 保持浏览器窗口为常见高度（如 1080p 非全屏，或 DevTools 打开时视口更矮）。
5. 自顶向下查看表单：基础字段 → 参考价格 → SKU 图片上传区 → SKU 视频上传区 → 备注说明。
6. 尝试使用鼠标滚轮、触控板或键盘在弹窗内滚动。
7. 观察底部字段与「取消 / 保存草稿 / 保存」操作区是否均可访问。

# 期望结果

- 弹窗整体 `max-height` 约束视口（如 `calc(100vh - 64px)`），**页眉**（标题/副标题/关闭）与**页脚**（操作按钮）保持可见或按 Design System 长表单弹窗规范固定。
- **内容区**（`modal-body`）在内容超出剩余高度时 MUST 出现垂直滚动条（`overflow-y: auto`），用户可滚动访问全部字段与上传控件。
- 滚动行为不影响遮罩层与 ESC/点击外部关闭交互。
- 对齐 REQ-0006 弹窗原型 `tile-sku-create-modal.html` 的可操作性与管理端其他长表单弹窗体验。

# 实际结果

- 弹窗卡片 `.sku-modal-card` 使用 `overflow: hidden` 且 flex 列布局，但 `.modal-body` 未设置 `flex: 1`、`min-height: 0` 与 `overflow-y: auto`。
- 表单字段较多（双列 grid + 图片 5 列 grid + 视频列表 + 备注 textarea）时，底部内容超出可视范围。
- 弹窗内无有效垂直滚动，用户看不到或无法操作底部字段与部分 footer 区域。
- 在含媒体上传区的创建/编辑场景下，构成**可用性阻塞**，而非单纯视觉问题。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / SKU 新增弹窗 | 无法完整填写并保存新 SKU |
| Web 管理端 / SKU 编辑弹窗 | 无法访问底部字段（备注、媒体区等） |
| REQ-0006 验收 | 阻塞 `add-tile-sku-management` 弹窗 AC 的人工验收 |
| 后端 / API | 无直接影响（纯前端布局） |
| 数据库 | 无直接影响 |

# 严重等级说明

严重程度为 `high`。

理由：

- **阻塞核心业务流程**：SKU 主数据创建/编辑在常见视口下不可完成。
- 影响范围明确且可稳定复现（长表单 + `overflow: hidden` 布局）。
- 不涉及数据损坏或安全边界，但优先级应高于 UI 一致性类 medium 缺陷（如 BUG-0009/0010）。
- 修复面集中：前端弹窗布局与 CSS，预计不涉及 API 或 schema 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| SKU 弹窗组件 | `src/web/src/features/admin/components/TileSkuFormModal.tsx` |
| 弹窗布局 DOM | `.sku-modal-card` → `.modal-head` + `.modal-body` + `.modal-footer` |
| 弹窗样式（`max-height` / `overflow: hidden`） | `src/web/src/features/admin/styles/tile-sku-management.css`（`.sku-modal-card`） |
| 列表页入口 | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 弹窗原型 | `issues/requirements/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html` |
| 父需求 | `issues/requirements/REQ-0006-tile-sku-management/` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（实现未满足可用性预期） |
| 根因类型 | frontend-ui（弹窗 flex 布局缺少可滚动内容区） |
| 建议修复 | `.modal-body` 增加 `flex: 1; min-height: 0; overflow-y: auto;`，必要时对齐品牌/用户弹窗长表单模式 |
