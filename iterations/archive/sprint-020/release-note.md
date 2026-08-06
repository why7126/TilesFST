---
sprint_id: sprint-020
status: published
created_at: 2026-08-05 09:55:00
updated_at: 2026-08-06 08:21:16
---

# Sprint 020 Release Note

## 计划发布内容

- 管理端 SKU 列表和 Banner 列表优先展示缩略图，降低图片密集列表加载成本。
- 品牌和证书列表复核既有缩略图优先策略，统一 image fallback 验收口径。
- 同步管理端 API 响应字段、OpenAPI、Orval 与相关测试。
- 管理后台系统设置支持全局缩略图目标体积上限；默认不限制，启用后影响新生成缩略图，历史对象需维护作业显式重生成。
- 小程序移除电话拨打、复制门店微信号和复制证书文件链接的残留隐私接口能力，支持提审时“未采集用户隐私”口径复核。
- Mintlify 文档站完成信息架构、版本入口、任务入口与公开安全校验收口。

## 不包含

- 不改变数据库结构。
- 不新增小程序电话、剪贴板、客服或文件分享能力。
- 不改变店主 Web 展示。
- 不新增视频缩略图、PDF 首页缩略图或历史媒体批量补齐能力。

## 发布状态

```yaml
publish_status: published
related_requirements:
  - REQ-0098-admin-media-list-thumbnails
  - REQ-0100-mintlify-docs-site-ia-content-experience
  - REQ-0099-global-thumbnail-size-limit
related_changes:
  - optimize-admin-media-list-thumbnails
  - improve-mintlify-docs-site
  - update-global-thumbnail-size-limit
related_bugs:
  - BUG-0117-miniapp-privacy-clipboard-phone-drift
```
