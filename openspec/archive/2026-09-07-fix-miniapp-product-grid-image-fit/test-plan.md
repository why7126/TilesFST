---
change_id: fix-miniapp-product-grid-image-fit
created_at: 2026-09-04 18:08:43
updated_at: 2026-09-04 18:08:43
---

# 测试计划

## 聚焦测试

- 运行 `python -m pytest tests/test_miniapp_static.py` 或项目当前等价小程序静态测试命令。
- 验证 `components/product-card` grid 商品图片展示模式为完整适配，不再使用填充裁切契约。
- 验证 grid 图片区域比例和骨架屏比例一致，避免加载前后布局跳动。
- 验证 compact/list 场景没有被本 Change 的断言强制改动。

## 视觉验收

- 使用小程序 DevTools 或等价截图覆盖 320、375、430 pt 逻辑宽度。
- 商品列表页、品牌详情商品 Tab、首页全部产品 grid 场景均需截图或人工验收摘要。
- 验收记录需说明证据来源和证明边界，不得写成体验版、真机或线上已通过，除非实际取得对应证据。

## 不需要执行

- 不需要 Orval。
- 不需要数据库迁移或数据库测试。
- 不需要 Docker Compose 验证。
- 不需要对象存储审计或媒体 URL smoke，除非实现阶段扩大范围。
