# 提案：管理后台主题入口移入用户菜单并收敛模式

## 背景

REQ-0109 已评审并纳入 `sprint-022`。当前管理后台主题选择器位于侧边栏用户区上方，且 Web / API / Design System 仍暴露 `system`、`dark_flagship`、`comfort_dark`、`light` 四种主题模式；这让主题偏好与导航混杂，也增加用户理解成本。

## 变更目标

- 将管理后台主题入口从侧边栏独立选择器移入用户菜单展开层。
- 使用主题切换按钮完成 `dark_flagship` 与 `system` 两种模式切换，不在按钮旁展示额外开关说明文案。
- 管理后台不再向用户暴露 `comfort_dark` 与独立 `light` 选项。
- 保留本地首屏恢复、已登录账号级同步、同步失败非阻断反馈和页面状态不丢失。
- 对历史 `light` 与 `comfort_dark` 偏好值提供兼容归一策略。
- 同步当前用户主题偏好 API、OpenAPI、Orval 和相关前后端测试。

## 非目标

- 不新增第三种主题模式。
- 不新增店主 Web 或微信小程序主题切换入口。
- 不把主题偏好放入系统设置页或全局配置。
- 不重做管理后台整体视觉。
- 不新增数据库表，不改变 Docker Compose、Nginx、端口或部署拓扑。

## 能力范围

### 新增能力

无。

### 修改能力

- `web-client`：管理端主题入口位置、控件形态、可见主题模式和本地/账号同步行为。
- `design-system`：Web 主题模式范围和 `/design-system` 主题预览范围。
- `auth`：当前用户主题偏好 API 支持值、历史值兼容和无效值校验。

## 影响范围

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
    - web-client
    - design-system
    - auth
```

## 风险

- 历史账号或本地偏好仍保存 `light` / `comfort_dark`，需要前后端一致归一，避免未知状态。
- API 枚举收敛若未同步 OpenAPI / Orval，会导致生成类型继续暴露废弃模式。
- 用户菜单空间有限，主题按钮不能挤压个人资料、密码修改和退出登录。
- `system` 在浅色系统下仍会解析为亮色，需要在视觉验收中覆盖暗色旗舰和系统浅色解析状态。

