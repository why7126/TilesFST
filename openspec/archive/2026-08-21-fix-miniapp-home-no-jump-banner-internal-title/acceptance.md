---
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: implemented
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 13:45:41
source_bug: BUG-0130-miniapp-home-no-jump-banner-internal-title
---

# 验收计划

## 回归验收

- 首页无跳转 Banner 不显示 `internal-*`、`MINIAPP_HOME`、`NO_JUMP` 或时间戳类内部标识。
- `GET /api/v1/miniapp/home` 公开响应不暴露后台内部标题。
- `GET /api/v1/miniapp/brands` 品牌列表页轮播公开响应不暴露后台内部标题。
- 无跳转首页 Banner 点击保持静默，不显示“内容建设中”；搜索兜底、分享文案和埋点展示摘要不包含内部标题。
- 首页首屏 Banner 图片不叠加从左深到右浅的渐变遮罩，且图片不做透明化。
- 后台 Banner 创建、编辑、列表、上线、下线、排序和跳转类型配置保持可用。

## 媒体四联验收

模板：`docs/standards/media-bug-four-point-acceptance-template.md`

| 维度 | 要求 |
|---|---|
| key | 记录脱敏 Banner `image_object_key`，确认与业务记录一致且符合 Banner 图片前缀策略。 |
| object | 确认图片对象真实存在，且图片像素不包含 `internal-*` 内部标题；若包含，记录替换/清理摘要。 |
| URL | 确认公开 `image_url` 可访问，且公开 DTO 不返回内部标题。 |
| render | 使用小程序 DevTools、真机或体验版补充首页轮播和品牌列表页轮播 render evidence。 |

## 验收结果回填

| 时间 | 结果 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-21 08:54:22 | pass_with_pending_render_evidence | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`：77 passed；新增 `test_miniapp_public_banners_hide_internal_no_jump_titles` 覆盖首页/品牌页内部标题 DTO 净化与搜索词净化；静态测试覆盖首页/品牌页搜索跳转不使用原始标题兜底。 | 字段 schema 未变化，不需要 Orval；当前环境未连接小程序 DevTools/真机，render evidence 需发布前补充。 |
| 2026-08-21 09:15:20 | modify_pending_validation | 验收反馈要求去掉首页 Banner 从左深到右浅的渐变遮罩，并取消 Banner 图片透明化；已调整小程序首页 WXML/WXSS 与静态测试契约。 | 待运行聚焦静态测试并补充小程序 DevTools/真机 render evidence。 |
| 2026-08-21 13:11:41 | modify_pending_validation | 验收反馈要求无跳转首页 Banner 点击后不显示“内容建设中”，保持静默；已调整首页点击逻辑与静态测试契约。 | 待运行聚焦静态测试；最终仍需小程序 DevTools/真机 render evidence。 |
| 2026-08-21 13:45:41 | pass | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py`：77 passed；`uv run pytest tests/test_miniapp_static.py::test_miniapp_home_runtime_entry_loads_home_data_and_interactions`：1 passed；用户补充首页运行截图。 | 用户截图确认首屏 Banner 无内部标题、无渐变遮罩、不透明化；无跳转点击静默由静态契约测试覆盖。API schema 未变化，不需要 Orval。 |
