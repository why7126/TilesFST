---
title: 修复小程序证书列表图片 URL 回填
change_id: fix-miniapp-certificate-media-urls
type: fix
status: proposed
source_bug: BUG-0147-miniapp-certificate-list-images-missing
source_sprint: sprint-028
created_at: 2026-08-30 10:44:25
updated_at: 2026-08-30 10:44:25
---

# 背景

`BUG-0147-miniapp-certificate-list-images-missing` 已确认生产小程序证书列表页中图片类证书全部显示“证书”占位。生产公开接口 `GET /api/v1/miniapp/certificates?page=1&pageSize=12` 能识别返回项为 `file_kind: "image"`，但同批记录的 `file_url` 与 `thumbnail_url` 均为空；小程序列表页按既有规范只在 `thumbnail_url` 可用时渲染图片，因此触发稳定占位。

该缺陷与 `REQ-0115-media-multi-variant-images` 的轻量图消费策略相关，也延续了 `BUG-0135-miniapp-certificate-card-file-url-fallback` 的边界：卡片不得 fallback 到 `file_url` 原文件。本次修复不放宽小程序端兜底规则，而是修正公开证书列表 API 与历史证书媒体数据的一致性，使图片类证书能拿到受控缩略图 URL。

# 变更内容

- 修复后端公开证书列表聚合逻辑，图片类证书在存在可信主图记录、可信 `file_key` 或可兼容旧单文件图片时，返回受控 `thumbnail_url`。
- 保持聚合列表 `file_url` 对卡片场景的安全边界：默认不向列表项下发原文件 URL 用作卡片 fallback。
- 补齐证书媒体 key / object / URL / render 四联验收，覆盖 `images/default/brand-certificates/`、历史 key 兼容、`.thumb.webp` 派生对象和小程序证书列表渲染。
- 如生产历史数据存在图片 key 仍落在 `files/default/brand-certificates/`、空 URL 或缺派生图，接入既有媒体维护 dry-run / apply / 幂等审计流程，生成脱敏摘要。
- 同步 API 文档、OpenAPI / Orval 判定、后端测试和小程序静态或设备验收任务。

# 能力影响

## 新增能力

- 无新增产品能力。

## 修改能力

- `miniapp-certificate-list-page`：强化公开证书聚合列表对图片类证书 `thumbnail_url` 的返回契约。
- `media-multi-variant-images`：补齐品牌证书图片历史数据回填、主图记录和受控缩略图 URL 的闭环要求。

# 影响范围

- 后端：`GET /api/v1/miniapp/certificates` 聚合查询、服务层媒体 URL 派生、品牌证书图片主图/旧单文件兼容。
- 小程序：证书列表页图片卡片渲染、加载失败占位、Network evidence。
- API：若响应字段语义、OpenAPI 示例或文档说明变化，需要同步 `docs/03-api-index.md` 和 Orval 生成物。
- 对象存储：证书图片 key 前缀、同目录 `.thumb.webp` 对象、受控 `/media/` URL、历史 key 兼容或回填。
- 数据库：当前不规划表结构变更；若实现阶段发现缺少必要字段或索引，需在设计和任务中追加 SQLite/MySQL schema、迁移和数据库文档同步。
- 产品数据采集与链路观测：适用 `backend_api`、`wechat_miniapp_request_flow`、`request_logs`、`maintenance_jobs`；若执行批量媒体回填任务，则同步适用 `task_traces` 与 `task_trace_spans`。

# 回滚计划

- 若后端列表 URL 派生修复引入错误，回滚到修复前的列表聚合逻辑，继续让小程序按占位兜底展示，不允许临时改为卡片请求原文件。
- 若历史媒体回填 apply 造成异常，使用执行前数据库备份和对象存储快照恢复；旧对象删除不纳入本 Change，需单独确认。
- 回滚后保留小程序图片加载失败占位策略、公开接口敏感字段过滤和请求日志脱敏边界。
