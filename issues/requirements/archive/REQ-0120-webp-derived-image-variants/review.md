---
review_id: REV-REQ-0120-001
requirement_id: REQ-0120-webp-derived-image-variants
date: 2026-08-22
reviewed_at: 2026-08-22 21:51:08
participants:
  - product
result: approved
created_at: 2026-08-22 21:51:08
updated_at: 2026-08-22 21:51:08
---

# 需求评审

## 评审结论

通过。REQ-0120 在已归档父需求 `REQ-0115-media-multi-variant-images` 的三规格图片模型基础上，收敛 `thumbnail` 与 `display` 派生图的格式策略为 WebP，目标明确、边界清晰、验收可测试，可进入 Sprint 规划。

## 评审清单

- [x] 范围清晰，Out of Scope 明确：不强制转换原图、不引入 AVIF、不新增前端直传、不自动重建历史对象。
- [x] 验收标准可测试：已覆盖 JPEG/PNG/WebP 上传、特殊格式跳过、WebP key/MIME 一致、端侧 fallback、历史维护和脱敏输出。
- [x] 优先级与依赖合理：优先级 P1，依赖 `REQ-0115` 三规格模型、`REQ-0118` 端侧消费矩阵、`REQ-0119` display 体积配置。
- [x] UI 类原型或实现策略已决：本需求复用既有上传和图片展示入口，不新增独立页面；已提供 `prototype/web/context.md` 策略说明。
- [x] 无与现有 REQ 重复未说明：与父需求差异为“派生图格式统一 WebP”，不是重复建设三规格模型。

## 条件通过项

- [ ] OpenSpec 阶段需确认是否仅复用现有 `thumbnail_url`、`display_url`、`original_url` 字段；若接口示例或 Schema 变化，必须同步 OpenAPI、Orval、API 文档和测试。
- [ ] OpenSpec 阶段需确认是否不新增数据库字段；若记录派生对象状态、尺寸、MIME 或体积，必须同步 SQLite/MySQL schema、迁移和数据库文档。
- [ ] 历史对象 WebP 补生成的 apply 执行必须在生产备份确认和执行窗口明确后进行。

## 下一步建议

先纳入 Sprint，再创建 OpenSpec Change。
