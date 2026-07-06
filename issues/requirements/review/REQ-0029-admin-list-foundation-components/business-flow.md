---
title: 业务流程
purpose: REQ-0029 管理端列表基础组件业务流程
content: 描述 MetricCard、分页窗口工具、设计验收与首批页面接入流程
source: AI 根据 requirement.md、capture.md 与知识库横切规则生成，项目团队确认
update_method: 组件策略、页面接入范围或验收标准变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 14:14:26
updated_at: 2026-07-05 14:14:26
note: REQ-0029-admin-list-foundation-components
---

# 业务流程

## 1. 总览

```text
REQ-0028 AdminListPage 页面契约
  -> REQ-0029 抽象基础组件
      -> MetricCard / MetricCardGrid
      -> PaginationWindow 工具
      -> 管理端分页 DOM 契约
  -> /design-system 展示
  -> 首批列表页接入
  -> Vitest / Testing Library 结构验证
  -> 后续管理端列表页按契约复用
```

## 2. MetricCard 抽象流程

1. 梳理现有管理端列表页的指标卡字段：label、value、description、danger 描述、空值占位。
2. 定义 `MetricCard` props 与 DOM 输出契约。
3. 定义 `MetricCardGrid` 或等价容器，承载 2–4 个指标卡。
4. 在 `/design-system` 展示正常、空值 / 加载中、danger 描述和不同卡片数量样例。
5. 选择首批页面替换手写 DOM。
6. 用组件测试和页面结构测试确认 `.metric-*` class 未漂移。

## 3. 分页窗口工具沉淀流程

```text
现有 getPaginationWindow
  -> 迁移到 shared util 或管理端共享层
  -> 保留最多 5 页码窗口规则
  -> 补齐非法输入和边界测试
  -> 管理端页面统一导入
  -> 页面分页 DOM 结构测试
```

约束：

- 通用 `Pagination` 可继续服务店主端或轻量场景。
- 管理端列表页 MUST 保留 `.page-summary`、`.page-right`、`.page-buttons`、`.page-size-wrap`。
- 本需求不新增或修改后端分页 API。

## 4. 首批页面接入流程

1. 从 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`、`BrandManagementPage` 中选择 2–3 个页面。
2. 先替换指标卡区域，再统一分页窗口导入路径。
3. 保持筛选、排序、分页状态、空态、权限逻辑不变。
4. 运行对应页面测试和共享工具测试。
5. 记录未纳入页面的后续推广清单，交由 `REQ-0028` 页面契约继续推进。

## 5. 与父需求差异

| 项目 | REQ-0028 | REQ-0029 |
|---|---|---|
| 关注层级 | 页面模板、页面矩阵、列表页横切契约 | 组件与工具 |
| 主要对象 | `AdminListPage`、页面结构、设计验收页 | `MetricCard`、`MetricCardGrid`、分页窗口工具 |
| 接入范围 | 后续管理端列表页全局契约 | 首批 2–3 个页面验证基础能力 |
| 验收重点 | 页面顺序、筛选、表格、操作列、分页、toast、confirm | 指标卡 DOM、分页窗口算法、共享层归属、组件测试 |

## 6. Knowledge-base Cross-cutting Report

| 标签 | 引用文档 | 将写入 acceptance 的 AC 条数 |
|---|---|---:|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 5 |

未命中标签：

- `admin-form`：本需求不涉及管理端表单页、设置页或页内保存。
- `admin-modal`：本需求不涉及新增 / 编辑弹窗或宽弹窗 CSS 层叠。
- `media-upload`：本需求不涉及图片、视频、头像、Logo 上传或回显。

## 7. 待评审确认

- 首批接入页面最终选择：建议 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage` 三选二或三选三。
- `MetricCard` 是否支持图标、趋势值、辅助 tooltip；若支持，应作为 v1 增强项还是后续迭代。
- 分页窗口工具最终归属：`src/web/src/shared/ui/` 邻近工具、`src/web/src/shared/lib/`，或管理端专属共享层。
- `/design-system` 展示放在 UI Section 还是 Admin Section。
