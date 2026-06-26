---
title: 变更验收标准
purpose: add-brand-management OpenSpec 可测试验收项
content: 自 issues/requirements/REQ-0005-brand-management/acceptance.md 映射
source: acceptance.md
owner: product
status: draft
note: 实现与 /opsx-apply 对齐
---

# 验收标准（OpenSpec Change）

## AC-001 ~ AC-004 访问与布局

- [ ] 已登录 admin/employee 可访问 `/admin/brands`，标题「瓷砖品牌」
- [ ] Sidebar「瓷砖品牌」激活；AdminLayout 264px + 1080px 内容区
- [ ] page-header：MASTER DATA、说明、「＋ 新增品牌」
- [ ] 无导出、批量、「品牌列表」「品牌检索」标题

## AC-005 ~ AC-019 列表、删除、分页

- [ ] 四指标卡；筛选一行；表格列与操作列正确
- [ ] 删除仅 SKU=0 且停用可点；其余置灰 + tooltip
- [ ] 确认弹窗标题「删除品牌」；服务端 `BRAND_DELETE_FORBIDDEN`
- [ ] 分页含跳页与每页 20/50/100

## AC-020 ~ AC-026 弹窗

- [ ] 720px 弹窗、字段顺序、校验、无状态字段
- [ ] Logo JPG/PNG/WebP；介绍 max 500
- [ ] 创建默认 ENABLED（UI 不提示）

## AC-027 ~ AC-036 接口与技术

- [ ] Admin Brands API 完整；Orval 已生成
- [ ] `brands` 表与 MinIO Logo
- [ ] CSS Port、vitest、pytest 通过

## AC-037 ~ AC-039 视觉

- [ ] HTML 原型并排（PNG 补齐后升级）
- [ ] trace.md checklist 填写
