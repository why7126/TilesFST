# REQ-0015 修改密码页面/弹窗 v1 - 产品原型图上下文工程

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 TILESFST 管理后台「修改密码」弹窗。开发时应优先参考：

1. `password-change-modal.html`
2. `password-change-modal.png`
3. `requirement.md`
4. `issues/requirements/archive/REQ-0005-user-management/prototype/web/user-management-list.html`（背景基准）
5. `rules/ui-design.md`

## 2. 页面画布

| 项目 | 值 |
|---|---|
| 设计稿尺寸 | 1440 × 1024 |
| 布局 | 左侧固定 Sidebar + 右侧内容区 + 居中弹窗 |
| Sidebar 宽度 | 264px |
| 右侧内容最大宽度 | 1080px（shell content-inner 以当前 admin-home.css 为准） |
| 页面滚动 | 右侧 main-content 独立滚动；弹窗打开时主体不可操作 |
| 弹窗宽度 | 520px |
| 遮罩 | 原型 rgba(0,0,0,.62)；实现用 DS semantic overlay class |

## 3. 视觉继承关系

- 继承用户管理列表页的 Sidebar、背景渐变、表格、按钮、Badge、分页样式。
- 修改密码采用居中 modal，不新增独立页面路由。
- 保持 `ui-design.md` 的暗色旗舰风：深色底、品牌金主 CTA、0.5px 细线、2–3px 低圆角。
- 生产实现 MUST NOT 复制 HTML 裸 Hex；使用 semantic token。

## 4. 页面结构

```text
<body>
  <div class="admin-shell is-modal-open">
    <aside class="sidebar">
      ...
      <div class="sidebar-user">
        <div class="user-menu open">
          <button>个人资料</button>
          <button class="active">密码修改</button>
          <div class="menu-divider"></div>
          <button class="danger">退出登录</button>
        </div>
        <button class="user-trigger">...</button>
      </div>
    </aside>

    <main class="main-content" aria-hidden="true">
      用户管理列表页主体作为背景
    </main>
  </div>

  <div class="modal-backdrop">
    <section class="modal-card password-modal">
      <header class="modal-head">修改密码 + close</header>
      <div class="modal-body">
        原密码 / 新密码 / 确认新密码 / 规则提示 / 安全提示
      </div>
      <footer class="modal-footer">取消 / 保存修改</footer>
    </section>
  </div>
</body>
```

## 5. Sidebar 用户菜单

用户菜单位于左侧底部用户卡上方，宽度与用户卡一致：

- 个人资料
- 密码修改（打开弹窗时菜单项可高亮）
- 分隔线
- 退出登录

## 6. 弹窗内容

### 6.1 标题区

- 标题：修改密码
- 副标题：当前账号：{displayName}
- 右侧关闭按钮：30 × 30px，细边框，hover 高亮

### 6.2 说明区

`为了账号安全，建议使用 8 位以上并包含字母、数字和特殊字符的密码。修改成功后需要重新登录。`

说明区左侧 2px 品牌金竖线。

### 6.3 表单区

字段顺序：原密码 → 新密码 → 确认新密码

- label：10px 大写/弱色字距风格
- 输入框高度 44px；右侧「显示」按钮
- focus：品牌金边框

### 6.4 密码规则提示

位于新密码下方：

- 8-32 位字符
- 至少包含字母和数字
- 不能与原密码相同

默认弱色；满足后绿色成功态。

### 6.5 底部按钮

- 取消：透明按钮
- 保存修改：品牌金实底主按钮
- 高度 40px，圆角 2px

## 7. 交互说明

- 弹窗打开后聚焦原密码
- ×、取消、Esc 关闭；有内容时二次确认
- 保存前前端校验；保存中禁用按钮
- 成功后 Toast + logout + 跳转登录页

## 8. 一致性检查清单（trace 验收引用）

- [ ] Sidebar 宽度 264px，与用户管理页一致
- [ ] 背景为用户管理列表页，不重做页面主体
- [ ] 用户菜单从底部用户卡向上展开
- [ ] 弹窗居中，宽度 520px
- [ ] 弹窗 0.5px 细边框与 3px 圆角
- [ ] 主按钮品牌金实底、深色文字
- [ ] 输入框 44px，focus 品牌金边框
- [ ] 密码规则提示为可开发文案（非 lorem）
- [ ] 与 PNG Golden Reference 并排无显著偏差
