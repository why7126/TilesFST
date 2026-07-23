---
purpose: 对象存储使用规范
content: 规定 MinIO/S3兼容对象存储桶、对象Key、目录前缀、权限、生命周期与AI更新要求
source: 人工编写 + AI辅助生成
update_method: 对象存储策略变化时由技术负责人确认后更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-21 13:44:26
note: V5 推荐一个项目一个 Bucket，桶内使用目录前缀区分业务资源；支持 MinIO 与 S3 兼容云对象存储
---

# 对象存储规范

## 1. 总原则

本项目使用 MinIO 或 S3 兼容对象存储作为媒体对象存储。V5 采用：

```text
一个项目一个 Bucket
桶内按对象前缀区分资源类型
```

默认：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

不推荐按资源拆成多个桶，例如 `tile-original`、`tile-thumbnail`、`tile-video`。

后端应用统一使用 `OBJECT_STORAGE_*` 环境变量。腾讯云 COS、火山云 TOS 等云上对象存储 MUST 通过 S3 兼容 endpoint 接入，并由运维提前创建 bucket、配置 region、TLS、访问风格和最小权限。

## 2. 标准对象前缀

```text
images/                图片类上传（头像、Logo、SKU 图、Banner 等）
videos/                原始视频
files/                 文档类（预留）
audios/                音频类（预留）
thumbnails/            图片缩略图
processed/             处理后的图片或文件
tmp/                   临时文件
imports/               批量导入文件
exports/               导出文件
videos/covers/         视频封面
videos/transcoded/     转码后视频
original/              Deprecated — 仅存量对象；新上传 MUST NOT 使用
```

## 2.1 Object Key 形态

新上传对象 Key MUST 符合：

```text
{prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

示例：

```text
images/default/user/avatars/<uuid>.jpg
images/default/brands/logos/<uuid>.webp
images/default/tiles/pending/<uuid>.jpg
videos/default/tiles/42/<uuid>.mp4
```

MUST NOT 在新 Key 中插入 `{YYYY}/{MM}` 日期分片。存量 `original/.../{YYYY}/{MM}/...` 通过 `scripts/migrate_object_keys.py` 一次性迁移。

## 3. AI必须遵守

AI 在新增文件上传、视频上传、图片处理、导入导出能力时：

1. 不允许新增多个业务 Bucket，除非 OpenSpec 明确要求；
2. 必须复用 `.env.example` 中的 `OBJECT_STORAGE_BUCKET`；
3. 必须使用标准前缀；
4. 必须更新媒体资源相关 OpenSpec 和文档；
5. 必须补充对象Key生成逻辑和测试。

## 4. 云上对象存储部署要求

- 云上对象存储 provider 可使用 `s3-compatible`、`tencent-cos`、`volcengine-tos` 等枚举值表达。
- `OBJECT_STORAGE_ENDPOINT` MUST 使用 S3 兼容 endpoint，且不得包含 access key、secret key 或真实不可公开域名截图。
- `OBJECT_STORAGE_REGION` 在云厂商要求时 MUST 显式配置。
- `OBJECT_STORAGE_AUTO_CREATE_BUCKET` 在云上生产环境 MUST 为 `false`，bucket 由运维提前创建。
- 前端、管理端和小程序 MUST 继续通过后端上传与 `/media/{object_key}` 受控读取，不得直连云对象存储写入。
