---
change_id: fix-miniapp-home-no-jump-banner-internal-title
status: implemented
created_at: 2026-08-21 08:45:32
updated_at: 2026-08-21 13:11:41
---

# 任务清单

- [x] 复核 `GET /api/v1/miniapp/home` 与 `GET /api/v1/miniapp/brands` 的 Banner DTO 字段，确认内部标题暴露路径和是否需要 OpenAPI/Orval 同步。
- [x] 实现后端公开 Banner 标题净化，禁止 `internal-*`、内部枚举和时间戳类标题进入公开小程序响应。
- [x] 补充小程序端防御，确保首页轮播、品牌列表页轮播、无跳转点击、搜索兜底、分享/埋点展示摘要不使用内部标题。
- [x] 保持后台 Banner 管理内部标题兼容能力，回归创建、编辑、列表、上线、下线和排序。
- [x] 补充后端回归测试：无跳转首页 Banner 与品牌列表页 Banner 均不暴露内部标题。
- [x] 补充小程序静态/交互回归：轮播不渲染 `item.title`，无跳转点击不显示内部标题。
- [x] 执行媒体四联验收：key、object、URL、render；若素材本身含内部标题，记录替换或清理摘要。
- [x] 如 API 字段语义或 schema 变化，更新 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。
- [x] 更新 BUG-0130 验收回填和 trace，保留根因证据闭环。
- [x] 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若不需要，在归档前说明原因。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-21 09:15:20 | 去掉首屏首页 Banner 图片上从左深到右浅的渐变遮罩，同时 Banner 图片不做透明化。 | 移除首页轮播图片后的 `hero-shade` 叠层，并取消 `.hero-image` 的透明度设置；保留无 Banner 兜底 Hero 的背景装饰。 | 待运行 `uv run pytest tests/test_miniapp_static.py::test_miniapp_home_runtime_entry_loads_home_data_and_interactions tests/test_miniapp_static.py::test_miniapp_home_images_have_runtime_fallback_handlers`。 |
| 2026-08-21 13:11:41 | 无跳转首页 Banner 点击后不显示“内容建设中”，保持静默。 | 首页 Banner 点击逻辑对 `jump_type === 'none'` 显式静默返回；保留搜索型 Banner 缺关键词时的防御提示。 | 待运行首页点击静态契约测试与 OpenSpec 校验。 |
