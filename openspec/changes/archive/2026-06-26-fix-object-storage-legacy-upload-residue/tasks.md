## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0008-object-storage-legacy-upload-residue` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 确认 BUG-0006 MinIO 上传与读取基线已 archive
- [x] 1.4 grep 确认 `settings.upload_dir` / `UPLOAD_DIR` 当前业务依赖范围
- [x] 1.5 确认本 change 不改变上传 API schema，默认不需要 Orval

## 2. Legacy uploads 清理

- [x] 2.1 新增 `scripts/clean_legacy_uploads.py`，支持 dry-run 与 `--apply`
- [x] 2.2 脚本 MUST 从 SQLite 收集媒体 `object_key` 引用（brands、users 头像、tiles 等已知字段）
- [x] 2.3 脚本 MUST 仅删除 `data/uploads/` 下不在引用集合中的业务媒体孤儿文件
- [x] 2.4 脚本 MUST 保留 `.gitkeep` 与目录占位结构
- [x] 2.5 在 `data/README.md` 文档化手动清理步骤（含 dry-run 示例）

## 3. 配置与 Docker 收敛

- [x] 3.1 评估并移除 `docker-compose.yml` 中无用的 `./data/uploads` 挂载（若 backend 无依赖）
- [x] 3.2 评估从 `src/backend/app/core/config.py` 移除或 deprecated `upload_dir`
- [x] 3.3 更新根目录 `.env.example`：`UPLOAD_DIR` 移除或标注历史兼容
- [x] 3.4 修复仍引用 `UPLOAD_DIR` 的测试（改用 tmp_path，不恢复生产本地写入）
- [x] 3.5 确认 `data/processed`、`data/tmp` 挂载仍满足非上传用途

## 4. 文档同步

- [x] 4.1 更新 `data/README.md`：澄清 `data/minio` vs `data/uploads` 职责
- [x] 4.2 更新 `docs/07-object-storage-strategy.md`：补充 post-migration cleanup 说明
- [x] 4.3 更新 `docs/02-deployment.md`：本地 MinIO 持久化卷与 legacy 清理指引
- [x] 4.4 若需要，更新 `rules/data-management.md` 运行时数据说明

## 5. 可选一致性检查

- [x] 5.1 合并进清理脚本 `--check-only`
- [x] 5.2 检查工具 MUST 报告 uploads 孤儿数量或「无残留」
- [x] 5.3 为脚本添加单元测试或文档化手动验证步骤

## 6. 测试与回归

- [x] 6.1 回归 `tests/test_admin_brands.py` 媒体上传与 `/media` 读取
- [x] 6.2 回归其他媒体上传测试（头像、SKU 若存在）
- [x] 6.3 Docker Compose：上传品牌 Logo 后 MinIO 有对象、`data/uploads` 无新增业务文件（已移除 uploads 挂载；见 test-plan 手动验证项）
- [x] 6.4 清理脚本 dry-run + apply 后在本地验证品牌 Logo 仍正常展示

## 7. 验收与追溯

- [x] 7.1 对照 `issues/bugs/BUG-0008-object-storage-legacy-upload-residue/acceptance.md` 完成 AC-001 ~ AC-007
- [x] 7.2 更新本 change `trace.md`、`acceptance.md`、`test-plan.md`
- [x] 7.3 更新 BUG trace 与 `iterations/sprint-002` 中 BUG-0008 Change 状态
- [x] 7.4 评估 `docs/knowledge-base/incidents/`：清理策略已写入 data/docs，无需单独 incident 条目
