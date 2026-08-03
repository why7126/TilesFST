---
bug_id: BUG-0097-admin-sku-material-main-image-tag-redundant
title: 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签
severity: low
status: done
owner:
discovered_at: 2026-07-31 14:19:22
environment: admin-web
related_requirement: REQ-0006-tile-sku-management
related_change: fix-admin-sku-material-main-image-tag
created_at: 2026-07-31 14:19:22
updated_at: 2026-07-31 20:54:53
---

# 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签

## 现象

管理后台瓷砖 SKU 页列表的「素材」列中，已有图片的 SKU 行会显示「主图已设」标签。当前业务规则下，只要 SKU 存在图片就会有主图，因此该标签没有提供额外判断价值，反而增加了列表扫描噪音。

## 复现步骤

1. 登录管理后台。
2. 打开「瓷砖 SKU」页面。
3. 查看任意已有图片的 SKU 行。
4. 观察「素材」列中的标签与素材数量展示。

## 期望结果

- 素材列不再显示「主图已设」标签。
- 素材列仍保留图片数量、视频数量等真正用于判断素材完整度的信息。
- 缺图或素材不完整状态仍可通过图片/视频数量识别，页面不再提供素材完整度条件筛选。

## 实际结果

- 已有图片的 SKU 行在素材列显示「主图已设」标签。
- 同一位置仍显示「1 图 / 0 视频」等数量信息，导致主图状态表达重复。
- 标签占用素材列视觉空间，降低 SKU 维护人员快速扫描素材完整度的效率。

## 影响范围

- 管理后台瓷砖 SKU 列表的素材列展示。
- SKU 维护人员查看图片、视频素材完整度的列表扫描体验。
- 可能涉及素材列渲染逻辑、素材完整度条件筛选，以及列表行高/列宽布局。

## 严重等级说明

严重等级为 `low`。该问题不影响 SKU 数据、图片主图兜底、上下架、删除或编辑流程，也不影响店主端/小程序展示；主要影响管理端列表的信息密度与维护体验。

## 附件

- `screenshots/admin-sku-material-main-image-tag-redundant.png`：管理后台瓷砖 SKU 页素材列显示冗余「主图已设」标签的截图。
