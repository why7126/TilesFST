---
review_id: REV-REQ-0016-001
date: 2026-06-28
participants: []
result: approved
created_at: 2026-06-28 11:10:00
updated_at: 2026-06-28 11:10:00
---

# 评审结论

**REQ:** REQ-0016-banner-management  
**结果:** approved  
**评审日期:** 2026-06-28

## 摘要

管理后台 Banner 管理需求文档完整（PRD v1）。交付范围含：`/admin/banners` 列表页、按跳转类型分化的新增/编辑弹窗（SKU 详情 / 外部链接 / 专题页 / 无跳转）、`banners` + 最小 `topics` 种子表、MinIO Banner 上传、上线/下线/删除（弹窗不含状态字段）、Dashboard 快捷入口落地。五件套 + 列表/四套弹窗 HTML、PNG Golden、context 齐全。探索阶段建议（单弹窗 jump_type 分支、`time_status` 计算字段、SKU 图库引用 `tile_images`）与 PRD 一致。建议 OpenSpec `add-banner-management`。准予 `/req-opsx` 与 Sprint 纳入。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确（不含消费端展示、类目页跳转创建、专题 CRUD、外链白名单引擎、过期 job）
- [x] 验收标准可测试（AC-001～AC-052：列表、四套弹窗、API、数据、媒体、视觉 trace）
- [x] 优先级与依赖合理（P1；父 REQ-0004；依赖 REQ-0006 SKU 图库；模式参考品牌/REQ-0008 确认）
- [x] UI 类：prototype HTML + PNG + context 已决；优先级 HTML > PNG > context > acceptance
- [x] 无与现有 REQ 重复未说明（补全 REQ-0004 占位；与品牌/类目为模式复用）

## 亮点

- 跳转类型按弹窗分化有完整原型与 context，降低视觉验收歧义。
- 状态在列表维护、弹窗不展示状态策略块 — 与品牌/规格主数据模式一致。
- SKU 详情路径明确 `image_source` 与 `tile_images` 引用，避免重复上传。

## 风险与备注

| 项 | 说明 |
|---|---|
| 消费端不可验 | 本期无店主 Web/小程序 Banner 展示，上线后仅能验管理端配置 |
| SKU 图库 UI | 选 SKU 后拉图库并切换预览 — 前端工作量高于纯上传 |
| 状态 vs 时间状态 | `time_status` 与 `status` 双维度须在 OpenSpec design 定稿计算规则 |
| topics 种子 | 仅 migration 种子 + 只读 API；专题内容另 REQ |
| 类目页 badge | 列表样例可出现「类目页」但不可创建 — 实现页勿误导运营 |

## 条件通过项

- [ ] OpenSpec `tasks.md` 含列表 + 四套弹窗 PNG 并排验收 checklist
- [ ] `req-opsx` design.md 声明单 `BannerFormModal` + jump_type 条件字段策略
- [ ] `.env.example` 同步 Banner 上传前缀（若新增 `MINIO_PREFIX_BANNERS` 或 uploads 路由）
- [ ] `time_status` 筛选/展示规则在 delta spec 与 acceptance 对齐一种实现

## 下一步

1. `/req-opsx REQ-0016-banner-management`
2. `/sprint-propose` 纳入迭代（P1，工作量约 1 周量级）
3. `/opsx-apply add-banner-management`
