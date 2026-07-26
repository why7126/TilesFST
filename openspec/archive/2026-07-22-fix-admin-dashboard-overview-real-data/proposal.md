## Why

`BUG-0079-admin-dashboard-overview-mock-data` 已评审通过。管理端 `/admin/dashboard` 首页的数据概览仍使用 Mock 数据，无法反映系统中的 SKU、品牌、Banner、用户等真实业务状态，降低首页信息可信度，并可能误导管理员进行运营判断。

现行 `admin-dashboard` 规格中「管理端 Dashboard 数据概览」仍明确要求“本期 MUST 使用 mock 数据”，这与当前缺陷修复目标冲突。需要通过修复 Change 将该能力调整为真实数据源驱动，并补充加载、空数据、错误状态、权限边界、API 同步与回归测试要求。

## What Changes

- 修改 `admin-dashboard` 规格：数据概览 4 个指标卡继续保留，但数值必须来自真实后端接口或真实业务聚合结果。
- 明确 SKU 总数、品牌数量、Banner 数量、用户数量的统计口径需要与管理端列表页或后端查询保持一致。
- 要求页面具备 loading、empty、error 状态，接口失败时不得以 Mock 数据伪装成功结果。
- 要求真实数据接入遵守管理端鉴权和权限边界。
- 要求如新增或修改 API，必须同步 OpenAPI、Orval、API 文档和后端/前端测试。
- 要求补充回归测试，覆盖真实数据、空数据、错误状态和至少一个指标口径校验。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `admin-dashboard`: 将 Dashboard 数据概览由 Mock 数据改为真实数据源，并补充数据状态、权限与测试约束。

## Impact

- **web/admin:** 预计修改管理端 Dashboard 首页数据概览组件的数据获取逻辑，移除 Mock 常量或限制为测试夹具。
- **api:** 可能新增或复用管理端 dashboard summary API；若新增或调整接口，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和接口测试。
- **database:** 不预期新增表或迁移；统计查询需兼容 SQLite demo 与 MySQL 生产环境。
- **miniapp:** 不涉及。
- **tests:** 需要补充后端/API 测试与前端页面测试，覆盖真实数据、空数据、错误状态、权限边界和指标口径。
- **docker:** 若新增 API 或后端统计查询，建议在 Docker Compose 本地环境完成 smoke 验证。

## Rollback Plan

如修复后 Dashboard 首页出现白屏、关键 API 连续失败或统计口径严重错误，可回滚前端真实数据接入和新增 API 到修复前版本，但不得恢复“接口失败展示 Mock 数据”的误导性兜底。回滚后应在验收记录中标明首页概览暂不可用，并重新评估 `BUG-0079`。
