---
bug_id: BUG-0064-theme-selector-sidebar-placement
status: done
created_at: 2026-07-11 19:34:59
updated_at: 2026-07-11 20:04:35
related_requirement: REQ-0020-theme-comfort-refine
suggested_fix_change: fix-theme-selector-sidebar-placement
related_requirements:
  - REQ-0020-theme-comfort-refine
related_bug: null
---

# 回归验收标准

> 修复本缺陷 MUST 将管理端「界面主题」选择器从页面右上角移动到左侧侧边栏，并放置在底部用户头像/账号信息块上方。默认不在本 BUG scope 内修改后端 API、数据库、鉴权、Orval 或主题持久化契约。

## AC-001 主题选择器 MUST 位于侧边栏用户头像上方

**Given** 管理员已登录 Web 管理端  
**When** 进入任意管理端 Shell 页面  
**Then** 左侧侧边栏 MUST 显示「界面主题」选择器  
**And** 该选择器 MUST 位于底部用户头像/账号信息块上方  
**And** 该选择器与用户信息块之间 MUST 有稳定间距，不得重叠或挤压头像、用户名、邮箱、展开按钮

## AC-002 页面右上角 MUST 不再显示主题选择器

**Given** 管理员已登录 Web 管理端  
**When** 进入「接口文档」、首页、用户管理、系统设置等任意管理端页面  
**Then** 页面右上角内容区 MUST NOT 显示「界面主题」选择器  
**And** 页面顶部操作区域 MUST 保持页面动作自身职责，不被全局主题偏好控件占用

## AC-003 主题切换行为 MUST 保持不变

**Given** 主题选择器已移动到侧边栏  
**When** 管理员选择任一主题选项  
**Then** 页面主题 MUST 按原有逻辑即时生效  
**And** 原有主题持久化行为 MUST 保持不变  
**And** 重新进入其他管理端页面后主题状态 MUST 与修复前一致

## AC-004 侧边栏展开/收起状态 MUST 可用

**Given** 侧边栏处于展开状态  
**When** 查看底部用户区域  
**Then** 主题选择器标签、图标与下拉控件 MUST 完整可读且不溢出

**Given** 侧边栏处于收起状态  
**When** 查看底部用户区域  
**Then** 主题入口 MUST 以适合收起态的形态展示或降级  
**And** MUST NOT 与用户头像、折叠按钮、导航项发生视觉重叠  
**And** 文本 MUST NOT 被压缩到不可读状态

## AC-005 管理端 Shell 布局 MUST 不回归

**Given** 修复已完成  
**When** 在管理端主要页面之间切换  
**Then** 侧边栏导航、品牌 Logo、版本号、用户头像/账号信息、退出/用户菜单等现有布局 MUST 保持可用  
**And** 侧边栏滚动、内容区宽度、表格首屏展示 MUST 不因主题选择器迁移发生异常

## AC-006 Design System 与样式约束 MUST 满足

**Given** 修复已完成  
**When** 检查主题选择器样式实现  
**Then** MUST 使用项目既有 semantic token 与组件风格  
**And** MUST NOT 新增裸 Hex 色值  
**And** MUST 使用 `cn()` 或项目既有 className 合并方式  
**And** 控件圆角、边框、间距、字体大小 MUST 与侧边栏信息密度一致

## AC-007 默认不修改 API / DB / Orval

**Given** 修复已完成  
**When** 检查变更范围  
**Then** 默认 MUST 仅涉及 Web 管理端布局与必要测试  
**And** MUST NOT 修改后端 API、SQLite/MySQL schema、Pydantic Schema 或 Orval 生成接口  
**And** 如实现确需调整主题偏好接口，MUST 在 OpenSpec Change 与测试计划中明确说明

## AC-008 自动化回归 MUST 覆盖入口位置

**Given** 对应 fix change 已实现  
**When** 运行 Web 管理端相关测试  
**Then** MUST 覆盖：主题选择器在侧边栏内出现  
**And** MUST 覆盖：页面右上角不再出现主题选择器  
**And** SHOULD 覆盖：选择主题后主题状态仍按原逻辑生效

## AC-009 视觉验收 MUST 覆盖桌面宽度

**Given** 修复已完成  
**When** 在 1440px 或更宽桌面视口查看管理端页面  
**Then** 主题选择器 MUST 位于侧边栏用户头像上方  
**And** 页面右上角 MUST 无主题选择器残留  
**And** 侧边栏底部区域整体视觉应与用户提供截图中的目标意图一致

## AC-010 移动或窄屏降级 MUST 不破坏可用性

**Given** 管理端在窄屏或移动视口展示  
**When** 打开侧边栏或导航抽屉  
**Then** 主题选择入口 MUST 仍可访问  
**And** MUST 不遮挡导航项、用户头像或退出入口  
**And** 如窄屏采用不同布局，MUST 在验收记录中说明降级策略
