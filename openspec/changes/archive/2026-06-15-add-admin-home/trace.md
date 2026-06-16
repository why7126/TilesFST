# add-admin-home — Trace

## 变更摘要

- **REQ**: `REQ-0004-admin-home`
- **Iteration**: `sprint-002`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `admin-home.html`）
- **Auth 冻结**: 不修改 `features/auth/` 核心逻辑
- **Mock**: Dashboard 指标与最近更新使用静态数据
- **Status**: applied（待 `/opsx-archive`）

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0004-admin-home/requirement.md` |
| 验收 | `issues/requirements/REQ-0004-admin-home/acceptance.md` |
| HTML Golden | `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.html` |
| PNG Golden | `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.png` |
| Context | `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home-context.md` |
| Design | `openspec/changes/add-admin-home/design.md` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 退出登录位置 | Sidebar 用户下拉；MODIFIED `web-client`「退出登录」 |
| 品牌 TILESFST | 全大写，以 HTML 为准 |
| TSX 裸 Hex | 禁止；CSS port 使用 `--color-*` |
| auth/me 无 email | `{username}@tilesfst.com` fallback |

## PNG 视觉 Diff Checklist（1280×1024）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 页面背景 + shell 渐变 | pass | `.admin-shell` token 映射 |
| 2 | 264px + 1fr 网格布局 | pass | |
| 3 | Sidebar 100vh sticky | pass | |
| 4 | 右侧 100vh 独立滚动 | pass | |
| 5 | Logo **TILESFST** 全大写 + 品牌金 | pass | |
| 6 | OPERATIONS 五 nav + SYSTEM 两 nav | pass | |
| 7 | 首页 nav active | pass | |
| 8 | 用户菜单固定 Sidebar 底部 | pass | |
| 9 | 无用户按钮下方直接退出 | pass | |
| 10 | 下拉框在用户按钮上方 | pass | |
| 11 | 下拉含个人资料、密码修改、分隔线、退出 | pass | |
| 12 | 退出登录风险色 | pass | `--color-error` |
| 13 | 无顶栏 header 退出按钮 | pass | |
| 14 | 数据概览四列指标卡 | pass | |
| 15 | 指标数值品牌金 | pass | |
| 16 | 快捷操作仅 4 项新建入口 | pass | |
| 17 | 无导入/价格/日志快捷项 | pass | 测试断言 |
| 18 | 最近更新表格四列 + badge | pass | |
| 19 | 无欢迎区/待办/数据质量等删除模块 | pass | |
| 20 | 主内容 max-width 1080px 居中 | pass | |
| 21 | 卡片 0.5px 边框 + 3px 圆角 | pass | |
| 22 | `<1024px` Sidebar 顶置、用户菜单隐藏 | pass | media query |

## 验证命令

```bash
cd src/web && npx vitest run src/features/admin src/pages/admin   # 5 passed
cd src/web && npm run build                                       # success
docker compose build web                                          # success
```

## 已知可接受偏差

| 项 | 说明 |
|----|------|
| 用户邮箱 | mock fallback 非真实 email 字段 |
| 导航 icon | CSS 占位 icon |
| Logo 字体 | `font-brand` vs HTML Georgia |
| PNG 人工 sign-off | Sprint 002 acceptance 建议 1280×1024 并排复核 |

## 遵循规范

- `rules/ui-design.md`
- `rules/directory-structure.md`
- `rules/testing.md`
- `AGENTS.md` Design System 应用规范
