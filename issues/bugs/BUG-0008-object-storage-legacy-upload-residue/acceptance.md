---
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: pending_review
updated_at: 2026-06-26 23:55:19
---

# 回归验收标准

## AC-001 历史 uploads 孤儿文件已清理或纳入脚本

**Given** 本地或 Docker 环境曾存在 BUG-0006 修复前的 `data/uploads` 业务文件  
**When** 执行修复提供的清理步骤或脚本  
**Then** `data/uploads/` 下 MUST NOT 存在与 DB `object_key` 无关联的业务媒体孤儿文件。  
**And** 清理 MUST NOT 删除 MinIO 中仍被 DB 引用的对象。  
**And** 清理后 MUST 保留 `.gitkeep` 等目录结构占位（若项目规范要求）。

## AC-002 新上传不得再写入 data/uploads

**Given** BUG-0008 修复已 apply  
**When** 管理端上传品牌 Logo、头像、SKU 图片或 SKU 视频  
**Then** 对象 MUST 仅写入 MinIO `MINIO_BUCKET`。  
**And** `data/uploads/` 下 MUST NOT 新增与 object key 对应的业务文件。  
**And** 上传与 `/media/{object_key}` 读取行为 MUST 与 BUG-0006/BUG-0007 验收一致，无回归。

## AC-003 文档澄清 data/minio 与 data/uploads 职责

**Given** 修复包含文档更新  
**When** 阅读 `data/README.md` 及对象存储/部署相关文档  
**Then** MUST 明确说明：  
- `data/minio` 为本地 Docker 下 MinIO 持久化卷，桶内对象增长属预期；  
- `data/uploads` 不为业务上传正式存储，BUG-0006 后不应承载新媒体；  
- 媒体排查应以 DB `object_key` + MinIO 为准。

## AC-004 UPLOAD_DIR 配置与挂载收敛

**Given** 修复评估完成  
**When** 检查 `docker-compose.yml`、`.env.example` 与后端配置  
**Then** 若 `UPLOAD_DIR` 与 `./data/uploads` 挂载已无业务用途，MUST 移除或标注为历史兼容且不参与上传。  
**And** 移除配置 MUST NOT 破坏现有 MinIO 上传、读取与测试。  
**And** 若保留配置，文档 MUST 说明保留原因与禁用上传写入的保证。

## AC-005 品牌 Logo 展示无回归

**Given** 存在 `logo_object_key` 的品牌记录  
**When** 访问 `/admin/brands` 列表与编辑弹窗  
**Then** Logo MUST 正常展示与回显。  
**And** 清理 uploads 残留后 MUST NOT 出现 404 或布局异常。

## AC-006 可选一致性检查工具

**Given** 修复提供 `scripts/` 下检查或清理工具（若 tasks 要求）  
**When** 在含 legacy uploads 的环境执行  
**Then** 工具 MUST 能列出 uploads 孤儿文件或报告「无残留」。  
**And** 工具 MUST NOT 默认删除 MinIO 或 DB 引用的有效对象。

## AC-007 测试与 CI

**Given** 修复涉及配置或脚本变更  
**When** 运行后端相关测试  
**Then** 现有媒体上传与 `/media` 测试 MUST 全部通过。  
**And** 若新增清理/校验脚本，MUST 有对应单元测试或文档化手动验证步骤。
