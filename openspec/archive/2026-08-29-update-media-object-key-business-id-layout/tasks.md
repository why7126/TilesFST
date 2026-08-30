## 1. 后端对象 Key 与 formalize

- [x] 1.1 梳理现有上传入口和媒体服务，确认头像、品牌 Logo、Banner、SKU 图片、SKU 视频、证书图片、证书文件的 key 生成调用点。
- [x] 1.2 实现统一媒体业务对象 id 目录构造函数，覆盖正式目录和 pending 目录，禁止用户原始文件名、本机路径、raw URL 或未脱敏业务文本进入 object key。
- [x] 1.3 调整品牌 Logo、Banner 图片、用户头像、品牌证书图片/文件的新上传 key 生成策略。
- [x] 1.4 保持 SKU 图片和 SKU 视频既有 `tiles/{tile_id}` 正式目录能力，并补齐统一 `images|videos/default/tiles/{tile_id}/` 扁平目录约束。
- [x] 1.5 为业务对象创建成功后的 pending 媒体 formalize 补齐原图、视频、文件、`.thumb.webp`、`.display.webp` 复制或补生成逻辑。
- [x] 1.6 确保 formalize 失败不会让业务记录引用不存在对象，重复执行保持幂等。

## 2. 旧媒体兼容与迁移

- [x] 2.1 保留 `/media/{object_key}` 对旧数据库完整 key 的受控读取兼容，禁止端侧或展示层按新目录推导旧路径。
- [x] 2.2 实现存量媒体业务对象 id 目录迁移 dry-run，输出待迁移数量、跳过数量、失败分类、目标冲突、对象缺失和风险摘要。
- [x] 2.3 实现存量媒体迁移 apply，要求显式参数和数据库、对象存储 bucket/prefix 备份确认。
- [x] 2.4 实现迁移二次审计，覆盖数据库引用、对象存在性、受控 URL 可读性、端侧 render/Network 和幂等复跑。
- [x] 2.5 明确旧对象删除或清理不在普通迁移中默认执行，并在命令帮助和 Runbook 中提示高风险边界。

## 3. API、DB 与观测

- [x] 3.1 评估上传、保存和媒体读取 API 字段是否变化；若变化，同步 OpenAPI、Orval、API 文档和前后端测试；若不变化，记录 N/A 原因。
- [x] 3.2 评估是否新增媒体别名表、迁移状态表、字段或索引；若变化，同步 SQLite/MySQL schema、迁移、数据库设计文档和测试；若不变化，说明继续复用既有媒体引用字段。
- [x] 3.3 为上传、formalize、迁移和维护任务补齐 `product_data_collection_observability` 声明、脱敏字段、失败分类和验证摘要。
- [x] 3.4 增加日志和维护输出脱敏测试，覆盖完整 object key、密钥、连接串、Authorization header、Cookie、`.env` 和本机绝对路径不泄露。

## 4. 端侧与展示验收

- [x] 4.1 验证管理端头像、品牌 Logo、Banner、SKU 图片/视频、品牌证书图片/文件上传状态机、即时回显、保存后重开回显和字段级错误。
- [x] 4.2 验证 Web 管理端、店主端和小程序只消费后端返回 URL 或 key 字段，不拼接对象存储 endpoint、bucket、业务 id 目录或 raw URL。
- [x] 4.3 补齐旧媒体兼容样本的 key、object、URL、render/Network 证据，覆盖 SKU 图片、品牌 Logo、Banner、证书图片和证书 PDF。
- [x] 4.4 若上传边界或 Nginx 配置变化，通过 Docker Web `http://localhost:3000` 验证小文件成功和超限业务错误；若不变化，记录 N/A 原因。

## 5. 文档与验证

- [x] 5.1 更新 `rules/object-storage.md`、`rules/media.md` 和 `docs/07-object-storage-strategy.md` 的对象 Key 策略矩阵、pending/formalize、旧 key 兼容和清理边界。
- [x] 5.2 更新 `docs/standards/batch-image-processing-runbook.md` 或生产媒体维护 Runbook，说明业务对象 id 目录迁移 dry-run/apply/audit/rollback。
- [x] 5.3 更新发布验收或升级计划材料，说明本版本是只改新上传、迁移存量对象，还是包含旧对象清理。
- [x] 5.4 运行 OpenSpec 校验、语言校验、产品数据采集与链路观测门禁校验和相关后端/前端聚焦测试。
- [x] 5.5 回填 Change 验收证据，记录 API、DB、Orval、Docker Compose、Web、小程序和管理端影响的通过或 N/A 结论。

