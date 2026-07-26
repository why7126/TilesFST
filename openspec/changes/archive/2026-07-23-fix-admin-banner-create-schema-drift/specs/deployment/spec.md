## MODIFIED Requirements

### Requirement: 生产部署文档必须包含外部 MySQL 前置检查

生产部署文档 MUST 包含客户 MySQL 前置条件检查清单，至少覆盖 MySQL 版本 8.0+、字符集 `utf8mb4`、collation `utf8mb4_unicode_ci`、账号具备 DDL + DML 权限、VPS 到 MySQL 主机和端口网络可达、生产密钥不得使用 `.env.example` 默认值。生产部署文档 MUST 包含目标 MySQL schema drift 检查步骤，且涉及 Banner 管理发布或修复时 MUST 明确检查 `banners` 表无阻塞缺列。若采用外部 MinIO 场景，文档 MUST 同时包含外部 MinIO/S3 兼容存储前置检查。

#### Scenario: 运维按文档检查 MySQL 前置条件

- **WHEN** 运维阅读 `docs/02-deployment.md` 的生产部署章节
- **THEN** MUST 找到 MySQL 8.0+、`utf8mb4`、权限、网络可达和密钥注入检查项
- **AND** MUST 找到禁止使用示例密钥的说明
- **AND** MUST 找到目标 MySQL schema drift 检查命令或等价步骤。

#### Scenario: Banner 修复发布前检查生产表结构

- **WHEN** 运维准备发布涉及 Banner 保存链路、MySQL schema 或生产迁移的修复
- **THEN** 发布材料 MUST 包含目标 MySQL drift 检查结果
- **AND** 对 `banners` 表缺失 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 等字段的情况 MUST 在发布前阻断或执行幂等迁移修复
- **AND** 修复验收 MUST 包含品牌类型 Banner 创建成功的生产或等价 smoke 证据。
