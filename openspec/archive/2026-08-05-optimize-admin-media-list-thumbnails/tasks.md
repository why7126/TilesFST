## 任务清单

- [x] 1. 后端契约
  - [x] 1.1 为管理端 SKU 列表项 Schema 增加 `main_image_thumbnail_url`。
  - [x] 1.2 为管理端 Banner 列表项 Schema 增加 `image_thumbnail_url`。
  - [x] 1.3 在 service 映射中复用受控媒体缩略图派生逻辑，缺失时返回空值并保留原图字段。

- [x] 2. Web 管理端展示
  - [x] 2.1 SKU 列表图片优先使用 `main_image_thumbnail_url`，失败或缺失时回退 `main_image_url` / 占位。
  - [x] 2.2 Banner 列表图片优先使用 `image_thumbnail_url`，失败或缺失时回退 `image_url` / 占位。
  - [x] 2.3 复核品牌列表和证书列表缩略图优先策略，并补齐必要测试或豁免说明（品牌列表已有 `logo_thumbnail_url` 优先测试；证书列表当前不渲染图片，证书媒体组件已有 `thumbnail_url` 优先）。

- [x] 3. API / Orval / 文档
  - [x] 3.1 重新导出 OpenAPI。
  - [x] 3.2 运行 Orval 生成前端客户端与类型。
  - [x] 3.3 同步 `docs/03-api-index.md` 或相关 API 文档片段，说明新增响应字段。

- [x] 4. 测试与验收
  - [x] 4.1 补充后端测试覆盖 SKU/Banner 缩略图字段、空图与原图兼容。
  - [x] 4.2 补充前端测试覆盖缩略图优先级、fallback 和无图态。
  - [x] 4.3 验收记录包含 URL/render 证据，证明列表使用缩略图且详情/预览保留原图。
  - [x] 4.4 执行 admin-list 横切验收：分页、toast、confirm、`window.confirm`、操作列布局不回归。

- [x] 5. 校验
  - [x] 5.1 运行后端相关 pytest。
  - [x] 5.2 运行前端相关 Vitest。
  - [x] 5.3 运行 OpenSpec 语言与结构校验。
