---
bug_id: BUG-0065-miniapp-home-preview-deviation
status: done
created_at: 2026-07-16 13:03:12
updated_at: 2026-07-19 15:32:13
related_requirement: REQ-0041-miniapp-home
suggested_fix_change: fix-miniapp-home-preview-runtime-entry
related_requirements:
  - REQ-0041-miniapp-home
related_bug: null
---

# 回归验收标准

> 修复本缺陷 MUST 确保微信开发者工具实际预览的首页运行脚本加载小程序首页业务逻辑，并使首页首屏重新满足 REQ-0041 的原型和验收要求。默认不在本 BUG scope 内修改后端 API、数据库、Orval 或 Docker Compose。

## AC-001 小程序运行入口 MUST 执行首页业务逻辑

**Given** 使用微信开发者工具打开 `src/miniapp/`  
**When** 进入首页 `pages/index/index`  
**Then** 实际运行脚本 MUST 初始化首页 `data`  
**And** 页面加载时 MUST 触发首页数据加载逻辑  
**And** MUST 请求 `GET /api/v1/miniapp/home` 或等价首页聚合接口  
**And** MUST NOT 继续执行空模板 `Page({ data: {}, onLoad() {} })`

## AC-002 `.ts` 与 `.js` 运行事实源 MUST 不脱节

**Given** 小程序页面目录同时存在 `.ts` 与 `.js`  
**When** 执行构建、预览或静态校验  
**Then** 运行时 `.js` MUST 与业务 `.ts` 保持同步，或项目 MUST 明确采用可验证的 TypeScript 编译链  
**And** 首页、搜索页、商品详情页、门店信息页的 `.js` MUST NOT 保持微信开发者工具空模板  
**And** CI 或本地测试 MUST 能发现关键页面 `.js` 与 `.ts` 脱节

## AC-003 首页首屏 MUST 展示核心模块

**Given** 后端服务可访问，且存在公开 Banner 和公开商品数据  
**When** 在微信开发者工具打开首页  
**Then** 首屏 MUST 展示品牌导航、搜索入口、Banner、快捷入口和至少一个推荐模块  
**And** 快捷入口 MUST 固定展示“按空间、按规格、按风格、按颜色、全部分类”  
**And** 新品推荐或热销推荐 MUST 展示可点击商品卡片

## AC-004 无商品数据时 MUST 模块级降级

**Given** 后端可访问但暂无公开商品  
**When** 打开首页  
**Then** 推荐商品模块 MAY 隐藏或显示品牌化空状态  
**And** Banner、快捷入口和品牌服务区 MUST 继续按可用数据展示  
**And** 页面 MUST NOT 因商品为空而丢失全部动态模块

## AC-005 视觉表现 MUST 对齐 REQ-0041 原型

**Given** 修复已完成  
**When** 对比 `prototype/miniapp/prototype.png` 和微信开发者工具预览  
**Then** 首页 MUST 采用暖白背景、墨黑主视觉 Banner 和品牌金点缀  
**And** Banner、搜索框、快捷入口、商品卡片、服务卡片的顺序、圆角、间距和模块密度 MUST 与原型保持同等级视觉比例  
**And** MUST NOT 出现大面积空白首屏

## AC-006 视口回归 MUST 覆盖小程序验收宽度

**Given** 修复已完成  
**When** 在 375x812、390x844 以及 320 到 430 pt 宽度范围检查首页  
**Then** 页面 MUST 无横向滚动、明显内容截断、控件重叠或底部 TabBar 遮挡  
**And** 主要点击区域 MUST 不小于 44x44 pt

## AC-007 首页交互路径 MUST 可用

**Given** 首页核心模块已展示  
**When** 用户点击门店信息、搜索框、快捷入口、Banner 或推荐商品  
**Then** MUST 分别进入门店信息页、搜索页、筛选结果页、有效 Banner 目标或商品详情页  
**And** 无效 Banner 目标 MUST 安全降级，不得出现空白页或路由错误

## AC-008 分享与咨询埋点 MUST 不回归

**Given** 修复已完成  
**When** 用户触发首页分享或品牌服务区咨询入口  
**Then** 小程序 MUST 继续记录 `home_share` 或 `home_contact_click` 等行为事件  
**And** 埋点失败 MUST 不阻断首页浏览和咨询操作

## AC-009 自动化测试 MUST 覆盖运行入口脱节

**Given** 对应 fix change 已实现  
**When** 运行小程序相关测试  
**Then** MUST 覆盖首页实际运行脚本包含关键 `Page` 数据和 `loadHome` 逻辑  
**And** MUST 覆盖空模板 `.js` 不得与业务 `.ts` 并存  
**And** SHOULD 覆盖搜索页、商品详情页、门店信息页的运行脚本不为空模板

## AC-010 默认不修改 API / DB / Orval / Docker

**Given** 修复已完成  
**When** 检查变更范围  
**Then** 默认 MUST 仅涉及小程序运行入口、构建/校验和必要测试  
**And** MUST NOT 修改后端 API、SQLite/MySQL schema、Pydantic Schema、Orval 生成物或 Docker Compose 配置  
**And** 如实现确需调整接口契约、数据模型或环境变量，MUST 在 OpenSpec Change、文档和测试计划中明确说明
