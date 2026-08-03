---
change_id: fix-admin-certificate-edit-file-image-display
acceptance_status: pending
source_bug: BUG-0108-admin-certificate-edit-file-ready-text-and-image-info
created_at: 2026-08-03 08:32:06
updated_at: 2026-08-03 08:32:06
---

# Acceptance

## 验收来源

- `BUG-0108-admin-certificate-edit-file-ready-text-and-image-info/acceptance.md`

## 验收项

- [ ] 管理员打开已有证书编辑弹窗时，PDF/兼容文件区域不显示 `证书文件已就绪`。
- [ ] 已有证书图片列表正常显示，图片卡片可供运营识别。
- [ ] 主图状态正确显示，非主图不被误标，没有主图时状态明确。
- [ ] 新增、替换、删除图片并保存后，再次打开编辑弹窗回显一致。
- [ ] 不回归 `BUG-0089`：不展示对象 key、原始文件名或无意义文件名噪音。
- [ ] 覆盖有 PDF、有兼容文件、无文件、有图片、无图片、单图、多图、有主图和无主图场景。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
evidence: []
failed_items: []
notes: 待 /opsx-apply 后回填。
```
