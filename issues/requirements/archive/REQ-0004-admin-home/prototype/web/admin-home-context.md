# 管理后台首页 V5 - 产品原型图上下文工程

## 1. 原型目标

本原型用于指导 Cursor / AI 前端开发还原 TILESFST 管理后台首页。开发时应优先参考 `prototype/web/admin-home.html`，并以 `prototype/images/admin-home.png` 作为视觉 Golden Reference。

## 2. 设计来源

- 全局设计规范：`ui-design.md`
- 登录页视觉参考：`user-login.html` / `user-login.png`
- 页面：Web 管理后台首页
- 版本：REQ-0003-admin-home-v5
- 风格：工业石材 · 暗色旗舰风

## 3. 页面画布

| 项目 | 值 |
|---|---|
| 推荐设计稿尺寸 | 1440 × 1024 |
| 页面布局 | 左侧固定 Sidebar + 右侧工作台内容 |
| Sidebar 宽度 | 264px |
| Sidebar 高度 | 100vh |
| 右侧内容 | 独立滚动 |
| 主内容最大宽度 | 1080px |

## 4. 信息架构

```text
<body>
  <div class="admin-shell">
    <aside class="sidebar">
      <div class="logo">TILESFST</div>
      <div class="nav-scroll">
        <nav>OPERATIONS...</nav>
        <nav>SYSTEM...</nav>
      </div>
      <div class="sidebar-user">
        <div class="user-dropdown">...</div>
        <button class="user-trigger">...</button>
      </div>
    </aside>
    <main class="main-content">
      <section>数据概览</section>
      <section>快捷操作</section>
      <section>最近更新</section>
    </main>
  </div>
</body>
```

## 5. 左侧 Sidebar 说明

### 5.1 固定行为

Sidebar 必须固定为视口高度：

```css
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  height: 100vh;
  overflow: auto;
}
```

该行为保证左侧导航栏不会随着右侧内容高度变化，体验类似 ChatGPT.com。

### 5.2 导航内容

OPERATIONS：

- 首页
- 瓷砖 SKU
- 瓷砖品牌
- 瓷砖类目
- Banner 管理

SYSTEM：

- 用户管理
- 系统设置

### 5.3 用户菜单

用户菜单位于 Sidebar 底部，使用 `margin-top: auto` 固定到底部。用户菜单按钮展示头像、用户名、邮箱和展开箭头。

用户菜单按钮下方不得直接展示「退出登录」。

### 5.4 用户下拉框

下拉框固定在用户按钮上方，包含：

```text
个人资料
密码修改
────────
退出登录
```

- 下拉框背景：`rgba(33,30,22,.98)`
- 边框：`0.5px solid rgba(255,255,255,.1)`
- 分隔线：`0.5px solid rgba(255,255,255,.07)`
- 退出登录：使用风险色 `#E07050`

## 6. 右侧内容说明

右侧删除所有顶部欢迎区和复杂 Dashboard 模块，仅保留三个工作台区块。

### 6.1 数据概览

4 个指标卡，采用四列网格：

- SKU 总数
- 品牌数量
- Banner 数量
- 用户数量

### 6.2 快捷操作

V5 快捷操作从 8 个缩减为 4 个，采用单行四列布局：

- 新增 SKU
- 新增品牌
- 新增类目
- 新增 Banner

已删除：

- 导入 SKU
- 导入图片
- 价格管理
- 操作日志

### 6.3 最近更新

最近更新为表格结构：

| 字段 | 说明 |
|---|---|
| 更新时间 | 变更发生时间 |
| 类型 | SKU / 品牌 / Banner / 类目 / 系统 |
| 名称 | 被操作对象 |
| 操作人 | 后台用户或 system |

## 7. 关键样式 Token

| Token | 值 | 用途 |
|---|---|---|
| 页面底色 | `#18160F` | 全局背景 |
| 深色底 | `#100F0A` | Sidebar 深层背景 |
| 卡片底 | `#211E16` | 卡片 / 下拉框 |
| 主文字 | `#EDE8DF` | 标题和重要文本 |
| 次文字 | `rgba(237,232,223,.5)` | 普通说明 |
| 弱文字 | `rgba(237,232,223,.3)` | 辅助说明 |
| 品牌金 | `#C8A055` | Logo / 激活态 / 数字 |
| 分割线 | `rgba(255,255,255,.07)` | 细线 |
| 强分割线 | `rgba(255,255,255,.1)` | 卡片边框 |
| 风险色 | `#E07050` | 退出登录 |

## 8. 响应式规则

- 桌面端：`grid-template-columns: 264px 1fr`。
- 小于 1024px：Sidebar 变为顶部区域，用户菜单隐藏。
- 小于 1024px：指标卡和快捷操作变为 2 列。
- 小于 640px：指标卡和快捷操作变为 1 列，表格隐藏操作人列。

## 9. 一致性检查清单

- [ ] Logo 为 TILESFST。
- [ ] 左侧 Sidebar 固定 100vh。
- [ ] 右侧内容独立滚动。
- [ ] 用户菜单固定在 Sidebar 底部。
- [ ] 用户菜单下方没有直接退出登录。
- [ ] 下拉框包含个人资料、密码修改、退出登录。
- [ ] 退出登录与上方两项之间有分隔线。
- [ ] 快捷操作仅有 4 个。
- [ ] 快捷操作中没有导入 SKU、导入图片、价格管理、操作日志。
- [ ] 页面整体延续登录页暗色旗舰风。
