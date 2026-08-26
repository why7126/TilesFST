---
change_id: fix-miniapp-usage-events-overreporting
change_type: fix
status: applied
source_bug: BUG-0144-miniapp-usage-events-overreporting
sprint: sprint-026
created_at: 2026-08-26 09:40:37
updated_at: 2026-08-26 10:02:13
---

# Change 追踪

## 基本信息

```yaml
change_id: fix-miniapp-usage-events-overreporting
change_type: fix
status: applied
source_bug: BUG-0144-miniapp-usage-events-overreporting
sprint: sprint-026
affected_capabilities:
  - product-usage-logging
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
orval_required: false
docker_compose_required: false
```

## 缺陷来源

- BUG：`issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/`
- Sprint：`iterations/change/sprint-026/`
- 根因状态：`confirmed`
- 关联 BUG：`BUG-0143-miniapp-telemetry-request-amplification`
- 目标：治理小程序商品列表页与搜索页 usage-events 偏多问题，收敛列表曝光双口径、搜索输入高频上报和曝光事件去重策略。

## 证据清单

| 证据 | 状态 | 说明 |
|---|---|---|
| 根因分析 | done | 见 BUG-0144 `root-cause.md`。 |
| 小程序代码定位 | done | 商品列表 `trackItems()`、搜索页 `onInput()` / `loadResults()`、商品卡 observer 已定位。 |
| OpenSpec delta | done | 已覆盖列表曝光口径、搜索输入频控、搜索结果与商品卡边界、去重键和安全字段。 |
| 单元或静态测试 | done | `uv run pytest tests/test_miniapp_static.py -q` 通过，覆盖商品列表曝光口径、搜索输入频控和商品卡去重键。 |
| 后端字典测试 | done | `uv run pytest tests/test_miniapp_home.py -q -k "usage_events_validate_dictionary or contract_drift_usage_events"` 通过，确认保留事件和禁止字段校验兼容。 |
| JS 语法检查 | done | `node --check` 覆盖 `components/product-card/index.js`、`pages/product-list/index.js`、`pages/search/index.js`。 |
| 网络证据 | done | 已补充商品列表页首屏、搜索连续输入和搜索结果展示三张微信开发者工具 Network 截图，见 BUG-0144 `screenshots/`。 |
| API / Orval 决策 | done | 采用小程序端口径收敛、去重和防抖，不新增后端 API，不涉及 DB 结构、Orval 或 Docker Compose。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-26 10:02:13 | 人工验收补证 | 补充商品列表、搜索输入、搜索结果三张微信开发者工具 Network 截图，证明 usage-events 数量受控。 |
| 2026-08-26 09:50:30 | `/opsx-apply BUG-0144` | 完成小程序列表曝光口径收敛、搜索输入频控、商品卡曝光去重键补强、测试与证据回填。 |
| 2026-08-26 09:40:37 | `/bug-opsx` | 从 BUG-0144 创建 OpenSpec fix Change，等待 Workflow Sync 回填 Sprint scope。 |
