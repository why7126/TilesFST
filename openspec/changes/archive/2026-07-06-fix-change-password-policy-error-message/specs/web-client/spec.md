## MODIFIED Requirements

### Requirement: 管理端修改密码弹窗组件

Web 客户端 MUST 在管理端修改密码弹窗中展示当前 effective 密码策略，并在新密码策略失败时展示具体失败原因。客户端 MUST NOT 仅依赖静态旧规则或泛化错误文案。若后端返回结构化策略失败详情，客户端 MUST 将详情映射为用户可理解的中文提示。

#### Scenario: 默认策略规则展示

- **GIVEN** effective 密码策略为最小 12 位、要求大写、小写、数字、特殊字符
- **WHEN** 用户打开修改密码弹窗
- **THEN** 页面 MUST 展示上述规则
- **AND** 页面 MUST NOT 只展示“8-32 位字符、至少包含字母和数字”

#### Scenario: API 策略失败详情映射

- **WHEN** 修改密码 API 返回策略失败详情，例如缺少特殊字符或缺少大写字母
- **THEN** 客户端 MUST 展示对应中文提示
- **AND** 提示 MUST 位于新密码字段或规则区
- **AND** 原密码字段 MUST NOT 误显示新密码策略失败

#### Scenario: 既有错误映射无回归

- **WHEN** API 返回原密码错误、弱密码、同原密码、限流或受保护账号不可改密
- **THEN** 客户端 MUST 继续展示对应明确文案
- **AND** MUST NOT 统一降级为“新密码不符合安全策略”
