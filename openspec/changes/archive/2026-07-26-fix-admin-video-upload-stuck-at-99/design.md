## Root Cause

BUG-0085 的直接原因不是单一文件传输进度异常，而是上传链路缺少端到端阶段语义：

- 前端 `onUploadProgress` 只表示浏览器请求体上传进度，并把进度封顶在 99%。
- 后端上传接口读取完整文件并同步写入对象存储，写入完成前不会返回结果。
- 生产链路经过外层 HTTPS Nginx、容器内 Web Nginx、backend 和 COS/TOS/MinIO；任何一层默认 60 秒级超时都可能导致对象已写入但浏览器拿不到成功响应。
- UI 没有把 99% 后的“服务端保存/等待确认”阶段与客户端上传阶段区分开。

## Fix Strategy

### Frontend Upload State

- 将 SKU 视频上传状态拆成可感知阶段：客户端上传中、服务端保存中、成功、失败。
- 当浏览器上传进度达到封顶值或请求体完成但 Promise 未 resolve 时，显示“正在保存视频，请稍候”或等价文案。
- 保持失败后可重新选择同一文件并重试；上传中仍禁止并发重复提交。

### Upload Response Chain

- 验证上传接口成功响应仍返回 `object_key` 与 `/media/{object_key}`，不让前端直连对象存储写入。
- 如果对象存储不可用、MIME 不允许、文件超限或代理超时，返回可诊断错误并在前端展示。

### Deployment Runtime Verification

- 确认 Web Nginx 模板和实际运行配置均包含 `/api/v1/admin/uploads/` 专用 location。
- 确认外层 HTTPS Nginx 或等价网关也设置上传专用 `proxy_send_timeout`、`proxy_read_timeout`、`send_timeout`。
- 生产或生产等价 smoke 必须覆盖大视频上传返回 200、对象存在、`/media/{object_key}` 可读取、SKU 表单保存闭环。

## Testing

- 前端 Vitest：覆盖 99% 后服务端保存中状态、成功回显、失败重试。
- 后端/部署 pytest：覆盖上传 Nginx 模板、Compose 默认环境变量和对象存储受控读取回归。
- 生产 smoke：记录 Network 状态码、耗时、对象 key、Nginx/backend 日志摘要。

## Non-Goals

- 不新增前端直传对象存储能力。
- 不新增数据库表或修改 SKU 视频元数据 schema。
- 不新增视频转码、压缩、多清晰度或后台异步处理能力。
- 不改变小程序视频播放逻辑。
