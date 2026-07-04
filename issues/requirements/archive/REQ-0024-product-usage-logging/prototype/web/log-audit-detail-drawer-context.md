---
title: 日志审计详情抽屉原型上下文
purpose: 为开发和 AI Coding 提供日志审计详情抽屉的 UI/UE、布局、字段、状态和交互上下文
content: prototype/web/log-audit-detail-drawer.html 配套说明
source: ui-design.md + admin-superuser-protection.html + requirement.md
update_method: UI 策略、权限或日志字段变更时同步更新
owner: product
status: draft
note: REQ-0024-log-audit-page-v2-detail-drawer
created_at: 2026-07-02
updated_at: 2026-07-02
---

# 日志审计详情抽屉原型上下文

## 1. 原型文件

| 文件 | 说明 |
|---|---|
| `prototype/web/log-audit-detail-drawer.html` | 日志审计详情抽屉静态 HTML Golden Reference |
| `prototype/images/log-audit-detail-drawer.png` | 与 HTML 一致的产品原型图 |
| `prototype/web/log-audit-list.html` | 抽屉关闭时的列表页状态 |

## 2. 页面定位

详情抽屉是列表页点击“查看详情”后的展开状态。它不是独立页面，而是保留列表上下文，在右侧以抽屉展示单条日志的完整排障与审计信息。

## 3. 触发入口

- 列表行操作列点击“查看详情”。
- 可通过路由参数 `id={log_id}` 直接进入抽屉打开状态。
- 抽屉关闭后回到列表页当前筛选与分页状态。

## 4. 抽屉结构

```text
.drawer-layer
├── .drawer-backdrop
└── .drawer
    ├── .drawer-head
    ├── .detail-section 基础信息
    ├── .detail-section 请求信息
    ├── .detail-section 操作者与客户端
    ├── .detail-section 错误摘要
    ├── .detail-section 行为上下文
    └── .detail-section Metadata JSON
```

## 5. 内容分组

| 分组 | 字段 |
|---|---|
| 基础信息 | 日志 ID、日志类型、创建时间、结果、request_id |
| 请求信息 | method、path、status_code、duration_ms、error_code |
| 操作者与客户端 | actor_name、actor_role、client_type、ip_masked、user_agent |
| 错误摘要 | 错误码、错误消息摘要、异常阶段、处理建议 |
| 行为上下文 | event_name、module、entity_type、entity_id、changed_fields |
| Metadata JSON | 脱敏后的 JSON，上限截断展示 |

## 6. 交互规则

- 点击关闭按钮、遮罩或 Esc 关闭抽屉。
- 抽屉宽度桌面端 520px，内部独立滚动。
- 背景列表弱化但保留可识别上下文。
- request_id 与日志 ID 支持复制。
- Metadata 使用等宽字体展示，敏感字段以 `******` 或 `已脱敏` 展示。

## 7. 安全约束

- 前端只能展示后端返回的脱敏结果，不得自行从原始 metadata 中隐藏敏感值作为安全边界。
- 不展示 password、token、authorization、cookie、secret、DSN 等原值。
- 普通运营用户直链详情接口必须返回 403。

## 8. 视觉约束

- 抽屉背景使用 `--surface`，边框使用极细分割线。
- 主强调使用品牌金，失败状态使用克制红色标签。
- 抽屉内每个信息分组使用细线分隔，不使用大面积卡片堆叠。
