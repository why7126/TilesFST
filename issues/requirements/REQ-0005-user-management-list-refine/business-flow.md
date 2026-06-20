---
title: 业务流程
purpose: 描述列表页 UI 优化后的搜索、列表与分页交互流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: approved
note: REQ-0005-user-management-list-refine
---

# 业务流程

## 1. 与 REQ-0005 的差异

本需求 **仅修改** 下列流程节点；添加/编辑/重置密码/冻结/删除流程不变（见 `REQ-0005-user-management/business-flow.md`）。

```text
变更前                          变更后
────────────────────────────────────────────────────────
点击「搜索」触发查询      →    无搜索按钮；输入防抖/回车/筛选项变更触发
keyword 匹配邮箱/手机号   →    仅匹配 username、display_name
「用户列表」标题行        →    删除
table-toolbar 提示行      →    删除
用户列可能单行挤显示      →    用户名、昵称固定两行
分页「1-10 / N」等        →    左「共 x 个用户」+ 右页码与每页条数
```

## 2. 列表查询流程（优化后）

```text
页面加载 / 条件变更
  ↓
GET /api/v1/admin/users?page=&page_size=&keyword=&role=&status=&login_filter=
  ↓
keyword 仅后端匹配 username、display_name
  ↓
渲染：筛选区 → 指标卡 → 表格（无标题/toolbar）→ 精简分页
```

### 2.1 搜索与重置

```text
用户输入关键词
  ↓
回车 或 防抖（~300ms）后自动请求，page=1
  ↓
或：变更角色/状态/登录情况下拉 → 立即请求，page=1
  ↓
点击「重置」→ 清空全部条件 → page=1 重新请求
```

## 3. 分页交互

```text
左侧展示 summary.total → 「共 {total} 个用户」
  ↓
右侧：‹ 页码 › + 「每页显示 [10|20|50] 条」
  ↓
切换每页条数 → page=1，重新请求
切换页码 → 带当前筛选条件请求
```

## 4. 用户列渲染规则

```text
读取 user.username、user.display_name
  ↓
第一行：username（主色）
第二行：display_name 非空 ? display_name : 「未设置昵称」（弱色）
  ↓
不读取 email 作为列表副标题
```

## 5. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0005-user-management | 列表页、API、权限基线 |
| add-user-management | 已实现代码入口 `UserManagementPage.tsx` |
| user_repository keyword | 须同步移除 email/phone LIKE 条件 |
