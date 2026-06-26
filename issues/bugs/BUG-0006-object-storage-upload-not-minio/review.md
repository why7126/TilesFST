---
bug_id: BUG-0006-object-storage-upload-not-minio
review_id: REV-BUG-0006-001
status: approved
reviewed_at: 2026-06-26 11:35:04
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0006-object-storage-upload-not-minio` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0006-object-storage-upload-not-minio
```

建议创建修复 Change：

```text
fix-object-storage-upload-not-minio
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 已给出 Docker Compose + MinIO Console 复现路径；`root-cause.md` 已定位到上传保存函数写入 `UPLOAD_DIR` 本地路径，未调用 MinIO client。 |
| 严重等级合理 | 通过 | 缺陷影响品牌 Logo、SKU 图片、SKU 视频、头像等媒体上传的对象存储一致性，且违反 MinIO 单桶存储规范；`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖 MinIO 单桶写入、标准对象前缀、后端授权校验、媒体读取、Docker Compose 验证、测试与文档同步要求。 |
| 是否需 hotfix 路径 | 不需要 | 当前上传和本地 `/media` 回显可能仍可用，未确认造成生产 blocker/critical；适合通过 `fix-*` OpenSpec Change 修复。 |

## 3. 批准理由

1. MinIO 服务和桶初始化已存在，但业务上传链路未写入对象存储，属于后端媒体存储适配层缺陷。
2. 缺陷覆盖多个上传入口，影响对象存储验收、Docker 演示环境和后续小程序/外部媒体访问策略。
3. 根因、临时规避方案和回归验收标准已经补齐，具备进入 `/bug-opsx` 的条件。
4. 修复会改变上传持久化与媒体读取策略，需要通过 OpenSpec Change 管理接口、测试、文档和部署影响。

## 4. 后续要求

1. 创建 `fix-*` OpenSpec Change 时，必须覆盖 MinIO 存储适配层、`put_object` 写入、受控读取或签名 URL 策略。
2. 修复必须继续遵守一个项目一个 Bucket、标准对象前缀和后端授权上传要求。
3. 修复阶段必须补充后端测试，验证上传后对象写入 MinIO，而不是仅验证本地 `/media` 可读。
4. 如调整上传响应 URL、错误码、环境变量或媒体元数据字段，必须同步 OpenAPI、Orval、`.env.example`、部署文档和数据库说明。
