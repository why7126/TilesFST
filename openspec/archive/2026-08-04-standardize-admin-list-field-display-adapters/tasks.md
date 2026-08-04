## 任务清单

- [x] 1.1 确认 `design-system` delta spec 已包含管理端列表字段展示 adapter 检查表要求。
- [x] 1.2 在实现阶段确定检查表最终落点：Design System 文档、管理端开发文档、验收模板或组合。
- [x] 1.3 建立 image adapter 检查项，覆盖缩略图优先、主图选择、无图态、加载失败态、容器尺寸和可访问性语义。
- [x] 1.4 建立 name adapter 检查项，覆盖主名称、辅助名称、关联对象名称、空名称、长名称截断和重复字段去重。
- [x] 1.5 建立 fallback adapter 检查项，覆盖未设置、无数据、不适用、加载失败、未知枚举值、无权限和接口字段缺失。
- [x] 1.6 盘点首批列表：品牌、证书、SKU、Banner，标记已有 helper、页面内判断、样式兜底、可复用逻辑和待治理项。
- [x] 1.7 将 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 的横切 gate 写入实现或验收说明。
- [x] 1.8 若改动 Web 代码，补充 Vitest/Testing Library 或代表页面 DOM smoke；若只改文档，记录测试 N/A 理由。
- [x] 1.9 若无 API、Schema、数据库、对象存储或上传链路变更，在验收记录中明确 OpenAPI、Orval、DB、Docker Compose 均为 N/A。
- [x] 1.10 运行 OpenSpec 校验与语言校验，保存结果摘要。
