---
requirement_id: REQ-0012-object-storage-key-layout
title: 对象存储前缀与 Object Key 生成规则优化
terminal: multi
version: v1
status: approved
owner: product
source: issues/requirements/archive/REQ-0012-object-storage-key-layout/capture.md
priority: P1
parent_requirement:
---

# REQ-0012 对象存储前缀与 Object Key 生成规则优化

## 1. 需求背景

本项目采用 MinIO **单桶 + 前缀** 策略（`MINIO_BUCKET=tile-info-platform`）。当前实现（`object_keys.py` + `uploads.py`）存在以下问题：

1. **前缀语义不清**：图片类资源统一使用 `original/`，与「原始视频 `videos/`」不对齐，且无法区分图片与普通文件。
2. **Key 层级过深**：现形态 `{prefix}/default/{resource_type}/{YYYY}/{MM}/{uuid}.{ext}` 含年月分片；业务检索依赖 SQLite 中的完整 `object_key`，Console 按目录浏览时层级过细，维护成本高。
3. **resource_type 命名不一致**：如头像为 `avatars`、SKU 图为 `tiles/{id}/images`，与领域路径 `user/avatars` 不对齐。
4. **规范与 env 脱节**：`MINIO_PREFIX_*` 已在 `.env.example` 定义，但上传代码硬编码 `"original"` / `"videos"`。

产品方已确认新规则：

- 前缀使用 **`images` / `videos` / `files` / `audios`** 等语义类型，**禁止**新增业务使用 `original/`。
- **保留** `{tenant}` 段，默认值为 `default`，作为多租户预留。
- Key 形态简化为：**`{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`**（无 `{YYYY}/{MM}`）。

## 2. 目标用户

- **后端 / 平台开发**：统一 Key 生成、迁移与测试。
- **管理端运营用户**：上传头像、Logo、SKU 图/视频后，媒体 URL 仍通过 `/media/{object_key}` 正常访问。
- **后续迭代**（导入导出、音频等）：可在同一规则下扩展前缀，无需再次推翻 Key 结构。

## 3. 范围

### 3.1 本期包含

- 重新定义标准前缀枚举与 `resource_type` 命名规范（FR-001、FR-002）
- 调整 `build_object_key()` 生成逻辑，移除 `{YYYY}/{MM}`（FR-003）
- 调整 4 个既有上传 API 的 prefix / resource_type 映射（FR-004）
- 同步 `rules/object-storage.md`、`docs/07-object-storage-strategy.md`、`.env.example` 中 `MINIO_PREFIX_*` 说明（FR-005）
- 历史 `object_key` 迁移或兼容策略（FR-006）
- 更新 OpenSpec `object-storage` delta、pytest 前缀断言与回归测试（FR-007）

### 3.2 本期不包含

- 新增 `audios/`、`files/` 实际上传 API（仅规范预留 prefix 与 env）
- 缩略图自动生成、`videos/covers/` 自动封面、`videos/transcoded/` 转码流水线
- 多 Bucket、前端直连 MinIO、签名 URL 权限分级
- 微信小程序端变更（仅间接受益于 URL 规则一致）
- 店主端 Web 新上传能力（当前上传均在管理端）

## 4. 功能要求

### FR-001 标准对象前缀（替代 original/）

系统 MUST 使用下列语义前缀；**MUST NOT** 在新上传对象上使用 `original/`：

| 前缀 | 用途 | 本期是否写入 |
|---|---|---|
| `images` | 位图类原始图片（头像、Logo、SKU 图等） | 是 |
| `videos` | 原始视频 | 是 |
| `files` | 通用原始文件（PDF、Excel、导入包等） | 规范预留 |
| `audios` | 原始音频 | 规范预留 |
| `thumbnails` | 缩略图（处理后） | 规范保留，本期不写 |
| `processed` | 其他处理后资源 | 规范保留，本期不写 |

`MINIO_PREFIX_*` 环境变量 MUST 与上表对齐；代码生成 Key 时 SHOULD 优先读取 `settings.minio_prefix_*`，避免硬编码字符串。

### FR-002 resource_type 命名规范

`resource_type` MUST 使用 **小写 + 斜杠路径**，表达业务域与资源种类，**MUST NOT** 再嵌套 `{YYYY}/{MM}`。

| 业务场景 | prefix | resource_type | 示例 Key |
|---|---|---|---|
| 用户头像 | `images` | `user/avatars` | `images/default/user/avatars/{uuid}.jpg` |
| 品牌 Logo | `images` | `brands/logos` | `images/default/brands/logos/{uuid}.webp` |
| SKU 图片（已有关联 tile_id） | `images` | `tiles/{tile_id}` | `images/default/tiles/42/{uuid}.jpg` |
| SKU 图片（新建暂存） | `images` | `tiles/pending` | `images/default/tiles/pending/{uuid}.jpg` |
| SKU 视频（已有关联 tile_id） | `videos` | `tiles/{tile_id}` | `videos/default/tiles/42/{uuid}.mp4` |
| SKU 视频（新建暂存） | `videos` | `tiles/pending` | `videos/default/tiles/pending/{uuid}.mp4` |
| 批量导入（预留） | `files` | `imports` | `files/default/imports/{uuid}.csv` |
| 批量导出（预留） | `files` | `exports` | `files/default/exports/{uuid}.xlsx` |

