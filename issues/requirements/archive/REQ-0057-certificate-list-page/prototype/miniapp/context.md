---
requirement_id: REQ-0057-certificate-list-page
status: pending_review
created_at: 2026-07-19 23:19:48
updated_at: 2026-07-19 23:19:48
prototype_type: miniapp-html-reference
---

# Prototype Context

## 定位

小程序 TabBar「证书」公开列表页，用于替代当前建设中占位页。原型为 HTML 参考稿，后续 OpenSpec Change 设计与实现应转换为微信小程序 WXML/WXSS，并复用项目已有 `custom-navigation` 组件。

## 页面结构

```text
CertificateListPage
├── CustomNavigation(title="证书")
├── SummaryHeader
│   ├── eyebrow: BRAND CERTIFICATES
│   ├── title: 菲尚特认证证书
│   └── stats: 公开证书 / 有效证书 / 绿色环保
├── SearchBox
├── FilterChips
│   ├── 全部
│   ├── 质量体系
│   ├── 产品检测
│   ├── 绿色环保
│   └── 荣誉资质
├── CertificateList
│   └── CertificateCard[]
└── LoadMore / Empty / Error
```

## 核心状态

- `loading`: 首屏骨架屏。
- `refreshing`: 下拉刷新。
- `loadingMore`: 触底加载更多。
- `empty`: 无公开证书。
- `filterEmpty`: 有筛选条件但无结果。
- `error`: 网络失败，保留重试入口。
- `previewFailed`: 证书文件暂时无法预览。

## 视觉约束

- 暗色页面背景、低圆角卡片、极细分割线、品牌金作为激活态。
- 证书卡片使用单列布局，左侧稳定缩略图或 PDF 占位，右侧为证书摘要。
- 筛选 chip 横向滚动，不遮挡主要列表。
- 长文本在移动端截断或换行，不撑破卡片。
- 页面顶部必须避让自定义导航和微信原生胶囊 reserve。

## 待导出

- PNG Golden Reference：待后续设计评审导出。
