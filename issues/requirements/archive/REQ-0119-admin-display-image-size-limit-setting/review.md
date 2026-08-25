---
review_id: REV-REQ-0119-001
requirement_id: REQ-0119-admin-display-image-size-limit-setting
date: 2026-08-22 21:29:55
participants:
  - product
result: approved
created_at: 2026-08-22 21:29:55
updated_at: 2026-08-22 21:29:55
---

# 需求评审

## 评审结论

通过。REQ-0119 范围清晰，目标是将现有 display 图体积目标从代码常量升级为管理端系统设置配置，默认值沿用 768KB，并保持与缩略图体积目标独立。

本需求与 `REQ-0115-media-multi-variant-images`、`REQ-0099-global-thumbnail-size-limit` 和 `REQ-0017-system-settings` 的关系明确：它不是重新设计多规格图，也不是新增上传入口，而是补齐详情展示图体积策略的可配置能力。

## 评审清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，已覆盖系统设置 API、管理端 UI、display 图生成、维护任务、文档和测试同步。
- [x] 优先级与依赖合理，建议作为 P1 媒体治理增强进入后续 Sprint。
- [x] UI 类需求已有 prototype/context 与轻量 HTML 策略，后续 OpenSpec 实现阶段补 UI Contract、截图和 computed style evidence。
- [x] 无与现有 REQ 重复未说明；与缩略图体积目标配置保持独立边界。

## 条件通过项

- [ ] OpenSpec 设计阶段需最终确定字段名与校验范围，建议优先比较 `media.display_max_size_kb` 与 `media.display_image_max_size_kb`。
- [ ] OpenSpec 实现阶段需补齐 `/admin/settings/media` 1440×1024 视觉证据、fixed toast、恢复默认 modal、dirty 切换确认和媒体 key/object/URL/render evidence。

## 后续建议

评审通过后先纳入 Sprint，再创建 OpenSpec Change。REQ 来源链路后续命令继续使用原始 `REQ-0119`。
