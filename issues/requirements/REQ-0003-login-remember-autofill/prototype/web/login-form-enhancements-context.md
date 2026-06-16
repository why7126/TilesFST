# REQ-0003-login-remember-autofill — 登录表单增强原型上下文

## 1. 目标

描述登录页 **记住凭证自动填充** 与 **密码显隐** 的 UI 行为，供实现与验收参考。视觉基线仍以 REQ-0001 登录页为准：

- `issues/requirements/REQ-0001-user-login/prototype/web/user-login.html`
- `issues/requirements/REQ-0001-user-login/prototype/web/user-login.png`

左栏布局以 `REQ-0003-login-left-panel-refine` 为准，本需求 **不修改** 左栏。

## 2. 密码字段（FR-004）

```text
.field（密码）
├─ .label-row → 「密码」
└─ .password-wrap（新增容器，position relative）
   ├─ input.field-input（type=password | text）
   └─ button.password-toggle（眼睛图标，输入框内右侧）
```

| 状态 | input type | 按钮 aria-label |
|---|---|---|
| 隐藏（默认） | password | 显示密码 |
| 显示 | text | 隐藏密码 |

- 图标建议使用 lucide `Eye` / `EyeOff` 或 SVG，颜色 `--login-muted`，hover `--login-text`。
- 输入框右侧预留 padding，避免文字与图标重叠。

## 3. 记住登录状态（FR-001 ~ FR-003）

- 复选框文案：**记住登录状态**（不变）。
- **行为**（实现必做，静态 HTML 无法表达）：
  - 成功登录 + 勾选 → `localStorage` 保存 `{ username, password, remember: true }`。
  - 再次进入登录页 → 填充两输入框 + 勾选复选框。
  - 成功登录 + 未勾选 → 清除 `localStorage` 凭证。
  - 退出登录 → 清除 `localStorage` 凭证。

### Storage key（定稿）

`stonex_login_credentials`（JSON）。

## 4. 与 REQ-0001 acceptance 对齐

- 密码输入框支持显隐切换（眼睛图标）— **本需求落地**。
- 记住我延长 JWT — 现网已有；本需求 **扩展** 为同时自动填充表单。

## 5. 一致性检查清单

- [ ] 密码显隐按钮在输入框内右侧
- [ ] 默认密码隐藏
- [ ] 记住登录状态文案不变
- [ ] 自动填充不破坏 Enter 提交与 Tab 顺序
- [ ] 左栏品牌区无变更（`REQ-0003-login-left-panel-refine`）
- [ ] 无忘记密码入口
- [ ] CSS Port + semantic token，无裸 Hex

## 6. 参考 HTML 片段（密码行）

```html
<div class="field">
  <div class="label-row"><label for="password">密码</label></div>
  <div class="password-wrap">
    <input id="password" class="field-input" type="password" placeholder="请输入登录密码" />
    <button type="button" class="password-toggle" aria-label="显示密码" aria-pressed="false">
      <!-- eye icon -->
    </button>
  </div>
</div>
```

完整页面结构见 REQ-0001 `user-login.html`；实现时在 `LoginForm.tsx` + `login-page.css` 对齐上述结构。
