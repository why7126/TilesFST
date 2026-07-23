---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
status: done
review_result: approved
reviewed_at: 2026-07-21 15:24:31
reviewer: AI
created_at: 2026-07-21 15:24:31
updated_at: 2026-07-22 08:59:18
severity: high
related_requirement: REQ-0062-admin-banner-placement-scope
related_change: fix-prod-admin-brand-banner-save
---

# Review - BUG-0075 生产环境管理端品牌类型 Banner 配置无法保存

## 评审结论

结论：`approved`，确认需要修复。

该缺陷发生在生产环境 Web 管理端 Banner 保存链路，直接阻断品牌类型 Banner 的配置闭环。缺陷包已补齐现象、复现路径、影响范围、初步根因、临时规避和回归验收标准；根因高概率指向生产 MySQL `banners` 表结构与当前应用期望不一致，仍需在修复阶段用生产日志或 schema drift 检查最终确认。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户反馈明确；本地新库品牌类型 Banner API 测试通过，生产失败高概率来自生产库结构、生产数据或版本差异 |
| 严重等级合理 | 通过 | `high` 合理：生产环境阻断运营配置品牌类型 Banner，影响品牌导流与线上内容更新 |
| 回归验收明确 | 通过 | acceptance 已覆盖 MySQL schema、品牌类型新增/编辑、品牌 Logo、自定义上传图、错误提示和小程序展示读取 |
| 是否需 hotfix 路径 | 建议优先修复，可走小范围 hotfix | 若生产日志确认 `banners.brand_id` 缺失或 SQL 写入失败，应优先补迁移/发布校验并验证保存链路 |

## 修复门禁

- 状态批准后允许执行 `/bug-opsx BUG-0075-prod-admin-brand-banner-save-fails`。
- 状态批准后允许纳入 Sprint 规划。
- 来源于该 BUG 的 OpenSpec Change 在 `/opsx-apply` 前仍必须先纳入正式 Sprint 范围。

## 修复建议

优先按生产证据收敛修复范围：

1. 收集保存接口 HTTP 状态码、响应 JSON、请求 payload 与后端日志。
2. 对目标 MySQL 执行 schema drift 检查，确认 `banners.brand_id`、外键、枚举约束与 `schema.mysql.sql` 一致。
3. 若确认为 schema drift，提供安全 MySQL 迁移、回滚说明和发布前 drift 检查证据。
4. 若确认为业务校验失败，补充更明确的错误提示和对应后端/前端测试。
5. 保持品牌状态、Logo 引用、上传鉴权、MIME Type、大小和对象 Key 安全校验，不通过放宽校验绕过问题。

## 后续动作

下一步可执行：

```bash
/bug-opsx BUG-0075
```

创建 OpenSpec Change 后，再纳入 Sprint 并进入实现。
