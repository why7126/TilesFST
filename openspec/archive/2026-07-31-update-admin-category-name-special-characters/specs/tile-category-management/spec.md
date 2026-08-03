## MODIFIED Requirements

### Requirement: 类目名称输入长度上限

管理端类目创建与更新 MUST 使用统一的业务输入规则：类目名称 trim 后 MUST 非空，MUST 允许 1 到 15 个用户可见字符，且 MUST 允许中文、英文、数字和常见可见特殊字符；超过 15 个用户可见字符时 MUST 拒绝保存。系统 MUST 禁止换行、制表符、不可见控制字符和仅由空白组成的输入。该规则不改变同层级唯一、编码自动生成、层级、排序权重、启停和删除要求。

#### Scenario: 创建特殊字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 包含合法特殊字符且不超过 15 个用户可见字符
- **THEN** 系统 MUST 接受该名称并创建类目
- **AND** 响应 MUST 返回统一 response envelope 与创建后的类目对象

#### Scenario: 更新特殊字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 包含合法特殊字符且不超过 15 个用户可见字符
- **THEN** 系统 MUST 接受该名称并更新类目
- **AND** 系统 MUST 继续保持既有 `code` 不变

#### Scenario: 创建 16 字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝创建
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 更新 16 字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝更新
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 拒绝控制字符类目名称

- **WHEN** 管理端提交创建或更新类目请求，`name` 包含换行、制表符、不可见控制字符或 trim 后为空
- **THEN** 系统 MUST 拒绝创建或更新
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称仅支持中文、英文、数字和特殊字符或等价字段级错误

#### Scenario: 前端弹窗字符集校验

- **WHEN** 后台用户在新增或编辑类目弹窗输入合法特殊字符类目名称
- **THEN** Web 管理端 MUST 允许提交
- **AND** 字段级错误 MUST NOT 因特殊字符出现

#### Scenario: 前端弹窗非法字符校验

- **WHEN** 后台用户在新增或编辑类目弹窗输入换行、制表符、不可见控制字符或 16 个用户可见字符的类目名称
- **THEN** Web 管理端 MUST 在保存前阻止提交
- **AND** 字段级错误 MUST 展示在类目名称字段或字段组下方

#### Scenario: 展示端特殊字符名称兼容

- **WHEN** 系统存在包含合法特殊字符的类目名称
- **THEN** 管理端类目列表、类目树和类目选择器 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破
- **AND** 小程序分类入口与 Web 展示端分类入口 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破

#### Scenario: 管理端类目树默认折叠

- **WHEN** 管理端类目树加载包含子级的类目结构
- **THEN** Web 管理端 MUST 默认只展示一级类目
- **AND** 二级及以下类目 MUST 默认收起
- **AND** 有子级的类目 MUST 提供 `+/-` 控件用于展开和收起
- **AND** 点击 `+/-` 控件 MUST NOT 触发类目筛选或改变当前筛选类目
