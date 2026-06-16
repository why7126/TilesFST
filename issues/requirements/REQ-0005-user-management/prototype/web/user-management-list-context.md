# REQ-0005 用户管理页面 v1 - 列表页原型上下文工程

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 TILESFST 管理后台用户管理列表页。开发时应优先参考：

1. `user-management-list.html`
2. `user-management-list.png`
3. `issues/requirements/REQ-0005-user-management/requirement.md`
4. `rules/ui-design.md`
5. `issues/requirements/REQ-0004-admin-home/prototype/web/admin-home.html` / `admin-home.png`

## 2. 页面画布

| 项目 | 值 |
|---|---|
| 设计稿尺寸 | 1440 × 1024 |
| 布局 | 左侧固定 Sidebar + 右侧内容区 |
| Sidebar 宽度 | 264px |
| 右侧内容最大宽度 | 1080px |
| 页面滚动 | 右侧 main-content 独立滚动 |

## 3. 页面结构

```text
<body>
  <div class="admin-shell">
    <aside class="sidebar">...</aside>
    <main class="main-content">
      <div class="content-inner">
        <section class="page-hero">...</section>
        <section class="filter-card">...</section>
        <section class="summary-grid">...</section>
        <section class="table-section">...</section>
      </div>
    </main>
  </div>
</body>
```

## 4. Sidebar

- Logo：TILESFST。
- 当前激活菜单：SYSTEM > 用户管理。
- 用户管理菜单仅后台管理员可见。
- 用户菜单固定在底部，保持首页样式。

## 5. 页面标题区

标题：`用户管理`
说明：`维护前台用户与后台管理用户，控制后台访问权限、账号状态与基础资料。`
右侧主按钮：`添加用户`。

主按钮使用品牌金实底，按钮圆角 2px，文字深色。

## 6. 搜索筛选区

筛选区使用卡片容器，包含：

- 关键词搜索输入框
- 角色筛选
- 状态筛选
- 登录情况筛选
- 搜索按钮
- 重置按钮

所有输入和选择器高度统一为 40px。

## 7. 用户统计区

4 个指标卡：

1. 用户总数
2. 当前筛选
3. 正常用户
4. 已冻结

卡片样式继承首页 metric-card。

## 8. 用户列表

表格字段：

| 字段 | 样式说明 |
|---|---|
| 用户 | 头像 + 用户名 + 昵称/邮箱 |
| 角色 | 金色轻量 badge |
| 状态 | 正常/冻结/删除不同 badge |
| 最后登录 | 弱文字；从未登录使用强调提示 |
| 创建时间 | 弱文字 |
| 操作 | 文本按钮组 |

操作按钮：编辑、重置密码、冻结/解冻、删除。

删除规则：只有从未登录用户允许删除；否则按钮置灰。

## 9. 分页

分页位于表格底部，包含：

- 每页条数选择
- 当前范围：`1-10 / 126`
- 上一页/下一页
- 页码按钮

## 10. 一致性检查清单

- [ ] Sidebar 宽度 264px。
- [ ] 当前菜单为用户管理。
- [ ] 页面右侧无首页顶部欢迎区。
- [ ] 搜索筛选卡片在标题下方。
- [ ] 表格视觉与首页最近更新表格一致。
- [ ] 添加用户按钮为品牌金实底。
- [ ] 分页按钮圆角 2px。
- [ ] 没有添加用户弹窗遮罩。
