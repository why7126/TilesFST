# 任务清单

## 1. 后端与接口契约

- [x] 1.1 定位小程序证书详情接口、Schema 和服务层的 `brand` 数据来源。
- [x] 1.2 为证书详情 `brand` 数据补齐 `brand_logo_thumbnail_url` 或等价缩略图字段，确保字段来自后端受控媒体 URL。
- [x] 1.3 补充后端测试，覆盖有缩略图、无缩略图、品牌不可公开或品牌缺失场景。
- [x] 1.4 如 OpenAPI 响应结构变化，更新 OpenAPI、Orval 或小程序服务层类型，并记录字段语义。

## 2. 小程序品牌入口复用

- [x] 2.1 将证书详情页所属品牌入口改为复用 `brand-card`，移除页面私有品牌入口结构和私有点击逻辑。
- [x] 2.2 将证书详情 `brand` 数据映射为 `brand-card` 入参，包含 `brandId`、`brandName`、`brand_logo_thumbnail_url`、入口参数、`sourcePage=certificate_detail` 和 `certificateId`。
- [x] 2.3 确认 `brand-card` 优先消费 `brand_logo_thumbnail_url`，缩略图缺失或加载失败时使用统一占位，不请求原图作为默认 fallback。
- [x] 2.4 保持商品详情页和其他既有 `brand-card` 调用方兼容。

## 3. 埋点与安全边界

- [x] 3.1 统一证书详情页品牌入口点击事件名为 `brand_card_click`。
- [x] 3.2 确认事件参数仅包含允许的品牌、来源、证书和 request id 上下文。
- [x] 3.3 确认埋点上报失败不阻断品牌详情跳转。

## 4. 验证与证据

- [x] 4.1 补充小程序静态测试或单元测试，覆盖证书详情页复用 `brand-card`、事件名和缩略图字段消费。
- [x] 4.2 补充小程序媒体四联验收证据：key、object、URL、render 与 Network evidence。
- [x] 4.3 补充 320 / 375 / 430 pt 逻辑宽度截图或等价验收摘要，覆盖正常、缩略图缺失、图片失败、长品牌名和不可用态。
- [x] 4.4 回归商品详情页和其他 `brand-card` 调用方，确认展示、跳转、不可用态和埋点没有回退。

## 5. 文档与归档准备

- [x] 5.1 更新受影响 API、媒体或小程序文档；若无长期文档需要更新，在 Change trace 中记录不适用原因。
- [x] 5.2 运行聚焦测试、OpenSpec 校验、语言校验、目录结构校验和 Workflow Sync。
- [x] 5.3 在验收记录中回填 REQ-0121 的 AC、媒体四联证据和剩余风险。
