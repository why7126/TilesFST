---
review_id: REV-REQ-0012-001
date: 2026-06-27
participants: []
result: approved
created_at: 2026-06-27 22:20:13
updated_at: 2026-06-27 22:20:13
---

# 评审结论

**REQ:** REQ-0012-object-storage-key-layout  
**结果:** approved  
**评审日期:** 2026-06-27

## 摘要

对象存储前缀与 Object Key 生成规则优化需求文档完整。新 Key 形态 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`、语义前缀（images/videos/files/audios）、四上传 API 映射、存量迁移方案 A（一次性脚本）均已明确。验收标准 AC-001～AC-034 可测试，无 UI 变更。建议 OpenSpec `update-object-storage-key-layout`。准予 `/req-opsx` 与 Sprint 纳入。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确（files/audios 实际上传、转码、缩略图、多桶、前端直连 MinIO 均 Out）
- [x] 验收标准可测试（Key 形态、前缀映射、迁移脚本 dry-run/apply、pytest、Docker 冒烟、文档同步）
- [x] 优先级与依赖合理（P1 基础设施；依赖 REQ-0005/0006 媒体字段；与 BUG-0006～0008 存储链路衔接清晰）
- [x] 非 UI 类：prototype N/A 已在 trace 声明；实现策略（方案 A 迁移）已决
- [x] 无与现有 REQ 重复未说明（MODIFIED `object-storage` spec，非重复新能力）

## 亮点

- 废弃 `original/`、去掉 `{YYYY}/{MM}`，Key 更短且语义与 `videos/` 对齐。
- 保留 `default` 租户段，多租户扩展无需再改结构。
- `business-flow.md` 含旧→新 Key 映射表，迁移可执行性强。
- 无 API schema 变更，前端零改动；影响面集中在后端 + 脚本 + 文档。

## 风险与备注

| 项 | 说明 |
|---|---|
| 存量迁移 | 本地/演示环境 MUST 先备份 SQLite + MinIO；apply 前 dry-run 必跑 |
| 发版顺序 | 建议：迁移脚本 + Key 生成同版本发布，避免新 Key 写入与旧 DB 混存 |
| env 对齐 | apply 时须同步 `MINIO_PREFIX_*` 与代码读取，避免硬编码残留 |
| OpenSpec | delta MUST MODIFIED 现有 `object-storage` Requirement 标题一致，否则 archive 失败 |

## 条件通过项

- [ ] OpenSpec design.md 确认迁移脚本失败回滚策略（MinIO copy 失败时 DB 不更新）
- [ ] archive 时在 `docs/07-object-storage-strategy.md` 移除 deprecated `original/` 示例或仅保留迁移说明

## 下一步

1. `/req-opsx REQ-0012-object-storage-key-layout`
2. `/sprint-propose` 纳入迭代（建议 P1，与 SKU/品牌媒体验收同 Sprint 或紧随其后）
3. `/opsx-apply update-object-storage-key-layout`
