## Why

小程序分类列表页仅展示一级与二级类目，管理后台继续允许三级类目会导致运营维护结构与小程序消费结构不一致。现在需要将管理端瓷砖类目创建约束收敛为最多 2 级，避免新增不可见或不可用的三级类目。

## What Changes

- **BREAKING:** 管理端瓷砖类目主数据从最多 3 级调整为最多 2 级。
- 后端创建类目时，若选择 `level=2` 的类目作为上级，必须拒绝并返回 `CATEGORY_MAX_DEPTH_EXCEEDED`。
- 管理端类目列表的层级筛选和 summary 最大层级调整为 2。
- Web 管理端新增/编辑类目弹窗不允许选择二级类目作为上级，并更新提示文案。
- 不迁移或删除既有历史三级数据；本变更只阻止新增三级类目，历史数据治理另行处理。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `tile-category-management`: 类目层级上限从 3 级改为 2 级，并调整创建、筛选、summary 与错误场景。
- `web-client`: 管理端瓷砖类目页面表单与提示同步最多 2 级限制。

## Impact

- **Backend/API:** 修改管理端类目创建校验、列表层级筛选限制、summary `max_level`，错误码沿用 `CATEGORY_MAX_DEPTH_EXCEEDED`。
- **Web/Admin:** 修改类目表单上级选择项与提示，避免前端发起三级类目创建请求。
- **Database:** 不修改表结构；`level` 字段仍为整数，但业务仅允许新建 1 或 2。
- **Docs/OpenSpec/Tests:** 更新 OpenSpec、API 文档和后端/前端测试。
- **Orval:** 响应结构不变，预计不需要重新生成；若 OpenAPI schema 发生变化则补跑 Orval。
