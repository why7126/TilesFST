---
change_id: update-search-experience-unification
source_requirement: REQ-0128-search-experience-unification
source_sprint: sprint-026
acceptance_status: pending
created_at: 2026-08-27 00:19:59
updated_at: 2026-08-28 15:10:59
---

# 验收

## 产品数据采集与链路观测门禁

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - usage_events
    - request_logs
    - web_request_wrapper
    - miniapp_request_wrapper
    - api
  reason: 搜索体验优化会新增或调整搜索入口、列表筛选、搜索提交、结果曝光和请求链路透传。
  validation: apply 阶段必须回填事件字典、关键词脱敏、链路 ID、request logs 摘要、OpenAPI/Orval/DB 同步或 N/A、Task Trace N/A 证据。
```

## 验收清单

- [ ] 小程序首页展示高权重搜索入口，点击进入 `/pages/search/index` 并携带 `sourcePage=home` 或等价来源。
- [ ] 品牌、证书、商品列表、收藏具备统一搜索入口或列表内搜索路径；品牌列表页、证书列表页和收藏列表页搜索保持当前页卡片布局且不跳完整搜索结果页；底部 Tab「全部分类」页不展示搜索入口。
- [ ] `components/search-entry` 或等价封装支持入口模式和输入模式，并具备 `keyword`、`placeholder`、`scope`、`sourcePage`、disabled、提交、清空、取消等契约。
- [ ] 搜索页继续承接搜索首页、历史、热门、联想、综合结果、分区结果、无结果和加载更多。
- [ ] 搜索结果页品牌卡片展示品牌图片或稳定占位、品牌名称和 `x 个 SKU`，不得展示“x 个公开 SKU”。
- [ ] 搜索结果页证书卡片展示证书图片或稳定占位、证书名称、品牌和证书类型。
- [ ] 搜索结果页在下滑到底且仍有下一页时自动加载更多，并避免 loading 中重复请求。
- [ ] 综合 Tab 结果展示顺序为最佳匹配、品牌、证书、SKU；顶部 Tab 顺序保持综合、品牌、SKU、证书。
- [ ] 综合 Tab 后续页按分区合并，只向 SKU 分区追加新 SKU，不覆盖首屏最佳匹配、品牌和证书分区。
- [ ] 综合 Tab 和 SKU Tab 后续页使用 SKU-only 轻量响应，避免重复查询品牌、证书、facets、推荐词和最佳匹配。
- [ ] 首页带关键词进入完整搜索页时 SHALL 直接发起搜索结果请求，不额外请求搜索首页；搜索首屏 SHALL NOT 通过 `get_search_home()` 同步生成推荐词或触发 `hot_score metadata LIKE` 慢查询分支。
- [ ] 完整搜索首屏 SHALL 只执行当前 Tab 展示所需查询；综合 Tab 不查询未展示的 facets、类目 named、规格 named，品牌/证书/SKU 单独 Tab 不查询其他 Tab 数据。
- [ ] 品牌关键词精确命中或高置信命中时，完整搜索页 SKU 查询 SHALL 使用品牌 ID 过滤，不得回落到 SKU 名称、编码、品牌、规格、表面、色系和类目等多字段 `OR LIKE` 主路径。
- [ ] 完整搜索接口 SHALL 提供服务端分段耗时观测信号，至少能定位品牌识别、SKU list、SKU count、品牌 named、证书查询和总构建耗时，且不得在观测信号中输出关键词原文、SQL、内部对象 key 或结果明细。
- [ ] 小程序列表型 SKU 卡片构建 SHALL 避免逐卡片同步探测对象存储文件存在性；列表图片使用约定缩略图 / 展示图 URL，由端侧图片 fallback 承接缺失素材；详情主媒体、Banner、证书详情和品牌 Hero SHALL 保留存在性探测。
- [ ] 自动加载下一页时页面 SHALL 保留已展示结果，不得切换为整页“加载中...”空白态；底部仅展示轻量加载状态或“已加载全部”。
- [ ] 自动加载模式下页面 SHALL NOT 展示黄色“加载更多”主按钮。
- [ ] 商品列表和证书列表既有“不展示搜索入口”旧约束已按新 spec 调整，且未引入复杂筛选抽屉或高级排序。
- [ ] 品牌列表页支持 `keyword` 按品牌名称、品牌简称和品牌英文名过滤；搜索态隐藏 Banner 轮播，清空后恢复完整品牌列表和 Banner。
- [ ] 证书列表页支持 `keyword` 按证书名称、品牌名称、证书类型枚举或中文类型标签过滤；搜索结果保持证书卡片布局，清空后恢复完整公开证书列表。
- [ ] 收藏列表页搜索只过滤当前收藏范围，搜索结果保持收藏卡片布局，空态弱化全局搜索调整入口并保留清空关键词路径。
- [ ] 管理端主要列表搜索区、筛选区、重置、表格、分页、空态和错误态体验一致。
- [ ] 管理端搜索、筛选、重置后分页回到第一页，并展示后端真实 total。
- [ ] 管理端搜索遵守权限边界，小程序搜索只返回公开可见数据。
- [ ] 搜索请求失败保留关键词和筛选条件，联想失败不阻断直接搜索提交。
- [ ] 小程序 320/375/430 pt 或等价视口下搜索入口、列表内容、悬浮按钮和 TabBar 不发生不可接受遮挡。
- [ ] Web 管理端实现不新增裸 Hex，使用 semantic token 或既有共享样式。
- [ ] 新增或调整 API 参数时同步 OpenAPI、Orval、API 文档、前后端测试；不改 API 时记录 N/A。
- [ ] 新增 DB 索引或检索字段时同步 SQLite/MySQL schema、迁移、数据库文档和测试；不改 DB 时记录 N/A。
- [ ] 行为事件覆盖搜索入口点击、输入停顿、提交、联想曝光/点击、结果曝光/点击、无结果、列表筛选和重置。
- [ ] 行为属性包含来源页面、搜索范围、关键词脱敏摘要、结果数量、选中 Tab、筛选条件摘要和请求 ID。
- [ ] 普通搜索默认 Task Trace N/A；若出现复杂长耗时查询，已按 Task Trace 覆盖规则补充。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
evidence: []
failed_items: []
notes: /req-opsx 仅创建 Change 文档；实现、测试和验收证据由 /opsx-apply 与 /opsx-archive 回填。
```
