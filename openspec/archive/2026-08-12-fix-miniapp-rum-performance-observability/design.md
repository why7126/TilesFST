---
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 15:19:57
---

# Design

## Scope

本 Change 仅修复 BUG-0129 对应的小程序 RUM 与管理后台性能观测口径：

- 小程序 `app_version` 不再使用环境名兜底。
- 小程序 RUM 上报补齐受控 `request_id`。
- 管理后台补齐小程序指标中文标签。
- 管理后台性能观测聚合列表展示完整分组键。
- 管理后台性能观测空态样式对齐表格内空态。

## 根因

1. 小程序 RUM 的版本号兜底使用 `miniappApiConfig.environment`，导致生产配置下 `app_version` 变为 `production`。
2. 小程序接口封装已有客户端请求 ID，但 RUM payload 没有承载 `request_id`，启动指标也没有生成独立追踪标识。
3. 管理后台性能观测页和样本页的指标标签映射未覆盖小程序指标枚举。
4. 后端聚合维度包含 `network_type`、`device_class`，但前端聚合列表隐藏这两个维度，导致不同聚合组看起来重复。
5. 聚合列表空态使用未规范化样式，视觉层级与管理端列表不一致。

## Solution

### 小程序 RUM 版本号

小程序 RUM SHALL 使用与 Web 管理后台一致的产品版本号来源。若运行环境无法提供真实小程序发布版本，端侧 SHALL 使用项目产品版本号或受控未知值，不得将环境名写入 `app_version`。

### 小程序 request_id

小程序 RUM SHALL 为每条性能事件写入受控 `request_id`。接口耗时指标 SHOULD 复用 API 封装生成的请求 ID；启动、页面生命周期等非接口指标 SHALL 生成独立 RUM 请求 ID。该字段不得包含 Token、openid、完整 URL、真实用户信息或随机明文业务数据。

小程序开发环境 API 配置 SHALL 由 `scripts/miniapp-env.py` 生成，dev `apiBaseUrl` 与 `apiFallbackBaseUrls` SHALL 读取根目录 `.env` 的 `HOST_PORT_BACKEND`；缺失或非法时再退回 `.env.example` 与默认 `8000`，不得在脚本中硬编码 `8010`。小程序 RUM 上报 SHOULD 复用小程序 API 的开发环境 baseUrl 与 fallback 策略。当前 baseUrl 连接失败或返回 5xx 时 SHALL 尝试下一个 fallback；4xx 校验错误 SHALL 停止重试，避免重复写入无效监控请求。若 fallback 返回 2xx，端侧 SHOULD 缓存该可用 baseUrl，并在后续 RUM 上报中优先使用它，减少每条性能事件都先触发连接失败的开发调试噪音。

### 管理后台指标标签

管理后台 SHALL 使用共享指标标签映射覆盖 Web 与小程序指标。小程序指标至少包含：

- `app_launch_ready`：小程序启动就绪
- `api_duration`：接口请求耗时
- `api_failed_duration`：接口失败耗时

聚合列表、样本页和指标筛选 SHALL 使用同一映射，未知指标可回退展示原始枚举值。

### 聚合列表完整分组键

管理后台性能观测聚合列表 SHALL 展示后端聚合使用的完整业务分组键，至少包含页面、版本号、端类型、指标、网络和设备。查看样本时 SHALL 携带同一分组上下文，保证样本明细与聚合行一致。

### 空态

聚合列表空态 SHALL 使用管理端表格内空态样式，字号、颜色、间距、最小高度和对齐方式与日志审计等列表保持一致。

## API / DB / UI Impact

- API：不新增接口；聚合与样本响应继续使用既有 `network_type`、`device_class`、`request_id` 字段。
- DB：不要求 schema 变更；历史样本保持原样。
- Web 管理后台：调整性能观测聚合列表、样本页、筛选项和空态。
- 小程序：调整 RUM 上报 payload 的版本号和 `request_id`。
- Orval：若 OpenAPI schema 未变更则不需要重新生成；若实现时收紧 schema 文档，应同步 Orval。

## 验证

- 小程序 RUM 上报 payload 中 `app_version` 不为 `production`、`development`、`dev` 等环境名。
- 小程序 API 耗时、失败耗时、启动就绪等样本均有非空 `request_id`。
- 小程序开发环境地址由根目录 `.env` 的 `HOST_PORT_BACKEND` 生成；切换 `8000` 或 `8010` 后重新执行环境生成，RUM 上报 SHALL 使用新配置。
- 小程序 fallback 成功后，后续 RUM 上报 SHOULD 优先使用缓存的可用 baseUrl。
- 管理后台聚合页和样本页显示小程序指标中文标签。
- 聚合列表显示网络和设备列后，同一页面/版本/端类型/指标下的不同分组可被区分。
- 空数据筛选条件下，聚合列表显示规范化空态。
- 回归 Web 管理后台 RUM 现有版本号与 `request_id` 展示不退化。
