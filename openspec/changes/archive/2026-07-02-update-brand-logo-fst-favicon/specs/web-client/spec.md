## ADDED Requirements

### Requirement: 管理端品牌 favicon

Web 客户端 MUST 为管理端入口声明菲尚特品牌 favicon 与 apple-touch-icon。图标 MUST 使用用户提供的菲尚特 Logo 或由该 Logo 派生的 Web 优化图标，MUST NOT 继续使用 Vite、React 或浏览器默认图标。本能力 MUST 使用前端静态资源实现，MUST NOT 新增后端 API、数据库字段、MinIO 上传流程、Orval 客户端或小程序能力。favicon 变更 MUST NOT 影响管理端路由守卫、权限、现有页面主体、`/api/`、`/media/` 或 `/openapi.json` 代理行为。

#### Scenario: 浏览器标签展示菲尚特图标

- **WHEN** 已登录或未登录用户通过 Web 入口打开管理端任意页面
- **THEN** 浏览器标签 favicon MUST 指向菲尚特 Logo 或其派生图标
- **AND** MUST NOT 展示 Vite、React 或浏览器默认图标

#### Scenario: Apple touch icon 声明

- **WHEN** 浏览器或设备读取 Web 入口 HTML 的 touch icon 声明
- **THEN** `apple-touch-icon` MUST 指向菲尚特 Logo 或其派生图标

#### Scenario: 静态图标不影响运行时能力

- **WHEN** favicon / apple-touch-icon 更新完成
- **THEN** 管理端登录、路由守卫、Sidebar 导航、`/api/`、`/media/` 与 `/openapi.json` 行为 MUST 保持不变
- **AND** 后端 API、数据库、MinIO、Orval 与小程序 MUST 无契约变更
