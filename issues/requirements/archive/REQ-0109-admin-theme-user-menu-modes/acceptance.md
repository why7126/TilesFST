---
requirement_id: REQ-0109-admin-theme-user-menu-modes
acceptance_status: passed
created_at: 2026-08-11 08:51:10
updated_at: 2026-08-12 00:15:15
owner: product
source: requirement.md
---

# REQ-0109 验收标准

## 功能 AC

- [ ] AC-001 管理后台侧边栏中不再展示独立主题选择器或主题偏好区域。
- [ ] AC-002 用户菜单展开层内提供主题切换按钮，且按钮不在旁侧展示额外“暗色旗舰 / 跟随系统”等开关说明文案。
- [ ] AC-003 主题切换按钮通过图标、状态样式、`aria-label` 或 tooltip 说明当前主题状态和点击后的切换意图。
- [ ] AC-004 用户菜单中的个人资料、密码修改、退出登录在加入主题按钮后仍可点击、可键盘访问、可正常关闭菜单。
- [ ] AC-005 管理后台可见主题模式仅包含 `dark_flagship` 与 `system`，不再暴露 `comfort_dark` 或独立 `light` 选项。
- [ ] AC-006 当前为 `dark_flagship` 时点击按钮切换为 `system`；当前为 `system` 时点击按钮切换为 `dark_flagship`。
- [ ] AC-007 选择 `dark_flagship` 后，即使操作系统为浅色偏好，管理后台实际主题仍解析为暗色。
- [ ] AC-008 选择 `system` 后，操作系统浅色/深色偏好变化可驱动实际主题在亮/暗之间切换。
- [ ] AC-009 主题切换即时生效，不刷新页面，不丢失当前路由、筛选条件、分页状态、表单输入或已打开弹层状态。
- [ ] AC-010 未登录或登录前初始化时，本地主题偏好可用于首屏恢复，避免主题闪烁或不可读状态。
- [ ] AC-011 已登录用户切换主题后，同步账号级主题偏好；同步失败时本机主题保持生效，并展示非阻断错误反馈。
- [ ] AC-012 切换账号或退出登录后，不错误沿用上一账号的服务端主题偏好。
- [ ] AC-013 历史本地或账号值 `light` 归一为 `system`，页面不进入未知主题状态。
- [ ] AC-014 历史本地或账号值 `comfort_dark` 归一为 `dark_flagship`，页面不进入未知主题状态。
- [ ] AC-015 后端主题偏好请求和用户资料返回枚举与前端主题枚举一致，非法值按 API 规范返回校验错误或按明确兼容策略归一。
- [ ] AC-016 OpenAPI 与 Orval 客户端类型同步更新，不再生成对 `comfort_dark` 和独立 `light` 的可见业务选项依赖。

## UI / 视觉 AC

- [ ] AC-UI-001 主题按钮在 1440px 管理端布局中不与用户姓名、邮箱、头像、菜单项或退出登录按钮重叠。
- [ ] AC-UI-002 侧边栏展开态与收起态下，用户菜单均可打开并触发主题按钮。
- [ ] AC-UI-003 窄屏管理端布局中，主题按钮不破坏既有用户菜单或侧边栏响应式行为。
- [ ] AC-UI-004 主题按钮样式使用 Design System semantic token 或既有 admin token，不新增裸 Hex 或硬编码颜色。
- [ ] AC-UI-005 主题按钮 focus、hover、active、disabled 或 loading 状态具备可见反馈，并与暗色旗舰和系统浅色解析结果均兼容。

## 测试与验证 AC

- [ ] AC-TST-001 前端测试覆盖用户菜单内主题按钮渲染、点击切换、`aria-label` 或 tooltip 语义。
- [ ] AC-TST-002 前端测试覆盖 `THEME_MODES` 收敛、`normalizeThemeMode` 历史值兼容和 `resolveThemeMode` 系统偏好解析。
- [ ] AC-TST-003 前端测试覆盖登录前初始化脚本的历史值兼容和 `data-theme-mode` / `data-theme` 写入。
- [ ] AC-TST-004 后端测试覆盖主题偏好 API 的新枚举、历史值兼容或非法值处理。
- [ ] AC-TST-005 Orval 生成后测试或类型检查通过，确认生成类型与前后端实现一致。

## 横切 AC（knowledge-base）

本 REQ 未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 四类知识库横切标签；用户菜单主题按钮不涉及 CRUD 列表、全页表单保存、弹窗宽度 CSS cascade 或上传链路。因此本节为 N/A，不追加 AC-XCUT。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: update-admin-theme-user-menu-modes
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

