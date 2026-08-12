---
change_id: update-miniapp-recall-pinned-product-badge
status: applied
created_at: 2026-08-08 09:36:33
updated_at: 2026-08-08 10:25:00
---

# 任务清单

## 1. 后端与 API

- [x] 1.1 在小程序公开商品记录或映射层保留当前列表实际生效的召回置顶状态。
- [x] 1.2 在 `MiniappProductCard` 或等价响应 Schema 中新增布尔字段，建议字段名为 `is_recall_pinned`，默认 false。
- [x] 1.3 确保普通商品列表和搜索 SKU 结果中实际生效的置顶商品返回 true。
- [x] 1.4 确保新品商品列表、热销商品列表和不应用置顶逻辑的入口返回 false 或不触发展示。
- [x] 1.5 同步 OpenAPI、Orval 和相关接口文档。

## 2. 小程序

- [x] 2.1 更新商品卡片类型定义，兼容缺少置顶字段的旧响应。
- [x] 2.2 调整商品卡片 badge 归一化逻辑，实现“置顶 > 新品 > 热销 > 下架”的展示优先级。
- [x] 2.3 复用现有角标区域展示固定文案“置顶”，避免新增页面、弹窗或说明文案。
- [x] 2.4 确认普通商品列表、搜索 SKU 结果、新品榜和热销榜入口表现符合验收边界。
- [x] 2.5 同步小程序 TS 与 JS 运行产物。

## 3. 测试与校验

- [x] 3.1 增加后端测试：普通商品列表实际置顶商品返回 `is_recall_pinned: true`。
- [x] 3.2 增加后端测试：搜索 SKU 结果实际置顶商品返回 `is_recall_pinned: true`。
- [x] 3.3 增加后端测试：新品榜和热销榜不返回置顶展示状态。
- [x] 3.4 增加小程序静态测试：置顶字段为 true 时展示“置顶”，缺省或 false 时不展示。
- [x] 3.5 回归测试加载更多不重复、不错位、不做端侧跨页重排。
- [x] 3.6 运行 `python scripts/validate-openspec-language.py`。

## 4. 文档同步

- [x] 4.1 如 API 响应字段变更，同步 `docs/03-api-index.md` 相关小程序接口说明。
- [x] 4.2 如 Orval 生成物变化，说明生成命令与影响范围。
- [x] 4.3 在 Change trace 或验收记录中引用 `REQ-0104`、`sprint-022` 和小程序商品列表排序 best practice。
