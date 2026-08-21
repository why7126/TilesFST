---
title: 小程序媒体四联验收最佳实践
purpose: 沉淀小程序媒体 key/object/URL/render 四联验收、Network evidence、历史对象审计与 helper 使用口径
content: BUG-0125、BUG-0126 经验复盘与可复用验收片段
source: REQ-0111-miniapp-media-four-part-acceptance-practice
update_method: 小程序媒体验收、审计 helper 或测试 helper 变化时同步更新
created_at: 2026-08-12 14:54:20
updated_at: 2026-08-12 14:54:20
---

# 小程序媒体四联验收最佳实践

## 1. 背景

BUG-0125、BUG-0126 暴露出同一类风险：媒体验收只确认对象存在，不能证明小程序端实际可见、可预览、可播放或性能收益成立。小程序媒体验收必须同时覆盖 `key`、`object`、`URL`、`render` 四联，并把 DevTools、真机或体验版 Network evidence 与历史对象审计结果分开记录。

本最佳实践适用于小程序 SKU 图片、SKU 视频、视频封面、品牌 Logo、品牌 Banner、品牌证书图片、缩略图和受控 `/media` URL。

## 2. 四联验收链

| 维度 | 验收目标 | 最小证据 |
|---|---|---|
| `key` | 业务记录中的媒体 key 稳定、符合单 Bucket 与标准前缀策略 | 脱敏 key hash、标准前缀、资源类型、是否 pending/fallback |
| `object` | 对象存储 object 真实可读，MIME、size、缩略图或封面关系正确 | 存在性、MIME、size、缩略图收益、失败原因枚举 |
| `URL` | 小程序使用后端受控 URL 或安全静态资源，不直连未授权对象存储 | URL 类型、HTTP 状态、业务状态、资源大小、耗时 |
| `render` | 小程序端展示、预览、播放、poster/cover、fallback、失败态符合预期 | DevTools/真机/体验版页面、截图/录屏/人工摘要、组件状态 |

任一维度为 `fail` 时不得写作验收通过；任一维度为 `blocked` 时必须记录阻塞原因、责任环境和补证方式。

## 3. Network Evidence

小程序媒体 Network evidence 至少记录：

| 字段 | 说明 |
|---|---|
| `source` | `network_devtools` 或 `network_trial` |
| `page_path` | 页面路径、query 和场景 |
| `media_kind` | `image` / `video` / `poster` / `cover` / `thumbnail` / `certificate_image` |
| `media_url_type` | `controlled_media_url` / `static_asset` / `signed_url` / `fallback` |
| `request_domain` | 请求域名，生产验收应为生产 API 或受控媒体域名 |
| `http_status` | HTTP 状态 |
| `business_status` | 业务响应状态或 N/A 原因 |
| `resource_bytes` | 资源大小摘要；不得记录敏感 header |
| `duration_ms` | Network 面板可见耗时摘要 |
| `render_result` | 页面展示、预览、播放、poster/cover、fallback 或失败态结论 |

DevTools Network 不等同于体验版或真机网络验收；缺少体验版证据时应写 `blocked` 或 `follow_up`，不得自动写 `passed`。

## 4. Helper 使用口径

测试 helper 用于静态约束小程序模板和 URL 安全边界，覆盖：

- 图片 `src` 必须包含展示 URL 与 fallback。
- 图片 preview 必须使用 `data-url` 或等价预览 URL。
- 视频 `src`、`poster`/`cover`、播放事件和失败态必须可断言。
- 图片列表应覆盖 `lazy-load` 策略。
- 小程序生产媒体 URL 应优先通过受控 `/media/` 相对路径或明确的静态资源路径。

测试 helper 不替代 DevTools、真机或体验版 Network evidence。

审计 helper 用于历史对象盘点，必须默认 dry-run，并输出脱敏统计：

- `classification_summary`：按 `missing_key`、`object_missing`、`thumbnail_missing`、`thumbnail_no_benefit`、`url_fallback_risk`、`closed` 分类。
- `deidentified_items`：只保留资源类型、资源 ID、key hash、标准前缀、四联状态和失败原因。
- `backfill`：写入动作必须显式参数触发，并记录 dry-run/apply、成功、失败、失败原因与幂等摘要。

审计 helper 的 dry-run 结果不能替代小程序 render evidence。

## 5. 可复制验收片段

```markdown
## 小程序媒体四联验收

| 维度 | 状态 | 证据 |
|---|---|---|
| key | pass / fail / n/a / blocked | 脱敏 key hash、标准前缀、资源类型、是否 fallback |
| object | pass / fail / n/a / blocked | object 存在性、MIME、size、缩略图/封面收益 |
| URL | pass / fail / n/a / blocked | URL 类型、HTTP 状态、业务状态、资源大小、耗时 |
| render | pass / fail / n/a / blocked | DevTools/真机/体验版页面表现、截图/录屏/摘要 |

Network evidence:
- source:
- page_path:
- media_kind:
- media_url_type:
- request_domain:
- http_status:
- business_status:
- resource_bytes:
- duration_ms:
- render_result:
- blocker_or_follow_up:
```

## 6. 安全边界

验收记录和 helper 输出不得包含 access key、secret key、Authorization header、Cookie、数据库连接串、真实 `.env` 内容、本机绝对路径、未脱敏 object key 全量值或真实客户数据。需要定位历史对象时，使用 key hash、标准前缀、资源类型和资源 ID。