规则：

- `{tenant}` 默认 `default`；未来多租户 MUST 可通过参数替换，结构不变。
- 扩展名 `{ext}` MUST 由后端 MIME 白名单映射，MUST NOT 使用用户原始文件名。
- `resource_type` MUST NOT 以 `/` 开头或结尾（除路径内部斜杠外）。

### FR-003 Object Key 生成形态

`build_object_key()`（或等价函数）MUST 生成：

```text
{prefix}/{tenant}/{resource_type}/{uuid}.{ext}
```

其中：

- `{prefix}`：FR-001 标准前缀（无尾部 `/` 或统一规范化）
- `{tenant}`：默认 `default`
- `{resource_type}`：FR-002 路径
- `{uuid}`：UUID v4
- `{ext}`：小写扩展名

**MUST NOT** 在 Key 中包含 `{YYYY}/{MM}` 或用户上传文件名。

示例（完整）：

```text
images/default/brands/logos/3fa85f64-5717-4562-b3fc-2c963f66afa6.webp
videos/default/tiles/pending/7c9e6679-7425-40de-944b-e07fc1f90ae7.mp4
```

### FR-004 既有上传 API 映射调整

下列 API 的 `object_key` 生成 MUST 符合 FR-001～FR-003：

| API | 现 Key 前缀示例 | 新 Key 前缀示例 |
|---|---|---|
| `POST /api/v1/admin/uploads` | `original/default/avatars/...` | `images/default/user/avatars/...` |
| `POST /api/v1/admin/uploads/brand-logos` | `original/default/brands/logos/...` | `images/default/brands/logos/...` |
| `POST /api/v1/admin/uploads/tile-images` | `original/default/tiles/{id\|pending}/images/...` | `images/default/tiles/{id\|pending}/...` |
| `POST /api/v1/admin/uploads/tile-videos` | `videos/default/tiles/{id\|pending}/...` | `videos/default/tiles/{id\|pending}/...`（结构不变，仅去 `{YYYY}/{MM}`） |

上传响应 MUST 仍为 `{ object_key, url: "/media/{object_key}" }`；MIME / 大小校验规则不变。

### FR-005 文档与配置同步

变更 MUST 同步：

- `rules/object-storage.md`
- `docs/07-object-storage-strategy.md`
- 根目录 `.env.example`（`MINIO_PREFIX_*` 注释与取值）
- `src/backend/.env.example`、`src/backend/.env.docker`（若引用旧前缀说明）
- `data/README.md` 媒体排查示例 Key

`original/` MUST 在规范中标记为 **已废弃（deprecated）**，仅用于迁移期读取兼容说明。

### FR-006 历史 object_key 迁移

SQLite 中已存 `object_key` 字段（`users.avatar_object_key`、`brands.logo_object_key`、`tile_images.object_key`、`tile_videos.object_key`）及 MinIO 存量对象 MUST 有明确策略，二选一或组合：

**方案 A（推荐）**：提供一次性迁移脚本

- MinIO 内 copy/rename 至新 Key（或 upload + delete 旧对象）
- 更新 DB 中全部引用
- 迁移脚本 MUST 支持 dry-run

**方案 B**：读取层短期双格式兼容

- `/media/{object_key}` 对旧 Key 仍可读
- 新上传仅写新 Key
- MUST 在 OpenSpec / runbook 注明兼容窗口与退役时间

PRD 不强制选定方案；`/req-complete` 或 OpenSpec design MUST 敲定并在 acceptance 中验收。

### FR-007 测试与 OpenSpec

- MUST 更新 `test_upload_endpoints_store_expected_minio_prefixes` 等 pytest 断言为新前缀。
- MUST 覆盖 Key 不含 `{YYYY}/{MM}`、不含 `original/`。
- MUST 通过 `/req-opsx` 创建 OpenSpec Change（建议 `update-object-storage-key-layout`），delta `object-storage` spec。
- `cd src/backend` pytest 与 Docker Compose 上传/读取冒烟 MUST 通过。

## 5. UI / UE 约束

- 本需求 **无** 管理端/店主端 UI 变更；前端仅继续存储与展示 API 返回的 `object_key` / `url`。
- 若迁移后旧 URL 失效，MUST 在迁移完成前避免用户可见 404（由 FR-006 保障）。

## 6. 非功能约束

- 单桶策略不变；MUST NOT 新增业务 Bucket。
- 安全校验不变：`validate_object_key()` 仍防路径穿越。
- Nginx `client_max_body_size`、上传大小 env 不变。

## 7. 关联需求与规范

| 关联 | 关系 |
|---|---|
| `openspec/specs/object-storage/spec.md` | 将被 MODIFIED（Key 前缀与形态） |
| REQ-0006 瓷砖 SKU 管理 | SKU 图/视频 object_key 受影响 |
| REQ-0005 品牌/用户管理 | Logo、头像 object_key 受影响 |
| BUG-0006～0008 | 已完成 MinIO 迁移；本需求为 Key 结构优化 |
| `rules/object-storage.md` | 事实规范，须同步 |

## 8. 状态

| 项 | 值 |
|---|---|
| status | draft |
| priority | P1 |
| 建议 Change | `update-object-storage-key-layout` |
| 下一步 | `/req-complete REQ-0012-object-storage-key-layout` |
