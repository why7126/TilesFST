---
purpose: API设计规范
content: FastAPI接口路径、响应结构、错误码、OpenAPI、Orval生成规则
source: AI自动生成初稿，项目团队确认
update_method: 新增接口、修改接口、调整错误码或前端生成方式时更新
note: API变更必须同步docs/03-api-index.md和Orval客户端
updated_at: 2026-08-26 20:26:00
---

# API设计规范

## 1. 路径规范

接口统一使用 `/api/v1` 前缀。

推荐资源：

```text
/api/v1/tiles
/api/v1/tile-categories
/api/v1/tile-series
/api/v1/media/images
/api/v1/media/videos
/api/v1/admin/tiles
```

## 2. 响应结构

统一响应结构：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页响应：

```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

## 3. OpenAPI与Orval

- FastAPI必须正确暴露OpenAPI。
- 前端接口类型必须通过Orval生成。
- API变更后必须运行：

```bash
./scripts/generate-openapi-client.sh
```

## 4. 媒体API

媒体上传接口必须返回：

- media_id
- object_key
- url或preview_url
- mime_type
- size
- width/height，若适用
- duration，若为视频且可获取
- cover_url，若为视频且有封面

## 5. AI更新规则

AI新增或修改API时，必须同步：

```text
docs/03-api-index.md
openspec/changes/<change-id>/specs/*/spec.md
src/web/orval.config.ts
src/web/src/api/generated/
tests/integration/
```

## 6. 产品数据采集与链路观测门禁

API 变更若涉及请求头、请求日志、链路 ID、行为埋点、Task Trace、错误码、响应字段、OpenAPI contract 或 Orval 生成输入，MUST 读取 `docs/standards/product-data-collection-observability.md`。

触发范围内的 REQ、OpenSpec Change、tasks、acceptance 或 trace MUST 记录 `product_data_collection_observability` 或等价固定声明，至少包含适用状态、`affected_layers`、`reason` 和 `validation`。若不适用，MUST 说明为什么不影响 API、`request_logs`、`usage_events`、Task Trace 或端请求封装；不得只写“无”或“不涉及”。
