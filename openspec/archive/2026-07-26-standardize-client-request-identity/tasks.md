## 1. 后端请求身份与日志模型

- [x] 1.1 确认客户端请求标识字段名、请求头兼容策略和长度 / 字符集约束，并在实现注释或 design follow-up 中固化。
- [x] 1.2 扩展请求日志 middleware，保持服务端可信 `request_id` 生成与 `x-request-id` 响应头返回不回归。
- [x] 1.3 增加客户端请求标识解析与校验，非法、缺失、超长时不得导致 500 或污染 metadata。
- [x] 1.4 扩展日志持久化模型、Repository、Service 和 Schema，保存 `client_request_id` 或等价字段。
- [x] 1.5 同步 SQLite schema、MySQL schema、migration、索引与 MySQL drift 校验。
- [x] 1.6 更新 usage event 上下文，使行为事件可携带相关 `request_id` 或客户端请求标识且失败不阻断主流程。

## 2. Web 与小程序请求封装

- [x] 2.1 扩展 Web 管理端 API client，注入 `x-client-type=web_admin` 和客户端请求标识。
- [x] 2.2 扩展店主 Web 前台 API client，注入 `x-client-type=web_catalog` 和客户端请求标识。
- [x] 2.3 扩展微信小程序统一 request 封装，注入 `x-client-type=wechat_miniapp` 和客户端请求标识。
- [x] 2.4 实现小程序 fallback base URL 重试复用同一客户端请求标识的策略。
- [x] 2.5 确认请求标识生成失败时三端均继续执行主业务请求。

## 3. 日志审计 UI

- [x] 3.1 更新 `/admin/logs` 列表字段，展示客户端类型、后端可信 `request_id`，并按 design 结论展示或隐藏客户端请求标识列。
- [x] 3.2 更新日志详情抽屉，分组展示 Trusted Request ID、Client Request ID 和响应头语义。
- [x] 3.3 保持长 ID 单行截断、完整复制和 fixed toast 反馈，不引起列表布局位移。
- [x] 3.4 保持 `admin-list` 横切 AC：分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`。

## 4. API 契约、文档与生成物

- [x] 4.1 更新日志 API request / response / query schema 与 OpenAPI 元数据。
- [x] 4.2 运行 Orval 生成并提交生成客户端，禁止手工修改 generated 文件。
- [x] 4.3 更新 `docs/03-api-index.md`、`docs/04-database-design.md` 和适用 API governance / error code 文档。
- [x] 4.4 若不实现 `client_request_id` 筛选参数，在 design 或验收记录中写明原因。

## 5. 测试与验证

- [x] 5.1 补充后端测试，覆盖三类 `client_type`、可信 `request_id` 响应头、客户端请求标识非法 / 缺失 / 超长降级。
- [x] 5.2 补充 Web 管理端测试，覆盖请求封装注入、日志审计字段展示、截断、复制成功与失败兜底。
- [x] 5.3 补充店主 Web 前台 smoke 或测试，覆盖 `web_catalog` 注入。
- [x] 5.4 补充小程序静态测试或 request 封装测试，覆盖 `wechat_miniapp` 注入和 fallback 重试复用客户端请求 ID。
- [x] 5.5 运行相关 pytest、Vitest / 小程序静态测试、OpenSpec validate 和必要的 schema drift 校验。
