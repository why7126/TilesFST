---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
created_at: 2026-07-23 11:19:18
updated_at: 2026-07-23 22:59:48
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
related_change: fix-admin-banner-create-schema-drift
---

# Acceptance - BUG-0083 生产环境创建品牌类型 Banner 保存接口返回 500

## 回归验收标准

- [ ] AC-BUG-001 生产 MySQL `banners` 表 MUST 与当前 `src/backend/app/db/schema.mysql.sql` 的 Banner 字段保持无阻塞 drift，至少包含 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark` 等创建接口写入字段。
- [ ] AC-BUG-002 修复 MUST 提供幂等 MySQL 兼容迁移或发布步骤，能安全补齐既有生产 `banners` 表缺失字段、必要索引和可添加的外键。
- [ ] AC-BUG-003 若生产脏数据导致外键或约束暂不能添加，修复 MUST 在实现记录中明确跳过原因、影响范围、后续清理方式和不阻断保存的边界。
- [ ] AC-BUG-004 `POST /api/v1/admin/banners` 创建 `jump_type=BRAND_DETAIL` Banner MUST 在生产环境保存成功，返回统一 envelope 和 HTTP 200。
- [ ] AC-BUG-005 保存成功响应 MUST 回显 `jump_type=BRAND_DETAIL`、正确 `brand_id`、`image_source`、`image_object_key`、展示位置、排序和有效期。
- [ ] AC-BUG-006 品牌类型 Banner 编辑保存 MUST 成功，且不得清空 `brand_id`、`image_source`、`image_object_key`、排序、有效期和备注。
- [ ] AC-BUG-007 `image_source=brand_logo` 时，提交的 `image_object_key` 与品牌 `logo_object_key` 一致则保存成功，不一致返回明确 4xx 错误，不得返回 500。
- [ ] AC-BUG-008 `image_source=custom_upload` 时，合法 Banner 上传图可保存成功，且不得绕过后端上传鉴权、MIME Type、大小和 object key 校验。
- [ ] AC-BUG-009 品牌不存在、品牌未启用、品牌无 Logo、Logo 引用不一致、标题重复、外部 URL 不合法等失败场景 MUST 返回统一错误 envelope 和稳定错误码，不得暴露 SQL、DSN、MinIO 凭据、内部路径或堆栈。
- [ ] AC-BUG-010 后端自动化测试 MUST 覆盖品牌类型 Banner 新增、编辑、品牌 Logo、自定义上传图、失败场景，以及旧 MySQL 表缺列后兼容迁移补齐的路径。
- [ ] AC-BUG-011 发布前 MUST 提供目标生产 MySQL schema drift 检查或等价证据，证明 `banners` 表无阻塞缺列。
- [ ] AC-BUG-012 保存成功后，管理端列表、详情、上线/下线操作和小程序对应 Banner 展示入口 MUST 读取到同一配置。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 生产接口证据 | 创建品牌类型 Banner 的 Network 或日志证据，包含 HTTP 200 与响应 `data.brand_id` |
| 数据库证据 | 目标 MySQL drift 检查输出，确认 `banners` 无阻塞缺列 |
| 后端日志 | 保存成功无 SQL 错误；失败分支返回业务错误码且无敏感信息 |
| 管理端证据 | 列表、详情、编辑弹窗能回显同一品牌类型 Banner 配置 |
| 小程序证据 | 对应展示位置可读取 Banner，并能跳转品牌详情 |
| 自动化测试 | pytest 覆盖 Banner API 与 MySQL 兼容迁移；必要时补前端表单 payload 测试 |
| 发布证据 | 迁移执行结果、回滚边界、drift 检查结果和生产 smoke 纳入修复记录 |

## 非目标

- 本 BUG 不要求新增新的 Banner 类型或新的展示位置。
- 本 BUG 不要求重做 Banner 管理页面视觉或小程序品牌详情页视觉。
- 本 BUG 不要求放宽品牌状态、Logo 引用、上传安全、鉴权或对象存储策略。
- 本 BUG 不要求提交真实生产数据库导出、真实客户素材或密钥。
- 本 BUG 不允许直接修改 `openspec/specs/`；后续修复必须先完成 `bug-review` 与 `bug-opsx`。
