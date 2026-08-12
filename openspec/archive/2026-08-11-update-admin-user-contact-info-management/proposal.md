# 提案：用户管理联系信息维护

## 背景

`REQ-0110-admin-user-contact-info-management` 已评审通过并纳入 `sprint-022`。当前管理端用户管理已返回 `email`、`phone` 字段，底层 `users` 表也已有对应字段，但管理端创建/编辑用户尚未形成联系邮箱和手机号码的维护闭环，列表也缺少明确的独立列展示。

本 Change 将邮箱和手机号定位为非唯一联系信息，不参与登录、通知、找回密码、权限或状态判断。

## 变更范围

- 管理端用户创建、编辑接口接收并保存可选 `email`、`phone`。
- 邮箱非空时执行邮箱格式校验；手机号非空时执行宽松格式校验，允许数字、空格、`+`、`-`。
- 用户管理列表在「状态」列后新增「联系邮箱」「手机号码」两个独立列；空值显示 `-`。
- 关键词搜索匹配 `username`、`display_name`、`email`、`phone`，并更新搜索文案。
- 用户添加/编辑弹窗新增联系邮箱、手机号码字段，支持回填、修改和清空。
- 同步 OpenAPI、Orval、后端集成测试与前端组件/页面测试。

## 非目标

- 不将邮箱或手机号作为登录账号。
- 不新增短信/邮件通知、验证码、找回密码或订阅能力。
- 不要求邮箱或手机号唯一。
- 不新增用户导入导出、批量修改或高级筛选。
- 不变更角色、状态、权限模型、受保护账号策略。
- 不主动新增数据库字段；仅校验既有 SQLite/MySQL schema/migration 兼容。

## 影响

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - user-management
```

## 风险

- 用户管理表格新增两列后可能压缩操作列，需要沿用既有横向滚动和 sticky action 策略。
- API Schema 变更后若未同步 Orval，前端调用类型会漂移。
- 旧需求曾将搜索范围收窄为用户名/昵称，本 Change 需明确重新扩展到邮箱/手机号。

## 验证

- 后端集成测试覆盖创建、编辑、清空、非法邮箱/手机号、搜索命中、非管理员 403。
- 前端测试覆盖弹窗字段、提交 payload、清空值、列表列顺序、空值 `-`、搜索 placeholder。
- 生成并校验 OpenAPI / Orval。
- UI 验证覆盖 1440px 列表与弹窗；必要时记录弹窗 computed width。
