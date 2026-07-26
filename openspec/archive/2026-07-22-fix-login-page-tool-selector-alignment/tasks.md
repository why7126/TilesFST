## 1. Web 登录页工具区修复

- [x] 1.1 定位 `src/web/src/pages/admin/LoginPage.tsx`、`src/web/src/features/auth/components/LoginFormPanel.tsx`、`src/web/src/features/auth/styles/login-page.css` 与主题切换组件相关样式。
- [x] 1.2 调整登录页组件结构或 CSS，使主题选择模块与语言选择模块共享统一工具区布局或等价对齐规则。
- [x] 1.3 保留语言选择按钮文案「简体中文⌄」、`.language` 原型视觉和 `aria-label="切换语言"`。
- [x] 1.4 保留主题选择器现有主题模式、`aria-label="主题"` 和主题持久化行为。
- [x] 1.5 验证桌面视口下两个控件垂直对齐、右侧边界和间距稳定。
- [x] 1.6 验证窄屏视口下工具区不重叠、不裁切、不遮挡登录标题、表单字段或安全提示。

## 2. 回归测试

- [x] 2.1 更新 Web 登录页测试，断言主题选择模块与语言选择按钮同时存在。
- [x] 2.2 更新 Web 登录页测试，断言语言按钮可通过 `aria-label="切换语言"` 定位。
- [x] 2.3 更新主题相关测试或登录页测试，断言主题选择控件仍可用且主题切换不回退。
- [x] 2.4 回归登录表单必填校验、账号密码提交、记住登录状态和登录成功跳转。
- [x] 2.5 如具备浏览器验收条件，补充桌面和窄屏截图或等价证据，覆盖工具区对齐状态。

## 3. 文档与同步

- [x] 3.1 如仅调整 Web 登录页布局且 API 契约不变，在实现输出中说明不需要 OpenAPI / Orval。
- [x] 3.2 若实际修改 API 字段或响应结构，同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。
- [x] 3.3 更新 `BUG-0071` trace、Change trace 与验收证据。
- [x] 3.4 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
