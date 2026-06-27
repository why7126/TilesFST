---
bug_id: BUG-0011-tile-sku-modal-content-overflow
status: pending_review
created_at: 2026-06-27 09:17:24
updated_at: 2026-06-27 09:17:24
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 弹窗卡片约束高度但未分配可滚动内容区

`tile-sku-management.css` 中 `.sku-modal-card` 已设置：

```css
max-height: calc(100vh - 64px);
display: flex;
flex-direction: column;
overflow: hidden;
```

弹窗结构为 `modal-head` + `modal-body` + `modal-footer`（见 `TileSkuFormModal.tsx`）。其中 **`.modal-body` 未配置** `flex: 1`、`min-height: 0` 与 `overflow-y: auto`，导致 flex 子项按内容自然撑开，超出部分被父级 `overflow: hidden` 裁切。

### 1.2 SKU 表单内容高度天然超过常见视口

SKU 弹窗字段多于品牌/用户弹窗：

- 双列 `sku-form-grid`（10+ 基础字段）
- 全宽 SKU 图片 5 列缩略图网格 + 上传入口
- 全宽 SKU 视频文件卡片列表 + 上传按钮
- 全宽备注 textarea

在 1080p 非全屏、DevTools 占用高度或笔记本常见视口下，总内容高度超过 `calc(100vh - 64px)`，底部区块不可见。

### 1.3 滚轮事件无法作用于被裁切区域

用户滚轮/触控板滚动作用于页面或遮罩层，弹窗内容区无独立滚动容器，因此无法访问被裁切的表单项与部分 footer 按钮。

## 2. 根本原因

### 2.1 实现未满足 REQ-0006 AC-022

`acceptance.md` **AC-022** 明确要求：弹窗 `max-height` 不超过视口，**主体可滚动**。当前实现仅完成 max-height 约束，遗漏主体滚动，属于对验收条款的实现缺口。

### 2.2 长表单弹窗 flex 布局模式未在 SKU 场景落地

管理端弹窗通用样式（`user-management.css` 的 `.modal-body`）仅定义 padding，未统一长表单场景的 flex + scroll 模式。SKU 弹窗引入专属 `.sku-modal-card` 时复制了 `overflow: hidden` 约束，但未同步补齐「固定头尾 + 可滚动 body」的完整模式。

### 2.3 add-tile-sku-management 开发时未覆盖矮视口验收

Change 实现聚焦字段与 API 对齐，未在 1440×1024 以下或 DevTools 打开等矮视口场景验收弹窗可操作性，导致布局缺陷进入联调/产品验收阶段才暴露。

## 3. 触发条件

满足以下条件可稳定复现：

1. admin 登录 Web 管理端，访问 `/admin/tile-skus`。
2. 打开「新增SKU」或「编辑」弹窗。
3. 浏览器视口高度不足以容纳完整表单（典型：窗口高度 ≤ 900px，或 1080p 浏览器非最大化）。
4. 表单含图片/视频区块（默认即存在上传区 DOM）。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 主要修复面 | `tile-sku-management.css` + `TileSkuFormModal` 弹窗布局 |
| 关联需求条款 | REQ-0006 AC-022 |

## 5. 后续修复建议

1. 为 `.sku-modal-card .modal-body`（或等价内容 wrapper）增加 `flex: 1; min-height: 0; overflow-y: auto;`。
2. 保持 `.modal-head`、`.modal-footer` 不参与滚动，确保标题与操作按钮始终可达。
3. 在 768px～1080px 视口高度下手工验收新增/编辑弹窗全字段可访问。
4. 建议 Change 命名：`fix-tile-sku-modal-content-overflow`（`fix-*` 类型，关联 REQ-0006）。
5. 补充组件测试：断言 modal-body 存在 scroll 相关 class 或 computed style（可选 Vitest + RTL）。
