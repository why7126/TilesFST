## Tasks

### 1. 实现（CSS Port）

- [x] 1.1 `AuthBrandPanel.tsx`：`.brand-title` →「瓷砖信息管理后台」；`.logo` 保持 TilesFST
- [x] 1.2 `LoginForm.tsx`：移除「忘记密码？」按钮；调整 `.form-options` 布局
- [x] 1.3 `login-page.css`：收紧 `.brand-top` / `.brand-content` Logo 间距
- [x] 1.4 `login-page.css`：调整 `.stats-card` / `.material-board` 避免 126 格遮挡

### 2. 测试

- [x] 2.1 更新 `LoginPage.test.tsx`：断言主标题「瓷砖信息管理后台」
- [x] 2.2 更新 `LoginForm.test.tsx`：断言无「忘记密码？」
- [x] 2.3 `cd src/web && pnpm test`（via `npx vitest run` 23/23 pass）
- [x] 2.4 `python scripts/validate-design-system.py`

### 3. 构建

- [x] 3.1 `cd src/web && pnpm build`（via `npx vite build` pass）
- [x] 3.2 `./scripts/run-tests.sh`（12/12 pass）

### 4. 视觉验收

- [x] 4.1 1440×1024 目视 checklist（design.md 8 项）写入 `trace.md`
- [x] 4.2 1280×720 复验无页面级纵向滚动（CSS 保持 `overflow: hidden` + fixed shell）
- [x] 4.3 更新 `iterations/sprint-001/acceptance-report.md` REQ-0003 项

### 5. 文档与追溯

- [x] 5.1 更新 `issues/requirements/REQ-0003-login-left-panel-refine/trace.md` status
- [x] 5.2 更新 `issues/requirements/REQ-0003-login-left-panel-refine/acceptance.md` 勾选
- [x] 5.3 更新 `iterations/sprint-001/sprint.yaml` 登记 REQ-0003 与 change（已在纳入 sprint 时完成）

### 6. 归档准备

- [x] 6.1 `openspec validate fix-login-left-panel-refine`
- [x] 6.2 完成后 `/opsx-archive fix-login-left-panel-refine`
