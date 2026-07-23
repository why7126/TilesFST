---
bug_id: BUG-0073-video-upload-23m-file-fails
status: done
created_at: 2026-07-21 15:01:07
updated_at: 2026-07-22 09:20:59
reviewed_at: 2026-07-21 15:01:07
review_result: approved
reviewer: AI
severity: high
related_requirement:
related_change: fix-upload-size-limit-consistency
---

# Review - BUG-0073 上传 23M 文件失败，图片、视频和文档均受影响

## 评审结论

批准修复。

该缺陷影响公共上传链路，已确认图片与证书 / PDF 类文件默认存在 20MB 限制，约 23M 文件会失败；视频 23M 在默认配置下理论应可上传，因此仍需在修复阶段复核具体入口、生产代理、对象存储和 MIME Type。根因分析充分，严重等级合理，回归验收覆盖图片、视频、文档、错误提示、对象存储安全和部署配置一致性。

## 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 图片默认 20MB，证书 / PDF 硬编码 20MB；视频失败有明确待排查触发条件 |
| 严重等级合理 | 通过 | 上传是媒体资料维护核心链路，且影响图片、视频、文档等多类型文件，`high` 合理 |
| 回归验收明确 | 通过 | `acceptance.md` 已覆盖约 23M 边界、超限、类型不支持、对象存储、代理配置和测试要求 |
| 是否需 hotfix 路径 | 不需要 | 暂无数据损坏、权限绕过或系统不可用；建议进入常规 BUG 修复流程 |

## 修复门禁

- 状态批准后允许执行 `/bug-opsx BUG-0073-video-upload-23m-file-fails`。
- 状态批准后允许纳入 Sprint 规划。
- 来源于该 BUG 的 OpenSpec Change 在 `/opsx-apply` 前仍必须先纳入正式 Sprint 范围。

## 评审备注

修复前必须先明确产品层面的图片、视频、文档大小上限。若修复涉及新增文件类大小配置、统一错误响应或上传限制查询接口，需要同步 `.env.example`、系统设置、OpenAPI、Orval、接口文档和测试。修复不得绕过后端鉴权、MIME Type 校验、扩展名校验、对象 Key 安全校验或 MinIO / S3 兼容对象存储适配层。
