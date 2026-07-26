---
change_id: fix-object-storage-legacy-upload-residue
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: applied
updated_at: 2026-06-27 00:04:00
---

# 验收标准

来源：`issues/bugs/archive/BUG-0008-object-storage-legacy-upload-residue/acceptance.md`

## AC-001 legacy uploads 孤儿已清理

- [x] 执行清理脚本后，`data/uploads/` 无无 DB 引用的业务媒体孤儿（本地删除 6 个 PNG）
- [x] MinIO 有效对象与 DB `object_key` 未受影响

## AC-002 新上传不写 uploads

- [x] 上传链路仍仅写 MinIO；已移除 backend `UPLOAD_DIR` 挂载

## AC-003 文档澄清

- [x] `data/README.md`、`docs/07-object-storage-strategy.md`、`docs/02-deployment.md` 已更新

## AC-004 UPLOAD_DIR 收敛

- [x] 已移除 `settings.upload_dir`、`.env.example` 中 `UPLOAD_DIR`、`docker-compose.yml` uploads 挂载

## AC-005 品牌 Logo 无回归

- [x] `test_admin_brands.py` 媒体用例通过

## AC-006 可选检查工具

- [x] `clean_legacy_uploads.py --check-only` 报告无残留

## AC-007 测试

- [x] `tests/test_clean_legacy_uploads.py` 4 passed；`test_admin_brands.py` + `test_auth.py` 30 passed
