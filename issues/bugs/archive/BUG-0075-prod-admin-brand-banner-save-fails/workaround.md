---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
created_at: 2026-07-21 15:21:45
updated_at: 2026-07-22 08:59:18
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-prod-admin-brand-banner-save
---

# Workaround - BUG-0075 生产环境管理端品牌类型 Banner 配置无法保存

## 临时规避方案

在正式修复前，可采用以下低风险方式降低影响：

1. 运营侧临时使用“无跳转”或非品牌类型 Banner，并通过标题、文案或图片引导用户识别品牌活动。
2. 如必须跳转到品牌主页，先保留 Banner 素材、目标品牌 ID、品牌名称、期望展示位置和有效期，等待修复后统一补录。
3. 若生产接口返回 400 业务错误，优先检查所选品牌是否为 `ENABLED`、是否存在 `logo_object_key`，必要时改用自定义上传 Banner 图再保存。
4. 若生产接口返回 500 或 SQL 错误，运维先执行只读 schema drift 检查，确认 `banners` 表是否包含 `brand_id`，不要直接手工改业务数据。
5. 若标题重复导致保存失败，临时调整 Banner 标题，确保同一展示端与展示位置下标题唯一。

## 运维排查建议

建议先收集以下证据，再决定是否进入 hotfix：

| 检查项 | 目标 |
|---|---|
| Network 响应 | 确认保存接口 HTTP 状态码、错误码、响应 message 和 payload |
| 后端日志 | 确认是否出现 `Unknown column 'brand_id'`、外键错误、Check 约束错误或 `30052` 业务错误 |
| MySQL schema drift | 对比生产 `banners` 表与 `src/backend/app/db/schema.mysql.sql` |
| 品牌数据 | 确认所选品牌 `status = 'ENABLED'` 且 `logo_object_key` 非空 |
| 版本一致性 | 确认生产 Web bundle 和后端镜像来自同一发布版本 |

## 不建议的规避方式

- 不建议直接在生产库手工插入或修改 Banner 业务记录来绕过管理端保存接口。
- 不建议把品牌类型 Banner 改成外部链接模拟品牌跳转，除非产品确认小程序端能安全打开该链接。
- 不建议关闭后端品牌状态、Logo 引用或外键校验。
- 不建议前端隐藏保存失败提示或吞掉接口错误。
- 不建议绕过后端鉴权或直接写对象存储 / 数据库。

## 风险

临时使用无跳转 Banner 会降低品牌主页导流效果；等待修复后补录会增加运营排期成本。若直接手工改生产数据，可能造成 Banner 列表、上线状态、小程序展示端和审计记录不一致，因此只应作为经过审批的最后手段。
