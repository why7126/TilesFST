---
bug_id: BUG-0105-admin-brand-list-logo-renders-text
acceptance_status: passed
created_at: 2026-08-03 08:22:26
updated_at: 2026-08-03 20:52:16
related_requirement:
source_change: fix-admin-brand-list-logo-rendering
source_sprint: sprint-018
---

# 回归验收标准

> 本 BUG 修复范围限定为管理后台品牌列表第一列 Logo 展示。必须将有效 Logo 渲染为图片或缩略图，并保持品牌列表既有操作能力。

## AC-001 已上传 Logo 的品牌 MUST 显示图片

**Given** 管理后台存在已上传 Logo 的品牌  
**When** 用户进入品牌列表页面  
**Then** 第一列品牌 Logo MUST 显示为图片或缩略图  
**And** 不得直接显示图片 URL、对象 key、文件名或普通文本字段值

## AC-002 未上传 Logo 的品牌 MUST 显示合理占位

**Given** 管理后台存在未上传 Logo 的品牌  
**When** 用户进入品牌列表页面  
**Then** 第一列品牌 Logo MUST 显示设计系统内的合理占位状态  
**And** 不得显示空白错位、破图图标或调试文案

## AC-003 图片加载失败 MUST 有兜底状态

**Given** 品牌 Logo 地址无效、过期或加载失败  
**When** 用户查看品牌列表第一列  
**Then** 页面 MUST 显示稳定的加载失败占位或默认 Logo 状态  
**And** 不得暴露内部对象 key、原始存储路径或异常堆栈

## AC-004 品牌列表布局 MUST 稳定

**Given** 修复已完成  
**When** 用户在常见桌面视口查看品牌列表  
**Then** Logo 列宽、高度和行间距 MUST 保持稳定  
**And** 图片不得挤压品牌名称、操作按钮或其他列内容  
**And** 图片加载中、加载成功和加载失败状态不得造成表格明显跳动

## AC-005 品牌管理操作 MUST NOT 回归

**Given** 修复已完成  
**When** 用户使用品牌列表搜索、编辑、上下架或其他既有操作  
**Then** 这些操作 MUST 保持可用  
**And** Logo 列渲染调整不得改变品牌数据保存、筛选或排序语义

## AC-006 修复范围 MUST 同步验证 API 字段契约

**Given** 修复已完成  
**When** 检查品牌列表 Logo 数据来源  
**Then** 前端渲染字段 MUST 与后端返回字段一致  
**And** 若涉及 API Schema 变化，MUST 同步 OpenAPI、Orval、API 文档和测试  
**And** 若不涉及 API Schema 变化，MUST 在实现或验收记录中说明无需 Orval

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-brand-list-logo-rendering
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

