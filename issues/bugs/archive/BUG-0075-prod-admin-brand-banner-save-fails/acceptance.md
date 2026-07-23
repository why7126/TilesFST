---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
created_at: 2026-07-21 15:21:45
updated_at: 2026-07-22 08:59:18
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-prod-admin-brand-banner-save
---

# Acceptance - BUG-0075 生产环境管理端品牌类型 Banner 配置无法保存

## 回归验收标准

- [ ] AC-BUG-001 生产 MySQL `banners` 表 MUST 包含 `brand_id` 字段，且与当前 `schema.mysql.sql` 中 Banner 相关字段、索引和约束保持一致。
- [ ] AC-BUG-002 若生产库存在旧版 `banners` 表，修复 MUST 提供可执行的 MySQL 迁移或发布步骤，安全补齐品牌类型 Banner 所需字段与约束。
- [ ] AC-BUG-003 生产环境 Web 管理端新建品牌类型 Banner MUST 保存成功，响应为统一 envelope，返回 `jump_type = BRAND_DETAIL`、正确 `brand_id` 和图片字段。
- [ ] AC-BUG-004 生产环境 Web 管理端编辑已有品牌类型 Banner MUST 保存成功，且不会清空 `brand_id`、`image_source`、`image_object_key`、有效期和排序等字段。
- [ ] AC-BUG-005 使用品牌 Logo 作为 Banner 图片时，后端 MUST 校验提交的 `image_object_key` 与品牌 `logo_object_key` 一致；一致时保存成功，不一致时返回明确错误提示。
- [ ] AC-BUG-006 使用自定义上传运营图作为品牌类型 Banner 图片时，合法图片 MUST 保存成功，且不得绕过后端上传鉴权、MIME Type、大小和对象 Key 校验。
- [ ] AC-BUG-007 品牌不存在、品牌未启用、品牌无 Logo、Logo 引用不一致、标题重复等失败场景 MUST 返回明确错误码和用户可理解提示，不得返回裸 500 或 SQL 错误文本。
- [ ] AC-BUG-008 保存成功后管理端列表、详情、上线/下线操作和小程序对应 Banner 展示入口 MUST 读取到同一配置。
- [ ] AC-BUG-009 后端自动化测试 MUST 覆盖品牌类型 Banner 新增、编辑、品牌 Logo、自定义上传图、无效品牌和 Logo 引用不一致场景。
- [ ] AC-BUG-010 发布前 MUST 提供目标 MySQL schema drift 检查或等价证据，证明生产库与 `schema.mysql.sql` 中 Banner 结构一致。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| 生产接口证据 | 保存品牌类型 Banner 的 Network 响应截图或日志，包含 HTTP 200 和返回数据 |
| 数据库证据 | 目标 MySQL `banners` 表结构检查结果，确认 `brand_id` 等字段存在 |
| 后端日志 | 保存成功无 SQL 错误；失败分支有明确业务错误码 |
| 管理端证据 | 管理端列表和详情能回显品牌类型 Banner 配置 |
| 小程序证据 | 对应 Banner 展示位置可读取并跳转到品牌详情 |
| 自动化测试 | pytest 覆盖后端 Banner 保存链路；必要时补前端表单 payload 测试 |
| 发布证据 | 迁移步骤、回滚说明和 schema drift 检查结果纳入修复记录 |

## 非目标

- 本 BUG 不要求新增新的 Banner 类型或新的展示位置。
- 本 BUG 不要求改造品牌详情页、品牌列表页或小程序页面视觉。
- 本 BUG 不要求放宽品牌状态、Logo 引用、上传安全或对象存储策略。
- 本 BUG 不要求修改 `openspec/specs/`；后续修复需先通过 `bug-review` 与 `bug-opsx`。
- 本 BUG 不要求提交真实生产数据库导出、真实客户素材或密钥。
