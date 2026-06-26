---
change_id: fix-object-storage-legacy-upload-residue
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: applied
updated_at: 2026-06-27 00:04:00
---

# 测试计划

## 1. 单元 / 集成

| 用例 | 命令 / 说明 | 结果 |
|---|---|---|
| 清理脚本单元测试 | `python -m pytest tests/test_clean_legacy_uploads.py -q` | 4 passed |
| 品牌媒体上传回归 | `cd src/backend && pytest tests/test_admin_brands.py -q` | passed |
| 认证回归 | `cd src/backend && pytest tests/test_auth.py -q` | passed |
| 清理脚本 dry-run | `python scripts/clean_legacy_uploads.py` | 6 orphans listed |
| 清理脚本 apply | `python scripts/clean_legacy_uploads.py --apply` | 6 deleted |
| check-only | `python scripts/clean_legacy_uploads.py --check-only` | exit 0 |

## 2. Docker Compose（手动）

1. `./scripts/docker-up.sh`
2. 上传品牌 Logo 并保存
3. 确认 MinIO Console / `data/minio/tile-info-platform/` 有对象
4. 确认 `data/uploads/original/` 无新增业务文件（backend 已无 uploads 卷挂载）
5. 访问 `/admin/brands` 确认 Logo 展示

## 3. 文档检查

- [x] `data/README.md` 双目录说明
- [x] `docs/07-object-storage-strategy.md` cleanup 段落
- [x] `docs/02-deployment.md` MinIO 卷说明
- [x] `rules/data-management.md` uploads 历史说明
