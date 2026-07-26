## 背景

BUG-0081 的生产证据显示，SKU 视频上传请求在浏览器侧返回 504，但腾讯 COS 中已经存在对应对象。容器 Nginx 日志中同一上传请求约 60 秒后记录为 499，且请求体先被缓冲到 Nginx 临时文件。

当前上传链路：

```text
浏览器 HTTPS 请求
→ 外层 HTTPS Nginx
→ 容器内 Web Nginx
→ FastAPI backend
→ 腾讯 COS S3 兼容 put_object
→ backend 返回 { object_key, url }
→ Nginx 返回浏览器
```

后端上传接口必须等待 COS `put_object` 完成后才返回 `object_key` 与 `url`。当浏览器上传、Nginx 缓冲、backend 读文件、COS 写入和响应返回总耗时超过 60 秒默认反代超时时，就会出现 COS 已写入但前端失败的状态不一致。

## 根因

根因是生产大文件上传链路缺少专用反代超时与请求缓冲策略，且容器内 Nginx 上传超时没有通过环境变量或部署参数统一配置。

已确认：

- 外层 HTTPS Nginx 443 server 仅有通用 `location /`，没有上传专用超时。
- 外层 `client_max_body_size 100m` 小于项目默认视频上限。
- 容器内 `src/web/nginx.conf` 的 `/api/` location 没有显式 `proxy_read_timeout`、`proxy_send_timeout`、`client_body_timeout` 或 `send_timeout`。
- 项目文档当前只强调 `client_max_body_size`，没有覆盖上传到云对象存储时的反代超时和环境变量化配置。

## 修复方案

### 1. Docker Web Nginx 上传专用 location

在容器内 Web Nginx 中，通用 `/api/` location 之前增加更具体的 `/api/v1/admin/uploads/` location：

- `client_max_body_size` 不小于项目最大上传上限。
- `client_body_timeout`、`proxy_send_timeout`、`proxy_read_timeout`、`send_timeout` 默认 600 秒。
- `proxy_connect_timeout` 保持较短默认，例如 60 秒。
- 评估开启 `proxy_request_buffering off`，减少大文件先落 Nginx 临时文件再转发 backend 的串行耗时。
- 保留现有 `Host`、`X-Real-IP`、`X-Forwarded-*` 请求头。

### 2. 上传超时环境变量化

Nginx 配置不能直接读取普通 Docker 环境变量，因此实现必须采用下列方案之一：

- 使用 `nginx.conf.template` + 容器启动脚本 `envsubst` 渲染为最终 `nginx.conf`。
- 使用 Docker 官方 Nginx 支持的 `/etc/nginx/templates/*.template` 机制。
- 使用项目已有脚本在构建或启动阶段生成配置。

建议变量：

```text
UPLOAD_CLIENT_MAX_BODY_SIZE=512m
UPLOAD_CLIENT_BODY_TIMEOUT_SECONDS=600
UPLOAD_PROXY_CONNECT_TIMEOUT_SECONDS=60
UPLOAD_PROXY_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_READ_TIMEOUT_SECONDS=600
UPLOAD_SEND_TIMEOUT_SECONDS=600
UPLOAD_PROXY_REQUEST_BUFFERING=off
```

变量名可在实现阶段按项目命名规范调整，但必须覆盖 body size、读写超时和请求缓冲策略。

### 3. 外层 HTTPS 反代文档

项目无法直接控制客户服务器上的外层 HTTPS Nginx，但部署文档必须明确：外层 `/api/v1/admin/uploads/` 的超时必须大于等于容器内 Web Nginx，否则外层仍会先 504。

### 4. 保持业务契约不变

本 Change 不修改上传 API 路径、响应 Schema、对象 Key 策略、鉴权要求、对象存储单桶策略或数据库模型。

## 测试策略

- 配置测试：验证 Nginx 上传 location 位于通用 `/api/` 前，且默认超时为 600 秒。
- 模板测试：如使用模板渲染，验证环境变量覆盖值能渲染到最终 Nginx 配置。
- 部署测试：运行 `tests/test_cloud_object_storage_deployment.py`，确保外部对象存储部署要求不回退。
- 媒体存储测试：运行 `tests/test_media_storage.py`，确保对象存储适配层行为不回退。
- 生产 smoke：上传同类视频，确认浏览器返回 200、COS 对象存在、SKU 表单可保存、Nginx 不再出现 60 秒 499/504。

## 风险与回滚

- 若 `proxy_request_buffering off` 在某些外层代理或网络环境下表现不稳定，可先回滚该项，保留长超时。
- 若模板渲染失败会导致 Web 容器 Nginx 启动失败，必须在启动脚本中 fail fast，并用测试覆盖默认渲染。
- 若外层 HTTPS Nginx 未同步配置，生产仍可能 504；因此文档和验收必须要求外层配置证据。
