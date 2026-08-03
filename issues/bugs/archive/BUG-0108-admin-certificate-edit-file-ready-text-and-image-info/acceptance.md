---
bug_id: BUG-0108-admin-certificate-edit-file-ready-text-and-image-info
acceptance_status: passed
created_at: 2026-08-03 08:23:05
updated_at: 2026-08-03 20:52:16
---

# 验收标准

## AC-001 PDF/兼容文件区域不显示冗余就绪文案

- GIVEN 管理员打开已有证书的编辑弹窗
- WHEN 证书已有 PDF 或兼容文件
- THEN PDF/兼容文件区域不应显示 `证书文件已就绪`
- AND 仍应保留文件缺失、上传失败、格式不兼容等必要错误提示

## AC-002 已有图片信息正常回显

- GIVEN 已有证书包含一张或多张图片
- WHEN 管理员打开该证书编辑弹窗
- THEN 图片列表应正常显示
- AND 每张图片应显示可用于运营判断的预览或必要信息
- AND 不应显示对象 key、原始文件名或无意义文件名噪音

## AC-003 主图状态正确显示

- GIVEN 已有证书存在主图
- WHEN 管理员打开编辑弹窗查看图片区域
- THEN 主图状态应正确标识
- AND 非主图不应被误标为主图
- AND 没有主图时应呈现明确且可操作的状态

## AC-004 图片替换、删除和新增后可保存并回显

- GIVEN 管理员在证书编辑弹窗中新增、替换或删除图片
- WHEN 保存成功并再次打开同一证书编辑弹窗
- THEN 图片列表、主图状态、预览信息和操作状态应与保存结果一致
- AND 不应出现图片信息全部消失或状态错乱

## AC-005 与既有图片文件名噪音问题不回归

- GIVEN 修复后打开证书列表和证书编辑弹窗
- WHEN 查看证书文件、证书图片和主图信息
- THEN 不应重新出现对象 key、内部路径、原始文件名或无意义文件名噪音
- AND `BUG-0089` 相关展示约束应继续成立

## AC-006 回归范围覆盖

- SHOULD 覆盖有 PDF、有兼容文件、无文件、有图片、无图片、单图、多图、有主图和无主图场景。
- SHOULD 覆盖新增图片、替换图片、删除图片、设置主图、保存后重新打开编辑弹窗。
- SHOULD 覆盖管理后台证书列表进入编辑弹窗的主流程。
- SHOULD 补充或更新 Web 前端组件测试、页面集成测试或等价手工验收记录。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:52:16
accepted_by: workflow-sync
source_change: fix-admin-certificate-edit-file-image-display
source_sprint: sprint-018
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

