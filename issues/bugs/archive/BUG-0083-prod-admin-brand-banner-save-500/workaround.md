---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
status: done
created_at: 2026-07-23 11:19:18
updated_at: 2026-07-23 22:59:48
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
related_change: fix-admin-banner-create-schema-drift
---

# Workaround - BUG-0083 生产环境创建品牌类型 Banner 保存接口返回 500

## 临时规避方案

在正式修复前，可采用以下低风险方式降低运营影响：

1. 暂停创建品牌类型 Banner，避免重复触发生产 500。
2. 若必须上线运营位，临时创建非品牌类型或无跳转 Banner，仅展示品牌活动图片与文案。
3. 记录待补录的品牌 Banner 信息，包括品牌 ID、品牌名称、展示位置、图片 object key、标题、排序、有效期和备注，待修复后统一补录。
4. 若用户使用的是品牌 Logo 图片来源，临时改用已上传的自定义 Banner 运营图；但如果接口仍返回 500，应停止继续尝试并进入 DB drift 排查。
5. 运维先执行只读 schema drift 检查，确认生产 `banners` 表是否缺失字段；不要直接手工插入业务 Banner 数据。

## 运维排查建议

| 检查项 | 目标 |
|---|---|
| Network 响应 | 收集 `POST /api/v1/admin/banners` 的 payload、响应 body、request_id 和 HTTP 状态 |
| 后端日志 | 查找对应 request_id 的 SQLAlchemy / MySQL 异常，重点看 `Unknown column`、外键失败、唯一约束失败、数据长度错误 |
| MySQL schema drift | 执行 `python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"`，重点看 `missing_columns.banners` |
| 生产版本 | 确认后端镜像包含最新 MySQL 兼容迁移，且应用启动日志中迁移执行成功 |
| 品牌数据 | 确认所选品牌 `status='ENABLED'`，且品牌 Logo key 与提交图片 key 一致 |
| 非品牌 Banner | 验证非品牌类型 Banner 是否能保存，以区分全局 Banner 创建失败与品牌类型特定失败 |

## 不建议的规避方式

- 不建议直接在生产库手工插入或修改 Banner 业务记录来绕过管理端接口。
- 不建议删除或放宽品牌状态、Logo 引用、外键、上传安全或对象 Key 校验。
- 不建议通过外部链接模拟品牌详情跳转，除非产品确认小程序端可安全打开且体验可接受。
- 不建议隐藏前端错误提示或吞掉接口 500。
- 不建议提交真实生产数据库导出、真实客户素材、密钥或对象存储凭据作为缺陷附件。

## 风险

临时使用无跳转或非品牌类型 Banner 会降低品牌主页导流效果。若直接手工修改生产数据，可能导致管理端列表、上线状态、小程序展示、审计记录和对象存储引用不一致；因此仅应在完成备份、审批和回滚预案后作为最后手段。
