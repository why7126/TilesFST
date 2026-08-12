---
requirement_id: REQ-0109-admin-theme-user-menu-modes
created_at: 2026-08-11 08:51:10
updated_at: 2026-08-11 08:51:10
owner: product
source: requirement.md
---

# REQ-0109 业务流程

## 1. 用户操作流程

```text
后台用户进入 /admin/*
  |
  v
打开侧边栏底部用户菜单
  |
  v
在菜单展开层点击主题切换按钮
  |
  +-- 当前为 dark_flagship --> 切换为 system
  |
  +-- 当前为 system --------> 切换为 dark_flagship
  |
  v
前端立即写入 localStorage 并应用实际主题
  |
  v
已登录？
  |
  +-- 否 --> 保留本机偏好，结束
  |
  +-- 是 --> 调用账号主题偏好同步 API
                  |
                  +-- 成功 --> 用户资料中的 theme_mode 与本机一致
                  |
                  +-- 失败 --> 本机主题保持生效，展示非阻断错误反馈
```

## 2. 跟随系统解析流程

```text
theme_mode = system
  |
  v
读取 prefers-color-scheme
  |
  +-- light --> data-theme = light
  |
  +-- dark / unknown --> data-theme = dark
```

## 3. 历史偏好兼容流程

```text
读取 localStorage 或账号 theme_mode
  |
  v
是否为新枚举值？
  |
  +-- system / dark_flagship --> 直接使用
  |
  +-- light ------------------> 归一为 system
  |
  +-- comfort_dark -----------> 归一为 dark_flagship
  |
  +-- 其他未知值 -------------> 归一为 system 或产品默认策略
```

## 4. 与父需求差异

| 项 | REQ-0020 | REQ-0109 |
|---|---|---|
| 主题数量 | 系统默认、暗色旗舰、舒适暗色、浅色 | 暗色旗舰、跟随系统 |
| 入口形态 | 可位于用户菜单、设置页、顶部工具区或等价入口 | 明确移入用户菜单 |
| 控件形态 | 允许选择器 | 明确为切换按钮，不展示额外开关文案 |
| 重点 | 建立主题舒适度与多主题能力 | 收敛模式、降低认知成本、统一个人偏好入口 |

## 5. 影响边界

| 领域 | 影响 |
|---|---|
| Web 管理端 | 影响用户菜单、侧边栏、主题上下文、登录前初始化、主题样式回归。 |
| API | 影响当前用户主题偏好请求和返回枚举。 |
| Orval | 需要同步生成客户端类型。 |
| 数据库 | 不新增表；如已有字段保留旧值，使用兼容映射处理。 |
| 小程序 | 不涉及。 |
| Docker Compose | 不涉及。 |
