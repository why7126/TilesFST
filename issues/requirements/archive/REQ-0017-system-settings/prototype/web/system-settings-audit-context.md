# REQ-0017 系统设置页面 v2 - 审计配置原型上下文工程

## 1. 原型目标

本文件用于指导 Cursor / AI 前端开发还原 TILESFST 管理后台系统设置「审计配置」页面。

开发优先级：
1. `prototype/web/system-settings-audit.html`
2. `prototype/web/system-settings-audit.png`
3. `requirement.md`
4. `rules/ui-design.md`
5. 用户管理列表页 Golden Reference

## 2. 页面画布

| 项目 | 值 |
|---|---|
| 设计稿尺寸 | 1440 × 1024 |
| 布局 | 左侧固定 Sidebar + 右侧独立滚动内容区 |
| Sidebar 宽度 | 264px |
| 内容最大宽度 | 1080px |
| 当前菜单 | SYSTEM / 系统设置 |
| 当前设置分组 | 审计配置 |

## 3. 页面结构

```text
admin-shell
├─ sidebar
└─ main-content
   └─ content-inner
      ├─ page-hero
      ├─ summary-grid
      └─ settings-layout
         ├─ settings-nav
         └─ settings-panel
```

## 4. 当前分组交互说明

- 左侧设置分组导航中「审计配置」为激活态。
- 页面保存按钮位于标题区和底部操作区，底部包含取消、恢复默认、保存设置。
- 所有必填字段使用红色星号。
- 修改后展示「有未保存修改」提示。
- 保存成功后需要写入审计日志。

## 5. 一致性检查

- 使用暗色工业风、品牌金主按钮、0.5px 细分割线。
- 不允许出现浅色后台模板。
- 不允许自由调整 Sidebar 宽度、页面最大宽度、按钮高度和圆角。
- HTML 必须与 PNG 视觉一致。
