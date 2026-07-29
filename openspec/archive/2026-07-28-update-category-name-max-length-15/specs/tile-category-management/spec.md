## ADDED Requirements

### Requirement: 类目名称输入长度上限

管理端类目创建与更新 MUST 使用统一的业务输入长度规则：类目名称 trim 后 MUST 非空，且 MUST 允许 1 到 15 个用户可见字符；超过 15 个用户可见字符时 MUST 拒绝保存。该规则不改变既有字符集、同层级唯一、编码自动生成、层级、排序权重、启停和删除要求。

#### Scenario: 创建 15 字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 为 15 个用户可见字符且满足字符集、层级、排序权重与同层级唯一规则
- **THEN** 系统 MUST 接受该名称并创建类目
- **AND** 响应 MUST 返回统一 response envelope 与创建后的类目对象

#### Scenario: 创建 16 字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝创建
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 更新 15 字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 为 15 个用户可见字符且满足字符集与同层级唯一规则
- **THEN** 系统 MUST 接受该名称并更新类目
- **AND** 系统 MUST 继续保持既有 `code` 不变

#### Scenario: 更新 16 字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝更新
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 前端弹窗长度校验

- **WHEN** 后台用户在新增或编辑类目弹窗输入 16 个用户可见字符的类目名称
- **THEN** Web 管理端 MUST 在保存前阻止提交
- **AND** 字段级错误 MUST 展示在类目名称字段或字段组下方

#### Scenario: 展示端 15 字符名称兼容

- **WHEN** 系统存在 15 个用户可见字符的合法类目名称
- **THEN** 管理端类目列表与类目树 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破
- **AND** 小程序分类入口与 Web 展示端分类入口 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破
