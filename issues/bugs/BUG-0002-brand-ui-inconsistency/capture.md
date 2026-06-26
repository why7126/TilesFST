---
bug_id: BUG-0002-brand-ui-inconsistency
status: captured
recorded_at: 2026-06-25
severity_hint: medium
environment: local|docker
related_requirement: null
related_change: null
---

# 现象

品牌管理相关界面存在两处 UI 设计一致性问题：

1. 瓷砖品牌列表底部的分页 UI 与用户管理页分页 UI 不一致。
2. 添加品牌弹窗中的「品牌 Logo」选择文件控件 UI 与当前管理端整体 Design System 风格不一致。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖品牌」列表页，观察列表底部分页区域。
3. 打开用户管理页，对比用户管理页底部分页区域的控件尺寸、边框、圆角、文字、激活态和布局。
4. 返回「瓷砖品牌」页，点击添加品牌入口打开弹窗。
5. 观察弹窗内「品牌 Logo」选择文件控件，与弹窗内其他输入项、按钮和管理端整体视觉进行对比。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 瓷砖品牌列表分页应与用户管理页分页样式和交互状态保持一致；添加品牌弹窗的 Logo 选择文件控件应使用 Design System 语义 Token、统一圆角、边框、字号、按钮态，并与管理端表单控件风格一致。 |
| **实际** | 品牌列表分页与用户管理页分页视觉不一致；Logo 文件选择控件呈现为与整体设计不统一的文件上传/选择样式，破坏弹窗表单一致性。 |

# 影响范围

- Web 管理端：瓷砖品牌列表页。
- Web 管理端：添加品牌弹窗。
- 可能影响品牌管理相关视觉验收和管理端组件一致性。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | UI 视觉一致性缺陷 |
| 严重程度建议 | medium |
| 可能修复面 | Web 管理端品牌管理页分页组件与 Logo 上传/选择控件 |
| 设计约束 | 应对齐 `rules/ui-design.md`、`src/web/README.md`、`/design-system` 预览页和用户管理页既有实现 |

# 附件

- 暂无截图。
- 参考页面：瓷砖品牌列表页、用户管理页、添加品牌弹窗。
- 参考规范：`rules/ui-design.md` §5.10 分页器、Design System 应用规范。
