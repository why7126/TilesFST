---
bug_id: BUG-0020-tile-sku-modal-video-upload-413
review_id: REV-BUG-0020-001
status: approved
reviewed_at: 2026-06-27 15:27:53
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0020-tile-sku-modal-video-upload-413` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0020-tile-sku-modal-video-upload-413
```

建议修复 Change：

```text
fix-tile-sku-modal-video-upload-413
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户已提供 `localhost:3000` + 413 Network 证据；`root-cause.md` 明确 Nginx 默认 ~1MB `client_max_body_size` 与 env 配置未对齐；对照直连 `8000` 可区分代理层与后端。 |
| 严重等级合理 | 通过 | Docker 演示路径下典型 MP4 无法上传，阻塞 REQ-0006 AC-035 端到端验收；`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-008 覆盖 Docker 大文件非 413、四类 env 可配置、Nginx 对齐、测试与 Change 记录；scope 与 BUG-0018 边界清晰。 |
| 是否需 hotfix 路径 | 不需要 | 修复面以 Nginx + 后端配置为主，变更集中、风险低，可走常规 `fix-*` Change；虽可快速合入，但不属安全/登录类 hotfix 强制路径。 |

## 3. 批准理由

1. 需求归属清晰：关联 `REQ-0006-tile-sku-management`，为部署/配置缺陷而非新需求。
2. 根因与修复方向明确：`nginx.conf` body 限制 + `MAX_IMAGE/VIDEO_SIZE_MB` 与 `ALLOWED_*_TYPES` env 落地；不涉及数据库 schema 变更。
3. 与 BUG-0018 分层明确：0020 为上传请求失败（413），0018 为上传成功后的 UI 回显；须分别修复。
4. 无可靠产品级 workaround，Docker `localhost:3000` 路径不得先行通过 AC-035 验收。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-tile-sku-modal-video-upload-413`，delta spec 引用 REQ-0006 AC-035 可上传性与 BUG acceptance AC-001～AC-008。
2. `client_max_body_size` MUST ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`；文档说明调大 env 时须同步 Nginx。
3. 修改 `nginx.conf` 后验收 MUST **重建 Web 镜像**，非仅重启 backend。
4. 补充后端测试（超限、MIME 白名单 env）后再 `/opsx-archive`。
5. 前端 413 友好提示可作为可选增强，不扩大本 Change 必选项。
