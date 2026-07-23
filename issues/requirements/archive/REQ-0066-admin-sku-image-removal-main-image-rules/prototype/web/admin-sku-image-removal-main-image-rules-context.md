---
requirement_id: REQ-0066-admin-sku-image-removal-main-image-rules
title: SKU 编辑弹窗图片移除与主图规则原型上下文
status: approved
owner: product
source: acceptance.md
created_at: 2026-07-22 09:19:53
updated_at: 2026-07-22 09:24:44
---

# 原型上下文

## 1. 使用方式

本原型用于表达 SKU 编辑弹窗中商品图片区域的目标交互，不替代 `REQ-0006` 的完整 SKU 弹窗原型。后续实现应优先复用现有 `TileSkuFormModal` 结构，只调整图片网格状态逻辑。

优先级：

```text
1. prototype/web/admin-sku-image-removal-main-image-rules.html
2. 本 context.md
3. acceptance.md
4. requirement.md
5. rules/ui-design.md
```

## 2. 关键交互

- 主图始终显示在第一张。
- 非主图显示“设为主图”和移除入口。
- 主图显示“主图”标签和移除入口。
- 点击“设为主图”后，目标图片移至第一张。
- 移除主图后，下一张图片成为主图；如没有下一张，则剩余第一张成为主图。
- 移除全部图片后，只保留“继续添加图片”入口和帮助文案。

## 3. 实现提示

- 图片状态建议在前端维护为 `ImageDraft[]`，保存前统一 normalize：唯一主图、主图第一、连续 `sort_order`。
- 移除操作只改变 SKU images payload，不触发对象存储物理删除。
- 继续沿用 `sku-modal-card`，不得增加通用 `modal-card`。
- 上传失败提示留在图片区域内。

## 4. 待导出

- PNG Golden Reference：待实现或设计确认后导出；当前 HTML 可作为交互布局参考。
