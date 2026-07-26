## 1. 管理端视频上传状态修复

- [x] 1.1 调整 SKU 视频上传前端状态机，区分客户端上传中与服务端保存/等待确认阶段。
- [x] 1.2 当浏览器上传进度达到 99% 且接口尚未返回时，展示“正在保存视频，请稍候”或等价文案。
- [x] 1.3 保持上传成功后即时加入视频列表，失败后展示错误并允许重新选择同一文件重试。
- [x] 1.4 确认 SKU 图片上传、品牌 Logo、Banner 图片和品牌证书上传状态不回归。

## 2. 上传响应链路与部署验证

- [x] 2.1 确认容器内 Web Nginx 运行配置包含 `/api/v1/admin/uploads/` 专用 location、上传超时和 `proxy_request_buffering` 策略。
- [x] 2.2 确认生产外层 HTTPS Nginx 或等价网关对上传路径配置不低于业务上限的 body size 和 600 秒级超时。
- [x] 2.3 若发现生产部署未应用 BUG-0081 修复，补充部署步骤或发布说明并记录 smoke 结果。
- [x] 2.4 确认对象存储写入成功后接口返回 `object_key` 与 `/media/{object_key}`，不得要求前端直连对象存储写入。

## 3. 测试与验收

- [x] 3.1 补充前端 Vitest，覆盖视频上传 99% 后服务端保存中状态、成功回显和失败重试。
- [x] 3.2 运行相关前端测试，例如 `pnpm --dir src/web test -- TileSkuFormModal` 或项目等价命令。
- [x] 3.3 运行后端/部署回归测试：`uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py`。
- [x] 3.4 完成生产或生产等价 smoke：合法 MP4 返回 200、对象存储存在对象、`/media/{object_key}` 可读取、SKU 表单保存闭环，且 Nginx/backend 日志无 60 秒 499/504。

## 4. 文档与知识沉淀

- [x] 4.1 如调整部署步骤或外层 Nginx 示例，同步 `docs/02-deployment.md` 或 `docs/standards/file-upload.md`。
- [x] 4.2 修复后评估是否将“上传 99% / 对象已写入但响应链路超时”沉淀到 `docs/knowledge-base/incidents/`；若不需要，在验收记录中说明原因。
