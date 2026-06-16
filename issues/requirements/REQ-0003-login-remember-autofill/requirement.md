---
requirement_id: REQ-0003-login-remember-autofill
title: 登录页记住凭证与密码显隐
terminal: web-admin
version: v1
status: draft
priority: P1
owner: product
source: 产品对管理端登录页交互优化
change_type: Enhancement
readiness: ready
parent_requirements:
  - REQ-0001-user-login
  - REQ-0002-product-brand-login-simplify
  - REQ-0003-login-left-panel-refine
---

# REQ-0003 登录页记住凭证与密码显隐

## 1. 需求背景

管理端登录页（`/admin/login`）已具备「记住登录状态」复选框与 `remember_me` 后端参数（延长 JWT 有效期）。当前实现 **未** 在下次访问时自动填充账号与密码；密码输入框也 **未** 提供显示/隐藏切换。

本需求补齐两项登录表单体验能力，面向企业内部员工日常重复登录场景。

## 2. 目标用户

- 企业内部运营员工、管理员：使用账号密码登录管理端。

## 3. 需求范围

| 项目 | 内容 |
|---|---|
| 页面 | Web 管理端登录页 `/admin/login` |
| 终端 | Web 桌面端优先，移动 Web 兼容 |
| 本期包含 | 记住登录状态 → 本地保存并自动填充用户名/密码；密码显隐切换 |
| 不包含 | 找回密码、企业微信 OAuth、多因素认证、服务端密码存储变更 |

## 4. 优化项总览

| # | 功能 | 说明 |
|---|------|------|
| F-01 | 记住登录状态 · 自动填充 | 勾选并成功登录后，下次进入登录页自动填充上次成功的用户名与密码，并勾选复选框 |
| F-02 | 密码显示/隐藏 | 密码框支持眼睛图标切换明文/密文 |

## 5. 功能要求

### FR-001 记住登录状态 · 凭证保存

- 登录页 MUST 保留「记住登录状态」复选框（文案不变）。
- 当用户 **勾选**「记住登录状态」且 **登录成功** 时，系统 MUST 在浏览器本地持久化上次成功使用的：
  - `username`（与提交登录时一致，trim 后）
  - `password`（明文，仅用于下次自动填充）
  - `remember` 标记（`true`）
- 当用户 **未勾选** 且登录成功时，系统 MUST **清除** 此前保存的登录凭证（若存在）。
- 保存与读取 MUST 仅发生在前端；MUST NOT 将密码写入服务端数据库、日志或 analytics。
- 与现有行为兼容：勾选时 `remember_me=true` 传给后端，JWT 存入 `localStorage`（7 天）；未勾选时使用 `sessionStorage`（2 小时）。**本需求在相同复选框上叠加凭证自动填充，不改变 token 存储策略。**

### FR-002 记住登录状态 · 自动填充

- 用户再次进入 `/admin/login`（未持有有效登录态，或已登出后）时：
  - 若本地存在 FR-001 保存的凭证且 `remember=true`，MUST 自动填充用户名、密码输入框，并将「记住登录状态」复选框设为勾选。
  - 若不存在保存凭证，表单 MUST 为空，复选框默认不勾选（与现网一致）。
- 自动填充 MUST 在页面首次渲染时完成，用户无需额外操作。
- 用户可在自动填充后手动修改账号或密码再登录；以 **最后一次成功登录** 且勾选记住时的值为准更新本地存储。

### FR-003 登出与凭证清除

- 用户主动 **退出登录** 时，MUST 清除本地保存的登录凭证（username/password/remember），避免下一访客或同机他人看到预填密码。
- 登录 **失败** 时 MUST NOT 更新已保存凭证（保留上一次成功保存的内容，若有）。

### FR-004 密码显示/隐藏切换

- 密码输入框 MUST 提供显隐切换控件（推荐：输入框右侧眼睛图标按钮）。
- 默认状态为 **隐藏**（`type="password"`）。
- 点击切换为 **显示** 时，输入框 `type="text"`，图标状态随之变化；再次点击恢复隐藏。
- 控件 MUST 具备可访问性：`aria-label` 或 `aria-pressed`（如「显示密码」「隐藏密码」）。
- 切换显隐 MUST NOT 清空已输入或已自动填充的密码值。
- 样式 MUST 与登录页 CSS Port（`login-page.css`）一致，使用 semantic token，禁止裸 Hex。

## 6. 非功能与安全约束

| 项 | 要求 |
|---|---|
| 存储位置 | 浏览器 `localStorage`（或项目统一 auth 存储模块下的专用 key） |
| 存储内容 | 仅登录页自动填充所需字段；key 命名应带项目前缀，避免与其他项冲突 |
| 安全风险 | 明文密码存于本机；适用于已接受风险的企业内网/受控设备场景；须在 trace 中记录产品确认 |
| 传输 | 登录请求仍走 HTTPS；密码仅出现在请求体，不落库明文 |
| 共享设备 | 登出清凭证（FR-003）降低残留风险 |

## 7. UI / UE 约束

- 继承 REQ-0001 / REQ-0002 登录页布局与 CSS Port，不改动左栏品牌区（`REQ-0003-login-left-panel-refine` 已落地部分保持）。
- 密码显隐按钮位于密码 `field-input` 容器内右侧，不挤压标签行布局。
- Tab 顺序：… → 密码 →（显隐按钮可聚焦）→ 记住登录状态 → 登录按钮。

## 8. 关联需求

| 需求 | 关系 |
|---|---|
| REQ-0001-user-login | 基线登录能力；本需求 MODIFIED「记住登录状态」语义（增加自动填充） |
| REQ-0002-product-brand-login-simplify | 登录表单结构 |
| REQ-0003-login-left-panel-refine | 左栏布局；本需求不改左栏 |
| openspec/specs/auth/spec.md | `remember_me` JWT 行为保持不变 |

## 9. 状态

```yaml
requirement_id: REQ-0003-login-remember-autofill
priority: P1
status: draft
owner: 产品负责人
iteration: sprint-002
suggested_change_id: add-login-remember-autofill
openspec_change: add-login-remember-autofill
estimated_story_points: 4
estimated_person_days: 2
```
