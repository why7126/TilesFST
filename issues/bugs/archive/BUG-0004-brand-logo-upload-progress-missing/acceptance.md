---
bug_id: BUG-0004-brand-logo-upload-progress-missing
status: in_sprint
updated_at: 2026-06-26 09:35:50
---

# 回归验收标准

## AC-001 选择 Logo 后必须触发上传

**Given** 管理员或员工已登录 Web 管理端并打开品牌编辑弹窗  
**When** 点击「更换 Logo」并选择 JPG、PNG 或 WebP 图片  
**Then** 系统 MUST 立即触发 Logo 上传流程。  
**And** 上传请求 MUST 使用既有后端授权上传接口。  
**And** 不得要求用户先保存品牌后才开始上传文件。

## AC-002 上传过程中必须展示进度反馈

**Given** 用户已选择 Logo 图片  
**When** 上传正在进行  
**Then** 弹窗内 MUST 展示进度条、百分比或等价可感知进度反馈。  
**And** 上传过程中「更换 Logo」入口 SHOULD 进入上传中或禁用状态，避免重复触发。  
**And** 进度反馈 MUST 位于 Logo 控件附近，用户无需离开弹窗即可感知等待状态。

## AC-003 上传成功后必须更新弹窗预览

**Given** Logo 上传接口返回成功  
**When** 返回新的 `object_key` 和可访问 URL  
**Then** 弹窗中的 Logo 预览 MUST 更新为新图片。  
**And** 表单提交时 MUST 使用新的 `logo_object_key`。  
**And** 保存品牌后再次打开编辑弹窗，MUST 回显最新 Logo。

## AC-004 上传失败时必须展示错误和重试入口

**Given** Logo 上传接口返回失败、网络异常或文件类型不合法  
**When** 上传流程结束  
**Then** 弹窗内 MUST 展示明确错误信息。  
**And** 用户 MUST 可以重新选择图片重试。  
**And** 失败时不得把旧 Logo 静默替换为无效预览或错误对象 Key。

## AC-005 重新选择同一文件也应可触发上传

**Given** 用户已经选择过某个 Logo 文件  
**When** 用户再次选择同一个文件  
**Then** 系统 SHOULD 能再次触发上传或明确提示当前文件已选择。  
**And** 文件 input 不得因 value 未重置导致用户无法重试。

## AC-006 修复不得破坏既有品牌管理功能

**Given** 用户在品牌管理页操作  
**When** 执行查询、重置、分页、新增、编辑、启用、停用、删除品牌  
**Then** 既有功能 MUST 保持可用。  
**And** 现有权限边界 MUST 保持：仅 admin / employee 可维护品牌，store_owner 不得进入管理端品牌维护能力。

## AC-007 修复必须符合媒体与安全规范

**Given** 修复完成  
**When** 检查 Logo 上传链路  
**Then** 图片上传 MUST 经过后端鉴权、MIME 校验和对象 Key 安全处理。  
**And** 不得暴露真实密钥、内部绝对路径或未授权对象存储地址。  
**And** 不得让前端绕过后端直连未授权对象存储。

## AC-008 测试必须覆盖上传进度与预览更新

**Given** 缺陷进入修复阶段  
**When** 完成 `fix-*` OpenSpec Change  
**Then** 应补充或更新前端测试，覆盖选择文件后进入上传中状态、进度反馈展示、上传成功后预览更新。  
**And** 应补充或更新测试，覆盖上传失败错误展示和重试入口。  
**And** 如上传 API 客户端为支持进度回调而改变接口封装，MUST 更新相关类型、调用方和必要文档。

## AC-009 Design System 约束必须满足

**Given** 修复修改 Web UI 样式  
**When** 检查品牌编辑弹窗 Logo 上传控件  
**Then** 进度条、按钮、错误文案和预览态 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式。  
**And** 不得新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式。
