---
change_id: fix-admin-avatar-upload-nginx-redirect-cors
source_bug: BUG-0139-admin-avatar-upload-nginx-redirect-cors
sprint: sprint-026
created_at: 2026-08-25 16:35:00
updated_at: 2026-08-25 16:35:00
---

# 修复管理端头像上传代理重定向与 CORS

## 背景

`BUG-0139-admin-avatar-upload-nginx-redirect-cors` 已确认：管理后台上传用户头像时，前端调用 `POST /api/v1/admin/uploads`，Docker Web Nginx 仅配置了 `/api/v1/admin/uploads/` 尾斜杠 location。请求先命中通用代理或 Nginx 路径规范化逻辑并返回 `301 Moved Permanently`，随后跳转到 `http://localhost/api/v1/admin/uploads/`，宿主机端口 `3000` 丢失，浏览器将其判定为跨源请求并被 CORS 拦截。

该问题阻断管理端用户头像上传，且影响所有复用 `POST /api/v1/admin/uploads` 无尾斜杠入口的图片上传场景。根因不在后端上传接口、鉴权、MinIO 写入或 Orval 生成，而在 Web/Nginx 上传专用代理路径没有覆盖无尾斜杠精确匹配。

## 变更内容

- 修复 `src/web/nginx.conf` 与 `src/web/nginx.conf.template` 的上传代理配置，使 `/api/v1/admin/uploads` 无尾斜杠请求不再被 301 重定向。
- 保留 `/api/v1/admin/uploads/` 及其子路径的上传专用代理能力、请求体大小、上传超时和缓冲策略。
- 补充 Web Nginx 配置回归测试，覆盖无尾斜杠精确匹配、尾斜杠路径、品牌 Logo 等子上传路径不回退。
- 完成 Docker Web `localhost:3000` 生产等价 smoke，确认浏览器 Network 中 `POST /api/v1/admin/uploads` 返回上传业务响应且没有 301、端口丢失或 CORS 拦截。

## 能力范围

### 修改能力

- `deployment`：补齐管理端上传路径代理对无尾斜杠入口的强约束。

### 非目标

- 不改变 `POST /api/v1/admin/uploads` API 路径、请求体、响应体或错误码。
- 不改变后端 FastAPI 路由、鉴权、对象存储适配层或 MinIO/COS/TOS 配置。
- 不改变数据库表结构、用户头像字段或 Orval 生成客户端。
- 不处理 `BUG-0140` 中当前登录用户头像 key 指向缺失对象的问题；该缺陷由 `fix-admin-current-user-avatar-object-consistency` 单独覆盖。

## 回滚计划

- 若 Nginx 精确匹配配置导致上传子路径异常，可回退本 Change 对 `nginx.conf` 与 `nginx.conf.template` 的代理 location 调整，并保留测试输出定位命中路径。
- 回滚不涉及数据库 migration、后端 API、Orval 生成或对象存储数据迁移。
- 回滚后 `POST /api/v1/admin/uploads` 可能重新触发 301 与 CORS 问题，必须在发布记录中标注影响。

## 验证计划

- 运行 Web/Nginx 配置聚焦测试，确认配置中存在 `/api/v1/admin/uploads` 精确匹配，并且 `/api/v1/admin/uploads/` 子路径专用代理仍存在。
- 启动 Docker Compose 或生产等价 Web 容器，使用浏览器或 HTTP smoke 上传头像文件，确认首次 `POST /api/v1/admin/uploads` 不返回 301。
- 上传成功后记录媒体四联验收：返回 `object_key`、对象存储存在性、`/media/{object_key}` 读取、管理端头像预览或用户表单渲染。
- 确认浏览器 Network 没有跳转到 `http://localhost/api/v1/admin/uploads/`，没有 CORS 拦截。

## 影响

- API：不改变 API 合约；请求仍为 `POST /api/v1/admin/uploads`，响应结构不变。
- 数据库：不影响。
- Web：影响 Docker Web Nginx 上传代理配置与管理端头像上传链路。
- 小程序：不影响。
- 管理端：修复用户头像上传被 301/CORS 阻断。
- Orval：不需要。
- Docker Compose：需要生产等价或本地 Docker Web 验证。
- 测试：需要补充 Nginx 配置与上传 smoke 回归测试。
