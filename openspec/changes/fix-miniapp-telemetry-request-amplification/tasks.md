## 1. 遥测请求边界

- [x] 1.1 在小程序统一请求封装中增加请求级遥测跳过标记，默认业务请求仍采集 API 性能指标。
- [x] 1.2 调整 `track()` 上报 `/api/v1/usage-events` 时的调用路径，确保 usage 请求成功或失败均不触发 RUM。
- [x] 1.3 调整 performance 上报路径，确保 `/api/v1/performance-events` 自身不会再派生新的 performance 请求。
- [x] 1.4 回归 `/api/v1/miniapp/home`、`/api/v1/miniapp/products` 和 `app_launch_ready`，确认业务 API 与启动性能观测不退化。

## 2. 商品卡曝光控制

- [x] 2.1 将商品卡曝光从逐次 observer 上报收敛为去重、队列批量或等价压力控制策略。
- [x] 2.2 覆盖同一页面、同一模块、同一列表上下文、同一 SKU 只上报一次曝光。
- [x] 2.3 覆盖同一 SKU 在不同模块或不同列表上下文中仍可按业务语义分别记录。
- [x] 2.4 确认埋点失败不会阻断商品卡展示、详情跳转、首页瀑布流加载或分享。

## 3. API、字典与隐私

- [x] 3.1 保持 `product_card_exposure`、`miniapp_home_waterfall_load` 等事件字段满足后端事件字典校验。
- [x] 3.2 确认 usage payload 不新增 Authorization header、Cookie、手机号、`.env` 内容、本机路径、对象存储原始 key 或真实客户隐私。
- [x] 3.3 若新增批量 usage 接收接口，同步后端 schema、OpenAPI、Orval、API 文档、错误码说明和测试；若不新增接口，在 Change trace 中记录“不需要 Orval”的依据。

## 4. 回归测试与证据

- [x] 4.1 补充或更新小程序测试，覆盖 usage 上报不触发 RUM、业务请求仍触发 RUM、曝光重复触发不重复请求。
- [x] 4.2 补充或更新后端 usage event 字典测试，覆盖合法事件、未知事件和禁止字段。
- [x] 4.3 冷启动小程序首页并记录网络面板证据，确认 usage-events 请求数量可控，performance-events 不包含 `/api/v1/usage-events` 样本。
- [x] 4.4 记录实现后的 API / DB / Orval / Docker Compose 影响结论。

## 5. 文档与收口

- [x] 5.1 更新 BUG-0143 acceptance evidence、Change `trace.md` 和 Sprint trace。
- [x] 5.2 运行 OpenSpec 校验、语言校验、目录结构校验和相关测试。
- [x] 5.3 如修复暴露新的埋点字典或批量接口治理需求，输出 follow-up capture 建议；无明确必要时不得自动创建 follow-up Issue。
