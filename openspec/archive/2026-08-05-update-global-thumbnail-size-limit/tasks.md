## 1. 系统设置与 API

- [x] 1.1 新增 `media.thumbnail_max_size_kb` 默认值和 effective settings 读取方法，默认 `0` 表示不限制。
- [x] 1.2 扩展 media 分组 Pydantic Schema、PATCH 校验、GET 响应和 reset 默认值，校验范围为 `0-1024 KB` 或设计确认范围。
- [x] 1.3 补充系统设置后端测试，覆盖读取、保存、非法值、恢复默认和上传链路读取 effective 值。
- [x] 1.4 同步 OpenAPI、Orval 生成物和相关 API 文档索引。

## 2. 缩略图生成策略

- [x] 2.1 为图片缩略图生成逻辑增加目标体积参数，默认不限制时保持现有行为。
- [x] 2.2 实现 JPEG / WebP 质量递减和必要的尺寸收缩策略，并设置尝试次数、质量、尺寸下限。
- [x] 2.3 明确 PNG / 透明图保持原格式优先的处理方式，无法达标时记录 warning 且不阻断上传。
- [x] 2.4 确保 SKU 上传、SKU 暂存图片正式化、品牌 Logo、Banner 图片和品牌证书图片生成缩略图时读取同一全局配置。
- [x] 2.5 补充缩略图生成测试，覆盖默认不限制、20KB 目标、未达标回退、`.thumb` Key 稳定和原图上传不失败。

## 3. 管理后台设置页

- [x] 3.1 在系统设置“媒体与存储”上传限制区域新增缩略图体积上限字段和帮助文案。
- [x] 3.2 保持全页单一保存 CTA、恢复默认/dirty 切换 DS modal、fixed toast 和对象存储策略只读区不变。
- [x] 3.3 补充前端测试，覆盖字段渲染、保存 payload、reset、非法值提示、无 `window.confirm` 和布局不被提示块推挤。

## 4. 历史维护任务

- [x] 4.1 让历史缩略图审计/重生成任务读取当前 `media.thumbnail_max_size_kb` effective 配置。
- [x] 4.2 dry-run 输出候选数量、已符合、缺失、失败、跳过、预计写入和脱敏对象摘要，不写数据库或对象存储。
- [x] 4.3 apply 输出成功、失败、跳过、未达标、重试候选和二次审计摘要，并保持幂等。
- [x] 4.4 确认保存系统设置不会自动触发历史重生成，并用测试或维护任务 dry-run 证据覆盖。

## 5. 验证与文档

- [x] 5.1 运行后端 pytest，至少覆盖系统设置、上传缩略图、品牌/Banner/SKU/证书相关媒体测试和维护任务测试。本地可执行集已通过；`test_admin_brands.py` / `test_admin_tile_skus.py` collection 因当前 uv 环境缺 Pillow 阻断，依赖已在 `pyproject.toml` 声明。
- [x] 5.2 运行前端 Vitest，至少覆盖 `SystemSettingsPage` 和媒体设置 helper 相关测试。
- [x] 5.3 运行 OpenSpec 语言校验、目录结构校验和必要的 OpenAPI/Orval diff 复核。
- [x] 5.4 记录 Web Docker `http://localhost:3000` 上传边界验证或明确 N/A 原因。本 Change 未调整 Nginx、Docker Web 上传大小边界或上传控件状态机，Docker Web 边界验证 N/A。
- [x] 5.5 更新受影响长期文档、`.env.example` 或部署说明，并记录不适用项。已更新 API / 对象存储 / 上传标准文档；本配置存系统设置 key-value，不新增环境变量，`.env.example` N/A。

## 验收返修记录

- [x] 2026-08-05 23:03:58 `/opsx-modify`：修正历史缩略图维护任务 dry-run 口径；当 `media.thumbnail_max_size_kb` 为正整数且既有 `.thumb` 缩略图已存在但体积仍超过目标上限时，计入 `retry_candidates` / `estimated_writes`，并输出 `exceeds_target_size` 与 `thumbnail_exceeds_target_size` 原因。
- [x] 2026-08-05 23:16:00 `/opsx-apply`：新增生产媒体维护作业 Runbook，沉淀 BUG-0116 聚合媒体漂移任务和历史缩略图重新生成任务的 dry-run/apply 命令、处理过程、字段解读、验收口径与停止条件。
- [x] 2026-08-05 23:33:54 `/opsx-apply`：扩展独立历史缩略图重新生成任务的数据源，覆盖 SKU、品牌 Logo 和品牌证书图片三类对象，并同步维护任务说明、Runbook、对象存储策略和 delta spec。
