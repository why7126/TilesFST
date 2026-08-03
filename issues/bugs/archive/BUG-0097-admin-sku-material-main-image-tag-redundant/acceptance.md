---
bug_id: BUG-0097-admin-sku-material-main-image-tag-redundant
title: 管理后台瓷砖 SKU 素材列不应显示冗余的主图已设标签
status: done
severity: low
created_at: 2026-07-31 14:56:58
updated_at: 2026-07-31 20:54:53
---

# Acceptance

## 回归验收

### AC-001 素材列只显示图片视频数量

Given 管理员进入管理后台「瓷砖 SKU」列表  
When 查看任意 SKU 的「素材」列  
Then 只显示图片数量与视频数量  
And 不显示「主图已设」「缺主图」或其他素材状态标签。

### AC-002 素材数量展示保持正确

Given 管理员进入管理后台「瓷砖 SKU」列表  
When 查看任意 SKU 的「素材」列  
Then 图片数量与视频数量仍按当前数据正确展示，例如「1 图 / 0 视频」。

### AC-003 缺图或素材不完整状态仍可识别

Given SKU 存在缺图、缺视频或素材不完整情况  
When 管理员查看素材列数量  
Then 仍能通过图片数量与视频数量识别对应素材缺失状态，不因移除素材状态标签而失去素材完整度判断能力。

### AC-004 删除素材完整度条件筛选

Given 管理员进入管理后台「瓷砖 SKU」列表  
When 查看筛选区或触发常规列表请求  
Then 不显示素材完整度条件筛选  
And 列表请求不提交 `material_completeness`。

### AC-005 列表布局不出现回归

Given 管理后台「瓷砖 SKU」列表存在不同图片/视频数量的 SKU  
When 移除素材状态标签后查看列表  
Then 素材列行高、列宽、状态列和操作列不出现遮挡、挤压或明显布局抖动。

### AC-006 SKU 维护操作不受影响

Given 管理员在「瓷砖 SKU」列表或编辑弹窗中维护 SKU  
When 执行新增、编辑、图片主图兜底、上下架、删除等操作  
Then 操作行为与修复前保持一致，且不引入接口请求或数据结构变化。
