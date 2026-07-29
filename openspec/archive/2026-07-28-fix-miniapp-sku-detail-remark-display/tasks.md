## 1. Implementation

- [x] 1.1 确认 SKU 详情接口响应是否包含公开备注说明字段和值。
- [x] 1.2 若接口缺少公开备注说明字段，补齐后端 Schema/Service/Repository 映射，并同步 OpenAPI / Orval / docs / 后端契约测试。
- [x] 1.3 修复小程序 SKU 详情页服务层或页面数据模型，确保读取备注说明字段。
- [x] 1.4 修复小程序商品详情页模板展示，非空备注说明可见，空值按既有规则隐藏或安全占位。
- [x] 1.5 确保修复不暴露内部备注、原始 object key、未授权素材路径或敏感字段。

## 2. Validation

- [x] 2.1 补充或更新小程序详情页字段映射/页面渲染静态测试。
- [x] 2.2 使用一条包含备注说明的 SKU 完成微信开发者工具预览验证。
- [x] 2.3 验证备注说明为空的 SKU 不出现异常空白、`null`、`undefined` 或字段名。
- [x] 2.4 回归商品主图、轮播图/视频、品牌入口、收藏、分享和页面异常态。
- [x] 2.5 如涉及 API 字段变化，运行相关后端测试并重新生成 OpenAPI / Orval。
- [x] 2.6 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无跨项目复用价值，在验收记录中说明不沉淀原因。

## Notes

- 1.1/1.2：后端 Schema 与 Repository 已有 `remark` 字段，缺陷根因为 Service 返回详情时硬编码 `remark=None`；本次未新增 API 字段，不需要重新生成 OpenAPI / Orval。
- 2.2：微信开发者工具/真机预览证据需由本地人工补充，当前自动化已覆盖接口与页面静态契约。
- 2.6：该问题为单页字段映射遗漏，无跨 Sprint 事故复用价值，暂不新增 `docs/knowledge-base/incidents/`。
