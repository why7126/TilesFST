## 背景

`BUG-0135-miniapp-certificate-card-file-url-fallback` 已确认小程序证书卡在缺少缩略图时存在直接 fallback 到 `file_url` 原文件的风险。该问题发生在品牌详情证书 Tab 等卡片展示场景，可能让列表或摘要浏览直接请求证书原图或原始文件。

该缺陷与 `REQ-0115-media-multi-variant-images` 的“列表/卡片使用 thumbnail，详情普通展示使用 display，预览/下载使用 original”策略不一致，也与已纳入 `sprint-025` 的证书详情 `display_url` 修复相邻但不相同：本 Change 聚焦卡片和摘要场景的原文件 fallback 边界。

## 变更内容

- 修复小程序品牌详情证书卡图片绑定，缺少 `thumbnail_url` 或缩略图加载失败时展示占位或受控失败态，不直接请求 `file_url` 原文件。
- 复核证书列表、品牌证书摘要、商品详情关联证书等证书卡片消费场景，统一“卡片不拉原文件”的展示策略。
- 明确后端品牌证书摘要接口中的 `file_url` 仅用于详情、预览或打开动作；卡片展示必须使用 `thumbnail_url`、卡片专用展示 URL 或占位。
- 补齐媒体四联验收、接口/静态测试、小程序 Network evidence、OpenAPI / Orval / API 文档同步任务。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `media-multi-variant-images`：补齐证书卡片场景不得 fallback 到 original/file_url 的多规格消费规则。
- `miniapp-certificate-list-page`：收紧证书卡片缺缩略图时的占位和失败态要求。
- `miniapp-brand-detail-home-page`：收紧品牌详情证书 Tab 卡片图片展示优先级和懒加载边界。

## 影响范围

- 后端：小程序品牌证书摘要接口字段语义、必要的卡片展示字段或兼容说明。
- 小程序：品牌详情页证书 Tab、证书列表页、其他复用证书卡片的摘要入口。
- API：如调整响应字段或字段说明，需要同步 OpenAPI、Orval 和 API 文档。
- 对象存储：图片证书 `images/default/brand-certificates/`、PDF/文档证书 `files/default/brand-certificates/`，以及缩略图对象可读性和审计摘要。
- 测试与验收：后端接口测试、小程序静态测试、媒体四联验收和小程序 Network evidence。

## 回滚计划

- 若修复导致证书卡无法展示图片，回滚小程序证书卡图片绑定和数据归一化，恢复到修复前策略，同时在验收记录中标注原文件 fallback 风险仍存在。
- 回滚不得删除或覆盖已生成的证书原文件、缩略图或 display 对象；如执行过历史对象 dry-run/apply，保留幂等摘要并按对象存储 runbook 单独处理。
- 回滚后仍必须保留 PDF/文档证书占位展示，避免将文档资源伪装为图片渲染。
