---
purpose: 小程序运行入口脱节事故复盘
content: 记录微信开发者工具实际加载 .js 与类型化 .ts 业务源码不一致导致首页预览缺失的经验
source: BUG-0065-miniapp-home-preview-deviation
created_at: 2026-07-16 13:40:44
updated_at: 2026-07-17 00:05:05
---

# 小程序运行入口脱节

## 现象

微信开发者工具预览首页时，WXML 静态结构可见，但 Banner、快捷入口、新品推荐、热销推荐和服务区等依赖运行时数据的模块缺失。

## 根因

页面目录同时存在 `.ts` 与 `.js` 时，当前项目没有启用可验证的 TypeScript 编译链。业务逻辑写在 `.ts`，但微信开发者工具实际加载的 `.js` 仍是空模板，导致 `onLoad()` 未触发首页聚合数据加载。

## 预防规则

- 关键小程序页面的 `.js` 必须作为运行事实源同步维护，或先建立可验证的 TypeScript 编译链。
- 首页、搜索页、商品详情页、门店信息页不得保留空模板 `Page({ data: {}, onLoad() {} })`。
- 小程序静态测试必须检查实际运行 `.js`，不能只检查 `.ts` 源码意图。
- 修复运行入口时同步验证网络失败、空商品和图片失败的模块级降级。

## 延伸经验

- 微信开发者工具的 `project.private.config.json` 可能覆盖项目配置；本地联调需要确认 `urlCheck=false`。
- 后端服务若通过 Docker Compose 运行，修改 `/api/v1/miniapp/home` 聚合逻辑后必须重新构建 backend 镜像，否则小程序可能继续命中旧接口或旧字段。
- 小程序首页视觉与数据来源要一起验证：Logo 应来自产品 Logo 资产，Banner 应来自后台 Banner 管理，新品与热门卡片应展示 SKU 主图和 `price_display`，底部导航应使用自定义 TabBar 图标和可读字号。

## 验证建议

- 运行 `uv run pytest tests/test_miniapp_static.py`。
- 运行 `uv run pytest tests/test_miniapp_home.py`。
- 在微信开发者工具中打开 `src/miniapp/`，确认首页请求 `/api/v1/miniapp/home`，且首屏展示品牌导航、搜索、Banner、快捷入口和至少一个推荐模块。
