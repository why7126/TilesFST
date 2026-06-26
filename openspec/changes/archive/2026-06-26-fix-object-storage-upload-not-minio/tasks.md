## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0006-object-storage-upload-not-minio` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `approved` 或 `in_sprint`
- [x] 1.3 确认本 change 不新增业务 Bucket，默认使用 `MINIO_BUCKET=tile-info-platform`
- [x] 1.4 梳理现有上传入口：头像、品牌 Logo、SKU 图片、SKU 视频
- [x] 1.5 确认是否保持 `/media/{object_key}` URL 语义；默认保持

## 2. 后端 MinIO 存储适配

- [x] 2.1 在 `src/backend/app/modules/media/` 中封装 MinIO client 或对象存储适配层
- [x] 2.2 使用 `settings.minio_endpoint`、`settings.minio_access_key`、`settings.minio_secret_key`、`settings.minio_secure`、`settings.minio_bucket`
- [x] 2.3 将 `save_upload_file()` 改为写入 MinIO `MINIO_BUCKET`
- [x] 2.4 保持 `build_upload_object_key()` 与标准前缀逻辑：`original/`、`videos/`、`videos/covers/`
- [x] 2.5 对 MinIO 不可用、Bucket 不存在、写入失败转换为统一 `AppError`
- [x] 2.6 禁止前端直连未授权 MinIO；上传仍经后端鉴权接口

## 3. 媒体读取与 URL 策略

- [x] 3.1 将 `/media/{object_key}` 或等价 URL 改为从 MinIO 受控读取对象
- [x] 3.2 保留 object_key 校验：拒绝 `..`、绝对路径、空路径、反斜杠和重复斜杠
- [x] 3.3 读取不存在对象时返回稳定媒体不存在错误
- [x] 3.4 错误响应不得暴露 AccessKey、SecretKey、MinIO 内部 endpoint 或服务器绝对路径
- [x] 3.5 确认品牌 Logo、头像、SKU 图片/视频现有 URL 回显不回退

## 4. API、配置与文档同步

- [x] 4.1 若上传响应 schema 不变，记录无需 Orval 的理由
- [x] 4.2 若 URL、错误码或响应字段变化，更新 OpenAPI、运行 Orval 并同步前端调用方
- [x] 4.3 检查 `.env.example` 是否包含 MinIO 与上传限制所需变量
- [x] 4.4 同步 `docs/03-api-index.md` 中上传接口实现状态
- [x] 4.5 同步 `docs/06-video-asset-management.md` 和 `docs/07-object-storage-strategy.md` 的单桶前缀策略
- [x] 4.6 同步 `data/README.md`，明确 `data/uploads` 不再作为业务上传正式存储

## 5. 测试

- [x] 5.1 后端 pytest：上传品牌 Logo 后调用 MinIO 写入 `MINIO_BUCKET`
- [x] 5.2 后端 pytest：上传头像、SKU 图片、SKU 视频时使用正确对象前缀
- [x] 5.3 后端 pytest：非法 MIME 与文件大小限制仍生效
- [x] 5.4 后端 pytest：非法 object_key / 路径穿越无法读取媒体
- [x] 5.5 后端 pytest：MinIO 不可用时返回 `STORAGE_UNAVAILABLE` 或等价稳定错误
- [x] 5.6 回归现有品牌管理、用户头像、SKU 媒体上传相关测试
- [x] 5.7 Docker Compose 验证：上传后 MinIO Console 或 `mc ls` 能看到业务对象

## 6. 验收与追溯

- [x] 6.1 对照 `issues/bugs/BUG-0006-object-storage-upload-not-minio/acceptance.md` 完成 AC-001 ~ AC-009
- [x] 6.2 更新本 change `trace.md`，记录测试命令、Docker 验证与是否执行 Orval
- [x] 6.3 更新 BUG trace 中 `fix-object-storage-upload-not-minio` 状态
- [x] 6.4 更新 `iterations/sprint-002/` 中 BUG-0006 的 Change 关联与验收状态
- [x] 6.5 评估是否需要更新 `docs/knowledge-base/incidents/`；若不沉淀，说明理由
