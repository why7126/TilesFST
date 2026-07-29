---
requirement_id: REQ-0080-miniapp-certificate-detail-page
title: 微信小程序证书详情页原型上下文
status: pending_review
created_at: 2026-07-29 08:06:38
updated_at: 2026-07-29 08:06:38
---

# 证书详情页原型上下文

## 1. 设计目标

证书详情页用于承接证书列表、品牌详情和微信分享入口，完整展示单张公开证书。页面参照商品详情页的大媒体区、信息分区、品牌入口、分享和错误态，但删除收藏、推荐、价格、库存、购物和询价相关元素。

## 2. 参考基线

- `REQ-0044-miniapp-sku-detail-page`：大媒体区、品牌入口、分享、骨架屏、错误态。
- `REQ-0057-certificate-list-page`：公开证书数据范围、证书卡片字段、证书文件预览策略。
- `REQ-0078-certificate-multiple-images-main-image`：证书多图、主图、排序和旧单文件兼容。
- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`：详情页分享直达、返回兜底、状态栏和胶囊避让。

## 3. 页面结构

```text
CertificateDetailPage
├── CustomNavigation
├── MediaHero
│   ├── 主图 / 多图轮播
│   ├── PDF / 未知文件占位
│   └── 图片数量与有效状态 Badge
├── CertificateSummary
│   ├── 证书名称
│   ├── 证书类型
│   └── 有效状态
├── BrandEntry
├── CertificateInfoPanel
│   ├── 证书编号
│   ├── 发证机构
│   ├── 有效期
│   └── 更新时间
├── DescriptionPanel
└── BottomActionBar
    ├── 打开文件 / 预览图片
    └── 分享证书
```

## 4. 视觉约束

- 深色页面背景，卡片使用深色低对比面。
- 品牌金只用于有效状态、重点 Badge、主按钮和分享按钮。
- 顶部媒体区是首屏主视觉，不放入小卡片。
- 证书详情不是电商页，不出现价格、收藏、推荐、购买、购物车和询价。
- 长字段必须可截断或换行，不产生横向滚动。

## 5. 状态覆盖

- 正常图片证书：主图 + 信息 + 品牌入口 + 底部分享。
- 多图证书：主图首项，支持轮播和图片预览。
- PDF 证书：顶部使用 PDF 占位，提供打开文件入口。
- 无公开文件：展示稳定占位和文字信息。
- 加载失败：错误态 + 重新加载 + 返回。
- 分享直达：无上一页栈时返回首页或证书列表。

## 6. 验收说明

- HTML 原型用于布局、信息层级和状态表达参考，不等同小程序最终实现。
- PNG Golden Reference 待后续设计导出。
- 后续 OpenSpec 设计需明确详情接口字段、旧单文件兼容和证书多图字段映射。
