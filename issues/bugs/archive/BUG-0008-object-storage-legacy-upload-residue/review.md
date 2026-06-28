---
bug_id: BUG-0008-object-storage-legacy-upload-residue
review_id: REV-BUG-0008-001
status: approved
reviewed_at: 2026-06-26 23:56:09
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0008-object-storage-legacy-upload-residue` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0008-object-storage-legacy-upload-residue
```

建议创建修复 Change：

```text
fix-object-storage-legacy-upload-residue
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 给出双目录对比复现路径；`root-cause.md` 定位 BUG-0006 修复缺 post-migration cleanup、`UPLOAD_DIR` 挂载未收敛；本地实测 uploads 下 6 个品牌 Logo 孤儿文件与 DB 无关联。 |
| 严重等级合理 | 通过 | 技术债/运维清理，不影响当前上传与展示；`medium` 合理，不应定为 `high` 或 hotfix。 |
| 回归验收明确 | 通过 | `acceptance.md` 覆盖孤儿清理、新上传不写 uploads、文档澄清、配置收敛、Logo 无回归、可选校验工具与测试。 |
| 是否需 hotfix 路径 | 不需要 | 无功能阻断；`workaround.md` 提供手动清理与认知规避；适合常规 `fix-*` OpenSpec Change。 |

## 3. 批准理由

1. BUG-0006 修复后双目录并存已造成开发/运维认知混淆，且 `data/uploads` 存在可证实的孤儿文件，属于应收敛的迁移收尾项。
2. 根因明确为存储迁移缺少清理门禁与文档澄清，而非新的上传或读取缺陷。
3. 临时规避方案与回归 AC 已定义安全边界（以 DB + MinIO 为准，清理不得影响有效引用）。
4. 修复面清晰：清理脚本/步骤、文档更新、Docker 与 `UPLOAD_DIR` 配置收敛，可通过 OpenSpec 管理影响范围。

## 4. 后续要求

1. 创建 `fix-object-storage-legacy-upload-residue` 时，MUST 包含历史 uploads 清理策略，且 MUST NOT 删除 MinIO 中仍被 DB 引用的对象。
2. 评估移除 `docker-compose.yml` 中 `./data/uploads` 挂载前，MUST 确认 `settings.upload_dir` 无业务代码依赖（当前上传链路已不写入）。
3. MUST 更新 `data/README.md`，澄清 `data/minio` 为 MinIO 持久化卷、`data/uploads` 非正式业务存储。
4. 修复后 MUST 回归 BUG-0006/BUG-0007 媒体上传与品牌 Logo 展示，确保无功能回退。
5. 可选提供 `scripts/` 一致性检查工具，便于本地与 CI 发现 future 残留。
