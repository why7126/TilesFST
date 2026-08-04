## 实施任务

- [x] 1. BUG-0116 维护任务编排
  - [x] 1.1 设计或接入维护命令，覆盖 SKU pending 主图、SKU 缩略图、品牌 Logo 缩略图、证书图片 key 迁移、证书图片缩略图五类动作。
  - [x] 1.2 若 `add-prod-media-maintenance-jobs` 已完成，复用其 maintenance CLI / Compose service；若未完成，记录生产 apply blocked，只完成本地等价与 dry-run 能力。
  - [x] 1.3 统一 dry-run 输出字段：总数、待处理、跳过、缺失原图、缺失缩略图、同 size、同 bytes、失败原因、重试候选。

- [x] 2. SKU 历史对象修复
  - [x] 2.1 正式化公开 SKU pending 主图到 `images/default/tiles/{tile_id}/` 或等价商品目录。
  - [x] 2.2 同步 `tile_images.object_key` 与 `tile_images.url`，确保 `/media/{target_key}` 可追溯。
  - [x] 2.3 生成或重生成 SKU 同目录 `.thumb` 缩略图，记录同 bytes / 同 size 判断。
  - [x] 2.4 二次审计确认公开 SKU 主图 `pending_main_image` 归零，或输出 remaining fail / blocked 摘要。

- [x] 3. 品牌 Logo 历史缩略图修复
  - [x] 3.1 审计 `brands.logo_object_key` 原图与同目录 `.thumb`。
  - [x] 3.2 对可读原图生成或重生成真实轻量缩略图。
  - [x] 3.3 输出品牌列表、品牌详情、Banner 选图相关 URL/render 验收入口或 blocked 原因。

- [x] 4. 证书图片历史对象修复
  - [x] 4.1 审计 `brand_certificates.file_key` 与 `brand_certificate_images.file_key` 中仍位于 `files/default/brand-certificates/` 的 JPG、JPEG、PNG、WebP 图片。
  - [x] 4.2 将图片类证书迁移到 `images/default/brand-certificates/`，同步数据库引用。
  - [x] 4.3 确认 PDF 和其他文档类证书继续留在 `files/default/brand-certificates/`。
  - [x] 4.4 生成或重生成证书图片同目录 `.thumb` 缩略图。
  - [x] 4.5 二次审计确认图片类证书 files 前缀清零，或输出 remaining fail / blocked 摘要。

- [x] 5. 安全、备份与回滚
  - [x] 5.1 apply 前阻断未确认 MySQL 快照和对象存储 bucket / prefix 快照的执行路径。
  - [x] 5.2 输出摘要不得包含 `.env`、数据库 DSN、对象存储密钥、Authorization header、Cookie、本机绝对路径或真实客户数据。
  - [x] 5.3 记录目标已存在、原图缺失、缩略图生成失败、provider 不支持 copy/remove 等失败原因和重试条件。

- [x] 6. 测试与校验
  - [x] 6.1 补充后端测试：dry-run 不写、apply 幂等、PDF 不迁移、图片证书迁移、SKU pending 正式化、品牌 Logo 缩略图回填。
  - [x] 6.2 补充 fake storage / provider 测试：缺失 object、目标已存在、同 bytes 缩略图、不可处理 MIME、对象存储不可用。
  - [x] 6.3 补充脱敏输出测试，覆盖 secret、DSN、Authorization header、Cookie、`.env` 和本机绝对路径。
  - [x] 6.4 运行相关 pytest、`python scripts/validate-openspec-language.py`、`openspec validate fix-prod-media-historical-object-drift --strict`。

- [x] 7. 文档与验收回填
  - [x] 7.1 更新受影响的媒体、对象存储、部署或生产维护文档；若 `add-prod-media-maintenance-jobs` 承担入口文档，记录引用关系。
  - [x] 7.2 按 BUG-0116 `acceptance.md` 回填媒体四联：`key`、`object`、`URL`、`render`。
  - [x] 7.3 若生产真实 apply 不在当前 Sprint 执行，记录 blocked / external evidence 状态，避免误判完成。
  - [x] 7.4 评估是否需要在 `docs/knowledge-base/incidents/` 沉淀历史媒体治理复盘；不适用时说明原因。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-04 12:05:00 | 生产媒体维护命令直接写成后端模块命令，运维入口是否应放在 `deploy/scripts/` 更合理。 | 保留后端包内维护实现作为镜像内真实执行入口，新增 `deploy/scripts/media-maintenance.sh` 作为 local/prod Compose 运维包装脚本，并同步部署与对象存储文档。 | `bash -n deploy/scripts/media-maintenance.sh`、OpenSpec strict、Workflow Sync。 |
| 2026-08-04 20:20:00 | 本地/生产真实 env 文件存在于工作区但不提交 Git，不应阻塞 `/opsx-archive`。 | 调整目录结构校验：`deploy/**/*.env` 未被 Git 跟踪或暂存时不阻塞，已跟踪/待提交时继续阻塞；同步环境规则、目录规则和归档技能说明。 | `python scripts/validate-directory-structure.py`、`python scripts/validate-openspec-language.py`、`tests/test_validate_directory_structure.py` 新增用例通过；该测试文件的既有 `docs-site` 用例仍因 compose 漂移失败。 |
