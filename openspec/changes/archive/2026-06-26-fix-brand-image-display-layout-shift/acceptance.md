---
purpose: fix-brand-image-display-layout-shift OpenSpec 可测试验收项
content: 自 issues/bugs/archive/BUG-0003-brand-image-display-layout-shift/acceptance.md 映射
bug_id: BUG-0003-brand-image-display-layout-shift
status: proposed
created_at: 2026-06-25 22:28:15
---

# 验收标准

- [ ] 上传品牌 Logo 后，接口返回的 `url` 或 `preview_url` 可被浏览器实际加载。
- [ ] 品牌列表页展示已上传 Logo；无 Logo 或加载失败时展示稳定占位。
- [ ] 品牌编辑弹窗打开时回显已上传 Logo；更换 Logo 后即时更新预览。
- [ ] 启用/停用品牌提示出现与消失时，`page-hero`、统计卡、筛选区、表格和分页不发生纵向位移。
- [ ] 删除、创建、更新品牌等提示同样不推挤页面主体。
- [ ] 媒体访问链路符合后端授权、MIME 校验、MinIO 单桶/前缀和 object_key 安全要求。
- [ ] 品牌查询、分页、新增、编辑、启停、删除等既有功能不回退。
- [ ] 若 API 响应结构变化，OpenAPI、Orval 和 API 文档已同步。
- [ ] Web UI 修改使用既有管理端样式变量或 semantic token，无新增裸 Hex。
