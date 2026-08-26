## 1. 曝光口径治理

- [x] 1.1 梳理商品列表页、搜索页和 `product-card` 的现有 usage event 调用点，确认 `product_list_item_exposure`、`product_card_exposure`、`search_result_exposure` 和 `search_input` 的保留口径。
- [x] 1.2 收敛商品列表页首屏曝光逻辑，确保同一批 SKU 不被无边界地同时逐条计入 `product_list_item_exposure` 与 `product_card_exposure`。
- [x] 1.3 为商品列表、搜索结果和商品卡片组件建立共享去重键或等价 helper，覆盖页面、来源模块、列表上下文、SKU、关键词或 `requestId`。
- [x] 1.4 明确刷新、分页、筛选切换、关键词切换和重新提交搜索时去重窗口的重置或延续规则。

## 2. 搜索输入频控

- [x] 2.1 将 `search_input` 从每次输入变化即时上报改为防抖、合并、采样或仅关键行为上报的受控策略。
- [x] 2.2 保留清空、取消、提交搜索等关键行为埋点，并确认埋点失败不阻断输入、建议加载或结果展示。
- [x] 2.3 确认搜索建议请求防抖与输入埋点频控互不替代，二者均有独立可验证行为。

## 3. 字典、安全与兼容

- [x] 3.1 保持保留事件满足后端 `EVENT_DEFINITIONS` 必填字段和类型约束。
- [x] 3.2 确认 usage payload 不新增 Authorization header、Cookie、手机号、`.env` 内容、本机路径、对象存储原始 key、内部备注或真实客户隐私。
- [x] 3.3 若新增或调整 usage API，同步后端 schema、OpenAPI、Orval、API 文档、错误码说明和测试；若不新增接口，在 Change trace 中记录“不需要 Orval”的依据。

## 4. 回归测试与证据

- [x] 4.1 补充或更新小程序静态或单元测试，覆盖商品列表页曝光双口径收敛。
- [x] 4.2 补充或更新小程序静态或单元测试，覆盖搜索输入频控策略。
- [x] 4.3 补充或更新商品卡曝光去重测试，覆盖同上下文去重和不同上下文可重新记录。
- [x] 4.4 补充或更新后端 usage event 字典测试，覆盖保留事件合法 payload、未知事件拒绝和禁止字段拒绝。
- [x] 4.5 记录修复前后商品列表首屏、搜索连续输入和搜索结果展示的 `/api/v1/usage-events` 数量与事件名分布对比。

## 5. 文档与收口

- [x] 5.1 更新 BUG-0144 acceptance evidence、Change `trace.md` 和 Sprint trace。
- [x] 5.2 运行 OpenSpec 校验、语言校验、目录结构校验和相关测试。
- [x] 5.3 评估是否需要沉淀 `docs/knowledge-base/incidents/` 复盘；若无生产事故证据，记录无需新增事故复盘。
- [x] 5.4 如修复暴露新的埋点字典、批量接口或报表口径治理需求，输出 follow-up capture 建议；无明确必要时不得自动创建 follow-up Issue。
