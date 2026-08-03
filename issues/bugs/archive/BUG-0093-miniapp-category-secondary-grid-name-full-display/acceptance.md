---
bug_id: BUG-0093-miniapp-category-secondary-grid-name-full-display
status: done
created_at: 2026-07-30 23:05:45
updated_at: 2026-07-31 00:08:23
---

# 验收标准

## AC-001 二级类目卡片列数

WHEN 用户进入微信小程序分类页并选择任意一级类目
THEN 右侧二级类目卡片 MUST 每行显示 2 个
AND 加载态 skeleton 的列数 MUST 与实际二级类目卡片保持一致。

## AC-002 类目名称完整展示

WHEN 二级类目名称包含 4 字以内、5-8 字、超过 8 字、数字规格和中文描述组合
THEN 分类页二级类目卡片 MUST 完整展示名称
AND MUST NOT 使用省略号、截断或隐藏溢出的方式省略类目名称。

## AC-003 长文本布局稳定

WHEN 二级类目名称自然换行到多行
THEN 文本 MUST 保持在当前卡片内
AND MUST NOT 遮挡相邻卡片、一级类目列表、当前一级类目标题或“查看全部商品”入口
AND 页面滚动与点击区域 MUST 保持可用。

## AC-004 分类入口行为不变

WHEN 用户点击任意二级类目卡片
THEN 小程序 MUST 进入对应二级类目的商品列表页
AND 路由参数 MUST 保持 `categoryId`、`categoryName`、`categoryLevel=secondary` 和 `sourcePage=category` 的现有语义。

## AC-005 多端回归

WHEN 在微信开发者工具、iOS 真机、Android 真机和窄屏设备验证分类页
THEN 二级类目卡片列数、名称完整展示和点击入口行为 MUST 一致可用。

## AC-006 非影响范围

WHEN 修复该缺陷
THEN 不应变更分类接口响应结构、数据库类目表结构、商品列表排序规则、品牌页、搜索页或首页商品卡片布局。
