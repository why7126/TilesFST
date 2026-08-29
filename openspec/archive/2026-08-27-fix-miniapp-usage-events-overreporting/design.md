## 根因结论

BUG-0144 的根因状态为 `confirmed`。小程序商品列表页在加载成功后对首屏商品逐条上报 `product_list_item_exposure`，同一页面又通过 `product-card` 组件触发 `product_card_exposure`。搜索页 `onInput()` 对每次输入变化立即上报 `search_input`，但搜索建议请求才具备 300ms 防抖。搜索结果加载后上报 `search_result_exposure`，结果 SKU 继续通过商品卡片组件曝光，当前缺少统一的去重键、重置窗口和事件语义边界。

## 修复方案

### 列表曝光口径

商品列表页需要收敛页面级与组件级曝光的关系。实现可选择以下等价策略之一：

- 以 `product_card_exposure` 作为 SKU 级主曝光口径，商品列表页不再对同一批 SKU 逐条发送 `product_list_item_exposure`。
- 保留 `product_list_item_exposure` 作为页面级或列表级聚合事件，但不得与 `product_card_exposure` 对同一 SKU、同一列表实例、同一窗口重复计入。
- 使用共享曝光 helper 判断事件是否已经由当前页面、模块、列表上下文和 SKU 记录过，重复 observer、重复 setData、列表重排不得重复发送。

### 搜索输入频控

搜索输入埋点不得与每个字符变化一比一绑定。实现可选择防抖、合并、采样或仅关键行为上报：

- 连续输入期间只在防抖窗口结束后记录一次受控 `search_input`。
- 对清空、取消、提交搜索等关键行为保留明确事件。
- payload 只保留必要关键词摘要、长度、来源页面、`requestId` 或等价上下文，不记录手机号、Authorization、Cookie、原始敏感内容或本机路径。

### 搜索结果与卡片曝光边界

搜索结果级曝光用于结果集合、模块或状态语义，商品卡片曝光用于 SKU 卡片语义。两者可同时存在，但必须满足：

- `search_result_exposure` 不得被解释为每个 SKU 的独立真实曝光，除非 payload 和去重策略明确支持集合语义。
- `product_card_exposure` 在同一关键词、同一 `requestId`、同一结果模块和同一 SKU 下应去重。
- 切换关键词、重新提交搜索、筛选条件变化、分页或列表上下文变化时，应按设计重置或延续去重窗口，并在测试中覆盖。

## 测试策略

- 小程序静态或单元测试覆盖商品列表页不会无边界同时上报 `product_list_item_exposure` 与 `product_card_exposure`。
- 小程序静态或单元测试覆盖搜索页 `search_input` 具备防抖、合并、采样或关键行为上报策略。
- 商品卡片曝光测试覆盖重复 observer、重复 setData、同 SKU 同上下文去重，以及不同模块、不同列表上下文、不同关键词或不同 `requestId` 可重新记录。
- 后端 usage event 字典测试继续覆盖保留事件的合法 payload、未知事件拒绝和禁止字段拒绝。
- 人工或等价自动化证据记录修复前后商品列表首屏、搜索连续输入和搜索结果展示的 `/api/v1/usage-events` 数量与事件名分布。

## 风险与边界

- 只删除某个事件名而不定义口径，会造成报表断层和后续分析歧义。
- 去重键过宽可能误杀不同模块或不同搜索上下文的真实曝光；去重键过窄会继续保留重复上报。
- 搜索输入频控应压缩高频噪音，但不得吞掉提交搜索、清空、取消等关键行为。
- 本 Change 不要求新增管理端报表、外部 BI、批量 usage API 或数据库结构；如实现期选择新增 API，必须同步 API、Orval、文档和测试。
