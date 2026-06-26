---
bug_id: BUG-0003-brand-image-display-layout-shift
status: approved
updated_at: 2026-06-25 22:19:51
---

# 回归验收标准

## AC-001 品牌 Logo 上传后必须返回可访问 URL

**Given** 管理员或员工已登录 Web 管理端  
**When** 在品牌新增或编辑弹窗中上传 JPG、PNG 或 WebP Logo  
**Then** 上传接口返回的 `url` 或 `preview_url` MUST 能被浏览器实际加载。  
**And** 返回的 `object_key` MUST 符合项目对象存储前缀策略。  
**And** 不得暴露真实密钥、内部绝对路径或未授权对象存储地址。

## AC-002 品牌列表必须正常展示已上传 Logo

**Given** 某品牌已保存 `logo_object_key`  
**When** 管理员访问「瓷砖品牌」列表页  
**Then** 品牌列 MUST 展示已上传 Logo 图片。  
**And** 图片加载失败时 MUST 有稳定空态或错误态，不得导致单元格尺寸跳动。  
**And** 无 Logo 的品牌仍 MUST 展示品牌首字/缩写占位。

## AC-003 品牌编辑弹窗必须正常回显已上传 Logo

**Given** 某品牌已保存 Logo  
**When** 管理员点击「编辑」打开品牌编辑弹窗  
**Then** 「品牌Logo」区域 MUST 展示当前已上传 Logo 预览。  
**And** 更换 Logo 后，弹窗内预览 MUST 即时更新。  
**And** 保存后再次打开弹窗，MUST 仍能回显最新 Logo。

## AC-004 品牌状态变更提示不得造成页面上下波动

**Given** 管理员位于「瓷砖品牌」列表页  
**When** 执行启用或停用品牌操作  
**Then** 系统 SHOULD 展示成功或失败提示。  
**And** 提示出现和消失 MUST NOT 改变 `page-hero`、统计卡、筛选区、表格或分页区域的纵向位置。  
**And** 提示组件 MUST 使用固定 toast、预留稳定空间或其他不推挤主体内容的方式。

## AC-005 删除与保存提示不得造成页面上下波动

**Given** 管理员位于「瓷砖品牌」列表页或品牌弹窗  
**When** 执行删除品牌、创建品牌、更新品牌等会触发提示的操作  
**Then** 提示出现和消失 MUST NOT 造成页面主体上下位移。  
**And** 弹窗内表单错误仍可使用 inline 错误文案，但不得影响列表页主体稳定性。

## AC-006 修复必须符合媒体与对象存储安全规范

**Given** 修复完成  
**When** 检查媒体上传与访问链路  
**Then** 图片上传 MUST 经过后端校验，限制 MIME Type 和扩展名。  
**And** 不得使用用户原始文件名作为最终可信对象 Key。  
**And** 媒体访问 MUST 符合 MinIO 单桶与前缀策略，或明确采用受控 `/media` 代理。  
**And** 不得让前端绕过后端直连未授权对象存储。

## AC-007 修复不得破坏品牌管理既有功能

**Given** 管理员在品牌管理页操作  
**When** 执行查询、重置、分页、每页显示切换、新增、编辑、启用、停用、删除品牌  
**Then** 既有功能 MUST 保持可用。  
**And** 现有权限边界 MUST 保持：仅 admin / employee 可维护品牌，store_owner 不得进入管理端品牌维护能力。

## AC-008 测试必须覆盖图片展示与提示稳定性

**Given** 缺陷进入修复阶段  
**When** 完成 `fix-*` OpenSpec Change  
**Then** 应补充或更新测试，覆盖上传返回 URL、列表 Logo 渲染、编辑弹窗 Logo 回显。  
**And** 应补充或更新前端测试，确认状态提示不使用会推挤主体内容的文档流插入模式。  
**And** 如涉及 API 响应结构变化，MUST 更新 OpenAPI 与 Orval 客户端。

## AC-009 Design System 约束必须满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** 新增或修改样式 MUST 使用既有管理端样式变量、语义 Token 或共享组件模式。  
**And** 不得新增裸 Hex、未登记局部色值或与 `rules/ui-design.md` 冲突的圆角、字号、边框和提示样式。
