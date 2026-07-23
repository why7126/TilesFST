---
title: 业务流程
purpose: REQ-0027 Web 管理端移动端基础适配优化流程与验收路径
content: 基于 requirement.md v1、用户故事与知识库横切最佳实践生成
source: AI 根据 PRD 与知识库最佳实践生成，项目团队确认
update_method: PRD、验收范围或原型变更时同步更新
owner: product
status: done
created_at: 2026-07-05 10:17:18
updated_at: 2026-07-22 09:23:55
note: REQ-0027-mobile-page-adaptation
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
选择移动端验收视口
  ├─ 375x812  手机小屏
  ├─ 390x844  主流手机
  ├─ 768x1024 小屏平板
  └─ 1440x1024 桌面回归
  ↓
进入当前已实现 Web 管理端路由
  ├─ 登录 / 无权限
  ├─ Dashboard / Shell / Sidebar
  ├─ 列表页：筛选 → 表格 → 分页 → 行内操作
  ├─ 表单页：设置 / 个人资料 → 保存 / 重置 / dirty 切换
  ├─ 弹窗：新增 / 编辑 / 状态确认 / 删除 / 重置密码
  └─ 上传控件：选择文件 → 上传状态 → 同会话回显
  ↓
记录移动端 smoke 结果
  ├─ 页面级横向溢出？
  ├─ 控件重叠？
  ├─ 弹窗可关闭 / 可滚动 / 底部按钮可达？
  ├─ 表格横向滚动是否限制在容器内？
  └─ 横切 AC 是否通过或有 N/A 理由？
```

## 2. 角色与权限边界

```text
JWT → ProtectedRoute
  ├─ role ∈ {admin, employee} → 允许访问授权范围内的 /admin/*
  ├─ requireAdmin 路由 → 仅 admin 可访问
  └─ 未授权 / 无权限 → /admin/login 或 /admin/forbidden
```

| 产品角色 | 后端 role | 本 REQ 影响 |
|---|---|---|
| 后台管理员 | admin | 覆盖所有已实现管理端路由 |
| 内部员工 | employee | 覆盖其可访问的管理端路由 |
| 店主 | store_owner | 不纳入本 REQ；不得新增管理端访问能力 |
| 小程序用户 | miniapp user | 不涉及 |

## 3. 页面验收路径

### 3.1 登录与 Shell

```text
/admin/login
  ↓
<1024px 隐藏左侧品牌区
  ↓
表单居中、账号密码可输入、登录按钮可点击
  ↓
进入 /admin/dashboard
  ↓
AdminLayout 在 ≤1023px 下单列显示，Sidebar 顶置或既有响应式结构可访问
```

### 3.2 列表页

```text
打开列表路由
  ↓
筛选区按断点降级
  ├─ ≥1024px：沿用桌面布局
  ├─ ≤1023px：2列或适配布局
  └─ ≤639px：单列可操作
  ↓
执行查询 / 重置
  ↓
查看表格
  ├─ 表格宽度超出 → table-card 内部横向滚动
  └─ 页面本身不得不可控横向滚动
  ↓
分页换页 / 调整 page size
  ↓
执行行内操作
  ├─ 状态变更 → DS confirm → fixed toast
  └─ 删除 / 重置密码 → DS confirm → fixed toast
```

### 3.3 表单与设置页

```text
/admin/profile 或 /admin/settings/:tab
  ↓
小屏下主内容单列可读
  ↓
编辑字段
  ↓
保存
  ├─ 成功 → fixed toast，不推挤页面
  └─ 失败 → 字段/区域错误提示，不遮挡操作按钮
  ↓
恢复默认 / dirty 切换
  └─ DS modal 二次确认，无 window.confirm
```

### 3.4 弹窗与抽屉

```text
列表页点击新增 / 编辑 / 详情 / 状态操作
  ↓
弹窗或抽屉打开
  ↓
375px 宽度下：
  ├─ 头部标题可读
  ├─ 关闭按钮可点击
  ├─ body 可滚动
  ├─ footer 主操作可达
  └─ 错误提示不造成关键控件错位
```

## 4. 横切知识库嵌入点

| 标签 | 覆盖流程 | 预防问题 |
|---|---|---|
| admin-list | 列表筛选、表格、分页、状态操作 | 分页 DOM 漂移、toast layout shift、原生 confirm 回归 |
| admin-form | 个人资料、系统设置、dirty 切换 | 双保存 CTA、原生 confirm、inline tip 推挤布局 |
| admin-modal | SKU / Banner / 品牌 / 用户等弹窗 | `modal-card` 层叠覆盖、宽弹窗 computed width 错误、矮视口不可滚动 |
| media-upload | Logo / Banner / SKU 媒体 / 头像上传控件 | 上传状态机缺失、同会话不回显、Docker 3000 边界未验收 |

## 5. 与关联 REQ 差异

| 对比项 | REQ-0004 | REQ-0011 | REQ-0013 | REQ-0027 |
|---|---|---|---|---|
| Shell 基础 | 建立 | 使用 | 调整 padding | 移动端基础可用回归 |
| Sidebar 折叠 | 不含 | 核心范围 | 不改列宽 | 只确保小屏不冲突 |
| Content 宽度 | 初始策略 | 无 | fluid 优化 | 避免移动端页面级横向溢出 |
| 页面覆盖 | Dashboard 为主 | 全 `/admin/*` 壳层 | 重点 SKU/用户/Dashboard | 当前已实现 `/admin/*` 页面 |
| 测试重点 | 首页 / Sidebar | 折叠状态 | 宽屏布局 | 375/390/768/1440 smoke |

## 6. 本期不包含流程

- 店主 Web 商品浏览流程。
- 微信小程序页面浏览或上传流程。
- 新增 API、数据模型或上传后端链路。
- 管理端完整移动办公重构（例如底部 Tab、移动端专属列表卡片、批量操作移动化）。
