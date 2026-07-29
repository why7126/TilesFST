---
sprint_id: sprint-013
title: Sprint 013 发布说明
status: published
lifecycle_stage: archive
created_at: 2026-07-28 00:24:49
updated_at: 2026-07-29 09:24:09
owner: product
---

# Sprint 013 发布说明

## 发布范围

| 类型 | ID | 标题 | 状态 |
|---|---|---|---|
| REQ | REQ-0077-category-name-max-length-15 | 类目名称输入最多 15 个字符 | done |
| REQ | REQ-0078-certificate-multiple-images-main-image | 证书支持多图上传与主图设置 | done |
| REQ | REQ-0079-admin-sku-list-published-at | 管理端瓷砖 SKU 列表新增发布时间列 | done |
| REQ | REQ-0080-miniapp-certificate-detail-page | 微信小程序新增证书详情页 | done |
| BUG | BUG-0086-miniapp-sku-detail-remark-not-shown | 小程序商品详情页备注说明信息没有显示 | done |
| BUG | BUG-0087-miniapp-brand-detail-product-tab-sort-order | 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序 | done |
| BUG | BUG-0088-admin-sku-edit-save-extra-step | 管理端 SKU 编辑保存成功后未直接关闭弹窗 | done |
| BUG | BUG-0089-admin-certificate-edit-image-filename-noise | 管理端证书编辑弹窗图片下方显示无意义文件名 | done |
| Change | update-category-name-max-length-15 | 类目名称长度上限调整 | archived |
| Change | update-certificate-multiple-images-main-image | 品牌证书多图上传与主图设置 | archived |
| Change | update-admin-sku-list-published-at | 管理端 SKU 列表发布时间列 | archived |
| Change | add-miniapp-certificate-detail-page | 小程序证书详情页 | archived |
| Change | fix-miniapp-sku-detail-remark-display | 小程序商品详情页备注说明展示修复 | archived |
| Change | fix-miniapp-brand-detail-product-sort-order | 品牌详情页商品排序修正 | archived |
| Change | fix-admin-sku-edit-save-extra-step | 管理端 SKU 编辑保存成功态修复 | archived |

## 用户可见变化

- 管理端类目新增 / 编辑时，类目名称最多可输入 15 个字符。
- 运营可使用更完整的瓷砖类目名称，减少缩写造成的含义不清。
- 微信小程序商品详情页展示已维护的备注说明信息，商品公开资料更完整。
- 管理端品牌证书新增 / 编辑支持多张图片和主图设置。
- 品牌证书列表优先展示主图缩略图，便于快速识别证书内容。
- 微信小程序新增证书详情页，用户可查看单张证书完整信息、图片/PDF、所属品牌并分享给客户。
- 证书列表页卡片点击进入详情页，详情页内提供图片预览或 PDF 受控打开。
- 微信小程序品牌详情页商品 Tab 按发布时间升序、ID 升序稳定展示当前品牌商品。
- 管理端瓷砖 SKU 列表新增发布时间列，便于运营区分首次发布和后续更新时间。
- 管理端品牌证书新增 / 编辑弹窗不再在证书图片上传说明下方展示无意义图片文件名。

## 技术同步范围

- 后端类目创建 / 更新校验。
- Web 管理端类目弹窗校验与错误提示。
- 管理端类目列表、类目树展示回归。
- 小程序与 Web 展示端分类入口 15 字符布局回归。
- OpenAPI、Orval、API/DB 文档与测试夹具。
- 小程序 SKU 详情页接口字段确认、端侧字段映射、页面展示和空态回归。
- 品牌证书 API、Schema、Service、Repository 与数据兼容逻辑。
- 品牌证书图片数组、主图、排序、旧单文件兼容与 MinIO 文件引用校验。
- Web 管理端品牌证书列表和新增/编辑弹窗多图上传状态。
- 证书图片上传 Docker Web 边界验收、后端 pytest、前端 Vitest。
- 小程序证书详情页路由、公开详情接口、证书列表跳转、品牌入口、分享、媒体预览和 PDF 打开。
- 小程序证书详情页 DevTools 320/375/430 pt evidence；真机不可用时标记 blocked 或 follow_up。
- 小程序公开商品列表接口在 `brandId` 过滤场景下的排序与分页稳定性测试。
- 管理端 SKU 列表响应发布时间字段确认、列表列顺序、时间格式、空值占位与 admin-list 横切回归。
- 管理端品牌证书图片上传组件文件名文本移除、图片操作能力和上传状态机回归。

## 不包含

- 不改变类目字符集、同层级唯一、编码自动生成、层级、排序权重、启停删除规则。
- 不做历史类目清洗或批量重命名。
- 不新增购物交易、库存管理或内部备注展示能力。
- 不实现店主 Web 证书详情页，不扩大管理端证书维护和上传能力。
- 不新增证书真伪校验、OCR、电子签章、防伪查询、证书与 SKU 强绑定、收藏、推荐、购物、购买、库存、促销或询价能力。
- 不做对象存储物理文件删除；删除证书图片仅解除业务关联。
- 不调整 SKU 图片、品牌 Logo、Banner 等其他媒体场景主图规则。
- 不改变普通商品列表、搜索页、新品榜或热销榜排序。
- 不新增品牌详情页 API 响应字段或数据库字段，除非实现阶段另行评审扩大范围。
- 不新增 SKU 发布时间筛选、排序、导出、发布流程、小程序或店主端展示。
- 不改变品牌证书图片上传、保存、删除、设为主图、预览、API、数据库或对象存储行为。

## 发布状态

当前为 published；Sprint 013 已完成归档闭环。8/8 Change 已归档，8/8 关联 REQ/BUG 已同步为 done/archive；小程序证书详情页 DevTools/真机 evidence 仍按 blocked/follow_up 保留为发布说明中的已知验证边界。
