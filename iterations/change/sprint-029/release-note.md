---
title: sprint-029 发布说明
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:36:34
---

# sprint-029 发布说明

## 范围摘要

- 强化发布流程产品版本号门禁：release prepare 和 publish 必须校验 Web 与小程序用户可见 `PRODUCT_VERSION` 等于发布版本。
- 任一版本源不一致时，发布确认必须阻断，并提示更新版本源后重跑 `/image-prepare` 与 `/image-build`。

## 用户可见变化

- 产品用户界面无变化。

## 技术变化

- 治理范围涉及发布技能、发布规则、release validator 和聚焦测试。
- API、DB、Orval、Docker Compose 与业务端实现不适用。

## 状态

```yaml
sprint_id: sprint-029
status: active
changes:
  - enforce-product-version-release-gates
```
