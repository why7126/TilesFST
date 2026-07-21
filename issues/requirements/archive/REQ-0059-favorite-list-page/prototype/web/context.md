---
requirement_id: REQ-0059-favorite-list-page
status: approved
created_at: 2026-07-19 23:13:48
updated_at: 2026-07-19 23:35:25
owner: product
source: requirement.md
---

# 收藏列表页原型说明

## 目标

该原型用于描述收藏列表页的首期信息架构、列表密度、状态位和操作关系，供后续 `/req-opsx` 设计和实现阶段参考。当前端范围仍为 `multi`，原型以移动端优先的 Web HTML 表达，可映射到微信小程序页面。

## 页面结构

```text
FavoriteListPage
├── TopBar
│   ├── BackAction / SafeArea
│   └── PageTitle
├── SummaryStrip
│   ├── FavoriteCount
│   └── ScopeHint
├── FavoriteList
│   └── FavoriteCard[]
│       ├── Cover
│       ├── TypeBadge
│       ├── Name
│       ├── Meta
│       ├── PriceOrHint
│       └── RemoveAction
├── EmptyState
├── ErrorState
└── BottomSafeArea
```

## 状态说明

| 状态 | 原型表达 | 验收重点 |
|---|---|---|
| 有收藏 | 展示 2-3 个收藏卡片 | 信息可扫读，整卡可进入详情，移除入口不误触 |
| 无收藏 | 中央空状态 + 去浏览入口 | 不误导为错误状态 |
| 未登录 | 登录引导 + 访客态说明 | 与无收藏区分 |
| 网络异常 | 错误文案 + 重试按钮 | 可恢复，不清空已有内容 |
| 对象失效 | 灰态卡片或禁用标记 | 不导致整页异常 |

## 交互约束

- 点击卡片主体进入详情页。
- 点击收藏图标或移除按钮执行取消收藏，不触发详情跳转。
- 取消收藏成功后列表即时移除或进入短暂灰态，具体方式后续设计确认。
- 下拉刷新同步最新收藏状态。
- 小程序实现时需按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 处理顶部导航 offset 与胶囊 reserve。

## PNG

PNG Golden Reference 待后续设计导出；当前以 HTML + context 作为原型策略。
