---
title: 修复小程序证书列表图片 URL 回填追踪
change_id: fix-miniapp-certificate-media-urls
type: fix
status: implemented
source_bug: BUG-0147-miniapp-certificate-list-images-missing
source_sprint: sprint-028
created_at: 2026-08-30 10:44:25
updated_at: 2026-08-30 11:46:57
---

# 变更追踪

```yaml
change_id: fix-miniapp-certificate-media-urls
type: fix
status: implemented
source_bug: BUG-0147-miniapp-certificate-list-images-missing
source_requirement: REQ-0115-media-multi-variant-images
source_sprint: sprint-028
affected_specs:
  - miniapp-certificate-list-page
  - media-multi-variant-images
product_data_collection_observability:
  status: applicable
  reason: 修复公开小程序证书列表 API 的媒体字段契约，并可能触发证书历史媒体 dry-run/apply 维护任务，需要保留请求日志、端侧请求链路和维护任务脱敏摘要。
  affected_layers:
    - backend_api
    - wechat_miniapp_request_flow
    - request_logs
    - maintenance_jobs
  validation: 本地接口回归、小程序静态测试、OpenSpec strict、语言、目录、Sprint scope 与观测门禁均通过；DevTools Network 与模拟器渲染 evidence 已补；用户确认开发环境不需要真机或体验版独立 Network evidence。
```

## 来源

- BUG：`BUG-0147-miniapp-certificate-list-images-missing`
- Sprint：`sprint-028`
- 父需求：`REQ-0115-media-multi-variant-images`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-30 10:44:25 | `/bug-opsx` | 创建 OpenSpec 修复 Change，等待实现。 |
| 2026-08-30 11:14:30 | `/opsx-apply` | 修复证书列表媒体 URL / 缩略图派生链路，补充空 URL + 可信图片 key 回归测试，并更新 API 文档。 |
| 2026-08-30 11:42:40 | `/miniapp-confirm` | 记录 DevTools Network 与模拟器渲染 evidence：证书接口和缩略图资源 200，品牌证书 Tab 与证书列表页均显示真实缩略图；真机或体验版独立 Network evidence 待补。 |
| 2026-08-30 11:46:57 | `/opsx-archive` | 用户确认开发环境不需要真机或体验版独立 Network evidence，开发验收闭环。 |

## 验证摘要

| 类型 | 状态 | 证据 |
|---|---|---|
| OpenSpec strict | pass | `openspec validate fix-miniapp-certificate-media-urls --strict` |
| Change 语言校验 | pass | `python scripts/validate-openspec-language.py --root openspec/changes/fix-miniapp-certificate-media-urls` |
| 目录结构 | pass | `python scripts/validate-directory-structure.py` |
| 产品数据采集与链路观测门禁 | pass | `python scripts/validate-product-data-observability-gates.py --change fix-miniapp-certificate-media-urls` |
| Sprint scope | pass | `python scripts/validate-sprint-scope.py sprint-028 --item BUG-0147-miniapp-certificate-list-images-missing --item fix-miniapp-certificate-media-urls` |
| 后端接口与小程序静态测试 | pass | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`，90 passed |
| DevTools Network 与渲染 | pass_devtools | `issues/bugs/archive/BUG-0147-miniapp-certificate-list-images-missing/screenshots/20260830-1138-devtools-brand-certificates-render.png`、`issues/bugs/archive/BUG-0147-miniapp-certificate-list-images-missing/screenshots/20260830-1139-devtools-certificate-list-render.png` |
| 证书缩略图回填脚本测试 | blocked | `uv run pytest tests/test_backfill_brand_certificate_thumbnails.py` 收集阶段缺少 `PIL`，未执行 |
