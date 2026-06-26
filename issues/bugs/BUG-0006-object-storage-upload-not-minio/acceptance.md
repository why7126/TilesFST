---
bug_id: BUG-0006-object-storage-upload-not-minio
status: in_sprint
updated_at: 2026-06-26 11:44:07
---

# 回归验收标准

## AC-001 上传成功后必须写入 MinIO 单桶

**Given** Docker Compose 环境已启动，且 `minio-init` 已创建 `tile-info-platform` 桶  
**When** 管理端上传品牌 Logo、SKU 图片、SKU 视频或头像  
**Then** 上传成功后对象 MUST 写入 `MINIO_BUCKET=tile-info-platform`。  
**And** MinIO Console 中 MUST 能看到对应业务对象。  
**And** 不得新增多个业务 Bucket，除非后续 OpenSpec Change 明确要求。

## AC-002 对象 Key 必须使用标准前缀

**Given** 用户上传图片或视频  
**When** 后端生成对象 Key  
**Then** 图片原始文件 MUST 使用 `original/` 前缀。  
**And** 视频原始文件 MUST 使用 `videos/` 前缀。  
**And** 若涉及视频封面，封面对象 MUST 使用 `videos/covers/` 前缀。  
**And** 对象 Key MUST 拒绝绝对路径、`..`、空路径、反斜杠和重复斜杠。

## AC-003 上传链路必须通过后端授权与校验

**Given** 上传接口被调用  
**When** 文件进入后端  
**Then** 后端 MUST 保持现有 admin / employee 权限边界。  
**And** 后端 MUST 校验 MIME Type、文件扩展名和大小限制。  
**And** 前端 MUST NOT 直接写入未授权对象存储。  
**And** 后端 MUST NOT 使用用户原始文件名作为对象 Key。

## AC-004 上传响应必须保持 API 兼容

**Given** 上传成功  
**When** API 返回响应  
**Then** 响应 MUST 继续包含 `object_key` 和可访问的 `url` 或 `preview_url`。  
**And** 响应结构 MUST 保持统一 `ApiResponse` 格式。  
**And** 若 URL 策略从 `/media/{object_key}` 调整为签名 URL 或代理 URL，MUST 同步 OpenAPI、Orval 与前端调用方。

## AC-005 媒体读取必须从 MinIO 受控读取

**Given** 上传对象已写入 MinIO  
**When** 用户访问返回的媒体 URL  
**Then** 后端 MUST 能从 MinIO 读取对象并返回媒体内容，或返回安全的签名 URL。  
**And** 读取失败时 MUST 返回统一错误结构和稳定错误码。  
**And** 错误响应 MUST NOT 暴露 MinIO 内部地址、Access Key、Secret Key 或服务器绝对路径。

## AC-006 Docker Compose 验证必须覆盖 MinIO

**Given** 修复完成  
**When** 使用 Docker Compose 启动服务并执行媒体上传  
**Then** `minio`、`minio-init`、`backend`、`web` 服务 MUST 能共同完成上传到 MinIO 的闭环。  
**And** 不得为了修复该问题修改应用内部默认端口。  
**And** 如新增或调整环境变量，MUST 同步 `.env.example` 和部署文档。

## AC-007 测试必须覆盖对象存储写入

**Given** 缺陷进入修复阶段  
**When** 完成 `fix-*` OpenSpec Change  
**Then** 后端测试 MUST 覆盖上传后调用 MinIO 存储适配层写入对象。  
**And** 测试 MUST 覆盖图片与视频对象 Key 前缀。  
**And** 测试 MUST 覆盖非法对象 Key 拒绝。  
**And** 测试 MUST 避免依赖真实密钥或真实客户素材。

## AC-008 不得破坏既有上传业务

**Given** 修复完成  
**When** 用户维护品牌、SKU、头像或其他媒体字段  
**Then** 既有上传入口 MUST 保持可用。  
**And** 已保存的 `object_key` MUST 能用于后续列表展示、编辑回显和详情展示。  
**And** 如涉及已有本地 `data/uploads` 文件迁移，MUST 在修复 Change 中明确迁移或重新上传策略。

## AC-009 文档与规范必须同步

**Given** 修复涉及对象存储、媒体上传、环境变量、接口或数据库字段  
**When** 修复完成  
**Then** MUST 按影响范围同步更新相关 OpenSpec Change、`docs/06-video-asset-management.md`、`.env.example`、`data/README.md`、API 文档和测试说明。  
**And** 若数据库媒体元数据字段含义变化，MUST 同步 `docs/04-database-design.md` 与 Pydantic Schema 说明。
