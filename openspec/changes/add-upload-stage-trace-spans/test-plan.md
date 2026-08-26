---
change_id: add-upload-stage-trace-spans
source_requirement: REQ-0123-upload-stage-trace-spans
sprint: sprint-026
created_at: 2026-08-25 18:58:00
updated_at: 2026-08-25 18:58:00
---

# 测试计划

## 聚焦测试

- 后端头像上传成功路径：断言 Task Trace spans 至少包含 `file_read` 与 `original_put_object`，并验证耗时和状态字段存在。
- 后端通用图片上传成功路径：断言六个基础阶段完整出现，顺序归属同一次 trace。
- 对象存储写入失败：模拟 `put_object` 抛错，断言失败阶段为 `failed`，已完成阶段仍保留。
- 派生图生成失败或跳过：断言 `thumbnail_generate` / `display_generate` 的失败或跳过语义可追踪。
- 脱敏检查：断言 span error metadata 不包含密钥、Authorization、Cookie、本机绝对路径或完整堆栈。

## 回归命令

- `uv run pytest` 聚焦后端媒体上传与头像上传相关测试。
- `openspec validate add-upload-stage-trace-spans --strict`。
- `python scripts/validate-directory-structure.py`。
- `python scripts/sync-workflow-status.py --event req.opsx --req REQ-0123-upload-stage-trace-spans --change add-upload-stage-trace-spans --sprint auto`。