## 验收返修记录

- 2026-08-29 23:14:05 `/opsx-modify`：补齐验收证据闭环。Pillow 环境确认 `12.3.0`；依赖 Pillow 的图片上传与媒体测试 `uv --project src/backend run python -m pytest src/backend/tests/test_admin_brands.py src/backend/tests/test_admin_tile_skus.py tests/integration/api/test_admin_brand_certificates.py tests/test_media_storage.py` 97 passed；对象 key、维护任务和部署脚本聚焦测试 47 passed；管理端媒体相关 Vitest 9 files / 94 tests passed；小程序媒体、首页、证据模板与媒体审计测试 61 passed；OpenSpec、语言、产品数据采集与链路观测门禁均通过；Docker Compose 当前 `tilesfst-backend`、`tilesfst-web`、`tilesfst-docs-site` 运行中。同步修正测试夹具：品牌 Logo 保存后应回显 `brand-logos/{brand_id}` 正式目录 URL，日志脱敏测试避免把 `auto_create_bucket` 误判为 raw `bucket` 泄露；小程序设备证据模板测试改为校验 `updated_at` 时间格式。REQ acceptance 已补充 `result: passed` 验收证据摘要；机器回填块按 `opsx.modify` 事件保持 pending，等待 `/opsx-archive` 正式关闭。生产 `media-drift-reconcile --apply --confirm-backup` 未由本命令直接执行，发布前仍需按 Runbook 完成数据库与对象存储 bucket/prefix 备份确认。
- 2026-08-29 22:18:26 `/opsx-modify`：将对象存储目录矩阵从 `users/{id}/avatars`、`brands/{id}/logos`、`banners/{id}/images`、`tiles/{id}/images` 等过渡形态调整为扁平业务媒体类型目录：`user-avatars/{id}`、`brand-logos/{id}`、`banners/{id}`、`tiles/{id}`、`brand-certificates/{id}`；pending 统一为同类资源 `pending/`；保留旧/过渡目录作为兼容来源，并补充 `avartars` 错误拼写审计。聚焦测试 `uv run pytest src/backend/tests/test_object_keys.py src/backend/tests/test_media_maintenance.py tests/test_migrate_pending_tile_images.py tests/test_deploy_media_maintenance_script.py` 47 passed；依赖 PIL 的图片上传集成测试在当前本机环境收集失败，需在具备 Pillow 的后端环境补跑。
- 2026-08-29 21:39:22 `/opsx-modify`：同步更新 `docs/standards/batch-image-processing-runbook.md` 与 `docs/standards/production-media-maintenance-runbook.md` 的 `media-drift-reconcile` 口径：补齐 `--progress` stderr/stdout 分流、5 个聚合阶段、`business_id_media_key_migration`、`business_id_media_candidates`、用户头像 UUID 字符串业务 id 目录和对象 key 迁移验收判断；修正生产 Runbook 后半段残留的 4 阶段说明。
- 2026-08-29 21:31:09 `/opsx-modify`：修正 `migrate-business-id-media-keys` 对 `users.id` UUID 执行 `int()` 导致 `media-drift-reconcile` 在 `business_id_media_key_migration` 阶段阻塞的问题；补充 UUID 用户头像迁移回归测试。重建本地后端容器后复跑 `media-drift-reconcile --progress` dry-run，5/5 阶段完成、`business_id_media_candidates=702`、`failed=0`、`non_standard_keys_after_audit=47`；端侧 render evidence 仍待 apply 后补证。
- 2026-08-29 21:14:09 `/opsx-modify`：修正 `docs/standards/production-media-maintenance-runbook.md` 中 `media-drift-reconcile` 进度阶段数量残留文案，将 “4 个子任务阶段” 改为 “5 个子任务阶段”，与新增 `business_id_media_key_migration` 聚合阶段保持一致。
