# 任务清单

## 1. 后端 API 与校验

- [x] 1.1 更新 `UserCreateRequest`、`UserUpdateRequest`，新增可选 `email`、`phone`。
- [x] 1.2 实现联系邮箱格式校验：允许空值，非空必须为邮箱格式，保存前裁剪空白。
- [x] 1.3 实现手机号码宽松校验：允许空值，非空仅允许数字、空格、`+`、`-`，保存前裁剪空白。
- [x] 1.4 更新 `UserRepository.create_user`、`UserRepository.update_user`，支持写入、修改和清空 `email`、`phone`。
- [x] 1.5 更新 `UserAdminService`，保持字段缺省不变、显式 `null` 清空。
- [x] 1.6 更新列表关键词搜索，匹配 `username`、`display_name`、`email`、`phone`。
- [x] 1.7 确认 SQLite/MySQL schema 与 migration 已覆盖 `users.email`、`users.phone`，无重复新增字段。

## 2. Web 管理端

- [x] 2.1 更新 `UserFormModal`，添加「联系邮箱」「手机号码」字段，顺序为用户名、头像、昵称、联系邮箱、手机号码、角色。
- [x] 2.2 编辑弹窗回填 `email`、`phone`，创建/编辑提交 payload 包含可选字段，清空时提交 `null`。
- [x] 2.3 更新 `UserManagementPage` 表头和行渲染：状态列后新增「联系邮箱」「手机号码」独立列，空值显示 `-`。
- [x] 2.4 更新搜索 placeholder 或帮助文案，表达可搜索用户名、昵称、邮箱、手机。
- [x] 2.5 验证新增列不遮挡操作列，窄屏沿用既有横向滚动策略。

## 3. API 生成物与文档

- [x] 3.1 重新生成 OpenAPI。
- [x] 3.2 重新生成 Orval 前端客户端。
- [x] 3.3 按项目规则同步 API 文档索引或相关接口说明。

## 4. 测试

- [x] 4.1 后端测试覆盖创建用户保存邮箱和手机号。
- [x] 4.2 后端测试覆盖编辑用户修改和清空邮箱/手机号。
- [x] 4.3 后端测试覆盖非法邮箱、非法手机号业务错误。
- [x] 4.4 后端测试覆盖关键词搜索命中邮箱和手机号。
- [x] 4.5 后端测试覆盖非管理员访问仍 403。
- [x] 4.6 前端测试覆盖添加/编辑弹窗字段展示、回填、提交 payload 和清空提交。
- [x] 4.7 前端测试覆盖列表新增独立列、列顺序、空值 `-` 展示和搜索 placeholder。

## 5. UI 验收与横切门禁

- [x] 5.1 记录 1440px 用户管理列表截图或等价视觉证据，确认列顺序与空值展示。
- [x] 5.2 记录添加/编辑弹窗字段顺序和矮视口滚动验证。
- [x] 5.3 确认 fixed toast、DS confirm modal、分页 DOM 未回退。
- [x] 5.4 确认 TSX/CSS 无新增裸 Hex，弹窗宽度未被 CSS 层叠覆盖。

## 验收返修记录

- [x] M1. 用户管理列表「创建时间」从仅日期展示调整为 `yyyy-mm-dd hh:MM` 分钟级格式。
- [x] M2. 前端列表测试补充创建时间分钟级展示断言。
- [x] M3. 同步 REQ 验收标准、requirement、Change design/spec delta 与 trace。
- [x] M4. 用户新增/编辑弹窗标题区收紧，减少标题上方空隙，且不改变通用确认弹窗。
- [x] M5. 前端表单弹窗测试补充专属 backdrop 作用域与紧凑 header CSS 证据。
- [x] M6. 同步 REQ 验收标准、requirement、Change design/spec delta 与 trace。
- [x] M7. 用户新增/编辑弹窗 backdrop 从垂直居中改为顶部对齐，减少弹窗整体顶部空隙。
- [x] M8. 同步 REQ 验收标准、requirement、Change design/spec delta 与 trace。
