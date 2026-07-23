## 1. 配置与兼容层

- [x] 1.1 在 `src/backend/app/core/config.py` 增加 `OBJECT_STORAGE_*` 配置项，并移除重复的 `MINIO_*` 应用配置。
- [x] 1.2 增加 provider、region、path-style/virtual-host、auto-create bucket 等配置解析与非敏感摘要方法。
- [x] 1.3 更新 `.env.example`，为新增或兼容变量补充注释、示例值、安全边界和 COS/TOS 配置提示。

## 2. 后端对象存储适配

- [x] 2.1 重命名或扩展 `MinioMediaStorageClient` 的内部语义，使其支持 MinIO 与 S3 兼容云上对象存储。
- [x] 2.2 按配置实现 bucket 初始化策略：本地/自建 MinIO 可自动创建，云上对象存储默认不自动创建。
- [x] 2.3 保持 `save_upload_file()`、`get_media_file_response()`、object_key 校验和 `/media/{object_key}` 响应语义不变。
- [x] 2.4 确保存储异常统一映射为既有对象存储不可用、媒体不存在或非法 object_key 错误，不暴露底层凭据与 SDK 堆栈。

## 3. 部署与文档

- [x] 3.1 更新 `docker-compose.prod.external.yml`，传递新增对象存储环境变量并维护邻近注释。
- [x] 3.2 按需更新 `docker-compose.prod.yml` 注释或变量传递，保持自建 MinIO 默认行为不回归。
- [x] 3.3 更新 `docs/02-deployment.md`，补充外部 MinIO、腾讯云 COS、火山云 TOS 等 S3 兼容对象存储的前置检查、示例配置和 smoke 步骤。
- [x] 3.4 更新 `docs/07-object-storage-strategy.md` 与 `rules/object-storage.md`，将对象存储表述从 MinIO 单一实现扩展为 MinIO/S3 兼容服务，同时保留单桶前缀策略。

## 4. 测试与验证

- [x] 4.1 补充后端配置单元测试，覆盖 `OBJECT_STORAGE_*` 默认值、云存储配置和 secret 不外泄。
- [x] 4.2 补充对象存储客户端测试，覆盖 auto-create bucket 开关、云上 bucket 不存在、上传成功、读取成功和异常映射。
- [x] 4.3 补充或更新部署配置测试，验证外部生产 Compose 仅包含 backend/web 且传递对象存储变量。
- [x] 4.4 运行后端相关 pytest；如涉及 OpenAPI 输出变更，补充 Orval 生成与前端类型校验。

## 5. OpenSpec 与交付检查

- [x] 5.1 运行 `openspec validate --change support-cloud-object-storage --strict` 并修复问题。
- [x] 5.2 运行 Workflow Sync 的 `opsx.apply` dry-run 门禁，确认纯技术治理 Change 可追踪。
- [x] 5.3 在实现输出中记录 API、数据库、Web、小程序、管理端、Orval、Docker Compose 和测试影响。
- [x] 5.4 如执行了生产等价 smoke，在 `acceptance.md` 或实现记录中写明对象存储 provider、bucket 预创建、上传和 `/media/{object_key}` 读取结果，且不得记录真实密钥。
