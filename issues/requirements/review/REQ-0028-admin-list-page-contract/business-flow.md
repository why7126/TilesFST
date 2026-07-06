---
requirement_id: REQ-0028-admin-list-page-contract
title: AdminListPage 模板与管理端列表页契约业务流程
status: approved
created_at: 2026-07-05 10:18:38
updated_at: 2026-07-05 14:36:29
owner: product
---

# 业务流程

## 1. 当前问题流

```text
新增或修改管理端列表页
        |
        v
页面内自行拼装标题 / 指标卡 / 筛选 / 表格 / 分页
        |
        v
局部 CSS 与 DOM 逐页演化
        |
        v
分页 DOM、指标卡 DOM、sticky 操作列、toast / confirm 行为漂移
        |
        v
产生 BUG-0009 / BUG-0027 / BUG-0030 / BUG-0052 / BUG-0055 等一致性问题
        |
        v
逐页 fix，经验未进入模板事实源
```

## 2. 目标流程

```text
新增或改造管理端列表页
        |
        v
检查 REQ-0028 AdminListPage 契约
        |
        v
优先选择 AdminListPage 模板或等价组合
        |
        +--> 标题模块
        +--> 指标卡模块
        +--> 筛选/搜索模块
        +--> 表格列表模块
        +--> 分页模块
        +--> sticky action column
        |
        v
在 /design-system 查看 AdminListPage 验收样例
        |
        v
执行功能 AC + 横切 AC
        |
        v
通过 req-review 后进入 req-opsx / sprint
```

## 3. 与父需求差异

| 项目 | REQ-0000-build-design-system | REQ-0028-admin-list-page-contract |
|---|---|---|
| 目标 | 建立整体 Design System、Token、基础组件和预览页 | 将管理端列表页沉淀为可复用页面模板和验收契约 |
| 范围 | 全局视觉、Token、shadcn 基础、业务组件、页面模板 | Web 管理端列表页：标题、指标卡、筛选、表格、分页、操作列 |
| 主要风险 | Token / 组件体系不统一 | 页面级 DOM 与交互继续分叉 |
| 验收方式 | `/design-system` 展示 DS 组件 | `/design-system` 增加 AdminListPage 场景样例和边界态 |

## 4. 与子需求差异

| 项目 | REQ-0028 | REQ-0029 |
|---|---|---|
| 定位 | 页面模板与列表页契约 | 基础组件与算法工具 |
| 关注对象 | AdminListPage、页面结构、验收页、8 页面矩阵 | MetricCard、PaginationWindow、局部 DOM 漂移 |
| 输出重点 | 页面级组合与门禁 | 可复用组件 / 工具规格 |
| 编排建议 | 可先定义契约，再由 REQ-0029 支撑实现 | 可先实现基础组件，再反向支撑 REQ-0028 |

## 5. 后续 OpenSpec 设计提示

后续 `/req-opsx` 生成 change design 时，应显式声明：

- `knowledge_base_refs` 必须包含 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`。
- UI 优先级为：`prototype/web/admin-list-page-contract.html` → `prototype/web/admin-list-page-contract-context.md` → `acceptance.md` → `rules/ui-design.md` → `openspec/specs/web-client/spec.md`。
- 若实现阶段选择迁移真实业务页，应先选一个低风险代表页作为示范，再推广到其他列表页。
