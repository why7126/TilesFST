---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
review_status: approved
created_at: 2026-08-25 15:47:17
updated_at: 2026-08-25 15:47:17
reviewed_at: 2026-08-25 15:47:17
reviewer: AI
decision: approved
---

# 缺陷评审

## 评审结论

`approved`

确认该问题属于需要修复的管理后台上传链路缺陷。默认评审通过，建议优先纳入当前或下一 Sprint 后创建 OpenSpec 修复 Change。

## 评审依据

| 检查项 | 结论 | 说明 |
|---|---|---|
| 根因 confirmed 门禁 | pass | `root_cause_status: confirmed`，且 `validate-root-cause-evidence.py --require-confirmed` 通过。 |
| 证据链可定位 | pass | 证据覆盖用户截图、前端生成客户端、后端路由、Web Nginx 模板和 Docker 端口映射。 |
| 严重等级 | pass | `high` 合理；问题阻断管理后台头像上传，普通用户无法自行恢复。 |
| 回归验收 | pass | `acceptance.md` 已覆盖无尾斜杠路径、CORS 消除、头像上传成功、上传代理不回归和媒体四联验收。 |
| hotfix 判断 | not_required | 当前影响集中于本地 / Docker Web 入口和管理后台头像上传，建议常规 Sprint 修复；如演示环境必须立即可用，可提升为 hotfix。 |

## 修复建议

- 在 `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 中补充 `location = /api/v1/admin/uploads` 精确匹配。
- 精确匹配应复用上传专用 body 限制、超时与 buffering 配置，并反代到后端无尾斜杠上传接口。
- 保留现有 `location /api/v1/admin/uploads/`，避免品牌 Logo、Banner、瓷砖图片、瓷砖视频等子路径上传代理回归。
- 补充 Nginx 配置测试，确认无尾斜杠上传路径优先于通用 `/api/` location。

## 后续门禁

- 必须先通过 `/sprint-propose` 纳入 `sprint-xxx`。
- 纳入 Sprint 后再执行 `/bug-opsx BUG-0139-admin-avatar-upload-nginx-redirect-cors` 创建修复 Change。
- 修复 Change 在 `/opsx-apply` 前必须满足 Sprint Inclusion Gate。
