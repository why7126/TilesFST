---
title: 业务流程
purpose: REQ-0026 产品版本发布与公告管理业务流程
created_at: 2026-07-02 13:39:28
updated_at: 2026-07-03 23:56:30
owner: product
status: done
---

# 业务流程

## 1. 总体流程

```text
已完成 Sprint / REQ / BUG / OpenSpec Change
        │
        ▼
选择产品版本号与发布范围
        │
        ▼
创建产品版本发布对象（releases/，须 OpenSpec 批准后）
        │
        ▼
执行发布前校验
        ├─ OpenSpec archive
        ├─ tests
        ├─ Orval
        ├─ Docker Compose
        ├─ database migration
        └─ .env.example
        │
        ├─ 校验失败 → 阻断发布，输出修复项
        │
        ▼
更新 PRODUCT_VERSION
        │
        ▼
生成 Mintlify 静态发布公告
        │
        ▼
人工 Review / Sign-off
        │
        ▼
公开页面发布
```

## 2. 与 REQ-0010 的差异

| 项 | REQ-0010 | REQ-0026 |
|---|---|---|
| 目标 | Web 端显示当前产品版本号 | 管理产品版本发布流程和公告 |
| 事实源 | `src/shared/product-version.ts` | 产品版本发布对象 + `PRODUCT_VERSION` 一致性校验 |
| 输出 | 管理端/店主端侧栏版本 badge | Mintlify 静态公开公告 |
| 范围 | UI 展示 | 发布目录、发布命令、校验清单、公告内容 |
| 状态 | 已归档能力 | 待评审需求 |

## 3. 发布范围选择

```text
产品负责人
  │
  ├─ 选择版本号
  ├─ 选择一个或多个 Sprint
  ├─ 校验 Sprint 内 REQ/BUG/Change 状态
  └─ 形成产品版本发布范围
```

规则：

- 一个产品版本允许合并多个 Sprint。
- 只有已评审、已纳入交付且完成归档闭环的内容可进入正式发布范围。
- 未完成项只能作为已知问题、后续计划或非本次正式交付说明。

## 4. 发布公告生成

```text
发布范围
  │
  ├─ 新增功能（REQ）
  ├─ 修复 BUG
  ├─ 影响范围
  ├─ 已知问题
  ├─ 升级步骤
  └─ 回滚说明
        │
        ▼
Mintlify 源文件
        │
        ▼
Mintlify 构建 / 预览校验
        │
        ▼
公开发布公告页面
```

## 5. 阻断条件

以下任一条件失败时，发布流程必须停止：

- OpenSpec Change 未 archive。
- 必要测试未执行或失败。
- API 变更后未同步 OpenAPI / Orval。
- Docker Compose 或部署文档未同步。
- 数据库迁移未同步文档、脚本或回滚说明。
- 环境变量变更未同步 `.env.example`。
- `PRODUCT_VERSION` 与发布公告版本不一致。
- Mintlify 构建或预览校验失败。

## 6. 非本期流程

- 不在管理端新增发布公告菜单。
- 不在登录页、店主端或小程序新增公告入口。
- 不支持草稿、待发布、已发布、撤回等状态机。
- 不在 capture / PRD 阶段创建 `releases/` 顶层目录。
