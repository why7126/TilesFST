---
bug_id: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
status: done
created_at: 2026-07-31 12:51:42
updated_at: 2026-07-31 21:32:14
---

# 验收标准

## AC-001 首页列表图片恢复展示

- GIVEN 微信小程序连接体验版或等价生产 API
- WHEN 用户打开首页
- THEN “新品推荐”“热销推荐”“全部产品”中有真实主图的商品卡片应展示真实商品图片
- AND 不应全部显示“暂无图片”

## AC-002 复用商品卡片入口一致

- GIVEN 分类商品列表、品牌商品列表、搜索结果页、品牌详情商品区复用商品卡片组件
- WHEN 页面加载商品列表数据
- THEN 有真实主图的商品卡片图片应正常展示
- AND 确实无主图或对象缺失的商品才允许展示“暂无图片”

## AC-003 缩略图 URL 可在小程序商品卡片展示

- GIVEN 列表接口返回商品卡片缩略图 URL
- WHEN 小程序商品卡片渲染该商品
- THEN 图片节点应正常加载并展示真实商品图片
- AND 不应因缩略图对象缺失进入“暂无图片”兜底
- AND 公开列表不得返回不可访问的缩略图 URL

## AC-004 pending 主图路径处理明确

- GIVEN 公开 SKU 主图 object key 为 `images/default/tiles/pending/<uuid>.<ext>`
- WHEN 后端生成列表 `cover_image`
- THEN 应返回同目录文件名差异化的可访问缩略图 URL
- AND 不应机械生成不可访问的 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>`

## AC-005 缩略图同路径命名规则

- GIVEN 原图对象 key 为 `images/default/tiles/pending/<uuid>.jpg`
- WHEN 系统生成或回填缩略图
- THEN 缩略图应保存在 `images/default/tiles/pending/` 同目录
- AND 缩略图文件名应与原图文件名有明确差异，能够区分原图和缩略图
- AND 不应把缩略图保存到独立 `thumbnails/default/tiles/pending/` 前缀作为最终策略

## AC-006 历史缩略图回填

- GIVEN 体验版存在公开 SKU
- WHEN 执行历史缩略图回填
- THEN 所有有原图的公开 SKU 主图均应补齐对应缩略图
- AND 回填结果应输出总数、成功数、失败数和失败原因摘要
- AND 不得输出密钥、Authorization header、Cookie、`.env` 内容或本机路径

## AC-007 数据一致性审计可定位问题

- GIVEN 体验版存在公开 SKU
- WHEN 执行商品卡片图片审计
- THEN 应输出公开 SKU 总数、无主图数量、pending 主图数量、原图对象缺失数量、缩略图对象缺失数量
- AND 审计结果应能定位到具体 SKU，但不得输出密钥、Authorization header、Cookie、`.env` 内容或本机路径
- AND 应能识别原图与同路径缩略图的匹配关系

## AC-008 性能优化不退化

- GIVEN 图片展示已恢复
- WHEN 用户打开首页并滚动商品列表
- THEN 图片加载速度优化仍应保留，首屏不应一次性加载大量非可见图片
- AND 可见区域图片应在可接受时间内显示
- AND `BUG-0092-miniapp-card-images-slow-load` 的核心验收不应回退

## AC-009 回归测试覆盖

- SHOULD 补充或更新后端测试，确认列表接口对 `images/default/tiles/pending/` 主图生成同路径可访问缩略图 URL。
- SHOULD 补充或更新缩略图生成/回填测试，覆盖新增上传和历史回填。
- SHOULD 补充或更新小程序静态测试，覆盖商品卡片图片失败兜底、`lazy-load` 保留和复用入口。
- SHOULD 补充或更新审计脚本测试或等价验证，覆盖公开 SKU 主图、pending key、原图对象和缩略图对象一致性。
