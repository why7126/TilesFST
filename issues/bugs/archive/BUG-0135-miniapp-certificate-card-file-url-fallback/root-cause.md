---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
root_cause_status: confirmed
category: design
created_at: 2026-08-22 21:11:44
updated_at: 2026-08-22 21:39:55
---

# Root Cause

## 根因状态

`confirmed`

代码定位和回归测试已闭环确认：品牌详情页证书卡片修复前使用 `thumbnail_url || file_url`，后端品牌证书摘要接口同时返回 `file_url` 和派生 `thumbnail_url`，这使卡片消费方在缩略图缺失、不可用或字段为空时能够直接退回证书原文件。

归档前已完成代码定位、端侧静态断言和后端接口回归测试；微信小程序 DevTools、真机或体验版 Network 证据在验收文档中按归档结论记录。

## 直接原因

品牌详情证书卡片在图片证书场景下使用 `src="{{item.thumbnail_url || item.file_url}}"`。当 `thumbnail_url` 缺失时，图片组件会直接请求 `file_url`，而 `file_url` 表达的是证书原文件访问入口，不适合作为列表或摘要卡片的默认展示资源。

## 根本原因

证书卡片展示契约没有明确区分“卡片展示资源”和“原文件预览/打开资源”。媒体多规格策略要求卡片场景优先消费缩略图或占位，原文件只应在详情、预览或下载动作中使用；但品牌证书摘要数据和小程序卡片模板仍保留可直接 fallback 到原文件的字段组合。

## 触发条件

1. 品牌证书为 JPG、PNG 或 WebP 图片证书。
2. 证书记录存在 `file_url`，但 `thumbnail_url` 缺失、为空、对象不可读或端侧未能消费。
3. 用户打开微信小程序品牌详情页证书 Tab，或其他复用同类证书卡片的摘要展示入口。
4. 证书卡片图片节点按照 `thumbnail_url || file_url` 求值。
5. 小程序端在卡片区域直接请求证书原文件。

## 证据链

| 证据入口 | 类型 | 摘要 | 结论 |
|---|---|---|---|
| `src/miniapp/pages/brand-detail/index.wxml` | 代码定位 | 品牌详情证书卡图片 `src` 使用 `item.thumbnail_url || item.file_url` | 缩略图缺失时卡片会退回 `file_url` |
| `src/backend/app/services/miniapp_home_service.py` | 代码定位 | `get_brand_certificates()` 返回 `file_url=item.file_url` 和 `thumbnail_url=self._certificate_thumbnail_url(...)` | 品牌证书摘要接口向卡片消费方暴露原文件 URL |
| `src/backend/app/schemas/miniapp_home.py` | 代码定位 | `MiniappCertificateItem` 包含 `file_url`、`thumbnail_url`，未提供卡片专用 `card_image_url` 或等价字段 | API 契约没有把卡片展示资源和原文件访问入口分离 |
| `src/miniapp/pages/certificates/index.wxml` | 对照代码定位 | 证书列表页只在 `item.file_kind == 'image' && item.thumbnail_url && !item.image_failed` 时渲染图片，否则展示占位 | 同类卡片已有“缺缩略图即占位”的更安全策略 |
| `issues/bugs/archive/BUG-0135-miniapp-certificate-card-file-url-fallback/bug.md` | 缺陷描述 | 正式 BUG 记录要求卡片缺缩略图时展示占位，不请求 `file_url` 原文件 | 修复与验收基线已明确 |
| `tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts` | 回归测试 | 断言品牌详情证书卡图片 `src` 只绑定 `item.thumbnail_url`，且不包含 `thumbnail_url || file_url` fallback | 端侧模板已移除原文件兜底 |
| `tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates` | 回归测试 | 断言品牌证书摘要接口保留 `file_url` 同时返回 `.thumb` 缩略图 URL | 原文件字段仅保留给详情/预览入口，卡片消费由端侧约束隔离 |

## 人工补证步骤

1. 在本地或测试环境请求品牌证书摘要接口，选择 1 条图片证书，记录脱敏后的 `file_url`、`thumbnail_url`、`file_kind` 字段摘要。
2. 准备或定位一条 `thumbnail_url` 缺失、对象不可读或返回空值的图片证书测试数据。
3. 使用微信小程序开发者工具打开品牌详情页证书 Tab，禁用缓存后记录证书卡片 Network 请求 URL、Size、Time、是否命中缓存。
4. 验证修复前是否请求 `file_url`；修复后应请求缩略图或不发起原文件请求并展示占位。
5. 对 PDF/文档证书补充一次卡片证据，确认使用 `files/default/brand-certificates/` 文件前缀，并在卡片上展示文件类型占位而不是图片请求。
6. 如修复涉及历史证书对象、缩略图生成或审计脚本，记录 dry-run、apply 和幂等摘要，并回填到 `acceptance.md`。

## 验证方式

- 修复前：品牌详情证书卡模板存在 `thumbnail_url || file_url` 绑定，缩略图缺失时会请求 `file_url` 原文件。
- 修复后：品牌详情证书卡模板只在图片证书存在 `thumbnail_url` 且未加载失败时渲染图片；缺缩略图或加载失败时展示占位，不再使用 `file_url`；证书详情页或明确预览动作仍可按受控策略访问原文件。
