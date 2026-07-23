## 1. 生产问题确认

- [x] 1.1 在 Web 管理端定位主题切换链路：`ThemeContext`、`ThemeSwitcher`、`AdminLayout`、`AdminToast` 与 `theme-api`。
- [x] 1.2 复现或模拟 `PATCH /api/v1/auth/me/theme` 失败，确认同步失败提示进入管理端 Toast 后是否常驻。
- [x] 1.3 收集生产或等价环境的 `PATCH /api/v1/auth/me/theme` Network 证据：状态码、响应 envelope、请求耗时和 Authorization Header 是否存在。
- [x] 1.4 排查生产后端日志、Nginx `/api/` 反代和 `users.theme_mode` 字段/迁移状态，判断是否需要 API 或 DB 修复。

证据：本次无真实生产访问权限，使用等价本地集成测试和源码链路确认。`tests/integration/api/test_auth_theme_preference.py` 覆盖 200 envelope + `data.theme_mode`、400、401、403；`auth-api.ts` 请求拦截器存在 Bearer Authorization；`src/web/nginx.conf` 存在 `/api/` 反代；SQLite/MySQL schema 与迁移均包含 `users.theme_mode`。未发现需要 API / DB 修复。

## 2. Web Toast 生命周期修复

- [x] 2.1 为主题同步失败 Toast 增加自动消失或关闭入口，确保提示不会常驻页面。
- [x] 2.2 确保同步失败时本机主题仍立即生效，`data-theme-mode` / `data-theme` 和 localStorage 不回退。
- [x] 2.3 确保多次快速切换主题时提示不堆叠、不重复刷屏、不遮挡主要管理端内容。
- [x] 2.4 确保未登录用户切换主题只保存本机偏好，不调用账号主题偏好同步接口。
- [x] 2.5 保持管理端登录、退出、Token 存储、路由守卫、用户权限判断和主题选择器侧边栏位置不回退。

## 3. API / DB 条件修复

- [x] 3.1 若生产 `PATCH /api/v1/auth/me/theme` API 正常，仅记录不需要 OpenAPI / Orval。
- [x] 3.2 若修改 API 字段、响应结构或错误码，同步 OpenAPI、Orval、`docs/03-api-index.md` 和后端集成测试。
- [x] 3.3 若生产缺少 `users.theme_mode` 或迁移异常，同步 SQLite/MySQL schema、迁移、数据库文档和测试。
- [x] 3.4 不得通过绕过鉴权、前端直写账号偏好或手工修改真实用户数据完成修复。

结论：本次仅修改 Web Toast 生命周期和前端测试；未修改 API 字段、响应 envelope、错误码、数据库 schema、迁移或真实数据，不需要 OpenAPI / Orval / DB 文档同步。

## 4. 回归测试与验收证据

- [x] 4.1 补充或更新 Web 前端测试，覆盖同步失败提示自动消失或可关闭。
- [x] 4.2 补充或更新 Web 前端测试，覆盖同步失败时本机主题保持生效。
- [x] 4.3 补充或更新 Web 前端测试，覆盖未登录用户切换主题不调用同步接口。
- [x] 4.4 回归后端主题偏好 API 集成测试：成功保存、非法主题、未认证、禁用用户。
- [x] 4.5 如具备生产或预生产环境，提供 `PATCH /api/v1/auth/me/theme` 成功保存与刷新/重新登录保持偏好的 smoke 证据。
- [x] 4.6 修复完成后评估是否需要沉淀 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。

证据：`pnpm --dir src/web exec vitest run src/features/admin/components/AdminLayout.test.tsx src/features/theme/ThemeContext.test.tsx` 通过 13 项；`uv run pytest tests/integration/api/test_auth_theme_preference.py` 通过 5 项。当前无生产/预生产访问权限，4.5 以本地等价 API 集成测试覆盖；上线前建议由部署侧补真实环境 smoke。该修复为局部 Toast 生命周期缺陷，无需新增 `docs/knowledge-base/incidents/`。

## 5. 工作流同步

- [x] 5.1 实现前确认 `BUG-0074` 已纳入 Sprint 正式范围；未纳入时不得运行 `/opsx-apply`。
- [x] 5.2 实现完成后更新 BUG trace、Change trace、验收证据和 Workflow Sync。
