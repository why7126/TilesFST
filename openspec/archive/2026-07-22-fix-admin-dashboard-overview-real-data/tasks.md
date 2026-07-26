## 1. Dashboard 数据源定位

- [x] 1.1 定位管理端 Dashboard 页面、数据概览组件、API client 和当前 Mock 数据来源。
- [x] 1.2 确认 4 个指标卡当前展示字段、辅助说明和现有布局约束。
- [x] 1.3 确认是否已有可复用的后端统计接口或列表页 total 接口。

## 2. 后端 / API 修复

- [x] 2.1 若已有真实接口可满足统计口径，复用现有接口并记录口径映射。
- [x] 2.2 若无可复用接口，新增受管理端鉴权保护的 Dashboard 概览接口。
- [x] 2.3 确保 SKU 总数、品牌数量、Banner 数量、用户数量与对应业务查询口径一致。
- [x] 2.4 确保 SQLite demo 与 MySQL 生产环境统计查询兼容。
- [x] 2.5 确保错误响应使用统一 envelope，不泄露 DSN、SQL、内部堆栈、MinIO 凭据或密钥。
- [x] 2.6 如新增或修改 API，同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关 API 文档。

## 3. Web 管理端修复

- [x] 3.1 移除生产页面成功态对 Mock 常量、演示数组或固定 fallback 值的依赖。
- [x] 3.2 接入真实 API client 或真实业务聚合结果。
- [x] 3.3 补齐 loading、empty、error 和无权限展示状态。
- [x] 3.4 保持四个指标卡、桌面四列网格、品牌金数值强调和现有视觉 token 不回退。
- [x] 3.5 确认前端不直连数据库或未授权对象存储。

## 4. 回归测试

- [x] 4.1 补充或更新后端/API 测试，覆盖真实统计成功返回。
- [x] 4.2 补充或更新后端/API 测试，覆盖空数据返回 0。
- [x] 4.3 补充或更新后端/API 测试，覆盖未授权或权限不足场景。
- [x] 4.4 补充或更新前端测试，覆盖 Dashboard 渲染真实数值。
- [x] 4.5 补充或更新前端测试，覆盖 loading、empty、error 状态。
- [x] 4.6 若 API 契约变化，运行 OpenAPI / Orval 生成并回归生成客户端使用点。
- [x] 4.7 如具备本地服务，完成管理端首页 smoke 验证；必要时使用 Docker Compose。

## 5. 文档与追溯

- [x] 5.1 更新 `BUG-0079` trace 和 Change trace 的实现/验收证据。
- [x] 5.2 在实现输出中说明是否影响 API、数据库、Web 管理端、小程序、Orval 与 Docker Compose。
- [x] 5.3 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
