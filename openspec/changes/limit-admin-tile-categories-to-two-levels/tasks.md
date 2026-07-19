## 1. Backend / API

- [x] 1.1 将管理端类目创建最大层级从 3 调整为 2，并沿用 `CATEGORY_MAX_DEPTH_EXCEEDED`。
- [x] 1.2 将类目列表 `level` 查询限制为 1/2，并将 summary `max_level` 调整为 2。
- [x] 1.3 更新 API 文档中管理端类目层级说明和错误场景。

## 2. Web Admin

- [x] 2.1 更新类目表单上级选项，只允许选择一级类目作为上级。
- [x] 2.2 更新类目表单提示文案为最多支持二级类目。
- [x] 2.3 保持管理端视觉 token 与现有组件结构，不新增裸 Hex 或新组件体系。

## 3. Tests / Validation

- [x] 3.1 补充或更新后端类目 API 测试，覆盖拒绝在二级类目下创建子类目。
- [x] 3.2 补充或更新 Web 类目管理测试，覆盖二级类目不出现在上级下拉框。
- [x] 3.3 运行相关 pytest、前端测试和 `openspec validate limit-admin-tile-categories-to-two-levels --strict`。
