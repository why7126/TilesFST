---
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: implemented
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 13:11:41
---

# 测试计划

## 后端

- 聚焦测试小程序首页公开 Banner：`NO_JUMP` + `internal-*` 标题不出现在公开响应。
- 聚焦测试品牌列表页公开 Banner：内部标题不出现在公开响应。
- 若 API schema 调整，运行 OpenAPI/Orval 生成并复核相关 generated 片段。

## 小程序

- 静态测试首页轮播与品牌列表页轮播不渲染 `item.title`。
- 静态测试首页轮播不包含 `hero-shade` 渐变遮罩，且 Banner 图片不设置透明化。
- 测试无跳转首页 Banner 点击静默，不显示“内容建设中”；搜索缺关键词兜底仍显示安全占位提示且不出现内部标题。
- 测试搜索 fallback、分享文案和埋点展示摘要不使用内部标题。

## 媒体验收

- 记录 Banner 图片 key/object/URL/render 四联状态。
- 小程序 DevTools、真机或体验版至少提供一种 render evidence；缺少体验版时记录 blocked 或发布前补证项。

## 文档

- 若公开 API 字段语义变化，更新 `docs/03-api-index.md`。
- 若产生可复用事故经验，更新 `docs/knowledge-base/incidents/` 或说明无需沉淀。
