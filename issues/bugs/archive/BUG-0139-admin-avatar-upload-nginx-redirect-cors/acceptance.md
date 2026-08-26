---
bug_id: BUG-0139-admin-avatar-upload-nginx-redirect-cors
acceptance_status: passed
created_at: 2026-08-25 15:35:15
updated_at: 2026-08-25 17:43:45
---

# 验收计划

## 回归验收项

| 编号 | 验收项 | 预期结果 | 状态 |
|---|---|---|---|
| AC-001 | 无尾斜杠头像上传路径 | `POST /api/v1/admin/uploads` 不再返回 `301`，直接进入 Web Nginx 上传专用反代链路。 | passed |
| AC-002 | CORS 拦截消除 | 从 `http://localhost:3000` 上传头像时不再跳转到 `http://localhost/...`，浏览器不再因 CORS 拦截上传。 | passed |
| AC-003 | 头像上传业务成功 | 管理后台用户创建 / 编辑弹窗上传 JPG / PNG / WebP 头像成功，返回 `object_key` 与 `/media/...` URL，并即时刷新预览。 | passed |
| AC-004 | 上传专用代理不回归 | Nginx 无尾斜杠上传路径优先于通用 `/api/` location，并复用上传专用 body 限制、超时与 buffering 配置。 | passed |
| AC-005 | 其他上传路径不回归 | 品牌 Logo、Banner、瓷砖图片、瓷砖视频等带子路径上传仍保持原有代理与上传限制。 | passed |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0139-admin-avatar-upload-nginx-redirect-cors |
| 标题 | 管理后台头像上传被 Nginx 301 重定向丢端口导致 CORS 拦截 |
| 严重等级 | high |
| 影响范围 | Web 管理端 / Docker Web Nginx / 头像上传接口 |
| 复现入口 | 管理后台用户创建或编辑弹窗上传头像 |
| 受影响端 | admin / backend-proxy |
| 环境 | docker-web-3000 |
| 媒体类型 | image |
| 业务资源 | 管理后台用户头像 |
| 修复前实际结果 | `POST /api/v1/admin/uploads` 返回 `301`，跳转到 `http://localhost/api/v1/admin/uploads/` 后被 CORS 拦截。 |
| 修复后期望结果 | `POST /api/v1/admin/uploads` 保持同源并直达上传代理，头像上传成功并返回可读 `/media/...` URL。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | passed | Docker Web smoke 返回 `images/default/user/avatars/1ac50a1a-d520-48ba-bed5-3058335d3889.png`，前缀符合用户头像图片策略。 | 无 |
| object | passed | Docker Web smoke 使用上传响应 key 读取 `/media/...`，返回 200，读取 68 bytes PNG。 | 无 |
| URL | passed | Docker Web smoke：`POST http://127.0.0.1:3000/api/v1/admin/uploads` 首响 200，`Location=null`，`/media/images/default/user/avatars/1ac50a1a-d520-48ba-bed5-3058335d3889.png` 返回 200。 | 无 |
| render | passed | `./node_modules/.bin/vitest run src/features/admin/components/UserFormModal.test.tsx` 通过，覆盖上传头像后预览 `img src` 更新；Docker Web smoke 覆盖后端受控 URL 可读。 | 无 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | passed | `UserFormModal.test.tsx` 通过，覆盖头像上传进度、成功状态与预览更新。 |
| 同会话即时回显 | passed | `UserFormModal.test.tsx` 通过，覆盖上传后同一弹窗内预览 `img src` 更新。 |
| Docker Web 边界 | passed | Docker Web smoke 经 `http://127.0.0.1:3000` 调用 `POST /api/v1/admin/uploads`，首响 200，未出现 301/302/307/308 或 Location。 |
| 媒体代理一致性 | passed | Docker Web smoke 返回 key 与 `/media/{object_key}` URL 一致，媒体读取返回 200。 |
| 历史对象与审计 | n/a | 本 BUG 不涉及历史对象迁移、缩略图回填或审计脚本。 |
| 小程序 evidence | n/a | 本 BUG 只影响 Web 管理端头像上传，不影响小程序页面或组件。 |

## 测试建议

- 增加或更新 `tests/test_cloud_object_storage_deployment.py`，断言 `src/web/nginx.conf.template` 包含 `location = /api/v1/admin/uploads` 且该配置位于通用 `/api/` location 之前。
- 同步覆盖 `src/web/nginx.conf` 静态配置，避免模板与仓库内 Nginx 配置漂移。
- 若具备本地 Docker 环境，使用 `curl -i -X POST http://localhost:3000/api/v1/admin/uploads` 或浏览器上传行为确认不再出现 `301`；实际上传验证仍需携带合法鉴权与 multipart 文件。

## 验收结论

当前状态：`pending_user_review`

修复实现和自动化 / smoke 验证已通过，等待用户或测试人员最终验收确认后关闭。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 17:43:45
accepted_by: workflow-sync
source_change: fix-admin-avatar-upload-nginx-redirect-cors
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: opsx.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

