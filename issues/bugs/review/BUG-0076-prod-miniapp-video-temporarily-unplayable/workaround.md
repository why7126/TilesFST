---
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
status: approved
created_at: 2026-07-21 15:21:40
updated_at: 2026-07-21 15:24:31
workaround_available: true
related_requirement:
related_change: fix-prod-miniapp-video-upstream-502
---

# Workaround - BUG-0076 生产环境微信小程序提示视频暂时无法播放

## 临时规避方案

当前可用的临时规避重点是先恢复生产域名到 Web/Backend 的访问链路：

1. 在生产服务器检查外层 Nginx upstream 配置，确认域名 `tilesfst.wjoyhappy.site` 指向正确的 Web 容器宿主端口。
2. 检查 Docker 服务状态：`tilesfst-web`、`tilesfst-backend`、MinIO/COS 依赖与数据库连接是否正常。
3. 若容器未运行或健康异常，按生产运维流程重启对应服务，并观察后端启动日志。
4. 恢复后先验证 `https://tilesfst.wjoyhappy.site/api/v1/health` 返回 200，再验证小程序实际 SKU 接口与 `/media/...` 视频 URL。
5. 若仅个别视频仍失败，可临时下架或替换对应视频素材，保留图片媒体展示，避免用户持续看到不可播放视频项。

## 不建议的规避

- 不建议让小程序直连 MinIO/COS 未授权地址。
- 不建议在小程序端硬编码视频 URL 或绕过后端 `/media/{object_key}` 受控读取链路。
- 不建议为了规避播放失败而关闭所有视频错误提示；这会降低可诊断性。
- 不建议在未确认生产容器状态前直接修改小程序播放器逻辑。

## 运维排查清单

| 检查项 | 期望 |
|---|---|
| 外层 Nginx 根路径 | 不再返回 502 |
| `/api/v1/health` | 返回 200 与健康响应 |
| Web 容器 | 运行中，宿主端口与外层 Nginx upstream 一致 |
| Backend 容器 | 运行中，容器内 `8000` 可访问 |
| `/api/v1/miniapp/skus/<SKU ID>` | 返回 200，`media[].url` 中视频 URL 有效 |
| `/media/<object_key>` | 返回 200，`Content-Type` 为小程序可播放视频类型 |
| 对象存储 | 对象存在，后端读取无权限或连接错误 |

## 回滚策略

若生产服务恢复过程中发现最近发布镜像导致后端启动失败，可按发布流程回滚到上一版可启动镜像；回滚后仍需确认 `BUG-0069` 的视频 URL 修复是否保留，否则可能出现旧的 `file_name` URL 回归。
