## Why

BUG-0085 记录了生产管理后台上传 SKU 视频时，前端长时间停留在“上传中 99%”的问题。当前代码和历史 BUG-0081 证据表明，99% 是前端对浏览器上传进度的封顶显示，真实等待点通常在后端保存对象、对象存储响应或代理链路返回阶段。

该问题直接影响 SKU 视频素材维护：管理员无法确认视频是否上传成功，可能重复上传并产生孤儿对象。如果对象已经写入 COS/TOS/MinIO 但响应链路被 Nginx、CDN 或网关超时截断，业务上等价于上传失败。

## What Changes

- 强化 SKU 视频上传 UX：上传请求体完成但接口未返回时，前端必须展示“服务端保存/等待确认”阶段，不能只长期显示“上传中 99%”。
- 强化对象存储上传闭环：对象写入成功后，上传接口必须在配置的超时窗口内返回 `object_key` 与 `/media/{object_key}`；失败时必须可诊断。
- 强化部署验收：外层 HTTPS Nginx 与容器内 Web Nginx 必须对 `/api/v1/admin/uploads/` 应用上传专用超时，并用运行中配置或生产等价 smoke 证明生效。
- 补充前端 Vitest、后端/部署 pytest 和生产或生产等价 smoke 验收任务。

## Capabilities

### Modified Capabilities

- `tile-sku-management`: 明确 SKU 视频上传 99% 后的服务端保存状态、成功回显和失败重试要求。
- `object-storage`: 明确大视频对象写入后的响应闭环、受控读取和错误诊断要求。
- `deployment`: 明确上传路径运行中代理配置和生产 smoke 验收要求。

## Impact

- 影响管理端 Web：`src/web/src/features/admin/components/TileSkuFormModal.tsx`、`src/web/src/features/admin/api/tile-skus-api.ts` 及相关测试。
- 可能影响 Web Nginx 模板、Docker Compose 上传超时环境变量、生产部署文档或 smoke 记录。
- 影响后端媒体上传链路测试，但默认不要求新增 API 字段、不修改数据库 schema。
- 若实现阶段改变 API 响应结构或错误码，必须同步 OpenAPI / Orval / docs / tests。

## Rollback Plan

1. 保留现有后端授权上传与 `/media/{object_key}` 受控读取链路，避免回滚时破坏素材上传基础能力。
2. 若前端阶段文案或状态机引入异常，可回退到当前单一 uploading 状态，同时保留错误展示和重试。
3. 若上传专用代理配置调整导致生产代理异常，可回滚 Nginx location 或超时变量，但必须保留 `client_max_body_size` 不低于业务上传上限。
4. 回滚后重新验证 SKU 视频上传、SKU 图片上传、品牌 Logo、Banner 图片和品牌证书上传不回归。
