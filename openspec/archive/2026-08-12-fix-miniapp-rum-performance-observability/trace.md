---
change_id: fix-miniapp-rum-performance-observability
type: fix
status: applied
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 15:19:57
source_bug: BUG-0129-miniapp-rum-app-version-production
sprint: sprint-023
---

# Change Trace

```yaml
change_id: fix-miniapp-rum-performance-observability
type: fix
status: applied
source_bug: BUG-0129-miniapp-rum-app-version-production
sprint: sprint-023
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-12 15:19:57 | `/opsx-modify BUG-0129` | 验收明确小程序开发环境 API 地址应由根目录 `.env` 的 `HOST_PORT_BACKEND` 决定；已调整 `miniapp-env.py` 渲染 dev `apiBaseUrl` 与 fallback 时读取该端口，避免脚本硬编码 `8010`。 |
| 2026-08-12 15:10:10 | `/opsx-modify BUG-0129` | 验收发现 fallback 成功后仍每条先请求不可用 `8010`；已缓存 2xx 成功的可用 baseUrl，后续 RUM 上报优先使用该地址。 |
| 2026-08-12 15:02:07 | `/opsx-modify BUG-0129` | 验收发现开发环境 RUM 固定打 `8010` 导致本地后端 `8000` 时全失败；已改为复用小程序 API fallback/baseUrl 策略，并补充测试与规格约束。 |
| 2026-08-12 14:41:04 | `/opsx-apply BUG-0129` | 完成 Change 实现与聚焦校验，状态更新为 applied，待归档。 |
| 2026-08-12 14:29:16 | `/bug-opsx BUG-0129` | 从已评审并纳入 `sprint-023` 的 BUG-0129 创建 OpenSpec 修复 Change。 |
