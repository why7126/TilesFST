---
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 15:19:57
---

# Tasks

- [x] 1. 小程序 RUM 版本号改为统一产品版本号口径，禁止用环境名作为 `app_version`。
- [x] 2. 小程序 RUM payload 补齐受控 `request_id`，接口耗时指标复用统一 API 请求 ID，非接口指标生成独立 RUM ID。
- [x] 3. 管理后台性能观测聚合页、样本页和筛选项补齐小程序指标中文标签，并复用同一标签映射。
- [x] 4. 管理后台性能观测聚合列表展示完整分组键，至少补充网络和设备列，并保证查看样本携带相同分组上下文。
- [x] 5. 管理后台性能观测聚合列表空态调整为规范表格内空态样式。
- [x] 6. 补充或更新小程序 RUM、管理后台性能观测展示和后端聚合上下文相关测试。
- [x] 7. 运行 OpenSpec、前端、小程序和后端聚焦校验；如实现过程发现真实事故价值，补充 `docs/knowledge-base/` 复盘记录。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-12 15:19:57 | 开发环境 API 地址仍由 `miniapp-env.py` 硬编码决定，不能跟随根目录 `.env` 的 `HOST_PORT_BACKEND` 在 `8010` 与 `8000` 间切换。 | `miniapp-env.py` 生成 dev `apiBaseUrl` 与 fallback 时改为读取根目录 `.env` 的 `HOST_PORT_BACKEND`，缺失时退回 `.env.example` 和默认 `8000`，不再在脚本中硬编码 `8010`。 | 补充小程序静态测试覆盖 env 生成脚本读取 `HOST_PORT_BACKEND` 与生成地址契约，并运行聚焦校验。 |
| 2026-08-12 15:10:10 | fallback 已能成功上报，但每条性能事件仍先请求不可用 `8010`，开发者工具 Network 持续出现红色失败噪音。 | RUM 上报在 2xx 成功后缓存当前可用 baseUrl，后续上报优先使用该地址，同时保留原 fallback 队列。 | 补充小程序静态测试覆盖可用 baseUrl 缓存契约，并运行聚焦校验。 |
| 2026-08-12 15:02:07 | 小程序 RUM 开发环境固定请求 `8010`，未复用 API fallback/baseUrl，导致本地后端在 `8000` 时 `performance-events` 全失败。 | RUM 上报改为按 `apiBaseUrl + apiFallbackBaseUrls` 依次尝试；连接失败或 5xx 时 fallback，4xx 停止。 | 补充小程序静态测试覆盖 RUM fallback 契约，并运行聚焦校验。 |
