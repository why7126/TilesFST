---
change_id: fix-admin-avatar-upload-nginx-redirect-cors
type: fix
status: applied
source_bug: BUG-0139-admin-avatar-upload-nginx-redirect-cors
sprint: sprint-026
created_at: 2026-08-25 16:35:00
updated_at: 2026-08-25 18:25:00
---

# 追溯

## 来源

- BUG：`BUG-0139-admin-avatar-upload-nginx-redirect-cors`
- Sprint：`sprint-026`
- 能力：`deployment`

## 根因状态

`confirmed`

## 证据摘要

- 浏览器 Network 显示 `POST http://localhost:3000/api/v1/admin/uploads` 返回 `301 Moved Permanently`。
- 重定向后目标变为 `http://localhost/api/v1/admin/uploads/`，宿主机端口 `3000` 丢失。
- 浏览器因 `Origin: http://localhost:3000` 访问 `http://localhost` 判定跨源，并拦截 OPTIONS/POST。
- `src/web/src/shared/api/generated.ts` 生成客户端调用 `POST /api/v1/admin/uploads`，路径无尾斜杠。
- `src/backend/app/api/v1/uploads.py` 后端路由支持 `/api/v1/admin/uploads`。
- `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 仅配置 `/api/v1/admin/uploads/` 上传专用 location。

## 同步状态

```yaml
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
change_id: fix-admin-avatar-upload-nginx-redirect-cors
sprint: sprint-026
status: applied
workflow_event: opsx.apply
```

## 实现验证

```yaml
implemented_at: 2026-08-25 17:17:46
checks:
  - command: uv run pytest tests/test_cloud_object_storage_deployment.py::test_web_nginx_uses_runtime_template_for_upload_timeout_env tests/test_cloud_object_storage_deployment.py::test_static_web_nginx_matches_upload_template_routes
    result: pass
  - command: docker compose build tilesfst-web
    result: pass
  - command: docker compose up -d tilesfst-web --force-recreate
    result: pass
  - command: docker compose exec -T tilesfst-web nginx -T
    result: pass
  - command: node smoke POST http://127.0.0.1:3000/api/v1/admin/uploads
    result: pass
  - command: ./node_modules/.bin/vitest run src/features/admin/components/UserFormModal.test.tsx
    result: pass
acceptance: pending_user_review
api_change: false
database_change: false
orval_required: false
docker_compose_smoke_required: true
docs_sync:
  - docs/02-deployment.md
  - docs/07-object-storage-strategy.md
incident_note: 已读取 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 并按 Docker Web 边界补充 Nginx exact location 与测试；本次为该最佳实践既有规则落地，无需新增知识文档。
```
