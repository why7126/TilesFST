## Context

生产环境管理端创建品牌类型 Banner 时返回 500，关联 `BUG-0083-prod-admin-brand-banner-save-500`。历史 `BUG-0075` 已针对 `banners.brand_id` 缺失补过 MySQL 兼容迁移，但当前 `BannerRepository.create()` 会写入完整 Banner 字段：`image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 等。生产旧表若缺失任一写入字段，仍可能触发 `Unknown column` 或约束异常。

当前约束：

- 不改变 Admin Banner API 契约。
- 不直接修改 `openspec/specs/`。
- 不提交生产数据库导出、真实客户素材或密钥。
- 修复必须兼容本地 SQLite/demo 路径和生产 MySQL 路径。

## Goals / Non-Goals

**Goals:**

- 幂等补齐既有 MySQL `banners` 表保存品牌类型 Banner 所需的完整字段。
- 让生产 schema drift 在迁移、发布前检查或启动阶段被发现并可运维处理，而不是在业务 API 中变成裸 500。
- 保持品牌类型 Banner 新增、编辑、品牌 Logo、自定义上传图与失败场景行为稳定。
- 增加测试和发布证据，防止同类生产 drift 回归。

**Non-Goals:**

- 不新增 Banner 类型或展示位置。
- 不重做 Banner 管理 UI 或小程序品牌详情页视觉。
- 不放宽品牌启用状态、Logo 引用、上传鉴权、MIME Type、大小或 object key 校验。
- 不将生产数据导出或运维密钥纳入仓库。

## Decisions

### 1. 以幂等 MySQL 兼容迁移补齐完整 Banner 字段

实现应把现有 `mysql_compat_banners_brand_id_v1` 思路扩展为 Banner 表兼容迁移，逐列检查 `banners` 是否包含当前 schema 写入字段。缺失字段使用 `ALTER TABLE ... ADD COLUMN ...` 幂等补齐，字段定义应与 `schema.mysql.sql` 保持一致。

理由：`CREATE TABLE IF NOT EXISTS` 只覆盖空库，不会升级既有生产表；逐列迁移可安全重复执行，并能覆盖旧生产表的多字段 drift。

替代方案：只补 `brand_id`。该方案已被 `BUG-0083` 证明覆盖不足。

### 2. 外键与索引允许安全添加，脏数据时记录跳过

索引可在缺失时幂等添加。外键添加前需要检查脏数据；若存在无法满足外键的历史数据，应记录跳过原因、脏数据计数和后续清理建议，不阻断本次保存字段补齐。

理由：生产库可能存在历史 Banner 数据，强制加外键可能导致启动失败；但缺列会直接阻断保存，需优先修复。

### 3. API 层保持契约不变，失败场景统一 envelope

若是业务校验错误，继续返回已有 Banner 业务错误码。若是数据库 drift，修复目标是让 drift 在迁移/发布前消除；若仍出现数据库异常，响应不得暴露 SQL、DSN、凭据或堆栈。

理由：前端和 Orval 客户端不应因本修复产生契约变化。只有新增错误码或 schema 字段时才触发 Orval。

### 4. 发布前必须跑目标 MySQL drift 检查

修复交付应包含 `scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"` 或等价证据，证明目标 `banners` 表无阻塞缺列。生产 smoke 需验证 `POST /api/v1/admin/banners` 创建品牌类型 Banner 成功。

理由：本缺陷发生在生产旧表路径，本地 SQLite 或新库 pytest 不能替代目标 MySQL drift 证据。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 生产旧表缺列较多，迁移顺序不当导致失败 | 逐列检查并按 nullable/default 安全顺序补齐；先补字段，再补索引/外键 |
| 旧数据违反外键约束 | 添加外键前检查脏数据；有脏数据时跳过外键并记录 |
| 新增迁移影响本地 SQLite | MySQL 兼容迁移仅在 MySQL backend 执行，SQLite 继续使用 `migrations.py` |
| 仍缺生产日志确认具体异常 | Change tasks 要求补生产 request_id/log 或 drift 检查证据，不能只依赖推测验收 |
| API 错误映射改动触发前端契约漂移 | 默认不改 API schema；若新增错误码或响应字段，必须同步 OpenAPI、Orval、docs 和测试 |

## Migration Plan

1. 备份目标 MySQL 或确认可回滚快照。
2. 部署包含扩展兼容迁移的后端镜像。
3. 启动时或发布前执行兼容迁移，记录字段补齐、索引/外键添加或跳过结果。
4. 执行 schema drift 检查，确认 `banners` 无阻塞缺列。
5. 使用生产或等价环境创建品牌类型 Banner，确认接口返回 200 且管理端回显。

## Rollback Plan

- 若迁移只新增 nullable 字段和索引，回滚优先回退应用镜像并保留新增字段；避免删除字段造成数据丢失。
- 若新增索引影响写入性能，可按已记录的索引名手工回滚索引。
- 若外键添加导致问题，优先删除新增外键，保留数据字段。
- 回滚过程不得删除真实 Banner 业务数据或对象存储素材。

## Open Questions

- 生产日志中具体异常列名或约束名仍待确认。
- 是否需要为 schema drift 失败新增独立错误码，待实现阶段根据异常映射范围决定。
