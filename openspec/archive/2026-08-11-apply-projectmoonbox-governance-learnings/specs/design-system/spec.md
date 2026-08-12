## ADDED Requirements

### Requirement: 原型驱动 UI 验收门禁

系统 SHALL 对包含 `prototype/`、`prototype_refs`、`AC-PROTOTYPE-*`、UI Skeleton 或明确引用既有页面视觉的 UI Change 执行原型驱动验收门禁。

#### Scenario: 生成 UI Contract

- **GIVEN** `/req-opsx` 创建带 prototype 的 UI Change
- **WHEN** Change `design.md` 被生成
- **THEN** `design.md` SHALL 包含 UI Contract
- **AND** UI Contract SHALL 覆盖事实源优先级、页面入口、信息架构、视觉 token、交互状态、图标文案、Mock/API 边界、权限规则和一致性参照

#### Scenario: UI 实现前完成 Skeleton

- **GIVEN** `/opsx-apply` 处理带 prototype 的 UI Change
- **WHEN** 进入细节实现前
- **THEN** AI SHALL 先完成 UI Skeleton 首轮确认
- **AND** 记录 1440px 桌面视口截图或等价视觉证据

#### Scenario: 归档前复核最终一致性

- **GIVEN** `/opsx-archive` 归档带 prototype 的 UI Change
- **WHEN** 关联 REQ 或 Change 包含视觉验收证据要求
- **THEN** AI SHALL 复核 UI Contract、Skeleton、截图、computed style、Mock/API 边界和最终实现一致
- **AND** 缺证据、证据过期或边界未声明时 SHALL 阻断归档
