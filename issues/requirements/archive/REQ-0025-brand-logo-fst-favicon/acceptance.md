---
requirement_id: REQ-0025-brand-logo-fst-favicon
title: 品牌区 Logo 与网页图标统一 - 验收标准
status: pending_review
owner: product
created_at: 2026-07-01 20:56:22
updated_at: 2026-07-01 20:56:22
---

# 验收标准

## 功能验收

| ID | 验收项 | 标准 |
|---|---|---|
| AC-001 | Sidebar 品牌区结构 | 展开态顶部品牌区同时展示 Logo、`菲尚特FST`、版本号、`家居建材资料库` 和展开/收起按钮。 |
| AC-002 | 品牌主标题 | 主标题文案必须为 `菲尚特FST`，不得显示 `TILESFST`、`菲尚特 FST` 或仅 `菲尚特`。 |
| AC-003 | 品牌副标题 | 副标题文案必须为 `家居建材资料库`；若旧原型出现 `家居建材管理后台`，以本验收项为准。 |
| AC-004 | 版本号 | 版本号必须沿用现有产品版本来源；视觉上靠近主标题右上侧，并保留弱边框或版本徽标样式。 |
| AC-005 | Logo 显示 | Logo 使用用户提供的菲尚特图片或其 Web 优化版本，保持比例，不拉伸、不裁切关键内容。 |
| AC-006 | Logo 容器 | Logo 区域不得新增独立卡片背景、边框、渐变底纹或投影。 |
| AC-007 | 收起按钮 | 展开/收起按钮与 Logo 同行，保持正方形热区，hover 后边框与 Sidebar 内右边界存在安全间距。 |
| AC-008 | 收起态 | Sidebar 收起后 Logo 仍可作为品牌识别元素；按钮可点击；品牌文案、导航图标无重叠。 |
| AC-009 | 网页图标 | 浏览器标签 favicon / apple-touch-icon 展示菲尚特 Logo，不显示 Vite、React 或浏览器默认图标。 |
| AC-010 | 页面业务不变 | Banner、用户、品牌、规格等管理页面主体结构、路由、权限与操作行为不因本需求改变。 |

## 视觉与兼容验收

| ID | 验收项 | 标准 |
|---|---|---|
| AC-011 | 原型对照 | 以 `prototype/web/banner-management-list-logo.html` 与 PNG 验证 Sidebar 品牌区结构；页面主体仅作为承载背景。 |
| AC-012 | 视口稳定 | 在 1366×768、1440×1024 桌面视口下，品牌区无重叠、无明显裁切、无布局抖动。 |
| AC-013 | Design System | Web UI 实现使用 semantic token / 既有组件样式；不得新增裸 Hex 或绕过 `cn()` 合并规则。 |
| AC-014 | 可访问性 | Logo 图片具备可理解的替代文本；展开/收起按钮保留可访问标签。 |

## 工程验收

| ID | 验收项 | 标准 |
|---|---|---|
| AC-015 | 接口影响 | 不新增、不修改后端 API；无需生成 OpenAPI 或 Orval 客户端。 |
| AC-016 | 数据库影响 | 不新增、不修改 SQLite 表结构或 Pydantic Schema。 |
| AC-017 | 对象存储影响 | 不引入 MinIO 上传、读取或 Bucket 变更。 |
| AC-018 | 测试 | 前端至少覆盖品牌文案、版本号展示、favicon 链接或入口 HTML 图标声明的回归检查。 |

## 知识库横切结论

本需求不涉及 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切标签。Banner 管理列表页只是原型承载页，不触发列表页一致性横切 AC。
