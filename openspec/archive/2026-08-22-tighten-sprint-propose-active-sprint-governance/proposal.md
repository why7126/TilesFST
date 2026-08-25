---
created_at: 2026-08-22 14:12:50
updated_at: 2026-08-22 14:12:50
---

# 收紧 Sprint 提议与归档冻结治理

## 背景

`/sprint-propose` 已具备自动编号、容量门禁和 Sprint scope 同步规则，但未指定 Sprint 时的“当前 Sprint”选择、并行 active Sprint 数量、跳号创建阻断和归档后冻结边界还不够明确。

## 变更内容

- 明确未指定 Sprint 时的默认选择：无 active Sprint 自动创建下一个连续编号；一个 active Sprint 默认使用当前 Sprint；两个及以上 active Sprint 必须失败并要求显式 `--sprint`。
- 明确指定新 Sprint 时必须为当前最大规范编号加一，不允许跳号创建；当前已有两个 active Sprint 时不得创建第三个。
- 保留现有容量区间：`<=100%` 通过，`100%~120%` 风险通过，`>120%` 硬阻断；容量硬阻断后才引导用户用 `--sprint` 创建下一个连续 Sprint。
- 明确 Sprint 归档后，关联 REQ、BUG、Change 和 Sprint 四件套默认冻结，只有只读探索、复盘、发布、镜像和升级命令可消费归档事实；治理修复必须走受控治理流程。

## 非目标

- 不修改业务 `src/`。
- 不改变 API、数据库、Web、小程序或管理端行为。
- 不取消现有 `100%~120%` 容量风险通过区间。
