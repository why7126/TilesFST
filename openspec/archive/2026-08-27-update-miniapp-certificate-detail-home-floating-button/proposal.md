## 背景

证书详情页已经具备公开证书内容、品牌入口、分享直达和自定义导航返回能力，但缺少与商品详情页、品牌详情页、商品列表页等深层页面一致的【返回首页】悬浮按钮。用户从证书列表、品牌详情或分享路径进入证书详情后，需要一个明确、稳定且可恢复的首页入口。

## 变更内容

- 在小程序证书详情页规格中明确接入 `home-floating-button`。
- 要求证书详情页复用既有返回首页悬浮按钮组件，不新增页面私有按钮样式、offset 或跳转逻辑。
- 要求证书详情页默认使用 `offset="list"`，并覆盖正常态、加载态、错误态、证书不可查看、分享直达和快速重复点击场景。
- 要求实现阶段同步维护 `pages/certificate-detail/index` 的 `.json`、`.wxml`、`.ts` 与 `.js`，并补充小程序静态检查和 DevTools 320 / 375 / 430 pt evidence。
- 不调整后端 API、数据库、对象存储、管理端、Web 展示端、Orval 或 Docker Compose。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `miniapp-certificate-list-page`：补充证书详情页返回首页悬浮按钮、状态覆盖和设备验收要求。
- `miniapp-global-custom-navigation-bar`：将证书详情页纳入非首页返回首页悬浮按钮覆盖页，并明确该页复用既有组件契约。

## 影响

- 小程序：影响 `src/miniapp/pages/certificate-detail/index.json`、`index.wxml`、`index.ts`、`index.js` 的后续实现。
- 组件：复用 `src/miniapp/components/home-floating-button/`，不改变组件契约。
- 测试：后续实现需补充或更新小程序静态检查，覆盖组件声明、WXML 挂载、`offset="list"` 和 `.ts` / `.js` 同步。
- API / 数据库 / Orval / Docker：不涉及。
