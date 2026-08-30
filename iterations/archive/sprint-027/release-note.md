---
title: sprint-027 发布说明
created_at: 2026-08-29 18:13:44
updated_at: 2026-08-30 08:42:16
---

# sprint-027 发布说明

## 范围摘要

- 纳入 REQ-0130「媒体维护任务进度输出」，目标是在生产媒体维护 CLI 中提供可选进度输出能力。
- 纳入 REQ-0131「统一媒体对象 Key 按业务对象 id 分目录」，目标是把新增与迁移媒体统一到扁平业务媒体类型目录。
- 纳入 BUG-0146「批量媒体维护命令未覆盖 Banner 自定义上传图」，目标是补齐历史 Banner `.thumb.webp` / `.display.webp` 派生图维护能力。

## 用户可见变化

- 管理端、店主 Web、小程序用户界面暂无变化。
- 运维执行媒体维护命令时，可通过可选进度输出查看任务、阶段、计数和百分比，默认 stdout JSON 兼容保持不变。
- 新上传与迁移后的媒体 object key 将优先使用 `user-avatars/{id}`、`brand-logos/{id}`、`banners/{id}`、`tiles/{id}`、`brand-certificates/{id}` 扁平目录；旧目录继续受控读取兼容，不随迁移默认删除。
- 生产 Banner 历史派生图补齐后，首页和品牌列表 Banner 普通展示应减少 fallback 原图加载。

## 技术变化

- REQ-0130 已归档 `add-media-maintenance-progress-output`，补齐媒体维护 CLI 可选进度输出和脱敏输出边界。
- BUG-0146 已归档 `fix-media-maintenance-banner-variants`，补齐 Banner 候选来源、旧无 id alias 派生图维护能力和本地 no-fallback 验收证据；生产 no-fallback 与公开 API 字段一致性补证后置到发布/运维窗口。
- REQ-0131 已归档 `update-media-object-key-business-id-layout`，不新增数据库表，复用既有媒体引用字段；上传 key 生成、formalize 和维护迁移任务已调整对象存储写入目录。

## 发布风险

- 进度输出必须保持 stdout JSON 兼容，避免影响生产脚本。
- 进度输出必须脱敏，不得泄露真实 object key、`.env`、密钥、连接串、Authorization header 或 Cookie。
- Banner 派生图修复验收不能只看 HTTP 200，必须检查 `Content-Type`、`Content-Length` 和 `x-media-fallback`。
- 扁平目录发布前需确认备份、dry-run 摘要、apply 后二次审计、旧/过渡目录兼容和端侧 render/Network evidence；旧对象清理必须另行确认。

## 状态

```yaml
sprint_id: sprint-027
status: completed
requirements:
  - REQ-0130-media-maintenance-progress-output
  - REQ-0131-media-object-key-business-id-layout
bugs:
  - BUG-0146-batch-media-maintenance-banner-variants
changes:
  - add-media-maintenance-progress-output
  - fix-media-maintenance-banner-variants
  - update-media-object-key-business-id-layout
archive_status: completed
archived_at: 2026-08-30 08:42:16
```
