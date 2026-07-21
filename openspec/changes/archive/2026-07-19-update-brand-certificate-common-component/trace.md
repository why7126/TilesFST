---
change_id: update-brand-certificate-common-component
type: update
status: proposed
req: REQ-0055-brand-certificate-common-component
sprint: sprint-009
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - brand-certificate-management
---

# Trace

## Requirement Readiness Report

| 项 | 结果 |
|---|---|
| REQ | `REQ-0055-brand-certificate-common-component` |
| status | `in_sprint`，已完成 `/req-review --approve`，已纳入 `sprint-009` |
| readiness | ready |
| 六件套 | requirement、user-stories、business-flow、acceptance、trace、prototype 均存在 |
| change_type | update |

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - brand-certificate-management
```

## Conflict Report

优先级：HTML > prototype context > acceptance.md > rules/ui-design.md > openspec/specs。

| 来源 | 冲突/差异 | 处理 |
|---|---|---|
| prototype HTML | 使用裸 Hex 与 scoped rgba 表达视觉 | 实现必须转换为 Design System semantic token；不复制裸 Hex |
| prototype HTML | 表达组件状态矩阵，不是完整品牌证书页面 | delta spec 只要求组件和页面局部应用，不要求还原 prototype 页面 |
| parent spec | 图片预览可大图，PDF 新窗口 | v1 统一要求图片/PDF 可通过新窗口打开受控 URL；不禁止后续图片大图 modal |
| acceptance | 文件卡片覆盖上传中/失败状态 | 组件只展示传入状态和触发回调，上传副作用留在页面容器 |

## PNG Checklist

- [ ] 后续实现如导出 PNG Golden Reference，需与 `prototype/web/brand-certificate-common-component.html` 状态矩阵一致。
- [ ] 1440x1024 管理端列表验收需覆盖缩略图稳定尺寸、Badge、分页 DOM、指标卡 DOM 和 fixed toast。
- [ ] 窄视口弹窗验收需覆盖文件卡片换行、头尾固定、body 可滚动和按钮可达。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 18:14:29 | /req-opsx REQ-0055 | 创建 OpenSpec Change，关联 REQ-0055 与 sprint-009。 |
