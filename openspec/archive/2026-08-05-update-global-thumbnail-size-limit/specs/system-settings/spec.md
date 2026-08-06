## MODIFIED Requirements

### Requirement: 系统设置分组字段范围

**basic（P0）** MUST 支持：平台名称（2–64 字）、默认语言、默认时区、数据刷新周期、客服邮箱、维护窗口、系统公告（≤500 字）、首页指标卡开关、维护公告开关。**media（P0）** 可写：图片最大 MB、视频最大 MB、文档 / 文件最大 MB、允许图片 MIME 列表、允许视频 MIME 列表、缩略图体积目标上限 KB；UI MUST 提供以下可勾选 MIME catalog：**图片** `image/jpeg`、`image/png`、`image/webp`、`image/gif`、`image/svg+xml`、`image/bmp`、`image/tiff`、`image/heic`；**视频** `video/mp4`、`video/quicktime`、`video/x-msvideo`、`video/webm`、`video/x-matroska`、`video/mpeg`、`video/3gpp`。后端 PATCH 校验子集 MUST 与 env `ALLOWED_IMAGE_TYPES` / `ALLOWED_VIDEO_TYPES` 及前端 catalog 对齐。缩略图体积目标上限 MUST 使用 KB 单位，`0` MUST 表示不限制并保持当前缩略图生成模式，`1-1024` MUST 表示后续新生成缩略图尽量不超过该目标；UI 文案 MUST 使用“目标上限”或“尽量不超过”等非绝对承诺，并说明该设置仅对新生成缩略图生效，历史缩略图需通过维护任务重生成。文档 / 文件最大 MB MUST 作为品牌证书、PDF、附件类上传的 effective 配置来源，MUST NOT 仅由业务上传接口硬编码。只读：存储桶、Key 生成规则（对齐 REQ-0012 / object-storage spec 文案）。**security（P1）** MUST 支持：密码最小长度 8–32、四项复杂度开关、密码有效期、会话超时（映射 JWT access expire）、首次登录强制改密；P1b 可选登录失败锁定。**notification（P3）** MUST 持久化开关与容量阈值（50–95%）；模板 MUST 只读 + 查看入口；MUST NOT 要求真实发信。**audit（P2）** 可写：日志保留天数 30–3650、导出权限、敏感操作强制记录、脱敏展示；只读：审计范围说明、最近变更列表。

#### Scenario: 媒体 Tab 展示三类上传大小限制

- **WHEN** `admin` 访问 `/admin/settings/media`
- **THEN** UI MUST 展示图片、视频、文档 / 文件三类最大 MB 配置
- **AND** 默认值 MUST 来自 env / 代码默认值与 DB override merge 后的 effective 值
- **AND** 页面提示 MUST 与上传入口使用的后端限制一致

#### Scenario: PATCH 后文件上传限制生效

- **WHEN** `admin` PATCH media 分组修改文档 / 文件最大 MB
- **THEN** 值 MUST 写入 `system_settings` 或等价设置事实源
- **AND** 后续品牌证书、PDF 或附件类上传 MUST 按新上限校验
- **AND** MUST NOT 要求重启 backend

#### Scenario: 媒体限制恢复默认

- **WHEN** `admin` POST reset `media` 分组
- **THEN** 图片、视频、文档 / 文件大小限制覆盖值 MUST 清除或恢复 seed
- **AND** GET MUST 返回 env / 代码默认值

#### Scenario: 配置缩略图体积目标上限

- **WHEN** `admin` 在 `/admin/settings/media` 设置 `thumbnail_max_size_kb` 为 `20`
- **THEN** PATCH MUST 写入 media 分组设置事实源
- **AND** 后续新生成图片缩略图 MUST 读取该 effective 值并尽量控制体积
- **AND** 保存设置 MUST NOT 自动扫描或重建历史 `.thumb` 缩略图对象
- **AND** 保存成功反馈 MUST 使用 fixed toast，页面 MUST NOT 出现 layout shift。

#### Scenario: 缩略图体积目标恢复默认

- **WHEN** `admin` POST reset `media` 分组
- **THEN** 缩略图体积目标覆盖值 MUST 清除或恢复 seed
- **AND** GET MUST 返回 `0` 或等价默认不限制值
- **AND** 后续新生成缩略图 MUST 回到不限制体积的当前生成模式。

