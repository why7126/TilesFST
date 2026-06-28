## MODIFIED Requirements

### Requirement: 系统设置分组字段范围

**basic（P0）** MUST 支持：平台名称（2–64 字）、默认语言、默认时区、数据刷新周期、客服邮箱、维护窗口、系统公告（≤500 字）、首页指标卡开关、维护公告开关。**media（P0）** 可写：图片/视频最大 MB、允许 MIME 列表；UI MUST 提供以下可勾选 MIME catalog：**图片** `image/jpeg`、`image/png`、`image/webp`、`image/gif`、`image/svg+xml`、`image/bmp`、`image/tiff`、`image/heic`；**视频** `video/mp4`、`video/quicktime`、`video/x-msvideo`、`video/webm`、`video/x-matroska`、`video/mpeg`、`video/3gpp`。后端 PATCH 校验子集 MUST 与 env `ALLOWED_IMAGE_TYPES` / `ALLOWED_VIDEO_TYPES` 及前端 catalog 对齐。只读：存储桶、Key 生成规则。**security（P1）** 及后续分组范围不变。

#### Scenario: 媒体 Tab MIME chip 扩展

- **WHEN** `admin` 访问 `/admin/settings/media`
- **THEN** UI MUST 展示至少 8 个图片格式 chip 与 7 个视频格式 chip
- **AND** PATCH 所选 MIME MUST 被 `_validate_media` 接受

#### Scenario: 媒体 Tab 桶路径只读

- **WHEN** `admin` PATCH `media` 尝试修改 bucket 或 key 规则
- **THEN** 服务端 MUST 忽略或拒绝

#### Scenario: PATCH 后 upload 生效

- **WHEN** `admin` PATCH 启用 `image/gif` 并上传 gif 文件
- **THEN** upload MUST 成功（在大小限制内）
