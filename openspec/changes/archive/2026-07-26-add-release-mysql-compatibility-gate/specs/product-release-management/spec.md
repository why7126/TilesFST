---
created_at: 2026-07-21 10:35:42
updated_at: 2026-07-21 10:35:42
---

# product-release-management Specification Delta

## MODIFIED Requirements

### Requirement: 发布前校验门禁
发布流程 SHALL 在必填发布就绪检查通过前阻断发布确认；若某项不适用，必须明确标记不适用并说明理由。

#### Scenario: 数据库变更门禁
- **WHEN** 发布范围包含数据库变更
- **THEN** 发布门禁 SHALL 要求提供迁移、数据库文档和回滚说明证据。
- **AND** 发布门禁 SHALL 要求提供目标 MySQL 兼容性证据，例如 MySQL schema drift 检查或目标 MySQL smoke 检查。
- **AND** 若缺少 MySQL 兼容性证据，发布准备 SHALL 失败。
