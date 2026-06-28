---
title: Change Trace
purpose: fix-object-storage-legacy-upload-residue 追溯记录
change_id: fix-object-storage-legacy-upload-residue
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: archived
created_at: 2026-06-27 00:00:20
applied_at: 2026-06-27 00:04:00
archived_at: 2026-06-27 00:11:29
---

# Trace

## 1. 来源

| 项目 | 内容 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0008-object-storage-legacy-upload-residue` |
| Sprint | `sprint-002` |
| 严重等级 | medium |
| 评审 | `REV-BUG-0008-001`，approved |
| 前置 BUG | `BUG-0006-object-storage-upload-not-minio` |
| 前置 Change | `fix-object-storage-upload-not-minio`（archived） |

## 2. Bug Analysis Report

| 维度 | 结论 |
|---|---|
| 现象 | BUG-0006 后 `data/uploads` 仍有孤儿文件，与 `data/minio` 双目录并存，文档与配置未收敛 |
| 复现 | 对比 DB `logo_object_key` 与 uploads/minio 目录文件名 |
| 根因分类 | legacy-local-upload / post-migration-cleanup / documentation |
| 关联需求 | 无 |
| 修复 Change | `fix-object-storage-legacy-upload-residue` |

## 3. 验收映射

| BUG AC | OpenSpec 覆盖 | 状态 |
|---|---|---|
| AC-001 | legacy uploads 孤儿清理 | done |
| AC-002 | 新上传不写 uploads | done |
| AC-003 | 文档澄清 | done |
| AC-004 | UPLOAD_DIR 收敛 | done |
| AC-005 | 品牌 Logo 无回归 | done |
| AC-006 | `--check-only` | done |
| AC-007 | pytest | done |

## 4. Checklist

- [x] 通过 OpenSpec CLI 创建 change
- [x] proposal.md 包含 Why / Impact / Rollback Plan
- [x] design.md 包含根因、修复方案、测试策略
- [x] specs 覆盖 legacy cleanup 与 uploads 禁止写入
- [x] tasks.md 全部完成
- [x] `/opsx-apply fix-object-storage-legacy-upload-residue`
- [x] `/opsx-archive fix-object-storage-legacy-upload-residue`

## 5. 影响评估

| 影响面 | 结论 |
|---|---|
| API schema | 未改变 |
| Orval | 不需要 |
| 数据库 | 无迁移 |
| Docker | 已移除 `./data/uploads` backend 挂载 |
| Web | 无 UI 变更 |
| 本地清理 | 删除 6 个 uploads 孤儿 PNG |

## 6. 实现摘要

- 新增 `scripts/clean_legacy_uploads.py`（dry-run / `--apply` / `--check-only`）
- 新增 `tests/test_clean_legacy_uploads.py`
- 移除 `settings.upload_dir`、`.env.example` 中 `UPLOAD_DIR`、Docker uploads 挂载
- 更新 `data/README.md`、`docs/02-deployment.md`、`docs/07-object-storage-strategy.md`、`rules/data-management.md`

## 7. 知识库

未新增 `docs/knowledge-base/incidents/` 条目；清理策略已写入 `data/README.md` 与对象存储/部署文档，足够支撑后续运维。

## 8. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 00:00:20 | `/bug-opsx` | 创建 OpenSpec Change |
| 2026-06-27 00:04:00 | `/opsx-apply` | 完成脚本、配置收敛、文档与测试 |
| 2026-06-27 00:11:29 | `/opsx-archive` | 同步 `object-storage` spec，归档至 `archive/2026-06-26-fix-object-storage-legacy-upload-residue/` |
