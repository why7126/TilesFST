---
change_id: fix-miniapp-search-prototype-alignment
type: fix
status: proposed
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-20 22:34:18
source_bug: BUG-0066-search-component-prototype-deviation
---

# Test Plan - fix-miniapp-search-prototype-alignment

## 静态 / 单元测试

- 小程序搜索页 WXML 结构测试：输入态返回按钮和搜索框、结果态关键词标题、安全区容器。
- 搜索通用组件应用或等价行为测试：关键词、清空、提交、取消/返回、禁用态、`scope`、`sourcePage`。
- 搜索首页结构测试：最近搜索、热门搜索、单条删除和全部清空事件；不展示最近浏览。
- 联想态测试：仅展示品牌和 SKU 两组，不展示最近搜索、普通关键词、类目、规格或证书。
- 结果态测试：综合/品牌/SKU/证书 Tab、综合默认激活、`sections` 分区、最佳匹配最多 1 条，品牌/SKU/证书 Tab 不展示分区标题和数量。
- 最佳匹配测试：覆盖 SKU 直接命中优先、品牌名精确命中次之、证书名称或编号精确命中最后。
- 筛选测试：搜索结果页不展示快捷筛选、筛选按钮或筛选抽屉。
- 无结果测试：当前关键词、搜索图标、调整建议、推荐搜索词，以及联系商家/找砖/购物车/询价/在线下单入口不展示。

## 手工 / 原型对照

- 对照 `01-search-home.html/png` 验收搜索首页。
- 对照 `02-search-suggestions.html/png` 验收联想态。
- 对照 `03-search-results.html/png` 验收结果态。
- 验收搜索结果页不展示筛选抽屉、快捷筛选或筛选按钮。
- 对照 `05-search-empty.html/png` 验收无结果态。
- 在 320 到 430 pt 宽度下检查安全区、44px 搜索框、结果页关键词标题、Tab 横向滚动和卡片内容不重叠。

## 回归命令建议

```bash
pnpm --dir src/web test
```

若小程序测试脚本与 Web 测试脚本分离，执行项目中对应的小程序静态测试命令，并在 apply 输出中记录实际命令。
