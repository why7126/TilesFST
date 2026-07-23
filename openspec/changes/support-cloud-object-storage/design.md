## Context

现有媒体上传链路已经集中在后端 `media` 模块：管理端通过鉴权 API 上传，后端校验 MIME、大小和 object_key 后写入 MinIO SDK，读取时通过 `/media/{object_key}` 从对象存储受控返回。生产部署已有 `docker-compose.prod.external.yml`，用于外部 MySQL + 外部 MinIO/S3 兼容对象存储，但规格、环境变量、文档和类名仍以 MinIO 为唯一语义。

腾讯云 COS、火山云 TOS 等云对象存储均提供 S3 兼容访问方式，但在 endpoint、region、bucket 预创建、path-style/virtual-host 风格、权限策略和 TLS 配置上存在差异。本变更需要把这些差异纳入部署配置和验收，不改变业务上传接口。

## Goals / Non-Goals

**Goals:**

- 支持使用 MinIO、自建 S3 兼容服务、腾讯云 COS、火山云 TOS 等云上对象存储承载业务媒体。
- 保持单桶 + 标准前缀策略，数据库仍只保存 `object_key`。
- 保持前端、小程序和管理端调用方式不变，上传和读取都经过后端。
- 允许自建 MinIO 自动创建 bucket；云上对象存储默认要求运维预创建 bucket 并配置最小权限。
- 补充配置校验、文档示例、测试和生产 smoke 清单。

**Non-Goals:**

- 不实现前端直传、STS 临时凭证、预签名上传或浏览器直连对象存储。
- 不新增多桶策略、跨区域复制、生命周期管理、CDN 回源配置或冷热分层。
- 不引入腾讯云/火山云专有 SDK；优先使用 S3 兼容协议。
- 不迁移既有 object_key，不改变媒体相关数据库结构。

## Decisions

1. 对象存储实现继续基于 S3 兼容协议。

   现有 MinIO Python SDK 已覆盖 S3 兼容对象的基础 put/get 能力。优先扩展配置而不是引入多个厂商 SDK，可以保持上传链路简单，也避免不同 SDK 的异常模型泄漏到业务层。若后续需要 COS/TOS 专有能力，应另行通过 OpenSpec Change 评估。

2. 增加存储提供方与连接参数，并统一应用配置命名。

   应用侧统一使用 `OBJECT_STORAGE_PROVIDER`、`OBJECT_STORAGE_ENDPOINT`、`OBJECT_STORAGE_ACCESS_KEY`、`OBJECT_STORAGE_SECRET_KEY`、`OBJECT_STORAGE_BUCKET`、`OBJECT_STORAGE_SECURE`、`OBJECT_STORAGE_REGION`、`OBJECT_STORAGE_PATH_STYLE`、`OBJECT_STORAGE_AUTO_CREATE_BUCKET` 以及 `OBJECT_STORAGE_PREFIX_*`。MinIO 容器自身所需的 `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` 只作为容器内部运行变量，不作为后端应用配置。

3. Bucket 初始化策略按部署类型区分。

   本地和自建 MinIO 可继续自动创建单桶，降低开发门槛。云上 COS/TOS 等对象存储的 bucket、区域、权限和白名单通常由云控制台/运维管控，应用启动或上传时不得尝试隐式创建生产 bucket；缺失或不可访问时返回对象存储不可用并给出可排查日志。

4. 受控读取保持 `/media/{object_key}`。

   前端不需要知道 bucket、endpoint 或云厂商信息。后端继续校验 object_key，读取对象后返回内容，避免暴露 raw endpoint、签名凭据、bucket 权限细节或内部错误栈。

5. 部署验收以真实云存储 smoke 加单元测试组合覆盖。

   单元测试覆盖配置解析、bucket 初始化策略、object_key 校验和存储异常映射。部署 smoke 覆盖生产 compose 仅启动 backend/web、连接外部 bucket、上传品牌 Logo 或 SKU 图片、通过 `/media/{object_key}` 读取。

## Risks / Trade-offs

- 云厂商 S3 兼容细节不一致 → 文档必须列出 endpoint、region、path-style、TLS、bucket 权限和网络白名单检查项，并要求生产 smoke。
- 云上对象存储配置错误可能导致上传失败 → 配置层只暴露非敏感摘要，部署文档必须明确 endpoint、region、TLS、访问风格与 bucket 前置检查。
- 关闭云上 bucket 自动创建后，首次部署更依赖运维前置动作 → `.env.example`、部署文档和错误排查章节必须说明 bucket 预创建和权限要求。
- 使用 S3 兼容协议无法覆盖厂商专有能力 → 本变更明确不支持专有增强能力，后续按独立 Change 扩展。

## Migration Plan

1. 保持现有本地和自建 MinIO 部署默认行为不变。
2. 在配置层加入 `OBJECT_STORAGE_*`，移除后端应用对 `MINIO_*` 的依赖。
3. 更新外部生产 Compose 和文档，示例覆盖 MinIO、腾讯云 COS、火山云 TOS 的配置形态，但不包含真实密钥或真实生产域名。
4. 部署到云上对象存储前，由运维预创建 bucket、授权最小读写权限并放通网络。
5. 执行上传与 `/media/{object_key}` 读取 smoke；失败时可回滚到原有 `MINIO_*` 外部 MinIO 配置或自建 MinIO Compose。

## Open Questions

- 是否要求在管理端系统设置页展示 `object_storage_provider` 只读摘要，替代现有 `minio_bucket` 单字段展示？若需要，这会影响 Web 文案和 Orval 生成。
- 是否需要为生产健康检查增加“对象存储连通性”诊断端点？当前建议先用部署 smoke 命令验证，避免公开新 API。
