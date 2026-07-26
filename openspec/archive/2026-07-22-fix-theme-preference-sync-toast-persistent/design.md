## Context

BUG-0074 指出生产环境 Web 管理端主题切换链路存在两个问题：

- 账号偏好同步失败后出现固定文案提示。
- 该提示持续存在，不会自动消失。

当前代码路径的初步分析显示：

- `ThemeContext` 在账号偏好同步失败时设置错误文案，并保留本机主题选择。
- `AdminLayout` 监听 `themeError` 后将文案写入 `toast` state，并清空 ThemeContext error。
- `AdminLayout` 对 `notice` 有 3200ms 自动清除逻辑，但 `toast` 没有等价生命周期。
- `AdminToast` 是纯展示组件，不负责倒计时关闭或手动关闭。

生产同步失败原因尚未定案，需要在实现阶段收集 `PATCH /api/v1/auth/me/theme` 的 Network/日志证据。

## Goals

- 主题偏好同步失败提示自动消失或可关闭，不常驻页面。
- 同步失败时本机主题仍立即生效，不回退、不丢失页面状态。
- 多次快速切换主题时不产生堆叠、重复刷屏或遮挡主要内容。
- 已登录用户合法主题偏好能在生产链路中保存并通过 `GET /api/v1/auth/me` 读取。
- 修复保持认证、权限、Token 存储、路由守卫和主题模式枚举不回退。

## Non-Goals

- 不新增主题模式。
- 不调整 Design System 颜色 Token。
- 不新增账号偏好管理页面。
- 不改变认证策略、用户角色权限或 Token 生命周期。
- 不绕过后端鉴权保存主题偏好。
- 不直接修复其他生产 BUG，例如 Banner 保存、视频播放或小程序跳转。

## Root Cause

直接原因是主题同步错误进入管理端固定 Toast 状态后没有清理生命周期。根本原因是全局管理端 Toast 使用方式不统一：不同页面自行管理提示状态，`AdminToast` 本身没有 `duration` / `onClose` 契约，`AdminLayout` 的主题错误提示没有复用已有 `notice` 自动清除逻辑。

账号偏好同步失败的生产原因可能包括：

- 401 / 403：Token 缺失、过期或用户状态异常。
- 404 / 网关问题：生产后端未部署 `PATCH /api/v1/auth/me/theme` 或 Nginx `/api/` 反代异常。
- 500 / DB 问题：生产 `users.theme_mode` 字段缺失、迁移未执行或写入失败。
- envelope 异常：前端收到 200 但 `response.data.data` 缺失，触发前端错误兜底。

## Proposed Design

1. Toast 生命周期修复：
   - 为 `AdminLayout` 的主题错误 Toast 增加自动清除计时器，或将自动清除/关闭能力收敛到 `AdminToast`。
   - 默认持续时间可沿用管理端已有短提示节奏（例如 3200ms）或采用等价设计系统反馈周期。
   - 清理逻辑必须在组件卸载或新提示覆盖时取消旧计时器。
2. 主题同步行为保持：
   - `ThemeContext` 在同步失败时仍保留本机主题模式和 localStorage 写入。
   - 已登录用户同步成功后继续用后端返回的 `theme_mode` 更新账号状态。
   - 未登录用户切换主题不得调用账号偏好同步接口。
3. 生产同步排查：
   - 确认 `PATCH /api/v1/auth/me/theme` 请求携带 Authorization Header。
   - 确认生产后端路由、Nginx `/api/` 反代和 DB `users.theme_mode` 字段。
   - 若仅前端 Toast 生命周期修复即可闭环，则不修改 API/DB/Orval。
   - 若发现 API/DB 漂移，按 API/数据库治理同步 OpenAPI、Orval、docs、schema、migration 和测试。
4. 回归边界：
   - 登录、退出、Token 存储、路由守卫、用户角色权限不变。
   - 管理端主题选择器侧边栏位置不回退。
   - Design System semantic token 使用不回退，不引入新的全局 Toast 库。

## Testing

- Web 前端测试覆盖：同步失败时本机主题仍生效，并展示错误提示。
- Web 前端测试覆盖：同步失败提示会自动消失或可关闭。
- Web 前端测试覆盖：多次快速切换主题不堆叠错误提示。
- Web 前端测试覆盖：未登录用户切换主题不调用账号偏好同步接口。
- 后端集成测试保留或补充：合法主题偏好保存成功、非法值返回 400、未认证返回 401、禁用用户返回 403。
- 若涉及 API 契约变化，运行 OpenAPI / Orval 生成并补充接口文档。
- 若涉及 DB 迁移，补充 SQLite/MySQL schema 与迁移测试。

## Risks

- 将 Toast 自动清除收敛到组件层可能影响其他页面成功/失败提示的可见时长。
- 仅修复前端 Toast 生命周期可能掩盖生产账号偏好 API 的真实故障，因此必须保留生产 Network/日志证据要求。
- 如果生产失败来自 DB schema 漂移，修复需要部署迁移，单纯前端改动不足以闭环。

缓解方式：先以 BUG acceptance 中 AC-BUG-001 至 AC-BUG-011 为实现验收标准，实施时明确 API/DB/Orval 是否受影响。
